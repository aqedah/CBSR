/* A5 4쪽 맞춤 (11-24 목사님)
   1쪽: 남는 자리를 쪽 아래에 몰지 않고 나눔(칸 머리 앞 → 항목 사이).
   4쪽: 해설과 성경 전체로가 넘치면 해설 장평을, 다음에 성경 전체로 장평을 줄이고(0.9까지), 그래도 넘치면 성경 전체로를 뒤에서부터 덜어 기도 칸을 지킴. */
function fit4(p1, p4){
  const MM=96/25.4, out={dropped:0, scale:1, wscale:1};
  if(p1){ const bx=p1.querySelector('.bx5');
    const slack=()=>{ const t=bx.getBoundingClientRect().top; let mb=0; [...bx.children].forEach(e=>{const r=e.getBoundingClientRect(); if(r.bottom>mb) mb=r.bottom}); return (bx.clientHeight-(mb-t))/MM - 1.5; };
    const bump=(els,cap,prop)=>{ els=els.filter(Boolean); if(!els.length) return; const sl=slack(); if(sl<=0) return; const add=Math.min(sl/els.length,cap); els.forEach(g=>{ g.style[prop]=(parseFloat(getComputedStyle(g)[prop])/MM+add)+'mm'; }); };
    bump([...bx.querySelectorAll(':scope > .sh')].slice(1),6,'marginTop');
    bump([...bx.querySelectorAll(':scope > .mk, :scope > .lk')],2.6,'marginBottom');
    bump([...bx.querySelectorAll(':scope > .blk p')],1.6,'marginBottom');
    bump([...bx.querySelectorAll(':scope > .sh')],3,'marginTop');
    if(bx.lastElementChild) bx.lastElementChild.style.marginBottom='0';
  }
  if(p4){ const bx=p4.querySelector('.bx5'); const over=()=>bx.scrollHeight>bx.clientHeight+1; const note=bx.querySelector('.note');
    const sq=(els,k)=>els.forEach(e=>{ e.style.transformOrigin='left top'; e.style.transform=`scaleX(${k})`; e.style.width=(100/k)+'%'; });
    for(const k of [0.96,0.93,0.9]){ if(!over()||!note) break; sq([note],k); out.scale=k; }
    const whs=[...bx.querySelectorAll(':scope > .wh')];
    for(const k of [0.96,0.93,0.9]){ if(!over()||!whs.length) break; sq(whs,k); out.wscale=k; }
    let wh=[...bx.querySelectorAll(':scope > .wh')];
    while(over()&&wh.length>1){ wh.pop().remove(); out.dropped++; }
  }
  return out; }
