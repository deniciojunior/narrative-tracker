"""
collector.py — Coleta artigos via RSS puro (sem GDELT).
Histórico existente no banco é preservado; só insere novos artigos.
"""

import hashlib
import re
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import feedparser

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

DB_PATH = "../articles.db"
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "articles.db")

WAR_START = "2026-02-28"  # data de corte — artigos anteriores são ignorados

# Fontes e feeds RSS
SOURCES = {
    # Wire services — âncora estatística central
    "Reuters":           "https://feeds.reuters.com/reuters/worldNews",
    "AP News":           "https://rsshub.app/apnews/topics/world-news",
    # Ocidentais de referência
    "BBC":               "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "The Guardian":      "https://www.theguardian.com/world/middleeast/rss",
    "NYT":               "https://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml",
    # Perspectiva europeia
    "France 24":         "https://www.france24.com/en/middle-east/rss",
    "DW English":        "https://rss.dw.com/rdf/rss-en-world",
    # Árabe / regional
    "Al Jazeera":        "https://www.aljazeera.com/xml/rss/all.xml",
    "Arab News":         "https://www.arabnews.com/rss.xml",
    "Middle East Eye":   "https://www.middleeasteye.net/rss",
    # Israelense
    "Haaretz":           "https://www.haaretz.com/cmlink/1.628765",
    "Jerusalem Post":    "https://www.jpost.com/Rss/RssFeedsHeadlines.aspx",
    "Times of Israel":   "https://www.timesofisrael.com/feed/",
    # Russo-chinês
    "RT":                "https://www.rt.com/rss/news/",
    "Xinhua":            "https://feeds.feedburner.com/xinhuanet/english",
    # Estatal iraniano (outlier documentado)
    "Press TV":          "https://www.presstv.ir/RSS",
}

# Palavras-chave de relevância — pelo menos 1 deve estar no título+lead
KEYWORDS = [
    "iran", "israel", "tehran", "idf", "irgc",
    "netanyahu", "khamenei", "trump", "middle east",
    "strikes", "missiles", "nuclear", "war", "attack",
    "hezbollah", "strait of hormuz", "natanz", "fordow",
    "beirut", "gaza", "west bank",
]

TAG_RE = re.compile(r"<[^>]+>")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_html(text: str) -> str:
    return TAG_RE.sub("", text or "").strip()


def sha256_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()


def is_relevant(title: str, lead: str) -> bool:
    text = (title + " " + lead).lower()
    return any(kw in text for kw in KEYWORDS)


# ---------------------------------------------------------------------------
# Fetch individual feed
# ---------------------------------------------------------------------------

def fetch_feed(source_name: str, feed_url: str) -> list[dict]:
    """Busca e filtra um feed RSS. Retorna lista de dicts prontos para inserção."""
    try:
        feed = feedparser.parse(
            feed_url,
            request_headers={"User-Agent": "NarrativeTracker/1.0 (research project)"},
        )
    except Exception as exc:
        print(f"  [ERRO] {source_name}: {exc}")
        return []

    articles = []
    for entry in feed.entries:
        # ── Data de publicação ────────────────────────────────────────────
        published = None
        for attr in ("published_parsed", "updated_parsed"):
            tp = getattr(entry, attr, None)
            if tp:
                try:
                    published = datetime(*tp[:6], tzinfo=timezone.utc).isoformat()
                    break
                except Exception:
                    pass
        if not published:
            published = datetime.now(timezone.utc).isoformat()

        # Só artigos desde o início do conflito
        if published[:10] < WAR_START:
            continue

        # ── Título e lead ────────────────────────────────────────────────
        title = strip_html(entry.get("title", "")).strip()
        summary = strip_html(
            entry.get("summary", entry.get("description", ""))
        ).strip()
        lead = (summary or title)[:400]

        url = entry.get("link", "").strip()
        if not url or not title:
            continue

        # ── Relevância ───────────────────────────────────────────────────
        if not is_relevant(title, lead):
            continue

        articles.append(
            {
                "id":           sha256_id(url),
                "url":          url,
                "title":        title,
                "lead":         lead,
                "source":       source_name,
                "published_at": published,
            }
        )

    return articles


# ---------------------------------------------------------------------------
# Coleta principal
# ---------------------------------------------------------------------------

def run_collection():
    conn = sqlite3.connect(DB_PATH)
    # Garante tabela existente (idempotente)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id              TEXT PRIMARY KEY,
            url             TEXT UNIQUE,
            title           TEXT,
            lead            TEXT,
            source          TEXT,
            source_country  TEXT,
            published_at    TEXT,
            collected_at    TEXT,
            analyzed        INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    total_new = 0
    collected_at = datetime.now(timezone.utc).isoformat()

    print(f"Coletando RSS de {len(SOURCES)} fontes em paralelo...\n")

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_name = {
            executor.submit(fetch_feed, name, url): name
            for name, url in SOURCES.items()
        }
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                articles = future.result()
            except Exception as exc:
                print(f"  [ERRO] {name}: {exc}")
                continue

            new = 0
            for a in articles:
                try:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO articles
                            (id, url, title, lead, source, published_at, collected_at, analyzed)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
                        """,
                        (
                            a["id"], a["url"], a["title"], a["lead"],
                            a["source"], a["published_at"], collected_at,
                        ),
                    )
                    if conn.execute("SELECT changes()").fetchone()[0] > 0:
                        new += 1
                except sqlite3.Error:
                    pass

            conn.commit()
            total_new += new
            status = f"{len(articles):>3} encontrados | {new:>3} novos"
            print(f"  {name:<22} {status}")

    # ── Resumo ────────────────────────────────────────────────────────────
    total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    by_source = conn.execute(
        "SELECT source, COUNT(*) FROM articles GROUP BY source ORDER BY COUNT(*) DESC"
    ).fetchall()

    print(f"\nColeta concluída: {total_new} novos artigos | {total} total no banco")
    print("\nPor fonte:")
    for src, cnt in by_source:
        print(f"  {src:<24} {cnt}")

    conn.close()


if __name__ == "__main__":
    run_collection()
