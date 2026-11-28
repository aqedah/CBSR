# 11-28 목사님: 인쇄본 뒤표지에서 '-니다.'의 '다.'만 다음 줄로 내려감. 글줄을 낱말 단위로만 끊도록(word-break:keep-all, text-wrap:pretty) 바꾸니
# 체험판 네 날(334·336·338·360)이 한 줄씩 넘쳐, 해설에서 군말 한두 문장을 덜어 냄. trial26_qt.json과 원고 스크립트(guide27/*.py)에 같은 고침.
import json, os, glob, time
H = os.path.dirname(os.path.abspath(__file__))
R = [('그런데 그 은사가', '그런데 그 은사가'),
 (' 방언하는 사람, 예언하는 사람, 가르치는 사람이 있었지요.', ''),
 (' 우리가 받은 것도 그렇습니다. 나를 돋보이게', ' 우리 은사도 나를 돋보이게'),
 (' 고난이 끝나서가 아닙니다. 그 고난 한가운데서', ' 고난 한가운데서'),
 (' 우리가 겪은 아픔도 그렇습니다. 그 자리에서 받은 위로가', ' 우리도 아픔의 자리에서 받은 위로가'),
 (' 그런데 얼마를 내라고 하지 않지요. 명령이 아니라고', ' 그런데 명령이 아니라고'),
 (' 그런데 끝은 같습니다. 이기는 자에게 주시는 약속입니다.', ' 그런데 두 편지 모두 이기는 자에게 주시는 약속으로 끝납니다.')]
P = os.path.join(H, '..', 'app', 'site_src', 'trial26_qt.json')
d = json.load(open(P, encoding='utf8')); U = int(time.time() * 1000)
for k in ['334', '336', '338', '360']:
    x = d['qt'][k]; n = x['note']
    for a, b in R: n = n.replace(a, b)
    if n != x['note']: x['note'] = n; x['u'] = U; print(k, 'ok')
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for f in glob.glob(os.path.join(H, '*.py')):
    if f.endswith('trial_1128_keepall.py'): continue
    s = open(f, encoding='utf8').read(); t = s
    for a, b in R[1:]: t = t.replace(a, b)
    if t != s: open(f, 'w', encoding='utf8').write(t); print('원고', os.path.basename(f))
# 이어서: 360 본문 관찰 첫 줄을 한 줄로(주님은 교회마다 형편을 다 아시고 맞는 말씀을 주십니다). trial26_qt.json과 trial_review15.py에 바로 고침.
# 이어서: 333 표시 문장 '〈덕을 세워〉를 작게 적으세요'의 '작게'를 빼서 '적으세요.'가 홀로 줄을 차지하지 않게.
