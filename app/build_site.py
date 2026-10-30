import json,base64,hashlib,os,shutil,re
OUT='site'; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/terrain')
t=open('template3.html').read()
plan=json.load(open('plan.json'))
# 성경연구는 MILALWV로 옮김(2026-10-23): 자리만 남김
t=t.replace('/*STUDY*/','const STUDY_ON=()=>false;\nfunction studyTabSync(){ document.documentElement.classList.remove("study-on"); try{ localStorage.removeItem("cbsr-study"); }catch(e){} if(view.tab==="study") view.tab="read"; }\n')
t=t.replace('/*LEAFLETCSS*/',open('npm/node_modules/leaflet/dist/leaflet.css').read())
data="\n".join(open(f).read() for f in ['engine.js','glossary.js','summaries.js','weeks.js','curated.js','qt_base.js','qt_extra.js','routes.js','incl.js','clues.js'])
data=data.replace('if(typeof module!=="undefined") module.exports={buildEntityIndex,buildGlossIndex,inScope,analyzeDay,makeQuiz,rng};','')
data+="\nconst PLACEINFO="+open('places/all.json').read()+";"
data+="\nconst ROUTES_B="+open('routes/all.json').read()+";"
data+="\nconst PEOPLEINFO="+open('people/all.json').read()+";"
data+="""
(function(){ const MOVE=["벧엘","브니엘","브엘세바","여호와 이레","마라","맛사","므리바","여호와 닛시","길갈","아골","여호와 샬롬","에벤에셀","골고다","겟세마네","실로암"];
  for(const n of NAME_MEAN){ if(!MOVE.includes(n[0])) continue; const p=PLACEINFO[n[0]];
    if(p){ if(!p.m) p.m=n[1]; } else PLACEINFO[n[0]]={k:"기타",v:[[[],n[1],null]]}; }
  for(let i=NAME_MEAN.length-1;i>=0;i--) if(MOVE.includes(NAME_MEAN[i][0])) NAME_MEAN.splice(i,1);
  /* 남은 이름의 뜻은 인물 정보로 합치기 */
  for(const n of NAME_MEAN){ const p=PEOPLEINFO[n[0]]; if(p){ if(!p.m) p.m=n[1]; } else if(n[0]!=="이스라엘"){ const sc=[]; const r=n[2]||[]; for(let i=0;i<r.length;i+=2) for(let b=r[i];b<=r[i+1];b++) sc.push(b); PEOPLEINFO[n[0]]=sc.length?{v:[[sc,n[1],null]],m:n[1],x:1,s:sc}:{v:[[[],n[1],null]],m:n[1]}; } }
  NAME_MEAN.length=0; })();
"""
data+="\nconst NAME_SET=new Set(NAME_MEAN.map(x=>x[0])); for(const n of NAME_MEAN){ if(!GLOSSARY.some(g=>g[0]===n[0])) GLOSSARY.push(n); }"
data+="\nconst LEITWORT="+open('leitwort.json').read()+";\nconst EMPH="+open('emph.json').read()+";\nconst GAZ="+open('gaz.json').read()+";\nconst PLAN="+json.dumps(plan,ensure_ascii=False,separators=(',',':'))+";\n"
tj=json.load(open('terrain.json')); terr={}
for k,v in tj.items():
    shutil.copy(f'terrain_{k}.jpg',f'{OUT}/terrain/{k}.jpg'); terr[k]={"bounds":v["bounds"],"url":f"terrain/{k}.jpg"}
data+="const TERRAIN="+json.dumps(terr)+";\n"
data+="const PLX="+(open("ux/place_extra.json").read() if os.path.exists("ux/place_extra.json") else "{}")+";\n"
data+="const NEARLAND="+open("ux/nearland.json").read()+";\n"
# ── 365 통독표 ──
P365=json.load(open('plan365.json')); AB=plan['abbr']
S365={}
import glob
for f in sorted(glob.glob('s365/part*.json')):
    for k,v in json.load(open(f)).items(): S365[int(k)]=v
def spec365(ch):
    a,b=ch[0],ch[-1]
    return f"{AB[a[0]-1]} {a[1]}" + (f"-{b[1]}" if a[0]==b[0] and b[1]!=a[1] else (f"-{AB[b[0]-1]} {b[1]}" if a[0]!=b[0] else ""))
