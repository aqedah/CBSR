# Soft (non-pixel) art for the bookshelf mockups: a high-angle hall rendered from a tiny 3D scene.
import math, random, os, json, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

OUT = '/home/claude/shelf-merged/art'
os.makedirs(OUT, exist_ok=True)
W, H = 780, 1692          # 2x of 390 x 846
SS = 2

PALS = {
    'tor': [(122, 38, 40), (150, 52, 44), (96, 30, 36), (170, 120, 60), (132, 70, 48)],
    'his': [(140, 96, 52), (112, 74, 42), (166, 124, 70), (94, 60, 38), (150, 80, 50)],
    'poe': [(54, 96, 76), (72, 118, 86), (40, 78, 66), (150, 140, 84), (88, 124, 104)],
    'pro': [(44, 62, 108), (60, 80, 130), (36, 48, 86), (120, 110, 150), (84, 100, 140)],
    'gos': [(190, 150, 78), (214, 186, 120), (160, 116, 58), (120, 44, 40), (226, 206, 160)],
    'pau': [(150, 48, 46), (48, 104, 108), (176, 70, 52), (60, 124, 120), (198, 160, 96)],
    'gen': [(98, 64, 118), (124, 84, 140), (76, 50, 98), (170, 140, 90), (140, 104, 150)],
    'mix': [(122, 38, 40), (140, 96, 52), (54, 96, 76), (44, 62, 108), (190, 150, 78), (98, 64, 118), (60, 124, 120)],
}


class Scene:
    def __init__(self, cam_h, cam_z, pitch_deg, f_css, cy_css=423):
        self.cw, self.ch = W * SS, H * SS
        self.img = Image.new('RGB', (self.cw, self.ch), (16, 12, 16))
        self.d = ImageDraw.Draw(self.img)
        self.cam = (0.0, cam_h, cam_z)
        self.sp, self.cp = math.sin(math.radians(pitch_deg)), math.cos(math.radians(pitch_deg))
        self.f = f_css * 2 * SS
        self.cx, self.cy = self.cw / 2, cy_css * 2 * SS
        self.fog = (26, 20, 30)

    def P(self, x, y, z):
        X, Y, Z = x - self.cam[0], y - self.cam[1], z - self.cam[2]
        zc = Z * self.cp - Y * self.sp
        yc = Y * self.cp + Z * self.sp
        zc = max(zc, 0.05)
        return (self.cx + self.f * X / zc, self.cy - self.f * yc / zc, zc)

    def css(self, x, y, z):
        sx, sy, zc = self.P(x, y, z)
        return (sx / (2 * SS), sy / (2 * SS), self.f / zc / (2 * SS))

    def shade(self, col, zc, k=1.0):
        t = min(max((zc - 9.0) / 22.0, 0.0), 1.0) * 0.62
        return tuple(int(min(255, c * k) * (1 - t) + f * t) for c, f in zip(col, self.fog))

    def quad(self, pts, col, k=1.0):
        pp = [self.P(*p) for p in pts]
        zc = sum(p[2] for p in pp) / len(pp)
        self.d.polygon([(p[0], p[1]) for p in pp], fill=self.shade(col, zc, k))


def books_front(sc, rnd, x0, x1, y0, y1, z, pal, flip=False):
    """Spines on a plane of constant z, between x0..x1, shelf from y0 (board) to y1 (clear height)."""
    x = x0 + 0.02
    while x < x1 - 0.06:
        w = rnd.uniform(0.07, 0.14)
        if x + w > x1 - 0.02:
            break
        r = rnd.random()
        if r < 0.07:
            x += w * 0.8
            continue
        h = (y1 - y0) * rnd.uniform(0.62, 0.93)
        col = rnd.choice(pal)
        k = rnd.uniform(0.82, 1.12)
        sc.quad([(x, y0, z), (x + w, y0, z), (x + w, y0 + h, z), (x, y0 + h, z)], col, k)
        # lit edge and gold bands
        sc.quad([(x, y0, z), (x + w * 0.22, y0, z), (x + w * 0.22, y0 + h, z), (x, y0 + h, z)], col, k * 1.22)
        if rnd.random() < 0.6:
            for by in (0.72, 0.8):
                sc.quad([(x, y0 + h * by, z), (x + w, y0 + h * by, z), (x + w, y0 + h * (by + 0.03), z), (x, y0 + h * (by + 0.03), z)], (206, 170, 96), 1.0)
        x += w + 0.008


def books_side(sc, rnd, z0, z1, y0, y1, x, pal):
    z = z0 + 0.03
    while z < z1 - 0.08:
        w = rnd.uniform(0.09, 0.18)
        if rnd.random() < 0.06:
            z += w
            continue
        h = (y1 - y0) * rnd.uniform(0.6, 0.92)
        col = rnd.choice(pal)
        k = rnd.uniform(0.6, 0.85)
        sc.quad([(x, y0, z), (x, y0, z + w), (x, y0 + h, z + w), (x, y0 + h, z)], col, k)
        z += w + 0.01


def case(sc, rnd, xa, xb, z, pal, h=3.1, depth=0.75, shelves=4):
    """Bookcase whose front faces the camera (plane z), spanning xa..xb. Inner side faces the aisle."""
    wood_f, wood_t, wood_s, back = (104, 68, 40), (146, 102, 60), (72, 46, 28), (30, 21, 18)
    inner = xa if abs(xa) < abs(xb) else xb
    zb = z + depth
    # inner side
    sc.quad([(inner, 0, z), (inner, 0, zb), (inner, h, zb), (inner, h, z)], wood_s, 0.9)
    # top
    sc.quad([(xa - 0.06, h, z - 0.06), (xb + 0.06, h, z - 0.06), (xb + 0.06, h, zb), (xa - 0.06, h, zb)], wood_t, 1.0)
    # front frame
    sc.quad([(xa, 0, z), (xb, 0, z), (xb, h, z), (xa, h, z)], wood_f, 1.0)
    m = 0.1
    base = 0.28
    sh = (h - base - 0.16) / shelves
    for i in range(shelves):
        y0 = base + i * sh
        y1 = y0 + sh - 0.07
        sc.quad([(xa + m, y0, z), (xb - m, y0, z), (xb - m, y1, z), (xa + m, y1, z)], back, 1.0)
        books_front(sc, rnd, xa + m, xb - m, y0, y1, z, pal)
        # board highlight
        sc.quad([(xa + m, y0 - 0.035, z), (xb - m, y0 - 0.035, z), (xb - m, y0, z), (xa + m, y0, z)], wood_t, 0.9)
    # crown
    sc.quad([(xa - 0.06, h - 0.14, z - 0.06), (xb + 0.06, h - 0.14, z - 0.06), (xb + 0.06, h, z - 0.06), (xa - 0.06, h, z - 0.06)], wood_f, 1.18)


