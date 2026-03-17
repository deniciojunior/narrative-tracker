"""
app.py — Dashboard Flask para o Narrative Tracker.
"""

import json
import os
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, g, jsonify, render_template, request

load_dotenv()

# ---------------------------------------------------------------------------
# Claude helper — SDK (preferred) ou subprocess fallback
# ---------------------------------------------------------------------------
_ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
_CLAUDE_BIN = os.environ.get(
    "CLAUDE_BIN",
    str(Path.home() / "AppData/Roaming/Claude/claude-code/2.1.72/claude.exe"),
)
_SUBPROCESS_ENV = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

if _ANTHROPIC_KEY:
    import anthropic as _anthropic
    _sdk_client = _anthropic.Anthropic(api_key=_ANTHROPIC_KEY)
else:
    _sdk_client = None


def _call_claude(prompt: str) -> str:
    """Call Claude Haiku. Uses SDK if ANTHROPIC_API_KEY set, else subprocess."""
    if _sdk_client:
        resp = _sdk_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=80,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()

    # Subprocess fallback (requires running inside Claude Code)
    result = subprocess.run(
        [_CLAUDE_BIN, "-p", prompt, "--model", "claude-haiku-4-5-20251001",
         "--output-format", "text"],
        capture_output=True, text=True, timeout=30, env=_SUBPROCESS_ENV,
    )
    out = (result.stdout or "").strip()
    if not out or "not logged in" in out.lower() or "please re" in out.lower():
        raise RuntimeError(f"Claude CLI auth failed: {out[:120]}")
    return out

DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(os.path.dirname(__file__), "..", "articles.db")
)

# ---------------------------------------------------------------------------
# Seed database from committed snapshot on first deploy
# ---------------------------------------------------------------------------
import shutil as _shutil
_HERE = os.path.dirname(os.path.abspath(__file__))
_SEED_PATH = os.path.join(_HERE, "..", "seed.db")
_DB_ABS = os.path.abspath(DB_PATH)
print(f"[seed] DB_PATH={_DB_ABS}  seed={_SEED_PATH}  db_exists={os.path.exists(_DB_ABS)}  seed_exists={os.path.exists(_SEED_PATH)}", flush=True)
if not os.path.exists(_DB_ABS) and os.path.exists(_SEED_PATH):
    try:
        _db_dir = os.path.dirname(_DB_ABS)
        if _db_dir:
            os.makedirs(_db_dir, exist_ok=True)
        _shutil.copy(_SEED_PATH, _DB_ABS)
        print(f"[seed] OK — copied seed.db → {_DB_ABS}", flush=True)
    except Exception as _e:
        print(f"[seed] FAILED — {_e} — falling back to default path", flush=True)
        DB_PATH = os.path.join(_HERE, "..", "articles.db")
        _DB_ABS = os.path.abspath(DB_PATH)
        _shutil.copy(_SEED_PATH, _DB_ABS)
        print(f"[seed] fallback OK — copied seed.db → {_DB_ABS}", flush=True)

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

EVENTS = {
    "2026-02-28": "EUA e Israel atacam Ira — Khamenei morto",
    "2026-03-02": "Hezbollah entra no conflito",
    "2026-03-06": "Ira fecha Estreito de Ormuz",
    "2026-03-11": "12 dia — sem cessar-fogo",
}

SOURCE_COLORS = {
    # Ocidente mainstream
    "Al Jazeera":      "#E8593C",
    "BBC":             "#1D4E8F",
    "Reuters":         "#FF8000",
    "NYT":             "#CCCCCC",
    "AP News":         "#9B59B6",
    "The Guardian":    "#052962",
    "France 24":       "#003D7C",
    "DW":              "#C0392B",
    # Direita ocidental
    "Fox News":        "#003DA5",
    "NY Post":         "#E74C3C",
    "The Times":       "#8B0000",
    "The Telegraph":   "#1A1A1A",
    # Israel
    "Haaretz":         "#0057B7",
    "Times of Israel": "#4A90D9",
    "Jerusalem Post":  "#2E86AB",
    # Eixo oposto
    "RT":              "#CC0000",
    "TASS":            "#8B1A1A",
    "Sputnik":         "#A93226",
    "Xinhua":          "#DE2910",
    "Global Times":    "#C0392B",
    "Press TV":        "#27AE60",
    "IRNA":            "#1E8449",
    # Árabe / Regional
    "Arab News":       "#006400",
    "Middle East Eye": "#D4AC0D",
    "Al-Monitor":      "#E67E22",
}