W365=[];SW=[];DC={};WK=[]
for i in range(0,len(P365),7):
    wk=P365[i:i+7]; w=i//7+1
    W365.append([{"spec":spec365(d['ch']),"label":d['label'],"ch":d['ch'],"topic":d['topic']} for d in wk])
    SW.append([(S365.get(d['n'],{}) or {}).get('s','') for d in wk])
    for j,d in enumerate(wk):
        c=(S365.get(d['n'],{}) or {}).get('c','')
        if c: DC[f"{w}-{j}"]=c
    a,b=wk[0]['ch'][0],wk[-1]['ch'][-1]
    tt=f"{AB[a[0]-1]} {a[1]}–{b[1]}" if a[0]==b[0] else f"{AB[a[0]-1]} {a[1]} – {AB[b[0]-1]} {b[1]}"
    WK.append({"t":tt,"story":"","christ":""})
J=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
data+='const PLAN_INFO={rj:{name:"리딩지저스 45주",short:"45주",src:"리딩지저스 45주 성경통독표(웨스트민스터코리아)",start:"2026-02-23"},y365:{name:"365 성경통독",short:"365일",src:"2026 365일 성경통독표",start:"2026-01-01"}};\n'
_P27=json.load(open('plan365_2027.json')); _D27={}
for _i,(_x,_y) in enumerate(zip(P365,_P27)):
    if _x['ch']!=_y['ch'] or _x['label']!=_y['label']: _D27[_i+1]={"spec":spec365(_y['ch']),"label":_y['label'],"ch":_y['ch'],"topic":_y.get('topic','')}
data+='const P365_27='+J(_D27)+';\n'
A365=json.load(open('s365b/all.json')); GD={};EY={};CQ={}
for i,d in enumerate(P365):
    w,j=i//7+1,i%7; v=A365.get(str(d['n']))
    if not v: continue
    GD[f"{w}-{j}"]=v['g']; EY[f"{w}-{j}"]=v['e']
    CQ[f"{w}-{j+1}"]=[{k:q[k] for k in ('t','kind','q','o','a','h','ref')} for q in v['qz']]
# 리딩지저스에서 손으로 다듬은 QT 질문(요 3–4장: 니고데모·사마리아 여자, 범위·붙잡을 구절 포함)을 365 같은 범위 날에 옮김
_RJ=json.load(open('srj/all.json'))
for _i,_d in enumerate(P365):
    if [tuple(x) for x in _d['ch']]==[(43,3),(43,4)]: EY[f"{_i//7+1}-{_i%7}"]=_RJ['35-1']['e']; Y_TOOL_FROM={f"y365:{_i//7+1}-{_i%7}":"rj:35-0"}
TRV=hashlib.sha1((open('bible_snb.b64').read()[:3000]+open('bible_shg.b64').read()[:3000]).encode()).hexdigest()[:8] if os.path.exists('bible_snb.b64') else '1'
data+='window.TR_VER="'+TRV+'";\n'
data+='const BOOKINFO='+open('books/all.json').read()+';\n'
data+='const RJ_PLAN=PLAN.plan, RJ_WEEKS=WEEKS.slice(), GUIDE={}, EYE={};\n'
data+='/* 시편은 "편" */ PLAN.plan.forEach(w=>w.forEach(d=>{ d.label=d.label.replace(/시편 ([0-9–\\-]+)장/g,"시편 $1편"); }));\n'
data+='window.STUDY_V="0";\n'  # 원문 연구는 MILALWV로 옮김(2026-10-23)
data+='window.CBSR_MODE=(()=>{try{const u=new URLSearchParams(location.search).get("p"); if(u==="rj"||u==="365"){const m=u==="rj"?"rj":"y365"; localStorage.setItem("cbsr-mode",m); return m;} return localStorage.getItem("cbsr-mode")==="y365"?"y365":"rj";}catch(e){return "rj";}})();\nconst DAYC={};\n'
data+='if(window.CBSR_MODE==="y365"){const R=(o,n)=>{for(const k in o)delete o[k];Object.assign(o,n);};\n'
data+=f'PLAN.plan={J(W365)};SUMMARY.length=0;SUMMARY.push(...{J(SW)});WEEKS.length=0;WEEKS.push(...{J(WK)});\n'
data+=f'R(LEITWORT,{open("leitwort365.json").read()});R(EMPH,{open("emph365.json").read()});R(INCL,{open("incl365.json").read()});PLAN.plan.forEach(w=>w.forEach(d=>{{ d.label=d.label.replace(/시편 ([0-9–\\-]+)장/g,"시편 $1편"); }}));R(DETAIL,{{}});R(CURATED,{J(CQ)});Object.assign(GUIDE,{J(GD)});Object.assign(EYE,{J(EY)});ARC_LIST.length=0;Object.assign(DAYC,{J(DC)});}}\n'
ARJ=json.load(open('srj/all.json')); GR={};ER={};CR={}
for k,v in ARJ.items():
    w,d=map(int,k.split('-')); GR[f"{w}-{d-1}"]=v['g']; ER[f"{w}-{d-1}"]=v['e']
    if v['qz']: CR[k]=[{kk:q[kk] for kk in ('t','kind','q','o','a','h','ref')} for q in v['qz']]
