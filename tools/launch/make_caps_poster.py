"""Sulabham — Indices & Reports 2026 capsule posters (EN + TE), 1080x1350.
usage: python3 tools/launch/make_caps_poster.py
 -> cards/launch/cap-indices-en.png / -te.png  (promo)
    cards/launch/india-ranks-en.png / -te.png  (free shareable infographic: India's ranks 2026)"""
import asyncio, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'daily'))
import make_day as M
from playwright.async_api import async_playwright
OUT = os.path.join(M.ROOT, 'cards', 'launch'); e = M.e

RANKS = [  # (en, te, rank, total, topper_en, topper_te)
 ('Global Innovation Index', 'గ్లోబల్ ఇన్నోవేషన్ సూచిక', 38, 139, 'Switzerland', 'స్విట్జర్లాండ్'),
 ('Corruption Index 2025', 'అవినీతి సూచిక 2025', 91, 182, 'Denmark', 'డెన్మార్క్'),
 ('SDG Index', 'SDG సూచిక', 94, 167, 'Finland', 'ఫిన్లాండ్'),
 ('Global Hunger Index', 'ప్రపంచ ఆకలి సూచిక', 100, 122, '24 countries tie', '24 దేశాలు సమానం'),
 ('World Happiness', 'ప్రపంచ ఆనంద నివేదిక', 116, 147, 'Finland', 'ఫిన్లాండ్'),
 ('Global Peace Index', 'ప్రపంచ శాంతి సూచిక', 127, 163, 'Iceland', 'ఐస్‌లాండ్'),
 ('Human Development 2025', 'మానవ అభివృద్ధి 2025', 130, 193, 'Iceland', 'ఐస్‌లాండ్'),
 ('Gender Gap Index', 'జెండర్ గ్యాప్ సూచిక', 131, 145, 'Iceland', 'ఐస్‌లాండ్'),
 ('Press Freedom Index', 'పత్రికా స్వేచ్ఛ సూచిక', 157, 180, 'Norway', 'నార్వే'),
 ('Environment Index (EPI)', 'పర్యావరణ సూచిక (EPI)', 176, 177, 'Estonia', 'ఎస్టోనియా'),
]
T = {
 'en': dict(eb='CURRENT AFFAIRS CAPSULE · APPSC GROUP 1 & 2', h='Indices &amp; Reports<br><span>2026</span>',
   sub='Every global index up to November 2026 — finished in one sitting.', strip='India 2026 at a glance',
   items=[('✅', 'Facts verified', 'Every rank checked with the official report — common coaching mistakes corrected'),
          ('🔗', 'Linked to all subjects', 'Polity, Economy, Geography, History & Environment links for each index'),
          ('✍️', '44 qualified MCQs', 'Statements, match-the-list, assertion–reason — APPSC pattern, tap to check'),
          ('📄', 'PDF in Telugu &amp; English', '15 pages each — print, revise, done')],
   free='🎁 Free preview: the Environment Index card + 3 questions', price='₹49', pay='one topic', cta='Open capsule →',
   r_eb='INDIA IN GLOBAL INDICES · 2026', r_h='Where does <span>India</span> stand?', r_sub='India’s rank in 10 global indices (best → worst)',
   r_top='Topper', r_cta='Full notes + 44 MCQs → sulabham.in/caps.html'),
 'te': dict(eb='కరెంట్ అఫైర్స్ క్యాప్సూల్ · APPSC గ్రూప్ 1 & 2', h='సూచీలు &amp; నివేదికలు <span>2026</span>',
   sub='నవంబర్ 2026 వరకు అన్ని ప్రపంచ సూచీలు — ఒక్కసారి కూర్చుంటే పూర్తి.', strip='2026లో భారత్ — ఒక చూపులో',
   items=[('✅', 'వాస్తవాలు నిర్ధారితం', 'ప్రతి ర్యాంకు అధికారిక నివేదికతో సరిచూశాం — సాధారణ పొరపాట్లు సవరించాం'),
          ('🔗', 'అన్ని సబ్జెక్టులతో అనుసంధానం', 'ప్రతి సూచికకు పాలిటీ, ఆర్థికం, భూగోళం, చరిత్ర, పర్యావరణ లింకులు'),
          ('✍️', '44 నాణ్యమైన ప్రశ్నలు', 'స్టేట్‌మెంట్లు, జతపరచడం, వాదన–కారణం — APPSC విధానం'),
          ('📄', 'తెలుగు &amp; ఇంగ్లీష్ PDF', 'ఒక్కొక్కటి 15 పేజీలు — ప్రింట్ తీసి రివైజ్ చేయండి')],
   free='🎁 ఉచిత నమూనా: పర్యావరణ సూచిక కార్డు + 3 ప్రశ్నలు', price='₹49', pay='ఒక అంశం', cta='క్యాప్సూల్ తెరవండి →',
   r_eb='ప్రపంచ సూచీల్లో భారత్ · 2026', r_h='<span>భారత్</span> ఎక్కడ ఉంది?', r_sub='10 ప్రపంచ సూచీల్లో భారత్ ర్యాంకు (ఉత్తమం → అధ్వాన్నం)',
   r_top='మొదటి స్థానం', r_cta='పూర్తి నోట్స్ + 44 ప్రశ్నలు → sulabham.in/caps.html'),
}
SUM = {
 'en': dict(eb='CURRENT AFFAIRS CAPSULE · JAN–NOV 2026', h='Summits &amp; Conferences<br><span>2026</span>',
   sub='Davos to COP31 — every summit APPSC can ask, in one sitting.', strip='Editions to remember',
   items=[('✅', 'Facts verified', 'Dates, venues and themes checked with official sources — common mistakes corrected'),
          ('🧩', 'Look-alikes side by side', 'Bishkek vs Dushanbe · 3 COPs · 3 New Delhi declarations — never mix them up'),
          ('✍️', '44 qualified MCQs', 'Statements, match-the-list, chronology, assertion–reason — APPSC pattern'),
          ('📄', 'PDF in Telugu &amp; English', '16 pages each — print, revise, done')],
   free='🎁 Free preview: the BRICS card + 3 questions · All topics bundle ₹249', price='₹49', pay='one topic', cta='Open capsule →',
   chips=[('18', 'BRICS · Delhi'), ('26', 'SCO · Bishkek'), ('31', 'COP · Antalya'), ('52', 'G7 · Évian'), ('49', 'ASEAN · Manila')]),
 'te': dict(eb='కరెంట్ అఫైర్స్ క్యాప్సూల్ · జనవరి–నవంబర్ 2026', h='సదస్సులు &amp; సమావేశాలు <span>2026</span>',
   sub='దావోస్ నుంచి COP31 వరకు — APPSC అడిగే ప్రతి సదస్సు, ఒక్కసారి కూర్చుంటే పూర్తి.', strip='గుర్తుంచుకోవాల్సిన ఎడిషన్లు',
   items=[('✅', 'వాస్తవాలు నిర్ధారితం', 'తేదీలు, వేదికలు, నినాదాలు అధికారిక మూలాలతో సరిచూశాం — పొరపాట్లు సవరించాం'),
          ('🧩', 'ఒకేలా ఉండేవి పక్కపక్కనే', 'బిష్కెక్ vs దుషాన్బే · 3 COPలు · 3 న్యూఢిల్లీ ప్రకటనలు — కలపకుండా'),
          ('✍️', '44 నాణ్యమైన ప్రశ్నలు', 'స్టేట్‌మెంట్లు, జతపరచడం, కాలక్రమం, వాదన–కారణం — APPSC విధానం'),
          ('📄', 'తెలుగు &amp; ఇంగ్లీష్ PDF', 'ఒక్కొక్కటి 16 పేజీలు — ప్రింట్ తీసి రివైజ్ చేయండి')],
   free='🎁 ఉచిత నమూనా: బ్రిక్స్ కార్డు + 3 ప్రశ్నలు · అన్ని అంశాలు ₹249', price='₹49', pay='ఒక అంశం', cta='క్యాప్సూల్ తెరవండి →',
   chips=[('18', 'బ్రిక్స్ · ఢిల్లీ'), ('26', 'SCO · బిష్కెక్'), ('31', 'COP · అంటాల్యా'), ('52', 'G7 · ఎవియన్'), ('49', 'ఆసియాన్ · మనీలా')]),
}
BASE = """*{box-sizing:border-box}html,body{margin:0}
body{width:1080px;height:1350px;font-family:FAM,sans-serif;color:#1e0629}
.card{width:1080px;height:1350px;display:flex;flex-direction:column;background:#fbf6ee}
.top{padding:40px 56px 34px;color:#fff;position:relative;background:radial-gradient(circle at 90% 6%,rgba(255,212,92,.55),transparent 32%),linear-gradient(160deg,#2a0b3d,#5b1f7a)}
.brand{display:flex;align-items:center;gap:14px;font-family:AK;font-weight:800;font-size:38px}.brand img{width:60px;height:60px;background:#fff;border-radius:14px;padding:4px}
.eb{display:inline-block;margin-top:22px;background:#ffd45c;color:#1b1500;font-weight:800;font-size:22px;letter-spacing:.04em;border-radius:999px;padding:8px 22px}
h1{font-family:AK;font-weight:800;font-size:72px;line-height:1.05;margin:14px 0 8px;max-width:680px}h1 span{color:#ffd45c}
.sub{font-size:28px;opacity:.94;max-width:700px}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;gap:20px;background:#2a0b3d;color:#fff;padding:26px 48px;font-size:25px;font-weight:700;white-space:nowrap}
.foot b{background:#ffd45c;color:#1b1500;border-radius:999px;padding:12px 26px;font-size:26px}
"""
def promo(m, X=None):
    x = (X or T)[m]; fam = 'NT,NS' if m == 'te' else 'NS,NT'
    it = ''.join(f'<div class="it"><i>{a}</i><div><b>{b}</b><span>{c}</span></div></div>' for a, b, c in x['items'])
    if 'chips' in x: bars = ''.join(f'<div class="ch"><em>{a}</em><span>{e(b)}</span></div>' for a, b in x['chips'])
    else:
        pick = [RANKS[i] for i in (0, 3, 5, 8, 9)]
        bars = ''.join(f'<div class="ch"><em>{r[2]}</em><span>{e(r[0] if m=="en" else r[1])}</span></div>' for r in pick)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{M.FONTS}{BASE.replace('FAM', fam)}
