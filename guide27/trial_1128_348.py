# 11-28 목사님: 12/13과 잇기 — 12/14 딤후 해설에 3:11(디모데가 보고 안 루스드라의 일, 주께서 건지심)을 한 줄 넣음
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, '..', 'app', 'site_src', 'trial26_qt.json')
A = '처음 재판을 받을 때는 곁에 아무도 없었지요. 그런데 바울은 원망하지 않습니다. 주께서 곁에 서서 힘을 주셨기 때문입니다.'
B = '처음 재판을 받을 때는 곁에 아무도 없었지요. 그래도 주께서 곁에 서서 힘을 주셨습니다. 디모데도 아는 일입니다. 루스드라에서 돌에 맞을 때에도 주께서 건지셨지요(3:11).'
for p in (P, os.path.join(H, 'trial_review23.py')):
    s = open(p, encoding='utf8').read()
    if A in s: s = s.replace(A, B); open(p, 'w', encoding='utf8').write(s); print('고침', os.path.basename(p))
