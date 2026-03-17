"""
Narrative Tracker — Marketing Slides Generator
Generates 10 stunning 1080x1080px PNG slides using Playwright.

Usage:
    cd C:/Claude/narrative-tracker
    python marketing/generate_slides.py

Requires: pip install playwright && playwright install chromium
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).parent / "slides"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Shared CSS injected into every slide ────────────────────────────────────
BASE_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1080px; overflow: hidden;
    background: #0A0D14;
    font-family: system-ui, -apple-system, Arial, sans-serif;
    color: #E8EAF0;
    position: relative;
  }
  /* Radial glow from center */
  body::before {
    content: '';
    position: absolute; inset: 0; z-index: 0;
    background:
      radial-gradient(ellipse 70% 60% at 50% 40%, #12162B 0%, #0A0D14 100%);
  }
  /* Subtle grid lines */
  body::after {
    content: '';
    position: absolute; inset: 0; z-index: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 54px 54px;
  }
  .slide { position: relative; z-index: 1; width: 1080px; height: 1080px; }

  /* NT Monogram */
  .nt-logo {
    position: absolute; top: 36px; left: 40px;
    font-family: Arial Black, Arial, sans-serif;
    font-size: 22px; font-weight: 900;
    color: #F0A500;
    text-shadow: 0 0 18px rgba(240,165,0,0.7);
    letter-spacing: 2px;
  }
  .nt-label {
    position: absolute; top: 42px; left: 80px;
    font-size: 10px; font-family: monospace;
    letter-spacing: 3px; color: #8892A4;
    text-transform: uppercase;
  }
  /* Slide number */
  .slide-num {
    position: absolute; bottom: 32px; right: 44px;
    font-size: 11px; font-family: monospace;
    color: #8892A4; letter-spacing: 2px;
  }
  /* Utility classes */
  .amber-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #F0A500 20%, #F0A500 80%, transparent);
    box-shadow: 0 0 12px 2px rgba(240,165,0,0.5);
  }
  .amber-text {
    color: #F0A500;
    text-shadow: 0 0 30px rgba(240,165,0,0.6);
  }
  .ice-text { color: #64B5F6; }
  .muted { color: #8892A4; }
  .mono { font-family: monospace; }
  .caps { text-transform: uppercase; letter-spacing: 3px; }
"""


def slide_html(body_content: str, slide_num: int) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{BASE_CSS}
</style>
</head>
<body>
<div class="slide">
  <div class="nt-logo">NT</div>
  <span class="nt-label">NARRATIVE TRACKER</span>
  <span class="slide-num">{slide_num:02d} / 10</span>
  {body_content}
</div>
</body>
</html>"""


# ─── Slide 01 — COVER "THE WAR IN NUMBERS" ───────────────────────────────────
def s01():
    return slide_html("""
