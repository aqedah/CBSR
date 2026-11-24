"""Art for the merged direction: tower hall, front shelf, clean reading page, ambient pieces."""
from px import *
from halls import FLOORS, bw, deco, big_spine
import random, math, os, json

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
A = {}


def tower2():
    rnd = random.Random(22)
    cv = Cv(bg='#0f0c12')
    X0, X1 = 6, 124
    TOP, FH = 28, 30
    stone(cv, X0, 18, X1 - X0, 228, rnd)
    cv.r(X0, 18, X1 - X0, 10, '#1b1519')
    cv.r(X0, 26, X1 - X0, 2, WOOD_DD)
    for x in (30, 65, 100):
        cv.r(x, 18, 2, 8, WOOD_DD)
        cv.line(x - 12, 26, x, 19, WOOD_DD)
        cv.line(x + 13, 26, x + 1, 19, WOOD_DD)
    lights = []
    ys = []
    for f, (name, r1, r2, cols) in enumerate(FLOORS):
        y0 = TOP + (6 - f) * FH
        ys.append((name, y0))
        cv.dith(X0 + 2, y0, X1 - X0 - 4, 3, STONE_DD, 11)
        ot = f < 4
        pc = '#55805f' if ot else '#9a4a50'
        cv.r(12, y0 + 1, 1, 5, '#8b8580'); cv.r(35, y0 + 1, 1, 5, '#8b8580')
        cv.r(8, y0 + 6, 32, 15, WOOD_DD)
        cv.r(9, y0 + 7, 30, 13, pc)
        cv.r(9, y0 + 7, 30, 1, lite(pc, 0.2))
        cv.r(9, y0 + 19, 30, 1, dark(pc, 0.25))
        sx, sw = 44, 54
        cv.r(sx - 1, y0 + 3, sw + 2, 23, WOOD_D)
        cv.r(sx - 1, y0 + 3, sw + 2, 1, WOOD_L)
        for ri, row in enumerate((r1, r2)):
            ry = y0 + 4 + ri * 11
            ws = [bw(c) for c in row]
            shelf_row(cv, sx, ry, sw, 10, rnd, cols, ws)
            used = sum(ws) + len(ws)
            deco(cv, sx + used, ry, sw - used, 10, rnd)
            cv.r(sx, ry + 10, sw, 1, WOOD_L)
        for (fx, fw) in ((X0, 97), (118, 6)):
            cv.r(fx, y0 + 26, fw, 4, WOOD)
            cv.r(fx, y0 + 26, fw, 1, WOOD_LL)
            cv.r(fx, y0 + 29, fw, 1, WOOD_DD)
        # lantern body (flame is animated on top)
        cv.r(101, y0 + 1, 1, 3, '#8b8580')
        cv.r(99, y0 + 4, 5, 8, '#2a2420')
        cv.r(100, y0 + 5, 3, 6, '#5a3a1c')
        lights.append((101, y0 + 8, 58, 0.72))
        lights.append((40, y0 + 12, 46, 0.30))
        if f % 2 == 1:
            cv.r(120, y0 + 8, 2, 9, '#27365c')
            cv.r(120, y0 + 9, 1, 6, '#7f97c9')
    cv.r(X0, TOP + 7 * FH, X1 - X0, 8, STONE_DD)
    cv.r(X0, TOP + 7 * FH, X1 - X0, 1, STONE_L)
    for x in (106, 115):
        cv.r(x, TOP + 6, 1, 7 * FH - 6, WOOD_LL)
        cv.r(x + 1, TOP + 6, 1, 7 * FH - 6, WOOD_D)
    for y in range(TOP + 9, TOP + 7 * FH, 4):
        cv.r(107, y, 8, 1, WOOD_L)
    cv.r(X0, 18, 2, 228, STONE_LL); cv.r(X1 - 2, 18, 2, 228, STONE_DD)
    light(cv, lights, ambient=0.38, y0=16, y1=248)
    for name, y0 in ys:
        cv.r(100, y0 + 5, 3, 6, '#8a4f1c')
        cv.r(99, y0 + 4, 5, 1, '#3a332c'); cv.r(99, y0 + 11, 5, 1, '#3a332c')
    A['tower'] = {n: y for n, y in ys}
    cv.save(os.path.join(OUT, 'tower2.png'))


