# 2027 365일표 5판 (2026-11-24 목사님 확정). 4판(plan365_2027v4.json)에서 아래만 바꿉니다.
#  창 12–14 / 15–17 / 18–19 (15장과 17장 두 언약)        창 32–33 / 34–36
#  출 39–40 · 레 1–3 한날(출 40 → 레 1 이음새를 한날 안에)  삼하 5–6 / 7–10 / 11–12 , 삼하 15–16 / 17–18(4판 그대로)
#  시 1–7 한날   눅 19–21 한날   행 6–8 / 9–11 / 12 / 13–14 / 15–16 / 17–18   롬 12–16 한날(4판 그대로)
#  (11-24 밤 고침: 삼하 15–18 한날은 2,428어절로 너무 무거워 다시 나누고, 대신 롬 12–13 / 14–16을 다시 한날로)
# 다시 돌려도 됩니다: 원고는 지금 쓰고 있는 표(plan365_2027v5.json, 없으면 4판)에서 범위가 같은 새 날로 옮깁니다.
# 결과: 365일 그대로, 1/1 창 1 → 12/31 계 22. 날 번호는 날짜(1월 1일 = 1)라서 주일 번호와 인도자 QR은 그대로입니다.
# 하는 일: ① plan365_2027v5.json ② guide.html의 PLAN과 권 경계 ③ guide_qt.json·book1.json 원고를 범위가 같은 새 날로 옮김
#          (범위가 바뀐 날의 원고는 guide27/archive_v4_days.json에 보관) ④ 책머리 보기 날짜
import json, os, re, sys, datetime as dt
A = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(A)
sys.path.insert(0, A)
P4 = json.load(open(f'{A}/plan365_2027v4.json'))
BIB = json.load(open(f'{A}/tools/bible_vc.json')) if os.path.exists(f'{A}/tools/bible_vc.json') else None

ID = {'창': 1, '출': 2, '레': 3, '삼하': 10, '시': 19, '눅': 42, '행': 44, '롬': 45}
def ch(b, a, z): return [[ID[b], c] for c in range(a, z + 1)]
G = [  # (4판에서 바꾸는 날들, 5판의 새 날들)
 (['창 12-16', '창 17-19'], [ch('창', 12, 14), ch('창', 15, 17), ch('창', 18, 19)]),
 (['창 32-36'], [ch('창', 32, 33), ch('창', 34, 36)]),
 (['출 39-레 1', '레 2-3'], [ch('출', 39, 40) + ch('레', 1, 3)]),
 (['삼하 5-7', '삼하 8-9', '삼하 10-12'], [ch('삼하', 5, 6), ch('삼하', 7, 10), ch('삼하', 11, 12)]),
 (['시 1-2', '시 3-7'], [ch('시', 1, 7)]),
 (['눅 19', '눅 20-21'], [ch('눅', 19, 21)]),
 (['행 6-9', '행 10-12', '행 13-14', '행 15', '행 16-18'], [ch('행', 6, 8), ch('행', 9, 11), ch('행', 12, 12), ch('행', 13, 14), ch('행', 15, 16), ch('행', 17, 18)]),
]
# 책 이름(4판 이름표에서)
ABBR, NAME = {}, {}
for d in P4:
    bks = []
    for b, _ in d['ch']:
        if b not in bks: bks.append(b)
    for b, part in zip(bks, d['label'].split(' · ')): NAME.setdefault(b, re.sub(r'\s*\d.*$', '', part))
    for b, part in zip(bks, re.split(r'-(?=\D)', d['spec'])): ABBR.setdefault(b, part.split()[0])
def spec(c):
    bs = []
    for b, n in c:
        if not bs or bs[-1][0] != b: bs.append([b, n, n])
        else: bs[-1][2] = n
    if len(bs) == 1:
        b, a, z = bs[0]; return f"{ABBR[b]} {a}" + (f"-{z}" if z != a else '')
    return f"{ABBR[bs[0][0]]} {bs[0][1]}-{ABBR[bs[-1][0]]} {bs[-1][2]}"
def label(c):
    bs = []
    for b, n in c:
        if not bs or bs[-1][0] != b: bs.append([b, n, n])
        else: bs[-1][2] = n
    return ' · '.join(f"{NAME[b]} {a}" + (f"–{z}" if z != a else '') + "장" for b, a, z in bs)

