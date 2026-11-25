# 실제 빌드: 서고 안의 통독표(앱 통독표와 같은 자료), 말씀 카드 기간(12월–1월), 닫기로만 나가기, 나가는 움직임
import sys, subprocess, time, json
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8766', '--bind', '127.0.0.1'], cwd='/tmp/cbsr_build_app/site', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
errs = []; S = '/home/claude/shelf-desk/check/dlg/'; ok = []
def chk(name, cond, extra=''):
    ok.append((name, bool(cond))); print(('  통과 ' if cond else '  실패 ') + name, '·', extra)
FAKE = "(()=>{const D=Date,t0=new D(%s).getTime()-D.now();class F extends D{constructor(...a){ if(a.length) super(...a); else super(D.now()+t0);} static now(){return D.now()+t0;}} window.Date=F;})()"
NAV = "(()=>{const b=[...document.querySelectorAll('.bnav button,.bnav a,nav button')].find(x=>/^\\s*%s\\s*$/.test(x.innerText)); if(b) b.click(); return !!b;})()"
def ctx(b, when, yv=None):
    cx = b.new_context(viewport={'width': 412, 'height': 820}, device_scale_factor=2, has_touch=True, service_workers='block')
    pg = cx.new_page(); pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)[:200]))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text[:160]) if m.type == 'error' and 'net::' not in m.text and 'Failed to load resource' not in m.text and '@firebase' not in m.text else None)
    pg.add_init_script(FAKE % when)
    if yv: pg.add_init_script("try{ if(!localStorage.getItem('cbsr-yv')) localStorage.setItem('cbsr-yv', %s); }catch(e){}" % json.dumps(json.dumps(yv)))
    pg.goto('http://127.0.0.1:8766/index.html', wait_until='domcontentloaded'); pg.wait_for_timeout(3500)
    pg.wait_for_timeout(1200); pg.evaluate("(()=>{const r=document.getElementById('sheetRoot'); if(r) r.innerHTML='';})()")   # 처음 들어온 사람에게 뜨는 앱의 안내 창은 닫아 둠(실제로는 사용자가 먼저 닫음)
    return cx, pg
def helpers(pg):
    T = lambda sel: pg.evaluate('(s)=>{const e=document.querySelector(s);return e?e.innerText.replace(/\\n/g," / "):null}', sel)
    has = lambda sel: pg.locator(sel).count() > 0
    def shelf():
        pg.evaluate("document.querySelector('#rgShelf').click()"); pg.wait_for_timeout(1800)
        for _i in range(4):
            if not (pg.locator('#cbsrShelf .dg button.dgb').count() and not pg.locator('#cbsrShelf .dgc').count()): break
            pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
    return T, has, shelf
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        cx, pg = ctx(b, '2027,2,15,9,0,0'); T, has, shelf = helpers(pg)
        LS = "rjnote:y365"
        def edit(js):   # 기기에 저장된 기록을 고치고 다시 엶
            pg.evaluate("""(js)=>{ const m=JSON.parse(localStorage.getItem('%s')||'{}'); m.done=m.done||{}; (new Function('m',js))(m); localStorage.setItem('%s',JSON.stringify(m)); }""" % (LS, LS), js)
            pg.reload(wait_until='domcontentloaded'); pg.wait_for_timeout(4200); pg.evaluate("(()=>{const r=document.getElementById('sheetRoot'); if(r) r.innerHTML='';})()"); pg.evaluate(NAV % '오늘'); pg.wait_for_timeout(700)
        KEYS = pg.evaluate("""()=>{ const r=[]; for(let w=1;w<=60;w++) for(let d=0;d<7;d++) r.push(w+"-"+d); return r; }""")
        def add(n, date, skip=0): return "let i=0; for(const k of %s.slice(%d)){ if(i>=%d) break; if(!m.done[k]){ m.done[k]='%s'; i++; } }" % (json.dumps(KEYS), skip, n, date)
        edit(add(60, '2027-01-20'))
        chk('서고에 들어간 적이 없으면 60일을 읽어도 배너 없음', not has('.sbnr.shst'))
        shelf(); pg.evaluate("document.querySelector('#cbsrShelf .bk').click()"); pg.wait_for_timeout(1200)
        t0 = pg.evaluate("(()=>{ const m=JSON.parse(localStorage.getItem('%s')); return m.shq&&m.shq._s&&m.shq._s.t0&&m.shq._s.t0.v; })()" % LS)
        chk('처음 들어간 날을 적음 ' + str(t0), t0 == '2027-03-15')
        pg.evaluate(NAV % '오늘'); pg.wait_for_timeout(600); chk('들어간 날에는 배너 없음', not has('.sbnr.shst'))
        edit(add(39, '2027-03-16'))
        chk('들어간 뒤 39일: 배너 없음', not has('.sbnr.shst'))
        edit(add(1, '2027-03-17'))
        chk('들어간 뒤 40일: 오늘 탭에 배너', has('.sbnr.shst') and '자리를 비웠' in (T('.sbnr.shst') or ''), T('.sbnr.shst') or '')
        pg.screenshot(path=S+'ap_banner.png')
        pg.click('.sbnr.shst'); pg.wait_for_timeout(1800)
        chk('배너를 누르면 서고에서 2막', '보이지 않는다' in (T('#cbsrShelf .dg .dgb span') or ''), T('#cbsrShelf .dg .dgb span') or '')
        for i in range(8):
            if pg.locator('#cbsrShelf .dgc').count(): break
            pg.click('#cbsrShelf .dg .dgb'); pg.wait_for_timeout(700)
        pg.evaluate("document.querySelector('#cbsrShelf .bk').click()"); pg.wait_for_timeout(1200)
        chk('2막을 본 뒤에는 배너가 사라짐', not has('.sbnr.shst'))
        cx.close(); b.close()
finally:
    srv.terminate()
bad = [n for n, c in ok if not c] + (['페이지 오류 %d건' % len(errs)] if errs else []); print('오류:', errs or '없음'); print('실패:', bad or '없음', '(%d가지)' % len(ok))
