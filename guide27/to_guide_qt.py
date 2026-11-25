# 새 틀 원고(book1.json)를 통독 작업대 원고(app/site_src/guide_qt.json)의 v27 칸과 옛 칸으로 옮깁니다. (11-20)
import json,re,time,sys
import os; R=os.path.dirname(os.path.abspath(__file__))
# 쓰는 법: python3 to_guide_qt.py [원고.json] [guide|trial]  (기본: book1.json → 2027 가이드북)
A=sys.argv[1:]; B=os.path.join(R,A[0] if A else 'book1.json')
GQ=os.path.join(R,'..','app','site_src','trial26_qt.json' if len(A)>1 and A[1]=='trial' else 'guide_qt.json')
TOK=[('<span class="o">동그라미</span>','{동그라미}'),('<span class="hy">형광펜</span>','{형광펜}'),('<span class="w">물결 밑줄</span>','{물결 밑줄}'),
('<span class="ht">빗금 형광펜</span>','{빗금 형광펜}'),('<span class="bx">네모</span>','{네모}'),('<b>[괄호]</b>','{괄호}')]
def tok(s):
    for a,b in TOK: s=s.replace(a,b)
    s=re.sub(r'((?:<span class="bn">[^<]*</span>)+)',lambda m:'{번호 '+' '.join(re.findall(r'<span class="bn">([^<]*)</span>',m.group(1)))+'}',s)
    s=re.sub(r'<b>(.*?)</b>',r'**\1**',s)
    assert '<' not in s,s
    return s
def plain(s): return re.sub(r'<[^>]+>','',s)
j=json.load(open(GQ)); q=j['qt']; now=int(time.time()*1000)
for D in json.load(open(B)):
    n=str(D['no']); x=q.setdefault(n,{})
    if 'sub' in D: x['sub']=D['sub']
    g=x.setdefault('guide',{})
    if 'today' in D: g['today']=D['today']
    if 'word' in D: g['word']=D['word'][0]+' — '+D['word'][1]
    g['find']=' '.join(dict.fromkeys(m['tool'] for m in D['marks']))
    o=x.setdefault('obs',{}); o['q']=D['q']
    if 'christ' in D: o['christ']=D['christ'][0]+' '+D['christ'][1]
    o['pair']=[[l['tool'],tok(l['text'])] for l in D['looks']]
    ap=D['apply']; x['apply']=tok(ap['lead'])+''.join(f' **→ {f}**' for f in ap['fu'])
    if 'godline' in D:   # 맺음 문장 바꾸기: 해설 끝에 붙은 옛 맺음 문장을 떼고 새 문장으로
        og=x.get('god','')
        if og and x.get('note','').rstrip().endswith(og): x['note']=x['note'].rstrip()[:-len(og)].rstrip()
        x['god']=D['godline']
    if 'note' in D:
        x['note']=D['note']
        s=[t for t in re.split(r'(?<=[.])\s+',D['note']) if t.startswith('하나님은')]
        if s and 'godline' not in D: x['god']=s[-1]
    if 'pray' in D: x['pray']=D['pray']
    # 체험판: 옛 원고는 해설과 맺음 문장(god)을 따로 두었으므로, 새 틀처럼 해설 끝에 맺음 문장을 붙임
    if GQ.endswith('trial26_qt.json') and x.get('god') and x['god'] not in x.get('note',''): x['note']=(x.get('note','').rstrip()+' '+x['god']).strip()
    if 'pic' in D:
        if D['pic']: x['img']={'id':re.search(r'(g\d+_\d+)',D['pic'][0]).group(1),'cap':plain(D['pic'][1])}
        else: x.pop('img',None)
    x['v27']={'scenes':D['scenes'],'marks':[{'tool':m['tool'],'rep':bool(m['rep']),'text':tok(m['text'])} for m in D['marks']],
              'looks':[{'ck':bool(l['ck']),'tool':l['tool'],'text':tok(l['text'])} for l in D['looks']],
              'god':[tok(D['god'][0]),tok(D['god'][1])]}
    if D.get('find'):   # 11-25 견본: 본문 관찰 '찾기 → 잇기'. 앱은 obs.q 하나만 읽으므로 물음을 굵게 붙여 둠
        x['v27'].update(obs0=tok(D['q']), find=tok(D['find']), link=tok(D['link']), start=tok(D.get('start','')))
        o['q']=D['q']+' **'+D['find']+'** **'+D['link']+'**'
    if D.get('q2'): x['v27']['obs2']=tok(D['q2']); x['v27']['god2']=[tok(D['god2'][0]),tok(D['god2'][1])]  # 11-24: 범위가 넓은 날의 둘째 갈래
    x['u']=now
j['updated']=time.strftime('%Y-%m-%dT%H:%M:%S')
json.dump(j,open(GQ,'w'),ensure_ascii=False,indent=1)
print('ok',now)
