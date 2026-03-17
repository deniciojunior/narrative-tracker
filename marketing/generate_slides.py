"""
generate_slides.py — Gera os 10 slides de marketing (1080×1080px).

Uso:
    cd C:/Claude/narrative-tracker
    python marketing/generate_slides.py

Requer playwright: pip install playwright && playwright install chromium
"""

import asyncio
import os
from pathlib import Path

# ─── DADOS REAIS DO APP (atualizado 2026-03-17) ────────────────────────────
LIVE_URL   = "https://web-production-8d4b.up.railway.app"
GITHUB_URL = "https://github.com/deniciojunior/narrative-tracker"
ARTICLES   = 700
SOURCES    = 17
DATE_RANGE = "01–17 Mar 2026"
API_COST   = "$0.03"

RANKING = [
    ("Press TV",       44.7, "#27AE60"),
    ("TASS",           35.6, "#8B1A1A"),
    ("DW English",     35.6, "#888888"),
    ("Xinhua",         32.2, "#DE2910"),
    ("NY Post",        31.7, "#E74C3C"),
    ("DW",             26.6, "#C0392B"),
    ("Haaretz",        26.5, "#0057B7"),
    ("Middle East Eye",22.0, "#D4AC0D"),
    ("Fox News",       21.6, "#003DA5"),
    ("The Guardian",   21.3, "#052962"),
    ("France 24",      20.0, "#003D7C"),
    ("RT",             19.7, "#CC0000"),
    ("Al Jazeera",     19.6, "#E8593C"),
    ("BBC",            20.8, "#1D4E8F"),
    ("Times of Israel",13.7, "#4A90D9"),
    ("Jerusalem Post", 12.3, "#2E86AB"),
    ("NYT",            12.2, "#CCCCCC"),
]

# ─── PALETA ────────────────────────────────────────────────────────────────
BG      = "#0D1117"
BG2     = "#161B22"
AMBER   = "#D29922"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
BORDER  = "#30363D"

OUT_DIR = Path(__file__).parent / "slides"
OUT_DIR.mkdir(exist_ok=True)

# ─── TEMPLATE BASE ──────────────────────────────────────────────────────────
def base(body_html: str, title: str = "") -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1080px; overflow:hidden; background:{BG}; color:{TEXT};
    font-family:'IBM Plex Sans', sans-serif; }}
  .slide {{ width:1080px; height:1080px; display:flex; flex-direction:column;
    padding:64px; position:relative; }}
  .tag {{ font-family:'IBM Plex Mono', monospace; font-size:13px; color:{AMBER};
    letter-spacing:0.12em; text-transform:uppercase; margin-bottom:24px; }}
  h1 {{ font-size:52px; font-weight:700; line-height:1.1; margin-bottom:20px; }}
  h2 {{ font-size:38px; font-weight:600; line-height:1.2; margin-bottom:16px; }}
  .accent {{ color:{AMBER}; }}
  .muted {{ color:{MUTED}; }}
  .mono {{ font-family:'IBM Plex Mono', monospace; }}
  .footer {{ margin-top:auto; padding-top:32px; border-top:1px solid {BORDER};
    display:flex; justify-content:space-between; align-items:center;
    font-size:13px; color:{MUTED}; font-family:'IBM Plex Mono', monospace; }}
  .corner-badge {{ position:absolute; top:48px; right:64px;
    font-family:'IBM Plex Mono',monospace; font-size:12px; color:{AMBER};
    border:1px solid rgba(210,153,34,0.35); padding:6px 12px; border-radius:4px; }}
  .divider {{ height:1px; background:{BORDER}; margin:24px 0; }}
</style>
</head>
<body>
<div class="slide">
  <div class="corner-badge">NT</div>
  {body_html}
  <div class="footer">
    <span>{LIVE_URL}</span>
    <span>github.com/deniciojunior/narrative-tracker</span>
  </div>
</div>
</body></html>"""


# ─── 10 SLIDES ──────────────────────────────────────────────────────────────

def slide_01():
    return base(f"""
<div class="tag">Narrative Tracker — Media Analysis 2026</div>
<h1>Same war.<br><span class="accent">17 narratives.</span><br>One divergence score.</h1>
<div class="divider"></div>
<p style="font-size:22px; color:{MUTED}; line-height:1.6; max-width:700px;">
  AI-powered analysis of how major media outlets frame the<br>
  <strong style="color:{TEXT}">US-Israel-Iran War 2026</strong> — in real time.
