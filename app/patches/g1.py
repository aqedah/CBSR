import re,sys
F='/home/claude/rj/template3.html'
s=open(F).read()
def rep(old,new,cnt=1):
    global s
    n=s.count(old)
    if n!=cnt: sys.exit(f"count {n}!={cnt} for: {old[:90]}")
    s=s.replace(old,new)

# ---------- 상단·하단 마크업 ----------
rep('''    <div class="brand"><span>이야기 통독 노트</span><span>리딩지저스 45주 · 시험판</span></div>''',
'''    <div class="brand"><span>이야기 통독 노트 · <span id="planName"></span></span><button class="menubtn" id="menuBtn" aria-label="사용법과 설정 열기"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button></div>''')
rep('''    <div class="tabs" role="tablist">
      <button class="tab" role="tab" data-tab="read" aria-selected="true">오늘 통독</button>
      <button class="tab" role="tab" data-tab="qt" aria-selected="false">QT</button>
      <button class="tab" role="tab" data-tab="record" aria-selected="false">나의 기록</button>
      <button class="tab" role="tab" data-tab="guide" aria-selected="false">사용법·설정</button>
    </div>
''','')
rep('''    <span>성경 본문: 개역개정4판 · 통독 일정: 리딩지저스 45주 성경통독표(웨스트민스터코리아)</span>''','''    <span>성경 본문: 개역개정4판 · 통독 일정: <span id="planSrc"></span></span>''')
rep('''<div id="sheetRoot"></div>''','''<nav class="bnav" aria-label="화면 바꾸기"><div class="bnav-in">
  <button class="tab" data-tab="read" aria-selected="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5.5C5.5 4.5 8.5 4.5 12 6.5c3.5-2 6.5-2 9-1V19c-2.5-1-5.5-1-9 1-3.5-2-6.5-2-9-1z"/><path d="M12 6.5V20"/></svg><span>오늘 통독</span></button>
  <button class="tab" data-tab="qt" aria-selected="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/></svg><span>QT</span></button>
  <button class="tab" data-tab="record" aria-selected="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg><span>나의 기록</span></button>
</div></nav>
<div id="drawerRoot"></div>
<div id="hlbar" class="hlbar" hidden></div>
<div id="sheetRoot"></div>''')

