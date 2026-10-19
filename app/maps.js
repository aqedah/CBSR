const topo=require('./npm/node_modules/topojson-client');
const fs=require('fs');
const frames={
 israel:{name:"이스라엘 땅",lon:[33.9,36.9],lat:[29.4,33.8],res:'10m'},
 asia:{name:"소아시아와 그리스",lon:[21.3,31.0],lat:[36.2,41.6],res:'10m'},
 med:{name:"지중해 세계",lon:[11,37.8],lat:[30.3,42.6],res:'50m'},
 neareast:{name:"고대 근동",lon:[24,50],lat:[21.5,40.5],res:'50m'}
};
const water={
 lakes:[[[32.88,35.60],[32.85,35.65],[32.78,35.65],[32.71,35.59],[32.72,35.55],[32.80,35.52],[32.86,35.54]],
        [[31.77,35.47],[31.75,35.56],[31.55,35.55],[31.35,35.53],[31.10,35.45],[31.05,35.40],[31.20,35.38],[31.45,35.40],[31.62,35.42]]],
 rivers:[[[33.10,35.62],[32.90,35.62]],[[32.71,35.57],[32.40,35.56],[32.10,35.53],[31.78,35.55]],
   [[31.40,30.41],[30.10,31.20]],[[31.47,31.85],[30.10,31.25]],[[30.05,31.23],[29.0,30.9],[27.2,31.2],[26.2,32.6],[25.7,32.65],[24.1,32.9],[22.0,31.4]],
   [[36.83,38.01],[35.95,39.0],[35.3,40.4],[34.4,40.9],[33.4,43.3],[32.54,44.42],[31.3,45.9],[30.95,46.9],[30.4,47.9]],
   [[37.5,42.0],[36.36,43.15],[35.4,43.4],[34.2,43.9],[33.3,44.4],[32.5,45.8],[31.0,47.4],[30.4,47.9]]]
};
const out={};
for(const [id,f] of Object.entries(frames)){
  const t=JSON.parse(fs.readFileSync(`npm/node_modules/world-atlas/land-${f.res}.json`));
  const land=topo.feature(t,t.objects.land);
  const latm=(f.lat[0]+f.lat[1])/2, kx=Math.cos(latm*Math.PI/180);
  const W=1000, sx=W/((f.lon[1]-f.lon[0])*kx), H=Math.round((f.lat[1]-f.lat[0])*sx);
  const P=(lon,lat)=>[(lon-f.lon[0])*kx*sx,(f.lat[1]-lat)*sx];
  const clip=(pts)=>{ // Sutherland-Hodgman against [-5,W+5]x[-5,H+5]
    const edges=[[p=>p[0]>=-5,(a,b)=>{const t=(-5-a[0])/(b[0]-a[0]);return[-5,a[1]+t*(b[1]-a[1])]}],
      [p=>p[0]<=W+5,(a,b)=>{const t=(W+5-a[0])/(b[0]-a[0]);return[W+5,a[1]+t*(b[1]-a[1])]}],
      [p=>p[1]>=-5,(a,b)=>{const t=(-5-a[1])/(b[1]-a[1]);return[a[0]+t*(b[0]-a[0]),-5]}],
      [p=>p[1]<=H+5,(a,b)=>{const t=(H+5-a[1])/(b[1]-a[1]);return[a[0]+t*(b[0]-a[0]),H+5]}]];
    for(const [inside,inter] of edges){ const res=[]; for(let i=0;i<pts.length;i++){const cur=pts[i],prev=pts[(i+pts.length-1)%pts.length];
      if(inside(cur)){ if(!inside(prev)) res.push(inter(prev,cur)); res.push(cur);} else if(inside(prev)) res.push(inter(prev,cur)); } pts=res; if(!pts.length) break; }
    return pts;
  };
  let d="";
  const polys=land.features.flatMap(ft=>ft.geometry.type==="Polygon"?[ft.geometry.coordinates]:ft.geometry.coordinates);
  for(const poly of polys) for(const ring of poly){
    let pts=ring.map(([lo,la])=>P(lo,la));
    // quick reject
    if(pts.every(p=>p[0]<-5)||pts.every(p=>p[0]>W+5)||pts.every(p=>p[1]<-5)||pts.every(p=>p[1]>H+5)) continue;
    pts=clip(pts); if(pts.length<3) continue;
    const s=[pts[0]]; for(const p of pts){const l=s[s.length-1]; if(Math.hypot(p[0]-l[0],p[1]-l[1])>1.2) s.push(p);}
    if(s.length<3) continue;
    d+="M"+s.map(p=>p[0].toFixed(0)+" "+p[1].toFixed(0)).join("L")+"Z";
  }
  const line=pts=>"M"+pts.map(([la,lo])=>P(lo,la).map(v=>v.toFixed(0)).join(" ")).join("L");
  out[id]={name:f.name,lon:f.lon,lat:f.lat,kx,sx,W,H,land:d,lakes:water.lakes.map(l=>line(l)+"Z").join(""),rivers:water.rivers.map(line).join("")};
  console.log(id,W,H,d.length);
}
fs.writeFileSync('maps.json',JSON.stringify(out));