</p>
<div style="display:flex; gap:48px; margin-top:40px;">
  <div><div style="font-size:56px; font-weight:700; color:{AMBER}; font-family:'IBM Plex Mono',monospace">{ARTICLES}</div>
    <div style="color:{MUTED}; font-size:16px; margin-top:4px;">articles analyzed</div></div>
  <div><div style="font-size:56px; font-weight:700; color:{AMBER}; font-family:'IBM Plex Mono',monospace">{SOURCES}</div>
    <div style="color:{MUTED}; font-size:16px; margin-top:4px;">global sources</div></div>
  <div><div style="font-size:56px; font-weight:700; color:{AMBER}; font-family:'IBM Plex Mono',monospace">{API_COST}</div>
    <div style="color:{MUTED}; font-size:16px; margin-top:4px;">total AI cost</div></div>
</div>
""", "Cover")


def slide_02():
    bars = ""
    max_score = RANKING[0][1]
    for name, score, color in RANKING[:8]:
        w = int((score / max_score) * 560)
        bars += f"""
        <div style="display:flex; align-items:center; gap:16px; margin-bottom:12px;">
          <div style="width:160px; font-size:15px; text-align:right; color:{MUTED}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{name}</div>
          <div style="width:{w}px; height:28px; background:{color}; border-radius:3px; flex-shrink:0;"></div>
          <div style="font-family:'IBM Plex Mono',monospace; font-size:15px; color:{TEXT};">{score}</div>
        </div>"""
    return base(f"""
<div class="tag">Divergence Ranking — Top 8</div>
<h2>Who diverges most from<br>the <span class="accent">global narrative?</span></h2>
<p style="font-size:15px; color:{MUTED}; margin-bottom:24px;">
  Bhattacharyya score 0–100. Higher = further from consensus framing.
</p>
{bars}
""", "Ranking")


def slide_03():
    top = RANKING[0]
    bot = RANKING[-1]
    return base(f"""
<div class="tag">Extremes — Most vs. Least Divergent</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:48px; flex:1; align-items:center;">
  <div style="background:{BG2}; border:1px solid {BORDER}; border-radius:12px; padding:40px; text-align:center;">
    <div style="font-size:13px; color:{MUTED}; font-family:'IBM Plex Mono',monospace; margin-bottom:16px;">MOST DIVERGENT</div>
    <div style="font-size:80px; font-weight:700; color:{top[2]}; font-family:'IBM Plex Mono',monospace; line-height:1;">{top[1]}</div>
    <div style="font-size:24px; font-weight:600; margin-top:16px;">{top[0]}</div>
    <div style="font-size:14px; color:{MUTED}; margin-top:8px;">frames the conflict unlike<br>any other source</div>
  </div>
  <div style="background:{BG2}; border:1px solid {BORDER}; border-radius:12px; padding:40px; text-align:center;">
    <div style="font-size:13px; color:{MUTED}; font-family:'IBM Plex Mono',monospace; margin-bottom:16px;">MOST ALIGNED</div>
    <div style="font-size:80px; font-weight:700; color:{bot[2]}; font-family:'IBM Plex Mono',monospace; line-height:1;">{bot[1]}</div>
    <div style="font-size:24px; font-weight:600; margin-top:16px;">{bot[0]}</div>
    <div style="font-size:14px; color:{MUTED}; margin-top:8px;">closest to the global<br>consensus framing</div>
  </div>
</div>
<p style="text-align:center; font-size:13px; color:{MUTED}; margin-top:24px;">
  Divergence ≠ bias. A high score means <em>different</em>, not necessarily wrong.
</p>
""", "Extremes")


def slide_04():
    frames = [
        ("Military",      38.5, AMBER),
        ("Geopolitical",  36.4, "#4A9EFF"),
        ("Humanitarian",  17.0, "#52D68A"),
        ("Diplomatic",     5.2, "#F8A35C"),
        ("Economic",       2.9, "#BB8FCE"),
    ]
    bars = ""
    for name, pct, color in frames:
        w = int((pct / 38.5) * 500)
        bars += f"""
        <div style="margin-bottom:18px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <span style="font-size:16px;">{name}</span>
            <span style="font-family:'IBM Plex Mono',monospace; font-size:16px; color:{AMBER};">{pct}%</span>
          </div>
          <div style="height:20px; background:{color}26; border-radius:3px;">
            <div style="width:{w}px; height:100%; background:{color}; border-radius:3px;"></div>
          </div>
        </div>"""
    return base(f"""
<div class="tag">Narrative Frames — Distribution</div>
<h2>How is the war being<br><span class="accent">framed?</span></h2>
<p style="font-size:15px; color:{MUTED}; margin-bottom:28px;">{ARTICLES} articles · {DATE_RANGE}</p>
{bars}
<p style="font-size:14px; color:{MUTED}; margin-top:16px;">
  Same events, radically different emphasis depending on who's writing.