def shelf3():
    rnd = random.Random(47)
    cv = Cv(bg='#15101a')
    stone(cv, 0, 15, 130, 201, rnd)
    cv.r(6, 30, 118, 180, STONE_DD)
    cv.r(6, 29, 118, 1, STONE_LL)
    cv.r(10, 36, 110, 172, WOOD_D)
    cv.r(10, 36, 110, 2, WOOD_L); cv.r(10, 36, 2, 172, WOOD); cv.r(118, 36, 2, 172, WOOD_DD)
    rows_y = [40, 94, 148]
    for ry in rows_y:
        cv.r(13, ry, 104, 48, '#1d130d')
        cv.r(13, ry + 48, 104, 4, WOOD); cv.r(13, ry + 48, 104, 1, WOOD_LL); cv.r(13, ry + 51, 104, 1, WOOD_DD)
    cv.r(10, 202, 110, 6, WOOD); cv.r(10, 202, 110, 1, WOOD_L)
    rows = [[('롬', 16, '#7b2d2f'), ('고전', 16, '#2e3f66'), ('고후', 13, '#44506b'), ('갈', 6, '#a24a2a'),
             ('엡', 6, '#2f5c48'), ('빌', 4, '#70492a')],
            [('골', 4, '#2d6770'), ('살전', 5, '#5b3861'), ('살후', 3, '#8a3b55')],
            [('딤전', 6, '#70492a'), ('딤후', 4, '#3f6b3a'), ('딛', 3, '#44506b'), ('몬', 1, '#7b2d2f')]]
    sp = {}
    for ri, row in enumerate(rows):
        x = 14
        for nm, ch, col in row:
            h = min(44, 28 + ch)
            y = rows_y[ri] + 48 - h
            big_spine(cv, x, y, 16, h, col)
            sp[nm] = [x, y, 16, h]
            x += 17
    A['shelf'] = sp
    # row 2 props: lying books, hourglass, candle (flame animated on top)
    ry = rows_y[1] + 48
    for k, c in enumerate(['#2e3f66', '#b07d2c', '#5b3861']):
        cv.r(68 + k, ry - 6 - k * 6, 24 - k * 2, 6, c)
        cv.r(68 + k, ry - 6 - k * 6, 24 - k * 2, 1, lite(c, 0.3))
        cv.r(68 + k, ry - 4 - k * 6, 3, 2, PARCH_D)
    cv.r(96, ry - 17, 7, 1, WOOD_LL); cv.r(96, ry - 1, 7, 1, WOOD_LL)
    cv.r(97, ry - 16, 5, 15, '#9db0bb'); cv.r(98, ry - 15, 3, 5, PARCH); cv.r(99, ry - 10, 1, 3, '#d6bf8a'); cv.r(98, ry - 6, 3, 5, '#d6bf8a')
    cv.r(107, ry - 1, 5, 1, GOLD_D); cv.r(108, ry - 10, 3, 9, '#efe3c4'); cv.r(110, ry - 10, 1, 9, '#cdbf9c')
    A['candle'] = [108, ry - 15]
    # row 3 props: scrolls, inkwell and quill
    ry3 = rows_y[2] + 48
    for k in range(4):
        cv.r(86 + k * 3, ry3 - 12, 3, 12, PARCH if k % 2 == 0 else PARCH_D)
        cv.r(86 + k * 3, ry3 - 12, 3, 1, PARCH_L)
        cv.p(87 + k * 3, ry3 - 12, PARCH_DD)
    cv.r(104, ry3 - 6, 6, 6, '#1a1a22'); cv.r(104, ry3 - 6, 6, 1, '#55556a')
    cv.line(107, ry3 - 6, 113, ry3 - 22, PARCH_L); cv.line(108, ry3 - 6, 114, ry3 - 21, PARCH_D)
    light(cv, [(109, ry - 13, 78, 0.85), (40, 60, 60, 0.30), (65, 24, 80, 0.30)], ambient=0.46, y0=15, y1=217)
    cv.r(108, ry - 10, 3, 9, '#f3e9cf'); cv.r(110, ry - 10, 1, 9, '#d9cba6')
    planks(cv, 0, 210, 130, 7, rnd)
    cv.r(0, 210, 130, 1, WOOD_LL)
    cv.r(0, 217, 130, 65, '#15101a')
    cv.save(os.path.join(OUT, 'shelf3.png'))


