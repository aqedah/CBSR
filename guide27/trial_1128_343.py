# 11-28 목사님: 12/9 빌립보서에 〈 〉 원래 낱말 표기를 하나 넣음(1번: 대표 '기뻐'는 그대로, 눈여겨볼 것에 확인 표시 없이 보탬)
import json, os
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, '..', 'app', 'site_src', 'trial26_qt.json')
T = '"이 마음을 품으라"(2:5), "같은 마음을 품으라"(4:2), "이렇게 생각할지니"〈마음을 품을지니〉(3:15). 같은 말이 편지를 잇습니다.'
d = json.load(open(P, encoding='utf8')); x = d['qt']['343']
if not any('〈마음을 품을지니〉' in m['text'] for m in x['v27']['looks']):
    x['v27']['looks'].append(dict(ck=False, tool='● 열쇠말', text=T)); x['obs'].setdefault('pair', []).append(['● 열쇠말', T])
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
p = os.path.join(H, 'trial_w4.py'); s = open(p, encoding='utf8').read()
a = "        dict(ck=False,tool='?! 아이러니',text='바울이 갇힌 일은 복음을 막을 것처럼 보였습니"
if '〈마음을 품을지니〉' not in s:
    i = s.index(a); j = s.index('\n', i)
    line = s[i:j]; end = line.endswith(']),') or line.endswith(')],')
    s = s[:j] + '' + s[j:]
    # 아이러니 줄 끝의 닫는 괄호 앞에 한 줄 끼움
    k = line.rfind("')"); s = s[:i] + line[:k + 2] + ",\n        dict(ck=False,tool='● 열쇠말',text='" + T.replace("'", "\\'") + "')" + line[k + 2:] + s[j:]
    open(p, 'w', encoding='utf8').write(s)
print('ok')
