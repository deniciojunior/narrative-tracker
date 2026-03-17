"""
generate_slides.py — Generates 10 1080x1080 PNG slides for LinkedIn/Instagram
Run: uv run src/generate_slides.py
"""
import asyncio, os, sys
from pathlib import Path

# ── Real data from DB (filled at generation time) ──
DATA = {
    "total_articles":    700,
    "analyzed":          717,
    "sources_count":     17,
    "date_min":          "2026-03-01",
    "date_max":          "2026-03-17",
    "dominant_frame":    "military",
    "dominant_frame_pct": 38.5,
    "dominant_tone":     "neutral",
    "dominant_tone_pct": 44.9,
    "most_divergent":    {"source": "Press TV", "score": 44.7},
    "least_divergent":   {"source": "NYT", "score": 12.2},
    "frames": {
        "military": 38.5,
        "geopolitical": 36.4,
        "humanitarian": 17.0,
        "diplomatic": 5.2,
        "terrorism": 1.8,
        "resistance": 0.7,
        "nuclear": 0.1,
    },
    "example_titles": [
        ["Middle East Eye", "Lebanese soldier killed after Israeli raid in south Lebanon"],
        ["The Guardian", "Iran's security chief, Ali Larijani, killed in airstrike, Israel says"],
        ["DW English", "Iran war overlaps with Afghanistan-Pakistan conflict"],
    ],
    "vocab_a": {"source": "Press TV", "words": ["agenda", "promise", "imminent"]},
    "vocab_b": {"source": "NY Post", "words": ["mehrabad", "crush", "despicable"]},
    "vocab": {
        "Al Jazeera": ["influenced", "suggests", "messages"],
        "BBC": ["fatigue", "uncertainty", "firepower"],
        "DW": ["hangi", "riskleri", "cine"],
        "DW English": ["suicide", "pakistan", "airfield"],
        "Fox News": ["backfires", "soldier", "readiness"],
        "France 24": ["simply", "alimardani", "associate"],
        "Haaretz": ["fewer", "firing", "ignite"],
        "Jerusalem Post": ["believes", "zarzir", "linked"],
        "Middle East Eye": ["recap", "bomb", "fears"],
        "NY Post": ["mehrabad", "crush", "despicable"],
        "NYT": ["dealing", "jailed", "minefields"],
        "Press TV": ["agenda", "promise", "imminent"],
        "RT": ["arabic", "aide", "kremlin"],
        "TASS": ["phase", "broadcaster", "launches"],
        "The Guardian": ["hold", "proxies", "regional"],
        "Times of Israel": ["apparent", "banned", "injuring"],
        "Xinhua": ["carburant", "complexes", "stockage"],
    },
}

OUT_DIR = Path("marketing/slides")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&family=IBM+Plex+Serif:ital@1&display=swap"

BASE_CSS = f"""
  @import url('{FONTS}');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px; height: 1080px; overflow: hidden;
    background: #080C10;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #E6EDF3;
    position: relative;
  }}
  .grid-bg {{
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(33,38,45,0.4) 1px, transparent 1px),
      linear-gradient(90deg, rgba(33,38,45,0.4) 1px, transparent 1px);
    background-size: 40px 40px;
  }}
  .content {{ position: relative; z-index: 1; padding: 72px; height: 100%; display: flex; flex-direction: column; }}
  .mono {{ font-family: 'IBM Plex Mono', monospace; }}
  .serif {{ font-family: 'IBM Plex Serif', serif; font-style: italic; }}
  .amber {{ color: #D29922; }}
  .green {{ color: #3FB950; }}
  .red   {{ color: #F85149; }}
  .muted {{ color: #8B949E; }}
  .tag {{
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
    border: 1px solid #30363D; padding: 4px 10px; color: #8B949E;
    margin-bottom: 24px;
  }}
  .badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;
    border: 1px solid currentColor; padding: 6px 14px; border-radius: 20px;
  }}
  .footer {{
    margin-top: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; color: #484F58;
    display: flex; justify-content: space-between; align-items: flex-end;
  }}
"""

