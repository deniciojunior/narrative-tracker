"""
Narrative Tracker — Marketing Slides v2
Bold, impactful visual design — 1080x1080px
"""
import asyncio, os
from playwright.async_api import async_playwright

OUT = os.path.join(os.path.dirname(__file__), "slides")
os.makedirs(OUT, exist_ok=True)

LIVE_URL = "web-production-8d4b.up.railway.app"
GITHUB   = "github.com/deniciojunior/narrative-tracker"
AUTHOR   = "linkedin.com/in/deniciosantos"

BG     = "#050A0F"
AMBER  = "#F0A500"
AMBER2 = "#FFD166"
RED    = "#FF4757"
BLUE   = "#00B4D8"
GREEN  = "#06D6A0"
PURPLE = "#A855F7"
TEXT   = "#F0F2F5"
MUTED  = "#6B7280"
CARD   = "#0D1520"
BORDER = "#1E2D3D"

def base():
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,sans-serif}}
html,body{{width:1080px;height:1080px;overflow:hidden;background:{BG};color:{TEXT}}}
.mono{{font-family:'Courier New',monospace}}
</style></head><body>"""

SLIDES = []

# ── SLIDE 1: Cover ─────────────────────────────────────────────────────────────
SLIDES.append(("slide_01.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.grid{{position:absolute;inset:0;
  background:linear-gradient(rgba(240,165,0,.07) 1px,transparent 1px),
    linear-gradient(90deg,rgba(240,165,0,.07) 1px,transparent 1px);
  background-size:60px 60px}}
.glow{{position:absolute;top:-100px;left:50%;transform:translateX(-50%);
  width:900px;height:700px;border-radius:50%;
  background:radial-gradient(circle,rgba(240,165,0,.12) 0%,transparent 70%)}}
.tag{{position:absolute;top:60px;left:60px;font-size:11px;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;color:{MUTED};
  border:1px solid {BORDER};padding:6px 14px;border-radius:4px;
  display:inline-flex;align-items:center;gap:8px}}
.dot{{width:7px;height:7px;border-radius:50%;background:{AMBER};
  box-shadow:0 0 10px {AMBER}}}
.center{{position:absolute;top:50%;left:50%;transform:translate(-50%,-52%);
  text-align:center;width:920px}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
  color:{AMBER};margin-bottom:28px}}
h1{{font-size:104px;font-weight:900;line-height:.88;letter-spacing:-.03em;
  background:linear-gradient(160deg,{TEXT} 20%,{AMBER2} 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  -webkit-font-smoothing:antialiased}}
.sub{{font-size:22px;font-weight:300;color:rgba(240,242,245,.5);
  margin-top:28px;line-height:1.5}}
.stats{{position:absolute;bottom:104px;left:50%;transform:translateX(-50%);
  display:flex;gap:80px;text-align:center;
  background:rgba(13,21,32,.8);border:1px solid {BORDER};
  border-radius:16px;padding:24px 48px}}
.stat-n{{font-size:48px;font-weight:800;color:{AMBER};line-height:1}}
.stat-l{{font-size:11px;color:{MUTED};letter-spacing:.1em;text-transform:uppercase;margin-top:4px}}
.bot{{position:absolute;bottom:44px;left:0;right:0;display:flex;
  justify-content:space-between;padding:0 60px;
  font-size:11px;color:{MUTED}}}
.hr{{position:absolute;height:1px;left:0;right:0;
  background:linear-gradient(90deg,transparent,rgba(240,165,0,.3),transparent)}}
.hr-top{{top:0}}.hr-bot{{bottom:82px}}
</style>
<div class="wrap">
  <div class="grid"></div><div class="glow"></div>
  <div class="hr hr-top"></div>
  <div class="tag"><span class="dot"></span>Live · March 2026</div>
  <div class="center">
    <div class="eyebrow">AI-Powered Media Analysis</div>
    <h1>NARRATIVE<br>TRACKER</h1>
    <div class="sub">How 17 media outlets frame the same war — differently</div>
  </div>
  <div class="stats">
    <div><div class="stat-n">717</div><div class="stat-l">Articles</div></div>
    <div><div class="stat-n">17</div><div class="stat-l">Sources</div></div>
    <div><div class="stat-n">$0.03</div><div class="stat-l">API Cost</div></div>
    <div><div class="stat-n">100%</div><div class="stat-l">Open Source</div></div>
  </div>
  <div class="hr hr-bot"></div>
  <div class="bot">
    <span>{LIVE_URL}</span>
    <span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 2: The Problem ────────────────────────────────────────────────────────
SLIDES.append(("slide_02.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.glow1{{position:absolute;top:-150px;right:-150px;width:700px;height:700px;border-radius:50%;
  background:radial-gradient(circle,rgba(168,85,247,.14) 0%,transparent 70%)}}
.glow2{{position:absolute;bottom:-200px;left:-100px;width:600px;height:600px;border-radius:50%;
  background:radial-gradient(circle,rgba(0,180,216,.09) 0%,transparent 70%)}}
.topbar{{position:absolute;top:0;left:0;right:0;height:5px;
  background:linear-gradient(90deg,{PURPLE},{AMBER},{RED})}}
.content{{position:absolute;top:80px;left:68px;right:68px;bottom:72px}}
.label{{font-size:11px;font-weight:700;letter-spacing:.2em;color:{PURPLE};
  text-transform:uppercase;margin-bottom:18px}}
h2{{font-size:68px;font-weight:900;line-height:.95;letter-spacing:-.025em;margin-bottom:24px}}
.hl{{color:{AMBER}}}
.lead{{font-size:18px;color:rgba(240,242,245,.6);line-height:1.65;
  max-width:680px;margin-bottom:40px}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.card{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:26px;
  position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.ca::before{{background:{AMBER}}}.cb::before{{background:{BLUE}}}
.cc::before{{background:{GREEN}}}.cd::before{{background:{RED}}}
.big{{font-size:52px;font-weight:800;line-height:1}}
.cname{{font-size:14px;font-weight:700;margin:6px 0 4px}}
.cdesc{{font-size:12px;color:{MUTED};line-height:1.5}}
.foot{{position:absolute;bottom:0;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="glow1"></div><div class="glow2"></div><div class="topbar"></div>
  <div class="content">
    <div class="label">The Problem</div>
    <h2>Same war.<br><span class="hl">17 realities.</span></h2>
    <div class="lead">
      Every outlet covers the US-Israel-Iran conflict.<br>
      But the <em>narrative</em> — framing, tone, vocabulary — reveals something completely different beneath the facts.
    </div>
    <div class="cards">
      <div class="card ca">
        <div class="big" style="color:{AMBER}">44.7</div>
        <div class="cname">Press TV divergence score</div>
        <div class="cdesc">Most distant from the global narrative consensus across 17 sources</div>
      </div>
      <div class="card cb">
        <div class="big" style="color:{BLUE}">12.2</div>
        <div class="cname">NYT divergence score</div>
        <div class="cdesc">Closest to the consensus — most neutral framing observed</div>
      </div>
      <div class="card cc">
        <div class="big" style="color:{GREEN}">38.5%</div>
        <div class="cname">Military frame</div>
        <div class="cdesc">Most common narrative across all 717 articles analyzed</div>
      </div>
      <div class="card cd">
        <div class="big" style="color:{RED}">8.5%</div>
        <div class="cname">Propagandistic tone</div>
        <div class="cdesc">Articles with clear agenda, loaded language, one-sided framing</div>
      </div>
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span>{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 3: Divergence Ranking ─────────────────────────────────────────────────
sources = [
  ("Press TV",44.7,RED),("Al Jazeera",38.2,"#FF6B35"),("Fox News",34.1,"#FF8C42"),
  ("RT",31.8,PURPLE),("CGTN",28.5,"#E040FB"),("Breitbart",26.3,"#FF4081"),
  ("Haaretz",23.1,"#00BCD4"),("Times of Israel",21.4,BLUE),("AP",19.7,AMBER),
  ("Reuters",17.2,AMBER2),("BBC",16.8,GREEN),("The Guardian",15.9,"#69F0AE"),
  ("Washington Post",15.1,"#A5D6A7"),("CNN",14.3,"#B2EBF2"),
  ("Al Monitor",13.7,"#CFD8DC"),("NPR",13.1,"#ECEFF1"),("NYT",12.2,TEXT),
]
bars = ""
for name, val, col in sources:
    w = int(val / 44.7 * 520)
    bars += f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
      <div style="width:128px;font-size:10.5px;color:{MUTED};text-align:right;flex-shrink:0;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</div>
      <div style="width:{w}px;height:20px;
        background:linear-gradient(90deg,{col}CC,{col}44);border-radius:3px;
        border-left:3px solid {col};position:relative;min-width:40px">
        <span style="position:absolute;right:6px;top:50%;transform:translateY(-50%);
          font-size:9.5px;font-weight:700;color:{col};font-family:'Courier New',monospace">{val}</span>
      </div>
    </div>"""

