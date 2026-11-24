/* 성경 서고 — 2026-11-24 목사님: 진입 경로를 넣고 앱에서 서고를 볼 수 있게.
   서고는 세 부분(구약 · 신약 · 외경과 위경과 교부 문헌). 구약과 신약은 그 안에서 서가로 나누어 들어감. 셋째 부분은 지금은 경고문만.
   서고 → (구약|신약) 서가 고르기 → 서가(책등) → 책 펼침 → 책(표지 · 대표 구절 · 배경 · 목적 · 구조 · 하나님 · 연결 · 읽기 · 맺음)
   원고는 shelf_66.json(성경책장 작업대의 내보내기 꼴). 그림은 img/shelf/. 앱에서는 필요할 때만 불러옴(template3.html의 shelfOpen). */
(function(){
"use strict";
var ART={"labels":{"tor":{"창세기":[49,110,196,13.0,30,63],"출애굽기":[108,110,196,13.0,30,80],"레위기":[167,128,178,13.0,30,63],"민수기":[226,116,190,13.0,30,63],"신명기":[285,118,188,13.0,30,63]},"his":{"여호수아":[49,132,174,13.0,30,80],"사사기":[108,137,169,13.0,30,63],"룻기":[167,160,146,13.0,30,46],"사무엘상":[226,123,183,13.0,30,80],"사무엘하":[285,132,174,13.0,30,80],"열왕기상":[49,369,171,13.0,30,80],"열왕기하":[108,365,175,13.0,30,80],"역대상":[167,359,181,13.0,30,63],"역대하":[226,350,190,13.0,30,63],"에스라":[74,620,154,13.0,30,63],"느헤미야":[133,616,158,13.0,30,80],"에스더":[192,620,154,13.0,30,63]},"poe":{"욥기":[49,110,196,13.0,30,46],"시편":[108,110,196,13.0,30,46],"잠언":[167,123,183,13.0,30,46],"전도서":[226,149,157,13.0,30,63],"아가":[285,155,151,13.0,30,46]},"pro":{"이사야":[43,110,196,9.0,30,63],"예레미야":[94,110,196,9.0,30,80],"예레미야애가":[145,159,147,3.0,42,97],"에스겔":[196,110,196,9.0,30,63],"다니엘":[247,149,157,9.0,30,63],"호세아":[298,146,160,9.0,30,63],"요엘":[43,396,144,9.0,30,46],"아모스":[94,387,153,9.0,30,63],"오바댜":[145,399,141,9.0,30,63],"요나":[196,394,146,9.0,30,46],"미가":[247,390,150,9.0,30,46],"나훔":[298,396,144,9.0,30,46],"하박국":[69,630,144,9.0,30,63],"스바냐":[120,630,144,9.0,30,63],"학개":[171,631,143,9.0,30,46],"스가랴":[222,614,160,9.0,30,63],"말라기":[273,628,146,9.0,30,63]},"gos":{"마태복음":[78,127,179,13.0,30,80],"마가복음":[137,144,162,13.0,30,80],"누가복음":[196,132,174,13.0,30,80],"요한복음":[255,137,169,13.0,30,80]},"pau":{"로마서":[49,106,200,13.0,30,63],"고린도전서":[108,106,200,13.0,30,97],"고린도후서":[167,119,187,13.0,30,97],"갈라디아서":[226,150,156,13.0,30,97],"에베소서":[285,150,156,13.0,30,80],"빌립보서":[44,392,148,13.0,30,80],"골로새서":[103,392,148,13.0,30,80],"데살로니가전서":[162,388,152,7.0,42,97],"데살로니가후서":[221,397,143,7.0,42,97],"디모데전서":[44,618,156,13.0,30,97],"디모데후서":[103,626,148,13.0,30,97],"디도서":[162,631,143,13.0,30,63],"빌레몬서":[221,640,134,13.0,30,80]},"gen":{"히브리서":[78,148,158,13.0,30,80],"야고보서":[137,159,147,13.0,30,80],"베드로전서":[196,159,147,13.0,30,97],"베드로후서":[255,162,144,13.0,30,97],"요한일서":[49,393,147,13.0,30,80],"요한이서":[108,399,141,13.0,30,80],"요한삼서":[167,399,141,13.0,30,80],"유다서":[226,399,141,13.0,30,63]}},"hall":{"cases":{"rev":[156,192,234,321],"pau":[74,239,165,380],"gen":[225,239,316,380],"gos":[55,302,161,457],"act":[229,302,335,457],"poe":[29,390,156,559],"pro":[234,390,361,559],"tor":[-8,512,148,696],"his":[242,512,398,696]},"lanterns":[[178,267,51.8],[212,267,51.8],[176,334,59.9],[214,334,59.9],[172,426,71.0],[218,426,71.0],[167,554,86.5],[223,554,86.5]]}};
var IMG="img/shelf/", W=390, H=846;
var SEC={ot:{n:"구약",c:"서른아홉 권",g:["모세오경","역사서","시가서","선지서"]},nt:{n:"신약",c:"스물일곱 권",g:["복음서","사도행전","바울서신","일반서신","요한계시록"]}};
var PRESS={"모세오경":"tor","역사서":"his","시가서":"poe","선지서":"pro","복음서":"gos","바울서신":"pau","일반서신":"gen"};
var CNT=["","한 권","두 권","세 권","네 권","다섯 권","여섯 권","일곱 권","여덟 권","아홉 권","열 권","열한 권","열두 권","열세 권","열네 권","열다섯 권","열여섯 권","열일곱 권"];
/* 셋째 부분(외경 · 위경 · 교부 문헌): 어둡고, 이름패는 불에 그을려 잘 읽히지 않음. 누르면 경고장부터(11-24 목사님의 글). 책은 아직 없음 */
var WARN={t:"경고",a:"이 서고의 책은 성경이 아닙니다.",q:"정말로 열람하시겠습니까?",e:"아직 들여놓은 책이 없습니다."};
var root=null,stage=null,O={},DATA=null,LOAD=null,levels=[],busy=false;
var CL='<svg class="ch" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="m15 5-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>', CR='<svg class="ch" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
var CSS=`
#cbsrShelf{position:fixed;inset:0;z-index:99000;overscroll-behavior:contain;background:#17100b;overflow:hidden;touch-action:manipulation;-webkit-tap-highlight-color:transparent;font-family:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;color:#33231a}
#cbsrShelf:before{content:"";position:absolute;inset:-40px;background:url(img/shelf/hall.webp) center/cover;filter:blur(16px) brightness(.4)}
#cbsrShelf *{box-sizing:border-box}
html.shelf-on .coach{display:none!important}
#cbsrShelf:focus{outline:none}
#cbsrShelf .st{position:absolute;left:50%;top:50%;width:390px;height:846px;transform-origin:50% 50%;overflow:hidden;background:#2a1d14;word-break:keep-all}
#cbsrShelf .sf{font-family:"Gowun Batang","Noto Serif KR",serif}
#cbsrShelf button{font:inherit;color:inherit;cursor:pointer;border-radius:0;margin:0;-webkit-appearance:none;appearance:none}
#cbsrShelf .ch{display:block;flex:none}
#cbsrShelf .scn{position:absolute;left:0;top:0;width:390px;height:846px;transform-origin:50% 0}
#cbsrShelf .bdp{position:absolute;inset:-24px;background:url(img/shelf/hall.webp) 50% 40%/cover;filter:blur(7px) brightness(.5)}
#cbsrShelf .lay{position:absolute;inset:0}
#cbsrShelf .wk{position:absolute;inset:0}
#cbsrShelf .wk.go{animation:cbsrWalk 1.5s ease-in-out 1}
#cbsrShelf .hl{position:absolute;inset:0;transition:transform 1.5s cubic-bezier(.45,.05,.25,1),transform-origin 1.5s cubic-bezier(.45,.05,.25,1);transform-origin:50% 60%}
#cbsrShelf .hl img,#cbsrShelf .full{position:absolute;left:0;top:0;width:390px;height:846px;display:block}
#cbsrShelf .hl.ot{transform:scale(1.95);transform-origin:2% 62%}
#cbsrShelf .hl.nt{transform:scale(1.95);transform-origin:98% 62%}
#cbsrShelf .hl.etc{transform:scale(2.3);transform-origin:50% 26%}
#cbsrShelf .dimv{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(26,17,11,.5),rgba(26,17,11,.72));opacity:0;transition:opacity .6s;pointer-events:none}
#cbsrShelf .dimv.on{opacity:1;transition:opacity .6s .85s}
#cbsrShelf .hallv.lv .wk{animation:none;transition:transform .43s ease-in;transform:scale(1.28)}
#cbsrShelf .hallv.lv .ui{transition:opacity .25s;opacity:0}
#cbsrShelf .zin{animation:cbsrZin .5s ease-out both}
#cbsrShelf .tb{background:#f1e6c8;border:1px solid #33231a;box-shadow:inset 0 0 0 2px #f1e6c8,inset 0 0 0 3px rgba(51,35,26,.5),0 2px 5px rgba(40,26,16,.35);color:#33231a}
#cbsrShelf .bk{position:absolute;left:12px;top:10px;height:36px;padding:0 12px 0 6px;display:flex;align-items:center;gap:2px;background:#f1e6c8;border:1px solid #33231a;box-shadow:0 2px 5px rgba(40,26,16,.35);font-size:15px;font-weight:700;z-index:5}
#cbsrShelf .ttl{position:absolute;left:0;right:0;top:10px;display:flex;justify-content:center;pointer-events:none;z-index:4}
#cbsrShelf .ttl b{padding:5px 20px;font:700 19px/1.3 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.12em}
#cbsrShelf .cnt{position:absolute;right:14px;top:17px;font-size:15px;font-weight:700;z-index:4;color:#33231a;background:#f1e6c8;border:1px solid #33231a;padding:1px 8px}
#cbsrShelf .zone{position:absolute;padding:0;border:0;background:transparent}
#cbsrShelf .zone span{position:absolute;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;white-space:nowrap;padding:8px 16px 7px}
#cbsrShelf .zone b{font:700 23px/1.25 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.14em;margin-right:-.14em}
#cbsrShelf .zone small{font-size:13.5px;font-weight:600;line-height:1.35}
#cbsrShelf .zone.e b{font-size:14px;letter-spacing:.02em;margin:0;line-height:1.4;text-align:center}
#cbsrShelf .zone.e span{padding:7px 12px;border-color:#120c08;box-shadow:0 2px 7px rgba(0,0,0,.7);background:radial-gradient(ellipse at 10% 16%,rgba(16,10,6,.95) 0,rgba(16,10,6,0) 48%),radial-gradient(ellipse at 92% 84%,rgba(16,10,6,.95) 0,rgba(16,10,6,0) 54%),radial-gradient(ellipse at 74% 6%,rgba(34,18,8,.8) 0,rgba(34,18,8,0) 42%),radial-gradient(ellipse at 16% 94%,rgba(34,18,8,.85) 0,rgba(34,18,8,0) 46%),radial-gradient(ellipse at 50% 50%,#7a6344 0,#57432c 100%);clip-path:polygon(3% 9%,13% 0,30% 6%,46% 1%,64% 7%,81% 0,96% 10%,100% 35%,95% 57%,100% 83%,89% 100%,70% 93%,52% 100%,34% 92%,16% 100%,2% 87%,6% 60%,0 36%)}
#cbsrShelf .zone.e b{color:#1c110a;opacity:.6;filter:blur(.75px);text-shadow:0 0 3px rgba(18,9,4,.85)}
#cbsrShelf .zone:focus-visible span,#cbsrShelf .gl button:focus-visible,#cbsrShelf .sp:focus-visible{outline:3px solid #9b3324;outline-offset:2px}
#cbsrShelf .gl{position:absolute;left:44px;right:44px;top:120px;display:flex;flex-direction:column;gap:14px;opacity:0;transform:translateY(10px);transition:opacity .5s 1.1s,transform .5s 1.1s}
#cbsrShelf .gl.now{transition:none}
#cbsrShelf .dimv.now{transition:opacity .3s}
#cbsrShelf .wn.late{animation-delay:1.05s}
#cbsrShelf .gl.on{opacity:1;transform:none}
#cbsrShelf .gl button{display:flex;align-items:baseline;justify-content:space-between;gap:12px;width:100%;min-height:64px;padding:14px 20px;text-align:left}
#cbsrShelf .gl b{font:700 22px/1.3 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.06em}
#cbsrShelf .gl small{font-size:15px;font-weight:600}
#cbsrShelf .hint{position:absolute;left:24px;right:24px;bottom:26px;margin:0;text-align:center;font-size:14.5px;line-height:1.5;color:#f6e7c1;text-shadow:0 1px 4px rgba(0,0,0,.85);pointer-events:none}
#cbsrShelf .wn{position:absolute;left:28px;right:28px;top:210px;padding:24px 22px 20px;text-align:center}
#cbsrShelf .wn h2{margin:0 0 12px;font:700 20px/1.4 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.04em}
#cbsrShelf .wn p{margin:0 0 10px;font:400 17px/1.75 "Gowun Batang","Noto Serif KR",serif;text-align:left}
#cbsrShelf .wn h2{color:#9b3324;letter-spacing:.5em;margin-right:-.5em;padding-bottom:10px;border-bottom:3px double #9b3324}
#cbsrShelf .wn p.w1{font-weight:700;text-align:center;font-size:18.5px;margin-top:16px}
#cbsrShelf .wn p.w2{text-align:center;font-size:18.5px}
#cbsrShelf .wn .wb{display:flex;gap:10px;justify-content:center;margin-top:16px}
#cbsrShelf .wn .wb button{margin:0;flex:1}
#cbsrShelf .wn .wb button.in{background:transparent;color:#33231a;border:1px solid #33231a;font-weight:600}
#cbsrShelf .wn p.e{font-family:inherit;font-size:15px;color:#6a5646;text-align:center;margin-top:14px}
#cbsrShelf .wn button{margin-top:6px;min-width:120px;height:46px;background:#33231a;color:#f6e7c1;border:0;font-weight:700;font-size:16px}
#cbsrShelf .sp{position:absolute;padding:0;border:0;background:transparent;border-radius:26px 26px 0 0/6px 6px 0 0}
#cbsrShelf .sp span{position:absolute;display:flex;align-items:center;justify-content:center}
#cbsrShelf .sp i{font-style:normal;writing-mode:vertical-rl;text-orientation:upright;white-space:nowrap;font:700 16px/1.15 "Gowun Batang","Noto Serif KR",serif;letter-spacing:1px;color:#33231a}
#cbsrShelf .sp:active{box-shadow:0 0 0 2px #9b3324,0 0 12px 2px rgba(155,51,36,.45)}
#cbsrShelf .veil{position:absolute;inset:0;background:rgba(34,23,16,.8);opacity:0;pointer-events:none}
#cbsrShelf .op{position:absolute;left:0;top:150px;width:390px;height:420px;perspective:1100px;pointer-events:none}
#cbsrShelf .ob{position:absolute;left:105px;top:60px;width:180px;height:250px;transform-style:preserve-3d}
#cbsrShelf .ob .bd{position:absolute;left:-5px;top:-5px;width:190px;height:260px;background:#4e1c13;border-radius:4px 9px 9px 4px;box-shadow:0 22px 44px rgba(0,0,0,.65)}
#cbsrShelf .ob .pg{position:absolute;inset:0;background:linear-gradient(to right,#d9c594 0%,#f3e6c4 10%,#f7edd4 100%);border-radius:2px 6px 6px 2px;box-shadow:3px 0 0 #e2d2a4,6px 1px 0 #cdb985}
#cbsrShelf .ob .pg:after{content:"";position:absolute;left:26px;top:58px;right:20px;bottom:30px;background:repeating-linear-gradient(to bottom,rgba(90,60,30,0) 0,rgba(90,60,30,0) 13px,rgba(90,60,30,.24) 13px,rgba(90,60,30,.24) 14px)}
#cbsrShelf .ob .cv{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d}
#cbsrShelf .ob .cf,#cbsrShelf .ob .cb{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden}
#cbsrShelf .ob .cf{background:linear-gradient(135deg,#96412a 0%,#732c1d 55%,#5a2016 100%);border-radius:3px 8px 8px 3px;box-shadow:inset 0 0 0 2px rgba(0,0,0,.25),inset 12px 0 14px rgba(0,0,0,.35)}
#cbsrShelf .ob .cf div{position:absolute;left:14px;top:14px;right:12px;bottom:14px;border:1.5px solid #d9b56a;border-radius:3px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center}
#cbsrShelf .ob .cf u{width:9px;height:9px;background:#d9b56a;transform:rotate(45deg)}
#cbsrShelf .ob .cf b{font:700 21px/1.3 "Gowun Batang","Noto Serif KR",serif;color:#ecc97a;letter-spacing:.04em;padding:0 6px}
#cbsrShelf .ob .cf small{font:400 13px/1.3 "Gowun Batang","Noto Serif KR",serif;color:rgba(236,201,122,.8);letter-spacing:.1em}
#cbsrShelf .ob .cb{transform:rotateY(180deg);background:linear-gradient(to left,#cdb784 0%,#ecdcb2 12%,#f3e6c4 100%);border-radius:6px 2px 2px 6px}
#cbsrShelf .blm{position:absolute;left:275px;top:325px;width:20px;height:20px;border-radius:50%;background:radial-gradient(circle,#fff3d6 0%,#ffe6b0 55%,rgba(255,214,140,0) 100%);transform:scale(0);opacity:0;pointer-events:none}
#cbsrShelf .bv{position:absolute;inset:0;background:#0c0908;color:#f6ecd2}
#cbsrShelf .bv .bg{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;animation:cbsrKb 28s ease-in-out infinite alternate}
#cbsrShelf .bv .sh{position:absolute;inset:0;pointer-events:none;background:linear-gradient(to bottom,rgba(12,9,8,.55) 0%,rgba(12,9,8,0) 11%,rgba(12,9,8,0) 30%,rgba(12,9,8,.66) 46%,rgba(12,9,8,.92) 62%,rgba(12,9,8,.98) 100%)}
#cbsrShelf .bv .sh.c{background:linear-gradient(to bottom,rgba(12,9,8,.5) 0%,rgba(12,9,8,0) 9%,rgba(12,9,8,0) 40%,rgba(12,9,8,.62) 52%,rgba(12,9,8,.9) 66%,rgba(12,9,8,.98) 100%)}
#cbsrShelf .bv .bb{position:absolute;left:6px;top:4px;height:48px;padding:0 10px;display:flex;align-items:center;gap:4px;font-size:16px;color:#f6e7c1;background:transparent;border:0;text-shadow:0 1px 4px rgba(0,0,0,.6);z-index:6}
#cbsrShelf .bv .bn{position:absolute;right:16px;top:17px;font:700 16px/1.4 "Gowun Batang","Noto Serif KR",serif;color:#f6e7c1;text-shadow:0 1px 4px rgba(0,0,0,.6);z-index:5}
#cbsrShelf .bv .pr{position:absolute;left:20px;right:20px;top:58px;display:flex;gap:4px;z-index:5}
#cbsrShelf .bv .pr i{flex:1;height:3px;border-radius:2px;background:rgba(246,231,193,.3)}
#cbsrShelf .bv .pr i.on{background:#e2b24a}
#cbsrShelf .bv .tap{position:absolute;top:70px;bottom:74px;width:50%;border:0;background:transparent;z-index:3}
#cbsrShelf .bv .tap.l{left:0}#cbsrShelf .bv .tap.r{right:0}
#cbsrShelf .bv main{position:absolute;left:24px;right:24px;bottom:84px;z-index:4;pointer-events:none}
#cbsrShelf .bv .k{margin:0 0 8px;font-size:15px;line-height:1.4;letter-spacing:.04em;color:#e6cf9a}
#cbsrShelf .bv h1{margin:0;font:700 40px/1.25 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df;text-shadow:0 2px 12px rgba(0,0,0,.6)}
#cbsrShelf .bv .rule{width:44px;height:2px;margin:12px 0;background:#d9b56a}
#cbsrShelf .bv .t{margin:0 0 10px;font:400 20px/1.72 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df;text-shadow:0 1px 8px rgba(0,0,0,.55)}
#cbsrShelf .bv .t.m{font-size:18px;line-height:1.7}#cbsrShelf .bv .t.s{font-size:16.5px;line-height:1.66}
#cbsrShelf .bv .rf{display:block;margin:2px 0 12px;font-size:15px;font-weight:600;color:#e6cf9a}
#cbsrShelf .bv .fn{margin:10px 0 0;font-size:14.5px;line-height:1.6;color:#b9ab8f}
#cbsrShelf .bv .vq{margin:12px 0 0;padding-left:12px;border-left:2px solid #d9b56a;font-size:15px;line-height:1.5;color:#cdbb93}
#cbsrShelf .bv dl{margin:14px 0 0;display:grid;grid-template-columns:auto 1fr;column-gap:14px;row-gap:3px;border-top:1px solid rgba(255,240,200,.22);padding-top:10px;font-size:15px;line-height:1.5}
#cbsrShelf .bv dt{color:#cdbb93}#cbsrShelf .bv dd{margin:0;color:#f6ecd2}
#cbsrShelf .bv ol{margin:8px 0 0;padding:0;list-style:none;font-size:15.5px;line-height:1.5}
#cbsrShelf .bv ol li{display:grid;grid-template-columns:92px 1fr;gap:10px;padding:5px 0;border-top:1px solid rgba(255,240,200,.16)}
#cbsrShelf .bv ol li span{color:#e6cf9a;font-weight:600;font-size:14.5px}
#cbsrShelf .bv .th{margin:6px 0 0;font-size:15px;color:#cdbb93}
#cbsrShelf .bv .qs{margin:0;padding:0;list-style:none}
#cbsrShelf .bv .qs li{margin:0 0 12px;font:400 19px/1.6 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df}
#cbsrShelf .bv .nv{position:absolute;left:14px;right:14px;bottom:18px;height:48px;display:flex;justify-content:space-between;align-items:center;z-index:6}
#cbsrShelf .bv .nv button{min-width:96px;height:48px;padding:0 12px;background:transparent;border:0;font-size:16px;font-weight:600;color:#f6e7c1;display:flex;align-items:center;gap:4px}
#cbsrShelf .bv .nv button:disabled{opacity:.3}
#cbsrShelf .bv .nv button.go{background:#e2b24a;color:#2a1d14;border-radius:2px;justify-content:center;padding:0 18px}
#cbsrShelf .bv .nv button.mid{min-width:0;font-size:14px;font-weight:400;color:#cdbb93;padding:0 8px}
#cbsrShelf .amb{pointer-events:none;position:absolute}
#cbsrShelf .fade{animation:cbsrIn .45s ease both}
@keyframes cbsrIn{from{opacity:0}to{opacity:1}}
@keyframes cbsrZin{from{opacity:0;transform:scale(1.07)}to{opacity:1;transform:none}}
@keyframes cbsrWalk{0%,100%{transform:translateY(0)}12%{transform:translateY(-5px)}25%{transform:translateY(0)}37%{transform:translateY(-5px)}50%{transform:translateY(0)}62%{transform:translateY(-4px)}75%{transform:translateY(0)}87%{transform:translateY(-3px)}}
@keyframes cbsrKb{from{transform:scale(1)}to{transform:scale(1.08) translate(-1.2%,-1%)}}
@keyframes cbsrGlw{0%,100%{opacity:.45}40%{opacity:1}65%{opacity:.66}}
@keyframes cbsrFlm{0%,100%{transform:scale(1,1)}30%{transform:scale(.84,1.14)}60%{transform:scale(1.1,.92)}}
@keyframes cbsrRay{0%,100%{opacity:.4}50%{opacity:.9}}
@media (prefers-reduced-motion:reduce){#cbsrShelf .amb,#cbsrShelf .bv .bg,#cbsrShelf .fade{animation:none!important}#cbsrShelf .hl,#cbsrShelf .gl,#cbsrShelf .dimv,#cbsrShelf .wk{transition:none!important;animation:none!important}#cbsrShelf .zin,#cbsrShelf .wn.late{animation:none!important}}
`;
var HS=H;
/* 무대는 너비 390에 맞추고, 높이는 화면 비율대로(HS). 가로가 넓은 화면은 높이 600을 채우고 양옆은 흐린 서고 */
function fit(){ if(!stage) return; var vw=innerWidth,vh=innerHeight,s=vw/W,hs=vh/s; if(hs<600){ hs=600; s=vh/600; } HS=Math.round(hs); stage.style.height=HS+"px"; stage.style.transform="translate(-50%,-50%) scale("+s+")"; }
function scn(){ return HS<=H?"transform:translateY("+(-(H-HS)*.3).toFixed(1)+"px)":"transform:scale("+(HS/H).toFixed(4)+")"; }
var lastHS=0; function onRs(){ fit(); if(busy||Math.abs(HS-lastHS)<3) return; lastHS=HS; draw(); }
function load(){ if(DATA) return Promise.resolve(DATA); if(LOAD) return LOAD;
  return LOAD=fetch("shelf_66.json").then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); }).then(function(d){ var by={},gs={}; (d.books||[]).forEach(function(b){ by[b.id]=b; (gs[b.group]=gs[b.group]||[]).push(b); }); DATA={by:by,gs:gs}; return DATA; }).catch(function(e){ LOAD=null; throw e; }); }
