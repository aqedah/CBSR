#!/usr/bin/env python3
"""성경 골든벨(도전 탭) 문제 자료 만들기.
  원본: ux/goldenbell_src.json (GPT 제안 v2.0, 500문항)
  고침: ux/goldenbell_fix.json (Claude 검수 결과: 오답 바꾸기·인용·난이도·해설)
  결과: site/gb.json (앱이 골든벨을 처음 열 때만 받음)
  외부 링크는 넣지 않음 — 앱 안 본문 창으로 엶. 문항 ID(GB001–GB500)는 바꾸지 않음."""
import json, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
AB = ['창','출','레','민','신','수','삿','룻','삼상','삼하','왕상','왕하','대상','대하','스','느','에','욥','시','잠','전','아','사','렘','애','겔','단','호','욜','암','옵','욘','미','나','합','습','학','슥','말','마','막','눅','요','행','롬','고전','고후','갈','엡','빌','골','살전','살후','딤전','딤후','딛','몬','히','약','벧전','벧후','요일','요이','요삼','유','계']

def parse(ref):
    """'창 1:3, 6–7, 9; 12:2' → 첫 구절 [b,c,v1,v2], 관련 장 [[b,c],…]"""
    b = None; c = None; first = None; chs = []
    for tok in re.split(r';\s*', ref):
        m = re.match(r'\s*([가-힣]+)\s*', tok)
        if m and m.group(1) in AB: b = AB.index(m.group(1)) + 1; tok = tok[m.end():]
        for part in tok.split(','):
            part = part.strip()
            m = re.match(r'(\d+):(\d+)(?:[–-](\d+)(?::(\d+))?)?$', part)
            if m:
                c = int(m.group(1)); a = int(m.group(2))
                if m.group(4): c2 = int(m.group(3)); z = int(m.group(4))
                else: c2 = c; z = int(m.group(3) or a)
                for cc in range(c, c2 + 1):
                    if [b, cc] not in chs: chs.append([b, cc])
                if not first: first = [b, c, a, z if c2 == c else a]
                continue
            m = re.match(r'(\d+)(?:[–-](\d+))?$', part)
            if m and c and not first: first = [b, c, int(m.group(1)), int(m.group(2) or m.group(1))]
    return first, chs

def build(out_path):
    src = json.load(open(os.path.join(D, 'goldenbell_src.json')))
    fx_p = os.path.join(D, 'goldenbell_fix.json')
    fixes = json.load(open(fx_p)) if os.path.exists(fx_p) else []
    Q = {q['id']: q for q in src['questions']}
    n_fix = 0
    for f in fixes:
        q = Q.get(f['id'])
        if not q: print('[골든벨] 없는 문항', f['id']); continue
        oid = f.get('option_id'); opt = next((o for o in q['options'] if o['id'] == oid), None) if oid else None
        k = f.get('field') or ('text' if f['issue'] == 'absurd_option' else '')
        if f['issue'] == 'difficulty' or k == 'difficulty':
            q['difficulty'] = f['new']; n_fix += 1; continue
        if k == 'question': q['question'] = f['new']; n_fix += 1
        elif k == 'explanation': q['explanation'] = f['new']; n_fix += 1
        elif opt is not None and k in ('text', 'feedback'):
            if f.get('new'): opt[k] = f['new']
            if f.get('new_feedback'): opt['feedback'] = f['new_feedback']
            if opt['id'] == q['correct_option_id'] and k == 'feedback': q['explanation'] = opt['feedback']
            n_fix += 1
        else: print('[골든벨] 적용 못함', f['id'], f.get('issue'), k)
    out = []; lv = {'easy': 0, 'medium': 0, 'hard': 0}
    for q in src['questions']:
        rv, chs = parse(q['reference'])
        if not rv: print('[골든벨] 주소 해석 불가', q['id'], q['reference']); continue
        ids = [o['id'] for o in q['options']]
        if len(ids) != 4 or q['correct_option_id'] not in ids: print('[골든벨] 보기·정답 오류', q['id']); continue
        lv[q['difficulty']] += 1
        out.append({'id': q['id'], 'd': q['difficulty'][0], 'bk': q['book'], 'r': q['reference'], 'rv': rv, 'ch': chs,
                    'q': q['question'], 'o': [[o['id'][-8:], o['text'], o['feedback']] for o in q['options']],
                    'a': q['correct_option_id'][-8:], 'x': q['explanation'], 'g': (q.get('scene_groups') or [''])[0]})
    for q in out:
        t = json.dumps(q, ensure_ascii=False)
        for w in ('우리야', '빵'):
            if w in t: print('[골든벨] 개역개정 표기 확인', q['id'], w)
    data = {'v': src.get('content_version', '') + '+c' + str(len(fixes)), 'n': lv, 'q': out}
    s = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    if re.search(r'@' + 'gmail|' + 'aqedah' + '22', s): sys.exit('이메일이 들어 있음')
    open(out_path, 'w').write(s)
    print(f'[골든벨] {len(out)}문항 {lv} · 고침 {n_fix}/{len(fixes)} · {len(s)//1024}KB')
    return data['v']

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else '/tmp/gb.json')
