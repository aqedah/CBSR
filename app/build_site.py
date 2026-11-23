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
data+='const P27='+J(_p27.build())+';\n'  # 2027 365일표 5판(11-24 목사님 확정, 4판 11-08). 313회는 일정표로만
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
    if isinstance(_v,dict) and _v.get('v27'): _f=' '.join(m.get('tool','') for m in _v['v27'].get('marks',[])).replace('[ ] 틀','□ 틀')  # 11-20 새 틀: ② 표시의 도구
    _L=[]
    for _m in _re9.findall(_GREX,_f):
        if _m not in _L: _L.append(_m)
    if _L and _n.isdigit(): _GT[int(_n)]=_L
data+='const GTOOLS='+J(_GT)+';\n'
# 11-12: 묵상 탭도 가이드북과 같은 질문(원고 한 벌) — 관찰·적용 질문만
_GQT={int(n):{'q':((v or {}).get('obs') or {}).get('q',''),'apply':(v or {}).get('apply',''),'note':(v or {}).get('note',''),'pray':(v or {}).get('pray','')} for n,v in _GQ.items() if n.isdigit()}  # 11-23 GPT 출시 검토 P0: 쓴 뒤에 읽기(해설·기도)도 가이드북 원고
for _n,_v in _GQ.items():  # 11-20 새 틀: 성품 물음도 가이드북과 같게
    if _n.isdigit() and isinstance(_v,dict) and _v.get('v27') and (_v['v27'].get('god') or ['',''])[1]: _GQT[int(_n)]['god']=' '.join(_v['v27']['god'])
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
        em=str((v.get('map') or {}).get('emph') or '').strip()  # 11-15: 앱 스토리 '오늘 본문의 무대'도 가이드북 지도 강조 지명으로
        k=None
        if v.get('v27'):  # 11-20 새 틀: ① 읽기 전에 가이드북 ② 표시를 그대로(표시 낱말은 글자로)
            def _pl(x): return _re9.sub(r'\{번호 ([^}]*)\}',lambda m:'번호 '+m.group(1),_re9.sub(r'\{(동그라미|형광펜|물결 밑줄|빗금 형광펜|네모|괄호)\}',r'\1',x)).replace('**','')
            k=[[m.get('tool',''),1 if m.get('rep') else 0,_pl(m.get('text',''))] for m in v['v27'].get('marks',[])]; f=''
            if ' — ' in wd: wd=wd.split(' — ',1)[0]+': '+wd.split(' — ',1)[1]
        if f or pm or t or wd or k: out[int(n)]=dict({'f':f,'p':pm,'t':t,'w':wd,'c':ch,'m':mp,'e':em},**({'k':k} if k else {}))  # t: 오늘의 흐름(11-13 앱 오늘 탭도 이것으로 통일)
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
_GQT26={int(n):{'q':((v or {}).get('obs') or {}).get('q',''),'apply':(v or {}).get('apply',''),'note':(v or {}).get('note',''),'pray':(v or {}).get('pray','')} for n,v in _TQ.items() if n.isdigit()}
for _n,_v in _TQ.items():  # 11-20 체험판도 새 틀로 바꾸는 날부터 성품 물음을 가이드북과 같게
    if _n.isdigit() and isinstance(_v,dict) and _v.get('v27') and (_v['v27'].get('god') or ['',''])[1]: _GQT26[int(_n)]['god']=' '.join(_v['v27']['god'])
data+='const GQT26='+J(_GQT26)+';\n'
# 11-22 목사님: 주일 공과(파이디온 공과 순서, 본문 범위는 목사님) — 365 통독과 따로 보는 주일 본문. 원고는 site_src/sunday_qt.json
data+='const SUNQ='+J(json.load(open('site_src/sunday_qt.json')))+';\n'

