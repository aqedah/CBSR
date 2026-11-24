/* 성경 서고 — 2026-11-24 목사님: 진입 경로를 넣고 앱에서 서고를 볼 수 있게.
   서고는 세 부분(구약 · 신약 · 외경과 위경과 교부 문헌). 구약과 신약은 그 안에서 서가로 나누어 들어감. 셋째 부분은 지금은 경고문만.
   서고 → (구약|신약) 서가 고르기 → 서가(책등) → 책 펼침 → 책(표지 · 대표 구절 · 배경 · 목적 · 구조 · 하나님 · 연결 · 읽기 · 맺음)
   원고는 shelf_66.json(성경책장 작업대의 내보내기 꼴). 그림은 img/shelf/. 앱에서는 필요할 때만 불러옴(template3.html의 shelfOpen). */
(function(){
"use strict";
var ART=__ART__;
var IMG="img/shelf/", VER="?v=8", W=390, H=846;   /* 그림을 바꾸면 VER를 올림(서비스 워커가 img/를 캐시에서 먼저 줌) */
var SEC={ot:{n:"구약",c:"서른아홉 권",g:["모세오경","역사서","시가서","선지서"]},nt:{n:"신약",c:"스물일곱 권",g:["복음서","사도행전","바울서신","일반서신","요한계시록"]}};
var PRESS={"모세오경":"tor","역사서":"his","시가서":"poe","선지서":"pro","복음서":"gos","바울서신":"pau","일반서신":"gen"};
var CNT=["","한 권","두 권","세 권","네 권","다섯 권","여섯 권","일곱 권","여덟 권","아홉 권","열 권","열한 권","열두 권","열세 권","열네 권","열다섯 권","열여섯 권","열일곱 권"];
/* 셋째 부분(외경 · 위경 · 교부 문헌): 어둡고, 이름패는 불에 그을려 잘 읽히지 않음. 누르면 경고장부터(11-24 목사님의 글). 책은 아직 없음 */
var WARN={t:"경고",a:"이 서고의 책은 성경이 아닙니다.",q:"정말로 열람하시겠습니까?",e:"아직 들여놓은 책이 없는 것 같다."};   /* e: 주인공(1인칭)의 혼잣말 */
var root=null,stage=null,O={},DATA=null,LOAD=null,levels=[],busy=false;
var CL='<svg class="ch" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="m15 5-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>', CR='<svg class="ch" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
var esc=function(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
var CSS=`
#cbsrShelf{position:fixed;inset:0;z-index:99000;overscroll-behavior:contain;background:#17100b;overflow:hidden;overflow:clip;touch-action:manipulation;-webkit-tap-highlight-color:transparent;font-family:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;color:#33231a}
#cbsrShelf:before{content:"";position:absolute;inset:-40px;background:url(img/shelf/hall.webp${VER}) center/cover;filter:blur(16px) brightness(.4)}
#cbsrShelf *{box-sizing:border-box}
html.shelf-on .coach{display:none!important}
#cbsrShelf:focus{outline:none}
#cbsrShelf .st{position:absolute;left:50%;top:0;width:390px;height:846px;transform-origin:50% 0;overflow:hidden;overflow:clip;background:#2a1d14;word-break:keep-all}
#cbsrShelf .sf{font-family:"Gowun Batang","Noto Serif KR",serif}
#cbsrShelf button{font:inherit;color:inherit;cursor:pointer;border-radius:0;margin:0;-webkit-appearance:none;appearance:none}
#cbsrShelf .ch{display:block;flex:none}
#cbsrShelf .scn{position:absolute;left:0;top:0;width:390px;height:846px;transform-origin:50% 0}
#cbsrShelf .bdp{position:absolute;inset:-24px;background:url(img/shelf/hall.webp${VER}) 50% 40%/cover;filter:blur(7px) brightness(.5)}
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
#cbsrShelf .bk,#cbsrShelf .ttl b,#cbsrShelf .cnt,#cbsrShelf .cdmix{height:38px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;background:#f1e6c8;border:1px solid #33231a;box-shadow:inset 0 0 0 2px #f1e6c8,inset 0 0 0 3px rgba(51,35,26,.5),0 2px 5px rgba(40,26,16,.35);color:#33231a}
#cbsrShelf .bk{position:absolute;left:12px;top:10px;min-width:76px;padding:0 12px 0 6px;gap:2px;font-size:15px;font-weight:700;z-index:5}
#cbsrShelf .ttl{position:absolute;left:0;right:0;top:10px;display:flex;justify-content:center;pointer-events:none;z-index:4}
#cbsrShelf .ttl b{padding:0 18px;font:700 19px/1 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.12em;text-indent:.12em}
#cbsrShelf .cnt{position:absolute;right:12px;top:10px;min-width:76px;padding:0 10px;font-size:15px;font-weight:700;z-index:4}
#cbsrShelf .zn{position:absolute;inset:0;transition:opacity .45s}
#cbsrShelf .zn.off{opacity:0;pointer-events:none;visibility:hidden;transition:opacity .3s,visibility 0s .3s}
#cbsrShelf .zone{position:absolute;padding:0;border:0;background:transparent}
#cbsrShelf .zone span{position:absolute;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;white-space:nowrap;padding:8px 16px 7px}
#cbsrShelf .zone b{font:700 23px/1.25 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.14em;margin-right:-.14em}
#cbsrShelf .zone small{font-size:13.5px;font-weight:600;line-height:1.35}
#cbsrShelf .zone.e b{font-size:14px;letter-spacing:.02em;margin:0;line-height:1.4;text-align:center}
#cbsrShelf .zone.e span{padding:7px 12px;border-color:#120c08;box-shadow:0 2px 7px rgba(0,0,0,.7);background:radial-gradient(ellipse at 10% 16%,rgba(16,10,6,.95) 0,rgba(16,10,6,0) 48%),radial-gradient(ellipse at 92% 84%,rgba(16,10,6,.95) 0,rgba(16,10,6,0) 54%),radial-gradient(ellipse at 74% 6%,rgba(34,18,8,.8) 0,rgba(34,18,8,0) 42%),radial-gradient(ellipse at 16% 94%,rgba(34,18,8,.85) 0,rgba(34,18,8,0) 46%),radial-gradient(ellipse at 50% 50%,#7a6344 0,#57432c 100%);clip-path:polygon(3% 9%,13% 0,30% 6%,46% 1%,64% 7%,81% 0,96% 10%,100% 35%,95% 57%,100% 83%,89% 100%,70% 93%,52% 100%,34% 92%,16% 100%,2% 87%,6% 60%,0 36%)}
#cbsrShelf .zone.e b{color:#1c110a;opacity:.5;filter:blur(1.35px);text-shadow:0 0 5px rgba(18,9,4,.9);letter-spacing:-.02em}
#cbsrShelf .zone.e span:after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 22% 36%,rgba(14,8,5,.8) 0,rgba(14,8,5,0) 30%),radial-gradient(ellipse at 72% 28%,rgba(14,8,5,.7) 0,rgba(14,8,5,0) 26%),radial-gradient(ellipse at 54% 78%,rgba(14,8,5,.8) 0,rgba(14,8,5,0) 32%),radial-gradient(ellipse at 90% 64%,rgba(22,11,5,.7) 0,rgba(22,11,5,0) 24%)}
#cbsrShelf .zone:focus-visible span,#cbsrShelf .gl button:focus-visible,#cbsrShelf .sp:focus-visible{outline:3px solid #9b3324;outline-offset:2px}
#cbsrShelf .gl{position:absolute;left:44px;right:44px;top:120px;display:flex;flex-direction:column;gap:14px;opacity:0;transform:translateY(10px);transition:opacity .5s 1.1s,transform .5s 1.1s}
#cbsrShelf .gl.now{transition:none}
#cbsrShelf .dimv.now{transition:opacity .3s}
#cbsrShelf .wn.late,#cbsrShelf .mono.late{animation-delay:1.05s}
#cbsrShelf .mono{position:absolute;left:14px;right:14px;bottom:18px;min-height:76px;padding:16px 40px 16px 20px;text-align:left;background:rgba(14,10,7,.86);border:1px solid rgba(230,207,154,.42);box-shadow:0 4px 18px rgba(0,0,0,.6);color:#f1e6c8;font:400 18.5px/1.65 "Gowun Batang","Noto Serif KR",serif;z-index:4}
#cbsrShelf .mono i{position:absolute;right:16px;bottom:14px;width:0;height:0;border:6px solid transparent;border-top:8px solid #e2b24a;border-bottom:0;animation:cbsrNx 1.2s ease-in-out infinite}
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
#cbsrShelf .lib{position:absolute;left:10px;right:10px;bottom:12px;display:flex;align-items:center;gap:10px;padding:8px 14px 8px 8px;z-index:4}
#cbsrShelf .lib.tmp{pointer-events:none;animation:cbsrBye .6s ease 3.6s forwards}
#cbsrShelf .lib span{flex:none;display:block;width:46px;height:46px}
#cbsrShelf .lib svg{display:block}
#cbsrShelf .lib p{margin:0;font:400 15.5px/1.5 "Gowun Batang","Noto Serif KR",serif;color:#33231a}
#cbsrShelf .lib b{display:block;font:700 12.5px/1.3 "IBM Plex Sans KR","Apple SD Gothic Neo",sans-serif;letter-spacing:.2em;color:#9b3324}
#cbsrShelf .sl{position:absolute;width:15px;height:15px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#cf5a40,#8f2a1c);box-shadow:0 1px 3px rgba(0,0,0,.55);pointer-events:none}
#cbsrShelf .bv main.qa{top:84px;bottom:auto;pointer-events:auto}
#cbsrShelf .bv .sh.q{background:linear-gradient(to bottom,rgba(12,9,8,.74),rgba(12,9,8,.92))}
#cbsrShelf .bv .qq{margin:0 0 12px;font:700 22px/1.45 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df}
#cbsrShelf .bv textarea{display:block;width:100%;height:132px;margin:0;padding:12px 14px;border:1px solid #d9b56a;border-radius:0;background:rgba(246,236,210,.97);color:#2a1d14;font:400 17px/1.6 "Gowun Batang","Noto Serif KR",serif;resize:none;outline:none;-webkit-appearance:none;appearance:none}
#cbsrShelf .bv textarea:focus{box-shadow:0 0 0 2px #e2b24a}
#cbsrShelf .bv .qb{display:flex;gap:10px;margin-top:12px}
#cbsrShelf .bv .qb button{height:48px;padding:0 14px;font-size:15.5px;font-weight:700;border:1px solid #d9b56a;background:transparent;color:#f6e7c1}
#cbsrShelf .bv .qb button.ans{flex:1;background:#e2b24a;color:#2a1d14;border-color:#e2b24a}
#cbsrShelf .seals{display:flex;justify-content:space-between;margin-top:20px}
#cbsrShelf .seals i{font-style:normal;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border:1.5px dashed rgba(230,207,154,.5);border-radius:50%;font:700 13px/1 "Gowun Batang","Noto Serif KR",serif;color:rgba(230,207,154,.6)}
#cbsrShelf .seals i.on{border:2px solid #b5402c;background:radial-gradient(circle at 35% 30%,#cf5a40,#8f2a1c);color:#f8e6c8;box-shadow:inset 0 0 0 3px rgba(0,0,0,.14),0 2px 5px rgba(0,0,0,.5);transform:rotate(-8deg)}
#cbsrShelf .seals i.cur{outline:2px solid #e2b24a;outline-offset:3px}
#cbsrShelf .seals i.st{animation:cbsrStamp .6s cubic-bezier(.3,1.3,.5,1) both}
#cbsrShelf .bv .fh{margin:0 0 14px;font:700 24px/1.35 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df}
#cbsrShelf .bv .fa{margin:0 0 10px;font:400 16.5px/1.6 "Gowun Batang","Noto Serif KR",serif;color:#fbf3df}
#cbsrShelf .bv .fa b{display:block;font:700 13.5px/1.5 "IBM Plex Sans KR","Apple SD Gothic Neo",sans-serif;color:#e6cf9a}
#cbsrShelf .amb{pointer-events:none;position:absolute}
#cbsrShelf .fl{border-radius:50% 50% 46% 46%/74% 74% 26% 26%;background:radial-gradient(ellipse at 50% 74%,#fffdf0 0,#ffe89a 38%,#f9bd52 72%,rgba(238,150,50,0) 100%);box-shadow:0 0 5px 1.5px rgba(255,206,110,.75),0 0 0 .5px rgba(120,70,20,.35);transform-origin:50% 100%;animation:cbsrFlm 2s ease-in-out infinite}
/* 대화(11-24 목사님): 사서의 말 · 나의 혼잣말 · 선택지 */
#cbsrShelf .dg{position:absolute;inset:0;z-index:8;pointer-events:none}
#cbsrShelf .dg.late{animation-delay:1.05s}
#cbsrShelf .dg .dgs{position:absolute;left:0;right:0;bottom:0;height:400px;background:linear-gradient(to top,rgba(10,7,5,.95) 0,rgba(10,7,5,.8) 34%,rgba(10,7,5,0) 100%)}
#cbsrShelf .dg.me .dgs{height:230px}
#cbsrShelf .dg .dgw{position:absolute;left:12px;right:12px;bottom:14px;display:flex;flex-direction:column}
#cbsrShelf .dg .dgr{display:flex;align-items:flex-end;justify-content:flex-end;gap:6px;min-height:8px}
#cbsrShelf .dg .dgp{flex:none;width:164px;height:auto;margin:0 auto -30px -18px;pointer-events:none}
#cbsrShelf .dg .dgc{flex:1;min-width:0;display:flex;flex-direction:column;gap:8px;margin-bottom:26px;pointer-events:auto}
#cbsrShelf .dg.me .dgc{margin-bottom:26px}
#cbsrShelf .dg .dgc button{height:48px;padding:0 12px 0 14px;display:flex;align-items:center;gap:8px;text-align:left;background:rgba(24,16,10,.94);border:1px solid #d9b56a;color:#f6e7c1;font:700 16px/1.2 "Gowun Batang","Noto Serif KR",serif;letter-spacing:-.01em;box-shadow:0 4px 12px rgba(0,0,0,.5)}
#cbsrShelf .dg .dgc button:before{content:"";flex:none;border:5px solid transparent;border-left:7px solid #e2b24a;border-right:0}
#cbsrShelf .dg .dgc button:first-child{background:#e2b24a;color:#2a1d14;border-color:#e2b24a}
#cbsrShelf .dg .dgc button:first-child:before{border-left-color:#2a1d14}
#cbsrShelf .dg .dgc button:focus-visible,#cbsrShelf .dg .dgb:focus-visible,#cbsrShelf .lbc:focus-visible{outline:3px solid #f6e7c1;outline-offset:2px}
#cbsrShelf .dg .dgb{position:relative;z-index:1;display:block;width:100%;min-height:104px;padding:22px 34px 16px 18px;text-align:left;background:#f1e6c8;border:1px solid #33231a;box-shadow:inset 0 0 0 2px #f1e6c8,inset 0 0 0 3px rgba(51,35,26,.5),0 4px 16px rgba(0,0,0,.6);color:#33231a;font:400 18px/1.65 "Gowun Batang","Noto Serif KR",serif;pointer-events:auto}
#cbsrShelf .dg .dgb b{position:absolute;left:14px;top:-14px;height:27px;padding:0 14px;display:flex;align-items:center;background:#33231a;color:#e6cf9a;border:1px solid #b68d3c;font:700 13px/1 "IBM Plex Sans KR","Apple SD Gothic Neo",sans-serif;letter-spacing:.2em}
#cbsrShelf .dg .dgb i{position:absolute;right:16px;bottom:13px;width:0;height:0;border:6px solid transparent;border-top:8px solid #9b3324;border-bottom:0;animation:cbsrNx 1.2s ease-in-out infinite}
#cbsrShelf .dg.me .dgb{min-height:84px;background:rgba(14,10,7,.88);border-color:rgba(230,207,154,.42);box-shadow:0 4px 18px rgba(0,0,0,.6);color:#f1e6c8}
#cbsrShelf .dg.me .dgb b{background:#f1e6c8;color:#33231a;border-color:#f1e6c8;letter-spacing:0}
#cbsrShelf .dg.me .dgb i{border-top-color:#e2b24a}
#cbsrShelf .lbc{position:absolute;left:12px;bottom:14px;width:66px;padding:0;background:none;border:0;display:flex;flex-direction:column;align-items:center;gap:5px;z-index:4;color:#f6e7c1;font:700 12.5px/1 "IBM Plex Sans KR","Apple SD Gothic Neo",sans-serif;letter-spacing:.15em;text-shadow:0 1px 3px #000}
#cbsrShelf .lbc img{display:block;width:58px;height:58px;border-radius:50%;box-shadow:0 0 0 2px #d9b56a,0 3px 10px rgba(0,0,0,.6)}
#cbsrShelf .lib img{display:block;width:46px;height:46px;border-radius:50%;box-shadow:0 0 0 1px #33231a}
#cbsrShelf .sp.hi{box-shadow:0 0 0 2px #e2b24a,0 0 16px 4px rgba(226,178,74,.6);animation:cbsrGlw 1.6s ease-in-out infinite}
#cbsrShelf .wn.up{top:92px}
#cbsrShelf .dg.np .dgs{height:150px}
/* 말씀 카드(11-24 목사님): 사서가 카드를 패처럼 쥐고 내밈. 고르면 앱의 말씀 뽑기 화면으로 이어짐 */
#cbsrShelf .cds{position:absolute;inset:0;pointer-events:none}
#cbsrShelf .cds .cdp{position:absolute;bottom:96px;height:auto;transform-origin:0 100%}
#cbsrShelf .cds.from .cdp{transform:translate(var(--fx),var(--fy)) scale(var(--fs))}
#cbsrShelf .cds.mv .cdp{transition:transform .8s cubic-bezier(.45,.05,.3,1)}
#cbsrShelf .cds .cdh{position:absolute;width:160px;height:230px;z-index:3}
#cbsrShelf .cdf{position:absolute;width:0;height:0;z-index:2}
#cbsrShelf .cds.from .cdf,#cbsrShelf .cds.from .cdh{opacity:0}
#cbsrShelf .cds.mv .cdf,#cbsrShelf .cds.mv .cdh{transition:opacity .3s .64s}
#cbsrShelf .cdk{position:absolute;left:-40px;top:-160px;width:80px;height:118px;padding:0;transform-origin:50% 135.6%;border-radius:8px;border:1.5px solid #cdb27a;background:linear-gradient(150deg,#5e3420,#331b10);color:#cdb27a;font-size:23px;line-height:1;box-shadow:0 2px 7px rgba(0,0,0,.65),inset 0 0 0 3px #40241a,inset 0 0 0 4px rgba(205,178,122,.5);pointer-events:auto;transition:transform .17s ease,opacity .4s}
#cbsrShelf .cdf.stk .cdk{transform:translate(var(--sx,0),var(--sy,0)) rotate(var(--sr,0deg))}
#cbsrShelf .cdf.open .cdk{transform:rotate(var(--a));transition:transform .45s cubic-bezier(.3,1.2,.5,1),opacity .4s}
#cbsrShelf .cdf.open.now .cdk{transition:none}
#cbsrShelf .cdf.open .cdk:active{transform:rotate(var(--a)) translateY(-10px)}
#cbsrShelf .cdf .cdk.pick{transform:translateY(-10px) rotate(0deg) scale(1.25);z-index:9;transition:transform .6s cubic-bezier(.3,1.2,.5,1);box-shadow:0 0 0 2px #e2b24a,0 6px 22px rgba(226,178,74,.5)}
#cbsrShelf .cdf .cdk.away{opacity:.18}
#cbsrShelf .cdk:focus-visible{outline:3px solid #f6e7c1;outline-offset:2px}
#cbsrShelf .cdmix{position:absolute;right:12px;top:10px;min-width:76px;padding:0 10px;font-size:15px;font-weight:700;z-index:5}
#cbsrShelf .cdmix:disabled{opacity:.45}
/* 내 말로 적어 두기(11-24 목사님: 사서가 묻지 않음. 적고 싶은 사람만 적음) */
#cbsrShelf .bv .cd0{margin:0 0 14px;font:400 15px/1.6 "IBM Plex Sans KR","Apple SD Gothic Neo",sans-serif;color:#e6cf9a}
#cbsrShelf .cdl{display:flex;flex-direction:column;gap:8px}
#cbsrShelf .cdl button{display:flex;align-items:center;gap:12px;width:100%;min-height:62px;padding:7px 12px 7px 8px;text-align:left;background:rgba(246,236,210,.07);border:1px solid rgba(230,207,154,.36);color:#fbf3df}
#cbsrShelf .cdl i{flex:none;font-style:normal;width:46px;height:46px;display:flex;align-items:center;justify-content:center;border:1.5px dashed rgba(230,207,154,.5);border-radius:50%;font:700 12.5px/1 "Gowun Batang","Noto Serif KR",serif;color:rgba(230,207,154,.7)}
#cbsrShelf .cdl i.on{border:2px solid #b5402c;background:radial-gradient(circle at 35% 30%,#cf5a40,#8f2a1c);color:#f8e6c8;box-shadow:inset 0 0 0 3px rgba(0,0,0,.14),0 2px 5px rgba(0,0,0,.5);transform:rotate(-8deg)}
#cbsrShelf .cdl span{flex:1;min-width:0;font:400 16px/1.5 "Gowun Batang","Noto Serif KR",serif;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
#cbsrShelf .cdl span.e{color:rgba(230,207,154,.62);font-size:15px}
#cbsrShelf .cdl button.stp i{animation:cbsrStamp .6s cubic-bezier(.3,1.3,.5,1) both}
#cbsrShelf .cdl button:focus-visible{outline:3px solid #e2b24a;outline-offset:2px}
#cbsrShelf.bye{animation:cbsrOut .62s ease forwards;pointer-events:none}
#cbsrShelf.bye .st>.lay{animation:cbsrAway .62s ease forwards;transform-origin:50% 38%}
@keyframes cbsrOut{0%{opacity:1;filter:brightness(1)}42%{opacity:1;filter:brightness(.28)}100%{opacity:0;filter:brightness(.12)}}
@keyframes cbsrAway{to{transform:scale(.88)}}
@keyframes cbsrUnroll{from{opacity:0;transform:scaleY(.12)}to{opacity:1;transform:none}}
/* 통독표(11-24 목사님): 서고 안에서 서고의 모습으로. 자료는 앱의 통독표와 같음 */
#cbsrShelf .pln{position:absolute;left:12px;right:12px;top:60px;padding:12px 12px 10px;transform-origin:50% 0}
#cbsrShelf .pln.in{animation:cbsrUnroll .5s cubic-bezier(.3,.9,.3,1) both}
#cbsrShelf .plh{display:flex;align-items:center;gap:8px;height:40px;margin-bottom:6px;border-bottom:3px double rgba(51,35,26,.55);padding-bottom:6px}
#cbsrShelf .plh b{flex:none;font:700 19px/1 "Gowun Batang","Noto Serif KR",serif;letter-spacing:.04em}
#cbsrShelf .plh span{flex:1;font-size:13.5px;font-weight:600;color:#6a5646;text-align:right;padding-right:2px}
#cbsrShelf .plh button{flex:none;width:38px;height:38px;padding:0;display:flex;align-items:center;justify-content:center;background:transparent;border:1px solid #33231a;color:#33231a}
#cbsrShelf .plh button:disabled{opacity:.28}
#cbsrShelf .plw,#cbsrShelf .plg{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:3px}
#cbsrShelf .plw span{height:20px;font-size:12px;font-weight:700;text-align:center;color:#6a5646}
#cbsrShelf .plw span:first-child{color:#9b3324}
#cbsrShelf .plc{position:relative;min-width:0;padding:5px 1px 3px;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:2px;background:rgba(51,35,26,.05);border:1px solid rgba(51,35,26,.2);color:#33231a}
#cbsrShelf span.plc{border-color:transparent;background:transparent}
#cbsrShelf span.plc.n b{opacity:.35}
#cbsrShelf .plc b{font:700 15px/1 "Gowun Batang","Noto Serif KR",serif}
#cbsrShelf .plc small{font-size:10.5px;line-height:1.15;font-weight:600;text-align:center;color:#5c4838;word-break:keep-all;overflow-wrap:anywhere;max-width:100%}
#cbsrShelf .plc.on{background:rgba(155,51,36,.1);border-color:rgba(155,51,36,.5)}
#cbsrShelf .plc.on:after{content:"";position:absolute;right:2px;top:2px;width:11px;height:11px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#cf5a40,#8f2a1c);box-shadow:0 1px 2px rgba(0,0,0,.4)}
#cbsrShelf .plc.miss{background:repeating-linear-gradient(135deg,rgba(51,35,26,.2) 0 1.5px,rgba(51,35,26,0) 1.5px 6px)}
#cbsrShelf .plc.today{background:#e2b24a;border:2px solid #33231a;padding:4px 0 2px}
#cbsrShelf .plc.today small{color:#33231a}
#cbsrShelf button.plc:active{background:#d9c59a}
#cbsrShelf button.plc:focus-visible,#cbsrShelf .plh button:focus-visible{outline:3px solid #9b3324;outline-offset:1px}
#cbsrShelf .pll{display:flex;align-items:center;gap:5px;margin:8px 0 0;font-size:12.5px;font-weight:600;color:#5c4838}
#cbsrShelf .pll i{display:inline-block;width:13px;height:13px;margin-left:8px;border:1px solid rgba(51,35,26,.4)}
#cbsrShelf .pll i:first-child{margin-left:0}
#cbsrShelf .pll i.on{border-radius:50%;border:0;background:radial-gradient(circle at 35% 30%,#cf5a40,#8f2a1c)}
#cbsrShelf .pll i.me{background:#e2b24a;border:1.5px solid #33231a}
#cbsrShelf .pll i.miss{background:repeating-linear-gradient(135deg,rgba(51,35,26,.3) 0 1.5px,rgba(51,35,26,0) 1.5px 5px)}
#cbsrShelf .pll button{margin-left:auto;height:28px;padding:0 8px;background:transparent;border:1px solid #33231a;font-size:12.5px;font-weight:700;color:#33231a}
#cbsrShelf .fade{animation:cbsrIn .45s ease both}
@keyframes cbsrIn{from{opacity:0}to{opacity:1}}
@keyframes cbsrZin{from{opacity:0;transform:scale(1.07)}to{opacity:1;transform:none}}
@keyframes cbsrWalk{0%,100%{transform:translateY(0)}12%{transform:translateY(-5px)}25%{transform:translateY(0)}37%{transform:translateY(-5px)}50%{transform:translateY(0)}62%{transform:translateY(-4px)}75%{transform:translateY(0)}87%{transform:translateY(-3px)}}
@keyframes cbsrKb{from{transform:scale(1)}to{transform:scale(1.08) translate(-1.2%,-1%)}}
@keyframes cbsrGlw{0%,100%{opacity:.55;transform:scale(1)}23%{opacity:.95;transform:scale(1.05)}41%{opacity:.7;transform:scale(.98)}64%{opacity:1;transform:scale(1.04)}82%{opacity:.62;transform:scale(1)}}
@keyframes cbsrFlm{0%,100%{transform:rotate(-4deg) scale(1,1)}14%{transform:rotate(5deg) scale(.9,1.1)}29%{transform:rotate(-7deg) scale(1.05,.93)}43%{transform:rotate(3deg) scale(.86,1.16)}57%{transform:rotate(8deg) scale(1,.96)}71%{transform:rotate(-3deg) scale(.92,1.12)}86%{transform:rotate(6deg) scale(1.04,.98)}}
@keyframes cbsrNx{0%,100%{transform:translateY(0)}50%{transform:translateY(4px)}}
@keyframes cbsrBye{to{opacity:0;transform:translateY(8px)}}
@keyframes cbsrStamp{0%{opacity:0;transform:scale(2.4) rotate(8deg)}60%{opacity:1;transform:scale(.92) rotate(-10deg)}100%{opacity:1;transform:scale(1) rotate(-8deg)}}
@keyframes cbsrRay{0%,100%{opacity:.4}50%{opacity:.9}}
@media (prefers-reduced-motion:reduce){#cbsrShelf .amb,#cbsrShelf .bv .bg,#cbsrShelf .fade{animation:none!important}#cbsrShelf .hl,#cbsrShelf .gl,#cbsrShelf .dimv,#cbsrShelf .wk{transition:none!important;animation:none!important}#cbsrShelf .zin,#cbsrShelf .wn.late,#cbsrShelf .mono.late,#cbsrShelf .mono i,#cbsrShelf .dg,#cbsrShelf .dg .dgb i,#cbsrShelf .sp.hi,#cbsrShelf .cdk,#cbsrShelf .cds .cdp,#cbsrShelf .pln.in,#cbsrShelf .cdl button.stp i{animation:none!important}}
`;
var HS=H;
/* 무대는 너비 390에 맞추고, 높이는 화면 비율대로(HS). 가로가 넓은 화면은 높이 600을 채우고 양옆은 흐린 서고 */
function fit(){ if(!stage) return; var vw=innerWidth,vh=innerHeight,s=vw/W,hs=vh/s; if(hs<600){ hs=600; s=vh/600; } HS=Math.round(hs); stage.style.height=HS+"px"; stage.style.transform="translateX(-50%) scale("+s+")"; }
function typing(){ var a=document.activeElement; return !!(a&&root&&root.contains(a)&&a.tagName==="TEXTAREA"); }
function scn(){ return HS<=H?"transform:translateY("+(-(H-HS)*.3).toFixed(1)+"px)":"transform:scale("+(HS/H).toFixed(4)+")"; }
var lastHS=0; function onRs(){ if(!root||typing()) return; fit(); if(busy||Math.abs(HS-lastHS)<3) return; lastHS=HS; flush(); draw(); }
function load(){ if(DATA) return Promise.resolve(DATA); if(LOAD) return LOAD;
  return LOAD=fetch("shelf_66.json").then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); }).then(function(d){ var by={},gs={}; (d.books||[]).forEach(function(b){ by[b.id]=b; (gs[b.group]=gs[b.group]||[]).push(b); }); DATA={by:by,gs:gs,list:d.books||[]}; return DATA; }).catch(function(e){ LOAD=null; throw e; }); }
