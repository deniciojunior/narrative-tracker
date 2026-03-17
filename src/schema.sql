CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    url TEXT UNIQUE,
    title TEXT,
    lead TEXT,
    source TEXT,
    source_country TEXT,
    published_at TEXT,
    collected_at TEXT,
    analyzed INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS analyses (
    article_id TEXT PRIMARY KEY REFERENCES articles(id),
    frame TEXT,
    vocabulary TEXT,
    victim_actor TEXT,
    tone TEXT,
    analyzed_at TEXT
);