def readface():
    rnd = random.Random(61)
    cv = Cv(bg='#17110d')
    x, y, w, h = 3, 15, 124, 247
    base = C('#F3E6C4'); d1 = C('#E6D1A1'); d2 = C('#D4B981'); burn = C('#9c7b47')
    cv.r(x, y, w, h, base)
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            dd = min(xx - x, x + w - 1 - xx, yy - y, y + h - 1 - yy)
            if dd < 8:
                t = rnd.random()
                if t < 0.16 - dd * 0.015:
                    cv.p(xx, yy, d1)
                thr = [15, 10, 6, 3, 1][dd] if dd < 5 else 0
                if BAYER[yy % 4][xx % 4] < thr:
                    cv.p(xx, yy, d2 if dd > 0 else burn)
    cv.box(x + 5, y + 5, w - 10, h - 10, '#b3915a')
    cv.box(x + 7, y + 7, w - 14, h - 14, '#dcc592')
    for (cx, cy) in ((x + 4, y + 4), (x + w - 9, y + 4), (x + 4, y + h - 9), (x + w - 9, y + h - 9)):
        cv.r(cx, cy, 5, 5, RED); cv.box(cx, cy, 5, 5, '#6b4d17'); cv.p(cx + 2, cy + 2, GOLD_L)
    cv.save(os.path.join(OUT, 'read.png'))


def small():
    g = Cv(40, 40, alpha=True)
    for yy in range(40):
        for xx in range(40):
            d = math.hypot(xx - 19.5, yy - 19.5)
            L = max(0.0, 1 - d / 20.0) ** 1.3
            if BAYER[yy % 4][xx % 4] < int(L * 17):
                g.p(xx, yy, '#ffd15a')
    g.save(os.path.join(OUT, 'glow.png'))
    fa = ["." + "2" + ".", "212", "212", "323", "333", "343"]
    fb = ["...", ".2.", "212", "323", "333", "343"]
    pal = {'1': FL1, '2': FL2, '3': FL3, '4': FL4}
    for nm, rows in (('flame_a.png', fa), ('flame_b.png', fb)):
        c = Cv(3, 6, alpha=True)
        c.spr(0, 0, rows, pal)
        c.save(os.path.join(OUT, nm))
    p = Cv(12, 16, alpha=True)
    p.spr(0, 0, PLAYER_BACK, PLAYER_PAL)
    p.save(os.path.join(OUT, 'player_back.png'))


if __name__ == '__main__':
    for fn in (tower2, shelf3, readface, small):
        fn()
    json.dump(A, open(os.path.join(OUT, 'anchors_merged.json'), 'w'), ensure_ascii=False)
    print(json.dumps(A, ensure_ascii=False))
    sheet = Image.new('RGB', (W * 3 * 3 + 4 * 8, H * 3 + 16), (60, 60, 60))
    for k, nm in enumerate(('tower2.png', 'shelf3.png', 'read.png')):
        im = Image.open(os.path.join(OUT, nm)).resize((W * 3, H * 3), Image.NEAREST)
        sheet.paste(im, (8 + k * (W * 3 + 8), 8))
    x = 8
    for nm, sc in (('glow.png', 3), ('flame_a.png', 12), ('flame_b.png', 12), ('player_back.png', 6)):
        im = Image.open(os.path.join(OUT, nm)).convert('RGBA')
        im = im.resize((im.width * sc // SCALE, im.height * sc // SCALE), Image.NEAREST)
        sheet.paste(im, (x, 8), im)
        x += im.width + 8
    sheet.resize((sheet.width * 2 // 3, sheet.height * 2 // 3), Image.LANCZOS).save(os.path.join(OUT, '_sheet_merged.png'))
