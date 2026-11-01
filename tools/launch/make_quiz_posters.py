"""Sulabham — advertising posters for the free quiz contest + Group 2 mock test (English + Telugu), 1080x1350.
usage: python3 tools/launch/make_quiz_posters.py
  -> cards/launch/quiz-mock-{en,te}.png   (both tests on one poster)
     cards/launch/ca-quiz-{en,te}.png     (only the current affairs grand quiz)
     cards/launch/g2-mock-{en,te}.png     (only the Group 2 mock test)
Reads the newest tests from mocks/index.json, so re-run it when a new quiz / mock is added."""
import asyncio, os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'daily'))
import make_day as M
from playwright.async_api import async_playwright
ROOT = M.ROOT
OUT = os.path.join(ROOT, 'cards', 'launch')
e = M.e

IX = json.load(open(os.path.join(ROOT, 'mocks', 'index.json'), encoding='utf-8'))
CA = next(m for m in IX if m.get('kind') == 'ca')
G2 = next(m for m in IX if m.get('kind') != 'ca')

T = {
 'en': dict(brand='Sulabham', eb='⭐ NEW · FREE', h='Quiz contest is on!', hg='New free mock test!', h1='Current Affairs Grand Quiz', h2='Group 2 Prelims Mock Test',
   sub='APPSC Group 1 & 2 · Telugu + English · free for everyone',
   ca_k='Monthly contest', g2_k='Weekly full mock · APPSC Group 2',
   q='questions', mn='minutes', neg='per wrong answer',
   ca_l=['Whole month’s current affairs in one test', 'Rank + leaderboard', 'Answers with explanations'],
   g2_l=['History · Geography · Society · Current Affairs · Mental Ability (30 each)', 'Real exam pattern with timer', 'Section-wise analysis + explanations'],
   cta='Take it free →', share='Share with your friends 🙏'),
 'te': dict(brand='సులభం', eb='⭐ కొత్తది · ఉచితం', h='క్విజ్ పోటీ జరుగుతోంది!', hg='కొత్త ఉచిత మాక్ టెస్ట్!', h1='కరెంట్ అఫైర్స్ గ్రాండ్ క్విజ్', h2='గ్రూప్ 2 ప్రిలిమ్స్ మాక్ టెస్ట్',
   sub='APPSC గ్రూప్ 1 & 2 · తెలుగు + English · అందరికీ ఉచితం',
   ca_k='నెలవారీ పోటీ', g2_k='వారపు పూర్తి మాక్ · APPSC గ్రూప్ 2',
   q='ప్రశ్నలు', mn='నిమిషాలు', neg='ప్రతి తప్పుకు',
   ca_l=['నెల మొత్తం కరెంట్ అఫైర్స్ ఒకే టెస్ట్‌లో', 'ర్యాంక్ + లీడర్‌బోర్డ్', 'వివరణలతో జవాబులు'],
   g2_l=['చరిత్ర · భూగోళం · సమాజం · కరెంట్ అఫైర్స్ · మెంటల్ ఎబిలిటీ (ఒక్కోటి 30)', 'అసలు పరీక్ష తరహా, టైమర్‌తో', 'విభాగాల వారీ విశ్లేషణ + వివరణలు'],
   cta='ఉచితంగా రాయండి →', share='మీ స్నేహితులకు పంపండి 🙏'),
}

def L(o, m): return o.get(m) or o['en']

def block(m, kind, big):
    x = T[m]
    t, cls, k, lst = (CA, 'ca', x['ca_k'], x['ca_l']) if kind == 'ca' else (G2, 'g2', x['g2_k'], x['g2_l'])
    stats = [(str(t.get('q', len(json.load(open(os.path.join(ROOT, 'mocks', t['id'] + '.json')))['qs']))), x['q']),
             (str(t.get('mins', 150)), x['mn']), ('−⅓', x['neg'])]
    return f"""<div class="b {cls}{' big' if big else ''}"><div class="bk"><span class="star">⭐ NEW</span>{e(k)}</div>
<div class="bh">{e(L(t['title'], m))}</div>
<div class="stats">{''.join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in stats)}</div>
<ul>{''.join(f'<li>{e(i)}</li>' for i in lst)}</ul>
<div class="go"><b>{e(x['cta'])}</b></div></div>"""

