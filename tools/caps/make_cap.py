"""Sulabham topic capsules (₹49 each): notes + MCQs (online tap-to-check and in the PDF with answer key) + PDFs, encrypted with one master code.

usage: python3 tools/caps/make_cap.py <source_dir> <module_prefix> <MASTER-CODE> [price]
  source_dir holds <prefix>_notes.py (META, BIG, MORE, REPORTS, LADDER, PUB) and <prefix>_mcq.py (MCQ).
  The source files are PRIVATE — keep them outside the repo (paid content).
Writes: caps/<id>.json (public meta + free preview + encrypted body), caps/<id>-en.bin / -te.bin
        (encrypted PDFs), caps/qr-<price>.png, and updates caps/index.json.
Device-locked personal codes use product id  cap-<id>  in the private code maker.
"""
import subprocess, asyncio, base64, html, importlib, json, os, re, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import qrcode
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'daily'))
import make_day as MD
from playwright.async_api import async_playwright

ROOT = MD.ROOT; ITER = 150000; UPI = 'raghu.cse999@axl'
E = lambda s: html.escape(str(s))
def norm(c): return re.sub(r'[^A-Z0-9]', '', c.upper())
def key_for(code, salt): return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(norm(code).encode())
def enc(key, data): n = secrets.token_bytes(12); return n + AESGCM(key).encrypt(n, data, None)
b64 = lambda b: base64.b64encode(b).decode()
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI']

def body(N, Q):
    """the full paid content as plain JSON (rendered by capsule.html)"""
    return {'meta': N.META, 'big': [{**c, 'facts': [list(f) for f in c['facts']]} for c in N.BIG],
            'more': N.MORE, 'reports': [list(r) for r in N.REPORTS], 'ladder': N.LADDER,
            'pub': [list(r) for r in N.PUB], 'mcq': Q.MCQ}

# ---------------- PDF ----------------
CSS = """
@page{size:A4;margin:10mm 10mm 12mm}
*{box-sizing:border-box}body{margin:0;font:9.4pt/1.42 NS,NT,sans-serif;color:#14212b}
html.te body{font-family:NT,NS,sans-serif;font-size:9.2pt;line-height:1.55}
h1,h2,h3,.ak{font-family:AK,NS,NT,sans-serif}
.cover{background:linear-gradient(135deg,#2a0b3d,#5b1f7a);color:#fff;border-radius:4mm;padding:6mm 7mm;margin-bottom:4mm;position:relative}
.cover .br{display:flex;align-items:center;gap:3mm;font:800 13pt AK}.cover .br img{width:10mm;height:10mm;background:#fff;border-radius:2mm;padding:.6mm}
.cover h1{margin:3mm 0 1mm;font-size:22pt;line-height:1.1}.cover p{margin:0;opacity:.92}
.cover .tag{position:absolute;right:6mm;top:6mm;background:#ffd45c;color:#1b1500;border-radius:99px;padding:1mm 3.5mm;font:800 9pt AK}
.how{background:#fff3cf;border:.4mm dashed #e3a400;border-radius:3mm;padding:2.5mm 3.5mm;margin:0 0 4mm}
.card{border:.35mm solid #d9dee3;border-radius:3mm;margin:0 0 4mm;break-inside:auto}
.card>h2{margin:0;color:#fff;font-size:13pt;padding:2mm 3.5mm;border-radius:2.6mm 2.6mm 0 0}
.in{padding:2.5mm 3.5mm}
table{width:100%;border-collapse:collapse;margin:1mm 0 2mm}td,th{border:.25mm solid #cfd6dc;padding:1mm 1.8mm;vertical-align:top;text-align:left}
th{background:#eef2f5;font-weight:600}td.k{width:24%;font-weight:600;background:#f8fafb}
.box{border-radius:2.5mm;padding:2mm 3mm;margin:2mm 0;break-inside:avoid}.box b.h{display:block;font-family:AK;font-size:10.5pt;margin-bottom:.8mm}
.cn{background:#eaf3ff;border-left:1.2mm solid #1d4f91}.ch{background:#eef8ef;border-left:1.2mm solid #2f7a3a}
.sj{background:#f6effa;border-left:1.2mm solid #7b3fa0}.tr{background:#fff0ee;border-left:1.2mm solid #b3322b}
ul{margin:.5mm 0;padding-left:4.5mm}li{margin:.6mm 0}
.mini{border:.3mm solid #d9dee3;border-radius:2.5mm;padding:2mm 3mm;margin:0 0 2.5mm;break-inside:avoid}
.mini h3{margin:0 0 1mm;font-size:11pt}.mini .r{margin:.4mm 0}.mini .r b{color:#3d1153}
h2.sec{font-size:15pt;color:#3d1153;margin:5mm 0 2.5mm;border-bottom:.6mm solid #e3a400;padding-bottom:1mm;break-after:avoid}
.q{margin:0 0 3mm;break-inside:avoid}.q .n{font-weight:700}.q .st{margin:.6mm 0 .6mm 4mm}
.q .ol{display:grid;grid-template-columns:1fr 1fr;gap:.4mm 4mm;margin:.8mm 0 0 4mm}
.ml{display:grid;grid-template-columns:1fr 1fr;gap:0 4mm;margin:1mm 0 1mm 4mm;border:.25mm solid #cfd6dc;border-radius:2mm;padding:1.2mm 2mm}
.ml div{margin:.3mm 0}.ml .hd{font-weight:700;color:#3d1153}
.key{font-size:8.8pt}.key p{margin:0 0 1.6mm}
.bar{display:flex;align-items:center;gap:2mm;margin:.8mm 0}.bar span.l{width:34mm;font-size:8.6pt}.bar i{display:block;height:3.6mm;border-radius:1mm;background:#b46fd6}.bar em{font-style:normal;font-size:8.4pt;font-weight:700}
"""

