# '적어 두기'(mem.shq)가 두 기기의 기록을 합칠 때 사라지지 않는지: 앱 원본(app/template3.html)의 mergeMem을 그대로 꺼내 확인
import io, json, subprocess, sys, tempfile, os
src = io.open(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/cbsr/app/template3.html', encoding='utf-8').read()
i = src.index('function mergeMem(a,b){'); d = 0; j = i
while True:
    c = src[j]
    if c == '{': d += 1
    elif c == '}':
        d -= 1
        if d == 0: break
    j += 1
fn = src[i:j + 1]
js = fn + r'''
let n=0, fails=[]; const chk=(name,ok)=>{ n++; console.log((ok?"  통과 ":"  실패 ")+name); if(!ok) fails.push(name); };
const M=(a,b)=>mergeMem(JSON.parse(JSON.stringify(a)),JSON.parse(JSON.stringify(b)));
const A={shq:{gen:{who:{v:"모세가 썼다",t:100}}}}, B={shq:{gen:{when:{v:"광야에서",t:200}},mat:{god:{v:"함께하시는 분",t:150}}}};
const r=M(A,B), r2=M(B,A), S=o=>JSON.stringify(o,Object.keys(o).sort());
chk("서로 다른 칸은 둘 다 남음", r.shq.gen.who.v==="모세가 썼다"&&r.shq.gen.when.v==="광야에서"&&r.shq.mat.god.v==="함께하시는 분");
chk("합치는 순서를 바꿔도 같음", r2.shq.gen.who.v==="모세가 썼다"&&r2.shq.gen.when.v==="광야에서"&&r2.shq.mat.god.v==="함께하시는 분");
const A2={shq:{gen:{who:{v:"먼저 적은 글",t:100}}}}, B2={shq:{gen:{who:{v:"나중에 고친 글",t:300}}}};
chk("같은 칸은 나중에 적은 글이 남음", M(A2,B2).shq.gen.who.v==="나중에 고친 글"&&M(B2,A2).shq.gen.who.v==="나중에 고친 글");
const A3={shq:{gen:{who:{v:"",t:400}}}};
chk("지운 뒤에 옛 글이 되살아나지 않음", M(A3,B2).shq.gen.who.v===""&&M(B2,A3).shq.gen.who.v==="");
chk("한쪽에만 있어도 남음", M(A,{}).shq.gen.who.v==="모세가 썼다"&&M({},A).shq.gen.who.v==="모세가 썼다");
chk("둘 다 없으면 만들지 않음", !("shq" in M({},{})));
const big={shq:{}}; for(let k=0;k<66;k++){ big.shq["b"+k]={}; for(const f of ["who","when","why","parts","god"]) big.shq["b"+k][f]={v:"가".repeat(400),t:k+1}; }
const rb=M(big,A); let cnt=0; for(const k in rb.shq) for(const f in rb.shq[k]) cnt++;
chk("예순여섯 권 다섯 칸을 가득 채워도 하나도 빠지지 않음("+cnt+"칸)", cnt===66*5+1);
console.log("실패:", fails.length?fails:"없음", "("+n+"가지)");
'''
f = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8'); f.write(js); f.close()
r = subprocess.run(['node', f.name], capture_output=True, text=True); os.unlink(f.name)
print(r.stdout[-1500:], r.stderr[-800:])
