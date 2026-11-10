# 2027 365일표(4판, 목사님 확정 2026-11-08: 313회 9판 경계 + 52일 분할) → 앱 데이터
# 원본: plan365_2027v4.json(가이드북 작업실 guide.html의 PLAN에서 뽑음, 2026-11-10)
# 격자: 2027-01-01부터 하루 한 칸(365 통독과 같은 7칸 격자, 주일 포함).
# 옛 365판(plan365_2027.json) 날과 범위가 똑같은 날만 그 날의 원고·질문·안내를 물려받음(11/4 결정 그대로).
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
def build():
    P = json.load(open(f'{R}/plan365_2027v4.json'))
    old = json.load(open(f'{R}/plan365_2027.json'))
    oldk = {tuple(map(tuple, d['ch'])): d['n'] for d in old}
    out = []
    for i, d in enumerate(P):
        ch = d['ch']
        out.append({'i': i+1, 'gi': i, 'ch': ch, 'spec': d['spec'], 'label': d['label'], 'topic': d.get('topic', ''),
                    'prim': oldk.get(tuple(map(tuple, ch)), 0)})
    allc = [tuple(x) for d in out for x in d['ch']]
    assert len(out) == 365 and len(allc) == 1189 and len(set(allc)) == 1189
    return out