def qhtml(i, q, m):
    h = f'<div class="q"><div class="n">{i}. {E(q["q"][m]).replace(chr(10), "<br>")}</div>'
    if q.get('st'):
        if q.get('plain'): h += ''.join(f'<div class="st">{E(s[m])}</div>' for s in q['st'])
        else: h += ''.join(f'<div class="st">{ROMAN[k]}. {E(s[m])}</div>' for k, s in enumerate(q['st']))
    if q.get('ml'):
        L = q['ml']; h += '<div class="ml"><div class="hd">' + ('List-I' if m == 'en' else 'జాబితా-I') + '</div><div class="hd">' + ('List-II' if m == 'en' else 'జాబితా-II') + '</div>'
        for a, b in zip(L['l1'], L['l2']): h += f'<div>{E(a[m])}</div><div>{E(b[m])}</div>'
        h += '</div>'
    if q.get('ask'): h += f'<div class="st"><i>{E(q["ask"][m])}</i></div>'
    h += '<div class="ol">' + ''.join(f'<div>({"abcd"[k]}) {E(o[m])}</div>' for k, o in enumerate(q['o'])) + '</div></div>'
    return h

def pdf_html(N, Q, m):
    L = lambda en, te: en if m == 'en' else te
    meta = N.META
    h = f'''<!doctype html><html class="{m}"><head><meta charset="utf-8"><style>{MD.FONTS}{CSS}</style></head><body>
<div class="cover"><div class="br"><img src="{MD.LOGO}" alt="">{L("Sulabham","సులభం")}</div><span class="tag">{L("Capsule","క్యాప్సూల్")} · {meta["updated"]}</span>
<h1>{E(meta["title"][m])}</h1><p>{E(meta["sub"][m])}</p></div>
<div class="how">💡 {E(meta["how"][m])}</div>'''
    for c in N.BIG:
        meta = N.META
        h += f'<div class="card"><h2 style="background:{c["color"]}">{c["icon"]} {E(c["name"][m])}</h2><div class="in"><table>'
        h += ''.join(f'<tr><td class="k">{E(a[m])}</td><td>{E(b[m])}</td></tr>' for a, b in c['facts']) + '</table>'
        h += f'<div class="box cn"><b class="h">🧠 {meta["concept_label"][m] if "concept_label" in meta else L("Understand the score","స్కోరును అర్థం చేసుకోండి")}</b>{E(c["concept"][m])}</div>'
        h += f'<div class="box ch"><b class="h">🔗 {L("Linked facts — the chain","అనుసంధాన వాస్తవాలు — గొలుసు")}</b><ul>' + ''.join(f'<li>{E(x[m])}</li>' for x in c['chain']) + '</ul></div>'
        h += f'<div class="box sj"><b class="h">📚 {L("Subject links","సబ్జెక్టు అనుసంధానం")}</b><ul>' + ''.join(f'<li>{E(x[m])}</li>' for x in c['subj']) + '</ul></div>'
        h += f'<div class="box tr"><b class="h">⚠️ {L("Traps & corrections","ఉచ్చులు & సవరణలు")}</b><ul>' + ''.join(f'<li>{E(x[m])}</li>' for x in c['trap']) + '</ul></div></div></div>'
    G = lambda k, en, te: meta[k][m] if k in meta else L(en, te)
    h += f'<h2 class="sec">➕ {G("more_title", "More indices & reports up to November 2026", "నవంబర్ 2026 వరకు మరిన్ని సూచీలు & నివేదికలు")}</h2>'
    ML = [x[m] for x in meta['more_labels']] if 'more_labels' in meta else [L("By", "ప్రచురణ"), L("Top / last", "మొదటి / చివరి"), L("India", "భారత్"), L("Link", "అనుసంధానం")]
    for c in N.MORE:
        h += f'<div class="mini"><h3>{c["icon"]} {E(c["name"][m])}</h3>'
        for lab, k in zip(ML, ('by', 'top', 'india', 'link')):
            h += f'<div class="r"><b>{lab}:</b> {E(c[k][m])}</div>'
        h += '</div>'
    h += f'<h2 class="sec">📄 {G("reports_title", "Reports to remember", "గుర్తుంచుకోవాల్సిన నివేదికలు")}</h2><table>' + ''.join(f'<tr><td class="k">{E(a[m])}</td><td>{E(b[m])}</td></tr>' for a, b in N.REPORTS) + '</table>'
    if N.LADDER: h += f'<h2 class="sec">📊 {L("India’s rank ladder (best → worst)","భారత్ ర్యాంకుల నిచ్చెన (ఉత్తమం → అధ్వాన్నం)")}</h2>'
    for name, r in N.LADDER:
        a, b = [int(x) for x in r.split('/')]
        h += f'<div class="bar"><span class="l">{E(name)}</span><i style="width:{max(4, 110 * a / b):.0f}mm"></i><em>{E(r)}</em></div>'
    PH = [x[m] for x in meta['pub_head']] if 'pub_head' in meta else [L("Index","సూచిక"), L("Publisher","ప్రచురణ సంస్థ"), L("Base","కేంద్రం")]
    h += f'<h2 class="sec">🏢 {G("pub_title", "Who publishes what — one table", "ఏ సూచిక ఎవరిది — ఒకే పట్టిక")}</h2><table><tr><th>{PH[0]}</th><th>{PH[1]}</th><th>{PH[2]}</th></tr>'
    h += ''.join(f'<tr><td>{E(a[m])}</td><td>{E(b[m])}</td><td>{E(c[m])}</td></tr>' for a, b, c in N.PUB) + '</table>'
    h += f'<h2 class="sec" style="break-before:page">✍️ {L("Practice test","ప్రాక్టీస్ టెస్ట్")} — {len(Q.MCQ)} {L("questions (APPSC Group 1 / 2 pattern)","ప్రశ్నలు (APPSC గ్రూప్ 1 / 2 విధానం)")}</h2>'
    h += ''.join(qhtml(i + 1, q, m) for i, q in enumerate(Q.MCQ))
    h += f'<h2 class="sec" style="break-before:page">🔑 {L("Answer key with explanations","జవాబులు & వివరణలు")}</h2><div class="key">'
    h += ''.join(f'<p><b>{i + 1}. ({"abcd"[q["a"]]})</b> {E(q["why"][m])}</p>' for i, q in enumerate(Q.MCQ)) + '</div>'
    h += '</body></html>'
    return h

