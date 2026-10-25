"""Episode: Violet Light Scatters Most. So Why Is the Sky Blue? (Rayleigh scattering, followed along one sunbeam)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Follow One Sunbeam"                      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                       # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why is the sky blue?"                     # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 2, 0.0), (5, 3, 0.0)]           # title card, "that's the blue sky", quiz answer
THUMB = ['VIOLET', 'SCATTERS MORE.', 'SO WHY BLUE?']
MUSIC_LEVEL = 0.006                                      # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                           # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.5, (4, 2): 0.6, (5, 3): 0.5, (6, 2): 0.4}
SHORT_PAUSES = {(0, 2): 0.3}
CAPTION_FIXES = {'sixteen times': '16 times', 'ten times': '10 times', 'eighteen seventy-one': '1871',
                 'zero point four': '0.4'}

RD = (255, 85, 70); OR = (255, 150, 60); YL = (255, 225, 80); GN = (90, 225, 120); BL = (70, 140, 255); VI = (160, 110, 255)
RAINBOW = [('red', RD, 700), ('orange', OR, 620), ('yellow', YL, 580), ('green', GN, 530), ('blue', BL, 470), ('violet', VI, 400)]
SPACE = (5, 6, 14); SKYB = (70, 140, 230); GREY = (70, 78, 120); WHITE = (250, 250, 255)
STARS = [((137 * k) % 1700 + 110, (89 * k) % 580 + 210, 1 + (k % 3)) for k in range(70)]

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def sun(c, x, y, r, t, a=1.0, col=(255, 236, 170), bg=BG):
    if a <= .01: return
    for k in range(12):
        ang = k * math.pi / 6 + t * .3
        c.line([(x + r * 1.25 * math.cos(ang), y + r * 1.25 * math.sin(ang)),
                (x + r * (1.55 + .08 * math.sin(t * 3 + k)) * math.cos(ang), y + r * (1.55 + .08 * math.sin(t * 3 + k)) * math.sin(ang))], col, max(3, r * .1), a, bg)
    c.circ(x, y, r * 1.1, mix(col, .35, bg), a, bg=bg)
    c.circ(x, y, r, col, a, bg=bg)

def wave(c, x0, y0, x1, y1, lam, amp, col, a=1.0, ph=0.0, w=5, bg=BG, p=1.0):
    """Sine wave from (x0,y0) toward (x1,y1); lam = wavelength in px; p = how much of it is drawn."""
    if a <= .01: return
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    n = max(2, int(L * clamp(p) / 4)); pts = []
    for k in range(n + 1):
        s = k * 4
        v = amp * math.sin(2 * math.pi * s / lam - ph)
        pts.append((x0 + ux * s + nx * v, y0 + uy * s + ny * v))
    c.line(pts, col, w, a, bg)

def molecule(c, x, y, r, a=1.0, col=(150, 175, 230), bg=BG):
    if a <= .01: return
    c.circ(x - r * .55, y, r, col, a, bg=bg); c.circ(x + r * .55, y, r, col, a, bg=bg)

def eye(c, x, y, r, a=1.0, iris=CY, bg=BG):
    if a <= .01: return
    top = [(x - r + 2 * r * u / 20, y - r * .55 * math.sin(math.pi * u / 20)) for u in range(21)]
    bot = [(x - r + 2 * r * u / 20, y + r * .55 * math.sin(math.pi * u / 20)) for u in range(21)]
    c.line(top, INK, max(3, r * .09), a, bg); c.line(bot, INK, max(3, r * .09), a, bg)
    c.circ(x, y, r * .38, iris, a, bg=bg); c.circ(x, y, r * .16, BG, a, bg=iris)

def person(c, x, y, s, col=INK, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x, y - s * 1.55, s * .38, col, a, bg=bg)
    c.rr(x - s * .45, y - s * 1.1, x + s * .45, y, s * .3, col, a, bg=bg)

def panel_sky(c, x0, y0, x1, y1, top, bot, a=1.0, n=24):
    for k in range(n):
        u = k / (n - 1); col = tuple(int(top[i] + (bot[i] - top[i]) * u) for i in range(3))
        c.d.rectangle((x0 * c.k, (y0 + (y1 - y0) * k / n) * c.k, x1 * c.k, (y0 + (y1 - y0) * (k + 1) / n) * c.k + 2), fill=mix(col, a))

def stars(c, x0, y0, x1, y1, t, a=1.0, bg=SPACE):
    for (x, y, r) in STARS:
        if x0 < x < x1 and y0 < y < y1:
            c.circ(x, y, r + .6, INK, a * (.45 + .35 * math.sin(t * 1.5 + x)), bg=bg)

def ground(c, cx, cy, R, col, a=1.0, x0=90, x1=1830, ymax=790):
    """Top of a big circle (planet, Moon) filled down to ymax, clipped to the panel, so nothing reaches the captions."""
    if a <= .01: return
    pts = []
    for k in range(81):
        x = x0 + (x1 - x0) * k / 80; d = R * R - (x - cx) ** 2
        y = cy - math.sqrt(d) if d > 0 else ymax
        pts.append((x * c.k, min(ymax, y) * c.k))
    pts += [(x1 * c.k, ymax * c.k), (x0 * c.k, ymax * c.k)]
    c.d.polygon(pts, fill=mix(col, a))

_rng = np.random.default_rng(11)
MOLS = [(float(_rng.uniform(150, 1770)), float(_rng.uniform(270, 740))) for _ in range(30)]

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

STAGES = ['SUN', 'SPACE', 'AIR', 'YOUR EYES', 'SUNSET']
def journey(c, stage, a=1.0):
    """Lesson of 2026-10-26: one sunbeam's journey, with a strip that shows where we are on it."""
    if a <= .01: return
    xs = [560 + i * 200 for i in range(5)]
    c.line([(xs[0], 822), (xs[-1], 822)], (50, 58, 100), 4, a)
    c.line([(xs[0], 822), (xs[stage], 822)], YE, 4, a)
    for i, x in enumerate(xs):
        on = i == stage; done = i < stage
        c.circ(x, 822, 13 if on else 9, YE if (on or done) else (60, 68, 110), a)
        c.text(x, 854, STAGES[i], 22 if not on else 24, YE if on else DIM, a, w='Bold')