function say(t){ if(O.toast) O.toast(t); }
/* ---- 단계: 서고 → 구역(구약·신약·그 밖) → 서가 → 책. 뒤로는 한 단계씩(화면의 ‹와 휴대폰의 뒤로 가기가 같은 일) ---- */
function top(){ return levels[levels.length-1]; }
function push(st){ var fn=function(pop){ var i=levels.indexOf(st); if(i<0) return; levels.length=i; if(pop!==true&&O.done) O.done(fn); draw(st); }; st.fn=fn; levels.push(st); if(O.push) O.push(fn); draw(); }
function back(){ var t=top(); if(busy) return; if(!t||t.t==="hall"){ api.close(); return; } t.fn(false); }
function draw(from){ var t=top(); if(!t||!stage) return; if(t.t==="hall"||t.t==="sec") drawHall(t); else if(t.t==="press") drawPress(t,from); else if(t.t==="book") drawBook(t); }
/* ---- 서고와 구역 ---- */
function lamps(){ var h="",i=0; ART.hall.lanterns.forEach(function(l){ var x=l[0],y=l[1],s=l[2],g=Math.round(s*1.7),w=Math.max(4,Math.round(s*.11));
    h+='<div class="amb" style="left:'+(x-g/2)+'px;top:'+(y-s*.68)+'px;width:'+g+'px;height:'+g+'px;border-radius:50%;background:radial-gradient(circle,rgba(255,238,180,.8) 0%,rgba(255,226,150,.32) 36%,rgba(255,220,140,0) 68%);mix-blend-mode:overlay;animation:cbsrGlw '+(2.8+(i%4)*.35)+'s ease-in-out -'+(i*.7)+'s infinite"></div>'+
       '<div class="amb" style="left:'+(x-w/2)+'px;top:'+(y+2)+'px;width:'+w+'px;height:'+(w*2)+'px;border-radius:50% 50% 50% 50%/64% 64% 36% 36%;background:radial-gradient(ellipse at 50% 70%,#fffbe6 0%,#ffd66e 50%,rgba(255,190,80,0) 78%);transform-origin:50% 100%;animation:cbsrFlm '+(1.3+(i%5)*.13)+'s ease-in-out -'+(i*.3)+'s infinite"></div>'; i++; });
  return h; }
