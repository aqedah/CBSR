# 11-28 목사님: 책머리 도구 다시 짬
# (11-28 뒤이어 화면에서 고친 것: 이름 해설, 짝 상자 뺌, 아이러니 상자 11쪽, 빈 제목 줄 뺌, 대화 5·5 — 이 스크립트를 다시 돌리지 말고 원고를 바로 고칠 것)
# 서술 도구 13: 침묵은 서술에 둠, 서술 공식(여는 말·맺는 말, 이야기 속 말머리) 넣음, 해설(성취를 알리는 말 포함) 넣음
# 담화 도구 10: 교차·송영 뺌, 이음말(까닭 문장 포함) 넣음, 언약 소송(변론)은 언약 공식에 합침
# 쓰는 곳: guide.html·trial26.html(기본값·도식·쪽 나눔), guide_qt.json·trial26_qt.json의 책머리(f0), 체험판에서 교차·송영을 쓴 날
import json, os, re
R = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(R, '..', 'app', 'site_src')

SYMS = '\n'.join([
 '● 열쇠말|**한 낱말이 본문 전체를 이끕니다.** 다른 말로 번역된 곳에는 〈 〉 안에 원래 낱말을 적었습니다.|창 29–31장의 ‘섬기다’. 야곱의 20년 내내 나옵니다.',
 '◆ 반복|같은 말이나 장면이 거듭됩니다. **같은 말을 힘주어 되풀이하는지, 무엇이 달라지는지** 봅니다.|창 5장의 "죽었더라" 여덟 번.',
 '↗ 점층|내용이 되풀이되면서 점점 심화됩니다. **마지막이 가장 무겁습니다.**|창 22:2 "네 아들 네 사랑하는 독자 이삭".',
 '⇔ 대조|두 대상을 나란히 놓고 비교합니다. **무엇과 무엇을 나란히 놓았는지** 먼저 찾습니다.|출 1:12 바로의 계획과 그 결과.',
 '□ 틀|처음과 끝이 맞물려 하나로 묶입니다. **처음과 끝, 그 사이가 한 단락을 이룹니다.**|시 8:1 [여호와 우리 주여] ⫽ 8:9 [여호와 우리 주여]',
 '¶ 서술 공식|서술자가 정해진 말로 이야기를 열고 닫습니다. **새 단락이 시작되는 곳**입니다. 누가 말하는지 알리는 말머리도 여기에 듭니다.|창 6:9 "이것이 노아의 족보니라" · 왕상 22:42 "여호사밧이 왕이 될 때에".',
 '∽ 전형장면|익숙한 장면의 틀이 다시 나옵니다. **달라진 곳이 뜻을 드러냅니다.**|우물가의 만남 — 창 24장; 29장; 출 2장.',
 '▲ 전환|이야기의 흐름이 **여기서 극적으로 바뀝니다.**|창 8:1 "하나님이 노아와 … 기억하사".',
 'ⓘ 해설|서술자가 잠시 멈추고 독자에게 직접 말합니다. 풀어 주고, 평가하고, **말씀이 이루어졌다고 알립니다.**|왕상 16:34 "여호수아를 통하여 하신 말씀과 같이 되었더라".',
 '○ 속마음|본문이 인물의 속마음을 독자에게만 열어 줍니다. **겉말과 비교하여 읽습니다.**|삼상 18:11 "그가 스스로 이르기를".',
 '◎ 침묵|말해야 할 사람이 말하지 않습니다. 대답이 없다는 것까지만 봅니다.|레 10:3 "아론이 잠잠하니".',
 '⋯ 생략|서술자가 나올 법한 말을 **한 대목에서 뺍니다.** 뒤따르는 반응을 봅니다.|눅 15:21 준비한 말(15:19)에서 "나를 품꾼의 하나로 보소서"가 빠집니다.',
 '?! 아이러니|**겉과 속이 어긋납니다.** 세 가지가 있습니다.|삿 6:12 포도주 틀에 숨은 이를 "큰 용사여".'])
SYMMARKS = '\n'.join(['열쇠말|{동그라미}을 치고, 〈 〉의 낱말은 그 옆에 작게 적습니다.', '반복|{동그라미}, 긴 말은 {물결 밑줄}을 긋고 ¹²³을 붙입니다.',
 '점층|절 앞에 {번호 1 2 3}을 적습니다.', '대조|짝을 이루는 절 앞에 {번호 A A}를 적습니다.', '틀|처음과 끝에 **[ ]**를 칩니다.',
 '서술 공식|{네모}를 칩니다.', '전형장면|같은 틀의 장면 앞에 {번호 A A′}를 적습니다.', '전환|여백에 ▲를 적고, 장면이 바뀌는 곳에는 ┄ 점선을 긋습니다.',
 '해설|여백에 ⓘ를 적습니다.', '속마음|{빗금 형광펜}을 칠합니다.', '침묵|여백에 ◎를 적습니다.', '생략|빠진 자리에 ∧, 더해진 말에 +를 적습니다.', '아이러니|여백에 ?!를 적습니다.'])