def bar_h(lam): return (700.0 / lam) ** 4          # Rayleigh: scattering goes as 1 / wavelength^4

def thumb_art(c):
    panel_sky(c, 1150, 60, 1850, 1020, (40, 90, 200), (140, 200, 255), 1.0, 30)
    sun(c, 1700, 220, 85, 0.4, 1.0, bg=(70, 130, 230))
    for j, (col, lam) in enumerate(((VI, 60), (BL, 80))):
        for q in range(3):
            ang = 2.2 + q * .55 + j * .25
            wave(c, 1500, 560, 1500 + 300 * math.cos(ang), 560 + 300 * math.sin(ang), lam, 14, col, 1, w=9, bg=(110, 170, 245))
    wave(c, 1620, 300, 1480, 540, 140, 16, WHITE, 1, w=10, bg=(80, 140, 230))
    c.circ(1500, 560, 26, INK, 1, bg=(110, 170, 245)); c.circ(1530, 560, 26, INK, 1, bg=(110, 170, 245))
    c.text(1500, 880, '?', 220, YE, 1, w='Bold', stroke=8)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 1.4, .5)
    if a > 0:
        c.text(960, 160, 'Sunlight: white. Space: black.', 70, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 160, 'So why is the sky blue?', 74, CY, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 160, 'Violet scatters even more...', 72, VI, a * hl(2) * (1 - hl(3)), w='Bold')
        c.text(960, 160, 'Follow one sunbeam to your eyes', 66, YE, a * hl(3), w='Bold')
        k = a * (1 - hl(2))
        if k > 0:
            # motion from frame one: three panels with the beam already moving
            c.rr(170, 270, 650, 730, 30, (40, 40, 60), k * .0)
            panel_sky(c, 190, 280, 630, 720, (32, 30, 50), (48, 44, 70), k, 6)
            sun(c, 410, 470, 80, t, k, bg=(40, 38, 60))
            wave(c, 410, 580, 410, 640, 400, 0, WHITE, k, w=10, bg=(44, 40, 66), p=clamp(t / .5))
            c.text(410, 685, 'WHITE', 40, INK, k, w='Bold', bg=(44, 40, 66))
            c.d.rectangle((740 * c.k, 280 * c.k, 1180 * c.k, 720 * c.k), fill=mix(SPACE, k))
            stars(c, 740, 280, 1180, 720, t, k)
            off = (t * 260) % 560
            c.line([(700 + off, 500), (820 + off, 500)], WHITE, 8, k * clamp((1180 - 820 - off) / 60) * clamp(off / 40), SPACE)
            c.text(960, 680, 'BLACK', 40, DIM, k, w='Bold', bg=SPACE)
            m1 = k * (.35 + .65 * hl(1))
            panel_sky(c, 1290, 280, 1730, 720, (40, 100, 215), (150, 205, 255), m1, 24)
            c.text(1510, 470, '?', 160, INK, m1 * hl(1) * (.75 + .25 * math.sin(t * 4)), w='Bold', stroke=5)
            c.text(1510, 680, 'BLUE', 40, INK, m1, w='Bold', stroke=3)
        k2 = a * hl(2)
        if k2 > 0:
            for j, (nm, col, lam) in enumerate(RAINBOW):
                x = 560 + j * 160; h = 52 * bar_h(lam) * fd(T(2), .2 + j * .1)
                c.rr(x - 50, 700 - h, x + 50, 700, 14, col, k2)
                c.text(x, 740, nm, 28, col, k2, w='Bold')
            c.text(560, 330, 'so why not violet?', 44, VI, k2 * fd(T(2), 1.4), w='Bold')
            journey(c, 0, k2 * hl(3))
    if T(3) > 1.4:
        m = fd(T(3), 1.7, .7)
        c.text(960, 330 + 30 * (1 - m), 'Why the Sky', 128, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'Is Blue', 128, CY, m, w='Bold')
        c.line([(960 - 300 * m, 590), (960 + 300 * m, 590)], YE, 8, m)
        c.text(960, 680, 'and not violet', 50, VI, fd(T(3), 2.3), w='Medium')

