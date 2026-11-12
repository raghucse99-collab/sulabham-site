"""AEE course poster, 1080x1350 -> cards/aee/aee-poster.png.   usage: python3 tools/aee/make_poster.py (from repo root)"""
import asyncio, os
from playwright.async_api import async_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
F = 'file://' + os.path.join(ROOT, 'tools', 'daily', 'fonts')
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anek;font-weight:800;src:url({F}/anek-telugu-latin-800-normal.woff2)}}
@font-face{{font-family:Anek;font-weight:700;src:url({F}/anek-telugu-latin-700-normal.woff2)}}
@font-face{{font-family:Noto;font-weight:400;src:url({F}/noto-sans-latin-400-normal.woff2)}}
@font-face{{font-family:Noto;font-weight:600;src:url({F}/noto-sans-latin-600-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;font-family:Noto,sans-serif;color:#fff;position:relative;overflow:hidden;
 background:radial-gradient(circle at 92% 4%,rgba(255,157,61,.6),transparent 34%),radial-gradient(circle at 0% 100%,rgba(92,140,255,.38),transparent 42%),linear-gradient(145deg,#141926,#252f4d 55%,#374878)}}
body::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:54px 54px}}
.in{{position:relative;padding:60px 64px;height:100%;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:16px;font-family:Anek;font-weight:800;font-size:44px}}
.top img{{width:64px;height:64px}}.top b{{color:#ffbe7a}}.top span.r{{margin-left:auto;font-family:Noto;font-weight:600;font-size:24px;opacity:.9}}
.eb{{align-self:flex-start;margin-top:44px;background:#ff9d3d;color:#1d1200;font-weight:600;font-size:26px;letter-spacing:.05em;border-radius:999px;padding:10px 26px;text-transform:uppercase}}
h1{{font-family:Anek;font-weight:800;font-size:112px;line-height:1.0;margin-top:22px;letter-spacing:-.01em}}
h1 em{{font-style:normal;color:#ffbe7a;display:block}}
.sub{{font-size:32px;line-height:1.35;margin-top:14px;max-width:820px;opacity:.95}}
.chips{{display:flex;gap:12px;margin-top:26px}}
.chips span{{background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.35);border-radius:999px;padding:8px 22px;font-weight:600;font-size:26px}}
ul{{list-style:none;margin-top:34px;display:grid;gap:15px}}
li{{position:relative;padding-left:58px;font-size:33px;line-height:1.25}}
li::before{{content:"";position:absolute;left:0;top:2px;width:38px;height:38px;border-radius:50%;background:#ff9d3d}}
li::after{{content:"";position:absolute;left:12px;top:10px;width:13px;height:20px;border:solid #1d1200;border-width:0 5px 5px 0;transform:rotate(40deg) scale(.8)}}
.row{{margin-top:auto;display:flex;align-items:flex-end;gap:30px}}
.price{{font-family:Anek;font-weight:800;font-size:170px;line-height:.82;color:#ffbe7a}}
.pt{{font-size:28px;font-weight:600;line-height:1.3;padding-bottom:10px}}
.free{{margin-left:auto;background:#1f8f4e;border-radius:22px;padding:16px 26px;font-weight:600;font-size:27px;line-height:1.3;text-align:center}}
.foot{{margin-top:30px;background:#fff;color:#16324a;border-radius:24px;padding:20px 28px;display:flex;align-items:center;font-size:29px;font-weight:600}}
.foot b{{font-family:Anek;font-weight:800;font-size:40px;margin-left:auto;color:#141926}}
svg.art{{position:absolute;right:44px;top:64px;width:300px;opacity:.95}}
</style></head><body>
<svg class="art" viewBox="0 0 240 200"><defs><linearGradient id="ag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffc27a"/><stop offset="1" stop-color="#ff8a2a"/></linearGradient></defs>
<circle cx="120" cy="100" r="92" fill="rgba(255,255,255,.06)" stroke="rgba(255,255,255,.35)" stroke-width="1.5" stroke-dasharray="4 5"/>
<path d="M20 150h200" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M30 150Q120 60 210 150" fill="none" stroke="url(#ag)" stroke-width="6" stroke-linecap="round"/>
<g stroke="#fff" stroke-width="2.5" opacity=".9"><path d="M60 150v-28M90 150v-47M120 150v-45M150 150v-47M180 150v-28"/></g>
<path d="M48 150v26M192 150v26" stroke="#fff" stroke-width="7" stroke-linecap="round"/><path d="M34 180q14-8 28 0t28 0 28 0 28 0 28 0 28 0" fill="none" stroke="#7fb2ff" stroke-width="3" stroke-linecap="round"/>
<g transform="translate(88 22)"><path d="M8 44a24 24 0 0 1 48 0z" fill="url(#ag)" stroke="#1d1200" stroke-width="2"/><rect x="2" y="44" width="60" height="8" rx="4" fill="#ffd45c" stroke="#1d1200" stroke-width="2"/><path d="M28 20v24M36 20v24" stroke="#1d1200" stroke-width="2"/></g></svg>
<div class="in">
<div class="top"><img src="file://{ROOT}/sulabham-icon.svg"><span>Sula<b>bham</b></span></div>
<span class="eb">APPSC AEE 2026 · Notification 27/2026</span>
<h1>AEE<em>Complete Course</em></h1>
<p class="sub">Every subject from the basics — understand first, then remember.</p>
<div class="chips"><span>Civil</span><span>Mechanical</span><span>Electrical</span><span>503 posts</span></div>
<ul><li>Notes from zero, with real photos and diagrams</li><li>2023 questions mapped to every topic</li><li>Tap-to-check quiz after every topic</li><li>50-question test after every module</li><li>Memory codes + Notebook pages for revision</li></ul>
<div class="row"><div class="price">₹499</div><div class="pt">one payment<br>till the exam</div><div class="free">2 modules FREE<br>try before you pay</div></div>
<div class="foot">Start free today<b>sulabham.in/aee.html</b></div>
</div></body></html>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport=dict(width=1080, height=1350))
        tmp = os.path.join(ROOT, 'cards', 'aee', '_poster.html'); open(tmp, 'w', encoding='utf-8').write(HTML)
        await pg.goto('file://' + tmp); await pg.wait_for_timeout(1200); os.remove(tmp)
        await pg.screenshot(path=os.path.join(ROOT, 'cards', 'aee', 'aee-poster.png')); await b.close()
asyncio.run(main())