# 11-20 소그룹 인도자(목사님 시안 승인): 날마다 인도자 화면이 쓰는 가이드북 칸 + 주일 인도자 전용 칸(qt.ldr)
def _ldrd(Q):
    import re as _r
    def pl(x): return _r.sub(r'\{번호 ([^}]*)\}',lambda m:m.group(1),_r.sub(r'\{(동그라미|형광펜|물결 밑줄|빗금 형광펜|네모|괄호)\}',r'\1',str(x or ''))).replace('**','')
    out={}
    for n,v in Q.items():
        if not n.isdigit() or not isinstance(v,dict): continue
        g=v.get('guide') or {}; o=v.get('obs') or {}; v27=v.get('v27') or {}
        if not (o.get('q') or v.get('apply') or isinstance(v.get('ldr'),dict)): continue  # 11-21 인도자 원고만 있는 날도 싣기
        rep=''
        if v27.get('marks'):
            m=[x for x in v27['marks'] if x.get('rep')] or v27['marks']; rep=pl(m[0].get('text',''))
        else:
            f=str(g.get('find','')); rep=_r.sub(r'^(?:\s*(?:\S{1,3}|\[ \])\s+(?:이끎말|반복|점층|대조|틀|전형장면|전환|속마음|침묵|생략|아이러니|주도어|속말|말씀 공식|후렴|평행|가정|수사적 질문|비유|호명|교차|언약 공식|상징|송영))+\s*','',f).strip()
        ctr=v.get('god','') or ''
        if not ctr:
            ss=[t for t in _r.split(r'(?<=[.])\s+',str(v.get('note',''))) if t.startswith('하나님은')]; ctr=ss[-1] if ss else ''
        d={'f':g.get('today',''),'r':rep,'q':o.get('q',''),'a':v.get('apply',''),'p':v.get('pray',''),'c':ctr}
        if (v27.get('god') or ['',''])[1]: d['g']=v27['god']
        if v27.get('scenes'): d['s']=v27['scenes']  # 11-20 인도자 화면 '읽을 차례'의 단락 이름
        if isinstance(v.get('ldr'),dict): d['l']=v['ldr']
        if v.get('sub'): d['t']=v['sub']
        if isinstance(v.get('hymn'),dict) and v['hymn'].get('no'): d['h']=v['hymn']  # 11-21 인도자 화면 찬송 = 가이드북 그날 찬송  # 11-21 인도자 '이번 주 읽은 곳'은 가이드북 소제목 먼저
        out[int(n)]=d
    return out
data+='const LDRD27='+J(_ldrd(_GQ))+';\nconst LDRD26='+J(_ldrd(_TQ))+';\n'
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
for f in ['sync.js','config.js','manifest.webmanifest','firestore.rules','og.png','guide.html','guide_qt.json','trial26.html','trial26_qt.json','earth.html','earth.js','borders.json','check.html','shelf_edit.html','shelf.js']: shutil.copy('site_src/'+f,OUT+'/'+f)  # guide.html·guide_qt.json: 통독 가이드북 작업실(2026-11-09)
# 성경책장(서고) 원고(2026-11-24): 작업대에서 올린 books/shelf_66.json이 있으면 그것을, 없으면 site_src의 원고를 앱에 실음. 대표 구절 본문은 여기서 개역개정을 붙임
try:
    _sp='books/shelf_66.json' if os.path.exists('books/shelf_66.json') else 'site_src/shelf_66.json'
    _sd=json.load(open(_sp,encoding='utf-8'))
    for _b in _sd.get('books',[]):
        for _k in ('ask','status'): _b.pop(_k,None)
        _m=re.match(r'^(\S+) (\d+):(\d+)(?:[–-](\d+))?$',(_b.get('verse') or '').strip())
        try:
            if _m and _m.group(1) in AB:
                _C=_BB[AB.index(_m.group(1))][int(_m.group(2))-1]; _b['verseText']=' '.join(_C[_i-1] for _i in range(int(_m.group(3)),int(_m.group(4) or _m.group(3))+1))
        except Exception: pass
    open(OUT+'/shelf_66.json','w',encoding='utf-8').write(json.dumps(_sd,ensure_ascii=False,separators=(',',':')))
except Exception as _e:
    print('shelf_66.json:',_e); shutil.copy('site_src/shelf_66.json',OUT+'/shelf_66.json')