FRAME_COLORS = {
    "humanitarian": "#1D9E75",
    "military":     "#D85A30",
    "geopolitical": "#534AB7",
    "terrorism":    "#C04828",
    "resistance":   "#854F0B",
    "nuclear":      "#185FA5",
    "diplomatic":   "#888780",
}

FRAMES = list(FRAME_COLORS.keys())


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db:
        db.close()


def cutoff_date(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template(
        "index.html",
        source_colors=SOURCE_COLORS,
        frame_colors=FRAME_COLORS,
    )


@app.route("/api/stats")
def api_stats():
    db      = get_db()
    today   = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yest    = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

    total = db.execute(
        "SELECT COUNT(*) FROM articles WHERE analyzed = 1"
    ).fetchone()[0]

    sources = db.execute(
        "SELECT COUNT(DISTINCT source) FROM articles WHERE source IS NOT NULL"
    ).fetchone()[0]

    period = db.execute(
        "SELECT MIN(substr(published_at,1,10)), MAX(substr(published_at,1,10)) FROM articles"
    ).fetchone()

    # Fallback: hoje → ontem → última data disponível
    div_val, div_label = None, "recente"
    for check_date, label in [(today, "hoje"), (yest, "ontem")]:
        val = db.execute(
            "SELECT AVG(score) FROM divergence_scores WHERE date = ?", (check_date,)
        ).fetchone()[0]
        if val is not None:
            div_val   = round(val, 1)
            div_label = label
            break
    if div_val is None:
        row = db.execute(
            "SELECT date, AVG(score) avg FROM divergence_scores GROUP BY date ORDER BY date DESC LIMIT 1"
        ).fetchone()
        if row and row["avg"] is not None:
            div_val   = round(row["avg"], 1)
            div_label = row["date"][5:]  # "MM-DD"

    last_updated = db.execute(
        "SELECT MAX(collected_at) FROM articles"
    ).fetchone()[0]

    return jsonify({
        "total_articles":   total,
        "sources_count":    sources,
        "period_start":     period[0] or "2026-02-28",
        "period_end":       period[1] or today,
        "divergence_today": div_val,
        "divergence_label": div_label,
        "last_updated":     last_updated or datetime.now(timezone.utc).isoformat(),
    })


@app.route("/api/divergence")
def api_divergence():
    days   = int(request.args.get("days", 30))
    cutoff = cutoff_date(days)
    db     = get_db()

    rows = db.execute(
        """
        SELECT source, date, score
        FROM divergence_scores
        WHERE date >= ?
        ORDER BY date, source
        """,
        (cutoff,),
    ).fetchall()

    dates_set   = sorted({r["date"] for r in rows})
    sources_set = sorted({r["source"] for r in rows})
    lookup      = {(r["source"], r["date"]): r["score"] for r in rows}

    avg_score_rows = db.execute(
        "SELECT source, AVG(score) avg FROM divergence_scores WHERE date >= ? GROUP BY source",
        (cutoff,),
    ).fetchall()
    avg_scores = {r["source"]: round(r["avg"], 1) for r in avg_score_rows}

    series = [
        {
            "source":    src,
            "color":     SOURCE_COLORS.get(src, "#888888"),
            "avg_score": avg_scores.get(src, 0),
            "data":      [lookup.get((src, d)) for d in dates_set],
        }
        for src in sources_set
    ]

    return jsonify({"dates": dates_set, "series": series})


@app.route("/api/frames")
def api_frames():
    # New-style parameters (cross-filter: sources plural, date_from/date_to)
    sources_param = request.args.get("sources", "")
    date_from     = request.args.get("date_from", "")
    date_to       = request.args.get("date_to", "")
    # Legacy parameters kept for backward compatibility
    source = request.args.get("source", "ALL")
    days   = int(request.args.get("days", 30))

    db = get_db()

    # If new-style parameters are provided, use the new aggregation mode
    if sources_param or date_from or date_to:
        conditions = ["a.analyzed = 1"]
        params = []

        if sources_param:
            src_list = [s.strip() for s in sources_param.split(",") if s.strip()]
            placeholders = ",".join("?" * len(src_list))
            conditions.append(f"a.source IN ({placeholders})")
            params.extend(src_list)

        if date_from:
            conditions.append("substr(a.published_at,1,10) >= ?")
            params.append(date_from)

        if date_to:
            conditions.append("substr(a.published_at,1,10) <= ?")
            params.append(date_to)

        where = " AND ".join(conditions)

        rows = db.execute(
            f"""SELECT an.frame, COUNT(*) as cnt
                FROM articles a JOIN analyses an ON a.id = an.article_id
                WHERE {where}
                GROUP BY an.frame ORDER BY cnt DESC""",
            params
        ).fetchall()

        total = sum(r["cnt"] for r in rows)

        return jsonify({
            "frames": [{"frame": r["frame"], "count": r["cnt"],
                        "pct": round(r["cnt"]/total*100, 1) if total else 0}
                       for r in rows],
            "total": total
        })

    # Legacy mode: source=ALL|name, days=N
    cutoff = cutoff_date(days)

    if source == "ALL":
        rows = db.execute(
            """
            SELECT a.source, an.frame, COUNT(*) cnt
            FROM articles a
            JOIN analyses an ON a.id = an.article_id
            WHERE substr(a.published_at,1,10) >= ?
            GROUP BY a.source, an.frame
            """,
            (cutoff,),
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT a.source, an.frame, COUNT(*) cnt
            FROM articles a
            JOIN analyses an ON a.id = an.article_id
            WHERE a.source = ? AND substr(a.published_at,1,10) >= ?
            GROUP BY a.source, an.frame
            """,
            (source, cutoff),
        ).fetchall()

    frames_data: dict = {}
    for r in rows:
        s = r["source"]
        if s not in frames_data:
            frames_data[s] = {}
        frames_data[s][r["frame"]] = r["cnt"]

    div_rows = db.execute(
        "SELECT source, AVG(score) avg FROM divergence_scores WHERE date >= ? GROUP BY source",
        (cutoff,),
    ).fetchall()
    div_scores = {r["source"]: round(r["avg"], 1) for r in div_rows}

    return jsonify({
        "frames":           frames_data,
        "divergence_scores": div_scores,
        "frame_colors":     FRAME_COLORS,
        "frames_order":     FRAMES,
    })


@app.route("/api/articles")
def api_articles():
    """Articles with optional filtering: sources, frame, tone, date_from, date_to, page, limit."""
    sources_param = request.args.get("sources", "")
    frame_param   = request.args.get("frame", "")
    tone_param    = request.args.get("tone", "")
    date_from     = request.args.get("date_from", "")
    date_to       = request.args.get("date_to", "")
    page          = max(1, int(request.args.get("page", 1)))
    limit         = min(50, max(1, int(request.args.get("limit", 20))))
    offset        = (page - 1) * limit

    conn = get_db()

    conditions = ["a.analyzed = 1"]
    params = []

    if sources_param:
        src_list = [s.strip() for s in sources_param.split(",") if s.strip()]
        placeholders = ",".join("?" * len(src_list))
        conditions.append(f"a.source IN ({placeholders})")
        params.extend(src_list)

    if frame_param:
        conditions.append("an.frame = ?")
        params.append(frame_param)

    if tone_param:
        conditions.append("an.tone = ?")
        params.append(tone_param)

    if date_from:
        conditions.append("substr(a.published_at,1,10) >= ?")
        params.append(date_from)

    if date_to:
        conditions.append("substr(a.published_at,1,10) <= ?")
        params.append(date_to)

    where = " AND ".join(conditions)

    total = conn.execute(
        f"SELECT COUNT(*) FROM articles a JOIN analyses an ON a.id = an.article_id WHERE {where}",
        params
    ).fetchone()[0]

    rows = conn.execute(
        f"""SELECT a.url, a.title, a.source, a.published_at,
                   an.frame, an.tone, an.vocabulary, an.victim_actor
            FROM articles a JOIN analyses an ON a.id = an.article_id
            WHERE {where}
            ORDER BY a.published_at DESC
            LIMIT ? OFFSET ?""",
        params + [limit, offset]
    ).fetchall()

    articles = []
    for r in rows:
        try:
            vocab = json.loads(r["vocabulary"] or "[]")
        except Exception:
            vocab = []
        articles.append({
            "url":          r["url"],
            "title":        r["title"],
            "source":       r["source"],
            "published_at": r["published_at"],
            "frame":        r["frame"],
            "tone":         r["tone"],
            "vocabulary":   vocab,
            "victim_actor": r["victim_actor"],
        })

    return jsonify({"articles": articles, "total": total, "page": page, "limit": limit})


@app.route("/api/vocabulary")
def api_vocabulary():
    source = request.args.get("source", "ALL")
    date   = request.args.get("date")
    limit  = int(request.args.get("limit", 20))
    db     = get_db()

    if date:
        if source == "ALL":
            rows = db.execute(
                "SELECT word, SUM(count) total FROM vocabulary_by_source "
                "WHERE date=? GROUP BY word ORDER BY total DESC LIMIT ?",
                (date, limit),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT word, count total FROM vocabulary_by_source "
                "WHERE source=? AND date=? ORDER BY count DESC LIMIT ?",
                (source, date, limit),
            ).fetchall()
    else:
        if source == "ALL":
            rows = db.execute(
                "SELECT word, SUM(count) total FROM vocabulary_by_source "
                "GROUP BY word ORDER BY total DESC LIMIT ?",
                (limit,),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT word, SUM(count) total FROM vocabulary_by_source "
                "WHERE source=? GROUP BY word ORDER BY total DESC LIMIT ?",
                (source, limit),
            ).fetchall()

    return jsonify({
        "words": [{"word": r["word"], "count": r["total"]} for r in rows]
    })


@app.route("/api/events")
def api_events():
    return jsonify(EVENTS)


@app.route("/api/sources")
def api_sources():
    db = get_db()
    rows = db.execute(
        "SELECT DISTINCT source FROM articles WHERE source IS NOT NULL ORDER BY source"
    ).fetchall()
    sources = [r["source"] for r in rows]
    return jsonify({
        "sources": sources,
        "colors":  {s: SOURCE_COLORS.get(s, "#888888") for s in sources},
    })


@app.route("/api/timeline")
def api_timeline():
    sources = request.args.getlist("source")
    limit   = int(request.args.get("limit", 60))
    db      = get_db()

    offset = int(request.args.get("offset", 0))

    if sources:
        ph   = ",".join("?" * len(sources))
        rows = db.execute(
            f"""
            SELECT a.id, a.source, a.title, a.lead, a.url, a.published_at,
                   an.frame, an.tone, a.source_country
            FROM articles a
            JOIN analyses an ON a.id = an.article_id
            WHERE a.source IN ({ph})
            ORDER BY a.published_at DESC
            LIMIT ? OFFSET ?
            """,
            (*sources, limit, offset),
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT a.id, a.source, a.title, a.lead, a.url, a.published_at,
                   an.frame, an.tone, a.source_country
            FROM articles a
            JOIN analyses an ON a.id = an.article_id
            ORDER BY a.published_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()

    return jsonify([
        {
            "id":           r["id"],
            "source":       r["source"],
            "title":        r["title"],
            "lead":         r["lead"],
            "url":          r["url"],
            "published_at": r["published_at"],
            "frame":        r["frame"],
            "tone":         r["tone"],
            "color":        SOURCE_COLORS.get(r["source"], "#888888"),
        }
        for r in rows
    ])


@app.route("/api/insights")
def api_insights():
    db        = get_db()
    today     = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    week_ago  = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    insights  = []

    # 1. Fonte mais divergente da semana
    row = db.execute("""
        SELECT source, AVG(score) avg_score
        FROM divergence_scores
        WHERE date >= ?
        GROUP BY source ORDER BY avg_score DESC LIMIT 1
    """, (week_ago,)).fetchone()
    if row:
        insights.append(
            f"Fonte mais divergente da semana: {row['source']} (score médio {row['avg_score']:.1f})"
        )

    # 2. Frame dominante hoje ou ontem
    for check_date, label in [(today, "hoje"), (yesterday, "ontem")]:
        rows = db.execute("""
            SELECT an.frame, COUNT(*) cnt
            FROM articles a JOIN analyses an ON a.id = an.article_id
            WHERE substr(a.published_at,1,10) = ?
              AND an.frame != 'unclassified'
            GROUP BY an.frame ORDER BY cnt DESC LIMIT 1
        """, (check_date,)).fetchall()
        if rows:
            total_day = db.execute("""
                SELECT COUNT(*) FROM articles a JOIN analyses an ON a.id = an.article_id
                WHERE substr(a.published_at,1,10) = ? AND an.frame != 'unclassified'
            """, (check_date,)).fetchone()[0]
            pct = int(rows[0]["cnt"] / total_day * 100) if total_day else 0
            insights.append(
                f"Frame dominante {label}: {rows[0]['frame']} — {pct}% dos artigos"
            )
            break

    # 3. Maior mudança de frame (fonte que mais variou entre dias consecutivos)
    rows = db.execute("""
        SELECT source, date, dominant_frame
        FROM divergence_scores WHERE date >= ?
        ORDER BY source, date
    """, (week_ago,)).fetchall()

    src_timeline: dict = {}
    for r in rows:
        src_timeline.setdefault(r["source"], []).append((r["date"], r["dominant_frame"]))

    best: tuple | None = None
    for src, timeline in src_timeline.items():
        for i in range(1, len(timeline)):
            d1, f1 = timeline[i - 1]
            d2, f2 = timeline[i]
            if f1 != f2:
                best = (src, d1, f1, d2, f2)
                break

    if best:
        src, d1, f1, d2, f2 = best
        insights.append(
            f"Maior mudança de frame: {src} passou de '{f1}' para '{f2}' entre {d1} e {d2}"
        )

    return jsonify({"insights": insights})


_FRAME_EXPLAIN = {
    "military":     "focuses on combat operations, troop movements, or weapons",
    "humanitarian": "highlights civilian casualties, displacement, or aid",
    "geopolitical": "centers on state actors, alliances, or strategic interests",
    "diplomatic":   "emphasizes negotiations, ceasefires, or international pressure",
    "terrorism":    "uses language labeling non-state actors as terrorist threats",
    "resistance":   "frames armed groups as legitimate resistance fighters",
    "nuclear":      "foregrounds nuclear capability, threat, or deterrence",
}
_TONE_EXPLAIN = {
    "neutral":        "uses balanced, factual language without loaded terms",
    "alarmist":       "uses urgent, catastrophic language to heighten tension",
    "technical":      "relies on dry, precise military or legal terminology",
    "emotional":      "appeals to empathy through personal stories or suffering",
    "propagandistic": "uses one-sided framing or state-aligned talking points",
}


def _local_explain(title: str, frame: str, tone: str) -> str:
    """Fallback explanation without Claude API — rule-based."""
    fe = _FRAME_EXPLAIN.get(frame, f"classified as {frame}")
    te = _TONE_EXPLAIN.get(tone, f"tone is {tone}")
    return f"Frame '{frame}': headline {fe}. Tone '{tone}': it {te}."


@app.route("/api/explain/<article_id>")
def api_explain(article_id: str):
    lang = request.args.get("lang", "en")
    db = get_db()

    # Create cache table if needed (with lang column)
    db.execute("""CREATE TABLE IF NOT EXISTS explanations (
        cache_key TEXT PRIMARY KEY,
        explanation TEXT,
        created_at TEXT
    )""")
    db.commit()

    # Migrate old schema: if table has article_id column instead of cache_key, recreate it
    cols = [r[1] for r in db.execute("PRAGMA table_info(explanations)").fetchall()]
    if "cache_key" not in cols:
        db.execute("ALTER TABLE explanations RENAME TO explanations_old")
        db.execute("""CREATE TABLE explanations (
            cache_key TEXT PRIMARY KEY,
            explanation TEXT,
            created_at TEXT
        )""")
        # Migrate existing rows using article_id as cache_key
        if "article_id" in cols:
            db.execute("""INSERT OR IGNORE INTO explanations
                SELECT article_id, explanation, created_at FROM explanations_old""")
        db.execute("DROP TABLE explanations_old")
        db.commit()

    cache_key = article_id if lang == "en" else f"{article_id}_{lang}"

    # Return cached
    cached = db.execute(
        "SELECT explanation FROM explanations WHERE cache_key = ?", (cache_key,)
    ).fetchone()
    if cached:
        return jsonify({"explanation": cached["explanation"]})

    # Fetch article + analysis
    row = db.execute(
        """SELECT a.title, a.lead, an.frame, an.tone
           FROM articles a JOIN analyses an ON a.id = an.article_id
           WHERE a.id = ?""",
        (article_id,),
    ).fetchone()
    if not row:
        return jsonify({"explanation": ""}), 404

    if lang == "pt":
        prompt = (
            f"Em uma frase, explique por que este título foi classificado como "
            f"frame='{row['frame']}' e tom='{row['tone']}'. "
            f"Foque nas escolhas de palavras específicas. Seja concreto. Máximo 25 palavras. Responda em português.\n\n"
            f"Título: {row['title']}\n"
            f"Lead: {row['lead'] or ''}"
        )
    else:
        prompt = (
            f"In one sentence, explain why this headline was classified as "
            f"frame='{row['frame']}' and tone='{row['tone']}'. "
            f"Focus on specific word choices. Be concrete. Max 20 words.\n\n"
            f"Headline: {row['title']}\n"
            f"Lead: {row['lead'] or ''}"
        )
    try:
        explanation = _call_claude(prompt)
    except Exception:
        explanation = _local_explain(row["title"], row["frame"], row["tone"])

    if explanation:
        db.execute(
            "INSERT OR REPLACE INTO explanations VALUES (?,?,?)",
            (cache_key, explanation, datetime.now(timezone.utc).isoformat()),
        )
        db.commit()

    return jsonify({"explanation": explanation})


@app.route("/api/compare")
def api_compare():
    src_a = request.args.get("source_a", "Al Jazeera")
    src_b = request.args.get("source_b", "Reuters")
    days  = int(request.args.get("days", 30))
    cutoff = cutoff_date(days)
    db = get_db()

    def source_data(src):
        frame_rows = db.execute(
            """SELECT an.frame, COUNT(*) cnt
               FROM articles a JOIN analyses an ON a.id = an.article_id
               WHERE a.source = ? AND substr(a.published_at,1,10) >= ?
               GROUP BY an.frame ORDER BY cnt DESC""",
            (src, cutoff),
        ).fetchall()
        frames = {r["frame"]: r["cnt"] for r in frame_rows}
        total = sum(frames.values())
        dominant_frame = frame_rows[0]["frame"] if frame_rows else None

        tone_rows = db.execute(
            """SELECT an.tone, COUNT(*) cnt
               FROM articles a JOIN analyses an ON a.id = an.article_id
               WHERE a.source = ? AND substr(a.published_at,1,10) >= ?
               GROUP BY an.tone ORDER BY cnt DESC LIMIT 1""",
            (src, cutoff),
        ).fetchone()
        dominant_tone = tone_rows["tone"] if tone_rows else None

        vocab_rows = db.execute(
            """SELECT word, SUM(count) total FROM vocabulary_by_source
               WHERE source = ? GROUP BY word ORDER BY total DESC LIMIT 10""",
            (src,),
        ).fetchall()
        vocab = [{"word": r["word"], "count": r["total"]} for r in vocab_rows]

        latest = db.execute(
            """SELECT a.title, a.id FROM articles a
               JOIN analyses an ON a.id = an.article_id
               WHERE a.source = ? ORDER BY a.published_at DESC LIMIT 1""",
            (src,),
        ).fetchone()

        div_row = db.execute(
            "SELECT AVG(score) avg FROM divergence_scores WHERE source = ? AND date >= ?",
            (src, cutoff),
        ).fetchone()
        div_score = round(div_row["avg"], 1) if div_row and div_row["avg"] else None

        return {
            "source": src,
            "color": SOURCE_COLORS.get(src, "#888"),
            "frames": frames,
            "total_articles": total,
            "dominant_frame": dominant_frame,
            "dominant_tone": dominant_tone,
            "vocab": vocab,
            "latest_title": latest["title"] if latest else None,
            "latest_id": latest["id"] if latest else None,
            "div_score": div_score,
        }

    data_a = source_data(src_a)
    data_b = source_data(src_b)

    import math

    def bhattacharyya(dist_a: dict, dist_b: dict) -> float:
        """Returns Bhattacharyya distance (0=identical, 1=no overlap) between two distributions."""
        all_keys = set(dist_a) | set(dist_b)
        tot_a = sum(dist_a.values()) or 1
        tot_b = sum(dist_b.values()) or 1
        bc = sum(
            math.sqrt((dist_a.get(k, 0) / tot_a) * (dist_b.get(k, 0) / tot_b))
            for k in all_keys
        )
        return 1 - min(bc, 1.0)

    # 1. Frame distribution distance (Bhattacharyya) — 25% weight
    frame_dist = bhattacharyya(data_a["frames"], data_b["frames"])

    # 2. Tone distribution distance — 25% weight
    def tone_dist_for(src):
        rows = db.execute(
            """SELECT an.tone, COUNT(*) cnt
               FROM articles a JOIN analyses an ON a.id = an.article_id
               WHERE a.source = ? AND substr(a.published_at,1,10) >= ?
               GROUP BY an.tone""",
            (src, cutoff),
        ).fetchall()
        return {r["tone"]: r["cnt"] for r in rows}

    tone_a = tone_dist_for(src_a)
    tone_b = tone_dist_for(src_b)
    tone_dist_val = bhattacharyya(tone_a, tone_b)

    # 3. Daily frame-agreement distance — 50% weight
    # On each day both sources published, do they agree on the dominant frame?
    # Disagreement rate → 0=always agree, 1=never agree
    def daily_dominant_frames(src):
        rows = db.execute(
            """SELECT substr(a.published_at,1,10) AS date, an.frame, COUNT(*) cnt
               FROM articles a JOIN analyses an ON a.id = an.article_id
               WHERE a.source = ? AND substr(a.published_at,1,10) >= ?
               GROUP BY date, an.frame""",
            (src, cutoff),
        ).fetchall()
        daily: dict = {}
        for r in rows:
            d, f, c = r["date"], r["frame"], r["cnt"]
            if d not in daily or c > daily[d][1]:
                daily[d] = (f, c)
        return {d: fr for d, (fr, _) in daily.items()}

    dom_a = daily_dominant_frames(src_a)
    dom_b = daily_dominant_frames(src_b)
    common_days = set(dom_a) & set(dom_b)
    if common_days:
        disagree = sum(1 for d in common_days if dom_a[d] != dom_b[d])
        daily_dist = disagree / len(common_days)
    else:
        daily_dist = 0.5  # no shared days → assume moderate distance

    # Composite: daily frame agreement 50% + tone 25% + overall frames 25%
    composite = 0.50 * daily_dist + 0.25 * tone_dist_val + 0.25 * frame_dist
    distance = round(composite * 100, 1)

    return jsonify({"source_a": data_a, "source_b": data_b, "distance": distance})


@app.route("/api/compass")
def api_compass():
    days = int(request.args.get("days", 30))
    cutoff = cutoff_date(days)
    db = get_db()

    sources = db.execute(
        "SELECT DISTINCT source FROM articles WHERE substr(published_at,1,10) >= ?",
        (cutoff,)
    ).fetchall()

    result = []
    for row in sources:
        src = row["source"]
        frames = db.execute(
            """SELECT an.frame, COUNT(*) cnt FROM articles a JOIN analyses an ON a.id=an.article_id
               WHERE a.source=? AND substr(a.published_at,1,10)>=? GROUP BY an.frame""",
            (src, cutoff)
        ).fetchall()
        tones = db.execute(
            """SELECT an.tone, COUNT(*) cnt FROM articles a JOIN analyses an ON a.id=an.article_id
               WHERE a.source=? AND substr(a.published_at,1,10)>=? GROUP BY an.tone""",
            (src, cutoff)
        ).fetchall()

        frame_dict = {r["frame"]: r["cnt"] for r in frames}
        tone_dict  = {r["tone"]:  r["cnt"] for r in tones}
        total_f = sum(frame_dict.values()) or 1
        total_t = sum(tone_dict.values())  or 1

        # X axis: tone lean 0=neutral, 1=propagandistic/alarmist
        tone_lean = (tone_dict.get("alarmist",0) + tone_dict.get("propagandistic",0) + tone_dict.get("emotional",0)) / total_t
        # Y axis: frame lean 0=military/factual, 1=geopolitical/narrative
        frame_lean = (frame_dict.get("geopolitical",0) + frame_dict.get("resistance",0) +
                      frame_dict.get("diplomatic",0) + frame_dict.get("nuclear",0)) / total_f

        div_row = db.execute(
            "SELECT AVG(score) avg FROM divergence_scores WHERE source=? AND date>=?",
            (src, cutoff)
        ).fetchone()

        result.append({
            "source": src,
            "color": SOURCE_COLORS.get(src, "#888"),
            "tone_lean": round(tone_lean, 3),
            "frame_lean": round(frame_lean, 3),
            "div_score": round(div_row["avg"], 1) if div_row and div_row["avg"] else 0,
            "total": total_f,
        })

    return jsonify({"sources": result})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    print(f"Dashboard: http://0.0.0.0:{port}")
    app.run(debug=debug, host="0.0.0.0", port=port, use_reloader=False)
