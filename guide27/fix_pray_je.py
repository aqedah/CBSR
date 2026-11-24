# 11-24 목사님: 기도의 1인칭을 '제'로 맞춤 ("맞추세요"). 인용(큰따옴표·작은따옴표 속 말)은 그대로.
import json, re, glob, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = [('내가', '제가'), ('내게', '제게'), ('나를', '저를'), ('나의', '저의'), ('나에게', '저에게'), ('내', '제')]
KEEP_SQ = {'‘내 것’': '‘제 것’'}  # 작은따옴표지만 기도하는 사람의 말이라 맞춤
def fix(p):
    for a, b in KEEP_SQ.items(): p = p.replace(a, b)
    p = re.sub(r'내 손이 나를 구원했다 말하지', '‘내 손이 나를 구원하였다’고 말하지', p)  # 삿 7:2 인용으로 밝힘
    parts = re.split(r'("[^"]*"|‘[^’]*’)', p)
    for i in range(0, len(parts), 2):
        s = parts[i]
        for a, b in MAP: s = re.sub(rf'(?<![가-힣]){a}(?![가-힣])', b, s)
        parts[i] = s
    return ''.join(parts)
ch = []
def walk(o, where):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'pray' and isinstance(v, str):
                nv = fix(v)
                if nv != v: o[k] = nv; ch.append((where, v, nv))
            else: walk(v, where + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, where + f'/{i}')
files = [f'{R}/app/site_src/guide_qt.json'] + sorted(glob.glob(f'{R}/guide27/book*.json'))
for f in files:
    D = json.load(open(f)); n0 = len(ch); walk(D, os.path.basename(f))
    if len(ch) > n0:
        ind = 1
        json.dump(D, open(f, 'w'), ensure_ascii=False, indent=ind, separators=None if ind else (',', ':'))
for w, a, b in ch: print(w, '\n  ', a, '\n→ ', b)
print(len(ch))