def slide_html(body_content: str) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>{BASE_CSS}</style>
</head><body>
<div class="grid-bg"></div>
<div class="content">
{body_content}
</div>
</body></html>"""

# ── Slide definitions ──────────────────────────────────────────────────────

def s01_cover():
    d = DATA
    frame_pct = d["dominant_frame_pct"]
    return slide_html(f"""
  <div class="tag">Narrative Tracker · US-Israel-Iran War 2026</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div class="mono" style="font-size:13px;color:#8B949E;letter-spacing:0.1em;margin-bottom:16px">A MESMA GUERRA.</div>
    <h1 class="serif" style="font-size:86px;line-height:1.05;color:#E6EDF3;margin-bottom:8px">
      {d['sources_count']} Narrativas<span class="amber">.</span>
    </h1>
    <p style="font-size:18px;color:#8B949E;font-weight:300;margin-bottom:48px">
      Como {d['sources_count']} veículos globais cobrem o mesmo conflito — analisado por IA
    </p>
    <div style="display:flex;gap:24px">
      <div style="background:#0D1117;border:1px solid #21262D;padding:20px 28px">
        <div class="mono amber" style="font-size:40px;font-weight:600">{d['analyzed']}</div>
        <div class="mono" style="font-size:11px;color:#8B949E;letter-spacing:0.1em;margin-top:4px">ARTIGOS ANALISADOS</div>
      </div>
      <div style="background:#0D1117;border:1px solid #21262D;padding:20px 28px">
        <div class="mono" style="font-size:40px;font-weight:600;color:#3FB950">{d['sources_count']}</div>
        <div class="mono" style="font-size:11px;color:#8B949E;letter-spacing:0.1em;margin-top:4px">FONTES MONITORADAS</div>
      </div>
      <div style="background:#0D1117;border:1px solid #21262D;padding:20px 28px">
        <div class="mono" style="font-size:40px;font-weight:600;color:#F85149">{frame_pct}%</div>
        <div class="mono" style="font-size:11px;color:#8B949E;letter-spacing:0.1em;margin-top:4px">FRAME {d['dominant_frame'].upper()}</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>github.com/[SEU_USUARIO]/narrative-tracker</span>
    <span>{d['date_min']} → {d['date_max']}</span>
  </div>
""")

def s02_problem():
    d = DATA
    titles = d["example_titles"]
    rows = ""
    colors = ["#F85149", "#D29922", "#3FB950"]
    for i, (src, title) in enumerate(titles[:3]):
        c = colors[i]
        # Truncate title if too long
        t = title[:90] + "…" if len(title) > 90 else title
        rows += f"""
    <div style="border-left:3px solid {c};padding:16px 20px;background:#0D1117;margin-bottom:12px">
      <div class="mono" style="font-size:10px;color:{c};letter-spacing:0.1em;margin-bottom:6px">{src.upper()}</div>
      <div style="font-size:17px;line-height:1.4;color:#E6EDF3">{t}</div>
    </div>"""
    return slide_html(f"""
  <div class="tag">O Problema</div>
  <h2 class="serif" style="font-size:52px;line-height:1.1;margin-bottom:12px">
    O mesmo evento.<br>Três realidades <span class="amber">diferentes</span>.
  </h2>
  <p style="font-size:15px;color:#8B949E;margin-bottom:32px">
    Todos os artigos abaixo cobrem o mesmo conflito. Publicados no mesmo período.
  </p>
  {rows}
  <div style="margin-top:20px;padding:16px 20px;border:1px solid #21262D;background:#0D1117">
    <span class="mono" style="font-size:12px;color:#8B949E">
      Isso é <span style="color:#D29922">framing</span> — a escolha de como enquadrar a narrativa molda a percepção sem mentir abertamente.
    </span>
  </div>
  <div class="footer"><span>Narrative Tracker · {d['analyzed']} artigos analisados</span></div>
""")

def s03_solution():
    d = DATA
    steps = [
        ("#3FB950", "01", "Coleta", f"RSS + GDELT · {d['sources_count']} fontes · atualização horária"),
        ("#58A6FF", "02", "Análise IA", f"Claude Haiku · {d['analyzed']} artigos · frame + tom + vocab"),
        ("#D29922", "03", "Score", "Distância de Bhattacharyya · 0-100 · por fonte e por dia"),
        ("#E6EDF3", "04", "Dashboard", "Flask + Chart.js · filtros · comparador · tour guiado"),
    ]
    rows = ""
    for color, num, title, desc in steps:
        rows += f"""
    <div style="display:flex;align-items:center;gap:20px;padding:18px;background:#0D1117;border:1px solid #21262D;margin-bottom:10px">
      <div class="mono" style="font-size:32px;font-weight:600;color:{color};min-width:56px">{num}</div>
      <div>
        <div style="font-size:18px;font-weight:600;color:{color};margin-bottom:3px">{title}</div>
        <div class="mono" style="font-size:12px;color:#8B949E">{desc}</div>
      </div>
    </div>"""
    return slide_html(f"""
  <div class="tag">A Solução</div>
  <h2 class="serif" style="font-size:52px;margin-bottom:8px">
    Pipeline de <span class="amber">4 passos</span>
  </h2>
  <p style="font-size:15px;color:#8B949E;margin-bottom:28px">Do RSS ao insight em minutos. 100% open source.</p>
  {rows}
  <div class="footer">
    <span>Python · Flask · SQLite · Claude Haiku · Chart.js</span>
    <span>Open Source · MIT License</span>
  </div>
