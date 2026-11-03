# 2027 통독표 9판(313회, 월–토 읽기·주일 쉼) → 앱 데이터 (2026-11-04)
# 격자: 2026-12-28(월)부터 한 주 7칸, 6번 칸 = 주일. 첫 주 0–3번 칸(12/28–12/31)은 비움.
# 옛 날(2027 365판 번호 n)이 새 날 안에 통째로 들어가면 그 날의 원고·질문·안내를 물려받음(목사님 결정 11/4: 권장안 A).
import json, datetime, os
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(H)

def build():
    AB = json.load(open(f'{R}/plan.json'))['abbr']
    FULL = json.load(open(f'{R}/plan.json'))['full']
    old = json.load(open(f'{R}/plan365_2027.json'))
    rows = [l for l in open(f'{H}/plan313_2027.txt', encoding='utf-8') if not l.startswith('#')]
    days = [x.strip() for l in rows for x in l.strip().split('|') if x.strip()]
    tops = [l.strip() for l in open(f'{H}/plan313_topics.txt', encoding='utf-8') if l.strip()]
    assert len(days) == 313 and len(tops) == 313, (len(days), len(tops))

    def chs(spec):
        out = []
        for part in spec.split(';'):
            bk, rg = part.rsplit(' ', 1)
            b = AB.index(bk) + 1
            a, z = (rg.split('-') + [rg])[:2]
            out += [[b, c] for c in range(int(a), int(z) + 1)]
        return out

    def label(ch):
        seg = []
        for b, c in ch:
            if seg and seg[-1][0] == b: seg[-1][2] = c
            else: seg.append([b, c, c])
        u = lambda b: '편' if b == 19 else '장'
        return ' · '.join(f"{FULL[b-1]} {a}{'–'+str(z) if z != a else ''}{u(b)}" for b, a, z in seg)

    own, oldch = {}, {}
    for d in old:
        oldch[d['n']] = [tuple(x) for x in d['ch']]
        for x in d['ch']: own[tuple(x)] = d['n']

    g0 = datetime.date(2026, 12, 28)
    dt = datetime.date(2027, 1, 1)
    out = []
    for i, s in enumerate(days):
        while dt.weekday() == 6: dt += datetime.timedelta(1)
        gi = (dt - g0).days
        ch = chs(s)
        S = set(map(tuple, ch))
        ns = sorted(set(own[tuple(x)] for x in ch))
        src = [n for n in ns if set(oldch[n]) <= S]
        sp=(f"{AB[ch[0][0]-1]} {ch[0][1]}"+(f"-{ch[-1][1]}" if ch[0][0]==ch[-1][0] and ch[-1][1]!=ch[0][1] else (f"-{AB[ch[-1][0]-1]} {ch[-1][1]}" if ch[0][0]!=ch[-1][0] else "")))
        out.append({'i': i + 1, 'gi': gi, 'ds': dt.isoformat(), 'ch': ch, 'spec': sp, 'label': label(ch), 'topic': tops[i],
                    'prim': (ns[0] if len(ns)==1 and oldch[ns[0]]==[tuple(x) for x in ch] else 0),  # 11/4 목사님: 옛 원고는 폐기, 범위가 똑같은 날만 재사용
                     'src': src, 'part': [n for n in ns if n not in src]})
        dt += datetime.timedelta(1)
    assert out[-1]['ds'] == '2027-12-31'
    allc = [tuple(x) for d in out for x in d['ch']]
    assert len(allc) == 1189 and len(set(allc)) == 1189
    return out

if __name__ == '__main__':
    o = build()
    print(len(o), o[0], o[-1]['ds'])
