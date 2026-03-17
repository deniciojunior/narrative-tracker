"""
scorer.py — Calcula divergência narrativa por fonte por dia.

Usa distância de Bhattacharyya entre a distribuição de frames de cada
fonte e a distribuição global do mesmo dia.
Score 0 = idêntico à média global. Score 100 = completamente oposto.
"""

import json
import math
import os
import re
import sqlite3
from collections import defaultdict

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "articles.db")

STOPWORDS = {
    "the","a","an","in","on","at","to","of","and","or",
    "is","are","was","were","has","have","had","it","its","for","with",
    "that","this","as","by","be","from","said","will","after","but",
    "not","he","she","they","we","us","their","also","over","into",
    "iran","israel","war","says","says","amid","new","says","report",
}

FRAMES = [
    "humanitarian", "military", "geopolitical",
    "terrorism", "resistance", "nuclear", "diplomatic",
]


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_tables(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS divergence_scores (
            source          TEXT,
            date            TEXT,
            score           REAL,
            dominant_frame  TEXT,
            article_count   INTEGER,
            PRIMARY KEY (source, date)
        );

        CREATE TABLE IF NOT EXISTS vocabulary_by_source (
            source  TEXT,
            date    TEXT,
            word    TEXT,
            count   INTEGER,
            PRIMARY KEY (source, date, word)
        );
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Matemática
# ---------------------------------------------------------------------------

def normalize_dist(counts: dict) -> dict:
    """Normaliza contagens para probabilidades. Fallback uniforme se vazio."""
    total = sum(counts.values())
    if total == 0:
        return {f: 1.0 / len(FRAMES) for f in FRAMES}
    return {f: counts.get(f, 0) / total for f in FRAMES}


def bhattacharyya_score(dist_source: dict, dist_global: dict) -> float:
    """
    Coeficiente de Bhattacharyya BC = sum(sqrt(p_i * q_i)).
    Score = (1 - BC) * 100  →  0 = idêntico, 100 = completamente divergente.
    """
    bc = sum(
        math.sqrt(dist_source.get(f, 0.0) * dist_global.get(f, 0.0))
        for f in FRAMES
    )
    bc = max(0.0, min(1.0, bc))
    return round((1.0 - bc) * 100, 2)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def calculate_scores():
    conn = get_db()
    ensure_tables(conn)

    # Busca todos os artigos analisados com data e fonte
    rows = conn.execute("""
        SELECT
            a.source,
            substr(a.published_at, 1, 10) AS date,
            an.frame,
            an.vocabulary
        FROM articles a
        JOIN analyses an ON a.id = an.article_id
        WHERE a.published_at IS NOT NULL
          AND a.source IS NOT NULL
          AND length(a.published_at) >= 10
    """).fetchall()

    if not rows:
        print("Nenhum dado para calcular scores.")
        print("Execute collector.py e analyzer.py primeiro.")
        conn.close()
        return

    # Estruturas de agregação
    # date -> source -> frame -> count
    date_source_frames: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    # date -> frame -> count  (global)
    date_global_frames: dict = defaultdict(lambda: defaultdict(int))
    # date -> source -> word -> count
    date_source_vocab: dict  = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for row in rows:
        source    = row["source"]
        date      = row["date"]
        frame     = row["frame"]
        vocab_raw = row["vocabulary"] or "[]"

        if not date or len(date) < 10:
            continue

        date_source_frames[date][source][frame] += 1
        # NÃO acumula date_global_frames aqui — calculamos depois como média igualmente
        # ponderada por fonte (evita distorção quando uma fonte domina o corpus)

        try:
            words = json.loads(vocab_raw)
            for w in words:
                w = str(w).strip().lower()
                if w and len(w) > 2:
                    date_source_vocab[date][source][w] += 1
        except (json.JSONDecodeError, TypeError, AttributeError):
            pass

    # Limpa tabelas e recalcula do zero
    conn.execute("DELETE FROM divergence_scores")
    conn.execute("DELETE FROM vocabulary_by_source")

    sources_processed: set = set()
    dates_processed:   set = set()
    all_scores: dict       = defaultdict(list)

    for date in sorted(date_source_frames):
        # Média igualmente ponderada: 1 voto por fonte, independente de volume de artigos.
        # Evita que RT (63% do corpus) distorça o "global mean" para o seu próprio framing.
        sources_on_date = list(date_source_frames[date].keys())
        n_src = len(sources_on_date)
        avg_dist: dict = {f: 0.0 for f in FRAMES}
        for src in sources_on_date:
            d = normalize_dist(dict(date_source_frames[date][src]))
            for f in FRAMES:
                avg_dist[f] += d[f]
        dist_global = {f: avg_dist[f] / n_src for f in FRAMES}
        dates_processed.add(date)

        for source, source_counts in date_source_frames[date].items():
            dist_source    = normalize_dist(dict(source_counts))
            score          = bhattacharyya_score(dist_source, dist_global)
            dominant_frame = max(source_counts, key=source_counts.get)
            article_count  = sum(source_counts.values())

            conn.execute(
                """
                INSERT OR REPLACE INTO divergence_scores
                    (source, date, score, dominant_frame, article_count)
                VALUES (?, ?, ?, ?, ?)
                """,
                (source, date, score, dominant_frame, article_count),
            )
            sources_processed.add(source)
            all_scores[source].append(score)

        # Vocabulário: top 50 palavras por (source, date)
        for source, word_counts in date_source_vocab[date].items():
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]
            for word, count in top_words:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO vocabulary_by_source
                        (source, date, word, count)
                    VALUES (?, ?, ?, ?)
                    """,
                    (source, date, word, count),
                )

    conn.commit()

    # Relatório
    n_sources = len(sources_processed)
    n_days    = len(dates_processed)
    print(f"Scores calculados para {n_sources} fontes em {n_days} dias")

    if all_scores:
        avg_scores  = {s: sum(v) / len(v) for s, v in all_scores.items()}
        most_div    = max(avg_scores, key=avg_scores.get)
        least_div   = min(avg_scores, key=avg_scores.get)
        print(f"Fonte mais divergente: {most_div} (media {avg_scores[most_div]:.1f})")
        print(f"Fonte mais neutra:     {least_div} (media {avg_scores[least_div]:.1f})")

    n_groups = extract_vocabulary_tfidf(conn)
    print(f"TF-IDF calculado para {n_groups} grupos (source × dia)")

    conn.close()


# ---------------------------------------------------------------------------
# TF-IDF sobre títulos + leads
# ---------------------------------------------------------------------------

def extract_vocabulary_tfidf(conn: sqlite3.Connection) -> int:
    """
    Calcula TF-IDF sobre títulos+leads de cada (source, date).
    Substitui todo o conteúdo de vocabulary_by_source.
    Retorna número de grupos processados.
    """
    rows = conn.execute("""
        SELECT a.source,
               substr(a.published_at, 1, 10) AS date,
               a.title,
               a.lead
        FROM articles a
        WHERE a.analyzed = 1
          AND a.source IS NOT NULL
          AND length(a.published_at) >= 10
    """).fetchall()

    if not rows:
        return 0

    # (source, date) → lista de textos
    groups: dict = defaultdict(list)
    for r in rows:
        text = " ".join(filter(None, [r["title"] or "", r["lead"] or ""]))
        groups[(r["source"], r["date"])].append(text)

    total_groups = len(groups)

    # Tokeniza e conta por grupo
    group_counts: dict = {}
    for key, texts in groups.items():
        full = " ".join(texts).lower()
        words = re.findall(r"\b[a-z]{4,}\b", full)
        counts: dict = defaultdict(int)
        for w in words:
            if w not in STOPWORDS:
                counts[w] += 1
        group_counts[key] = dict(counts)

    # IDF: quantos grupos contêm cada palavra
    doc_freq: dict = defaultdict(int)
    for wc in group_counts.values():
        for w in wc:
            doc_freq[w] += 1

    # TF-IDF top-15 por grupo → vocabulary_by_source
    conn.execute("DELETE FROM vocabulary_by_source")
    n_inserted = 0

    for (source, date), word_counts in group_counts.items():
        total_words = sum(word_counts.values())
        if total_words == 0:
            continue

        tfidf: dict = {}
        for word, cnt in word_counts.items():
            tf  = cnt / total_words
            idf = math.log(total_groups / (doc_freq[word] + 1) + 1)
            tfidf[word] = tf * idf

        top = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:15]
        for word, score in top:
            conn.execute(
                "INSERT OR REPLACE INTO vocabulary_by_source (source, date, word, count) VALUES (?, ?, ?, ?)",
                (source, date, word, max(1, int(score * 10_000))),
            )
            n_inserted += 1

    conn.commit()
    return total_groups


if __name__ == "__main__":
    calculate_scores()
