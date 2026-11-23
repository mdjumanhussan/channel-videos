"""Episode: The Internet Isn't in the Sky. It's Under the Sea. (undersea cables: size, light, boosters, breaks)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'The Internet Under the Sea'                    # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.94
SHORT_HOOK = 'How does the internet cross oceans?'            # headline on the vertical Short
HITS = [(0, 1, 0.0), (5, 0, 0.0), (6, 2, 0.0)]                # "It goes down.", "It's B.", "About eighty percent come from people"
THUMB = ['YOUR INTERNET', 'IS UNDERWATER']
THUMB_COLS = [CY, YE]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
# Lesson of 2026-11-24 (TubeLab): a beat of silence BEFORE the biggest reveals (earlier videos paused after them).
PAUSES = {(0, 0): 0.9, (4, 0): 3.4, (6, 1): 0.9, (7, 0): 0.3}
SHORT_PAUSES = {(0, 0): 0.5}
QZ = 9.9                                                      # length of the quiz line (set from tl.json after audio)
CAPTION_FIXES = {'ninety-nine percent': '99%', 'five hundred': '500', '1.7 million kilometres': '1.7 million km',
                 'one hundred and fifty to two hundred': '150 to 200', 'less than one percent': 'under 1%',
                 'eighty percent': '80%', 'twenty-five years': '25 years', 'more than forty times': 'more than 40 times'}
CAPTION_FIXES = dict(sorted(CAPTION_FIXES.items(), key=lambda kv: -len(kv[0])))

# Colour code kept in every scene:
# light / the cable's data yellow, sea blue, boosters green, damage and "wrong guess" pink,
# copper orange, people / phones cyan.
LIGHT = YE; SEA = (22, 52, 104); SEA2 = (14, 34, 76); FLOOR = (70, 62, 66); BOOST = GR; HARM = PK
COPPER = (232, 140, 70); STEEL = (150, 156, 180); JACKET = (30, 32, 44); QUIZ = (46, 28, 74); DARK = (20, 22, 38)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    """3 to 6 word headline with one key word in colour (most mobile viewers watch muted)."""
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def sea(c, a, t, y0=560, y1=860, x0=60, x1=1860):
    """A slice of ocean: waves on top, a sandy floor at the bottom."""
    if a <= .01: return
    c.rr(x0, y0, x1, y1, 22, SEA, a)
    c.rr(x0, y0 + (y1 - y0) * .45, x1, y1, 22, SEA2, a, bg=SEA)
    wav = [(x, y0 + 8 * math.sin(x / 70 + t * 1.6)) for x in range(int(x0) + 10, int(x1) - 9, 20)]
    c.line(wav, (120, 180, 240), 5, a, bg=SEA)
    c.rr(x0, y1 - 34, x1, y1, 16, FLOOR, a, bg=SEA2)

def pulses(c, pts, a, t, n=7, speed=.35, r=9, col=LIGHT, bg=SEA2):
    """Light pulses travelling along a polyline."""
    if a <= .01: return
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; L = sum(seg)
    for k in range(n):
        d = ((t * speed + k / n) % 1.0) * L
        for i, s in enumerate(seg):
            if d <= s:
                q = d / max(s, 1e-6)
                x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * q; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * q
                c.circ(x, y, r * 1.9, col, a * .25, bg=bg); c.circ(x, y, r, col, a, bg=bg); break
            d -= s

def phone(c, x, y, s, a, col=CY, face=True):
    if a <= .01: return
    c.rr(x - 70 * s, y - 130 * s, x + 70 * s, y + 130 * s, 26 * s, (40, 46, 84), a, outline=col, ow=5)
    c.rr(x - 56 * s, y - 108 * s, x + 56 * s, y + 100 * s, 14 * s, (24, 30, 60), a, bg=(40, 46, 84))
    if face:
        c.circ(x, y - 20 * s, 26 * s, col, a, bg=(24, 30, 60))
        c.rr(x - 40 * s, y + 18 * s, x + 40 * s, y + 70 * s, 22 * s, col, a, bg=(24, 30, 60))

def satellite(c, x, y, s, a):
    if a <= .01: return
    c.rr(x - 120 * s, y - 26 * s, x - 40 * s, y + 26 * s, 6 * s, (70, 90, 170), a)
    c.rr(x + 40 * s, y - 26 * s, x + 120 * s, y + 26 * s, 6 * s, (70, 90, 170), a)
    c.line([(x - 40 * s, y), (x + 40 * s, y)], STEEL, 6 * s, a)
    c.rr(x - 30 * s, y - 34 * s, x + 30 * s, y + 34 * s, 10 * s, STEEL, a)

def xsec(c, x, y, r, a, glow=0.0, copper=0.0, bg=BG):
    """Cable cross-section: plastic jacket, steel wires, copper layer, a core of glass fibres."""
    if a <= .01: return
    c.circ(x, y, r, JACKET, a, bg=bg)
    for k in range(18):
        ang = 6.283 * k / 18
        c.circ(x + r * .72 * math.cos(ang), y + r * .72 * math.sin(ang), r * .11, STEEL, a, bg=JACKET)
    c.circ(x, y, r * .55, None, a, outline=mix(COPPER, .45 + .55 * copper), ow=max(3, r * .09), bg=JACKET)
    c.circ(x, y, r * .42, (16, 18, 30), a, bg=JACKET)
    for k in range(6):
        ang = 6.283 * k / 6 + .3
        c.circ(x + r * .2 * math.cos(ang), y + r * .2 * math.sin(ang), r * .07, LIGHT, a * (.55 + .45 * glow), bg=(16, 18, 30))
    if glow > .01: c.circ(x, y, r * .3, None, a * glow, outline=LIGHT, ow=3, bg=(16, 18, 30))

def booster(c, x, y, a, on=1.0, bg=SEA2):
    if a <= .01: return
    c.rr(x - 64, y - 36, x + 64, y + 36, 16, (40, 90, 80), a, bg=bg)
    c.rr(x - 64, y - 36, x + 64, y + 36, 16, None, a * (.4 + .6 * on), outline=BOOST, ow=7, bg=bg)
    c.text(x, y, '+', 50, BOOST, a * (.4 + .6 * on), w='Bold', bg=(40, 90, 80))

def ship(c, x, y, s, a, bg=SEA):
    if a <= .01: return
    poly(c, [(x - 170 * s, y - 30 * s), (x + 170 * s, y - 30 * s), (x + 130 * s, y + 30 * s), (x - 140 * s, y + 30 * s)], (210, 215, 230), a, bg)
    c.rr(x - 60 * s, y - 95 * s, x + 70 * s, y - 30 * s, 10 * s, (230, 235, 245), a, bg=bg)
    c.rr(x + 90 * s, y - 120 * s, x + 110 * s, y - 30 * s, 4 * s, (230, 235, 245), a, bg=bg)

def anchor(c, x, y, s, a, col=STEEL, bg=SEA2):
    if a <= .01: return
    c.line([(x, y - 70 * s), (x, y + 50 * s)], col, 10 * s, a, bg=bg)
    c.line([(x - 34 * s, y - 40 * s), (x + 34 * s, y - 40 * s)], col, 10 * s, a, bg=bg)
    c.line([(x - 55 * s, y + 20 * s), (x - 30 * s, y + 52 * s), (x, y + 58 * s), (x + 30 * s, y + 52 * s), (x + 55 * s, y + 20 * s)], col, 10 * s, a, bg=bg)
    c.circ(x, y - 82 * s, 14 * s, None, a, outline=col, ow=7 * s, bg=bg)

def fish(c, x, y, s, a, col=(130, 140, 170), bg=SEA2):
    """A generic shark-shaped fish facing left."""
    if a <= .01: return
    poly(c, [(x - 150 * s, y), (x - 60 * s, y - 40 * s), (x + 90 * s, y - 30 * s), (x + 150 * s, y - 70 * s), (x + 130 * s, y),
             (x + 150 * s, y + 60 * s), (x + 90 * s, y + 28 * s), (x - 60 * s, y + 38 * s)], col, a, bg)
    poly(c, [(x - 20 * s, y - 36 * s), (x + 20 * s, y - 100 * s), (x + 40 * s, y - 34 * s)], col, a, bg)
    c.circ(x - 100 * s, y - 8 * s, 7 * s, DARK, a, bg=col)

def cloud_icon(c, x, y, s, a, col=(200, 210, 235), bg=BG):
    if a <= .01: return
    for dx, dy, r in ((-60, 10, 48), (-10, -22, 64), (52, 6, 52)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)
    c.rr(x - 108 * s, y + 6 * s, x + 104 * s, y + 58 * s, 26 * s, col, a, bg=bg)

FLOOR_Y = 812
def floor_cable(x0, x1, y=FLOOR_Y, wob=10):
    return [(x, y + wob * math.sin(x / 140)) for x in range(int(x0), int(x1) + 1, 30)]

# ---------- scenes ----------
def s_hook(c, T, t):
    """Bold claim with its proof on screen from frame one: two phones, the sky route, the sea route."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Not up to ', INK), ('space', HARM)], sw_out(T, 1))
    headline(c, [('Down to ', INK), ('the sea floor', LIGHT)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('99%', LIGHT), (' goes by cable', INK)], sw_in(T, 2))
    sea(c, 1, t, y0=600, y1=860, x0=420, x1=1500)
    phone(c, 260, 600, 1.0, 1); phone(c, 1660, 600, 1.0, 1)
    # the sky route people imagine
    sat_y = 330
    sky = 1 - .65 * hl(1) - .3 * hl(2)
    satellite(c, 960, sat_y, 1.0, sky)
    for x0, x1 in ((330, 860), (1590, 1060)):
        n = 10
        for k in range(n):
            if k % 2: continue
            q0, q1 = k / n, (k + 1) / n
            c.line([(x0 + (x1 - x0) * q0, 470 + (sat_y - 470) * q0), (x0 + (x1 - x0) * q1, 470 + (sat_y - 470) * q1)], DIM, 5, sky)
    c.cross(960, sat_y, 120, HARM, (fd(T(0), 3.8) if T(0) > -.1 else 0) * (1 - hl(2)))
    # the real route: down, along the floor, up
    path = [(260, 740), (420, 740), (470, FLOOR_Y)] + floor_cable(500, 1420) + [(1450, 740), (1660, 740)]
    on = .35 + .65 * hl(1)
    c.line(path, (120, 110, 80), 12, 1)
    c.line(path, LIGHT, 6, on)
    pulses(c, path, hl(1), t, n=8, speed=.3, r=8, bg=SEA2)
    m2 = hl(2)
    if m2 > .01:
        c.rr(760, 380, 1160, 520, 34, CARD, m2, outline=LIGHT, ow=5)
        c.text(960, 440, '99%', 96, LIGHT, m2, w='Bold', bg=CARD)
        c.text(960, 560, 'of data between countries', 34, INK, m2, w='Bold', bg=SEA)