def lantern(sc, x, z, inner, y=2.2):
    """Lantern hanging from a short arm fixed to the case edge (inner) at height y."""
    iron = (30, 24, 22)
    sc.quad([(inner, y + 0.50, z), (x, y + 0.50, z), (x, y + 0.455, z), (inner, y + 0.455, z)], iron, 1.0)
    sc.quad([(x - 0.012, y + 0.36, z), (x + 0.012, y + 0.36, z), (x + 0.012, y + 0.5, z), (x - 0.012, y + 0.5, z)], iron, 1.0)
    sc.quad([(x - 0.13, y + 0.30, z), (x + 0.13, y + 0.30, z), (x, y + 0.42, z)], iron, 1.15)
    sc.quad([(x - 0.11, y - 0.02, z), (x + 0.11, y - 0.02, z), (x + 0.11, y + 0.30, z), (x - 0.11, y + 0.30, z)], iron, 1.1)
    pp = [sc.P(*p) for p in [(x - 0.075, y + 0.02, z), (x + 0.075, y + 0.02, z), (x + 0.075, y + 0.27, z), (x - 0.075, y + 0.27, z)]]
    sc.d.polygon([(p[0], p[1]) for p in pp], fill=(255, 220, 130))
    pp = [sc.P(*p) for p in [(x - 0.03, y + 0.05, z), (x + 0.03, y + 0.05, z), (x + 0.03, y + 0.2, z), (x - 0.03, y + 0.2, z)]]
    sc.d.polygon([(p[0], p[1]) for p in pp], fill=(255, 246, 214))


