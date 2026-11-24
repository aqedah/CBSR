# season_src.html → app/site_src/season.html
# A4 한 장 모양(build.py CSS)은 .sheet 아래로, 가이드북 A5 모양(a5.py CSS)은 .a5w 아래로 가두어 넣습니다.
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import build, a5
def scope(css, pre, keep_global=('.sans',)):
    out = []
    for line in css.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('@page') or line.startswith('*{') or line.startswith('body{'): continue
        m = re.match(r'^([^{]+)\{(.*)\}$', line)
        if not m: out.append(line); continue
        sels = [x.strip() for x in m.group(1).split(',')]
        ss = []
        for x in sels:
            if x in keep_global: ss.append(x)
            ss.append(f'{pre} {x}')
        out.append(','.join(dict.fromkeys(ss)) + '{' + m.group(2) + '}')
    return '\n'.join(out)
s = open(os.path.join(H, 'season_src.html')).read()
s = s.replace('/*SHEETCSS*/', scope(build.CSS, '.sheet')).replace('/*A5CSS*/', scope(a5.CSS, '.a5w'))
open(os.path.join(H, '../../app/site_src/season.html'), 'w').write(s)
print('ok', len(s))
