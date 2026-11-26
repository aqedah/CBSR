import glob, re, sys, json, os
files = sorted(glob.glob('data/*.md'))
src = '\n'.join(open(f, encoding='utf-8').read().strip() for f in files)
# 그을린 서가(제2경전·위경·교부 문헌, 11-26 목사님): 작업대에만 칸을 둠. 앱 원고(shelf_66.json)에는 들어가지 않음
src_etc = '\n'.join(open(f, encoding='utf-8').read().strip() for f in sorted(glob.glob('data_etc/*.md')))
assert '</script' not in src
# ---- checks on the manuscript
CH = dict(gen=50,exo=40,lev=27,num=36,deu=34,jos=24,jdg=21,rut=4,**{'1sa':31,'2sa':24,'1ki':22,'2ki':25,'1ch':29,'2ch':36},ezr=10,neh=13,est=10,job=42,psa=150,pro=31,ecc=12,sng=8,isa=66,jer=52,lam=5,ezk=48,dan=12,hos=14,jol=3,amo=9,oba=1,jon=4,mic=7,nam=3,hab=3,zep=3,hag=2,zec=14,mal=4,mat=28,mrk=16,luk=24,jhn=21,act=28,rom=16,**{'1co':16,'2co':13},gal=6,eph=6,php=4,col=4,**{'1th':5,'2th':3,'1ti':6,'2ti':4},tit=3,phm=1,heb=13,jas=5,**{'1pe':5,'2pe':3,'1jn':5,'2jn':1,'3jn':1},jud=1,rev=22)
books, cur = [], None
for l in src.split('\n'):
    m = re.match(r'^## (.+?) \| (\w+) \| (\d+)$', l.strip())
    if m:
        cur = dict(name=m.group(1), id=m.group(2), ch=int(m.group(3)), f={}); books.append(cur); continue
    m = re.match(r'^- ([^:]+): (.*)$', l.strip())
    if m and cur:
        cur['f'].setdefault(m.group(1), []).append(m.group(2))
need = ['한줄','구절','저자','수신자','갈래','배경','목적','흐름','구조','하나님','주제','연결','읽기']
bad = re.compile(r'봅니다|(?<!야고)보입니다|전해집니다|것 같습니다|듯합니다')
err = []
ids = [b['id'] for b in books]
if len(books) != 66 or len(set(ids)) != 66: err.append('책 수 %d' % len(books))
if list(CH) != ids: err.append('책 순서나 id가 다름: %s' % [i for i in ids if i not in CH])
for b in books:
    if CH.get(b['id']) != b['ch']: err.append('%s 장 수 %s' % (b['name'], b['ch']))
    for k in need:
        if k not in b['f']: err.append('%s: %s 없음' % (b['name'], k))
    for k, vs in b['f'].items():
        for v in vs:
            if k not in ('확인','읽기') and bad.search(v): err.append('%s %s: 단정문 아님 → %s' % (b['name'], k, v[:40]))
            if k not in ('확인','구조','구절','저자','수신자','시기','갈래','주제') and not re.search(r'[.다]\)?$|\)$', v): err.append('%s %s: 문장 끝 → %s' % (b['name'], k, v[-20:]))
    for v in b['f'].get('구조', []):
        if '|' not in v: err.append('%s 구조 꼴 → %s' % (b['name'], v))
print('books', len(books), 'chapters', sum(b['ch'] for b in books), 'chars', len(src))
print('한줄 가장 긴 것:', sorted(((len(b['f']['한줄'][0]), b['name']) for b in books), reverse=True)[:6])
print('각주:', [b['name'] for b in books if '각주' in b['f']], '| 확인:', len([b for b in books if '확인' in b['f']]))
print('\n'.join(err) if err else 'manuscript checks: ok')
html = open('template.html', encoding='utf-8').read().replace('%%DATA%%', src + ('\n' + src_etc if src_etc else ''))
assert '</script' not in src_etc
print('그을린 서가 칸:', len(re.findall(r'^## ', src_etc, re.M)))
for out in ('dist/index.html', 'dist/성경책장_작업대.html'):
    open(out, 'w', encoding='utf-8').write(html)
print('built', len(html.encode('utf-8')), 'bytes')