# 스토리 작업실(2026-11-11): 원고를 붙여 카드로 나누고 앱(v2) 미리보기로 보고 GitHub(ux/story_in)에 저장 → 다음 빌드가 story_cards.json에 합침
_PE=[{'id':p['id'],'memo':p.get('memo',''),'refs':p.get('refs',[]),'role':p.get('role','')} for p in (json.load(open('ux/photos.json')) if os.path.exists('ux/photos.json') else [])]
_P26=[{'n':x['n'],'label':x['label'],'ch':x['ch'],'topic':x.get('topic','')} for x in P365]
open(OUT+'/story_edit.html','w').write(open('site_src/story_edit.html').read().replace('/*PLANS*/','const PLAN26='+J(_P26)+';\nconst P27='+J(_p27.build())+';\nconst ABBR_L='+J(AB)+';\nconst PHOTOS_E='+J(_PE)+';\nconst MSD='+J((json.load(open('ux/ms_days.json')).get('days',{}) if os.path.exists('ux/ms_days.json') else {}))+';'))
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
<meta name="description" content="성경의 이야기를 따라 읽고, 묵상으로 마음에 새깁니다">
<meta property="og:type" content="website">
<meta property="og:site_name" content="이야기통독">
<meta property="og:title" content="이야기통독">
<meta property="og:description" content="성경의 이야기를 따라 읽고, 묵상으로 마음에 새깁니다">
<meta property="og:url" content="https://aqedah.github.io/CBSR/">
<meta property="og:image" content="https://aqedah.github.io/CBSR/og.png?v=9">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F8F5EF">
<script>try{{var t=localStorage.getItem("cbsr-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}</script>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="이야기통독">
<link rel="manifest" href="manifest.webmanifest">
<script>window.addEventListener("beforeinstallprompt",function(e){{e.preventDefault();window.__bip=e;}});</script>
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png?v=1">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png?v=3">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png?v=3">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}html{{-webkit-text-size-adjust:100%}}</style>
<style>#appBoot{{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;justify-content:center;background:#F8F5EF;color:#2A211B;transition:opacity .3s ease;font-family:"Gowun Batang","Nanum Myeongjo","AppleMyungjo",serif;text-align:center}}#appBoot.out{{opacity:0;pointer-events:none}}#appBoot .k{{font-family:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:12.5px;letter-spacing:.14em;color:#6E6152}}#appBoot .t{{font-weight:700;font-size:30px;margin-top:10px;color:#7A4528}}#appBoot .s{{font-size:15px;color:#6E6152;margin-top:8px}}#appBoot .bar{{width:160px;height:2px;background:#E5D9C8;margin:24px auto 0;overflow:hidden;border-radius:2px}}#appBoot .bar i{{display:block;height:100%;width:40%;background:#7A4528;animation:bootBar 1s ease-in-out infinite}}@keyframes bootBar{{from{{transform:translateX(-100%)}}to{{transform:translateX(250%)}}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) #appBoot{{background:#16120F;color:#EEE5D8}}:root:not([data-theme="light"]) #appBoot .t{{color:#D9A27A}}:root:not([data-theme="light"]) #appBoot .k,:root:not([data-theme="light"]) #appBoot .s{{color:#A69887}}:root:not([data-theme="light"]) #appBoot .bar{{background:#352C24}}:root:not([data-theme="light"]) #appBoot .bar i{{background:#D9A27A}}}}
:root[data-theme="dark"] #appBoot{{background:#16120F;color:#EEE5D8}}:root[data-theme="dark"] #appBoot .t{{color:#D9A27A}}:root[data-theme="dark"] #appBoot .k,:root[data-theme="dark"] #appBoot .s{{color:#A69887}}:root[data-theme="dark"] #appBoot .bar{{background:#352C24}}:root[data-theme="dark"] #appBoot .bar i{{background:#D9A27A}}
@media (prefers-reduced-motion: reduce){{#appBoot .bar i{{animation:none;width:100%}}}}</style>
</head>
<body>
<div id="appBoot" role="status"><div><img src="icons/icon-192.png?v=3" width="76" height="76" alt="" style="display:block;margin:0 auto 16px;border-radius:18px;box-shadow:0 4px 14px rgba(0,0,0,.12)"><div class="k">이야기통독</div><div class="t" id="bootD">&nbsp;</div><div class="s">성경의 이야기를 따라 읽습니다</div><div class="bar"><i></i></div></div></div><script>(function(){{try{{var q=location.search.match(/[?&]now=(\d{{4}})-(\d\d)-(\d\d)/),d=q?new Date(+q[1],q[2]-1,+q[3]):new Date();document.getElementById("bootD").textContent=(d.getMonth()+1)+"월 "+d.getDate()+"일 ("+["주일","월","화","수","목","금","토"][d.getDay()]+")";}}catch(e){{}}}})();</script>
'''
html=head+body+'\n</body>\n</html>\n'
# 11/17: 옛 화면(v1.html)·옛 체험판(demo.html)·스토리 시험(story.html)·UI 시안은 정식 배포에서 뺌
# QT 스토리 카드 시험 페이지: 기록은 'story:' 앞머리로 앱 기록과 분리, 365 통독표로 시작
SSHIM='<script>window.CBSR_STORY=1;(function(){try{var L=window.localStorage,P="story:",S={getItem:function(k){return L.getItem(P+k)},setItem:function(k,v){L.setItem(P+k,String(v))},removeItem:function(k){L.removeItem(P+k)},clear:function(){}};Object.defineProperty(window,"localStorage",{value:S,configurable:true});if(S.getItem("cbsr-mode")==null)S.setItem("cbsr-mode","y365");}catch(e){}})();</script>\n'
shead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+SSHIM).replace('<link rel="manifest" href="manifest.webmanifest">','').replace('content="https://aqedah.github.io/CBSR/"','content="https://aqedah.github.io/CBSR/story.html"')
# 전체 개편 시험(v2.html): 오늘·본문·도전·기록, 이야기 QT, 말씀 카드, 내일 본문 시계. 기록은 v2: 앞머리로 따로
VSHIM=SSHIM.replace('window.CBSR_STORY=1;','window.CBSR_STORY=1;window.CBSR_V2=1;').replace('Object.defineProperty(window,"localStorage"','/* v1 기록 가져오기: v2를 처음 열 때 한 번, v1(앞머리 없는 기록)을 v2: 쪽에 복사(이미 있는 v2 기록은 그대로) */if(!L.getItem("v2:cbsr-v1import")){var K=[];for(var i=0;i<L.length;i++){var k=L.key(i);if(k&&/^(cbsr-|rjnote:)/.test(k))K.push(k);}K.forEach(function(k){if(L.getItem("v2:"+k)==null)L.setItem("v2:"+k,L.getItem(k));});L.setItem("v2:cbsr-v1import",new Date().toISOString()+" "+K.length);}try{for(var j=0;j<L.length;j++){var kk=L.key(j);if(kk&&/^(cbsr-|rjnote:)/.test(kk)&&kk!=="cbsr-login-v1"){window.CBSR_HADV1=1;break;}}}catch(e){}window.__rawLS=L;Object.defineProperty(window,"localStorage"',1).replace('P="story:"','P="v2:"').replace('if(S.getItem("cbsr-mode")==null)','if(/[?&]p=rj/.test(location.search))S.setItem("cbsr-mode","rj");else if(/[?&]day=/.test(location.search))S.setItem("cbsr-mode","y365");else if(S.getItem("cbsr-mode")==null)S.setItem("cbsr-mode","y365");if(0)')
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
import datetime as _dt
_BUILD=(_dt.datetime.utcnow()+_dt.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M')
NOUNSHIM='<script>window.CBSR_BUILD="'+_BUILD+'";window.NOUNS_KRV='+json.dumps(sorted(k for k,v in _NM.items() if len(v)>=2),ensure_ascii=False,separators=(',',':'))+';</script>'
body_v2=body.replace('스토리 QT','스토리') # v2: 이름은 '스토리'만(2026-11-02)
v2html=shead.replace(SSHIM,VSHIM+NOUNSHIM).replace('story.html','v2.html')+body_v2+'\n</body>\n</html>\n'
# 11-20 GPT 감사: index.html과 v2.html이 같은 앱(각 8.9MB)이라 오프라인 설치 때 두 번 받았음 → v2.html은 index.html로 넘기는 작은 쪽(옛 즐겨찾기·링크는 그대로 열림)
open(f'{OUT}/v2.html','w').write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>이야기통독</title><script>location.replace("./"+location.search+location.hash)</script><a href="./">이야기통독 열기</a>\n')
ihead=head.replace('<meta charset="utf-8">','<meta charset="utf-8">\n'+VSHIM+NOUNSHIM)
open(f'{OUT}/index.html','w').write(ihead+body_v2+'\n</body>\n</html>\n')
V=h(html+v2html+bible)
sw=f'''/* 오프라인 지원: 앱 화면은 인터넷이 되면 늘 새로 받고(network first),
   성경 본문·지형도·아이콘·글꼴·라이브러리는 처음 받은 뒤 보관해 둡니다(cache first). 기록은 Firestore가 따로 보관합니다. */
const V="cbsr-{V}", D="cbsr-data-1", KEEP=["bible.js?v={h(bible[:5000]+str(len(bible)))}","bible_snb.js?v={TRV}","bible_shg.js?v={TRV}"];
/* 11-20 GPT 2차: 새 판마다 본문·지형도·그림까지 모두 지우던 것을 고침 — 앱 화면(V)만 판마다 바꾸고, 한 번 받은 자료(D)는 남김. 본문 파일은 지금 판이 아닌 것만 정리 */
const SHELL=["./","index.html","config.js","sync.js","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()));}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>/^cbsr-/.test(k)&&k!==V&&k!==D).map(k=>caches.delete(k))))
  .then(()=>caches.open(D)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(q=>{{const u=new URL(q.url);return /\/bible(_[a-z]+)?\.js$/.test(u.pathname)&&!KEEP.includes(u.pathname.split("/").pop()+u.search);}}).map(q=>c.delete(q))))).then(()=>caches.open(D)).then(c=>c.keys().then(rs=>Promise.all(rs.filter(q=>/ibasemaps-api|maps\\.eox\\.at|gibs\\.earthdata|elevation-tiles-prod/.test(q.url)).map(q=>c.delete(q))))).then(()=>self.clients.claim()));}});
