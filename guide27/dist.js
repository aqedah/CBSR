(function(){
 const d=document.createElement('div');d.style.cssText='position:absolute;width:100mm';document.body.appendChild(d);const MM=d.getBoundingClientRect().width/100;d.remove();
 function slackOf(pg){const pr=pg.getBoundingClientRect();const ab=pg.querySelector('.after');const lim=ab?ab.getBoundingClientRect().top:pr.bottom-11*MM;let mb=0;pg.querySelectorAll(':scope > *:not(.after):not(.pn)').forEach(e=>{const q=e.getBoundingClientRect();if(q.bottom>mb)mb=q.bottom});return (lim-mb)/MM;}
 const RES=1.5;
 document.querySelectorAll('.pg').forEach(pg=>{
  const right=pg.classList.contains('r');
  const bump=(els,cap,prop)=>{els=els.filter(Boolean);if(!els.length)return;const sl=slackOf(pg)-RES;if(sl<=0)return;const add=Math.min(sl/els.length,cap);els.forEach(g=>{const cs=getComputedStyle(g);g.style[prop]=(parseFloat(cs[prop])/MM+add)+'mm';});};
  if(right){
   const lnw=[...pg.querySelectorAll(':scope > .lnw')];
   const order=[0,2,3,1].filter(i=>lnw[i]);let k=0,guard=0;
   while(slackOf(pg)>5.9+RES+2&&guard++<12){const w=lnw[order[k%order.length]];const l=document.createElement('div');l.className='ln';w.appendChild(l);k++;}
   bump([...pg.querySelectorAll(':scope > .lab')],3,'marginTop');
  } else {
   const secs=[...pg.querySelectorAll(':scope > .sec')].slice(1).concat([...pg.querySelectorAll(':scope > .lab')]);
   bump(secs,6,'marginTop');
   bump([...pg.querySelectorAll('.mk .mi, .lk .i')],2.6,'marginBottom');
   bump([pg.querySelector(':scope > .sec'),pg.querySelector(':scope > .wd')],2,'marginTop');
  }
 });
})();