def hall(cfg, name='hall_q', seed=5):
    rnd = random.Random(seed)
    sc = Scene(cfg['h'], cfg['z'], cfg['pitch'], cfg['f'], cfg.get('cy', 423))
    HW = cfg['hw']                # hall half width
    Z0, Z1 = -6.0, cfg['zend']
    # floor
    z = Z0
    while z < Z1:
        x = -HW
        i = 0
        while x < HW - 1e-6:
            x2 = min(x + 0.8, HW)
            j = int(round((z - Z0) / 0.8))
            base = (86, 72, 64) if (i + j) % 2 == 0 else (76, 63, 57)
            sc.quad([(x, 0, z), (x2, 0, z), (x2, 0, z + 0.8), (x, 0, z + 0.8)], base, rnd.uniform(0.94, 1.06))
            x = x2
            i += 1
        z += 0.8
    # carpet runner
    cwid = cfg['carpet']
    sc.quad([(-cwid, 0, Z0), (cwid, 0, Z0), (cwid, 0, Z1 - 0.9), (-cwid, 0, Z1 - 0.9)], (100, 34, 36))
    for s in (-1, 1):
        sc.quad([(s * cwid, 0, Z0), (s * (cwid - 0.07), 0, Z0), (s * (cwid - 0.07), 0, Z1 - 0.9), (s * cwid, 0, Z1 - 0.9)], (182, 140, 66))
        sc.quad([(s * (cwid - 0.16), 0, Z0), (s * (cwid - 0.19), 0, Z0), (s * (cwid - 0.19), 0, Z1 - 0.9), (s * (cwid - 0.16), 0, Z1 - 0.9)], (150, 108, 52))
    zz = Z0 + 0.6
    while zz < Z1 - 1.5:   # carpet diamonds
        sc.quad([(0, 0, zz), (0.22, 0, zz + 0.3), (0, 0, zz + 0.6), (-0.22, 0, zz + 0.3)], (124, 48, 44))
        zz += 1.6
    WH = cfg['wh']
    # side walls with wall shelves
    for s in (-1, 1):
        x = s * HW
        zc = Z0
        while zc < Z1:     # split wall in strips for fog gradient
            z2 = min(zc + 1.0, Z1)
            sc.quad([(x, 0, zc), (x, 0, z2), (x, WH, z2), (x, WH, zc)], (58, 48, 50), 0.9)
            zc = z2
        for (za, zb) in cfg['wallbays']:
            for lv in range(4):
                y0 = 0.5 + lv * 1.05
                sc.quad([(x, y0 - 0.06, za), (x, y0 - 0.06, zb), (x, y0 + 0.92, zb), (x, y0 + 0.92, za)], (26, 19, 18), 1.0)
                books_side(sc, rnd, za, zb, y0, y0 + 0.9, x, PALS['mix'])
                sc.quad([(x, y0 - 0.06, za), (x, y0 - 0.06, zb), (x, y0, zb), (x, y0, za)], (120, 82, 48), 0.8)
    # end wall and window
    sc.quad([(-HW, 0, Z1), (HW, 0, Z1), (HW, WH, Z1), (-HW, WH, Z1)], (52, 44, 48), 0.9)
    ww = cfg.get('win_w', 0.9)
    wy0, wy1 = cfg.get('win_y', (3.6, 7.2))
    pts = [(-ww, wy0, Z1 - 0.01), (ww, wy0, Z1 - 0.01), (ww, wy1 - ww, Z1 - 0.01)]
    for a in range(0, 181, 15):
        pts.append((ww * math.cos(math.radians(a)), wy1 - ww + ww * math.sin(math.radians(a)), Z1 - 0.01))
    pts.append((-ww, wy1 - ww, Z1 - 0.01))
    pp = [sc.P(*p) for p in pts]
    sc.d.polygon([(p[0], p[1]) for p in pp], fill=(255, 232, 176))
    for bx in (-ww / 3, ww / 3):
        sc.quad([(bx - 0.035, wy0, Z1 - 0.02), (bx + 0.035, wy0, Z1 - 0.02), (bx + 0.035, wy1 - 0.25, Z1 - 0.02), (bx - 0.035, wy1 - 0.25, Z1 - 0.02)], (120, 86, 60), 1.0)
    for by in (wy0 + (wy1 - wy0) * 0.33, wy0 + (wy1 - wy0) * 0.62):
        sc.quad([(-ww, by, Z1 - 0.02), (ww, by, Z1 - 0.02), (ww, by + 0.06, Z1 - 0.02), (-ww, by + 0.06, Z1 - 0.02)], (120, 86, 60), 1.0)
    # objects far to near
    anchors = {'cases': {}, 'lanterns': []}
    rows = sorted(cfg['rows'], key=lambda r: -r['z'])
    lights, shadows = [], []
    ch = cfg['case_h']
    for r in rows:
        for (key, xa, xb) in r['cases']:
            case(sc, rnd, xa, xb, r['z'], PALS[key], h=ch)
            cs = [sc.css(x, y, r['z']) for x in (xa, xb) for y in (0, ch)]
            anchors['cases'][key] = [round(min(c[0] for c in cs)), round(min(c[1] for c in cs)), round(max(c[0] for c in cs)), round(max(c[1] for c in cs))]
            shadows.append([sc.css(xa - 0.1, 0, r['z'] - 0.75), sc.css(xb + 0.1, 0, r['z'] - 0.75), sc.css(xb + 0.1, 0, r['z'] + 0.8), sc.css(xa - 0.1, 0, r['z'] + 0.8)])
            sides = [xa, xb] if r.get('both') else [xa if abs(xa) < abs(xb) else xb]
            for inner in sides:
                sgn = -1 if inner > 0 else 1
                if r.get('both'):
                    sgn = -1 if inner == xa else 1
                lx = inner + sgn * 0.3
                lz = r['z'] - 0.1
                lantern(sc, lx, lz, inner)
                hx, hy, hs = sc.css(lx, 2.35, lz)
                bx, by, _ = sc.css(lx, 0, lz - 0.5)
                anchors['lanterns'].append([round(hx), round(hy), round(hs, 1)])
                lights.append((hx, hy, bx, by, hs))
    img = sc.img.resize((W, H), Image.LANCZOS)
    # ---- light pass (in output px = 2 x css) ----
    base = np.asarray(img).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # painterly low-frequency variation
    ng = np.random.default_rng(11)
    lo = Image.fromarray((ng.random((H // 24 + 2, W // 24 + 2)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    base *= (0.93 + 0.14 * np.asarray(lo).astype(np.float32)[..., None] / 255.0)
    # contact shadows
    sh = Image.new('L', (W, H), 0)
    sd = ImageDraw.Draw(sh)
    for q in shadows:
        sd.polygon([(p[0] * 2, p[1] * 2) for p in q], fill=255)
    S = np.asarray(sh.filter(ImageFilter.GaussianBlur(16))).astype(np.float32) / 255.0
    base *= (1 - 0.42 * S[..., None])
    lum = Image.new('L', (W, H), 0)
    ld = ImageDraw.Draw(lum)
    for (hx, hy, bx, by, hs) in lights:
        r = hs * 2 * 1.7
        ld.ellipse([bx * 2 - r, by * 2 - r * 0.5, bx * 2 + r, by * 2 + r * 0.5], fill=215)
        r2 = hs * 2 * 1.15
        ld.ellipse([hx * 2 - r2, hy * 2 - r2 * 0.9, hx * 2 + r2, hy * 2 + r2 * 1.3], fill=170)
    lum = lum.filter(ImageFilter.GaussianBlur(34))
    L = np.asarray(lum).astype(np.float32) / 255.0
    # window bloom and the shaft it throws down the carpet
    wl = Image.new('L', (W, H), 0)
    wd = ImageDraw.Draw(wl)
    wx, wy, ws = sc.css(0, (wy0 + wy1) / 2, Z1)
    r = ws * 2 * 2.6
    wd.ellipse([wx * 2 - r, wy * 2 - r * 1.25, wx * 2 + r, wy * 2 + r * 1.25], fill=230)
    a = sc.css(-0.5, 0, Z1 - 2.2); b2 = sc.css(0.5, 0, Z1 - 2.2); c = sc.css(1.25, 0, Z1 - 13.5); e = sc.css(-1.25, 0, Z1 - 13.5)
    wd.polygon([(a[0] * 2, a[1] * 2), (b2[0] * 2, b2[1] * 2), (c[0] * 2, c[1] * 2), (e[0] * 2, e[1] * 2)], fill=120)
    WL = np.asarray(wl.filter(ImageFilter.GaussianBlur(44))).astype(np.float32) / 255.0
    amb = cfg.get('amb', 0.5)
    cool = np.array([0.80, 0.80, 1.0], dtype=np.float32) * amb
    warm = np.array([1.0, 0.84, 0.58], dtype=np.float32)
    dawn = np.array([1.0, 0.90, 0.72], dtype=np.float32)
    out = base * (cool + 0.95 * L[..., None] * warm + 0.75 * WL[..., None] * dawn)
    out += (L[..., None] ** 2.2) * warm * 0.16 + (WL[..., None] ** 1.8) * dawn * 0.34
    # vignette
    v = 1 - 0.6 * np.clip(((xx - W / 2) / (W * 0.74)) ** 2 + ((yy - H * 0.47) / (H * 0.6)) ** 2, 0, 1)
    out *= v[..., None]
    out = np.clip(out, 0, 1) ** 0.92
    res = Image.fromarray((out * 255).astype(np.uint8))
    # shallow depth of field: far end and nearest floor go soft
    blur = np.asarray(res.filter(ImageFilter.GaussianBlur(3.2))).astype(np.float32)
    sharp = np.asarray(res.filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)
    m = np.clip((cfg.get('dof_top', 300) * 2 - yy) / (cfg.get('dof_top', 300) * 2), 0, 1) ** 1.3 * 0.9 + np.clip((yy - 1500) / 192.0, 0, 1) * 0.7
    m = np.clip(m, 0, 1)[..., None]
    out = sharp * (1 - m) + blur * m
    g = np.random.default_rng(3).normal(0, 2.6, (H, W, 1)).astype(np.float32)
    res = Image.fromarray(np.clip(out + g, 0, 255).astype(np.uint8))
    res.save(os.path.join(OUT, name + '.jpg'), quality=88)
    res.resize((390, 846), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))
    json.dump(anchors, open(os.path.join(OUT, name + '_anchors.json'), 'w'))
    print(json.dumps(anchors))


CFG = dict(
    h=9.5, z=-8.0, pitch=33, f=900, hw=2.45, zend=12.4, wh=7.4, carpet=0.5, case_h=3.1,
    win_w=0.85, win_y=(3.5, 6.7),
    wallbays=[(-6.0, -0.5), (0.95, 3.3), (4.75, 7.1), (8.55, 12.3)],
    rows=[
        dict(z=0.0, cases=[('tor', -2.3, -0.62), ('his', 0.62, 2.3)]),
        dict(z=3.8, cases=[('poe', -2.3, -0.62), ('pro', 0.62, 2.3)]),
        dict(z=7.6, cases=[('gos', -2.3, -0.62), ('pau', 0.62, 2.3)]),
        dict(z=11.0, cases=[('gen', -0.85, 0.85)], both=True),
    ],
)


# ------------------------------------------------------------------ helpers for painted stills
def canvas(w, h, col):
    A = np.empty((h, w, 3), dtype=np.float32)
    A[:] = np.array(col, dtype=np.float32)
    return A


def mask_poly(w, h, pts, blur=0.0, ss=2):
    m = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(m).polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m).astype(np.float32)[..., None] / 255.0


def mask_ell(w, h, box, blur=0.0):
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).ellipse(box, fill=255)
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m).astype(np.float32)[..., None] / 255.0


