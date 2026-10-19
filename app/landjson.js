const topo=require('./npm/node_modules/topojson-client');const fs=require('fs');
for(const r of ['50m','10m']){const t=JSON.parse(fs.readFileSync(`npm/node_modules/world-atlas/land-${r}.json`));const f=topo.feature(t,t.objects.land);
const polys=f.features.flatMap(ft=>ft.geometry.type==="Polygon"?[ft.geometry.coordinates]:ft.geometry.coordinates).filter(p=>p[0].some(([lo,la])=>lo>5&&lo<55&&la>15&&la<48));
fs.writeFileSync(`land${r.replace('m','')}.json`,JSON.stringify(polys));console.log(r,polys.length);}