def s_white(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Sunlight looks white', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'It is every colour mixed', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Each colour is a wave', 64, CY, hl(2), w='Bold')
    k = hl(0) * (1 - hl(2))
    if k > 0:
        sun(c, 260, 480, 95, t, k)
        px = 900
        wave(c, 400, 480, px - 40, 480, 400, 0, WHITE, k, w=12, p=clamp(T(0) / 1.0))
        tri = [(px - 90, 600), (px + 90, 600), (px, 330), (px - 90, 600)]
        c.line(tri, (190, 215, 255), 6, k * fd(T(0), .8))
        c.text(px, 650, 'prism', 30, DIM, k * fd(T(0), 1.0), w='Bold')
        g = hl(1)
        for j, (nm, col, lam) in enumerate(RAINBOW):
            y1 = 300 + j * 75
            c.line([(px + 30, 480), (px + 30 + (1600 - px) * g, 480 + (y1 - 480) * g)], col, 10, k * g)
            c.text(1660, y1, nm, 36, col, k * fd(T(1), .8 + j * .25), 'lm', 'Bold')
        c.text(1200, 760, 'a rainbow is sunlight pulled apart', 36, DIM, k * fd(T(1), 2.4), w='Medium')
    k2 = hl(2)
    if k2 > 0:
        for j, (nm, col, lam, lab) in enumerate((('red', RD, 280, 'long waves'), ('blue', BL, 165, 'short waves'), ('violet', VI, 140, 'shortest'))):
            y = 330 + j * 170
            wave(c, 420, y, 1600, y, lam, 46, col, k2 * fd(T(2), j * .5), ph=t * 4, w=8, p=clamp((T(2) - j * .5) / 1.2))
            c.text(370, y, nm.upper(), 38, col, k2 * fd(T(2), j * .5), 'rm', 'Bold')
            c.text(1640, y, lab, 34, col, k2 * fd(T(2), .8 + j * .5), 'lm', 'Bold')
    journey(c, 0, max(hl(0), hl(2)))

def s_space(c, T, t):
    hl = lambda i: hl_(T, i)
    k = hl(0)
    c.d.rectangle((90 * c.k, 230 * c.k, 1830 * c.k, 780 * c.k), fill=mix(SPACE, k))
    stars(c, 90, 230, 1830, 780, t, k)
    c.text(960, 150, 'Space: almost nothing to hit', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'So the light flies straight past', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'The Moon: no air, black sky', 64, DIM, hl(2), w='Bold')
    k1 = k * (1 - hl(2))
    if k1 > 0:
        sun(c, 230, 500, 80, t, k1, bg=SPACE)
        for q in range(3):
            off = ((t * 300 + q * 450) % 1400)
            c.line([(350 + off, 500 + (q - 1) * 70), (470 + off, 500 + (q - 1) * 70)], WHITE, 8, k1 * clamp((1350 - off) / 100), SPACE)
        if hl(1) > 0:
            eye(c, 960, 680, 70, k1 * hl(1), GREY, bg=SPACE)
            c.text(1100, 680, 'no light comes your way', 34, DIM, k1 * fd(T(1), .8), 'lm', 'Bold', bg=SPACE)
            c.text(960, 330, 'black, even in full sunlight', 40, INK, k1 * fd(T(1), 1.5), w='Bold', bg=SPACE)
    k2 = hl(2)
    if k2 > 0:
        ground(c, 960, 2300, 1600, (120, 120, 130), k2, ymax=780)
        for (x, y, r) in ((600, 755, 16), (1250, 740, 12), (1500, 760, 14)):
            c.circ(x, y, r, (95, 95, 105), k2, bg=(120, 120, 130))
        sun(c, 1500, 380, 60, t, k2, bg=SPACE)
        person(c, 820, 700, 60, (220, 220, 230), k2, bg=SPACE)
        c.text(400, 400, 'sunshine', 34, YE, k2 * fd(T(2), .8), w='Bold', bg=SPACE)
        c.text(400, 450, 'and a black sky', 34, INK, k2 * fd(T(2), 1.2), w='Bold', bg=SPACE)
    journey(c, 1, 1.0 if k > 0 else 0)