def page(m, kinds):
    x = T[m]; big = len(kinds) == 1
    head = x['h'] if len(kinds) == 2 else (x['h'] if kinds[0] == 'ca' else x['hg'])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{M.FONTS}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{width:1080px;height:1350px;font-family:{'NT,NS' if m=='te' else 'NS,NT'},sans-serif;color:#16324a}}
.card{{width:1080px;height:1350px;display:flex;flex-direction:column;position:relative;overflow:hidden;
 background:radial-gradient(circle at 88% 6%,rgba(255,212,92,.6),transparent 30%),linear-gradient(160deg,#5c1530,#9e2a2b 45%,#d9601a)}}
.card::after{{content:"";position:absolute;right:-120px;top:150px;width:420px;height:420px;border-radius:50%;border:40px dashed rgba(255,255,255,.08)}}
.top{{padding:38px 56px 0;color:#fff;position:relative;z-index:1}}
.brand{{display:flex;align-items:center;gap:14px;font-family:AK;font-weight:800;font-size:38px}}
.brand img{{width:60px;height:60px;background:#fff;border-radius:14px;padding:4px}}
.eb{{display:inline-block;margin-top:24px;background:#ffd45c;color:#1b1500;font-weight:800;font-size:28px;letter-spacing:.06em;border-radius:999px;padding:8px 24px}}
h1{{font-family:AK;font-weight:800;font-size:{'80' if m=='en' else '72'}px;line-height:1.08;margin:14px 0 6px;max-width:830px}}
.sub{{font-size:28px;opacity:.95;font-weight:600}}
.bigstar{{position:absolute;right:56px;top:40px;font-size:120px;filter:drop-shadow(0 8px 18px rgba(0,0,0,.3))}}
.blocks{{flex:1;display:flex;flex-direction:column;gap:20px;padding:26px 56px 0;position:relative;z-index:1}}
.b{{flex:1;background:#fff;border-radius:30px;padding:26px 30px 22px;box-shadow:0 18px 40px rgba(0,0,0,.28);display:flex;flex-direction:column;border-top:14px solid #e3a400}}
.b.g2{{border-top-color:#1d4f91}}
.bk{{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#52677a}}
.star{{background:#ffd45c;color:#1b1500;border-radius:999px;padding:4px 14px;font-size:20px;letter-spacing:.05em}}
.bh{{font-family:AK;font-weight:800;font-size:{'46' if m=='en' else '42'}px;line-height:1.12;margin:10px 0 14px;color:#0c2238}}
.big .bh{{font-size:{'60' if m=='en' else '54'}px}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:12px}}
.stats div{{background:#fff3cf;border-radius:18px;padding:10px 12px;text-align:center}}
.g2 .stats div{{background:#e6eef8}}
.stats b{{display:block;font-family:AK;font-size:{'64' if big else '50'}px;line-height:1;color:#b3322b}}.g2 .stats b{{color:#1d4f91}}
.stats span{{font-size:21px;font-weight:700;color:#52677a}}
ul{{margin:0;padding:0;list-style:none;font-size:{'30' if big else '23'}px;line-height:1.35}}
li{{padding:4px 0 4px 38px;position:relative}}
li::before{{content:"✓";position:absolute;left:0;top:6px;width:28px;height:28px;border-radius:50%;background:#1f7a55;color:#fff;font-size:17px;font-weight:800;display:flex;align-items:center;justify-content:center}}
.go{{margin-top:auto;display:flex;align-items:center;justify-content:flex-end;gap:12px;padding-top:12px;font-size:22px;font-weight:700;color:#52677a}}
.go b{{background:#b3322b;color:#fff;border-radius:999px;padding:10px 22px;font-size:26px;white-space:nowrap}}.g2 .go b{{background:#1d4f91}}
.url{{display:inline-block;background:#fff;color:#0c2238;border-radius:999px;padding:8px 26px;margin-bottom:10px;font-size:29px}}
.foot{{padding:20px 56px 26px;color:#fff;text-align:center;font-size:28px;font-weight:800;position:relative;z-index:1}}
{'.b{flex:none;padding:34px 34px 30px}.blocks{justify-content:center}.big .stats{margin:10px 0 22px}.big .stats div{padding:22px 12px}.big li{padding:8px 0 8px 44px}.big li::before{top:12px;width:32px;height:32px}.go{margin-top:26px}' if big else '.go{display:none}.b{flex:none}.blocks{flex:1;justify-content:center}'}
.url{{display:table;margin:0 auto 10px}}
</style></head><body><div class="card">
<div class="top"><div class="brand"><img src="{M.LOGO}" alt="">{e(x['brand'])}</div><div class="bigstar">⭐</div>
<div class="eb">{e(x['eb'])}</div><h1>{e(head)}</h1><div class="sub">{e(x['sub'])}</div></div>
<div class="blocks">{''.join(block(m, k, big) for k in kinds)}</div>
<div class="foot"><div class="url">👉 {M.SITE_URL}/mock.html</div>{e(x['share'])}</div>
</div></body></html>"""

async def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [('quiz-mock', ['ca', 'g2']), ('ca-quiz', ['ca']), ('g2-mock', ['g2'])]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for name, kinds in jobs:
            for m in ('en', 'te'):
                await pg.set_content(page(m, kinds)); await pg.wait_for_timeout(500)
                if await pg.evaluate('document.querySelector(".card").scrollHeight>1352'):
                    print('WARNING: content taller than poster for', name, m)
                await pg.screenshot(path=os.path.join(OUT, f'{name}-{m}.png'))
        await b.close()
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'compress_cards.py'), OUT], check=False)
    print('done', OUT)

if __name__ == '__main__':
    asyncio.run(main())