function hallBase(){ var el=stage.querySelector(".hallv"); if(el) return el;
  stage.innerHTML='<div class="lay hallv"><div class="scn"><div class="wk"><div class="hl"><img src="'+IMG+'hall.webp" alt="옛 판화처럼 그린 긴 서고. 촛불이 밝힌 돌바닥 양옆으로 서가가 늘어서 있고, 덧문을 닫은 창 아래 맨 끝은 어둡다">'+
    lamps()+'</div></div><div class="zn"></div></div><div class="dimv"></div><div class="ui"></div></div>';
  el=stage.querySelector(".hallv"); el._fresh=true; return el; }
function drawHall(t){ var v=hallBase(), hl=v.querySelector(".hl"), ui=v.querySelector(".ui"), dim=v.querySelector(".dimv"), zn=v.querySelector(".zn"), wk=v.querySelector(".wk"), fresh=v._fresh, cls=(t.t==="sec"&&!(t.s==="etc"&&t.step!=="in"))?" "+t.s:"", moved=(hl.className!=="hl"+cls); v._fresh=false; v.classList.remove("lv"); v.querySelector(".scn").style.cssText=scn(); zn.innerHTML="";
  if(!fresh&&moved){ wk.classList.remove("go"); void wk.offsetWidth; wk.classList.add("go"); } /* 걸어서 그 앞으로(돌아올 때도) */
  hl.className="hl"+cls; dim.className="dimv"+(t.t==="sec"?" on":"");
  if(t.t==="hall"){ ui.innerHTML='<button type="button" class="bk" data-a="back" aria-label="성경 서고 닫기">'+CL+'닫기</button><div class="ttl"><b class="tb">성경 서고</b></div><p class="hint">들어갈 곳을 고르세요.</p>';
    zn.innerHTML='<button type="button" class="zone" data-s="ot" style="left:0;top:230px;width:168px;height:480px" aria-label="구약 서른아홉 권"><span class="tb" style="top:150px"><b>구약</b><small>서른아홉 권</small></span></button>'+
      '<button type="button" class="zone" data-s="nt" style="left:222px;top:230px;width:168px;height:480px" aria-label="신약 스물일곱 권"><span class="tb" style="top:150px"><b>신약</b><small>스물일곱 권</small></span></button>'+
      '<button type="button" class="zone e" data-s="etc" style="left:140px;top:128px;width:110px;height:196px" aria-label="외경, 위경, 교부 문헌"><span class="tb" style="top:6px"><b>외경 · 위경<br>교부 문헌</b></span></button>'; return; }
  if(t.s==="etc"){ var bkb='<button type="button" class="bk" data-a="back">'+CL+'서고</button>';
    if(t.step!=="in") ui.innerHTML=bkb+'<div class="wn tb fade" role="alertdialog" aria-label="경고"><h2>'+WARN.t+'</h2><p class="w1">'+WARN.a+'</p><p class="w2">'+WARN.q+'</p><div class="wb"><button type="button" data-a="back">돌아가기</button><button type="button" class="in" data-a="enter">열람하기</button></div></div>';
    else ui.innerHTML=bkb+'<div class="wn tb fade'+(fresh?"":" late")+'" role="alertdialog" aria-label="'+WARN.e+'"><p class="w1" style="margin-top:4px">'+WARN.e+'</p><div class="wb"><button type="button" data-a="back">서고로</button></div></div>';
    if(t.step!=="in") dim.className="dimv on now";
    return; }
  var S=SEC[t.s], h='<button type="button" class="bk" data-a="back">'+CL+'서고</button><div class="ttl"><b class="tb">'+S.n+'</b></div><span class="cnt">'+S.c+'</span><div class="gl">';
  var N={"모세오경":5,"역사서":12,"시가서":5,"선지서":17,"복음서":4,"사도행전":1,"바울서신":13,"일반서신":8,"요한계시록":1};
  S.g.forEach(function(g){ h+='<button type="button" class="tb" data-g="'+g+'"><b>'+g+'</b><small>'+CNT[N[g]]+'</small></button>'; });
  ui.innerHTML=h+'</div><p class="hint">빈 곳을 누르면 서고로 돌아갑니다.</p>'; var gl=ui.querySelector(".gl"); if(fresh){ gl.classList.add("now"); gl.classList.add("on"); return; }
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ gl.classList.add("on"); }); }); }
/* ---- 서가 ---- */
function drawPress(t,from){ var key=PRESS[t.g], L=ART.labels[key], sw=(key==="pro"?48:56), S=SEC[t.s];
  var k=(HS-50)/802, ty=50-44*k; /* 서가는 너비를 꽉 채우고 높이만 화면에 맞춤(양옆 빈 띠 없음). 글자는 눌리지 않게 되돌림 */
  var h='<div class="lay zin"><div class="bdp"></div><div class="scn pr" style="transform:translateY('+ty.toFixed(1)+'px) scale(1,'+k.toFixed(4)+')"><img class="full" src="'+IMG+'press_'+key+'.webp" alt="'+esc(t.g)+' 서가">';
  var books=(DATA&&DATA.gs[t.g])||[];
  books.forEach(function(b){ var a=L[b.name]; if(!a) return; var two=b.name.length>5, nm=two?esc(b.name.slice(0,b.name.length-2))+"<br>"+esc(b.name.slice(-2)):esc(b.name);
    h+='<button type="button" class="sp" data-b="'+b.id+'" aria-label="'+esc(b.name)+' 펼치기" style="left:'+a[0]+'px;top:'+a[1]+'px;width:'+sw+'px;height:'+a[2]+'px"><span style="left:'+a[3]+'px;top:26px;width:'+a[4]+'px;height:'+a[5]+'px"><i style="font-size:'+(16*Math.min(1,k)).toFixed(1)+'px;transform:scaleY('+(1/k).toFixed(4)+')">'+nm+'</i></span></button>'; });
  stage.innerHTML=h+'</div><button type="button" class="bk" data-a="back">'+CL+S.n+'</button><div class="ttl"><b class="tb">'+esc(t.g)+'</b></div><span class="cnt">'+CNT[Object.keys(L).length]+'</span><p class="hint">책을 고르면 펼쳐집니다.</p></div>'; }
