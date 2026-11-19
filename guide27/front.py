import re
css=open('css.css').read()
bcss=re.search(r"extra='''(.*?)'''",open('build.py').read(),re.S).group(1)
miniL=open('miniL.html').read(); miniR=open('miniR.html').read()
S=0.56

def b(t): return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
def vs(t): return re.sub(r'(?<=\()([^()]*\d+:\d+[^()]*)(?=\))',r'<span class="vs">\1</span>',t)

# ---------- 8–9 이 책 쓰는 법 ----------
stepsL=[('오늘의 흐름','읽기 전에 오늘 본문의 **줄거리**를 잡습니다. 낯선 낱말은 말뜻에서 봅니다.'),
        ('성경 읽기','**성경책을 펴서** 읽으며, 이 책이 짚어 준 곳에 표시합니다. 바탕색이 칠해진 표시가 오늘의 **대표 관찰**입니다.'),
        ('눈여겨볼 것','다 읽고 돌아와 ✓ 항목으로 **내 표시를 확인**하고, 이어지는 관찰을 읽습니다.')]
stepsR=[('나의 묵상','본문 관찰, 하나님의 성품, 적용, 오늘의 기도를 **손으로 씁니다.** 칸마다 한두 문장이면 넉넉합니다. 정답은 없습니다.'),
        ('쓴 뒤에 읽기','**④를 다 쓴 뒤에** 아래 띠의 해설과 기도를 읽습니다. 해설은 본문의 뜻을 풀고, 이 본문의 하나님이 어떤 분인지로 맺습니다.')]
calL=[('.hd2','머리','날짜와 오늘 읽을 본문, 성경 읽기에 걸리는 시간'),
      ('.wd','말뜻','본문에 나오는 낯선 낱말'),
      ('.scn','장면 단추','오늘 본문이 몇 장면으로 나뉘는지'),
      ('.mi.rep','대표 관찰','오늘 묵상이 여기서 시작됩니다'),
      ('.two','눈여겨볼 것','✓는 내가 표시한 것을 확인하는 항목'),
      ('.lab','성경 전체로','오늘 본문이 성경 전체와 이어지는 곳')]
calR=[('lab:0','본문 관찰','대표 관찰을 끝까지 따라갑니다'),
      ('lab:1','하나님의 성품','짚어 준 구절의 하나님이 내게 어떻게 다가오는지'),
      ('lab:2','적용','하나님이 하신 일 앞에서 내 모습과 할 일'),
      ('lab:3','오늘의 기도','내 말로 드리는 기도'),
      ('.after','해설과 기도','다 쓴 뒤에 읽습니다')]
def steps(lst,start,cls):
    return f'<div class="hsteps {cls}">'+''.join(f'<div class="hstep"><span class="stn">{start+i}</span><b>{a}</b><span>{b(t)}</span></div>' for i,(a,t) in enumerate(lst))+'</div>'
def calls(lst): return ''.join(f'<div class="hco" data-t="{s}"><b>{a}</b>{t}</div>' for s,a,t in lst)
mini=lambda h,side: f'<div class="howmini" style="{side}:0;width:{148*S:.2f}mm;height:{210*S:.2f}mm"><div style="transform:scale({S});transform-origin:0 0;width:148mm;height:210mm">{h}</div></div>'
P8=f'''<div class="pg fm q1 howpgx"><p class="fh">이 책 쓰는 법</p>
<p class="fp sm hlead">하루는 펼친 두 쪽입니다. <b>왼쪽 면</b>은 성경을 읽기 전과 읽은 뒤에 봅니다.</p>
<div class="howwrap L">{mini(miniL,'right')}{calls(calL)}<svg class="howsvg"></svg></div>
{steps(stepsL,1,'s3')}<div class="pn">8</div></div>'''
P9=f'''<div class="pg fm r q1 howpgx"><p class="fh">&nbsp;</p>
<p class="fp sm hlead"><b>오른쪽 면</b>은 손으로 씁니다. 본문 앞에서 솔직하게 쓰며 은혜를 사모합시다.</p>
<div class="howwrap R">{mini(miniR,'left')}{calls(calR)}<svg class="howsvg"></svg></div>
{steps(stepsR,4,'s2')}<div class="pn">9</div></div>'''

