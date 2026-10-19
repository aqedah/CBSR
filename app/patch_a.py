s=open('mapcode.js').read()
s=s.replace('Math.max(map.getZoom(),fid==="israel"?9:7)','Math.max(map.getZoom(),fid==="israel"?8.5:6.5)').replace('{maxZoom:fid==="israel"?10:7,animate:false}','{maxZoom:fid==="israel"?8.5:6.5,animate:false}')
open('mapcode.js','w').write(s)
r=open('readcode.js').read()
r=r.replace('''  const det=DETAIL[key]; const list=[];
  traits.forEach(t=>list.push(t.verse));''','''  const det=DETAIL[key]; const list=[];
  if(det){ const txt=[det.god,det.christ,det.apply].join(" ");
    for(const m of txt.matchAll(/\\((\\d+):(\\d+)\\)/g)){ const v=A.verses.find(x=>x.c===+m[1]&&x.v===+m[2]); if(v) list.push(v); } }
  traits.forEach(t=>list.push(t.verse));''')
r=r.replace('const n=qtVerses(A,godTraits(A),"").length;','const n=qtVerses(A,godTraits(A),view.w+"-"+(view.d+1)).length;')
open('readcode.js','w').write(r)
