# 세라핌 묵상지 새 틀 A5 4쪽(11-25). 체험판 하루 지면과 같은 쓰임.
# 1쪽 ① 오늘의 흐름(지도 또는 본문 구조) ② 성경 읽기 → 마음에 남은 말씀 / 2쪽 ③ 눈여겨볼 것 ④ 나의 묵상 1 본문 관찰
# 3쪽 ④ 이어서 2 하나님의 성품 3 적용 4 나의 기도 / 4쪽 ⑤ 쓴 뒤에 읽기 · 해설, 성경 전체로 ⑥ 함께 드리는 기도
# 쓰는 법: python3 sera4.py 2up 출력.pdf w1124 …   (A4 가로 양면, 회마다 1–4쪽)
#          python3 sera4.py a5 출력.pdf 70 w1201 …  (A5 낱쪽, 70쪽부터 이어 매김 — 12월 체험판 부록)
import sys, os, asyncio, importlib, re
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import a5
from sera_v3_content import S3
from playwright.async_api import async_playwright
inl = a5.inl
L = lambda n: '<div class="ln"></div>' * n
CSS = '''
.x2{display:flex;width:297mm;height:210mm;page-break-after:always;overflow:hidden}
.p5.p4,.p5.p4.r{padding:9mm 10mm 10mm 10mm;flex:none}
.p4 .bx5{height:191mm}.p4 .pn,.p4 .rn{bottom:4mm}.p4 .pn{left:10mm}.p4.r .pn{left:auto;right:10mm}
.b1{display:block!important}
.one .p5{page-break-after:always}
.kp{margin-top:2.6mm}
.ref{white-space:nowrap;font-size:8pt;font-weight:700;color:var(--c);border-left:.7mm solid var(--c);padding-left:1.2mm;margin-right:1.6mm}
.oq{margin:1mm 0 .6mm;text-align:justify}.oh{font-size:8.4pt;color:#666;margin-bottom:.4mm}
.lab4{display:flex;align-items:center;gap:1.8mm;font-size:10pt;font-weight:700;margin:4.4mm 0 .8mm;color:#222}
.lab4 b{display:inline-flex;width:4.6mm;height:4.6mm;background:color-mix(in srgb,var(--c) 16%,#fff);color:var(--c);border-radius:.8mm;align-items:center;justify-content:center;font-size:8pt;font-weight:800}
.lab4 small{font-weight:400;font-size:7.8pt;color:#777;margin-left:auto}
.p4 .ans{flex:none;border-bottom:0}
.p4 .ln{border-bottom:.22mm dotted #888;height:7.2mm}
.ln.lbl{position:relative}.ln.lbl span{position:absolute;left:0;bottom:.6mm;font-size:7pt;color:#999}
.p4 .pr4{margin-top:8mm}
.stc{float:right;width:50mm;margin:0 0 1mm 3mm;border:.3mm solid #ccc;border-radius:1mm;padding:1.6mm 2.2mm;font-size:8.2pt;line-height:1.45;background:#fff}
.stc .sth{font-size:7.6pt;color:#777;margin-bottom:.8mm;font-weight:700}
.stc .sr{display:flex;gap:1.2mm;margin:.4mm 0;line-height:1.35}.stc .sr b{font-weight:700;color:#333}.stc .sr i{font-style:normal;font-weight:700;color:var(--c);width:3mm;flex:none}
.stc .sr.x{margin-left:2.4mm}.stc .sr.b{margin-left:1.2mm}.stc .sr small{color:#666}
.stc .scn{margin:1.4mm 0 0;padding-top:1.2mm;border-top:.2mm solid #ddd;gap:.8mm}.p4 .b1 .stc .scn span{font-size:6.8pt;padding:0 1mm}
.p4 .b1 .stc .scn span.sth2,.stc .scn .sth2{font-size:7pt;color:#777;font-weight:700;width:100%;border:0;padding:0}
.clr{clear:both;height:0}
.lar{display:inline-block;width:4.2mm;height:3.2mm;vertical-align:-.1mm;margin:0 .8mm 0 .2mm;color:var(--c)}
.stp{margin-top:2.2mm}.stp .sn{display:inline-block;font-size:7.4pt;font-weight:700;color:#fff;background:var(--c);border-radius:2.4mm;padding:0 1.9mm;margin-right:1.6mm;line-height:1.55;vertical-align:.2mm}
.p4 .ln.fl{border-bottom:0;display:flex;align-items:flex-end;gap:1.4mm;font-size:8.8pt;color:#555;padding-bottom:.4mm}
.ln.fl i{flex:1;border-bottom:.22mm dotted #888;height:5mm}.ln.fl span{white-space:nowrap}
'''
def lab(n, t, sm=''): return f'<div class="lab4 sans"><b>{n}</b>{t}{"<small>"+sm+"</small>" if sm else ""}</div>'
def lab0(t, sm=''): return f'<div class="lab4 sans">{t}{"<small>"+sm+"</small>" if sm else ""}</div>'
def struct(rows, scn=''):
    ind = {'A': '', 'B': ' b', 'X': ' x'}
    if scn: scn = scn.replace('<div class="scn">', '<div class="scn"><span class="sth2">장면</span>', 1).replace('<span class="sans sth2">', '<span class="sth2">')
    return '<div class="stc sans"><div class="sth">본문 구조</div>' + ''.join(f'<div class="sr{ind.get(a, "")}"><i>{a}.</i><span><b>{re.sub(r"^[가-힣]+ (?=\d)", "", t)}</b> <small>{s}</small></span></div>' for a, t, s in rows) + scn + '</div>'
