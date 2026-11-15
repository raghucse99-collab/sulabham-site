"""Sulabham — Group 2 Complete Pack poster (English + Telugu), 1080x1350.
usage: python3 tools/launch/make_g2pack.py  ->  cards/launch/g2pack-en.png, g2pack-te.png
Reads the number of monthly packs from ca/index.json, so re-run when a new month is added."""
import asyncio, os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'daily'))
import make_day as M
from playwright.async_api import async_playwright
ROOT = M.ROOT
OUT = os.path.join(ROOT, 'cards', 'launch')
e = M.e
NM = len(json.load(open(os.path.join(ROOT, 'ca', 'index.json'), encoding='utf-8')))
SEP = 499 + 29 * NM
T = {
 'en': dict(eb='APPSC GROUP 2 · NOTIFICATION 37/2026', h='Group 2 <span>Complete Pack</span>',
   sub='One payment. Everything for Group 2 till the exam — Telugu & English.',
   was=f'₹{SEP}+ separately', pay='one-time',
   items=[('📚', 'Prelims Pack', '13 volumes — Geography, History & Culture, Polity — from basics, 650 practice questions'),
          ('🗓️', f'All {NM} monthly current affairs packs', 'July 2026 onwards — topic-wise notes, PDFs, 50-question test each month'),
          ('➕', 'Every NEW month till the exam', 'Code reaches you on the 1st — no extra payment'),
          ('🎯', 'Real exam pattern', 'Statement-based, match-the-list, assertion–reason — with full explanations')],
   free='🎁 Free daily quiz, current affairs & weekly Group 2 mock — try first',
   how='How to buy', steps=['Pay ₹549 by UPI on the pack page', 'Send screenshot + device number on Telegram', 'Open your one unlock link — done!'],
   cta='See the pack →'),
 'te': dict(eb='APPSC గ్రూప్ 2 · నోటిఫికేషన్ 37/2026', h='గ్రూప్ 2 <span>కంప్లీట్ ప్యాక్</span>',
   sub='ఒక్కసారి చెల్లింపు. పరీక్ష వరకు గ్రూప్ 2కి కావలసినవన్నీ — తెలుగు & ఇంగ్లీష్.',
   was=f'విడిగా ₹{SEP}+', pay='ఒక్కసారి',
   items=[('📚', 'ప్రిలిమ్స్ ప్యాక్', '13 సంపుటాలు — భూగోళం, చరిత్ర & సంస్కృతి, పాలిటీ — మూలాల నుంచి, 650 ప్రాక్టీస్ ప్రశ్నలు'),
          ('🗓️', f'మొత్తం {NM} నెలల కరెంట్ అఫైర్స్ ప్యాక్‌లు', 'జూలై 2026 నుంచి — అంశాల వారీ నోట్స్, PDFలు, ప్రతి నెల 50 ప్రశ్నల టెస్ట్'),
          ('➕', 'పరీక్ష వరకు ప్రతి కొత్త నెల', 'ప్రతి నెల 1న కోడ్ మీకు వస్తుంది — అదనపు చెల్లింపు లేదు'),
          ('🎯', 'అసలు పరీక్ష విధానం', 'స్టేట్‌మెంట్, జతపరచడం, అసర్షన్–రీజన్ ప్రశ్నలు — పూర్తి వివరణలతో')],
   free='🎁 ఉచిత రోజువారీ క్విజ్, కరెంట్ అఫైర్స్ & వారపు గ్రూప్ 2 మాక్ — ముందు ప్రయత్నించండి',
   how='ఎలా కొనాలి', steps=['ప్యాక్ పేజీలో UPIతో ₹549 చెల్లించండి', 'స్క్రీన్‌షాట్ + పరికరం నంబర్ టెలిగ్రామ్‌లో పంపండి', 'మీ అన్‌లాక్ లింక్ తెరవండి — పూర్తి!'],
   cta='ప్యాక్ చూడండి →'),
}

