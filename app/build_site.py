import subprocess,sys
import json,base64,hashlib,os,shutil,re
OUT='site'; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/terrain')
t=open('template3.html').read()
plan=json.load(open('plan.json'))
# 성경연구는 MILALWV로 옮김(2026-10-23): 자리만 남김
t=t.replace('/*STUDY*/','const STUDY_ON=()=>false;\nfunction studyTabSync(){ document.documentElement.classList.remove("study-on"); try{ localStorage.removeItem("cbsr-study"); }catch(e){} if(view.tab==="study") view.tab="read"; }\n')
t=t.replace('/*LEAFLETCSS*/',open('npm/node_modules/leaflet/dist/leaflet.css').read())
data="\n".join(open(f).read() for f in ['engine.js','glossary.js','qt_base.js','qt_extra.js','routes.js','clues.js'])
data+='\nconst SUMMARY=[], CURATED={}, INCL={}, WEEKS=[];'  # 리딩지저스 요약·문제·봉투 구조는 지움(2026-11-11): 365 자료로 채움
data=data.replace('if(typeof module!=="undefined") module.exports={buildEntityIndex,buildGlossIndex,inScope,analyzeDay,makeQuiz,rng};','')
data+="\nconst PLACEINFO="+open('places/all.json').read()+";"
data+="\nconst ROUTES_B="+open('routes/all.json').read()+";"
data+="\nconst BM_TOURS="+open('ux/big_tours.json').read()+";"
# 공용 평면도 여정 엔진과 각 편 자료(2026-11-10): 앱 본문(IIFE) 안의 /*PLANS*/ 자리에 넣음(esc·mvNar·C 등을 써야 하므로)
import glob as _g
import subprocess as _sp
if _sp.call(['python3','ux/plans_check.py'])!=0: raise SystemExit('평면도 여정 인용이 개역개정 원문과 다릅니다(ux/plans_check.py)')
t=t.replace('/*PLANS*/',open('ux/journey_ui.js').read()+"\n"+open('ux/plans.js').read()+"\n"+"\n".join(open(f).read() for f in sorted(_g.glob('ux/plans/*.js'))))
data+="\nconst RIVERS="+open('ux/rivers.json').read()+";"
data+="\nconst PHOTO_PIN="+json.dumps(json.load(open('ux/photo_pin.json'))['pins'],ensure_ascii=False,separators=(',',':'))+";"
data+="\nconst PHOTO_USE="+json.dumps(json.load(open('ux/photo_use_proposed.json'))['uses'],ensure_ascii=False,separators=(',',':'))+";"
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
# 그림 밝기(0–255): 그림 없는 스토리 카드의 바탕을 그날 그림들의 분위기에 맞춤(2026-11-02)
try:
  from PIL import Image as _I, ImageStat as _S
  _lum=json.load(open('ux/phlum.json')) if os.path.exists('ux/phlum.json') else {}
  _ch=False
  for _f in os.listdir('site_src/img/g'):
    _n,_e=os.path.splitext(_f)
    if _e.lower() in ('.jpg','.jpeg','.png','.webp') and _n not in _lum:
      _im=_I.open('site_src/img/g/'+_f).convert('L'); _im.thumbnail((64,64)); _lum[_n]=round(_S.Stat(_im).mean[0]); _ch=True
  if _ch: json.dump(_lum,open('ux/phlum.json','w'),separators=(',',':'))
except Exception as _x:
  _lum=json.load(open('ux/phlum.json')) if os.path.exists('ux/phlum.json') else {}
