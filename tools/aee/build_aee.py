# AEE course lock: encrypts paid module pages and PDFs into ak/*.bin and writes ak/index.json.
# usage: AEE_CODE=AEE-XXXXXX python3 tools/aee/build_aee.py <repo root> <dir with built AEE_Module*.html / .pdf>
#        AEE_CODE=AEE-XXXXXX python3 tools/aee/build_aee.py <repo root> --export <dir>   (decrypt published files back)
# The code is never stored in the repo. Re-running with the SAME code keeps the salt, so codes already given
# to students keep working. A new module: add it to FREE or LOCKED below, rebuild, push.
import json, os, re, sys, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
R, SRC = sys.argv[1], sys.argv[2]
FREE = ['AEE_Module2_Fluid_Mechanics', 'AEE_Module2_Test']          # written to the repo root as normal pages (+ their PDFs)
LOCKED = ['AEE_Module3_Surveying', 'AEE_Module3_Test', 'AEE_Module4_Building_Materials', 'AEE_Module4_Test',
          'AEE_Module5_Transportation', 'AEE_Module5_Test',
          'AEE_Module6_Soil_Mechanics', 'AEE_Module6_Test',
          'AEE_Module7_Environmental', 'AEE_Module7_Test',
          'AEE_Module8_Hydraulics_Hydrology', 'AEE_Module8_Test',
          'AEE_Module9_Irrigation', 'AEE_Module9_Test']  # each: .html and .pdf
ITER = 200000
ip = os.path.join(R, 'ak/index.json'); os.makedirs(os.path.join(R, 'ak'), exist_ok=True)
old = json.load(open(ip)) if os.path.exists(ip) else None
code = re.sub(r'[^A-Z0-9]', '', os.environ['AEE_CODE'].upper())
salt = base64.b64decode(old['salt']) if old else secrets.token_bytes(16)
g = AESGCM(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode()))
def enc(b): n = secrets.token_bytes(12); return n + g.encrypt(n, b, None)
def dec(b): return g.decrypt(b[:12], b[12:], None)
if old: dec(base64.b64decode(old['check']))  # refuse a different code: it would lock out every student
if SRC == '--export':
    dst = sys.argv[3]; os.makedirs(dst, exist_ok=True)
    for i, m in old['lessons'].items():
        open(os.path.join(dst, m['f']), 'wb').write(dec(open(os.path.join(R, 'ak', i + '.bin'), 'rb').read()))
    print('exported', len(old['lessons']), 'files to', dst); sys.exit()
lk = '|'.join(re.escape(x) for x in LOCKED)
def relink(h, me=None):
    h = re.sub(r'(href=")(' + lk + r')\.html(?:\?from=aee)?(#[^"]*)?"', lambda m: f'{m.group(1)}aee-view.html?l={m.group(2)}{m.group(3) or ""}"', h)
    h = re.sub(r'(href=")(' + lk + r')\.pdf"', lambda m: f'{m.group(1)}aee-view.html?l={m.group(2)}-pdf"', h)
    h = re.sub(r'"(' + lk + r')\.pdf"', lambda m: f'"aee-view.html?l={m.group(1)}-pdf"', h)       # PDF named in a test page's config
    h = h.replace('index.html#aee', 'aee.html#lessons').replace('← Back to AEE', '← AEE course').replace('All AEE files', 'AEE course page')
    if me: h = h.replace('"?t="+tn+"&from="+from', '"?l=' + me + '&t="+tn+"&from="+from')   # keep the lesson id in the address
    return h
STUB = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>AEE course · Sulabham</title><meta http-equiv="refresh" content="0;url=aee-view.html?l={i}"><link rel="canonical" href="https://sulabham.in/aee.html"></head><body><p><a href="aee-view.html?l={i}">Open this lesson in the AEE course</a></p></body></html>\n'
les = {}
for i in LOCKED:
    h = open(os.path.join(SRC, i + '.html'), encoding='utf-8').read()
    open(os.path.join(R, 'ak', i + '.bin'), 'wb').write(enc(relink(h, i).encode()))
    les[i] = {'t': re.search(r'<title>(.*?)</title>', h, re.S).group(1).replace(' · Sulabham', '').strip(), 'k': 'html', 'f': i + '.html'}
    open(os.path.join(R, i + '.html'), 'w', encoding='utf-8').write(STUB.replace('{i}', i))   # old public address -> lock screen
    open(os.path.join(R, 'ak', i + '-pdf.bin'), 'wb').write(enc(open(os.path.join(SRC, i + '.pdf'), 'rb').read()))
    les[i + '-pdf'] = {'t': les[i]['t'] + ' (PDF)', 'k': 'pdf', 'f': i + '.pdf'}
    p = os.path.join(R, i + '.pdf')
    if os.path.exists(p): os.remove(p)
for f in FREE:
    h = open(os.path.join(SRC, f + '.html'), encoding='utf-8').read()
    open(os.path.join(R, f + '.html'), 'w', encoding='utf-8').write(relink(h))
json.dump({'v': 1, 'salt': base64.b64encode(salt).decode(), 'iter': ITER,
           'check': base64.b64encode(enc(b'sulabham-aee-ok')).decode(), 'lessons': les},
          open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('locked', len(les), 'free', len(FREE))
