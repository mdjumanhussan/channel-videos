"""Episode: Popcorn Is a Tiny Pressure Cooker (steam in a sealed hull, 180 °C, the millisecond clock of a pop, what makes the sound, why some kernels don't pop)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Popcorn'                                      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'What makes popcorn go pop?'                    # headline on the vertical Short
HITS = [(0, 1, 0.0), (3, 0, 0.0), (6, 0, 0.0)]               # 'not the crack', the hull gives way, 'something else'
THUMB = ['STEAM', 'POPS IT.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.3, (0, 2): 0.3, (2, 3): 0.3, (3, 0): 0.3, (4, 3): 0.3, (5, 0): 3.2, (6, 0): 0.3, (7, 3): 0.3}
SHORT_PAUSES = {(0, 0): 0.2, (2, 1): 0.2}
CAPTION_FIXES = {'one hundred and eighty degrees Celsius': '180 °C', 'one hundred and eighty degrees': '180 °C',
                 'one hundred and eighty': '180', 'one seventy': '170 °C', 'one hundred degrees': '100 °C',
                 'two thousand nine hundred': '2,900', 'fourteen percent': '14%', 'forty-eight out of fifty': '48 out of 50',
                 'ten bar': '10 bar', 'about seven milliseconds': 'about 7 ms', 'about fourteen': 'about 14 ms',
                 'about twenty-one': 'about 21 ms'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the hull is orange-brown, water and steam are cyan, heat is pink, starch and the popped flake are cream,
# pressure is yellow, sound is purple, the millisecond clock is green.
HULL = (214, 128, 56); WATER = CY; HEAT = PK; STARCH = (250, 238, 205); PRESS = YE; SOUND = PU; CLOCK = GR
DARK = (20, 22, 38); QUIZ = (60, 36, 24); PAN = (52, 56, 80); BOX = (34, 40, 76)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

# Headlines of 2 to 5 words with one key word in colour (kept from 2026-11-13: most mobile viewers watch muted).
def headline(c, parts, a, size=88, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def drop_pts(x, y, r, s=1.0):
    """A kernel outline: round on top, narrowing to a blunt tip at the bottom."""
    pts = []
    for k in range(48):
        th = 6.283 * k / 48
        w = .82 * math.sin(th) * (.5 + .5 * (1 + math.cos(th)) / 2)
        pts.append((x + r * s * w, y - r * s * math.cos(th) * 1.05))
    return pts

WATER_PTS = [(random.Random(k).uniform(-.45, .45), random.Random(k + 50).uniform(-.55, .6)) for k in range(18)]
def kernel(c, x, y, r, a, cut=1.0, water=1.0, steam=0.0, crack=0.0, t=0.0, bg=BG, dry=0.0, thick=1.0):
    """A popcorn kernel. cut shows the inside (starch + water); steam makes the water dots jitter and swell."""
    if a <= .01: return
    poly(c, drop_pts(x, y, r), HULL, a, bg)
    inner = mix(STARCH, 1, HULL)
    if cut > .01:
        poly(c, drop_pts(x, y + r * .03, r, 1 - .18 * thick), (236, 214, 170), a * cut, HULL)
        n = int(len(WATER_PTS) * (1 - .8 * dry))
        for k, (u, v) in enumerate(WATER_PTS[:n]):
            jx = steam * 10 * math.sin(t * 9 + k * 1.7); jy = steam * 10 * math.cos(t * 8 + k)
            rr_ = r * (.035 + .035 * steam)
            col = WATER if steam < .5 else (200, 236, 255)
            c.circ(x + u * r * (1 - abs(v) * .3) + jx, y + v * r + jy, rr_, col, a * cut * water, bg=(236, 214, 170))
    if crack > .01:
        pts = [(x - r * .15, y - r * 1.02), (x - r * .02, y - r * .7), (x - r * .18, y - r * .45), (x + r * .02, y - r * .2)]
        n = max(2, int(len(pts) * crack + .99))
        c.line(pts[:n], DARK, max(3, int(r * .04)), a, bg=HULL)

def flake(c, x, y, r, a, p=1.0, t=0.0, bg=BG, leg=0.0):
    """A popped flake: cream foam lumps with a bit of hull left; leg stretches a lump downwards."""
    if a <= .01: return
    rnd = random.Random(3)
    for k in range(9):
        ang = 6.283 * k / 9 + rnd.uniform(-.3, .3); d = r * .55 * p
        c.circ(x + d * math.cos(ang), y + d * math.sin(ang) * .8, r * (.25 + .25 * p) * rnd.uniform(.8, 1.1), STARCH, a, bg=bg)
    c.circ(x, y, r * .45 * max(p, .4), STARCH, a, bg=bg)
    if leg > .01:
        c.rr(x - r * .22, y, x + r * .22, y + r * (.6 + 1.0 * leg), r * .2, STARCH, a, bg=bg)
    poly(c, [(x - r * .5, y + r * .1), (x - r * .1, y - r * .1), (x - r * .05, y + r * .35), (x - r * .45, y + r * .5)], HULL, a * .9, STARCH)

def pan(c, a, y=760, hot=1.0, t=0.0, x0=360, x1=1560):
    if a <= .01: return
    c.rr(x0, y, x1, y + 50, 14, PAN, a)
    c.rr(x1, y + 12, x1 + 260, y + 34, 10, (80, 60, 50), a)
    if hot > .01:
        c.rr(x0 + 20, y + 4, x1 - 20, y + 12, 4, HEAT, a * hot)
        for k in range(7):
            xx = x0 + 120 + k * (x1 - x0 - 240) / 6; p = (t * .7 + k * .3) % 1
            yy = y - 20 - p * 120
            c.line([(xx + 10 * math.sin(p * 9 + k), yy), (xx + 10 * math.sin(p * 9 + k + 1.5), yy - 30)], HEAT, 4, a * hot * (1 - p))

def gauge(c, x, y, r, level, a, lab='pressure', bg=BG, txt=None):
    """A round pressure dial; the needle sweeps from left (low) to right (high)."""
    if a <= .01: return
    c.circ(x, y, r, CARD, a, outline=(70, 80, 130), ow=5, bg=bg)
    for k in range(11):
        ang = math.radians(210 - 240 * k / 10)
        c.line([(x + r * .78 * math.cos(ang), y - r * .78 * math.sin(ang)), (x + r * .9 * math.cos(ang), y - r * .9 * math.sin(ang))], DIM, 3, a, bg=CARD)
    ang = math.radians(210 - 240 * clamp(level))
    c.line([(x, y), (x + r * .72 * math.cos(ang), y - r * .72 * math.sin(ang))], PRESS, 7, a, bg=CARD)
    c.circ(x, y, r * .1, PRESS, a, bg=CARD)
    c.text(x, y + r * .5, txt or '', int(r * .26), PRESS, a, w='Bold', bg=CARD)
    c.text(x, y + r + 40, lab, 34, PRESS, a, w='Bold', bg=bg)

def thermo(c, x, y0, y1, level, a, marks=(), bg=BG):
    """A thermometer; level 0..1 between y1 (bottom) and y0 (top)."""
    if a <= .01: return
    c.rr(x - 28, y0, x + 28, y1, 28, CARD, a, outline=(70, 80, 130), ow=4, bg=bg)
    c.circ(x, y1 + 20, 46, HEAT, a, bg=bg)
    h = (y1 - y0 - 30) * clamp(level)
    c.rr(x - 14, y1 - h, x + 14, y1 + 10, 14, HEAT, a, bg=CARD)
    for lv, lab in marks:
        yy = y1 - (y1 - y0 - 30) * lv
        c.line([(x + 34, yy), (x + 60, yy)], DIM, 3, a); c.text(x + 72, yy, lab, 32, INK, a, anchor='lm', w='Bold')

def arcs(c, x, y, a, t, n=3, r0=40, col=SOUND, side=1, bg=BG):
    """Sound: curved arcs spreading out to one side."""
    if a <= .01: return
    for k in range(n):
        rr_ = r0 + 34 * k + 18 * ((t * 2) % 1)
        pts = [(x + side * rr_ * math.cos(math.radians(d)), y + rr_ * math.sin(math.radians(d))) for d in range(-40, 41, 8)]
        c.line(pts, col, 6, a * (1 - k * .25), bg=bg)

def puff(c, x, y, a, t, n=8, spread=1.0, up=1.0, bg=BG):
    """Steam puffs drifting up and out."""
    if a <= .01: return
    for k in range(n):
        p = (t * .8 + k / n) % 1
        xx = x + spread * (k - n / 2) * 18 * p + 8 * math.sin(t * 3 + k); yy = y - up * p * 160
        c.circ(xx, yy, 12 + 20 * p, (200, 236, 255), a * (1 - p) * .8, bg=bg)

def tag(c, x, y, txt, col, a, sub=None, bg=BG, w=300):
    if a <= .01: return
    c.rr(x - w / 2, y - 50, x + w / 2, y + 50, 22, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - (12 if sub else 0), txt, 42, col, a, w='Bold', bg=CARD)
    if sub: c.text(x, y + 28, sub, 26, DIM, a, w='Bold', bg=CARD)

def msclock(c, x, y, ms, a, bg=BG):
    """The running millisecond clock (lesson applied 2026-11-17)."""
    if a <= .01: return
    c.rr(x - 190, y - 60, x + 190, y + 60, 24, DARK, a, outline=CLOCK, ow=4, bg=bg)
    c.text(x, y, f'{ms:4.1f} ms', 64, CLOCK, a, w='Bold', bg=DARK)

def timeline(c, ms, a, marks, y=820, x0=360, x1=1560, maxms=21.0):
    if a <= .01: return
    c.rr(x0, y - 8, x1, y + 8, 8, CARD, a)
    c.rr(x0, y - 8, x0 + (x1 - x0) * clamp(ms / maxms), y + 8, 8, CLOCK, a, bg=CARD)
    for m, lab, on in marks:
        xx = x0 + (x1 - x0) * m / maxms
        c.circ(xx, y, 16, CLOCK if ms >= m - .05 else CARD, a, outline=CLOCK, ow=3)
        c.text(xx, y + 44, lab, 28, INK if ms >= m - .05 else DIM, a * on, w='Bold')

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: a surprising true statement, with the kernel already heating from frame one."""
    hl = lambda i: hl_(T, i)
    headline(c, [('A tiny ', INK), ('pressure cooker', PRESS)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Not the ', INK), ('crack', HULL)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('In ', INK), ('1/50', CLOCK), (' of a second', INK)], sw_in(T, 2))
    m1 = hl(1); m2 = hl(2)
    pan(c, 1, hot=1, t=t)
    lvl = .25 + .6 * fd(t, 0, 3.5)
    kernel(c, 720, 500, 200, 1 - m1, steam=.6 + .4 * math.sin(t * 3) ** 2, t=t)
    gauge(c, 1300, 470, 150, lvl + .03 * math.sin(t * 7), 1 - m1)
    if m1 > .01:
        flake(c, 720, 520, 170, m1, p=fd(T(1), 0, .4), t=t)
        puff(c, 720, 380, m1, t)
        arcs(c, 900, 420, m1 * (1 - m2 * .6), t)
        tag(c, 1320, 400, 'shell cracking', HULL, m1, w=380); c.cross(1560, 400, 34, PK, m1)
        tag(c, 1320, 600, 'escaping steam', SOUND, m1, w=380); c.circ(1560, 600, 34, GR, m1); c.check(1560, 600, 28, DARK, m1)
    timeline(c, 20.7 * fd(T(2), .3, 2.0), m2, [(0, '0', 1), (20.7, '21 ms', 1)], y=860)


def s_inside(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Three ', INK), ('parts', HULL)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('A tough ', INK), ('hull', HULL)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Starch', STARCH), (' + ', INK), ('water', WATER)], sw_in(T, 2))
    m1 = hl(1); m2 = hl(2)
    cut = fd(T(0), .3, .8)
    kernel(c, 960, 520, 300, 1, cut=cut, water=fd(T(2), .8, .6), t=t)
    if m1 > .01:
        for k in range(5):
            p = (t * .6 + k * .2) % 1; yy = 330 + k * 80
            c.line([(560 - 140 * (1 - p), yy), (560 - 140 * (1 - p) + 60, yy)], (200, 236, 255), 5, m1 * (1 - m2) * (.4 + .6 * p))
        c.cross(560, 520, 30, PK, m1 * (1 - m2))
        tag(c, 400, 760, 'hull', HULL, m1, sub='steam barely gets through', w=440)
    if m2 > .01:
        tag(c, 1500, 380, 'starch', (236, 214, 170), m2, w=300)
        tag(c, 1500, 640, 'water', WATER, m2, sub='about 14% of the kernel', w=400)
        c.line([(1350, 380), (1080, 450)], DIM, 3, m2); c.line([(1300, 640), (1060, 600)], DIM, 3, m2)