""")

def s04_cost():
    return slide_html(f"""
  <div class="tag">O Custo Real</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">
    <div class="mono" style="font-size:140px;font-weight:600;color:#3FB950;line-height:1">$0.03</div>
    <div style="font-size:22px;color:#8B949E;margin-top:16px;margin-bottom:48px">
      Para analisar <span style="color:#E6EDF3;font-weight:600">{DATA['analyzed']} artigos</span> com IA
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;width:100%">
      <div style="background:#0D1117;border:1px solid #21262D;padding:20px">
        <div class="mono amber" style="font-size:28px;font-weight:600">$0.000042</div>
        <div class="mono" style="font-size:11px;color:#8B949E;margin-top:6px">POR ARTIGO ANALISADO</div>
      </div>
      <div style="background:#0D1117;border:1px solid #21262D;padding:20px">
        <div class="mono" style="font-size:28px;font-weight:600;color:#58A6FF">Claude Haiku</div>
        <div class="mono" style="font-size:11px;color:#8B949E;margin-top:6px">MODELO MAIS EFICIENTE</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Narrative Tracker · análise automatizada de mídia</span>
    <span>Anthropic API</span>
  </div>
""")

def s05_methodology():
    return slide_html(f"""
  <div class="tag">Metodologia · Score de Divergência</div>
  <h2 class="serif" style="font-size:52px;margin-bottom:8px">
    Bhattacharyya <span class="amber">Distance</span>
  </h2>
  <p style="font-size:15px;color:#8B949E;margin-bottom:36px">
    Medida estatística de sobreposição entre distribuições de probabilidade.<br>
    Comparamos a distribuição de frames de cada fonte com a média global diária.
  </p>
  <div style="margin-bottom:32px">
    {"".join([
      f'<div style="margin-bottom:14px;display:flex;align-items:center;gap:16px">'
      f'<div class="mono" style="font-size:13px;color:#8B949E;min-width:60px">{label}</div>'
      f'<div style="flex:1;background:#21262D;height:12px;border-radius:2px">'
      f'<div style="width:{pct}%;height:100%;background:{color};border-radius:2px"></div>'
      f'</div>'
      f'<div class="mono" style="font-size:13px;color:{color};min-width:80px;text-align:right">{desc}</div>'
      f'</div>'
      for label, pct, color, desc in [
        ("Score 0", 2, "#3FB950", "= média global"),
        ("Score 20", 20, "#3FB950", "baixa divergência"),
        ("Score 40", 40, "#D29922", "divergência moderada"),
        ("Score 60", 60, "#D29922", "divergência alta"),
        ("Score 80", 80, "#F85149", "muito divergente"),
        ("Score 100", 100, "#F85149", "= outlier extremo"),
      ]
    ])}
  </div>
  <div style="background:#0D1117;border:1px solid #30363D;padding:20px">
    <div class="mono" style="font-size:12px;color:#8B949E;line-height:1.7">
      <span style="color:#D29922">50%</span> concordância de frame dominante diário &nbsp;·&nbsp;
      <span style="color:#D29922">25%</span> distribuição de frames (Bhattacharyya) &nbsp;·&nbsp;
      <span style="color:#D29922">25%</span> distribuição de tons
    </div>
  </div>
  <div class="footer"><span>Fórmula completa no README · github.com/[SEU_USUARIO]/narrative-tracker</span></div>