data+="\nconst MEM100="+(json.dumps({"list":[{"r":x["r"],"t":x["t"]} for x in json.load(open('site_src/mem100.json'))["list"]]},ensure_ascii=False,separators=(',',':')) if os.path.exists('site_src/mem100.json') else "null")+";"  # 꼭 외울 말씀 100(도전 탭 놀이)
data+="\nconst CHROLE="+(open('ux/christ_role.json').read() if os.path.exists('ux/christ_role.json') else "{}")+";"
data+="\nconst PHLUM="+json.dumps(_lum,separators=(',',':'))+";"
data+="\nconst NAME_SET=new Set(NAME_MEAN.map(x=>x[0])); for(const n of NAME_MEAN){ if(!GLOSSARY.some(g=>g[0]===n[0])) GLOSSARY.push(n); }"
data+="\nconst LEITWORT="+open('leitwort365.json').read()+";\nconst EMPH="+open('emph365.json').read()+";\nconst GAZ="+open('gaz.json').read()+";\nconst PLAN="+json.dumps({**plan,"plan":[]},ensure_ascii=False,separators=(',',':'))+";\n"
tj=json.load(open('terrain.json')); terr={}
for k,v in tj.items():
    shutil.copy(f'terrain_{k}.jpg',f'{OUT}/terrain/{k}.jpg'); terr[k]={"bounds":v["bounds"],"url":f"terrain/{k}.jpg"}
    if k in ('levant','sinai','israel','israelhi'):
        # 가장자리 흐림을 그림 자체(알파)에 구움: CSS mask는 휴대폰에서 다시 그릴 때마다 한 프레임씩 번쩍임(목사님 녹화 2026-10-30)
        import os
        src=f'terrain_{k}.jpg'; dst=f'{OUT}/terrain/{k}.webp'; cache=f'terrain_{k}_a.webp'
        if not os.path.exists(cache) or os.path.getmtime(cache)<os.path.getmtime(src):
            from PIL import Image
            im=Image.open(src).convert('RGBA'); w,h=im.size; fx,fy=int(w*.07),int(h*.07)
            import numpy as np
            ax=np.ones(w); ax[:fx]=np.linspace(0,1,fx); ax[-fx:]=np.linspace(1,0,fx)
            ay=np.ones(h); ay[:fy]=np.linspace(0,1,fy); ay[-fy:]=np.linspace(1,0,fy)
            A=(np.minimum.outer(ay,ax)*0.92*255).astype('uint8'); im.putalpha(Image.fromarray(A)); im.save(cache,'WEBP',quality=82)
        shutil.copy(cache,dst); terr[k]["url"]=f"terrain/{k}.webp"
data+="const TERRAIN="+json.dumps(terr)+";\n"
# 지형 조각 타일(terrain_tiles.py)은 2026-10-31에 Esri 음영 지도로 바꾸며 그만 씀
# 자세한 지형 조각(terrain_hi.py, 2026-11-02): 요단·갈릴리·사해 권역 8–13배율
if os.path.isdir('terrhi'): shutil.copytree('terrhi',f'{OUT}/terrhi')
for _d in ['terrw','terrm']:
    if os.path.isdir(_d): shutil.copytree(_d,f'{OUT}/{_d}')
data+="\nconst TERRIDX="+(open('terrindex.json').read() if os.path.exists('terrindex.json') else 'null')+";"
data+="\nconst TERRWIDE="+(open('terrwide.json').read() if os.path.exists('terrwide.json') else 'null')+";"
data+="\nconst TERRHI="+(open('terrhi.json').read() if os.path.exists('terrhi.json') else 'null')+";"
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
data+='const PLAN_INFO={y365:{name:"365 성경통독",short:"365일",src:"2026 365일 성경통독표",start:"2026-01-01"}};\n'
import importlib.util as _iu3; _sp3=_iu3.spec_from_file_location('p27','ux/plan365v4_build.py'); _p27=_iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_p27)
data+='const P27='+J(_p27.build())+';\n'  # 2027 365일표 4판(목사님 확정 11-08; 313회는 일정표로만 — 11-10 앱 반영)
A365=json.load(open('s365b/all.json')); GD={};EY={};CQ={}
for i,d in enumerate(P365):
    w,j=i//7+1,i%7; v=A365.get(str(d['n']))
    if not v: continue
    GD[f"{w}-{j}"]=v['g']; EY[f"{w}-{j}"]=v['e']
    CQ[f"{w}-{j+1}"]=[{k:q[k] for k in ('t','kind','q','o','a','h','ref')} for q in v['qz']]