/* ---- 책 펼침(한 번, 2초쯤) ---- */
function openBook(id,rect){ var b=DATA&&DATA.by[id]; if(!b||busy) return; var st={t:"book",id:id,p:0};
  var rm=matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches; if(rm||!rect||!stage.animate){ push(st); return; }
  busy=true; var lay=document.createElement("div"); lay.className="lay"; lay.style.zIndex=20;
  lay.innerHTML='<div class="veil"></div><div class="op"><div class="ob"><div class="bd"></div><div class="pg"></div><div class="cv"><div class="cf"><div><u></u><b>'+esc(b.name)+'</b><small>'+esc(b.group)+'</small></div></div><div class="cb"></div></div></div></div><div class="blm"></div>';
  stage.appendChild(lay); var ob=lay.querySelector(".ob"), cv=lay.querySelector(".cv"), veil=lay.querySelector(".veil"), blm=lay.querySelector(".blm");
  var cy=Math.round(HS*.42); lay.querySelector(".op").style.top=(cy-185)+"px"; blm.style.top=(cy-10)+"px";
  var dx=(rect.x+rect.w/2)-195, dy=(rect.y+rect.h/2)-cy, sc=Math.max(.26,rect.h/250), D=1900, E="cubic-bezier(.4,0,.2,1)";
  veil.animate([{opacity:0},{opacity:1,offset:.3},{opacity:1}],{duration:D,fill:"forwards"});
  ob.animate([{transform:"translate("+dx+"px,"+dy+"px) scale("+sc+")",opacity:0},{transform:"translate("+dx+"px,"+dy+"px) scale("+sc+")",opacity:1,offset:.06},{transform:"translate(0,0) scale(1)",opacity:1,offset:.36},{transform:"translate(0,0) scale(1)",opacity:1,offset:.42},{transform:"translate(90px,0) scale(1)",opacity:1,offset:.72},{transform:"translate(90px,0) scale(1)",opacity:1,offset:.8},{transform:"translate(90px,0) scale(1.35)",opacity:0}],{duration:D,easing:E,fill:"forwards"});
  cv.animate([{transform:"rotateY(0deg)"},{transform:"rotateY(0deg)",offset:.42},{transform:"rotateY(-166deg)",offset:.72},{transform:"rotateY(-166deg)"}],{duration:D,easing:E,fill:"forwards"});
  var a=blm.animate([{transform:"scale(0)",opacity:0},{transform:"scale(0)",opacity:0,offset:.72},{transform:"scale(6)",opacity:.85,offset:.82},{transform:"scale(90)",opacity:1}],{duration:D,easing:"ease-in",fill:"forwards"});
  var done=function(){ if(!busy) return; busy=false; push(st); }; a.onfinish=done; setTimeout(done,D+250); }