function say(t){ if(O.toast) O.toast(t); }
/* ---- 사서(11-24 목사님): 말을 걸고 길을 안내함. 묻지 않음. 책 끝의 다섯 가지는 적고 싶은 사람만 적음(도장) ---- */
function LIBR(){ return '<img src="'+IMG+'libr_f.webp'+VER+'" alt="" width="46" height="46">'; }
function libr(t,tmp){ return '<div class="lib tb'+(tmp?" tmp":"")+'" role="status"><span>'+LIBR()+'</span><p><b>사서</b>'+t+'</p></div>'; }   /* tmp: 서가에서는 책을 가리지 않게 잠깐 말하고 물러남 */
var QS=[{f:"who",s:"누가",q:"누가 누구에게 썼습니까?",pg:"cover"},{f:"when",s:"언제",q:"어느 시기의 책입니까?",pg:"cover"},{f:"why",s:"왜",q:"왜 썼습니까?",pg:"why"},{f:"parts",s:"구조",q:"어떤 흐름으로 짜여 있습니까?",pg:"parts"},{f:"god",s:"하나님",q:"이 책에서 하나님은 어떤 분이십니까?",pg:"god"}], ORD=["첫째","둘째","셋째","넷째","다섯째"];
function qaAll(){ try{ if(O.store&&O.store.get) return O.store.get()||{}; return JSON.parse(localStorage.getItem("cbsr_shelf_qa")||"{}"); }catch(e){ return {}; } }
function qaGet(id){ return qaAll()[id]||{}; }
function qaVal(id,f){ var x=qaGet(id)[f]; return x&&x.v?x.v:""; }
function qaSet(id,f,v){ try{ if(O.store&&O.store.set){ O.store.set(id,f,v); return; } var a=qaAll(); a[id]=a[id]||{}; a[id][f]={v:v,t:Date.now()}; localStorage.setItem("cbsr_shelf_qa",JSON.stringify(a)); }catch(e){} }
function qaCount(id){ var g=qaGet(id),n=0; QS.forEach(function(q){ if(g[q.f]&&g[q.f].v) n++; }); return n; }
function qaDone(){ var a=qaAll(),n=0,k; for(k in a) if(qaCount(k)===5) n++; return n; }
function flush(){ var ta=root&&root.querySelector("#cbsrQa"), t=top(); if(!ta||!t||t.t!=="book") return; var v=ta.value.trim(); if(v&&v!==qaVal(t.id,ta.dataset.f)) qaSet(t.id,ta.dataset.f,v); }
/* ---- 대화: 단계(level)마다 dg 하나. who l=사서, me=나의 혼잣말. ch=선택지, tap=말상자를 누르면, esc=빈 곳을 누르면 ---- */
function nick(){ var n=String(O.nick||"").replace(/\s+/g," ").trim(); if(!n) return ""; return /님$/.test(n)?n:(/(목사|전도사|장로|권사|집사|사모|선교사|간사|선생|교수|형제|자매)$/.test(n)?n+"님":n+" 님"); } /* 목사님 11-24: 기본은 부르지 않음. 구글 계정에 닉네임을 정한 분만 그 호칭으로 */
function dgDraw(){ if(!stage) return; var old=stage.querySelector(".dg"), t=top(), d=t&&t.dg; if(old&&old._d===d) return; if(old) old.remove(); if(!d) return;
  var me=d.who==="me", tag=d.tap?"button":"div", h='<div class="dgs"></div><div class="dgw"><div class="dgr">'+((me||d.np)?"":'<img class="dgp" src="'+IMG+'libr.webp'+VER+'" alt="두건을 쓰고 촛대를 든 사서">');
  if(d.ch) h+='<div class="dgc'+(d.ch.length>3?" n4":"")+'">'+d.ch.map(function(c){ return '<button type="button" data-a="'+c.a+'">'+c.t+'</button>'; }).join("")+'</div>';
  h+='</div><'+tag+(d.tap?' type="button" data-a="'+d.tap+'"':' role="status"')+' class="dgb"><b>'+(me?"나":"사서")+'</b><span>'+d.t+'</span>'+(d.tap?"<i></i>":"")+'</'+tag+'></div>';
  var el=document.createElement("div"); el.className="dg fade"+(me?" me":"")+(d.np?" np":"")+(d.late?" late":""); el.innerHTML=h; el._d=d; stage.appendChild(el); }
