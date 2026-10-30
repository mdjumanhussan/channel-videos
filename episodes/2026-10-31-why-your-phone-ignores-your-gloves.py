"""Episode: Why Your Phone Ignores Your Gloves (capacitive touchscreens, insulators, touchscreen gloves, older pressure screens)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "The Screen That Feels You"                  # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                          # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why don't phones work with gloves?"          # headline on the vertical Short
HITS = [(0, 2, 0.0), (0, 3, 0.0), (5, 3, 0.0)]             # the electricity reveal, title card, quiz answer
THUMB = ['YOUR PHONE', "CAN'T FEEL", 'GLOVES']
MUSIC_LEVEL = 0.006                                         # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                              # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.5, (0, 2): 0.5, (3, 2): 0.4, (4, 1): 0.4, (5, 3): 0.6}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'twenty ten': '2010'}

WOOL = (200, 70, 90); WOOLD = (150, 45, 65); SKIN = (225, 180, 150); SKIND = (190, 140, 115)
SILV = (215, 222, 240); GLASS = (24, 34, 74); BODY = (70, 78, 120); SNOW = (225, 235, 255)
ROW = CY; COL = PU

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerpc(p, q, u): u = clamp(u); return tuple(int(p[i] + (q[i] - p[i]) * u) for i in range(3))

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def snow(c, t, a=1.0, n=40):
    if a <= .01: return
    for i in range(n):
        x = (rnd(i, 1) * 1920 + 30 * math.sin(t * .8 + i)) % 1920
        y = 120 + (rnd(i, 2) * 760 + t * (40 + 40 * rnd(i, 3))) % 760
        c.circ(x, y, 3 + 4 * rnd(i, 4), SNOW, a * .7)

def phone(c, x, y, w, h, a=1.0, lit=0.0, bg=BG):
    """A phone, face-on. lit 0..1 brightens the screen. Returns the screen rectangle."""
    if a <= .01: return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, w * .14, BODY, a, bg=bg)
    sx0, sy0, sx1, sy1 = x - w / 2 + w * .06, y - h / 2 + w * .1, x + w / 2 - w * .06, y + h / 2 - w * .1
    c.rr(sx0, sy0, sx1, sy1, w * .09, lerpc(GLASS, (60, 110, 170), lit), a, bg=BODY)
    c.rr(x - w * .12, y - h / 2 + w * .035, x + w * .12, y - h / 2 + w * .07, 6, (40, 46, 80), a, bg=BODY)
    return (sx0, sy0, sx1, sy1)

def finger(c, x, ty, a=1.0, glove=False, silver=False, w=110, ln=420, bg=BG):
    """A finger pointing down, tip at (x, ty). glove=True wraps it in a knitted glove; silver puts metal thread in the tip."""
    if a <= .01: return
    ln = max(140, min(ln, ty - 215))                 # never reach up into the headline
    col = WOOL if glove else SKIN
    c.rr(x - w / 2, ty - ln, x + w / 2, ty, w / 2, col, a, bg=bg)
    if glove:
        for k in range(int(ln / 34)):
            yy = ty - 30 - k * 34
            if yy < ty - ln + 20: break
            c.line([(x - w / 2 + 14, yy), (x, yy + 10), (x + w / 2 - 14, yy)], WOOLD, 4, a, col)
        if silver:
            c.rr(x - w / 2 + 6, ty - 70, x + w / 2 - 6, ty - 4, w / 2 - 6, SILV, a, bg=col)
            for k in range(4):
                c.line([(x - w / 2 + 16, ty - 60 + k * 14), (x + w / 2 - 16, ty - 54 + k * 14)], (150, 160, 190), 3, a, SILV)
    else:
        c.rr(x - w / 2 + 18, ty - ln, x + w / 2 - 18, ty - ln + 60, 20, SKIND, a * .0, bg=col)
        c.rr(x - w * .28, ty - 95, x + w * .28, ty - 22, 22, (240, 205, 185), a, bg=col)   # nail (seen from behind)

def grid(c, x0, y0, x1, y1, nr, nc, a=1.0, pr=1.0, pc=1.0, la=1.0, dots=0.0, val=None, t=0.0, scan=None):
    """The wire grid under the glass. pr/pc draw rows/columns in; dots shows the field at each crossing.
    val(i, j) -> 0..1 field strength (1 = normal). scan = (i, j) crossing being checked."""
    if a <= .01: return
    xs = [x0 + (x1 - x0) * (j + .5) / nc for j in range(nc)]; ys = [y0 + (y1 - y0) * (i + .5) / nr for i in range(nr)]
    for i, yy in enumerate(ys):
        p = clamp(pr * nr - i)
        if p > 0: c.line([(x0, yy), (x0 + (x1 - x0) * p, yy)], ROW, 5, a * la)
    for j, xx in enumerate(xs):
        p = clamp(pc * nc - j)
        if p > 0: c.line([(xx, y0), (xx, y0 + (y1 - y0) * p)], COL, 5, a * la)
    if dots > .01:
        for i, yy in enumerate(ys):
            for j, xx in enumerate(xs):
                v = val(i, j) if val else 1.0
                pul = .85 + .15 * math.sin(t * 3 + i * .7 + j * .5)
                c.circ(xx, yy, 18 * pul, lerpc(PK, YE, v), a * dots * (.25 + .5 * v))
                c.circ(xx, yy, 8, lerpc(PK, YE, v), a * dots)
    if scan is not None:
        i, j = scan
        if 0 <= i < nr and 0 <= j < nc: c.circ(xs[j], ys[i], 30, None, a, outline=INK, ow=4)
    return xs, ys

def meter(c, x, y, vals, a=1.0, labels=True):
    """A panel of readings: one bar per crossing (1 = normal)."""
    if a <= .01: return
    n = len(vals); w = 46; gap = 14; tot = n * w + (n - 1) * gap
    c.rr(x - tot / 2 - 40, y - 230, x + tot / 2 + 40, y + 80, 28, CARD, a, outline=(60, 70, 120), ow=3)
    c.text(x, y - 190, 'readings', 36, DIM, a, w='Bold', bg=CARD)
    c.text(x + tot / 2 + 30, y + 62, 'Illustrative', 22, DIM, a, 'rm', 'Medium', bg=CARD)
    for k, v in enumerate(vals):
        bx = x - tot / 2 + k * (w + gap)
        hh = 200 * v
        c.rr(bx, y + 40 - hh, bx + w, y + 40, 10, GR if v > .8 else PK, a, bg=CARD)

def zap(c, x0, y0, x1, y1, a=1.0, t=0.0, col=YE):
    """A flickering line of electricity from (x0, y0) to (x1, y1)."""
    if a <= .01: return
    pts = []
    for u in range(9):
        f = u / 8; jx = (rnd(u, int(t * 12)) - .5) * 26 if 0 < u < 8 else 0
        pts.append((x0 + (x1 - x0) * f + jx, y0 + (y1 - y0) * f))
    c.line(pts, col, 5, a)

def pen(c, x, ty, a=1.0, bg=BG):
    """A plain plastic pen pointing down, tip at (x, ty)."""
    if a <= .01: return
    c.rr(x - 30, ty - 420, x + 30, ty - 60, 14, (90, 150, 230), a, bg=bg)
    poly(c, [(x - 30, ty - 62), (x + 30, ty - 62), (x + 5, ty), (x - 5, ty)], (230, 230, 240), a, bg)
    c.rr(x + 22, ty - 400, x + 42, ty - 280, 8, (70, 120, 200), a, bg=bg)

def stylus(c, x, ty, a=1.0, bg=BG):
    """A phone stylus with a soft conductive tip."""
    if a <= .01: return
    c.rr(x - 26, max(ty - 420, 215), x + 26, ty - 70, 12, SILV, a, bg=bg)
    c.circ(x, ty - 36, 36, (60, 64, 80), a, bg=bg)
    c.rr(x - 26, ty - 90, x + 26, ty - 60, 6, (150, 160, 190), a, bg=SILV)

def sausage(c, x, ty, a=1.0, bg=BG):
    if a <= .01: return
    c.rr(x - 38, ty - 330, x + 38, ty, 38, (200, 90, 70), a, bg=bg)
    c.rr(x - 20, ty - 300, x - 6, ty - 40, 7, (230, 130, 105), a, bg=(200, 90, 70))
    c.rr(x - 10, ty - 360, x + 10, ty - 322, 6, (230, 210, 90), a, bg=bg)

def atm(c, x, y, a=1.0, bg=BG):
    """A cash machine with a pressure screen."""
    if a <= .01: return
    c.rr(x - 190, y - 230, x + 190, y + 230, 26, (80, 90, 140), a, bg=bg)
    c.rr(x - 150, y - 190, x + 150, y - 10, 14, (50, 120, 110), a, bg=(80, 90, 140))
    c.text(x - 70, y - 100, 'ATM', 54, INK, a, w='Bold', bg=(50, 120, 110))
    c.rr(x - 120, y + 50, x + 120, y + 70, 8, (30, 34, 60), a, bg=(80, 90, 140))
    for k in range(3):
        for m in range(3): c.rr(x - 80 + m * 55, y + 100 + k * 36, x - 40 + m * 55, y + 126 + k * 36, 6, (140, 150, 190), a, bg=(80, 90, 140))

def window(c, x, y, a=1.0, t=0.0, bg=BG):
    """Talking through a closed window: sound waves stop at the glass."""
    if a <= .01: return
    c.rr(x - 30, y - 230, x + 30, y + 230, 10, (120, 160, 220), a * .5, outline=(170, 200, 240), ow=4)
    for k in range(4):
        r = 60 + ((t * 80 + k * 50) % 200)
        aa = a * clamp(1 - r / 260)
        pts = [(x - 300 + r * math.cos(u / 10 - .5), y + r * math.sin(u / 10 - .5)) for u in range(11)]
        if pts[-1][0] < x - 30: c.line(pts, INK, 5, aa)
    c.circ(x - 320, y - 60, 50, SKIN, a); c.rr(x - 380, y, x - 260, y + 200, 40, CY, a)
    c.circ(x + 320, y - 60, 50, SKIN, a); c.rr(x + 260, y, x + 380, y + 200, 40, PU, a)
    c.text(x + 320, y - 170, '?', 64, YE, a, w='Bold')

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    """A phone with its glowing grid, and a gloved finger that gets nothing."""
    sx0, sy0, sx1, sy1 = phone(c, 1560, 560, 520, 900)
    grid(c, sx0 + 20, sy0 + 30, sx1 - 20, sy1 - 30, 7, 4, 1.0, la=.6, dots=1.0, t=1.0)
    finger(c, 1560, 470, 1.0, glove=True, w=150, ln=480)
    c.cross(1740, 330, 120, PK)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Gloves on. Tap. Nothing.', 76, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'One glove off: it works', 76, GR, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, "It feels your electricity, not your push", 62, YE, a * hl(2), w='Bold')
        snow(c, t, a * (1 - hl(2)))
        sc = phone(c, 760, 540, 380, 640, a, lit=hl(1) * .8)
        bare = hl(1)
        tap = abs(math.sin(t * 3.0)) * 40
        if bare < 1: finger(c, 760, 450 - tap, a * (1 - bare), glove=True)
        if bare > 0:
            finger(c, 760, 450 - 20 * (1 - fd(T(1), .4)), a * bare)
            for k in range(3):
                r = 40 + ((t * 120 + k * 50) % 150)
                c.circ(760, 455, r, None, a * bare * clamp(1 - r / 190), outline=GR, ow=5)
        if T(0) > 1.6 and bare < .5:
            c.cross(1220, 420, 120, PK, a * fd(T(0), 1.6) * (1 - bare))
            c.text(1220, 560, 'nothing', 50, PK, a * fd(T(0), 1.6) * (1 - bare), w='Bold')
        if bare > .5 and hl(2) < 1:
            c.check(1220, 420, 80, GR, a * (1 - hl(2)), fd(T(1), .8))
        k2 = a * hl(2)
        if k2 > 0:
            for j in range(3):
                zap(c, 760 + (j - 1) * 25, 235 + j * 20, 760 + (j - 1) * 8, 450, k2 * fd(T(2), .3 + j * .3), t)
            c.text(1360, 400, 'not the push', 50, DIM, k2 * fd(T(2), .4), w='Bold')
            c.text(1360, 480, 'the electricity', 56, YE, k2 * fd(T(2), 1.4), w='Bold')
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 330 + 30 * (1 - m), 'Why Your Phone', 112, INK, m, w='Bold')
        c.text(960, 470 + 30 * (1 - m), 'Ignores Your Gloves', 112, YE, m, w='Bold')
        c.line([(960 - 360 * m, 580), (960 + 360 * m, 580)], CY, 8, m)
        phone(c, 760, 740, 110, 180, m * fd(T(3), .5))
        finger(c, 1160, 790, m * fd(T(3), .7), glove=True, w=60, ln=180)
        c.cross(1240, 690, 50, PK, m * fd(T(3), 1.0))

def s_grid(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Under the glass: a grid of tiny wires', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Made of a material you can see through', 64, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Like graph paper over your screen', 70, YE, hl(2), w='Bold')
    k = hl(0) * (1 - hl(2))
    if k > 0:
        sc = phone(c, 620, 540, 420, 700, k)
        la = 1 - .75 * hl(1)
        grid(c, sc[0] + 20, sc[1] + 30, sc[2] - 20, sc[3] - 30, 8, 5, k, pr=fd(T(0), .3, 1.6), pc=fd(T(0), 1.6, 1.6), la=la)
        c.text(1300, 380, 'rows go across', 52, ROW, k * fd(T(0), .5), 'lm', 'Bold')
        c.text(1300, 470, 'columns go down', 52, COL, k * fd(T(0), 1.8), 'lm', 'Bold')
        k1 = k * hl(1)
        if k1 > 0:
            c.rr(1280, 580, 1820, 760, 30, CARD, k1, outline=CY, ow=3)
            c.text(1550, 640, 'see-through', 48, CY, k1, w='Bold', bg=CARD)
            c.text(1550, 710, 'so you never notice them', 36, INK, k1 * fd(T(1), .8), w='Medium', bg=CARD)
    k2 = hl(2)
    if k2 > 0:
        c.rr(300, 260, 900, 820, 20, (235, 238, 245), k2)
        for q in range(1, 12):
            c.line([(300, 260 + q * 47), (900, 260 + q * 47)], (150, 190, 230), 3, k2 * fd(T(2), q * .05), (235, 238, 245))
            c.line([(300 + q * 50, 260), (300 + q * 50, 820)], (150, 190, 230), 3, k2 * fd(T(2), q * .05), (235, 238, 245))
        c.text(600, 870 - 20, 'graph paper', 40, DIM, k2, w='Bold')
        c.arrow(960, 540, 1120, 540, INK, 6, k2 * fd(T(2), .8), 18)
        sc = phone(c, 1450, 540, 380, 620, k2 * fd(T(2), .8))
        grid(c, sc[0] + 20, sc[1] + 30, sc[2] - 20, sc[3] - 30, 8, 5, k2 * fd(T(2), .8), la=.8)

def s_field(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Every crossing holds a small electric field', 62, YE, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'The phone keeps checking every crossing', 64, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Nothing touching: every reading normal', 64, GR, hl(2), w='Bold')
    k = hl(0)
    x0, y0, x1, y1 = 240, 250, 1040, 830
    scan = None
    if hl(1) > .5:
        n = int(T(1) * 14) % 40; scan = (n // 8, n % 8)
    grid(c, x0, y0, x1, y1, 5, 8, k, dots=fd(T(0), .6, 1.0), t=t, scan=scan)
    if hl(0) * (1 - hl(1)) > 0:
        c.text(1440, 480, 'a crossing', 52, YE, k * (1 - hl(1)) * fd(T(0), 1.2), w='Bold')
        c.text(1440, 550, '= a tiny electric field', 44, INK, k * (1 - hl(1)) * fd(T(0), 1.8), w='Bold')
        c.arrow(1250, 500, 1000, 480, YE, 6, k * (1 - hl(1)) * fd(T(0), 1.2), 18)
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.text(1440, 480, 'check, check, check...', 50, INK, k1, w='Bold')
        c.text(1440, 560, 'every crossing, again and again', 38, DIM, k1 * fd(T(1), 1.0), w='Medium')
    k2 = hl(2)
    if k2 > 0:
        meter(c, 1450, 560, [1.0] * 8, k2)
        c.text(1450, 690, 'all normal', 44, GR, k2 * fd(T(2), .8), w='Bold')

TOUCH = (2, 5)
def s_finger(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Your body conducts electricity', 70, YE, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Your fingertip pulls some field away', 66, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'One reading drops: you touched here', 66, PK, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Two fingers? Two drops. Pinch to zoom', 64, CY, hl(3), w='Bold')
    x0, y0, x1, y1 = 240, 250, 1040, 830
    xs = [x0 + (x1 - x0) * (j + .5) / 8 for j in range(8)]; ys = [y0 + (y1 - y0) * (i + .5) / 5 for i in range(5)]
    sp = 1.6 * fd(T(3), .3, 1.4)
    pts = [TOUCH] if hl(3) < .01 else [(2, int(round(4 - sp))), (2, int(round(5 + sp)))]
    drop = fd(T(1), .8, .8)
    def val(i, j):
        return 1 - .85 * drop if (i, j) in pts else 1.0
    grid(c, x0, y0, x1, y1, 5, 8, 1.0, dots=1.0, val=val, t=t)
    if hl(3) < .01:
        ty = ys[TOUCH[0]] + 30 - 120 * (1 - fd(T(0), .2, 1.2)) - 60 * (1 - fd(T(1), 0, .8))
        finger(c, xs[TOUCH[1]], ty, hl(0))
        if hl(0) * (1 - hl(1)) > 0:
            for j in range(4):
                yy = (ty - 380 + ((t * 160 + j * 90) % 340))
                c.circ(xs[TOUCH[1]], yy, 9, YE, hl(0) * (1 - hl(1)))
    else:
        for (i, j), side in zip(pts, (-1, 1)):
            finger(c, xs[j], ys[i] + 30, hl(3))
    if hl(1) * (1 - hl(2)) > 0:
        kk = hl(1) * (1 - hl(2))
        c.text(1450, 480, 'the field there', 50, INK, kk * fd(T(1), .8), w='Bold')
        c.text(1450, 550, 'gets weaker', 56, PK, kk * fd(T(1), 1.2), w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        meter(c, 1450, 560, [1, 1, 1, 1, 1, .15, 1, 1], k2)
        c.text(1450, 690, 'that spot = your touch', 40, PK, k2 * fd(T(2), .6), w='Bold')
        ring(c, xs[TOUCH[1]], ys[TOUCH[0]], 60, fd(T(2), .2, .8), PK, k2, 6)
    k3 = hl(3)
    if k3 > 0:
        meter(c, 1450, 560, [1, 1, .15, 1, 1, 1, .15, 1] if sp > .8 else [1, 1, 1, 1, .15, .15, 1, 1], k3)
        c.text(1450, 690, 'two touches at once', 40, CY, k3 * fd(T(3), .6), w='Bold')

def s_glove(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Wool, leather, cotton: insulators', 68, WOOL, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Glove on the glass: no change', 70, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, "Like talking through a closed window", 66, YE, hl(2), w='Bold')
    k = 1 - hl(2)
    if k > 0:
        x0, y0, x1, y1 = 240, 250, 1040, 830
        xs = [x0 + (x1 - x0) * (j + .5) / 8 for j in range(8)]; ys = [y0 + (y1 - y0) * (i + .5) / 5 for i in range(5)]
        grid(c, x0, y0, x1, y1, 5, 8, k, dots=1.0, t=t)
        ty = ys[2] + 30 - 120 * (1 - fd(T(1), 0, 1.0))
        finger(c, xs[5], ty, k * hl(0), glove=True)
        k0 = hl(0) * (1 - hl(1))
        if k0 > 0:
            for j, lab in enumerate(('wool', 'leather', 'cotton')):
                c.text(1450, 400 + j * 80, lab, 52, WOOL, k0 * fd(T(0), .3 + j * .4), w='Bold')
            c.text(1450, 680, "don't conduct electricity", 44, INK, k0 * fd(T(0), 2.0), w='Bold')
        k1 = hl(1)
        if k1 > 0:
            meter(c, 1450, 560, [1.0] * 8, k1 * k)
            c.text(1450, 690, 'no change', 48, PK, k1 * k * fd(T(1), 1.2), w='Bold')
            c.cross(1450, 770, 60, PK, k1 * k * fd(T(1), 1.6))
    k2 = hl(2)
    if k2 > 0:
        window(c, 960, 520, k2, t)
        c.text(960, 820, "you're right there... nothing gets through", 40, DIM, k2 * fd(T(2), 1.0), w='Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 208, 'Which one will your phone feel?', 44, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'B: the silver thread conducts', 68, GR, ans, w='Bold')
    k0 = m * (1 - hl(1))
    if k0 > 0:
        sc = phone(c, 960, 560, 300, 520, k0 * fd(T(0), .8))
        c.text(960, 560, '?', 120, YE, k0 * fd(T(0), 1.2), w='Bold', bg=GLASS)
    kc = hl(1)
    if kc > 0:
        for j, (lab, x, txt) in enumerate((('A', 560, 'a plastic pen'), ('B', 1360, 'glove + silver thread'))):
            kk = kc * (.3 + .7 * fd(T(1), j * 1.6))
            good = ans * (1 if j == 1 else 0)
            col = GR if good > .5 else (DIM if ans > .5 else CY)
            c.rr(x - 330, 290, x + 330, 780, 34, CARD, kk, outline=col, ow=4 if good > .5 else 3)
            c.circ(x - 270, 340, 38, CY, kk, bg=CARD); c.text(x - 270, 340, lab, 44, BG, kk, w='Bold', bg=CY)
            if j == 0: pen(c, x, 660, kk, bg=CARD)
            else: finger(c, x, 660, kk, glove=True, silver=True, ln=380, bg=CARD)
            c.rr(x - 200, 670, x + 200, 690, 8, GLASS, kk, bg=CARD)
            c.text(x, 735, txt, 40, INK, kk, w='Bold', bg=CARD)
            if ans > 0:
                if j == 0: c.cross(x + 250, 350, 70, PK, ans)
                else: c.check(x + 250, 350, 46, GR, ans, fd(T(3), .4))
    if T(2) > 0 and ans < 1:
        ring(c, 960, 520, 70, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        c.text(960, 840, 'it links your finger to the screen', 40, GR, ans * fd(T(3), 2.0), w='Bold')

def s_fixes(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Touchscreen gloves: metal thread in the tip', 62, SILV, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Phone styluses: a tip that conducts', 66, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'South Korea, 2010: the sausage stylus', 64, YE, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        finger(c, 700, 640, k0, glove=True, silver=True, w=200, ln=420)
        c.rr(420, 650, 980, 680, 10, GLASS, k0)
        for j in range(3):
            zap(c, 650 + j * 50, 300, 650 + j * 50, 640, k0 * fd(T(0), 1.2 + j * .3), t + j, SILV)
        for j, (lab, col) in enumerate((('silver', SILV), ('or copper', (220, 140, 90)))):
            c.text(1400, 420 + j * 90, lab, 56, col, k0 * fd(T(0), 1.0 + j * .8), w='Bold')
        c.text(1400, 650, 'woven into the fingertip', 40, INK, k0 * fd(T(0), 2.4), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        sc = phone(c, 760, 560, 360, 600, k1)
        grid(c, sc[0] + 20, sc[1] + 30, sc[2] - 20, sc[3] - 30, 7, 4, k1, la=.5, dots=1.0, t=t,
             val=lambda i, j: .2 if (i, j) == (3, 2) else 1.0)
        xs = sc[0] + 20 + (sc[2] - sc[0] - 40) * 2.5 / 4; ys = sc[1] + 30 + (sc[3] - sc[1] - 60) * 3.5 / 7
        stylus(c, xs, ys + 30, k1 * fd(T(1), .2))
        c.text(1400, 450, 'conductive tip', 54, CY, k1 * fd(T(1), .8), w='Bold')
        c.text(1400, 530, 'not plain plastic', 40, DIM, k1 * fd(T(1), 1.6), w='Medium')
    k2 = hl(2)
    if k2 > 0:
        snow(c, t, k2 * .8, 30)
        sc = phone(c, 720, 560, 340, 580, k2, lit=.6)
        sausage(c, 720, 600 + 20 * abs(math.sin(t * 3)), k2 * fd(T(2), .3))
        c.text(1380, 420, 'news reports said', 40, DIM, k2 * fd(T(2), .8), w='Medium')
        c.text(1380, 500, 'people tapped phones', 50, INK, k2 * fd(T(2), 1.2), w='Bold')
        c.text(1380, 570, 'with sausage snacks', 50, YE, k2 * fd(T(2), 1.8), w='Bold')
        c.text(1380, 650, 'to keep their gloves on', 40, INK, k2 * fd(T(2), 2.8), w='Medium')

def s_old(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Some screens DO work with gloves', 70, GR, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'An older kind: two thin layers, a tiny gap', 62, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Press, the layers touch: one touch at a time', 60, CY, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        atm(c, 620, 540, k0 * fd(T(0), .3))
        finger(c, 690, 480, k0 * fd(T(0), .6), glove=True, w=70, ln=260)
        c.check(840, 330, 50, GR, k0 * fd(T(0), 1.2), fd(T(0), 1.4))
        c.rr(1150, 360, 1650, 720, 30, (80, 90, 140), k0 * fd(T(0), 1.6))
        c.rr(1190, 400, 1610, 600, 16, (50, 120, 110), k0 * fd(T(0), 1.6), bg=(80, 90, 140))
        c.text(1400, 500, 'self-checkout', 46, INK, k0 * fd(T(0), 1.6), w='Bold', bg=(50, 120, 110))
        c.text(1400, 780, 'some ATMs and checkouts', 40, DIM, k0 * fd(T(0), 2.0), w='Bold')
    k = hl(1)
    if k > 0:
        press = fd(T(2), .3, .8) * (1 - fd(T(2), 2.6, .6)) if hl(2) > 0 else 0
        x0, x1, yb = 300, 1300, 620
        c.rr(x0, yb, x1, yb + 30, 10, (120, 200, 160), k)
        c.text(800, yb + 80, 'bottom layer', 38, DIM, k * fd(T(1), .4), w='Bold')
        px = 800; dip = 40 * press
        pts = []
        for u in range(41):
            xx = x0 + (x1 - x0) * u / 40
            d = dip * math.exp(-((xx - px) / 120) ** 2)
            pts.append((xx, yb - 46 + d))
        c.line(pts, (200, 220, 255), 14, k)
        c.text(800, yb - 120 - 60 * (1 - press), 'top layer', 38, DIM, k * fd(T(1), .8) * (1 - hl(2)), w='Bold')
        c.text(1330, yb - 23, 'gap', 34, YE, k * fd(T(1), 1.4) * (1 - press), 'lm', 'Bold')
        if hl(2) > 0:
            finger(c, px, yb - 52 + dip, hl(2), glove=True, w=110, ln=330)
            if press > .8:
                c.circ(px, yb - 8, 26, YE, hl(2)); c.circ(px, yb - 8, 50, YE, hl(2) * .35)
            for j, lab in enumerate(('glove', 'fingernail', 'pen')):
                c.text(1580, 360 + j * 90, lab, 46, INK, hl(2) * fd(T(2), 1.2 + j * .4), 'lm', 'Bold')
                c.check(1520, 360 + j * 90, 26, GR, hl(2) * fd(T(2), 1.2 + j * .4), fd(T(2), 1.4 + j * .4))
            c.text(1640, 680, 'but one touch at a time', 36, PK, hl(2) * fd(T(2), 3.4), w='Bold')

RECAPS = [('1', 'It feels', 'your electricity,', 'not your push', YE),
          ('2', 'Gloves', 'are insulators,', 'so nothing changes', WOOL),
          ('3', 'Touch gloves', 'and styluses work:', 'their tips conduct', SILV)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 150, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, l1, l2, l3, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 420 + i * 540; dy = 50 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        sc = phone(c, x, 560 + dy, 400, 640, m, lit=.25)
        c.circ(x, 340 + dy, 46, col, m, bg=GLASS); c.text(x, 340 + dy, nn, 52, BG, m, w='Bold', bg=col)
        c.text(x, 470 + dy, l1, 48, col, m, w='Bold', bg=GLASS)
        c.text(x, 570 + dy, l2, 36, INK, m, w='Bold', bg=GLASS)
        c.text(x, 625 + dy, l3, 36, INK, m, w='Bold', bg=GLASS)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["It's freezing. You're wearing gloves. You tap your phone. Nothing.",
            "Take one glove off, and it works straight away.",
            "That's because your screen isn't feeling the push of your finger. It's feeling your electricity.",
            "Here's why your phone ignores your gloves."], s_hook),
 ('1  ·  THE GRID', ["Under the glass of most phones is a grid of tiny wires. Rows go across, and columns go down.",
            "They're made of a material you can see through, so you never notice them.",
            "Think of the lines on graph paper, laid over your whole screen."], s_grid),
 ('2  ·  THE FIELD', ["Every spot where a row crosses a column holds a small electric field.",
            "The phone keeps checking every one of those crossings, again and again.",
            "With nothing touching the glass, every reading is normal."], s_field),
 ('3  ·  YOUR FINGER', ["Your body conducts electricity. And so does your fingertip.",
            "When it touches the glass over a crossing, it pulls away some of that electric field.",
            "The phone sees the reading drop at that exact spot. That's where you touched.",
            "And because it checks every crossing, it can follow two fingers at once. That's how pinch to zoom works."], s_finger),
 ('4  ·  THE GLOVE', ["Now put a glove on. Wool, leather and cotton don't conduct electricity. They're insulators.",
            "Your finger is right there. But the glove keeps it apart from the field, so the reading doesn't change.",
            "It's like talking to someone through a closed window. You're close, but nothing gets through."], s_glove),
 ('5  ·  QUICK QUESTION', ["Quick question. Which one will your phone feel?",
            "A, a plain plastic pen. Or B, a glove with silver thread in the fingertip.",
            "Three, two, one.",
            "B. The silver thread conducts, so it links your finger to the screen. The plastic pen does nothing."], s_quiz),
 ('6  ·  THE FIXES', ["That's how touchscreen gloves work. Their fingertips have thread with metal, like silver or copper, woven in.",
            "Phone styluses work the same way. Their tips are made to conduct, not plain plastic.",
            "And in twenty ten, news reports from South Korea said people were tapping their phones with sausage snacks, so they could keep their gloves on in the cold."], s_fixes),
 ('7  ·  OLDER SCREENS', ["Some screens do work with gloves, like some cash machines and self-checkouts.",
            "They use an older kind of screen. Two thin layers, with a tiny gap between them.",
            "Press down, the layers touch, and the screen knows where. A glove, a fingernail or a pen all work. But usually only one touch at a time."], s_old),
 ('RECAP', ["So remember three things.",
            "One. Your phone's screen feels the electricity in your finger, not the push.",
            "Two. Gloves are insulators, so the screen can't feel you through them.",
            "Three. Touchscreen gloves and styluses work, because their tips conduct.",
            "If you learned something, subscribe to Short Story Long Thinking."], s_recap),
]

def remap(fn, mp):
    """Reuse a long-video scene with a different line order: mp maps the scene's line index -> narration line index."""
    def g(c, T, t):
        def T2(i, off=0.0):
            if i not in mp: return -99
            j, o = mp[i] if isinstance(mp[i], tuple) else (mp[i], 0.0)
            return T(j, off + o)
        fn(c, T2, t)
    return g