</p>
""", "Frames")


def slide_05():
    tones = [
        ("Neutral",        44.9, "#8B949E"),
        ("Alarming",       15.9, "#E74C3C"),
        ("Informative",    15.7, "#4A9EFF"),
        ("Emotional",       9.5, "#F39C12"),
        ("Propagandistic",  8.5, "#8E44AD"),
        ("Other",           5.5, "#52D68A"),
    ]
    items = ""
    for name, pct, color in tones:
        items += f"""
        <div style="background:{BG2}; border:1px solid {BORDER}; border-radius:8px; padding:20px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:12px; height:12px; background:{color}; border-radius:2px; flex-shrink:0;"></div>
            <span style="font-size:17px;">{name}</span>
          </div>
          <span style="font-family:'IBM Plex Mono',monospace; font-size:22px; font-weight:600; color:{AMBER};">{pct}%</span>
        </div>"""
    return base(f"""
<div class="tag">Emotional Tone — All Sources</div>
<h2>Neutral is the <span class="accent">minority</span>.<br>44% — but barely.</h2>
{items}
""", "Tones")


def slide_06():
    vocab = [
        ("Press TV",     "#27AE60", ["agenda",    "promise",   "imminent",  "accord",   "proxy"]),
        ("NY Post",      "#E74C3C", ["mehrabad",  "crush",     "despicable","strike",   "obliterate"]),
        ("RT",           "#CC0000", ["escalation","provocation","retaliation","Zionist", "hegemony"]),
        ("NYT",          "#CCCCCC", ["officials", "reported",  "confirmed", "coalition","strikes"]),
        ("Al Jazeera",   "#E8593C", ["displaced", "civilians", "siege",     "massacre", "enclave"]),
    ]
    items = ""
    for src, color, words in vocab:
        tags = "".join(f'<span style="background:{color}22;border:1px solid {color}44;color:{color};padding:4px 10px;border-radius:4px;font-size:13px;margin:3px;display:inline-block;">{w}</span>' for w in words)
        items += f"""
        <div style="margin-bottom:16px;">
          <div style="font-size:14px; color:{MUTED}; margin-bottom:6px; font-family:'IBM Plex Mono',monospace;">{src}</div>
          <div>{tags}</div>
        </div>"""
    return base(f"""
<div class="tag">Revealing Vocabulary — Word Choice as Signal</div>
<h2>Words betray the<br><span class="accent">frame</span> before you read the article.</h2>
{items}
""", "Vocabulary")


def slide_07():
    return base(f"""
<div class="tag">Methodology — How it works</div>
<h2>The <span class="accent">pipeline</span> behind the scores.</h2>
<div style="display:flex; flex-direction:column; gap:20px; margin-top:12px;">
  {"".join(f'''<div style="display:flex; align-items:flex-start; gap:24px;">
    <div style="width:36px; height:36px; background:rgba(210,153,34,0.15); border:1px solid {AMBER}; border-radius:6px;
      display:flex; align-items:center; justify-content:center; font-family:'IBM Plex Mono',monospace;
      font-size:15px; color:{AMBER}; flex-shrink:0;">{n}</div>
    <div><div style="font-size:17px; font-weight:600; margin-bottom:4px;">{t}</div>
    <div style="font-size:14px; color:{MUTED};">{d}</div></div>
  </div>''' for n, t, d in [
    ("1", "Collect", f"RSS feeds + GDELT every 60 min → {ARTICLES} articles, {DATE_RANGE}"),
    ("2", "Classify", "Claude Haiku reads title + lead → frame, tone, vocabulary (7 frames × 5 tones)"),
    ("3", "Score", "Bhattacharyya distance between each source's daily distribution and global median"),
    ("4", "Visualize", "Flask dashboard: heatmap, DNA chart, compass, article feed — updated hourly"),
  ])}
</div>
<div style="margin-top:28px; background:{BG2}; border:1px solid {BORDER}; border-radius:8px; padding:20px 24px; font-family:'IBM Plex Mono',monospace; font-size:14px; color:{MUTED};">
  Total analysis cost: <span style="color:{AMBER};">{API_COST}</span> &nbsp;·&nbsp;
  Updates every <span style="color:{AMBER};">60 min</span> &nbsp;·&nbsp;
  Open source &nbsp;·&nbsp; 100% reproducible
</div>
""", "Pipeline")


def slide_08():
    return base(f"""