# 요 3–4장 QT 질문(s365b 308일)과 읽기 도구(tools/toolx.json y365:44-6)는 365 자료로 옮겨 둠(리딩지저스 삭제 2026-11-10·11)
TRV=hashlib.sha1((open('bible_snb.b64').read()[:3000]+open('bible_shg.b64').read()[:3000]).encode()).hexdigest()[:8] if os.path.exists('bible_snb.b64') else '1'
data+='window.TR_VER="'+TRV+'";\n'
data+='const BOOKINFO='+open('books/all.json').read()+';\n'
data+='const GUIDE={}, EYE={};\n'
data+='window.STUDY_V="0";\n'  # 원문 연구는 MILALWV로 옮김(2026-10-23)
data+='/* 리딩지저스 삭제(목사님 2026-11-10): 365 통독만 */ window.CBSR_MODE="y365"; try{ localStorage.setItem("cbsr-mode","y365"); }catch(e){}\nconst DAYC={};\n'
data+='{const R=(o,n)=>{for(const k in o)delete o[k];Object.assign(o,n);};\n'
data+=f'PLAN.plan={J(W365)};SUMMARY.length=0;SUMMARY.push(...{J(SW)});WEEKS.length=0;WEEKS.push(...{J(WK)});\n'
data+=f'R(INCL,{open("incl365.json").read()});PLAN.plan.forEach(w=>w.forEach(d=>{{ d.label=d.label.replace(/시편 ([0-9–\\-]+)장/g,"시편 $1편"); }}));R(DETAIL,{{}});R(CURATED,{J(CQ)});Object.assign(GUIDE,{J(GD)});Object.assign(EYE,{J(EY)});ARC_LIST.length=0;Object.assign(DAYC,{J(DC)});}}\n'
import glob as _g
CK=json.load(open('ux/christ_out.json')); MN=json.load(open('ux/mean_out.json')); GF={}
for f in sorted(_g.glob('ux/guide_out*.json')): GF.update(json.load(open(f)))
data+='const FLOW='+open('flow/all.json').read()+';\n'
data+='const WHERE365='+J(json.load(open('ux/where365.json'))['list'])+';\n'  # 읽기 도우미 '지금 어디쯤?'(11-11)
import importlib.util as _iu2
import base64 as _b64, gzip as _gz
_BB=json.loads(_gz.decompress(_b64.b64decode(open('bible.b64').read())))
_sp4=_iu2.spec_from_file_location('tsay','ux/tour_say.py'); _ts=_iu2.module_from_spec(_sp4); _sp4.loader.exec_module(_ts)
data+='const SAYX='+json.dumps(_ts.build(lambda b,c,v: (_BB[b-1][c-1][v-1] if b<=len(_BB) and c<=len(_BB[b-1]) and v<=len(_BB[b-1][c-1]) else '')),ensure_ascii=False,separators=(',',':'))+';\n'  # 큰 여정 말한 사람(2026-11-04)
data+='const TRAITS_C='+open('traits/all.json').read()+';\n'
data+='const PARA='+open('para/all.json').read()+';\n'
data+='const SCX='+open('scene/scx.json').read()+';\n'
data+='const TOOLX='+(open('tools/toolx.json').read() if os.path.exists('tools/toolx.json') else '{}')+';\n'
# 가이드북이 쓴 서술자의 장치(2층 9가지)를 앱의 '오늘의 읽기 도구'에도(2026-11-11 목사님)
import re as _re9
_GQ=json.load(open('site_src/guide_qt.json')).get('qt',{})
_GREX=r'(?:●|◆|◇|⇔|↗|□|∽|▲|○|◎|⋯|\?!|“”|♪|∥|if|¿|≒|☞|×|∞|※|☆) ?(이끎말|반복|점층|대조|틀|전형장면|전환|속말|속마음|침묵|공백|생략|아이러니|말씀 공식|후렴|평행|가정|수사적 질문|비유|호명|교차|언약 공식|상징|송영)'
_GT={}
for _n,_v in _GQ.items():
    _f=((_v or {}).get('guide') or {}).get('find','')
    _L=[]
    for _m in _re9.findall(_GREX,_f):
        if _m not in _L: _L.append(_m)
    if _L and _n.isdigit(): _GT[int(_n)]=_L
data+='const GTOOLS='+J(_GT)+';\n'
# 11-12: 묵상 탭도 가이드북과 같은 질문(원고 한 벌) — 관찰·적용 질문만
_GQT={int(n):{'q':((v or {}).get('obs') or {}).get('q',''),'apply':(v or {}).get('apply','')} for n,v in _GQ.items() if n.isdigit()}
data+='const GQT='+J(_GQT)+';\n'
# 11-12 목사님: 2026 체험판 가이드북(317–365일)도 앱에 — 2026년 화면에서만 씀
try:
    _TQ=json.load(open('site_src/trial26_qt.json')).get('qt',{})
except Exception: _TQ={}
_GT26={}
for _n,_v in _TQ.items():
    if not _n.isdigit(): continue
    _f=((_v or {}).get('guide') or {}).get('find','')
    _L=[]
    for _m in _re9.findall(_GREX,_f):
        if _m not in _L: _L.append(_m)
    if _L: _GT26[int(_n)]=_L