SLIDES.append(("slide_03.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.accent{{position:absolute;top:0;left:0;right:0;height:4px;
  background:linear-gradient(90deg,{AMBER},{RED})}}
.content{{position:absolute;top:68px;left:68px;right:68px;bottom:68px}}
.eyebrow{{font-size:11px;letter-spacing:.2em;color:{AMBER};text-transform:uppercase;
  font-weight:700;margin-bottom:10px}}
h2{{font-size:46px;font-weight:900;letter-spacing:-.02em;margin-bottom:4px}}
.sub{{font-size:13px;color:{MUTED};margin-bottom:20px}}
.chart{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:22px 24px}}
.legend{{display:flex;gap:20px;margin-top:16px;font-size:11px;color:{MUTED};
  align-items:center}}
.leg-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0}}
.foot{{position:absolute;bottom:0;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="accent"></div>
  <div class="content">
    <div class="eyebrow">Bhattacharyya Divergence Score · 0–100</div>
    <h2>Who diverges the most?</h2>
    <div class="sub">Distance from global narrative consensus across 17 sources · 717 articles · March 2026</div>
    <div class="chart">{bars}</div>
    <div class="legend">
      <div class="leg-dot" style="background:{RED}"></div><span>High divergence</span>
      <div class="leg-dot" style="background:{GREEN};margin-left:12px"></div><span>Consensus-aligned</span>
      <span style="margin-left:auto">Narrative Tracker · {LIVE_URL}</span>
    </div>
  </div>
  <div class="foot"><span></span><span class="mono">{GITHUB}</span></div>
</div></body></html>"""))

# ── SLIDE 4: Press TV Spotlight ─────────────────────────────────────────────────
SLIDES.append(("slide_04.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.glow{{position:absolute;top:-200px;left:-200px;width:900px;height:900px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,71,87,.18) 0%,transparent 65%)}}
.stripe{{position:absolute;top:0;left:0;right:0;height:6px;background:{RED}}}
.content{{position:absolute;top:80px;left:72px;right:72px;bottom:72px}}
.badge{{display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,71,87,.15);border:1px solid rgba(255,71,87,.4);
  border-radius:6px;padding:7px 16px;font-size:11px;font-weight:700;
  color:{RED};letter-spacing:.12em;text-transform:uppercase;margin-bottom:20px}}
h2{{font-size:80px;font-weight:900;line-height:.92;letter-spacing:-.03em;margin-bottom:8px}}
.score-row{{display:flex;align-items:baseline;gap:16px;margin:20px 0 32px}}
.bignum{{font-size:128px;font-weight:900;color:{RED};line-height:1;
  text-shadow:0 0 80px rgba(255,71,87,.5)}}
.score-lbl{{font-size:18px;color:{MUTED}}}
.words-lbl{{font-size:11px;letter-spacing:.15em;text-transform:uppercase;
  color:{MUTED};font-weight:700;margin-bottom:12px}}
.words{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}}
.w{{background:rgba(255,71,87,.13);border:1px solid rgba(255,71,87,.35);
  border-radius:6px;padding:8px 16px;font-size:14px;font-weight:700;color:{RED}}}
.note{{background:{CARD};border:1px solid {BORDER};border-left:3px solid {RED};
  border-radius:0 12px 12px 0;padding:20px 24px;
  font-size:15px;color:rgba(240,242,245,.7);line-height:1.65}}
.foot{{position:absolute;bottom:0;left:72px;right:72px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="glow"></div><div class="stripe"></div>
  <div class="content">
    <div class="badge">⚠ Highest Divergence</div>
    <h2>Press TV</h2>
    <div class="score-row">
      <div class="bignum">44.7</div>
      <div class="score-lbl">divergence<br>score</div>
    </div>
    <div class="words-lbl">Characteristic vocabulary</div>
    <div class="words">
      <span class="w">agenda</span><span class="w">promise</span>
      <span class="w">imminent</span><span class="w">regime</span>
      <span class="w">aggression</span><span class="w">resistance</span>
    </div>
    <div class="note">
      <strong>Divergence ≠ bias.</strong> A high score means the narrative is
      <em>statistically distant</em> from the global consensus — it could be more accurate, or more slanted.
      The score measures <strong>difference</strong>, not <strong>quality</strong>.
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 5: Frame Distribution ─────────────────────────────────────────────────
frames = [
  ("Military",38.5,AMBER,"Strikes, operations, weapons"),
  ("Geopolitical",36.4,BLUE,"Alliances, sanctions, diplomacy"),
  ("Humanitarian",17.0,GREEN,"Casualties, civilians, aid"),
  ("Diplomatic",5.2,PURPLE,"Negotiations, ceasefires"),
  ("Economic",2.9,"#F59E0B","Oil, trade, sanctions impact"),
]
frame_html = ""
for name, pct, col, desc in frames:
    w = int(pct / 38.5 * 100)
    frame_html += f"""<div style="margin-bottom:18px">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">
        <span style="font-size:15px;font-weight:700">{name}</span>
        <span style="font-size:28px;font-weight:800;color:{col}">{pct}%</span>
      </div>
      <div style="height:9px;background:{CARD};border-radius:5px;overflow:hidden;margin-bottom:3px">
        <div style="width:{w}%;height:100%;background:linear-gradient(90deg,{col},{col}70);border-radius:5px"></div>
      </div>
      <div style="font-size:12px;color:{MUTED}">{desc}</div>
    </div>"""

SLIDES.append(("slide_05.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.sidebar{{position:absolute;left:0;top:0;bottom:0;width:5px;
  background:linear-gradient(180deg,{AMBER},{BLUE},{GREEN})}}
.glr{{position:absolute;top:0;right:-150px;width:550px;height:550px;border-radius:50%;
  background:radial-gradient(circle,rgba(240,165,0,.09) 0%,transparent 70%)}}
.content{{position:absolute;top:68px;left:84px;right:68px;bottom:68px}}
.eyebrow{{font-size:11px;letter-spacing:.2em;color:{AMBER};text-transform:uppercase;
  font-weight:700;margin-bottom:10px}}
h2{{font-size:52px;font-weight:900;letter-spacing:-.02em;margin-bottom:6px}}
.sub{{font-size:14px;color:{MUTED};margin-bottom:32px;max-width:600px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}}
.insight{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:24px}}
.ins-title{{font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:{MUTED};font-weight:700;margin-bottom:14px}}
.ins-text{{font-size:14px;line-height:1.65;color:rgba(240,242,245,.72)}}
.foot{{position:absolute;bottom:0;left:84px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="sidebar"></div><div class="glr"></div>
  <div class="content">
    <div class="eyebrow">Narrative Frame Distribution · 717 articles</div>
    <h2>How is the war being framed?</h2>
    <div class="sub">7 possible narrative frames. One dominates — but the split varies wildly by source.</div>
    <div class="cols">
      <div>{frame_html}</div>
      <div class="insight">
        <div class="ins-title">Key Insight</div>
        <div class="ins-text">
          <strong style="color:{AMBER}">Military + Geopolitical = 74.9%</strong><br>
          of all coverage. The humanitarian angle — real people, casualties, displacement — gets only
          <strong style="color:{GREEN}">17%</strong> of the framing.<br><br>
          Same facts. Different lens.<br>Different understanding.
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 6: Tone Analysis ──────────────────────────────────────────────────────
SLIDES.append(("slide_06.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.mesh{{position:absolute;inset:0;
  background:radial-gradient(ellipse 800px 500px at 30% 40%,rgba(6,214,160,.08) 0%,transparent 60%),
    radial-gradient(ellipse 600px 600px at 80% 70%,rgba(168,85,247,.07) 0%,transparent 60%)}}
.toprule{{position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,transparent,{GREEN},transparent)}}
.content{{position:absolute;top:68px;left:68px;right:68px;bottom:68px}}
.eyebrow{{font-size:11px;letter-spacing:.2em;color:{GREEN};text-transform:uppercase;
  font-weight:700;margin-bottom:10px}}
h2{{font-size:54px;font-weight:900;letter-spacing:-.02em;margin-bottom:28px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:24px}}
.tc{{background:{CARD};border:1px solid {BORDER};border-radius:14px;
  padding:28px;position:relative;overflow:hidden}}
.tc::after{{content:'';position:absolute;top:0;right:0;
  width:70px;height:70px;border-radius:0 14px 0 70px}}
.tca::after{{background:rgba(240,165,0,.07)}}
.tcb::after{{background:rgba(255,71,87,.07)}}
.tcc::after{{background:rgba(168,85,247,.07)}}
.tcd::after{{background:rgba(0,180,216,.07)}}
.tc-pct{{font-size:62px;font-weight:800;line-height:1;margin-bottom:6px}}
.tc-name{{font-size:15px;font-weight:700;margin-bottom:4px}}
.tc-desc{{font-size:12px;color:{MUTED};line-height:1.45}}
.alert{{background:rgba(255,71,87,.1);border:1px solid rgba(255,71,87,.3);
  border-radius:12px;padding:18px 22px;
  font-size:15px;color:rgba(240,242,245,.82);line-height:1.6}}
.foot{{position:absolute;bottom:0;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="mesh"></div><div class="toprule"></div>
  <div class="content">
    <div class="eyebrow">Emotional Tone Breakdown</div>
    <h2>Neutrality is the minority</h2>
    <div class="grid">
      <div class="tc tca">
        <div class="tc-pct" style="color:{AMBER}">44.9%</div>
        <div class="tc-name">Neutral</div>
        <div class="tc-desc">Factual, balanced reporting without evident emotional loading</div>
      </div>
      <div class="tc tcb">
        <div class="tc-pct" style="color:{RED}">15.9%</div>
        <div class="tc-name">Alarmist</div>
        <div class="tc-desc">Heightened urgency, catastrophizing language, fear-driven framing</div>
      </div>
      <div class="tc tcc">
        <div class="tc-pct" style="color:{PURPLE}">9.5%</div>
        <div class="tc-name">Emotional</div>
        <div class="tc-desc">Appeals to empathy, human stories, sentiment-heavy coverage</div>
      </div>
      <div class="tc tcd">
        <div class="tc-pct" style="color:{BLUE}">8.5%</div>
        <div class="tc-name">Propagandistic</div>
        <div class="tc-desc">Loaded language, clear agenda, one-sided narrative construction</div>
      </div>
    </div>
    <div class="alert">
      <strong style="color:{RED}">55.1% of articles have non-neutral tone.</strong>
      More than half of war coverage carries emotional, alarmist, or propagandistic framing.
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 7: Vocabulary ─────────────────────────────────────────────────────────
SLIDES.append(("slide_07.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.bg{{position:absolute;inset:0;
  background:radial-gradient(ellipse 900px 600px at 50% 20%,rgba(240,165,0,.07) 0%,transparent 70%)}}
.topbar{{position:absolute;top:0;left:0;right:0;height:5px;
  background:linear-gradient(90deg,{RED},{AMBER},{GREEN})}}
.content{{position:absolute;top:72px;left:68px;right:68px;bottom:68px}}
.eyebrow{{font-size:11px;letter-spacing:.2em;color:{AMBER};text-transform:uppercase;
  font-weight:700;margin-bottom:10px}}
h2{{font-size:50px;font-weight:900;letter-spacing:-.02em;margin-bottom:6px}}
.sub{{font-size:14px;color:{MUTED};margin-bottom:32px;max-width:700px}}
.vsgrid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.ob{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:26px}}
.on{{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:4px}}
.os{{font-size:12px;color:{MUTED};margin-bottom:16px}}
.wc{{display:flex;flex-wrap:wrap;gap:7px}}
.wt{{border-radius:6px;padding:7px 14px;font-size:13px;font-weight:700}}
.vrow{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}}
.vcard{{background:{CARD};border:1px solid {BORDER};border-radius:12px;
  padding:18px 20px;font-size:13px;color:{MUTED};line-height:1.55}}
.vcard strong{{display:block;font-size:14px;margin-bottom:5px}}
.foot{{position:absolute;bottom:0;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="bg"></div><div class="topbar"></div>
  <div class="content">
    <div class="eyebrow">Vocabulary Analysis — Distinctive Words</div>
    <h2>Words reveal the frame</h2>
    <div class="sub">What an outlet chooses to say — and not say — exposes its narrative before you read a single article.</div>
    <div class="vsgrid">
      <div class="ob" style="border-color:rgba(255,71,87,.3)">
        <div class="on" style="color:{RED}">Press TV</div>
        <div class="os">Score: 44.7 · Most divergent</div>
        <div class="wc">
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">agenda</span>
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">promise</span>
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">imminent</span>
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">regime</span>
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">aggression</span>
          <span class="wt" style="background:rgba(255,71,87,.14);color:{RED}">resistance</span>
        </div>
      </div>
      <div class="ob" style="border-color:rgba(0,180,216,.3)">
        <div class="on" style="color:{BLUE}">NY Post</div>
        <div class="os">Score: 24.1 · High divergence</div>
        <div class="wc">
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">mehrabad</span>
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">crush</span>
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">despicable</span>
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">obliterate</span>
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">terror</span>
          <span class="wt" style="background:rgba(0,180,216,.14);color:{BLUE}">threat</span>
        </div>
      </div>
    </div>
    <div class="vrow">
      <div class="vcard"><strong style="color:{AMBER}">NYT — score 12.2</strong>
        "officials", "military", "statement" — institutional, neutral framing
      </div>
      <div class="vcard"><strong style="color:{GREEN}">Reuters — score 17.2</strong>
        "said", "confirmed", "reported" — wire service attribution language
      </div>
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 8: Tech Stack & Cost ──────────────────────────────────────────────────
SLIDES.append(("slide_08.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.grid{{position:absolute;inset:0;
  background:linear-gradient(rgba(240,165,0,.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(240,165,0,.04) 1px,transparent 1px);
  background-size:54px 54px}}
.cglow{{position:absolute;bottom:-100px;right:-100px;width:500px;height:500px;border-radius:50%;
  background:radial-gradient(circle,rgba(6,214,160,.11) 0%,transparent 70%)}}
.topbar{{position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,{GREEN},{AMBER})}}
.content{{position:absolute;top:68px;left:68px;right:68px;bottom:68px}}
.eyebrow{{font-size:11px;letter-spacing:.2em;color:{GREEN};text-transform:uppercase;
  font-weight:700;margin-bottom:10px}}
h2{{font-size:54px;font-weight:900;letter-spacing:-.02em;margin-bottom:28px}}
.pipeline{{display:flex;align-items:center;margin-bottom:36px}}
.step{{background:{CARD};border:1px solid {BORDER};border-radius:12px;
  padding:18px 14px;flex:1;text-align:center}}
.si{{font-size:26px;margin-bottom:6px}}
.sn{{font-size:12px;font-weight:700;margin-bottom:3px}}
.st{{font-size:11px;color:{MUTED}}}
.arr{{color:{AMBER};font-size:18px;padding:0 4px;flex-shrink:0}}
.cost{{background:linear-gradient(135deg,rgba(6,214,160,.1),rgba(240,165,0,.1));
  border:1px solid rgba(6,214,160,.3);border-radius:16px;
  padding:28px 36px;display:flex;align-items:center;gap:36px}}
.costnum{{font-size:96px;font-weight:900;color:{GREEN};line-height:1;
  text-shadow:0 0 50px rgba(6,214,160,.4)}}
.costdet{{flex:1}}
.costtitle{{font-size:20px;font-weight:700;margin-bottom:10px}}
.costlist{{font-size:13px;color:{MUTED};line-height:1.85}}
.costlist span{{color:{TEXT}}}
.foot{{position:absolute;bottom:0;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="grid"></div><div class="cglow"></div><div class="topbar"></div>
  <div class="content">
    <div class="eyebrow">How It Works</div>
    <h2>The entire pipeline.<br>$0.03.</h2>
    <div class="pipeline">
      <div class="step"><div class="si">📡</div><div class="sn">Collect</div><div class="st">RSS+GDELT</div></div>
      <div class="arr">→</div>
      <div class="step"><div class="si">🤖</div><div class="sn">Classify</div><div class="st">Claude Haiku</div></div>
      <div class="arr">→</div>
      <div class="step"><div class="si">📐</div><div class="sn">Score</div><div class="st">Bhattacharyya</div></div>
      <div class="arr">→</div>
      <div class="step"><div class="si">📊</div><div class="sn">Visualize</div><div class="st">Flask+Chart.js</div></div>
      <div class="arr">→</div>
      <div class="step"><div class="si">⚡</div><div class="sn">Deploy</div><div class="st">Railway</div></div>
    </div>
    <div class="cost">
      <div class="costnum">$0.03</div>
      <div class="costdet">
        <div class="costtitle">Total API cost to analyze 717 articles</div>
        <div class="costlist">
          <span>717 articles</span> classified by Claude Haiku<br>
          ~$0.80 per million input tokens<br>
          Avg. 100 tokens per article<br>
          <span style="color:{GREEN}">Total: under 3 cents</span><br>
          <span>Runs entirely on Railway's $5/mo free credit</span>
        </div>
      </div>
    </div>
  </div>
  <div class="foot">
    <span>Narrative Tracker · {LIVE_URL}</span><span class="mono">{GITHUB}</span>
  </div>
</div></body></html>"""))