/* ---- 책 ---- */
function pages(b){ var P=[],bg=(b.background||[]).filter(function(x){return x&&x.text;}),i;
  P.push({k:"cover"}); if(b.verseText) P.push({k:"verse"});
  for(i=0;i<bg.length;i+=2) P.push({k:"bg",a:bg.slice(i,i+2),n:Math.floor(i/2)+1,last:i+2>=bg.length});
  if(!bg.length&&b.footnote) P.push({k:"bg",a:[],n:1,last:true});
  if(b.purpose) P.push({k:"why"}); if(b.flow||(b.structure||[]).length) P.push({k:"parts"}); if(b.god) P.push({k:"god"});
  if(b.connection) P.push({k:"link"}); if(b.reading) P.push({k:"read"}); P.push({k:"end"}); return P; }
function sz(s){ var n=(s||"").length; return n>190?" s":n>120?" m":""; }
function drawBook(t){ var b=DATA.by[t.id], P=pages(b); t.n=P.length; t.p=Math.max(0,Math.min(t.p,P.length-1)); var pg=P[t.p], ot=(SEC.ot.g.indexOf(b.group)>=0), m="", bgs=Math.ceil((b.background||[]).length/2)||1;
  var cover=(pg.k==="cover"||pg.k==="verse"||pg.k==="end");
  if(pg.k==="cover"){ m='<p class="k">'+(ot?"구약":"신약")+" · "+esc(b.group)+" · "+b.chapters+'장</p><h1>'+esc(b.name)+'</h1><div class="rule"></div><p class="t m">'+esc(b.line)+'</p>'+(b.verse?'<p class="vq">'+esc(b.verse)+(b.mem100?" · 꼭 외울 말씀 100":"")+'</p>':"")+
      '<dl><dt>저자</dt><dd>'+esc(b.author)+'</dd><dt>수신자</dt><dd>'+esc(b.audience)+'</dd>'+(b.time?'<dt>시기</dt><dd>'+esc(b.time)+'</dd>':"")+'<dt>갈래</dt><dd>'+esc(b.genre)+'</dd></dl>'; }
  else if(pg.k==="verse"){ m='<p class="k">대표 구절</p><p class="t'+sz(b.verseText)+'">'+esc(b.verseText)+'</p><span class="rf">'+esc(b.verse)+" · 개역개정"+(b.mem100?" · 꼭 외울 말씀 100":"")+'</span>'; }
  else if(pg.k==="bg"){ var all=pg.a.map(function(x){return x.text;}).join(""); m='<p class="k">배경'+(bgs>1?" "+pg.n+" / "+bgs:"")+'</p>'+pg.a.map(function(x){ return '<p class="t'+sz(all)+'" style="margin-bottom:0">'+esc(x.text)+'</p><span class="rf">'+esc(x.ref||"")+'</span>'; }).join("")+(pg.last&&b.footnote?'<p class="fn">* '+esc(b.footnote)+'</p>':""); }
  else if(pg.k==="why"){ m='<p class="k">목적 · 왜 썼습니까</p><p class="t'+sz(b.purpose)+'">'+esc(b.purpose)+'</p>'; }
  else if(pg.k==="parts"){ var S=b.structure||[]; m='<p class="k">구조 · 어떻게 흘러갑니까</p><p class="t s">'+esc(b.flow)+'</p><ol>'+S.map(function(x){ return '<li><span>'+esc(x.range)+'</span>'+esc(x.title)+'</li>'; }).join("")+'</ol>'; }
  else if(pg.k==="god"){ m='<p class="k">하나님은 어떤 분이십니까</p><p class="t'+sz(b.god)+'">'+esc(b.god)+'</p>'+((b.themes||[]).length?'<p class="th">'+esc(b.themes.join(" · "))+'</p>':""); }
  else if(pg.k==="link"){ m='<p class="k">연결 · 성경 전체에서</p><p class="t'+sz(b.connection)+'">'+esc(b.connection)+'</p>'; }
  else if(pg.k==="read"){ m='<p class="k">읽기 · 이렇게 읽어 보세요</p><p class="t'+sz(b.reading)+'">'+esc(b.reading)+'</p>'; }
  else { m='<p class="k">책을 덮고, 내 말로 설명해 보세요</p><ul class="qs"><li>누가 누구에게 왜 썼습니까?</li><li>어떤 흐름으로 무엇을 말합니까?</li><li>이 책에서 하나님은 어떤 분이십니까?</li></ul>'; }
  var pr=""; for(var i=0;i<P.length;i++) pr+='<i'+(i<=t.p?' class="on"':"")+'></i>';
  var last=t.p===P.length-1, bkLab=(PRESS[b.group]?"서가":(ot?"구약":"신약"));
  stage.innerHTML='<div class="lay bv"><img class="bg" src="'+IMG+(cover?"bg_road":"bg_lamp")+'.webp" alt=""><div class="sh'+(cover?" c":"")+'"></div><button type="button" class="bb" data-a="back">'+CL+''+bkLab+'</button>'+(pg.k==="cover"?"":'<span class="bn">'+esc(b.name)+'</span>')+
    '<div class="pr" role="img" aria-label="'+(t.p+1)+" / "+P.length+'">'+pr+'</div><button type="button" class="tap l" data-a="prev" aria-label="앞 장" tabindex="-1"></button><button type="button" class="tap r" data-a="next" aria-label="다음 장" tabindex="-1"></button><main class="fade" aria-live="polite">'+m+'</main>'+
    '<div class="nv"><button type="button" data-a="prev"'+(t.p?"":" disabled")+'>'+CL+'앞 장</button><button type="button" class="mid" data-a="back" aria-label="'+bkLab+'로 돌아가기">'+(t.p+1)+" / "+P.length+' · 닫기</button>'+(last?'<button type="button" class="go" data-a="back">'+bkLab+'로</button>':'<button type="button" data-a="next">다음'+CR+'</button>')+'</div></div>';
  var mn=stage.querySelector("main"), sh=stage.querySelector(".sh"), lim=HS-84-80, f=1, i; if(!mn||!sh) return;
  for(i=0;i<4&&mn.offsetHeight*f>lim;i++){ f=Math.max(.66,f*Math.sqrt(lim/(mn.offsetHeight*f))*.985); mn.style.transformOrigin="0 100%"; mn.style.transform="scale("+f.toFixed(3)+")"; mn.style.width=(342/f).toFixed(1)+"px"; mn.style.right="auto"; }
  var vis=mn.offsetHeight*f; if(vis>HS*.5) sh.style.background="linear-gradient(to bottom,rgba(12,9,8,.6) 0%,rgba(12,9,8,.86) "+Math.max(8,Math.round((HS-84-vis-60)/HS*100))+"%,rgba(12,9,8,.97) 100%)"; }