def s_heat(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Add ', INK), ('heat', HEAT)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Water', WATER), (' to ', INK), ('steam', (200, 236, 255))], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Pressure', PRESS), (' climbs', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('About ', INK), ('10 bar', PRESS)], sw_in(T, 3))
    m1 = hl(1); m2 = hl(2); m3 = hl(3)
    heat = fd(T(0), .8, 1.0)
    pan(c, 1, hot=heat, t=t, x0=300, x1=1100)
    kernel(c, 700, 500, 200, 1, steam=m1, t=t)
    thermo(c, 1240, 300, 680, .2 + .3 * heat + .25 * fd(T(1), 0, 1.5) + .1 * m2, 1 - m3, marks=((.55, '100 °C'),))
    if m2 > .01:
        lvl = .1 + .75 * fd(T(2), 0, 2.5)
        gauge(c, 1620, 470, 150, lvl + .02 * math.sin(t * 9), m2 * (1 - m3), txt='')
        c.text(1620, 760, 'like a locked pressure cooker', 30, DIM, m2 * (1 - m3), w='Bold')
    if m3 > .01:
        c.rr(1150, 300, 1800, 760, 26, CARD, m3 * .95)
        for k, (lab, v, col) in enumerate((('the air around you', 1, DIM), ('inside the kernel', 10, PRESS))):
            x = 1320 + k * 320; hh = 34 * v * fd(T(3), .2 + .3 * k, .7)
            c.rr(x - 90, 680 - hh, x + 90, 680, 14, col, m3, bg=CARD)
            c.text(x, 680 - hh - 34, f'{v} bar', 38, col, m3 * fd(T(3), .5 + .3 * k), w='Bold', bg=CARD)
            c.text(x, 720, lab, 28, col, m3, w='Bold', bg=CARD)
        c.text(1475, 840, 'Virot & Ponomarenko, 2015 (estimate)', 26, DIM, m3, w='Regular')