# ── SLIDE 9: Open Source CTA ─────────────────────────────────────────────────────
SLIDES.append(("slide_09.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center}}
.gcenter{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:700px;height:700px;border-radius:50%;
  background:radial-gradient(circle,rgba(168,85,247,.14) 0%,transparent 70%)}}
.grid{{position:absolute;inset:0;
  background:linear-gradient(rgba(168,85,247,.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(168,85,247,.05) 1px,transparent 1px);
  background-size:72px 72px}}
.frame{{position:absolute;inset:36px;border:1px solid rgba(168,85,247,.2);
  border-radius:24px;pointer-events:none}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;
  color:{PURPLE};margin-bottom:20px;text-align:center}}
h2{{font-size:76px;font-weight:900;text-align:center;letter-spacing:-.025em;
  line-height:.95;margin-bottom:14px}}
.sub{{font-size:19px;color:{MUTED};text-align:center;margin-bottom:44px;
  max-width:680px;line-height:1.55}}
.cards{{display:flex;gap:18px;margin-bottom:44px}}
.cc{{background:{CARD};border:1px solid {BORDER};border-radius:14px;
  padding:26px 28px;text-align:center;width:274px}}
.ci{{font-size:34px;margin-bottom:10px}}
.ct{{font-size:15px;font-weight:700;margin-bottom:5px}}
.cu{{font-size:11px;color:{PURPLE};font-family:'Courier New',monospace;word-break:break-all}}
.foot{{position:absolute;bottom:40px;left:68px;right:68px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="gcenter"></div><div class="grid"></div><div class="frame"></div>
  <div class="eyebrow">100% Free &amp; Open Source</div>
  <h2>Fork it.<br>Extend it.</h2>
  <div class="sub">Track any conflict. Any topic. Any set of sources.<br>
    All you need is an API key and a free Railway account.</div>
  <div class="cards">
    <div class="cc">
      <div class="ci">🌐</div>
      <div class="ct">Live Dashboard</div>
      <div class="cu">{LIVE_URL}</div>
    </div>
    <div class="cc">
      <div class="ci">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="{PURPLE}">
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
        </svg>
      </div>
      <div class="ct">Source Code</div>
      <div class="cu">{GITHUB}</div>
    </div>
    <div class="cc">
      <div class="ci">👤</div>
      <div class="ct">Author</div>
      <div class="cu">{AUTHOR}</div>
    </div>
  </div>
  <div class="foot">
    <span>Built with Claude Haiku · Flask · Python · Railway</span>
    <span>March 2026</span>
  </div>
</div></body></html>"""))

# ── SLIDE 10: Closing ────────────────────────────────────────────────────────────
SLIDES.append(("slide_10.png", base() + f"""
<style>
.wrap{{width:1080px;height:1080px;position:relative;overflow:hidden}}
.bg{{position:absolute;inset:0;
  background:radial-gradient(ellipse 800px 500px at 20% 30%,rgba(240,165,0,.09) 0%,transparent 60%),
    radial-gradient(ellipse 600px 600px at 80% 80%,rgba(0,180,216,.07) 0%,transparent 60%)}}
.grid{{position:absolute;inset:0;
  background:linear-gradient(rgba(255,255,255,.022) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.022) 1px,transparent 1px);
  background-size:60px 60px}}
.lbar{{position:absolute;top:0;left:0;bottom:0;width:5px;
  background:linear-gradient(180deg,{AMBER},{BLUE},{GREEN})}}
.content{{position:absolute;top:50%;left:84px;right:84px;transform:translateY(-50%)}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.22em;color:{AMBER};
  text-transform:uppercase;margin-bottom:18px}}
h2{{font-size:80px;font-weight:900;line-height:.92;letter-spacing:-.03em;margin-bottom:24px}}
.amber{{color:{AMBER}}}
.div{{width:56px;height:4px;background:{AMBER};border-radius:2px;margin-bottom:24px}}
.body{{font-size:19px;color:rgba(240,242,245,.62);line-height:1.7;
  max-width:730px;margin-bottom:44px}}
.links{{display:flex;gap:14px}}
.lbtn{{display:inline-flex;align-items:center;gap:9px;
  border-radius:10px;padding:14px 22px;font-size:13px;font-weight:700}}
.lprimary{{background:{AMBER};color:{BG}}}
.lsecondary{{background:transparent;color:{TEXT};border:1px solid rgba(240,242,245,.22)}}
.mono{{font-family:'Courier New',monospace;font-size:12px}}
.author{{position:absolute;bottom:40px;left:84px;right:84px;
  display:flex;justify-content:space-between;font-size:11px;color:{MUTED}}}
</style>
<div class="wrap">
  <div class="bg"></div><div class="grid"></div><div class="lbar"></div>
  <div class="content">
    <div class="eyebrow">Narrative Tracker · Live Now</div>
    <h2>Read news with<br><span class="amber">divergence</span><br>awareness.</h2>
    <div class="div"></div>
    <div class="body">
      Every article you read comes with a score.<br>
      Every score comes from 717 real articles, 17 real sources,<br>
      and $0.03 of AI analysis. Open source. Forever free.
    </div>
    <div class="links">
      <div class="lbtn lprimary">🌐 <span class="mono">{LIVE_URL}</span></div>
      <div class="lbtn lsecondary">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
        </svg>
        <span class="mono">{GITHUB}</span>
      </div>
    </div>
  </div>
  <div class="author">
    <span>by Denicio Santos · {AUTHOR}</span>
    <span>March 2026</span>
  </div>
</div></body></html>"""))

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width":1080,"height":1080})
        for fname, html in SLIDES:
            await page.set_content(html, wait_until="networkidle")
            await page.wait_for_timeout(400)
            path = os.path.join(OUT, fname)
            await page.screenshot(path=path, clip={"x":0,"y":0,"width":1080,"height":1080})
            kb = os.path.getsize(path)//1024
            print(f"  [OK] {fname}  ({kb} KB)")
        await browser.close()
    print(f"\nAll {len(SLIDES)} slides → {OUT}")

asyncio.run(render())
