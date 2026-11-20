"""Poster for the 'Current Affairs 2026 — Topic-wise' tile: cards/launch/ca-topics-{en,te}.png (1080x1350).
Reads caps/index.json to mark which topics are ready."""
import json, os, sys, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'daily'))
import make_day as M
PLAN = [("indices-2026","📊","Indices & Reports","సూచీలు & నివేదికలు"),("summits-2026","🤝","Summits & Conferences","సదస్సులు & సమావేశాలు"),
 ("schemes-2026","📜","Govt Schemes (Centre + AP)","ప్రభుత్వ పథకాలు (కేంద్రం + ఏపీ)"),("awards-2026","🏅","Awards & Honours","అవార్డులు & పురస్కారాలు"),
 ("persons-2026","👤","Persons in News","వార్తల్లో వ్యక్తులు"),("sports-2026","🏟️","Sports","క్రీడలు"),
 ("scitech-2026","🚀","Science, Tech & Space","సైన్స్, టెక్ & అంతరిక్షం"),("defence-2026","🛡️","Defence & Security","రక్షణ & భద్రత"),
 ("economy-2026","💰","Economy, Budget & Banking","ఆర్థికం, బడ్జెట్ & బ్యాంకింగ్"),("environment-2026","🌿","Environment & Climate","పర్యావరణం & వాతావరణం"),
 ("ap-2026","🏛️","Andhra Pradesh Special","ఆంధ్రప్రదేశ్ ప్రత్యేకం"),("days-2026","📅","Important Days & Books","ముఖ్య దినాలు & పుస్తకాలు")]
def html(m, live):
    T = lambda en, te: en if m == 'en' else te
    rows = ''.join(f'<div class="r {"on" if pid in live else ""}"><span>{ic}</span><b>{T(en,te)}</b><i>{(T("✅ Ready","✅ సిద్ధం") + f" · {live[pid]} MCQs") if pid in live else T("⏳ Coming","⏳ త్వరలో")}</i></div>' for pid, ic, en, te in PLAN)
    return f'''<html><head><meta charset="utf-8"><style>{M.FONTS}
*{{box-sizing:border-box}}body{{margin:0;width:1080px;height:1350px;font-family:{'NT,NS' if m=='te' else 'NS,NT'},sans-serif;background:linear-gradient(160deg,#2a0b3d,#5b1f7a 60%,#7a2c8f);color:#fff;padding:56px 60px}}
.k{{display:inline-block;background:#ffd45c;color:#1b1500;font-weight:800;border-radius:999px;padding:8px 22px;font-size:28px}}
h1{{font-family:AK,{'NT' if m=='te' else 'NS'};font-size:{70 if m=='en' else 58}px;line-height:1.12;margin:22px 0 8px}}p.s{{font-size:28px;opacity:.9;margin:0 0 26px}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.r{{background:rgba(255,255,255,.1);border:2px dashed rgba(255,255,255,.3);border-radius:18px;padding:14px 16px;display:grid;grid-template-columns:52px 1fr;align-items:center}}
.r span{{font-size:38px;grid-row:span 2}}.r b{{font-size:{27 if m=='en' else 25}px;line-height:1.2}}.r i{{font-style:normal;font-size:21px;opacity:.85}}.r.on{{background:#eefaf2;color:#0f3d24;border:2px solid #1f8a4c}}.r.on i{{font-weight:800;opacity:1;color:#1f6f4a}}
.f{{display:flex;gap:16px;margin-top:28px;align-items:center}}.p{{background:#ffd45c;color:#1b1500;border-radius:22px;padding:14px 24px;font-weight:800;font-size:34px;line-height:1.1;text-align:center}}.p small{{display:block;font-size:20px}}
.f ul{{margin:0;padding-left:26px;font-size:24px;line-height:1.45}}.u{{margin-top:22px;font-size:30px;font-weight:800;text-align:center;letter-spacing:.5px}}
</style></head><body><span class="k">APPSC Group 1 & 2</span>
<h1>📰 {T("Current Affairs 2026<br>Topic-wise","కరెంట్ అఫైర్స్ 2026<br>అంశాల వారీగా")}</h1><p class="s">{T("January – November 2026 · Telugu & English","జనవరి – నవంబర్ 2026 · తెలుగు & ఇంగ్లీష్")}</p>
<div class="g">{rows}</div>
<div class="f"><div class="p">₹49<small>{T("per topic","ఒక్కో అంశం")}</small></div><div class="p">₹499<small>{T("ALL topics","అన్ని అంశాలు")}</small></div>
<ul><li>{T("Facts verified, mistakes corrected","వాస్తవాలు నిర్ధారితం, పొరపాట్లు సరిదిద్దాం")}</li><li>{T("Notes PDF + online practice MCQs","నోట్స్ PDF + ఆన్‌లైన్ ప్రాక్టీస్ ప్రశ్నలు")}</li><li>{T("Free preview before you pay","చెల్లించే ముందు ఉచిత నమూనా")}</li></ul></div>
<div class="u">sulabham.in/caps.html</div></body></html>'''
async def main():
    live = {c['id']: c['mcq'] for c in json.load(open(os.path.join(ROOT, 'caps', 'index.json'), encoding='utf-8'))}
    out = os.path.join(ROOT, 'cards', 'launch'); os.makedirs(out, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for m in ('en', 'te'):
            await pg.set_content(html(m, live)); await pg.wait_for_timeout(500)
            await pg.screenshot(path=os.path.join(out, f'ca-topics-{m}.png')); print('wrote', m)
        await b.close()
asyncio.run(main())
