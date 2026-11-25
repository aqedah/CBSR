# season_src.html → app/site_src/season.html
# A4 한 장 모양(build.py CSS)은 .sheet 아래로, 가이드북 A5 모양(a5.py CSS)은 .a5w 아래로 가두어 넣습니다.
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import build, a5, sera4
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
s = s.replace('/*SHEETCSS*/', scope(build.CSS, '.sheet')).replace('/*A5CSS*/', scope(a5.CSS, '.a5w') + '\n' + scope(sera4.CSS, '.a5w')).replace('/*FIT4JS*/', open(os.path.join(H, 'fit4.js')).read())
open(os.path.join(H, '../../app/site_src/season.html'), 'w').write(s)
print('ok', len(s))

# ── 세라핌 묶음 원고를 w*.py에서 season.json으로 (python3 make_season.py sync) ──
def week_json(W, old):
    tk = lambda t: re.sub(r'\{.:([^}]*)\}', r'{\1}', t)
    j = dict(old)
    for k in ('youth', 'churchn'): j.pop(k, None)
    j.update(label=W['label'], season=W.get('season', ''), title=W['title'], sub=W['sub'], vv=W['vv'], color=W['color'], light=W['light'],
             flow='\n\n'.join(W['flow']), words='\n'.join(f'{a} — {b}' for a, b in W['words']), scenes='\n'.join(W['scenes']),
             marks='\n'.join(f'{"★ " if m.get("rep") else ""}{m["tool"]} | {tk(m["text"])}' for m in W['marks']),
             looks='\n'.join(f'{"✓ " if l.get("ck") else ""}{l["tool"]} | {tk(l["text"])}' for l in W['looks']),
             note=W['note'],
             whole_title=W.get('whole_title', ''), whole='\n'.join(f'{x["lab"]} | {x["ref"]} | {x["text"]}' for x in W.get('whole', [])))
    from sera_v3_content import S3
    k = j.get('key'); S = S3.get(k, {})
    for f in ('apply',): j.pop(f, None)
    j.update(obs_ref=S.get('obs_ref', ''), obs=S.get('obs', ''), god=S.get('god', ''), god_q=S.get('god_q', ''), ap_lead=S.get('ap_lead', ''), ap_fu=S.get('ap_fu', ''),
             struct='\n'.join(f'{a} | {t} | {x}' for a, t, x in S.get('struct', [])))
    return j
if len(sys.argv) > 1 and sys.argv[1] == 'sync':
    import json, importlib
    P = os.path.join(H, '../../app/site_src/season.json'); raw = open(P).read(); D = json.loads(raw)
    S = next(s for s in D['sets'] if s['id'] == 'sera-2026-advent')
    S['weeks'] = [week_json(importlib.import_module('w' + w['key']).W, w) for w in S['weeks']]
    import time; S['_u'] = int(time.time() * 1000)  # 새 틀이 이 기기 옛 원고보다 앞서도록
    json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1 if raw.startswith('{\n "') else None)
    print('season.json 세라핌', len(S['weeks']), '회')
