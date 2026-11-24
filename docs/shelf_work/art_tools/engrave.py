# Old-print look: scenes are drawn as tone / hatch-class / wash / line plates, then "printed"
# as sepia line engraving with hand-colour washes on aged paper.
import math, random, os, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from soft import Scene, lo_noise, OUT

CW, CH = 390, 846          # css px
K = 4                      # css px -> plate px (2x output, 2x supersample)
OW, OH = CW * 2, CH * 2
INK = np.array((50, 33, 22), dtype=np.float32)


class Plate:
    def __init__(self, tone=0.9, cls=0, wash=(255, 255, 255)):
        sz = (CW * K, CH * K)
        self.tone = Image.new('L', sz, int(tone * 255)); self.dt = ImageDraw.Draw(self.tone)
        self.cls = Image.new('L', sz, cls); self.dc = ImageDraw.Draw(self.cls)
        self.wash = Image.new('RGB', sz, wash); self.dw = ImageDraw.Draw(self.wash)
        self.line = Image.new('L', sz, 0); self.dl = ImageDraw.Draw(self.line)

    def poly(self, pts, tone=0.9, cls=0, wash=None, lw=0.8, erase=True):
        p = [(x * K, y * K) for x, y in pts]
        self.dt.polygon(p, fill=int(max(0, min(1, tone)) * 255))
        self.dc.polygon(p, fill=cls)
        self.dw.polygon(p, fill=wash or (255, 255, 255))
        if erase:
            self.dl.polygon(p, fill=0)
        if lw:
            self.dl.line(p + [p[0]], fill=255, width=max(1, int(round(lw * K))), joint='curve')

    def stroke(self, pts, lw=0.6, v=255):
        self.dl.line([(x * K, y * K) for x, y in pts], fill=v, width=max(1, int(round(lw * K))), joint='curve')

    def rect(self, x0, y0, x1, y1, **kw):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)

    def ell(self, cx, cy, rx, ry, n=28, **kw):
        self.poly([(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)], **kw)


HATCH = {1: (45, -38), 2: (90, 28), 3: (0, 62), 4: (0, 45), 5: (45, -45), 6: (90, 40)}


def printit(pl, name, light=None, lift=None, seed=1, paper=(224, 204, 164), washA=0.58, vig=0.36, frame=True):
    w, h = OW, OH
    tone = np.asarray(pl.tone.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0
    cls = np.asarray(pl.cls.resize((w, h), Image.NEAREST))
    wash = np.asarray(pl.wash.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255.0
    line = np.asarray(pl.line.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    L = light if light is not None else np.full((h, w), 0.5, dtype=np.float32)
    v = 1 - vig * np.clip(((xx - w / 2) / (w * 0.66)) ** 2 + ((yy - h * 0.46) / (h * 0.60)) ** 2, 0, 1)
    tone = tone * (0.74 + 0.52 * L) * (0.55 + 0.45 * v)
    if lift is not None:
        tone = tone + lift * (1 - tone)
    tone = np.clip(tone, 0, 1)
    # paper with stains
    pp = np.array(paper, dtype=np.float32)[None, None, :] * (0.90 + 0.2 * lo_noise(w, h, 110, seed))[..., None] * (0.965 + 0.07 * lo_noise(w, h, 14, seed + 1))[..., None]
    pp *= (0.84 + 0.26 * L)[..., None] * v[..., None]
    edge = np.clip(1 - np.minimum(np.minimum(xx, w - xx), np.minimum(yy, h - yy)) / 90.0, 0, 1) ** 2
    pp = pp * (1 - 0.3 * edge[..., None]) + np.array((120, 84, 50), dtype=np.float32) * 0.3 * edge[..., None]
    rng = random.Random(seed + 5)
    fx = Image.new('L', (w, h), 0)
    fd = ImageDraw.Draw(fx)
    for _ in range(46):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(3, 15)
        fd.ellipse([x - r, y - r * rng.uniform(0.6, 1.2), x + r, y + r], fill=int(rng.uniform(40, 120)))
    fox = np.asarray(fx.filter(ImageFilter.GaussianBlur(5))).astype(np.float32)[..., None] / 255.0
    pp = pp * (1 - 0.34 * fox) + np.array((150, 104, 60), dtype=np.float32) * 0.34 * fox
    # hand colouring
    col = pp * (1 - washA * (1 - wash))
    # hatching
    wob = (lo_noise(w, h, 60, seed + 2) - 0.5) * 3.2 + (lo_noise(w, h, 9, seed + 3) - 0.5) * 1.1

    def lines(deg, sp, wd):
        a = math.radians(deg + 90)
        s = xx * math.cos(a) + yy * math.sin(a) + wob
        d = np.abs(((s / sp) % 1.0) - 0.5) * sp
        return np.clip(wd / 2 - d + 0.5, 0, 1) * np.clip(wd * 1.6, 0, 1)

    ink = np.zeros((h, w), dtype=np.float32)
    w1 = 2.1 * np.clip((0.84 - tone) / 0.34, 0, 1)
    w2 = 2.1 * np.clip((0.56 - tone) / 0.28, 0, 1)
    w3 = 2.0 * np.clip((0.33 - tone) / 0.22, 0, 1)
    for c, (a1, a2) in HATCH.items():
        m = (cls == c)
        if not m.any():
            continue
        k = np.maximum(lines(a1, 5.6, w1), lines(a2, 5.6, w2))
        k = np.maximum(k, lines(a1 + 90, 4.2, w3))
        ink = np.where(m, k, ink)
    ink = np.maximum(ink * 0.82, line)
    ink *= (0.80 + 0.2 * np.random.default_rng(seed).random((h, w)).astype(np.float32))
    out = col * (1 - 0.93 * ink[..., None]) + INK[None, None, :] * 0.93 * ink[..., None]
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.45))
    if frame:
        d = ImageDraw.Draw(im)
        for inset, wd in ((12, 2), (18, 1)):
            d.rectangle([inset, inset, w - 1 - inset, h - 1 - inset], outline=(70, 48, 32), width=wd)
    g = np.random.default_rng(seed + 9).normal(0, 2.2, (h, w, 1)).astype(np.float32)
    im = Image.fromarray(np.clip(np.asarray(im).astype(np.float32) + g, 0, 255).astype(np.uint8))
    im.save(os.path.join(OUT, name + '.jpg'), quality=86)
    im.resize((CW, CH), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))
    return im


