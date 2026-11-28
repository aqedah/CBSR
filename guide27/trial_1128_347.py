# 11-28 목사님: 12/13 딤전 잇기는 디모데후서와 이어짐 — 디모데는 루스드라 사람(행 16:1–2)이고, 바울이 루스드라에서 돌에 맞은 일(행 14:19)을 보고 알았음(딤후 3:11).
# 박해받는 바울을 본 디모데에게 바울이 박해자였던 과거를 털어놓는다는 흐름으로 관찰 사실·잇기·해설을 고침. trial26_qt.json을 바로 고치고 trial_review23.py도 맞춤.
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app', 'site_src', 'trial26_qt.json')
Q = '디모데는 바울이 루스드라에서 당한 박해를 보고 안 사람입니다(행 14:19; 딤후 3:11). 그런 디모데에게 바울은 자신을 "죄인 중에 내가 괴수"라고 부릅니다(1:15).'
LINK = '바울은 왜 박해받는 자기를 보았던 디모데에게 박해자였던 과거를 털어놓을까요? 1:12–13을 보며 생각해 보세요.'
NOTE = '디모데는 바울이 루스드라에서 돌에 맞던 일을 보고 안 사람입니다(딤후 3:11). 그가 아는 바울은 복음 때문에 박해받는 사도였지요. 그런 디모데에게 바울은 뜻밖의 이야기를 꺼냅니다. 전에 나는 비방자요 박해자요 폭행자였다고 합니다(1:13). 왜 굳이 이 말을 할까요? 자기가 섬기는 힘이 자격에서 나오지 않는다는 것을 알기 때문입니다. 박해하던 사람에게 주님이 직분을 맡기셨습니다(1:12). 그 긍휼이 뒤에 올 사람들에게 소망이 됩니다.'
END = '하나님은 죄인 중의 괴수에게 먼저 오래 참으심을 보이셔서, 뒤에 믿을 사람들에게 본이 되게 하시는 분입니다.'
d = json.load(open(P, encoding='utf8')); x = d['qt']['347']
x['obs']['q'] = Q; x['v27']['link'] = LINK; x['note'] = NOTE + ' ' + END
json.dump(d, open(P, 'w', encoding='utf8'), ensure_ascii=False, indent=1); print('ok', len(x['note']))
if __name__ == '__main__':
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trial_review23.py'); s = open(p, encoding='utf8').read()
    s = s.replace("347: dict(link='바울은 왜 부끄러운 자기 과거를 디모데에게 다시 꺼낼까요? 1:13을 보며 생각해 보세요.',", "347: dict(link='" + LINK + "',  # 11-28 고침(trial_1128_347.py)")
    i = s.index("347: dict(link="); j = s.index("348: dict(link=")
    blk = s[i:j]; k = blk.index("  note='"); blk = blk[:k] + "  note='" + NOTE + "'),\n"
    s = s[:i] + blk + s[j:]; open(p, 'w', encoding='utf8').write(s)