function turn(d){ var t=top(); if(!t||t.t!=="book") return; var p=t.p+d; if(p<0||p>=t.n) return; t.p=p; drawBook(t); }
/* ---- 눌림 ---- */
function approach(cb){ var v=stage.querySelector(".hallv"), rm=window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches; if(!v||rm){ cb(); return; } busy=true; v.classList.add("lv"); setTimeout(function(){ busy=false; if(root) cb(); },440); }
function onClick(e){ if(busy||!root) return; var el=e.target.closest("[data-a],[data-s],[data-g],[data-b]");
  if(!el||!root.contains(el)){ var t0=top(); if(!t0||t0.t==="book"||e.target.closest(".ttl,.cnt,.wn,.gl,.bk")) return; /* 11-24 목사님: 빈 곳(배경)을 눌러도 나올 수 있게 */
    if(t0.t==="press"){ var im=stage.querySelector(".scn.pr img"); if(im){ var rr=im.getBoundingClientRect(), fx=(e.clientX-rr.left)/rr.width*W, fy=(e.clientY-rr.top)/rr.height*H; if(fx>24&&fx<366&&fy>84&&fy<790) return; } }
    back(); return; }
  var d=el.dataset;
  if(d.a==="back"){ back(); return; } if(d.a==="next"){ turn(1); return; } if(d.a==="prev"){ turn(-1); return; }
  if(d.a==="enter"){ var te=top(); if(te&&te.t==="sec"&&te.s==="etc"){ te.step="in"; drawHall(te); } return; }
  if(d.s){ push({t:"sec",s:d.s}); return; }
  if(d.g){ var s=top().s, g=d.g; load().then(function(D){ if(!PRESS[g]){ var one=(D.gs[g]||[])[0]; if(one) approach(function(){ push({t:"book",id:one.id,p:0,s:s}); }); return; } approach(function(){ push({t:"press",g:g,s:s}); }); }).catch(function(){ say("책장 원고를 받지 못했습니다. 인터넷 연결을 확인해 주세요."); }); return; }
  if(d.b){ var r=el.getBoundingClientRect(), q=stage.getBoundingClientRect(), k=q.width/W; openBook(d.b,{x:(r.left-q.left)/k,y:(r.top-q.top)/k,w:r.width/k,h:r.height/k}); } }