# ---------- 도구 ----------
G='var(--main)'
def svg(body,w=15,h=11): return f'<svg viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm" class="dg">{body}</svg>'
ln=lambda x1,y1,x2,y2,sw=.35,c=G,da='': f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}" {("stroke-dasharray=%s"%da) if da else ""}/>'
dot=lambda x,y,r=.9,f=G: f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}"/>'
txt=lambda x,y,t,s=2.6,c=G,w=700: f'<text x="{x}" y="{y}" font-size="{s}" fill="{c}" font-weight="{w}" text-anchor="middle" font-family="Noto Sans KR">{t}</text>'
box=lambda x,y,w,h,f='none',c=G: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx=".6" fill="{f}" stroke="{c}" stroke-width=".35"/>'
D={
'lead': svg(ln(1,5.5,14,5.5,.3,'#bbb')+''.join(dot(x,5.5) for x in (2.5,6,9.5,13))+txt(7.5,10,'한 낱말이 끝까지',1.9,'#666',400)),
'rep': svg(txt(2.5,6.5,'A')+txt(6.5,6.5,'A')+txt(10.5,6.5,"A′")+ln(9,8,12,8,.3)+txt(7.5,10.5,'무엇이 달라지나',1.9,'#666',400)),
'grad': svg(''.join(f'<rect x="{1.5+i*4.4}" y="{8-2-i*2}" width="3" height="{2+i*2}" fill="{G}" opacity="{.35+i*.3}"/>' for i in range(3))+txt(7.5,10.6,'갈수록 무겁게',1.9,'#666',400)),
'contrast': svg(box(1,2.5,5,4)+box(9,2.5,5,4)+txt(7.5,5.8,'⇔',3)+txt(3.5,5.6,'A',2.4)+txt(11.5,5.6,'B',2.4)+txt(7.5,10.3,'나란히 놓고 비교',1.9,'#666',400)),
'frame': svg(txt(2,6.5,'[',4.2)+txt(13,6.5,']',4.2)+ln(4,5,11,5,.3,'#bbb')+txt(7.5,4,'처음 … 끝',1.9,G,700)+txt(7.5,10.3,'한 단락으로 묶음',1.9,'#666',400)),
'type': svg(box(1,2,3.6,4)+box(5.7,2,3.6,4)+box(10.4,2,3.6,4,'color-mix(in srgb,var(--main) 30%,#fff)')+txt(7.5,10.3,'같은 틀, 다른 장면',1.9,'#666',400)),
'turn': svg(f'<path d="M1 7 L8 7 L13 2.5" fill="none" stroke="{G}" stroke-width=".45"/>'+txt(8,5.5,'▲',2.2)+txt(7.5,10.3,'흐름이 바뀌는 곳',1.9,'#666',400)),
'inner': svg(f'<rect x="1" y="1.5" width="6" height="3.6" rx="1.6" fill="none" stroke="#999" stroke-width=".3"/><circle cx="10.5" cy="3.3" r="2.3" fill="none" stroke="{G}" stroke-width=".35" stroke-dasharray=".6 .5"/>'+txt(4,4.2,'말',1.9,'#777',400)+txt(10.5,4.1,'속',1.9,G,700)+txt(7.5,9.6,'겉말과 속마음',1.9,'#666',400)),
'silence': svg(f'<rect x="4.5" y="1.2" width="6" height="4" rx="1.6" fill="none" stroke="{G}" stroke-width=".35"/>'+txt(7.5,4.3,'…',2.4)+txt(7.5,9.6,'대답이 없음',1.9,'#666',400)),
'omit': svg(box(1,2.5,3,3)+box(5.9,2.5,3,3,'none','#bbb').replace('stroke-width=".35"','stroke-width=".3" stroke-dasharray=".7 .5"')+box(11,2.5,3,3)+txt(7.4,5,'∧',2.4)+txt(7.5,9.8,'빠진 말',1.9,'#666',400)),
'irony': svg(txt(4.5,6,'겉',2.6)+txt(10.5,6,'속',2.6,'#999')+ln(7.5,2,7.5,7.5,.3,'#bbb','.6 .5')+txt(7.5,10.3,'어긋남',1.9,'#666',400)),
'speech': svg(txt(3,6,'“',4.6)+txt(12,6,'”',4.6)+txt(7.5,5.2,'여호와',1.9,'#666',400)+txt(7.5,10.3,'누가 말하나',1.9,'#666',400)),
'refrain': svg(''.join(box(1+i*4.7,2,3.8,4.5)+f'<rect x="{1+i*4.7}" y="5" width="3.8" height="1.5" fill="{G}"/>' for i in range(3))+txt(7.5,10.3,'끝마다 같은 말',1.9,'#666',400)),
'para': svg(ln(2,3.5,13,3.5,.45)+ln(4,6.5,13,6.5,.45)+txt(1.6,7.4,'∥',2.2)+txt(7.5,10.3,'둘째 줄이 더하는 것',1.9,'#666',400)),
'if': svg(f'<path d="M1.5 5 L6 5 L10 2 M6 5 L10 8" fill="none" stroke="{G}" stroke-width=".4"/>'+dot(10.8,2,.8)+dot(10.8,8,.8,'#bbb')+txt(3.2,3.8,'if',2,G,700)),
'rq': svg(txt(7.5,6.5,'¿',5)+f'<path d="M11 3 A4 4 0 1 1 4 3" fill="none" stroke="#bbb" stroke-width=".3"/>'+txt(7.5,10.3,'듣는 이가 답함',1.9,'#666',400)),
'meta': svg(box(1,2.5,4.5,3.5)+box(9.5,2.5,4.5,3.5,'color-mix(in srgb,var(--main) 30%,#fff)')+txt(7.5,5.4,'≒',2.8)+txt(7.5,10.3,'무엇에 빗댔나',1.9,'#666',400)),
'call': svg(txt(4,6.2,'☞',4)+txt(10.5,5.6,'이스라엘아',1.8,G,700)+txt(7.5,10.3,'누구에게 하는 말',1.9,'#666',400)),
'chi': svg(txt(2,4,'A',2.1)+txt(5.5,5.8,'B',2.1)+txt(9.5,5.8,'B′',2.1)+txt(13,4,'A′',2.1)+f'<path d="M2 5 Q7.5 9 13 5" fill="none" stroke="{G}" stroke-width=".3"/><path d="M5.5 6.6 Q7.5 8 9.5 6.6" fill="none" stroke="{G}" stroke-width=".3"/>'+txt(7.5,10.6,'가운데를 보라',1.8,'#666',400)),
'cov': svg(f'<circle cx="5.6" cy="4.6" r="3" fill="none" stroke="{G}" stroke-width=".4"/><circle cx="9.4" cy="4.6" r="3" fill="none" stroke="{G}" stroke-width=".4"/>'+txt(5,5.3,'하',1.8,G,700)+txt(10,5.3,'백',1.8,G,700)+txt(7.5,10.3,'하나님과 백성',1.9,'#666',400)),
'sym': svg(txt(4,6.2,'※',3.4)+txt(10.5,4.4,'7별',1.8,'#999',400)+txt(10.5,7,'=교회',1.8,G,700)+txt(7.5,10.3,'본문이 푸는 대로',1.9,'#666',400)),
'dox': svg(ln(1,5,10,5,.3,'#bbb')+txt(12.3,6.1,'☆',3.4)+txt(7.5,10.3,'영광으로 닫음',1.9,'#666',400)),
}
MK={'circle':'<span class="o">동그라미</span>','wave':'<span class="w">물결 밑줄</span>','hl':'<span class="hy">형광펜</span>','hatch':'<span class="ht">빗금 형광펜</span>','box':'<span class="bx">네모</span>','br':'<b>[ ]</b>'}
def banner(t): return ''.join(f'<span class="bn">{x}</span>' for x in t.split())
NARR=[ # id, chip, name, desc, mark, example
('lead','●','이끎말','**한 낱말이 본문 전체를 이끕니다.** 다른 말로 옮겨진 곳은 〈 〉에 원래 낱말을 적었습니다.',f'{MK["circle"]}을 치고, 〈 〉의 낱말은 그 옆에 작게 적습니다.','창 29–31장의 ‘섬기다’. 야곱의 스무 해 내내 이 말이 나옵니다.'),
('rep','◆','반복','같은 말이나 장면이 거듭됩니다. 거듭될 때마다 **무엇이 달라지는지**가 핵심입니다.',f'{MK["circle"]}, 긴 말은 {MK["wave"]}을 긋고 ¹²³을 붙입니다.','창 5장의 "죽었더라" 여덟 번. 그 사이에서 에녹만 "하나님이 그를 데려가시므로 세상에 있지 아니하였더라"(5:24).'),
('grad','↗','점층','내용이 되풀이되면서 점점 깊어집니다. **마지막이 가장 무겁습니다.**',f'절 앞에 {banner("1 2 3")}을 적습니다.','창 22:2 "네 아들 네 사랑하는 독자 이삭". 부를수록 좁혀지며 명령이 무거워집니다.'),
('contrast','⇔','대조','두 대상을 나란히 놓고 비교합니다. **무엇과 무엇을 나란히 놓았는지** 먼저 찾습니다.',f'짝을 이루는 절 앞에 {banner("A A")}를 적습니다.','출 1:12 바로가 학대할수록 "더욱 번성하여 퍼져나가니". 계획과 결과가 나란히 놓입니다.'),
('frame','[ ]','틀','처음과 끝이 맞물려 하나로 묶입니다. **처음과 끝, 그 사이가 한 단락을 이룹니다.**',f'처음과 끝에 {MK["br"]}를 칩니다.','시 8:1 [여호와 우리 주여] … 8:9 [여호와 우리 주여]'),
('type','∽','전형장면','익숙한 장면의 틀이 다시 나옵니다. 그러나 늘 같지는 않습니다. **달라진 곳이 뜻을 드러냅니다.**',f'같은 틀의 장면 앞에 {banner("A A′")}를 적습니다.','우물가의 만남 — 창 24장; 29장; 출 2장. 누가 물을 긷는지가 달라집니다.'),
('turn','▲','전환','이야기의 흐름이 **여기서 크게 바뀝니다.**','여백에 ▲를 적고, 장면이 바뀌는 곳에는 ┄ 점선을 긋습니다.','창 8:1 "하나님이 노아와 … 기억하사". 이 말에서 물이 줄어들기 시작합니다.'),
('inner','○','속마음','본문이 인물의 속마음을 독자에게만 열어 줍니다. **겉으로 한 말과 비교하여 읽습니다.**',f'{MK["hatch"]}을 칠합니다.','창 27:41 에서가 "심중에 이르기를 … 내가 내 아우 야곱을 죽이리라".'),
('silence','◎','침묵','말해야 할 사람이 말하지 않습니다. 대답이 없다는 것까지만 봅니다.','여백에 ◎를 적습니다.','레 10:3 두 아들을 잃은 뒤 "아론이 잠잠하니".'),
('omit','⋯','생략','나올 것으로 예상한 말이 **한 대목에서 빠집니다.** 빠진 것이 오히려 드러납니다.','빠진 자리에 ∧, 더해진 말에 +를 적습니다.','눅 15:21 탕자가 준비한 말(15:19)에서 "나를 품꾼의 하나로 보소서"가 빠지고, 곧바로 아버지가 말합니다.'),
('irony','?!','아이러니','**겉과 속이 어긋납니다.** 아래 세 가지가 있습니다.','여백에 ?!를 적습니다.','삿 6:12 포도주 틀에 숨은 기드온을 "큰 용사여".'),
]
DISC=[
('speech','“”','말씀 공식','누가 말하는지 알리는 정해진 말입니다. 여는 말과 맺는 말이 있습니다.',f'{MK["hl"]}으로 칠합니다.','출 12:1 "여호와께서 애굽 땅에서 모세와 아론에게 일러 말씀하시되" · 사 1:20 "여호와의 입의 말씀이니라".'),
('refrain','♪','후렴','단락 끝마다 같은 말이 돌아옵니다. 돌아올 때마다 **무게가 쌓입니다.**',f'{MK["hl"]}으로 칠합니다.','시 42:5, 11; 43:5 "내 영혼아 네가 어찌하여 낙심하며" · 암 4:6, 8 "너희가 내게로 돌아오지 아니하였느니라".'),
('para','∥','평행','두 줄이 서로 호응하거나 반대 뜻으로 짝을 이룹니다. **둘째 줄이 무엇을 더하는지** 봅니다.',f'두 줄 앞에 {banner("A A′")}를 적습니다.','사 1:3 "소는 그 임자를 알고 나귀는 그 주인의 구유를 알건마는 // 이스라엘은 알지 못하고 나의 백성은 깨닫지 못하는도다".'),
('if','if','가정','만일 …하면 …하리라 하는 꼴입니다. **두 길과 그 끝**이 나란히 놓입니다.',f'"만일", "…하면"에 {MK["circle"]}을 칩니다.','사 1:19–20 "너희가 즐겨 순종하면 … 거절하여 배반하면".'),
('rq','¿','수사적 질문','대답을 구하지 않는 물음입니다. 듣는 사람이 스스로 답하게 합니다.','여백에 ¿를 적습니다.','롬 8:31 "누가 우리를 대적하리요" · 욥 38:4 "네가 어디 있었느냐".'),
('meta','≒','비유','하나님이나 사람을 다른 것에 빗댑니다. **무엇을 무엇에 빗댔는지, 어디까지 닮았는지** 봅니다.','여백에 ≒를 적습니다.','시 23:1 "여호와는 나의 목자시니". 목자가 하는 일이 이어지는 절에 나옵니다.'),
('call','☞','호명','듣는 사람을 이름이나 호칭으로 부릅니다. 누구에게 하는 말인지가 정해집니다.',f'부르는 말에 {MK["circle"]}을 칩니다.','신 6:4 "이스라엘아 들으라" · 잠 3:1 "내 아들아".'),
('chi','×','교차','말이 A–B–B′–A′로 되짚어 돌아옵니다. **맞대어 보고, 가운데 무엇이 놓였는지** 살핍니다.',f'절 앞에 {banner("A B B′ A′")}를 적습니다.','사 6:10 마음 – 귀 – 눈 – 눈 – 귀 – 마음.'),
('cov','∞','언약 공식','"나는 너희 하나님, 너희는 내 백성". 하나님과 백성의 관계를 정하는 말이 성경 처음부터 끝까지 이어집니다.',f'{MK["hl"]}으로 칠합니다.','레 26:12 "너희의 하나님이 되고 너희는 내 백성이 될 것이니라".'),
('sym','※','상징','숫자, 짐승, 색, 이름이 다른 것을 가리킵니다. **본문이 무엇이라고 풀어 주는지**부터 봅니다.','여백에 ※를 적습니다.','계 1:20 "일곱 별은 일곱 교회의 사자요 일곱 촛대는 일곱 교회니라".'),
('dox','☆','송영','하나님께 영광을 돌리며 단락을 닫습니다.',f'{MK["hl"]}으로 칠합니다.','시 89:52 "여호와를 영원히 찬송할지어다 아멘 아멘" · 롬 11:36 "그에게 영광이 세세에 있을지어다 아멘".'),
]
IRONY=[('뜻과 반대로 말합니다','소풍 가는 날 비가 오는데 "날씨 참 좋다"','마 27:29 로마 군인이 예수님께 "유대인의 왕이여 평안할지어다".'),
       ('정반대의 결과가 옵니다','늦지 않으려고 지름길로 갔는데 더 늦었다','에 7:10 하만이 모르드개를 매달려던 나무에 자기가 달립니다.'),
       ('독자는 알고 인물은 모릅니다','깜짝 생일잔치가 준비된 줄 모르고 친구가 서운해한다','창 22:1 "하나님이 아브라함을 시험하시려고".')]