DSYMS = '\n'.join([
 '“” 말씀 공식|말하는 사람이 그 말의 권위와 신뢰성을 알리는 정해진 표현입니다. 말을 열거나, 앞서 한 말을 확인하며 맺습니다.|사 1:20 "여호와의 입의 말씀이니라" · 레 19:3 "나는 너희의 하나님 여호와이니라".',
 '♪ 후렴|단락 끝마다 같은 말이 돌아옵니다. 노래의 마디가 나뉘고, 반복해서 부를수록 여운과 감정이 쌓입니다.|시 42:5, 11; 43:5 "내 영혼아 네가 어찌하여 낙심하며" · 암 4:6, 8 "너희가 내게로 돌아오지 아니하였느니라".',
 '∥ 평행|두 줄이 서로 호응하거나 반대 뜻으로 나타납니다. 히브리 시의 특징이며, **둘째 줄이 첫째 줄에서 무엇을 더 쌓는지 봅니다.**|사 1:3 "소는 그 임자를 알고 나귀는 그 주인의 구유를 알건마는 ⫽ // 이스라엘은 알지 못하고 나의 백성은 깨닫지 못하는도다".',
 'if 가정|만일 …하면 …하리라 하는 꼴입니다. 두 길과 그 끝이 나란히 놓입니다.|사 1:19–20 "너희가 즐겨 순종하면 … 거절하여 배반하면".',
 '∴ 이음말|앞뒤 말을 잇는 "그러므로", "이제는", "이는 … 함이라" 같은 말입니다. **앞의 말과 뒤의 말이 어떻게 이어지는지**, 명령에 어떤 까닭이 붙었는지 봅니다.|롬 12:1 "그러므로 형제들아" · 레 19:2 "너희는 거룩하라 이는 나 여호와 너희 하나님이 거룩함이니라".',
 '¿ 수사적 질문|대답을 구하지 않는 물음입니다. 듣는 사람이 스스로 답하게 합니다.|롬 8:31 "누가 우리를 대적하리요" · 욥 38:4 "네가 어디 있었느냐".',
 '≒ 비유|하나님이나 사람을 다른 것에 빗댑니다. **무엇을 무엇에 빗댔는지, 어디까지 닮았는지** 봅니다.|시 23:1 "여호와는 나의 목자시니".',
 '☞ 호명|듣는 사람을 이름이나 호칭으로 부릅니다. 누구에게 하는 말인지 정해집니다.|신 6:4 "이스라엘아 들으라" · 잠 3:1 "내 아들아".',
 '∞ 언약 공식|"나는 너희 하나님, 너희는 내 백성". 하나님과 백성의 관계를 정하는 말입니다. 백성이 언약을 어기면 하나님은 **그 언약을 근거로 변론하십니다.**|레 26:12 "너희의 하나님이 되고 너희는 내 백성이 될 것이니라" · 미 6:2 "여호와께서 자기 백성과 변론하시며".',
 '※ 상징|숫자, 짐승, 색, 이름이 다른 것을 가리킵니다. **본문이 무어라고 풀어 주는지부터** 봅니다.|계 1:20 "일곱 별은 일곱 교회의 사자요 일곱 촛대는 일곱 교회니라".'])
DSMARKS = '\n'.join(['말씀 공식|{형광펜}으로 칠합니다.', '후렴|{형광펜}으로 칠합니다.', '평행|두 줄 앞에 {번호 A A′}를 적습니다.',
 '가정|"만일", "…하면"에 {동그라미}을 칩니다.', '이음말|잇는 말에 {동그라미}을 칩니다.', '수사적 질문|여백에 ¿를 적습니다.', '비유|여백에 ≒를 적습니다.',
 '호명|부르는 말에 {동그라미}을 칩니다.', '언약 공식|{형광펜}으로 칠합니다.', '상징|여백에 ※를 적습니다.'])
GEN = {'율법': '“” 말씀 공식 · if 가정 · ∴ 이음말', '노래': '∥ 평행 · ♪ 후렴 · ≒ 비유',
       '예언': '“” 말씀 공식 · ∞ 언약 공식 · ¿ 수사적 질문 · ≒ 비유', '편지': '∴ 이음말 · ¿ 수사적 질문 · ☞ 호명'}
