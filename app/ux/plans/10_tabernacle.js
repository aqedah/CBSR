/* ===== 성막을 세우는 날(출 40:17–38) · 이스라엘의 진과 행진(민 2·3·10장) — 2026-11-10 목사님 승인, GPT 검토 반영(9장면·수족 씻음·36–38은 '이후의 여정'·민 2는 따로)
   평면은 대속죄일과 같은 세로 성막(위 서·아래 동). 기구는 처음에 보이지 않다가(data-off) 장면마다 제자리에 나타남. 인용은 개역개정 그대로. */
(function(){
const PL="class=\"pl m\"";
/* 성막 평면 SVG. 기구 요소에 id와 data-off(처음엔 숨김) */
function TAB_SVG(){ return `
    <text class="pl m" x="8" y="14">↑ 서</text><text class="pl m" x="8" y="424">↓ 동</text><text class="pl m" x="292" y="14" text-anchor="end">북 →</text>
    <g class="camp"><rect x="8" y="70" width="7" height="10"/><rect x="10" y="120" width="7" height="10"/><rect x="8" y="170" width="7" height="10"/><rect x="10" y="220" width="7" height="10"/><rect x="8" y="270" width="7" height="10"/>
      <rect x="285" y="70" width="7" height="10"/><rect x="283" y="120" width="7" height="10"/><rect x="285" y="170" width="7" height="10"/><rect x="283" y="220" width="7" height="10"/><rect x="285" y="270" width="7" height="10"/>
      <rect x="100" y="16" width="10" height="7"/><rect x="145" y="14" width="10" height="7"/><rect x="190" y="16" width="10" height="7"/></g>
    <text class="pl m s" x="20" y="320" transform="rotate(-90 20 320)">이스라엘 진영</text>
    <g id="tb_court" data-off="1"><rect class="wall" x="50" y="34" width="200" height="290"/><text ${PL} x="54" y="46">성막 뜰</text></g>
    <g id="tb_gate" data-off="1"><rect x="118" y="320" width="64" height="8" fill="#f3e6c4" stroke="#6b4a24" stroke-width="1.5"/><text ${PL} x="186" y="327">뜰 문</text></g>
    <g id="tb_tent" data-off="1"><rect class="tent" x="102" y="56" width="96" height="150"/><rect class="hh" x="104" y="58" width="92" height="46"/><text class="pl" x="204" y="70">지성소</text><text class="pl" x="204" y="150">성소</text><text ${PL} x="150" y="217" text-anchor="middle">회막 문</text></g>
    <g id="tb_veil" data-off="1"><line class="veil" x1="102" y1="106" x2="198" y2="106"/><text ${PL} x="204" y="110">휘장</text></g>
    <g id="tb_ark" data-off="1"><rect class="obj" x="139" y="72" width="22" height="16" rx="1.5"/><text class="pl m s" x="150" y="68">증거궤 · 속죄소</text></g>
    <g id="tb_table" data-off="1"><rect class="obj" x="174" y="134" width="10" height="18"/><text class="pl m s" x="179" y="164">떡상</text><circle cx="177" cy="140" r="1.6" fill="#f3e6c4"/><circle cx="181" cy="140" r="1.6" fill="#f3e6c4"/><circle cx="177" cy="146" r="1.6" fill="#f3e6c4"/><circle cx="181" cy="146" r="1.6" fill="#f3e6c4"/></g>
    <g id="tb_lamp" data-off="1"><g stroke="#8a6a20" stroke-width="2" fill="none"><line x1="120" y1="138" x2="120" y2="154"/><path d="M113 140 q7 8 14 0"/><path d="M110 138 q10 13 20 0"/></g><text class="pl m s" x="120" y="166">등잔대</text></g>
    <g id="tb_lampfire" data-off="1"><circle cx="110" cy="137" r="1.8" fill="#ffb347"/><circle cx="113" cy="138" r="1.8" fill="#ffb347"/><circle cx="120" cy="136" r="1.8" fill="#ffb347"/><circle cx="127" cy="138" r="1.8" fill="#ffb347"/><circle cx="130" cy="137" r="1.8" fill="#ffb347"/></g>
    <g id="tb_inc" data-off="1"><rect class="obj" x="145" y="114" width="10" height="10"/><text ${PL} x="158" y="122">향단</text></g>
    <g id="tb_door" data-off="1"><line x1="118" y1="206" x2="182" y2="206" stroke="#7a2a5a" stroke-width="3"/></g>
    <g id="tb_laver" data-off="1"><circle class="bronze" cx="150" cy="238" r="8"/><text ${PL} x="161" y="241">물두멍</text></g>
    <g id="tb_altar" data-off="1"><rect class="bronze" x="132" y="258" width="36" height="36"/><text ${PL} x="172" y="290">번제단</text></g>
    <g><path class="dune" d="M40 352 q14 -9 28 0 t28 0"/><path class="dune" d="M180 350 q14 -9 28 0 t28 0 t28 0"/><path class="dune" d="M60 398 q14 -9 28 0 t28 0 t28 0"/><path class="dune" d="M200 404 q14 -9 28 0 t28 0"/></g>`; }
const Q=(v,t)=>({r:[2,40,v],q:t});
planReg({id:"tab",title:"성막을 세우는 날",card:"성막을 세우는 날",sub:"출애굽기 40장 · 모세가 기구를 제자리에",kicker:"출애굽기 40장 · 둘째 해 첫째 달 초하루",here:"성막 평면도 위에서",
 intro:"애굽을 떠난 지 1년, 하나님이 보여 주신 모양대로 성막이 세워집니다. 기구가 하나씩 제자리에 놓일 때마다 본문은 같은 말을 되풀이합니다. \"여호와께서 모세에게 명령하신 대로 되니라.\" 위가 서쪽(지성소), 아래가 동쪽(뜰 문)입니다.",
 open:[[2,40]],svg:TAB_SVG(),actors:{me:{ch:"moses",n:"모세",w:26},aaron:{ch:"aaronhp",n:"아론",w:22,side:-1},p1:{ch:"priest",n:"",w:18},p2:{ch:"priest",n:"",w:18}},
 note:"평면은 출 26–27·40장의 배치를 따른 그림이며 크기 비율은 그림을 위해 조정했습니다",
 scenes:[
  {s:"40:17–19",t:"성막을 세우고 막을 펴다",d:"둘째 해 첫째 달 초하루. 모세가 받침과 널판과 띠와 기둥을 세우고, 그 위에 막을 펴고 덮개를 덮습니다. 본문은 모세를 주어로 쓰지만, 모세 혼자 메어 세운 것이 아니라 모세가 세우는 일을 주관했다는 뜻으로 읽습니다.",
   ...Q(19,"또 성막 위에 막을 펴고 그 위에 덮개를 덮으니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[150,350],[150,224]],show:["tb_tent"],label:[[150,32,"둘째 해 첫째 달 초하루 (40:17)","t"]]},
  {s:"40:20–21",t:"증거궤를 들여놓고 휘장을 늘어뜨리다",d:"증거판을 궤 속에 넣고 채를 꿰고 속죄소를 그 위에 둡니다. 그 궤를 성막 안 가장 깊은 곳에 들여놓고, 가리개 휘장을 늘어뜨려 증거궤를 가립니다.",
   ...Q(21,"또 그 궤를 성막에 들여놓고 가리개 휘장을 늘어뜨려 그 증거궤를 가리니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[150,224],[150,120],[150,98]],show:["tb_ark"],fx:[["wait",900],["show","tb_veil",900],["walk","me",[[150,130]]]]},
  {s:"40:22–25",t:"북쪽에 상, 남쪽에 등잔대",d:"휘장 밖 성소에 상을 북쪽으로 놓고 여호와 앞에 떡을 진설합니다. 상과 마주하도록 남쪽에 등잔대를 놓고 등잔에 불을 켭니다. 이 그림에서 북쪽은 오른쪽, 남쪽은 왼쪽입니다.",
   ...Q(25,"또 여호와 앞에 등잔대에 불을 켜니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[150,130],[160,146]],show:["tb_table"],fx:[["wait",700],["label",179,128,"북쪽 · 떡을 진설","t"],["wait",900],["walk","me",[[136,146]]],["show","tb_lamp",800],["wait",700],["show","tb_lampfire",600],["label",120,128,"남쪽 · 불을 켬","t"]]},
  {s:"40:26–28",t:"휘장 앞의 금 향단, 성막 문의 휘장",d:"휘장 바로 앞에 금 향단을 두고 향기로운 향을 사릅니다. 그런 다음 성막 문에 휘장을 달아 성소를 닫습니다.",
   ...Q(27,"그 위에 향기로운 향을 사르니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[136,146],[150,128]],show:["tb_inc"],fx:[["wait",600],["smoke",150,108,3],["wait",1200],["walk","me",[[150,196],[150,224]]],["show","tb_door",800],["label",212,200,"성막 문 휘장 (40:28)","t","start"]]},
  {s:"40:29",t:"회막 문 앞의 번제단",d:"회막 문 앞에 번제단을 두고 그 위에 번제와 소제를 드립니다. 성소 밖 뜰에서 드리는 첫 제사입니다.",
   ...Q(29,"또 회막의 성막 문 앞에 번제단을 두고 번제와 소제를 그 위에 드리니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[150,224],[150,250]],show:["tb_altar"],fx:[["wait",800],["fire",150,276,6]]},
  {s:"40:30–32",t:"회막과 제단 사이의 물두멍",d:"회막과 제단 사이에 물두멍을 두고 씻을 물을 담습니다. 모세와 아론과 그 아들들이 회막에 들어갈 때와 제단에 가까이 갈 때 거기서 손과 발을 씻습니다. 레위기 8장의 위임식에서 온몸을 씻는 것과는 다른, 날마다 하는 씻음입니다.",
   ...Q(32,"그들이 회막에 들어갈 때와 제단에 가까이 갈 때에 씻었으니 여호와께서 모세에게 명령하신 대로 되니라"),path:[[150,250],[162,240]],show:["tb_laver"],at:[["aaron",128,246],["p1",118,256],["p2",136,258]],fx:[["wait",700],["water",150,238],["label",150,226,"수족을 씻음 (40:31)","t"]]},
  {s:"40:33",t:"뜰에 포장을 치고 뜰 문에 휘장을 달다",d:"성막과 제단 둘레에 뜰의 포장을 치고 뜰 문에 휘장을 답니다. 모세가 이같이 역사를 마칩니다.",
   ...Q(33,"그는 또 성막과 제단 주위 뜰에 포장을 치고 뜰 문에 휘장을 다니라 모세가 이같이 역사를 마치니"),path:[[162,240],[150,300]],gone:["aaron","p1","p2"],show:["tb_court"],fx:[["wait",1000],["show","tb_gate",800]]},
  {s:"40:34–35",t:"구름이 회막에 덮이고 영광이 충만하다",d:"성막이 다 세워지자 구름이 회막에 덮이고 여호와의 영광이 성막에 가득합니다. 모세도 회막에 들어갈 수 없습니다.",
   ...Q(35,"모세가 회막에 들어갈 수 없었으니 이는 구름이 회막 위에 덮이고 여호와의 영광이 성막에 충만함이었으며"),path:[[150,300],[150,224]],fx:[["glow",150,130,70,1800],["cloud",150,120,120,170],["wait",1500],["x",150,236,"들어갈 수 없음"]]},
  {s:"40:36–38",t:"이후의 여정 · 구름이 떠오르면 가고, 머물면 머물다",d:"36–38절은 이날의 일이 아니라, 이후 광야 여정 전체가 어떻게 움직였는지를 설명하는 마침말입니다. 구름이 성막 위에서 떠오르면 백성이 나아가고, 떠오르지 않으면 그날까지 머뭅니다. 낮에는 구름, 밤에는 그 구름 가운데 불이 있습니다.",
   ...Q(38,"낮에는 여호와의 구름이 성막 위에 있고 밤에는 불이 그 구름 가운데에 있음을 이스라엘의 온 족속이 그 모든 행진하는 길에서 그들의 눈으로 보았더라"),path:[[150,224],[150,340]],hold:12000,
   fx:async c=>{ const {FX,mk,sleep,my,tok,svg}=c; FX.label(150,32,"이후의 여정 (40:36–38)","t"); const cl=FX.cloud(150,120,120,170); const gl=FX.glow(150,130,70,900);
     await sleep(1400); if(my!==tok()) return false; cl.animate([{transform:"translateY(0)"},{transform:"translateY(-70px)"}],{duration:1600,fill:"forwards"}); gl.animate([{opacity:1},{opacity:0}],{duration:900,fill:"forwards"});
     FX.label(230,60,"구름이 떠오르면 → 나아감","t","start"); const camp=svg.querySelectorAll("#pl_base .camp rect"); camp.forEach(r=>r.animate([{transform:"translateY(0)"},{transform:"translateY(-26px)"}],{duration:1800,delay:400,fill:"forwards"}));
     await sleep(2800); if(my!==tok()) return false; cl.animate([{transform:"translateY(-70px)"},{transform:"translateY(0)"}],{duration:1600,fill:"forwards"}); FX.label(230,330,"떠오르지 않으면 → 머묾","t","start"); camp.forEach(r=>r.animate([{transform:"translateY(-26px)"},{transform:"translateY(0)"}],{duration:1600,fill:"forwards"}));
     await sleep(2400); if(my!==tok()) return false; c.el.querySelector("#pl_night").setAttribute("opacity",.45); const f=mk("circle",{cx:150,cy:120,r:14,fill:"#ffb347",opacity:0,filter:"url(#pl_blur)"}); f.animate([{opacity:0},{opacity:.95}],{duration:1200,fill:"forwards"}); FX.label(230,120,"밤에는 구름 가운데 불","t","start"); return true; }}
 ],end:"말씀대로 세워진 성막에 하나님의 영광이 가득합니다. 레위기는 이 성막 문 앞에서 시작됩니다(레 1:1)."});

/* ===== 이스라엘의 진과 행진(민 2·3·10장): 같은 성막을 멀리서 본 그림. 위 서 · 아래 동 · 오른쪽 북 · 왼쪽 남 ===== */
function CAMP_SVG(){ const T=(id,x,y,w,h,n,num,rot)=>{ const cx=x+w/2, cy=y+h/2, tr=rot?` transform="rotate(${rot} ${cx} ${cy})"`:""; return `<g id="${id}" data-off="1"><rect class="tribe" x="${x}" y="${y}" width="${w}" height="${h}"/><text class="pl" x="${cx}" y="${cy-1}" text-anchor="middle" style="font-size:9px"${tr}>${n}</text>${num?`<text class="pl m" x="${cx}" y="${cy+10}" text-anchor="middle" style="font-size:7px"${tr}>${num}</text>`:""}</g>`; };
  return `
    <text class="pl m" x="8" y="14">↑ 서</text><text class="pl m" x="8" y="424">↓ 동 (해 돋는 쪽)</text><text class="pl m" x="292" y="14" text-anchor="end">북 →</text><text class="pl m" x="8" y="222">← 남</text>
    <g id="cp_tab"><rect class="tent" x="128" y="186" width="44" height="60"/><rect class="hh" x="130" y="188" width="40" height="18"/><rect class="wall" x="112" y="176" width="76" height="80"/><text class="pl m s" x="150" y="172">회막</text><rect x="146" y="256" width="8" height="3" fill="#f3e6c4" stroke="#6b4a24" stroke-width="1"/></g>
    ${T("cp_lv_w",104,146,92,20,"게르손 종족","서쪽 · 성막 뒤 (민 3:23)")}${T("cp_lv_s",64,176,42,80,"고핫","남쪽 (3:29)",-90)}${T("cp_lv_n",194,176,42,80,"므라리","북쪽 (3:35)",90)}${T("cp_lv_e",104,262,92,20,"모세 · 아론과 아들들","동 · 회막 앞 (3:38)")}
    ${T("cp_e",70,300,160,60,"유다 진영 · 유다 잇사갈 스불론","동쪽 · 186,400명 · 제일대 (2:3–9)")}
    ${T("cp_s",8,120,50,190,"르우벤 진영 · 르우벤 시므온 갓","남쪽 · 151,450명 · 제이대 (2:10–16)",-90)}
    ${T("cp_w",70,70,160,60,"에브라임 진영 · 에브라임 므낫세 베냐민","서쪽 · 108,100명 · 제삼대 (2:18–24)")}
    ${T("cp_n",242,120,50,190,"단 진영 · 단 아셀 납달리","북쪽 · 157,600명 · 후대 (2:25–31)",90)}
    <g id="cp_cloud" data-off="1"><g filter="url(#pl_blur6)" opacity=".92"><circle cx="150" cy="200" r="22" fill="#fff"/><circle cx="135" cy="208" r="18" fill="#fff"/><circle cx="166" cy="206" r="18" fill="#fff"/></g></g>
    <g id="cp_road" data-off="1"><path class="road" d="M150 400 L150 420"/><text class="pl m" x="150" y="428" text-anchor="middle">행진하는 길 (민 10장)</text></g>`; }
planReg({id:"camp",title:"이스라엘의 진과 행진",card:"이스라엘의 진과 행진",sub:"민수기 2·3·10장 · 회막을 가운데 두고",kicker:"민수기 2장 · 회막을 향하여 사방으로",here:"진 배치 그림 위에서",
 intro:"시내 광야에서 하나님이 진 치는 자리와 행진하는 차례를 정해 주십니다. 회막이 한가운데, 레위인이 그 둘레에, 열두 지파가 사방에 섭니다. 위가 서쪽, 아래가 동쪽(해 돋는 쪽)입니다.",
 open:[[4,2],[4,3],[4,10]],svg:CAMP_SVG(),actors:{me:{ch:"moses",n:"모세",w:22,trail:false}},note:"진의 크기와 간격은 그림을 위한 것이며 본문은 방향과 차례만 말합니다",
 scenes:[
  {s:"2:1–2",t:"회막을 향하여 사방으로",d:"하나님이 모세와 아론에게 진 치는 법을 말씀하십니다. 각 지파는 자기 군기와 가문의 기호 곁에, 회막을 향하여 사방으로 진을 칩니다.",god:true,r:[4,2,2],q:"이스라엘 자손은 각각 자기의 진영의 군기와 자기의 조상의 가문의 기호 곁에 진을 치되 회막을 향하여 사방으로 치라",at:[["me",150,268]]},
  {s:"2:3–9",t:"동쪽 · 유다 진영",d:"해 돋는 동쪽에 유다·잇사갈·스불론, 모두 186,400명. 행진할 때 제일대로 앞서 갑니다.",r:[4,2,9],q:"유다 진영에 속한 군대로 계수된 군인의 총계는 십팔만 육천사백 명이라 그들은 제일대로 행진할지니라",show:["cp_e"]},
  {s:"2:10–16",t:"남쪽 · 르우벤 진영",d:"남쪽에 르우벤·시므온·갓, 151,450명. 제이대로 행진합니다. 이 그림에서 남쪽은 왼쪽입니다.",r:[4,2,16],q:"르우벤 진영에 속하여 계수된 군인의 총계는 십오만 천사백오십 명이라 그들은 제이대로 행진할지니라",show:["cp_s"]},
  {s:"2:17 · 3:23–38",chs:[[4,3]],t:"가운데 · 회막과 레위인의 진영",d:"회막은 레위인의 진영과 함께 모든 진영의 중앙에 있습니다. 게르손 종족은 성막 뒤 서쪽에, 고핫은 남쪽에, 므라리는 북쪽에, 모세와 아론과 그 아들들은 회막 앞 동쪽에 진을 칩니다(민 3장).",r:[4,2,17],q:"그 다음에 회막이 레위인의 진영과 함께 모든 진영의 중앙에 있어 행진하되 그들의 진 친 순서대로 각 사람은 자기의 위치에서 자기들의 기를 따라 앞으로 행진할지니라",show:["cp_lv_w","cp_lv_s","cp_lv_n","cp_lv_e"]},
  {s:"2:18–24",t:"서쪽 · 에브라임 진영",d:"서쪽에 에브라임·므낫세·베냐민, 108,100명. 제삼대로 행진합니다.",r:[4,2,24],q:"에브라임 진영에 속하여 계수된 군인의 총계는 십만 팔천백 명이라 그들은 제삼대로 행진할지니라",show:["cp_w"]},
  {s:"2:25–34",t:"북쪽 · 단 진영, 그리고 모두 603,550명",d:"북쪽에 단·아셀·납달리, 157,600명. 맨 뒤 후대로 행진합니다. 계수된 군인은 모두 603,550명이고, 이스라엘은 명령하신 대로 진을 치고 행진합니다.",r:[4,2,34],q:"이스라엘 자손이 여호와께서 모세에게 명령하신 대로 다 준행하여 각기 종족과 조상의 가문에 따르며 자기들의 기를 따라 진 치기도 하며 행진하기도 하였더라",show:["cp_n"],label:[[150,56,"모두 603,550명 (2:32)","t"]]},
  {s:"10:11–13",t:"둘째 해 둘째 달 스무날 · 구름이 떠오르다",d:"성막을 세운 지 50일 가량 뒤, 구름이 증거의 성막에서 떠오릅니다. 이스라엘이 시내 광야를 떠나 행진을 시작합니다. 이 장면부터는 날이 바뀐 다른 사건입니다.",r:[4,10,11],q:"둘째 해 둘째 달 스무날에 구름이 증거의 성막에서 떠오르매",show:["cp_cloud","cp_road"],fx:[["wait",800],async c=>{ const g=c.el.querySelector("#cp_cloud"); g.animate([{transform:"translateY(0)"},{transform:"translateY(-40px)"}],{duration:1800,fill:"forwards"}); return true; }]},
  {s:"10:14–28",t:"행진하는 차례",d:"선두는 유다 진영. 성막을 걷어 게르손과 므라리 자손이 메고 가고, 다음은 르우벤 진영. 고핫인이 성물을 메고 가는데, 그들이 이르기 전에 성막이 먼저 세워집니다. 다음은 에브라임 진영, 맨 뒤는 단 진영입니다.",r:[4,10,28],q:"이스라엘 자손이 행진할 때에 이와 같이 그들의 군대를 따라 나아갔더라",hold:13000,
   fx:async c=>{ const {el,sleep,my,tok,FX}=c; const order=[["cp_e","1 유다 진영 (10:14)"],["cp_lv_w","2 게르손·므라리 — 성막을 메고 (10:17)"],["cp_lv_n",""],["cp_s","3 르우벤 진영 (10:18)"],["cp_lv_s","4 고핫 — 성물을 메고 (10:21)"],["cp_w","5 에브라임 진영 (10:22)"],["cp_n","6 단 진영 · 마지막 (10:25)"]]; let k=0;
     for(const [id,lab] of order){ if(my!==tok()) return false; const g=el.querySelector("#"+id); if(!g) continue; g.animate([{transform:"translateY(0)",opacity:1},{transform:"translateY(90px)",opacity:.15}],{duration:1500,fill:"forwards"}); if(lab){ FX.label(150,k%2?404:392,lab,"t"); k++; } await sleep(1500); }
     return true; }},
  {s:"10:33–36",t:"궤가 앞서 가며 쉴 곳을 찾다",d:"여호와의 산을 떠나 사흘 길을 갈 때, 여호와의 언약궤가 앞서 가며 쉴 곳을 찾습니다. 궤가 떠날 때와 쉴 때 모세가 기도합니다.",r:[4,10,35],sayer:"모세",say:"여호와여 일어나사 주의 대적들을 흩으시고 주를 미워하는 자가 주 앞에서 도망하게 하소서",part:"mid",fx:[["label",150,56,"궤가 쉴 때: 여호와여 이스라엘 종족들에게로 돌아오소서 (10:36)","t"]]}
 ],end:"진을 치는 자리도, 떠나는 차례도 하나님이 정하셨습니다. 민수기의 광야 길은 이 질서 안에서 시작됩니다."});
})();
