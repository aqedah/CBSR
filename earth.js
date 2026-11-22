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
function crew(list,at){ CW.forEach(m=>m.remove()); CW=[]; if(!O.figure||!at) return; list.slice(0,4).forEach(([nm,as],j)=>{ const el=document.createElement("div"); el.className="ewalk co"; el.innerHTML=O.figure(as||"man")+`<span class="enm">${esc(nm)}</span>`; CW.push(new maplibregl.Marker({element:el,anchor:"top-left",offset:[-(j+1)*30,6+(j%2)*6]}).setLngLat(at).addTo(M)); }); }
function mood(txt){ if(!W||!txt) return; const el=W.getElement(); el.querySelector(".emood")?.remove(); const b=document.createElement("span"); b.className="emood"; b.textContent=txt; el.appendChild(b); setTimeout(()=>b.remove(),3300); }
/* 일행에서 떨어져 따로 가는 사람(룻 1:14 오르바 등): 그 사람만 자기 길로 걸어가다 사라짐 */
let SW=null; function sideWalk(sd,at){ if(SW){ SW.remove(); SW=null; } if(!O.figure) return; const pts=[at,...sd.p.map(p=>[p[2],p[1]])], el=document.createElement("div"); el.className="ewalk co";
  el.innerHTML=O.figure(sd.as_||"man")+`<span class="enm">${esc(sd.n||"")}</span>`; SW=new maplibregl.Marker({element:el,anchor:"bottom"}).setLngLat(at).addTo(M); const mk=SW;
  if(RM()){ mk.setLngLat(pts[pts.length-1]); return; } let t0=null; const dur=3200, f=ts=>{ if(SW!==mk) return; t0=t0||ts; const u=Math.min(1,(ts-t0)/dur), x=u*(pts.length-1), i=Math.min(pts.length-2,Math.floor(x)), r=x-i;
    mk.setLngLat([pts[i][0]+(pts[i+1][0]-pts[i][0])*r,pts[i][1]+(pts[i+1][1]-pts[i][1])*r]); el.style.opacity=u>.8?String((1-u)/.2):"1"; if(u<1) requestAnimationFrame(f); else { mk.remove(); if(SW===mk) SW=null; } }; setTimeout(()=>requestAnimationFrame(f),900); }
function noWalker(){ if(SW){ SW.remove(); SW=null; }  if(W){ W.remove(); W=null; WID=""; } CW.forEach(m=>m.remove()); CW=[]; }
/* 장면 k에서의 주인공·동행: 처음 동행(wth)에서 장면마다 합류(add)·이탈(drop) — 이탈은 그 장면이 끝난 뒤(dropAt:start면 처음부터) */
function cast(t,k){ let lead=t.as_||"man", nm=t.who||"", co=(t.wth||[]).map(x=>[x[0],x[1]]);
  for(let i=0;i<=k;i++){ const s=t.steps[i]; if(s.as_) lead=s.as_; if(s.who) nm=s.who; /* 11-22: add·drop은 한 사람일 수도, 여러 사람일 수도 있음(룻 1장: 오르바와 룻이 함께, 말론과 기룐이 함께) */
    if(s.add){ (Array.isArray(s.add[0])?s.add:[s.add]).forEach(a=>{ if(a&&a[0]&&!co.some(x=>x[0]===a[0])) co.push([a[0],a[1]]); }); }
    if(s.drop&&(i<k||s.dropAt==="start")){ const D=Array.isArray(s.drop)?s.drop:[s.drop]; co=co.filter(x=>!D.includes(x[0])); } }
  return {lead,nm,co}; }
