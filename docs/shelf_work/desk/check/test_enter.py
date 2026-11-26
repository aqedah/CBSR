# 서고를 열면 문을 지나 걸어 들어감(11-26) · 누르면 건너뜀
import sys, subprocess, time
from playwright.sync_api import sync_playwright
OUT='/home/claude/shelf-desk/check/dlg/'
srv=subprocess.Popen([sys.executable,'-m','http.server','8765'],cwd='/tmp/shelftest',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
ok=[]; errs=[]
def chk(n,c): ok.append((n,bool(c))); print(('  통과 ' if c else '  실패 ')+n)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for tag,vw,vh in (('phone',390,800),('tablet',820,1180)):
      cx=b.new_context(viewport={'width':vw,'height':vh},has_touch=True); pg=cx.new_page(); pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.goto('http://localhost:8765/index.html?today=45'); pg.click('#go'); pg.wait_for_timeout(250)
      chk(tag+' 열자마자 들어가는 중(문이 보이고 말상자는 아직)', pg.locator('#cbsrShelf.ent .door').is_visible() and pg.evaluate("(()=>{const d=document.querySelector('#cbsrShelf .dg');return !d||+getComputedStyle(d).opacity<.05})()"))
      pg.screenshot(path=OUT+'ent_%s_0.png'%tag); pg.wait_for_timeout(900); pg.screenshot(path=OUT+'ent_%s_1.png'%tag)
      pg.wait_for_timeout(1800)
      chk(tag+' 다 들어오면 문이 사라지고 사서가 말함', pg.locator('#cbsrShelf.ent').count()==0 and not pg.locator('#cbsrShelf .door').is_visible() and pg.locator('#cbsrShelf .dg').count()==1); pg.screenshot(path=OUT+'ent_%s_2.png'%tag)
      pg.close(); pg=cx.new_page(); pg.goto('http://localhost:8765/index.html?today=45'); pg.click('#go'); pg.wait_for_timeout(400)
      t0=pg.evaluate("document.querySelector('#cbsrShelf .dg .dgb')?document.querySelector('#cbsrShelf .dg .dgb').innerText:''")
      pg.mouse.click(vw/2,vh/2); pg.wait_for_timeout(600)
      chk(tag+' 누르면 건너뛰고 첫 말은 그대로', pg.locator('#cbsrShelf.ent').count()==0 and pg.evaluate("+getComputedStyle(document.querySelector('#cbsrShelf .dg')).opacity")>.9 and (pg.evaluate("document.querySelector('#cbsrShelf .dg .dgb').innerText")==t0))
      pg.close(); cx.close()
finally: srv.terminate()
bad=[n for n,c in ok if not c]+errs; print('실패:', bad or '없음', '(%d가지)'%len(ok))
