# 11-26 목사님: 12/1 성품 물음 '지금 내 수고' → '지금 내 열심' (청년에게 와닿는 말)
import json
for n in range(1, 8):
    p = f'/home/claude/cbsr/guide27/trial_w{n}.json'
    try: W = json.load(open(p, encoding='utf8'))
    except FileNotFoundError: continue
    ch = 0
    for D in W:
        if D.get('no') == 335:
            D['god'][1] = '<b>그 하나님 앞에서, 지금 내 열심을 어떻게 바라보고 있습니까?</b>'; ch = 1
    if ch: json.dump(W, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1); print(p)