def s_burst(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('180 °C', HEAT), (': it bursts', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('170 °C', INK), (' vs ', DIM), ('180 °C', HEAT)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Big or small: ', INK), ('180', HEAT)], sw_in(T, 2))
    m0 = 1 - hl(1); m1 = hl(1) * (1 - hl(2)); m2 = hl(2)
    if m0 > .01:
        lv = .55 + .37 * fd(T(0), 0, 1.4)
        thermo(c, 430, 300, 720, lv, m0, marks=((.55, '100 °C'), (.92, '180 °C')))
        b = fd(T(0), 1.4, .25)
        kernel(c, 1100, 520, 220, m0 * (1 - b), steam=1, crack=fd(T(0), .9, .5), t=t)
        flake(c, 1100, 520, 210, m0 * b, p=b, t=t)
    if m1 > .01:
        for g, (temp, n, x0) in enumerate((('170 °C', 17, 300), ('180 °C', 48, 1020))):
            c.rr(x0 - 20, 290, x0 + 620, 760, 26, CARD, m1 * .95)
            for k in range(50):
                xx = x0 + 40 + (k % 10) * 60; yy = 340 + (k // 10) * 70
                on = k < n and fd(T(1), .3 + .4 * g + k * .012) > .5
                if on: c.circ(xx, yy, 24, STARCH, m1, bg=CARD)
                else: poly(c, drop_pts(xx, yy, 20), HULL, m1, CARD)
            c.text(x0 + 300, 720, f'{temp}: {n} of 50 popped', 36, HEAT if g else INK, m1, w='Bold', bg=CARD)
        c.text(960, 840, 'Oven tests, 50 kernels each (Virot & Ponomarenko, 2015)', 28, DIM, m1, w='Regular')
    if m2 > .01:
        for k, (x, r) in enumerate(((560, 110), (960, 160), (1380, 85))):
            b = fd(T(2), .5 + .25 * k, .4)
            kernel(c, x, 500, r, m2 * (1 - b), cut=0)
            flake(c, x, 500, r, m2 * b, p=b, t=t)
            tag(c, x, 760, '≈180 °C', HEAT, m2 * b, w=240)

def s_clock(c, T, t):
    """Four moments of a pop on a running millisecond clock (lesson applied 2026-11-17)."""
    hl = lambda i: hl_(T, i)
    stages = [0.0, 6.9, 13.8, 20.7]
    st = max([i for i in range(4) if T(i) > -.1], default=0)
    prev = stages[st - 1] if st else 0.0
    ms = prev + (stages[st] - prev) * fd(T(st), 0, .8)
    headline(c, [('2,900', CLOCK), (' frames a second', INK)], sw_out(T, 1))
    headline(c, [('Starch ', STARCH), ('foams', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('A ', INK), ('leg', STARCH), (' pushes', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('It ', INK), ('jumps', CLOCK)], sw_in(T, 3))
    msclock(c, 1560, 330, ms, 1)
    pan(c, 1, y=700, hot=.6, t=t, x0=300, x1=1300)
    m1 = hl(1); m2 = hl(2); m3 = hl(3)
    if st == 0:
        kernel(c, 800, 560, 130, 1, steam=1, crack=fd(T(0), 1.5, .6), t=t)
        c.rr(1440, 520, 1680, 640, 18, (70, 74, 96), 1); c.circ(1560, 580, 40, DARK, 1, bg=(70, 74, 96)); c.circ(1560, 580, 22, CY, 1, bg=DARK)
        c.rr(1500, 496, 1560, 520, 6, (70, 74, 96), 1); c.text(1560, 690, 'high-speed camera', 30, DIM, 1, w='Bold')
    elif st == 1:
        p = fd(T(1), 0, .8)
        kernel(c, 800, 560, 130, 1 - p * .7, steam=1, crack=1, t=t)
        flake(c, 800, 520, 130, .3 + .7 * p, p=p, t=t)
        puff(c, 800, 440, 1, t, n=6)
    elif st == 2:
        lg = fd(T(2), 0, .8)
        flake(c, 800, 470 + 40 * (1 - lg), 130, 1, p=1, t=t, leg=lg)
        c.arrow(990, 520, 990, 660, STARCH, 5, lg)
        c.text(1010, 590, 'pushed onto the pan', 30, STARCH, lg, anchor='lm', w='Bold')
    else:
        j = fd(T(3), 0, .9)
        x = 800 + 220 * j; y = 470 - 120 * math.sin(math.pi * .5 * j)
        flake(c, x, y, 120, 1, p=1, t=t, leg=1 - j)
        pts = [(800 + 220 * u / 10, 470 - 120 * math.sin(math.pi * .5 * u / 10)) for u in range(int(10 * j) + 1)]
        if len(pts) > 1: c.line(pts, CLOCK, 4, .6)
        c.text(1560, 520, 'a few millimetres', 32, INK, fd(T(3), .6), w='Bold')
        c.text(1560, 570, 'to several centimetres', 32, INK, fd(T(3), .6), w='Bold')
    timeline(c, ms, 1, [(6.9, 'starch', 1), (13.8, 'leg', 1), (20.7, 'jump', 1)], y=800, x0=300, x1=1500)

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a warm pattern-interrupt background (lesson of 2026-10-13)."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('What makes the ', INK), ('pop', SOUND), ('?', INK)], 1, bg=QUIZ)
    for k, (lab, col) in enumerate((('A: the shell cracking', HULL), ('B: something else', SOUND))):
        x = 560 + k * 800
        c.rr(x - 330, 330, x + 330, 680, 30, CARD, 1, outline=col, ow=5, bg=QUIZ)
        if k == 0:
            kernel(c, x, 470, 90, 1, cut=0, crack=1, bg=CARD)
        else:
            c.text(x, 470, '?', 140, SOUND, 1, w='Bold', bg=CARD)
        c.text(x, 620, lab, 40, col, 1, w='Bold', bg=CARD)
    if T(0) > 0:
        e = T(0) - 5.2; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 5.0)
        c.circ(960, 790, 60, PRESS, u, bg=QUIZ); c.text(960, 790, str(k) if k else '?', 60, DARK, u, w='Bold', bg=PRESS)

def s_sound(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Most cracks: ', HULL), ('silent', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('The pop: ', SOUND), ('steam out', (200, 236, 255))], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Hollows ', INK), ('ring', SOUND)], sw_in(T, 2))
    m0 = 1 - hl(1); m1 = hl(1) * (1 - hl(2)); m2 = hl(2)
    if m0 > .01:
        for k, x in enumerate((520, 960, 1400)):
            kernel(c, x, 500, 120, m0, cut=0, crack=fd(T(0), .3 + .3 * k, .4))
            tag(c, x, 720, 'no sound', DIM, m0 * fd(T(0), .5 + .3 * k), w=240)
    if m1 > .01:
        c.rr(300, 300, 1620, 760, 26, CARD, m1 * .95)
        c.line([(360, 560), (1560, 560)], DIM, 3, m1, bg=CARD)
        xc = 640; xp = xc + 6 * 90
        c.line([(xc, 360), (xc, 700)], HULL, 6, m1 * fd(T(1), .2), bg=CARD); c.text(xc, 730, 'crack', 32, HULL, m1 * fd(T(1), .2), w='Bold', bg=CARD)
        wv = fd(T(1), 1.2, .6)
        pts = []
        for i in range(200):
            xx = xp + i * 2.0; env = math.exp(-i / 60)
            pts.append((xx, 560 - 150 * env * math.sin(i * .7) * wv))
        c.line(pts, SOUND, 4, m1, bg=CARD)
        c.text(xp + 300, 730, 'pop', 32, SOUND, m1 * wv, w='Bold', bg=CARD)
        c.arrow(xc + 10, 340, xp - 10, 340, INK, 4, m1 * wv); c.text((xc + xp) / 2, 315, '6 ms', 30, INK, m1 * wv, w='Bold', bg=CARD)
        c.text(960, 840, 'Crack and sound timing, Virot & Ponomarenko 2015', 28, DIM, m1, w='Regular')
    if m2 > .01:
        kernel(c, 700, 520, 220, m2, cut=1, water=0, crack=1)
        for k, (u, v) in enumerate(((-.2, -.3), (.15, 0), (-.1, .35))):
            c.circ(700 + u * 220, 520 + v * 220, 30, DARK, m2, bg=(236, 214, 170))
            arcs(c, 700 + u * 220 + 30, 520 + v * 220, m2, t + k * .3, n=2, r0=20, bg=(236, 214, 170))
        puff(c, 690, 330, m2, t, n=5, up=.2)
        # bottle comparison
        c.rr(1340, 420, 1460, 720, 30, (70, 140, 120), m2); c.rr(1370, 330, 1430, 430, 12, (70, 140, 120), m2)
        c.line([(1270, 320), (1390, 320)], (200, 236, 255), 5, m2)
        arcs(c, 1480, 380, m2, t, n=2, r0=30)
        c.text(1400, 780, 'like blowing over a bottle', 32, DIM, m2, w='Bold')
        c.text(1400, 820, '(a comparison)', 28, DIM, m2, w='Regular')

def s_duds(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('The ', INK), ('duds', HULL)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Cracked', HULL), (' = leak', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Too ', INK), ('dry', WATER)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('A ', INK), ('tougher', HULL), (' hull', INK)], sw_in(T, 3))
    m0 = 1 - hl(1); m1 = hl(1) * (1 - hl(2)); m2 = hl(2) * (1 - hl(3)); m3 = hl(3)
    if m0 > .01:
        c.d.pieslice([(560 * c.k, 200 * c.k), (1360 * c.k, 800 * c.k)], 0, 180, fill=mix((70, 90, 160), m0))
        for k in range(14):
            rnd = random.Random(k); flake(c, 640 + k * 48 + rnd.uniform(-20, 20), 500 - 60 * (k % 3), 60, m0, p=1, bg=(70, 90, 160))
        for k, x in enumerate((820, 960, 1100)):
            kernel(c, x, 690, 40, m0, cut=0, bg=(70, 90, 160))
        c.text(960, 850, 'some never pop', 36, INK, m0, w='Bold')
    if m1 > .01:
        kernel(c, 760, 520, 210, m1, steam=1, crack=1, t=t)
        for k in range(4):
            p = (t * .5 + k * .25) % 1
            c.circ(745 + 20 * math.sin(t + k), 300 - 100 * p, 8 + 8 * p, (200, 236, 255), m1 * (1 - p))
        gauge(c, 1350, 480, 150, .15 + .03 * math.sin(t * 4), m1, txt='')
        c.text(1350, 760, 'no pressure, no pop', 36, PRESS, m1, w='Bold')
    if m2 > .01:
        kernel(c, 760, 520, 210, m2, dry=1, t=t)
        tag(c, 1350, 420, 'too little water', WATER, m2, w=420)
        gauge(c, 1350, 620, 100, .2, m2, lab='', txt='')
    if m3 > .01:
        kernel(c, 620, 500, 190, m3, water=1, thick=2.0)
        kernel(c, 1300, 500, 190, m3, water=1, thick=.25)
        c.text(620, 780, 'popcorn: tough, tight hull', 34, HULL, m3, w='Bold')
        c.text(1300, 780, 'most other corn', 34, DIM, m3, w='Bold')