data+='const GTOOLS26='+J(_GT26)+';\n'
# 11-13 목사님: 가이드북에 쓴 그날의 도구 설명(읽으며 둘 초점 문장 + 눈여겨볼 것의 도구별 설명)을 앱 '오늘의 읽기 도구'에도
def _gdesc(Q):
    out={}
    for n,v in Q.items():
        if not n.isdigit() or not v: continue
        f=((v.get('guide') or {}).get('find') or '')
        f=_re9.sub(r'^(?:\s*'+_GREX+r')+\s*','',f).strip()
        pm={}
        for pr in ((v.get('obs') or {}).get('pair') or []):
            if isinstance(pr,list) and len(pr)>=2:
                m=_re9.match(r'\s*'+_GREX,pr[0] or '')
                if m and m.group(1) not in pm: pm[m.group(1)]=pr[1]
        t=((v.get('guide') or {}).get('today') or '').strip()
        wd=((v.get('guide') or {}).get('word') or '').strip()
        ch=((v.get('obs') or {}).get('christ') or '').strip(); mp=((v.get('map') or {}).get('cap') or '').strip()  # 11-13: ③ 읽은 뒤(성경 전체로·지도)도 앱에
        if f or pm or t or wd: out[int(n)]={'f':f,'p':pm,'t':t,'w':wd,'c':ch,'m':mp}  # t: 오늘의 흐름(11-13 앱 오늘 탭도 이것으로 통일)
    return out
# 11-13 목사님: 도구 이름·기호·풀이·예는 가이드북 책머리(f0.syms·dsyms) 한 벌을 앱도 그대로 씀
_GBS={}
for _fk in ('syms','dsyms'):
    for _ln in str(((_GQ.get('f0') or {}).get(_fk)) or '').split('\n'):
        _pp=_ln.split('|')
        _mm=_re9.match(r'^(\S{1,3}) (.+)$',_pp[0].strip()) if len(_pp)>=2 else None
        if _mm: _GBS[_mm.group(2).strip()]=[_mm.group(1),_pp[1].strip(),(_pp[2].strip() if len(_pp)>2 else '')]
data+='const GBSYMS='+J(_GBS)+';\n'
data+='const GBDESC='+J(_gdesc(_GQ))+';\n'
data+='const GBDESC26='+J(_gdesc(_TQ))+';\n'
data+='const GQT26='+J({int(n):{'q':((v or {}).get('obs') or {}).get('q',''),'apply':(v or {}).get('apply','')} for n,v in _TQ.items() if n.isdigit()})+';\n'
# 11-12: 원고 성구 약칭이 빠진 곳이 있으면 알림(다른 저장으로 덮였을 때)
try:
    import subprocess as _sp
    _o=_sp.run(['python3','tools/guide_refs_fix.py'],capture_output=True,text=True,timeout=60).stdout.strip().splitlines()
    if _o and _o[-1].strip()!='0': print('경고: 가이드북 성구 약칭 '+_o[-1].strip()+'곳이 빠짐 → python3 tools/guide_refs_fix.py --write')
except Exception as _e: pass
data+='const CHRIST_K='+J({k:v['k'] for k,v in CK.items()})+';\n'