def tool(t):
    i,c,n,d,m,e=t
    return f'''<div class="tl"><div class="tdg">{D[i]}</div><div class="ttx"><p class="tn"><span class="chip">{c} {n}</span></p><p class="td">{b(d)}</p><p class="tm"><span class="k">표시</span>{m}</p><p class="te"><span class="k">보기</span>{vs(e)}</p></div></div>'''
def tpage(head,lead,items,pn,right,extra=''):
    return f'<div class="pg fm{" r" if right else ""} q1 tp"><p class="fh">{head}</p>{f"<p class=\"fp sm\">{b(lead)}</p>" if lead else ""}<div class="tls">{"".join(tool(t) for t in items)}</div>{extra}<div class="pn">{pn}</div></div>'
irx='<div class="irb"><p class="irh">?! 아이러니의 세 가지</p>'+''.join(f'<div class="irr"><b>{a}</b><span class="ire">생활 속: {x}</span><span class="irs">{vs(y)}</span></div>' for a,x,y in IRONY)+'</div>'
pairs='<div class="irb"><p class="irh">하는 일은 같고 이름이 다른 짝</p><div class="pr2"><div><b>같은 것이 거듭 나옵니다</b><span>이야기에서는 ◆ 반복, 노래와 예언에서는 ♪ 후렴</span></div><div><b>둘을 나란히 놓습니다</b><span>이야기에서는 ⇔ 대조, 노래와 지혜에서는 ∥ 평행</span></div></div><p class="prn">● 이끎말, [ ] 틀, ▲ 전환, ?! 아이러니는 이야기와 말 모두에서 씁니다.</p></div>'
P10=tpage('이야기를 읽는 열한 가지 도구','**서술 도구**입니다. 성경 저자가 들려주는 이야기에서 씁니다. 하루에 몇 개가 나오든 **도구보다 본문이 먼저입니다.**',NARR[:6],10,False)
P11=tpage('&nbsp;','',NARR[6:],11,True,irx)
P12=tpage('말을 읽는 열한 가지 도구','**담화 도구**입니다. 하나님, 선지자, 시인, 사도가 직접 전하는 말에서 씁니다. 모세의 설교나 한나의 노래처럼 이야기 안에 담긴 말에서도 씁니다.',DISC[:6],12,False)
P13=tpage('&nbsp;','',DISC[6:],13,True,pairs)