.pr{{position:absolute;right:52px;top:140px;width:260px;height:260px;border-radius:50%;background:#ffd45c;color:#1b1500;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(0,0,0,.3);transform:rotate(-6deg)}}
.pr b{{font-family:AK;font-size:100px;line-height:1}}.pr span{{font-size:26px;font-weight:800}}
.box{{margin:24px 56px 0;background:#fff;border-radius:28px;padding:10px 30px;box-shadow:0 18px 40px rgba(42,11,61,.18)}}
.it{{display:flex;gap:20px;align-items:flex-start;padding:12px 0;border-bottom:2px solid #f0e6f5}}.it:last-child{{border:0}}
.it i{{font-style:normal;font-size:44px;flex:none;width:58px;text-align:center}}.it b{{display:block;font-size:31px;color:#3d1153}}.it span{{display:block;font-size:{'23' if m=='en' else '21'}px;color:#5a4a66;margin-top:3px;line-height:1.3}}
.strip{{margin:22px 56px 0}}.strip h3{{margin:0 0 10px;font-family:AK;font-size:28px;color:#3d1153}}.chips{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
.ch{{background:#2a0b3d;color:#fff;border-radius:18px;padding:12px 8px;text-align:center}}.ch em{{display:block;font-style:normal;font-family:AK;font-weight:800;font-size:46px;color:#ffd45c;line-height:1}}.ch span{{display:block;font-size:{'17' if m=='en' else '16'}px;line-height:1.2;margin-top:6px}}
.free{{margin:22px 56px 0;background:#fff3cf;border:3px dashed #e3a400;border-radius:22px;padding:14px 22px;font-size:26px;font-weight:800;text-align:center}}
</style></head><body style="font-family:{fam}"><div class="card">
<div class="top"><div class="brand"><img src="{M.LOGO}" alt="">{'సులభం' if m=='te' else 'Sulabham'}</div><div class="eb">{x['eb']}</div>
<h1>{x['h']}</h1><div class="sub">{x['sub']}</div><div class="pr"><b>{x['price']}</b><span>{x['pay']}</span></div></div>
<div class="box">{it}</div><div class="free">{x['free']}</div><div class="strip"><h3>📊 {x['strip']}</h3><div class="chips">{bars}</div></div>
<div class="foot"><span>👉 {M.SITE_URL}/caps.html</span><b>{x['cta']}</b></div></div></body></html>"""

def ranks(m):
    x = T[m]; fam = 'NT,NS' if m == 'te' else 'NS,NT'
    rows = ''
    for r in RANKS:
        pct = r[2] / r[3]; col = '#1f8a4c' if pct < .55 else ('#e3a400' if pct < .8 else '#c0392b')
        rows += f"""<div class="row"><div class="nm"><b>{e(r[0] if m=='en' else r[1])}</b><small>{x['r_top']}: {e(r[4] if m=='en' else r[5])}</small></div>
<div class="tr"><i style="width:{max(6, 100*pct):.0f}%;background:{col}"></i></div><div class="rk" style="color:{col}">{r[2]}<small>/{r[3]}</small></div></div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{M.FONTS}{BASE.replace('FAM', fam)}
h1{{font-size:60px;max-width:none}}
.box{{margin:22px 44px 0;background:#fff;border-radius:28px;padding:10px 28px;box-shadow:0 18px 40px rgba(42,11,61,.18)}}
.row{{display:grid;grid-template-columns:{'330px' if m=='en' else '350px'} 1fr 130px;gap:16px;align-items:center;padding:9px 0;border-bottom:2px solid #f3ecf6}}.row:last-child{{border:0}}
.nm b{{display:block;font-size:{'25' if m=='en' else '23'}px;color:#3d1153;line-height:1.15}}.nm small{{display:block;font-size:19px;color:#6a5a76}}
.tr{{height:22px;background:#f1eaf5;border-radius:11px;overflow:hidden}}.tr i{{display:block;height:100%;border-radius:11px}}
.rk{{font-family:AK;font-weight:800;font-size:44px;text-align:right}}.rk small{{font-size:20px;color:#7b6b86}}
.lg{{margin:14px 52px 0;font-size:21px;color:#5a4a66;display:flex;gap:22px}}.lg i{{display:inline-block;width:18px;height:18px;border-radius:5px;vertical-align:-2px;margin-right:6px}}
</style></head><body style="font-family:{fam}"><div class="card">
<div class="top"><div class="brand"><img src="{M.LOGO}" alt="">{'సులభం' if m=='te' else 'Sulabham'}</div><div class="eb">{x['r_eb']}</div>
<h1>{x['r_h']}</h1><div class="sub">{x['r_sub']}</div></div>
<div class="box">{rows}</div>
<div class="lg"><span><i style="background:#1f8a4c"></i>{'top half' if m=='en' else 'పై సగం'}</span><span><i style="background:#e3a400"></i>{'middle' if m=='en' else 'మధ్యలో'}</span><span><i style="background:#c0392b"></i>{'bottom fifth' if m=='en' else 'చివరి ఐదో వంతు'}</span></div>
<div class="foot" style="font-size:24px"><span>{x['r_cta']}</span></div></div></body></html>"""

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for m in ('en', 'te'):
            for name, fn in (('cap-indices', promo), ('india-ranks', ranks), ('cap-summits', lambda mm: promo(mm, SUM))):
                await pg.set_content(fn(m)); await pg.wait_for_timeout(500)
                if await pg.evaluate('document.querySelector(".card").scrollHeight>1352'): print('WARNING too tall', name, m)
                await pg.screenshot(path=os.path.join(OUT, f'{name}-{m}.png'))
        await b.close()
    subprocess.run([sys.executable, os.path.join(M.ROOT, 'tools', 'compress_cards.py'), OUT], check=False)
    print('done')

if __name__ == '__main__':
    asyncio.run(main())
