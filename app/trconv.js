/* ── 번역별 표기 맞추기: 새번역·새한글을 고르면 요약·길잡이·설명 글의 이름·용어·인용을 그 번역으로 ── */
const TRX=(()=>{try{const t=localStorage.getItem("cbsr-tr");return t==="snb"||t==="shg"?t:"krv";}catch(e){return "krv";}})();
const TRMAP=TRX==="snb"?TRMAP_SNB:TRX==="shg"?TRMAP_SHG:null;
const TR_ALIAS={};
if(TRMAP){
  const keys=Object.keys(TRMAP.n).sort((a,b)=>b.length-a.length);
  const J1="(이여|이라|이요|이며|이니|이나|으로|이|가|은|는|을|를|과|와|로|여|아|야|라|요|며|니|나)?";
  const REST="(?:이라는|이라고|으로부터|에서부터|에서는|에서도|에서|에게서|에게|께서|까지|부터|에도|에는|보다|처럼|의|에|도|만|께|들|인|란|라는|이|은|는|을|를|과|와|으로|로)*";
  const RE=new RegExp("(?<![가-힣])("+keys.map(escRe).join("|")+")"+J1+"(?="+REST+"(?![가-힣]))","g");
  const Q=Object.entries(TRMAP.q).sort((a,b)=>b[0].length-a[0].length);
  const conv=s=>{ if(typeof s!=="string"||!s) return s;
    for(const [q,t] of Q) if(s.includes(q)) s=s.split(q).join(t);
    return s.replace(RE,(m,n,j,off,str)=>{ if(n==="바로"&&!j){ const af=str.slice(off+m.length,off+m.length+3); if(!af||/^\s/.test(af)&&!/^ 왕/.test(af)) return m; } const t=TRMAP.n[n]; return t+(j?fixJosa(t,j):""); }); };
  const walk=o=>{ if(Array.isArray(o)){ for(let i=0;i<o.length;i++){ if(typeof o[i]==="string") o[i]=conv(o[i]); else if(o[i]&&typeof o[i]==="object") walk(o[i]); } }
    else if(o&&typeof o==="object"){ for(const k in o){ if(typeof o[k]==="string") o[k]=conv(o[k]); else if(o[k]&&typeof o[k]==="object") walk(o[k]); } } };
  [SUMMARY,WEEKS,CURATED,DETAIL,CLUE_LIST,GAP_LIST,ARC_LIST,GUIDE,EYE,DAYC,BOOKINFO].forEach(walk);
  for(const o of [PLACEINFO,PEOPLEINFO]) for(const k in o){ const p=o[k]; p.v.forEach(x=>{ x[1]=conv(x[1]); }); if(p.m) p.m=conv(p.m); }
  GLOSSARY.forEach(g=>{ g[1]=conv(g[1]); });
  for(const k in FLOW){ FLOW[k].t=conv(FLOW[k].t); walk(FLOW[k].qz); }
  ROUTES_B.forEach(r=>{ r.n=conv(r.n); r.p.forEach(q=>{ if(TRMAP.n[q[0]]) q[0]=TRMAP.n[q[0]]; }); });
  /* 번역 본문에서 이름·용어를 찾을 수 있도록 번역 표기를 별칭으로 */
  for(const [a,t] of Object.entries(TRMAP.n)){
    if(PLACEINFO[a]||PEOPLEINFO[a]) TR_ALIAS[t]=a;
    const gp=GAZ.places.find(p=>p[0]===a); if(gp&&!GAZ.places.some(p=>p[0]===t)) GAZ.places.push([t,gp[1],gp[2],gp[3]]);
    if(GAZ.people.includes(a)&&!GAZ.people.includes(t)) GAZ.people.push(t);
    const gl=GLOSSARY.find(g=>g[0]===a); if(gl&&!GLOSSARY.some(g=>g[0]===t)) GLOSSARY.push([t,gl[1],gl[2]]);
  }
}