def mask_rr(w, h, box, rad, corners=(True, True, True, True), blur=0.0):
    m = Image.new('L', (w * 2, h * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([box[0] * 2, box[1] * 2, box[2] * 2, box[3] * 2], rad * 2, fill=255, corners=corners)
    m = m.resize((w, h), Image.LANCZOS)
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    return np.asarray(m).astype(np.float32)[..., None] / 255.0


def lay(A, m, col, k=1.0):
    A *= (1 - m * k)
    A += m * k * (np.array(col, dtype=np.float32) if not isinstance(col, np.ndarray) else col)


def finish(A, path, blur=0.7, grain=2.4, vig=0.5, q=88, vc=(0.5, 0.47)):
    h, w = A.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = 1 - vig * np.clip(((xx - w * vc[0]) / (w * 0.75)) ** 2 + ((yy - h * vc[1]) / (h * 0.62)) ** 2, 0, 1)
    A = np.clip(A * v[..., None], 0, 255)
    im = Image.fromarray(A.astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    g = np.random.default_rng(5).normal(0, grain, (h, w, 1)).astype(np.float32)
    im = Image.fromarray(np.clip(np.asarray(im).astype(np.float32) + g, 0, 255).astype(np.uint8))
    im.save(path, quality=q)
    return im


def lo_noise(w, h, cell, seed):
    ng = np.random.default_rng(seed)
    return np.asarray(Image.fromarray((ng.random((h // cell + 2, w // cell + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255.0


# ------------------------------------------------------------------ front shelf (soft)
SHELF_ROWS = [
    (250, [('롬', 132, (118, 40, 42)), ('고전', 132, (44, 70, 110)), ('고후', 123, (52, 84, 124)), ('갈', 102, (150, 62, 40)),
           ('엡', 102, (52, 104, 92)), ('빌', 96, (70, 116, 100))]),
    (410, [('골', 96, (126, 88, 46)), ('살전', 99, (96, 60, 110)), ('살후', 93, (110, 72, 124))]),
    (570, [('딤전', 102, (60, 90, 62)), ('딤후', 96, (74, 104, 70)), ('딛', 93, (134, 96, 52)), ('몬', 87, (140, 54, 50))]),
]


def spine(A, x, yb, w, h, col):
    """x, yb (base), w, h in output px."""
    x0, y0, x1, y1 = int(x), int(yb - h), int(x + w), int(yb)
    sub = A[y0:y1, x0:x1]
    hh, ww = sub.shape[:2]
    u = (np.arange(ww, dtype=np.float32) + 0.5) / ww
    prof = 0.58 + 0.62 * np.exp(-((u - 0.34) / 0.30) ** 2)
    prof[:3] *= 0.6; prof[-3:] *= 0.55
    vv = 1.0 - 0.18 * (np.arange(hh, dtype=np.float32) / hh)
    C = np.array(col, dtype=np.float32)[None, None, :] * prof[None, :, None] * vv[:, None, None]
    gold = np.array((214, 176, 100), dtype=np.float32)[None, None, :] * prof[None, :, None]
    for (a, b) in ((18, 23), (28, 31), (hh - 34, hh - 29), (hh - 24, hh - 21)):
        C[a:b] = gold * 0.92
    # small ornament
    cy, cx = hh - 58, ww // 2
    for dy in range(-7, 8):
        for dx in range(-7, 8):
            if abs(dx) + abs(dy) <= 7:
                C[cy + dy, cx + dx] = gold[0, cx + dx] * 0.9
    m = Image.new('L', (ww * 2, hh * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, ww * 2 - 1, hh * 2 + 30], 14, fill=255)
    m = np.asarray(m.resize((ww, hh), Image.LANCZOS)).astype(np.float32)[..., None] / 255.0
    sub *= (1 - m); sub += m * C


def shelf_soft(name='shelf_soft'):
    A = canvas(W, H, (30, 22, 20))
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    A *= (0.88 + 0.24 * lo_noise(W, H, 60, 4)[..., None])
    R = lambda x0, y0, x1, y1, rad=0, blur=0.0: mask_rr(W, H, (x0 * 2, y0 * 2, x1 * 2, y1 * 2), rad * 2, blur=blur)
    Pm = lambda pts, blur=0.0: mask_poly(W, H, [(x * 2, y * 2) for x, y in pts], blur=blur)
    E = lambda x0, y0, x1, y1, blur=0.0: mask_ell(W, H, [x0 * 2, y0 * 2, x1 * 2, y1 * 2], blur)
    # soft shadow behind the case, then the frame with vertical grain
    lay(A, R(14, 60, 376, 622, 8, blur=18), (8, 6, 6), 0.8)
    g = np.asarray(Image.fromarray((np.random.default_rng(8).random((H // 40 + 2, W // 3 + 2)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32) / 255.0
    wood = np.array((112, 72, 42), dtype=np.float32)[None, None, :] * (0.84 + 0.32 * g[..., None])
    lay(A, R(24, 66, 366, 606, 5), wood)
    lay(A, R(24, 66, 366, 71, 3), (170, 120, 70), 0.7)            # lit top edge
    lay(A, R(20, 606, 370, 622, 3), wood * 0.8)                   # plinth
    comps = [(84, 250), (262, 410), (422, 570)]
    for (ya, yb) in comps:
        t = np.clip((yy - ya * 2) / ((yb - ya) * 2.0), 0, 1)
        dark = np.array((40, 28, 22), dtype=np.float32)[None, None, :] * (0.5 + 0.8 * t ** 0.8)[..., None]
        lay(A, R(38, ya, 352, yb, 1), dark)
    for (yb, books) in SHELF_ROWS:
        x = 42
        for (_, h, col) in books:
            lay(A, R(x + 3, yb - h + 6, x + 54, yb, 3, blur=3), (10, 8, 8), 0.55)   # shadow to the right of each spine
            spine(A, x * 2, yb * 2, 96, h * 2, col)
            x += 51
    for (ya, yb) in comps:
        lay(A, R(38, yb, 352, yb + 2.5), (186, 132, 76))           # board edge catching light
    # row 2: two leaning books and a candle on a brass dish
    for i, (c, hh) in enumerate([((104, 74, 44), 86), ((168, 142, 96), 80)]):
        x0 = 206 + i * 27
        lay(A, Pm([(x0 + 16, 410 - hh), (x0 + 38, 410 - hh + 6), (x0 + 23, 410), (x0, 410 - 5)]), c)
        lay(A, Pm([(x0 + 16, 410 - hh), (x0 + 21, 410 - hh + 1.5), (x0 + 5, 410 - 4), (x0, 410 - 5)]), tuple(min(255, v * 1.25) for v in c))
    cx, cb = 318, 410
    lay(A, E(cx - 22, cb - 8, cx + 22, cb + 1), (170, 126, 60))
    lay(A, E(cx - 15, cb - 7, cx + 15, cb - 2), (120, 86, 40))
    lay(A, R(cx - 6, cb - 48, cx + 6, cb - 4, 2), (226, 208, 172))
    lay(A, R(cx - 6, cb - 48, cx - 1, cb - 4, 2), (250, 238, 206), 0.8)
    lay(A, E(cx - 5, cb - 68, cx + 5, cb - 48, blur=1.4), (255, 206, 110))
    lay(A, E(cx - 2.5, cb - 61, cx + 2.5, cb - 49, blur=0.8), (255, 248, 224))
    # row 3: lying stack, ink pot, reed pen
    for i, (c, w) in enumerate([((84, 56, 96), 86), ((156, 116, 62), 76), ((52, 90, 96), 68)]):
        yb = 570 - i * 15
        lay(A, R(266, yb - 14, 266 + w, yb - 1, 2), c)
        lay(A, R(266 + w - 6, yb - 13, 266 + w - 1, yb - 2, 1), (226, 208, 170))
        lay(A, R(266, yb - 14, 266 + w, yb - 11, 1), tuple(min(255, v * 1.3) for v in c), 0.8)
    lay(A, R(316, 506, 334, 525, 4), (44, 36, 40))
    lay(A, Pm([(324, 508), (327, 509), (345, 462), (343, 461)]), (222, 204, 166))
    # light: the candle, plus a soft key from the upper left
    d = np.sqrt((xx - cx * 2) ** 2 + ((yy - (cb - 58) * 2) * 0.9) ** 2)
    L = np.exp(-(d / 430.0) ** 1.35)
    key = np.clip(1.25 - (xx / W) * 0.45 - (yy / H) * 0.95, 0.3, 1.1)
    warm = np.array([1.0, 0.84, 0.60], dtype=np.float32)
    cool = np.array([0.90, 0.88, 1.0], dtype=np.float32)
    for (ya, yb) in comps:                                          # shadow cast down from each board
        sh = np.clip(1 - (yy - ya * 2) / 64.0, 0, 1) * ((yy >= ya * 2) & (yy <= yb * 2) & (xx >= 76) & (xx <= 704))
        A *= (1 - 0.45 * sh[..., None])
    A = A * ((0.78 * key)[..., None] * cool + (1.15 * L)[..., None] * warm) + (np.exp(-(d / 70.0) ** 2)[..., None]) * np.array((110, 86, 40), dtype=np.float32)
    A[1264:] *= np.clip(1 - (yy[1264:] - 1264) / 300.0, 0.25, 1)[..., None]
    finish(A, os.path.join(OUT, name + '.jpg'), blur=0.7, vig=0.5, vc=(0.5, 0.40)).resize((390, 846), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))


# ------------------------------------------------------------------ dusk road (cover background)
def ridge(w, base, amp, seed, f1=1.0):
    r = random.Random(seed)
    xs = np.arange(w, dtype=np.float32)
    y = np.zeros(w, dtype=np.float32)
    for k in range(1, 6):
        y += math.sin(r.uniform(0, 6.28)) * 0 + np.sin(xs / w * 6.283 * k * f1 * r.uniform(0.6, 1.4) + r.uniform(0, 6.28)) * amp / (k ** 1.25)
    return base - y


def bg_road(name='bg_road'):
    w, h = 780, 1892      # painted taller, then the top 200 px is cropped so the horizon sits high
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    hz = 700.0
    # sky
    stops = [(0, (30, 46, 60)), (300, (64, 84, 92)), (520, (150, 132, 108)), (640, (226, 168, 100)), (hz, (246, 196, 120))]
    A = np.zeros((h, w, 3), dtype=np.float32)
    for (y0, c0), (y1, c1) in zip(stops, stops[1:]):
        t = np.clip((yy - y0) / (y1 - y0), 0, 1)[..., None]
        seg = ((yy >= y0) & (yy <= y1))[..., None]
        A = np.where(seg, np.array(c0, dtype=np.float32) * (1 - t) + np.array(c1, dtype=np.float32) * t, A)
    A = np.where((yy > hz)[..., None], np.array((246, 196, 120), dtype=np.float32), A)
    sx, sy = 520.0, 676.0
    d = np.sqrt((xx - sx) ** 2 + ((yy - sy) * 1.25) ** 2)
    A += (np.exp(-(d / 230.0) ** 1.4)[..., None]) * np.array((70, 56, 30), dtype=np.float32)
    A += (np.exp(-(d / 46.0) ** 2)[..., None]) * np.array((60, 60, 50), dtype=np.float32)
    # thin clouds lit from below
    r = random.Random(4)
    cl = Image.new('L', (w, h), 0)
    cd = ImageDraw.Draw(cl)
    for _ in range(9):
        cxp, cyp = r.uniform(-60, w + 60), r.uniform(250, 600)
        ww_, hh_ = r.uniform(180, 420), r.uniform(8, 20)
        cd.ellipse([cxp - ww_, cyp - hh_, cxp + ww_, cyp + hh_], fill=int(r.uniform(90, 170)))
    cm = np.asarray(cl.filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255.0
    A = A * (1 - cm * 0.55) + cm * 0.55 * np.array((236, 170, 120), dtype=np.float32)
    # hills, far to near
    layers = [(708, 26, (188, 142, 100), 1, 1.0), (730, 34, (150, 108, 76), 2, 1.3), (772, 44, (112, 78, 56), 3, 1.1), (840, 40, (80, 56, 42), 4, 0.8)]
    for (base, amp, col, seed, f1) in layers:
        rg = ridge(w, base, amp, seed, f1)
        m = (yy >= rg[None, :]).astype(np.float32)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)[..., None] / 255.0
        glow = np.exp(-((xx - sx) / 260.0) ** 2)[..., None] * np.clip(1 - (yy - rg[None, :]) / 60.0, 0, 1)[..., None]
        C = np.array(col, dtype=np.float32) * (1 + 0.35 * glow)
        A = A * (1 - m) + m * C
    # ground plane
    g0 = 880.0
    t = np.clip((yy - g0) / (h - g0), 0, 1)[..., None]
    G = np.array((92, 64, 46), dtype=np.float32) * (1 - t) + np.array((30, 22, 20), dtype=np.float32) * t
    gm = np.clip((yy - 850) / 60.0, 0, 1)[..., None]
    A = A * (1 - gm) + gm * G
    A *= (1 + gm * (0.24 * lo_noise(w, h, 40, 9)[..., None] - 0.12))
    # the road
    def cx_(t):
        return 400 + 210 * math.sin(t * 3.6 + 0.5) * (1 - t) ** 0.55 + (sx - 400) * t ** 1.4
    def wid(t):
        return 330 * (1 - t) ** 2.4 + 5
    def ry(t):
        return h + 40 - (h + 40 - 852) * (1 - (1 - t) ** 1.9)
    N = 140
    left, right = [], []
    for i in range(N + 1):
        t = i / N
        left.append((cx_(t) - wid(t), ry(t)))
        right.append((cx_(t) + wid(t), ry(t)))
    rm = mask_poly(w, h, left + right[::-1], blur=1.6, ss=1)
    tt = np.clip((h - yy) / (h - 852.0), 0, 1)[..., None]
    RC = np.array((120, 88, 62), dtype=np.float32) * (1 - tt) + np.array((232, 182, 118), dtype=np.float32) * tt ** 1.5
    A = A * (1 - rm) + rm * RC
    # paving joints across the road
    jd = Image.new('L', (w, h), 0)
    jdd = ImageDraw.Draw(jd)
    for i in range(1, 60):
        t = 1 - (1 - i / 60.0) ** 1.0
        t = (i / 60.0) ** 1.6
        y = ry(t)
        if i % 2 == 0:
            jdd.line([(cx_(t) - wid(t) * 0.9, y), (cx_(t) + wid(t) * 0.9, y)], fill=70, width=max(1, int(3 * (1 - t) + 1)))
    jm = np.asarray(jd.filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)[..., None] / 255.0
    A *= (1 - 0.32 * jm * rm)
    # olive tree at left
    tr = Image.new('L', (w, h), 0)
    td = ImageDraw.Draw(tr)
    td.polygon([(96, 1010), (120, 1010), (132, 900), (160, 840), (146, 834), (122, 880), (112, 820), (98, 822), (104, 900)], fill=255)
    rr = random.Random(12)
    for _ in range(46):
        a, rad = rr.uniform(0, 6.28), rr.uniform(0, 1)
        px, py = 126 + math.cos(a) * 118 * rad, 790 + math.sin(a) * 70 * rad
        s_ = rr.uniform(16, 38)
        td.ellipse([px - s_, py - s_ * 0.7, px + s_, py + s_ * 0.7], fill=255)
    tm = np.asarray(tr.filter(ImageFilter.GaussianBlur(1.4))).astype(np.float32)[..., None] / 255.0
    rim = np.clip(np.asarray(ImageChops.subtract(tr.filter(ImageFilter.GaussianBlur(1.4)), ImageChops.offset(tr, -5, 3).filter(ImageFilter.GaussianBlur(2)))).astype(np.float32) / 255.0, 0, 1)[..., None]
    A = A * (1 - tm) + tm * np.array((34, 30, 24), dtype=np.float32)
    A += rim * np.array((150, 104, 50), dtype=np.float32) * 0.8
    # traveler with a staff, walking away
    tv = 0.62
    px, py = cx_(tv) + 6, ry(tv)
    sc_ = 0.8
    fg = Image.new('L', (w * 2, h * 2), 0)
    fd = ImageDraw.Draw(fg)
    def P2(dx, dy):
        return ((px + dx * sc_) * 2, (py + dy * sc_) * 2)
    fd.polygon([P2(-15, 0), P2(15, 0), P2(11, -52), P2(8, -70), P2(-8, -70), P2(-11, -52)], fill=255)   # robe
    fd.ellipse([P2(-9, -90)[0], P2(-9, -90)[1], P2(9, -68)[0], P2(9, -68)[1]], fill=255)                 # head with cloth
    fd.polygon([P2(-13, -66), P2(13, -66), P2(17, -30), P2(-17, -30)], fill=255)                          # mantle
    fd.line([P2(22, 2), P2(19, -84)], fill=255, width=5)                                                  # staff
    fd.polygon([P2(-22, -40), P2(-12, -58), P2(-10, -30), P2(-24, -22)], fill=255)                        # bag
    fm = np.asarray(fg.resize((w, h), Image.LANCZOS)).astype(np.float32)[..., None] / 255.0
    shd = mask_poly(w, h, [(px - 11, py), (px + 11, py), (px - 22, py + 120), (px - 58, py + 120)], blur=5, ss=1)
    A *= (1 - 0.45 * shd)
    A = A * (1 - fm) + fm * np.array((30, 24, 22), dtype=np.float32)
    fr = np.clip(fm - np.roll(fm, -3, axis=1), 0, 1)
    A += fr * np.array((190, 130, 60), dtype=np.float32)
    # foreground grass and stones
    fgd = Image.new('L', (w, h), 0)
    gd = ImageDraw.Draw(fgd)
    r3 = random.Random(8)
    for _ in range(420):
        gx = r3.choice([r3.uniform(-20, 250), r3.uniform(560, 800)])
        gy = r3.uniform(h - 312, h + 28)
        gl = r3.uniform(30, 90)
        gd.line([(gx, gy), (gx + r3.uniform(-16, 16), gy - gl)], fill=255, width=2)
    gmk = np.asarray(fgd.filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)[..., None] / 255.0
    A = A * (1 - gmk * 0.85) + gmk * 0.85 * np.array((22, 18, 16), dtype=np.float32)
    # haze and low rays from the sun
    haze = np.exp(-((yy - 800) / 150.0) ** 2)[..., None] * np.exp(-((xx - sx) / 520.0) ** 2)[..., None]
    A += haze * np.array((64, 44, 20), dtype=np.float32)
    A = A[200:]
    finish(A, os.path.join(OUT, name + '.jpg'), blur=1.0, grain=3.0, vig=0.5, vc=(0.62, 0.34)).resize((390, 846), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))


# ------------------------------------------------------------------ lamp and scroll (background section)
def bg_lamp(name='bg_lamp'):
    w, h = 780, 600
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    A = canvas(w, h, (44, 32, 26))
    A *= (0.86 + 0.28 * lo_noise(w, h, 60, 2)[..., None])
    # window opening in a thick wall, dusk outside
    wx0, wx1, wy0, wy1 = 540, 716, 40, 300
    sky = np.zeros((h, w, 3), dtype=np.float32)
    t = np.clip((yy - wy0) / (wy1 - wy0), 0, 1)[..., None]
    sky[:] = np.array((44, 66, 82), dtype=np.float32) * (1 - t) + np.array((232, 160, 96), dtype=np.float32) * t
    hill = (yy > (246 + 14 * np.sin(xx / 46.0) + 8 * np.sin(xx / 17.0 + 1)))[..., None]
    sky = np.where(hill, np.array((70, 48, 40), dtype=np.float32), sky)
    pts = [(wx0, wy1), (wx0, wy0 + 88)] + [(628 + 88 * math.cos(math.radians(a)), wy0 + 88 - 88 * math.sin(math.radians(a))) for a in range(180, -1, -12)] + [(wx1, wy1)]
    wm = mask_poly(w, h, pts)
    lay(A, mask_poly(w, h, [(x - 16 if x < 628 else x, y) for x, y in pts]), (86, 64, 50))     # lit reveal of the wall
    A = A * (1 - wm) + wm * sky
    # table
    ty = 372
    tm = (yy >= ty)[..., None].astype(np.float32)
    grain = np.asarray(Image.fromarray((lo_noise(w // 10, h, 3, 6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32)[..., None] / 255.0
    T = np.array((104, 66, 38), dtype=np.float32) * (0.8 + 0.4 * grain)
    A = A * (1 - tm) + tm * T
    lay(A, ((yy >= ty) & (yy <= ty + 5))[..., None].astype(np.float32), (168, 116, 66))
    # scroll: sheet in perspective with rolled ends
    sheet = [(150, 428), (470, 414), (500, 540), (112, 560)]
    lay(A, mask_poly(w, h, [(x + 6, y + 10) for x, y in sheet], blur=8), (20, 14, 10), 0.6)
    lay(A, mask_poly(w, h, sheet), (228, 206, 160))
    for (ra, rb, rad) in (((150, 428), (112, 560), 13), ((470, 414), (500, 540), 13)):
        lay(A, mask_poly(w, h, [(ra[0] - rad, ra[1] - 4), (ra[0] + rad, ra[1] - 4), (rb[0] + rad, rb[1] + 4), (rb[0] - rad, rb[1] + 4)], blur=0.8), (196, 168, 118))
        lay(A, mask_poly(w, h, [(ra[0] - rad * 0.3, ra[1] - 4), (ra[0] + rad * 0.3, ra[1] - 4), (rb[0] + rad * 0.3, rb[1] + 4), (rb[0] - rad * 0.3, rb[1] + 4)], blur=1.6), (240, 222, 180))
    # big letters, as lines of strokes
    ink = Image.new('L', (w, h), 0)
    idr = ImageDraw.Draw(ink)
    r = random.Random(3)
    for row in range(5):
        v = (row + 0.8) / 5.8
        xl = 150 + (112 - 150) * v + 30
        xr = 470 + (500 - 470) * v - 30
        y = 428 + (560 - 428) * v - 6
        x = xl
        while x < xr - 12:
            ln = r.uniform(8, 20)
            if r.random() < 0.86:
                yo = -(x - xl) * 0.043 * (1 - v) - (x - xl) * 0.01 * v
                k = r.random()
                if k < 0.45:
                    idr.line([(x, y + yo), (x + ln, y + yo + r.uniform(-2, 2))], fill=255, width=4)
                elif k < 0.75:
                    idr.arc([x, y + yo - 6, x + ln, y + yo + 6], 20, 320, fill=255, width=3)
                else:
                    idr.line([(x, y + yo + 5), (x + ln * 0.5, y + yo - 5), (x + ln, y + yo + 5)], fill=255, width=3)
            x += ln + r.uniform(5, 10)
    im_ = np.asarray(ink.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[..., None] / 255.0
    A = A * (1 - 0.8 * im_) + 0.8 * im_ * np.array((52, 36, 28), dtype=np.float32)
    # reed pen and ink pot
    lay(A, mask_poly(w, h, [(520, 520), (526, 524), (640, 430), (636, 426)]), (214, 190, 140))
    lay(A, mask_poly(w, h, [(520, 520), (526, 524), (512, 534)]), (40, 30, 26))
    lay(A, mask_ell(w, h, [596, 486, 668, 546], 0.8), (58, 44, 40))
    lay(A, mask_ell(w, h, [606, 480, 658, 502], 0.8), (30, 22, 22))
    lay(A, mask_ell(w, h, [612, 484, 652, 498], 0.8), (12, 10, 14))
    # oil lamp: clay body, nozzle to the left, small handle
    lx, ly = 330, 350
    lay(A, mask_ell(w, h, [lx - 62, ly + 34, lx + 74, ly + 62], 6), (20, 14, 10), 0.7)
    lay(A, mask_poly(w, h, [(lx - 96, ly + 12), (lx - 30, ly - 2), (lx - 20, ly + 30), (lx - 84, ly + 28)], blur=1.0), (150, 86, 52))
    lay(A, mask_ell(w, h, [lx - 56, ly - 22, lx + 64, ly + 46], 0.8), (164, 94, 56))
    lay(A, mask_ell(w, h, [lx - 40, ly - 20, lx + 30, ly + 6], 5), (206, 130, 78), 0.6)
    lay(A, mask_ell(w, h, [lx - 14, ly - 16, lx + 22, ly - 2], 0.8), (60, 34, 24))
    hd = Image.new('L', (w, h), 0)
    ImageDraw.Draw(hd).ellipse([lx + 50, ly - 10, lx + 96, ly + 30], outline=255, width=9)
    lay(A, np.asarray(hd.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[..., None] / 255.0, (140, 78, 48))
    fx, fy = lx - 96, ly + 2
    flame = [(fx, fy + 10)] + [(fx + 13 * math.sin(math.radians(a)) * (0.5 + 0.5 * math.cos(math.radians(a / 2))), fy - 22 - 26 * math.cos(math.radians(a)) * 0 - 50 * (1 - abs(a) / 180.0)) for a in range(-180, 181, 20)]
    lay(A, mask_ell(w, h, [fx - 11, fy - 44, fx + 11, fy + 10], 2.2), (255, 196, 96))
    lay(A, mask_ell(w, h, [fx - 6, fy - 26, fx + 6, fy + 8], 1.6), (255, 244, 210))
    # light
    d = np.sqrt((xx - fx) ** 2 + ((yy - (fy - 16)) * 1.15) ** 2)
    L = np.exp(-(d / 250.0) ** 1.5)
    warm = np.array([1.0, 0.80, 0.52], dtype=np.float32)
    keep = wm[..., 0]
    lit = A * ((0.30 + 1.25 * L)[..., None] * warm + 0.06) + (np.exp(-(d / 52.0) ** 2)[..., None]) * np.array((120, 96, 50), dtype=np.float32)
    A = lit * (1 - keep[..., None] * 0.75) + A * keep[..., None] * 0.75
    finish(A, os.path.join(OUT, name + '.jpg'), blur=1.0, grain=3.0, vig=0.55, vc=(0.42, 0.55)).save(os.path.join(OUT, name + '_preview.png'))


def sheet():
    names = ['hall_q', 'shelf_soft', 'bg_road']
    ims = [Image.open(os.path.join(OUT, n + '_preview.png')) for n in names]
    sh = Image.new('RGB', (390 * 3 + 40, 846 + 20), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (10 + i * 400, 10))
    sh.save(os.path.join(OUT, '_sheet.png'))


if __name__ == '__main__':
    what = sys.argv[1:] or ['hall', 'shelf', 'road', 'lamp']
    if 'hall' in what: hall(CFG)
    if 'shelf' in what: shelf_soft()
    if 'road' in what: bg_road()
    if 'lamp' in what: bg_lamp()
    sheet()


def bg_lamp_p(name='bg_lamp_p', oy=300, woy=150):
    """Portrait version of the lamp-and-scroll still life: wall and window above, the table running down under the text."""
    w, h = 780, 1692
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    A = canvas(w, h, (44, 32, 26))
    A *= (0.86 + 0.28 * lo_noise(w, h, 60, 2)[..., None])
    wx0, wx1, wy0, wy1 = 500, 690, 60 + woy, 330 + woy
    sky = np.zeros((h, w, 3), dtype=np.float32)
    t = np.clip((yy - wy0) / (wy1 - wy0), 0, 1)[..., None]
    sky[:] = np.array((44, 66, 82), dtype=np.float32) * (1 - t) + np.array((232, 160, 96), dtype=np.float32) * t
    hill = (yy > (wy1 - 56 + 14 * np.sin(xx / 46.0) + 8 * np.sin(xx / 17.0 + 1)))[..., None]
    sky = np.where(hill, np.array((70, 48, 40), dtype=np.float32), sky)
    mx, rad = (wx0 + wx1) / 2, (wx1 - wx0) / 2
    pts = [(wx0, wy1), (wx0, wy0 + rad)] + [(mx + rad * math.cos(math.radians(a)), wy0 + rad - rad * math.sin(math.radians(a))) for a in range(180, -1, -12)] + [(wx1, wy1)]
    wm = mask_poly(w, h, pts)
    lay(A, mask_poly(w, h, [(x - 18 if x < mx else x, y) for x, y in pts]), (86, 64, 50))
    A = A * (1 - wm) + wm * sky
    ty = 372 + oy
    tm = (yy >= ty)[..., None].astype(np.float32)
    grain = np.asarray(Image.fromarray((lo_noise(w // 10, h, 3, 6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32)[..., None] / 255.0
    T = np.array((104, 66, 38), dtype=np.float32) * (0.8 + 0.4 * grain)
    A = A * (1 - tm) + tm * T
    lay(A, ((yy >= ty) & (yy <= ty + 5))[..., None].astype(np.float32), (168, 116, 66))
    S = lambda pts_: [(x, y + oy) for x, y in pts_]
    sheet = S([(150, 440), (470, 426), (512, 600), (100, 624)])
    lay(A, mask_poly(w, h, [(x + 6, y + 10) for x, y in sheet], blur=8), (20, 14, 10), 0.6)
    lay(A, mask_poly(w, h, sheet), (228, 206, 160))
    for (ra, rb, rad_) in ((sheet[0], sheet[3], 14), (sheet[1], sheet[2], 14)):
        lay(A, mask_poly(w, h, [(ra[0] - rad_, ra[1] - 4), (ra[0] + rad_, ra[1] - 4), (rb[0] + rad_, rb[1] + 4), (rb[0] - rad_, rb[1] + 4)], blur=0.8), (196, 168, 118))
        lay(A, mask_poly(w, h, [(ra[0] - rad_ * 0.3, ra[1] - 4), (ra[0] + rad_ * 0.3, ra[1] - 4), (rb[0] + rad_ * 0.3, rb[1] + 4), (rb[0] - rad_ * 0.3, rb[1] + 4)], blur=1.6), (240, 222, 180))
    ink = Image.new('L', (w, h), 0)
    idr = ImageDraw.Draw(ink)
    r = random.Random(3)
    for row in range(6):
        v = (row + 0.8) / 6.8
        xl = sheet[0][0] + (sheet[3][0] - sheet[0][0]) * v + 32
        xr = sheet[1][0] + (sheet[2][0] - sheet[1][0]) * v - 32
        y = sheet[0][1] + (sheet[3][1] - sheet[0][1]) * v - 4
        x = xl
        while x < xr - 12:
            ln = r.uniform(8, 20)
            if r.random() < 0.86:
                yo = -(x - xl) * 0.043 * (1 - v) - (x - xl) * 0.05 * v
                k = r.random()
                if k < 0.45:
                    idr.line([(x, y + yo), (x + ln, y + yo + r.uniform(-2, 2))], fill=255, width=4)
                elif k < 0.75:
                    idr.arc([x, y + yo - 6, x + ln, y + yo + 6], 20, 320, fill=255, width=3)
                else:
                    idr.line([(x, y + yo + 5), (x + ln * 0.5, y + yo - 5), (x + ln, y + yo + 5)], fill=255, width=3)
            x += ln + r.uniform(5, 10)
    im_ = np.asarray(ink.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[..., None] / 255.0
    A = A * (1 - 0.8 * im_) + 0.8 * im_ * np.array((52, 36, 28), dtype=np.float32)
    lay(A, mask_poly(w, h, S([(536, 560), (542, 564), (656, 470), (652, 466)])), (214, 190, 140))
    lay(A, mask_poly(w, h, S([(536, 560), (542, 564), (528, 574)])), (40, 30, 26))
    lay(A, mask_ell(w, h, [600, 500 + oy, 672, 560 + oy], 0.8), (58, 44, 40))
    lay(A, mask_ell(w, h, [610, 494 + oy, 662, 516 + oy], 0.8), (30, 22, 22))
    lay(A, mask_ell(w, h, [616, 498 + oy, 656, 512 + oy], 0.8), (12, 10, 14))
    lx, ly = 330, 350 + oy
    lay(A, mask_ell(w, h, [lx - 62, ly + 34, lx + 74, ly + 62], 6), (20, 14, 10), 0.7)
    lay(A, mask_poly(w, h, [(lx - 96, ly + 12), (lx - 30, ly - 2), (lx - 20, ly + 30), (lx - 84, ly + 28)], blur=1.0), (150, 86, 52))
    lay(A, mask_ell(w, h, [lx - 56, ly - 22, lx + 64, ly + 46], 0.8), (164, 94, 56))
    lay(A, mask_ell(w, h, [lx - 40, ly - 20, lx + 30, ly + 6], 5), (206, 130, 78), 0.6)
    lay(A, mask_ell(w, h, [lx - 14, ly - 16, lx + 22, ly - 2], 0.8), (60, 34, 24))
    hd = Image.new('L', (w, h), 0)
    ImageDraw.Draw(hd).ellipse([lx + 50, ly - 10, lx + 96, ly + 30], outline=255, width=9)
    lay(A, np.asarray(hd.filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32)[..., None] / 255.0, (140, 78, 48))
    fx, fy = lx - 96, ly + 2
    lay(A, mask_ell(w, h, [fx - 11, fy - 44, fx + 11, fy + 10], 2.2), (255, 196, 96))
    lay(A, mask_ell(w, h, [fx - 6, fy - 26, fx + 6, fy + 8], 1.6), (255, 244, 210))
    d = np.sqrt((xx - fx) ** 2 + ((yy - (fy - 16)) * 0.95) ** 2)
    L = np.exp(-(d / 330.0) ** 1.5)
    warm = np.array([1.0, 0.80, 0.52], dtype=np.float32)
    keep = wm[..., 0]
    lit = A * ((0.26 + 1.3 * L)[..., None] * warm + 0.05) + (np.exp(-(d / 56.0) ** 2)[..., None]) * np.array((120, 96, 50), dtype=np.float32)
    A = lit * (1 - keep[..., None] * 0.75) + A * keep[..., None] * 0.75
    finish(A, os.path.join(OUT, name + '.jpg'), blur=1.0, grain=3.0, vig=0.5, vc=(0.42, 0.40)).resize((390, 846), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))
    print('flame css', fx / 2, (fy - 17) / 2)
