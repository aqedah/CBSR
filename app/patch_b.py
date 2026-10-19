r=open('readcode.js').read()
old_med='''  h+=`<div class="qcard"><p>${esc(det&&det.apply?det.apply:APPLY_Q)}</p></div><textarea id="qt-med" data-qt="med" placeholder="오늘 말씀 앞에서 내가 할 한 가지">${esc(q.med||"")}</textarea></section>`;'''
new_med='''  h+=`<div class="qcard"><span class="k">이 구절과 함께 생각하기</span><p>${esc(kv?verseQuestion(kv):(det&&det.apply?det.apply:APPLY_Q))}</p>${kv&&det&&det.apply?`<p class="clue">오늘 본문 전체 적용: ${esc(det.apply)}</p>`:""}</div><textarea id="qt-med" data-qt="med" placeholder="오늘 말씀 앞에서 내가 할 한 가지">${esc(q.med||"")}</textarea></section>`;'''
assert old_med in r; r=r.replace(old_med,new_med)
i=r.index('  const ph=traits[0]?traits[0].at.p:"사랑의";'); j=r.index('\n',r.index('  const pray=`'))
r=r[:i]+'  const pray=makePrayer(key,vi,q.pv,p.label,kv,traits);'+r[j:]
old_btn='<span class="lead" id="qtSaved"></span></div></section>`;'
assert old_btn in r
r=r.replace('<p class="prayer">${esc(pray)}</p>','<p class="prayer">${esc(pray)}</p><div class="row"><button class="btn ghost small" id="qtNextP">다른 기도문</button></div>')
r=r.replace('''  const dn=document.getElementById("qtDone");''','''  const np=document.getElementById("qtNextP"); if(np) np.onclick=()=>{q.pv=(q.pv||0)+1; save(); const y=window.scrollY; render(); window.scrollTo({top:y});};
  const dn=document.getElementById("qtDone");''')
r+="\n"+open('prayers.js').read()
open('readcode.js','w').write(r)
print('patched')
