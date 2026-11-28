/* 11-28 목사님: 문단 마지막 줄에 두세 글자('다.', '니까?', '멘.')만 남으면 그 문단만 자간을 조금씩(최대 -0.04em) 줄여 윗줄로 끌어올림. 그래도 안 올라가면 그대로 둠. */
function wLines(el){ const r=document.createRange(); r.selectNodeContents(el); const rs=[...r.getClientRects()].filter(x=>x.width>0.3&&x.height>0.3); if(!rs.length) return {n:0,last:0};
  const fs=parseFloat(getComputedStyle(el).fontSize)*(el.getBoundingClientRect().width/(el.offsetWidth||1)||1); const L=[];
  rs.forEach(x=>{ const c=(x.top+x.bottom)/2; let g=L.find(l=>Math.abs(l.c-c)<fs*0.55); if(!g){ g={c,l:x.left,r:x.right}; L.push(g) } else { g.l=Math.min(g.l,x.left); g.r=Math.max(g.r,x.right) } });
  L.sort((a,b)=>a.c-b.c); const z=L[L.length-1]; return {n:L.length,last:z.r-z.l,fs} }
function widow(root){ root.querySelectorAll('.pg *, .p5 *').forEach(el=>{
  if(el.closest('svg')||(typeof inMini==='function'&&inMini(el,root))) return;
  if(![...el.childNodes].some(n=>n.nodeType===3&&/[가-힣]/.test(n.textContent))) return;
  if(el.querySelector(':scope > div, :scope > p, :scope > ul, :scope > ol, :scope > table, :scope > section')) return;
  const cs=getComputedStyle(el); if(!/^(block|list-item|flow-root)$/.test(cs.display)||/nowrap|pre/.test(cs.whiteSpace)) return;
  const a=wLines(el); if(a.n<2||a.last>a.fs*3.3) return;
  const fs=parseFloat(cs.fontSize), base=(parseFloat(cs.letterSpacing)||0)/fs, keep=el.style.letterSpacing;
  for(const d of [0.01,0.02,0.03,0.04]){ el.style.letterSpacing=(base-d).toFixed(3)+'em'; if(wLines(el).n<a.n) return; }
  el.style.letterSpacing=keep; }) }