function ch0(){ var c=[{t:"안내를 받아 이동한다",a:"guide"},{t:"자유롭게 둘러본다",a:"free"}]; if(O.plan) c.push({t:"통독표를 받는다",a:"plan"}); if(O.card) c.push({t:"말씀 카드를 받는다",a:"card"}); return c; } /* 목사님 11-24: 통독표와 말씀 카드도 사서에게 받음 */
function helloDg(how){ var n=nick(); return {who:"l",t:how==="back"?"…더 찾는 것이 있습니까?":(how==="call"?"…부르셨습니까":how==="first"?"…어서 오십시오":"…오셨습니까")+(n?", "+esc(n):"")+".<br>무엇을 찾으십니까?",ch:ch0(),esc:"free"}; }
function hello(how){ var t=levels[0]; if(!t) return; if(!qaVal("_s","met")) qaSet("_s","met","1"); t.dg=helloDg(how); draw(); }
function greet(){ var t=levels[0]; if(qaVal("_s","met")){ hello(); return; } t.dg={who:"me",t:"오래된 서고다. 촛불 몇 개만 켜져 있다.",tap:"hello1",esc:"hello1"}; draw(); }
function bookDg(b){ return {who:"l",t:esc(b.name)+", "+b.chapters+"장입니다.",ch:[{t:"펼쳐 본다",a:"gopen"},{t:"도로 꽂는다",a:"put"}],esc:"put"}; }
function cardHtml(t){ var wp=Math.round(Math.min(300,(HS-152)*.6304)), lf=Math.round((W-wp)/2), px=195, py=HS-160, i;   /* 목사님 11-24: 사서가 화면 가운데로 오고, 카드 패는 그 앞에 */
  var h='<button type="button" class="bk" data-a="back">'+CL+(O.solo?"닫기":"서고")+'</button><div class="ttl"><b class="tb">말씀 카드</b></div><button type="button" class="cdmix tb" data-a="mix">다시 섞기</button><div class="cds" style="--fx:'+(-6-lf)+'px;--fy:8px;--fs:'+(164/wp).toFixed(4)+'"><img class="cdp" src="'+IMG+'libr_c.webp'+VER+'" alt="두건을 쓴 사서가 가운데 서서 카드 일곱 장을 부채꼴로 쥐고 앞으로 내민다" style="left:'+lf+'px;width:'+wp+'px"><div class="cdf stk" style="left:'+px+'px;top:'+py+'px">';
  for(i=0;i<7;i++) h+='<button type="button" class="cdk" data-a="pick" data-i="'+i+'" style="--a:'+((i-3)*13)+'deg" aria-label="'+(i+1)+'번째 카드"><span>✝</span></button>';
  return h+'</div><img class="cdh" src="'+IMG+'libr_h.webp'+VER+'" alt="" style="left:'+(px-80)+'px;top:'+(py-90)+'px"></div>'; }