def build():
    first = {g[0][0]: g for g in G}; skip = {s for g in G for s in g[0]}
    out = []; old_by = {tuple(map(tuple, d['ch'])): d for d in P4}
    for d in P4:
        if d['spec'] in first:
            for c in first[d['spec']][1]:
                o = old_by.get(tuple(map(tuple, c)))
                out.append({'ch': c, 'spec': spec(c), 'label': label(c), 'topic': o.get('topic', '') if o else ''})
        elif d['spec'] in skip: continue
        else: out.append({'ch': d['ch'], 'spec': d['spec'], 'label': d['label'], 'topic': d.get('topic', '')})
    assert len(out) == 365, len(out)
    allc = [tuple(x) for d in out for x in d['ch']]; assert len(allc) == 1189 and len(set(allc)) == 1189
    t0 = dt.date(2027, 1, 1)
    return [{'n': i + 1, 'date': (t0 + dt.timedelta(i)).isoformat(), **d} for i, d in enumerate(out)]

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(A, "tools")); from bq_local import VC  # 장마다 절 수
    PREV = json.load(open(f'{A}/plan365_2027v5.json')) if os.path.exists(f'{A}/plan365_2027v5.json') else P4
    P5 = build()
    json.dump(P5, open(f'{A}/plan365_2027v5.json', 'w'), ensure_ascii=False, indent=0)
    # ② guide.html PLAN
    LAST = {}
    for b, c in [tuple(x) for d in P5 for x in d['ch']]: LAST[b] = max(LAST.get(b, 0), c)
    def rng(c, lab):
        bs = []
        for b, n in c:
            if not bs or bs[-1][0] != b: bs.append([b, n, n])
            else: bs[-1][2] = n
        if len(bs) == 1: return lab + '을'
        return f"{NAME[bs[0][0]]} {bs[0][1]}장부터 {NAME[bs[-1][0]]} {bs[-1][2]}장까지"
    PL = []
    for d in P5:
        t = dt.date.fromisoformat(d['date']); vv = sum(VC[b][n - 1] for b, n in d['ch'])
        ends = []
        for b, n in d['ch']:
            if n == LAST[b] and NAME[b] not in ends: ends.append(NAME[b])
        PL.append({'no': d['n'], 'm': t.month, 'd': t.day, 't': d['label'], 'rng': rng(d['ch'], d['label']), 'sub': d['topic'],
                   'nch': len(d['ch']), 'vv': vv, 'min': int(vv / 7.5 + 0.5), 'end': ends})
    gp = f'{A}/site_src/guide.html'; s = open(gp).read()
    old = json.loads(re.search(r'const PLAN=(\[.*?\]);', s).group(1))
    # 생성기 확인: 4판에서 범위가 같은 날은 옛 PLAN과 같아야 함
    ob = {o['t']: o for o in old}
    bad = [p['t'] for p in PL if p['t'] in ob and {k: v for k, v in ob[p['t']].items() if k not in ('no', 'm', 'd')} != {k: v for k, v in p.items() if k not in ('no', 'm', 'd')}]
    if bad: print('생성기 차이', bad[:5])
    s = re.sub(r'const PLAN=\[.*?\];', lambda m: 'const PLAN=' + json.dumps(PL, ensure_ascii=False, separators=(',', ':')) + ';', s, count=1)
    # 권 경계: 1권 창–룻 · 2권 삼상–에 · 3권 욥–아 · 4권 사–말 · 5권 마–계
    lastof = lambda bk: max(d['n'] for d in P5 if any(b == bk for b, _ in d['ch']))
    q1, q2, q3, q4 = lastof(8), lastof(17), lastof(22), lastof(39)
    s, k = re.subn(r'\(p\.no<=\d+\?1:p\.no<=\d+\?2:p\.no<=\d+\?3:p\.no<=\d+\?4:5\)', f'(p.no<={q1}?1:p.no<={q2}?2:p.no<={q3}?3:p.no<={q4}?4:5)', s); assert k == 1
    # ④ 책머리 보기 날짜
    def md(b, c):
        n = next(d['n'] for d in P5 if [b, c] in d['ch']); t = dt.date(2027, 1, 1) + dt.timedelta(n - 1); return f'{t.month}/{t.day}'
    for (b, c), tail in [((1, 15), ' 창 15:6'), ((4, 32), ' 민 32:17'), ((2, 12), ' 유월절 양'), ((2, 12), ' 출 12:46'), ((1, 11), ' 바벨의')]:
        s = re.sub(r'\|\d{1,2}/\d{1,2}' + re.escape(tail), lambda m: '|' + md(b, c) + tail, s)
    s = re.sub(r'"p":\{"no":\d+,"m":1,"d":\d+,"t":"출애굽기 14–15장"', lambda m: (lambda n: f'"p":{{"no":{n},"m":1,"d":{n},"t":"출애굽기 14–15장"')(next(d['n'] for d in P5 if d['label'] == '출애굽기 14–15장')), s)
    open(gp, 'w').write(s)
    print('권 경계', q1, q2, q3, q4)
    # ③ 원고 옮기기
    key4 = {d['n']: tuple(map(tuple, d['ch'])) for d in PREV}; new5 = {tuple(map(tuple, d['ch'])): d['n'] for d in P5}
    MAP = {o: new5.get(c) for o, c in key4.items()}
    AP = f'{ROOT}/guide27/archive_v4_days.json'
    arch = json.load(open(AP)) if os.path.exists(AP) else {'설명': '2027 통독표 5판(2026-11-24)으로 범위가 바뀐 날의 옛 원고. 새 날 원고를 쓸 때 참고합니다.', 'guide_qt': {}, 'book1': []}
    qp = f'{A}/site_src/guide_qt.json'; J = json.load(open(qp)); Q = J['qt']; NQ = {}
    for k, v in Q.items():
        if not k.isdigit(): NQ[k] = v; continue
        o = int(k); n = MAP.get(o)
        if n: NQ[str(n)] = v
        else: arch['guide_qt']['옛 ' + k + ' ' + next(d['label'] for d in PREV if d['n'] == o)] = v
    J['qt'] = NQ; json.dump(J, open(qp, 'w'), ensure_ascii=False, indent=1)
    bp = f'{ROOT}/guide27/book1.json'; L = json.load(open(bp)); NL = []
    WD = '월화수목금토일'
    for D in L:
        n = MAP.get(D['no'])
        if not n: arch['book1'].append(D); continue
        t = dt.date(2027, 1, 1) + dt.timedelta(n - 1); D['no'] = n
        if 'date' in D: D['date'] = f"{t.month}월 {t.day}일 ({WD[t.weekday()]})"
        NL.append(D)
    json.dump(NL, open(bp, 'w'), ensure_ascii=False, indent=1)
    json.dump(arch, open(AP, 'w'), ensure_ascii=False, indent=1)
    moved = {o: n for o, n in MAP.items() if n and n != o}
    print('보관함', list(arch['guide_qt'])[-6:], '옮긴 날', len(moved))
    # 2027 원고 원본(week*.py·json)의 날 번호와 날짜도 옮김
    for w in (1, 2, 3):
        wp = f'{ROOT}/guide27/week{w}.py'; ws = open(wp).read()
        def rep(m):
            o = int(m.group(1)); n = MAP.get(o)
            if n is None: return f"no=-{o},date='(옛 {o}일: 5판에서 범위가 바뀜, 보관용)'"
            t = dt.date(2027, 1, 1) + dt.timedelta(n - 1); return f"no={n},date='{t.month}월 {t.day}일 ({WD[t.weekday()]})'"
        open(wp, 'w').write(re.sub(r"no=(\d+),date='[^']*'", rep, ws))
        jp = f'{ROOT}/guide27/week{w}.json'; WL = json.load(open(jp))
        for D in WL:
            if D['no'] > 0 and MAP.get(D['no']):
                n = MAP[D['no']]; t = dt.date(2027, 1, 1) + dt.timedelta(n - 1); D['no'] = n; D['date'] = f"{t.month}월 {t.day}일 ({WD[t.weekday()]})"
            elif D['no'] > 0: D['no'] = -D['no']
        json.dump(WL, open(jp, 'w'), ensure_ascii=False, indent=1)