data+=f'if(window.CBSR_MODE!=="y365"){{Object.assign(GUIDE,{J(GR)});Object.assign(EYE,{J(ER)});const CR={J(CR)};for(const k in CR) if(!CURATED[k]) CURATED[k]=CR[k];}}\n'
import glob as _g
CK=json.load(open('ux/christ_out.json')); MN=json.load(open('ux/mean_out.json')); GF={}
for f in sorted(_g.glob('ux/guide_out*.json')): GF.update(json.load(open(f)))
data+='const FLOW='+open('flow/all.json').read()+';\n'
data+='const TRAITS_C='+open('traits/all.json').read()+';\n'
data+='const PARA='+open('para/all.json').read()+';\n'
data+='const SCX='+open('scene/scx.json').read()+';\n'
data+='const TOOLX='+(open('tools/toolx.json').read() if os.path.exists('tools/toolx.json') else '{}')+';\n'
data+='if(window.CBSR_MODE==="y365"){const F='+J(Y_TOOL_FROM)+';for(const k in F) if(TOOLX[F[k]]) TOOLX[k]=TOOLX[F[k]];}\n'
data+='const RJDESC='+(open('rjdesc/rjdesc.json').read() if os.path.exists('rjdesc/rjdesc.json') else '{}')+';\n'
data+='const CHRIST_K='+J({k:v['k'] for k,v in CK.items()})+';\n'
FIXD={"35-1":{"god":"밤에 예수님을 찾아온 유대인의 지도자 니고데모와 우물가에서 예수님의 말씀을 듣게 된 사마리아 여자는 서로 다른 자리에서 예수님을 만납니다. 니고데모는 먼저 예수님을 찾아왔고(3:2), 사마리아 여자에게는 예수님이 먼저 말을 거셨습니다(4:7). 예수님은 니고데모에게 인자가 들려야 하며 믿는 자가 영생을 얻는다고 말씀하시고(3:14–15), 사마리아 여자에게는 자신이 메시아이심을 밝히십니다(4:25–26). 여자의 증언으로 많은 사람이 예수님을 믿고(4:39), 이어 예수님의 말씀을 직접 듣고 그분을 세상의 구주로 고백합니다(4:41–42). 서로 다른 사람들에게 자신을 드러내시고 생명의 말씀을 전하시는 예수님을 봅니다.","christ":"요한복음은 창세기처럼 '태초에'라는 말로 시작합니다(요 1:1; 창 1:1). 만물이 말씀으로 말미암아 지은 바 되었고(1:3), 그 말씀이 육신이 되어 우리 가운데 거하셨습니다(1:14). 니고데모에게 말씀하신 거듭남(3:3)과 사마리아 여자에게 약속하신 샘물(4:14)은 서로 다른 그림이지만, 둘 다 사람이 스스로 만들어 낼 수 없는 생명을 가리킵니다. 창조의 말씀이신 예수님이 사람들에게 생명을 주시는 분으로 나타나십니다."}}
RJDAY=json.load(open('ux/christ_rjday.json'))
data+='if(window.CBSR_MODE!=="y365"){const RD='+J(RJDAY)+';for(const k in RD){ if(!DAYC[k]) DAYC[k]=RD[k].t; if(!CHRIST_K["rjd:"+k]) CHRIST_K["rjd:"+k]=RD[k].k; }}\n'
data+='if(window.CBSR_MODE!=="y365"){const FX='+J(FIXD)+';for(const k in FX) DETAIL[k]=Object.assign({},DETAIL[k]||{},FX[k]); CHRIST_K["rjd:35-0"]="흐름";}\n'