function cardSay(t,x){ t.dg={who:"l",np:1,t:x}; if(top()===t) dgDraw(); }
function cardMix(t,again){ var f=stage&&stage.querySelector(".cdf"); if(!f) return; var cs=[].slice.call(f.querySelectorAll(".cdk")), mb=stage.querySelector(".cdmix"), n=0, N=again?6:3, r=function(a){ return ((Math.random()*2-1)*a).toFixed(0); }, rm=window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches;
  var done=function(){ busy=false; t.ready=true; if(mb) mb.disabled=false; if(root&&top()===t) cardSay(t,"…한 장 고르십시오."); };
  t.ready=false; if(rm){ f.className="cdf open now"; done(); return; }
  busy=true; f.className="cdf stk"; if(mb) mb.disabled=true; cardSay(t,again?"…다시 섞겠습니다.":"…잠시만 기다리십시오.");
  var step=function(){ if(!root||top()!==t){ busy=false; return; }
    if(n<N){ cs.forEach(function(c){ c.style.setProperty("--sx",r(36)+"px"); c.style.setProperty("--sy",r(10)+"px"); c.style.setProperty("--sr",r(16)+"deg"); c.style.zIndex=String(Math.floor(Math.random()*7)); }); n++; setTimeout(step,170); return; }
    cs.forEach(function(c){ c.style.setProperty("--sx","0px"); c.style.setProperty("--sy","0px"); c.style.setProperty("--sr","0deg"); c.style.zIndex=""; });
    setTimeout(function(){ if(!root||top()!==t){ busy=false; return; } f.className="cdf open"; setTimeout(done,480); },300); };
  step(); }