async def pdfs(N, Q, out):
    res = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for m in ('en', 'te'):
            await pg.set_content(pdf_html(N, Q, m)); await pg.wait_for_timeout(600)
            path = os.path.join(out, f'{N.META["id"]}-{m}.pdf')
            foot = ('<div style="width:100%;font-size:7px;color:#6b7a86;text-align:center;font-family:sans-serif">sulabham.in · '
                    + E(N.META['title']['en']) + ' · For the buyer’s personal use only · <span class="pageNumber"></span>/<span class="totalPages"></span></div>')
            await pg.pdf(path=path, format='A4', print_background=True, display_header_footer=True, header_template='<div></div>', footer_template=foot,
                         margin={'top': '10mm', 'bottom': '13mm', 'left': '10mm', 'right': '10mm'})
            res[m] = path
        await b.close()
    return res

def main():
    src, prefix, code = sys.argv[1], sys.argv[2], sys.argv[3]
    price = int(sys.argv[4]) if len(sys.argv) > 4 else 49
    assert len(norm(code)) == 9, 'master code must have 9 letters/digits (device codes need it)'
    sys.path.insert(0, os.path.abspath(src))
    N = importlib.import_module(prefix + '_notes'); Q = importlib.import_module(prefix + '_mcq')
    cid = N.META['id']; out = os.path.join(ROOT, 'caps'); os.makedirs(out, exist_ok=True)
    # validate
    for i, q in enumerate(Q.MCQ):
        assert len(q['o']) == 4 and 0 <= q['a'] < 4, f'Q{i+1} options/answer'
        for k in ('q', 'why'): assert q[k]['en'] and q[k]['te'], f'Q{i+1} {k}'
    tmp = os.path.abspath(src)
    P = asyncio.run(pdfs(N, Q, tmp))
    salt = secrets.token_bytes(16); key = key_for(code, salt)
    full = body(N, Q)
    TOC = [{'icon': c.get('icon', '•'), 'name': c['name']} for c in list(N.BIG) + list(N.MORE)]
    pub = {'id': cid, 'title': N.META['title'], 'sub': N.META['sub'], 'updated': N.META['updated'], 'price': price,
           'salt': b64(salt), 'iter': ITER, 'check': b64(enc(key, b'sulabham-ok')),
           'counts': {'big': len(N.BIG), 'more': len(N.MORE), 'mcq': len(Q.MCQ)}, 'toc': TOC,
           'free': {'big': full['big'][0], 'mcq': Q.MCQ[:5], 'how': N.META['how']}, 'concept_label': N.META.get('concept_label'),
           'enc': b64(enc(key, json.dumps(full, ensure_ascii=False).encode())),
           'pdf': {}}
    for m, path in P.items():
        data = open(path, 'rb').read(); fn = f'{cid}-{m}.bin'
        open(os.path.join(out, fn), 'wb').write(enc(key, data)); pg = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout).group(1)); pub['pdf'][m] = {'file': f'caps/{fn}', 'kb': len(data) // 1024, 'pages': pg}
    # optional one-page revision picture (paid): <src>/onepic-<prefix>-<en|te>.png
    pub['pic'] = {}
    for m in ('en', 'te'):
        ip = os.path.join(tmp, f'onepic-{prefix}-{m}.png')
        if os.path.exists(ip):
            fn = f'{cid}-pic-{m}.bin'; open(os.path.join(out, fn), 'wb').write(enc(key, open(ip, 'rb').read())); pub['pic'][m] = {'file': f'caps/{fn}'}
    upi = f'upi://pay?pa={UPI}&pn=Sulabham&am={price}&cu=INR&tn=' + re.sub(' ', '%20', f'Sulabham Capsule {cid}')
    pub['upi'] = upi
    qp = os.path.join(out, f'qr-{cid}.png'); qrcode.make(upi).save(qp); pub['qr'] = f'caps/qr-{cid}.png'
    json.dump(pub, open(os.path.join(out, cid + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    ip = os.path.join(out, 'index.json')
    idx = json.load(open(ip, encoding='utf-8')) if os.path.exists(ip) else []
    idx = [x for x in idx if x['id'] != cid]
    idx.append({'id': cid, 'title': N.META['title'], 'sub': N.META['sub'], 'price': price, 'updated': N.META['updated'],
                'mcq': len(Q.MCQ), 'cards': len(N.BIG) + len(N.MORE), 'icon': N.META.get('icon', '💊'), 'toc': TOC, 'pages': pub['pdf'].get('en', {}).get('pages')})
    json.dump(idx, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('OK', cid, {m: pub['pdf'][m]['kb'] for m in P}, 'KB · product id for code maker: cap-' + cid)
    print('PDF previews (private):', ', '.join(P.values()))

if __name__ == '__main__':
    main()
