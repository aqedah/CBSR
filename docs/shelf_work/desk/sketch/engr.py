# 초상에 판화 결과 밤 촛불빛을 입힌다:  engr.py in.svg out.png [W]
import sys, math, io, numpy as np
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright
src, dst = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 464
OPT = dict(a.split('=', 1) for a in sys.argv[4:])
VB = [float(x) for x in OPT.get('vb', '34 12 232 368').split()]
FLAME = None if OPT.get('flame') == 'none' else [float(x) for x in OPT.get('flame', '66.5 284').split()]
FACE = None if OPT.get('face') == 'none' else [float(x) for x in OPT.get('face', '150 166').split()]
FACEL, BASE, GAIN = float(OPT.get('facel', 0.8)), float(OPT.get('base', 0.36)), float(OPT.get('gain', 1))
H = round(W * VB[3] / VB[2])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': W * 2, 'height': H * 2})
    import os, tempfile
    hp = os.path.join(os.path.dirname(src), '_engr_view.html')
    open(hp, 'w').write('<html><body style="margin:0;background:transparent"><img src="%s" width="%d" style="display:block"></body></html>' % (os.path.basename(src), W * 2))
    pg.goto('file://' + hp)
    pg.wait_for_timeout(300)
    raw = pg.screenshot(omit_background=True); b.close()
im = Image.open(io.BytesIO(raw)).convert('RGBA').resize((W, H), Image.LANCZOS)
a = np.asarray(im).astype(np.float32) / 255.0
rgb, al = a[..., :3], a[..., 3]
tone = rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
k = W / VB[2]
L = np.zeros((H, W), np.float32)
fx = fy = -9999.0
if FLAME:
    fx, fy = (FLAME[0] - VB[0]) * k, (FLAME[1] - VB[1]) * k
    d = np.sqrt((xx - fx) ** 2 + ((yy - fy) * 0.9) ** 2) / (232 * k * 0.95)
    L = np.clip(1.0 / (1 + 5.5 * d * d), 0, 1)
if FACE:
    fcx, fcy = (FACE[0] - VB[0]) * k, (FACE[1] - VB[1]) * k
    L = np.maximum(L, FACEL * np.exp(-(((xx - fcx) / (232 * k * 0.30)) ** 2 + ((yy - fcy) / (232 * k * 0.46)) ** 2)))
rs = np.random.RandomState(3)
def lo(n):
    g = Image.fromarray((rs.rand(H // n + 2, W // n + 2) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return np.asarray(g).astype(np.float32) / 255.0
wob = (lo(40) - 0.5) * 3.0 + (lo(8) - 0.5) * 1.0
def lines(deg, sp, wd):
    r = math.radians(deg + 90)
    s = xx * math.cos(r) + yy * math.sin(r) + wob
    dd = np.abs(((s / sp) % 1.0) - 0.5) * sp
    return np.clip(wd / 2 - dd + 0.5, 0, 1) * np.clip(wd * 1.6, 0, 1)
t = np.clip(tone * 1.25 + 0.04, 0, 1)
w1 = 1.9 * np.clip((0.80 - t) / 0.36, 0, 1)
w2 = 1.9 * np.clip((0.50 - t) / 0.28, 0, 1)
w3 = 1.8 * np.clip((0.26 - t) / 0.20, 0, 1)
ink = np.maximum(np.maximum(lines(42, 4.6, w1), lines(-40, 4.6, w2)), lines(90, 4.6, w3)) * 0.82
ink = np.maximum(ink, np.clip((0.10 - tone) / 0.06, 0, 1))             # 굵은 먹선
flame = np.clip((tone - 0.86) / 0.08, 0, 1)
ink *= (1 - flame)
paper = np.array((226, 206, 166), np.float32) / 255.0
wash = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255.0
col = paper[None, None, :] * (0.34 + 0.66 * np.clip(wash * 1.5, 0, 1)) * (0.95 + 0.1 * lo(30))[..., None]
INK = np.array((34, 22, 14), np.float32) / 255.0
out = col * (1 - ink[..., None]) + INK[None, None, :] * ink[..., None]
night = np.array((BASE, BASE * 0.84, BASE * 0.70), np.float32)[None, None, :] + np.array((0.98, 0.88, 0.70), np.float32)[None, None, :] * L[..., None]
out = out * np.clip(night, 0, 1.25)
out = out + flame[..., None] * (np.array((1.0, 0.93, 0.70), np.float32) - out)
glow = np.clip(1 - np.sqrt((xx - fx) ** 2 + (yy - fy) ** 2) / (232 * k * 0.20), 0, 1) ** 2
out = 1 - (1 - np.clip(out, 0, 1)) * (1 - 0.42 * glow[..., None] * np.array((1.0, 0.72, 0.36), np.float32))
fade = np.clip((H - yy) / (H * 0.10), 0, 1) * np.clip(xx / (W * 0.05), 0, 1) * np.clip((W - xx) / (W * 0.05), 0, 1)
out = out * GAIN + flame[..., None] * (np.clip(out, 0, 1) - out * GAIN) if GAIN != 1 else out
if OPT.get('fade') == 'none': fade = np.ones_like(al)
res = np.dstack([np.clip(out, 0, 1), al * fade])
Image.fromarray((res * 255).astype(np.uint8), 'RGBA').save(dst)
print(dst, W, H)
