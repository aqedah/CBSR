import re, sys, os
from playwright.sync_api import sync_playwright
from PIL import Image
P = '/home/claude/shelf-merged/project'
ART = '/home/claude/shelf-merged/art'
OUT = '/home/claude/shelf-merged/check'
BLOB = {'a3d139b89231c153b09cd95cce982b87': 'hall_q.jpg', '42817b7c394c530f596f73aea865c6d7': 'shelf_soft.jpg',
        '15ea836c96d5c1ad4ea2256a2fc80d15': 'bg_road.jpg', '55b772566d94416f33c02ddd8ee4c856': 'bg_lamp.jpg',
        '7b4d652ca2a7cd0f63ac4f836c31e0f0': 'hall_e.jpg', 'a4e3e410987f58712c7bf77f7ad8eaf8': 'shelf_e.jpg', '29ced3a1f5134f2b60fd888ce996c5cf': 'bg_lamp_p.jpg', 'b34b5f5511f9f94acc44ce57494bd857': 'shelf_f.jpg'}
ALIAS = """<style>
@font-face{font-family:'Noto Serif KR';src:local('Noto Serif CJK KR');font-weight:400}
@font-face{font-family:'Noto Serif KR';src:local('Noto Serif CJK KR Bold'),local('Noto Serif CJK KR');font-weight:700}
@font-face{font-family:'IBM Plex Sans KR';src:local('Noto Sans CJK KR')}
@font-face{font-family:'Gowun Batang';src:local('Noto Serif CJK KR Bold'),local('Noto Serif CJK KR')}
@font-face{font-family:'Song Myung';src:local('Noto Serif CJK KR Bold'),local('Noto Serif CJK KR')}
</style>"""

def build(name, t):
    s = open(os.path.join(P, name)).read()
    inner = s[s.index('<x-dc>') + 6:s.index('</x-dc>')]
    hm = re.search(r'<helmet>(.*?)</helmet>', inner, re.S)
    head = hm.group(1) if hm else ''
    head = re.sub(r'<link[^>]*>', '', head)
    body = inner.replace(hm.group(0), '') if hm else inner
    for k, v in BLOB.items():
        body = body.replace('/_blob/' + k, 'file://' + os.path.join(ART, v))
    pause = '<style>*,*::before,*::after{animation-play-state:paused!important;animation-delay:-%ss!important}</style>' % t
    html = '<!doctype html><html lang="ko"><head><meta charset="utf-8">%s%s%s</head><body>%s</body></html>' % (ALIAS, head, pause, body)
    path = os.path.join(OUT, name.replace('.dc.html', '') + '_t%s.html' % t)
    open(path, 'w').write(html)
    return path

jobs = [(a.split('@')[0], a.split('@')[1] if '@' in a else '2') for a in sys.argv[1:]]
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 390, 'height': 846}, device_scale_factor=1)
    for name, t in jobs:
        path = build(name, t)
        pg.goto('file://' + path)
        pg.wait_for_timeout(350)
        out = path.replace('.html', '.png')
        pg.screenshot(path=out)
        shots.append(out)
    b.close()
sc = float(os.environ.get('SC', '1'))
w, h = int(390 * sc), int(846 * sc)
sheet = Image.new('RGB', (len(shots) * (w + 10) + 10, h + 20), (60, 60, 60))
for i, f in enumerate(shots):
    sheet.paste(Image.open(f).convert('RGB').resize((w, h), Image.LANCZOS), (10 + i * (w + 10), 10))
sheet.save(os.path.join(OUT, os.environ.get('SHEET', 'sheet') + '.png'))
print('ok', len(shots))
