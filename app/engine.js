/* ───────── 이름·지명·용어 찾기와 자동 퀴즈 엔진 ───────── */
const PARTICLE="(?:께서|에게서|으로부터|에게|에서|으로|까지|부터|이여|이요|이라|이니|이며|이나|이다|이시|사람|족속|자손|지방|광야|이|가|은|는|을|를|의|에|로|과|와|도|만|아|야|여|라|땅|성|산|강|왕|온|들|께|인|요|며|니|나|고)";
const escRe=s=>s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");

function buildEntityIndex(PLACES, PEOPLE){
  const map=new Map();
  for(const p of PLACES) map.set(p[0],{name:p[0],type:"place",lat:p[1],lon:p[2],kind:p[3]});
  for(const n of PEOPLE) if(!map.has(n)) map.set(n,{name:n,type:"person"});
  const names=[...map.keys()].sort((a,b)=>b.length-a.length);
  const re=new RegExp("(?<![가-힣])("+names.map(escRe).join("|")+")(?="+PARTICLE+"?(?![가-힣]))","g");
  return {map,re};
}
function buildGlossIndex(GLOSSARY){
  const items=GLOSSARY.map(([t,d,scope],i)=>({t,d,scope,i}));
  const terms=items.map(x=>x.t).sort((a,b)=>b.length-a.length);
  const re=new RegExp("(?<![가-힣])("+terms.map(escRe).join("|")+")(?="+PARTICLE+"?(?![가-힣])|하[는며고여]|하던|하신|하라|하면|하였)","g");
  const by=new Map(items.map(x=>[x.t,x]));
  return {re,by};
}
function inScope(item,b){
  if(!item.scope) return true;
  for(let i=0;i<item.scope.length;i+=2) if(b>=item.scope[i]&&b<=item.scope[i+1]) return true;
  return false;
}


/* 받침에 맞춰 조사 고치기 */
const JOSA=[["이","가"],["은","는"],["을","를"],["과","와"],["으로","로"],["이여","여"],["아","야"],["이라","라"],["이요","요"],["이며","며"],["이니","니"],["이나","나"]];
const JOSA_RE="(이여|이라|이요|이며|이니|이나|으로|이|가|은|는|을|를|과|와|로|여|아|야|라|요|며|니|나)?";
const hasB=w=>{const c=w.charCodeAt(w.length-1)-0xAC00;return c>=0&&c<11172&&c%28!==0;};
const endsL=w=>{const c=w.charCodeAt(w.length-1)-0xAC00;return c>=0&&c<11172&&c%28===8;};
function fixJosa(newName,j){ if(!j) return ""; for(const [a,b] of JOSA){ if(j===a||j===b){ if(a==="으로"&&endsL(newName)) return "로"; return hasB(newName)?a:b; } } return j; }
function blankJosa(j){ if(!j) return ""; for(const [a,b] of JOSA){ if(j===a||j===b) return a+"/"+b; } return j; }
function swapName(text,name,newName){ return text.replace(new RegExp("(?<![가-힣])"+escRe(name)+JOSA_RE+"(?![가-힣])","g"),(m,j)=>newName+fixJosa(newName,j)); }
function blankName(text,name){ return text.replace(new RegExp("(?<![가-힣])"+escRe(name)+JOSA_RE+"(?![가-힣])","g"),(m,j)=>"(　　)"+blankJosa(j)); }
const honor=(t,e)=>t.slice(e.idx+e.name.length).startsWith("께");

/* 하루 본문 분석 */
function analyzeDay(chs, BIBLE, EI){
  const verses=[];
  for(const [b,c] of chs) BIBLE[b-1][c-1].forEach((t,i)=>verses.push({b,c,v:i+1,t,ents:[]}));
  const people=new Map(), places=new Map();
  for(const vs of verses){
    EI.re.lastIndex=0; let m;
    while((m=EI.re.exec(vs.t))){
      const e=EI.map.get(m[1]); vs.ents.push({name:m[1],type:e.type,idx:m.index});
      const tgt=e.type==="person"?people:places;
      if(!tgt.has(m[1])) tgt.set(m[1],{name:m[1],n:0,refs:[]});
      const r=tgt.get(m[1]); r.n++; if(r.refs.length<8) r.refs.push([vs.b,vs.c,vs.v]);
    }
  }
  return {verses,people,places,text:verses.map(v=>v.t).join(" ")};
}