def genres(g):
    out = []
    for l in g.split('\n'):
        p = l.split('|')
        if len(p) >= 4 and p[0] in GEN: p[3] = GEN[p[0]]
        out.append('|'.join(p))
    return '\n'.join(out)

SV = lambda body: '<svg viewBox="0 0 15 11" width="15mm" height="11mm" class="dg">' + body + '</svg>'
TX = lambda x, y, t, s=2.6, c='var(--main)', w=700: f'<text x="{x}" y="{y}" font-size="{s}" fill="{c}" font-weight="{w}" text-anchor="middle" font-family="Noto Sans KR">{t}</text>'
CAP = lambda t, y=10.3: TX(7.5, y, t, 1.9, '#666', 400)
DG = {
 '서술 공식': SV('<rect x="1.2" y="1.6" width="5.2" height="2.6" rx=".4" fill="none" stroke="var(--main)" stroke-width=".35"/>' + TX(3.8, 3.5, '족보', 1.7) +
                '<line x1="7.4" y1="2.9" x2="13.8" y2="2.9" stroke="#bbb" stroke-width=".3"/><line x1="1.2" y1="5.6" x2="13.8" y2="5.6" stroke="#bbb" stroke-width=".3"/><line x1="1.2" y1="7" x2="9" y2="7" stroke="#bbb" stroke-width=".3"/>' + CAP('정해진 여는 말', 10.4)),
 '해설': SV('<line x1="1" y1="3" x2="14" y2="3" stroke="#bbb" stroke-width=".3"/><line x1="1" y1="7.2" x2="14" y2="7.2" stroke="#bbb" stroke-width=".3"/>' +
                '<rect x="4.2" y="3.9" width="6.6" height="2.4" rx="1.2" fill="color-mix(in srgb,var(--main) 18%,#fff)" stroke="var(--main)" stroke-width=".3"/>' + TX(7.5, 5.7, 'ⓘ', 1.9) + CAP('서술자가 끼어듦', 10.4)),
 '이음말': SV('<rect x="1" y="2.5" width="4.2" height="3.4" rx=".6" fill="none" stroke="var(--main)" stroke-width=".35"/><rect x="9.8" y="2.5" width="4.2" height="3.4" rx=".6" fill="none" stroke="var(--main)" stroke-width=".35"/>' +
             '<line x1="5.2" y1="4.2" x2="9.8" y2="4.2" stroke="var(--main)" stroke-width=".35"/>' + TX(7.5, 3.6, '∴', 2.4) + CAP('어떻게 이어지나')),
}

def html(p):
    s = open(p, encoding='utf8').read()
    def put(key, val, q):  # 기본값 한 줄 갈아 끼움
        nonlocal s
        pat = re.compile(r'^( %s:)(".*?(?<!\\)"|\'.*?(?<!\\)\'),$' % key, re.M)
        assert pat.search(s), key
        s = pat.sub(lambda m: m.group(1) + json.dumps(val, ensure_ascii=False) + ',', s, count=1)
    put('symhead', '이야기를 읽는 열세 가지 도구', 0); put('dshead', '대화를 읽는 열 가지 도구', 0)
    put('syms', SYMS, 0); put('dsyms', DSYMS, 0); put('symmarks', SYMMARKS, 0); put('dsmarks', DSMARKS, 0)
    gp = re.compile(r"^( genres:)'(.*?)',$", re.M); gm = gp.search(s); assert gm
    gv = gm.group(2).replace('\\n', '\n').replace("\\'", "'")
    s = s[:gm.start(2)-1] + json.dumps(genres(gv), ensure_ascii=False) + s[gm.end(2)+1:]
    m = re.search(r'^const TDG27=(\{.*\});$', s, re.M); T = json.loads(m.group(1))
    for k in ('교차', '송영'): T.pop(k, None)
    T.update(DG)
    s = s[:m.start(1)] + json.dumps(T, ensure_ascii=False) + s[m.end(1):]
    # 11-28: 이야기 도구 13은 6·7로 나누고, 아이러니 세 가지 상자는 13쪽 짝 표 아래로(아이러니는 이야기와 말 모두에서 씀)
    s = s.replace("const extra=k===1?`<div class=\"irb\"><p class=\"irh\">${esc(f.irhead)}</p>", "const IRB=`<div class=\"irb\"><p class=\"irh\">${esc(f.irhead)}</p>", 1)
    old = "}).join('')}</div>`\n    :k===3?`<div class=\"irb\"><p class=\"irh\">${esc(f.dsphead||'')}</p>"
    assert old in s, 'irb'
    s = s.replace(old, "}).join('')}</div>`;\n  const extra=k===1?''\n    :k===3?`<div class=\"irb\"><p class=\"irh\">${esc(f.dsphead||'')}</p>", 1)
    old2 = "${f.dspnote?`<p class=\"prn\">${esc(f.dspnote)}</p>`:''}</div>`:'';"
    assert old2 in s, 'irb2'
    s = s.replace(old2, "${f.dspnote?`<p class=\"prn\">${esc(f.dspnote)}</p>`:''}</div>`+IRB:'';", 1)
    open(p, 'w', encoding='utf8').write(s)

