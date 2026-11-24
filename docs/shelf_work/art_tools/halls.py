"""Five library ("서고") scenes."""
from px import *
import random, math, json, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
ANCH = {}


# ------------------------------------------------------------------ 1 쿼터뷰
def s1():
    rnd = random.Random(11)
    cv = Cv(bg='#120e14')
    TW, TH, N = 10, 5, 6
    OX, OY = 65, 100
    WH, SHH = 50, 38

    def iso(i, j, z=0):
        return (OX + (i - j) * TW, OY + (i + j) * TH - z)

    T, L, R, B = iso(0, 0), iso(0, N), iso(N, 0), iso(N, N)
    # walls
    cv.poly([(T[0], T[1] - WH), (L[0], L[1] - WH), L, T], STONE_D)
    cv.poly([(T[0], T[1] - WH), (R[0], R[1] - WH), R, T], STONE)
    for k in range(6, WH, 6):
        cv.line(T[0], T[1] - WH + k, L[0], L[1] - WH + k, STONE_DD)
        cv.line(T[0], T[1] - WH + k, R[0], R[1] - WH + k, STONE_D)
    for k in range(0, 3):
        cv.line(T[0], T[1] - WH - k, L[0], L[1] - WH - k, STONE_L)
        cv.line(T[0], T[1] - WH - k, R[0], R[1] - WH - k, STONE_LL)
    cv.r(T[0], T[1] - WH - 2, 1, WH + 2, STONE_DD)
    # floor
    for i in range(N):
        for j in range(N):
            c = '#5d4c3f' if (i + j) % 2 == 0 else '#514236'
            cv.poly([iso(i, j), iso(i + 1, j), iso(i + 1, j + 1), iso(i, j + 1)], c)
    # floor edge thickness
    cv.poly([L, B, (B[0], B[1] + 4), (L[0], L[1] + 4)], '#2f261f')
    cv.poly([B, R, (R[0], R[1] + 4), (B[0], B[1] + 4)], '#3a2f27')
    # carpet
    cv.poly([iso(1.7, 1.7), iso(4.6, 1.7), iso(4.6, 4.6), iso(1.7, 4.6)], GOLD_D)
    cv.poly([iso(1.9, 1.9), iso(4.4, 1.9), iso(4.4, 4.4), iso(1.9, 4.4)], WINE)
    cv.poly([iso(2.5, 2.5), iso(3.8, 2.5), iso(3.8, 3.8), iso(2.5, 3.8)], '#8e3a3a')
    # doormat
    cv.poly([iso(5.0, 5.0), iso(5.9, 5.0), iso(5.9, 5.9), iso(5.0, 5.9)], '#3d4a5e')

    groups_l = [('모세오경', 0.8, 2.05, ['#7b2d2f', '#70492a', '#b07d2c']),
                ('역사서', 2.1, 3.35, ['#2e3f66', '#44506b', '#cbb689']),
                ('시가서', 3.4, 4.65, ['#2f5c48', '#3f6b3a', '#b07d2c']),
                ('선지서', 4.7, 5.95, ['#5b3861', '#8a3b55', '#7b2d2f'])]
    groups_r = [('복음서', 0.8, 2.45, ['#b07d2c', '#cbb689', '#a24a2a']),
                ('바울서신', 2.55, 4.2, ['#2d6770', '#2e3f66', '#a24a2a', '#cbb689']),
                ('일반서신', 4.3, 5.95, ['#70492a', '#5b3861', '#2f5c48'])]
    D = 0.7
    hl_edges = None

    def col_books(x, ytop, k, colors, seed, edge):
        for dy in range(SHH):
            row = dy // 9
            if dy == 0:
                c = WOOD_LL
            elif dy % 9 == 0 or dy >= SHH - 2:
                c = WOOD
            elif edge:
                c = WOOD_D
            else:
                hsh = (k // 2) * 7 + row * 13 + seed
                c = colors[hsh % len(colors)]
                if k % 2 == 1:
                    c = dark(c, 0.28)
                if dy % 9 == 1 and (hsh * 5) % 4 == 0:
                    c = '#20140e'
            cv.p(x, int(ytop) + dy, c)

    for gi, (name, j0, j1, cols) in enumerate(groups_l):
        A = iso(D, j0, SHH); Bp = iso(D, j1, SHH)
        cv.poly([iso(0, j0, SHH), A, Bp, iso(0, j1, SHH)], WOOD_L)
        xa, xb = int(A[0]), int(Bp[0])
        for x in range(xb, xa + 1):
            ytop = A[1] + (xa - x) * TH / TW
            col_books(x, ytop, xa - x, cols, gi * 31, x in (xa, xb))
        cv.poly([iso(0, j1, SHH), Bp, iso(D, j1, 0), iso(0, j1, 0)], WOOD_DD)
        ANCH.setdefault('s1', {})[name] = [(xa + xb) // 2, int((A[1] + Bp[1]) / 2) - 3]
    for gi, (name, i0, i1, cols) in enumerate(groups_r):
        A = iso(i0, D, SHH); Bp = iso(i1, D, SHH)
        cv.poly([iso(i0, 0, SHH), iso(i1, 0, SHH), Bp, A], WOOD_LL)
        xa, xb = int(A[0]), int(Bp[0])
        for x in range(xa, xb + 1):
            ytop = A[1] + (x - xa) * TH / TW
            col_books(x, ytop, x - xa, cols, 100 + gi * 17, x in (xa, xb))
        cv.poly([iso(i1, 0, SHH), Bp, iso(i1, D, 0), iso(i1, 0, 0)], WOOD_D)
        ANCH['s1'][name] = [(xa + xb) // 2, int((A[1] + Bp[1]) / 2) - 3]
        if name == '바울서신':
            hl_edges = (A, Bp)

    lights = []

    def stand(i, j, hgt=15):
        x, y = iso(i, j)
        x, y = int(x), int(y)
        cv.r(x - 2, y - 1, 5, 2, '#2a2420')
        cv.r(x, y - hgt, 1, hgt, '#3a332c')
        cv.r(x - 1, y - hgt, 3, 1, GOLD_D)
        f = candle(cv, x - 1, y - hgt, 3)
        lights.append((f[0], f[1], 46, 0.75))

    objs = []
    objs.append((0.45 + 0.45, lambda: stand(0.45, 0.45, 18)))

    def lectern():
        cv.poly([iso(2.75, 3.25, 9), iso(3.25, 3.25, 9), iso(3.25, 3.25, 0), iso(2.75, 3.25, 0)], WOOD_D)
        cv.poly([iso(3.25, 2.75, 9), iso(3.25, 3.25, 9), iso(3.25, 3.25, 0), iso(3.25, 2.75, 0)], WOOD)
        cv.poly([iso(2.6, 2.6, 10), iso(3.4, 2.6, 10), iso(3.4, 3.4, 10), iso(2.6, 3.4, 10)], WOOD_LL)
        cv.poly([iso(2.7, 2.7, 11), iso(3.3, 2.7, 11), iso(3.3, 3.3, 11), iso(2.7, 3.3, 11)], PARCH_L)
        a, b = iso(2.7, 2.7, 11), iso(3.3, 3.3, 11)
        cv.line(a[0], a[1], b[0], b[1], PARCH_DD)
        lights.append((OX, iso(3, 3, 12)[1], 30, 0.45))

    objs.append((6.0, lectern))

    def who(i, j, rows, pal, flip=False):
        x, y = iso(i, j)
        cv.dith(int(x) - 5, int(y) - 1, 10, 3, '#241a16', 8)
        cv.spr(int(x) - 6, int(y) - len(rows) + 1, rows, pal, flip)

    objs.append((2.3 + 3.6, lambda: who(2.3, 3.6, LIBRARIAN, LIB_PAL)))
    objs.append((3.4 + 1.55, lambda: who(3.4, 1.55, PLAYER_BACK, PLAYER_PAL)))
    objs.append((1.5 + 4.9, lambda: stand(1.5, 4.9)))
    objs.append((4.9 + 1.5 + 0.01, lambda: stand(4.9, 1.2)))
    for _, fn in sorted(objs, key=lambda o: o[0]):
        fn()
    light(cv, lights, ambient=0.40, y0=40, y1=175)
    # highlight the chosen shelf (drawn after light so it stays bright)
    A, Bp = hl_edges
    xa, xb = int(A[0]), int(Bp[0])
    for x in range(xa, xb + 1):
        yt = int(A[1] + (x - xa) * TH / TW)
        cv.p(x, yt - 1, GOLD_L)
        cv.p(x, yt + SHH, GOLD_L)
    cv.r(xa - 1, int(A[1]) - 1, 1, SHH + 2, GOLD_L)
    cv.r(xb + 1, int(Bp[1]) - 1, 1, SHH + 2, GOLD_L)
    cv.save(os.path.join(OUT, 'hall1.png'))


# ------------------------------------------------------------------ 2 층층 서고
FLOORS = [('모세오경', [50, 40, 27], [36, 34], ['#7b2d2f', '#70492a', '#b07d2c']),
          ('역사서', [24, 21, 4, 31, 24, 22], [25, 29, 36, 10, 13, 10], ['#2e3f66', '#44506b', '#cbb689']),
          ('시가서', [42, 150], [31, 12, 8], ['#2f5c48', '#3f6b3a', '#b07d2c']),
          ('선지서', [66, 52, 5, 48, 12], [14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4], ['#5b3861', '#8a3b55', '#7b2d2f']),
          ('복음서', [28, 16, 24, 21], [28], ['#b07d2c', '#cbb689', '#a24a2a']),
          ('바울서신', [16, 16, 13, 6, 6, 4, 4, 5, 3], [6, 4, 3, 1], ['#2d6770', '#2e3f66', '#a24a2a', '#cbb689']),
          ('일반서신', [13, 5, 5, 3], [5, 1, 1, 1, 22], ['#70492a', '#5b3861', '#2f5c48'])]


def bw(ch):
    return max(2, min(14, int(round(ch ** 0.55 * 1.35))))


def deco(cv, x, y, w, h, rnd):
    """Fill left-over shelf space: lying books, a jar, a scroll bundle."""
    if w < 8:
        return
    cx = x + 2
    if w >= 14:
        for k in range(rnd.choice([2, 3])):
            c = rnd.choice(BOOKC)
            cv.r(cx, y + h - 2 - k * 2, 9 - k, 2, c)
            cv.r(cx, y + h - 2 - k * 2, 9 - k, 1, lite(c, 0.25))
        cx += 12
    if x + w - cx >= 8:
        # scroll bundle
        for k in range(3):
            cv.r(cx + k * 2, y + h - 6, 2, 6, PARCH if k % 2 == 0 else PARCH_D)
            cv.p(cx + k * 2, y + h - 6, PARCH_L)
        cx += 9
    if x + w - cx >= 6:
        cv.r(cx + 1, y + h - 5, 3, 5, '#6a7b86')
        cv.r(cx + 1, y + h - 5, 3, 1, '#9db0bb')
        cv.r(cx + 2, y + h - 6, 1, 1, '#3a332c')


def s2():
    rnd = random.Random(22)
    cv = Cv(bg='#0f0c12')
    X0, X1 = 6, 124
    TOP, FH = 28, 30
    stone(cv, X0, 18, X1 - X0, 228, rnd)
    # roof truss
    cv.r(X0, 18, X1 - X0, 10, '#1b1519')
    cv.r(X0, 26, X1 - X0, 2, WOOD_DD)
    for x in (30, 65, 100):
        cv.r(x, 18, 2, 8, WOOD_DD)
        cv.line(x - 12, 26, x, 19, WOOD_DD)
        cv.line(x + 13, 26, x + 1, 19, WOOD_DD)
    lights = []
    sel = 5
    for f, (name, r1, r2, cols) in enumerate(FLOORS):
        y0 = TOP + (6 - f) * FH
        cv.dith(X0 + 2, y0, X1 - X0 - 4, 3, STONE_DD, 11)
        # hanging plaque
        ot = f < 4
        pc = '#55805f' if ot else '#9a4a50'
        cv.r(11, y0 + 1, 1, 6, '#8b8580'); cv.r(30, y0 + 1, 1, 6, '#8b8580')
        cv.r(8, y0 + 7, 26, 13, WOOD_DD)
        cv.r(9, y0 + 8, 24, 11, pc)
        cv.r(9, y0 + 8, 24, 1, lite(pc, 0.2))
        ANCH.setdefault('s2', {})[name] = [21, y0 + 13]
        # shelf
        sx, sw = 37, 62
        cv.r(sx - 1, y0 + 3, sw + 2, 23, WOOD_D)
        cv.r(sx - 1, y0 + 3, sw + 2, 1, WOOD_L)
        for ri, row in enumerate((r1, r2)):
            ry = y0 + 4 + ri * 11
            ws = [bw(c) for c in row]
            out = shelf_row(cv, sx, ry, sw, 10, rnd, cols, ws)
            used = sum(ws) + len(ws)
            deco(cv, sx + used, ry, sw - used, 10, rnd)
            cv.r(sx, ry + 10, sw, 1, WOOD_L)
        # floor planks with a ladder opening
        for (fx, fw) in ((X0, 97), (118, 6)):
            cv.r(fx, y0 + 26, fw, 4, WOOD)
            cv.r(fx, y0 + 26, fw, 1, WOOD_LL)
            cv.r(fx, y0 + 29, fw, 1, WOOD_DD)
        # lantern
        cv.r(101, y0 + 1, 1, 4, '#8b8580')
        cv.r(100, y0 + 5, 3, 5, '#2a2420')
        cv.r(101, y0 + 6, 1, 3, FL2)
        cv.p(101, y0 + 7, FL1)
        lights.append((101, y0 + 8, 70 if f == sel else 58, 0.95 if f == sel else 0.70))
        lights.append((40, y0 + 12, 46, 0.30))
        # arrow-slit window
        if f % 2 == 1:
            cv.r(120, y0 + 8, 2, 9, '#27365c')
            cv.r(120, y0 + 9, 1, 6, '#7f97c9')
    # base
    cv.r(X0, TOP + 7 * FH, X1 - X0, 8, STONE_DD)
    cv.r(X0, TOP + 7 * FH, X1 - X0, 1, STONE_L)
    # ladder
    for x in (105, 114):
        cv.r(x, TOP + 6, 1, 7 * FH - 6, WOOD_LL)
        cv.r(x + 1, TOP + 6, 1, 7 * FH - 6, WOOD_D)
    for y in range(TOP + 9, TOP + 7 * FH, 4):
        cv.r(106, y, 8, 1, WOOD_L)
    # pillars
    cv.r(X0, 18, 2, 228, STONE_LL); cv.r(X1 - 2, 18, 2, 228, STONE_DD)
    # player on the ladder at the chosen floor
    ys = TOP + (6 - sel) * FH
    cv.spr(104, ys + 9, PLAYER_BACK, PLAYER_PAL)
    light(cv, lights, ambient=0.36, y0=16, y1=248)
    cv.box(X0 + 1, ys - 1, X1 - X0 - 2, FH + 1, GOLD_L)
    ANCH['s2']['sel_y'] = ys
    cv.save(os.path.join(OUT, 'hall2.png'))


# ------------------------------------------------------------------ 3 양피지 평면도
def s3():
    rnd = random.Random(33)
    cv = Cv(bg='#1c130e')
    parchment(cv, 3, 15, 124, 265, rnd)
    ink = '#3b2a1e'

    def wh(x0, x1, y):
        cv.r(x0, y, x1 - x0 + 1, 2, ink)

    def wv(x, y0, y1):
        cv.r(x, y0, 2, y1 - y0 + 1, ink)

    # banner
    cv.r(28, 22, 74, 12, PARCH_L); cv.box(28, 22, 74, 12, ink)
    cv.poly([(28, 24), (21, 24), (24, 29), (21, 35), (28, 35)], PARCH_D); cv.line(28, 24, 21, 24, ink); cv.line(21, 24, 24, 29, ink); cv.line(24, 29, 21, 35, ink); cv.line(21, 35, 28, 35, ink)
    cv.poly([(101, 24), (108, 24), (105, 29), (108, 35), (101, 35)], PARCH_D); cv.line(101, 24, 108, 24, ink); cv.line(108, 24, 105, 29, ink); cv.line(105, 29, 108, 35, ink); cv.line(108, 35, 101, 35, ink)

    Y0, Y1 = 50, 208
    lrooms = [('모세오경', 5, '#c79a4a'), ('역사서', 12, '#b9805c'), ('시가서', 5, '#8fa878'), ('선지서', 17, '#b78a96')]
    rrooms = [('복음서', 5, '#d3a548'), ('바울서신', 13, '#7f9bb5'), ('일반서신', 9, '#a493bb')]
    lx0, lx1, hx0, hx1, rx1 = 9, 54, 54, 75, 120
    # washes + rooms
    lh = (Y1 - Y0) / 4
    rh = (Y1 - Y0) / 3
    cv.dith(hx0 + 2, Y0 + 2, hx1 - hx0 - 2, Y1 - Y0 - 2, PARCH_L, 6)
    rects = {}
    for k, (name, n, col) in enumerate(lrooms):
        ya, yb = int(Y0 + k * lh), int(Y0 + (k + 1) * lh)
        cv.dith(lx0 + 2, ya + 2, lx1 - lx0 - 2, yb - ya - 2, col, 6)
        rects[name] = (lx0, ya, lx1, yb, n)
    for k, (name, n, col) in enumerate(rrooms):
        ya, yb = int(Y0 + k * rh), int(Y0 + (k + 1) * rh)
        cv.dith(hx1 + 2, ya + 2, rx1 - hx1 - 2, yb - ya - 2, col, 6)
        rects[name] = (hx1, ya, rx1, yb, n)
    # walls
    wh(lx0, rx1 + 1, Y0); wh(lx0, hx0, Y1); wh(hx1, rx1 + 1, Y1)
    wv(lx0, Y0, Y1); wv(rx1, Y0, Y1); wv(hx0, Y0, Y1); wv(hx1, Y0, Y1)
    for k in range(1, 4):
        wh(lx0, hx0, int(Y0 + k * lh))
    for k in range(1, 3):
        wh(hx1, rx1, int(Y0 + k * rh))
    # entrance + steps
    wh(hx0, 59, Y1); wh(70, hx1, Y1)
    for k in range(3):
        cv.r(59 - k, Y1 + 3 + k * 2, 12 + k * 2, 1, ink)
    # apse
    for a in range(0, 181, 4):
        x = 65 + math.cos(math.radians(a)) * 11
        y = Y0 - math.sin(math.radians(a)) * 9
        cv.r(int(round(x)), int(round(y)), 2, 2, ink)
    cv.r(hx0 + 2, Y0, hx1 - hx0 - 2, 2, PARCH)
    cv.dith(hx0 + 3, Y0 - 7, 17, 9, PARCH_L, 6)
    # doors
    for name, (xa, ya, xb, yb, n) in rects.items():
        cy = (ya + yb) // 2
        dx = hx0 if xa == lx0 else hx1
        cv.r(dx, cy - 3, 2, 7, PARCH)
        cv.p(dx, cy - 4, ink); cv.p(dx + 1, cy - 4, ink); cv.p(dx, cy + 4, ink); cv.p(dx + 1, cy + 4, ink)
        # book glyphs: one per book in the group
        gc = ['#7b2d2f', '#2e3f66', '#2f5c48', '#70492a']
        per = 12
        for b in range(n):
            bx = xa + 5 + (b % per) * 3
            by = ya + 5 + (b // per) * 6
            c = gc[b % 4]
            if name == '복음서' and b == 4:
                c = '#a24a2a'
            if name == '일반서신' and b in (0, 8):
                c = '#a24a2a'
            cv.r(bx, by, 2, 4, c)
        ANCH.setdefault('s3', {})[name] = [(xa + xb) // 2 + 1, (ya + yb) // 2 + 4]
    # hall: runner + lectern
    cv.dith(62, Y0 + 14, 7, Y1 - Y0 - 16, WINE, 5)
    cv.r(61, Y0 - 3, 9, 6, ink); cv.r(62, Y0 - 2, 3, 4, PARCH_L); cv.r(66, Y0 - 2, 3, 4, PARCH_L)
    ANCH['s3']['성경 전체'] = [65, Y0 + 10]
    # route to 바울서신
    xa, ya, xb, yb, n = rects['바울서신']
    cy = (ya + yb) // 2
    for y in range(Y1 + 8, cy, -3):
        cv.r(65, y, 1, 2, RED)
    for x in range(66, xa + 12, 3):
        cv.r(x, cy, 2, 1, RED)
    # pawn marker
    mx, my = xa + 14, cy
    cv.r(mx - 1, my - 6, 3, 3, FL4); cv.r(mx - 2, my - 3, 5, 4, FL4); cv.r(mx - 3, my + 1, 7, 1, ink)
    cv.p(mx - 1, my - 6, FL3)
    # chosen room outline
    cv.box(xa + 3, ya + 3, xb - xa - 4, yb - ya - 4, RED)
    # compass rose
    cx, cy2 = 22, 232
    for k in range(-9, 10):
        cv.p(cx, cy2 + k, ink); cv.p(cx + k, cy2, ink)
    for k in range(-5, 6):
        cv.p(cx + k, cy2 + k, PARCH_B); cv.p(cx + k, cy2 - k, PARCH_B)
    cv.poly([(cx, cy2 - 9), (cx - 2, cy2), (cx + 2, cy2)], RED)
    cv.poly([(cx, cy2 + 9), (cx - 2, cy2), (cx + 2, cy2)], ink)
    cv.r(cx - 1, cy2 - 1, 3, 3, GOLD)
    # scale bar
    cv.r(84, 236, 34, 1, ink)
    for x in (84, 95, 106, 117):
        cv.r(x, 233, 1, 4, ink)
    cv.r(84, 234, 11, 2, ink); cv.r(106, 234, 11, 2, ink)
    cv.save(os.path.join(OUT, 'hall3.png'))


# ------------------------------------------------------------------ 4 서가와 사서
def big_spine(cv, x, y, w, h, col):
    cv.r(x, y, w, h, col)
    cv.r(x, y, 1, h, lite(col, 0.25))
    if w >= 4:
        cv.r(x + 1, y, 1, h, lite(col, 0.10))
    cv.r(x + w - 1, y, 1, h, dark(col, 0.4))
    cv.r(x, y, w, 1, lite(col, 0.35))
    for yy in (3, 5, h - 6, h - 4):
        cv.r(x, y + yy, w, 1, GOLD_D)
        cv.p(x, y + yy, GOLD)
    if w >= 6:
        m = x + w // 2
        cv.p(m, y + h - 11, GOLD); cv.r(m - 1, y + h - 10, 3, 1, GOLD); cv.p(m, y + h - 9, GOLD)


def s4():
    rnd = random.Random(44)
    cv = Cv(bg='#15101a')
    stone(cv, 0, 15, 130, 167, rnd)
    # alcove
    cv.r(8, 30, 114, 146, STONE_DD)
    for k, (dx, dy) in enumerate([(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]):
        cv.p(8 + dx, 30 + dy, STONE); cv.p(121 - dx, 30 + dy, STONE)
    cv.r(8, 29, 114, 1, STONE_LL)
    # shelf frame
    cv.r(12, 38, 106, 130, WOOD_D)
    cv.r(12, 38, 106, 2, WOOD_L); cv.r(12, 38, 2, 130, WOOD); cv.r(116, 38, 2, 130, WOOD_DD)
    cv.r(14, 40, 102, 58, '#1d130d'); cv.r(14, 102, 102, 54, '#1d130d')
    for by in (98, 156):
        cv.r(14, by, 102, 4, WOOD); cv.r(14, by, 102, 1, WOOD_LL); cv.r(14, by + 3, 102, 1, WOOD_DD)
    cv.r(12, 160, 106, 8, WOOD); cv.r(12, 160, 106, 1, WOOD_L)
    row1 = [('롬', 15, '#7b2d2f'), ('고전', 15, '#2e3f66'), ('고후', 12, '#44506b'), ('갈', 8, '#a24a2a'),
            ('엡', 8, '#2f5c48'), ('빌', 7, '#b07d2c'), ('골', 7, '#2d6770'), ('살전', 7, '#5b3861'), ('살후', 6, '#8a3b55')]
    row2 = [('딤전', 8, '#70492a'), ('딤후', 7, '#3f6b3a'), ('딛', 6, '#44506b'), ('몬', 6, '#7b2d2f')]
    hts = [46, 44, 45, 44, 42, 45, 43, 44, 41]
    x = 17
    sel = None
    A = ANCH.setdefault('s4', {})
    for k, (nm, w, col) in enumerate(row1):
        h = hts[k]
        y = 98 - h
        if nm == '갈':
            y -= 6
            sel = (x, y, w, h)
        big_spine(cv, x, y, w, h, col)
        A[nm] = [x, y, w, h]
        x += w + 1
    x = 17
    for k, (nm, w, col) in enumerate(row2):
        h = [44, 42, 45, 41][k]
        big_spine(cv, x, 156 - h, w, h, col)
        A[nm] = [x, 156 - h, w, h]
        x += w + 1
    # lower shelf props
    for k, c in enumerate(['#2e3f66', '#b07d2c', '#5b3861']):
        cv.r(54 + k, 150 - k * 6, 26 - k * 2, 6, c)
        cv.r(54 + k, 150 - k * 6, 26 - k * 2, 1, lite(c, 0.3))
        cv.r(54 + k, 152 - k * 6, 3, 2, PARCH_D)
    # hourglass
    cv.r(86, 139, 7, 1, WOOD_LL); cv.r(86, 155, 7, 1, WOOD_LL)
    cv.r(87, 140, 5, 15, '#9db0bb'); cv.r(88, 141, 3, 5, PARCH); cv.r(89, 146, 1, 3, '#d6bf8a'); cv.r(88, 150, 3, 5, '#d6bf8a')
    cv.p(87, 147, '#1d130d'); cv.p(91, 147, '#1d130d'); cv.p(87, 148, '#1d130d'); cv.p(91, 148, '#1d130d')
    f = candle(cv, 99, 155, 8)
    # inkwell + quill
    cv.r(106, 151, 5, 5, '#1a1a22'); cv.r(106, 151, 5, 1, '#55556a')
    cv.line(108, 151, 113, 136, PARCH_L); cv.line(109, 151, 114, 137, PARCH_D)
    light(cv, [(f[0], f[1], 60, 0.7), (66, 62, 34, 0.55), (65, 20, 70, 0.35)], ambient=0.42, y0=15, y1=182)
    sx, sy, sw, sh = sel
    cv.box(sx - 1, sy - 1, sw + 2, sh + 2, GOLD_L)
    cv.r(sx, sy + sh + 1, sw, 5, '#0f0a07')
    # counter
    planks(cv, 0, 176, 130, 8, rnd)
    cv.r(0, 176, 130, 1, WOOD_LL)
    cv.r(0, 184, 130, 98, '#15101a')
    cv.save(os.path.join(OUT, 'hall4.png'))


# ------------------------------------------------------------------ 5 서고 통로
def s5():
    cv = Cv(bg='#0d0a10')
    VX, VY = 65, 112
    FL, FR, FT, FB = 51, 79, 92, 136
    kb, kt = 24 / 14, 20 / 14

    def hsh(a, b, c=0):
        return (a * 73856093 ^ b * 19349663 ^ c * 83492791) & 0xffff

    # ceiling
    for y in range(0, FT):
        z = 1.0 / (VY - y)
        f = 0.30 + 0.70 * ((VY - y) / 112.0)
        beam = ((z * 112) % 1.0) < 0.30
        for x in range(0, W):
            wx = (x - VX) * z
            if abs(wx) > 0.72:
                continue
            c = WOOD_D if beam else ('#2a2530' if int(wx * 5 + 50) % 2 == 0 else '#25212b')
            cv.p(x, y, dark(c, 1 - f))
    # floor
    for y in range(FB, H):
        z = 1.0 / (y - VY)
        f = 0.35 + 0.65 * min(1.0, (y - VY) / 150.0)
        for x in range(0, W):
            wx = (x - VX) * z
            if abs(wx) > 0.60:
                continue
            par = (int(wx * 6 + 60) + int(z * 204)) % 2
            c = '#5e535c' if par == 0 else '#4a414a'
            if abs(wx) < 0.25:
                c = WINE if ((z * 204) % 1.0) > 0.12 else '#8e3a3a'
                if abs(wx) > 0.20:
                    c = GOLD_D
            cv.p(x, y, dark(c, 1 - f))

    # walls
    def wall(side):
        for xx in range(0, FL):
            x = xx if side == 0 else W - 1 - xx
            u = 65.0 / (65 - xx)
            yt = VY - (65 - xx) * kt
            yb = VY + (65 - xx) * kb
            hgt = yb - yt
            f = 1.0 / (u ** 0.75)
            pillar = (u % 1.0) < 0.07
            book = int(u * 10)
            colw = 1.0 / (10 * (u * u) / 65.0)  # px per book
            nxt = int((65.0 / (65 - xx - 1)) * 10) if xx + 1 < 65 else book
            for y in range(max(0, int(yt)), min(H, int(yb) + 1)):
                t = (y - yt) / hgt
                rowf = (t - 0.06) / 0.88 * 6
                if t < 0.06:
                    c = WOOD_L
                elif t > 0.94:
                    c = WOOD_D
                elif pillar:
                    c = WOOD_DD
                else:
                    row = int(rowf)
                    fr = rowf - row
                    if fr > 0.90:
                        c = WOOD
                    else:
                        hv = hsh(book, row, side)
                        c = BOOKC[hv % len(BOOKC)]
                        if fr < 0.05 + (hv % 5) * 0.03:
                            c = '#20140e'
                        elif colw >= 2.5 and nxt != book:
                            c = dark(c, 0.35)
                cv.p(x, y, dark(c, 1 - f))

    wall(0); wall(1)
    # end wall
    cv.r(FL, FT, FR - FL, FB - FT, '#35303b')
    for y in range(FT, FB, 5):
        cv.r(FL, y, FR - FL, 1, '#2a2630')
    lights = [(65, 112, 80, 0.55)]
    for u, rad, it in ((1.45, 34, 0.70), (2.5, 22, 0.55), (3.5, 14, 0.45)):
        xx = 65 - 65 / u
        yt = VY - (65 - xx) * kt
        yb = VY + (65 - xx) * kb
        sy = int(yt + (yb - yt) * 0.30)
        for x in (int(xx), W - 1 - int(xx)):
            cv.r(x - 1, sy + 2, 3, 1, '#2a2420')
            cv.r(x, sy - 1, 1, 3, FL3); cv.p(x, sy, FL1)
            lights.append((x, sy, rad, it))
    # player, seen from behind
    cv.dith(52, 226, 26, 4, '#1a1216', 8)
    cv.spr(53, 196, PLAYER_BACK, PLAYER_PAL, k=2)
    light(cv, lights, ambient=0.50, steps=7)
    # glowing window + lectern (after light)
    cv.r(58, 96, 14, 30, '#1a1418')
    for k, c in enumerate(['#fff1b8', '#ffe59a', '#ffd67a', '#ffc65c', '#f9ae4a', '#f39a3c']):
        cv.r(59, 98 + k * 4, 12, 4, c)
    cv.p(59, 98, '#1a1418'); cv.p(70, 98, '#1a1418'); cv.p(59, 99, '#1a1418'); cv.p(70, 99, '#1a1418'); cv.r(59, 97, 3, 1, '#1a1418'); cv.r(68, 97, 3, 1, '#1a1418')
    cv.r(65, 97, 1, 25, '#1a1418'); cv.r(59, 108, 12, 1, '#1a1418')
    cv.r(63, 126, 5, 10, '#120d10'); cv.r(59, 123, 13, 3, PARCH_L); cv.r(65, 123, 1, 3, PARCH_DD)
    # hanging sign
    cv.r(40, 20, 1, 12, '#8b8580'); cv.r(89, 20, 1, 12, '#8b8580')
    cv.r(33, 32, 64, 17, WOOD_DD); cv.r(34, 33, 62, 15, WOOD); cv.r(34, 33, 62, 1, WOOD_LL); cv.r(34, 47, 62, 1, WOOD_D)
    for (nx, ny) in ((36, 35), (93, 35), (36, 45), (93, 45)):
        cv.p(nx, ny, GOLD)
    cv.save(os.path.join(OUT, 'hall5.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fn in (s1, s2, s3, s4, s5):
        fn()
    json.dump(ANCH, open(os.path.join(OUT, 'anchors_hall.json'), 'w'), ensure_ascii=False, indent=0)
    sheet = Image.new('RGB', (W * 5 * 3 + 6 * 8, H * 3 + 16), (60, 60, 60))
    for k in range(5):
        im = Image.open(os.path.join(OUT, 'hall%d.png' % (k + 1))).resize((W * 3, H * 3), Image.NEAREST)
        sheet.paste(im, (8 + k * (W * 3 + 8), 8))
    sheet.save(os.path.join(OUT, '_sheet_hall.png'))
    print(json.dumps(ANCH, ensure_ascii=False))
