"""Five opened-book scenes and the small shared pieces."""
from px import *
import random, math, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
INKB = '#3b2a1e'


def frame(cv, x, y, w, h):
    cv.box(x, y, w, h, INKB)
    cv.box(x + 1, y + 1, w - 2, h - 2, GOLD_D)


# ------------------------------------------------------------------ 1 넘기는 책
def b1():
    rnd = random.Random(101)
    cv = Cv(bg='#120e0c')
    planks(cv, 0, 15, 130, 267, rnd, base='#3a2416', d='#2a190e', l='#4a2f1c', ph=9)
    light(cv, [(65, 110, 170, 0.75)], ambient=0.22, y0=15)
    cv.r(3, 19, 124, 234, '#3c1f1a'); cv.r(3, 19, 124, 1, '#5e332b'); cv.r(3, 252, 124, 1, '#241210')
    parchment(cv, 6, 22, 116, 225, rnd, torn=False, burn=3)
    for k, c in enumerate([PARCH_D, PARCH_DD, PARCH_D]):
        cv.r(122 + k, 23 + k, 1, 225, c)
        cv.r(7 + k, 247 + k, 116, 1, c)
    for k, thr in enumerate([12, 8, 5, 2]):
        cv.dith(6 + k, 22, 1, 225, PARCH_DD, thr)
    # ribbon bookmark
    cv.r(98, 17, 4, 22, RED); cv.r(98, 17, 1, 22, lite(RED, 0.2)); cv.p(99, 38, PARCH); cv.p(100, 38, PARCH)
    # dog-ear
    cv.poly([(121, 237), (112, 246), (121, 246)], PARCH_DD)
    cv.line(121, 237, 112, 246, PARCH_B)
    frame(cv, 13, 29, 100, 52)
    # ribbon tabs under the book
    tabs = ['#70492a', '#a24a2a', '#2f5c48', '#2e3f66', '#5b3861', '#2d6770', '#b07d2c']
    for k, c in enumerate(tabs):
        x = 6 + k * 17
        on = (k == 1)
        y0 = 250 if not on else 248
        hh = 17 if not on else 21
        cc = c if on else dark(c, 0.25)
        cv.r(x, y0, 16, hh, cc)
        cv.r(x, y0, 1, hh, lite(cc, 0.2)); cv.r(x + 15, y0, 1, hh, dark(cc, 0.3))
        cv.poly([(x + 4, y0 + hh), (x + 8, y0 + hh - 4), (x + 12, y0 + hh)], '#120e0c')
        if on:
            cv.r(x, y0, 16, 1, GOLD_L)
    cv.save(os.path.join(OUT, 'book1.png'))


# ------------------------------------------------------------------ 2 두루마리
def b2():
    rnd = random.Random(102)
    cv = Cv(bg='#0f0c12')
    stone(cv, 0, 15, 130, 267, rnd, base='#3a3640', d='#2b2831', l='#46414d')
    light(cv, [(65, 70, 150, 0.6)], ambient=0.24, y0=15)
    parchment(cv, 12, 26, 106, 228, rnd, torn=False, burn=3)
    for k, thr in enumerate([13, 10, 6, 3]):
        cv.dith(12, 27 + k * 2, 106, 2, PARCH_DD, thr)
        cv.dith(12, 250 - k * 2, 106, 2, PARCH_DD, thr)

    def roller(y, thick):
        cv.r(7, y, 116, thick, WOOD); cv.r(7, y, 116, 1, WOOD_LL); cv.r(7, y + 1, 116, 1, WOOD_L)
        cv.r(7, y + thick - 2, 116, 2, WOOD_DD)
        for x in (2, 123):
            cv.r(x, y - 1, 5, thick + 2, GOLD_D); cv.r(x, y - 1, 5, 1, GOLD_L); cv.r(x, y + thick, 5, 1, '#6b4d17')
            cv.r(x + 1, y + 1, 1, thick - 2, GOLD_L)

    roller(20, 7)
    cv.r(10, 252, 110, 10, PARCH_D); cv.r(10, 252, 110, 1, PARCH_L); cv.r(10, 256, 110, 1, PARCH_DD)
    cv.r(10, 260, 110, 2, PARCH_B)
    for x in (2, 123):
        cv.r(x, 253, 5, 8, GOLD_D); cv.r(x, 253, 5, 1, GOLD_L); cv.r(x + 1, 255, 1, 4, GOLD_L)
    cv.r(7, 255, 3, 4, WOOD); cv.r(120, 255, 3, 4, WOOD)
    frame(cv, 15, 35, 100, 52)
    cv.save(os.path.join(OUT, 'book2.png'))


