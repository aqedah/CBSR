# 그림 분류(도서관식): 주제 폴더(대분류 › 소분류), 때, 계절·날씨. 태그와 설명(memo)으로 자동 분류하고, ux/photo_cats_fix.json으로 손볼 수 있다.
import json,os,re
FULL=json.load(open('plan.json'))['full']
SETN={1:'자연·하늘',2:'족장',3:'애굽·출애굽',4:'광야·성막',5:'정착·사사',6:'왕국',7:'분열·포로',8:'시·지혜·일상',9:'복음서',10:'사도행전·서신',11:'원역사(창 1–11)'}
# (폴더, 태그들, 설명 낱말들) — 위에서부터 먼저 맞는 것
RULES=[
 ('자연 › 날씨 › 폭풍·번개·회오리',['storm_sky','lightning','storm','whirlwind','sandstorm','bolt'],['폭풍','번개','광풍','회오리','풍랑']),
 ('자연 › 날씨 › 비·홍수·무지개',['rain','flood','rainbow'],['비 ','홍수','무지개']),
 ('자연 › 날씨 › 눈·서리·겨울',['winter','frost','snow'],['눈 덮','서리','겨울']),
 ('자연 › 날씨 › 바람·먼지·가뭄',['wind','dust','drought','dry_ground','dry_riverbed'],['먼지','바람','가뭄','갈라진 땅','마른']),
 ('자연 › 하늘 › 해 뜰 무렵',['dawn','sunrise','sunrise_light_rays','morning_star'],['새벽','아침','동틀','해 뜨']),
 ('자연 › 하늘 › 해 질 무렵',['dusk','sunset'],['노을','저녁','해 질','해 지']),
 ('자연 › 하늘 › 밤하늘·별·달',['night_sky','stars','star','moon'],['밤하늘','은하수','별','달빛']),
 ('자연 › 하늘 › 구름·빛줄기',['clouds','cloud','sky','light'],['구름','빛줄기','빛이']),
 ('자연 › 물 › 바다·파도',['sea','waves','island'],['바다','파도']),
 ('자연 › 물 › 강·시내',['river','stream','brook','reeds'],['강','시내','시냇','급류']),
 ('자연 › 물 › 샘·우물·호수',['spring','well','pool','oasis','lake','water'],['샘','우물','호수','물웅덩이']),
 ('자연 › 땅 › 광야·사막',['desert','wilderness_path','red_rock'],['광야','사막','모래']),
 ('자연 › 땅 › 산·바위·협곡',['mountain_peak','mountain','rock','canyon','cave','valley','hill','hills','stones'],['산','바위','협곡','골짜기','동굴','언덕']),
 ('자연 › 땅 › 들·목초지',['field','pasture','land','soil'],['들','풀밭']),
 ('자연 › 땅 › 길',['road','path','roman_road','crossroads','milestone','cairn'],['길']),
 ('자연 › 식물 › 곡식·추수',['wheat_field','grain','harvest','sheaves','wheat','threshing_floor','winnowing','chaff','sickle','seed'],['밀','보리','곡식','추수','타작','겨']),
 ('자연 › 식물 › 포도원·포도',['vineyard','grapes','vine','winepress'],['포도']),
 ('자연 › 식물 › 나무',['tree','trees','olive_tree','fig_tree','palm','cedar','willow','broom_tree','stump','sprout','almond_blossom'],['나무','감람','무화과','종려','백향목','버드나무']),
 ('자연 › 식물 › 꽃·풀',['flowers','grass','poppies','plant','thorns'],['꽃','들풀','풀']),
 ('자연 › 동물 › 양·목자',['sheep','shepherd','lamb','sheepfold','ram','goat'],['양','목자']),
 ('자연 › 동물 › 새',['dove','birds','ravens','eagle','sparrows'],['비둘기','까마귀','새']),
 ('자연 › 동물 › 짐승',['deer','donkey','camel','lion','fox','ant','horse','cattle','oxen','fish','frogs','locusts'],['사슴','나귀','낙타','사자','여우','개미','말','소','물고기']),
]
OBJ=[
 ('물건 › 등불·불·연기',['oil_lamp','lamp','fire','torch','smoke','lampstands','menorah','incense','censer'],['등불','등잔','불','연기','향']),
 ('물건 › 두루마리·글',['scroll','letter','ink','reed_pen','clay_cylinder','stone_tablets','seals'],['두루마리','편지','글','조서','돌판']),
 ('물건 › 그릇·토기·잔',['clay_jar','jar','jars','bowl','bowls','basin','potsherd','flask','cup','silver_cup','alabaster','gold_cups'],['그릇','항아리','토기','잔','옥합']),
 ('물건 › 떡·음식',['bread','meat','flour','manna','oven','fruit','figs'],['떡','음식','만나','화덕']),
 ('물건 › 옷·천',['robe','garment','linen','cloth','sackcloth','white_robes','rags','towel'],['옷','겉옷','베','수건']),
 ('물건 › 무기·전쟁',['army','sword','swords','spear','shield','armor','soldiers','chariot','archers','bow','helmet','sling','siege'],['군대','칼','창','방패','병거','군인']),
 ('물건 › 사슬·감옥·구덩이',['chains','prison','pit','bound','captives'],['사슬','감옥','옥','구덩이']),
 ('물건 › 배·그물',['ship','ships','boat','fishing_boat','harbor','anchor','net','shipwreck','sailors'],['배','그물','항구']),
 ('물건 › 악기',['lyre','trumpet','shofar','timbrel','cymbals','horn'],['수금','나팔','소고','제금']),
 ('물건 › 연장·일감',['tools','loom','millstone','plow','yoke','wheel','potter','needle','plumb_line','olive_press','bricks','brick'],['맷돌','베틀','쟁기','멍에','물레','벽돌']),
]
PLACE=[
 ('장소 › 성막·성전·제단',['tabernacle','tabernacle_court','temple','temple_stones','temple_doors','altar','stone_altar','holy_of_holies','ark','cherubim','laver','veil','high_place'],['성막','성전','제단','언약궤','지성소','산당']),
 ('장소 › 성·성벽·성문',['city_wall','city_gate','gate','fortress','tower','ruins','city','jerusalem','wall','watchman'],['성벽','성문','성','망대','폐허']),
 ('장소 › 궁전·보좌',['palace','throne','king','scepter'],['궁','보좌','왕']),
 ('장소 › 집·마을·방',['house','village','door','roof','rooftop','courtyard','room','window','house_church','threshold','stairs'],['집','마을','문','지붕','다락방','방']),
 ('장소 › 장막·진영',['tent','tents','camp','camp_far','booth'],['장막','진영','초막']),
 ('장소 › 회당·광장·시장',['synagogue','forum','market','judgment_seat'],['회당','광장','시장']),
 ('장소 › 무덤',['rock_tomb','tomb','graves','burial','bones'],['무덤','장사']),
]
PEOPLE=[
 ('사람 › 손·발·몸짓',['hands','hand','feet','priest_hand'],['손','발']),
 ('사람 › 기도·예배·경배',['prayer','bowing','worship','anointing'],['기도','엎드','경배','기름 부']),
 ('사람 › 슬픔·통곡',['sorrow','weeping','ashes','ash','tear'],['통곡','우는','울며','슬픔','재를']),
 ('사람 › 기쁨·잔치·노래',['joy','feast','festival','dance','singers','singer','musicians'],['잔치','기뻐','노래','춤']),
 ('사람 › 일하는 사람',['labor','builder','fishermen','carpenter','sower'],['일하','짓는','쌓는','고기 잡']),
 ('사람 › 가족·아이',['child','children','baby','family','boy','girl','father','son','mother'],['아이','아기','가족','아버지']),
 ('사람 › 길 가는 사람',['pilgrim','caravan','runners','travel'],['길을 가','나그네','행렬']),
 ('사람 › 무리',['crowd','people','men','women','elders','disciples'],['무리','백성','사람들']),
]
TIME=[('새벽·아침',['dawn','sunrise','sunrise_light_rays','morning_star'],['새벽','아침','동틀','해 뜨']),('저녁·노을',['dusk','sunset'],['노을','저녁','해 질','해 지','초저녁']),('밤',['night_sky','night','stars','star','moon','darkness'],['밤','은하수','달빛','어두운']),('한낮',['noon'],['한낮','정오'])]
SEASON=[('겨울·눈·서리',['winter','frost','snow'],['겨울','서리','눈 덮']),('폭풍·비',['storm_sky','storm','lightning','rain','flood','whirlwind','sandstorm','waves'],['폭풍','비 ','번개','광풍','풍랑','회오리']),('가뭄·마른 땅',['drought','dry_ground','dry_riverbed'],['가뭄','마른','갈라진']),('봄·꽃',['flowers','poppies','almond_blossom'],['꽃','봄','싹']),('추수·가을',['harvest','sheaves','threshing_floor','winnowing','grapes','winepress','wheat_field'],['추수','타작','포도','곡식 단'])]
def _m(r,tags,words): T=set(r.get('tags',[])); return bool(T&set(tags)) or any(w in r.get('memo','') for w in words)
def first(r,rules):
    # 태그는 그림의 주인공부터 적혀 있으므로 앞 태그부터 본다
    for tg in r.get('tags',[]):
        for f,t,w in rules:
            if tg in t: return f
    for f,t,w in rules:
        if any(len(x)>=2 and x in r.get('memo','') for x in w): return f
    return None