/* 난수 */
function rng(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const pick=(r,arr)=>arr[Math.floor(r()*arr.length)];
function shuffle(r,arr){const a=arr.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}

const ALIAS=[["아브람","아브라함"],["사래","사라"],["시몬","베드로"],["사울","바울"]];
const sameish=(a,b)=>a===b||ALIAS.some(g=>g.includes(a)&&g.includes(b));
const FALLBACK_OT=["모세","다윗","아브라함","솔로몬","엘리야","사무엘","여호수아","이삭","요셉","야곱","사울","이사야"];
const FALLBACK_NT=["베드로","요한","야고보","바울","바나바","빌립","도마","마태","안드레","디모데","실라","마리아"];
const FALLBACK_PL=["예루살렘","베들레헴","애굽","바벨론","갈릴리","사마리아","여리고","가버나움","다메섹","니느웨","헤브론","벧엘"];

function chapLabel(b,c){return b===19?`${c}편`:`${c}장`;}
function refStr(PLANINFO,b,c,v){return `${PLANINFO.abbr[b-1]} ${c}:${v}`;}

/* 문장 자르기 */
function snippetAround(t,idx,max){
  if(t.length<=max) return t;
  const words=t.split(" "); let pos=0, wi=0;
  for(;wi<words.length;wi++){ if(pos+words[wi].length>=idx) break; pos+=words[wi].length+1; }
  let s=wi, e=wi+1, len=words[wi].length;
  while(true){
    let grew=false;
    if(e<words.length && len+words[e].length+1<=max){len+=words[e].length+1;e++;grew=true;}
    if(s>0 && len+words[s-1].length+1<=max){s--;len+=words[s].length+1;grew=true;}
    if(!grew) break;
  }
  return (s>0?"… ":"")+words.slice(s,e).join(" ")+(e<words.length?" …":"");
}
function trimTail(q){
  return q.replace(/\s(하니|하시니|하매|하시매|하거늘|하시거늘|하더라|하시더라|하고|하시고|하므로|하시므로|하였더니|하였으나|하는지라|하시는지라)$/,"").trim();
}

/* ── 문제 만들기 ── */
function makeQuiz(day, ctx, seed, opts={}){
  const r=rng(seed), A=day, b0=day.verses[0].b;
  const NT=b0>=40;
  const used=new Set();
  const nOX=opts.nOX??3, nMC=opts.nMC??3;
  const peopleDay=[...A.people.values()].sort((x,y)=>y.n-x.n).map(x=>x.name);
  const placesDay=[...A.places.values()].sort((x,y)=>y.n-x.n).map(x=>x.name);
  const bookPeople=ctx.bookPeople(b0), bookPlaces=ctx.bookPlaces(b0);
  function distract(answer, pool1, pool2, pool3, n=3){
    const out=[];
    for(const pool of [shuffle(r,pool1),shuffle(r,pool2),shuffle(r,pool3)])
      for(const x of pool){ if(out.length>=n) break; if(!sameish(x,answer)&&!out.some(o=>sameish(o,x))) out.push(x); }
    return out.length===n?out:null;
  }
  const C=(b,c)=>chapLabel(b,c);
  const gens={
    speaker(){
      const cands=[];
      const VERB="(이르되|이르시되|대답하되|대답하여 이르되|대답하여 이르시되|말하되|여짜오되|이르기를|대답하기를|가로되)";
      for(const vs of A.verses) for(const e of vs.ents){ if(e.type!=="person") continue;
        const after=vs.t.slice(e.idx+e.name.length);
        const m=after.match(new RegExp("^(이|가|께서|은|는)\\s(?:[^\\s]+\\s){0,3}?"+VERB+"\\s(.+)$"));
        if(!m) continue;
        let q=trimTail(m[3]); if(q.length<10) continue;
        if(q.includes(e.name)) continue;
        if(q.length>70){ q=snippetAround(q,0,66); }
        cands.push({vs,name:e.name,q});
      }
      if(!cands.length) return null;
      const c=pick(r,cands); if(used.has(c.vs)) return null;
      const speakers=[...new Set(cands.map(x=>x.name))];
      const ds=distract(c.name,speakers,peopleDay,bookPeople.concat(NT?FALLBACK_NT:FALLBACK_OT)); if(!ds) return null;
      used.add(c.vs);
      const o=shuffle(r,[c.name,...ds]);
      return {t:"mc",kind:"말한 사람",q:"다음 말을 한 사람은 누구일까요?",quote:c.q,o,a:o.indexOf(c.name),vs:c.vs,
        hint:`${C(c.vs.b,c.vs.c)}의 대화입니다. 이 말을 듣고 있는 사람이 누구였는지, 그 앞뒤 장면을 떠올려 보세요.`};
    },
    personCloze(){
      const cands=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=20&&!vs.t.startsWith("[")&&vs.ents.some(e=>e.type==="person"&&!honor(vs.t,e)&&!vs.ents.some(x=>x.name===e.name&&honor(vs.t,x))));
      if(!cands.length) return null;
      const vs=pick(r,cands); const pe=vs.ents.filter(e=>e.type==="person"&&!vs.ents.some(x=>x.name===e.name&&honor(vs.t,x))); const e=pick(r,pe);
      const sn=snippetAround(vs.t,e.idx,90);
      const blank=blankName(sn,e.name);
      if(!blank.includes("(　　)")) return null;
      const ds=distract(e.name,peopleDay.filter(n=>!vs.ents.some(x=>x.name===n)),bookPeople,NT?FALLBACK_NT:FALLBACK_OT); if(!ds) return null;
      used.add(vs); const o=shuffle(r,[e.name,...ds]);
      return {t:"mc",kind:"인물",q:"빈칸에 들어갈 사람은 누구일까요?",quote:blank,o,a:o.indexOf(e.name),vs,
        hint:`${C(vs.b,vs.c)}에서 이 일이 벌어질 때 곁에 있던 사람들을 떠올려 보세요. 누가 무엇을 했나요?`};
    },
    placeCloze(){
      const cands=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=18&&vs.ents.some(e=>e.type==="place"));
      if(!cands.length) return null;
      const vs=pick(r,cands); const e=pick(r,vs.ents.filter(x=>x.type==="place"));
      const sn=snippetAround(vs.t,e.idx,90); const blank=blankName(sn,e.name);
      if(!blank.includes("(　　)")) return null;
      const ds=distract(e.name,placesDay.filter(n=>!vs.ents.some(x=>x.name===n)),bookPlaces,FALLBACK_PL); if(!ds) return null;
      used.add(vs); const o=shuffle(r,[e.name,...ds]);
      return {t:"mc",kind:"장소",q:"빈칸에 들어갈 곳은 어디일까요?",quote:blank,o,a:o.indexOf(e.name),vs,
        hint:`이 일이 어디서 일어났는지 ${C(vs.b,vs.c)}의 흐름을 떠올려 보세요. 위의 지도에서 오늘 나온 곳들을 다시 살펴봐도 좋습니다.`};
    },
    chapter(){
      const chs=[...new Set(A.verses.map(v=>v.b+"-"+v.c))]; if(chs.length<4) return null;
      const cands=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=25&&vs.t.length<=110&&A.text.split(vs.t.slice(0,18)).length===2);
      if(!cands.length) return null;
      const vs=pick(r,cands); const key=vs.b+"-"+vs.c; const multi=new Set(A.verses.map(v=>v.b)).size>1;
      const others=shuffle(r,chs.filter(k=>k!==key)).slice(0,3);
      const o=shuffle(r,[key,...others]).map(k=>{const [b,c]=k.split("-").map(Number);return {k,label:(multi?ctx.abbr[b-1]+" ":"")+C(b,c)};});
      used.add(vs);
      return {t:"mc",kind:"어디에",q:`다음 말씀은 오늘 본문 몇 ${vs.b===19?"편":"장"}에 있을까요?`,quote:snippetAround(vs.t,0,90),o:o.map(x=>x.label),a:o.findIndex(x=>x.k===key),vs,
        hint:"오늘 요약을 다시 읽어 보세요. 이 말씀의 앞뒤에는 어떤 내용이 있었나요?"};
    },
    phraseMC(){
      const v=splitCands(); if(!v) return null;
      const {vs,first,second,pool}=v;
      const ds=shuffle(r,pool).filter(x=>x!==second&&!A.text.includes(first+" "+x)).slice(0,3); if(ds.length<3) return null;
      used.add(vs); const o=shuffle(r,[second,...ds]);
      return {t:"mc",kind:"말씀 잇기",q:"다음 말씀의 뒷부분으로 알맞은 것은?",quote:first+" …",o,a:o.indexOf(second),vs,
        hint:`앞부분의 뜻과 자연스럽게 이어지는지 생각해 보세요. ${C(vs.b,vs.c)} 근처의 말씀입니다.`};
    },
    nameOX(){
      const cands=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=20&&!vs.t.startsWith("[")&&new Set(vs.ents.filter(e=>e.type==="person").map(e=>e.name)).size===1&&!vs.ents.some(e=>honor(vs.t,e)));
      if(!cands.length) return null;
      const vs=pick(r,cands); const e=vs.ents.find(x=>x.type==="person");
      const sn=snippetAround(vs.t,e.idx,85);
      const truth=r()<0.5;
      let stmt=sn, swapped=null;
      if(!truth){
        if(e.name==="예수") return null;
        const ds=distract(e.name,peopleDay.filter(n=>n!=="예수"),bookPeople.filter(n=>n!=="예수"),NT?FALLBACK_NT:FALLBACK_OT,1); if(!ds) return null;
        swapped=ds[0]; stmt=swapName(sn,e.name,swapped);
        if(A.text.includes(stmt.replace(/^… | …$/g,""))) return null;
      }
      used.add(vs);
      return {t:"ox",kind:"인물 확인",q:"본문의 내용과 맞으면 O, 틀리면 X를 고르세요.",quote:stmt,o:["O","X"],a:truth?0:1,vs,
        hint: truth?`이 문장의 사람과 행동을 ${C(vs.b,vs.c)}에서 다시 떠올려 보세요. 정말 다른 사람이었나요?`
                   :`문장 속 사람 이름을 눈여겨보세요. ${C(vs.b,vs.c)}에서 이 일을 한 사람이 정말 그 사람이었나요?`};
    },
    orderOX(){
      const pool=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=18);
      if(pool.length<10) return null;
      for(let tries=0;tries<20;tries++){
        const x=pick(r,pool), y=pick(r,pool);
        const gx=A.verses.indexOf(x), gy=A.verses.indexOf(y);
        const far=(x.c!==y.c||x.b!==y.b)||Math.abs(gx-gy)>=8;
        if(!far||x===y) continue;
        const [p,q]=gx<gy?[x,y]:[y,x];
        const sp=snippetAround(p.t,0,42), sq=snippetAround(q.t,0,42);
        const truth=r()<0.5;
        used.add(x);used.add(y);
        const [s1,s2]=truth?[sp,sq]:[sq,sp];
        return {t:"ox",kind:"순서",q:"두 장면의 순서가 맞으면 O, 틀리면 X를 고르세요.",quote:`‘${s1}’\n이 장면이 먼저 나오고, 그다음에\n‘${s2}’`,o:["O","X"],a:truth?0:1,vs:p,
          hint:"두 장면이 각각 몇 장쯤에 있었는지 떠올려 보세요. 오늘 요약의 흐름을 따라가 보면 순서가 보입니다."};
      }
      return null;
    },
    phraseOX(){
      const v=splitCands(); if(!v) return null;
      const {vs,first,second,pool}=v; const truth=r()<0.5; let tail=second;
      if(!truth){ const alt=shuffle(r,pool).find(x=>x!==second&&!A.text.includes(first+" "+x)); if(!alt) return null; tail=alt; }
      used.add(vs);
      return {t:"ox",kind:"말씀 확인",q:"본문에 있는 그대로의 말씀이면 O, 뒷부분이 바뀌었으면 X를 고르세요.",quote:first+" "+tail,o:["O","X"],a:truth?0:1,vs,
        hint:truth?"앞부분과 뒷부분의 뜻이 정말 어긋나나요? 문장을 천천히 다시 읽어 보세요.":`앞부분이 말하는 내용과 뒷부분이 같은 이야기인가요? ${C(vs.b,vs.c)} 근처를 떠올려 보세요.`};
    }
  };
  function splitCands(){
    const cands=A.verses.filter(vs=>!used.has(vs)&&vs.t.length>=34&&vs.t.length<=120);
    const parts=[];
    for(const vs of cands){
      const sp=[...vs.t.matchAll(/ /g)].map(m=>m.index); if(!sp.length) continue;
      const mid=vs.t.length*0.55; let best=sp[0]; for(const i of sp) if(Math.abs(i-mid)<Math.abs(best-mid)) best=i;
      const first=vs.t.slice(0,best), second=vs.t.slice(best+1);
      if(second.length<10||second.length>55||first.length<12) continue;
      if(A.text.split(second).length!==2) continue;
      parts.push({vs,first,second});
    }
    if(parts.length<4) return null;
    const c=pick(r,parts);
    const L=c.second.length;
    const pool=parts.filter(p=>p!==c&&p.second.length>=L*0.55&&p.second.length<=L*1.6).map(p=>p.second);
    return pool.length>=3?{...c,pool}:null;
  }
  const out=[];
  const cur=(opts.curated||[]).slice();
  const curMC=cur.filter(q=>q.t==="mc"), curOX=cur.filter(q=>q.t==="ox");
  const mcOrder=shuffle(r,["speaker","speaker","personCloze","placeCloze","chapter"]).concat(["phraseMC","personCloze","placeCloze","chapter","phraseMC","speaker"]);
  const oxOrder=shuffle(r,["nameOX","nameOX","orderOX","phraseOX"]).concat(["orderOX","phraseOX","nameOX","phraseOX","orderOX"]);
  function fill(order,n,base){
    const res=base.slice(0,n);
    for(const g of order){ if(res.length>=n) break; let q=null; for(let k=0;k<3&&!q;k++) q=gens[g](); if(q) res.push(q); }
    return res;
  }
  // 직접 만든 이해 문제가 있으면: 사실 확인(자동) 먼저, 이해 문제는 끝에 차례대로
  if(cur.length){
    const keep=cur.slice(0,4), rest=Math.max(2,nMC+nOX-keep.length);
    const a=fill(mcOrder,Math.ceil(rest/2),[]), b=fill(oxOrder,rest-Math.ceil(rest/2),[]);
    for(let i=0;i<Math.max(a.length,b.length);i++){ if(b[i]) out.push(b[i]); if(a[i]) out.push(a[i]); }
    return out.slice(0,rest).concat(keep);
  }
  const mcs=fill(mcOrder,nMC,shuffle(r,curMC).slice(0,2));
  const oxs=fill(oxOrder,nOX,shuffle(r,curOX).slice(0,2));
  // 모자라면 다른 쪽으로 채우기
  while(mcs.length+oxs.length<nMC+nOX){
    const q=gens.phraseOX()||gens.orderOX()||gens.phraseMC(); if(!q) break; (q.t==="mc"?mcs:oxs).push(q);
  }
  for(let i=0;i<Math.max(mcs.length,oxs.length);i++){ if(oxs[i]) out.push(oxs[i]); if(mcs[i]) out.push(mcs[i]); }
  return out;
}
if(typeof module!=="undefined") module.exports={buildEntityIndex,buildGlossIndex,inScope,analyzeDay,makeQuiz,rng};
