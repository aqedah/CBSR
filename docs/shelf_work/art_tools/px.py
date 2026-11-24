"""Small pixel-art toolkit for the 성경책장 design mockups."""
from PIL import Image, ImageDraw
import random, math

W, H = 130, 282          # art pixels; shown at 3x = 390 x 846 CSS px
SCALE = 6                # saved at 6x so 3x CSS stays crisp on 2x screens


def C(s):
    if isinstance(s, tuple):
        return s[:3]
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def mix(a, b, t):
    a, b = C(a), C(b)
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def dark(c, t):
    return mix(c, '#000000', t)


def lite(c, t):
    return mix(c, '#ffffff', t)


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

# palette
INK = '#1a1210'
INK2 = '#2a1d17'
WOOD = '#5c3a21'
WOOD_D = '#422816'
WOOD_DD = '#2c1a0f'
WOOD_L = '#7a5230'
WOOD_LL = '#9a6c3f'
STONE = '#4b4650'
STONE_D = '#37333c'
STONE_DD = '#26232b'
STONE_L = '#5e5863'
STONE_LL = '#736c79'
PARCH = '#e6d3a3'
PARCH_L = '#f0e2bb'
PARCH_D = '#d6bf8a'
PARCH_DD = '#bfa36a'
PARCH_B = '#9c7b47'
GOLD = '#d9a93f'
GOLD_L = '#f2cf63'
GOLD_D = '#a67a25'
FL1 = '#fff1a8'
FL2 = '#ffd15a'
FL3 = '#ff9b3d'
FL4 = '#e2582b'
WINE = '#7b2d2f'
RED = '#b23a2e'
BLUE = '#2e3f66'
BLUE_L = '#4a6296'
GREEN = '#2f5c48'
SKIN = '#e2b48c'
SKIN_D = '#b98561'
BOOKC = ['#7b2d2f', '#2f5c48', '#2e3f66', '#b07d2c', '#5b3861', '#2d6770',
         '#70492a', '#cbb689', '#a24a2a', '#44506b', '#3f6b3a', '#8a3b55']


class Cv:
    def __init__(s, w=W, h=H, bg='#000000', alpha=False):
        s.w, s.h = w, h
        s.alpha = alpha
        fill = (0, 0, 0, 0) if alpha else C(bg) + (255,)
        s.im = Image.new('RGBA', (w, h), fill)
        s.d = ImageDraw.Draw(s.im)
        s.px = s.im.load()

    def p(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h:
            s.px[x, y] = C(c) + (255,)

    def g(s, x, y):
        return s.px[x, y][:3]

    def r(s, x, y, w, h, c):
        if w <= 0 or h <= 0:
            return
        s.d.rectangle([x, y, x + w - 1, y + h - 1], fill=C(c) + (255,))

    def box(s, x, y, w, h, c):
        s.r(x, y, w, 1, c); s.r(x, y + h - 1, w, 1, c)
        s.r(x, y, 1, h, c); s.r(x + w - 1, y, 1, h, c)

    def poly(s, pts, c):
        s.d.polygon([(int(round(a)), int(round(b))) for a, b in pts], fill=C(c) + (255,))

    def line(s, x0, y0, x1, y1, c):
        s.d.line([int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))], fill=C(c) + (255,), width=1)

    def dith(s, x, y, w, h, c, thr=8):
        for yy in range(max(0, y), min(s.h, y + h)):
            for xx in range(max(0, x), min(s.w, x + w)):
                if BAYER[yy % 4][xx % 4] < thr:
                    s.px[xx, yy] = C(c) + (255,)

    def spr(s, x, y, rows, pal, flip=False, k=1):
        for j, row in enumerate(rows):
            rr = row[::-1] if flip else row
            for i, ch in enumerate(rr):
                if ch in pal:
                    if k == 1:
                        s.p(x + i, y + j, pal[ch])
                    else:
                        s.r(x + i * k, y + j * k, k, k, pal[ch])

    def paste(s, other, x, y):
        s.im.alpha_composite(other.im, (x, y))
        s.d = ImageDraw.Draw(s.im)
        s.px = s.im.load()

    def save(s, path, scale=SCALE):
        im = s.im if s.alpha else s.im.convert('RGB')
        im.resize((s.w * scale, s.h * scale), Image.NEAREST).save(path, optimize=True)


def light(cv, lights, ambient=0.22, x0=0, y0=0, x1=None, y1=None, steps=7, floor=0.16):
    """Quantised, dithered candle light. lights: (x, y, radius, intensity)."""
    x1 = cv.w if x1 is None else x1
    y1 = cv.h if y1 is None else y1
    for y in range(y0, y1):
        for x in range(x0, x1):
            if cv.px[x, y][3] == 0:
                continue
            L = ambient
            for (lx, ly, rad, inten) in lights:
                d = math.hypot(x - lx, y - ly)
                if d < rad:
                    L += inten * (1 - d / rad) ** 1.7
            L = min(1.0, L)
            q = L * (steps - 1)
            lo = int(q)
            fr = q - lo
            if lo < steps - 1 and fr > (BAYER[y % 4][x % 4] + 0.5) / 16:
                lo += 1
            f = floor + (1 - floor) * lo / (steps - 1)
            r, g, b = cv.g(x, y)
            nr = int(r * f * (0.78 + 0.22 * f))
            ng = int(g * f * (0.82 + 0.18 * f))
            nb = int(min(255, b * f * (1.0 + 0.30 * (1 - f))))
            if f > 0.9:
                nr = min(255, int(nr * 1.05))
            cv.px[x, y] = (nr, ng, nb, 255)


