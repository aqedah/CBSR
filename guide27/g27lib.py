# 2027 가이드북 1권 원고 쓰기 도움(11-27). g27_w04.py부터 씁니다.
# 새 틀(v27)이 있는 날은 keep(n)으로 ①②③을 가져오고, 옛 틀만 있는 날은 old(n, …)로 장면·표시·눈여겨볼 것을 새로 붙입니다.
import json, os
R = os.path.dirname(os.path.abspath(__file__))
O='<span class="o">동그라미</span>'; H='<span class="hy">형광펜</span>'; W='<span class="w">물결 밑줄</span>'
HT='<span class="ht">빗금 형광펜</span>'; BX='<span class="bx">네모</span>'; BR='<b>[괄호]</b>'
B = lambda s: '<b>' + s + '</b>'
Q = json.load(open(os.path.join(R, '..', 'app', 'site_src', 'guide_qt.json'), encoding='utf8'))['qt']
def end(g):
    s = g[g.find('하나님은'):]; assert s.endswith('분이십니다.'), g
    return s[:-len('분이십니다.')] + '분입니다.'
def _christ(x):
    c = x['obs'].get('christ', ''); ct, _, cb = c.partition(' '); return [ct, cb]
def _word(w):
    return list(w.split(' — ', 1)) if w else []
def keep(n, mk=None, lk=None, word=None, today=None):
    """새 틀 원고의 ①②③. mk·lk: 남길 표시·눈여겨볼 것의 번호(없으면 모두)"""
    x = Q[str(n)]; v = x['v27']; g = x['guide']
    marks = v['marks'] if mk is None else [v['marks'][i] for i in mk]
    looks = v['looks'] if lk is None else [v['looks'][i] for i in lk]
    return dict(no=n, sub=x.get('sub', ''), today=today or g['today'], word=word if word is not None else _word(g.get('word', '')),
                scenes=v['scenes'], marks=marks, looks=looks, christ=_christ(x))
def old(n, scenes, marks, looks, word=None, today=None, sub=None, christ=None, pic=None):
    """옛 틀만 있는 날: 오늘의 흐름·말뜻·성경 전체로는 옛 원고에서, 장면·표시·눈여겨볼 것은 새로"""
    x = Q[str(n)]; g = x['guide']
    d = dict(no=n, sub=sub or x.get('sub', ''), today=today or g['today'], word=word if word is not None else _word(g.get('word', '')),
             scenes=scenes, marks=[dict(tool=t, rep=r, text=s) for t, r, s in marks],
             looks=[dict(ck=c, tool=t, text=s) for c, t, s in looks], christ=christ or _christ(x))
    if pic: d['pic'] = pic
    return d
def new(n, sub, today, word, scenes, marks, looks, christ, pic=None):
    d = dict(no=n, sub=sub, today=today, word=word, scenes=scenes, marks=[dict(tool=t, rep=r, text=s) for t, r, s in marks],
             looks=[dict(ck=c, tool=t, text=s) for c, t, s in looks], christ=christ)
    if pic: d['pic'] = pic
    return d
def day(D, base, **k):
    d = dict(base); d.update(k)
    d['god'] = [k['god0'], B(k['god1'])]; d['apply'] = dict(lead=k['lead'], fu=[k['fu']])
    d['note'] = k['note'] + ' ' + end(k['god0'])
    for x in ('god0', 'god1', 'lead', 'fu'): d.pop(x)
    D.append(d)
def save(D, name):
    json.dump(D, open(os.path.join(R, name), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    for d in D: print(d['no'], len(d['note']))
