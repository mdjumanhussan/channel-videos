"""Episode: Your Brain Can't Really Multitask (It Switches)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Your Brain Can't Really Multitask"   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.97
SHORT_HOOK = "Can your brain really multitask?"     # headline on the vertical Short
HITS = [(0, 2, 0.0), (4, 4, 0.0), (7, 3, 0.0)]     # title card, "up to 40%", 1 in 40 supertaskers
THUMB = ["YOUR BRAIN", "CAN'T DO TWO", 'AT ONCE']
MUSIC_LEVEL = 0.006                                 # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                      # applied lesson 2026-10-19: no dead air before the first word
CAPTION_FIXES = {
    'two thousand and one': '2001', 'two thousand and fifteen': '2015', 'two thousand and ten': '2010',
    'forty percent': '40%', '20 percent': '20%', '2.5 percent': '2.5%', 'one in forty': '1 in 40',
}
# Applied lesson (learnings.md, 2026-10-19): cut the silence before the first word. The engine used to start
# every video with 0.6 s of silence; this episode sets LEAD_IN = 0.15 so the hook is spoken almost at once
# (long video and Short). The engine default stays 0.6 s.

LAPTOP = (120, 135, 190); SCREEN = (34, 52, 96); PHONE = (60, 66, 110)
EMAIL = CY; CALL = PK; ROUTINE = GR

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def hop(t, period=1.2, move=.28):
    """0 or 1 position that jumps back and forth quickly, like attention switching."""
    k = int(t / period); f = t / period - k
    a0 = k % 2; m = ease(f / move)
    return a0 + ((1 - a0) - a0) * m

def beam(c, x0, y0, tx, ty, w, a=1.0, col=YE):
    """Soft spotlight cone from (x0, y0) to an ellipse of half-width w around (tx, ty)."""
    if a <= 0.01: return
    pts = [(x0 - 18, y0), (x0 + 18, y0), (tx + w, ty), (tx - w, ty)]
    c.d.polygon([(px * c.k, py * c.k) for px, py in pts], fill=mix(col, a * .16))
    c.d.ellipse(((tx - w) * c.k, (ty - w * .22) * c.k, (tx + w) * c.k, (ty + w * .22) * c.k), fill=mix(col, a * .26))

def laptop(c, x, y, s, a=1.0, lit=1.0, bg=BG):
    """Laptop centred at (x, y); s = half-width of the screen. lit dims the screen content."""
    if a <= 0.01: return
    c.rr(x - s, y - s * .7, x + s, y + s * .25, s * .06, LAPTOP, a, bg=bg)
    c.rr(x - s * .9, y - s * .6, x + s * .9, y + s * .15, s * .03, SCREEN, a, bg=LAPTOP)
    for j, ln in enumerate((.9, .7, .8, .45)):
        yy = y - s * .45 + j * s * .14
        c.line([(x - s * .75, yy), (x - s * .75 + s * 1.5 * ln, yy)], mix(EMAIL, .35 + .65 * lit, SCREEN), max(3, s * .05), a, SCREEN)
    c.rr(x - s * 1.2, y + s * .25, x + s * 1.2, y + s * .36, s * .05, LAPTOP, a, bg=bg)

def phone(c, x, y, s, a=1.0, lit=1.0, buzz=0.0, t=0.0, bg=BG, col=CALL):
    """Phone centred at (x, y); s = half-height. buzz > 0 shakes it and draws ring waves."""
    if a <= 0.01: return
    dx = buzz * 6 * math.sin(t * 60)
    x = x + dx
    c.rr(x - s * .5, y - s, x + s * .5, y + s, s * .12, PHONE, a, bg=bg)
    c.rr(x - s * .42, y - s * .86, x + s * .42, y + s * .86, s * .08, SCREEN, a, bg=PHONE)
    c.circ(x, y - s * .2, s * .2, mix(col, .35 + .65 * lit, SCREEN), a, bg=SCREEN)
    c.rr(x - s * .25, y + s * .2, x + s * .25, y + s * .32, s * .05, mix(col, .35 + .65 * lit, SCREEN), a, bg=SCREEN)
    if buzz > 0:
        for j in range(2):
            r = s * (.75 + .35 * j + .15 * ((t * 2) % 1))
            for sg in (-1, 1):
                pts = [(x + sg * r * math.cos(u), y + r * math.sin(u)) for u in [-.5 + v * .1 for v in range(11)]]
                c.line(pts, col, max(3, s * .05), a * buzz * (1 - .4 * j), bg)

def tv(c, x, y, s, a=1.0, bg=CARD, t=0.0):
    if a <= 0.01: return
    c.rr(x - s, y - s * .65, x + s, y + s * .55, s * .08, (70, 76, 120), a, bg=bg)
    c.rr(x - s * .9, y - s * .55, x + s * .9, y + s * .45, s * .05, (40, 90, 140), a, bg=(70, 76, 120))
    c.circ(x - s * .3 + s * .2 * math.sin(t * 2), y - s * .1, s * .2, YE, a, bg=(40, 90, 140))
    c.line([(x - s * .3, y + s * .55), (x - s * .5, y + s * .8)], (70, 76, 120), s * .06, a, bg)
    c.line([(x + s * .3, y + s * .55), (x + s * .5, y + s * .8)], (70, 76, 120), s * .06, a, bg)

def shirt(c, x, y, s, a=1.0, bg=CARD, col=GR):
    """A folded T-shirt."""
    if a <= 0.01: return
    c.rr(x - s, y - s * .55, x + s, y + s * .55, s * .12, col, a, bg=bg)
    c.line([(x - s * .35, y - s * .55), (x, y - s * .25), (x + s * .35, y - s * .55)], mix(BG, .3, col), max(3, s * .07), a, col)
    c.line([(x - s * .8, y + s * .1), (x + s * .8, y + s * .1)], mix(BG, .2, col), max(2, s * .04), a, col)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def pie(c, x, y, r, p, col, a=1.0, bg=BG, base=(40, 46, 84)):
    if a <= 0.01: return
    c.circ(x, y, r, base, a, bg=bg)
    if p > 0.005:
        pts = [(x, y)] + [(x + r * math.sin(2 * math.pi * p * u / 60), y - r * math.cos(2 * math.pi * p * u / 60)) for u in range(61)]
        c.d.polygon([(px * c.k, py * c.k) for px, py in pts], fill=mix(col, a, bg))

def person(c, x, y, s, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.circ(x, y - s * .55, s * .32, col, a, bg=bg)
    c.rr(x - s * .45, y - s * .15, x + s * .45, y + s * .6, s * .3, col, a, bg=bg)

def wheel(c, x, y, r, a=1.0, bg=BG, ang=0.0):
    if a <= 0.01: return
    c.circ(x, y, r, None, a, outline=(150, 160, 200), ow=r * .14, bg=bg)
    c.circ(x, y, r * .2, (150, 160, 200), a, bg=bg)
    for da in (math.pi / 2, math.pi * 7 / 6, -math.pi / 6):
        u = da + ang
        c.line([(x, y), (x + r * .9 * math.cos(u), y + r * .9 * math.sin(u))], (150, 160, 200), r * .1, a, bg)

def thumb_art(c):
    beam(c, 1700, 200, 1700, 720, 170, 1)
    laptop(c, 1360, 560, 150, lit=.3)
    phone(c, 1700, 560, 120, lit=1, buzz=1, t=.3)
    c.text(1520, 860, 'switch, switch, switch', 46, YE, 1, w='Bold')

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(2), .2, .5)
    if a > 0:
        # moving from frame one: a spotlight jumps between an email and a phone call
        h = hop(t, 1.0)
        tx = 620 + 680 * h
        beam(c, 960, 250, tx, 760, 230, a)
        laptop(c, 620, 640, 220, a, lit=1 - h)
        phone(c, 1300, 600, 170, a, lit=h, buzz=h, t=t)
        c.text(620, 820, 'email', 40, EMAIL, a * (.45 + .55 * (1 - h)), w='Bold')
        c.text(1300, 820, 'phone call', 40, CALL, a * (.45 + .55 * h), w='Bold')
        c.text(960, 150, 'Doing two things at once?', 70, INK, a, w='Bold')
        k1 = fd(T(1)) if T(1) > -.1 else 0.0
        if k1 > 0:
            n = 1 + int(max(0, T(1)) / 1.0 + .5 * (1 - h))
            pill(c, 960, 245, f'switches: {n}', YE, a * k1, 40, h=74)
    if T(2) > 0:
        m = fd(T(2), .35, .7)
        c.text(960, 330 + 30 * (1 - m), "Your Brain Can't", 128, INK, m, w='Bold')
        c.text(960, 490 + 30 * (1 - m), 'Really Multitask', 128, YE, m, w='Bold')
        c.line([(960 - 340 * m, 600), (960 + 340 * m, 600)], CY, 8, m)
        k = fd(T(2), 1.2)
        c.text(960, 690, 'It switches. Every switch costs time.', 46, DIM, k, w='Medium')

NUMS = [str(i) for i in range(1, 11)]
LETS = list('ABCDEFGHIJ')
MIXED = [v for p in zip(LETS, NUMS) for v in p]
def s_try(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    c.text(960, 140, 'Try this', 66, INK, hl(0), w='Bold')
    def row(items, y, start, rate, cols, a, label):
        if a <= 0.01: return
        c.text(250, y, label, 34, DIM, a, 'rm', 'Medium')
        for j, it in enumerate(items):
            x = 300 + j * (1400 / max(10, len(items))) + 30
            on = T(start) > j * rate if start is not None else False
            col = cols[j % len(cols)]
            sz = 46 if len(items) <= 10 else 36
            c.text(x, y, it, sz, col if on else (70, 78, 120), a, w='Bold')
    a0 = hl(0)
    row(NUMS, 300, 0, .18, [CY], a0, 'numbers')
    row(LETS, 400, 0, .18, [PK], a0 * fd(T(0), .8), 'letters')
    k1 = hl(1)
    if k1 > 0:
        # mixed: slower, with a small "switch" mark between items
        row(MIXED, 540, 1, .3, [PK, CY], k1, 'mixed')
        n = int(clamp(T(1) / .3 - .5, 0, 19))
        for j in range(n):
            x = 300 + (j + .5) * 70 + 30
            c.circ(x, 590, 6, YE, k1 * .8)
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, v, col) in enumerate((('separately', .42, GR), ('mixed together', .78, YE))):
            y = 690 + j * 80
            c.text(470, y, lab, 36, INK, k2, 'rm', 'Bold')
            c.rr(500, y - 24, 500 + 900 * v * fd(T(2), .2 + j * .3, .8), y + 24, 12, col, k2)
        c.text(1440, 730, 'same 20 items', 34, DIM, k2, 'lm', 'Medium')
        c.text(1440, 775, '+ switching', 34, YE, k2, 'lm', 'Bold')
        c.text(1440, 820, 'Illustrative', 22, DIM, k2, 'lm', 'Regular')

def s_spot(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a0 = hl(0) * (1 - fd(T(2), -.2, .4))
    if a0 > 0:
        c.rr(360, 230, 1560, 640, 30, CARD, a0, outline=PU, ow=5)
        c.text(470, 330, '“', 160, PU, a0, w='Bold', bg=CARD)
        c.text(960, 380, '...switching between them', 60, INK, a0, w='Bold', bg=CARD)
        c.text(960, 470, 'very rapidly.', 60, YE, a0, w='Bold', bg=CARD)
        c.text(960, 575, 'Earl Miller, neuroscientist, MIT (NPR, 2008)', 32, DIM, a0, w='Medium', bg=CARD)
        k1 = hl(1)
        if k1 > 0:
            # one attention dot hopping between two task boxes
            h = hop(t, .7, .3)
            for j, (lab, col) in enumerate((('task A', EMAIL), ('task B', CALL))):
                x = 700 + j * 520
                on = (1 - h) if j == 0 else h
                c.rr(x - 140, 700, x + 140, 800, 20, col, k1 * (.35 + .65 * on))
                c.text(x, 750, lab, 38, BG, k1 * (.35 + .65 * on), w='Bold', bg=col)
            x = 700 + 520 * h
            c.circ(x, 670 - 40 * math.sin(math.pi * clamp((t / .7 % 1) / .3)), 16, YE, k1)
    k2 = hl(2)
    if k2 > 0:
        c.text(960, 140, 'A spotlight on a stage', 64, INK, k2, w='Bold')
        c.rr(260, 720, 1660, 790, 14, (60, 50, 70), k2)                         # the stage floor
        h = hop(t, 1.1)
        for j, (lab, col) in enumerate((('EMAIL', EMAIL), ('PHONE CALL', CALL))):
            x = 640 + j * 640
            on = (1 - h) if j == 0 else h
            if j == 0: beam(c, 960, 210, 640 + 640 * h, 715, 210, k2)
            person(c, x, 590, 170, mix(col, .3 + .7 * on), k2)
            c.text(x, 840, lab, 40, col, k2 * (.4 + .6 * on), w='Bold')
        c.text(960, 250, 'lights one actor, then jumps', 38, YE, k2 * fd(T(2), .8), w='Bold')

def s_steps(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a = 1 - fd(T(3), -.2, .4)
    c.text(960, 140, 'Every switch: two hidden steps', 62, INK, hl(0), w='Bold')
    if a > 0:
        for j, (num, title, sub, col, li) in enumerate((('1', 'GOAL SHIFT', '"Do this now, not that"', CY, 1),
                                                         ('2', 'RULE SWAP', '"Rules for that: off. This: on."', PU, 2))):
            k = hl(li) * a
            if k <= 0: continue
            x = 560 + j * 800
            c.rr(x - 340, 240, x + 340, 800, 30, CARD, k, outline=col, ow=5)
            c.circ(x - 270, 305, 38, col, k, bg=CARD); c.text(x - 270, 305, num, 44, BG, k, w='Bold', bg=col)
            c.text(x + 30, 305, title, 50, col, k, w='Bold', bg=CARD)
            c.text(x, 740, sub, 32, INK, k, w='Medium', bg=CARD)
            if j == 0:
                # an arrow swings from target A to target B
                sw = fd(T(1), .5, .8)
                for q, (tx, tc) in enumerate(((x - 160, EMAIL), (x + 160, CALL))):
                    for r in (90, 60, 30):
                        c.circ(tx, 520, r, tc if (r // 30) % 2 else CARD, k * (.4 + .6 * (sw if q else 1 - sw)), bg=CARD)
                ang = math.pi * (1 - sw) * .5 + math.pi * .25
                c.arrow(x, 680, x + 170 * math.cos(math.pi - ang) * (1 if sw > .5 else -1) * -1, 680 - 150, YE, 8, k, 26)
            else:
                # two switches: the old rules turn off, the new rules turn on
                sw = fd(T(2), .7, .5)
                for q, (lab, col2, on) in enumerate((('rules A', EMAIL, 1 - sw), ('rules B', CALL, sw))):
                    yy = 450 + q * 140
                    c.text(x - 140, yy, lab, 36, col2, k, 'lm' if False else 'mm', 'Bold', bg=CARD)
                    c.rr(x + 30, yy - 36, x + 190, yy + 36, 36, mix(col2, .25 + .75 * on, (50, 56, 96)), k, bg=CARD)
                    kx = x + 66 + 88 * on
                    c.circ(kx, yy, 28, INK, k, bg=mix(col2, .25 + .75 * on, (50, 56, 96)))
                    c.text(x + 250, yy, 'ON' if on > .5 else 'OFF', 30, INK if on > .5 else DIM, k, w='Bold', bg=CARD)
    if T(3) > -.1:
        k = fd(T(3))
        # tiny time blocks pile up into a big one
        n = int(clamp(T(3) / 4.5) * 60)
        for j in range(60):
            if j >= n: break
            col_, row_ = j % 12, j // 12
            c.rr(665 + col_ * 50, 760 - row_ * 50, 705 + col_ * 50, 800 - row_ * 50, 6, YE, k * .9)
        c.rr(580, 290, 620, 330, 6, YE, k)
        c.text(645, 310, 'one switch: a few tenths of a second', 40, INK, k, 'lm', 'Bold')
        c.text(960, 410, 'switch all day: it adds up', 44, YE, k * fd(T(3), 1.5), w='Bold')
        c.text(1280, 800, 'Illustrative', 22, DIM, k, 'lm', 'Regular')

def s_study(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a = 1 - fd(T(4), -.2, .4)
    if a > 0:
        c.text(960, 140, 'The switching study, 2001', 62, INK, hl(0) * a, w='Bold')
        a0 = hl(0) * (1 - hl(1))
        if a0 > 0:
            for j in range(3): person(c, 760 + j * 200, 470, 150, (PU, CY, PK)[j], a0 * fd(T(0), .3 + j * .25))
            c.text(960, 700, 'Journal of Experimental Psychology, 2001', 36, DIM, a0, w='Medium')
        k1 = hl(1) * a
        if k1 > 0:
            h = hop(t, 1.0)
            c.rr(300, 230, 820, 470, 26, CARD, k1 * (.45 + .55 * (1 - h)), outline=CY, ow=5)
            c.text(560, 350, '7 × 8 = ?', 64, CY, k1 * (.45 + .55 * (1 - h)), w='Bold', bg=CARD)
            c.rr(1100, 230, 1620, 470, 26, CARD, k1 * (.45 + .55 * h), outline=PK, ow=5)
            kk = k1 * (.45 + .55 * h)
            c.circ(1230, 350, 50, PK, kk, bg=CARD)
            c.rr(1310, 300, 1410, 400, 8, YE, kk, bg=CARD)
            c.d.polygon([(1490 * c.k, 300 * c.k), (1545 * c.k, 400 * c.k), (1435 * c.k, 400 * c.k)], fill=mix(GR, kk, CARD))
            c.arrow(840, 350 - 30, 1080, 350 - 30, YE, 5, k1 * (1 - h), 18)
            c.arrow(1080, 350 + 30, 840, 350 + 30, YE, 5, k1 * h, 18)
            c.text(960, 300, 'switch', 30, YE, k1, w='Bold')
        k2 = hl(2) * a
        if k2 > 0:
            bars = [('simple', .3, GR, 2, 0), ('complex', .62, YE, 2, .6), ('unfamiliar', .9, PK, 3, 0)]
            c.text(300, 560, 'time lost per switch', 32, DIM, k2, 'lm', 'Medium')
            for j, (lab, v, col, li, d) in enumerate(bars):
                kk = hl(li) * a * fd(T(li), d)
                if kk <= 0: continue
                y = 630 + j * 75
                c.text(560, y, lab, 36, INK, kk, 'rm', 'Bold')
                c.rr(590, y - 24, 590 + 900 * v * kk, y + 24, 12, col, a)
            c.text(1520, 800, 'Illustrative', 22, DIM, k2, 'lm', 'Regular')
    if T(4) > -.1:
        k = fd(T(4))
        p = .4 * fd(T(4), .6, 1.4)
        pie(c, 700, 500, 230, p, PK, k)
        c.text(700, 790, 'a working day', 36, DIM, k, w='Medium')
        c.text(1020, 400, 'up to', 50, INK, k, 'lm', 'Bold')
        c.text(1020, 510, '40%', 150, PK, k * fd(T(4), .8), 'lm', 'Bold')
        c.text(1020, 620, 'of productive time', 46, INK, k * fd(T(4), 1.0), 'lm', 'Bold')
        c.text(1020, 690, "David Meyer's estimate", 32, DIM, k * fd(T(4), 1.2), 'lm', 'Medium')

def s_quiz(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 220, 'Which pair is easier together?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 170, 'Routine + thinking: OK', 68, GR, ans, w='Bold')
    k1 = hl(1)
    for j, (x, lab, col) in enumerate(((560, 'Fold laundry + watch TV', ROUTINE), (1360, 'Write email + phone call', CALL))):
        kk = k1 * fd(T(1), j * 1.6)
        if kk <= 0: continue
        good = j == 0
        dim = 1 - (.45 * ans if not good else 0)
        c.rr(x - 330, 290, x + 330, 770, 30, CARD, kk * dim, outline=(GR if ans > 0 else col) if good else col, ow=5)
        c.text(x - 260, 355, 'AB'[j], 46, col, kk * dim, w='Bold', bg=CARD)
        if good:
            shirt(c, x - 130, 560, 90, kk)
            tv(c, x + 140, 520, 120, kk, t=t)
        else:
            laptop(c, x - 120, 560, 120, kk, bg=CARD)
            phone(c, x + 170, 540, 90, kk, buzz=.6, t=t, bg=CARD)
        c.text(x, 710, lab, 38, INK, kk * dim, w='Bold', bg=CARD)
        if ans > 0:
            if good: c.check(x + 260, 355, 40, GR, ans, fd(T(3), .2))
            else: c.cross(x + 260, 355, 40, PK, ans)
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 550, 60, 1 - p, CY, fd(T(2)) * (1 - ans))
        c.text(960, 550, 'or', 40, DIM, fd(T(2)) * (1 - ans), w='Bold')
    if ans > 0:
        c.text(960, 830, 'Two word tasks compete for the same resources', 36, YE, fd(T(4)) if T(4) > -.1 else 0, w='Bold')

SART = '7 2 9 4 3 8 1 6 5 2 9 3 4 7 1 8 2 6'.split()
def s_phone(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0)
    c.text(960, 140, "Even a phone you don't answer", 62, INK, m, w='Bold')
    buzz = (.5 + .5 * math.sin(t * 3)) if T(0) > .5 else 0
    k1 = hl(1)
    phone(c, 1550, 480, 170, m, buzz=buzz * (1 - hl(2) * .5), t=t)
    if k1 <= 0:
        c.text(1550, 720, 'buzz... ignored', 38, CALL, m * fd(T(0), .8), w='Bold')
        laptop(c, 700, 560, 260, m, lit=1)
    else:
        c.text(700, 240, '166 students, a focus task (2015)', 40, INK, k1, w='Bold')
        c.rr(330, 300, 1070, 520, 24, CARD, k1, outline=CY, ow=4)
        c.text(700, 340, 'press for every number except 3', 30, DIM, k1, w='Medium', bg=CARD)
        off = (t * 2.2) % 1
        i0 = int(t * 2.2)
        for j in range(5):
            v = SART[(i0 + j) % len(SART)]
            x = 420 + (j - off) * 140
            if 360 < x < 1040:
                c.text(x, 440, v, 64, YE if v == '3' else INK, k1 * (1 - abs(x - 700) / 500), w='Bold', bg=CARD)
        c.text(1550, 720, 'a call or a text arrives', 34, CALL, k1, w='Bold')
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, v, col) in enumerate((('no alert', .3, GR), ('got an alert', .75, PK))):
            y = 640 + j * 90
            c.text(560, y, lab, 36, INK, k2, 'rm', 'Bold')
            c.rr(590, y - 26, 590 + 520 * v * fd(T(2), .2 + j * .3, .8), y + 26, 12, col, k2)
        c.text(590, 820, 'mistakes (Illustrative)', 26, DIM, k2, 'lm', 'Regular')
        c.text(1550, 780, 'never picked up', 38, YE, k2 * fd(T(2), 1.5), w='Bold')

def s_super(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a = 1 - fd(T(3), -.2, .4)
    c.text(960, 140, 'Two hard things at once?', 62, INK, hl(0) * a, w='Bold')
    if a > 0:
        k1 = hl(1) * a
        if k1 > 0:
            # simulator: road, wheel, a call in progress
            c.rr(360, 220, 1180, 560, 24, (30, 40, 70), k1, outline=DIM, ow=3)
            for j in range(6):
                yy = 280 + ((t * .8 + j / 6) % 1) * 280
                ww = 30 + (yy - 220) * .8
                c.rr(770 - ww * .05, yy, 770 + ww * .05, yy + 22, 4, YE, k1 * .8, bg=(30, 40, 70))
            c.line([(770, 230), (430, 555)], DIM, 5, k1, (30, 40, 70)); c.line([(770, 230), (1110, 555)], DIM, 5, k1, (30, 40, 70))
            wheel(c, 770, 700, 130, k1, ang=.2 * math.sin(t * 1.5))
            phone(c, 1400, 420, 110, k1, buzz=.6, t=t)
            c.text(1400, 580, 'hands-free call:', 32, CALL, k1, w='Bold')
            c.text(1400, 625, 'memory + maths', 32, CALL, k1, w='Bold')
            c.text(1400, 700, '200 people (2010)', 34, INK, k1, w='Medium')
        k2 = hl(2) * a
        if k2 > 0:
            c.rr(1180, 760, 1700, 860, 20, CARD, k2, outline=PK, ow=4)
            c.text(1440, 810, 'braking ≈ 20% slower', 38, PK, k2, w='Bold', bg=CARD)
    if T(3) > -.1:
        k = fd(T(3))
        c.text(960, 140, 'About 1 in 40 had no drop', 62, INK, k, w='Bold')
        for j in range(40):
            col_, row_ = j % 10, j // 10
            x = 600 + col_ * 80; y = 300 + row_ * 120
            star = j == 27
            kk = k * fd(T(3), .02 * j, .3)
            glow = .6 + .4 * math.sin(t * 4) if star else 0
            if star: c.circ(x, y + 5, 52, YE, kk * .25 * glow)
            person(c, x, y + 10, 60, YE if star else (90, 100, 150), kk)
        c.text(960, 820, 'supertaskers: about 2.5%', 46, YE, k * fd(T(3), 1.4), w='Bold')

REC = [('1', 'Thinking tasks: it switches', CY), ('2', 'Each switch costs time', PK), ('3', 'One hard thing at a time', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 530 + up
        if i == 0:
            h = hop(t, .8)
            for q, cc in enumerate((EMAIL, CALL)):
                on = (1 - h) if q == 0 else h
                c.rr(x - 170 + q * 200, y - 60, x - 30 + q * 200, y + 40, 16, cc, m * (.35 + .65 * on), bg=CARD)
            c.circ(x - 100 + 200 * h, y - 100, 14, YE, m, bg=CARD)
        elif i == 1:
            for j in range(9):
                c.rr(x - 120 + (j % 3) * 85, y + 40 - (j // 3) * 60, x - 60 + (j % 3) * 85, y + 85 - (j // 3) * 60, 6, YE, m, bg=CARD)
        else:
            laptop(c, x - 50, y, 110, m, bg=CARD)
            phone(c, x + 175, y + 10, 70, m * .6, lit=.2, bg=CARD)
            c.cross(x + 175, y + 10, 60, PK, m)
        c.text(x, 740 + up, lab, 34, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["You think you're doing two things at once.",
            "Your brain isn't. It's switching, back and forth.",
            "And every switch costs you time. Here's what is really going on."], s_hook),
 ('1  ·  TRY IT', ["Try this. Count from one to ten, then say the letters A to J.",
            "Easy. Now mix them. A, one. B, two. C, three.",
            "Feel the slowdown? Same twenty items. The only new thing is the switching."], s_try),
 ('2  ·  THE SPOTLIGHT', ["MIT neuroscientist Earl Miller puts it simply.",
            "When you think you're multitasking, you're really switching between tasks, very fast.",
            "Think of a spotlight on a stage. It lights one actor, then jumps to the next."], s_spot),
 ('3  ·  TWO STEPS', ["Every switch has two hidden steps.",
            "First, goal shifting. I want to do this now, instead of that.",
            "Second, rule activation. Turn off the rules for that task, and turn on the rules for this one.",
            "One switch can take just a few tenths of a second. But switch all day, and it adds up."], s_steps),
 ('4  ·  THE STUDY', ["In two thousand and one, three psychologists put this to the test.",
            "Young adults switched between tasks, like solving maths problems and sorting shapes.",
            "Every switch cost time. The more complex the tasks, the more time was lost.",
            "And switching to an unfamiliar task cost the most.",
            "One of them, David Meyer, estimates these little blocks can cost as much as forty percent of someone's productive time."], s_study),
 ('5  ·  QUICK QUESTION', ["Quick question. Which pair is easier to do together?",
            "Folding laundry while watching TV? Or writing an email during a phone call?",
            "Three, two, one.",
            "Laundry and TV. Folding is routine, so it needs little attention.",
            "But an email and a call both use words, so they compete for the same resources in your brain."], s_quiz),
 ('6  ·  YOUR PHONE', ["Even a phone you never answer can pull you off task.",
            "In a two thousand and fifteen study, 166 students did a task that needed steady focus, while researchers called or texted some of their phones.",
            "Those who got a call or a text made more mistakes, even though they never picked up."], s_phone),
 ('7  ·  SUPERTASKERS', ["So can anyone do two hard things at once?",
            "In two thousand and ten, 200 people drove in a simulator while doing memory and maths tasks on a hands-free call.",
            "Most did worse. Their braking was about 20 percent slower.",
            "Only about 2.5 percent, around one in forty, showed no drop at all. Researchers call them supertaskers."], s_super),
 ('RECAP', ["So remember three things.",
            "One. For two thinking tasks, your brain doesn't work in parallel. It switches.",
            "Two. Every switch costs time, and complex or unfamiliar tasks cost more.",
            "Three. Do one hard thing at a time. Pair it only with routine jobs, and silence notifications while you focus.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('SWITCHING', ["Can your brain really do two things at once?",
                "Not two thinking tasks. It switches between them, very fast, like a spotlight.",
                "And every switch costs a little time."], s_hook),
 ('TWO STEPS', ["Every switch has two hidden steps.",
                "Pick the new goal.",
                "Then swap in the new task's rules.",
                "Each switch is quick, but they add up."], s_steps),
 ('THE COST', ["Psychologist David Meyer estimates these tiny pauses add up fast.",
               "They can cost as much as forty percent of your productive time."],
              card('Tiny pauses add up', 'Up to 40% of productive time')),
 ('THE ANSWER', ["So no. For thinking tasks, your brain switches, and every switch costs time.",
                 "Do one hard thing at a time. Follow for more."],
                card('Your brain switches', 'Do one hard thing at a time')),
]
SHORT_HITS = [(3, 0, 0.0)]