<div class="tag">Live Dashboard — Features</div>
<h2>Four views.<br>One <span class="accent">coherent picture.</span></h2>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:16px;">
  {"".join(f'''<div style="background:{BG2}; border:1px solid {BORDER}; border-radius:10px; padding:28px;">
    <div style="font-size:22px; margin-bottom:10px;">{icon}</div>
    <div style="font-size:17px; font-weight:600; margin-bottom:6px;">{name}</div>
    <div style="font-size:14px; color:{MUTED}; line-height:1.5;">{desc}</div>
  </div>''' for icon, name, desc in [
    ("🌡️", "Divergence Heatmap", f"17 sources × 17 days — spot which outlet had a spike"),
    ("🧬", "Source DNA", "Frame + tone breakdown per outlet — compare their editorial fingerprints"),
    ("🧭", "Consensus Compass", "Scatter: how far from center is each source, day by day"),
    ("📰", "Article Feed", "Browse individual articles with AI-generated frame explanation"),
  ])}
</div>
<div style="margin-top:24px; text-align:center; font-size:15px; color:{MUTED};">
  Filter any chart by source or frame — all panels update simultaneously.
</div>
""", "Dashboard")


def slide_09():
    return base(f"""
<div class="tag">Tech Stack — Open Source</div>
<h2>Built with<br><span class="accent">off-the-shelf</span> tools.</h2>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:20px;">
  {"".join(f'''<div style="background:{BG2}; border:1px solid {BORDER}; border-radius:8px; padding:20px 24px; display:flex; align-items:center; gap:16px;">
    <div style="font-size:24px;">{icon}</div>
    <div>
      <div style="font-size:15px; font-weight:600;">{name}</div>
      <div style="font-size:13px; color:{MUTED};">{role}</div>
    </div>
  </div>''' for icon, name, role in [
    ("🗞️", "GDELT + RSS",      "Data collection — free, global"),
    ("🤖", "Claude Haiku",     f"AI classification — {API_COST} for {ARTICLES} articles"),
    ("🐍", "Python + Flask",   "Backend — lightweight, fast"),
    ("🗃️", "SQLite",           "Database — zero ops, self-contained"),
    ("📊", "Chart.js",         "Frontend — interactive, no build step"),
    ("🚂", "Railway",          "Deployment — auto-deploys from GitHub"),
  ])}
</div>
<div style="margin-top:24px; font-family:'IBM Plex Mono',monospace; font-size:13px; color:{MUTED}; text-align:center;">
  Full source code → {GITHUB_URL}
</div>
""", "Stack")


def slide_10():
    return base(f"""
<div class="tag">Narrative Tracker — Live Now</div>
<div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
  <div style="font-size:96px; margin-bottom:32px;">🌐</div>
  <h1 style="font-size:44px; margin-bottom:24px;">
    See the data.<br>Read the divergence.<br><span class="accent">Form your own view.</span>
  </h1>
  <div style="background:{BG2}; border:1px solid rgba(210,153,34,0.4); border-radius:10px; padding:24px 48px; margin-top:16px;">
    <div style="font-family:'IBM Plex Mono',monospace; font-size:22px; color:{AMBER};">{LIVE_URL}</div>
    <div style="font-size:14px; color:{MUTED}; margin-top:8px;">Updated every 60 minutes · Free · Open source</div>
  </div>
  <div style="margin-top:32px; font-family:'IBM Plex Mono',monospace; font-size:15px; color:{MUTED};">
    ⭐ Star on GitHub → {GITHUB_URL.replace("https://", "")}
  </div>
</div>
""", "CTA")


# ─── RENDER ──────────────────────────────────────────────────────────────────
SLIDES = [
    ("slide_01", slide_01, "Cover — Hook"),
    ("slide_02", slide_02, "Divergence ranking"),
    ("slide_03", slide_03, "Extremes: Press TV vs NYT"),
    ("slide_04", slide_04, "Frame distribution"),
    ("slide_05", slide_05, "Tone breakdown"),
    ("slide_06", slide_06, "Revealing vocabulary"),
    ("slide_07", slide_07, "Pipeline methodology"),
    ("slide_08", slide_08, "Dashboard features"),
    ("slide_09", slide_09, "Tech stack"),
    ("slide_10", slide_10, "CTA — live URL"),
]


async def render(name: str, html: str, out: Path):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=str(out), full_page=False)
        await browser.close()


async def main():
    for fname, fn, desc in SLIDES:
        html = fn()
        out  = OUT_DIR / f"{fname}.png"
        print(f"  → {fname}.png  ({desc})")
        await render(fname, html, out)
    print(f"\n✓ {len(SLIDES)} slides saved to {OUT_DIR}/")


if __name__ == "__main__":
    print(f"Generating {len(SLIDES)} slides → {OUT_DIR}/\n")
    asyncio.run(main())