def s_air(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Into the air: tiny molecules', 64, INK, hl(0) * (1 - max(hl(1), hl(2))), w='Bold')
    c.text(960, 150, 'Long waves roll past. Short ones splash.', 60, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Blue gets thrown all over the sky', 64, BL, hl(2), w='Bold')
    k0 = hl(0) * (1 - max(hl(1), hl(2)))
    if k0 > 0:
        panel_sky(c, 90, 230, 1830, 780, (18, 30, 70), (30, 60, 120), k0, 12)
        for q, (x0_, y0_) in enumerate(MOLS):
            x = x0_ + 18 * math.sin(t * 1.3 + q); y = y0_ + 14 * math.cos(t * 1.1 + q)
            if 600 < x < 1320 and 410 < y < 610: continue
            molecule(c, x, y, 9, k0, bg=(25, 45, 100))
        c.rr(620, 430, 1300, 590, 26, CARD, k0 * fd(T(0), 1.0), outline=CY, ow=3, bg=(25, 45, 100))
        c.text(960, 480, 'nitrogen + oxygen', 44, CY, k0 * fd(T(0), 1.0), w='Bold', bg=CARD)
        c.text(960, 540, 'each about 0.4 nm wide', 36, INK, k0 * fd(T(0), 1.4), w='Bold', bg=CARD)
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        SEA = (20, 50, 90)
        c.rr(90, 230, 1830, 780, 30, SEA, k1)
        px, py = 960, 500
        c.rr(px - 16, 300, px + 16, 720, 6, (150, 105, 70), k1, bg=SEA)
        c.text(px, 270, 'post', 30, DIM, k1, w='Bold', bg=SEA)
        wave(c, 120, 380, 1800, 380, 520, 40, (120, 190, 255), k1 * fd(T(1), .3), ph=t * 2.2, w=8, bg=SEA)
        c.text(1500, 300, 'long swell: rolls past', 34, (120, 190, 255), k1 * fd(T(1), 1.0), w='Bold', bg=SEA)
        wave(c, 120, 620, px - 20, 620, 70, 14, BL, k1 * fd(T(1), 2.2), ph=t * 6, w=6, bg=SEA)
        for q in range(4):
            ph = (t * .9 + q / 4) % 1.0
            rr_ = 30 + ph * 140
            pts = [(px + rr_ * math.cos(u / 20 * math.pi - math.pi / 2), 620 + rr_ * math.sin(u / 20 * math.pi - math.pi / 2)) for u in range(21)]
            c.line(pts, BL, 4, k1 * fd(T(1), 2.8) * (1 - ph), SEA)
        c.text(1500, 720, 'short ripples: splash off', 34, BL, k1 * fd(T(1), 3.2), w='Bold', bg=SEA)
    k2 = hl(2)
    if k2 > 0:
        panel_sky(c, 90, 230, 1830, 780, (25, 55, 130), (60, 120, 210), k2, 12)
        bgc = (45, 90, 170)
        wave(c, 100, 500, 1820, 500, 300, 10, RD, k2, ph=t * 3, w=9, bg=bgc)
        c.text(960, 735, 'red: mostly straight through', 36, RD, k2 * fd(T(2), 1.0), w='Bold', stroke=3)
        for q, (mx, my) in enumerate(((520, 500), (960, 500), (1380, 500))):
            molecule(c, mx, my, 12, k2, (230, 235, 255), bg=bgc)
            for j in range(6):
                ang = j * math.pi / 3 + .5 + q
                ph = (t * .8 + j / 6) % 1.0
                L = 40 + 210 * ph
                wave(c, mx + 30 * math.cos(ang), my + 30 * math.sin(ang), mx + (30 + L) * math.cos(ang), my + (30 + L) * math.sin(ang), 34, 7, BL,
                     k2 * fd(T(2), .4 + q * .3) * (1 - ph * .6), w=5, bg=bgc)
    journey(c, 2, max(hl(0), hl(2)) if hl(1) == 0 or hl(2) > 0 else 0.0)

def s_much(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Halve the wave: 16 times the scatter', 60, YE, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Violet: about 10 times red', 64, VI, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Blue arrives from every direction', 64, BL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Rayleigh scattering', 70, CY, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j, (lab, lam, h, col) in enumerate((('one wavelength', 260, 30, RD), ('half as long', 130, 480, BL))):
            x = 640 + j * 640
            wave(c, x - 220, 235, x + 220, 235, lam, 24, col, k0 * fd(T(0), j * .6), ph=t * 4, w=7)
            hh = h * .8 * fd(T(0), .8 + j * .8, .9)
            c.rr(x - 90, 770 - hh, x + 90, 770, 16, col, k0)
            c.text(x, 770 - hh - 40, '1x' if j == 0 else '16x', 50, col, k0 * fd(T(0), 1.2 + j * .8), w='Bold')
            c.text(x, 285, lab, 32, DIM, k0 * fd(T(0), j * .6), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        for j, (nm, col, lam) in enumerate(RAINBOW):
            x = 520 + j * 176; h = 50 * bar_h(lam) * fd(T(1), .2 + j * .15, .7)
            c.rr(x - 58, 740 - h, x + 58, 740, 14, col, k1)
            c.text(x, 772, nm, 28, col, k1, w='Bold')
        c.line([(430, 740), (1490, 740)], DIM, 3, k1)
        c.text(1660, 340, '~10x', 64, VI, k1 * fd(T(1), 1.6), w='Bold')
        c.text(1660, 410, 'violet vs red', 30, DIM, k1 * fd(T(1), 1.8), w='Bold')
        c.text(1840, 740, 'Bars: 1 / wavelength^4', 24, DIM, k1, 'rm', 'Medium')
    k2 = max(hl(2) * (1 - hl(3)), hl(3))
    if k2 > 0:
        panel_sky(c, 90, 230, 1830, 780, (35, 85, 200), (130, 195, 255), k2, 20)
        bgc = (80, 145, 235)
        person(c, 960, 760, 70, (20, 26, 50), k2, bg=bgc)
        eye(c, 960, 620, 34, k2, BL, bg=bgc)
        for j in range(9):
            ang = math.pi + j * math.pi / 8
            ph = (t * .7 + j / 9) % 1.0
            r0 = 520 - 360 * ph
            wave(c, 960 + r0 * math.cos(ang), 600 + r0 * .8 * math.sin(ang), 960 + (r0 - 90) * math.cos(ang), 600 + (r0 - 90) * .8 * math.sin(ang),
                 30, 6, (30, 70, 200), k2 * (1 - ph * .3) * fd(T(2), j * .1), w=5, bg=bgc)
        if hl(3) > 0:
            c.rr(1300, 300, 1780, 470, 24, CARD, hl(3), outline=CY, ow=3, bg=bgc)
            c.text(1540, 355, 'Lord Rayleigh', 40, CY, hl(3), w='Bold', bg=CARD)
            c.text(1540, 415, 'first papers: 1871', 34, INK, hl(3) * fd(T(3), .6), w='Bold', bg=CARD)
    journey(c, 3, 1.0)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3); eyes = hl(4)
    short = T(1) < -50 and T(2) < -50          # the Short reuses this scene without the A/B choice
    c.text(960, 140, 'Quick question' if not short else 'So why not violet?', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 215, 'Violet scatters most. Why is the sky not violet?', 44, INK, m * fd(T(0), .5) * (1 - ans) * (0 if short else 1), w='Bold')
    c.text(960, 140, 'Less violet arrives' if short else 'B: less violet arrives', 64, GR, ans * (1 - eyes), w='Bold')
    c.text(960, 140, 'And your eyes favour blue', 64, BL, eyes, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        for j, (nm, col, lam) in enumerate(RAINBOW):
            x = 560 + j * 160; h = 46 * bar_h(lam)
            c.rr(x - 50, 760 - h, x + 50, 760, 14, col, k0 * (1 if nm == 'violet' else .45))
        c.text(1520, 300, '?', 120, VI, k0 * (.7 + .3 * math.sin(t * 4)), w='Bold')
    kc = hl(1) * (1 - ans)
    if kc > 0:
        for j, (lab, l1, l2, x) in enumerate((('A', 'Sunlight has', 'no violet', 560), ('B', 'Less violet arrives,', 'eyes see it poorly', 1360))):
            kk = hl(1) * (.3 + .7 * fd(T(1), j * 1.6)) * (1 - ans)
            c.rr(x - 320, 300, x + 320, 700, 34, CARD, kk, outline=CY, ow=3)
            c.circ(x - 250, 360, 42, CY, kk, bg=CARD); c.text(x - 250, 360, lab, 48, BG, kk, w='Bold', bg=CY)
            c.text(x, 500, l1, 44, INK, kk, w='Bold', bg=CARD)
            c.text(x, 570, l2, 44, INK, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 500, 70, 1 - p, YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        ka = ans * (1 - eyes)
        if ka > 0:
            # sunlight per colour (illustrative): less at the violet end, a little more lost high in the air
            sunlight = [1.0, 1.05, 1.08, 1.08, 1.0, .62]
            for j, (nm, col, lam) in enumerate(RAINBOW):
                x = 560 + j * 160; full = 46 * bar_h(lam)
                fac = sunlight[j] * (1 if nm != 'violet' else 1 - .25 * fd(T(3), 2.0, 1.0))
                h = full * (1 - (1 - fac) * fd(T(3), .6, 1.0))
                c.rr(x - 50, 760 - full, x + 50, 760, 14, None, ka * .6, outline=GREY, ow=3)
                c.rr(x - 50, 760 - h, x + 50, 760, 14, col, ka)
                c.text(x, 790, nm, 26, col, ka, w='Bold')
            c.text(1500, 300, 'Sun sends less violet', 36, VI, ka * fd(T(3), .8), w='Bold')
            c.text(1500, 350, 'some absorbed high up', 36, VI, ka * fd(T(3), 2.0), w='Bold')
            c.text(1840, 740, 'Illustrative', 26, DIM, ka, 'rm', 'Medium')
        if eyes > 0:
            eye(c, 520, 470, 150, eyes)
            for j, (lab, col, s) in enumerate((('blue', BL, 1.0), ('violet', VI, .35))):
                y = 380 + j * 170
                c.text(800, y, lab, 40, col, eyes, 'lm', 'Bold')
                c.rr(980, y - 30, 980 + 520 * s * fd(T(4), .4 + j * .4, .8), y + 30, 14, col, eyes)
            c.text(1240, 300, 'how strongly your eye responds (illustrative)', 28, DIM, eyes, w='Medium')
            panel_sky(c, 980, 630, 1500, 740, (90, 160, 245), (120, 185, 250), eyes * fd(T(4), 1.4), 6)
            c.text(1240, 685, 'sky blue', 40, INK, eyes * fd(T(4), 1.6), w='Bold', stroke=3)
    journey(c, 3, 1.0 if not short else 0.0)

def s_sunset(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'Evening: a much longer path', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 140, 'Blue is scattered away on the way', 64, BL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 140, "What's left: yellow, orange, red", 64, OR, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 140, 'Dust and haze: even redder', 64, RD, hl(3), w='Bold')
    k = hl(0)
    if k <= 0: return
    glow = hl(2)
    top = tuple(int(a_ + (b_ - a_) * glow) for a_, b_ in zip((20, 40, 90), (60, 40, 90)))
    bot = tuple(int(a_ + (b_ - a_) * (glow + .3 * hl(3)) / 1.3) for a_, b_ in zip((50, 100, 180), (255, 120, 60)))
    panel_sky(c, 90, 230, 1830, 790, top, bot, k, 20)
    # atmosphere shell and ground
    cx, cy = 960, 2500
    ground(c, cx, cy, 1900, mix((70, 120, 200), .35, bot), k)
    ground(c, cx, cy, 1780, (40, 70, 50), k)
    ox, oy = 960, 720
    person(c, ox, oy + 4, 40, (20, 24, 40), k, bg=(40, 70, 50))
    # noon: short path from above
    c.text(1450, 280, 'noon: short path', 32, INK, k * (1 - glow), w='Bold', stroke=3)
    sun(c, 1450, 360, 34, t, k * (1 - glow), bg=top)
    c.line([(1450, 400), (ox + 30, oy - 70)], WHITE, 6, k * (1 - glow) * .8)
    # evening: low sun, long path through the air
    sx, sy = 170, 650
    sun(c, sx, sy, 50, t, k, col=(255, 200, 120), bg=bot)
    n = 30
    for q in range(n):
        u = q / (n - 1); x = sx + 60 + (ox - 40 - sx - 60) * u; y = sy + (oy - 40 - sy) * u
        col = tuple(int(WHITE[i] + (OR[i] - WHITE[i]) * clamp(u * 1.4 * hl(1) + .2 * hl(3))) for i in range(3))
        c.circ(x, y, 6, col, k * fd(T(0), u * .8, .3), bg=bot)
    c.text(520, 560, 'sunset: long path', 32, INK, k * fd(T(0), 1.0), w='Bold', stroke=3)
    if hl(1) > 0:
        for q in range(7):
            u = (q + .5) / 7; x = sx + 60 + (ox - 100 - sx) * u; y = sy + (oy - 40 - sy) * u
            ph = (t * .8 + q / 7) % 1.0
            wave(c, x, y, x + 30 * math.cos(-1.9 + q * .5), y - 140 * ph - 20, 30, 6, BL, hl(1) * (1 - ph), w=5, bg=bot)
    if hl(2) > 0:
        c.circ(ox + 70, oy - 60, 22, OR, hl(2), bg=bot)
        c.text(ox + 110, oy - 60, 'reaches you: orange', 32, OR, hl(2) * fd(T(2), .6), 'lm', 'Bold', stroke=3)
    if hl(3) > 0:
        for q in range(40):
            x = 200 + (q * 97) % 760; y = 600 + (q * 53) % 110
            c.circ(x + 6 * math.sin(t + q), y, 3, (200, 170, 140), hl(3) * .8, bg=bot)
    journey(c, 4, 1.0)

def cloud(c, x, y, s, a=1.0, col=WHITE, bg=BG):
    for (dx, dy, r) in ((-1.0, .15, .55), (-.4, -.25, .75), (.35, -.1, .7), (.95, .2, .5), (0, .3, .6)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)

def s_clouds(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Cloud droplets are much bigger', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'All colours, scattered evenly = white', 62, WHITE, hl(1), w='Bold')
    k = hl(0)
    if k <= 0: return
    bgc = (40, 95, 190)
    panel_sky(c, 90, 230, 1830, 790, (30, 80, 190), (110, 180, 250), k, 16)
    k0 = k * (1 - hl(1))
    if k0 > 0:
        molecule(c, 520, 500, 8, k0, (230, 235, 255), bg=bgc)
        c.text(520, 580, 'air molecule', 34, INK, k0, w='Bold', stroke=3)
        c.circ(1250, 480, 190, (190, 220, 255), k0 * fd(T(0), .5), bg=bgc)
        c.circ(1200, 420, 40, WHITE, k0 * fd(T(0), .5) * .6, bg=(190, 220, 255))
        c.text(1250, 720, 'water droplet (not to scale: far bigger still)', 32, INK, k0 * fd(T(0), 1.0), w='Bold', stroke=3)
        wave(c, 720, 480, 1040, 480, 90, 16, WHITE, k0 * fd(T(0), 1.6), ph=t * 4, w=6, bg=bgc)
        c.text(880, 420, 'light wave', 28, INK, k0 * fd(T(0), 1.8), w='Bold', stroke=3)
    k1 = hl(1)
    if k1 > 0:
        cx, cy = 700, 500
        c.circ(cx, cy, 95, (190, 220, 255), k1, bg=bgc)
        for j, (nm, col, lam) in enumerate(RAINBOW):
            for q in range(2):
                ang = j * math.pi / 6 + q * math.pi + t * .2
                ph = (t * .7 + j / 6 + q / 2) % 1.0
                L = 50 + 150 * ph
                wave(c, cx + 105 * math.cos(ang), cy + 105 * math.sin(ang), cx + (105 + L) * math.cos(ang), cy + (105 + L) * math.sin(ang),
                     50, 8, col, k1 * (1 - ph * .5), w=6, bg=bgc)
        c.text(1150, 500, '=', 110, INK, k1 * fd(T(1), 1.4), w='Bold', stroke=3)
        cloud(c, 1500, 520, 150, k1 * fd(T(1), 1.8), bg=bgc)
        c.text(1500, 720, 'white', 44, INK, k1 * fd(T(1), 2.2), w='Bold', stroke=3)

def s_glass(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Try it at home', 70, YE, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, '1 teaspoon of milk + a glass of water', 60, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A sky and a sunset in one glass', 64, OR, hl(2), w='Bold')
    k = max(hl(0), hl(1))
    if k <= 0: return
    gx0, gx1, gy0, gy1 = 760, 1160, 280, 760
    milk = hl(1); side = fd(T(1), 2.0); top = hl(2)
    # water, cloudy once the milk is in; bluish from the side, orange at the bottom when lit from the top
    for q in range(20):
        u = q / 19
        base = tuple(int(30 + (205 - 30) * milk * .55) for _ in range(3))
        col = mix((150, 185, 255), .5 * side * (1 - top) * milk, base)
        col = mix(OR, top * clamp((u - .35) / .65) * .9, mix((220, 230, 255), top * (1 - u) * .7, col))
        c.d.rectangle((gx0 * c.k, (gy0 + 40 + (gy1 - gy0 - 40) * q / 20) * c.k, gx1 * c.k, (gy0 + 40 + (gy1 - gy0 - 40) * (q + 1) / 20) * c.k + 2), fill=mix(col, k))
    c.line([(gx0, gy0), (gx0, gy1), (gx1, gy1), (gx1, gy0)], (200, 215, 245), 8, k)
    if hl(0) > 0 and milk < 1:
        c.text(960, 220, 'clear water', 34, DIM, hl(0) * (1 - milk), w='Bold')
    if milk > 0:
        # teaspoon drip
        ph = clamp(T(1) / 1.2)
        c.circ(960, 230 + ph * 120, 14, WHITE, milk * (1 - ph))
    # phone light from the side (line 1), then from the top (line 2)
    ks = milk * (1 - top)
    if ks > 0:
        c.rr(380, 470, 470, 630, 16, (60, 64, 90), ks)
        c.circ(470, 550, 14, YE, ks)
        c.line([(485, 550), (gx0, 550)], YL, 10, ks * .7)
        eye(c, 960, 860 - 40, 40, ks * side, BL)
        c.text(1220, 560, 'from the side:', 34, DIM, ks * side, 'lm', 'Bold')
        c.text(1220, 610, 'slightly blue', 44, BL, ks * side, 'lm', 'Bold')
    if top > 0:
        c.rr(880, 205, 1040, 255, 14, (60, 64, 90), top)
        c.line([(960, 255), (960, gy0 + 40)], YL, 10, top * .7)
        c.text(1220, 680, 'bottom:', 34, DIM, top * fd(T(2), .6), 'lm', 'Bold')
        c.text(1220, 730, 'yellow-orange', 44, OR, top * fd(T(2), .6), 'lm', 'Bold')
        c.text(560, 330, 'more milk to cross', 32, DIM, top * fd(T(2), 1.2), w='Bold')
        c.text(560, 375, '= more blue lost', 32, BL, top * fd(T(2), 1.5), w='Bold')

RECAPS = [('1', 'Air scatters short blue waves the most', BL),
          ('2', 'Not violet: less of it, and eyes favour blue', VI),
          ('3', 'Sunset: a long path, blue scattered away', OR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 160, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; y = 320 + i * 170; dx = 40 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        c.rr(300 + dx, y - 70, 1620 + dx, y + 70, 34, CARD, m, outline=col, ow=4)
        c.circ(390 + dx, y, 42, col, m, bg=CARD); c.text(390 + dx, y, nn, 48, BG, m, w='Bold', bg=col)
        if i == 0:
            for j in range(4):
                ang = j * math.pi / 2 + t
                wave(c, 520 + dx, y, 520 + dx + 46 * math.cos(ang), y + 46 * math.sin(ang), 20, 5, BL, m, w=4, bg=CARD)
            molecule(c, 520 + dx, y, 7, m, INK, bg=CARD)
        elif i == 1:
            eye(c, 520 + dx, y, 44, m, BL, bg=CARD)
        else:
            c.circ(520 + dx, y + 14, 34, OR, m, bg=CARD); c.d.rectangle(((470 + dx) * c.k, (y + 16) * c.k, (570 + dx) * c.k, (y + 60) * c.k), fill=CARD)
            c.line([(470 + dx, y + 16), (570 + dx, y + 16)], OR, 4, m, CARD)
        c.text(600 + dx, y, lab, 46, INK, m, 'lm', 'Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Sunlight is white. Space is black.",
            "So why is the sky above you blue?",
            "And here's the strange part: violet scatters even more than blue.",
            "Let's follow one sunbeam down to your eyes, and find out."], s_hook),
 ('1  ·  WHITE LIGHT', ["Start at the Sun. Its light looks white.",
            "But it's every colour mixed. A rainbow is that light pulled apart.",
            "Each colour is a wave. Red waves are long. Blue and violet waves are short."], s_white),
 ('2  ·  SPACE', ["Next, the beam crosses space, where there's almost nothing to hit.",
            "So it flies straight past, and space looks black, even in full sunshine.",
            "The Moon has no air. So even in daytime, its sky is black."], s_space),
 ('3  ·  INTO THE AIR', ["Then the beam hits our air: tiny nitrogen and oxygen molecules, far smaller than a light wave.",
            "Picture waves at sea passing a thin post. Long swells roll past. Short ripples splash off in every direction.",
            "Air does the same to light. Short blue waves get thrown all over the sky. Long red waves mostly carry on."], s_air),
 ('4  ·  YOUR EYES', ["Halve a wave's length, and it scatters sixteen times more.",
            "So violet, at the short end, scatters about ten times more than red, at the long end.",
            "That scattered blue reaches your eyes from all over the sky. That's the blue sky.",
            "It's called Rayleigh scattering, after Lord Rayleigh's work in eighteen seventy-one."], s_much),
 ('5  ·  QUICK QUESTION', ["Quick question. If violet scatters most, why isn't the sky violet?",
            "A: sunlight has no violet. Or B: less violet arrives, and your eyes don't see it well.",
            "Three, two, one.",
            "B. Sunlight has violet, but the Sun sends less of it, and some is absorbed high up.",
            "And your eyes respond more to blue than violet. So the mix looks sky blue."], s_quiz),
 ('6  ·  SUNSET', ["In the evening, the Sun sits low, so its light crosses far more air.",
            "Along that long path, most of the blue is scattered away before it arrives.",
            "What's left is yellow, orange and red. That's a sunset.",
            "Dust and haze can make it even redder."], s_sunset),
 ('7  ·  CLOUDS', ["And clouds? Their droplets are much bigger than a light wave.",
            "Big droplets scatter all colours about equally. And all colours mixed together look white."], s_clouds),
 ('8  ·  TRY IT', ["You can see all of this at home.",
            "Stir a teaspoon of milk into water, and shine a phone light through the side. It looks slightly blue.",
            "Shine it down from the top, and the bottom looks yellow-orange. A sky and a sunset, in one glass."], s_glass),
 ('RECAP', ["So remember three things.",
            "One. Air scatters short blue waves far more than long red ones.",
            "Two. The sky isn't violet: less violet arrives, and our eyes favour blue.",
            "Three. At sunset, the long path scatters the blue away, leaving red.",
            "If this made you look up, subscribe to Short Story Long Thinking."], s_recap),
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

# The Short: its own complete mini-story; the answer (air scatters blue the most) lands by about 10 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["Sunlight is white. Space is black.",
                 "So why is the sky blue?",
                 "Because air scatters blue light far more than red."], remap(s_hook, {0: 0, 1: 1})),
 ('HOW', ["Air molecules are tiny. Long red waves mostly pass straight through them.",
          "But short blue waves get thrown all over the sky, and reach your eyes from every direction."], remap(s_air, {0: 0, 2: 1})),
 ('NOT VIOLET', ["Violet scatters even more. But the Sun sends less of it, and your eyes respond much more to blue."],
                remap(s_quiz, {0: 0, 3: (0, .1), 4: (0, 3.2)})),
 ('SUNSET', ["At sunset, light crosses far more air. The blue is scattered away, and orange and red are left."],
            remap(s_sunset, {0: 0, 1: (0, 1.6), 2: (0, 4.0)})),
 ('THE ANSWER', ["So the sky is blue because air scatters short blue waves the most.",
                 "Follow for more."],
                card('Air scatters blue the most.', 'So the sky looks blue.')),
]
SHORT_HITS = [(4, 0, 0.0)]