def s_map(c, T, t):
    """A simple globe filling with cable arcs; then the length; then the satellite's tiny share."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Over ', INK), ('500', LIGHT), (' cables', INK)], sw_out(T, 1))
    headline(c, [('1.7 million km', LIGHT), (' of them', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Satellites: a ', INK), ('tiny share', HARM)], sw_in(T, 2))
    X, Y, R = 620, 570, 260
    c.circ(X, Y, R, (24, 48, 100), 1)
    rng = random.Random(11)
    for blob in range(6):    # loose land shapes, not a real map
        bx, by = X + rng.uniform(-.55, .55) * R, Y + rng.uniform(-.5, .5) * R
        for _ in range(4):
            c.circ(bx + rng.uniform(-50, 50), by + rng.uniform(-35, 35), rng.uniform(30, 60), (52, 70, 86), 1, bg=(24, 48, 100))
    c.circ(X, Y, R, None, 1, outline=(70, 110, 190), ow=4)
    grow = fd(T(0), 0, 3.0) if T(0) > -.1 else 0
    n = int(34 * grow)
    rng = random.Random(5)
    for k in range(34):
        a0, a1 = rng.uniform(0, 6.283), rng.uniform(0, 6.283)
        p0 = (X + R * .92 * math.cos(a0), Y + R * .92 * math.sin(a0)); p1 = (X + R * .92 * math.cos(a1), Y + R * .92 * math.sin(a1))
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        cx, cy = X + (mx - X) * .3, Y + (my - Y) * .3
        if k < n:
            pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * cx + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * cy + u * u * p1[1]) for u in [j / 16 for j in range(17)]]
            c.line(pts, LIGHT, 3, .75, bg=(24, 48, 100))
    cnt = int(500 * grow)
    c.text(1360, 360, f'{cnt}+' if grow >= 1 else str(cnt), 120, LIGHT, 1 - hl(1) * .7, w='Bold')
    c.text(1360, 450, 'cables in service', 40, DIM, 1 - hl(1) * .7, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        c.rr(1080, 520, 1680, 700, 28, CARD, m1, outline=LIGHT, ow=4)
        c.text(1380, 585, 'about 1.7 million km', 46, LIGHT, m1, w='Bold', bg=CARD)
        c.text(1380, 645, '= 40+ times around Earth', 38, INK, m1, w='Bold', bg=CARD)
        c.text(1380, 740, 'our arithmetic: Earth is about 40,000 km round', 26, DIM, m1, w='Regular')
        loops = fd(T(1), .3, 2.0) if T(1) > -.1 else 0
        for k in range(int(6 * loops)):
            c.circ(X, Y, R + 14 + 9 * k, None, m1 * .8, outline=LIGHT, ow=3)
    m2 = hl(2)
    if m2 > .01:
        satellite(c, 1380, 560, .9, m2)
        for k, (lab, val, col) in enumerate((('cables', 1.0, LIGHT), ('satellites', .02, HARM))):
            y = 690 + k * 90
            c.text(1130, y, lab, 34, col, m2, 'rm', 'Bold')
            c.rr(1150, y - 26, 1750, y + 26, 14, CARD, m2)
            c.rr(1150, y - 26, 1150 + max(16, 600 * val * fd(T(2), .4, .8)), y + 26, 14, col, m2, bg=CARD)
        c.text(1450, 850, 'shares are illustrative', 26, DIM, m2, w='Regular')

def s_hose(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Huge? ', HARM), ('No.', INK)], sw_out(T, 1))
    headline(c, [('About a ', INK), ('garden hose', LIGHT)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Near shore: ', INK), ('steel armour', STEEL)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:
        c.circ(960, 520, 250, None, m0, outline=(70, 80, 130), ow=40)
        c.circ(960, 520, 250, None, m0 * .6, outline=DIM, ow=4)
        c.text(960, 820, 'a giant pipe?', 54, DIM, m0, w='Bold')
        c.cross(960, 520, 260, HARM, fd(T(0), 1.2) if T(0) > -.1 else 0)
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        # same width, side by side: a garden hose and a deep-sea cable
        c.rr(360, 400, 1400, 450, 25, (70, 170, 90), m1)
        c.circ(1400, 425, 25, (40, 110, 60), m1, outline=(110, 210, 130), ow=4)
        c.text(380, 360, 'garden hose', 42, (110, 210, 130), m1, 'lm', 'Bold')
        c.rr(360, 600, 1400, 650, 25, (62, 66, 92), m1, outline=(120, 126, 160), ow=3)
        xsec(c, 1400, 625, 25, m1, glow=.8)
        c.text(380, 700, 'deep-sea cable', 42, LIGHT, m1, 'lm', 'Bold')
        for y0, y1 in ((400, 450), (600, 650)):
            c.line([(1480, y0), (1530, y0)], DIM, 3, m1); c.line([(1480, y1), (1530, y1)], DIM, 3, m1)
        c.line([(1505, 450), (1505, 600)], DIM, 3, m1, ); c.text(1640, 525, 'same width', 36, DIM, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        poly(c, [(140, 560), (700, 560), (1100, 820), (140, 820)], (120, 104, 80), m2)       # the shore
        sea(c, m2, t, y0=560, y1=860, x0=700, x1=1820)
        c.line([(200, 640), (700, 680), (1100, 812), (1800, 812)], JACKET, 30, m2)
        for k in range(12):
            q = k / 11; x = 230 + q * 450; y = 642 + 38 * (x - 200) / 500
            c.line([(x - 8, y - 18), (x + 8, y + 18)], STEEL, 6, m2, bg=JACKET)
        c.line([(1100, 812), (1800, 812)], JACKET, 14, m2, bg=SEA2)
        c.text(500, 600, 'armoured here', 34, STEEL, m2, w='Bold', bg=(120, 104, 80))
        c.text(1500, 760, 'thin out here', 34, LIGHT, m2, w='Bold', bg=SEA2)
        anchor(c, 980, 380, .9, m2, bg=BG)
        c.text(980, 470, 'anchors, nets', 30, DIM, m2, w='Medium')

def s_light(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Glass as thin ', INK), ('as a hair', LIGHT)], sw_out(T, 1))
    headline(c, [('Data = ', INK), ('flashes of light', LIGHT)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('It ', INK), ('bounces', LIGHT), (' along inside', INK)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:
        xsec(c, 520, 520, 210, m0, glow=.5 + .5 * math.sin(t * 3))
        c.circ(520, 520, 92, None, m0, outline=LIGHT, ow=4)
        c.line([(612, 520), (1060, 420)], DIM, 3, m0)
        hair = [(1100 + x, 520 + 60 * math.sin(x / 120)) for x in range(0, 640, 20)]
        c.line(hair, (150, 110, 80), 8, m0)
        fib = [(1100 + x, 660 + 6 * math.sin(x / 160)) for x in range(0, 640, 20)]
        c.line(fib, LIGHT, 8, m0)
        c.text(1420, 440, 'a human hair', 34, (190, 150, 120), m0, w='Bold'); c.text(1420, 720, 'one glass fibre', 34, LIGHT, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        c.rr(220, 430, 420, 610, 22, (60, 66, 100), m1); c.text(320, 650, 'laser', 34, DIM, m1, w='Bold')
        c.rr(420, 500, 1700, 540, 20, (36, 40, 66), m1, outline=(90, 96, 140), ow=3)
        for k in range(10):
            x = 440 + ((t * 420 + k * 130) % 1240)
            on = 1 if (k * 7 + 3) % 3 else 0      # on/off pattern: 1s and 0s
            c.rr(x, 506, x + 50, 534, 10, LIGHT, m1 * (.15 + .85 * on), bg=(36, 40, 66))
        c.text(960, 640, 'on, off, on, on: a code of 1s and 0s', 38, INK, m1, w='Bold')
        c.text(960, 700, 'billions of flashes every second', 34, LIGHT, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        y0, y1 = 420, 640
        c.rr(200, y0, 1720, y1, 40, (30, 36, 64), m2, outline=(120, 140, 200), ow=6)
        zz = [(200 + k * 95, y0 + 14 if k % 2 else y1 - 14) for k in range(17)]
        c.line(zz, LIGHT, 4, m2 * .45, bg=(30, 36, 64))
        pulses(c, zz, m2, t, n=3, speed=.16, r=12, bg=(30, 36, 64))
        c.text(960, 720, 'the walls act like mirrors, so the light stays in', 36, INK, m2, w='Bold')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('How does light ', INK), ('cross an ocean', LIGHT), ('?', INK)], 1, bg=QUIZ, size=80)
    for k, txt in enumerate(('A  One giant laser', 'B  Boosters on the way')):
        u = fd(t, .8 + .3 * k)
        c.rr(300, 380 + k * 190, 1140, 510 + k * 190, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(350, 445 + k * 190, txt, 52, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    if T(0) > 0:
        e = T(0) - QZ; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), QZ - .3)
        c.circ(1460, 540, 96, LIGHT, u, bg=QUIZ); c.text(1460, 540, str(k) if k else '?', 88, DARK, u, w='Bold', bg=LIGHT)

def s_boost(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('B: ', INK), ('boosters', BOOST)], sw_out(T, 1))
    headline(c, [('Each one ', INK), ('re-brightens', BOOST), (' the light', INK)], sw_in(T, 1) * sw_out(T, 2), size=80)
    headline(c, [('Power: a ', INK), ('copper layer', COPPER)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Many colours', LIGHT), (' at once', INK)], sw_in(T, 3))
    m01 = 1 - hl(2)
    if m01 > .01:
        sea(c, m01, t, y0=420, y1=860)
        cab = floor_cable(80, 1840, y=FLOOR_Y - 20, wob=6)
        c.line(cab, JACKET, 16, m01, bg=SEA2)
        bx = (520, 960, 1400)
        for x in bx: booster(c, x, FLOOR_Y - 20, m01, on=hl(1) * (.6 + .4 * math.sin(t * 5 + x)))
        # one pulse: fades with distance, re-brightened at each booster once line 1 starts
        x = 80 + ((t * 300) % 1760)
        last = max([80] + [b for b in bx if b <= x])
        fade = clamp(1 - (x - last) / 520) if hl(1) > .5 else clamp(1 - (x - 80) / 700)
        c.circ(x, FLOOR_Y - 20, 44, LIGHT, m01 * fade * .3, bg=SEA2); c.circ(x, FLOOR_Y - 20, 22, LIGHT, m01 * max(.06, fade), bg=SEA2)
        c.text(960, 520, 'fades as it goes', 38, HARM, m01 * (1 - hl(1)), w='Bold', bg=SEA)
        c.text(960, 520, 'boosted again and again', 38, BOOST, m01 * hl(1), w='Bold', bg=SEA)
        c.text(960, 340, 'not to scale', 26, DIM, m01, w='Regular')
    m2 = hl(2) * (1 - hl(3))
    if m2 > .01:
        xsec(c, 700, 520, 260, m2, glow=.4, copper=.5 + .5 * math.sin(t * 5))
        c.line([(980, 520), (1160, 520)], COPPER, 4, m2)
        c.text(1180, 470, 'copper layer', 52, COPPER, m2, 'lm', 'Bold')
        c.text(1180, 540, 'carries electricity', 38, INK, m2, 'lm', 'Bold')
        c.text(1180, 590, 'to every booster', 38, INK, m2, 'lm', 'Bold')
        bolt = [(1580, 640), (1540, 720), (1590, 720), (1550, 800)]
        c.line(bolt, COPPER, 10, m2)
    m3 = hl(3)
    if m3 > .01:
        c.rr(200, 380, 1720, 680, 60, (30, 36, 64), m3, outline=(120, 140, 200), ow=6)
        cols = (LIGHT, (255, 120, 90), GR, CY, PU, PK)
        for k, col in enumerate(cols):
            y = 420 + k * 46
            for j in range(9):
                x = 220 + ((t * (300 + 40 * k) + j * 170 + k * 60) % 1460)
                c.rr(x, y - 10, x + 60, y + 10, 8, col, m3, bg=(30, 36, 64))
        c.text(960, 760, 'one cable: hundreds of terabits every second', 40, LIGHT, m3, w='Bold')

def s_break(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('150 to 200', HARM), (' breaks a year', INK)], sw_out(T, 1))
    headline(c, [('Sharks? ', INK), ('Under 1%', HARM)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('80%', HARM), (': anchors and nets', INK)], sw_in(T, 2))
    sea(c, 1, t, y0=330, y1=860)
    cab = floor_cable(80, 1840, y=FLOOR_Y - 20, wob=6)
    c.line(cab, JACKET, 16, 1, bg=SEA2); pulses(c, cab, .7, t, n=6, speed=.12, r=7)
    m0 = 1 - hl(1)
    if m0 > .01:
        rng = random.Random(3); n = int(12 * fd(T(0), .3, 2.5)) if T(0) > -.1 else 0
        for k in range(12):
            x = rng.uniform(180, 1740)
            if k < n:
                c.circ(x, FLOOR_Y - 20, 26, None, m0, outline=HARM, ow=6, bg=SEA2)
                c.line([(x - 10, FLOOR_Y - 34), (x + 4, FLOOR_Y - 20), (x - 6, FLOOR_Y - 6)], HARM, 5, m0, bg=SEA2)
        c.rr(700, 470, 1220, 620, 28, CARD, m0, bg=SEA)
        c.text(960, 520, 'about 3 or 4', 50, HARM, m0, w='Bold', bg=CARD); c.text(960, 580, 'every week', 36, INK, m0, w='Bold', bg=CARD)
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        fish(c, 860 + 60 * math.sin(t * .8), 560, 1.4, m1)
        c.rr(1320, 440, 1700, 620, 28, CARD, m1, bg=SEA)
        c.text(1510, 510, 'under 1%', 60, HARM, m1, w='Bold', bg=CARD); c.text(1510, 575, 'of faults', 34, INK, m1, w='Bold', bg=CARD)
        c.text(960, 880 - 20, '', 10, INK, 0)
        c.text(1510, 660, 'sharks and other fish, up to 2006', 26, DIM, m1, w='Regular', bg=SEA)
    m2 = hl(2)
    if m2 > .01:
        ship(c, 560, 360, .9, m2)
        drag = fd(T(2), .2, 2.5) if T(2) > -.1 else 0
        ax = 560 + 380 * drag
        c.line([(640, 380), (ax, FLOOR_Y - 80)], STEEL, 4, m2, bg=SEA)
        anchor(c, ax, FLOOR_Y - 60, .7, m2)
        if drag > .9:
            c.circ(ax + 40, FLOOR_Y - 20, 34, None, m2, outline=HARM, ow=7, bg=SEA2)
        # trawler net on the right
        c.line([(1400, 360), (1560, 700)], STEEL, 3, m2, bg=SEA); c.line([(1700, 360), (1640, 700)], STEEL, 3, m2, bg=SEA)
        for k in range(6):
            y = 600 + k * 20; c.line([(1530, y), (1680, y)], (160, 160, 180), 2, m2, bg=SEA2)
        for k in range(8):
            x = 1530 + k * 20; c.line([(x, 600), (x, 700)], (160, 160, 180), 2, m2, bg=SEA2)
        c.rr(1060, 420, 1360, 560, 26, CARD, m2, outline=HARM, ow=4, bg=SEA)
        c.text(1210, 470, '80%', 64, HARM, m2, w='Bold', bg=CARD); c.text(1210, 528, 'from people', 30, INK, m2, w='Bold', bg=CARD)

def s_repair(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Repair ', INK), ('ships', CY), (' fix them', INK)], sw_out(T, 1))
    headline(c, [('Days, ', INK), ('weeks', LIGHT), (', or months', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('One cable = ', INK), ('no backup', HARM)], sw_in(T, 2))
    m01 = 1 - hl(2)
    if m01 > .01:
        sea(c, m01, t, y0=380, y1=860)
        ship(c, 960 + 20 * math.sin(t * .7), 400, 1.1, m01)
        lift = fd(T(0), .5, 2.0) if T(0) > -.1 else 0
        hy = FLOOR_Y - 20 - 220 * lift
        c.line([(1010, 420), (1010, hy)], STEEL, 4, m01, bg=SEA)
        c.line([(140, FLOOR_Y - 20), (700, FLOOR_Y - 20), (1010, hy), (1320, FLOOR_Y - 20), (1780, FLOOR_Y - 20)], JACKET, 14, m01, bg=SEA2)
        c.circ(1010, hy, 22, None, m01, outline=LIGHT, ow=6, bg=SEA2)
        for k, txt in enumerate(('days', 'weeks', 'months')):
            u = (fd(T(1), .5 + .6 * k) if T(1) > -.1 else 0) * m01
            c.rr(300 + k * 520, 540, 580 + k * 520, 620, 24, CARD, u, outline=LIGHT, ow=3, bg=SEA)
            c.text(440 + k * 520, 580, txt, 44, LIGHT, u, w='Bold', bg=CARD)
    m2 = hl(2)
    if m2 > .01:
        sea(c, m2, t, y0=300, y1=860)
        poly(c, [(1240, 640), (1420, 520), (1600, 640)], (110, 120, 90), m2, SEA)       # the island
        c.circ(1420, 520, 18, (150, 150, 140), m2, bg=(110, 120, 90))
        rng = random.Random(8)
        for k in range(5):
            u = ((t * .3 + k / 5) % 1.0); c.circ(1420 + 30 * math.sin(k), 500 - 140 * u, 20 + 30 * u, (160, 160, 170), m2 * (1 - u) * .7, bg=SEA)
        c.line([(160, FLOOR_Y - 20), (1300, FLOOR_Y - 20), (1380, 640)], JACKET, 14, m2, bg=SEA2)
        c.cross(820, FLOOR_Y - 20, 70, HARM, m2 * (fd(T(2), 1.0) if T(2) > -.1 else 0))
        c.text(1420, 690, 'Tonga, 2022', 38, INK, m2, w='Bold', bg=SEA2)
        c.rr(260, 420, 900, 560, 26, CARD, m2, outline=HARM, ow=4, bg=SEA)
        c.text(580, 470, 'its only cable cut', 40, HARM, m2, w='Bold', bg=CARD)
        c.text(580, 525, 'internet lost for over a month', 32, INK, m2, w='Bold', bg=CARD)

def s_payoff(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Not in a ', INK), ('cloud', HARM)], sw_out(T, 1))
    headline(c, [('Glass threads', LIGHT), (' on the sea floor', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Built for about ', INK), ('25 years', LIGHT)], sw_in(T, 2))
    m0 = 1 - hl(1)
    cloud_icon(c, 960, 480, 1.8, m0)
    c.cross(960, 500, 280, HARM, m0 * (fd(T(0), 1.0) if T(0) > -.1 else 0))
    m12 = hl(1)
    if m12 > .01:
        sea(c, m12, t, y0=360, y1=860)
        for k in range(5):
            y = FLOOR_Y - 30 - 40 * k
            pts = floor_cable(80, 1840, y=y, wob=8 + 3 * k)
            c.line(pts, (90, 80, 50), 6, m12, bg=SEA2); pulses(c, pts, m12, t + k * .7, n=5, speed=.18 + .03 * k, r=7)
        m2 = hl(2)
        c.rr(720, 420, 1200, 560, 30, CARD, m2, outline=LIGHT, ow=5, bg=SEA)
        c.text(960, 470, 'about 25 years', 52, LIGHT, m2, w='Bold', bg=CARD); c.text(960, 528, 'per cable', 32, INK, m2, w='Bold', bg=CARD)

def s_recap(c, T, t):
    """Recap as three cable cut-ends in a row."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', LIGHT)], 1)
    items = ((1, '99%', 'under the sea', 'data between countries', LIGHT),
             (2, 'light', 'in hair-thin glass', 'with boosters on the way', BOOST),
             (3, '80%', 'anchors and nets', 'not sharks', HARM))
    for ln, big, l1, l2, col in items:
        m = hl(ln); x = 400 + (ln - 1) * 560; dy = 40 * (1 - m)
        xsec(c, x, 450 + dy, 170, m, glow=.5)
        c.circ(x, 450 + dy, 92, (16, 18, 30), m, bg=JACKET)
        c.text(x, 450 + dy, big, 62 if len(big) > 3 else 70, col, m, w='Bold', bg=(16, 18, 30))
        c.text(x, 690 + dy, l1, 42, col, m, w='Bold')
        c.text(x, 750 + dy, l2, 30, DIM, m, w='Medium')
    c.text(960, 850, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """A glowing cable cut-end over a dark sea, light pouring out of its fibres."""
    c.rr(1150, 560, 1880, 1000, 30, SEA2, 1)
    pts = floor_cable(1150, 1880, y=880, wob=10)
    c.line(pts, JACKET, 26, 1, bg=SEA2); c.line(pts, LIGHT, 8, 1, bg=JACKET)
    xsec(c, 1520, 420, 230, 1, glow=1.0)
    c.circ(1520, 420, 250, None, 1, outline=YE, ow=10)

SCENES = [
 ('THE ROUTE', ["When you video call someone in another country, your voice doesn't go up to space.",
                "It goes down. To the bottom of the sea.",
                "About ninety-nine percent of the data crossing between countries travels through cables on the ocean floor."], s_hook),
 ('THE CABLES', ["There are more than five hundred of these cables.",
                 "Together they stretch about 1.7 million kilometres. That's enough to wrap around the Earth more than forty times.",
                 "Satellites help reach remote places, but they carry only a tiny share."], s_map),
 ('THE SIZE', ["You might picture something huge. It isn't.",
               "In the deep sea, a cable is roughly as thick as a garden hose.",
               "Near the shore, where ship anchors and fishing nets reach, it gets wrapped in steel armour."], s_hose),
 ('THE LIGHT', ["Inside are strands of glass, each no thicker than a human hair.",
                "Your message becomes flashes of laser light. On, off, on. Billions of flashes every second.",
                "The light bounces along inside the glass, the way a torch beam would bounce down a tube lined with mirrors."], s_light),
 ('QUICK QUESTION', ["Quick question. Light fades as it travels. So how does it cross a whole ocean? One giant laser, or boosters along the way? Have a guess."], s_quiz),
 ('THE BOOSTERS', ["It's B.",
                   "Along the cable sit boosters. Each one makes the fading light strong again, like a relay runner taking the baton.",
                   "They're powered by electricity sent down a copper layer inside the cable itself.",
                   "And one fibre carries dozens of laser colours at once, so a single cable can move hundreds of terabits every second."], s_boost),
 ('THE BREAKS', ["These cables get damaged about one hundred and fifty to two hundred times a year.",
                 "Sharks? Hardly ever. Up to 2006, sharks and other fish caused less than one percent of faults.",
                 "About eighty percent come from people: ship anchors and fishing trawlers dragging along the seabed."], s_break),
 ('THE REPAIR', ["So special repair ships haul the broken cable up and mend it.",
                 "A fix can take days, weeks, or even months.",
                 "And if a place has only one cable, a break really hurts. In 2022, a volcano damaged Tonga's only cable, and the islands lost their internet for over a month."], s_repair),
 ('THE PAYOFF', ["So the internet isn't really in the sky, or in a cloud.",
                 "It's mostly glass threads lying on the sea floor, carrying light.",
                 "Each one built to last about twenty-five years."], s_payoff),
 ('RECAP', ["Three things to keep.",
            "One: about ninety-nine percent of data between countries runs through cables under the sea.",
            "Two: inside, hair-thin glass carries laser light, with boosters along the way.",
            "Three: most breaks come from anchors and fishing, not sharks.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_inside(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('As thick as a ', INK), ('garden hose', LIGHT)], sw_out(T, 1), size=80)
    headline(c, [('Inside: ', INK), ('flashes of light', LIGHT)], sw_in(T, 1), size=88)
    sp = hl(1)
    xsec(c, 560 - 120 * sp, 520, 170 + 60 * sp, 1, glow=.5 + .5 * sp)
    m0 = 1 - sp
    c.circ(1300, 520, 170, (70, 170, 90), m0); c.circ(1300, 520, 118, (20, 50, 30), m0, bg=(70, 170, 90))
    c.text(560, 760, 'cable', 44, LIGHT, m0, w='Bold'); c.text(1300, 760, 'garden hose', 44, (110, 210, 130), m0, w='Bold')
    c.text(930, 520, '≈', 90, INK, m0, w='Bold')
    m1 = sp
    if m1 > .01:
        c.rr(820, 500, 1820, 540, 20, (36, 40, 66), m1, outline=(90, 96, 140), ow=3)
        for k in range(8):
            x = 840 + ((t * 380 + k * 125) % 960); on = 1 if (k * 7 + 3) % 3 else 0
            c.rr(x, 506, x + 46, 534, 10, LIGHT, m1 * (.15 + .85 * on), bg=(36, 40, 66))
        c.text(1320, 620, 'hair-thin glass', 46, LIGHT, m1, w='Bold')

def short_boost(c, T, t):
    headline(c, [('Boosters', BOOST), (' keep it bright', INK)], 1, size=84)
    sea(c, 1, t, y0=380, y1=860)
    cab = floor_cable(80, 1840, y=FLOOR_Y - 20, wob=6); c.line(cab, JACKET, 16, 1, bg=SEA2)
    bx = (520, 960, 1400)
    for x in bx: booster(c, x, FLOOR_Y - 20, 1, on=.6 + .4 * math.sin(t * 5 + x))
    x = 80 + ((t * 300) % 1760); last = max([80] + [b for b in bx if b <= x]); fade = clamp(1 - (x - last) / 520)
    c.circ(x, FLOOR_Y - 20, 44, LIGHT, fade * .3, bg=SEA2); c.circ(x, FLOOR_Y - 20, 22, LIGHT, max(.06, fade), bg=SEA2)
    c.text(960, 520, 'across the whole ocean', 50, BOOST, 1, w='Bold', bg=SEA)

def short_break(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Breaks? ', INK), ('Not sharks', HARM)], sw_out(T, 1), size=88)
    headline(c, [('Anchors', HARM), (' and nets', INK)], sw_in(T, 1), size=88)
    sea(c, 1, t, y0=330, y1=860)
    cab = floor_cable(80, 1840, y=FLOOR_Y - 20, wob=6); c.line(cab, JACKET, 16, 1, bg=SEA2)
    m0 = 1 - hl(1)
    fish(c, 960 + 60 * math.sin(t * .8), 560, 1.4, m0)
    c.cross(960, 560, 200, HARM, m0 * (fd(T(0), .8) if T(0) > -.1 else 0))
    m1 = hl(1)
    ship(c, 560, 360, .9, m1)
    drag = fd(T(1), .2, 2.0) if T(1) > -.1 else 0; ax = 560 + 380 * drag
    c.line([(640, 380), (ax, FLOOR_Y - 80)], STEEL, 4, m1, bg=SEA); anchor(c, ax, FLOOR_Y - 60, .7, m1)
    c.rr(1200, 440, 1640, 600, 28, CARD, m1, outline=HARM, ow=4, bg=SEA)
    c.text(1420, 500, 'about 80%', 60, HARM, m1, w='Bold', bg=CARD); c.text(1420, 560, 'from people', 34, INK, m1, w='Bold', bg=CARD)

SHORT_SCENES = [
 ('THE ROUTE', ["Your video call to another country doesn't go through space.",
                "It goes along the bottom of the sea.",
                "About ninety-nine percent of data between countries travels through undersea cables."], s_hook),
 ('INSIDE', ["Each cable is roughly as thick as a garden hose.",
             "Inside, hair-thin glass carries your data as flashes of laser light."], short_inside),
 ('BOOSTERS', ["Boosters along the cable keep that light strong, all the way across the ocean."], short_boost),
 ('BREAKS', ["And when a cable breaks, it's hardly ever sharks.",
             "About eighty percent of damage comes from ship anchors and fishing gear."], short_break),
 ('THE ANSWER', ["So the internet isn't in the sky.",
                 "It's glass on the sea floor, carrying light."], card('Not in the sky.', 'Glass on the sea floor.')),
]
SHORT_HITS = [(4, 1, 0.0)]