data+='(()=>{ const FX='+J({k:v['fix'] for k,v in CK.items() if v.get('fix')})+', MN='+J(MN)+', GF='+J(GF)+';\n'
data+=""" const M=window.CBSR_MODE==="y365"?"y365":"rj";
 for(const k in FX){ const [t,r]=k.split(":");
   if(t==="rjw"&&M==="rj"&&WEEKS[+r-1]) WEEKS[+r-1].christ=FX[k];
   if(t==="rjd"&&M==="rj"){ const [w,d]=r.split("-").map(Number); const o=DETAIL[w+"-"+(d+1)]; if(o) o.christ=FX[k]; }
   if(t==="y"&&M==="y365") DAYC[r]=FX[k]; }
 for(const k in MN){ const n=k.slice(3), o=k.startsWith("pe:")?PEOPLEINFO[n]:PLACEINFO[n]; if(o){ o.m=MN[k].m; o.mc=MN[k].c; } }
 for(const k in GF){ const [m,r]=k.split(":"); if(m!==M) continue; if(GF[k].find&&GUIDE[r]) GUIDE[r].find=GF[k].find; if(GF[k].eye&&EYE[r]) EYE[r].q=GF[k].eye; }
})();\n"""
data+='const KWQ='+open('ux/kwq.json').read()+';\nconst CARDNEWS='+open('ux/cardnews.json').read()+';\n'
_PH=json.load(open('ux/photos.json')) if os.path.exists('ux/photos.json') else []
_SC=json.load(open('ux/story_cards.json')) if os.path.exists('ux/story_cards.json') else {}
_SC={k:v for k,v in _SC.items() if not k.startswith('_')}  # 보관본(_backup)은 앱에 싣지 않음
_PCAT=json.load(open('ux/photo_cats.json')) if os.path.exists('ux/photo_cats.json') else {}
_TM={'밤':'n','저녁·노을':'e','새벽·아침':'d','한낮':'m'}
for _p in _PH:
    _t=_TM.get((_PCAT.get(_p['id']) or {}).get('t',''))
    if _t: _p['tm']=_t
import photo_policy as _pp
_POL=_pp.load(); _PMR={r['id']:r for r in json.load(open('ux/photos_master.json'))} if os.path.exists('ux/photos_master.json') else {}
_perr=_pp.validate(_POL,set(_PMR)); 
if _perr: print('그림 정책 오류:',_perr[:5])
for _p in _PH: _p.update(_pp.app_fields(_pp.effective(_PMR.get(_p['id'],_p),_POL)))
_PH=[_p for _p in _PH if _p['rs'] not in ('hold','out')]  # 보류·제외는 자동·지정·고정 어느 길로도 앱에 나오지 않음
data+='const PHOTOS='+J([{k:v for k,v in p.items() if k in ('id','u','pl','tags','fx','mood','set','sets','scope','refs','kw','deny','role','tm','ak','ap','rs','va','bu','au','rl','er')} for p in _PH])+';\nconst STORYC='+J({k:v for k,v in _SC.items() if not k.startswith('_')})+';\n'
_SRJ=json.load(open('ux/story_rj.json')) if os.path.exists('ux/story_rj.json') else {}
_SRJ={k:v for k,v in _SRJ.items() if not k.startswith('_')}
data+='const STORYC_RJ='+J(_SRJ)+';\n'
data+='const DSTATUS='+(open('edits/status.json',encoding='utf-8').read() if os.path.exists('edits/status.json') else '{}')+';\n'  # 날짜별 승인 상태(관리자 상태판)
Y365NT=json.load(open('ux/christ_y365nt.json'))
DY=json.load(open('ux/detail_y365.json'))
data+='if(window.CBSR_MODE==="y365"){const DY='+J({k:{f:v for f,v in o.items() if not f.startswith('_')} for k,o in DY.items()})+';for(const k in DY) DETAIL[k]=Object.assign({},DETAIL[k]||{},DY[k]);}\n'
YN={f"{(int(n)-1)//7+1}-{(int(n)-1)%7}":v for n,v in Y365NT.items()}
data+='if(window.CBSR_MODE==="y365"){const YN='+J(YN)+';for(const k in YN){ DAYC[k]=YN[k].t; CHRIST_K["y:"+k]=YN[k].k; }}\n'
data+="\nconst TRMAP_SNB="+open('trmap/snb.json').read()+";\nconst TRMAP_SHG="+open('trmap/shg.json').read()+";\n"+open('trconv.js').read()
print("365 summaries:",len(S365))

