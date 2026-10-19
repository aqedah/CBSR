# 시험 네 날 자동 보고 + subjects 검사
import json,gzip,base64
K=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/rj/bible.b64').read())))
PARA=json.load(open('/home/claude/rj/para/all.json')); T=json.load(open('/home/claude/rj/tools/toolx.json'))
D=json.load(open('/home/claude/rj/srj/all.json')); PL=json.load(open('/home/claude/rj/plan.json'))['plan']
AB="창 출 레 민 신 수 삿 룻 삼상 삼하 왕상 왕하 대상 대하 스 느 에 욥 시 잠 전 아 사 렘 애 겔 단 호 욜 암 옵 욘 미 나 합 습 학 슥 말 마 막 눅 요".split()
import re
def scope(e,chs):
    if e.get('sc'): return e['sc'],'sc'
    R=[]
    def addR(b,c,s,t):
        for r in R:
            if r[0]==b and r[1]==c and not (t<r[2]-1 or s>r[3]+1): r[2]=min(r[2],s); r[3]=max(r[3],t); return
        R.append([b,c,s,t])
    for m in re.finditer(r'(\d+):(\d+)(?:\s*[-–]\s*(\d+))?',e['q']):
        c=int(m[1]); xs=[x for x in chs if x[1]==c]
        if len(xs)==1: addR(xs[0][0],c,int(m[2]),int(m[3] or m[2]))
    for l in e.get('look',[]):
        b,c,v=l['r']
        if [b,c] not in chs: continue
        st=PARA.get(f"{b}-{c}",[1]); s0=1
        for x in st:
            if x<=v: s0=x
        nx=[x for x in st if x>v]; addR(b,c,s0,nx[0]-1 if nx else len(K[b-1][c-1]))
    for r in e.get('sx',[]): addR(*r)
    return (R or None),'auto'
out=["# 시험 네 날 자동 보고","","내용이 맞는지는 사람이 최종 판정합니다. 이 보고는 추출 결과일 뿐입니다.",""]
for key,lab in [("35-1","요 1–4장"),("9-4","삼상 16–20장"),("16-1","욥 1–7장"),("17-4","시 19–24편")]:
    w,dd=map(int,key.split('-')); e=D[key]['e']; chs=PL[w-1][dd-1]['ch']; R,how=scope(e,chs); tk=T.get(f"rj:{w}-{dd-1}",{})
    out+= [f"## {lab} (리딩지저스 {w}-{dd-1})","",f"- 질문: {e['q']}",f"- 도구: 질문 {tk.get('q')} · 살펴보기 {tk.get('look')}",
           f"- 질문의 본문({how}): "+(", ".join(f"{AB[b-1]} {c}:{s}–{t}" for b,c,s,t in R) if R else "NEEDS_SCOPE_REVIEW")]
    for i,l in enumerate(e['look']):
        b,c,v=l['r']; inR=bool(R) and any(r[0]==b and r[1]==c and r[2]<=v<=r[3] for r in R)
        out.append(f"- 살펴보기 {i+1} '{l['t']}' {AB[b-1]} {c}:{v} [{(tk.get('look') or ['?']*3)[i]}] 범위 안: {'예' if inR else '아니오'} — {K[b-1][c-1][v-1]}")
    for s in e.get('subjects',[]):
        ok=all(any(r[0]==b and r[1]==c and r[2]<=s0 and t<=r[3] for r in (R or [])) for b,c,s0,t in s['refs'])
        out.append(f"- 인물 '{s['label']}' 근거 범위 {s['refs']} 포함: {'예' if ok else 'REVIEW_REQUIRED'}")
    out.append("")
open('/home/claude/rj/ux/시험4일_자동보고.md','w').write("\n".join(out)); print("\n".join(out))