def short_hook(c, T, t):
    if T(1) < 0: remap(s_hook, {0: 0})(c, T, t)
    else: remap(s_hook, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

def short_field(c, T, t):
    if T(1) < 0: remap(s_field, {0: 0})(c, T, t)
    else: remap(s_finger, {0: (1, -9), 1: 1, 2: (1, 2.6)})(c, T, t)

def short_glove(c, T, t):
    if T(1) < 0: remap(s_glove, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_fixes, {0: 1})(c, T, t)

# The Short: its own complete mini-story (hook -> the screen senses electricity -> gloves block it -> answer).
SHORT_SCENES = [
 ('THE HOOK', ["Why doesn't your phone work when you wear gloves?",
               "Because your screen doesn't feel your push. It feels your electricity."],
              short_hook),
 ('THE SCREEN', ["Under the glass is a grid of see-through wires, and every crossing holds a small electric field.",
                 "Your fingertip conducts electricity. Touch the glass, and it pulls some of that field away. The phone sees the drop, right where you touched."],
                short_field),
 ('THE GLOVE', ["Wool and leather don't conduct. So through a glove, nothing changes, and the screen can't feel you.",
                "Touchscreen gloves have metal thread in the fingertips, which carries your touch through."],
               short_glove),
 ('THE ANSWER', ["So why do gloves stop your phone?",
                 "They block the electricity your screen is looking for, right at your fingertip."],
                card('Why gloves stop your phone?', 'They block your electricity.')),
]
SHORT_HITS = [(3, 1, 0.0)]
