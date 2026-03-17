![Python](https://img.shields.io/badge/Python-3.11+-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Claude Haiku](https://img.shields.io/badge/AI-Claude%20Haiku-orange) ![Data](https://img.shields.io/badge/Data-RSS%20%2B%20GDELT-lightgrey) ![Cost](https://img.shields.io/badge/Analysis%20Cost-%240.03-brightgreen)

# Narrative Tracker

> AI-powered media framing analysis of the US-Israel-Iran War 2026

This project analyzed **717 articles** from **17 English-language sources** covering the US-Israel-Iran War, spanning **2026-03-01 to 2026-03-17**. Each headline and lead was classified by Claude Haiku into narrative frames, emotional tones, and revealing vocabulary — then scored for divergence from the global consensus narrative.

## What it does

- Collects articles from **17 English-language sources** via RSS + GDELT
- Analyzes each headline + lead with **Claude Haiku**: narrative frame, emotional tone, revealing vocabulary
- Calculates a **Bhattacharyya divergence score** (0–100) showing how far each source drifts from the global average narrative
- Serves a live **interactive dashboard** built with Flask + Chart.js

## Live demo

> 🚀 **[Live Dashboard →](https://web-production-8d4b.up.railway.app)**
>
> ⭐ Star this repo to follow updates as the conflict develops

## How it works

```
RSS / GDELT feeds
      ↓
  collector.py  ──→  SQLite (700 articles)
      ↓
  analyzer.py   ──→  Claude Haiku  (~$0.03 total)
      ↓
  scorer.py     ──→  Bhattacharyya divergence scores
      ↓
  app.py        ──→  Flask dashboard  (localhost:5000)
```

**The divergence score**: We compare each source's daily frame distribution against the global median using Bhattacharyya distance — a statistical measure of overlap between probability distributions. Score 0 = identical to average. Score 100 = completely different framing.

## Key findings (as of 2026-03-17)

- **Most divergent source**: Press TV (avg score 44.7)
- **Most neutral source**: NYT (avg score 12.2)
- **Dominant frame**: military (38.5% of all articles)
- **Dominant tone**: neutral (44.9%)
- **Press TV** characteristic words: agenda, promise, imminent
- **NY Post** characteristic words: mehrabad, crush, despicable

## Quick start

```bash
git clone https://github.com/deniciojunior/narrative-tracker
cd narrative-tracker
cp .env.example .env           # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python src/collector.py        # collect historical data (GDELT)
python src/analyzer.py         # analyze with Claude Haiku (~$0.03)
python src/scorer.py           # calculate divergence scores
python src/app.py              # dashboard at localhost:5000

# Continuous hourly updates via RSS:
python src/scheduler.py
```

## Tech stack

| Component  | Technology               |
|------------|--------------------------|
| Collection | GDELT Project + RSS      |
| AI         | Claude Haiku (Anthropic) |
| Backend    | Python 3.11 + Flask      |
| Database   | SQLite                   |
| Frontend   | Vanilla JS + Chart.js    |
| Deployment | Railway                  |

## Methodology

**1. Data collection** — Articles are collected from 17 sources via RSS feeds every hour, plus historical data via the GDELT Project. Only English-language content is processed.

**2. AI classification** — Each article's title and lead are sent to Claude Haiku with a structured prompt asking for: narrative frame (one of 7 categories), emotional tone (one of 5 categories), and the 5 most revealing vocabulary terms.

**3. Divergence score** — We compute the Bhattacharyya coefficient between each source's daily frame distribution and the global average. This gives a distance score (0–100) — the higher the score, the more a source's framing deviates from the consensus.

**4. Limitations**
- RSS feeds contain only title + excerpt, not full article text
- AI classification is probabilistic — individual articles may be misclassified
- Only English editions are analyzed; Arabic/Hebrew/Russian versions may differ
- Divergence ≠ bias — a source can deviate from the average by being *more* accurate

## Project structure

```
narrative-tracker/
├── src/
│   ├── app.py              # Flask dashboard
│   ├── collector.py        # GDELT + RSS collector
│   ├── analyzer.py         # Claude Haiku classifier
│   ├── scorer.py           # Bhattacharyya scorer
│   ├── scheduler.py        # Hourly automation
│   └── templates/
│       └── index.html      # Dashboard UI (Chart.js)
├── articles.db             # SQLite (gitignored)
├── requirements.txt        # Python dependencies
├── Procfile                # Railway/Heroku deploy
├── railway.toml            # Railway config
└── .env.example            # Environment template
```

## Contributing

Issues and PRs welcome. To add a new source, add its RSS feed to `rss_collector.py` and submit a PR.

## License

MIT © 2026
