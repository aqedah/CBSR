# 11-28 목사님: "서고 앉는 게 중요합니까?" — 12/18 히 7–10의 찾기·잇기를 자세(서다/앉다)가 아니라 대표 관찰 '단번에'로 옮김.
# 앉으심은 해설에서 단번 제사를 보여 주는 모습으로 한 번만. 서서/앉으사 표시는 평행이 아니라 대조로.
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, '..', 'app', 'site_src', 'trial26_qt.json')
Q = '옛 제사장들은 같은 제사를 자주 드렸습니다(10:11). 그리스도는 자기 몸을 단번에 드리셨습니다(10:10).'
FIND = '10:3과 10:17에서 해마다 드리는 제사와 그리스도의 제사 뒤에, 죄는 각각 어떻게 됩니까?'
LINK = '그리스도의 제사 뒤에는 왜 다시 드릴 제사가 없을까요? 10:14를 보며 생각해 보세요.'
NOTE = '옛 제사는 해마다 죄를 기억하게 했습니다(10:3). 그런데 그리스도는 자기 몸을 단번에 드리셨습니다. 한 번의 제사로 영원히 온전하게 하셨기에 다시 드릴 제사가 없습니다(10:14). 히브리서는 이것을 앉으신 모습으로 보여 줍니다. 제사장들은 날마다 서 있었지만, 그리스도는 하나님 우편에 앉으셨지요(10:12). 그런데 우리는 이미 용서받은 죄를 스스로 다시 꺼내 들 때가 있습니다. 그럴 때 붙들 말씀이 여기 있습니다.'
END = '하나님은 그리스도의 단번 제사로 우리 죄와 불법을 다시 기억하지 않으시는 분입니다.'
d = json.load(open(P, encoding='utf8')); x = d['qt']['352']; v = x['v27']
x['obs']['q'] = Q; v['find'] = FIND; v['link'] = LINK; x['note'] = NOTE + ' ' + END
for m in v['marks'] + v['looks']:
    if m['tool'] == '∥ 평행' and ('서서' in m['text'] or '앉' in m['text']): m['tool'] = '⇔ 대조'
for pr in x['obs'].get('pair', []):
    if pr and pr[0] == '∥ 평행' and ('서서' in pr[1] or '앉' in pr[1]): pr[0] = '⇔ 대조'
x['guide']['find'] = x['guide'].get('find', '').replace('∥ 평행', '⇔ 대조') if isinstance(x['guide'].get('find'), str) else x['guide'].get('find')
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1); print('ok', len(x['note']))
p = os.path.join(H, 'trial_review23.py'); s = open(p, encoding='utf8').read()
i = s.index("352: dict(link="); j = s.index("353: dict(link="); blk = s[i:j]
blk = "352: dict(link='" + LINK + "',  # 11-28 고침(trial_1128_352.py)\n" + blk[blk.index("  god1="):]
k = blk.index("  note='"); blk = blk[:k] + "  note='" + NOTE + "'),\n"
s = s[:i] + blk + s[j:]; open(p, 'w', encoding='utf8').write(s)
