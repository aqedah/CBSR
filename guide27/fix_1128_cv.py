# 11-28 목사님: 한 장뿐인 책(유다서, 요한이서, 요한삼서, 빌레몬서, 오바댜)도 장:절로 적음 — '유 24' → '유 1:24', 빌레몬서 날의 '16절' → '1:16'
import json, os, re, glob
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
BK = re.compile(r'(?<![가-힣])(유|요이|요삼|몬|옵) (\d+(?:–\d+)?(?:, ?\d+(?:–\d+)?)*)(?![\d:])')
def conv(t, phm=False):
    t = BK.sub(lambda m: m.group(1) + ' 1:' + m.group(2), t)
    if phm: t = re.sub(r'(?<![\d:])(\d+(?:–\d+)?(?:, ?\d+(?:–\d+)?)*)절', r'1:\1', t)
    t = re.sub(r'(\d+:\d+(?:–\d+)?(?:, ?\d+(?:–\d+)?)*)절', r'\1', t)
    return t
def walk(o, phm):
    if isinstance(o, dict): return {k: walk(v, phm) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, phm) for v in o]
    if isinstance(o, str): return conv(o, phm)
    return o
def do_json(p, phm_keys=('350',)):
    d = json.load(open(p, encoding='utf8')); o = json.dumps(d, ensure_ascii=False)
    tgt = d['qt'] if 'qt' in d else d
    for k in list(tgt):
        tgt[k] = walk(tgt[k], k in phm_keys)
    n = json.dumps(d, ensure_ascii=False)
    if n != o: json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return n != o
def do_text(p, blocks=()):
    s = open(p, encoding='utf8').read(); o = s
    for a, b in blocks:  # 빌레몬서 구간(시작 표지, 끝 표지)
        i = s.find(a)
        if i < 0: continue
        j = s.find(b, i + len(a)); j = len(s) if j < 0 else j
        s = s[:i] + conv(s[i:j], True) + s[j:]
    s = conv(s)
    if s != o: open(p, 'w', encoding='utf8').write(s)
    return s != o
if __name__ == '__main__':
    A = os.path.join(R, 'app')
    for p in ('site_src/trial26_qt.json', 'site_src/guide_qt.json', 'site_src/season.json', 'ux/story_cards.json'):
        try: print(p, do_json(os.path.join(A, p)))
        except Exception as e: print(p, 'skip', e)
    G = os.path.join(R, 'guide27')
    print('w5', do_text(os.path.join(G, 'trial_w5.py'), [('D.append(dict(no=350', 'D.append(dict(no=')]))
    print('w7', do_text(os.path.join(G, 'trial_w7.py')))
    print('r23', do_text(os.path.join(G, 'trial_review23.py'), [('350: dict(', '351: dict('), ("350: '", '\n')]))
    D = os.path.join(R, 'docs')
    print('doc', do_text(os.path.join(D, 'CBSR_체험판가이드북_바꾼것_스토리맞춤용_2026-11-25.md'), [('### 12/16 빌레몬서', '### 12/17')]))
    print('doc2', do_text(os.path.join(D, 'CBSR_체험판_세라핌_모범답_검토_2026-11-28.md'), [('12/16 몬', '\n')]))