def obs_steps(S):
    """본문 관찰을 '찾기 → 잇기' 두 걸음으로(11-25 견본). obs_find(찾기 물음)·obs_link(잇기 물음)·obs_start(문장 앞머리, 있을 때만). 없으면 줄 넷."""
    if not S.get('obs_find'): return f'<div class="ans">{L(4)}</div>'
    st = S.get('obs_start', '')
    first = f'<div class="ln fl sans"><span>{inl(st)}</span><i></i></div>' if st else '<div class="ln"></div>'
    return (f'<div class="oq stp"><b class="sn sans">찾기</b><b>{inl(S["obs_find"])}</b></div><div class="ans">{L(1)}</div>'
            f'<div class="oq stp"><svg class="lar" viewBox="0 0 12 9" aria-hidden="true"><path d="M2 0V4.5Q2 7 4.5 7H10.5M8.3 4.8L10.6 7L8.3 9.2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg><b class="sn sans">잇기</b><b>{inl(S["obs_link"])}</b></div><div class="ans">{first}{L(2)}</div>')
def pages(key):
    W = importlib.import_module('w' + key).W; S = S3[key]
    A, O, G, D = a5.blocks(W)
    i3 = next(k for k, x in enumerate(A) if '눈여겨볼 것' in x)
    p1 = [x for x in A[:i3] if 'class="wd' not in x and 'class="map' not in x]
    i = next(k for k, x in enumerate(p1) if '오늘의 흐름' in x)
    if W.get('map'):
        svg = open(os.path.join(H, W['map'])).read()
        p1.insert(i + 1, f'<div class="map mf">{svg}<div class="mcap sans">{inl(W["mapcap"])}</div></div>')
    elif S.get('struct'):
        # 본문 구조는 ① 머리 높이에서 시작하고, ② 성경 읽기의 장면 단추를 상자 안으로 옮김(11-25)
        k = next((k for k, x in enumerate(p1) if 'class="scn"' in x), None)
        scn = p1.pop(k) if k is not None else ''
        p1.insert(i, struct(S['struct'], scn))
    j = next(k for k, x in enumerate(p1) if '성경 읽기<small>' in x)
    p1.insert(j, '<div class="clr"></div>')
    if S.get('word'):   # 11-25 목사님: 말뜻 한 낱말(원칙: 이 문장에서 뜻을 모르면 막히는 말). 본문 구조 아래, ② 앞
        wa, _, wb = S['word'].partition(' — ')
        p1.insert(j + 1, f'<div class="wd sans"><span class="k">말뜻</span><b>{inl(wa)}</b> {inl(wb)}</div>')
    lnl = lambda t, n: ''.join(f'<div class="ln lbl"><span class="sans">{t if k == 0 else ""}</span></div>' for k in range(n))
    p1.append(f'<div class="kp">{lab0("마음에 남은 말씀", "읽고 나서 바로 적습니다")}{lnl("말씀 · 장절", 2)}{lnl("이유", 2)}</div>')
    p2 = ''.join(A[i3:]) + (f'<div class="sh sans"><span class="n">4</span>나의 묵상</div>' + lab(1, '본문 관찰', '오늘 본문을 더 살펴보는 한 길') +
          f'<div class="oq"><span class="ref sans">{S["obs_ref"]}</span>{inl(S["obs"])}</div>' + obs_steps(S))
    m = re.match(r'^([^\s,]+(?:, ?\d+(?:[–-]\d+)?)*)\s+(.*)$', S['god'])
    ref, gst = (m.group(1), m.group(2)) if m else ('', S['god'])
    p3 = (f'<div class="sh sans" style="margin-top:0"><span class="n">4</span>나의 묵상<small>이어서</small></div>' + lab(2, '하나님의 성품') +
          f'<div class="oq"><span class="ref sans">{ref}</span>{inl(gst)} <b>{inl(S["god_q"])}</b></div><div class="ans">{L(4)}</div>'
          + lab(3, '적용') + f'<div class="oq">{inl(S["ap_lead"])} <b>→ {inl(S["ap_fu"])}</b></div><div class="ans">{L(3)}</div>'
          + lab(4, '나의 기도') + f'<div class="oh sans">오늘 마음에 남은 말씀과 내 응답을 하나님께 말씀드립니다.</div><div class="ans">{L(3)}</div>')
    pr = ('<div class="pr4"><div class="sh sans"><span class="n">6</span>함께 드리는 기도</div><h4 class="sans">청년부 기도제목</h4>' + '<div class="pln"></div>' * 5
          + '<h4 class="sans">교회 기도제목</h4>' + '<div class="pln"></div>' * 3 + '</div>')
    D0 = re.sub(r'<small>.*?</small>', '', D[0].replace('<span class="n">6</span>해설', '<span class="n">5</span>쓴 뒤에 읽기 · 해설'))
    p4 = D0 + ''.join(D[1:-1]) + pr
    st = f'--c:{W["color"]};--l:{W["light"]};--hl:#F3E6A0'
    run = f'{W.get("season") or W.get("label","")} · {W["title"]}'.strip(' ·')
    return [p1 and ''.join(p1), p2, p3, p4], st, run
