"""
analyzer.py — Analisa artigos com Claude Haiku e armazena frames no banco.

Auth (ordem de prioridade):
  1. ANTHROPIC_API_KEY no .env  → SDK direto
  2. CLAUDE_CODE_OAUTH_TOKEN    → subprocess claude.exe (conta Pro/Max no Claude Code)
"""

import json
import os
import subprocess
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "articles.db")
MODEL   = "claude-haiku-4-5-20251001"
BATCH_SIZE  = 10
MAX_WORKERS_SDK = 8   # SDK suporta mais paralelismo
MAX_WORKERS_SUB = 1   # subprocess: serial evita timeout/conflitos no claude.exe
MAX_TOKENS  = 200

# Preços por token (USD) — Haiku
PRICE_INPUT  = 0.00000025   # $0.25 / 1M tokens
PRICE_OUTPUT = 0.00000125   # $1.25 / 1M tokens

# Caminho do claude CLI embutido no Claude Desktop
_CLAUDE_BIN_DEFAULT = (
    Path.home() / "AppData/Roaming/Claude/claude-code/2.1.72/claude.exe"
)

SYSTEM_PROMPT = """\
You are a media framing analyst. Analyze how the article's title and lead \
frame the US-Israel-Iran war (started Feb 28, 2026).
Return ONLY valid JSON, no explanation, no markdown."""

USER_TEMPLATE = """\
Source: {source}
Title: {title}
Lead: {lead}

Return JSON:
{{
  "frame": one of ["humanitarian","military","geopolitical","terrorism","resistance","nuclear","diplomatic"],
  "vocabulary": [5 words or short phrases that reveal the frame],
  "victim_actor": "who is presented as the victim (one entity name or null)",
  "tone": one of ["neutral","alarmist","technical","emotional","propagandistic"]
}}"""

VALID_FRAMES = {"humanitarian", "military", "geopolitical", "terrorism",
                "resistance", "nuclear", "diplomatic", "unclassified"}
VALID_TONES  = {"neutral", "alarmist", "technical", "emotional", "propagandistic", "unknown"}

# Strings que indicam recusa por knowledge cutoff / identidade errada
REFUSAL_STRINGS = [
    "knowledge cutoff", "training data", "cannot", "don't have information",
    "hypothetical", "fictional", "not aware", "i'm claude code",
    "claude code", "software engineering", "i need to clarify",
    "i appreciate", "my knowledge", "i have concerns",
]

SYSTEM_PROMPT_RETRY = """\
You are a media framing classifier. Classify the WRITING STYLE and WORD CHOICE \
of this headline. Do not evaluate whether the events are real or fictional. \
Focus only on linguistic analysis: what frame does this text use? What tone?
Return ONLY valid JSON, no explanation."""


# ---------------------------------------------------------------------------
# Backend de chamada à API
# ---------------------------------------------------------------------------