function planHtml(t){ var P=O.plan&&O.plan.get(t.m), i, x, h; if(!P) return '<div class="pln tb"><p class="pll">통독표가 없습니다.</p></div>'; t.m=P.M; t.ms=P.months; t.mi=P.mi;
  var ch=Math.max(46,Math.min(62,Math.floor((HS-60-14-150)/6)-3));
  h='<div class="pln tb'+(t.seen?"":" in")+'"><div class="plh"><button type="button" data-a="pm" data-d="-1"'+(P.mi>0?"":" disabled")+' aria-label="이전 달">'+CL+'</button><b>'+P.Y+'년 '+(P.Mo+1)+'월</b><span>'+P.r+' / '+P.n+'일 읽음</span><button type="button" data-a="pm" data-d="1"'+(P.mi<P.months.length-1?"":" disabled")+' aria-label="다음 달">'+CR+'</button></div><div class="plw">'+["주일","월","화","수","목","금","토"].map(function(w){ return "<span>"+w+"</span>"; }).join("")+'</div><div class="plg" style="grid-auto-rows:'+ch+'px">';
  for(i=0;i<P.lead;i++) h+='<span class="plc"></span>';
  for(i=1;i<=P.nd;i++){ x=P.days[i-1]; if(!x){ h+='<span class="plc n"><b>'+i+'</b></span>'; continue; }
    h+='<button type="button" class="plc '+x.st+(x.me?" today":"")+'" data-a="pgo" data-k="'+x.w+"-"+x.d+'" aria-label="'+(P.Mo+1)+"월 "+i+"일 "+esc(x.full)+(x.st==="on"?", 읽음":x.st==="miss"?", 안 읽음":x.me?", 오늘":"")+'"><b>'+i+'</b><small>'+esc(x.lab)+'</small></button>'; }
  for(i=P.lead+P.nd;i<42;i++) h+='<span class="plc"></span>';
  t.seen=1; return h+'</div><p class="pll"><i class="on"></i>읽음<i class="me"></i>오늘<i class="miss"></i>안 읽은 지난 날'+((P.M!==P.nowK&&P.hasNow)?'<button type="button" data-a="pnow">이번 달'+CR+'</button>':"")+'</p></div>'; }
function planMonth(t,d){ if(!t.ms) return; var i=t.mi+d; if(i<0||i>=t.ms.length) return; t.m=t.ms[i]; drawHall(t); }
function guide(){ var h=levels[0]; if(busy||top()!==h) return;                                   /* 목사님 11-24: 안내는 오늘 읽는 책으로 */
  load().then(function(D){ if(!root||top()!==h) return; var i=parseInt(O.today,10), b=(i>0&&D.list[i-1])||null;
    if(!b){ h.dg={who:"l",t:"…오늘 읽을 책을 찾지 못했습니다.<br>천천히 둘러보십시오.",tap:"free",esc:"free"}; draw(); return; }
    var s=SEC.ot.g.indexOf(b.group)>=0?"ot":"nt"; h.dg={who:"l",t:"오늘 읽으실 책은 "+esc(b.name)+"입니다.<br>따라오십시오."}; draw(); busy=true;
    setTimeout(function(){ if(!root||top()!==h){ busy=false; return; } h.dg=null; var sc={t:"sec",s:s,gd:b.id}; push(sc);
      setTimeout(function(){ busy=false; if(!root||top()!==sc) return;
        if(!PRESS[b.group]){ sc.dg=bookDg(b); draw(); return; }
        approach(function(){ if(top()!==sc) return; var pr={t:"press",g:b.group,s:s,gd:b.id,dg:bookDg(b)}; sc.gd=null; push(pr); }); },1700); },1500);
  }).catch(function(){ say("책장 원고를 받지 못했습니다. 인터넷 연결을 확인해 주세요."); }); }
/* ---- 단계: 서고 → 구역(구약·신약·그 밖) → 서가 → 책. 뒤로는 한 단계씩(화면의 ‹와 휴대폰의 뒤로 가기가 같은 일) ---- */
function top(){ return levels[levels.length-1]; }
function push(st){ var fn=function(pop){ var i=levels.indexOf(st); if(i<0) return; flush(); levels.length=i; if(pop!==true&&O.done) O.done(fn); draw(st); }; st.fn=fn; levels.push(st); if(O.push) O.push(fn); draw(); }
function back(){ var t=top(); if(busy) return; flush(); if(!t||t.t==="hall"||(t.t==="card"&&O.solo)){ api.close(); return; } t.fn(false); }
function draw(from){ var t=top(); if(!t||!stage) return; if(t.t==="hall"||t.t==="sec"||t.t==="card"||t.t==="plan") drawHall(t); else if(t.t==="press") drawPress(t,from); else if(t.t==="book") drawBook(t); }
/* ---- 서고와 구역 ---- */
function lamps(){ var h="",i=0; ART.hall.lanterns.forEach(function(l){ var x=l[0],y=l[1],s=l[2],g=Math.round(s*1.9),w=Math.max(5,s*.115),fh=w*2.15;
    h+='<div class="amb" style="left:'+(x-g/2)+'px;top:'+(y-g*.46).toFixed(1)+'px;width:'+g+'px;height:'+g+'px;border-radius:50%;background:radial-gradient(circle,rgba(255,232,170,.85) 0%,rgba(255,214,130,.34) 34%,rgba(255,200,110,0) 68%);mix-blend-mode:screen;animation:cbsrGlw '+(2.6+(i%4)*.37)+'s ease-in-out -'+(i*.7)+'s infinite"></div>'+
       '<div class="amb fl" style="left:'+(x-w/2).toFixed(1)+'px;top:'+(y-fh*.56).toFixed(1)+'px;width:'+w.toFixed(1)+'px;height:'+fh.toFixed(1)+'px;animation-duration:'+(1.7+(i%5)*.23)+'s;animation-delay:-'+(i*.43)+'s"></div>'; i++; });
  return h; }