data+='(()=>{ const FX='+J({k:v['fix'] for k,v in CK.items() if v.get('fix')})+', MN='+J(MN)+', GF='+J(GF)+';\n'
data+=""" for(const k in FX){ const [t,r]=k.split(":"); if(t==="y") DAYC[r]=FX[k]; }
 for(const k in MN){ const n=k.slice(3), o=k.startsWith("pe:")?PEOPLEINFO[n]:PLACEINFO[n]; if(o){ o.m=MN[k].m; o.mc=MN[k].c; } }
 for(const k in GF){ const [m,r]=k.split(":"); if(m!=="y365") continue; if(GF[k].find&&GUIDE[r]) GUIDE[r].find=GF[k].find; if(GF[k].eye&&EYE[r]) EYE[r].q=GF[k].eye; }
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
if _perr:
    print('그림 정책 오류 — 빌드를 멈춥니다:'); [print('  -',x) for x in _perr[:30]]; raise SystemExit(2)
for _p in _PH: _p.update(_pp.app_fields(_pp.effective(_PMR.get(_p['id'],_p),_POL)))
_PH=[_p for _p in _PH if _p['rs'] not in ('hold','out')]
_FXA=json.load(open('ux/photo_fx.json')) if os.path.exists('ux/photo_fx.json') else {}
for _p in _PH:
    if _p['id'] in _FXA: _p['fx']=_FXA[_p['id']]  # 11/4: 세로 화면에서 인물 얼굴이 잘리지 않게(ux/photo_fx_auto.py)  # 보류·제외는 자동·지정·고정 어느 길로도 앱에 나오지 않음
data+='const PHOTOS='+J([{k:v for k,v in p.items() if k in ('id','u','pl','tags','fx','mood','set','sets','scope','refs','kw','deny','role','tm','ak','ap','rs','va','bu','au','rl','er','rq','ac','gp')} for p in _PH])+';\nconst STORYC='+J({k:v for k,v in _SC.items() if not k.startswith('_')})+';\n'
data+='const DSTATUS='+(open('edits/status.json',encoding='utf-8').read() if os.path.exists('edits/status.json') else '{}')+';\n'  # 날짜별 승인 상태(관리자 상태판)
Y365NT=json.load(open('ux/christ_y365nt.json'))
DY=json.load(open('ux/detail_y365.json'))
data+='{const DY='+J({k:{f:v for f,v in o.items() if not f.startswith('_')} for k,o in DY.items()})+';for(const k in DY) DETAIL[k]=Object.assign({},DETAIL[k]||{},DY[k]);}\n'
YN={f"{(int(n)-1)//7+1}-{(int(n)-1)%7}":v for n,v in Y365NT.items()}
data+='{const YN='+J(YN)+';for(const k in YN){ DAYC[k]=YN[k].t; CHRIST_K["y:"+k]=YN[k].k; }}\n'
data+="\nconst TRMAP_SNB="+open('trmap/snb.json').read()+";\nconst TRMAP_SHG="+open('trmap/shg.json').read()+";\n"+open('trconv.js').read()
print("365 summaries:",len(S365))

bible='const BIBLE_B64="'+open('bible.b64').read()+'";\n'
bible+='window.SPEECH_krv='+open('speech/bible.json').read()+';\n'
open(f'{OUT}/bible.js','w').write(bible)
for tk in ('snb','shg'):
    open(f'{OUT}/bible_{tk}.js','w').write('window.BIBLE_TR=window.BIBLE_TR||{};BIBLE_TR.'+tk+'="'+open(f'bible_{tk}.b64').read()+'";\nwindow.SPEECH_'+tk+'='+open(f'speech/bible_{tk}.json').read()+';\n')

h=lambda s:hashlib.sha1(s.encode()).hexdigest()[:8]
for f in ['sync.js','config.js','manifest.webmanifest','firestore.rules','og.png','sample_story.html','phreview.html','ui1.html','ui2.html','ui3.html','guide.html','guide_qt.json','trial26.html','trial26_qt.json']: shutil.copy('site_src/'+f,OUT+'/'+f)  # guide.html·guide_qt.json: 통독 가이드북 작업실(2026-11-09)
# 스토리 작업실(2026-11-11): 원고를 붙여 카드로 나누고 앱(v2) 미리보기로 보고 GitHub(ux/story_in)에 저장 → 다음 빌드가 story_cards.json에 합침
_PE=[{'id':p['id'],'memo':p.get('memo',''),'refs':p.get('refs',[]),'role':p.get('role','')} for p in (json.load(open('ux/photos.json')) if os.path.exists('ux/photos.json') else [])]
_P26=[{'n':x['n'],'label':x['label'],'ch':x['ch'],'topic':x.get('topic','')} for x in P365]
open(OUT+'/story_edit.html','w').write(open('site_src/story_edit.html').read().replace('/*PLANS*/','const PLAN26='+J(_P26)+';\nconst P27='+J(_p27.build())+';\nconst ABBR_L='+J(AB)+';\nconst PHOTOS_E='+J(_PE)+';'))
if os.path.isdir('ux/story_prev'): shutil.copytree('ux/story_prev',OUT+'/story_prev',dirs_exist_ok=True)  # 작업실 되돌리기용 이전 원고
open(OUT+'/story_cards.json','w').write(J({k:v for k,v in (json.load(open('ux/story_cards.json')) if os.path.exists('ux/story_cards.json') else {}).items() if not k.startswith('_')}))  # 작업실 '공개 원고 불러오기'
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
VSHIM=SSHIM.replace('window.CBSR_STORY=1;','window.CBSR_STORY=1;window.CBSR_V2=1;').replace('Object.defineProperty(window,"localStorage"','/* v1 기록 가져오기: v2를 처음 열 때 한 번, v1(앞머리 없는 기록)을 v2: 쪽에 복사(이미 있는 v2 기록은 그대로) */if(!L.getItem("v2:cbsr-v1import")){var K=[];for(var i=0;i<L.length;i++){var k=L.key(i);if(k&&/^(cbsr-|rjnote:)/.test(k))K.push(k);}K.forEach(function(k){if(L.getItem("v2:"+k)==null)L.setItem("v2:"+k,L.getItem(k));});L.setItem("v2:cbsr-v1import",new Date().toISOString()+" "+K.length);}try{for(var j=0;j<L.length;j++){var kk=L.key(j);if(kk&&/^(cbsr-|rjnote:)/.test(kk)&&kk!=="cbsr-login-v1"){window.CBSR_HADV1=1;break;}}}catch(e){}window.__rawLS=L;Object.defineProperty(window,"localStorage"',1).replace('P="story:"','P="v2:"').replace('if(S.getItem("cbsr-mode")==null)','if(/[?&]p=rj/.test(location.search))S.setItem("cbsr-mode","rj");else if(/[?&]day=/.test(location.search))S.setItem("cbsr-mode","y365");else if(S.getItem("cbsr-mode")==null)S.setItem("cbsr-mode","y365");if(0)')
exec(open('review_build.py').read())
open(OUT+'/demo.html','w').write(open('site_src/demo.html').read().replace('<!--FB-->',_GFB))  # 스토리 QT 체험판(2026-10-30)
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
body_v2=body.replace('스토리 QT','스토리') # v2: 이름은 '스토리'만(2026-11-02)
v2html=shead.replace(SSHIM,VSHIM+NOUNSHIM).replace('story.html','v2.html')+body_v2+'\n</body>\n</html>\n'
open(f'{OUT}/v2.html','w').write(v2html)
ihead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+VSHIM+NOUNSHIM)
open(f'{OUT}/index.html','w').write(ihead+body_v2+'\n</body>\n</html>\n')
V=h(html+v2html+bible)
sw=f'''/* 오프라인 지원: 앱 화면은 인터넷이 되면 늘 새로 받고(network first),
   성경 본문·지형도·아이콘·글꼴·라이브러리는 처음 받은 뒤 보관해 둡니다(cache first). 기록은 Firestore가 따로 보관합니다. */
const V="cbsr-{V}";
const SHELL=["./","index.html","v2.html","v1.html","config.js","sync.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^cbsr-/.test(k)&&k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
self.addEventListener("fetch",e=>{{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(/firestore\\.googleapis\\.com|identitytoolkit|securetoken|firebaseinstallations/.test(u.hostname))return;
  const shell=u.origin===location.origin&&!/bible\\.js|\\/terrain\\/|\\/terr[hwm]i?\\/|\\/icons\\/|\\/img\\//.test(u.pathname);
  if(shell){{e.respondWith(fetch(r).then(res=>{{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res;}}).catch(()=>caches.match(r,{{ignoreSearch:true}}).then(m=>m||caches.match(/v1\\.html$/.test(u.pathname)?"v1.html":/v2\\.html$/.test(u.pathname)?"v2.html":"index.html"))));return;}}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));}}return res;}})));}});
'''
open(f'{OUT}/sw.js','w').write(sw)
# 성경 골든벨 문제(도전 탭에서 처음 열 때만 받음, 2026-11-03)
import importlib.util as _iu; _sp=_iu.spec_from_file_location('gbb','ux/gb_build.py'); _gbb=_iu.module_from_spec(_sp); _sp.loader.exec_module(_gbb); _gbb.build(f'{OUT}/gb.json')
for f in []:
  if os.path.exists('study/'+f): shutil.copy('study/'+f,f'{OUT}/study/'+f)
open(f'{OUT}/.nojekyll','w').write('')
shutil.copy('site_src/README.md',OUT+'/README.md')
for f in ['CLAUDE.md']: shutil.copy('site_src/'+f,OUT+'/'+f); shutil.copy('site_src/'+f,OUT+'/AGENTS.md')
print({f:os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if os.path.isfile(os.path.join(OUT,f))})