def _detect_backend() -> str:
    """Retorna 'sdk' ou 'subprocess'."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "sdk"
    if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        return "subprocess"
    raise RuntimeError(
        "Nenhuma credencial encontrada.\n"
        "  • Defina ANTHROPIC_API_KEY no .env, ou\n"
        "  • Execute dentro do Claude Code (injeta CLAUDE_CODE_OAUTH_TOKEN)."
    )


BACKEND = _detect_backend()

if BACKEND == "sdk":
    import anthropic as _anthropic
    _sdk_client = _anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print(f"Auth: SDK direto (ANTHROPIC_API_KEY)")
else:
    _sdk_client = None
    # encontra o claude.exe (permite override via env CLAUDE_BIN)
    _CLAUDE_BIN = os.environ.get("CLAUDE_BIN", str(_CLAUDE_BIN_DEFAULT))
    if not Path(_CLAUDE_BIN).exists():
        raise RuntimeError(
            f"claude.exe não encontrado em {_CLAUDE_BIN}.\n"
            "Defina a variável CLAUDE_BIN com o caminho correto."
        )
    # Ambiente para o subprocess: remove CLAUDECODE para evitar bloqueio
    _SUBPROCESS_ENV = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    print(f"Auth: subprocess via claude CLI ({Path(_CLAUDE_BIN).name})")


def _call_sdk(prompt_full: str, system: str = SYSTEM_PROMPT) -> tuple[str, int, int]:
    """Chama a API via SDK; retorna (texto, in_tokens, out_tokens)."""
    resp = _sdk_client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": prompt_full}],
    )
    return resp.content[0].text.strip(), resp.usage.input_tokens, resp.usage.output_tokens


def _call_subprocess(prompt_full: str, system: str = SYSTEM_PROMPT) -> tuple[str, int, int]:
    """Chama o claude CLI como subprocess; retorna (texto, in_tokens_est, out_tokens_est)."""
    full_prompt = f"[SYSTEM]\n{system}\n\n[USER]\n{prompt_full}"
    result = subprocess.run(
        [_CLAUDE_BIN, "-p", full_prompt,
         "--model", MODEL,
         "--output-format", "text"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=_SUBPROCESS_ENV, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI error: {result.stderr[:200]}")
    text = result.stdout.strip()
    # Estimativa de tokens (sem acesso à contagem real via subprocess)
    in_est  = max(1, len(full_prompt) // 4)
    out_est = max(1, len(text) // 4)
    return text, in_est, out_est


def call_model(prompt_full: str, system: str = SYSTEM_PROMPT) -> tuple[str, int, int]:
    if BACKEND == "sdk":
        return _call_sdk(prompt_full, system)
    return _call_subprocess(prompt_full, system)


def _is_refusal(text: str) -> bool:
    t = text.lower()
    return any(s in t for s in REFUSAL_STRINGS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_unanalyzed(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT id, source, title, lead FROM articles WHERE analyzed = 0"
    ).fetchall()
    return [dict(r) for r in rows]


def format_cost(usd: float) -> str:
    return f"${usd:.4f}"


def eta_str(remaining: int, elapsed_s: float, done: int) -> str:
    if done == 0:
        return "?"
    rate = done / elapsed_s
    secs = remaining / rate
    return f"~{int(secs // 60)}min restantes"


# ---------------------------------------------------------------------------
# Análise individual
# ---------------------------------------------------------------------------

def analyze_article(article: dict) -> tuple[dict, int, int]:
    """
    Retorna (result_dict, input_tokens, output_tokens).
    result_dict vazio em caso de falha.
    """
    user_msg = USER_TEMPLATE.format(
        source=article["source"] or "",
        title=article["title"] or "",
        lead=article["lead"] or "",
    )

    raw_text, in_tok, out_tok = "", 0, 0
    parsed = None

    systems_to_try = [SYSTEM_PROMPT, SYSTEM_PROMPT_RETRY]

    for attempt, system in enumerate(systems_to_try, start=1):
        try:
            raw_text, it, ot = call_model(user_msg, system)
            in_tok += it
            out_tok += ot

            # Se o modelo recusou por knowledge cutoff, tenta com prompt neutro
            if _is_refusal(raw_text):
                if attempt < len(systems_to_try):
                    continue
                # Esgotou retries — marca como unclassified
                return {
                    "article_id":   article["id"],
                    "frame":        "unclassified",
                    "vocabulary":   "[]",
                    "victim_actor": None,
                    "tone":         "unknown",
                    "analyzed_at":  datetime.now(timezone.utc).isoformat(),
                }, in_tok, out_tok

            # Extrai JSON mesmo se vier envolto em markdown
            text = raw_text
            if "```" in text:
                text = text.split("```")[-2].strip()
                if text.startswith("json"):
                    text = text[4:].strip()
            parsed = json.loads(text)
            break

        except json.JSONDecodeError:
            if attempt < len(systems_to_try):
                continue
            print(f"  [SKIP] JSON inválido id={article['id'][:12]}… raw={raw_text[:80]}")
            return {}, in_tok, out_tok
        except Exception as e:
            print(f"  [ERRO] {e} — id={article['id'][:12]}…")
            return {}, in_tok, out_tok

    if parsed is None:
        return {}, in_tok, out_tok

    frame = parsed.get("frame", "geopolitical")
    if frame not in VALID_FRAMES:
        frame = "geopolitical"

    tone = parsed.get("tone", "neutral")
    if tone not in VALID_TONES:
        tone = "neutral"

    vocab = parsed.get("vocabulary", [])
    if not isinstance(vocab, list):
        vocab = []

    return {
        "article_id": article["id"],
        "frame": frame,
        "vocabulary": json.dumps(vocab[:5]),
        "victim_actor": parsed.get("victim_actor"),
        "tone": tone,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }, in_tok, out_tok


# ---------------------------------------------------------------------------
# Commit em lote
# ---------------------------------------------------------------------------

def commit_batch(conn: sqlite3.Connection, results: list[dict]):
    for r in results:
        if not r:
            continue
        conn.execute(
            """
            INSERT OR REPLACE INTO analyses
                (article_id, frame, vocabulary, victim_actor, tone, analyzed_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (r["article_id"], r["frame"], r["vocabulary"],
             r["victim_actor"], r["tone"], r["analyzed_at"]),
        )
        conn.execute(
            "UPDATE articles SET analyzed = 1 WHERE id = ?",
            (r["article_id"],),
        )
    conn.commit()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze():
    conn = get_db()
    articles = fetch_unanalyzed(conn)
    total = len(articles)

    if total == 0:
        print("Nenhum artigo para analisar (todos já foram processados).")
        conn.close()
        return

    print(f"Analisando {total} artigos com {MODEL} via {BACKEND}...")
    done = 0
    total_in_tok  = 0
    total_out_tok = 0
    start_time = time.time()

    for batch_start in range(0, total, BATCH_SIZE):
        batch = articles[batch_start: batch_start + BATCH_SIZE]
        batch_results: list[dict] = []

        n_workers = MAX_WORKERS_SDK if BACKEND == "sdk" else MAX_WORKERS_SUB
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {executor.submit(analyze_article, art): art for art in batch}
            for future in as_completed(futures):
                result, in_tok, out_tok = future.result()
                total_in_tok  += in_tok
                total_out_tok += out_tok
                if result:
                    batch_results.append(result)

        commit_batch(conn, batch_results)
        done += len(batch)
        cost    = (total_in_tok * PRICE_INPUT) + (total_out_tok * PRICE_OUTPUT)
        elapsed = time.time() - start_time
        note    = " (estimado)" if BACKEND == "subprocess" else ""
        print(
            f"Analisados: {done}/{total} | "
            f"Custo{note}: {format_cost(cost)} | "
            f"{eta_str(total - done, elapsed, done)}"
        )

    # Relatório final
    cost = (total_in_tok * PRICE_INPUT) + (total_out_tok * PRICE_OUTPUT)
    note = " (estimado)" if BACKEND == "subprocess" else ""
    print()
    print(f"Análise concluída: {done} artigos | Custo total{note}: {format_cost(cost)}")

    rows = conn.execute(
        "SELECT frame, COUNT(*) cnt FROM analyses GROUP BY frame ORDER BY cnt DESC"
    ).fetchall()
    if rows:
        tot = sum(r["cnt"] for r in rows)
        print("Distribuição de frames: " +
              " | ".join(f"{r['frame']}={r['cnt']/tot:.0%}" for r in rows))

    rows_t = conn.execute(
        "SELECT tone, COUNT(*) cnt FROM analyses GROUP BY tone ORDER BY cnt DESC"
    ).fetchall()
    if rows_t:
        tot = sum(r["cnt"] for r in rows_t)
        print("Distribuição de tons:   " +
              " | ".join(f"{r['tone']}={r['cnt']/tot:.0%}" for r in rows_t))

    unclassified = conn.execute(
        "SELECT COUNT(*) FROM analyses WHERE frame='unclassified'"
    ).fetchone()[0]
    print(f"Unclassified (retry falhou): {unclassified}")

    conn.close()


if __name__ == "__main__":
    analyze()
