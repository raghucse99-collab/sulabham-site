# DSC SGT course lock: encrypts paid lesson pages into dk/*.bin and writes dk/index.json.
# usage: DSC_CODE=DSC-XXXXXX python3 build_dsc.py <repo root> <dir with built lesson .html files>
# The code is never stored in the repo. Re-running with the SAME code keeps the salt, so codes already
# given to students keep working. A new lesson: add it to LOCKED/TITLES, rebuild, push.
import json, os, re, sys, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
R, SRC = sys.argv[1], sys.argv[2]
FREE = ['dsc-sgt-study-guide', 'dsc-sgt-perspectives-day1', 'dsc-sgt-psychology-day1']
LOCKED = ['dsc-sgt-perspectives-day2', 'dsc-sgt-week1-2-psychology', 'dsc-sgt-psychology-day2', 'dsc-sgt-psychology-day3',
          'dsc-sgt-psychology-day4', 'dsc-sgt-week1-2-test', 'dsc-sgt-maths-day1']
ITER = 200000
ip = os.path.join(R, 'dk/index.json'); os.makedirs(os.path.join(R, 'dk'), exist_ok=True)
old = json.load(open(ip)) if os.path.exists(ip) else None
code = re.sub(r'[^A-Z0-9]', '', os.environ['DSC_CODE'].upper())
salt = base64.b64decode(old['salt']) if old else secrets.token_bytes(16)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(code.encode())
g = AESGCM(key)
def enc(b): n = secrets.token_bytes(12); return n + g.encrypt(n, b, None)
if old:  # refuse a different code: it would lock out every student who already has the old one
    raw = base64.b64decode(old['check']); g.decrypt(raw[:12], raw[12:], None)
ids = [f'{x}{m}' for x in LOCKED for m in ('', '-te')]
lk = '|'.join(re.escape(x) for x in ids)
def relink(h):  # links to other locked lessons go through the viewer
    return re.sub(r'href="(' + lk + r')\.html(#[^"]*)?"', lambda m: f'href="dsc-view.html?l={m.group(1)}{m.group(2) or ""}"', h)
for i in ids:
    h = open(os.path.join(SRC, i + '.html'), encoding='utf-8').read()
    open(os.path.join(R, 'dk', i + '.bin'), 'wb').write(enc(relink(h).encode()))
for f in FREE:
    for m in ('', '-te'):
        h = open(os.path.join(SRC, f + m + '.html'), encoding='utf-8').read()
        open(os.path.join(R, f + m + '.html'), 'w', encoding='utf-8').write(relink(h))
titles = {}
for i in ids:
    h = open(os.path.join(SRC, i + '.html'), encoding='utf-8').read()
    titles[i] = re.search(r'<title>(.*?)</title>', h, re.S).group(1).strip()
json.dump({'v': 1, 'salt': base64.b64encode(salt).decode(), 'iter': ITER,
           'check': base64.b64encode(enc(b'sulabham-dsc-ok')).decode(), 'lessons': titles},
          open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('locked', len(ids), 'free', len(FREE) * 2)
