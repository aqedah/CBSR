/* 본문에서 하나님의 성품 찾기 */
const DIVINE=/(하나님|여호와|주께서|주께|주의|주는|주여|주님|예수|그리스도|성령|아버지께|아버지는|아버지여|전능자|지존자|만군의)/;
const ATTRS=[
 {n:"거룩하신 하나님",p:"거룩하신",re:/거룩하시|거룩하니|거룩하다|거룩한 이|거룩하신|거룩하심|거룩함이니/},
 {n:"사랑하시는 하나님",p:"우리를 사랑하시는",re:/사랑하시|사랑하사|사랑하셨|사랑하심|사랑을/},
 {n:"긍휼이 많으신 하나님",p:"긍휼이 많으신",re:/긍휼|불쌍히|자비/},
 {n:"인자하신 하나님",p:"인자하신",re:/인자하|인애|인자가|인자를|인자는|인자와/,ot:true},
 {n:"은혜로우신 하나님",p:"은혜로우신",re:/은혜를 베푸|은혜로|은혜가|은혜를 주|은혜와/},
 {n:"의로우신 하나님",p:"의로우신",re:/공의|정의|의로우|의로운|공평/},
 {n:"신실하신 하나님",p:"약속을 지키시는 신실하신",re:/신실|성실|미쁘|진실하/},
 {n:"능력의 하나님",p:"능력이 크신",re:/능력으로|능력이|하나님의 능력|권능|전능하/},
 {n:"지혜로우신 하나님",p:"지혜로우신",re:/지혜/},
 {n:"오래 참으시는 하나님",p:"오래 참으시는",re:/오래 참|노하기를 더디|인내/},
 {n:"심판하시는 하나님",p:"죄를 그냥 두지 않으시는 공의의",re:/심판|진노|벌하|노하사|노하시/},
 {n:"용서하시는 하나님",p:"죄를 용서하시는",re:/(?<![가-힣])(사하시|사하셨|사하리|사하여 주|사하는)|용서하시|용서하셨|용서하리|씻으시|깨끗하게 하시/},
 {n:"기억하시는 하나님",p:"우리를 잊지 않고 기억하시는",re:/기억하/},
 {n:"구원하시는 하나님",p:"구원하시는",re:/구원하시|구원하셨|구원하리|구원을 베푸|구원이|건지시|건지셨|건지리|속량하/},
 {n:"돌보시는 하나님",p:"필요를 채우시는",re:/먹이|입히|돌보|채우|공급|기르/},
 {n:"함께하시는 하나님",p:"늘 함께하시는",re:/함께 하시|함께하시|함께 하리|함께하리|함께 있으리|함께 있으시|너를 떠나지 아니|버리지 아니하/},
 {n:"목자 되시는 하나님",p:"목자 되시는",re:/목자/},
 {n:"창조주 하나님",p:"모든 것을 지으신",re:/창조|지으시|지으신|만드시|만드신/},
 {n:"약속하시는 하나님",p:"약속하시는",re:/약속하|약속을|언약을 기억|언약을 세우|내 언약/},
 {n:"들으시는 하나님",p:"기도를 들으시는",re:/들으시|응답/},
 {n:"다스리시는 하나님",p:"온 세상을 다스리시는",re:/다스리|왕이시|보좌|통치/},
 {n:"생명을 주관하시는 하나님",p:"생명을 주관하시는",re:/생명을 주관하시/}
];
function near(t,re){
  const di=[...t.matchAll(new RegExp(DIVINE.source,"g"))].map(m=>m.index); if(!di.length) return false;
  const ai=[...t.matchAll(new RegExp(re.source,"g"))].map(m=>m.index);
  return ai.some(a=>di.some(d=>Math.abs(a-d)<=22)) && !/거짓 (그리스도|선지자)|맹세하는 자|희롱|조롱|비웃|모욕/.test(t);
}
function godTraits(A){
  /* 사람이 장마다 골라 둔 성품이 있으면 그것을 씁니다 */
  if(typeof TRAITS_C!=="undefined"){ const chs=[...new Set(A.verses.map(v=>v.b+"-"+v.c))]; if(chs.some(k=>TRAITS_C[k])){
    const out=[], seen=new Set();
    for(const k of chs) for(const x of (TRAITS_C[k]||[])){ if(seen.has(x.n)) continue; const [b,c]=k.split("-").map(Number); const v=A.verses.find(y=>y.b===b&&y.c===c&&y.v===x.v); const at=ATTRS.find(a=>a.n===x.n); if(!v||!at) continue; seen.add(x.n); out.push({at,vs:[v],verse:v}); }
    /* 여러 장이면 장마다 고르게 앞에 오도록 */
    return out.slice(0,6); } }
  const res=[];
  for(const at of ATTRS){
    const vs=A.verses.filter(v=>(!at.ot||v.b<40)&&near(v.t,at.re));
    if(vs.length) res.push({at,vs});
  }
  res.sort((a,b)=>b.vs.length-a.vs.length);
  return res.slice(0,3).map(x=>{
    const pickV=x.vs.slice().sort((a,b)=>Math.abs(a.t.length-70)-Math.abs(b.t.length-70))[0];
    return {...x,verse:pickV};
  });
}