self.addEventListener("fetch",e=>{{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);
  if(/firestore\\.googleapis\\.com|identitytoolkit|securetoken|firebaseinstallations/.test(u.hostname))return;
  /* 11-21 목사님(데이터·저장 공간): 성경 지구의 위성사진·높이 조각은 보관함에 넣지 않음(브라우저가 알아서 잠깐 보관). 넣으면 돌려 볼 때마다 휴대폰 저장 공간이 끝없이 참 */
  if(/ibasemaps-api\\.arcgis\\.com|maps\\.eox\\.at|gibs\\.earthdata\\.nasa\\.gov/.test(u.hostname)||/elevation-tiles-prod/.test(u.pathname))return;
  const shell=u.origin===location.origin&&!/bible\\.js|\\/terrain\\/|\\/terr[hwm]i?\\/|\\/icons\\/|\\/img\\//.test(u.pathname);
  /* 11-13: 앱 화면을 다시 열 때(탭이 지워졌다 돌아올 때 등) 망이 1.5초 안에 안 오면 보관본을 먼저 보여 주고, 새 판은 뒤에서 받아 둠(다음에 열 때 반영) */
  if(shell&&r.mode==="navigate"){{const net=fetch(r).then(res=>{{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));return res;}});
    const appPage=/(^|\\/)(index\\.html|v2\\.html)?$/.test(u.pathname);
    e.respondWith(caches.match(r,{{ignoreSearch:true}}).then(m=>m||(appPage?caches.match("index.html"):null)).then(m=>{{ if(!m) return net; let done=false; return Promise.race([net.then(x=>{{done=true;return x;}}).catch(()=>m),new Promise(ok=>setTimeout(()=>ok(m),1500))]); }}));return;}}
  /* 11-20 GPT 감사 P1-7: 망이 끊겼을 때 앱 화면 대신 index.html을 돌려주는 것은 앱 화면을 열 때만. 자료(json 등)·다른 쪽은 보관본이 없으면 분명한 오류로 */
  if(shell){{e.respondWith(fetch(r).then(res=>{{if(res.ok){{const cp=res.clone();caches.open(V).then(c=>c.put(r,cp));}}return res;}}).catch(()=>caches.match(r,{{ignoreSearch:true}}).then(m=>m||new Response("오프라인: 아직 받아 두지 않은 자료입니다.",{{status:503,headers:{{"Content-Type":"text/plain; charset=utf-8"}}}}))));return;}}
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{{if(res.ok||res.type==="opaque"){{const cp=res.clone();caches.open(D).then(c=>c.put(r,cp));}}return res;}})));}});
'''
open(f'{OUT}/sw.js','w').write(sw)
# 성경 골든벨 문제(도전 탭에서 처음 열 때만 받음, 2026-11-03)
import importlib.util as _iu; _sp=_iu.spec_from_file_location('gbb','ux/gb_build.py'); _gbb=_iu.module_from_spec(_sp); _sp.loader.exec_module(_gbb); _gbb.build(f'{OUT}/gb.json')
for f in []:
  if os.path.exists('study/'+f): shutil.copy('study/'+f,f'{OUT}/study/'+f)
open(f'{OUT}/.nojekyll','w').write('')
shutil.copy('site_src/README.md',OUT+'/README.md')
if os.path.exists('elev.json'): shutil.copy('elev.json',OUT+'/elev.json')  # 여정 높낮이(tools/elev_build.py, 2026-11-17)
for f in ['CLAUDE.md']: shutil.copy('site_src/'+f,OUT+'/'+f); shutil.copy('site_src/'+f,OUT+'/AGENTS.md')
print({f:os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT) if os.path.isfile(os.path.join(OUT,f))})