def stone(cv, x, y, w, h, rnd, base=STONE, d=STONE_D, l=STONE_L, bw=12, bh=6):
    cv.r(x, y, w, h, base)
    for row in range(0, h, bh):
        off = ((row // bh) % 2) * (bw // 2)
        for xx in range(x, x + w):
            cv.p(xx, y + row, d)
        for col in range(-off, w, bw):
            if 0 <= col < w:
                for yy in range(row, min(h, row + bh)):
                    cv.p(x + col, y + yy, d)
            # block tone variation
            t = rnd.random()
            if t < 0.22 or t > 0.82:
                tone = l if t < 0.22 else mix(base, d, 0.5)
                for yy in range(row + 1, min(h, row + bh)):
                    for xx in range(max(0, col + 1), min(w, col + bw)):
                        cv.p(x + xx, y + yy, tone)
    for _ in range(w * h // 40):
        cv.p(x + rnd.randrange(w), y + rnd.randrange(h), rnd.choice([d, l]))


def planks(cv, x, y, w, h, rnd, base=WOOD, d=WOOD_D, l=WOOD_L, ph=7):
    cv.r(x, y, w, h, base)
    for row in range(0, h, ph):
        for xx in range(x, x + w):
            cv.p(xx, y + row, d)
        j = rnd.randrange(8, 30)
        for col in range(j, w, rnd.randrange(22, 40)):
            for yy in range(row, min(h, row + ph)):
                cv.p(x + col, y + yy, d)
        for _ in range(max(1, w // 14)):
            gx = rnd.randrange(w - 6)
            gy = row + rnd.randrange(2, max(3, ph - 1))
            if gy < h:
                cv.r(x + gx, y + gy, rnd.randrange(3, 8), 1, rnd.choice([d, l, l]))


def parchment(cv, x, y, w, h, rnd, torn=True, burn=5):
    cv.r(x, y, w, h, PARCH)
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            t = rnd.random()
            if t < 0.05:
                cv.p(xx, yy, PARCH_D)
            elif t < 0.085:
                cv.p(xx, yy, PARCH_L)
    # stains
    for _ in range(max(2, w * h // 2600)):
        cx, cy, rr = x + rnd.randrange(w), y + rnd.randrange(h), rnd.randrange(4, 10)
        for yy in range(cy - rr, cy + rr):
            for xx in range(cx - rr, cx + rr):
                if x <= xx < x + w and y <= yy < y + h and math.hypot(xx - cx, yy - cy) < rr:
                    if BAYER[yy % 4][xx % 4] < 5:
                        cv.p(xx, yy, PARCH_D)
    # edge burn
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            dd = min(xx - x, x + w - 1 - xx, yy - y, y + h - 1 - yy)
            if dd < burn:
                thr = [15, 10, 6, 3, 1][dd] if dd < 5 else 0
                if BAYER[yy % 4][xx % 4] < thr:
                    cv.p(xx, yy, PARCH_DD if dd > 0 else PARCH_B)
    if torn:
        for xx in range(x, x + w):
            if rnd.random() < 0.3:
                cv.p(xx, y, PARCH_B)
            if rnd.random() < 0.3:
                cv.p(xx, y + h - 1, PARCH_B)
        for yy in range(y, y + h):
            if rnd.random() < 0.3:
                cv.p(x, yy, PARCH_B)
            if rnd.random() < 0.3:
                cv.p(x + w - 1, yy, PARCH_B)


def spine(cv, x, y, w, h, col, bands=True):
    cv.r(x, y, w, h, col)
    if w >= 3:
        cv.r(x, y, 1, h, lite(col, 0.22))
        cv.r(x + w - 1, y, 1, h, dark(col, 0.35))
    elif w == 2:
        cv.r(x + 1, y, 1, h, dark(col, 0.28))
    cv.r(x, y, w, 1, lite(col, 0.3))
    if bands and h >= 8:
        cv.r(x, y + 2, w, 1, GOLD_D)
        if h >= 12:
            cv.r(x, y + h - 3, w, 1, GOLD_D)


def shelf_row(cv, x, y, w, h, rnd, colors=BOOKC, widths=None):
    """Fill a shelf row with spines. Returns [(x, w, top_y, h)]."""
    cv.r(x, y, w, h, '#20140e')
    out = []
    cx = x
    if widths is not None:
        for i, bw in enumerate(widths):
            bh = h - [1, 0, 2, 0, 1, 3, 0, 2][i % 8]
            col = colors[i % len(colors)]
            spine(cv, cx, y + h - bh, bw, bh, col)
            out.append((cx, bw, y + h - bh, bh))
            cx += bw + 1
        return out
    while cx < x + w - 1:
        bw = rnd.choice([2, 2, 3, 3, 3, 4])
        if cx + bw > x + w:
            break
        if rnd.random() < 0.07:
            cx += rnd.choice([1, 2, 3])
            continue
        bh = h - rnd.choice([0, 0, 1, 1, 2, 3])
        spine(cv, cx, y + h - bh, bw, bh, rnd.choice(colors))
        out.append((cx, bw, y + h - bh, bh))
        cx += bw
    return out


def bookshelf(cv, x, y, w, h, rows, rnd, colors=BOOKC):
    cv.r(x, y, w, h, WOOD_D)
    cv.r(x, y, w, 1, WOOD_L)
    cv.r(x, y, 1, h, WOOD)
    cv.r(x + w - 1, y, 1, h, WOOD_DD)
    rh = (h - 2 - (rows - 1)) // rows
    yy = y + 1
    for _ in range(rows):
        shelf_row(cv, x + 1, yy, w - 2, rh, rnd, colors)
        yy += rh
        cv.r(x + 1, yy, w - 2, 1, WOOD_L)
        yy += 1


def candle(cv, x, y, tall=4):
    """x,y = base centre-left of a 2px candle; returns flame position."""
    cv.r(x - 1, y, 4, 1, GOLD_D)
    cv.r(x, y - tall, 2, tall, '#efe3c4')
    cv.r(x + 1, y - tall, 1, tall, '#cdbf9c')
    cv.r(x, y - tall - 3, 2, 3, FL3)
    cv.p(x, y - tall - 2, FL2)
    cv.p(x + 1, y - tall - 2, FL1)
    cv.p(x, y - tall - 4, FL2)
    return (x + 1, y - tall - 2)


# ---------------------------------------------------------------- sprites
LIBRARIAN = [
    "....hhhh....",
    "...hhhhhh...",
    "..hhsssshh..",
    "..hsessesh..",
    "..hssssssh..",
    "..hwwwwwwh..",
    "..rrwwwwrr..",
    ".rrrrwwrrrr.",
    ".rrrrrrrrrr.",
    ".rRrrrrrrRr.",
    ".sRrbbbbrRs.",
    "..rrbBBbrr..",
    "..rrrrrrrr..",
    "..rrrrrrrr..",
    "..rRrrrrRr..",
    ".rrRrrrrRrr.",
    ".RRRRRRRRRR.",
]
LIB_PAL = {'h': '#274a3b', 'r': '#2f5c48', 'R': '#21412f', 's': SKIN, 'e': INK,
           'w': '#d8d2c4', 'b': '#7b2d2f', 'B': GOLD}

PLAYER = [
    "....kkkk....",
    "...kkkkkk...",
    "...kssssk...",
    "...sesses...",
    "...ssssss...",
    "....ssss....",
    "..oottttoo..",
    ".ooottttooo.",
    ".ooogttgooo.",
    ".oOottttoOo.",
    ".soottttoos.",
    "..ooLLLLoo..",
    "...tttttt...",
    "...tt..tt...",
    "...tt..tt...",
    "...BB..BB...",
]
PLAYER_PAL = {'k': '#3a2718', 's': SKIN, 'e': INK, 'o': '#d9622b', 'O': '#a84519',
              't': '#e9dcb8', 'g': GOLD, 'L': '#70492a', 'B': '#3a2718'}

PLAYER_BACK = [
    "....kkkk....",
    "...kkkkkk...",
    "...kkkkkk...",
    "...kkkkkk...",
    "...skkkks...",
    "....ssss....",
    "..oooooooo..",
    ".oooooooooo.",
    ".oooOooOooo.",
    ".oooOooOooo.",
    ".sooOooOoos.",
    "..ooOooOoo..",
    "...oooooo...",
    "...tt..tt...",
    "...tt..tt...",
    "...BB..BB...",
]

PAUL = [
    "....ssss....",
    "...ssssss...",
    "..kssssssk..",
    "..ksessesk..",
    "..kssssssk..",
    "...kkkkkk...",
    "...kkkkkk...",
    "..cckkkkcc..",
    ".ccctttcccc.",
    ".ccttttttcc.",
    ".cCttttttCc.",
    ".sCtwwwwtCs.",
    "..ctwWWwtc..",
    "..cttttttc..",
    "..cttttttc..",
    "..cCttttCc..",
    ".ccCttttCcc.",
]
PAUL_PAL = {'s': SKIN, 'e': INK, 'k': '#3b2a20', 'c': '#7a5230', 'C': '#5c3a21',
            't': '#e4d6b0', 'w': '#f3ead0', 'W': '#b9a67a'}