bible='const BIBLE_B64="'+open('bible.b64').read()+'";\n'
bible+='window.SPEECH_krv='+open('speech/bible.json').read()+';\n'
open(f'{OUT}/bible.js','w').write(bible)
for tk in ('snb','shg'):
    open(f'{OUT}/bible_{tk}.js','w').write('window.BIBLE_TR=window.BIBLE_TR||{};BIBLE_TR.'+tk+'="'+open(f'bible_{tk}.b64').read()+'";\nwindow.SPEECH_'+tk+'='+open(f'speech/bible_{tk}.json').read()+';\n')

h=lambda s:hashlib.sha1(s.encode()).hexdigest()[:8]
for f in ['sync.js','config.js','manifest.webmanifest','firestore.rules','og.png','sample_story.html']: shutil.copy('site_src/'+f,OUT+'/'+f)
shutil.copytree('site_src/icons',OUT+'/icons')
shutil.copytree('site_src/img',OUT+'/img')
FB="https://www.gstatic.com/firebasejs/10.14.1/"
tags=(f'<script src="{FB}firebase-app-compat.js"></script>\n<script src="{FB}firebase-auth-compat.js"></script>\n<script src="{FB}firebase-firestore-compat.js"></script>\n'
      f'<script src="config.js?v={h(open("site_src/config.js").read())}"></script>\n<script src="sync.js?v={h(open("site_src/sync.js").read())}"></script>\n<script src="bible.js?v={h(bible[:5000]+str(len(bible)))}"></script>\n')
