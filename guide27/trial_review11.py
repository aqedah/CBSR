# 체험판 49일 새 틀(11-25): 관찰·성품·적용을 trial_v3_content.py로 바꿈. 윤문 세션이 trial26_qt.json에 직접 고친 것(327 말뜻·해설, 357 눈여겨볼 것)도 원고에 옮김.
# 순서: … trial_review10.py → fix_quote_stem.py → 이 파일 → to_guide_qt.py, trial_ldr.py, trial_hymn.py
import json, os, sys
R = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, R)
from trial_v3_content import V3
for w in range(1, 8):
    F = os.path.join(R, f'trial_w{w}.json'); L = json.load(open(F))
    for D in L:
        n = D['no']
        if n == 327:
            D['word'] = ['의', '하나님 앞에서 옳다고 인정받는 것. 로마서는 이 의가 복음에 나타나 믿는 사람에게 주어진다고 말합니다(1:17; 3:22).']
            if 'note' in D: D['note'] = D['note'].replace('값 없이 의롭다', '값없이 의롭다')
            if D.get('godline'): D['godline'] = D['godline'].replace('값 없이', '값없이')
        if n == 357:
            for l in D['looks']:
                if l['text'].startswith('"만일 우리가"가 1:6–10에 네 번'):
                    l['text'] = '"만일 우리가"가 1:6–10에 네 번 나옵니다. 우리가 하는 말과 사는 모습이 맞는지 거듭 묻다가, 1:9에서 죄를 자백하는 사람에게 주시는 약속을 말합니다.'
        if n in V3:
            q, g0, g1, lead, fu = V3[n]
            D['q'] = q; D['god'] = [g0, f'<b>{g1}</b>']; D['apply'] = {'lead': lead, 'fu': [fu]}
    json.dump(L, open(F, 'w'), ensure_ascii=False, indent=1)
print('ok')
# 새 틀로 왼쪽이 넘치는 세 날만 문장을 줄임(말뜻·✓ 없는 항목·기록 줄·간격을 줄여도 넘침)
TRIM = {
 318: [('looks', '"나사렛 예수 그리스도의 이름으로"(3:6), "다른 이름을 우리에게 주신 일이 없음이라"(4:12), "이 이름으로 아무에게도 말하지 말게 하자"(4:17). 표시한 구절들에 "이름"이 거듭 나옵니다.', '"나사렛 예수 그리스도의 이름으로"(3:6), "다른 이름을 우리에게 주신 일이 없음이라"(4:12). 표시한 구절들에 "이름"이 거듭 나옵니다.'),
       ('christ', '예수님은 이 구절로 자신을 가리키셨지요(마 21:42). 이제 베드로가 공회 앞에서 같은 구절을 다시 예수님께 적용합니다.', '예수님이 자신을 가리키신 이 구절을(마 21:42) 베드로가 공회 앞에서 다시 예수님께 적용합니다.')],
 321: [('looks', '하늘이 열려 베드로가 환상을 봅니다. 베드로는 입을 열어 깨달은 것을 말합니다. 옥문이 열려 베드로가 밖으로 나옵니다.', '하늘이, 베드로의 입이, 옥문이 차례로 열립니다.'),
       ('christ', '하나님이 이방인도 받아 주셨음을 확인한 이 일이 13장의 이방 선교를 준비합니다.', '이 일이 13장의 이방 선교를 준비합니다.')],
 348: [('looks', '편지의 처음과 끝이 주님이 오실 그날을 바라봅니다.', '편지의 처음과 끝이 그날을 바라봅니다.'),
       ('looks', '2:3–6에서도 믿음의 삶을 병사와 경기하는 자와 농부에 빗댑니다.', '2장에서는 병사와 경기하는 자와 농부에 빗댑니다.')],
}
for w in range(1, 8):
    F = os.path.join(R, f'trial_w{w}.json'); L = json.load(open(F)); ch = False
    for D in L:
        for k, a, b in TRIM.get(D['no'], []):
            if k == 'looks':
                for l in D['looks']:
                    if a in l['text']: l['text'] = l['text'].replace(a, b); ch = True
            elif k == 'christ' and D.get('christ') and a in D['christ'][1]:
                D['christ'][1] = D['christ'][1].replace(a, b); ch = True
    if ch: json.dump(L, open(F, 'w'), ensure_ascii=False, indent=1)
print('trim ok')