fcss='''
body{margin:0;background:#ddd}.spread{display:flex;gap:6mm;padding:6mm;width:max-content}
.pg .o{border:0.25mm solid #111;border-radius:50%/55%;padding:0 0.7mm;white-space:nowrap}
.pg .w{text-decoration:underline wavy;text-decoration-thickness:0.2mm;text-underline-offset:0.6mm;white-space:nowrap}
.pg .hy{background:color-mix(in srgb,var(--main) 28%,#fff);padding:0 0.4mm;white-space:nowrap}
.pg .ht{background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--main) 18%,#fff) 0 0.4mm,#fff 0.4mm 0.9mm);padding:0 0.4mm;white-space:nowrap}
.pg .bx{border:0.25mm solid #111;padding:0 0.6mm;white-space:nowrap}
.pg .bn{display:inline-block;background:var(--main);color:#fff;font-family:"Noto Sans KR",sans-serif;font-size:6.6pt;padding:0 0.8mm;margin-right:0.3mm;border-radius:0.4mm;line-height:1.4}
.howpgx .howwrap{position:absolute;left:var(--pl);right:var(--pr)}
.howmini{position:absolute;top:0;box-shadow:0 0.3mm 1.6mm rgba(0,0,0,.25);overflow:hidden;background:#fff}
.howsvg{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.hsteps.s2 .hstep{flex:1}
.tp .tls{display:flex;flex-direction:column}
.tl{display:flex;gap:2.6mm;padding:1.1mm 0;border-bottom:0.15mm solid #ddd}
.tl:last-child{border-bottom:0}
.tdg{flex:0 0 16mm;display:flex;align-items:flex-start;justify-content:center;padding-top:1mm}
.tdg .dg{display:block;background:color-mix(in srgb,var(--main) 6%,#fff);border-radius:1mm}
.ttx{flex:1;min-width:0}
.ttx p{margin:0}
.tn .chip{font-size:8.6pt;font-weight:700}
.td{font-size:8.5pt;line-height:1.5;margin-top:0.6mm!important;text-align:justify}
.tm,.te{font-family:"Noto Sans KR",sans-serif;font-size:7.8pt;line-height:1.5;color:#333;margin-top:0.4mm!important}
.tm .k,.te .k{display:inline-block;font-weight:700;color:var(--main);margin-right:1.4mm;font-size:7.2pt}
.te{color:#555}
.irb{margin-top:2.4mm;border-top:0.5mm solid var(--main);padding-top:1.6mm}
.irh{font-family:"Noto Sans KR",sans-serif;font-weight:700;color:var(--main);font-size:9.4pt;margin:0 0 1mm}
.irr{display:grid;grid-template-columns:30mm 1fr;column-gap:2mm;font-size:8.4pt;line-height:1.45;padding:0.8mm 0;border-bottom:0.15mm dotted #ccc}
.irr b{font-family:"Noto Sans KR",sans-serif;font-size:8.4pt;grid-row:span 2}
.irr .ire{color:#666;font-size:7.8pt}
.irr .irs{font-size:8.2pt}
.pr2{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.pr2 div{background:color-mix(in srgb,var(--main) 7%,#fff);border-radius:1mm;padding:1.4mm 2mm;font-size:8.2pt;line-height:1.45}
.pr2 b{display:block;font-family:"Noto Sans KR",sans-serif;font-size:8.6pt;color:var(--main);margin-bottom:0.4mm}
.prn{font-size:8pt;color:#555;margin:1.4mm 0 0}
'''
js=r'''<script>
(function(){
 const d=document.createElement('div');d.style.cssText='position:absolute;width:100mm';document.body.appendChild(d);const MM=d.getBoundingClientRect().width/100;d.remove();
 document.querySelectorAll('.tp').forEach(pg=>{const pr=pg.getBoundingClientRect();let mb=0;pg.querySelectorAll(':scope > *:not(.pn)').forEach(e=>{const q=e.getBoundingClientRect();if(q.bottom>mb)mb=q.bottom});const sl=(pr.bottom-11*MM-mb)/MM-1.5;if(sl<=0)return;const T=[...pg.querySelectorAll('.tl')];const ex=pg.querySelector('.irb');const n=T.length*2+(ex?1:0);const add=Math.min(sl/n,1.6);T.forEach(t=>{t.style.paddingTop=t.style.paddingBottom=(1.1+add)+'mm'});if(ex)ex.style.marginTop=(2.4+add)+'mm';});
 (function(){const H=[...document.querySelectorAll('.howpgx .hstep')];const mx=Math.max(...H.map(h=>h.getBoundingClientRect().height));H.forEach(h=>h.style.minHeight=(mx/MM)+'mm');})();
 document.querySelectorAll('.howpgx').forEach(pg=>{
  const w=pg.querySelector('.howwrap'),ld=pg.querySelector('.hlead'),st=pg.querySelector('.hsteps');const pr=pg.getBoundingClientRect();
  const A=(ld.getBoundingClientRect().bottom-pr.top)/MM, B=(st.getBoundingClientRect().top-pr.top)/MM, H=210*0.56;
  w.style.top=(A+(B-A-H)/2).toFixed(2)+'mm'; w.style.height=H+'mm';
  const L=w.classList.contains('L'), mini=w.querySelector('.howmini'), wr=w.getBoundingClientRect(), mm=v=>v/MM;
  const Wmm=mm(wr.width), MW=148*0.56, CW=Wmm-MW-6, mr=mini.getBoundingClientRect(), edge=L?mm(mr.left-wr.left):mm(mr.right-wr.left);
  let prev=-99; const paths=[];
  const items=[...w.querySelectorAll('.hco')].map(c=>{c.style.width=CW+'mm';const t=c.dataset.t;const e=t.startsWith('lab:')?mini.querySelectorAll('p.lab')[+t.slice(4)]:mini.querySelector(t);if(!e)return null;const r=e.getBoundingClientRect();const y=mm(r.top-wr.top)+Math.min(mm(r.height),4)/2;const x=L?mm(r.left-wr.left)-0.6:mm(r.right-wr.left)+0.6;return{c,x,y}}).filter(Boolean).sort((a,b)=>a.y-b.y);
  items.forEach(it=>{it.h=mm(it.c.getBoundingClientRect().height);it.top=Math.max(it.y-2.3,prev+2.2);prev=it.top+it.h});
  const Hmm=mm(wr.height); if(prev>Hmm){for(let i=items.length-1;i>=0;i--){const lim=i<items.length-1?items[i+1].top-items[i].h-2.2:Hmm-items[i].h;if(items[i].top>lim)items[i].top=lim}}
  items.forEach(it=>{it.c.style.top=it.top+'mm';const x0=L?CW+0.8:Wmm-CW-0.8,y0=it.top+2.3,xm=L?edge-2.6:edge+2.6;
   const dd=Math.abs(y0-it.y)<0.6?`M${x0} ${it.y} L${it.x} ${it.y}`:`M${x0} ${y0} L${xm} ${y0} L${xm} ${it.y} L${it.x} ${it.y}`;
   paths.push(`<path d="${dd}" fill="none" stroke="#fff" stroke-width="1.1" opacity=".9"/><path d="${dd}" fill="none" stroke="var(--main)" stroke-width=".32"/><circle cx="${it.x}" cy="${it.y}" r=".85" fill="var(--main)"/>`)});
  const svg=w.querySelector('.howsvg');svg.setAttribute('viewBox',`0 0 ${Wmm} ${Hmm}`);svg.setAttribute('preserveAspectRatio','none');svg.innerHTML=paths.join('');
 });
})();
</script>'''
html=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}\n{bcss}\n{fcss}</style></head><body><div class="spread" id="s89">{P8}{P9}</div><div class="spread" id="s1011">{P10}{P11}</div><div class="spread" id="s1213">{P12}{P13}</div>{js}</body></html>'
open('front.html','w').write(html)
