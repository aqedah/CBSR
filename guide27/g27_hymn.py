# 2027 가이드북 새찬송가(체험판과 같은 방식): 본문 내용에 맞는 찬송 한 장. 장·제목·고른 까닭만.
# guide_qt.json의 qt[날]['hymn']={no,t,why}. 다시 돌려도 결과가 같습니다. 장·제목은 새찬송가 목록과 대조함.
import json,os
R=os.path.dirname(os.path.abspath(__file__))
H={
5:(323,'부름 받아 나선 이 몸','떠나라는 부르심(12:1)'),
26:(384,'나의 갈 길 다 가도록','독수리 날개로 업어 인도하심(19:4)'),
33:(252,'나의 죄를 씻기는','무슨 허물이든지 사함을 받음(6:7)'),
58:(200,'달고 오묘한 그 말씀','오늘 우리와 세우신 언약(5:3)'),
63:(204,'주의 말씀 듣고서','말씀을 평생 옆에 두고 읽음(17:19)'),
73:(330,'어둔 밤 쉬 되리니','"어느 때까지 지체하겠느냐"(18:3)'),
83:(379,'내 갈 길 멀고 밤은 깊은데','어두운 때에 주께 길을 물음(20:18)'),
}
p=os.path.join(R,'..','app','site_src','guide_qt.json'); j=json.load(open(p,encoding='utf8'))
for n,(no,t,why) in H.items(): j['qt'].setdefault(str(n),{})['hymn']={'no':no,'t':t,'why':why}
json.dump(j,open(p,'w',encoding='utf8'),ensure_ascii=False,indent=1); print('hymn',len(H))