body=t.replace('<script>\n/*DATA*/','\n'+tags+'<script>\n'+data)
title=re.search(r'<title>.*?</title>',body).group(0); body=body.replace(title,'',1)
head=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
<meta name="description" content="성경통독 · 오늘 본문, 요약, 지도, 퀴즈, QT">
<meta property="og:type" content="website">
<meta property="og:site_name" content="이야기 통독 노트">
<meta property="og:title" content="이야기 통독 노트">
<meta property="og:description" content="성경통독 · 오늘 본문, 요약, 지도, 퀴즈, QT">
<meta property="og:url" content="https://aqedah.github.io/CBSR/">
<meta property="og:image" content="https://aqedah.github.io/CBSR/og.png?v=3">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2C5C52">
<script>try{{var t=localStorage.getItem("cbsr-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}</script>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="통독 노트">
<link rel="manifest" href="manifest.webmanifest">
<script>window.addEventListener("beforeinstallprompt",function(e){{e.preventDefault();window.__bip=e;}});</script>
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}html{{-webkit-text-size-adjust:100%}}</style>
<style>#appBoot{{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center;background:#F3F5F1;color:#1B2420;transition:opacity .3s ease;font-family:"Gowun Batang","Nanum Myeongjo","AppleMyungjo",serif;text-align:center}}#appBoot.out{{opacity:0;pointer-events:none}}#appBoot .k{{font-family:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:12.5px;letter-spacing:.14em;color:#5B6862}}#appBoot .t{{font-weight:700;font-size:30px;margin-top:10px;color:#2C5C52}}#appBoot .s{{font-size:15px;color:#5B6862;margin-top:8px}}#appBoot .bar{{width:160px;height:2px;background:#D9E0DA;margin:24px auto 0;overflow:hidden;border-radius:2px}}#appBoot .bar i{{display:block;height:100%;width:40%;background:#2C5C52;animation:bootBar 1s ease-in-out infinite}}@keyframes bootBar{{from{{transform:translateX(-100%)}}to{{transform:translateX(250%)}}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) #appBoot{{background:#111714;color:#E4EAE6}}:root:not([data-theme="light"]) #appBoot .t{{color:#8FC4B5}}:root:not([data-theme="light"]) #appBoot .k,:root:not([data-theme="light"]) #appBoot .s{{color:#97A49D}}:root:not([data-theme="light"]) #appBoot .bar{{background:#2A3430}}:root:not([data-theme="light"]) #appBoot .bar i{{background:#8FC4B5}}}}
:root[data-theme="dark"] #appBoot{{background:#111714;color:#E4EAE6}}:root[data-theme="dark"] #appBoot .t{{color:#8FC4B5}}:root[data-theme="dark"] #appBoot .k,:root[data-theme="dark"] #appBoot .s{{color:#97A49D}}:root[data-theme="dark"] #appBoot .bar{{background:#2A3430}}:root[data-theme="dark"] #appBoot .bar i{{background:#8FC4B5}}
@media (prefers-reduced-motion: reduce){{#appBoot .bar i{{animation:none;width:100%}}}}</style>
</head>
<body>
<div id="appBoot" role="status"><div><div class="k">이야기 통독 노트</div><div class="t">오늘 통독</div><div class="s">이야기를 따라 읽습니다</div><div class="bar"><i></i></div></div></div>
'''
html=head+body+'\n</body>\n</html>\n'
# 2026-10-29 v2가 첫 화면(index.html)이 됨. v1은 v1.html로 남겨 둠(이전 화면)
open(f'{OUT}/v1.html','w').write(html.replace('<link rel="manifest" href="manifest.webmanifest">','').replace('content="https://aqedah.github.io/CBSR/"','content="https://aqedah.github.io/CBSR/v1.html"'))
# 시험 페이지(요 1-4장 하루): 연동 없음, 기록은 'try:' 앞머리를 붙여 앱 기록과 분리
SHIM='<script>window.CBSR_TRY=1;(function(){try{var L=window.localStorage,P="try:",S={getItem:function(k){return L.getItem(P+k)},setItem:function(k,v){L.setItem(P+k,String(v))},removeItem:function(k){L.removeItem(P+k)},clear:function(){}};Object.defineProperty(window,"localStorage",{value:S,configurable:true});}catch(e){}})();</script>\n'
btag=f'<script src="bible.js?v={h(bible[:5000]+str(len(bible)))}"></script>\n'
tbody=t.replace('<script>\n/*DATA*/','\n'+btag+'<script>\n'+data)
tbody=tbody.replace(title,'',1)
thead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+SHIM).replace('<link rel="manifest" href="manifest.webmanifest">','').replace('content="https://aqedah.github.io/CBSR/"','content="https://aqedah.github.io/CBSR/try.html"')
open(f'{OUT}/try.html','w').write(thead+tbody+'\n</body>\n</html>\n')
# QT 스토리 카드 시험 페이지: 기록은 'story:' 앞머리로 앱 기록과 분리, 365 통독표로 시작
SSHIM='<script>window.CBSR_STORY=1;(function(){try{var L=window.localStorage,P="story:",S={getItem:function(k){return L.getItem(P+k)},setItem:function(k,v){L.setItem(P+k,String(v))},removeItem:function(k){L.removeItem(P+k)},clear:function(){}};Object.defineProperty(window,"localStorage",{value:S,configurable:true});if(S.getItem("cbsr-mode")==null)S.setItem("cbsr-mode","y365");}catch(e){}})();</script>\n'
shead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+SSHIM).replace('<link rel="manifest" href="manifest.webmanifest">','').replace('content="https://aqedah.github.io/CBSR/"','content="https://aqedah.github.io/CBSR/story.html"')
open(f'{OUT}/story.html','w').write(shead+body+'\n</body>\n</html>\n')
# 전체 개편 시험(v2.html): 오늘·본문·도전·기록, 이야기 QT, 말씀 카드, 내일 본문 시계. 기록은 v2: 앞머리로 따로
VSHIM=SSHIM.replace('window.CBSR_STORY=1;','window.CBSR_STORY=1;window.CBSR_V2=1;').replace('Object.defineProperty(window,"localStorage"','/* v1 기록 가져오기: v2를 처음 열 때 한 번, v1(앞머리 없는 기록)을 v2: 쪽에 복사(이미 있는 v2 기록은 그대로) */if(!L.getItem("v2:cbsr-v1import")){var K=[];for(var i=0;i<L.length;i++){var k=L.key(i);if(k&&/^(cbsr-|rjnote:)/.test(k))K.push(k);}K.forEach(function(k){if(L.getItem("v2:"+k)==null)L.setItem("v2:"+k,L.getItem(k));});L.setItem("v2:cbsr-v1import",new Date().toISOString()+" "+K.length);}try{for(var j=0;j<L.length;j++){var kk=L.key(j);if(kk&&/^(cbsr-|rjnote:)/.test(kk)&&kk!=="cbsr-login-v1"){window.CBSR_HADV1=1;break;}}}catch(e){}window.__rawLS=L;Object.defineProperty(window,"localStorage"',1).replace('P="story:"','P="v2:"').replace('if(S.getItem("cbsr-mode")==null)','if(/[?&]p=rj/.test(location.search))S.setItem("cbsr-mode","rj");else if(/[?&]day=/.test(location.search))S.setItem("cbsr-mode","y365");else if(S.getItem("cbsr-mode")==null)S.setItem("cbsr-mode","rj");if(0)')
exec(open('review_build.py').read())
import base64 as _b64,gzip as _gz
_BB=json.loads(_gz.decompress(_b64.b64decode(open('bible.b64').read())).decode()); _NM={}; _NR=_re.compile(r'^([가-힣]{2,})(을|를|의|에게|과|와|께서|에서|으로)$')
for _bk in _BB:
  for _ch in _bk:
    for _v in _ch:
      if not _v: continue
      for _tk in _re.sub(r'[^가-힣\s]',' ',_v).split():
        _m=_NR.match(_tk)
        if _m: _NM.setdefault(_m.group(1),set()).add(_m.group(2))
NOUNSHIM='<script>window.NOUNS_KRV='+json.dumps(sorted(k for k,v in _NM.items() if len(v)>=2),ensure_ascii=False,separators=(',',':'))+';</script>'
v2html=shead.replace(SSHIM,VSHIM+NOUNSHIM).replace('story.html','v2.html')+body+'\n</body>\n</html>\n'
open(f'{OUT}/v2.html','w').write(v2html)
ihead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+VSHIM+NOUNSHIM)
open(f'{OUT}/index.html','w').write(ihead+body+'\n</body>\n</html>\n')
V=h(html+v2html+bible)
sw=f'''/* 오프라인 지원: 앱 화면은 인터넷이 되면 늘 새로 받고(network first),
   성경 본문·지형도·아이콘·글꼴·라이브러리는 처음 받은 뒤 보관해 둡니다(cache first). 기록은 Firestore가 따로 보관합니다. */
const V="cbsr-{V}";
const SHELL=["./","index.html","v2.html","v1.html","config.js","sync.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^cbsr-/.test(k)&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener("fetch",e=>{{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(/firestore\\.googleapis\\.com|identitytoolkit|securetoken|firebaseinstallations/.test(u.hostname))return;
  const shell=u.origin===location.origin&&!/bible\\.js|\\/terrain\\/|\\/icons\\/|\\/img\\//.test(u.pathname);
  if(shell){{e.respondWith(fetch(r).then(res=>{{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res;}}).catch(()=>caches.match(r,{{ignoreSearch:true}}).then(m=>m||caches.match(/v1\\.html$/.test(u.pathname)?"v1.html":/v2\\.html$/.test(u.pathname)?"v2.html":"index.html"))));return;}}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));}}return res;}})));}});
'''
open(f'{OUT}/sw.js','w').write(sw)
for f in []:
  if os.path.exists('study/'+f): shutil.copy('study/'+f,f'{OUT}/study/'+f)
open(f'{OUT}/.nojekyll','w').write('')
shutil.copy('site_src/README.md',OUT+'/README.md')
for f in ['CLAUDE.md']: shutil.copy('site_src/'+f,OUT+'/'+f); shutil.copy('site_src/'+f,OUT+'/AGENTS.md')
print({f:os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if os.path.isfile(os.path.join(OUT,f))})
