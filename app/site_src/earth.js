/* 성경 지구(2026-11-21 목사님: 구글어스처럼 지구에서 성경의 땅으로). 앱이 필요할 때만 불러오는 별도 파일.
   자료는 앱이 넘겨줌(큰 여정 BM_TOURS·작은 경로 ROUTES_B·지명 GAZ·주인공 묶음 BM_WHO를 그대로 읽어 바꾼 것) → 원본 자료와 지금 지도(Leaflet)는 그대로.
   위성사진: 멀리 NASA 블루마블(퍼블릭 도메인) · 가까이 Esri World Imagery(목사님 계정 열쇠). 높이: AWS Terrain Tiles */
(function(){
"use strict";
const CSS=`
#eov{position:fixed;inset:0;z-index:9990;background:radial-gradient(ellipse at 50% 60%,#0c1430 0%,#050814 45%,#010204 100%);color:#f7f1e6;font-family:"Noto Sans KR",system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
#eov .estars{position:absolute;inset:0;background-image:radial-gradient(1px 1px at 20px 30px,#fff,transparent),radial-gradient(1px 1px at 120px 80px,#cfe0ff,transparent),radial-gradient(1.5px 1.5px at 200px 150px,#fff,transparent),radial-gradient(1px 1px at 300px 40px,#fff,transparent),radial-gradient(1px 1px at 380px 210px,#ffeacc,transparent),radial-gradient(1px 1px at 60px 260px,#fff,transparent);background-size:420px 340px;opacity:.7}
#eov .emap{position:absolute;inset:0}
#eov .maplibregl-ctrl-attrib{background:rgba(0,0,0,.35)!important;color:#ddd;font-size:10px}#eov .maplibregl-ctrl-attrib a{color:#eee}
#eov .eg{background:rgba(14,12,10,.6);border:1px solid rgba(255,255,255,.16);color:#f7f1e6;border-radius:12px;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
#eov .etop{position:absolute;z-index:4;top:calc(10px + env(safe-area-inset-top));left:max(10px,env(safe-area-inset-left));right:max(10px,env(safe-area-inset-right));display:flex;gap:8px;align-items:center;pointer-events:none}
#eov .etop>*{pointer-events:auto}
#eov .etop button{height:42px;min-width:42px;padding:0 12px;font:600 14px "Noto Sans KR";cursor:pointer}
#eov .etop .ettl{flex:1;text-align:center;font:600 13.5px "Noto Sans KR";color:#e2d8c8;text-shadow:0 1px 6px #000;pointer-events:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#eov .eintro{position:absolute;z-index:5;left:0;right:0;bottom:0;padding:0 20px calc(28px + env(safe-area-inset-bottom));text-align:center;background:linear-gradient(transparent,rgba(0,0,0,.65) 55%);transition:opacity .8s,transform .8s}
#eov .eintro.off{opacity:0;transform:translateY(30px);pointer-events:none}
#eov .eintro small{display:block;letter-spacing:.3em;color:#e9c38a;font-size:12px;margin-bottom:10px}
#eov .eintro h1{font:700 clamp(30px,6.4vw,58px)/1.2 "Noto Serif KR",serif;margin:0 0 10px;text-shadow:0 4px 30px rgba(0,0,0,.6);text-wrap:balance}
#eov .eintro p{margin:0 0 20px;color:#d8ccbb;font-size:15px}
#eov .ego{border:0;border-radius:999px;padding:14px 34px;font:700 16px "Noto Sans KR";background:#e9c38a;color:#22170d;cursor:pointer;box-shadow:0 8px 30px rgba(233,195,138,.35)}
/* 칸: PC 오른쪽, 휴대폰 아래 */
#eov .epan{position:absolute;z-index:4;display:flex;flex-direction:column;opacity:0;pointer-events:none;transition:opacity .5s,transform .45s}
#eov .epan.on{opacity:1;pointer-events:auto}
@media (min-width:900px){ #eov .epan{top:64px;right:12px;bottom:12px;width:360px} #eov .epan.fold{transform:translateX(calc(100% + 16px))} }
@media (max-width:899px){ #eov .epan{left:8px;right:8px;bottom:calc(8px + env(safe-area-inset-bottom));max-height:46vh} #eov .epan.fold{transform:translateY(calc(100% - 46px))} }
#eov .ephd{display:flex;align-items:center;gap:8px;padding:10px 12px 6px}
#eov .ephd b{flex:1;font:700 15px "Noto Sans KR";white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#eov .ephd button{border:0;background:rgba(255,255,255,.1);color:#f7f1e6;border-radius:9px;height:34px;min-width:34px;padding:0 10px;font:600 13px "Noto Sans KR";cursor:pointer}
#eov .epb{overflow:auto;padding:4px 12px 12px;-webkit-overflow-scrolling:touch}
#eov .esec{font:700 12px "Noto Sans KR";color:#e9c38a;margin:10px 0 6px;letter-spacing:.04em}
#eov .erow{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:#f7f1e6;border-radius:11px;padding:10px 12px;margin-bottom:6px;cursor:pointer;font-family:"Noto Sans KR"}
#eov .erow:hover{background:rgba(255,255,255,.12)}
#eov .erow .ic{color:#e9c38a;font-size:13px;margin-top:2px;flex:none}
#eov .erow b{display:block;font-size:14.5px}#eov .erow small{display:block;color:#cfc3b1;font-size:12.5px;line-height:1.45}
#eov .etabs{display:flex;gap:2px;background:rgba(255,255,255,.08);border-radius:999px;padding:3px;margin:2px 0 8px}
#eov .etabs button{flex:1;border:0;background:none;color:#cfc3b1;border-radius:999px;padding:6px 0;font:600 13px "Noto Sans KR";cursor:pointer}
#eov .etabs button.on{background:rgba(255,255,255,.18);color:#fff}
#eov .eq{width:100%;box-sizing:border-box;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.08);color:#fff;border-radius:10px;padding:10px 12px;font:15px "Noto Sans KR";margin:2px 0 8px}
#eov .edress .fig{animation:edress 1.5s ease-out}@keyframes edress{0%{filter:brightness(2.2) drop-shadow(0 0 10px #fff3b0)}100%{filter:none}}#eov .ebord[aria-pressed="true"]{background:#e8c48a;color:#2a1d0c}#eov .ebchip{position:absolute;z-index:4;top:calc(58px + env(safe-area-inset-top));right:max(10px,env(safe-area-inset-right));font:600 12px "Noto Sans KR";color:#f3ead9;background:rgba(20,14,8,.62);padding:4px 10px;border-radius:12px;pointer-events:none}
#eov .ebl{font:700 13px/1.2 "Noto Sans KR";color:#fff;padding:2px 8px;border-radius:9px;box-shadow:0 1px 4px rgba(0,0,0,.45);white-space:nowrap;opacity:.88;pointer-events:none}#eov .ebl.sm{font-size:11px;opacity:.8}
#eov .efxm{pointer-events:none}.efx0{position:relative;width:0;height:0;pointer-events:none}.eparch{top:calc(env(safe-area-inset-top,0px) + 64px);z-index:30}@media (min-width:900px){.eparch{left:3%;right:auto;width:min(340px,calc(100% - 430px))}}#eov .mvpart.long i{width:28px;left:-14px;border-radius:14px}#eov .mvpart.long.on i:first-child{transform:translateX(-36px)}#eov .mvpart.long.on i:last-child{transform:translateX(36px)}#eov .etent{font-size:22px;text-align:center;transform:translate(-50%,-60%);filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}#eov .etent small{display:block;font:700 10.5px "Noto Sans KR";color:#fff;text-shadow:0 1px 3px #000}
#eov .egrp{position:absolute;left:46px;top:-4px;white-space:nowrap;font:700 11px "Noto Sans KR";color:#fff;background:rgba(70,52,30,.85);padding:2px 7px;border-radius:9px}
#eov .eburn{font-size:26px;transform:translate(-50%,-70%);animation:eburn 1.1s ease-in-out infinite alternate}@keyframes eburn{from{transform:translate(-50%,-70%) scale(.85)}to{transform:translate(-50%,-80%) scale(1.15)}}
#eov .mvquake canvas.maplibregl-canvas{animation:mvquake .11s linear infinite}
#eov .eunfold{display:none}#eov.pfold .eunfold{display:inline-flex;align-items:center}
.epin.hid b{opacity:0!important}
#eov .egrid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
#eov .egrid button{border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);color:#f7f1e6;border-radius:11px;padding:10px 4px;font:600 13px "Noto Sans KR";cursor:pointer}
#eov .eback{border:0;background:none;color:#e9c38a;font:700 13.5px "Noto Sans KR";padding:4px 0;cursor:pointer}
#eov .ed{font-size:13.5px;color:#e2d8c8;margin:4px 0 10px;line-height:1.6}
#eov .ebig{width:100%;height:46px;border:0;border-radius:11px;background:#e9c38a;color:#22170d;font:700 15px "Noto Sans KR";cursor:pointer;margin:4px 0 10px}
/* 따라가기 카드 */
#eov .ecard .dots{display:flex;gap:3px;margin:2px 0 8px}#eov .ecard .dots i{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.2)}#eov .ecard .dots i.on{background:#e9c38a}
#eov .ecard .k{font-size:12px;color:#e9c38a;font-weight:700}
#eov .ecard h2{font:700 20px/1.35 "Noto Serif KR";margin:2px 0 6px}
#eov .ecard .n{font-size:14px;line-height:1.65;color:#efe6d8;margin:0 0 8px}
#eov .ecard .v{font:15px/1.75 "Noto Serif KR";margin:0 0 2px;color:#fff}
#eov .ecard .r{font-size:12px;color:#cfc3b1;margin:0 0 10px}
#eov .ecard .row{display:flex;gap:8px}#eov .ecard .row button{flex:1;height:44px;border-radius:11px;border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.08);color:#f7f1e6;font:700 14px "Noto Sans KR";cursor:pointer}
#eov .ecard .row button.p{background:#e9c38a;color:#22170d;border-color:#e9c38a}
/* 지명 */
.epin{display:flex;align-items:center;gap:6px;pointer-events:none;opacity:0;transition:opacity .7s}
.epin.on{opacity:1}
.epin i{width:9px;height:9px;border-radius:50%;background:#ffd79a;box-shadow:0 0 0 3px rgba(255,215,154,.25),0 0 14px 4px rgba(255,190,110,.7)}
.epin b{font:700 12.5px "Noto Sans KR";color:#fff;text-shadow:0 1px 3px #000,0 0 10px rgba(0,0,0,.8);white-space:nowrap}
.epin.big i{width:13px;height:13px;background:#fff3dc}.epin.big b{font-size:15px}
.epin.sm b{opacity:0;transition:opacity .5s}.epin.sm.seen b{opacity:1}
/* 걷는 사람·배(앱의 여정 지도와 같은 도트 그림) */
.ewalk{width:0;height:0;pointer-events:none}.ewalk .chm{filter:drop-shadow(0 3px 4px rgba(0,0,0,.65))}
.ewalk .emood{position:absolute;left:0;bottom:62px;transform:translateX(-50%);background:#fff;color:#222;border-radius:14px;padding:3px 8px;font-size:18px;line-height:1.2;box-shadow:0 3px 10px rgba(0,0,0,.35);white-space:nowrap;animation:emood 3.2s ease forwards}
.ewalk .emood::after{content:"";position:absolute;left:50%;top:100%;transform:translateX(-50%);border:6px solid transparent;border-top-color:#fff}
@keyframes emood{0%{opacity:0;transform:translate(-50%,6px)}12%{opacity:1;transform:translate(-50%,0)}80%{opacity:1}100%{opacity:0}}
.ewalk.co .chm{transform:translate(-50%,-92%) scale(.86)}
.ewalk .enm{position:absolute;left:0;top:4px;transform:translateX(-50%);font:700 11.5px "Noto Sans KR";color:#fff;background:rgba(160,70,40,.92);border-radius:999px;padding:0 7px;white-space:nowrap}
#eov .epas{margin:2px 0 10px;padding:10px 12px;border-radius:10px;background:rgba(255,255,255,.07);font:14.5px/1.75 "Noto Serif KR"}
#eov .epas sup{color:#e9c38a;font:700 10px "Noto Sans KR";margin-right:2px}#eov .epas .on{background:rgba(233,195,138,.22);border-radius:3px}
#eov .elink{border:0;background:none;color:#e9c38a;font:700 13px "Noto Sans KR";padding:2px 0 8px;cursor:pointer}
#eov .eelev{margin:4px 0 10px}#eov .eelev svg{width:100%;height:auto;display:block}#eov .eelev small{color:#cfc3b1;font-size:12px}
/* 11-22: 글자·단추 줄이기는 휴대폰(599px 이하)만. 세로 태블릿(600–899px)은 정보판이 아래에 있어도 글자는 PC 크기 */
@media (max-width:599px){
 #eov .epan{max-height:40vh}
 #eov .ephd{padding:7px 10px 4px}#eov .ephd b{font-size:14px}#eov .ephd button{height:30px;min-width:30px}
 #eov .epb{padding:2px 10px 10px}
 #eov .ecard .dots{margin:0 0 5px}
 #eov .ecard .k{font-size:11px}
 #eov .ecard h2{font-size:16px;margin:1px 0 3px}
 #eov .ecard .n{font-size:12.5px;line-height:1.5;margin:0 0 5px}
 #eov .ecard .v{font-size:13.5px;line-height:1.6}
 #eov .ecard .r{font-size:11px;margin:0 0 6px}
 #eov .elink{font-size:12px;padding:0 0 6px}
 #eov .epas{font-size:13.5px;line-height:1.65;padding:8px 10px}
 #eov .ecard .row button{height:38px;font-size:13px}
 #eov .erow{padding:8px 10px}#eov .erow b{font-size:13.5px}#eov .erow small{font-size:12px}
 #eov .ed{font-size:12.5px}#eov .ebig{height:40px;font-size:14px}
}
@media (max-width:899px){ #eov .maplibregl-ctrl-bottom-left .maplibregl-ctrl-group{display:none} }
@media (prefers-reduced-motion:reduce){ #eov .eintro,#eov .epan{transition:none} }`;

let M=null, O=null, root=null, pins=[], spinOn=false, TER=false, cur=null, step=-1, stack=[], W=null, WID="", CW=[];
const RM=()=>matchMedia("(prefers-reduced-motion: reduce)").matches;
/* 11-21 목사님(카메라가 느림): 처음 선명도 휴대폰 1.5배·PC 2배까지 → 들어간 뒤 그리는 속도를 재서 느리면 1배로 */
const TOUCH=matchMedia("(pointer:coarse)").matches; const PR0=()=>Math.min(devicePixelRatio||1,(TOUCH||innerWidth<900)?1.5:2); /* 11-22: 태블릿 큰 화면을 2배로 그리면 버벅이며 깜빡임 → 손가락 기기는 1.5배까지 */
function perfWatch(){ let n=0, t0=performance.now(); const f=()=>{ if(!M) return; n++; const dt=performance.now()-t0; if(dt<4000) requestAnimationFrame(f); else { const fps=n*1000/dt; if(fps<28&&M.getPixelRatio()>1) M.setPixelRatio(1); } }; requestAnimationFrame(f); }
const wide=()=>innerWidth>=900;
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const $=s=>root.querySelector(s);

function style(key){
  const ESRI=(z,y,x)=>`https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}?token=${key}`;
  return {version:8,projection:{type:"globe"},
   sky:{"sky-color":"#0b1a3a","sky-horizon-blend":0.5,"horizon-color":"#a9c4ea","horizon-fog-blend":0.7,"fog-color":"#c8d5e6","fog-ground-blend":0.4,"atmosphere-blend":["interpolate",["linear"],["zoom"],0,1,5,1,8,0]},
   /* 11-22 목사님(휴대폰·태블릿 깜빡임): 사진 세 종류(블루마블·Sentinel-2·Esri)의 색이 서로 달라, 날아가는 동안 덜 온 조각 자리에 다른 색 사진이 비쳐 번쩍였음.
      → 지구 전체를 볼 때만 블루마블, 그 밖은 모두 Esri 한 가지(색이 같은 6~11배율). Esri는 12배율부터 다른 위성(어둡고 푸르스름)으로 바뀌므로
        여정이 쓰는 거리(11.5배율까지)에서는 11배율 사진을 늘려 쓰고, 손으로 더 다가갈 때만 12배율 이상을 색을 맞춰 겹침.
        6배율 사진을 늘 맨 아래 깔아 둬서(같은 색) 새 조각이 오기 전에도 빈자리·회색이 보이지 않음. */
   sources:{
    bm:{type:"raster",tiles:["https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_NextGeneration/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg"],tileSize:256,maxzoom:6,attribution:"NASA Blue Marble"},
    e6:{type:"raster",tiles:[ESRI("{z}","{y}","{x}")],tileSize:256,maxzoom:6},
    e11:{type:"raster",tiles:[ESRI("{z}","{y}","{x}")],tileSize:256,maxzoom:11,attribution:"Powered by Esri · Esri, Maxar, Earthstar Geographics"},
    esri:{type:"raster",tiles:[ESRI("{z}","{y}","{x}")],tileSize:256,minzoom:12,maxzoom:17},
    dem:{type:"raster-dem",tiles:["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],tileSize:256,encoding:"terrarium",maxzoom:12,attribution:"AWS Terrain Tiles"}},
   layers:[
    {id:"bg",type:"background",paint:{"background-color":"#9a8462"}},
    {id:"bm",type:"raster",source:"bm",maxzoom:3.2,paint:{"raster-fade-duration":0,"raster-brightness-min":0.08,"raster-saturation":-0.05}},
    {id:"e6",type:"raster",source:"e6",minzoom:2,paint:{"raster-opacity":["interpolate",["linear"],["zoom"],2.2,0,3,1],"raster-fade-duration":0}},
    {id:"e11",type:"raster",source:"e11",minzoom:5.5,paint:{"raster-fade-duration":200}},
    {id:"esri",type:"raster",source:"esri",minzoom:11.8,paint:{"raster-opacity":["interpolate",["linear"],["zoom"],11.8,0,12.6,1],"raster-hue-rotate":-16,"raster-saturation":0.35,"raster-brightness-min":0.1,"raster-contrast":-0.05}},
    {id:"shade",type:"hillshade",source:"dem",minzoom:5.5,paint:{"hillshade-exaggeration":["interpolate",["linear"],["zoom"],5.5,0.12,7.5,0.42],"hillshade-shadow-color":"rgba(30,18,6,.75)","hillshade-highlight-color":"rgba(255,248,232,.12)","hillshade-accent-color":"rgba(40,26,12,.6)","hillshade-illumination-direction":315}}]};
}
function terr(){ if(!M) return; const on=M.getZoom()>4.2; if(on!==TER){ TER=on; M.setTerrain(on?{source:"dem",exaggeration:1.7}:null); } }
function spin(){ if(!spinOn||RM()||!M) return; const c=M.getCenter(); c.lng-=0.06; M.easeTo({center:c,duration:60,easing:t=>t}); }
/* 미리 받기 */
const PRE=new Set();
function lx(l,z){ return Math.floor((l+180)/360*2**z); } function ly(a,z){ const r=a*Math.PI/180; return Math.floor((1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*2**z); }
function prefetch(c,z){ const zz=Math.round(z); [[Math.min(zz,11),"e"],[Math.min(zz-1,10),"e"],[Math.min(zz-1,12),"d"]].forEach(([q,k])=>{ if(q<1) return; const x0=lx(c[0],q), y0=ly(c[1],q); for(let dx=-2;dx<=2;dx++) for(let dy=-2;dy<=1;dy++){ const x=x0+dx, y=y0+dy; const u=k==="e"?`https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/${q}/${y}/${x}?token=${O.esriKey}`:k==="s"?`https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/${q}/${y}/${x}.jpg`:`https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${q}/${x}/${y}.png`; if(PRE.has(u)) continue; PRE.add(u); const im=new Image(); im.crossOrigin="anonymous"; im.src=u; } }); }
/* 11-22: 가까운 곳으로 옮길 때 멀어졌다 다가오면(flyTo) 지나는 배율마다 새 사진 조각을 받느라 깜빡임 → 화면 2.5개 거리 안이면 같은 높이로 미끄러지듯(easeTo) */
function move(o){ if(RM()) return M.jumpTo(o); const c=M.getCenter(), t=maplibregl.LngLat.convert(o.center), z=Math.min(o.zoom!=null?o.zoom:M.getZoom(),M.getZoom()), dpp=360/(512*2**z),
  px=Math.hypot((t.lng-c.lng)*Math.cos(t.lat*Math.PI/180),t.lat-c.lat)/dpp, q=Object.assign({},o); delete q.curve;
  if(px<2.5*Math.max(innerWidth,innerHeight)) M.easeTo(Object.assign(q,{duration:Math.min(o.duration||2600,2800),essential:true})); else M.flyTo(Object.assign(q,{curve:1.25,essential:true})); }
/* ── 카메라 원칙(11-22 목사님 확정, 문서 CBSR_성경지구_카메라원칙) ──
   ① 한 여정 안에서는 지도 방향을 한 번 정하고 바꾸지 않음(여정 전체가 가는 쪽, 북쪽에서 30° 넘게 돌리지 않음)
   ② 눕힌 각도는 어디서나 50° 하나
   ③ 장면마다 카메라는 한 번만, 걷기 전에 움직이고 걷는 동안은 멈춤(눈이 두 움직임을 동시에 쫓지 않게)
   ④ 이번 길이 이미 화면 안쪽(가장자리 12%를 뺀 곳)에 다 보이면 카메라를 움직이지 않음
   ⑤ 확대는 조금(0.8단계 미만) 더 당길 일이면 그대로 둠 — 자잘한 확대·축소를 하지 않음
   ⑥ 머무는 장면은 사람이 화면 안쪽에 있으면 그대로
   ⑦ 가까우면 같은 높이로 미끄러지고(2.4초), 멀 때만 한 번 날아감 */
const PITCH=50;
function bfold(b){ while(b>180) b-=360; while(b<-180) b+=360; if(b>90) b-=180; if(b<-90) b+=180; return b; }
function jbear(c){ return c.length<2?0:Math.max(-30,Math.min(30,bfold(bear(c[0],c[c.length-1])))); }
function visPad(){ return wide()?{top:90,bottom:70,left:60,right:420}:{top:80,bottom:Math.round(innerHeight*0.5),left:30,right:30}; }
function inSafe(pts){ if(!M) return false; const P=visPad(), W=M.getContainer().clientWidth, H=M.getContainer().clientHeight, l=P.left, r=W-P.right, t=P.top, b=H-P.bottom, mx=(r-l)*.12, my=(b-t)*.12;
  return pts.every(c=>{ const q=M.project(c); return q.x>=l+mx&&q.x<=r-mx&&q.y>=t+my&&q.y<=b-my; }); }
function settled(){ return Math.abs(M.getPitch()-PITCH)<1; }
/* 카메라를 한 번 옮기고, 다 옮긴 뒤 then() — 옮길 일이 없으면 바로 */
function camTo(o,then){ const c=M.getCenter(), t=maplibregl.LngLat.convert(o.center||c), same=Math.abs(c.lng-t.lng)<1e-4&&Math.abs(c.lat-t.lat)<1e-4&&Math.abs(M.getZoom()-(o.zoom!=null?o.zoom:M.getZoom()))<.01&&Math.abs(M.getBearing()-(o.bearing!=null?o.bearing:M.getBearing()))<.5&&Math.abs(M.getPitch()-(o.pitch!=null?o.pitch:M.getPitch()))<.5;
  if(same||RM()){ if(!same) M.jumpTo(o); then&&then(); return; } let done=false; const fin=()=>{ if(done) return; done=true; then&&then(); }; M.once("moveend",fin); setTimeout(fin,4200); move(o); }
function showSeg(seg,bb,mz,then){ const P=visPad(), z0=M.getZoom(), aligned=settled()&&Math.abs(M.getBearing()-bb)<1;
  if(seg.length<2){ const zt=Math.min(mz,Math.max(z0,mz-1.5)); if(aligned&&inSafe(seg)&&z0>=zt-1) { then&&then(); return; } camTo({center:seg[0],zoom:zt,bearing:bb,pitch:PITCH,padding:P},then); return; }
  const b=new maplibregl.LngLatBounds(); seg.forEach(c=>b.extend(c)); const cam=fitCam(b,{padding:P,bearing:bb,maxZoom:mz});
  if(!cam){ camTo({center:seg[seg.length-1],zoom:Math.min(z0,mz),bearing:bb,pitch:PITCH,padding:P},then); return; }
  let zt=Math.min(cam.zoom-0.35,mz);
  if(aligned&&inSafe(seg)&&z0>=zt-1&&z0<=zt+0.3){ then&&then(); return; } /* ④ 이미 알맞게 보이면 그대로 */
  if(zt>z0&&zt-z0<0.8) zt=z0; camTo({center:cam.center,zoom:zt,bearing:bb,pitch:PITCH},then); }
function bear(a,b){ const R=Math.PI/180, y=Math.sin((b[0]-a[0])*R)*Math.cos(b[1]*R), x=Math.cos(a[1]*R)*Math.sin(b[1]*R)-Math.sin(a[1]*R)*Math.cos(b[1]*R)*Math.cos((b[0]-a[0])*R); return Math.atan2(y,x)/R; }
function pad(){ return wide()?{top:80,bottom:60,left:60,right:400}:{top:80,bottom:Math.round(innerHeight*0.48),left:30,right:30}; }

function clearPins(){ pins.forEach(m=>m.remove()); pins=[]; }
/* 지명 이름이 겹치면 앞 순서(큰 곳 먼저)만 남김. 지도가 멈출 때마다 */
function declutter(){ if(!pins.length) return; const R2=[]; const L=pins.map((m,i)=>({el:m.getElement(),i})).sort((a,b)=>(b.el.classList.contains("big")-a.el.classList.contains("big"))||a.i-b.i);
  L.forEach(({el})=>{ el.classList.remove("hid"); const b=el.querySelector("b"); if(!b) return; if(el.classList.contains("sm")&&!el.classList.contains("seen")) return; const r=b.getBoundingClientRect(); if(!r.width) return;
    if(R2.some(q=>r.left<q.right+4&&r.right>q.left-4&&r.top<q.bottom+2&&r.bottom>q.top-2)) el.classList.add("hid"); else R2.push(r); }); }
function addPins(list){ clearPins(); list.forEach((p,i)=>{ const el=document.createElement("div"); el.className="epin"+(p.big?" big":p.sm?" sm":""); el.innerHTML=`<i></i><b>${esc(p.n)}</b>`; pins.push(new maplibregl.Marker({element:el,anchor:"left",offset:[-6,0]}).setLngLat([p.lng,p.lat]).addTo(M)); setTimeout(()=>el.classList.add("on"),200+Math.min(i,20)*90); }); }
function setLine(id,coords){ const s=M&&M.getSource(id); if(!s) return; /* 11-22: 장면이 다른 곳에서 새로 시작하면(from) 끊긴 여러 토막으로 그림 */
  if(coords&&coords.length&&Array.isArray(coords[0][0])){ const L=coords.filter(c=>c&&c.length>1); s.setData(L.length?{type:"Feature",geometry:{type:"MultiLineString",coordinates:L}}:{type:"FeatureCollection",features:[]}); return; }
  s.setData(coords&&coords.length>1?{type:"Feature",geometry:{type:"LineString",coordinates:coords}}:{type:"FeatureCollection",features:[]}); }
/* 11-21 목사님: 위성지도 위로 캐릭터·배. 장면의 주인공(as_)이 길을 따라 걷고, 바다 장면(sea)은 배 */
function walker(id,at,name){ if(!O.figure||!at||!M) return; if(W&&WID===id&&(W._nm||"")!==(name||"")){ W.remove(); W=null; } /* 11-22: 같은 그림이라도 이름이 바뀌면(스룹바벨→느헤미야) 새로 */ if(!W||WID!==id){ if(W) W.remove(); const el=document.createElement("div"); el.className="ewalk"; el.innerHTML=O.figure(id)+(name?`<span class="enm">${esc(name)}</span>`:""); W=new maplibregl.Marker({element:el,anchor:"top-left"}).setLngLat(at).addTo(M); W._nm=name||""; WID=id; } else W.setLngLat(at); CW.forEach(m=>m.setLngLat(at)); }
/* 동행: 주인공 뒤로 조금씩 비켜 서서 같이 움직임(바다에서는 배에 탄 것으로 보고 숨김) */
/* 장면 끝 옷 바꿈: 반짝이며 그 사람의 그림만 바뀜 */
function dressNow(D,cs,at,gone,key){ setTimeout(()=>{ if(!M||(key!=null&&key!==FXK)) return; /* 장면을 넘기면 옛 장면의 동행을 다시 그리지 않음 */ const co=cs.co.filter(x=>!(gone||[]).includes(x[0])).map(x=>{ const d=D.find(q=>q[0]===x[0]); return d?[x[0],d[1]]:x; }); crew(co,at);
  CW.forEach((m,j)=>{ if(D.some(q=>q[0]===co[j][0])){ const e=m.getElement(); e.classList.add("edress"); setTimeout(()=>e.classList.remove("edress"),1600); } }); },RM()?0:1400); }
function crew(list,at){ CW.forEach(m=>m.remove()); CW=[]; if(!O.figure||!at) return; list.slice(0,4).forEach(([nm,as],j)=>{ const el=document.createElement("div"); el.className="ewalk co"; el.innerHTML=O.figure(as||"man")+`<span class="enm">${esc(nm)}</span>`; const m=new maplibregl.Marker({element:el,anchor:"top-left",offset:[-(j+1)*30,6+(j%2)*6]}).setLngLat(at).addTo(M); m._n=nm; CW.push(m); }); }
function mood(txt){ if(!W||!txt) return; const el=W.getElement(); el.querySelector(".emood")?.remove(); const b=document.createElement("span"); b.className="emood"; b.textContent=txt; el.appendChild(b); setTimeout(()=>b.remove(),3300); }
/* 일행에서 떨어져 따로 가는 사람(룻 1:14 오르바 등): 그 사람만 자기 길로 걸어가다 사라짐 */
let SW=null; function sideWalk(sd,at){ if(SW){ SW.remove(); SW=null; } if(!O.figure) return; const pts=[at,...sd.p.map(p=>[p[2],p[1]])], el=document.createElement("div"); el.className="ewalk co";
  el.innerHTML=O.figure(sd.as_||"man")+`<span class="enm">${esc(sd.n||"")}</span>`; SW=new maplibregl.Marker({element:el,anchor:"bottom"}).setLngLat(at).addTo(M); const mk=SW;
  if(RM()){ mk.setLngLat(pts[pts.length-1]); return; } let t0=null; const dur=3200, f=ts=>{ if(SW!==mk) return; t0=t0||ts; const u=Math.min(1,(ts-t0)/dur), x=u*(pts.length-1), i=Math.min(pts.length-2,Math.floor(x)), r=x-i;
    mk.setLngLat([pts[i][0]+(pts[i+1][0]-pts[i][0])*r,pts[i][1]+(pts[i+1][1]-pts[i][1])*r]); el.style.opacity=u>.8?String((1-u)/.2):"1"; if(u<1) requestAnimationFrame(f); else { mk.remove(); if(SW===mk) SW=null; } }; setTimeout(()=>requestAnimationFrame(f),900); }
function noWalker(){ if(LD){ LD.remove(); LD=null; } if(SW){ SW.remove(); SW=null; }  if(W){ W.remove(); W=null; WID=""; } CW.forEach(m=>m.remove()); CW=[]; }
/* 장면 k에서의 주인공·동행: 처음 동행(wth)에서 장면마다 합류(add)·이탈(drop) — 이탈은 그 장면이 끝난 뒤(dropAt:start면 처음부터) */
function cast(t,k){ let lead=t.as_||"man", nm=t.who||"", co=(t.wth||[]).map(x=>[x[0],x[1]]);
  for(let i=0;i<=k;i++){ const s=t.steps[i]; if(s.as_) lead=s.as_; if(s.who) nm=s.who; /* 11-22: add·drop은 한 사람일 수도, 여러 사람일 수도 있음(룻 1장: 오르바와 룻이 함께, 말론과 기룐이 함께) */
    if(s.add){ (Array.isArray(s.add[0])?s.add:[s.add]).forEach(a=>{ if(a&&a[0]&&!co.some(x=>x[0]===a[0])) co.push([a[0],a[1]]); }); }
    if(s.drop&&(i<k||s.dropAt==="start")){ const D=Array.isArray(s.drop)?s.drop:[s.drop]; co=co.filter(x=>!D.includes(x[0])); }
    /* 11-23 목사님(민 20:28 엘르아살): 옷 바꿈 — dress0은 장면 처음, dress는 장면 끝(그 뒤 장면부터는 바뀐 옷) */
    const dr=d=>(d||[]).forEach(([n,a])=>{ co=co.map(x=>x[0]===n?[x[0],a]:x); if(n===nm) lead=a; }); dr(s.dress0); if(i<k) dr(s.dress); }
  return {lead,nm,co}; }
function animLine(base,seg,done,onPt,minMs,o){ o=o||{}; const segs=Array.isArray(base[0]&&base[0][0])?base:(base.length?[base]:[]), head=segs.slice(0,-1), last=segs[segs.length-1]||[], same=last.length&&seg.length&&last[last.length-1][0]===seg[0][0]&&last[last.length-1][1]===seg[0][1];
  const draw0=pts=>same?[...head,last.concat(pts.slice(1))]:[...segs,pts], DS=o.ds||[]; /* 11-24 dash: 성경이 길을 말하지 않는 장면의 길은 점선 층(eroutd)에 */
  const draw=pts=>{ if(o.dash){ setLine("eroutd",[...DS,pts]); return segs; } setLine("eroutd",DS.length?DS:null); return draw0(pts); };
  if(RM()||seg.length<2){ setLine("eroute",draw(seg)); onPt&&onPt(seg[seg.length-1]); done&&done(); return; }
  let L=0; const d=[0]; for(let i=1;i<seg.length;i++){ L+=Math.hypot(seg[i][0]-seg[i-1][0],seg[i][1]-seg[i-1][1]); d.push(L); }
  let t0=null; const dur=Math.max(minMs||0,Math.min(4200,1400+L*260)*(o.mul||1)); /* slow: 마을마다 들르며 천천히(눅 8:1) */
  const f=ts=>{ t0=t0||ts; const t=Math.min(1,(ts-t0)/dur), e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2, at=e*L; const pts=[seg[0]]; for(let i=1;i<seg.length;i++){ if(d[i]<=at) pts.push(seg[i]); else { const k=(at-d[i-1])/(d[i]-d[i-1]||1); pts.push([seg[i-1][0]+(seg[i][0]-seg[i-1][0])*k,seg[i-1][1]+(seg[i][1]-seg[i-1][1])*k]); break; } }
    setLine("eroute",draw(pts)); onPt&&onPt(pts[pts.length-1]); if(t<1) requestAnimationFrame(f); else done&&done(); }; requestAnimationFrame(f); }

/* 칸 내용 */
function fold(on){ const p=$(".epan"); p.classList.toggle("fold",on); root.classList.toggle("pfold",on&&wide()); }
/* 11-22: 화면을 돌리면(세로↔가로) 접힌 정보판의 '☰ 목록' 단추 표시를 다시 맞춤 — 세로에서 접고 가로로 돌리면 정보판이 옆으로 숨는데 단추가 없어 다시 열 수 없었음 */
addEventListener("resize",()=>{ if(!root) return; const p=root.querySelector(".epan"); root.classList.toggle("pfold",!!(p&&p.classList.contains("fold"))&&wide()); });
function panel(title,html,opt){ opt=opt||{}; const p=$(".epan"); p.classList.add("on"); fold(false); $(".ephd b").textContent=title; $(".epb").innerHTML=html; $(".epb").scrollTop=0; $(".epback").hidden=!stack.length; p.classList.toggle("ecard",!!opt.card); }
function push(fn){ stack.push(fn); }
let TAB="today", LASTLIST=null;
const TABS=[["today","오늘"],["who","주인공"],["era","시대"],["war","전쟁"],["place","지명"]];
function routeRows(idx){ return (idx||[]).map(i=>{ const r=O.routes[i]; return r?`<button class="erow" data-route="${i}"><span class="ic">〰</span><span><b>${esc(r.n)}</b><small>${esc(r.ref||"")}</small></span></button>`:""; }).join(""); }
function tourRows(ids){ return (ids||[]).map(id=>O.tours.find(t=>t.id===id)).filter(Boolean).map(t=>`<button class="erow" data-tour="${esc(t.id)}"><span class="ic">▶</span><span><b>${esc(t.n)}</b><small>${esc(t.sub||"")} · ${t.steps.length}장면</small></span></button>`).join(""); }
/* ── 나라 경계(11-23 목사님): 켜고 끄기, 시대는 보는 장면·경로·오늘 본문으로 자동. 경계는 번지게(정확한 선을 모르므로). 그 시대 자료가 없으면 그리지 않음 ── */
function eraOf(b,c){ if(!b) return null; c=c||1;
  if(b===1) return null; if(b<=6) return "exodus"; if(b===7||b===8) return "judges"; if(b===9) return c<=8?"judges":"saul"; if(b===10) return "united";
  if(b===11) return c<=11?"united":"divided"; if(b===12) return c<=15?"divided":c<=23?"assyria":"babylon";
  if(b===13) return c>=10?"united":null; if(b===14) return c<=9?"united":c<=27?"divided":c<=35?"assyria":"babylon";
  if(b>=15&&b<=17) return "persia"; if(b>=18&&b<=22) return null; if(b===23) return c<=39?"assyria":"babylon"; if(b>=24&&b<=26) return "babylon"; if(b===27) return c<=5?"babylon":"persia";
  if(b===28||b===30) return "divided"; if(b===32||b===33||b===34||b===36) return "assyria"; if(b===31||b===35) return "babylon"; if(b>=37&&b<=39) return "persia";
  if(b>=40&&b<=43) return "jesus"; if(b>=44) return "rome"; return null; }
let BON=false; try{ BON=localStorage.getItem("cbsr_bord")==="1"; }catch(e){} let BERA=null, BDRAWN=null, BDATA=null, BLAB=[];
function bLoad(){ return BDATA||(BDATA=fetch("borders.json").then(r=>r.json()).catch(()=>({eras:[]}))); }
let BCV=null, BPRO=false;
function bProto(){ if(BPRO||!window.maplibregl||!maplibregl.addProtocol) return; BPRO=true;
  maplibregl.addProtocol("bord",(params)=>new Promise((res)=>{ const m=params.url.match(/bord:\/\/[^/]+\/(\d+)\/(\d+)\/(\d+)/), t=document.createElement("canvas"); t.width=t.height=256;
    if(m&&BCV){ const z=+m[1], x=+m[2], y=+m[3], n=2**z, lon=k=>k/n*360-180, R=Math.PI/180, Ym=k=>Math.PI*(1-2*k/n); /* 조각의 메르카토르 y */
      const C=BCV, W=C.cv.width, H=C.cv.height, X=lo=>(lo-C.w)/(C.e-C.w)*W, YY=ym=>(C.Y0-ym)/(C.Y0-C.Y1)*H, sx=X(lon(x)), ex=X(lon(x+1)), sy=YY(Ym(y)), ey=YY(Ym(y+1));
      if(ex>0&&sx<W&&ey>0&&sy<H) t.getContext("2d").drawImage(C.cv,sx,sy,ex-sx,ey-sy,0,0,256,256); }
    t.toBlob(b=>b.arrayBuffer().then(buf=>res({data:buf})),"image/png"); })); }
function setEra(id){ BERA=id||null; bDraw(); }
function bClear(){ BLAB.forEach(m=>m.remove()); BLAB=[]; if(M&&M.getLayer("bord")) M.removeLayer("bord"); if(M&&M.getSource("bord")) M.removeSource("bord"); BDRAWN=null; }
function bChip(t){ const c=root&&root.querySelector(".ebchip"); if(!c) return; c.textContent=t||""; c.hidden=!t; }
function bDraw(){ const btn=root&&root.querySelector(".ebord"); if(btn) btn.setAttribute("aria-pressed",BON?"true":"false");
  if(!BON){ bClear(); bChip(""); return; } if(!BERA){ bClear(); bChip("이 본문 시대의 나라 경계는 아직 없습니다"); return; } if(BDRAWN===BERA) return;
  const want=BERA; bLoad().then(D=>{ if(!M||!BON||BERA!==want) return; const E=(D.eras||[]).find(e=>e.id===want); bClear(); if(!E){ bChip("이 본문 시대의 나라 경계는 아직 없습니다"); return; }
    let w=180,e=-180,sN=-90,sS=90; E.items.forEach(it=>it.p.forEach(([lo,la])=>{ w=Math.min(w,lo); e=Math.max(e,lo); sS=Math.min(sS,la); sN=Math.max(sN,la); })); w-=1.2; e+=1.2; sS-=1.2; sN+=1.2;
    const my=l=>Math.log(Math.tan(Math.PI/4+l*Math.PI/360)), Y0=my(sN), Y1=my(sS), W=Math.min(2048,Math.max(900,Math.round((e-w)*90))), H=Math.max(64,Math.round(W*(Y0-Y1)/((e-w)*Math.PI/180)));
    const cv=document.createElement("canvas"); cv.width=W; cv.height=H; const g=cv.getContext("2d"), kmpx=(e-w)*111*Math.cos((sN+sS)/2*Math.PI/180)/W, X=lo=>(lo-w)/(e-w)*W, Y=la=>(Y0-my(la))/(Y0-Y1)*H;
    E.items.forEach(it=>{ g.filter=`blur(${Math.max(2,Math.round((it.k?Math.min(6,E.blur):E.blur)/kmpx))}px)`; g.globalAlpha=.5; g.fillStyle=it.c; g.beginPath(); it.p.forEach(([lo,la],i)=>i?g.lineTo(X(lo),Y(la)):g.moveTo(X(lo),Y(la))); g.closePath(); g.fill(); });
    /* 땅 높이(3D)를 켠 지구에서는 그림 한 장(image) 층이 그려지지 않음 → 지도 조각(타일)처럼 잘라 주는 길(bord://)로 넣음 */
    BCV={cv,w,e,Y0,Y1,my}; bProto(); M.addSource("bord",{type:"raster",tiles:[`bord://${want}/{z}/{x}/{y}`],tileSize:256,minzoom:2,maxzoom:12}); const before=["efull","eroute"].find(id=>M.getLayer(id)); M.addLayer({id:"bord",type:"raster",source:"bord",paint:{"raster-opacity":.95,"raster-fade-duration":0}},before);
    E.items.forEach(it=>{ const ll=it.l||[it.p.reduce((a,q)=>a+q[0],0)/it.p.length,it.p.reduce((a,q)=>a+q[1],0)/it.p.length], el=document.createElement("div"); el.className="ebl"+(it.k?" sm":""); el.style.background=it.c; el.textContent=it.n+(it.k?` (${it.k})`:"");
      BLAB.push(new maplibregl.Marker({element:el}).setLngLat(ll).addTo(M)); });
    BDRAWN=want; bChip(`나라 경계 · ${E.n} · 대략`); }); }
function home(keepView){ stack=[]; cur=null; step=-1; fxClear(); tplSet(""); { const tc=(O.todayCh||[])[0]; setEra(tc?eraOf(tc[0],tc[1]):null); } setLine("eroute",null); setLine("efull",null); noWalker();
  const T=O.todayTours||[], pl=O.todayPlaces||[];
  let h=`<div class="etabs" role="tablist">${TABS.map(([k,n])=>`<button role="tab" data-etab="${k}" class="${TAB===k?"on":""}" aria-selected="${TAB===k}">${n}</button>`).join("")}</div>`;
  if(TAB==="who"){ h+=`<div class="egrid">${(O.groups||[]).map((g,i)=>`<button data-grp="${i}">${esc(g.n)}</button>`).join("")}</div>`; panel(O.title||"성경 지도",h); return; }
  if(TAB==="era"){ h+=(O.eras||[]).map((e,i)=>`<button class="erow" data-era="${i}"><span class="ic">${i+1}</span><span><b>${esc(e.n)}</b><small>${esc(e.y||"")}</small></span></button>`).join(""); panel(O.title||"성경 지도",h); return; }
  if(TAB==="war"){ h+=(O.wars||[]).map((e,i)=>`<button class="erow" data-war="${i}"><span class="ic">${i+1}</span><span><b>${esc(e.n)}</b><small>${esc(e.d||"")}</small></span></button>`).join(""); panel(O.title||"성경 지도",h); return; }
  if(TAB==="place"){ h+=`<input class="eq" type="search" placeholder="지명 찾기 (예: 가버나움)" aria-label="지명 찾기"><div class="eres"></div>`; panel(O.title||"성경 지도",h); const q=$(".eq"), res=$(".eres");
    const run=()=>{ const v=q.value.trim(); const L=(O.places||[]).map((p,i)=>[p,i]).filter(([p])=>!v||p.n.includes(v)).slice(0,60); res.innerHTML=L.map(([p,i])=>`<button class="erow" data-place="${i}"><span class="ic">●</span><span><b>${esc(p.n)}</b><small>${esc(p.k||"")}</small></span></button>`).join("")||`<p class="ed">찾는 곳이 없습니다.</p>`; };
    q.addEventListener("input",run); run(); return; }
  if(T.length) h+=`<p class="esec">오늘 본문이 들어 있는 큰 여정</p>`+T.map(x=>`<button class="erow" data-tour="${esc(x.id)}" data-from="${x.from||0}"><span class="ic">▶</span><span><b>${esc(x.n)}</b><small>${esc(x.note||x.sub||"")}</small></span></button>`).join("");
  if(pl.length) h+=`<p class="esec">오늘 나오는 곳 ${pl.length}곳</p><div class="ed">${pl.map(p=>esc(p.n)).join(" · ")}</div>`;
  if(!T.length&&!pl.length) h+=`<p class="ed">오늘 본문에는 지도에 나오는 곳이 없습니다. 주인공·시대·전쟁·지명으로 찾아 보세요.</p>`;
  panel(O.title||"성경 지도",h);
  if(pl.length&&!keepView){ addPins(pl.map(p=>({...p,big:true}))); const b=new maplibregl.LngLatBounds(); pl.forEach(p=>b.extend([p.lng,p.lat])); M.fitBounds(b,{padding:pad(),pitch:PITCH,bearing:0,maxZoom:8.5,duration:RM()?0:6500,curve:1.6,essential:true}); }
}
function listView(title,d,tours,routes,me){ LASTLIST=me; const tr=tourRows(tours), rr=routeRows(routes);
  panel(title,`${d?`<p class="ed">${esc(d)}</p>`:""}${tr?`<p class="esec">따라가는 큰 여정</p>${tr}`:""}${rr?`<p class="esec">지도로 보는 여정 ${routes.length}</p>${rr}`:""}${!tr&&!rr?`<p class="ed">이 묶음에는 지도에 그릴 여정이 없습니다.</p>`:""}`); }
function group(i){ const g=O.groups[i]; listView(g.n,"",g.tours,g.routes,()=>group(i)); }
function era(i){ const e=O.eras[i]; listView(e.n+(e.y?` · ${e.y}`:""),e.d,e.tours,e.routes,()=>era(i)); }
function war(i){ const e=O.wars[i]; listView(e.n,e.d,e.tours,e.routes,()=>war(i)); }
/* 작은 경로(지도로 보는 여정 237): 길을 그리며 사람이 걸어감 */
function route(i){ const r=O.routes[i]; if(!r) return; cur=null; step=-1; fxClear(); tplSet(""); setEra(eraOf(r.b,r.c&&r.c[0])); noWalker(); const c=r.p.map(p=>[p[2],p[1]]); setLine("efull",null); setLine("eroute",null);
  addPins(r.p.filter(p=>p[0]).map((p,k,a)=>({n:p[0],lat:p[1],lng:p[2],big:k===0||k===a.length-1})));
  const bb=jbear(c);
  try{ M.setPaintProperty("eroute","line-dasharray",r.est?[2,1.6]:[1,0]); }catch(e){} /* 성경이 길을 말하지 않는 추정 길은 점선 */
  const fig=r.sea?"boat":"man"; walker(fig,c[0]); showSeg(c,bb,11,()=>animLine([],c,null,pt=>walker(fig,pt)));
  panel(r.n,`<p class="ed">${esc(r.ref||"")}</p><p class="ed">${esc(r.p.map(p=>p[0]).filter(Boolean).join(" → "))}</p><button class="ebig" data-route="${i}">↻ 다시 걸어 보기</button>`,{card:true});
}
/* 높낮이 그래프(길을 따라 잰 땅 높이). 바다 아래(사해 등)도 그대로 */
function elevSVG(E){ const e=E.e, W=320, H=96, top=14, bot=20, mn=Math.min(0,...e), mx=Math.max(...e), sp=Math.max(50,mx-mn);
  const X=i=>i/(e.length-1)*W, Y=v=>top+(1-(v-mn)/sp)*(H-top-bot); const d=e.map((v,i)=>`${i?"L":"M"}${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join("");
  const im=e.indexOf(mx), sea=mn<0?`<line x1="0" x2="${W}" y1="${Y(0)}" y2="${Y(0)}" stroke="#7fb3d5" stroke-dasharray="3 3" stroke-width="1"/>`:"";
  let lastX=-99; const marks=(E.m||[]).filter(([n,f])=>{ const x=f*W; if(x-lastX<34) return false; lastX=x; return true; }).map(([n,f])=>`<line x1="${(f*W).toFixed(1)}" x2="${(f*W).toFixed(1)}" y1="${H-bot}" y2="${H-bot+4}" stroke="#cfc3b1"/><text x="${Math.min(W-2,Math.max(2,f*W)).toFixed(1)}" y="${H-4}" fill="#cfc3b1" font-size="9.5" text-anchor="${f<.08?"start":f>.92?"end":"middle"}">${esc(n)}</text>`).join("");
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="길의 높낮이"><path d="${d} L${W} ${H-bot} L0 ${H-bot} Z" fill="rgba(233,195,138,.22)"/><path d="${d}" fill="none" stroke="#e9c38a" stroke-width="1.8"/>${sea}<circle cx="${X(im)}" cy="${Y(mx)}" r="3" fill="#fff"/><text x="${Math.min(W-4,Math.max(4,X(im)))}" y="${Y(mx)-5}" fill="#fff" font-size="10" text-anchor="middle">${Math.round(mx)}m</text>${marks}</svg><small>길이 약 ${E.km}km · 가장 높은 곳 ${Math.round(mx)}m${mn<0?` · 가장 낮은 곳 해수면 아래 ${Math.round(-mn)}m`:""}</small>`; }
function place(i){ const p=O.places[i]; if(!p) return; addPins([{n:p.n,lat:p.lat,lng:p.lng,big:true}]); move({center:[p.lng,p.lat],zoom:p.z||10.5,pitch:PITCH,bearing:M.getBearing(),duration:RM()?0:3200,curve:1.42,essential:true,padding:wide()?{right:390}:{bottom:Math.round(innerHeight*0.48)}}); if(!wide()) fold(true); }
function tourSegs(t){ const S=[]; let c=t.start?[[t.start[2],t.start[1]]]:[]; t.steps.forEach(s=>{ if(s.from){ if(c.length) S.push(c); c=[[s.from[2],s.from[1]]]; } (s.p||[]).forEach(p=>c.push([p[2],p[1]])); }); if(c.length) S.push(c); return S; }
function tourAll(t){ const c=[t.start?[t.start[2],t.start[1]]:null]; t.steps.forEach(s=>(s.p||[]).forEach(p=>c.push([p[2],p[1]]))); return c.filter(Boolean); }
function tourPlaces(t){ const L=[]; if(t.start&&t.start[0]) L.push({n:t.start[0],lat:t.start[1],lng:t.start[2],big:true}); t.steps.forEach(s=>{ if(s.from&&s.from[0]&&!L.some(x=>x.n===s.from[0])) L.push({n:s.from[0],lat:s.from[1],lng:s.from[2],sm:true}); const e=(s.p||[])[(s.p||[]).length-1]; if(e&&e[0]&&!L.some(x=>x.n===e[0])) L.push({n:e[0],lat:e[1],lng:e[2],sm:true}); }); return L; }
function tour(id,from){ const t=O.tours.find(x=>x.id===id); if(!t) return; cur=t; step=-1; fxClear(); { const [tp,tn]=tplAt(t,0,true); tplSet(tp,tn); } { const r0=(t.steps.find(x=>x.r)||{}).r; setEra(r0?eraOf(r0[0],r0[1]):null); } const all=tourAll(t);
  addPins(tourPlaces(t)); setLine("eroute",null); setLine("efull",tourSegs(t)); noWalker(); const c0=cast(t,0); walker(c0.lead,all[0],c0.nm); crew(c0.co,all[0]);
  t._b=jbear(all); const b=new maplibregl.LngLatBounds(); all.forEach(c=>b.extend(c)); M.fitBounds(b,{padding:pad(),pitch:PITCH,bearing:t._b,duration:RM()?0:4200,curve:1.5,essential:true});
  panel(t.n,`<p class="ed">${esc(t.d||t.sub||"")}</p><button class="ebig" data-follow="${from||0}">▶ ${from?`${from+1}번째 장면부터 `:""}따라가기 · ${t.steps.length}장면</button>`+t.steps.map((s,k)=>`<button class="erow" data-follow="${k}"><span class="ic">${k+1}</span><span><b>${esc(s.t)}</b><small>${esc(s.ref||s.s||"")}</small></span></button>`).join(""));
  const e0=tourAll(t)[0]; if(e0) prefetch(e0,(t.steps[0]&&t.steps[0].z)||8); }
/* 11-21: 휴대폰에서 짧은 길은 "맞출 수 없다"며 오류가 나 다음 장면으로 안 넘어가던 문제 → 실패하면 여백을 줄여 다시, 그래도 안 되면 null(도착지로 날아감) */
function fitCam(b,o){ for(const sc of [1,.5,0]){ try{ const P=o.padding, q=Object.assign({},o,{padding:{top:P.top*sc,bottom:P.bottom*sc,left:P.left*sc,right:P.right*sc}}); const c=M.cameraForBounds(b,q); if(c&&c.center) return c; }catch(e){} } return null; }
/* ── 장면 효과: 옛 여정 지도(Leaflet)의 효과를 지구 지도로 옮김(11-23 목사님). 모양(CSS)은 앱의 것을 그대로 씀 ── */
const FXL=[]; let FXK=0, NIGHT=null;
function fxClear(){ FXK++; FXL.forEach(m=>{ try{ m.remove(); }catch(e){} }); FXL.length=0; const c=M&&M.getContainer(); if(c){ c.classList.remove("mvburn","mvquake","mvstorm","mvnight","mvdark","mvsplash"); }
  root&&root.querySelectorAll(".bmtgap,.mvcycle,.egrp,.parch").forEach(e=>e.remove()); try{ M&&M.getSource("eroutd")&&setLine("eroutd",null); }catch(e){}
  /* 앞 장면 효과가 남긴 인물 상태(오름·사라짐·엎드림·숨김)를 되돌림 */ [W,...CW].forEach(m=>{ if(!m) return; m.getElement().classList.remove("mvhide"); const h=chmOf(m); if(h){ h.classList.remove("rise","vanish","slow","dip","fall","stretch"); h.style.opacity=""; } }); }
const chmOf=m=>m&&m.getElement&&m.getElement().querySelector(".chm");
const tween=(ms,key,fn)=>new Promise(r=>{ if(RM()){ fn(1); return r(key===FXK); } const t0=performance.now(), f=ts=>{ if(key!==FXK) return r(false); const q=Math.min(1,(ts-t0)/ms); fn(q); q<1?requestAnimationFrame(f):r(true); }; requestAnimationFrame(f); });
const fxSky=(ll,html,z)=>fxMk(ll,"efx0",html,z||5);
function fxNight(){ const c=M.getContainer(); if(!NIGHT||!c.contains(NIGHT)){ NIGHT=document.createElement("div"); NIGHT.className="bmtnight"; c.appendChild(NIGHT); } }
function fxMk(ll,cls,html,z){ const o=document.createElement("div"); o.className="efxm"; o.style.zIndex=String(z||2); const i=document.createElement("div"); i.className=cls; i.innerHTML=html||""; o.appendChild(i);
  const m=new maplibregl.Marker({element:o,anchor:"center"}).setLngLat(ll).addTo(M); FXL.push(m); m._in=i; return m; }
function fxFig(ll,id,name){ const m=fxMk(ll,"ewalk co",O.figure(id)+(name?`<span class="enm">${esc(name)}</span>`:""),3); return m; }
const fxWait=(ms,key)=>new Promise(r=>setTimeout(()=>r(key===FXK),RM()?0:ms));
function fxEmo(m,e){ const el=m&&m.getElement&&m.getElement(); if(!el) return; const b=document.createElement("span"); b.className="emood"; b.textContent=e; el.appendChild(b); setTimeout(()=>b.remove(),1500); }
function scr(ll){ return M.project(ll); } function unscr(x,y){ const q=M.unproject([x,y]); return [q.lng,q.lat]; }
/* 무리 이름(grp)·사람 핀(pin)·장막(tent): 장면이 열릴 때 바로 */
function fxStatic(t,k,here){ const s=t.steps[k]; let P=new Map(), T=new Map(); (t.tent||[]).forEach(q=>T.set(q[0],q));
  for(let i=0;i<=k;i++){ const x=t.steps[i]; (x.pin||[]).forEach(q=>P.set(q[0],q)); (x.unpin||[]).forEach(n=>P.delete(n)); (x.tent||[]).forEach(q=>T.set(q[0],q)); (x.untent||[]).forEach(n=>T.delete(n)); }
  P.forEach(([n,as,pl])=>{ if(pl) fxFig([pl[2],pl[1]],as||"man",n); });
  T.forEach(([n,lat,lng])=>{ fxMk([lng,lat],"etent",`⛺<small>${esc(n)}</small>`,1); });
  let g=""; for(let i=0;i<=k;i++){ if(t.steps[i].grp!=null) g=t.steps[i].grp; } if(g&&W){ const e=document.createElement("span"); e.className="egrp"; e.textContent="＋ "+g; W.getElement().appendChild(e); } }
/* 홍해(출 14): 물이 갈라지고 → 건너고 → 애굽 군대가 따라오다 물이 덮음 */
async function fxPart(seg,key,walkP){ const a=seg[0], b=seg[seg.length-1], mid=[(a[0]+b[0])/2,(a[1]+b[1])/2], A=scr(a), B=scr(b), rot=Math.atan2(B.y-A.y,B.x-A.x)*180/Math.PI-90, len=Math.hypot(B.x-A.x,B.y-A.y);
  const m=fxMk(mid,"mvpart long","<i></i><i></i>",1); m._in.style.transform=`rotate(${rot}deg)`; m._in.style.setProperty("--pl",Math.round(Math.max(150,len*1.05))+"px"); requestAnimationFrame(()=>m._in.classList.add("on"));
  if(W) fxEmo(W,"😮"); if(!(await fxWait(1700,key))) return; await walkP(4600);
  if(key!==FXK) return; const sol=[0,1,2,3].map(()=>fxFig(a,"foe")); const t0=performance.now();
  await new Promise(r=>{ const f=ts=>{ if(key!==FXK) return r(); const q=Math.min(1,(ts-t0)/1300); sol.forEach((x,j)=>{ const g=Math.max(0,q-j*.08)*.45; x.setLngLat([a[0]+(b[0]-a[0])*g,a[1]+(b[1]-a[1])*g]); }); q<1?requestAnimationFrame(f):r(); }; requestAnimationFrame(f); });
  m._in.classList.add("off","close"); M.getContainer().classList.add("mvsplash"); sol.forEach(x=>x._in.style.cssText+=";transition:opacity 1.2s;opacity:0");
  if(!(await fxWait(1300,key))) return; M.getContainer().classList.remove("mvsplash"); if(W) fxEmo(W,"🎉🙌"); }
/* 요단(수 3:16): 위쪽 아담 성읍에서 물이 멈춰 쌓이고 아래는 마른 바닥 */
async function fxJordan(key){ const m=fxMk([35.55,32.1],"mvjor","<i></i><b></b>",1); requestAnimationFrame(()=>m._in.classList.add("on")); setTimeout(()=>m._in.classList.add("off"),RM()?0:5200); if(W) fxEmo(W,"😮🙏"); return fxWait(1200,key); }
/* 전쟁: 적군과 우리 편이 달려와 부딪히고 ⚔️💥, 진 쪽이 사라짐. w=["적 이름","lose"] */
async function fxBattle(at,w,key){ const nm=Array.isArray(w)?w[0]:typeof w==="string"?w:"적군", lose=Array.isArray(w)&&w[1]==="lose", P0=scr(at), R=Math.random;
  const mk=(dx,dy,id,n)=>{ const m=fxFig(unscr(P0.x+dx,P0.y+dy),id,n); m.getElement().querySelector(".chm")?.classList.add("walk"); return m; };
  const E=Array.from({length:6},(_,k)=>({m:mk(150+R()*60,(k-2.5)*20,"soldier",k===0?nm:""),to:[24+R()*20,(k-2.5)*11]})), Aa=Array.from({length:4},(_,k)=>({m:mk(-110-R()*40,(k-1.5)*20,"soldier",""),to:[-22-R()*14,(k-1.5)*12]}));
  E.forEach(e=>e.m.getElement().querySelector(".chm")?.classList.add("flip")); const all=[...E,...Aa]; all.forEach(x=>{ const q=scr(x.m.getLngLat()); x.f=[q.x-P0.x,q.y-P0.y]; });
  let t0=performance.now(); await new Promise(r=>{ const f=ts=>{ if(key!==FXK) return r(); const k=Math.min(1,(ts-t0)/1500), e=k*k*(3-2*k); all.forEach(x=>x.m.setLngLat(unscr(P0.x+x.f[0]+(x.to[0]-x.f[0])*e,P0.y+x.f[1]+(x.to[1]-x.f[1])*e))); k<1?requestAnimationFrame(f):r(); }; requestAnimationFrame(f); });
  t0=performance.now(); let nx=0; await new Promise(r=>{ const f=ts=>{ if(key!==FXK) return r(); all.forEach(x=>x.m.setLngLat(unscr(P0.x+x.to[0]+(R()-.5)*7,P0.y+x.to[1]+(R()-.5)*5))); if(ts>nx){ nx=ts+180; fxEmo(all[Math.floor(R()*all.length)].m,R()<.6?"⚔️":"💥"); } ts-t0<2400?requestAnimationFrame(f):r(); }; requestAnimationFrame(f); });
  (lose?Aa:E).forEach(x=>{ x.m._in.style.cssText+=";transition:opacity 1s;opacity:0"; }); if(W) fxEmo(W,lose?"😢":"🙌"); return fxWait(800,key); }
function fxBurn(at){ M.getContainer().classList.add("mvburn"); const P=scr(at); [[0,0],[18,-14],[-16,12],[22,16],[-20,-10]].forEach(([dx,dy],j)=>{ const m=fxMk(unscr(P.x+dx,P.y+dy),"eburn","🔥",2); m._in.style.animationDelay=(j*.15)+"s"; }); }
function fxSun(at){ const P=scr(at); fxMk(unscr(P.x-70,P.y-90),"mvsky","☀️",2); fxMk(unscr(P.x+80,P.y-70),"mvsky moon","🌙",2); }
function fxCycle(s){ const C=s.cycle||[1,1,1,1,1], N=["악을 행함","넘기심","부르짖음","구원자","평안"], d=document.createElement("div"); d.className="mvcycle";
  d.innerHTML=`<b>${esc(s.cyc||"사사기의 틀")}</b><div class="mvcyr">${N.map((n,k)=>`<span class="${C[k]?"on":"off"}"><i>${C[k]?"●":"○"}</i>${n}</span>`).join("<em>→</em>")}</div>${C.includes(0)?`<small>이 이야기에 기록되지 않은 것: ${N.filter((n,k)=>!C[k]).join(" · ")}</small>`:"<small>다섯 요소가 모두 있음</small>"}`;
  root.appendChild(d); requestAnimationFrame(()=>d.classList.add("on")); setTimeout(()=>{ d.classList.remove("on"); setTimeout(()=>d.remove(),700); },RM()?3000:6600); }
/* ── 2차(11-24): 포위·겉옷·승천·세례·로뎀·물고기·수레·양피지·성전·앞서가는 것·떠남 ── */
let TPLM=null, LD=null; const TPL_LL=[35.2354,31.778], LMN={site:"성전 터",built:"성전",ruin:"무너진 성전",build:"다시 짓는 성전"};
function tplAt(t,k,start){ let tp=t.tpl||"", n=""; for(let i=0;i<=k&&i<t.steps.length;i++){ const x=t.steps[i]; if(x.tpl&&!(start&&i===k&&x.burn)){ tp=x.tpl; n=x.tplN||""; } } return [tp,n]; }
function tplSet(kind,nm){ const k2=kind?kind+"|"+(nm||""):""; if(TPLM&&TPLM._k===k2) return; if(TPLM){ const o=TPLM; o.getElement().querySelector(".lmk")?.classList.add("out"); setTimeout(()=>o.remove(),RM()?0:700); TPLM=null; }
  if(!kind||!O.lm||!M) return; const el=document.createElement("div"); el.className="efx0"; el.style.zIndex="1"; el.innerHTML=O.lm(kind,nm||LMN[kind]||""); TPLM=new maplibregl.Marker({element:el,anchor:"center"}).setLngLat(TPL_LL).addTo(M); TPLM._k=k2; }
/* 언약궤·관처럼 무리 앞에서 가는 것(수 3:3, 창 50:13) */
function leadSet(s,at){ if(!s.lead||!O.figure||s.sea){ if(LD){ LD.remove(); LD=null; } return; } const k2=s.lead.join("|"); if(!(LD&&LD._k===k2)){ if(LD) LD.remove(); const el=document.createElement("div"); el.className="ewalk co"; el.innerHTML=O.figure(s.lead[1])+`<span class="enm">${esc(s.lead[0])}</span>`; LD=new maplibregl.Marker({element:el,anchor:"top-left"}).setLngLat(at).addTo(M); LD._k=k2; }
  LD.setLngLat(at); LD.setOffset([36,-2]); } /* 화면 칸(px)으로 비켜 둠 — 카메라가 옮겨 가도 곁에 있게 */
function leadAhead(hist,pt){ if(!LD) return; LD.setLngLat(pt); if(hist.length<5) return; const a=scr(hist[hist.length-5]), b=scr(pt), dx=b.x-a.x, dy=b.y-a.y, L=Math.hypot(dx,dy); if(L>1.5) LD.setOffset([dx/L*36,dy/L*36-2]); }
/* 떠남: 손 흔들고(👋) 사라짐 · 죽음은 손 흔들지 않고 천천히 · quiet는 조용히 */
async function fxDrop(s,key){ const dead=s.exit==="death"; for(const n of [].concat(s.drop||[])){ const m=CW.find(x=>x._n===n); if(!m) continue;
    if(!s.quiet&&!dead){ fxEmo(m,"👋"); if(!(await fxWait(700,key))) return false; } const h=chmOf(m); if(h){ h.classList.add("vanish"); if(dead) h.classList.add("slow"); } m.getElement().querySelector(".enm")?.style.setProperty("opacity","0");
    if(!(await fxWait(dead?1500:900,key))) return false; m.remove(); const i=CW.indexOf(m); if(i>=0) CW.splice(i,1); } return true; }
/* 포위(왕하 18, 25 · 렘 39): 북쪽 화면 밖에서 군대가 내려와 성을 에워쌈 → 불(burn이 있을 때만) */
async function fxSiege(at,t,s,key,burned){ const P0=scr(at), n=14, R=Math.random, A=[];
  for(let k=0;k<n;k++){ const th=k/n*Math.PI*2, fx=(R()-.5)*230, fy=-210-R()*90, tx=48*Math.sin(th), ty=38*Math.cos(th), m=fxFig(unscr(P0.x+fx,P0.y+fy),"foe",k?"":(t.siegeBy||"바벨론 군대")), h=chmOf(m); if(h){ h.classList.add("walk"); h.classList.toggle("flip",tx<fx); } A.push({m,fx,fy,tx,ty,d:R()*.25}); }
  if(!(await tween(5200,key,q=>{ A.forEach(a=>{ const g=Math.max(0,Math.min(1,(q-a.d)/(1-a.d))), e=1-(1-g)*(1-g); a.m.setLngLat(unscr(P0.x+a.fx+(a.tx-a.fx)*e,P0.y+a.fy+(a.ty-a.fy)*e)); }); if(R()<.03) fxEmo(A[Math.floor(R()*n)].m,"⚔️"); }))) return false;
  A.forEach(a=>chmOf(a.m)?.classList.remove("walk")); if(!(await fxWait(700,key))) return false; if(s.burn) burned(at); if(W) fxEmo(W,s.burn?"😭":"😨"); return fxWait(1500,key); }
/* 겉옷으로 물을 치니 갈라짐(왕하 2:8, 14): 팔을 들고 → 요단 물길에서만 짧게 갈라짐 → 건넘 → 다시 흐름 */
async function fxMantle(seg,key,walkP){ const h=chmOf(W); if(h) h.classList.add("stretch"); if(W) fxEmo(W,"🧥"); if(!(await fxWait(1100,key))) return;
  let X=null; for(let i=1;i<seg.length&&!X;i++){ const a=seg[i-1], b=seg[i], u=a[0]-35.552, v=b[0]-35.552; if(u*v<=0&&a[0]!==b[0]){ const k=u/(u-v); X=[a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k]; } } /* 여리고 앞 요단 물길(경도 35.55쯤) */
  const a=seg[0], b=seg[seg.length-1], A=scr(a), B=scr(b); X=X||[(a[0]+b[0])/2,(a[1]+b[1])/2];
  const m=fxMk(X,"mvpart long","<i></i><i></i>",1); m._in.style.transform=`rotate(${Math.atan2(B.y-A.y,B.x-A.x)*180/Math.PI-90}deg)`; m._in.style.setProperty("--pl","70px"); requestAnimationFrame(()=>m._in.classList.add("on"));
  [W,...CW].forEach(x=>x&&fxEmo(x,"😮")); if(!(await fxWait(1000,key))) return; if(h) h.classList.remove("stretch"); await walkP(3600); if(key!==FXK) return; m._in.classList.add("off","close"); }
/* 승천: 엘리야(왕하 2:11) 불수레가 두 사람 사이를 지나 갈라놓고, 회오리바람으로 올라감 · 예수님(눅 24:51) 축복하실 때 하늘로 올려지심 */
async function fxAscend(t,key){ if(!W) return true; const c0=W.getLngLat(), P0=scr(c0), at=(x,y)=>unscr(P0.x+x,P0.y+y), h=chmOf(W);
  if(t.id!=="elijah"){ fxMk(c0,"mvbeam","",3); if(!(await fxWait(1100,key))) return false; if(h) h.classList.add("rise"); CW.forEach(m=>fxEmo(m,"😮")); if(!(await fxWait(2600,key))) return false; CW.forEach(m=>fxEmo(m,"🙏")); return fxWait(1600,key); } /* 구름(행 1:9)은 누가복음에 없어 넣지 않음 */
  const off=m=>{ const o=m.getOffset(); return {x:o.x,y:o.y}; }, O0=CW.map(off), O1=CW.map((m,k)=>({x:20+k*12,y:2})), O2=CW.map((m,k)=>({x:30+k*14,y:66}));
  CW.forEach(m=>chmOf(m)?.classList.add("walk")); if(!(await tween(1300,key,q=>CW.forEach((m,k)=>m.setOffset([O0[k].x+(O1[k].x-O0[k].x)*q,O0[k].y+(O1[k].y-O0[k].y)*q]))))) return false;
  CW.forEach(m=>chmOf(m)?.classList.remove("walk")); if(!(await fxWait(700,key))) return false;
  const MY=30, X0=-230, X1=320, CT=2600, ts=CT*(0-X0)/(X1-X0), RS=ts+500, RD=2400, END=Math.max(CT,RS+RD), ch=fxSky(at(X0,MY),O.px?O.px("firechariot",{s:2,dy:18}):"🔥",6); let wh=null, rose=false, cry=false;
  if(!(await tween(END,key,q=>{ const tm=q*END;
    if(tm<=CT){ const f=tm/CT; ch.setLngLat(at(X0+(X1-X0)*f,MY-Math.sin(f*Math.PI*3)*3)); ch._in.style.opacity=String(1-Math.max(0,(f-.72)/.28)); } else ch._in.style.opacity="0";
    const g=Math.max(0,Math.min(1,(tm-(ts-250))/550)), g2=1-(1-g)*(1-g); if(g>0) CW.forEach((m,k)=>m.setOffset([O1[k].x+(O2[k].x-O1[k].x)*g2,O1[k].y+(O2[k].y-O1[k].y)*g2])); /* 불수레가 지나는 순간 밀려남 */
    if(!wh&&tm>=ts-100){ wh=fxSky(c0,O.px?O.px("whirlwind",{s:5,dy:10,cls:"pxgrow"}):"🌪️",5); CW.forEach(m=>fxEmo(m,"😮")); }
    if(!rose&&tm>=RS){ rose=true; if(h) h.classList.add("rise"); }
    if(wh&&tm>=RS){ const f=Math.min(1,(tm-RS)/RD); wh.setLngLat(at(0,-f*f*200)); wh._in.style.opacity=String(1-Math.max(0,(f-.55)/.45)); if(!cry&&f>.6){ cry=true; CW.forEach(m=>fxEmo(m,"😭")); } } }))) return false;
  if(!(await fxWait(900,key))) return false; const O3=CW.map(off); CW.forEach(m=>chmOf(m)?.classList.add("walk")); /* 엘리사가 엘리야가 섰던 자리로(왕하 2:13 겉옷을 주움) */
  const ok=await tween(1100,key,q=>CW.forEach((m,k)=>m.setOffset([O3[k].x*(1-q),O3[k].y*(1-q)]))); CW.forEach(m=>chmOf(m)?.classList.remove("walk")); return ok; }
/* 양피지 성벽 지도(느 2:12–15) */
async function fxParch(key){ if(!O.parch) return true; const pa=document.createElement("div"); pa.className="parch eparch"; pa.innerHTML=O.parch(); root.appendChild(pa); requestAnimationFrame(()=>pa.classList.add("on")); fxNight(); const c=M.getContainer(); c.classList.add("mvnight");
  const me=pa.querySelector(".pme"), X=pa.querySelector(".px");
  const run=(id,ms)=>{ const p=pa.querySelector("#"+id), L0=p.getTotalLength(); p.style.strokeDasharray=L0; p.style.strokeDashoffset=L0; p.style.opacity=1; return tween(ms,key,k=>{ const q=p.getPointAtLength(L0*k); p.style.strokeDashoffset=L0*(1-k); me.setAttribute("cx",q.x); me.setAttribute("cy",q.y); }); };
  if(!(await fxWait(1400,key))) return false; if(!(await run("pwRide",5200))) return false; if(X){ X.style.transition="opacity .6s"; X.setAttribute("opacity","1"); } me.classList.add("stop");
  if(!(await fxWait(2400,key))) return false; me.classList.remove("stop"); me.classList.add("foot"); if(!(await run("pwWalk",2800))) return false; if(!(await run("pwBack",4200))) return false;
  if(!(await fxWait(1500,key))) return false; pa.classList.remove("on"); c.classList.remove("mvnight"); setTimeout(()=>pa.remove(),900); return true; }
/* 에디오피아 내시의 수레(행 8:27–39) */
const cartMk=ll=>fxSky(ll,O.px?O.px("cart",{s:2,dy:14,cls:"pxflip"}):"🛞",4), cartRun=(C,on)=>{ const p=C&&C._in.querySelector(".pxs"); if(p) p.style.animationPlayState=on?"running":"paused"; };
/* 도착한 뒤 그 자리에서 벌어지는 일 */
const FXE={
  light:async(s,key)=>{ const c=W.getLngLat(), h=chmOf(W), b=fxMk(c,"mvbeam","",3); fxMk(c,"mvflash","",4)._in.classList.add("on"); if(!(await fxWait(700,key))) return false; fxMk(c,"mvflash","",4)._in.classList.add("on"); if(h) h.classList.add("fall"); /* 행 9:3–4 땅에 엎드러짐 */
    if(!(await fxWait(5100,key))) return false; b.remove(); if(h) h.classList.remove("fall"); fxEmo(W,"😶"); return fxWait(1200,key); },
  fire:async(s,key)=>{ const c=W.getLngLat(); if(!(await fxWait(1800,key))) return false; const fall=fxSky(c,O.px?O.px("firefall",{s:3,dx:64,dy:-6,cls:"pxdrop"}):"",6); if(!(await fxWait(750,key))) return false; /* 왕상 18:38 */
    fxMk(c,"mvflash","",4)._in.classList.add("on"); fxSky(c,O.px?O.px("altarfire",{s:2,dx:64,dy:8,cls:"pxgrow"}):"🔥",4); if(!(await fxWait(250,key))) return false; fall.remove(); if(!(await fxWait(5450,key))) return false; fxEmo(W,"🙇"); return fxWait(1000,key); },
  baptism:async(s,key)=>{ const c=W.getLngLat(), h=chmOf(W); if(!(await fxWait(900,key))) return false; if(h) h.classList.add("dip"); const sp=fxSky(c,'<span class="mvprop">💧</span>',4); if(!(await fxWait(1500,key))) return false; if(h) h.classList.remove("dip"); sp.remove();
    if(!(await fxWait(500,key))) return false; fxMk(c,"mvbeam","",3); const dv=fxSky(c,'<span class="mvdove">🕊️</span>',6); /* 성령이 비둘기 같이 내려오심(마 3:16) */
    if(!(await tween(2600,key,f=>{ const q=1-(1-f)*(1-f); dv.setOffset([Math.sin(f*7)*12,-200+148*q]); }))) return false; return fxWait(3000,key); },
  sleep:async(s,key)=>{ const c=W.getLngLat(), P=scr(c), at=(x,y)=>unscr(P.x+x,P.y+y), h=chmOf(W); if(h) h.classList.add("dip"); const zz=fxSky(c,`<span class="pxwrap pxzz" style="left:6px;top:-92px">${O.pxEmo?O.pxEmo("sleeps",3):"💤"}</span>`,6);
    for(let k=0;k<2;k++){ if(!(await fxWait(2300,key))) return false; const an=fxSky(at(40,-36),'<span class="mvangel">👼</span>',6); if(!(await fxWait(900,key))) return false; if(h) h.classList.remove("dip"); /* 천사가 두 번 깨움(왕상 19:5, 7) */
      const fd=fxSky(at(-30,6),'<span class="mvprop">🍞💧</span>',5); if(!(await fxWait(k?2600:3800,key))) return false; an._in.querySelector(".mvangel")?.classList.add("out"); fd.remove(); if(k===0&&h) h.classList.add("dip"); }
    if(h) h.classList.remove("dip"); zz.remove(); return true; },
  fish:async(s,key)=>{ const c=W.getLngLat(); [W,...CW].forEach(m=>m&&m.getElement().classList.add("mvhide")); fxSky(c,'<span class="mvfish">🐋<b>물고기 뱃속의 요나</b></span>',6); return fxWait(5200,key); }, /* 욘 1:17 */
  meetcart:async(s,key)=>{ const c=W.getLngLat(), P=scr(c), at=(x,y)=>unscr(P.x+x,P.y+y), C=cartMk(at(240,-150)), h=chmOf(W); cartRun(C,true); /* 행 8:29–31 */
    if(!(await tween(3000,key,f=>{ const q=1-(1-f)*(1-f); C.setLngLat(at(240-196*q,-150+146*q)); }))) return false; cartRun(C,false); if(!(await fxWait(1600,key))) return false;
    if(h) h.classList.add("walk"); if(!(await tween(900,key,f=>W.setLngLat(at(44*f,-4*f))))) return false; if(h){ h.classList.remove("walk"); h.style.opacity="0"; } cartRun(C,true);
    const ok=await tween(1200,key,f=>{ const q=at(44*(1-f),-4*(1-f)); W.setLngLat(q); C.setLngLat(q); }); cartRun(C,false); return ok; },
  spirit:async(s,key)=>{ const c=W.getLngLat(), P=scr(c), at=(x,y)=>unscr(P.x+x,P.y+y), C=cartMk(at(-40,-4)), h=chmOf(W); cartRun(C,false); /* 행 8:38–39 */
    if(!(await fxWait(900,key))) return false; if(h) h.classList.add("dip"); if(!(await fxWait(1600,key))) return false; if(h) h.classList.remove("dip"); if(!(await fxWait(1800,key))) return false;
    if(h) h.classList.add("vanish","slow"); fxEmo(C,"😮"); if(!(await fxWait(1600,key))) return false; cartRun(C,true); fxEmo(C,"😊");
    return tween(3400,key,f=>{ C.setLngLat(at(-40-240*f,-4+50*f)); C._in.style.opacity=String(1-Math.max(0,(f-.6)/.4)); }); } };
function follow(k){ const t=cur; if(!t) return; try{ M.setPaintProperty("eroute","line-dasharray",[1,0]); }catch(e){} if(k>=t.steps.length){ tour(t.id); return; } step=k; const s=t.steps[k]; if(s.r) setEra(eraOf(s.r[0],s.r[1]));
  /* 11-22 목사님("에스라가 예루살렘에서 페르시아로 이동하는 장면은 왜?"): 장면에 from(다른 곳에서 새 인물로 시작)이 있으면 앞 장면 끝에서 걸어가지 않고 그곳에서 시작 */
  /* 11-24 dash: 성경이 길을 말하지 않는 장면(민 33 광야 38년 등)의 길은 점선 토막(DS)으로 따로 */
  const base=[], DS=[]; let c0=t.start?[[t.start[2],t.start[1]]]:[]; t.steps.slice(0,k).forEach(x=>{ if(x.from){ if(c0.length) base.push(c0); c0=[[x.from[2],x.from[1]]]; } const P=(x.p||[]).map(p=>[p[2],p[1]]);
    if(x.dash&&P.length){ const a=c0.length?c0[c0.length-1]:P[0]; DS.push([a,...P]); if(c0.length) base.push(c0); c0=[P[P.length-1]]; } else P.forEach(p=>c0.push(p)); });
  if(s.from){ if(c0.length) base.push(c0); c0=[[s.from[2],s.from[1]]]; } if(c0.length) base.push(c0);
  const sp=(s.p||[]).map(p=>[p[2],p[1]]), lastSeg=base[base.length-1]||[]; const here=lastSeg.length?lastSeg[lastSeg.length-1]:(sp[0]||tourAll(t)[0]); const seg=[here,...sp]; /* 머무는 장면은 seg가 한 점 */
  setLine("eroute",base); const cs=cast(t,k), fig=s.sea?"boat":cs.lead; let co=cs.co.slice();
  if(s.drop&&s.dropAt==="start"&&k>0){ const pv=cast(t,k-1).co; [].concat(s.drop).forEach(n=>{ const q=pv.find(x=>x[0]===n); if(q&&!co.some(x=>x[0]===n)) co.push(q); }); } /* 처음에 떠나는 사람도 장면이 열릴 때는 보이고, 손 흔들고 떠남 */
  walker(fig,here,s.sea?"":cs.nm); crew(s.sea?[]:co.filter(x=>!(s.side&&x[0]===s.side.n)),here); setTimeout(()=>mood(s.mood),RM()?0:600); fxClear(); const key=FXK; setLine("eroutd",DS.length?DS:null); fxStatic(t,k,here); if(s.cycle||s.fx==="cycle") fxCycle(s);
  { const [tp,tn]=tplAt(t,k,true); tplSet(tp,tn); } leadSet(s,here);
  const burned=at=>{ fxBurn(at); if(s.tpl) setTimeout(()=>{ if(key===FXK){ const [a,b]=tplAt(t,k,false); tplSet(a,b); } },RM()?0:1600); }; /* 성전이 불탐(왕하 25:9) → 무너진 성전 */
  let CART=null; if(s.ride&&!s.sea){ CART=cartMk(here); const h=chmOf(W); if(h) h.style.opacity="0"; } /* 행 8:31 수레에 함께 탐 */
  const go=async()=>{ if(cur!==t||step!==k||key!==FXK) return; const c=M.getContainer();
    if(s.gap){ const g=document.createElement("div"); g.className="bmtgap"; g.textContent=s.gap; root.appendChild(g); setTimeout(()=>g.remove(),2700); if(!(await fxWait(2200,key))) return; }
    if(s.drop&&s.dropAt==="start"){ if(!(await fxDrop(s,key))) return; }
    if(s.side&&s.side.p&&s.side.p.length) sideWalk(s.side,here);
    if(s.quake){ c.classList.add("mvquake"); setTimeout(()=>c.classList.remove("mvquake"),RM()?0:1500); }
    if(s.storm) c.classList.add("mvstorm"); if(s.fx==="dark"){ fxNight(); c.classList.add("mvdark"); } if(s.fx==="sun") fxSun(here);
    let pil=null; if(s.fx==="pillar"){ pil=fxMk(here,"mvpil","<i></i><b></b>",2); fxNight(); setTimeout(()=>{ if(key!==FXK) return; pil._in.classList.add("fire"); c.classList.add("mvnight"); },RM()?0:2600); }
    const hist=[]; let CH=[]; if(s.chase){ const [cn,ca,cc]=s.chase; CH=Array.from({length:cc||3},(_,j)=>fxFig(here,ca||"soldier",j?"":cn)); CH.forEach(m=>m.getElement().querySelector(".chm")?.classList.add("walk")); }
    const walkP=(mn)=>new Promise(res=>{ cartRun(CART,true); animLine(base,seg,()=>{ cartRun(CART,false); res(); },pt=>{ walker(fig,pt,s.sea?"":cs.nm); if(pil) pil.setLngLat(pt); if(CART) CART.setLngLat(pt); hist.push(pt); leadAhead(hist,pt); CH.forEach((m,j)=>{ const q=hist[Math.max(0,hist.length-1-18-j*6)]; if(q) m.setLngLat(q); }); },mn,{mul:s.slow,dash:!!s.dash,ds:DS}); });
    if(s.fx==="jordan"&&seg.length>1){ if(!(await fxJordan(key))) return; }
    if(s.fx==="siege"){ if(!(await fxSiege(here,t,s,key,burned))) return; }
    else if(s.war&&s.stay){ if(!(await fxBattle(here,s.war,key))) return; if(s.burn) burned(here); }
    else if(s.burn&&s.stay) burned(here);
    if(s.fx==="ascend"){ if(!(await fxAscend(t,key))) return; }
    if(s.fx==="parch"){ if(!(await fxParch(key))) return; }
    if(s.fx==="part"&&seg.length>1) await fxPart(seg,key,walkP); else if(s.fx==="mantle"&&seg.length>1) await fxMantle(seg,key,walkP); else await walkP();
    if(key!==FXK) return; const end=seg[seg.length-1];
    if(s.war&&!s.stay){ if(!(await fxBattle(end,s.war,key))) return; if(s.burn) burned(end); }
    if(FXE[s.fx]&&W){ if(!(await FXE[s.fx](s,key))) return; }
    const dead=s.exit==="death"; /* 민 20:28: 옷을 벗겨 엘르아살에게 입히고 → 그 뒤에 아론이 죽음(본문 순서대로) */
    if(s.dress&&dead){ dressNow(s.dress,cs,end,[],key); if(!(await fxWait(3200,key))) return; }
    if(s.drop&&s.dropAt!=="start"){ if(!(await fxDrop(s,key))) return; }
    if(s.dress&&!dead&&cur===t&&step===k) dressNow(s.dress,cs,end,[].concat(s.drop||[]),key);
    if(s.storm) setTimeout(()=>c.classList.remove("mvstorm"),RM()?0:2500);
    if(pil) setTimeout(()=>{ if(key!==FXK) return; c.classList.remove("mvnight"); pil._in.style.opacity="0"; },RM()?0:3500); };
  pins.forEach((m,i)=>m.getElement().classList.toggle("seen",i<=k+1));
  if(t._b==null) t._b=jbear(tourAll(t)); const z=s.z||8, mz=Math.min(11.5,z+1.5);
  showSeg(seg,t._b,mz,go);
  const nx=t.steps[k+1]; if(nx&&nx.p&&nx.p.length){ const e=nx.p[nx.p.length-1]; setTimeout(()=>prefetch([e[2],e[1]],nx.z||8),1500); }
  panel(t.n,`<div class="dots">${t.steps.map((_,i)=>`<i class="${i<=k?"on":""}"></i>`).join("")}</div><div class="k">${k+1} / ${t.steps.length}${s.mood?` · ${esc(s.mood)}`:""}</div><h2>${esc(s.t)}</h2><p class="n">${esc(s.n||"")}</p>${s.verse?`<p class="v">${esc(s.verse)}</p><p class="r">${esc(s.ref||"")}</p>`:s.ref?`<p class="r">${esc(s.ref)}</p>`:""}${s.r&&O.passage?`<button class="elink" data-pas="1">본문 앞뒤 더 보기 ›</button><div class="epas" hidden></div>`:""}<div class="row"><button data-follow="${Math.max(0,k-1)}"${k?"":" disabled"}>‹ 앞</button><button class="p" data-follow="${k+1}">${k===t.steps.length-1?"여정 처음으로":"다음 ›"}</button></div>`,{card:true}); }

function onClick(e){ const t=e.target.closest("button"); if(!t||!root.contains(t)) return;
  if(t.dataset.grp!=null){ push(()=>home(true)); group(+t.dataset.grp); return; }
  if(t.dataset.tour){ const id=t.dataset.tour, f=+t.dataset.from||0; push(LASTLIST&&stack.length?LASTLIST:()=>home(true)); tour(id,f); return; }
  if(t.dataset.follow!=null){ const k=+t.dataset.follow; if(step<0) push(()=>tour(cur.id)); follow(k); return; }
  if(t.classList.contains("epback")){ const f=stack.pop(); if(f) f(); else home(); return; }
  if(t.classList.contains("efold")){ fold(!$(".epan").classList.contains("fold")); return; }
  if(t.classList.contains("eunfold")){ fold(false); return; }
  if(t.dataset.etab){ TAB=t.dataset.etab; home(true); return; }
  if(t.dataset.era!=null){ push(()=>home(true)); era(+t.dataset.era); return; }
  if(t.dataset.war!=null){ push(()=>home(true)); war(+t.dataset.war); return; }
  if(t.dataset.route!=null){ if(!t.classList.contains("ebig")) push(stack.length&&LASTLIST?LASTLIST:()=>home(true)); route(+t.dataset.route); return; }
  if(t.dataset.place!=null){ place(+t.dataset.place); return; }
  if(t.dataset.pas){ const box=$(".epas"); if(!box) return; if(!box.hidden){ box.hidden=true; t.textContent="본문 앞뒤 더 보기 ›"; return; } const s=cur&&cur.steps[step]; const P=s&&O.passage(s.r); if(!P) return; box.innerHTML=P.L.map(([v,x])=>`<span class="${v===s.r[2]?"on":""}"><sup>${v}</sup>${esc(x)}</span> `).join("")+`<br><small style="color:#cfc3b1;font-family:'Noto Sans KR'">${esc(P.lab)}${P.tr?` · ${esc(P.tr)}`:""}</small>`; box.hidden=false; t.textContent="본문 접기"; return; }
  if(t.classList.contains("eearth")){ toEarth(); return; }
  if(t.classList.contains("ebord")){ BON=!BON; try{ localStorage.setItem("cbsr_bord",BON?"1":"0"); }catch(e){} BDRAWN=null; bDraw(); return; }
  if(t.classList.contains("ex")){ close(); return; }
  if(t.classList.contains("ego")){ enter(); return; } }
/* 11-22: 맨 아래 깔리는 6배율 사진을 성경 땅 전체(이탈리아~메소보다미아, 약 65장)만큼 들어갈 때 미리 받아 둠 */
function preBase(){ [[3,4,5,2,3],[4,8,10,5,6],[5,16,20,11,13],[6,32,41,23,27]].forEach(([z,x0,x1,y0,y1])=>{ for(let x=x0;x<=x1;x++) for(let y=y0;y<=y1;y++){ const u=`https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}?token=${O.esriKey}`; if(PRE.has(u)) continue; PRE.add(u); const im=new Image(); im.crossOrigin="anonymous"; im.src=u; } }); }
function enter(){ spinOn=false; preBase(); $(".eintro").classList.add("off"); setTimeout(perfWatch,1500); if(O.startTour) { push(()=>home(true)); tour(O.startTour,O.startFrom||0); } else if(O.startRoute!=null){ push(()=>home(true)); route(O.startRoute); } else home(); }
function toEarth(){ clearPins(); noWalker(); fxClear(); tplSet(""); setLine("eroute",null); setLine("efull",null); fold(true); M.flyTo({center:[38,24],zoom:1.3,pitch:0,bearing:0,duration:RM()?0:5500,essential:true}); }
function key(e){ if(!root) return; const tg=e.target; if(tg&&/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName)) return;
  /* Esc는 앱이 처리(뒤로 가기와 같은 길) */ if(cur&&step>=0&&e.key==="ArrowRight") follow(step+1); else if(cur&&step>0&&e.key==="ArrowLeft") follow(step-1); }

function open(opts){ if(root) close(true); O=opts||{}; stack=[]; cur=null; step=-1;
  if(!document.getElementById("eovcss")){ const s=document.createElement("style"); s.id="eovcss"; s.textContent=CSS; document.head.appendChild(s); }
  root=document.createElement("div"); root.id="eov"; root.setAttribute("role","dialog"); root.setAttribute("aria-label","성경 지구 지도");
  root.innerHTML=`<div class="estars"></div><div class="emap"></div>
   <div class="etop"><button class="eg ex" aria-label="닫기">✕</button><span class="ettl">${esc(O.kicker||"")}</span><button class="eg eunfold" aria-label="목록 펼치기">☰ 목록</button><button class="eg ebord" aria-pressed="false" aria-label="나라 경계 켜고 끄기">나라</button><button class="eg eearth" aria-label="지구로">◐ 지구</button></div><div class="ebchip" hidden></div>
   <div class="eintro${O.skipIntro?" off":""}"><small>이야기통독 · 성경의 땅</small><h1>${esc(O.heading||"성경의 땅으로")}</h1><p>${esc(O.sub||"")}</p><button class="ego">들어가기</button></div>
   <aside class="epan eg"><div class="ephd"><button class="epback" aria-label="뒤로" hidden>‹</button><b></b><button class="efold" aria-label="칸 접기">⌄</button></div><div class="epb"></div></aside>`;
  document.body.appendChild(root); root.addEventListener("click",onClick); addEventListener("keydown",key);
  try{
    M=new maplibregl.Map({container:root.querySelector(".emap"),center:O.center||[38,24],zoom:O.skipIntro?4:1.3,pitch:0,maxPitch:75,attributionControl:{compact:true},pixelRatio:PR0(),maxTileCacheSize:800,fadeDuration:280,cancelPendingTileRequestsWhileZooming:false,style:style(O.esriKey)});
  }catch(e){ close(true); if(O.onFail) O.onFail(e); return false; }
  M.addControl(new maplibregl.NavigationControl({visualizePitch:true}),"bottom-left"); /* 오른쪽은 칸이 가림 */
  M.on("zoomend",terr); M.on("moveend",declutter);
  M.on("load",()=>{ M.addSource("efull",{type:"geojson",data:{type:"FeatureCollection",features:[]}}); M.addSource("eroute",{type:"geojson",data:{type:"FeatureCollection",features:[]}});
    M.addLayer({id:"efull",type:"line",source:"efull",paint:{"line-color":"#fff2d6","line-width":2,"line-opacity":.35,"line-dasharray":[2,2]},layout:{"line-cap":"round","line-join":"round"}});
    M.addLayer({id:"eroute-glow",type:"line",source:"eroute",paint:{"line-color":"#ffd08a","line-width":12,"line-blur":10,"line-opacity":.55},layout:{"line-cap":"round","line-join":"round"}});
    M.addLayer({id:"eroute",type:"line",source:"eroute",paint:{"line-color":"#fff2d6","line-width":3},layout:{"line-cap":"round","line-join":"round"}});
    M.addSource("eroutd",{type:"geojson",data:{type:"FeatureCollection",features:[]}}); M.addLayer({id:"eroutd",type:"line",source:"eroutd",paint:{"line-color":"#fff2d6","line-width":3,"line-dasharray":[2,1.6]},layout:{"line-join":"round"}});
    if(O.skipIntro) enter(); else { spinOn=true; M.on("moveend",()=>{ if(spinOn) spin(); }); spin(); } });
  ["mousedown","touchstart","wheel"].forEach(ev=>M.on(ev,()=>{ if(spinOn&&$(".eintro").classList.contains("off")) spinOn=false; }));
  M.on("error",e=>{ if(O.onTileError) O.onTileError(e); });
  return true; }
function close(silent){ removeEventListener("keydown",key); try{ fxClear(); TPLM=null; clearPins(); noWalker(); M&&M.remove(); }catch(e){} M=null; if(root){ root.remove(); root=null; } spinOn=false; TER=false; const f=O&&O.onClose; O=null; if(!silent&&f) f(); }
window.CBSR_EARTH={open,close,isOpen:()=>!!root,_map:()=>M};
})();