def s_recap(c, T, t):
    """Recap as three tall side-by-side cards, each with a small drawing."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', PRESS)], 1)
    items = ((1, ['A sealed shell', 'with water inside'], HULL), (2, ['Steam builds;', 'it bursts near 180 °C'], HEAT),
             (3, ['The pop is steam', 'escaping, not the crack'], SOUND))
    for ln, txt, col in items:
        m = hl(ln); x = 400 + (ln - 1) * 560; dy = 50 * (1 - m)
        c.rr(x - 250, 280 + dy, x + 250, 800 + dy, 30, CARD, m, outline=col, ow=4)
        c.circ(x, 340 + dy, 40, col, m, bg=CARD); c.text(x, 340 + dy, str(ln), 46, DARK, m, w='Bold', bg=col)
        if ln == 1: kernel(c, x, 520 + dy, 110, m, bg=CARD)
        elif ln == 2: thermo(c, x, 400 + dy, 580 + dy, .9, m, bg=CARD)
        else:
            flake(c, x - 40, 530 + dy, 80, m, bg=CARD); arcs(c, x + 50, 520 + dy, m, t, bg=CARD)
        for j, s in enumerate(txt):
            c.text(x, 700 + dy + j * 46, s, 34, INK, m, w='Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    flake(c, 1560, 420, 230, 1, p=1)
    puff(c, 1560, 250, 1, 0.3, n=8)
    arcs(c, 1790, 420, 1, 0.2)
    kernel(c, 1300, 700, 90, 1, cut=0, crack=1)

SCENES = [
 ('THE KERNEL', ["Every popcorn kernel is a tiny pressure cooker.",
                 "And the pop you hear isn't the shell cracking.",
                 "Here's what happens inside, in about one fiftieth of a second."], s_hook),
 ('INSIDE', ["A kernel has three simple parts.",
             "A hard, shiny shell, called the hull. Steam can barely get through it.",
             "Inside is starch, like a packed cupboard of flour. And a little water, about fourteen percent of the kernel."], s_inside),
 ('THE HEAT', ["Now heat it in a pan.",
               "Past one hundred degrees, the water turns to steam. But the hull holds it in.",
               "So the pressure climbs, just like a pressure cooker with the lid locked.",
               "Researchers estimate it reaches about ten bar. That's about ten times the push of the air around you."], s_heat),
 ('THE BURST', ["Then, at about one hundred and eighty degrees Celsius, the hull gives way.",
                "In oven tests by two French physicists, only seventeen kernels out of fifty popped at one seventy. At one eighty, forty-eight out of fifty did.",
                "Big kernel or small, they burst at almost the same temperature."], s_burst),
 ('THE CLOCK', ["They filmed it with a camera taking two thousand nine hundred frames a second. Watch the clock.",
                "At about seven milliseconds, the soft starch bursts out of the crack, and the steam puffs it into foam.",
                "At about fourteen, a leg of starch pushes down on the hot pan.",
                "At about twenty-one, the leg springs back, and the popcorn jumps. Like a gymnast pushing off the floor."], s_clock),
 ('QUICK QUESTION', ["Quick question. What makes the pop sound? The shell cracking, or something else?"], s_quiz),
 ('THE SOUND', ["Something else. In their recordings, most cracks made no sound at all.",
                "The pop came about six milliseconds after the crack, as the trapped steam rushed out.",
                "Their best explanation: the sudden drop in pressure makes the little hollows inside ring, a bit like blowing over a bottle."], s_sound),
 ('THE DUDS', ["So why do some kernels never pop?",
               "If the hull is cracked, the steam leaks out slowly, like air from a punctured tyre. No pressure, no pop.",
               "And a kernel that has dried out has too little water to build the pressure.",
               "It's also why ordinary corn won't pop like this. Popcorn is a special kind, with a tougher, tighter hull."], s_duds),
 ('RECAP', ["Three things to keep.",
            "One: a popcorn kernel is a sealed shell with a little water inside.",
            "Two: heat turns that water to steam, and at about one hundred and eighty degrees the hull bursts.",
            "Three: the pop you hear is the steam escaping, not the shell cracking.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('Not the ', INK), ('crack', HULL)], 1, size=96)
    pan(c, 1, hot=1, t=t)
    b = fd(t, 1.2, .5)
    kernel(c, 760, 500, 190, 1 - b, steam=1, crack=fd(t, .6, .5), t=t)
    flake(c, 760, 520, 170, b, p=b, t=t); puff(c, 760, 380, b, t); arcs(c, 940, 420, b, t)
    tag(c, 1360, 400, 'shell cracking', HULL, 1, w=380); c.cross(1600, 400, 34, PK, 1)
    tag(c, 1360, 600, '?', SOUND, 1, w=380)

SHORT_SCENES = [
 ('THE POP', ["The pop you hear from popcorn isn't the shell cracking.",
              "It's something hiding inside."], short_hook),
 ('THE HEAT', ["Every kernel holds a little water, sealed inside a tough shell.",
               "Heat it, and the water turns to steam. But the shell holds it in.",
               "So the pressure climbs, like a pressure cooker with the lid locked."], s_heat),
 ('THE SOUND', ["At about one hundred and eighty degrees, the shell bursts. But in high-speed recordings, most cracks made no sound.",
                "The pop came a few milliseconds later, as the trapped steam rushed out.",
                "The sudden drop in pressure makes the hollows inside ring, like blowing over a bottle."], s_sound),
 ('THE ANSWER', ["So the pop isn't the shell.", "It's the steam escaping."], card('Not the shell.', 'Escaping steam.')),
]
SHORT_HITS = [(3, 0, 0.0)]