""")

def s06_most_divergent():
    d = DATA
    md = d["most_divergent"]
    src = md["source"]
    score = md["score"]
    words = d["vocab"].get(src, ["N/A", "N/A", "N/A"])[:3]
    return slide_html(f"""
  <div class="tag">Fonte Mais Divergente</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div class="mono red" style="font-size:13px;letter-spacing:0.1em;margin-bottom:12px">SCORE MÉDIO MAIS ALTO</div>
    <h2 style="font-size:64px;font-weight:600;color:#F85149;margin-bottom:4px">{src}</h2>
    <div class="mono" style="font-size:96px;font-weight:600;color:#F85149;line-height:1;margin-bottom:24px">{score}</div>
    <p style="font-size:16px;color:#8B949E;margin-bottom:32px">
      Score {score}/100 de divergência média — o mais distante da narrativa global
    </p>
    <div style="margin-bottom:24px">
      <div class="mono" style="font-size:11px;color:#8B949E;letter-spacing:0.1em;margin-bottom:12px">VOCABULÁRIO CARACTERÍSTICO</div>
      <div style="display:flex;gap:12px">
        {"".join([f'<span class="mono" style="font-size:20px;font-weight:600;color:#F85149;background:#0D1117;border:1px solid #F8514940;padding:10px 18px">{w}</span>' for w in words])}
      </div>
    </div>
    <div style="background:#0D1117;border:1px solid #21262D;padding:16px">
      <div class="mono" style="font-size:12px;color:#8B949E">
        Termos com maior score TF-IDF — palavras que <span style="color:#E6EDF3">{src}</span> usa muito mais do que as outras fontes
      </div>
    </div>
  </div>
  <div class="footer"><span>Narrative Tracker · {d['analyzed']} artigos · {d['sources_count']} fontes</span></div>
""")

def s07_least_divergent():
    d = DATA
    ld = d["least_divergent"]
    src = ld["source"]
    score = ld["score"]
    words = d["vocab"].get(src, ["N/A", "N/A", "N/A"])[:3]
    return slide_html(f"""
  <div class="tag">Fonte Mais Neutra</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div class="mono green" style="font-size:13px;letter-spacing:0.1em;margin-bottom:12px">SCORE MÉDIO MAIS BAIXO</div>
    <h2 style="font-size:64px;font-weight:600;color:#3FB950;margin-bottom:4px">{src}</h2>
    <div class="mono" style="font-size:96px;font-weight:600;color:#3FB950;line-height:1;margin-bottom:24px">{score}</div>
    <p style="font-size:16px;color:#8B949E;margin-bottom:32px">
      Score {score}/100 de divergência média — o mais próximo da narrativa consensual global
    </p>
    <div style="margin-bottom:24px">
      <div class="mono" style="font-size:11px;color:#8B949E;letter-spacing:0.1em;margin-bottom:12px">VOCABULÁRIO CARACTERÍSTICO</div>
      <div style="display:flex;gap:12px">
        {"".join([f'<span class="mono" style="font-size:20px;font-weight:600;color:#3FB950;background:#0D1117;border:1px solid #3FB95040;padding:10px 18px">{w}</span>' for w in words])}
      </div>
    </div>
    <div style="background:#0D1117;border:1px solid #21262D;padding:16px">
      <div class="mono" style="font-size:12px;color:#8B949E">
        Proximidade à média não equivale a precisão. Significa apenas que o enquadramento está alinhado com o consenso dos {d['sources_count']} veículos monitorados.
      </div>
    </div>
  </div>
  <div class="footer"><span>Narrative Tracker · {d['analyzed']} artigos · {d['sources_count']} fontes</span></div>
""")

def s08_frames():
    d = DATA
    frames = d["frames"]  # dict frame -> pct
    FRAME_COLORS = {
        "military":     "#F85149",
        "geopolitical": "#D29922",
        "humanitarian": "#58A6FF",
        "terrorism":    "#FF7B72",
        "resistance":   "#A371F7",
        "nuclear":      "#3FB950",
        "diplomatic":   "#8B949E",
    }
    bars = ""
    for frame, pct in list(frames.items())[:7]:
        color = FRAME_COLORS.get(frame, "#8B949E")
        bars += f"""
    <div style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span class="mono" style="font-size:12px;color:{color};letter-spacing:0.06em;text-transform:uppercase">{frame}</span>
        <span class="mono" style="font-size:12px;color:{color}">{pct}%</span>
      </div>
      <div style="background:#21262D;height:16px;border-radius:2px">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:2px;opacity:0.85"></div>
      </div>
    </div>"""
    return slide_html(f"""
  <div class="tag">Distribuição de Frames · {d['analyzed']} artigos</div>
  <h2 class="serif" style="font-size:52px;margin-bottom:8px">
    Como a guerra é <span class="amber">enquadrada</span>
  </h2>
  <p style="font-size:15px;color:#8B949E;margin-bottom:28px">
    Cada artigo é classificado em um dos 7 frames narrativos pela IA.
  </p>
  {bars}
  <div class="footer">
    <span>Narrative Tracker · Claude Haiku · {d['date_min']} → {d['date_max']}</span>
    <span>Dominante: <span style="color:#D29922">{d['dominant_frame']} ({d['dominant_frame_pct']}%)</span></span>
  </div>