def classify(r):
    role=r.get('role') or ''
    if r.get('scope')=='s':
        f='성경 장면 › '+SETN.get((r.get('sets') or [0])[0],'기타')
        if r.get('refs'): f+=' › '+FULL[r['refs'][0][0]-1]
    elif role=='symbolic': f='상징·환상'
    elif role=='landscape': f=first(r,RULES) or '자연 › 기타'
    elif role=='setting': f=first(r,PLACE) or first(r,OBJ) or first(r,RULES) or '장소 › 기타'
    elif role=='object': f=first(r,RULES[-3:]) or first(r,OBJ) or first(r,PEOPLE) or first(r,PLACE) or first(r,RULES) or '물건 › 기타'
    else: f=first(r,PEOPLE) or first(r,PLACE) or first(r,OBJ) or first(r,RULES) or '사람 › 기타'
    t=next((n for n,tg,w in TIME if _m(r,tg,w)),'')
    s=next((n for n,tg,w in SEASON if _m(r,tg,w)),'')
    return {'f':f,'t':t,'w':s}
def build(rows):
    fix=json.load(open('ux/photo_cats_fix.json')) if os.path.exists('ux/photo_cats_fix.json') else {}
    out={}
    for r in rows:
        c=classify(r); c.update(fix.get(r['id'],{})); out[r['id']]=c
    json.dump(out,open('ux/photo_cats.json','w'),ensure_ascii=False,indent=0)
    return out
if __name__=='__main__':
    import collections
    R=json.load(open('ux/photos_master.json')); C=build(R)
    act=[r for r in R if not r['out']]
    for k in ('f','t','w'):
        print('==',k); print(collections.Counter(C[r['id']][k] for r in act).most_common())
