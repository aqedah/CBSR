# 11-25 목사님: 인용부호 안에 말을 끊어 넣지 않습니다("덕을 세우"처럼). 끊긴 말은 풀어 씁니다.
import glob, os
R = os.path.dirname(os.path.abspath(__file__))
REP = [
 ('8:1과 10:23에서 \\"덕을 세우\\"를 찾아', '8:1과 10:23에서 덕을 세운다는 말을 찾아'),
 ('14:3, 4, 5, 12, 26에서 \\"덕을 세우\\"를 찾아', '14:3, 4, 5, 12, 26에서 덕을 세운다는 말을 찾아'),
 ('1:17, 18; 3:21에서 \\"나타나\\"를 찾아', '1:17, 18; 3:21에서 나타난다는 말을 찾아'),
 ('2:11, 13; 3:4에서 \\"나타나\\", \\"나타날\\"을 찾아', '2:11, 13; 3:4에서 나타난다는 말을 찾아'),
 ('자비가 \\"나타나\\"는 말로 시작합니다', '자비가 나타났다는 말로 시작합니다'),
 ('4:11; 5:9, 12에서 \\"합당하\\"를 찾아', '4:11; 5:9, 12에서 합당하다는 말을 찾아'),
 ('9:27과 9:34에서 \\"범죄하\\"를 찾아', '9:27과 9:34에서 범죄했다는 말을 찾아'),
]
files = glob.glob(os.path.join(R, 'trial_w*.json')) + glob.glob(os.path.join(R, 'book*.json')) + glob.glob(os.path.join(R, '*qt*.json')) + glob.glob(os.path.join(R, '../app/site_src/*_qt.json')) + glob.glob(os.path.join(R, '../app/*_qt.json'))
n = 0
for f in sorted(set(files)):
    s = open(f).read(); t = s
    for a, b in REP: t = t.replace(a, b)
    if t != s: open(f, 'w').write(t); n += 1; print('고침', os.path.relpath(f, R))
print(n, '파일')
