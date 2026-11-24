from playwright.sync_api import sync_playwright
from PIL import Image
errs=[]; S='/tmp/shelftest/shots/'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=b.new_context(viewport={'width':412,'height':699},device_scale_factor=2,has_touch=True)
    pg=cx.new_page(); pg.on('pageerror',lambda e: errs.append('PAGEERROR '+str(e)[:200])); pg.on('console',lambda m: errs.append(m.text[:100]) if m.text.startswith('TOAST') else None)
    pg.goto('http://127.0.0.1:8765/index.html'); pg.click('#go'); pg.wait_for_timeout(1200); pg.screenshot(path=S+'q1.png'); print('사서(서고):',pg.inner_text('.lib').replace('\n',' '))
    pg.click('.zone[data-s="nt"]'); pg.wait_for_timeout(2200); print('사서(신약):',pg.inner_text('.lib').replace('\n',' '))
    pg.click('.gl button[data-g="바울서신"]'); pg.wait_for_timeout(1200); print('사서(서가):',pg.inner_text('.lib').replace('\n',' ')); pg.screenshot(path=S+'q2.png')
    pg.click('.sp[data-b="gal"]'); pg.wait_for_timeout(2700)
    n=int(pg.inner_text('.nv .mid').split('/')[1].split('·')[0]); print('쪽수',n)
    while not pg.locator('#cbsrQa').count(): pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(90)
    print('첫 물음:',pg.inner_text('main .qq'),'|',pg.inner_text('.nv .mid')); pg.screenshot(path=S+'q3.png')
    pg.click('.qb .ans'); pg.wait_for_timeout(200); print('빈 채로 답하기 →',errs[-1] if errs else None)
    pg.click('.qb button[data-a="see"]'); pg.wait_for_timeout(200); print('책에서 다시 보기 →',pg.inner_text('main .k')[:14],'| 오른쪽 단추:',pg.inner_text('.nv .go'))
    pg.click('.nv .go'); pg.wait_for_timeout(200); print('물음으로 →',pg.inner_text('main .qq'))
    ans=['바울이 갈라디아의 여러 교회에 썼습니다.','첫 전도여행 뒤, 예루살렘 공의회 전입니다.','다른 복음으로 옮겨 가는 교회를 붙들려고 썼습니다.','받은 복음, 믿음으로 의롭게 됨, 성령으로 사는 삶의 차례입니다.','약속하신 대로 아들을 보내시고 성령을 주시는 분입니다.']
    for i,a in enumerate(ans):
        pg.fill('#cbsrQa',a); pg.click('.qb .ans'); pg.wait_for_timeout(450)
        if i==0: pg.screenshot(path=S+'q4.png')
        pg.wait_for_timeout(900)
    print('다 답한 뒤:',pg.inner_text('main').replace('\n',' / ')[:150]); pg.screenshot(path=S+'q5.png')
    print('저장된 것:',pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('cbsr_shelf_qa')).gal)"))
    pg.click('.nv .go'); pg.wait_for_timeout(600); print('서가의 인장 표시:',pg.locator('.sl').count()); pg.screenshot(path=S+'q6.png')
    pg.go_back(); pg.wait_for_timeout(500); pg.go_back(); pg.wait_for_timeout(1800); print('사서(서고):',pg.inner_text('.lib').replace('\n',' '))
    # 쓰던 글이 쪽을 넘겨도 남는지
    pg.click('.zone[data-s="nt"]'); pg.wait_for_timeout(2200); pg.click('.gl button[data-g="바울서신"]'); pg.wait_for_timeout(1200); pg.click('.sp[data-b="rom"]'); pg.wait_for_timeout(2700)
    while not pg.locator('#cbsrQa').count(): pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(90)
    pg.fill('#cbsrQa','쓰다 만 글'); pg.click('.nv button[data-a="next"]'); pg.wait_for_timeout(150); pg.click('.nv button[data-a="prev"]'); pg.wait_for_timeout(150); print('넘겼다 돌아온 글:',pg.input_value('#cbsrQa'))
    b.close()
print('errors',[e for e in errs if not e.startswith('TOAST')])
ims=[Image.open(S+n+'.png') for n in ('q1','q2','q3','q4','q5','q6')]
sh=Image.new('RGB',(834*6+70,1418),(200,60,60))
for i,im in enumerate(ims): sh.paste(im,(10+i*844,10))
sh=sh.resize((sh.width*24//100,sh.height*24//100)); sh.save(S+'sheet_qa.png'); print(sh.size)
Image.open(S+'q1.png').crop((180,560,650,1398)).save(S+'crop_hall_low.png')