function hallBase(){ var el=stage.querySelector(".hallv"); if(el) return el;
  stage.innerHTML='<div class="lay hallv"><div class="scn"><div class="wk"><div class="hl"><img src="'+IMG+'hall.webp'+VER+'" alt="옛 판화처럼 그린 긴 서고. 촛불이 밝힌 돌바닥 양옆으로 서가가 늘어서 있고, 덧문을 닫은 창 아래 맨 끝은 어둡다">'+
    lamps()+'<div class="zn">'+
      '<button type="button" class="zone" data-s="ot" style="left:0;top:230px;width:168px;height:480px" aria-label="구약 서른아홉 권"><span class="tb" style="top:150px"><b>구약</b><small>서른아홉 권</small></span></button>'+
      '<button type="button" class="zone" data-s="nt" style="left:222px;top:230px;width:168px;height:480px" aria-label="신약 스물일곱 권"><span class="tb" style="top:150px"><b>신약</b><small>스물일곱 권</small></span></button>'+
      '<button type="button" class="zone e" data-s="etc" style="left:140px;top:128px;width:110px;height:196px" aria-label="외경, 위경, 교부 문헌"><span class="tb" style="top:6px"><b>외경 · 위경<br>교부 문헌</b></span></button>'+
    '</div></div></div></div><div class="dimv"></div><div class="ui"></div></div>';
  el=stage.querySelector(".hallv"); el._fresh=true; return el; }
function drawHall(t){ drawHall0(t); dgDraw(); }
function drawHall0(t){ var v=hallBase(), hl=v.querySelector(".hl"), ui=v.querySelector(".ui"), dim=v.querySelector(".dimv"), zn=v.querySelector(".zn"), wk=v.querySelector(".wk"), fresh=v._fresh, cls=(t.t==="sec"&&!(t.s==="etc"&&t.step!=="in"))?" "+t.s:"", moved=(hl.className!=="hl"+cls); v._fresh=false; v.classList.remove("lv"); v.querySelector(".scn").style.cssText=scn(); zn.className="zn"+((t.t==="hall"&&!t.dg)?"":" off"); /* 11-24 목사님: 나올 때 팻말이 따로 움직여 보임 → 팻말을 그림 층에 두고 흐리게 나타나고 사라지게 */
  if(!fresh&&moved){ wk.classList.remove("go"); void wk.offsetWidth; wk.classList.add("go"); } /* 걸어서 그 앞으로(돌아올 때도) */
  hl.className="hl"+cls; dim.className="dimv"+(t.t==="sec"?" on":"");
  if(t.t==="plan"){ dim.className="dimv on now"; ui.innerHTML='<button type="button" class="bk" data-a="back">'+CL+'서고</button><div class="ttl"><b class="tb">통독표</b></div>'+planHtml(t)+(HS>=664?libr("날짜를 누르면 그날 본문으로 갑니다."):""); return; }
  if(t.t==="card"){ dim.className="dimv on now"; ui.innerHTML=cardHtml(t); if(t.ready){ ui.querySelector(".cdf").className="cdf open now"; return; }
    var tm=t.mix, cs0=ui.querySelector(".cds"), go=function(){ if(root&&top()===t&&!t.ready) cardMix(t,tm); }, rm0=window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches; t.mix=false;
    if(t.seen||O.scene==="card"||rm0){ t.seen=1; go(); return; }                                 /* 배너에서 바로 왔거나 다시 그릴 때는 옮겨 오는 움직임 없이 */
    t.seen=1; busy=true; t.dg={who:"l",np:1,t:"…말씀 카드를 드리겠습니다."}; cs0.classList.add("from"); void cs0.offsetWidth; requestAnimationFrame(function(){ cs0.classList.add("mv"); cs0.classList.remove("from"); }); /* 말하던 자리(왼쪽 아래)에서 가운데로 */
    setTimeout(function(){ busy=false; go(); },900); return; }
  if(t.t==="hall"){ ui.innerHTML='<button type="button" class="bk" data-a="back" aria-label="성경 서고 닫기">'+CL+'닫기</button><div class="ttl"><b class="tb">성경 서고</b></div>'+(t.dg?"":'<button type="button" class="lbc fade" data-a="call" aria-label="사서 부르기"><img src="'+IMG+'libr_f.webp'+VER+'" alt=""><span>사서</span></button>');
    return; }
  if(t.s==="etc"){ var bkb='<button type="button" class="bk" data-a="back">'+CL+'서고</button>';
    if(t.step!=="in") ui.innerHTML=bkb+'<div class="wn up tb fade" role="alert" aria-label="경고" style="top:'+Math.max(54,Math.min(92,HS-546))+'px"><h2>'+WARN.t+'</h2><p class="w1">'+WARN.a+'</p><p class="w2">'+WARN.q+'</p></div>';
    else ui.innerHTML=bkb;
    if(t.step!=="in") dim.className="dimv on now";
    return; }
  var S=SEC[t.s], h='<button type="button" class="bk" data-a="back">'+CL+'서고</button><div class="ttl"><b class="tb">'+S.n+'</b></div><span class="cnt">'+S.c+'</span><div class="gl">';
  if(t.gd){ ui.innerHTML=h+'</div>'; return; }                                                   /* 안내를 받아 걷는 동안에는 서가 목록을 띄우지 않음 */
  var N={"모세오경":5,"역사서":12,"시가서":5,"선지서":17,"복음서":4,"사도행전":1,"바울서신":13,"일반서신":8,"요한계시록":1};
  S.g.forEach(function(g){ h+='<button type="button" class="tb" data-g="'+g+'"><b>'+g+'</b><small>'+CNT[N[g]]+'</small></button>'; });
  ui.innerHTML=h+'</div>'+libr(S.n+" "+S.c+"입니다. 서가를 고르십시오."); var gl=ui.querySelector(".gl"); if(fresh){ gl.classList.add("now"); gl.classList.add("on"); return; }
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ gl.classList.add("on"); }); }); }
/* ---- 서가 ---- */
function drawPress(t,from){ drawPress0(t,from); dgDraw(); }
function drawPress0(t,from){ var key=PRESS[t.g], L=ART.labels[key], sw=(key==="pro"?48:56), S=SEC[t.s];
  var k=(HS-50)/802, ty=50-44*k; /* 서가는 너비를 꽉 채우고 높이만 화면에 맞춤(양옆 빈 띠 없음). 글자는 눌리지 않게 되돌림 */
  var h='<div class="lay zin"><div class="bdp"></div><div class="scn pr" style="transform:translateY('+ty.toFixed(1)+'px) scale(1,'+k.toFixed(4)+')"><img class="full" src="'+IMG+'press_'+key+'.webp'+VER+'" alt="'+esc(t.g)+' 서가">';
  var books=(DATA&&DATA.gs[t.g])||[];
  books.forEach(function(b){ var a=L[b.name]; if(!a) return; var two=b.name.length>5, nm=two?esc(b.name.slice(0,b.name.length-2))+"<br>"+esc(b.name.slice(-2)):esc(b.name);
    h+='<button type="button" class="sp'+(t.gd===b.id?" hi":"")+'" data-b="'+b.id+'" aria-label="'+esc(b.name)+' 펼치기" style="left:'+a[0]+'px;top:'+a[1]+'px;width:'+sw+'px;height:'+a[2]+'px"><span style="left:'+a[3]+'px;top:26px;width:'+a[4]+'px;height:'+a[5]+'px"><i style="font-size:'+(16*Math.min(1,k)).toFixed(1)+'px;transform:scaleY('+(1/k).toFixed(4)+')">'+nm+'</i></span></button>'+(qaCount(b.id)===5?'<i class="sl" style="left:'+(a[0]+sw/2-7.5)+'px;top:'+(a[1]+a[2]-34)+'px;transform:scaleY('+(1/k).toFixed(4)+')"></i>':''); });
  stage.innerHTML=h+'</div><button type="button" class="bk" data-a="back">'+CL+S.n+'</button><div class="ttl"><b class="tb">'+esc(t.g)+'</b></div><span class="cnt">'+CNT[Object.keys(L).length]+'</span>'+(t.dg?"":libr(esc(t.g)+" 서가입니다. "+CNT[Object.keys(L).length]+"이 꽂혀 있습니다. 책을 고르면 펼쳐 드립니다.",1))+'</div>'; }
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
  if(b.connection) P.push({k:"link"}); if(b.reading) P.push({k:"read"}); P.push({k:"card"}); return P; }   /* 맨 끝 한 장: 내 말로 적어 두기 */