def page(m):
    x = T[m]
    it = ''.join(f'<div class="it"><i>{a}</i><div><b>{e(b)}</b><span>{e(c)}</span></div></div>' for a, b, c in x['items'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{M.FONTS}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{width:1080px;height:1350px;font-family:{'NT,NS' if m=='te' else 'NS,NT'},sans-serif;color:#1e0629;background:#f7f2fa}}
.card{{width:1080px;height:1350px;display:flex;flex-direction:column;background:radial-gradient(circle at 88% 5%,rgba(255,212,92,.5),transparent 30%),linear-gradient(180deg,#2a0b3d 0,#5b1f7a 520px,#f7f2fa 520px)}}
.top{{padding:44px 56px 0;color:#fff;position:relative}}
.brand{{display:flex;align-items:center;gap:14px;font-family:AK;font-weight:800;font-size:38px}}
.brand img{{width:60px;height:60px;background:#fff;border-radius:14px;padding:4px}}
.eb{{display:inline-block;margin-top:24px;background:#ffd45c;color:#1b1500;font-weight:800;font-size:23px;letter-spacing:.05em;border-radius:999px;padding:8px 22px}}
h1{{font-family:AK;font-weight:800;font-size:{'86' if m=='en' else '76'}px;line-height:1.05;margin:16px 0 8px}}h1 span{{color:#f6c3ff;display:block}}
.sub{{font-size:28px;opacity:.93;max-width:700px}}
.pr{{position:absolute;right:50px;top:150px;width:290px;height:290px;border-radius:50%;background:#ffd45c;color:#1b1500;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.3);transform:rotate(-6deg)}}
.pr s{{font-size:24px;font-weight:700;opacity:.75}}.pr b{{font-family:AK;font-size:104px;line-height:1}}.pr span{{font-size:24px;font-weight:800}}
.box{{margin:40px 56px 0;background:#fff;border-radius:28px;padding:14px 30px;box-shadow:0 18px 40px rgba(42,11,61,.18)}}
.it{{display:flex;gap:20px;align-items:flex-start;padding:16px 0;border-bottom:2px solid #f0e6f5}}.it:last-child{{border:0}}
.it i{{font-style:normal;font-size:46px;flex:none;width:60px;text-align:center}}
.it b{{display:block;font-size:{'31' if m=='en' else '29'}px;color:#3d1153}}.it span{{display:block;font-size:{'23' if m=='en' else '22'}px;color:#5a4a66;margin-top:4px;line-height:1.3}}
.free{{margin:24px 56px 0;background:#fff3cf;border:3px dashed #e3a400;border-radius:22px;padding:14px 22px;font-size:25px;font-weight:800;text-align:center}}
.how{{margin:22px 56px 0;display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:14px;align-items:stretch}}
.how h3{{margin:0;font-family:AK;font-size:29px;display:flex;align-items:center;max-width:140px;line-height:1.1}}
.st{{background:#fff;border-radius:18px;padding:14px 16px;font-size:{'21' if m=='en' else '19'}px;font-weight:600;box-shadow:0 6px 16px rgba(42,11,61,.08);display:flex;gap:12px;align-items:flex-start}}
.st i{{font-style:normal;flex:none;width:38px;height:38px;border-radius:50%;background:#5b1f7a;color:#ffd45c;font-weight:800;font-size:22px;display:flex;align-items:center;justify-content:center}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:20px;background:#2a0b3d;color:#fff;padding:26px 48px;font-size:24px;font-weight:700;white-space:nowrap}}
.foot b{{background:#ffd45c;color:#1b1500;border-radius:999px;padding:12px 26px;font-size:26px}}
</style></head><body><div class="card">
<div class="top"><div class="brand"><img src="{M.LOGO}" alt="">{'సులభం' if m=='te' else 'Sulabham'}</div>
<div class="eb">{e(x['eb'])}</div><h1>{x['h']}</h1><div class="sub">{e(x['sub'])}</div>
<div class="pr"><s>{e(x['was'])}</s><b>₹549</b><span>{e(x['pay'])}</span></div></div>
<div class="box">{it}</div>
<div class="free">{e(x['free'])}</div>
<div class="how"><h3>{e(x['how'])}</h3>{''.join(f'<div class="st"><i>{i+1}</i><span>{e(s)}</span></div>' for i, s in enumerate(x['steps']))}</div>
<div class="foot"><span>👉 {M.SITE_URL}/group2-pack.html</span><b>{e(x['cta'])}</b></div>
</div></body></html>"""

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for m in ('en', 'te'):
            await pg.set_content(page(m)); await pg.wait_for_timeout(500)
            if await pg.evaluate('document.querySelector(".card").scrollHeight>1352'): print('WARNING: too tall', m)
            await pg.screenshot(path=os.path.join(OUT, f'g2pack-{m}.png'))
        await b.close()
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'compress_cards.py'), OUT], check=False)
    print('done', OUT)

if __name__ == '__main__':
    asyncio.run(main())
