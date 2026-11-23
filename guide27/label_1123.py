# 11-23 목사님: 성경 전체로 이름표를 인용 · 약속 · 성취 · 주제 · 모형 다섯으로. '흐름'과 '예언'은 뜻에 맞게 옮깁니다.
# 성경 전체로 본문은 목사님 칸이라 이름표만 바꿉니다. 다시 돌려도 결과가 같습니다.
import json,os,glob,re
R=os.path.dirname(os.path.abspath(__file__)); SS=os.path.join(R,'..','app','site_src')
NEW={13:'주제',15:'모형',17:'약속',71:'주제',75:'주제',81:'주제',83:'주제',          # 2027
     321:'성취',325:'주제',344:'주제',345:'주제',348:'주제',360:'주제',361:'성취',363:'주제'}  # 체험판
OLD=('흐름','예언')
n=0; texts={}
for f in glob.glob(os.path.join(R,'trial_w[0-9].json'))+glob.glob(os.path.join(R,'week*.json'))+[os.path.join(R,'book1.json')]:
    L=json.load(open(f)); ch=False
    for D in L:
        c=D.get('christ')
        if isinstance(c,list) and c and c[0] in OLD and D.get('no') in NEW:
            texts[c[1][:20]]=NEW[D['no']]; c[0]=NEW[D['no']]; ch=True; n+=1
    if ch: json.dump(L,open(f,'w'),ensure_ascii=False,indent=1)
for f in glob.glob(os.path.join(R,'trial_w[0-9].py'))+glob.glob(os.path.join(R,'week*.py')):
    s=open(f).read(); t=s
    for head,lab in texts.items():
        for o in OLD: t=t.replace(f"christ=['{o}','{head}",f"christ=['{lab}','{head}")
    if t!=s: open(f,'w').write(t)
for f in ['guide_qt.json','trial26_qt.json']:
    p=os.path.join(SS,f); J=json.load(open(p))
    for k,v in J['qt'].items():
        if k.isdigit() and int(k) in NEW:
            c=(v.get('obs') or {}).get('christ','')
            m=re.match(r'^(흐름|예언)\s',c or '')
            if m: v['obs']['christ']=NEW[int(k)]+c[len(m.group(1)):]; n+=1
    json.dump(J,open(p,'w'),ensure_ascii=False,indent=1)
print('바꾼 곳',n)
