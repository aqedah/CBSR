# 체험판: 성경 읽기 표시를 본문 차례대로, 눈여겨볼 것은 표시 확인(ck) 먼저 본문 차례대로 (11-23 목사님). '되풀이'를 '반복'으로 바꾸는 것도 다시 한 번.
# 순서: … trial_review6.py → 이 파일 → to_guide_qt.py
import json,os,sys
R=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,R)
from fix_1123 import walk,order  # fix_1123은 이 파일의 '되풀이' 글자도 바꾸므로 머리말은 풀어 씀
for w in range(1,8):
    F=os.path.join(R,f'trial_w{w}.json'); L=walk(json.load(open(F)))
    for D in L: D['marks'],D['looks']=order(D.get('marks',[]),D.get('looks',[]))
    json.dump(L,open(F,'w'),ensure_ascii=False,indent=1)
print('ok')