def qt(p):
    d = json.load(open(p, encoding='utf8')); f = d['qt']['f0']
    f['syms'] = SYMS; f['dsyms'] = DSYMS; f['genres'] = genres(f['genres'])
    for k in ('symhead', 'dshead', 'symmarks', 'dsmarks'): f.pop(k, None)
    json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    for h in ('guide.html', 'trial26.html'): html(os.path.join(A, h))
    for j in ('guide_qt.json', 'trial26_qt.json'): qt(os.path.join(A, j))
    print('ok')

# 체험판에서 교차·송영을 쓴 날: 다른 도구로(원고 trial_w*.py와 작업대 JSON 둘 다)
RETAG = [  # (본문 일부, 새 도구, 문장 고침)
 ('12장은 은사를, 14장은', '[ ] 틀', None),
 ('어디까지 낮아지시고', '⇔ 대조', None), ('종의 형체를 가지시고 십자가에', '⇔ 대조', None),
 ('하루와 천 년의 차례를', '∥ 평행', None),
 ('근심으로 시작한 세 장은', '⇔ 대조', None), ('9장을 큰 근심으로 시작한', '⇔ 대조', None),
 ('갈라디아서는 인사 끝에', '⋯ 생략', ('인사 끝에 송영을 두고', '인사 끝에 영광을 돌리는 찬송을 두고')),
 ('곧이어 무엇을 드립니까', '▲ 전환', None), ('하고 고백한 바로 뒤에', '▲ 전환', None),
 ('모두 자기를 버렸다고', '⇔ 대조', ('송영으로 맺습니다', '찬송으로 맺습니다')),
 ('유다서는 어떤 찬송으로', '⇔ 대조', None), ('는 권면으로 시작해', '⇔ 대조', ('하는 송영으로 끝납니다', '하는 찬송으로 끝납니다')),
]
def retag_json(p):
    d = json.load(open(p, encoding='utf8')); n = 0
    for k, x in d['qt'].items():
        v = x.get('v27') or {}
        for m in v.get('marks', []) + v.get('looks', []):
            if m.get('tool') in ('× 교차', '☆ 송영'):
                for key, tool, fix in RETAG:
                    if key in m['text']:
                        m['tool'] = tool; n += 1
                        if fix: m['text'] = m['text'].replace(*fix)
                        break
                else: raise SystemExit('남은 것 ' + k + ' ' + m['text'][:30])
        DAYMAP = {'329': '⇔ 대조', '340': '⋯ 생략', '347': '▲ 전환', '349': '▲ 전환', '348': '⇔ 대조', '356': '∥ 평행', '359': '⇔ 대조'}
        if k in DAYMAP:  # 옛 칸(오늘의 도구 줄, obs.pair)도 같은 도구로
            g = x.get('guide', {})
            if isinstance(g.get('find'), str): g['find'] = g['find'].replace('☆ 송영', DAYMAP[k]).replace('× 교차', DAYMAP[k])
            for pr in (x.get('obs') or {}).get('pair', []):
                if pr and pr[0] in ('☆ 송영', '× 교차'): pr[0] = DAYMAP[k]
        if 'scenes' in v: v['scenes'] = [s.replace('유다서 믿음의 도와 송영', '유다서 믿음의 도와 찬송') for s in v['scenes']]
    json.dump(d, open(p, 'w', encoding='utf8'), ensure_ascii=False, indent=1); return n
def retag_py(p):
    s = open(p, encoding='utf8').read(); o = s
    for line in s.split('\n'):
        if "'× 교차'" in line or "'☆ 송영'" in line:
            for key, tool, fix in RETAG:
                if key in line:
                    nl = line.replace("'× 교차'", "'%s'" % tool).replace("'☆ 송영'", "'%s'" % tool)
                    if fix: nl = nl.replace(*fix)
                    s = s.replace(line, nl); break
            else: raise SystemExit('남은 것 ' + p + ' ' + line[:60])
    s = s.replace('유다서 믿음의 도와 송영', '유다서 믿음의 도와 찬송')
    if s != o: open(p, 'w', encoding='utf8').write(s)
if __name__ == '__main__':
    import glob
    for j in ('guide_qt.json', 'trial26_qt.json'): print(j, retag_json(os.path.join(A, j)))
    for f in sorted(glob.glob(os.path.join(R, 'trial_w*.py'))): retag_py(f)
