/* ===== 여리고 성 돌기(수 6장) — 2026-11-10, GPT 검토 반영(8장면·침묵과 외침의 대비·6:17–19 경고·라합/소각/맹세 구분·개념 평면)
   성은 둥근 담 하나로 된 개념도(발굴 평면이 아님). 행렬 차례(6:8–9): 무장한 자 → 나팔 부는 제사장 일곱 → 언약궤 → 후군. */
(function(){
const CX=150, CY=186, R=78, CAMP=[150,372];
const ring=(n,a0,a1)=>Array.from({length:n+1},(_,i)=>{ const a=a0+(a1-a0)*i/n; return [+(CX+R*Math.cos(a)).toFixed(1),+(CY+R*Math.sin(a)).toFixed(1)]; });
const DEG=d=>d*Math.PI/180, START=DEG(100); /* 남쪽(진영 쪽)에서 시작해 반시계 */
const lap=(off,laps)=>ring(Math.round(28*(laps||1)),START-off,START-off-DEG(360*(laps||1)));
const OFF={s:0,p:DEG(13),k:DEG(24),r:DEG(35)};
const ARK=`<rect x="-9" y="-9" width="18" height="10" rx="1.5" fill="#c9a24a" stroke="#5a3c1c" stroke-width="1.2"/><path d="M-5 -9 q5 -6 10 0" fill="none" stroke="#8a6a20" stroke-width="1.5"/><line x1="-13" y1="-3" x2="13" y2="-3" stroke="#5a3c1c" stroke-width="1.4"/>`;
function JER_SVG(){ return `
    <text class="pl m" x="8" y="14">↑ 북</text>
    <g><path class="dune" d="M20 410 q14 -9 28 0 t28 0"/><path class="dune" d="M230 404 q14 -9 28 0 t28 0"/></g>
    <path class="valley" d="M262 10 C258 120 266 260 258 420" style="opacity:.5"/><text class="pl m pk-r" x="270" y="220" style="font-size:8px">요단</text>
    <g id="jc_wall"><circle cx="${CX}" cy="${CY}" r="${R-10}" fill="rgba(160,120,60,.12)" stroke="#6b4a24" stroke-width="5"/><rect x="${CX-5}" y="${CY+R-16}" width="10" height="7" fill="#f3e6c4" stroke="#6b4a24" stroke-width="1.4"/><text class="pl m" x="${CX}" y="${CY+R-20}" text-anchor="middle" style="font-size:7.5px">성문 · 굳게 닫힘</text></g>
    <g id="jc_ruin" data-off="1"><circle cx="${CX}" cy="${CY}" r="${R-10}" fill="rgba(160,120,60,.12)" stroke="#a78452" stroke-width="2.4" stroke-dasharray="6 7"/>${Array.from({length:14},(_,i)=>{ const a=DEG(i*26); return `<rect x="${(CX+(R-10)*Math.cos(a)-3).toFixed(1)}" y="${(CY+(R-10)*Math.sin(a)+2).toFixed(1)}" width="6" height="4" fill="#8a6a40" transform="rotate(${i*31} ${(CX+(R-10)*Math.cos(a)).toFixed(1)} ${(CY+(R-10)*Math.sin(a)+4).toFixed(1)})"/>`; }).join("")}</g>
    <text class="pl big s" x="${CX}" y="${CY-6}">여리고</text><text class="pl m" x="${CX}" y="${CY+8}" text-anchor="middle" style="font-size:7.5px">개념도 · 실제 모양이 아닙니다</text>
    <g id="jc_rahab"><rect x="${CX+R-16}" y="${CY-36}" width="9" height="9" fill="#f3e6c4" stroke="#8f1d0f" stroke-width="1.4"/><text class="pl m" x="${CX+R-2}" y="${CY-30}" style="font-size:7.5px">라합의 집 · 성벽 위 (2:15)</text></g>
    <g><rect class="tribe" x="96" y="352" width="108" height="42"/><text class="pl" x="150" y="378" text-anchor="middle" style="font-size:9px">이스라엘 진영 · 길갈</text></g>
    <g id="jc_fire" data-off="1">${[[-30,-20],[20,-34],[36,16],[-18,30],[0,0],[-40,10],[28,-6]].map(([a,b])=>`<text x="${CX+a-6}" y="${CY+b+6}" style="font-size:13px">🔥</text>`).join("")}</g>`; }
const R6=v=>[6,6,v];
planReg({id:"jericho",title:"여리고 성 돌기",card:"여리고 성 돌기",sub:"여호수아 6장 · 엿새 한 바퀴, 이레째 일곱 바퀴",kicker:"여호수아 6장 · 약속의 땅에서 첫 싸움",here:"여리고 성 둘레 개념도 위에서",
 intro:"요단을 건넌 이스라엘 앞에 여리고가 굳게 닫혀 있습니다. 하나님이 정해 주신 방식은 싸움이 아니라 행진입니다. 무장한 자, 나팔 부는 제사장 일곱, 언약궤, 후군이 차례로 성을 돕니다. 백성은 명령이 있기까지 아무 소리도 내지 않습니다.",
 note:"성의 모양은 개념도입니다. 행렬의 차례만 본문(6:8–9)을 따릅니다",open:[[6,6]],svg:JER_SVG(),
 actors:{s:{ch:"soldier",n:"무장한 자",w:19,side:1,trail:false},p:{ch:"priest",n:"제사장 일곱 · 나팔",w:19,side:1,trail:false},k:{svg:ARK,n:"언약궤",w:18,side:1,fs:8,trail:false},r:{ch:"man",n:"후군",w:17,side:1,trail:false},j:{ch:"joshua",n:"여호수아",w:22,side:-1,trail:false},y1:{ch:"youth",n:"정탐꾼 둘",w:17,side:1,trail:false},y2:{ch:"youth",n:"",w:17,trail:false},rh:{ch:"woman",n:"라합의 가족",w:17,side:1,trail:false}},
 scenes:[
  {s:"6:1",t:"굳게 닫힌 여리고",d:"이스라엘 자손 때문에 여리고는 굳게 닫히고, 드나드는 사람이 없습니다.",r:R6(1),q:"이스라엘 자손들로 말미암아 여리고는 굳게 닫혔고 출입하는 자가 없더라",at:[["j",122,348],["s",150,340],["p",168,348],["k",184,344],["r",200,350]]},
  {s:"6:2–5",t:"여호와의 말씀 · 엿새 한 바퀴, 일곱째 날 일곱 바퀴",d:"하나님이 여호수아에게 여리고를 넘겨 주셨다고 하시며 방법을 일러 주십니다. 군사는 날마다 한 번씩 엿새를 돌고, 제사장 일곱은 양각 나팔을 들고 궤 앞에서 갑니다. 일곱째 날에는 일곱 번 돌고, 나팔 소리가 길게 들릴 때 백성이 외치면 성벽이 무너집니다.",god:true,r:R6(5),q:"제사장들이 양각 나팔을 길게 불어 그 나팔 소리가 너희에게 들릴 때에는 백성은 다 큰 소리로 외쳐 부를 것이라 그리하면 그 성벽이 무너져 내리리니 백성은 각기 앞으로 올라갈지니라",part:"post",pray:true,who:"j",fx:[["glow",122,310,26,1200]]},
  {s:"6:6–11",t:"첫째 날 · 행렬의 차례, 그리고 침묵",d:"무장한 자들이 앞서고, 제사장 일곱이 나팔을 불며 가고, 여호와의 언약궤가 뒤따르고, 후군이 궤 뒤를 따릅니다. 여호수아는 백성에게 외치지 말고 아무 말도 내지 말라고 명령합니다. 들리는 것은 나팔 소리뿐입니다. 한 바퀴를 돌고 진영으로 돌아와 잡니다.",r:R6(10),sayer:"여호수아",say:"너희는 외치지 말며 너희 음성을 들리게 하지 말며 너희 입에서 아무 말도 내지 말라 그리하다가 내가 너희에게 명령하여 외치라 하는 날에 외칠지니라",part:"mid",hold:13000,spd:3,
   moves:{s:[[CX+R*Math.cos(START),CY+R*Math.sin(START)],...lap(OFF.s).slice(1),[150,340]],p:[[CX+R*Math.cos(START-OFF.p),CY+R*Math.sin(START-OFF.p)],...lap(OFF.p).slice(1),[168,348]],k:[[CX+R*Math.cos(START-OFF.k),CY+R*Math.sin(START-OFF.k)],...lap(OFF.k).slice(1),[184,344]],r:[[CX+R*Math.cos(START-OFF.r),CY+R*Math.sin(START-OFF.r)],...lap(OFF.r).slice(1),[200,350]]},
   fx:[["label",150,330,"🤫 외치지 말라 · 나팔 소리만","t"]]},
  {s:"6:12–14",t:"엿새 동안 날마다 한 바퀴",d:"둘째 날에도 성을 한 번 돌고 진영으로 돌아옵니다. 엿새 동안 이같이 합니다. 여리고 사람들은 성 안에서 날마다 같은 행렬을 봅니다.",r:R6(14),q:"그 둘째 날에도 그 성을 한 번 돌고 진영으로 돌아오니라 엿새 동안을 이같이 행하니라",hold:12000,
   fx:async c=>{ const {walk,FX,my,tok,sleep}=c; const days=["둘째 날","셋째 날","넷째 날","다섯째 날","여섯째 날"]; for(let d=0;d<5;d++){ if(my!==tok()) return false; FX.label(150,330,days[d]+" · 한 바퀴","t"); const rs=await Promise.all(["s","p","k","r"].map(k=>walk(k,[[CX+R*Math.cos(START-OFF[k]),CY+R*Math.sin(START-OFF[k])],...lap(OFF[k]).slice(1)],my,9))); if(rs.some(x=>!x)) return false; await sleep(250); } return await Promise.all([walk("s",[[150,340]],my,6),walk("p",[[168,348]],my,6),walk("k",[[184,344]],my,6),walk("r",[[200,350]],my,6)]).then(rs=>!rs.some(x=>!x)); }},
  {s:"6:15",t:"일곱째 날 새벽 · 일곱 바퀴",d:"일곱째 날 새벽에 일찍 일어나 전과 같은 방식으로 성을 일곱 번 돕니다. 일곱 번 돌기는 이날뿐입니다. 아직 아무도 외치지 않습니다.",r:R6(15),q:"일곱째 날 새벽에 그들이 일찍이 일어나서 전과 같은 방식으로 그 성을 일곱 번 도니 그 성을 일곱 번 돌기는 그 날뿐이었더라",hold:14000,
   fx:async c=>{ const {walk,FX,my,tok,sleep}=c; for(let d=1;d<=7;d++){ if(my!==tok()) return false; FX.label(150,330,`일곱째 날 · ${d}바퀴째`,"t"); const rs=await Promise.all(["s","p","k","r"].map(k=>walk(k,[[CX+R*Math.cos(START-OFF[k]),CY+R*Math.sin(START-OFF[k])],...lap(OFF[k]).slice(1)],my,11))); if(rs.some(x=>!x)) return false; await sleep(120); } return true; }},
  {s:"6:16–19",t:"외치라 · 그러나 바친 물건에는 손대지 말라",d:"일곱 번째에 제사장들이 나팔을 불 때 여호수아가 말합니다. \"외치라.\" 성과 그 안의 모든 것은 여호와께 온전히 바치되, 라합과 그 집 사람들은 살려 줍니다. 바친 물건을 취하면 이스라엘 진영이 고통을 당합니다 — 7장의 아간 사건이 여기에 걸려 있습니다.",r:R6(16),sayer:"여호수아",say:"외치라 여호와께서 너희에게 이 성을 주셨느니라",part:"pre",who:"j",path:[[122,348],[122,300]],fx:[["wait",2200],["label",150,330,"바친 물건에 손대지 말라 (6:18) → 7장 아간","t"]]},
  {s:"6:20",t:"백성이 외치매 성벽이 무너지다",d:"백성이 외치고 제사장들이 나팔을 붑니다. 백성이 나팔 소리를 듣고 크게 소리 질러 외치니 성벽이 무너져 내리고, 백성이 각기 앞으로 나아가 성을 점령합니다. 엿새의 침묵 뒤에 나온 단 한 번의 외침입니다.",r:R6(20),q:"이에 백성은 외치고 제사장들은 나팔을 불매 백성이 나팔 소리를 들을 때에 크게 소리 질러 외치니 성벽이 무너져 내린지라 백성이 각기 앞으로 나아가 그 성에 들어가서 그 성을 점령하고",
   fx:[["sound",CX,CY+R+10,6],["emo",CX-40,CY+R+30,"📣",3000],["emo",CX+40,CY+R+30,"📯",3000],["wait",1400],["quake"],["hide","jc_wall",900],["hide","jc_rahab",900],["show","jc_ruin",900],["wait",900],["walk","s",[[CX,CY+30]],5]]},
  {s:"6:22–26",t:"라합의 가족을 이끌어 내고 · 성을 불사르고 · 맹세하다",d:"세 가지 일이 차례로 있습니다. 정탐했던 두 젊은이가 라합의 집에 들어가 라합과 부모와 형제와 친족을 이끌어 내어 진영 밖에 둡니다(22–23, 25). 무리가 성과 그 안의 모든 것을 불사르고 은금과 동철 기구는 여호와의 집 곳간에 둡니다(24). 여호수아가 여리고를 다시 세우는 자에게 저주를 맹세하게 합니다(26).",r:R6(25),q:"여호수아가 기생 라합과 그의 아버지의 가족과 그에게 속한 모든 것을 살렸으므로 그가 오늘까지 이스라엘 중에 거주하였으니 이는 여호수아가 여리고를 정탐하려고 보낸 사자들을 숨겼음이었더라",hold:15000,
   fx:async c=>{ const {walk,FX,my,tok,sleep,setAt,vis}=c; const H=[CX+R-12,CY-26]; setAt("y1",150,330); setAt("y2",164,336); FX.label(150,330,"① 라합의 가족을 이끌어 냄 (6:22–23)","t"); FX.label(H[0]+2,H[1]-14,"라합의 집 (6:22)","t","start"); const r1=await Promise.all([walk("y1",[[H[0]-8,H[1]+8]],my,4),walk("y2",[[H[0]+4,H[1]+12]],my,4)]); if(r1.some(x=>!x)) return false; await sleep(600); setAt("rh",H[0]-2,H[1]+10);
     const r2=await Promise.all([walk("y1",[[236,330]],my,4),walk("y2",[[248,336]],my,4),walk("rh",[[242,322]],my,4)]); if(r2.some(x=>!x)) return false; FX.label(246,352,"진영 밖에 둠","t"); await sleep(1200); if(my!==tok()) return false;
     FX.label(150,330,"② 성을 불사름 (6:24)","t"); vis("jc_fire",true,900); FX.fire(CX,CY+10,10); await sleep(2600); if(my!==tok()) return false;
     FX.label(150,330,"③ 여리고를 다시 세우는 자는 저주 (6:26)","t"); return true; }}
 ],end:"엿새의 침묵과 한 번의 외침. 여리고는 이스라엘의 힘이 아니라 여호와께서 주신 성이었습니다(6:16). 다음 장의 아간 사건은 6:18의 경고에서 시작됩니다."});
})();
