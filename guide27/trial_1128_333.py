# 11-28 목사님: 빌립보서는 열쇠말이 둘이 되어 애매함 → 〈 〉 표기를 12/9에서 빼고 11/29 고전 8–10에 넣음.
# 대표 관찰(틀: 8:1과 10:23 '덕을 세우다')에 8:10 "담력을 얻어"〈덕을 세워〉를 붙임 — 같은 말이 약한 형제를 엉뚱한 쪽으로 세움.
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, '..', 'app', 'site_src', 'trial26_qt.json')
MK0 = '세 장을 열고 닫는 말은 무엇입니까? 8:1과 10:23에서 덕을 세운다는 말을 찾아 {형광펜}으로 칠하세요.'
MK1 = MK0 + ' 8:10 "담력을 얻어" 옆에는 〈덕을 세워〉를 적으세요.'
LK0 = '8:1 "지식은 교만하게 하며 사랑은 덕을 세우나니"로 열고, 10:23 "모든 것이 가하나 모든 것이 덕을 세우는 것은 아니니"로 닫습니다.'
LK1 = LK0 + ' 8:10 "담력을 얻어"〈덕을 세워〉도 같은 말입니다. 지식이 약한 형제를 엉뚱한 쪽으로 세웁니다.'
P343 = '"이 마음을 품으라"(2:5), "같은 마음을 품으라"(4:2), "이렇게 생각할지니"〈마음을 품을지니〉(3:15). 같은 말이 편지를 잇습니다.'
d = json.load(open(P, encoding='utf8')); q = d['qt']
x = q['333']; v = x['v27']
for m in v['marks']:
    if m['text'] == MK0: m['text'] = MK1
for m in v['looks']:
    if m['text'] == LK0: m['text'] = LK1
for pr in x['obs'].get('pair', []):
    if pr[1] == LK0: pr[1] = LK1
y = q['343']
y['v27']['looks'] = [m for m in y['v27']['looks'] if m['text'] != P343]
y['obs']['pair'] = [pr for pr in y['obs'].get('pair', []) if pr[1] != P343]
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for f, A, B in [('trial_w1.py', MK0, MK1), ('trial_w1.py', LK0, LK1), ('trial_w2.py', MK0, MK1), ('trial_w2.py', LK0, LK1)]:
    p = os.path.join(H, f); s = open(p, encoding='utf8').read()
    if A in s and B not in s: open(p, 'w', encoding='utf8').write(s.replace(A, B)); print('고침', f)
p = os.path.join(H, 'trial_w4.py'); s = open(p, encoding='utf8').read()
line = ",\n        dict(ck=False,tool='● 열쇠말',text='" + P343 + "')"
if line in s: open(p, 'w', encoding='utf8').write(s.replace(line, '')); print('뺌 w4')
print('ok')
