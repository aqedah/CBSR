# 꼭 외울 말씀 100 — 목사님 지시(2026-11-13): 이 목록 밖의 구절은 외우라고 하지 않는다.
# 본문은 앱의 개역개정(bible.b64)에서 그대로 가져온다. 실행: python3 tools/mem100_build.py  →  site_src/mem100.json
import json,gzip,base64,os,re
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
B=json.loads(gzip.decompress(base64.b64decode(open('bible.b64').read())))
AB="창 출 레 민 신 수 삿 룻 삼상 삼하 왕상 왕하 대상 대하 스 느 에 욥 시 잠 전 아 사 렘 애 겔 단 호 욜 암 옵 욘 미 나 합 습 학 슥 말 마 막 눅 요 행 롬 고전 고후 갈 엡 빌 골 살전 살후 딤전 딤후 딛 몬 히 약 벧전 벧후 요일 요이 요삼 유 계".split()
L="""창 1:1|창 1:27|창 3:15|창 12:2|창 15:6|창 50:20|출 3:14|출 20:3|레 19:18|민 6:24-26|신 6:4-5|신 8:3|수 1:9|수 24:15|삼상 15:22|삼상 16:7|대하 7:14|욥 1:21|욥 23:10|시 1:1-2|시 16:8|시 19:14|시 23:1|시 27:1|시 37:5|시 46:1|시 51:10|시 103:2|시 119:105|시 121:1-2|시 139:23|잠 1:7|잠 3:5-6|잠 16:9|전 12:13|사 9:6|사 40:31|사 41:10|사 53:5|사 53:6|렘 29:11|렘 33:3|애 3:22-23|겔 36:26|미 6:8|합 2:4|합 3:17-18|슥 4:6|마 5:3|마 5:16|마 6:33|마 7:7|마 11:28|마 16:16|마 22:37|마 28:19-20|막 10:45|눅 19:10|요 1:1|요 1:12|요 1:14|요 3:16|요 8:32|요 11:25|요 13:34|요 14:6|요 15:5|요 20:31|행 1:8|행 4:12|행 16:31|롬 1:16|롬 3:23|롬 5:8|롬 6:23|롬 8:1|롬 8:28|롬 10:9|롬 12:1|롬 12:2|고전 10:13|고전 13:13|고전 15:3-4|고후 5:17|고후 12:9|갈 2:20|갈 5:22-23|엡 2:8-9|빌 4:6-7|빌 4:13|골 3:23|살전 5:16-18|딤후 3:16|히 4:12|히 11:1|히 12:2|벧전 5:7|요일 1:9|계 3:20|계 21:4""".split('|')
out=[]
for r in L:
    bk,cv=r.split(' '); c,v=cv.split(':'); a,b=(v.split('-')+[v])[:2]; c,a,b=int(c),int(a),int(b)
    bi=AB.index(bk); t=' '.join(B[bi][c-1][x-1] for x in range(a,b+1))
    t=re.sub(r'^\[[^\]]*\]\s*','',t)  # 시편 표제([다윗의 시] 등)는 뺌
    out.append({'r':r.replace('-','–'),'b':bi+1,'c':c,'v':[a,b],'t':t})
assert len(out)==100,len(out); assert len(set(L))==100
json.dump({'title':'꼭 외울 말씀 100','note':'외워 둘 말씀은 이 백 구절이면 넉넉합니다. 날마다의 묵상에서는 외우라고 하지 않습니다. 표시해 두고 다시 읽으면 됩니다.','list':out},open('site_src/mem100.json','w'),ensure_ascii=False,indent=0)
print(len(out), sum(len(x['t']) for x in out))

# 가이드북 부록에 넣기: guide.html·trial26.html 안의 /*MEM100*/…/*MEM100 끝*/ 자리를 새로 채움
import re
D=json.load(open('site_src/mem100.json'))
blk='/*MEM100*/const MEM100='+json.dumps(D,ensure_ascii=False,separators=(',',':'))+';/*MEM100 끝*/'
for f in ['site_src/guide.html','site_src/trial26.html']:
    s=open(f).read()
    if '/*MEM100*/' in s: s=re.sub(r'/\*MEM100\*/.*?/\*MEM100 끝\*/',lambda m:blk,s,flags=re.S)
    else: s=s.replace('/* ── 권 끝 부록: 여정 한눈에 · 성막 ── */',blk+'\n/* ── 권 끝 부록: 여정 한눈에 · 성막 ── */',1)
    open(f,'w').write(s); print('부록 자료 넣음:',f)
