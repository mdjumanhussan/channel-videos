"""Episode: How a Microwave Oven Heats Your Food."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Microwaves Heat Food'      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {}
SHORT_HOOK = 'How does a microwave heat food?'    # headline on the vertical Short
HITS = [(0, 4, 0.2), (4, 1, 0.0), (8, 4, 0.0)]    # title card, the key answer, the closing line
THUMB = ['HOW YOUR', 'MICROWAVE', 'HEATS FOOD']

OR = (255, 140, 60); BR = (150, 96, 60); WIN = (8, 11, 26); RED = (235, 50, 60)
METAL = (150, 160, 200); BODY = (44, 52, 100); CHINA = (215, 222, 245); COLD = (60, 90, 170)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def sine(c, x0, x1, y, amp, wl, ph, col, w=5, a=1.0, bg=BG, decay=0.0):
    """Horizontal sine wave from x0 to x1. ph moves it to the right. decay shrinks it along the way."""
    if x1 - x0 < 3 or a <= 0.01: return
    n = max(2, int((x1 - x0) / 3)); pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y + amp * (1 - decay * i / n) * math.sin(2 * math.pi * x / wl - ph)))
    c.line(pts, col, w, a, bg)

def bowl(c, x, y, r, a=1.0, liquid=OR, bg=BG):
    """Bowl with its rim at height y."""
    if a <= 0.01: return
    k = c.k
    c.d.chord(((x - r) * k, (y - r * .95) * k, (x + r) * k, (y + r * .95) * k), 0, 180, fill=mix(CHINA, a, bg))
    c.rr(x - r * .4, y + r * .88, x + r * .4, y + r * 1.02, 6, CHINA, a, bg=bg)
    c.d.ellipse(((x - r) * k, (y - r * .17) * k, (x + r) * k, (y + r * .17) * k), fill=mix(CHINA, a, bg))
    c.d.ellipse(((x - r * .9) * k, (y - r * .12) * k, (x + r * .9) * k, (y + r * .12) * k), fill=mix(liquid, a, bg))

def steam(c, x, y, t, a=1.0, bg=BG, col=DIM, n=3, h=110):
    for i in range(n):
        xx = x + (i - (n - 1) / 2) * 46
        pts = [(xx + 11 * math.sin(j * .55 - t * 3 + i * 1.7), y - j * h / 13) for j in range(14)]
        c.line(pts, col, 5, a * .75, bg)

def oven(c, x, y, w, h, a=1.0, label='', on=0.0, bg=BG):
    c.rr(x, y, x + w, y + h, 28, BODY, a, outline=(90, 100, 160), ow=5, bg=bg)
    c.rr(x + w * .05, y + h * .1, x + w * .72, y + h * .9, 18, mix(YE, .10 * on, WIN), a, outline=mix(YE, on, DIM), ow=4, bg=bg)
    c.rr(x + w * .77, y + h * .1, x + w * .95, y + h * .28, 10, WIN, a, bg=bg)
    if label: c.text(x + w * .86, y + h * .19, label, h * .085, GR, a, w='Mono', bg=WIN)
    for i in range(3):
        for j in range(2): c.circ(x + w * (.815 + j * .09), y + h * (.42 + i * .14), h * .035, DIM, a * .8, bg=BODY)
    c.rr(x + w * .79, y + h * .82, x + w * .93, y + h * .9, 8, CY, a * .8, bg=BODY)

def magnetron(c, x, y, r, a=1.0, bg=BG):
    for i in range(-3, 4):
        c.rr(x - r * 1.25, y + i * r * .26 - r * .06, x + r * 1.25, y + i * r * .26 + r * .06, 6, (70, 80, 130), a, bg=bg)
    c.rr(x - r * .7, y - r, x + r * .7, y + r, 18, (60, 70, 120), a, outline=DIM, ow=4, bg=bg)
    c.rr(x - r * .22, y - r * 1.45, x + r * .22, y - r + 4, 10, PK, a, bg=bg)

def mol(c, x, y, ang, r, a=1.0, bg=BG, signs=False):
    """Water molecule. ang (degrees) is the way the positive (hydrogen) end points."""
    for da in (-52, 52):
        q = math.radians(ang + da); hx, hy = x + r * 1.42 * math.cos(q), y + r * 1.42 * math.sin(q)
        c.circ(hx, hy, r * .6, INK, a, bg=bg)
        if signs: c.text(hx, hy, '+', r * .7, BG, a, w='Bold', bg=INK)
    c.circ(x, y, r, PK, a, bg=bg)
    if signs:
        q = math.radians(ang + 180); c.text(x + r * .35 * math.cos(q), y + r * .35 * math.sin(q) - r * .05, '–', r * .8, BG, a, w='Bold', bg=PK)

def thumb_art(c):
    oven(c, 1170, 330, 660, 420, 1, '2:00', 1)
    bowl(c, 1420, 560, 120, 1, OR, WIN)
    steam(c, 1420, 520, 0.4, 1, WIN, YE)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(4), 0, .5)
    if a > 0:
        rem = max(0, 120 - int(t * 9))
        oven(c, 520, 230, 880, 540, a, f'{rem // 60}:{rem % 60:02d}', fd(t, .3, .6))
        c.line([(690, 692), (1030, 692)], DIM, 6, a * .6, WIN)
        bowl(c, 860, 540, 150, a, OR, WIN)
        steam(c, 860, 500, t, a * fd(t, 1.5, 2.0), WIN)
        if T(1) > 0:
            for i, lab in enumerate(['No flame', 'No glowing coil']):
                m = fd(T(1), i * 1.0) * a; y = 400 + i * 160
                c.rr(70, y - 60, 480, y + 60, 22, CARD, m, outline=PK, ow=3)
                c.cross(125, y, 44, PK, m); c.text(170, y, lab, 38, INK, m, 'lm', 'Medium', bg=CARD)
        if T(2) > 0:
            m = fd(T(2)) * a * (1 - fd(T(3), 0, .4))
            c.text(1640, 480 + 12 * math.sin(t * 3), '?', 300, YE, m, w='Bold')
        if T(3) > 0:
            m = fd(T(3), .8) * a
            for i, (dx, dy) in enumerate([(-70, 0), (0, 6), (70, 0)]):
                r = 13 + 4 * math.sin(t * 5 + i * 2)
                c.circ(860 + dx, 540 + dy, r, CY, m, bg=OR)
            c.text(1040, 380, 'Water', 46, CY, m, w='Bold', bg=WIN)
            c.arrow(1010, 412, 925, 510, CY, 5, m, 16)
    if T(4) > 0:
        m = fd(T(4), .2, .7)
        c.text(960, 400 + 30 * (1 - m), 'How a Microwave', 130, INK, m, w='Bold')
        c.text(960, 560 + 30 * (1 - m), 'Heats Your Food', 130, CY, m, w='Bold')
        c.line([(960 - 260 * m, 670), (960 + 260 * m, 670)], YE, 8, m)
        c.text(960, 740, 'The science inside your kitchen', 44, DIM, fd(T(4), .8), w='Medium')

POPS = [(1330, 0.0), (1420, .5), (1510, .2), (1600, .9), (1690, .35), (1760, 1.2)]
def s_accident(c, T, t):
    c.text(960, 480, 'It started with an accident.', 96, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1))
    c.text(330, 215, '1945', 110, YE, m, w='Bold')
    for k in range(3):                                   # waves leaving the magnetron
        R = 170 + ((t * 120 + k * 90) % 270)
        pts = [(330 + R * math.cos(math.radians(d)), 520 + R * math.sin(math.radians(d))) for d in range(-34, 35, 4)]
        c.line(pts, YE, 6, m * (1 - (R - 170) / 270) * .9)
    magnetron(c, 330, 540, 105, m)
    c.text(330, 745, 'Magnetron (radar part)', 32, DIM, m, w='Medium')
    if T(2) > 0:
        bm = fd(T(2)); p = ease((T(2) - .6) / 2.0)
        c.rr(905, 300 + 120 * p, 1015, 560, 14, BR, bm)
        for k in range(3): c.line([(905, 350 + 120 * p + k * 44), (1015, 350 + 120 * p + k * 44)], (110, 68, 40), 4, bm * (1 - p))
        c.rr(830, 430, 1090, 660, 20, CARD, bm, outline=DIM, ow=4)
        c.line([(830, 485), (960, 520), (1090, 485)], DIM, 4, bm)
        for k, f in enumerate((.7, 1.0, .5)):
            x = 900 + k * 60; c.rr(x - 9, 655, x + 9, 662 + 44 * p * f, 9, BR, bm * fd(T(2), .9))
        c.text(960, 745, 'Candy bar: melted', 32, PK, fd(T(2), 1.6), w='Medium')
    if T(3) > 0:
        pm = fd(T(3))
        c.line([(1280, 640), (1810, 640)], DIM, 4, pm)
        for x, d in POPS:
            u = (T(3) - 1.6 - d) / .7
            if u <= 0: c.circ(x, 622, 15, YE, pm)
            else:
                y = 612 - 190 * math.sin(math.pi * clamp(u)) - (0 if u < 1 else 0)
                for dx, dy in ((-17, 4), (15, 6), (0, -14), (-3, 10)): c.circ(x + dx, y + dy, 20, INK, pm)
                c.circ(x, y + 4, 8, YE, pm)
        c.text(1545, 745, 'Popcorn kernels: popped' if T(3) > 3.2 else 'Popcorn kernels', 32, GR if T(3) > 3.2 else DIM, pm, w='Medium')
    if T(4) > 0:
        fm = fd(T(4))
        c.rr(520, 800, 1400, 874, 26, CARD, fm, outline=YE, ow=3)
        c.text(960, 837, '1947: first microwave oven on sale', 38, INK, fm, w='Medium', bg=CARD)

FAM = [('Radio waves', PU, 400), ('Microwaves', YE, 130), ('Visible light', CY, 24)]
def s_waves(c, T, t):
    c.text(960, 480, 'What is a microwave?', 100, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) < -.1: return
    c.text(960, 185, 'One family: electromagnetic waves', 40, DIM, fd(T(1)), w='Medium')
    for i, (lab, col, wl) in enumerate(FAM):
        m = fd(T(1), .4 + i * .7); x0 = 160 + i * 560
        hi = i == 1 and T(1) > 2.6
        c.rr(x0, 240, x0 + 480, 520, 26, CARD, m, outline=col if hi else None, ow=6)
        c.text(x0 + 240, 300, lab, 44, col, m, w='Bold', bg=CARD)
        sine(c, x0 + 36, x0 + 444, 420, 46, wl, t * 2.2, col, 5, m, CARD)
    c.text(960, 552, 'Wave sizes not to scale', 26, DIM, fd(T(1), 2.4) * .8, w='Regular')
    if T(2) > 0:
        m = fd(T(2))
        sine(c, 370, 370 + 1110 * ease(T(2, .3) / 1.6), 720, 52, 200, t * 5, YE, 6, m)
        magnetron(c, 260, 730, 66, m)
        c.text(260, 852, 'Magnetron', 30, DIM, m, w='Medium')
    if T(3) > 0:
        m = fd(T(3))
        c.line([(610, 622), (810, 622)], INK, 4, m)
        for x in (610, 810): c.line([(x, 606), (x, 638)], INK, 4, m)
        c.text(710, 590, '12 cm', 44, YE, m, w='Bold')
        dm = fd(T(3), 1.4)
        c.circ(1650, 715, 100, (176, 186, 228), dm, outline=INK, ow=4); c.circ(1650, 715, 62, None, dm, outline=(140, 150, 200), ow=3)
        c.circ(1650, 715, 20, BG, dm, outline=INK, ow=3)
        c.line([(1550, 590), (1750, 590)], INK, 4, dm)
        for x in (1550, 1750): c.line([(x, 576), (x, 604)], INK, 4, dm)
        c.text(1650, 850, 'As wide as a CD', 32, INK, dm, w='Medium')

def s_water(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        bowl(c, 960, 430, 230, a0, OR)
        steam(c, 960, 380, t, a0, n=3, h=130)
        for i, (dx, dy) in enumerate([(-110, 0), (0, 8), (110, 0)]):
            c.circ(960 + dx, 430 + dy, 16 + 4 * math.sin(t * 5 + i * 2), CY, a0 * fd(T(0), 1.6 + i * .3), bg=OR)
        c.text(960, 790, 'Almost all food contains water', 54, INK, a0 * fd(T(0), 1.4), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1)); down = False; dip = 1.0
    if T(3) > 0:
        n = int(T(3) / .9); u = T(3) % .9
        ang = -90 + 180 * (n + ease(u / .5)); down = n % 2 == 0; dip = .35 + .65 * ease(u / .2)
    elif T(2) > 0: ang = -20 - 70 * ease(T(2, .4) / .9)
    else: ang = -20 + 5 * math.sin(t * 2)
    if T(2) > 0:
        fm = fd(T(2)) * .85 * dip
        for x in (240, 420, 600, 1320, 1500, 1680):
            if down: c.arrow(x, 300, x, 700, YE, 6, fm, 22)
            else: c.arrow(x, 700, x, 300, YE, 6, fm, 22)
        c.text(420, 790, 'Electric field', 38, YE, fd(T(2)), w='Bold')
    c.text(960, 195, 'Water molecule', 54, INK, m, w='Bold')
    mol(c, 960, 500, ang, 95, m, signs=True)
    lm = m * fd(T(1), 1.0) * (1 - fd(T(2), -.3, .3))
    c.text(1215, 500, 'positive end', 40, INK, lm, 'lm', 'Medium')
    c.text(835, 500, 'negative end', 40, PK, lm, 'rm', 'Medium')
    if T(3) > 0:
        km = fd(T(3), .4)
        c.text(1330, 780, 'Billions of flips every second', 40, INK, km, w='Bold')
        c.text(1330, 835, 'Slowed down here so you can see it', 26, DIM, km * .9, w='Regular')

def s_heat(c, T, t):
    aA = fd(T(0)) * (1 - fd(T(3), -.4, .4))
    if aA > 0:
        heat = ease(t / 7)
        box = mix(OR, .22 * heat, CARD)
        c.rr(150, 230, 950, 740, 30, box, aA, outline=mix(OR, heat, DIM), ow=4)
        for i in range(5):
            for j in range(3):
                ph = t / .5 + i * .37 + j * .61
                ang = 180 * (int(ph) + ease((ph % 1) / .6)) + i * 40
                x = 230 + i * 160 + (4 + 12 * heat) * math.sin(t * 13 + i * 3 + j * 5)
                y = 325 + j * 160 + (4 + 12 * heat) * math.cos(t * 11 + i * 2 + j * 7)
                mol(c, x, y, ang, 24, aA, box)
        c.rr(1018, 250, 1062, 690, 22, CARD, aA, outline=DIM, ow=3)
        col = mix(PK, heat, CY)
        c.rr(1026, 690 - 60 - 360 * heat, 1054, 690, 12, col, aA)
        c.circ(1040, 700, 40, col, aA, outline=DIM, ow=3)
        c.text(1040, 790, 'Heat', 34, DIM, aA, w='Medium')
        if T(1) > 0:
            c.text(1500, 310, 'Moving molecules', 58, INK, fd(T(1)) * aA, w='Bold')
            c.text(1500, 420, '= heat', 100, YE, fd(T(1), .9) * aA, w='Bold')
        if T(2) > 0:
            hm = fd(T(2)) * aA; off = 34 * math.sin(t * 11); skin = (240, 190, 150)
            c.rr(1412, 560 + off, 1496, 770 + off, 40, skin, hm)
            c.rr(1504, 560 - off, 1588, 770 - off, 40, skin, hm)
            c.line([(1500, 540), (1500, 790)], BG, 5, hm)
            for k, (x, y) in enumerate([(1370, 600), (1630, 600), (1355, 700), (1645, 700)]):
                s = 1 if k % 2 else -1
                c.line([(x, y), (x + s * 34, y - 14)], PK, 5, hm * (.5 + .5 * math.sin(t * 9 + k)))
            c.text(1500, 845, 'Like rubbing your hands together', 30, DIM, hm, w='Medium')
    if T(3) > 0:
        m = fd(T(3))
        c.rr(200, 250, 900, 780, 30, CARD, m, outline=GR, ow=4)
        bowl(c, 550, 420, 130, m, OR, CARD); steam(c, 550, 385, t, m, CARD, n=3, h=90)
        c.text(550, 640, 'Wet food', 58, INK, m, w='Bold', bg=CARD)
        c.text(550, 715, 'heats fast', 44, GR, m, w='Medium', bg=CARD)
    if T(4) > 0:
        m = fd(T(4)); k = c.k
        c.rr(1020, 250, 1720, 780, 30, CARD, m, outline=CY, ow=4)
        c.d.ellipse((1190 * k, 420 * k, 1550 * k, 520 * k), fill=mix(CHINA, m, CARD))
        c.d.ellipse((1250 * k, 440 * k, 1490 * k, 500 * k), fill=mix((170, 180, 215), m, CARD))
        c.text(1370, 640, 'Dry plate', 58, INK, m, w='Bold', bg=CARD)
        c.text(1370, 715, 'stays cooler', 44, CY, m, w='Medium', bg=CARD)
        c.text(1370, 832, 'until the hot food warms it', 30, DIM, fd(T(4), 1.6), w='Regular')

def s_box(c, T, t):
    aA = fd(T(0)) * (1 - fd(T(3), -.4, .4))
    if aA > 0:
        c.rr(460, 230, 1460, 750, 26, WIN, aA, outline=METAL, ow=12)
        x, y, vx, vy = 520.0, 320.0, 7.1, 5.3; pts = []
        for _ in range(int(t * 75)):
            x += vx; y += vy
            if x < 486 or x > 1434: vx = -vx; x += 2 * vx
            if y < 256 or y > 724: vy = -vy; y += 2 * vy
            pts.append((x, y))
        pts = pts[-260:]
        for i in range(0, len(pts) - 1, 20):
            c.line(pts[i:i + 21], YE, 5, aA * (.15 + .85 * i / max(1, len(pts))), WIN)
        if pts: c.circ(pts[-1][0], pts[-1][1], 12, YE, aA, bg=WIN)
        c.text(960, 815, 'Metal walls reflect the waves', 46, INK, aA * (1 - fd(T(2), -.2, .3)), w='Bold')
        c.text(960, 815, 'But what about the window?', 46, YE, aA * fd(T(2), .1), w='Bold')
    if T(3) > -.1:
        m = fd(T(3))
        c.rr(930, 195, 990, 815, 14, METAL, m)
        for k in range(16): c.circ(960, 220 + k * 38, 9, BG, m)
        c.text(960, 158, 'Door screen: tiny holes', 38, INK, m, w='Bold')
        if T(4) > 0:
            wm = fd(T(4))
            sine(c, 150, 150 + 770 * ease(T(4) / 1.2), 410, 140, 520, t * 4, YE, 8, wm)
            c.text(330, 215, 'Microwave', 42, YE, wm, w='Bold')
            xm = fd(T(4), 2.2)
            c.cross(1090, 410, 60, PK, xm); c.text(1150, 410, 'Too big for the holes', 46, PK, xm, 'lm', 'Bold')
        if T(5) > 0:
            lm = fd(T(5))
            sine(c, 150, 150 + 1620 * ease(T(5) / 1.6), 676, 6, 16, t * 9, CY, 3, lm)
            c.text(330, 625, 'Light', 42, CY, lm, w='Bold')
            cm = fd(T(5), 1.8)
            c.check(1090, 600, 56, GR, cm, clamp((T(5) - 1.8) / .4)); c.text(1150, 600, 'Light slips through', 46, GR, cm, 'lm', 'Bold')
            c.text(1420, 790, 'Not to scale', 26, DIM, cm * .8, w='Regular')

def s_spots(c, T, t):
    aA = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if aA > 0:
        c.rr(310, 230, 870, 790, 24, WIN, aA, outline=METAL, ow=8)
        for i in range(4):
            for j in range(4):
                hot = (i + j) % 2 == 0
                r = 46 + 6 * math.sin(t * 2.2 + i + j)
                c.circ(380 + i * 140, 300 + j * 140, r, OR if hot else COLD, aA * (.9 if hot else .7), bg=WIN)
        c.circ(1010, 290, 22, OR, aA); c.text(1050, 290, 'Hot spot', 40, INK, aA, 'lm', 'Medium')
        c.circ(1010, 360, 22, COLD, aA); c.text(1050, 360, 'Cold spot', 40, INK, aA, 'lm', 'Medium')
        c.text(590, 835, 'Top view. Illustrative pattern.', 26, DIM, aA * .8, w='Regular')
        if T(1) > 0:
            m = fd(T(1)) * aA
            c.circ(590, 510, 245, None, m, outline=INK, ow=5)
            q = t * 1.3; fx, fy = 590 + 150 * math.cos(q), 510 + 150 * math.sin(q)
            c.circ(fx, fy, 62, CHINA, m, outline=BG, ow=4); c.circ(fx, fy, 40, YE, m)
            c.text(1380, 520, 'The plate turns', 60, INK, m, w='Bold')
            c.text(1380, 600, 'Food moves through the pattern', 34, DIM, m * fd(T(1), .8), w='Medium')
    if T(2) > -.1:
        m = fd(T(2))
        w = c.tw('Myth: it cooks from the inside out', 58, 'Bold')
        c.text(1000, 215, 'Myth: it cooks from the inside out', 58, INK, m, w='Bold')
        c.cross(1000 - w / 2 - 60, 215, 60, PK, fd(T(2, 2.2), 0, .3))
        pm = fd(T(2), 1.0) * (1 - fd(T(3), -.2, .4))          # the myth: heat starting in the middle
        c.circ(960, 550, 225, (70, 66, 100), pm)
        c.circ(960, 550, 70 + 8 * math.sin(t * 4), OR, pm * .9)
        for d in (0, 90, 180, 270):
            q = math.radians(d + 45)
            c.arrow(960 + 95 * math.cos(q), 550 + 95 * math.sin(q), 960 + 175 * math.cos(q), 550 + 175 * math.sin(q), PK, 6, pm, 16)
        c.cross(960, 550, 300, PK, fd(T(2, 3.0), 0, .3) * (1 - fd(T(3), -.2, .4)))
    if T(3) > 0:
        m = fd(T(3)); out = 1 - fd(T(4), -.2, .4)
        warm = ease((T(3) - 5.0) / 4.0)
        c.circ(960, 550, 225, OR, m)
        c.circ(960, 550, 150, mix(OR, .15 + .6 * warm, (70, 66, 100)), m)
        c.text(410, 500, 'Microwaves reach', 40, YE, m * out, w='Bold')
        c.text(410, 556, 'a few centimetres', 40, YE, m * out, w='Bold')
        c.arrow(600, 530, 745, 545, YE, 5, m * out, 16)
        hm = fd(T(3), 4.6)
        for d in (0, 90, 180, 270):
            q = math.radians(d + 45); r0 = 140 - 10 * math.sin(t * 4)
            c.arrow(960 + r0 * math.cos(q), 550 + r0 * math.sin(q), 960 + (r0 - 70) * math.cos(q), 550 + (r0 - 70) * math.sin(q), INK, 6, hm, 16)
        c.text(1510, 500, 'The centre heats', 40, INK, hm * out, w='Bold')
        c.text(1510, 556, 'as heat spreads in', 40, INK, hm * out, w='Bold')
    if T(4) > 0:
        for i, (lab, x) in enumerate([('Stir', 410), ('Let it stand', 1510)]):
            m = fd(T(4), .2 + i * .9)
            c.rr(x - 220, 470, x + 220, 600, 30, CARD, m, outline=GR, ow=5)
            c.text(x, 535, lab, 58, GR, m, w='Bold', bg=CARD)

def s_safe(c, T, t):
    c.text(960, 430, 'Does it make food', 96, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    c.text(960, 560, 'radioactive?', 96, YE, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    aA = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    if T(1) > -.1 and aA > 0:
        c.text(420, 400, 'No.', 240, GR, aA, w='Bold')
        bm = fd(T(1), .9) * aA
        c.rr(180, 600, 660, 710, 30, CARD, bm, outline=CY, ow=5)
        c.text(420, 655, 'Non-ionizing', 54, CY, bm, w='Bold', bg=CARD)
        if T(2) > 0:
            m = fd(T(2)) * aA; k = c.k
            sine(c, 880, 880 + 880 * ease(T(2) / 1.5), 470, 30, 190, t * 5, YE, 6, m)
            for rx, ry, sp, ph in ((230, 95, 1.6, 0), (120, 200, 2.3, 2)):
                c.d.ellipse(((1320 - rx) * k, (470 - ry) * k, (1320 + rx) * k, (470 + ry) * k), outline=mix(DIM, m * .7), width=int(3 * k))
                q = t * sp + ph; c.circ(1320 + rx * math.cos(q), 470 + ry * math.sin(q), 18, CY, m)
            c.circ(1320, 470, 40, PK, m)
            c.text(1320, 760, 'Electrons stay in their atoms', 40, INK, fd(T(2), 1.8) * aA, w='Bold')
    aB = fd(T(3)) * (1 - fd(T(4), -.4, .4))
    if T(3) > -.1 and aB > 0:
        g = ease((T(3) - .8) / 2.4)
        c.circ(1250, 490, 190, mix(OR, .2 + .8 * g, (80, 72, 104)), aB)
        sine(c, 240, 1060, 490, 60, 200, t * 5, YE, 7, aB)
        sine(c, 1060, 1400, 490, 60, 200, t * 5, YE, 7, aB * .8, decay=1.0)
        c.text(560, 340, 'Wave energy', 46, YE, aB, w='Bold')
        c.text(1250, 765, 'becomes heat in the food', 46, OR, aB * fd(T(3), 1.2), w='Bold')
    if T(4) > 0:
        m = fd(T(4)); on = T(4) < 2.1
        oven(c, 240, 300, 600, 370, m, 'ON' if on else 'OPEN', 1.0 if on else 0.0)
        if on: sine(c, 290, 650, 485, 40, 120, t * 6, YE, 5, m, WIN)
        else:                                            # the door swings open
            c.rr(190, 320, 262, 650, 12, BODY, m, outline=DIM, ow=4)
        c.text(540, 745, 'Waves on' if on else 'Door open: waves stop', 40, YE if on else INK, m, w='Bold')
        col = YE if on else (70, 76, 110)
        if on:
            for d in range(0, 360, 45):
                q = math.radians(d + 22); c.line([(1380 + 140 * math.cos(q), 430 + 140 * math.sin(q)), (1380 + 190 * math.cos(q), 430 + 190 * math.sin(q))], YE, 6, m)
        c.circ(1380, 430, 110, col, m)
        c.rr(1335, 525, 1425, 610, 12, METAL, m)
        c.text(1380, 745, 'Lamp on' if on else 'Lamp off: light stops', 40, YE if on else INK, m, w='Bold')

REC = [('1', 'Water molecules flip', CY), ('2', 'Motion becomes heat', OR), ('3', 'Metal keeps waves in', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 250, 290 + up, x + 250, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 185, 355 + up, 40, col, m, bg=CARD); c.text(x - 185, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 520 + up
        if i == 0: mol(c, x, y, -90 + 180 * (int(t / .8) + ease((t % .8) / .45)), 46, m, CARD)
        elif i == 1:
            for k in range(3):
                h = 70 + 30 * math.sin(t * 5 + k * 2)
                poly(c, [(x - 90 + k * 60, y + 60), (x - 30 + k * 60, y + 60), (x - 60 + k * 60, y + 60 - h * 1.6)], mix(OR, .6 + .4 * math.sin(t * 4 + k), YE), m, CARD)
        else:
            c.rr(x - 110, y - 80, x + 110, y + 80, 16, WIN, m, outline=METAL, ow=10, bg=CARD)
            sine(c, x - 90, x + 90, y, 34, 90, t * 5, YE, 5, m, WIN)
        c.text(x, 715 + up, lab, 36, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        o2 = 1 - fd(T(5), -.3, .5)
        c.text(960, 420, 'Not magic.', 130, INK, fd(T(4)) * o2, w='Bold')
        c.text(960, 600, 'Just water, dancing very fast.', 76, CY, fd(T(4), 1.0) * o2, w='Bold')
    if T(5) > 0:
        m = fd(T(5), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, RED, m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=RED)
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(5), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(5), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Your microwave can heat a bowl of soup in two minutes.", "There is no flame. No glowing coil.",
            "So where does the heat come from?", "The answer is hiding in the water inside your food.",
            "Here is how a microwave oven really works."], s_hook),
 ('1  ·  THE ACCIDENT', ["It started with an accident.", "In 1945, an engineer named Percy Spencer was testing a radar part called a magnetron.",
            "A candy bar in his pocket melted.", "He tried popcorn kernels next. They popped.",
            "Two years later, the first microwave oven went on sale."], s_accident),
 ('2  ·  THE WAVES', ["So what is a microwave?", "It is a wave of energy, in the same family as radio waves and visible light.",
            "Inside your oven, a magnetron makes these waves.", "Each wave is about twelve centimetres long. That is as wide as a CD."], s_waves),
 ('3  ·  WATER', ["Now look at the food. Almost all food contains water.", "A water molecule has a positive end and a negative end.",
            "The microwave's electric field pulls on it, so it turns to line up.", "But the field flips direction billions of times every second.",
            "So the molecule keeps flipping, back and forth."], s_water),
 ('4  ·  HEAT', ["All that flipping makes the molecules bump and rub against their neighbours.", "And moving molecules are exactly what heat is.",
            "It is like rubbing your hands together on a cold day.", "That is why wet foods, like soup and vegetables, heat up fast.",
            "And why a dry plate stays cooler, until the hot food warms it."], s_heat),
 ('5  ·  THE BOX', ["The waves stay trapped inside, because metal reflects them.", "The oven is a metal box.", "But what about the window?",
            "The door has a metal screen full of tiny holes.", "The holes are far smaller than the wave, so microwaves cannot get out.",
            "Light waves are much smaller, so you can still see your dinner."], s_box),
 ('6  ·  HOT SPOTS', ["The bouncing waves create a pattern of hot spots and cold spots.", "That is why the plate turns. It moves the food through the pattern.",
            "Here is a common myth. Microwaves do not cook from the inside out.",
            "They only reach a few centimetres into the food. The centre heats as warmth spreads inward.",
            "So stir your food, and let it stand for a minute."], s_spots),
 ('7  ·  IS IT SAFE?', ["Does this make food radioactive?", "No. Microwaves are non-ionizing.",
            "They do not have enough energy to knock electrons out of atoms.", "Their energy simply turns into heat inside the food.",
            "And the moment you open the door, the waves stop. Like switching off a lamp."], s_safe),
 ('RECAP', ["So remember three things.", "One. Microwaves make water molecules flip back and forth.", "Two. That motion becomes heat.",
            "Three. A metal box, and a screen with tiny holes, keep the waves inside.", "Not magic. Just water, dancing very fast.",
            "If this helped, subscribe for more."], s_recap),
]