function onKey(e){ if(!root) return; if(e.key==="Escape"){ e.preventDefault(); back(); } else if(e.key==="ArrowRight") turn(1); else if(e.key==="ArrowLeft") turn(-1); }
var sx=null; function onTs(e){ sx=e.touches.length===1?e.touches[0].clientX:null; } function onTe(e){ if(sx==null) return; var dx=e.changedTouches[0].clientX-sx; sx=null; if(Math.abs(dx)>56) turn(dx<0?1:-1); }
var api={ isOpen:function(){ return !!root; },
  open:function(o){ if(root) return true; O=o||{}; levels=[]; busy=false;
    if(!document.getElementById("cbsrShelfCss")){ var st=document.createElement("style"); st.id="cbsrShelfCss"; st.textContent=CSS; document.head.appendChild(st); }
    root=document.createElement("div"); root.id="cbsrShelf"; root.setAttribute("role","dialog"); root.setAttribute("aria-modal","true"); root.setAttribute("aria-label","성경 서고"); root.innerHTML='<div class="st"></div>';
    document.body.appendChild(root); stage=root.firstChild; fit(); lastHS=HS; addEventListener("resize",onRs); root.addEventListener("click",onClick); document.addEventListener("keydown",onKey); root.addEventListener("touchstart",onTs,{passive:true}); root.addEventListener("touchend",onTe,{passive:true}); root.addEventListener("touchmove",function(e){ e.preventDefault(); },{passive:false});
    document.documentElement.classList.add("shelf-on"); levels.push({t:"hall"}); draw(); load().then(function(){ if(O.book&&DATA.by[O.book]) push({t:"book",id:O.book,p:0,s:(SEC.ot.g.indexOf(DATA.by[O.book].group)>=0?"ot":"nt")}); }).catch(function(){});
    root.tabIndex=-1; try{ root.focus({preventScroll:true}); }catch(e){}
    return true; },
  close:function(silent){ if(!root) return; var deep=levels.slice(1); levels=[]; removeEventListener("resize",onRs); document.removeEventListener("keydown",onKey); root.remove(); root=null; stage=null; busy=false; document.documentElement.classList.remove("shelf-on");
    if(O.done) deep.reverse().forEach(function(st){ if(st.fn) O.done(st.fn); });
    if(!silent&&O.onClose) O.onClose(); } };
window.CBSR_SHELF=api;
})();