function sz(s){ var n=(s||"").length; return n>190?" s":n>120?" m":""; }
function drawBook(t){ var b=DATA.by[t.id], P=pages(b); t.n=P.length; t.p=Math.max(0,Math.min(t.p,P.length-1)); var pg=P[t.p], ot=(SEC.ot.g.indexOf(b.group)>=0), m="", bgs=Math.ceil((b.background||[]).length/2)||1;
  var cover=(pg.k==="cover"||pg.k==="verse"), qa=(pg.k==="card"), sheet=false; if(qa) t.ret=null; else t.q=null;
  if(pg.k==="cover"){ m='<p class="k">'+(ot?"구약":"신약")+" · "+esc(b.group)+" · "+b.chapters+'장</p><h1>'+esc(b.name)+'</h1><div class="rule"></div><p class="t m">'+esc(b.line)+'</p>'+(b.verse?'<p class="vq">'+esc(b.verse)+(b.mem100?" · 꼭 외울 말씀 100":"")+'</p>':"")+
      '<dl><dt>저자</dt><dd>'+esc(b.author)+'</dd><dt>수신자</dt><dd>'+esc(b.audience)+'</dd>'+(b.time?'<dt>시기</dt><dd>'+esc(b.time)+'</dd>':"")+'<dt>갈래</dt><dd>'+esc(b.genre)+'</dd></dl>'; }
  else if(pg.k==="verse"){ m='<p class="k">대표 구절</p><p class="t'+sz(b.verseText)+'">'+esc(b.verseText)+'</p><span class="rf">'+esc(b.verse)+" · 개역개정"+(b.mem100?" · 꼭 외울 말씀 100":"")+'</span>'; }
  else if(pg.k==="bg"){ var all=pg.a.map(function(x){return x.text;}).join(""); m='<p class="k">배경'+(bgs>1?" "+pg.n+" / "+bgs:"")+'</p>'+pg.a.map(function(x){ return '<p class="t'+sz(all)+'" style="margin-bottom:0">'+esc(x.text)+'</p><span class="rf">'+esc(x.ref||"")+'</span>'; }).join("")+(pg.last&&b.footnote?'<p class="fn">* '+esc(b.footnote)+'</p>':""); }
  else if(pg.k==="why"){ m='<p class="k">목적 · 왜 썼습니까</p><p class="t'+sz(b.purpose)+'">'+esc(b.purpose)+'</p>'; }
  else if(pg.k==="parts"){ var S=b.structure||[]; m='<p class="k">구조 · 어떻게 흘러갑니까</p><p class="t s">'+esc(b.flow)+'</p><ol>'+S.map(function(x){ return '<li><span>'+esc(x.range)+'</span>'+esc(x.title)+'</li>'; }).join("")+'</ol>'; }
  else if(pg.k==="god"){ m='<p class="k">하나님은 어떤 분이십니까</p><p class="t'+sz(b.god)+'">'+esc(b.god)+'</p>'+((b.themes||[]).length?'<p class="th">'+esc(b.themes.join(" · "))+'</p>':""); }
  else if(pg.k==="link"){ m='<p class="k">연결 · 성경 전체에서</p><p class="t'+sz(b.connection)+'">'+esc(b.connection)+'</p>'; }
  else if(pg.k==="read"){ m='<p class="k">읽기 · 이렇게 읽어 보세요</p><p class="t'+sz(b.reading)+'">'+esc(b.reading)+'</p>'; }
  else { var nq=qaCount(b.id);
    if(t.q!=null&&QS[t.q]){ var Q=QS[t.q], val=qaVal(b.id,Q.f); sheet=true;
      m='<p class="k">내 말로 적어 두기 · '+Q.s+'</p><p class="qq">'+Q.q+'</p><textarea id="cbsrQa" data-f="'+Q.f+'" maxlength="400" placeholder="내 말로 한두 줄 적어 두십시오." aria-label="'+Q.q+'">'+esc(val)+'</textarea><div class="qb"><button type="button" data-a="see" data-pg="'+Q.pg+'">책에서 다시 보기</button><button type="button" class="ans" data-a="ans">적어 두기</button></div>'; }
    else { m='<p class="k">내 말로 적어 두기</p><h2 class="fh">'+(nq===5?"내가 설명하는 "+esc(b.name):esc(b.name)+", 다섯 가지")+'</h2><p class="cd0">'+(nq===5?"도장 다섯 개를 모두 찍었습니다. 줄을 누르면 고쳐 적을 수 있습니다.":"적고 싶은 줄만 눌러서 적어 두십시오. 적은 줄에는 도장이 찍힙니다. 비워 두어도 됩니다.")+'</p><div class="cdl">'+
        QS.map(function(q,i){ var v=qaVal(b.id,q.f); return '<button type="button" data-a="wr" data-i="'+i+'"'+(t.just===i?' class="stp"':"")+' aria-label="'+q.s+(v?", 적어 둠":", 비어 있음")+'"><i'+(v?' class="on"':"")+'>'+q.s+'</i><span'+(v?"":' class="e"')+'>'+esc(v||q.q)+'</span></button>'; }).join("")+'</div>'; t.just=null; } }
  var pr=""; for(var i=0;i<P.length;i++) pr+='<i'+(i<=t.p?' class="on"':"")+'></i>';
  var last=t.p===P.length-1, bkLab=(PRESS[b.group]?"서가":(ot?"구약":"신약"));
  stage.innerHTML='<div class="lay bv"><img class="bg" src="'+IMG+(cover?"bg_road":"bg_lamp")+'.webp'+VER+'" alt=""><div class="sh'+(cover?" c":qa?" q":"")+'"></div><button type="button" class="bb" data-a="back">'+CL+''+bkLab+'</button>'+(pg.k==="cover"?"":'<span class="bn">'+esc(b.name)+'</span>')+
    '<div class="pr" role="img" aria-label="'+(t.p+1)+" / "+P.length+'">'+pr+'</div>'+(qa?"":'<button type="button" class="tap l" data-a="prev" aria-label="앞 장" tabindex="-1"></button><button type="button" class="tap r" data-a="next" aria-label="다음 장" tabindex="-1"></button>')+'<main class="fade'+(qa?" qa":"")+'" aria-live="polite">'+m+'</main>'+
    '<div class="nv">'+(sheet?'<button type="button" data-a="cardback">'+CL+'다섯 가지</button>':'<button type="button" data-a="prev"'+(t.p?"":" disabled")+'>'+CL+'앞 장</button>')+'<button type="button" class="mid" data-a="back" aria-label="'+bkLab+'로 돌아가기">'+(t.p+1)+" / "+P.length+' · 닫기</button>'+((t.ret!=null&&!qa)?'<button type="button" class="go" data-a="ret">적던 곳으로</button>':sheet?'<button type="button" disabled style="visibility:hidden"></button>':last?'<button type="button" class="go" data-a="back">'+bkLab+'로</button>':'<button type="button" data-a="next">다음'+CR+'</button>')+'</div></div>';
  var mn=stage.querySelector("main"), sh=stage.querySelector(".sh"), lim=HS-84-80, f=1, i; if(!mn||!sh) return;
  for(i=0;i<4&&mn.offsetHeight*f>lim;i++){ f=Math.max(.66,f*Math.sqrt(lim/(mn.offsetHeight*f))*.985); mn.style.transformOrigin=qa?"0 0":"0 100%"; mn.style.transform="scale("+f.toFixed(3)+")"; mn.style.width=(342/f).toFixed(1)+"px"; mn.style.right="auto"; }
  var vis=mn.offsetHeight*f; if(!qa&&vis>HS*.5) sh.style.background="linear-gradient(to bottom,rgba(12,9,8,.6) 0%,rgba(12,9,8,.86) "+Math.max(8,Math.round((HS-84-vis-60)/HS*100))+"%,rgba(12,9,8,.97) 100%)"; }
function turn(d){ var t=top(); if(!t||t.t!=="book") return; flush(); if(t.q!=null){ t.q=null; drawBook(t); return; } var p=t.p+d; if(p<0||p>=t.n) return; t.p=p; drawBook(t); }
/* ---- 눌림 ---- */
function approach(cb){ var v=stage.querySelector(".hallv"), rm=window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches; if(!v||rm){ cb(); return; } busy=true; v.classList.add("lv"); setTimeout(function(){ busy=false; if(root) cb(); },440); }
function act(a){ var t=top(); if(!t) return false;                                              /* 대화의 선택지와 말상자 */
  if(a==="back"){ back(); return true; }
  if(a==="hello1"){ hello("first"); return true; }
  if(a==="plan"){ if(!O.plan||busy) return true; t.dg={who:"l",t:"…통독표입니다.<br>여기 있습니다."}; draw(); busy=true; setTimeout(function(){ busy=false; if(root&&top()===t){ t.dg=helloDg("back"); push({t:"plan"}); } },1000); return true; }
  if(a==="pm"||a==="pnow"||a==="pgo"){ return true; }
  if(a==="card"){ if(!O.card||busy) return true;
    if(O.card.had&&O.card.had()){ t.dg={who:"l",t:"…이미 받으신 말씀이 있습니다.<br>여기 있습니다."}; draw(); busy=true; setTimeout(function(){ busy=false; if(root&&top()===t){ t.dg=helloDg("back"); O.card.show(); } },1100); return true; }
    t.dg=helloDg("back"); push({t:"card"}); return true; }
  if(a==="mix"){ if(t.t==="card"&&!busy) cardMix(t,true); return true; }
  if(a==="pick"){ return true; }
  if(a==="call"){ hello("call"); return true; }
  if(a==="free"){ t.dg=null; draw(); return true; }
  if(a==="guide"){ guide(); return true; }
  if(a==="put"){ t.dg=null; t.gd=null; draw(); return true; }
  if(a==="gopen"){ var id=t.gd; t.dg=null; t.gd=null; draw(); if(!id) return true;
    if(t.t==="press"){ var sp=stage.querySelector('.sp[data-b="'+id+'"]'); if(sp){ var r=sp.getBoundingClientRect(), q=stage.getBoundingClientRect(), k=q.width/W; openBook(id,{x:(r.left-q.left)/k,y:(r.top-q.top)/k,w:r.width/k,h:r.height/k}); return true; } }
    approach(function(){ push({t:"book",id:id,p:0,s:t.s}); }); return true; }
  if(a==="enter"){ if(t.t==="sec"&&t.s==="etc"){ t.step="in"; t.dg={who:"me",t:WARN.e,tap:"back",esc:"back",late:1}; drawHall(t); } return true; }
  return false; }