# ------------------------------------------------------------------ 3 채식 사본
def b3():
    rnd = random.Random(103)
    cv = Cv(bg='#1c130e')
    parchment(cv, 3, 15, 124, 265, rnd)
    # illuminated initial
    x, y = 10, 24
    cv.r(x, y, 30, 30, INKB); cv.r(x + 1, y + 1, 28, 28, GOLD); cv.r(x + 3, y + 3, 24, 24, BLUE)
    for (cx, cy) in ((x + 3, y + 3), (x + 23, y + 3), (x + 3, y + 23), (x + 23, y + 23)):
        cv.r(cx, cy, 4, 4, RED); cv.p(cx + 1, cy + 1, GOLD_L)
    for k in range(9, 22, 3):
        cv.p(x + k, y + 4, GOLD_L); cv.p(x + k, y + 25, GOLD_L); cv.p(x + 4, y + k, GOLD_L); cv.p(x + 25, y + k, GOLD_L)
    cv.box(x + 1, y + 1, 28, 28, GOLD_L)
    # vine border
    vx = 9
    for yy in range(60, 238):
        cv.p(vx + (1 if (yy // 6) % 2 == 0 else 0), yy, GREEN)
    for k, yy in enumerate(range(62, 236, 12)):
        side = 1 if k % 2 == 0 else -1
        cv.r(vx + (2 if side > 0 else -2), yy, 2, 2, GREEN); cv.p(vx + (3 if side > 0 else -2), yy + 2, GREEN)
        cv.r(vx + (-2 if side > 0 else 2), yy + 6, 2, 2, RED if k % 3 else BLUE)
        cv.p(vx + (-2 if side > 0 else 2), yy + 6, GOLD_L)
    # rule between text and margin
    cv.r(86, 62, 1, 172, RED)
    # foot ornament
    cv.r(20, 242, 90, 1, INKB)
    cv.poly([(65, 239), (62, 242), (65, 245), (68, 242)], RED)
    cv.p(65, 242, GOLD_L)
    for xx in (30, 100):
        cv.r(xx, 241, 3, 3, BLUE); cv.p(xx + 1, 242, GOLD_L)
    cv.save(os.path.join(OUT, 'book3.png'))


# ------------------------------------------------------------------ 4 문답
def b4():
    rnd = random.Random(104)
    cv = Cv(bg='#15101a')
    stone(cv, 0, 15, 130, 137, rnd)
    bookshelf(cv, 0, 26, 24, 126, 6, rnd)
    bookshelf(cv, 106, 26, 24, 126, 6, rnd)
    # round window
    for yy in range(-12, 13):
        for xx in range(-12, 13):
            d = math.hypot(xx, yy)
            if d <= 12.5:
                c = STONE_DD
                if d <= 10.5:
                    seg = int((math.atan2(yy, xx) + math.pi) / (math.pi / 4))
                    c = ['#2e3f66', '#4a6296', '#27365c', '#4a6296'][seg % 4]
                    if d <= 3.5:
                        c = GOLD
                    if abs(xx) < 1 or abs(yy) < 1 or abs(abs(xx) - abs(yy)) < 1:
                        c = STONE_DD if d > 3.5 else GOLD_L
                cv.p(65 + xx, 44 + yy, c)
    planks(cv, 0, 152, 130, 18, rnd, ph=6)
    cv.r(0, 152, 130, 1, WOOD_LL)
    # rug
    cv.r(30, 158, 70, 9, WINE); cv.r(30, 158, 70, 1, GOLD_D); cv.r(30, 166, 70, 1, GOLD_D)
    lights = [(65, 44, 50, 0.35)]
    for x in (41, 88):
        cv.r(x - 2, 150, 5, 2, '#2a2420'); cv.r(x, 104, 1, 46, '#3a332c'); cv.r(x - 1, 104, 3, 1, GOLD_D)
        f = candle(cv, x - 1, 104, 5)
        lights.append((f[0], f[1], 62, 0.85))
    # lectern
    cv.r(62, 122, 6, 30, WOOD_D); cv.r(62, 122, 1, 30, WOOD_L)
    cv.r(54, 149, 22, 3, WOOD); cv.r(54, 149, 22, 1, WOOD_LL)
    cv.poly([(45, 114), (85, 114), (81, 123), (49, 123)], WOOD); cv.line(45, 114, 85, 114, WOOD_LL)
    cv.poly([(46, 97), (64, 100), (64, 114), (46, 112)], PARCH_L)
    cv.poly([(66, 100), (84, 97), (84, 112), (66, 114)], PARCH)
    cv.r(65, 100, 1, 15, PARCH_DD)
    for k in range(4):
        cv.line(49, 102 + k * 3, 61, 104 + k * 3, '#7a6348')
        cv.line(69, 104 + k * 3, 81, 102 + k * 3, '#7a6348')
    cv.r(48, 100, 3, 3, RED)
    # figures
    cv.dith(13, 150, 26, 4, '#1a1216', 8); cv.dith(91, 150, 26, 4, '#1a1216', 8)
    cv.spr(14, 118, LIBRARIAN, LIB_PAL, k=2)
    cv.spr(92, 120, PLAYER_BACK, PLAYER_PAL, k=2)
    light(cv, lights, ambient=0.34, y0=15, y1=172)
    cv.r(0, 170, 130, 112, '#15101a')
    cv.save(os.path.join(OUT, 'book4.png'))


# ------------------------------------------------------------------ 5 필사실 책상
def b5():
    rnd = random.Random(105)
    cv = Cv(bg='#120e0c')
    planks(cv, 0, 15, 130, 153, rnd, base='#4a2f1c', d='#35200f', l='#5e3d24', ph=10)
    # open book
    cv.r(19, 37, 92, 80, '#1c110b')
    cv.r(18, 34, 92, 80, '#3c1f1a'); cv.r(18, 34, 92, 1, '#5e332b')
    cv.r(21, 37, 43, 73, PARCH); cv.r(66, 37, 41, 73, PARCH_L)
    for k, c in enumerate([PARCH_D, PARCH_DD]):
        cv.r(107 + k, 38 + k, 1, 73, c); cv.r(20 - k, 38 + k, 1, 73, c)
    cv.r(64, 37, 2, 73, PARCH_DD)
    for k, thr in enumerate([9, 5, 2]):
        cv.dith(61 - k, 37, 1, 73, PARCH_DD, thr); cv.dith(68 + k, 37, 1, 73, PARCH_DD, thr)
    cv.r(24, 41, 6, 6, RED); cv.box(24, 41, 6, 6, GOLD_D); cv.p(26, 43, GOLD_L)
    for k, yy in enumerate(range(42, 106, 4)):
        x0 = 32 if yy < 48 else 24
        cv.r(x0, yy, rnd.randrange(22, 36) - (x0 - 24), 1, '#7a6348')
    # small picture on the right page
    cv.r(70, 41, 34, 22, INKB); cv.r(71, 42, 32, 20, '#27365c')
    cv.r(71, 54, 32, 8, '#70492a'); cv.r(84, 46, 6, 8, PARCH_L); cv.r(86, 44, 2, 2, SKIN); cv.r(95, 44, 4, 6, FL3); cv.p(96, 45, FL1)
    for yy in range(67, 106, 4):
        cv.r(70, yy, rnd.randrange(24, 35), 1, '#7a6348')
    cv.r(58, 30, 3, 90, RED); cv.r(58, 30, 1, 90, lite(RED, 0.2)); cv.p(59, 119, PARCH)
    # candle dish
    cv.r(6, 30, 12, 3, GOLD_D); cv.r(6, 30, 12, 1, GOLD_L); cv.r(4, 31, 2, 1, GOLD_D)
    f = candle(cv, 11, 30, 7)
    # inkwell + quill
    cv.r(114, 60, 8, 8, '#1a1a22'); cv.r(114, 60, 8, 1, '#55556a'); cv.r(116, 62, 4, 4, '#0c0c12')
    cv.line(118, 60, 126, 34, PARCH_L); cv.line(119, 60, 127, 35, PARCH_D); cv.line(120, 58, 128, 38, PARCH_L)
    # key ring
    cv.box(6, 128, 9, 9, GOLD); cv.box(7, 129, 7, 7, GOLD_D)
    cv.r(14, 133, 12, 2, GOLD); cv.r(22, 135, 2, 3, GOLD); cv.r(25, 135, 1, 2, GOLD)
    cv.r(11, 137, 2, 11, GOLD_D); cv.r(13, 144, 3, 2, GOLD_D); cv.r(13, 147, 2, 1, GOLD_D)
    # wax + seal
    cv.r(104, 132, 18, 4, RED); cv.r(104, 132, 18, 1, lite(RED, 0.25))
    for yy in range(-5, 6):
        for xx in range(-5, 6):
            if math.hypot(xx, yy) <= 5.3:
                cv.p(96 + xx, 145 + yy, RED if math.hypot(xx, yy) > 3.2 else dark(RED, 0.2))
    cv.p(94, 143, lite(RED, 0.35)); cv.r(95, 144, 3, 3, GOLD_D)
    light(cv, [(f[0], f[1], 95, 0.95), (65, 75, 70, 0.40)], ambient=0.34, y0=15, y1=170)
    cv.r(0, 168, 130, 114, '#120e0c')
    cv.save(os.path.join(OUT, 'book5.png'))


# ------------------------------------------------------------------ small pieces
def scene_paul():
    rnd = random.Random(7)
    cv = Cv(96, 48, bg='#2b2530')
    stone(cv, 0, 0, 96, 34, rnd, base='#5b4a44', d='#47393a', l='#6c5a50', bw=10, bh=5)
    planks(cv, 0, 34, 96, 14, rnd, ph=5)
    # window with dusk sky
    cv.r(64, 5, 18, 21, WOOD_DD)
    for k, c in enumerate(['#27365c', '#34467a', '#4a5a8a', '#8a6a86', '#c97a4a', '#e7a35a']):
        cv.r(66, 7 + k * 3, 14, 3, c)
    cv.p(68, 8, '#e8e2b8'); cv.p(76, 10, '#e8e2b8'); cv.p(72, 13, '#e8e2b8')
    cv.r(72, 7, 1, 18, WOOD_DD); cv.r(66, 15, 14, 1, WOOD_DD)
    # wall shelf with jars
    cv.r(4, 14, 16, 2, WOOD_L)
    cv.r(6, 9, 3, 5, '#a0623a'); cv.r(11, 10, 4, 4, '#6a7b86'); cv.r(16, 8, 2, 6, PARCH_D)
    # Paul
    cv.spr(24, 13, PAUL, PAUL_PAL)
    # table
    cv.r(30, 29, 34, 3, WOOD_L); cv.r(30, 29, 34, 1, WOOD_LL); cv.r(32, 32, 2, 10, WOOD_D); cv.r(60, 32, 2, 10, WOOD_D)
    # scroll on the table, big letters (갈 6:11)
    cv.r(36, 26, 17, 3, PARCH_L); cv.r(35, 25, 2, 5, PARCH_D); cv.r(52, 25, 2, 5, PARCH_D)
    for xx in range(38, 51, 3):
        cv.r(xx, 27, 2, 1, INKB)
    cv.line(33, 24, 37, 27, '#efe3c4')
    # oil lamp
    cv.r(56, 26, 5, 3, '#a0623a'); cv.r(55, 27, 1, 1, '#a0623a'); cv.r(58, 23, 2, 3, FL3); cv.p(58, 24, FL1)
    light(cv, [(59, 24, 70, 1.0), (36, 20, 40, 0.45), (73, 16, 20, 0.25)], ambient=0.46)
    cv.save(os.path.join(OUT, 'scene_paul.png'))


def portrait(name, rows, pal, bg):
    cv = Cv(24, 24, bg=bg)
    cv.dith(0, 0, 24, 24, dark(bg, 0.25), 4)
    cv.spr(0, 2, rows[:11], pal, k=2)
    cv.box(0, 0, 24, 24, GOLD_D)
    cv.save(os.path.join(OUT, name))


def icons():
    # wax seal: earned / empty
    for nm, on in (('seal_on.png', True), ('seal_off.png', False)):
        cv = Cv(13, 13, alpha=True)
        for yy in range(13):
            for xx in range(13):
                d = math.hypot(xx - 6, yy - 6)
                if on:
                    if d <= 6.3:
                        cv.p(xx, yy, RED if d > 4.3 else dark(RED, 0.18))
                elif 5.2 < d <= 6.3 and (xx + yy) % 2 == 0:
                    cv.p(xx, yy, '#8a7a5c')
        if on:
            cv.p(3, 3, lite(RED, 0.4)); cv.p(4, 2, lite(RED, 0.4))
            cv.r(6, 3, 1, 3, FL2); cv.r(5, 5, 3, 3, FL2); cv.p(6, 6, FL1); cv.r(5, 8, 3, 1, GOLD_D)
        cv.save(os.path.join(OUT, nm))
    for nm, on in (('key_on.png', True), ('key_off.png', False)):
        cv = Cv(8, 15, alpha=True)
        c1, c2 = (GOLD_L, GOLD_D) if on else ('#5a4a3a', '#3f3328')
        cv.box(1, 0, 6, 6, c1); cv.box(2, 1, 4, 4, c2)
        cv.r(3, 6, 2, 9, c1); cv.r(4, 6, 1, 9, c2)
        cv.r(5, 10, 2, 1, c1); cv.r(5, 13, 3, 1, c1)
        cv.save(os.path.join(OUT, nm))
    # rubric pointer for margin notes
    cv = Cv(7, 9, alpha=True)
    for k in range(5):
        cv.r(1 + k, k, 1, 9 - 2 * k, RED)
    cv.r(0, 0, 1, 9, dark(RED, 0.3))
    cv.save(os.path.join(OUT, 'manicule.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for fn in (b1, b2, b3, b4, b5, scene_paul, icons):
        fn()
    portrait('face_librarian.png', LIBRARIAN, LIB_PAL, '#3a2a20')
    portrait('face_paul.png', PAUL, PAUL_PAL, '#3a2a20')
    portrait('face_me.png', PLAYER, PLAYER_PAL, '#3a2a20')
    sheet = Image.new('RGB', (W * 5 * 3 + 6 * 8, H * 3 + 16 + 170), (60, 60, 60))
    for k in range(5):
        im = Image.open(os.path.join(OUT, 'book%d.png' % (k + 1))).resize((W * 3, H * 3), Image.NEAREST)
        sheet.paste(im, (8 + k * (W * 3 + 8), 8))
    x = 8
    for nm, sc in (('scene_paul.png', 3), ('face_librarian.png', 4), ('face_paul.png', 4), ('face_me.png', 4),
                   ('seal_on.png', 6), ('seal_off.png', 6), ('key_on.png', 6), ('key_off.png', 6), ('manicule.png', 6)):
        im = Image.open(os.path.join(OUT, nm)).convert('RGBA')
        im = im.resize((im.width * sc // SCALE, im.height * sc // SCALE), Image.NEAREST)
        sheet.paste(im, (x, H * 3 + 20), im)
        x += im.width + 12
    sheet.save(os.path.join(OUT, '_sheet_book.png'))
