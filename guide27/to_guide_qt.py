# 새 틀 원고(book1.json)를 통독 작업대 원고(app/site_src/guide_qt.json)의 v27 칸과 옛 칸으로 옮깁니다. (11-20)
import json,re,time,sys
import os; R=os.path.dirname(os.path.abspath(__file__)); GQ=os.path.join(R,'..','app','site_src','guide_qt.json')
B=os.path.join(R,'book1.json')
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
    n=str(D['no']); x=q[n]
    x['sub']=D['sub']
    g=x.setdefault('guide',{}); g['today']=D['today']; g['word']=D['word'][0]+' — '+D['word'][1]
    g['find']=' '.join(dict.fromkeys(m['tool'] for m in D['marks']))
    o=x.setdefault('obs',{}); o['q']=D['q']; o['christ']=D['christ'][0]+' '+D['christ'][1]
    o['pair']=[[l['tool'],tok(l['text'])] for l in D['looks']]
    ap=D['apply']; x['apply']=tok(ap['lead'])+''.join(f' **→ {f}**' for f in ap['fu'])
    x['note']=D['note']; x['pray']=D['pray']
    s=[t for t in re.split(r'(?<=[.])\s+',D['note']) if t.startswith('하나님은')]
    if s: x['god']=s[-1]
    if D.get('pic'):
        x['img']={'id':re.search(r'(g\d+_\d+)',D['pic'][0]).group(1),'cap':plain(D['pic'][1])}
    else: x.pop('img',None)
    x['v27']={'scenes':D['scenes'],'marks':[{'tool':m['tool'],'rep':bool(m['rep']),'text':tok(m['text'])} for m in D['marks']],
              'looks':[{'ck':bool(l['ck']),'tool':l['tool'],'text':tok(l['text'])} for l in D['looks']],
              'god':[tok(D['god'][0]),tok(D['god'][1])]}
    x['u']=now
j['updated']=time.strftime('%Y-%m-%dT%H:%M:%S')
json.dump(j,open(GQ,'w'),ensure_ascii=False,indent=1)
print('ok',now)