function animLine(base,seg,done,onPt){ const segs=Array.isArray(base[0]&&base[0][0])?base:(base.length?[base]:[]), head=segs.slice(0,-1), last=segs[segs.length-1]||[], same=last.length&&seg.length&&last[last.length-1][0]===seg[0][0]&&last[last.length-1][1]===seg[0][1];
  const draw=pts=>same?[...head,last.concat(pts.slice(1))]:[...segs,pts];
  if(RM()||seg.length<2){ setLine("eroute",draw(seg)); onPt&&onPt(seg[seg.length-1]); done&&done(); return; }
  let L=0; const d=[0]; for(let i=1;i<seg.length;i++){ L+=Math.hypot(seg[i][0]-seg[i-1][0],seg[i][1]-seg[i-1][1]); d.push(L); }
  let t0=null; const dur=Math.min(4200,1400+L*260);
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
function home(keepView){ stack=[]; cur=null; step=-1; setLine("eroute",null); setLine("efull",null); noWalker();
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
function route(i){ const r=O.routes[i]; if(!r) return; cur=null; step=-1; noWalker(); const c=r.p.map(p=>[p[2],p[1]]); setLine("efull",null); setLine("eroute",null);
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
function tour(id,from){ const t=O.tours.find(x=>x.id===id); if(!t) return; cur=t; step=-1; const all=tourAll(t);
  addPins(tourPlaces(t)); setLine("eroute",null); setLine("efull",tourSegs(t)); noWalker(); const c0=cast(t,0); walker(c0.lead,all[0],c0.nm); crew(c0.co,all[0]);
  t._b=jbear(all); const b=new maplibregl.LngLatBounds(); all.forEach(c=>b.extend(c)); M.fitBounds(b,{padding:pad(),pitch:PITCH,bearing:t._b,duration:RM()?0:4200,curve:1.5,essential:true});
  panel(t.n,`<p class="ed">${esc(t.d||t.sub||"")}</p><button class="ebig" data-follow="${from||0}">▶ ${from?`${from+1}번째 장면부터 `:""}따라가기 · ${t.steps.length}장면</button>`+t.steps.map((s,k)=>`<button class="erow" data-follow="${k}"><span class="ic">${k+1}</span><span><b>${esc(s.t)}</b><small>${esc(s.ref||s.s||"")}</small></span></button>`).join(""));
  const e0=tourAll(t)[0]; if(e0) prefetch(e0,(t.steps[0]&&t.steps[0].z)||8); }
/* 11-21: 휴대폰에서 짧은 길은 "맞출 수 없다"며 오류가 나 다음 장면으로 안 넘어가던 문제 → 실패하면 여백을 줄여 다시, 그래도 안 되면 null(도착지로 날아감) */
function fitCam(b,o){ for(const sc of [1,.5,0]){ try{ const P=o.padding, q=Object.assign({},o,{padding:{top:P.top*sc,bottom:P.bottom*sc,left:P.left*sc,right:P.right*sc}}); const c=M.cameraForBounds(b,q); if(c&&c.center) return c; }catch(e){} } return null; }
function follow(k){ const t=cur; if(!t) return; try{ M.setPaintProperty("eroute","line-dasharray",[1,0]); }catch(e){} if(k>=t.steps.length){ tour(t.id); return; } step=k; const s=t.steps[k];
  /* 11-22 목사님("에스라가 예루살렘에서 페르시아로 이동하는 장면은 왜?"): 장면에 from(다른 곳에서 새 인물로 시작)이 있으면 앞 장면 끝에서 걸어가지 않고 그곳에서 시작 */
  const base=[]; let c0=t.start?[[t.start[2],t.start[1]]]:[]; t.steps.slice(0,k).forEach(x=>{ if(x.from){ if(c0.length) base.push(c0); c0=[[x.from[2],x.from[1]]]; } (x.p||[]).forEach(p=>c0.push([p[2],p[1]])); });
  if(s.from){ if(c0.length) base.push(c0); c0=[[s.from[2],s.from[1]]]; } if(c0.length) base.push(c0);
  const sp=(s.p||[]).map(p=>[p[2],p[1]]), lastSeg=base[base.length-1]||[]; const here=lastSeg.length?lastSeg[lastSeg.length-1]:(sp[0]||tourAll(t)[0]); const seg=[here,...sp]; /* 머무는 장면은 seg가 한 점 */
  setLine("eroute",base); const cs=cast(t,k), fig=s.sea?"boat":cs.lead; walker(fig,here,s.sea?"":cs.nm); crew(s.sea?[]:cs.co.filter(x=>!(s.side&&x[0]===s.side.n)),here); setTimeout(()=>mood(s.mood),RM()?0:600); const go=()=>{ if(cur!==t||step!==k) return; if(s.side&&s.side.p&&s.side.p.length) sideWalk(s.side,here); animLine(base,seg,null,pt=>walker(fig,pt,s.sea?"":cs.nm)); };
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
  if(t.classList.contains("ex")){ close(); return; }
  if(t.classList.contains("ego")){ enter(); return; } }
/* 11-22: 맨 아래 깔리는 6배율 사진을 성경 땅 전체(이탈리아~메소보다미아, 약 65장)만큼 들어갈 때 미리 받아 둠 */
function preBase(){ [[3,4,5,2,3],[4,8,10,5,6],[5,16,20,11,13],[6,32,41,23,27]].forEach(([z,x0,x1,y0,y1])=>{ for(let x=x0;x<=x1;x++) for(let y=y0;y<=y1;y++){ const u=`https://ibasemaps-api.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/${z}/${y}/${x}?token=${O.esriKey}`; if(PRE.has(u)) continue; PRE.add(u); const im=new Image(); im.crossOrigin="anonymous"; im.src=u; } }); }
function enter(){ spinOn=false; preBase(); $(".eintro").classList.add("off"); setTimeout(perfWatch,1500); if(O.startTour) { push(()=>home(true)); tour(O.startTour,O.startFrom||0); } else if(O.startRoute!=null){ push(()=>home(true)); route(O.startRoute); } else home(); }
function toEarth(){ clearPins(); noWalker(); setLine("eroute",null); setLine("efull",null); fold(true); M.flyTo({center:[38,24],zoom:1.3,pitch:0,bearing:0,duration:RM()?0:5500,essential:true}); }
function key(e){ if(!root) return; const tg=e.target; if(tg&&/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName)) return;
  /* Esc는 앱이 처리(뒤로 가기와 같은 길) */ if(cur&&step>=0&&e.key==="ArrowRight") follow(step+1); else if(cur&&step>0&&e.key==="ArrowLeft") follow(step-1); }

function open(opts){ if(root) close(true); O=opts||{}; stack=[]; cur=null; step=-1;
  if(!document.getElementById("eovcss")){ const s=document.createElement("style"); s.id="eovcss"; s.textContent=CSS; document.head.appendChild(s); }
  root=document.createElement("div"); root.id="eov"; root.setAttribute("role","dialog"); root.setAttribute("aria-label","성경 지구 지도");
  root.innerHTML=`<div class="estars"></div><div class="emap"></div>
   <div class="etop"><button class="eg ex" aria-label="닫기">✕</button><span class="ettl">${esc(O.kicker||"")}</span><button class="eg eunfold" aria-label="목록 펼치기">☰ 목록</button><button class="eg eearth" aria-label="지구로">◐ 지구</button></div>
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
    if(O.skipIntro) enter(); else { spinOn=true; M.on("moveend",()=>{ if(spinOn) spin(); }); spin(); } });
  ["mousedown","touchstart","wheel"].forEach(ev=>M.on(ev,()=>{ if(spinOn&&$(".eintro").classList.contains("off")) spinOn=false; }));
  M.on("error",e=>{ if(O.onTileError) O.onTileError(e); });
  return true; }
function close(silent){ removeEventListener("keydown",key); try{ clearPins(); noWalker(); M&&M.remove(); }catch(e){} M=null; if(root){ root.remove(); root=null; } spinOn=false; TER=false; const f=O&&O.onClose; O=null; if(!silent&&f) f(); }
window.CBSR_EARTH={open,close,isOpen:()=>!!root,_map:()=>M};
})();
