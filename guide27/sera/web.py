import sys, importlib, json
sys.path.insert(0, '.')
import build
KEYS = sys.argv[2:]; OUT = sys.argv[1]
ws = [importlib.import_module('w'+k).W for k in KEYS]
body = ''
for w in ws:
    body += f'<div class="wk" id="w{w["key"]}" style="--c:{w["color"]};--l:{w["light"]};--hl:{w.get("hl","#F3E6A0")}">' + build.page1(w) + build.page2(w) + build.page3(w) + build.page4(w, edit=True) + '</div>'
btns = ''.join(f'<button data-w="{w["key"]}">{w["date"].split(" (")[0]}<small>{w["title"]}</small></button>' for w in ws)
html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>세라핌 기도회 묵상지</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&family=Noto+Serif+KR:wght@300;400;700&display=swap" rel="stylesheet">
<style>{build.CSS}
html{{background:#e9e9e9}}
.bar{{position:sticky;top:0;z-index:9;background:#222;color:#fff;font-family:"Noto Sans KR",sans-serif;padding:8px 12px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.bar button{{font:inherit;font-size:13px;border:1px solid #666;background:#333;color:#fff;border-radius:6px;padding:4px 10px;cursor:pointer;line-height:1.3;text-align:left}}
.bar button small{{display:block;font-size:10px;opacity:.7}}
.bar button.on{{background:#fff;color:#222}}
.bar .pr{{margin-left:auto;background:#5B3E8A;border-color:#5B3E8A;font-weight:700}}
.tip{{width:100%;font-size:12px;opacity:.8;margin-top:2px}}
.wk{{display:none}} .wk.on{{display:block}}
.wk .pg{{margin:14px auto;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.2)}}
.prow span:empty::before{{content:"이름";color:#ccc}}
@media print{{html{{background:#fff}}.bar{{display:none}}.wk .pg{{margin:0;box-shadow:none}}[contenteditable]:focus{{background:none}}.prow span:empty::before{{content:none}}}}
</style></head><body>
<div class="bar"><b style="margin-right:6px">세라핌 묵상지</b>{btns}<button class="pr" onclick="print()">인쇄 / PDF 저장</button>
<div class="tip">4쪽 오늘의 기도 칸을 눌러 기도제목을 입력하세요. 입력한 내용은 이 기기에 저장됩니다. 인쇄할 때 용지는 A4, 여백 없음, 배경 그래픽 켜기로 하세요.</div></div>
{body}
<script>
const K='sera_pray_';
function store(){{try{{return JSON.parse(localStorage.getItem(K)||'{{}}')}}catch(e){{return {{}}}}}}
function save(d){{try{{localStorage.setItem(K,JSON.stringify(d))}}catch(e){{}}}}
const d=store();
document.querySelectorAll('.wk').forEach(wk=>{{
  const id=wk.id;
  const fs=[...wk.querySelectorAll('[contenteditable]')];
  fs.forEach((f,i)=>{{
    const k=id+'_'+f.dataset.k; if(d[k]) f.textContent=d[k];
    f.addEventListener('input',()=>{{const x=store();x[k]=f.textContent;save(x)}});
    f.addEventListener('keydown',e=>{{if(e.key==='Enter'){{e.preventDefault();(fs[i+1]||f).focus()}}}});
    f.addEventListener('paste',e=>{{e.preventDefault();document.execCommand('insertText',false,(e.clipboardData.getData('text')||'').replace(/\\s+/g,' '))}});
  }});
}});
function show(k){{document.querySelectorAll('.wk').forEach(w=>w.classList.toggle('on',w.id==='w'+k));document.querySelectorAll('.bar button[data-w]').forEach(b=>b.classList.toggle('on',b.dataset.w===k));history.replaceState(null,'','?w='+k)}}
document.querySelectorAll('.bar button[data-w]').forEach(b=>b.onclick=()=>show(b.dataset.w));
const q=new URLSearchParams(location.search).get('w');
const ks={json.dumps(KEYS)};
const today=new Date();const md=String(today.getMonth()+1).padStart(2,'0')+String(today.getDate()).padStart(2,'0');
show(ks.includes(q)?q:(ks.find(k=>k.padStart(4,'0')>=md)||ks[ks.length-1]));
function fit(){{const z=Math.min(1,(innerWidth-8)/800);document.querySelectorAll('.wk').forEach(w=>w.style.zoom=z)}}
addEventListener('resize',fit);fit();
addEventListener('beforeprint',()=>document.querySelectorAll('.wk').forEach(w=>w.style.zoom=1));
addEventListener('afterprint',fit);
</script></body></html>'''
open(OUT,'w').write(html)
print('ok', len(html))