""")

def s09_lesson():
    d = DATA
    lessons = [
        ("Narrativa não é Mentira", f"Uma fonte pode ter score {d['most_divergent']['score']} de divergência sendo mais precisa — ou mais tendenciosa. O score mede diferença, não qualidade."),
        ("O frame revela a agenda", f"{d['dominant_frame_pct']}% dos artigos usam o frame '{d['dominant_frame']}'. A escolha de frame é a escolha do que importa."),
        ("Dados mudam percepção", f"Ao ver {d['analyzed']} artigos lado a lado, padrões invisíveis emergem. BI aplicado à mídia."),
    ]
    rows = ""
    colors = ["#D29922", "#58A6FF", "#3FB950"]
    for i, (title, body) in enumerate(lessons):
        c = colors[i]
        rows += f"""
    <div style="display:flex;gap:20px;padding:20px;background:#0D1117;border:1px solid #21262D;margin-bottom:12px">
      <div class="mono" style="font-size:28px;font-weight:600;color:{c};min-width:40px">{i+1:02d}</div>
      <div>
        <div style="font-size:18px;font-weight:600;color:{c};margin-bottom:6px">{title}</div>
        <div style="font-size:14px;color:#8B949E;line-height:1.5">{body}</div>
      </div>
    </div>"""
    return slide_html(f"""
  <div class="tag">Lição de BI de Mídia</div>
  <h2 class="serif" style="font-size:52px;margin-bottom:28px">
    O que os dados <span class="amber">revelam</span>
  </h2>
  {rows}
  <div style="margin-top:4px;padding:16px 20px;border:1px solid #D2992240;background:#D2992208">
    <div class="mono" style="font-size:13px;color:#D29922">
      "Toda cobertura de conflito é uma escolha editorial. O objetivo não é julgar — é tornar visível."
    </div>
  </div>
  <div class="footer"><span>Narrative Tracker · análise de mídia orientada a dados</span></div>
""")

def s10_cta():
    d = DATA
    return slide_html(f"""
  <div class="tag">Narrative Tracker · Open Source</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center">
    <div class="serif" style="font-size:64px;line-height:1.1;margin-bottom:24px">
      Como <span class="amber">você</span> lê<br>as notícias agora?
    </div>
    <p style="font-size:17px;color:#8B949E;margin-bottom:48px;max-width:700px">
      Depois de analisar {d['analyzed']} artigos de {d['sources_count']} fontes, fica impossível não notar os padrões.
    </p>
    <div style="display:flex;gap:16px;margin-bottom:40px">
      <div style="background:#0D1117;border:1px solid #D29922;padding:16px 32px">
        <div class="mono amber" style="font-size:16px;font-weight:600">Star no GitHub</div>
        <div class="mono" style="font-size:11px;color:#8B949E;margin-top:4px">github.com/[SEU_USUARIO]/narrative-tracker</div>
      </div>
      <div style="background:#0D1117;border:1px solid #3FB950;padding:16px 32px">
        <div class="mono green" style="font-size:16px;font-weight:600">Live Demo</div>
        <div class="mono" style="font-size:11px;color:#8B949E;margin-top:4px">your-app.up.railway.app</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
      {"".join([f'<span class="badge muted" style="font-size:11px">{h}</span>' for h in ["#AnaliseDeMidia","#IA","#OpenSource","#DataJournalism","#NarrativeTracker"]])}
    </div>
  </div>
  <div class="footer">
    <span>Feito com Python + Claude Haiku · MIT License · 2026</span>
    <span>{d['analyzed']} artigos · {d['sources_count']} fontes</span>
  </div>
""")

# ── Main generator ──────────────────────────────────────────────────────────

async def generate():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Installing playwright...")
        os.system("uv add playwright")
        os.system("uv run playwright install chromium")
        from playwright.async_api import async_playwright

    slides = [
        ("01", s01_cover()),
        ("02", s02_problem()),
        ("03", s03_solution()),
        ("04", s04_cost()),
        ("05", s05_methodology()),
        ("06", s06_most_divergent()),
        ("07", s07_least_divergent()),
        ("08", s08_frames()),
        ("09", s09_lesson()),
        ("10", s10_cta()),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})

        for num, html in slides:
            path = OUT_DIR / f"slide_{num}.png"
            await page.set_content(html, wait_until="networkidle")
            # Wait for fonts
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(path), clip={"x":0,"y":0,"width":1080,"height":1080})
            size_kb = path.stat().st_size // 1024
            print(f"slide_{num}.png ({size_kb} KB)")

        await browser.close()
    print(f"\nAll 10 slides saved to {OUT_DIR}/")

if __name__ == "__main__":
    asyncio.run(generate())