# ---------- CSS ----------
css=r'''
body{padding-bottom:calc(84px + env(safe-area-inset-bottom,0px))}
.brand{align-items:center}
.menubtn{border:0;background:none;color:var(--ink);padding:6px;margin:-6px -6px -6px 0;border-radius:8px;display:flex}
.menubtn:hover{background:var(--accent-soft)}
.bnav{position:fixed;left:0;right:0;bottom:0;z-index:9200;background:var(--card);border-top:1px solid var(--line);padding-bottom:env(safe-area-inset-bottom,0px);box-shadow:0 -2px 12px rgba(0,0,0,.05)}
.bnav-in{max-width:720px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr)}
.bnav .tab{border:0;background:none;display:grid;justify-items:center;gap:2px;padding:9px 4px 8px;color:var(--muted);font-size:12px;font-weight:500}
.bnav .tab svg{width:24px;height:24px}
.bnav .tab[aria-selected="true"]{color:var(--accent);font-weight:700}
.bnav .tab[aria-selected="true"] svg{stroke-width:2.4}
.totop{bottom:calc(84px + env(safe-area-inset-bottom,0px))!important}
.drawer-bg{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:9800;display:flex;justify-content:flex-end;animation:fadein .2s}
.drawer{background:var(--paper);width:min(92vw,460px);height:100%;overflow:auto;padding:0 16px calc(30px + env(safe-area-inset-bottom,0px));display:grid;gap:22px;align-content:start;animation:slidein .22s ease-out}
.drawer-head{position:sticky;top:0;background:var(--paper);display:flex;justify-content:space-between;align-items:center;padding:18px 0 10px;border-bottom:1px solid var(--line);z-index:1}
.drawer-head b{font-family:var(--f-text);font-size:20px}
@keyframes slidein{from{transform:translateX(30px);opacity:.4}to{transform:none;opacity:1}}
@keyframes fadein{from{opacity:0}to{opacity:1}}
.plans{display:grid;gap:8px}
.plan{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;align-items:start;text-align:left;border:1.5px solid var(--line);background:var(--card);border-radius:12px;padding:12px 14px}
.plan .dot{width:18px;height:18px;border-radius:50%;border:2px solid var(--line);margin-top:3px}
.plan[aria-checked="true"]{border-color:var(--accent);background:var(--accent-soft)}
.plan[aria-checked="true"] .dot{border:5px solid var(--accent)}
.plan b{font-size:16px}.plan span.lead{grid-column:2}
.topic{margin:0;font-family:var(--f-text);font-size:18px;font-weight:700;color:var(--accent)}
.toqt{width:100%;padding:15px;display:flex;justify-content:center;gap:8px;align-items:center}
/* 형광펜 */
.v{cursor:pointer;border-radius:3px;transition:background .15s}
.v.sel{outline:2px dashed var(--accent);outline-offset:1px}
.v.mk-y{background:linear-gradient(transparent 30%,rgba(255,214,64,.55) 30%)}
.v.mk-g{background:linear-gradient(transparent 30%,rgba(110,214,140,.5) 30%)}
.v.mk-p{background:linear-gradient(transparent 30%,rgba(255,140,180,.45) 30%)}
.v.mk-b{background:linear-gradient(transparent 30%,rgba(110,180,255,.45) 30%)}
:root[data-theme="dark"] .v.mk-y{background:linear-gradient(transparent 30%,rgba(255,214,64,.3) 30%)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .v.mk-y{background:linear-gradient(transparent 30%,rgba(255,214,64,.3) 30%)}:root:not([data-theme="light"]) .v.mk-g{background:linear-gradient(transparent 30%,rgba(110,214,140,.28) 30%)}:root:not([data-theme="light"]) .v.mk-p{background:linear-gradient(transparent 30%,rgba(255,140,180,.28) 30%)}:root:not([data-theme="light"]) .v.mk-b{background:linear-gradient(transparent 30%,rgba(110,180,255,.28) 30%)}}
.hlbar{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:9600;background:var(--card);border:1px solid var(--line);box-shadow:0 6px 24px rgba(0,0,0,.18);border-radius:16px;padding:10px 12px;display:flex;gap:10px;align-items:center;width:max-content;max-width:calc(100vw - 24px)}
.hlbar[hidden]{display:none}
.hlbar .cnt{font-size:12.5px;color:var(--muted);white-space:nowrap}
.sw{width:34px;height:34px;border-radius:50%;border:2px solid var(--card);box-shadow:0 0 0 1px var(--line)}
.sw.y{background:#FFD640}.sw.g{background:#6ED68C}.sw.p{background:#FF8CB4}.sw.b{background:#6EB4FF}
.sw.x{background:var(--paper);display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:14px}
.hlbar .cl{border:0;background:none;color:var(--muted);font-size:13px;padding:6px}
/* QT 항목별 칸 */
.qcard textarea{min-height:56px;background:var(--paper)}
/* 프로필 */
.prof{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 16px;display:grid;gap:14px}
.prof-top{display:flex;gap:14px;align-items:center}
.avatar{width:62px;height:62px;border-radius:50%;background:var(--accent);color:var(--accent-ink);display:flex;align-items:center;justify-content:center;font-family:var(--f-text);font-size:26px;font-weight:700;flex:none}
.prof-name{display:grid;gap:2px;min-width:0}
.prof-name b{font-family:var(--f-text);font-size:21px;display:flex;align-items:center;gap:6px}
.prof-name .edit{border:0;background:none;color:var(--muted);font-size:12.5px;padding:2px 4px;text-decoration:underline}
.ring{display:flex;gap:16px;align-items:center}
.ring svg{flex:none}
.ring .rt{display:grid;gap:2px}
.ring .rt b{font-family:var(--f-text);font-size:26px;font-variant-numeric:tabular-nums}
.pstats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.pstat{background:var(--paper);border-radius:12px;padding:10px 8px;text-align:center;display:grid;gap:0}
.pstat b{font-family:var(--f-text);font-size:22px;font-variant-numeric:tabular-nums}
.pstat span{font-size:11.5px;color:var(--muted)}
.badges{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.bdg{display:grid;justify-items:center;gap:4px;text-align:center;font-size:11.5px;color:var(--muted);line-height:1.3}
.bdg i{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:20px;background:var(--paper);border:2px dashed var(--line);color:var(--line);font-weight:700}
.bdg.on{color:var(--ink);font-weight:600}
.bdg.on i{background:var(--gold-soft);border:2px solid var(--gold);color:var(--gold)}
.books{display:grid;grid-template-columns:repeat(auto-fill,minmax(38px,1fr));gap:4px}
.bk{position:relative;border-radius:6px;background:var(--paper);border:1px solid var(--line);font-size:11.5px;text-align:center;padding:5px 0;overflow:hidden;color:var(--muted)}
.bk i{position:absolute;left:0;bottom:0;top:0;background:var(--ok-soft)}
.bk span{position:relative}
.bk.full{background:var(--ok);border-color:var(--ok);color:var(--ok-soft);font-weight:700}
.hllist{display:grid;gap:8px}
.hlitem{text-align:left;border:1px solid var(--line);background:var(--card);border-radius:10px;padding:10px 12px;font-family:var(--f-text);font-size:15px;line-height:1.7}
.hlitem small{display:block;font-family:var(--f-ui);font-size:12px;color:var(--muted)}
details.more{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}
details.more summary{cursor:pointer;font-weight:600}
details.more .tbl{border:0;padding:0}
'''
rep('</style>',css+'</style>')
open(F,'w').write(s)
print("ok g1")