def blur_map(draw_fn, blur):
    m = Image.new('L', (OW, OH), 0)
    draw_fn(ImageDraw.Draw(m))
    return np.asarray(m.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255.0


# ------------------------------------------------------------------ the hall
WOOD, WOOD_L, WOOD_D = (196, 156, 112), (214, 182, 136), (160, 120, 84)
_CALF, _CALF_D, _VEL, _VEL_D, _RED, _GRN, _BLU = (168, 118, 80), (136, 92, 62), (224, 208, 172), (204, 184, 144), (166, 84, 66), (116, 132, 104), (110, 120, 140)
EPALS = {
    'tor': [_CALF, _CALF_D, _VEL, _RED, _CALF],
    'his': [_CALF, _VEL, _CALF_D, _VEL_D, _CALF],
    'poe': [_CALF, _VEL, _GRN, _CALF_D, _VEL_D],
    'pro': [_CALF_D, _VEL, _BLU, _CALF, _VEL_D],
    'gos': [_VEL, _VEL_D, _CALF, _RED, _VEL],
    'pau': [_CALF, _RED, _VEL, _CALF_D, _VEL_D],
    'gen': [_CALF_D, _VEL, _CALF, _VEL_D, _BLU],
    'mix': [_CALF, _CALF_D, _VEL, _VEL_D, _RED, _GRN],
}


def hall(name='hall_e', seed=7, nine=False, night=False, flames=True, fp=False, cz=-2.6):
    # cz: 2026-11-24 밤 목사님 — 화살표로 한 걸음씩 걷기. 통로 안쪽에서 본 그림을 그릴 때의 눈 자리(z)
    # fp: 2026-11-24 목사님 — 위에서 내려다보는 그림 대신 1인칭(눈높이)으로 통로에 서서 본 서고
    rnd = random.Random(seed)
    sc = Scene(1.55, cz, 0, 500, cy_css=470) if fp else Scene(9.5, -8.0, 33, 900)
    pl = Plate(tone=0.7 if not fp else 0.3, cls=1)
    HW, Z0, Z1, WH, CHT = 2.45, (cz + 0.4 if fp else -6.0), 12.4, 7.4, 3.1
    NEAR = sc.cam[2] + 0.25

    def fog(zc):
        return min(max((zc - 10.0) / 17.0, 0.0), 1.0) * 0.6

    def q(pts, tone=0.9, cls=0, wash=None, lw=0.7, erase=True):
        if fp and min(p[2] for p in pts) < NEAR:
            return
        pp = [sc.P(*p) for p in pts]
        f = fog(sum(p[2] for p in pp) / len(pp))
        if wash:
            wash = tuple(int(c + (255 - c) * f * 0.7) for c in wash)
        pl.poly([(p[0] / K, p[1] / K) for p in pp], tone=tone + (1 - tone) * f, cls=cls, wash=wash, lw=lw * (1 - 0.5 * f) if lw else 0, erase=erase)

    def ln(pts, lw=0.5):
        if fp and min(p[2] for p in pts) < NEAR:
            return
        pp = [sc.P(*p) for p in pts]
        f = fog(sum(p[2] for p in pp) / len(pp))
        pl.stroke([(p[0] / K, p[1] / K) for p in pp], lw=lw * (1 - 0.5 * f))

    # floor: chequered flags
    T = 0.7
    nz = int((Z1 - Z0) / T) + 1
    for j in range(nz):
        z = Z0 + j * T
        for i in range(7):
            x = -HW + i * T
            dark = (i + j) % 2 == 0
            q([(x, 0, z), (x + T, 0, z), (x + T, 0, z + T), (x, 0, z + T)], tone=0.44 if dark else 0.96, cls=3 if dark else 0, wash=(168, 150, 132) if dark else (240, 230, 204), lw=0.45)
    # side walls: ashlar, then book presses between the stalls
    for s in (-1, 1):
        x = s * HW
        z = Z0
        while z < Z1:
            z2 = min(z + 1.0, Z1)
            q([(x, 0, z), (x, 0, z2), (x, WH, z2), (x, WH, z)], tone=0.6, cls=2, wash=(206, 196, 176), lw=0)
            z = z2
        for yy_ in np.arange(0.6, WH, 0.6):
            ln([(x, yy_, Z0), (x, yy_, Z1)], lw=0.35)
        for (za, zb) in ([(-6.0, -0.5), (0.95, 2.5), (3.65, 5.3), (6.45, 8.1), (9.25, 12.3)] if nine else [(-6.0, -0.5), (0.95, 3.3), (4.75, 7.1), (8.55, 12.3)]):
            for lv in range(4):
                y0 = 0.5 + lv * 1.05
                q([(x, y0 - 0.06, za), (x, y0 - 0.06, zb), (x, y0 + 0.92, zb), (x, y0 + 0.92, za)], tone=0.22, cls=5, wash=(170, 150, 126), lw=0.5)
                zz = za + 0.03
                while zz < zb - 0.1:
                    wd = rnd.uniform(0.1, 0.2)
                    hh = 0.9 * rnd.uniform(0.6, 0.92)
                    q([(x, y0, zz), (x, y0, zz + wd), (x, y0 + hh, zz + wd), (x, y0 + hh, zz)], tone=rnd.uniform(0.5, 0.8), cls=6, wash=rnd.choice(EPALS['mix']), lw=0.4)
                    zz += wd + 0.012
    if fp:   # 천장과 들보(눈높이에서는 위가 보임)
        q([(-HW, WH, Z0), (HW, WH, Z0), (HW, WH, Z1), (-HW, WH, Z1)], tone=0.42, cls=2, wash=(150, 132, 110), lw=0)
        for bz in np.arange(Z1 - 0.6, Z0 + 0.5, -1.5):
            q([(-HW, WH - 0.42, bz), (HW, WH - 0.42, bz), (HW, WH, bz), (-HW, WH, bz)], tone=0.3, cls=1, wash=WOOD_D, lw=0.7)
            q([(-HW, WH - 0.42, bz), (HW, WH - 0.42, bz), (HW, WH - 0.42, bz + 0.3), (-HW, WH - 0.42, bz + 0.3)], tone=0.2, cls=5, wash=WOOD_D, lw=0.5)
    # end wall with a tall lattice window
    q([(-HW, 0, Z1), (HW, 0, Z1), (HW, WH, Z1), (-HW, WH, Z1)], tone=0.74, cls=1, wash=(214, 204, 184), lw=0.8)
    for jy, yy_ in enumerate(np.arange(0.6, WH, 0.6)):
        ln([(-HW, yy_, Z1), (HW, yy_, Z1)], lw=0.3)
        for xx_ in np.arange(-HW + (0.45 if jy % 2 else 0.0), HW, 0.9):
            ln([(xx_, yy_, Z1), (xx_, yy_ + 0.6, Z1)], lw=0.25)
    ww, wy0, wy1 = 0.95, 3.4, 6.9

    def arch(wd, y0, y1, zz):
        pts = [(-wd, y0, zz), (wd, y0, zz)]
        for a in range(0, 181, 12):
            pts.append((wd * math.cos(math.radians(a)), y1 - wd * 1.25 + wd * 1.25 * math.sin(math.radians(a)), zz))
        return pts
    q(arch(ww + 0.16, wy0 - 0.12, wy1 + 0.14, Z1 - 0.01), tone=0.9, cls=0, wash=(226, 214, 190), lw=1.0)
    if night:   # 2026-11-24 목사님: 창의 빛을 막고 촛불로만 밝힘 — 덧문을 닫은 창
        q(arch(ww, wy0, wy1, Z1 - 0.02), tone=0.2, cls=1, wash=(92, 74, 56), lw=0.9)
        for yy_ in np.arange(wy0 + 0.35, wy1 - ww * 1.25, 0.42):
            ln([(-ww * 0.97, yy_, Z1 - 0.03), (ww * 0.97, yy_, Z1 - 0.03)], lw=0.45)
        for xx_ in (-ww * 0.5, ww * 0.5):
            ln([(xx_, wy0, Z1 - 0.03), (xx_, wy1 - ww * 0.7, Z1 - 0.03)], lw=0.35)
    else:
        q(arch(ww, wy0, wy1, Z1 - 0.02), tone=1.0, cls=0, wash=(255, 247, 214), lw=0.8)
    for k in ([] if night else np.arange(-4, 9, 0.28)):          # diamond lattice, clipped roughly to the opening
        for sgn in (1, -1):
            a = (-ww, wy0 + k, Z1 - 0.03); b = (ww, wy0 + k + sgn * 2 * ww, Z1 - 0.03)
            ya, yb = a[1], b[1]
            if max(ya, yb) < wy0 or min(ya, yb) > wy1 - 0.5:
                continue
            t0 = max(0.0, (wy0 - ya) / (yb - ya)) if yb != ya and ya < wy0 else 0.0
            t1 = 1.0
            if max(ya, yb) > wy1 - 0.55:
                continue
            ln([(a[0] + (b[0] - a[0]) * t0, ya + (yb - ya) * t0, a[2]), b], lw=0.22)
    ln([(0, wy0, Z1 - 0.03), (0, wy1, Z1 - 0.03)], lw=0.7)
    # stalls, far to near
    anchors = {'cases': {}, 'lanterns': []}
    lights, shadows = [], []
    if nine:   # 2026-11-24: nine presses — four pairs along the aisle, Revelation alone under the window
        rows = [dict(z=11.0, cases=[('rev', -0.85, 0.85)], both=True), dict(z=8.3, cases=[('pau', -2.3, -0.62), ('gen', 0.62, 2.3)]),
                dict(z=5.5, cases=[('gos', -2.3, -0.62), ('act', 0.62, 2.3)]), dict(z=2.7, cases=[('poe', -2.3, -0.62), ('pro', 0.62, 2.3)]),
                dict(z=0.0, cases=[('tor', -2.3, -0.62), ('his', 0.62, 2.3)])]
    else:
        rows = [dict(z=11.0, cases=[('gen', -0.85, 0.85)], both=True), dict(z=7.6, cases=[('gos', -2.3, -0.62), ('pau', 0.62, 2.3)]),
                dict(z=3.8, cases=[('poe', -2.3, -0.62), ('pro', 0.62, 2.3)]), dict(z=0.0, cases=[('tor', -2.3, -0.62), ('his', 0.62, 2.3)])]
    for r in rows:
        z = r['z']
        if z == (5.5 if nine else 3.8):   # a lectern with an open book stands in the aisle beyond the second stalls
            lz = 7.1 if nine else 5.6
            q([(-0.07, 0, lz), (0.07, 0, lz), (0.07, 1.05, lz), (-0.07, 1.05, lz)], tone=0.7, cls=2, wash=WOOD, lw=0.6)
            q([(-0.3, 0, lz - 0.02), (0.3, 0, lz - 0.02), (0.2, 0.1, lz - 0.02), (-0.2, 0.1, lz - 0.02)], tone=0.6, cls=1, wash=WOOD_D, lw=0.6)
            q([(-0.42, 1.0, lz - 0.1), (0.42, 1.0, lz - 0.1), (0.42, 1.34, lz + 0.3), (-0.42, 1.34, lz + 0.3)], tone=0.85, cls=4, wash=WOOD_L, lw=0.7)
            q([(-0.36, 1.04, lz - 0.08), (0, 1.03, lz - 0.08), (0, 1.31, lz + 0.26), (-0.36, 1.32, lz + 0.26)], tone=1.0, cls=0, wash=(250, 242, 216), lw=0.5)
            q([(0.36, 1.04, lz - 0.08), (0, 1.03, lz - 0.08), (0, 1.31, lz + 0.26), (0.36, 1.32, lz + 0.26)], tone=0.95, cls=0, wash=(244, 234, 204), lw=0.5)
        if fp and z < NEAR:   # 눈 뒤에 있는 서가 줄은 그리지 않음(그림자·촛불 자리도)
            continue
        for (key, xa, xb) in r['cases']:
            if fp:   # 눈 자리가 달라도 같은 서가에는 같은 책이 꽂히게, 서가마다 난수를 새로 시작
                rnd = random.Random(seed * 1000 + sum(map(ord, key)))
            inner = xa if abs(xa) < abs(xb) else xb
            zb = z + 0.75
            pal = EPALS.get(key) or EPALS[{'act': 'gos', 'rev': 'gen'}[key]]
            burnt = fp and night and r.get('both')   # 11-24 밤 목사님: 그을린 곳은 팻말이 아니라 배경으로
            if burnt:
                pal = [(58, 46, 36), (46, 36, 28), (70, 54, 40), (38, 30, 24), (84, 62, 44)]
            q([(inner, 0, z), (inner, 0, zb), (inner, CHT, zb), (inner, CHT, z)], tone=0.5, cls=2, wash=WOOD_D, lw=0.8)
            q([(xa - 0.08, CHT, z - 0.08), (xb + 0.08, CHT, z - 0.08), (xb + 0.08, CHT, zb), (xa - 0.08, CHT, zb)], tone=0.93, cls=4, wash=WOOD_L, lw=0.9)
            q([(xa, 0, z), (xb, 0, z), (xb, CHT, z), (xa, CHT, z)], tone=0.5 if burnt else 0.82, cls=1, wash=(92, 74, 56) if burnt else WOOD, lw=1.0)
            base, m = 0.3, 0.12
            sh = (CHT - base - 0.2) / 4
            for i in range(4):
                y0 = base + i * sh
                y1 = y0 + sh - 0.08
                q([(xa + m, y0, z), (xb - m, y0, z), (xb - m, y1, z), (xa + m, y1, z)], tone=0.2, cls=5, wash=(44, 34, 26) if burnt else (170, 150, 126), lw=0.6)
                x = xa + m + 0.02
                while x < xb - m - 0.07:
                    wd = rnd.uniform(0.08, 0.16)
                    if x + wd > xb - m - 0.01:
                        break
                    if rnd.random() < (0.34 if burnt else 0.06):
                        x += wd * (1.3 if burnt else 0.7)
                        continue
                    hh = (y1 - y0) * rnd.uniform(0.62, 0.94)
                    q([(x, y0, z), (x + wd, y0, z), (x + wd, y0 + hh, z), (x, y0 + hh, z)], tone=rnd.uniform(0.6, 0.92) * (0.6 if burnt else 1), cls=6, wash=rnd.choice(pal), lw=0.5)
                    rr_ = rnd.random()
                    if sc.css(x, y0, z)[2] > 52 and rr_ < 0.8:
                        for by in (0.74, 0.82, 0.2):
                            ln([(x, y0 + hh * by, z), (x + wd, y0 + hh * by, z)], lw=0.3)
                    x += wd + 0.01
            # cornice and plinth
            q([(xa - 0.08, CHT - 0.17, z - 0.08), (xb + 0.08, CHT - 0.17, z - 0.08), (xb + 0.08, CHT, z - 0.08), (xa - 0.08, CHT, z - 0.08)], tone=0.9, cls=0, wash=WOOD_L, lw=0.9)
            ln([(xa - 0.08, CHT - 0.09, z - 0.08), (xb + 0.08, CHT - 0.09, z - 0.08)], lw=0.35)
            q([(xa - 0.04, 0, z - 0.04), (xb + 0.04, 0, z - 0.04), (xb + 0.04, 0.24, z - 0.04), (xa - 0.04, 0.24, z - 0.04)], tone=0.7, cls=1, wash=WOOD_D, lw=0.8)
            cs = [sc.css(x_, y_, z) for x_ in (xa, xb) for y_ in (0, CHT)]
            anchors['cases'][key] = [round(min(c[0] for c in cs)), round(min(c[1] for c in cs)), round(max(c[0] for c in cs)), round(max(c[1] for c in cs))]
            za_, zb_ = (max(z - 0.7, NEAR + 0.05), z + 0.02) if fp else (z - 0.7, z + 0.8)
            shadows.append([sc.css(xa - 0.1, 0, za_), sc.css(xb + 0.1, 0, za_), sc.css(xb + 0.1, 0, zb_), sc.css(xa - 0.1, 0, zb_)])
            sides = [xa, xb] if r.get('both') else [inner]
            for edge in sides:
                sgn = (-1 if edge == xa else 1) if r.get('both') else (-1 if edge > 0 else 1)
                lx, lz, ly = edge + sgn * 0.3, z - 0.1, 2.2
                ln([(edge, ly + 0.06, lz), (lx - 0.04, ly + 0.06, lz), (lx, ly, lz)], lw=0.8)
                q([(lx - 0.1, ly - 0.03, lz), (lx + 0.1, ly - 0.03, lz), (lx + 0.07, ly + 0.02, lz), (lx - 0.07, ly + 0.02, lz)], tone=0.6, cls=1, wash=(170, 150, 110), lw=0.6)
                q([(lx - 0.035, ly + 0.02, lz), (lx + 0.035, ly + 0.02, lz), (lx + 0.035, ly + 0.26, lz), (lx - 0.035, ly + 0.26, lz)], tone=1.0, cls=0, wash=(252, 244, 222), lw=0.55)
                if night and r.get('both'):   # 맨 끝 서가(외경 쪽)의 촛불은 꺼 둠: 초만 있고 불꽃과 빛이 없음
                    ln([(lx, ly + 0.26, lz), (lx + 0.01, ly + 0.3, lz)], lw=0.5)
                    continue
                fpts = [(lx, ly + 0.48, lz)] + [(lx + 0.05 * math.sin(math.radians(a_)), ly + 0.345 + 0.075 * math.cos(math.radians(a_)), lz) for a_ in range(40, 321, 40)]
                if flames:   # 앱에서는 불꽃을 그림에 넣지 않고 화면에서 흔들리게 그림(11-24 목사님)
                    q(fpts, tone=1.0, cls=0, wash=(255, 226, 140), lw=0.5)
                hx, hy, hs = sc.css(lx, ly + 0.36, lz)
                for a in range(0, 360, 30):          # engraved rays around the flame
                    r0, r1 = hs * 0.2, hs * (0.44 if a % 60 == 0 else 0.33)
                    pl.stroke([(hx + r0 * math.cos(math.radians(a)), hy + r0 * math.sin(math.radians(a))), (hx + r1 * math.cos(math.radians(a)), hy + r1 * math.sin(math.radians(a)))], lw=0.4)
                bx, by, _ = sc.css(lx, 0, lz - 0.5)
                anchors['lanterns'].append([round(hx), round(hy), round(hs, 1)])
                lights.append((hx, hy, bx, by, hs))
    if fp:
        rnd = random.Random(seed + 99)
    # a ladder against the nearest left stall
    for lx in (-1.95, -1.45):
        q([(lx - 0.035, 0, -1.0), (lx + 0.035, 0, -1.0), (lx + 0.035, 3.0, -0.1), (lx - 0.035, 3.0, -0.1)], tone=0.85, cls=0, wash=WOOD, lw=0.6)
    for i in range(1, 10):
        t = i / 10.0
        ln([(-1.95, 3.0 * t, -1.0 + 0.9 * t), (-1.45, 3.0 * t, -1.0 + 0.9 * t)], lw=0.6)

    # light: the window and its shaft, the candles
    def draw(d):
        if not night:
            wx, wy, ws = sc.css(0, (wy0 + wy1) / 2, Z1)
            r = ws * 2 * 2.8
            d.ellipse([wx * 2 - r, wy * 2 - r * 1.3, wx * 2 + r, wy * 2 + r * 1.3], fill=255)
            a = sc.css(-0.6, 0, Z1 - 2.0); b = sc.css(0.6, 0, Z1 - 2.0); c = sc.css(1.5, 0, -4.5); e = sc.css(-1.5, 0, -4.5)
            d.polygon([(a[0] * 2, a[1] * 2), (b[0] * 2, b[1] * 2), (c[0] * 2, c[1] * 2), (e[0] * 2, e[1] * 2)], fill=170)
        for (hx, hy, bx, by, hs) in lights:
            r = hs * 2 * 1.5
            d.ellipse([bx * 2 - r, by * 2 - r * 0.5, bx * 2 + r, by * 2 + r * 0.5], fill=200)
            r2 = hs * 2 * 1.0
            d.ellipse([hx * 2 - r2, hy * 2 - r2, hx * 2 + r2, hy * 2 + r2 * 1.2], fill=210)
    L = blur_map(draw, 40)

    def draw_s(d):
        for qd in shadows:
            d.polygon([(p[0] * 2, p[1] * 2) for p in qd], fill=255)
    S = blur_map(draw_s, 14)

    def draw_a(d):
        for (hx, hy, bx, by, hs) in lights:
            r = hs * 2 * 0.62
            d.ellipse([hx * 2 - r, hy * 2 - r, hx * 2 + r, hy * 2 + r], fill=255)
    A = blur_map(draw_a, 12)
    if night:
        def draw_d(d):   # 어둠: 끝 벽과 그 앞 바닥, 끝 서가
            for P in ([sc.css(-HW, 0, Z1), sc.css(HW, 0, Z1), sc.css(HW, WH, Z1), sc.css(-HW, WH, Z1)], [sc.css(-1.5, 0, 9.7), sc.css(1.5, 0, 9.7), sc.css(1.5, 0, Z1), sc.css(-1.5, 0, Z1)]):
                d.polygon([(p_[0] * 2, p_[1] * 2) for p_ in P], fill=255)
        D = np.clip(blur_map(draw_d, 30) * 1.2, 0, 1)
        printit(pl, name, light=np.clip(0.2 + 1.0 * L - 0.3 * S - 0.4 * D, 0, 1.3), lift=0.6 * A, seed=seed)
        G = np.clip(L * 1.35, 0, 1)
        M = (0.5 + 0.5 * G) * (1 - 0.6 * D)
        fp = os.path.join(OUT, name + '.jpg')
        arr = np.asarray(Image.open(fp).convert('RGB')).astype(np.float32) * M[..., None]
        arr[..., 2] *= 0.95
        im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        im.save(fp, quality=86)
        im.resize((CW, CH), Image.LANCZOS).save(os.path.join(OUT, name + '_preview.png'))
    else:
        printit(pl, name, light=np.clip(0.25 + 0.95 * L - 0.3 * S, 0, 1.3), lift=0.6 * A, seed=seed)
    json.dump(anchors, open(os.path.join(OUT, name + '_anchors.json'), 'w'))
    print(json.dumps(anchors))


# ------------------------------------------------------------------ the press (front view)
SW = 56                      # spine width, css px
PRESS_ROWS = [
    (306, 49, [('로마서', 16, _CALF), ('고린도전서', 16, _VEL), ('고린도후서', 13, _VEL_D), ('갈라디아서', 6, _RED), ('에베소서', 6, _CALF_D)]),
    (540, 44, [('빌립보서', 4, _CALF), ('골로새서', 4, _VEL), ('데살로니가전서', 5, _CALF_D), ('데살로니가후서', 3, _CALF)]),
    (774, 44, [('디모데전서', 6, _GRN), ('디모데후서', 4, _CALF), ('디도서', 3, _VEL), ('빌레몬서', 1, _CALF_D)]),
]


def press(name='shelf_f', seed=9, deco=True, hfn=None):
    """Front view of one press. Every spine carries a paper label tall enough for the book's full name, set vertically."""
    pl = Plate(tone=0.74, cls=1, wash=(214, 204, 184))
    for y in range(20, 820, 46):
        pl.stroke([(0, y), (390, y)], lw=0.3)
        for x in range(-20 + (y // 46 % 2) * 40, 400, 80):
            pl.stroke([(x, y), (x, y + 46)], lw=0.3)
    pl.rect(0, 812, 390, 846, tone=0.55, cls=3, wash=(190, 164, 132), lw=0.8)
    pl.stroke([(0, 828), (390, 828)], lw=0.4)
    pl.rect(24, 84, 366, 790, tone=0.8, cls=1, wash=WOOD, lw=1.2)
    comps = ((96, 306), (318, 540), (552, 774))
    for (ya, yb) in comps:
        pl.rect(40, ya, 350, yb, tone=0.2, cls=5, wash=(168, 146, 120), lw=0.9)
    pl.rect(28, 72, 362, 84, tone=0.86, cls=0, wash=WOOD_L, lw=1.0)
    pl.rect(22, 62, 368, 72, tone=0.72, cls=1, wash=WOOD, lw=1.0)
    pl.rect(16, 52, 374, 62, tone=0.92, cls=0, wash=WOOD_L, lw=1.1)
    for x in range(32, 360, 12):
        pl.rect(x, 74, x + 6, 82, tone=0.6, cls=1, wash=WOOD_D, lw=0.4)
    for x0 in (24, 350):
        for dx in (4, 8, 12):
            pl.stroke([(x0 + dx, 100), (x0 + dx, 782)], lw=0.35)
    for (_, yb) in comps:
        pl.rect(36, yb, 354, yb + 12, tone=0.9, cls=0, wash=WOOD_L, lw=0.9)
        pl.stroke([(36, yb + 4), (354, yb + 4)], lw=0.3)
    pl.rect(18, 786, 372, 812, tone=0.7, cls=1, wash=WOOD_D, lw=1.2)
    pl.rect(40, 792, 350, 806, tone=0.82, cls=0, wash=WOOD, lw=0.5)
    labels = {}
    for (yb, x0, books) in PRESS_ROWS:
        x = x0
        for (nm, ch, col) in books:
            h = int(round(hfn(ch) if hfn else 130 + 4.4 * ch))
            top = yb - h
            hw = SW / 2.0
            body = [(x, yb), (x, top + 5)] + [(x + hw - hw * math.cos(math.radians(a)), top + 5 - 5 * math.sin(math.radians(a))) for a in range(0, 181, 20)] + [(x + SW, top + 5), (x + SW, yb)]
            pl.poly(body, tone=0.9, cls=0, wash=col, lw=0.9)
            # 2026-11-24 목사님: 책등이 오른쪽으로 쏠려 보임 — 그늘을 양쪽에 같게 두어 이름표가 가운데로 보이게
            pl.rect(x + 0.6, top + 6, x + 4, yb - 1, tone=0.5, cls=6, wash=col, lw=0, erase=False)
            pl.rect(x + 4, top + 6, x + 9, yb - 1, tone=0.76, cls=6, wash=col, lw=0, erase=False)
            pl.rect(x + SW - 9, top + 6, x + SW - 4, yb - 1, tone=0.76, cls=6, wash=col, lw=0, erase=False)
            pl.rect(x + SW - 4, top + 6, x + SW - 0.7, yb - 1, tone=0.5, cls=6, wash=col, lw=0, erase=False)
            pl.stroke(body + [body[0]], lw=0.9)
            two = len(nm) > 5
            rows = 5 if two else len(nm)
            lw_, lh = (42 if two else 30), rows * 17 + 12
            lx, ly = x + (SW - lw_) / 2.0, top + 26
            bands = [top + 14, top + 19, yb - 8]
            if ly + lh < yb - 30:
                bands += [yb - 26, yb - 21]
            for by in bands:
                pl.stroke([(x + 0.5, by), (x + SW - 0.5, by)], lw=0.4)
            pl.rect(lx, ly, lx + lw_, ly + lh, tone=1.0, cls=0, wash=(250, 242, 218), lw=0.6)
            pl.stroke([(lx + 2, ly + 2), (lx + lw_ - 2, ly + 2), (lx + lw_ - 2, ly + lh - 2), (lx + 2, ly + lh - 2), (lx + 2, ly + 2)], lw=0.25)
            labels[nm] = [x, top, h, round(lx - x, 1), 26, lw_, lh]
            x += SW + 3
    cx, cb = 316, 540
    if deco:
        # row 2: candlestick
        pl.poly([(cx - 20, cb), (cx + 20, cb), (cx + 14, cb - 6), (cx - 14, cb - 6)], tone=0.7, cls=1, wash=(190, 160, 96), lw=0.8)
        pl.rect(cx - 3, cb - 20, cx + 3, cb - 6, tone=0.75, cls=2, wash=(190, 160, 96), lw=0.7)
        pl.poly([(cx - 13, cb - 20), (cx + 13, cb - 20), (cx + 9, cb - 25), (cx - 9, cb - 25)], tone=0.8, cls=1, wash=(190, 160, 96), lw=0.7)
        pl.rect(cx - 5, cb - 60, cx + 5, cb - 25, tone=1.0, cls=0, wash=(250, 242, 218), lw=0.7)
        pl.stroke([(cx + 2.5, cb - 58), (cx + 2.5, cb - 27)], lw=0.3)
        fl = [(cx, cb - 82)] + [(cx + 5 * math.sin(math.radians(a)), cb - 70 + 9 * math.cos(math.radians(a))) for a in range(40, 321, 20)]
        pl.poly(fl, tone=1.0, cls=0, wash=(255, 232, 150), lw=0.6)
        for a in range(0, 360, 20):
            r0, r1 = 17, (30 if a % 40 == 0 else 24)
            pl.stroke([(cx + r0 * math.cos(math.radians(a)), cb - 72 + r0 * math.sin(math.radians(a))), (cx + r1 * math.cos(math.radians(a)), cb - 72 + r1 * math.sin(math.radians(a)))], lw=0.35)
        # row 3: lying volumes with an hourglass, ink and quill on top
        for i, (c, wd) in enumerate([(_CALF, 62), (_VEL, 56), (_RED, 50)]):
            yb = 774 - i * 15
            pl.rect(286, yb - 15, 286 + wd, yb, tone=0.82, cls=4, wash=c, lw=0.8)
            pl.rect(286 + wd - 8, yb - 13, 286 + wd - 1, yb - 2, tone=1.0, cls=0, wash=(250, 242, 218), lw=0.4)
            for bx in (293, 299):
                pl.stroke([(bx, yb - 15), (bx, yb)], lw=0.35)
        hx, hy = 302, 729
        pl.rect(hx - 13, hy - 42, hx + 13, hy - 38, tone=0.8, cls=1, wash=WOOD, lw=0.6)
        pl.rect(hx - 13, hy - 4, hx + 13, hy, tone=0.8, cls=1, wash=WOOD, lw=0.6)
        pl.poly([(hx - 9, hy - 38), (hx + 9, hy - 38), (hx + 1.5, hy - 21), (hx + 9, hy - 4), (hx - 9, hy - 4), (hx - 1.5, hy - 21)], tone=1.0, cls=0, wash=(236, 240, 232), lw=0.6)
        pl.poly([(hx - 6, hy - 4), (hx + 6, hy - 4), (hx, hy - 13)], tone=0.6, cls=1, wash=(200, 170, 120), lw=0.3)
        for px in (hx - 11, hx + 11):
            pl.stroke([(px, hy - 38), (px, hy - 4)], lw=0.5)
        pl.poly([(322, 729), (336, 729), (334, 716), (324, 716)], tone=0.35, cls=5, wash=(120, 110, 110), lw=0.7)
        pl.poly([(328, 717), (331, 718), (346, 672), (343, 671)], tone=1.0, cls=0, wash=(250, 242, 218), lw=0.5)
        for t in np.arange(0.2, 0.95, 0.1):
            qx, qy = 330 + 15 * t, 717 - 46 * t
            pl.stroke([(qx, qy), (qx + 6 - 3 * t, qy - 2)], lw=0.3)

    def draw(d):
        d.ellipse([(cx - 200) * 2, (cb - 330) * 2, (cx + 200) * 2, (cb + 200) * 2], fill=255)
        d.ellipse([-200, -300, 620, 760], fill=120)
    L = blur_map(draw, 70)

    def draw_a(d):
        if deco:
            d.ellipse([(cx - 62) * 2, (cb - 138) * 2, (cx + 62) * 2, (cb - 8) * 2], fill=255)
    A = blur_map(draw_a, 26)
    printit(pl, name, light=0.3 + 0.8 * L, lift=0.62 * A, seed=seed, vig=0.3)
    json.dump(labels, open(os.path.join(OUT, name + '_labels.json'), 'w'), ensure_ascii=False)
    print(json.dumps(labels, ensure_ascii=False))


if __name__ == '__main__':
    what = sys.argv[1:] or ['hall', 'press']
    if 'hall' in what: hall()
    if 'press' in what: press()
    ims = [Image.open(os.path.join(OUT, n + '_preview.png')) for n in ('hall_e', 'shelf_f') if os.path.exists(os.path.join(OUT, n + '_preview.png'))]
    sh = Image.new('RGB', (400 * len(ims) + 10, 866), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (10 + i * 400, 10))
    sh.save(os.path.join(OUT, '_sheet_e.png'))