function onClick(e){ if(busy||!root) return; var el=e.target.closest("[data-a],[data-s],[data-g],[data-b]");
  if(!el||!root.contains(el)){ var t0=top(); if(!t0||t0.t==="book"||e.target.closest(".ttl,.cnt,.wn,.gl,.bk,.lib,.dgb,.dgc,.pln")) return;
    if(t0.dg){ if(t0.dg.esc) act(t0.dg.esc); return; }
    if(t0.t==="hall"||t0.t==="card"||t0.t==="plan") return;                                      /* 11-24 목사님: 자유롭게 둘러볼 때는 닫기를 눌러야만 서고에서 나감 */                                           /* 말이 떠 있을 때 빈 곳을 누르면 그 말의 기본 길로 */ /* 11-24 목사님: 빈 곳(배경)을 눌러도 나올 수 있게 */
    if(t0.t==="press"){ var im=stage.querySelector(".scn.pr img"); if(im){ var rr=im.getBoundingClientRect(), fx=(e.clientX-rr.left)/rr.width*W, fy=(e.clientY-rr.top)/rr.height*H; if(fx>24&&fx<366&&fy>84&&fy<790) return; } }
    back(); return; }
  var d=el.dataset;
  if(d.a==="back"){ back(); return; } if(d.a==="next"){ turn(1); return; } if(d.a==="prev"){ turn(-1); return; }
  if(d.a==="pick"){ var tk=top(); if(!tk||tk.t!=="card"||!tk.ready||!O.card) return; var pv=O.card.pick(); if(!pv){ say("말씀을 불러오지 못했습니다. 잠시 뒤에 다시 해 주세요."); return; }
    busy=true; tk.ready=false; el.classList.add("pick"); [].forEach.call(stage.querySelectorAll(".cdk"),function(x){ if(x!==el) x.classList.add("away"); }); var mb2=stage.querySelector(".cdmix"); if(mb2) mb2.style.visibility="hidden"; cardSay(tk,"…받으십시오."); try{ if(navigator.vibrate) navigator.vibrate(20); }catch(er){}
    setTimeout(function(){ busy=false; if(root) O.card.reveal(pv,!O.solo); },850); return; }
  if(d.a==="pm"||d.a==="pnow"||d.a==="pgo"){ var tp=top(); if(!tp||tp.t!=="plan") return; if(d.a==="pm"){ planMonth(tp,+d.d); return; } if(d.a==="pnow"){ tp.m=null; drawHall(tp); return; }
    var wk=String(d.k||"").split("-"); if(O.plan&&O.plan.go) O.plan.go(+wk[0],+wk[1]); return; }
  if(act(d.a)) return;
  if(d.a==="ans"){ var ta=root.querySelector("#cbsrQa"), tb=top(); if(!ta||!tb||tb.t!=="book") return; var av=ta.value.trim(), was=qaVal(tb.id,ta.dataset.f); if(av!==was) qaSet(tb.id,ta.dataset.f,av); ta.blur(); tb.just=(av&&av!==was)?tb.q:null; tb.q=null; drawBook(tb); return; }
  if(d.a==="wr"||d.a==="cardback"||d.a==="see"||d.a==="ret"){ var tc=top(); if(!tc||tc.t!=="book") return; flush();
    if(d.a==="wr"){ tc.q=+d.i; drawBook(tc); var tx=root.querySelector("#cbsrQa"); if(tx){ try{ tx.focus({preventScroll:true}); tx.setSelectionRange(tx.value.length,tx.value.length); }catch(er){} } return; }
    if(d.a==="cardback"){ tc.q=null; drawBook(tc); return; }
    if(d.a==="ret"){ if(tc.ret){ tc.p=tc.ret.p; tc.q=tc.ret.q; tc.ret=null; drawBook(tc); } return; }
    var Pz=pages(DATA.by[tc.id]), iz; for(iz=0;iz<Pz.length;iz++){ if(Pz[iz].k===d.pg){ tc.ret={p:tc.p,q:tc.q}; tc.q=null; tc.p=iz; drawBook(tc); break; } } return; }

  if(d.s){ var ns={t:"sec",s:d.s}; if(d.s==="etc") ns.dg={who:"l",t:"…그쪽은, 성경이 아닙니다.",ch:[{t:"돌아간다",a:"back"},{t:"열람한다",a:"enter"}],esc:"back"}; push(ns); return; }
  if(d.g){ var s=top().s, g=d.g; load().then(function(D){ if(!PRESS[g]){ var one=(D.gs[g]||[])[0]; if(one) approach(function(){ push({t:"book",id:one.id,p:0,s:s}); }); return; } approach(function(){ push({t:"press",g:g,s:s}); }); }).catch(function(){ say("책장 원고를 받지 못했습니다. 인터넷 연결을 확인해 주세요."); }); return; }
  if(d.b){ var r=el.getBoundingClientRect(), q=stage.getBoundingClientRect(), k=q.width/W; openBook(d.b,{x:(r.left-q.left)/k,y:(r.top-q.top)/k,w:r.width/k,h:r.height/k}); } }
function onKey(e){ if(!root) return; if(typing()){ if(e.key==="Escape") document.activeElement.blur(); return; } if(e.key==="Escape"){ e.preventDefault(); back(); } else if(e.key==="ArrowRight") turn(1); else if(e.key==="ArrowLeft") turn(-1); }
var sx=null; function onTs(e){ sx=(e.touches.length===1&&!(e.target.closest&&e.target.closest("textarea")))?e.touches[0].clientX:null; } function onTe(e){ if(sx==null) return; var dx=e.changedTouches[0].clientX-sx; sx=null; if(Math.abs(dx)>56){ var tw=top(); if(tw&&tw.t==="plan") planMonth(tw,dx<0?1:-1); else turn(dx<0?1:-1); } }
var api={ isOpen:function(){ return !!root; },
  open:function(o){ if(root) return true; O=o||{}; levels=[]; busy=false;
    if(!document.getElementById("cbsrShelfCss")){ var st=document.createElement("style"); st.id="cbsrShelfCss"; st.textContent=CSS; document.head.appendChild(st); }
    root=document.createElement("div"); root.id="cbsrShelf"; root.setAttribute("role","dialog"); root.setAttribute("aria-modal","true"); root.setAttribute("aria-label","성경 서고"); root.innerHTML='<div class="st"></div>';
    document.body.appendChild(root); stage=root.firstChild; fit(); lastHS=HS; addEventListener("resize",onRs); root.addEventListener("click",onClick); document.addEventListener("keydown",onKey); root.addEventListener("touchstart",onTs,{passive:true}); root.addEventListener("touchend",onTe,{passive:true}); root.addEventListener("touchmove",function(e){ if(e.target.closest&&e.target.closest("textarea")) return; e.preventDefault(); },{passive:false}); [root,stage].forEach(function(sc){ sc.addEventListener("scroll",function(){ if(sc.scrollTop||sc.scrollLeft){ sc.scrollTop=0; sc.scrollLeft=0; } }); }); /* 낮은 화면(태블릿)에서 아래로 걸친 단추를 누르면 서고가 위로 밀려 위쪽 단추가 잘리던 것을 막음 */ root.addEventListener("focusout",function(){ setTimeout(function(){ if(root&&!typing()) onRs(); },350); });
    document.documentElement.classList.add("shelf-on"); levels.push({t:"hall"}); if(O.scene==="card"&&O.card){ levels[0].dg=helloDg("back"); draw(); push({t:"card",mix:!!O.mix}); } else if(O.back){ hello("back"); } else if(O.book) draw(); else greet(); load().then(function(){ if(O.book&&DATA.by[O.book]) push({t:"book",id:O.book,p:0,s:(SEC.ot.g.indexOf(DATA.by[O.book].group)>=0?"ot":"nt")}); }).catch(function(){});
    root.tabIndex=-1; try{ root.focus({preventScroll:true}); }catch(e){}
    return true; },
  close:function(silent,anim){ if(!root) return; flush(); var deep=levels.slice(1), el=root, rm=window.matchMedia&&matchMedia("(prefers-reduced-motion:reduce)").matches; levels=[]; removeEventListener("resize",onRs); document.removeEventListener("keydown",onKey); root=null; stage=null; busy=false; document.documentElement.classList.remove("shelf-on");
    if((anim||!silent)&&!rm){ el.classList.add("bye"); el.setAttribute("aria-hidden","true"); setTimeout(function(){ el.remove(); },640); } else el.remove();   /* 11-24 목사님: 서고에서 나갈 때의 움직임(다른 화면에 바로 넘겨줄 때는 없이) */
    if(O.done) deep.reverse().forEach(function(st){ if(st.fn) O.done(st.fn); });
    if(!silent&&O.onClose) O.onClose(); } };
window.CBSR_SHELF=api;
})();
