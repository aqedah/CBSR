from playwright.sync_api import sync_playwright
from PIL import Image
errs=[]; S='/tmp/shelftest/shots/'
def run(p,w,h,tag,shots=True):
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1,has_touch=True)
    pg=cx.new_page()
    pg.on('console',lambda m: errs.append(tag+' '+m.text[:120]) if (m.type=='error' and '404' not in m.text) or m.text.startswith('TOAST') else None)
    pg.on('pageerror',lambda e: errs.append(tag+' PAGEERROR '+str(e)[:200]))
    pg.goto('http://127.0.0.1:8765/index.html'); pg.click('#go'); pg.wait_for_timeout(900); pg.wait_for_function("!document.querySelector('#cbsrShelf.ent')")
    st=pg.evaluate("(()=>{const r=document.querySelector('#cbsrShelf .st').getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]})()")
    print(tag,'무대(왼쪽,위,너비,높이)',st,'화면',w,h)
    out=[]
    def shot(n):
        if shots: pg.screenshot(path=S+tag+'_'+n+'.png'); out.append(tag+'_'+n)
    shot('1hall')
    pg.click('.zone[data-s="ot"]'); pg.wait_for_timeout(700); shot('2walk'); pg.wait_for_timeout(1500); shot('3ot')
    pg.mouse.click(w-20,90); pg.wait_for_timeout(1700); print(tag,' 빈 곳 → 서고?',pg.locator('.zone').count()==3,'ovs',pg.evaluate('__ovs()'))
    pg.click('.zone[data-s="ot"]'); pg.wait_for_timeout(2100)
    pg.click('.gl button[data-g="선지서"]'); pg.wait_for_timeout(1200); shot('4press'); print(tag,' 책등',pg.locator('.sp').count())
    r=pg.evaluate("(()=>{const a=document.querySelector('.sp[data-b=\"isa\"]').getBoundingClientRect(),q=document.querySelector('.scn.pr img').getBoundingClientRect();return [Math.round(a.left-q.left),Math.round(q.right-document.querySelector('.sp[data-b=\"hos\"]').getBoundingClientRect().right),Math.round(q.left),Math.round(q.width)]})()"); print(tag,' 첫 책 왼쪽 틈·끝 책 오른쪽 틈·그림 왼쪽·그림 너비',r)
    q=pg.evaluate("(()=>{const q=document.querySelector('.scn.pr img').getBoundingClientRect();return [q.left,q.top,q.width,q.height]})()"); pg.mouse.click(q[0]+q[2]*50/390, q[1]+q[3]*700/846); pg.wait_for_timeout(300); print(tag,' 서가 안 빈 곳 → 그대로?',pg.locator('.sp').count()==17)
    pg.click('.sp[data-b="isa"]'); pg.wait_for_timeout(2700); shot('5cover')
    n=int(pg.inner_text('.nv .mid').split('/')[1].replace('쪽','').split('·')[0]); over=[]
    for i in range(1,n):
        pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(110)
        m=pg.evaluate("(()=>{const m=document.querySelector('#cbsrShelf main').getBoundingClientRect(),p=document.querySelector('#cbsrShelf .pr').getBoundingClientRect(),q=document.querySelector('#cbsrShelf .st').getBoundingClientRect();return [Math.round(m.top-p.bottom),Math.round(q.right-m.right)]})()")
        if m[0]<4 or m[1]<8: over.append((i+1,m))
        if pg.inner_text('main .k').startswith('구조'): shot('6parts')
        if pg.locator('#cbsrQa').count() and i<n-5: shot('7q')
    print(tag,' 쪽수',n,'| 머리줄과 겹치거나 오른쪽이 넘친 쪽:',over)
    pg.click('.nv .mid'); pg.wait_for_timeout(500); print(tag,' 아래 가운데 닫기 → 서가?',pg.locator('.sp').count()==17)
    pg.mouse.click(4,h/2); pg.wait_for_timeout(500); print(tag,' 서가 바깥 → 구약?',pg.locator('.gl button').count()==4)
    pg.click('.bk'); pg.wait_for_timeout(1700); pg.mouse.click(w-20,90); pg.wait_for_timeout(500); print(tag,' 서고 바닥 → 닫힘?',pg.evaluate('!CBSR_SHELF.isOpen()'),'ovs',pg.evaluate('__ovs()'))
    b.close(); return out
with sync_playwright() as p:
    a=run(p,412,699,'ph')
    run(p,360,640,'sm',shots=False)
    c=run(p,1280,800,'tb',shots=True)
print('errors:',errs)
ims=[Image.open(S+n+'.png') for n in a]
sh=Image.new('RGB',(422*len(ims)+10,719),(200,60,60))
for i,im in enumerate(ims): sh.paste(im,(10+i*422,10))
sh=sh.resize((sh.width*45//100,sh.height*45//100)); sh.save(S+'sheet_ph.png'); print(sh.size)
Image.open(S+'tb_1hall.png').resize((640,400)).save(S+'sheet_tb.png')