def sec(h, i, num, st, run, right):
    return f'<section class="p5 p4{" r" if right else ""}" style="{st}"><div class="bx5{" b1" if i in (0, 1) else ""}">{h}</div><span class="pn sans">{num}</span><span class="rn sans">{run}</span></section>'
async def main(mode, out, start, mods):
    body = ''
    for k, m in enumerate(mods):
        P, st, run = pages(m[1:])
        if mode == '2up':
            pg = [sec(h, i, i + 1, st, run, i % 2) for i, h in enumerate(P)]
            body += f'<div class="x2 wk">{pg[0]}{pg[1]}</div><div class="x2 wk">{pg[2]}{pg[3]}</div>'
        else:
            n0 = start + 4 * k
            body += '<div class="one wk">' + ''.join(sec(h, i, n0 + i, st, run, (n0 + i) % 2) for i, h in enumerate(P)) + '</div>'
    page = '@page{size:297mm 210mm;margin:0}' if mode == '2up' else '@page{size:148mm 210mm;margin:0}'
    doc = f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{a5.CSS}{CSS}{page}</style></head><body>{body}</body></html>'
    async with async_playwright() as p:
        b = await p.chromium.launch(); g = await b.new_page(); await g.set_content(doc); await g.wait_for_timeout(500)
        fit = await g.evaluate('()=>{' + open(os.path.join(H, 'fit4.js')).read() + '''; const r=[];
          document.querySelectorAll('.wk').forEach(()=>{});
          const ps=[...document.querySelectorAll('.p5')];
          for(let i=0;i<ps.length;i+=4){ const f=fit4(ps[i], ps[i+3]); fit4(ps[i+1], null); r.push(f); }
          return r; }''')
        bad = await g.evaluate('''()=>[...document.querySelectorAll('.p5')].map((p,i)=>{const b=p.firstElementChild;return [i, Math.round((b.scrollHeight-b.clientHeight)*25.4/96)]}).filter(x=>x[1]>0)''')
        print('맞춤(행간, 뺀 성경 전체로):', [(mods[i], f.get('lh'), f.get('dropped')) for i, f in enumerate(fit) if f.get('lh') or f.get('dropped')])
        print('넘침(쪽 순번, mm):', bad or '없음')
        if mode == '2up': await g.pdf(path=out, width='297mm', height='210mm', print_background=True)
        else: await g.pdf(path=out, width='148mm', height='210mm', print_background=True)
        await b.close()
if __name__ == '__main__':
    mode, out = sys.argv[1], sys.argv[2]
    if mode == 'a5': asyncio.run(main(mode, out, int(sys.argv[3]), sys.argv[4:]))
    else: asyncio.run(main(mode, out, 1, sys.argv[3:]))