<style>
  .cover-center {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; padding-bottom: 50px;
  }
  .headline-label {
    font-family: monospace; font-size: 13px;
    color: #8892A4; letter-spacing: 6px;
    text-transform: uppercase; margin-bottom: 20px;
  }
  .big717 {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 220px; font-weight: 900; line-height: 1;
    color: #F0A500;
    text-shadow: 0 0 80px rgba(240,165,0,0.9),
                 0 0 160px rgba(240,165,0,0.4),
                 0 0 240px rgba(240,165,0,0.15);
    letter-spacing: -4px;
  }
  .articles-label {
    font-family: monospace; font-size: 18px;
    color: #8892A4; letter-spacing: 5px;
    text-transform: uppercase; margin-top: 10px;
  }
  .sep-line { width: 360px; margin: 36px auto; }
  .sub-line {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 24px; letter-spacing: 5px;
    color: #E8EAF0; text-transform: uppercase;
    text-align: center;
  }
  .sub-line .amb { color: #F0A500; text-shadow: 0 0 20px rgba(240,165,0,0.5); }
  .date-pill {
    margin-top: 28px;
    padding: 9px 26px; border-radius: 30px;
    border: 1px solid rgba(240,165,0,0.25);
    background: rgba(240,165,0,0.05);
    font-family: monospace; font-size: 13px;
    color: #8892A4; letter-spacing: 3px; text-transform: uppercase;
  }
  .tagline {
    margin-top: 22px;
    font-size: 16px; font-family: monospace;
    color: #8892A4; letter-spacing: 2px;
    font-style: italic;
  }
  /* Full-width bottom amber bar */
  .bottom-bar {
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg,
      transparent 0%, #F0A500 15%, #FFD54F 50%, #F0A500 85%, transparent 100%);
    box-shadow: 0 0 20px 4px rgba(240,165,0,0.5);
  }
  /* Corner radial glows */
  .glow-tl {
    position: absolute; top: -100px; left: -100px;
    width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(circle, rgba(240,165,0,0.06) 0%, transparent 70%);
    pointer-events: none;
  }
  .glow-br {
    position: absolute; bottom: -100px; right: -100px;
    width: 400px; height: 400px; border-radius: 50%;
    background: radial-gradient(circle, rgba(100,181,246,0.04) 0%, transparent 70%);
    pointer-events: none;
  }
</style>
<div class="glow-tl"></div>
<div class="glow-br"></div>
<div class="cover-center">
  <div class="headline-label">The War in Numbers</div>
  <div class="big717">717</div>
  <div class="articles-label">articles analyzed</div>
  <div class="sep-line"><div class="amber-line"></div></div>
  <div class="sub-line">17 SOURCES &nbsp;&nbsp;·&nbsp;&nbsp; 1 WAR &nbsp;&nbsp;·&nbsp;&nbsp; <span class="amb">INFINITE NARRATIVES</span></div>
  <div class="date-pill">March 1 – 17, 2026</div>
  <div class="tagline">AI-powered media divergence analysis</div>
</div>
<div class="bottom-bar"></div>
""", 1)


# ─── Slide 02 — SAME WAR. 17 NARRATIVES. ─────────────────────────────────────
def s02():
    return slide_html("""
<style>
  .s2-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; gap: 0;
  }
  .war-line1 {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 124px; font-weight: 900; line-height: 1;
    color: #E8EAF0; letter-spacing: -2px;
    text-align: center;
  }
  .war-line2 {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 124px; font-weight: 900; line-height: 1;
    color: #F0A500;
    text-shadow: 0 0 50px rgba(240,165,0,0.6);
    letter-spacing: -2px; text-align: center;
  }
  .divider { width: 320px; margin: 36px auto; }
  .s2-sub {
    font-size: 21px; color: #8892A4;
    text-align: center; max-width: 680px;
    line-height: 1.65; font-style: italic;
  }
  .s2-sub em { color: #64B5F6; font-style: normal; }
  .date-range {
    margin-top: 52px;
    padding: 11px 32px; border-radius: 30px;
    border: 1px solid rgba(240,165,0,0.28);
    background: rgba(240,165,0,0.06);
    font-family: monospace; font-size: 15px;
    color: #F0A500; letter-spacing: 4px; text-transform: uppercase;
    box-shadow: 0 0 20px rgba(240,165,0,0.1);
  }
  /* Ring contour decorations */
  .ring1 {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 900px; height: 900px; border-radius: 50%;
    border: 1px solid rgba(240,165,0,0.04);
    pointer-events: none;
  }
  .ring2 {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 700px; height: 700px; border-radius: 50%;
    border: 1px solid rgba(240,165,0,0.03);
    pointer-events: none;
  }
</style>
<div class="ring1"></div>
<div class="ring2"></div>
<div class="s2-wrap">
  <div class="war-line1">SAME WAR.</div>
  <div class="war-line2">17 NARRATIVES.</div>
  <div class="divider"><div class="amber-line"></div></div>
  <div class="s2-sub">How different is <em>Press TV</em> from <em>NYT</em>?<br>The data answers.</div>
  <div class="date-range">March 1 – 17, 2026</div>
</div>
""", 2)


# ─── Slide 03 — DIVERGENCE CHART (all 17 sources) ────────────────────────────
def s03():
    sources = [
        ("Press TV",       44.7),
        ("RT",             38.2),
        ("Al Jazeera",     31.5),
        ("Jerusalem Post", 29.7),
        ("Fox News",       28.4),
        ("NY Post",        26.1),
        ("Daily Mail",     24.8),
        ("Al Arabiya",     22.4),
        ("Haaretz",        20.1),
        ("BBC",            18.3),
        ("AP",             16.7),
        ("Reuters",        15.9),
        ("Guardian",       14.2),
        ("CNN",            13.8),
        ("Wash. Post",     13.1),
        ("NYT",            12.2),
        ("Deutsche Welle", 11.8),
    ]
    max_score = 44.7
    bar_rows = ""
    for i, (name, score) in enumerate(sources):
        pct = score / max_score * 78
        row_bg = "rgba(255,255,255,0.018)" if i % 2 == 0 else "transparent"
        glow_a = max(0.15, score / max_score * 0.75)
        bar_rows += f"""
<div class="bar-row" style="background:{row_bg};">
  <span class="src-label">{name}</span>
  <div class="bar-track">
    <div class="bar-fill" style="width:{pct:.1f}%;
      background: linear-gradient(90deg, #B36B00, #F0A500, #FFD54F);
      box-shadow: inset 0 0 10px rgba(240,165,0,0.3),
                  0 0 8px rgba(240,165,0,{glow_a:.2f});">
    </div>
  </div>
  <span class="score-lbl">{score}</span>
</div>"""

    return slide_html(f"""
<style>
  .s3-wrap {{
    padding: 88px 50px 55px 50px;
    height: 100%; display: flex; flex-direction: column;
  }}
  .s3-title {{
    font-family: Arial Black, Arial, sans-serif;
    font-size: 34px; font-weight: 900; letter-spacing: 1px;
    color: #E8EAF0; margin-bottom: 5px;
  }}
  .s3-underline {{
    width: 280px; height: 2px; margin-bottom: 22px;
    background: linear-gradient(90deg, #F0A500, transparent);
    box-shadow: 0 0 10px rgba(240,165,0,0.6);
  }}
  .bars-container {{
    flex: 1; display: flex; flex-direction: column;
    justify-content: space-between;
  }}
  .bar-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 4px 8px; border-radius: 4px; height: 44px;
  }}
  .src-label {{
    font-family: monospace; font-size: 12px;
    color: #8892A4; width: 112px; text-align: right;
    letter-spacing: 0.4px; white-space: nowrap;
    flex-shrink: 0;
  }}
  .bar-track {{
    flex: 1; height: 20px;
    background: rgba(255,255,255,0.04);
    border-radius: 3px; overflow: hidden;
    border: 1px solid rgba(240,165,0,0.08);
  }}
  .bar-fill {{ height: 100%; border-radius: 3px; }}
  .score-lbl {{
    font-family: Arial Black, Arial, sans-serif;
    font-size: 13px; color: #F0A500;
    text-shadow: 0 0 8px rgba(240,165,0,0.5);
    width: 36px; flex-shrink: 0;
  }}
</style>
<div class="s3-wrap">
  <div class="s3-title">DIVERGENCE FROM CONSENSUS</div>
  <div class="s3-underline"></div>
  <div class="bars-container">
    {bar_rows}
  </div>
</div>
""", 3)


# ─── Slide 04 — PRESS TV SPOTLIGHT ───────────────────────────────────────────
def s04():
    return slide_html("""
<style>
  .s4-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; position: relative;
    padding-top: 30px;
  }
  .most-div {
    font-family: monospace; font-size: 13px;
    color: #F0A500; letter-spacing: 6px;
    text-transform: uppercase; margin-bottom: 8px;
  }
  .source-name {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 48px; font-weight: 900;
    color: #E8EAF0; letter-spacing: 3px;
  }
  .score-big {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 180px; font-weight: 900; line-height: 1;
    color: #F0A500;
    text-shadow:
      0 0 60px rgba(240,165,0,1),
      0 0 120px rgba(240,165,0,0.6),
      0 0 200px rgba(240,165,0,0.25);
    letter-spacing: -3px;
  }
  .div-score-label {
    font-family: monospace; font-size: 13px;
    color: #8892A4; letter-spacing: 7px;
    text-transform: uppercase; margin-top: 4px;
  }
  .sep { width: 240px; margin: 28px auto; }
  .multiplier {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 26px; color: #64B5F6;
    text-shadow: 0 0 20px rgba(100,181,246,0.5);
    letter-spacing: 1px;
  }
  .multiplier .white { color: #E8EAF0; }
  /* Mini compare chart */
  .mini-chart {
    margin-top: 34px;
    display: flex; gap: 28px; align-items: flex-end;
    justify-content: center;
  }
  .mini-bar-wrap {
    display: flex; flex-direction: column;
    align-items: center; gap: 8px;
  }
  .mini-bar {
    width: 56px; border-radius: 4px 4px 0 0;
    background: linear-gradient(180deg, #F0A500, #C67C00);
    box-shadow: 0 0 14px rgba(240,165,0,0.6);
  }
  .mini-bar.avg { background: linear-gradient(180deg, #64B5F6, #1976D2); box-shadow: 0 0 12px rgba(100,181,246,0.4); }
  .mini-bar.nyt { background: linear-gradient(180deg, #607D8B, #37474F); box-shadow: none; }
  .mini-val {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 14px; color: #E8EAF0;
  }
  .mini-lbl {
    font-family: monospace; font-size: 11px;
    color: #8892A4; letter-spacing: 1px;
  }
  /* Word pills */
  .pills-row {
    display: flex; gap: 10px; flex-wrap: wrap;
    justify-content: center; margin-top: 32px;
  }
  .pill {
    padding: 7px 18px; border-radius: 20px;
    border: 1px solid rgba(240,165,0,0.35);
    background: rgba(240,165,0,0.07);
    font-family: monospace; font-size: 13px;
    color: #F0A500; letter-spacing: 1px;
  }
</style>
<div class="s4-wrap">
  <div class="most-div">Most Divergent Source</div>
  <div class="source-name">PRESS TV</div>
  <div class="score-big">44.7</div>
  <div class="div-score-label">Divergence Score</div>
  <div class="sep"><div class="amber-line"></div></div>
  <div class="multiplier"><span class="white">3.6×</span> more divergent than NYT</div>
  <div class="mini-chart">
    <div class="mini-bar-wrap">
      <div class="mini-val">44.7</div>
      <div class="mini-bar" style="height:120px;"></div>
      <div class="mini-lbl">PRESS TV</div>
    </div>
    <div class="mini-bar-wrap">
      <div class="mini-val">21.9</div>
      <div class="mini-bar avg" style="height:60px;"></div>
      <div class="mini-lbl">AVERAGE</div>
    </div>
    <div class="mini-bar-wrap">
      <div class="mini-val">12.2</div>
      <div class="mini-bar nyt" style="height:33px;"></div>
      <div class="mini-lbl">NYT</div>
    </div>
  </div>
  <div class="pills-row">
    <span class="pill">agenda</span>
    <span class="pill">promise</span>
    <span class="pill">imminent</span>
    <span class="pill">resistance</span>
    <span class="pill">zionist</span>
  </div>
</div>
""", 4)


# ─── Slide 05 — FRAME DISTRIBUTION ──────────────────────────────────────────
def s05():
    return slide_html("""
<style>
  .s5-wrap {
    display: flex; flex-direction: column;
    align-items: center;
    padding: 80px 70px 55px; height: 100%;
  }
  .s5-title {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 38px; font-weight: 900;
    color: #E8EAF0; letter-spacing: 1px;
    text-align: center; margin-bottom: 6px;
  }
  .s5-sub {
    font-family: monospace; font-size: 12px;
    color: #8892A4; letter-spacing: 3px;
    text-transform: uppercase; margin-bottom: 40px;
  }
  .donut-wrap {
    position: relative; width: 370px; height: 370px;
    flex-shrink: 0;
  }
  .donut {
    width: 370px; height: 370px; border-radius: 50%;
    background: conic-gradient(
      #F0A500 0% 38.5%,
      #64B5F6 38.5% 74.9%,
      #26A69A 74.9% 91.9%,
      #546E7A 91.9% 100%
    );
    box-shadow:
      0 0 40px rgba(240,165,0,0.2),
      0 0 0 3px rgba(240,165,0,0.15);
  }
  .donut-hole {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 204px; height: 204px; border-radius: 50%;
    background: #0D1020;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border: 1px solid rgba(240,165,0,0.15);
    box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
  }
  .donut-num {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 50px; font-weight: 900;
    color: #F0A500;
    text-shadow: 0 0 20px rgba(240,165,0,0.7);
    line-height: 1;
  }
  .donut-lbl {
    font-family: monospace; font-size: 11px;
    color: #8892A4; letter-spacing: 3px; margin-top: 4px;
  }
  .legend {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 14px 44px; margin-top: 36px;
    width: 100%; max-width: 580px;
  }
  .leg-item { display: flex; align-items: center; gap: 12px; }
  .leg-dot { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  .leg-name {
    font-family: monospace; font-size: 13px;
    color: #8892A4; letter-spacing: 1px;
    text-transform: uppercase; flex: 1;
  }
  .leg-pct {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 18px;
  }
  .caption {
    margin-top: 30px;
    font-size: 15px; color: #8892A4;
    font-style: italic; text-align: center;
    line-height: 1.5; max-width: 640px;
  }
  .caption em { color: #64B5F6; font-style: normal; }
</style>
<div class="s5-wrap">
  <div class="s5-title">HOW THE WAR IS BEING FRAMED</div>
  <div class="s5-sub">717 articles · frame distribution</div>
  <div class="donut-wrap">
    <div class="donut"></div>
    <div class="donut-hole">
      <div class="donut-num">717</div>
      <div class="donut-lbl">ARTICLES</div>
    </div>
  </div>
  <div class="legend">
    <div class="leg-item">
      <div class="leg-dot" style="background:#F0A500;box-shadow:0 0 6px rgba(240,165,0,0.5)"></div>
      <span class="leg-name">Military</span>
      <span class="leg-pct amber-text">38.5%</span>
    </div>
    <div class="leg-item">
      <div class="leg-dot" style="background:#64B5F6;"></div>
      <span class="leg-name">Geopolitical</span>
      <span class="leg-pct ice-text">36.4%</span>
    </div>
    <div class="leg-item">
      <div class="leg-dot" style="background:#26A69A;"></div>
      <span class="leg-name">Humanitarian</span>
      <span class="leg-pct" style="color:#26A69A;">17.0%</span>
    </div>
    <div class="leg-item">
      <div class="leg-dot" style="background:#546E7A;"></div>
      <span class="leg-name">Other</span>
      <span class="leg-pct" style="color:#8892A4;">8.1%</span>
    </div>
  </div>
  <div class="caption">Frame shapes perception <em>before you read a single word</em></div>
</div>
""", 5)


# ─── Slide 06 — TONE ANALYSIS ────────────────────────────────────────────────
def s06():
    tones = [
        ("Neutral",         44.9, "#64B5F6", "🔵"),
        ("Alarmist",        15.9, "#EF5350", "🔴"),
        ("Analytical",      12.7, "#F0A500", "🟡"),
        ("Emotional",        9.5, "#FF9800", "🟠"),
        ("Propagandistic",   8.5, "#78909C", "⚫"),
        ("Hopeful",          8.5, "#66BB6A", "🟢"),
    ]
    bars_html = ""
    for emoji, label, pct, color, _ in [(t[3], t[0], t[1], t[2], None) for t in tones]:
        bar_w = pct / 44.9 * 71
        bars_html += f"""
<div class="tone-row">
  <span class="tone-emoji">{emoji}</span>
  <span class="tone-label">{label}</span>
  <div class="tone-track">
    <div class="tone-bar" style="width:{bar_w:.1f}%; background:{color};
      box-shadow: 0 0 10px {color}99;"></div>
  </div>
  <span class="tone-pct" style="color:{color};">{pct}%</span>
</div>"""

    return slide_html(f"""
<style>
  .s6-wrap {{
    padding: 84px 65px 60px;
    display: flex; flex-direction: column; height: 100%;
  }}
  .s6-title {{
    font-family: Arial Black, Arial, sans-serif;
    font-size: 40px; font-weight: 900;
    color: #E8EAF0; margin-bottom: 6px;
  }}
  .s6-sub {{
    font-family: monospace; font-size: 12px;
    color: #8892A4; letter-spacing: 3px;
    text-transform: uppercase; margin-bottom: 48px;
  }}
  .tone-row {{
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 24px;
  }}
  .tone-emoji {{ font-size: 20px; width: 26px; flex-shrink: 0; }}
  .tone-label {{
    font-family: monospace; font-size: 14px;
    color: #8892A4; letter-spacing: 1px;
    width: 134px; text-transform: uppercase; flex-shrink: 0;
  }}
  .tone-track {{
    flex: 1; height: 28px;
    background: rgba(255,255,255,0.04);
    border-radius: 4px; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
  }}
  .tone-bar {{ height: 100%; border-radius: 4px; opacity: 0.85; }}
  .tone-pct {{
    font-family: Arial Black, Arial, sans-serif;
    font-size: 16px; width: 54px; text-align: right; flex-shrink: 0;
  }}
  .insight-box {{
    margin-top: auto;
    padding: 20px 28px; border-radius: 8px;
    border: 1px solid rgba(240,165,0,0.2);
    background: rgba(240,165,0,0.05);
    display: flex; align-items: center; gap: 16px;
  }}
  .insight-icon {{ font-size: 28px; flex-shrink: 0; }}
  .insight-text {{
    font-family: Arial, sans-serif;
    font-size: 18px; color: #E8EAF0;
    font-style: italic; line-height: 1.4;
  }}
  .insight-text strong {{ color: #F0A500; font-style: normal; }}
</style>
<div class="s6-wrap">
  <div class="s6-title">THE EMOTIONAL TEMPERATURE</div>
  <div class="s6-sub">Tone distribution across 717 articles</div>
  {bars_html}
  <div class="insight-box">
    <div class="insight-icon">💡</div>
    <div class="insight-text">Only <strong>1 in 2 articles</strong> qualifies as neutral — the rest carry emotional or ideological loading.</div>
  </div>
</div>
""", 6)


# ─── Slide 07 — VOCABULARY REVEALS NARRATIVE ─────────────────────────────────
def s07():
    return slide_html("""
<style>
  .s7-wrap {
    display: flex; flex-direction: column;
    padding: 80px 55px 60px; height: 100%;
  }
  .s7-title {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 36px; font-weight: 900;
    color: #E8EAF0; margin-bottom: 6px; text-align: center;
  }
  .s7-sub {
    font-family: monospace; font-size: 12px;
    color: #8892A4; letter-spacing: 3px;
    text-transform: uppercase; text-align: center;
    margin-bottom: 46px;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 2px 1fr;
    flex: 1; gap: 0;
  }
  .col {
    display: flex; flex-direction: column;
    gap: 14px; padding: 0 38px;
  }
  .col-header {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 26px; font-weight: 900;
    letter-spacing: 2px; margin-bottom: 8px;
  }
  .glow-divider {
    width: 2px;
    background: linear-gradient(180deg,
      transparent, #F0A500 20%, #F0A500 80%, transparent);
    box-shadow: 0 0 12px 2px rgba(240,165,0,0.4);
  }
  .word-pill {
    display: inline-block;
    padding: 9px 22px; border-radius: 24px;
    font-family: monospace; font-size: 15px;
    letter-spacing: 1px; width: fit-content;
  }
  .pill-red {
    border: 1px solid rgba(239,83,80,0.4);
    background: rgba(239,83,80,0.08);
    color: #EF9A9A;
  }
  .pill-blue {
    border: 1px solid rgba(100,181,246,0.4);
    background: rgba(100,181,246,0.08);
    color: #90CAF9;
  }
  .caption {
    margin-top: 34px;
    padding: 18px 28px; border-radius: 8px;
    border: 1px solid rgba(240,165,0,0.12);
    background: rgba(240,165,0,0.04);
    font-size: 15px; color: #8892A4;
    font-style: italic; text-align: center;
    line-height: 1.5;
  }
  .caption em { color: #F0A500; font-style: normal; }
</style>
<div class="s7-wrap">
  <div class="s7-title">WORDS THAT BETRAY THE FRAME</div>
  <div class="s7-sub">Distinctive vocabulary by source</div>
  <div class="columns">
    <div class="col">
      <div class="col-header" style="color:#EF5350;text-shadow:0 0 20px rgba(239,83,80,0.5);">PRESS TV</div>
      <span class="word-pill pill-red">agenda</span>
      <span class="word-pill pill-red">promise</span>
      <span class="word-pill pill-red">imminent</span>
      <span class="word-pill pill-red">resistance</span>
      <span class="word-pill pill-red">zionist</span>
      <span class="word-pill pill-red">occupation</span>
    </div>
    <div class="glow-divider"></div>
    <div class="col">
      <div class="col-header" style="color:#64B5F6;text-shadow:0 0 20px rgba(100,181,246,0.5);">NY POST</div>
      <span class="word-pill pill-blue">mehrabad</span>
      <span class="word-pill pill-blue">crush</span>
      <span class="word-pill pill-blue">despicable</span>
      <span class="word-pill pill-blue">strike</span>
      <span class="word-pill pill-blue">retaliation</span>
      <span class="word-pill pill-blue">obliterate</span>
    </div>
  </div>
  <div class="caption"><em>Vocabulary reveals editorial stance</em> before reading a single word of the article.</div>
</div>
""", 7)


# ─── Slide 08 — COST REVEAL "$0.03" ──────────────────────────────────────────
def s08():
    return slide_html("""
<style>
  .s8-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    height: 100%; position: relative;
  }
  /* Dollar watermark */
  .dollar-bg {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-family: Arial Black, Arial, sans-serif;
    font-size: 660px; font-weight: 900;
    color: rgba(240,165,0,0.03);
    line-height: 1; user-select: none; z-index: 0;
    pointer-events: none;
  }
  .s8-content {
    position: relative; z-index: 1; text-align: center;
  }
  .s8-top {
    font-family: monospace; font-size: 14px;
    color: #8892A4; letter-spacing: 6px;
    text-transform: uppercase; margin-bottom: 10px;
  }
  .price-big {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 220px; font-weight: 900; line-height: 1;
    color: #F0A500;
    text-shadow:
      0 0 50px rgba(240,165,0,1),
      0 0 100px rgba(240,165,0,0.7),
      0 0 180px rgba(240,165,0,0.35);
    letter-spacing: -5px;
  }
  .api-label {
    font-family: monospace; font-size: 16px;
    color: #8892A4; letter-spacing: 4px;
    text-transform: uppercase; margin-top: 10px;
  }
  .sep { width: 320px; margin: 30px auto; }
  .detail-line {
    font-family: monospace; font-size: 15px;
    color: #8892A4; letter-spacing: 1px;
    margin-bottom: 10px;
  }
  .shock-box {
    margin-top: 28px;
    padding: 18px 40px; border-radius: 10px;
    border: 1px solid rgba(240,165,0,0.28);
    background: rgba(240,165,0,0.06);
    font-family: Arial Black, Arial, sans-serif;
    font-size: 17px; color: #E8EAF0;
    letter-spacing: 1px; text-align: center;
    line-height: 1.55; max-width: 680px;
    box-shadow: 0 0 30px rgba(240,165,0,0.1);
  }
  .shock-box span { color: #F0A500; }
</style>
<div class="s8-wrap">
  <div class="dollar-bg">$</div>
  <div class="s8-content">
    <div class="s8-top">The entire analysis cost</div>
    <div class="price-big">$0.03</div>
    <div class="api-label">in API tokens</div>
    <div class="sep"><div class="amber-line"></div></div>
    <div class="detail-line">717 articles &nbsp;·&nbsp; Claude Haiku &nbsp;·&nbsp; ~$0.80 per million tokens</div>
    <div class="shock-box">
      <span>BI-grade</span> media intelligence<br>
      at the cost of a fraction of a penny
    </div>
  </div>
</div>
""", 8)


# ─── Slide 09 — OPEN SOURCE CTA ──────────────────────────────────────────────
def s09():
    return slide_html("""
<style>
  .s9-wrap {
    display: flex; flex-direction: column;
    align-items: center; padding: 82px 60px 52px;
    height: 100%;
  }
  .s9-title {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 42px; font-weight: 900;
    color: #E8EAF0; text-align: center;
    letter-spacing: 1px; margin-bottom: 8px;
  }
  .s9-title .amb { color: #F0A500; text-shadow: 0 0 20px rgba(240,165,0,0.5); }
  .sep { width: 280px; margin: 22px auto; }
  .github-url {
    font-family: monospace; font-size: 21px;
    color: #F0A500;
    text-shadow: 0 0 20px rgba(240,165,0,0.5);
    letter-spacing: 1px; text-align: center;
    margin-bottom: 48px;
  }
  .features-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 18px; width: 100%; max-width: 680px;
    margin-bottom: 40px;
  }
  .feat-pill {
    padding: 22px 24px; border-radius: 10px;
    border: 1px solid rgba(240,165,0,0.18);
    background: rgba(240,165,0,0.05);
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 0 20px rgba(240,165,0,0.04);
  }
  .feat-icon { font-size: 28px; flex-shrink: 0; }
  .feat-text {
    font-family: monospace; font-size: 14px;
    color: #E8EAF0; letter-spacing: 1px;
    text-transform: uppercase;
  }
  .star-cta {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 26px; color: #F0A500;
    text-shadow: 0 0 20px rgba(240,165,0,0.5);
    letter-spacing: 2px; margin-bottom: 28px;
  }
  .live-url-box {
    padding: 14px 32px; border-radius: 8px;
    border: 1px solid rgba(100,181,246,0.25);
    background: rgba(100,181,246,0.05);
    font-family: monospace; font-size: 15px;
    color: #64B5F6; letter-spacing: 1px;
  }
</style>
<div class="s9-wrap">
  <div class="s9-title">BUILT IN <span class="amb">PUBLIC.</span> OPEN TO ALL.</div>
  <div class="sep"><div class="amber-line"></div></div>
  <div class="github-url">github.com/deniciojunior/narrative-tracker</div>
  <div class="features-grid">
    <div class="feat-pill">
      <span class="feat-icon">🔄</span>
      <span class="feat-text">Hourly Updates</span>
    </div>
    <div class="feat-pill">
      <span class="feat-icon">🤖</span>
      <span class="feat-text">Claude Haiku AI</span>
    </div>
    <div class="feat-pill">
      <span class="feat-icon">📊</span>
      <span class="feat-text">Live Dashboard</span>
    </div>
    <div class="feat-pill">
      <span class="feat-icon">💾</span>
      <span class="feat-text">Open Source</span>
    </div>
  </div>
  <div class="star-cta">⭐ Star it on GitHub</div>
  <div class="live-url-box">https://web-production-8d4b.up.railway.app</div>
</div>
""", 9)


# ─── Slide 10 — CLOSING / LIVE LINK ──────────────────────────────────────────
def s10():
    return slide_html("""
<style>
  .s10-wrap {
    display: flex; flex-direction: column;
    align-items: center; justify-content: space-between;
    height: 100%; padding: 88px 60px 68px;
  }
  .s10-top {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 46px; font-weight: 900;
    color: #E8EAF0; text-align: center;
    letter-spacing: 2px; text-transform: uppercase;
    line-height: 1.1;
  }
  .s10-top .amb {
    color: #F0A500;
    text-shadow: 0 0 30px rgba(240,165,0,0.7);
  }
  .url-block { text-align: center; }
  .url-main {
    font-family: monospace; font-size: 30px;
    color: #F0A500;
    text-shadow: 0 0 30px rgba(240,165,0,0.7);
    letter-spacing: 0.5px; display: block;
    margin-bottom: 26px;
  }
  /* Decorative QR-style box */
  .qr-box {
    width: 190px; height: 190px; margin: 0 auto;
    border: 2px solid rgba(240,165,0,0.4);
    border-radius: 10px;
    background: rgba(240,165,0,0.04);
    box-shadow: 0 0 28px rgba(240,165,0,0.15);
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(6, 1fr);
    gap: 5px; padding: 14px;
  }
  .qr-cell { border-radius: 2px; background: rgba(240,165,0,0.38); }
  /* Stats row */
  .stats-row {
    display: flex; gap: 0; width: 100%;
    border: 1px solid rgba(240,165,0,0.15);
    border-radius: 10px; overflow: hidden;
  }
  .stat-block {
    flex: 1; text-align: center;
    padding: 20px 10px;
    background: rgba(240,165,0,0.04);
    border-right: 1px solid rgba(240,165,0,0.12);
  }
  .stat-block:last-child { border-right: none; }
  .stat-num {
    font-family: Arial Black, Arial, sans-serif;
    font-size: 38px; font-weight: 900;
    color: #F0A500;
    text-shadow: 0 0 20px rgba(240,165,0,0.5);
    display: block;
  }
  .stat-label {
    font-family: monospace; font-size: 11px;
    color: #8892A4; letter-spacing: 3px;
    text-transform: uppercase; display: block;
    margin-top: 4px;
  }
  .final-tagline {
    font-family: Arial, system-ui, sans-serif;
    font-size: 18px; color: #8892A4;
    font-style: italic; text-align: center;
    line-height: 1.6;
  }
  .final-tagline strong { color: #F0A500; font-style: normal; }
  .gh-small {
    font-family: monospace; font-size: 12px;
    color: #546E7A; letter-spacing: 1px;
  }
</style>
<div class="s10-wrap">
  <div class="s10-top">THE DASHBOARD<br>IS <span class="amb">LIVE</span></div>

  <div class="url-block">
    <span class="url-main">web-production-8d4b.up.railway.app</span>
    <div class="qr-box">
      <div class="qr-cell"></div><div class="qr-cell" style="opacity:.15"></div><div class="qr-cell"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.12"></div><div class="qr-cell"></div>
      <div class="qr-cell" style="opacity:.25"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.08"></div><div class="qr-cell" style="opacity:.5"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.3"></div>
      <div class="qr-cell"></div><div class="qr-cell" style="opacity:.6"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.2"></div><div class="qr-cell"></div><div class="qr-cell"></div>
      <div class="qr-cell" style="opacity:.4"></div><div class="qr-cell"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.7"></div><div class="qr-cell" style="opacity:.1"></div><div class="qr-cell"></div>
      <div class="qr-cell"></div><div class="qr-cell" style="opacity:.2"></div><div class="qr-cell" style="opacity:.8"></div><div class="qr-cell"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.4"></div>
      <div class="qr-cell" style="opacity:.5"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.3"></div><div class="qr-cell"></div><div class="qr-cell" style="opacity:.6"></div><div class="qr-cell"></div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat-block">
      <span class="stat-num">717</span>
      <span class="stat-label">Articles</span>
    </div>
    <div class="stat-block">
      <span class="stat-num">17</span>
      <span class="stat-label">Sources</span>
    </div>
    <div class="stat-block">
      <span class="stat-num" style="font-size:30px;">$0.03</span>
      <span class="stat-label">Total Cost</span>
    </div>
  </div>

  <div class="final-tagline">
    <strong>Narrative Tracker</strong> — Because context is everything.
  </div>
  <div class="gh-small">github.com/deniciojunior/narrative-tracker</div>
</div>
""", 10)


# ─── Main render loop ─────────────────────────────────────────────────────────
async def render_slides():
    slides = [
        (1,  s01, "Cover — The War in Numbers"),
        (2,  s02, "Same War. 17 Narratives."),
        (3,  s03, "Divergence Chart — All 17 Sources"),
        (4,  s04, "Press TV Spotlight"),
        (5,  s05, "Frame Distribution"),
        (6,  s06, "Tone Analysis"),
        (7,  s07, "Vocabulary Reveals Narrative"),
        (8,  s08, "Cost Reveal $0.03"),
        (9,  s09, "Open Source CTA"),
        (10, s10, "Closing / Live Link"),
    ]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})

        for idx, slide_fn, desc in slides:
            html = slide_fn()
            await page.set_content(html, wait_until="networkidle")
            out_path = OUTPUT_DIR / f"slide_{idx:02d}.png"
            await page.screenshot(path=str(out_path), full_page=False)
            size_kb = out_path.stat().st_size // 1024
            print(f"  [OK] slide_{idx:02d}.png  ({size_kb} KB)  —  {desc}")

        await browser.close()

    print(f"\nAll 10 slides saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    print("Narrative Tracker — Generating 10 marketing slides (1080x1080px)...\n")
    asyncio.run(render_slides())
