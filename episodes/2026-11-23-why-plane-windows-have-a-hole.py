"""Episode: Why Plane Windows Have a Tiny Hole (three panes, the breather hole, the spare pane, and the fog)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'The Tiny Hole in Plane Windows'                # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.94
SHORT_HOOK = 'Why do plane windows have a hole?'              # headline on the vertical Short
HITS = [(0, 1, 0.0), (3, 3, 0.2), (5, 0, 0.0)]                # "It isn't.", outer pane takes the load, "It keeps a spare."
THUMB = ['WHY THE', 'TINY HOLE?']
THUMB_COLS = [CY, YE]                                         # no white text (lesson of 2026-11-23, vidIQ)
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.4, (0, 1): 0.3, (3, 2): 0.3, (4, 0): 3.4, (5, 0): 0.5, (7, 0): 0.3}
SHORT_PAUSES = {(0, 0): 0.2}
CAPTION_FIXES = {'thirty-five thousand feet': '35,000 feet', 'seven thousand feet': '7,000 feet',
                 'seven-thirty-seven': '737', 'one and a half times': '1.5 times', 'half a kilo': 'half a kilo'}
CAPTION_FIXES = dict(sorted(CAPTION_FIXES.items(), key=lambda kv: -len(kv[0])))

# Colour code kept in every scene:
# outer pane (takes the load) cyan, middle pane (the spare) green, inner scratch pane grey,
# cabin air pressure pink, the hole yellow, moisture violet.
OUT_P = CY; MID_P = GR; IN_P = (120, 128, 168); PRES = PK; HOLE = YE; WET = PU
DARK = (20, 22, 38); QUIZ = (46, 28, 74); SKY = (70, 130, 215); CLOUD = (226, 236, 252)
BEZEL = (196, 202, 222); WALL = (40, 46, 84)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    """3 to 7 word headline with one key word in colour (most mobile viewers watch muted)."""
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def cloud(c, x, y, s, a, bg=SKY):
    for dx, dy, r in ((-40, 6, 26), (-8, -10, 34), (30, 4, 28), (0, 14, 30)):
        c.circ(x + dx * s, y + dy * s, r * s, CLOUD, a, bg=bg)

def window(c, x, y, s, a, t, hole=1.0, fog=0.0, bg=BG):
    """Front view of a cabin window: bezel, sky with drifting clouds, the tiny hole near the bottom."""
    if a <= .01: return
    w, h = 150 * s, 205 * s
    c.rr(x - w - 34 * s, y - h - 34 * s, x + w + 34 * s, y + h + 34 * s, 150 * s, BEZEL, a, bg=bg)
    c.rr(x - w, y - h, x + w, y + h, 125 * s, SKY, a, bg=BEZEL)
    for k, (yy, sp, off) in enumerate(((-.45, 14, 0), (.05, 9, .4), (.4, 12, .75))):
        u = ((t * sp / (2 * w) + off) % 1.0)
        cx = x - w * .55 + u * w * 1.1; e = min(1, u / .15, (1 - u) / .15)
        cloud(c, cx, y + yy * h, s * .9, a * e)
    if fog > .01: c.rr(x - w, y - h, x + w, y + h, 125 * s, (214, 222, 240), a * fog * .85, bg=SKY)
    hx, hy = x, y + h * .74
    if hole > .01:
        pr = (t * 1.2) % 1.0
        c.circ(hx, hy, (10 + 46 * pr) * s, None, a * hole * (1 - pr), outline=HOLE, ow=5)
    c.circ(hx, hy, 7 * s, (18, 22, 40), a, bg=SKY)

PX = {'outer': 760, 'mid': 900, 'inner': 1040}; PY0, PY1, HY = 290, 770, 712

def outside(c, a, t, bg=BG):
    """The sky side of the cross-section, with sparse air dots."""
    if a <= .01: return
    c.rr(250, PY0 - 20, PX['outer'] - 14, PY1 + 20, 26, (18, 26, 58), a)
    rng = random.Random(4)
    for _ in range(14):
        x, y = rng.uniform(280, 720), rng.uniform(PY0 + 10, PY1 - 10)
        c.circ(x + 6 * math.sin(t + y), y, 5, (110, 130, 190), a * .8, bg=(18, 26, 58))
    c.text(495, PY1 + 50, 'outside: thin air', 34, DIM, a, w='Bold')

def cabin(c, a, t, x0=1068, x1=1660, label=True):
    if a <= .01: return
    c.rr(x0, PY0 - 20, x1, PY1 + 20, 26, WALL, a)
    rng = random.Random(9)
    for _ in range(48):
        x, y = rng.uniform(x0 + 20, x1 - 20), rng.uniform(PY0 + 10, PY1 - 10)
        c.circ(x + 5 * math.sin(t * 1.3 + y), y, 5, (230, 130, 170), a * .75, bg=WALL)
    if label: c.text((x0 + x1) / 2, PY1 + 50, 'cabin air', 34, PRES, a, w='Bold')

def pane(c, key, a, col, glow=0.0, hole=False, wdt=26, crack=0.0):
    if a <= .01: return
    x = PX[key]
    if glow > .01: c.rr(x - wdt / 2 - 12, PY0 - 12, x + wdt / 2 + 12, PY1 + 12, 18, None, a * glow, outline=col, ow=6)
    if hole:
        c.rr(x - wdt / 2, PY0, x + wdt / 2, HY - 14, 8, col, a); c.rr(x - wdt / 2, HY + 14, x + wdt / 2, PY1, 8, col, a)
    else:
        c.rr(x - wdt / 2, PY0, x + wdt / 2, PY1, 8, col, a)
    if crack > .01:
        pts = [(x - 4, PY0 + 60), (x + 10, PY0 + 140), (x - 12, PY0 + 220), (x + 8, PY0 + 300), (x - 10, PY0 + 380)]
        n = 1 + int(4 * clamp(crack)); c.line(pts[:n + 1], PRES, 7, a)

def hole_ring(c, a, t):
    if a <= .01: return
    pr = (t * 1.2) % 1.0
    c.circ(PX['mid'], HY, 16 + 40 * pr, None, a * (1 - pr), outline=HOLE, ow=5)
    c.circ(PX['mid'], HY, 12, HOLE, a)

def push(c, x0, x1, ys, a, col=PRES, w=7, head=20):
    for y in ys: c.arrow(x0, y, x1, y, col, w, a, head)

def flow(c, a, t, n=16):
    """Cabin air dots squeezing through the hole into the gap."""
    if a <= .01: return
    for k in range(n):
        ph = (t * .35 + k / n) % 1.0
        if ph < .55:
            q = ph / .55; x, y = 1060 - q * (1060 - PX['mid']), HY
        else:
            q = (ph - .55) / .45; x = PX['mid'] - 20 - q * 70; y = HY - q * 400 * ((k % 4) + 1) / 4
        c.circ(x, y, 7, (240, 140, 180), a * min(1, (1 - ph) / .1, ph / .05))

def plane(c, x, y, s, a, col=INK, bg=BG):
    """A simple side-on airliner silhouette facing right."""
    if a <= .01: return
    c.rr(x - 150 * s, y - 22 * s, x + 150 * s, y + 22 * s, 22 * s, col, a, bg=bg)
    poly(c, [(x + 130 * s, y - 22 * s), (x + 175 * s, y), (x + 130 * s, y + 22 * s)], col, a, bg)
    poly(c, [(x - 20 * s, y), (x + 40 * s, y), (x - 50 * s, y + 80 * s), (x - 85 * s, y + 80 * s)], col, a, bg)
    poly(c, [(x - 150 * s, y - 10 * s), (x - 115 * s, y - 10 * s), (x - 150 * s, y - 80 * s), (x - 172 * s, y - 80 * s)], col, a, bg)
    for k in range(7): c.circ(x - 90 * s + k * 30 * s, y - 4 * s, 5 * s, SKY, a, bg=col)

def tyre(c, x, y, r, a, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, (34, 36, 52), a, bg=bg)
    for k in range(16):
        ang = 6.283 * k / 16
        c.line([(x + r * .82 * math.cos(ang), y + r * .82 * math.sin(ang)), (x + r * .98 * math.cos(ang), y + r * .98 * math.sin(ang))], (70, 74, 100), 6, a, bg=bg)
    c.circ(x, y, r * .55, (150, 156, 180), a, bg=(34, 36, 52)); c.circ(x, y, r * .18, (60, 64, 90), a, bg=(150, 156, 180))

def drop(c, x, y, r, a, bg=BG):
    if a <= .01: return
    poly(c, [(x, y - r * 1.8), (x - r * .9, y - r * .3), (x + r * .9, y - r * .3)], WET, a, bg)
    c.circ(x, y, r, WET, a, bg=bg)

# ---------- scenes ----------
def s_hook(c, T, t):
    """A look-at-this callout: the window and its pulsing hole are on screen from frame one."""
    hl = lambda i: hl_(T, i)
    headline(c, [('See the ', INK), ('tiny hole', HOLE), ('?', INK)], sw_out(T, 1))
    headline(c, [('A flaw? ', PRES), ('No.', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('It has a ', INK), ('job', HOLE)], sw_in(T, 2))
    window(c, 700, 560, 1.25, 1, t)
    # a magnifier on the hole, from frame one
    hx, hy = 700, 560 + 205 * 1.25 * .74
    c.line([(hx + 30, hy - 10), (1180, 520)], (90, 100, 150), 4, 1)
    c.circ(1390, 520, 210, BEZEL, 1); c.circ(1390, 520, 192, SKY, 1, bg=BEZEL)
    c.circ(1390, 520, 34, (18, 22, 40), 1, bg=SKY)
    pr = (t * 1.2) % 1.0
    c.circ(1390, 520, 46 + 110 * pr, None, 1 - pr, outline=HOLE, ow=7, bg=SKY)
    m1 = hl(1) * (1 - hl(2)); c.cross(1390, 520, 150, PRES, m1)
    m2 = hl(2); c.check(1390, 520, 120, GR, m2, fd(T(2), .2, .6) if T(2) > -.1 else 0)

def s_panes(c, T, t):
    """Exploded view: the window splits into three panes."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Not one sheet: ', INK), ('three panes', HOLE)], sw_out(T, 1))
    headline(c, [('Outer', OUT_P), (' + ', INK), ('middle (hole)', MID_P)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Inner: a ', INK), ('scratch shield', IN_P)], sw_in(T, 2))
    sp = fd(T(0), .8, 1.2) if T(0) > -.1 else 0.0
    X, Y, w, h, r = 660, 540, 150, 205, 125
    win_a = 1 - sp
    window(c, X, Y, 1, win_a, t)
    layers = (('outer', OUT_P, 1, 'OUTER', 'faces the sky'), ('mid', MID_P, 0, 'MIDDLE', 'has the hole'), ('inner', IN_P, -1, 'INNER', 'you touch this'))
    for key, col, k, name, sub in layers:
        dx, dy = 150 * k * sp, -70 * k * sp
        em = 1.0
        if T(1) > -.1 and key == 'inner': em = 1 - .6 * hl(1) * (1 - hl(2))
        if T(2) > -.1 and key != 'inner': em = 1 - .6 * hl(2)
        u = sp * em
        if key == 'outer': c.rr(X + dx - w, Y + dy - h, X + dx + w, Y + dy + h, r, (30, 52, 96), sp)
        c.rr(X + dx - w, Y + dy - h, X + dx + w, Y + dy + h, r, None, u, outline=col, ow=8)
        if key == 'mid':
            c.circ(X + dx, Y + dy + h * .74, 9, HOLE, u)
            pr = (t * 1.2) % 1.0; c.circ(X + dx, Y + dy + h * .74, 14 + 30 * pr, None, u * (1 - pr), outline=HOLE, ow=4)
        ly = 360 + (1 - k) * 150
        c.text(1130, ly, name, 50, col, u, 'lm', 'Bold'); c.text(1130, ly + 50, sub, 34, DIM, u, 'lm', 'Medium')
    # line 2: the scratch pane is like a screen protector
    m2 = hl(2)
    c.rr(1500, 560, 1700, 860, 30, (26, 30, 56), m2, outline=(90, 98, 140), ow=5)
    c.rr(1488, 548, 1712, 872, 34, None, m2, outline=IN_P, ow=4)
    c.text(1600, 900 - 30, '', 10, INK, 0)
    c.text(1600, 520, 'like a screen protector', 30, IN_P, m2, w='Bold')

def s_pressure(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Cruising at ', INK), ('35,000 ft', OUT_P)], sw_out(T, 1))
    headline(c, [('Outside: about ', INK), ('⅓ the push', OUT_P)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Cabin: like a ', INK), ('7,000 ft', PRES), (' mountain', INK)], sw_in(T, 2) * sw_out(T, 3), size=80)
    headline(c, [('Air pushes ', PRES), ('outward', INK)], sw_in(T, 3))
    m0 = 1 - hl(1)
    if m0 > .01:
        plane(c, 960 + 30 * math.sin(t * .6), 420, 1.6, m0)
        c.line([(300, 700), (1620, 700)], (60, 68, 110), 4, m0)
        c.arrow(1700, 690, 1700, 440, OUT_P, 6, m0, 22)
        c.text(1700, 400, '35,000 ft', 44, OUT_P, m0, w='Bold')
        c.text(960, 780, 'thin air outside', 40, DIM, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        g = fd(T(1), .3, 1.2) if T(1) > -.1 else 0
        for k, (lab, val, col) in enumerate((('cabin', 11.0, PRES), ('outside', 3.4, OUT_P))):
            y = 400 + k * 200; L = 1000 * val / 11 * g
            c.text(380, y, lab, 48, col, m1, 'rm', 'Bold')
            c.rr(420, y - 50, 420 + 1000, y + 50, 22, CARD, m1)
            if L > 30: c.rr(420, y - 50, 420 + L, y + 50, 22, col, m1, bg=CARD)
            c.text(1460, y, f'about {val:g} psi', 40, INK, m1 * g, 'lm', 'Bold')
        c.text(960, 820, 'air pressure at cruise (Gizmodo, citing a Boeing 737 manual)', 30, DIM, m1, w='Regular')
    m2 = hl(2) * (1 - hl(3))
    if m2 > .01:
        poly(c, [(560, 800), (960, 330), (1360, 800)], (70, 80, 130), m2)
        poly(c, [(890, 412), (960, 330), (1030, 412), (995, 400), (960, 420), (925, 400)], CLOUD, m2, (70, 80, 130))
        c.circ(960, 330, 18, PRES, m2); c.text(960, 270, '7,000 ft', 46, PRES, m2, w='Bold')
        c.rr(1430, 440, 1750, 620, 26, WALL, m2, outline=PRES, ow=4)
        c.text(1590, 500, 'the cabin', 40, INK, m2, w='Bold', bg=WALL); c.text(1590, 560, 'feels like this', 34, DIM, m2, w='Medium', bg=WALL)
    m3 = hl(3)
    if m3 > .01:
        # a fingertip pressed by half a kilo
        c.rr(820, 470, 1100, 800, 130, (230, 180, 150), m3)
        c.rr(870, 500, 1050, 620, 70, (245, 210, 190), m3, bg=(230, 180, 150))
        k = fd(T(3), 1.0, .8) if T(3) > -.1 else 0
        yy = 300 + 130 * k
        c.rr(860, yy - 90, 1060, yy + 50, 24, PRES, m3); c.text(960, yy - 20, '½ kg', 64, DARK, m3, w='Bold', bg=PRES)
        push(c, 1500, 1230, (420, 540, 660), m3)
        c.text(1365, 760, 'on every fingertip-sized patch', 34, PRES, m3, w='Bold')
        c.text(960, 860, 'our arithmetic: 11 − 3.4 psi ≈ 0.53 kg per square centimetre', 28, DIM, m3, w='Regular')

def s_job(c, T, t):
    """Cross-section: air flows through the hole, balances the middle pane, loads the outer pane."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Here comes ', INK), ('the hole', HOLE)], sw_out(T, 1))
    headline(c, [('Cabin air ', PRES), ('gets into the gap', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Middle pane: ', MID_P), ('balanced', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Outer pane: ', OUT_P), ('takes the load', INK)], sw_in(T, 3))
    outside(c, 1, t); cabin(c, 1, t)
    pane(c, 'outer', 1, OUT_P, glow=hl(3) * (.6 + .4 * math.sin(t * 4)))
    pane(c, 'mid', 1, MID_P, hole=True)
    pane(c, 'inner', .35, IN_P, wdt=14)
    c.text(PX['outer'], PY0 - 50, 'outer', 32, OUT_P, 1, w='Bold'); c.text(PX['mid'], PY0 - 50, 'middle', 32, MID_P, 1, w='Bold')
    hole_ring(c, 1, t)
    flow(c, hl(1), t)
    m2 = hl(2)
    push(c, 1210, PX['mid'] + 24, (400, 520, 640), m2)                  # cabin side pushes on the middle pane
    push(c, PX['outer'] + 26, PX['mid'] - 22, (400, 520, 640), m2 * (1 - hl(3)) , col=(240, 150, 185), w=5, head=14)
    push(c, PX['mid'] - 24, PX['outer'] + 22, (460, 580), m2, col=(240, 150, 185), w=5, head=14)  # gap pushes both ways
    c.text(PX['mid'], PY1 + 50, '= push both sides', 32, MID_P, m2 * (1 - hl(3)), w='Bold')
    m3 = hl(3)
    for y in (380, 470, 560, 650): c.arrow(PX['mid'] - 40, y, PX['outer'] + 24, y, PRES, 9, m3, 22)
    c.text(PX['outer'] - 260, PY0 + 40, 'all the load', 40, OUT_P, m3, w='Bold', bg=(18, 26, 58))

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Why load just ', INK), ('one pane', OUT_P), ('?', INK)], 1, bg=QUIZ)
    for k, txt in enumerate(('A  A lighter window', 'B  A spare pane')):
        u = fd(t, .8 + .3 * k)
        c.rr(330, 380 + k * 190, 1100, 510 + k * 190, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(380, 445 + k * 190, txt, 52, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    if T(0) > 0:
        e = T(0) - 8.6; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 8.3)
        c.circ(1450, 540, 96, HOLE, u, bg=QUIZ); c.text(1450, 540, str(k) if k else '?', 88, DARK, u, w='Bold', bg=HOLE)

def s_spare(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('B: it keeps a ', INK), ('spare', MID_P)], sw_out(T, 1))
    headline(c, [('Middle pane: ', MID_P), ('rested', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Outer cracks? ', PRES), ('Middle takes over', MID_P)], sw_in(T, 2) * sw_out(T, 3), size=78)
    headline(c, [('Built for ', INK), ('1.5×', MID_P), (' normal pressure', INK)], sw_in(T, 3), size=80)
    m = 1 - hl(1) * (1 - hl(2))
    cr = hl(2)
    outside(c, m, t); cabin(c, m, t, x0=1068, x1=1300, label=False)
    pane(c, 'outer', m * (1 - .55 * cr), OUT_P, crack=fd(T(2), .4, 1.0) if T(2) > -.1 else 0)
    pane(c, 'mid', m, MID_P, hole=True, glow=cr * (.6 + .4 * math.sin(t * 4)))
    pane(c, 'inner', m * .35, IN_P, wdt=14)
    hole_ring(c, m * (1 - cr), t)
    for y in (380, 470, 560, 650):
        c.arrow(PX['mid'] - 40, y, PX['outer'] + 24, y, PRES, 9, m * (1 - cr), 22)
        c.arrow(1280, y, PX['mid'] + 24, y, PRES, 9, m * cr, 22)
    c.text(PX['mid'], PY0 - 50, 'spare', 36, MID_P, m, w='Bold')
    # line 1: the spare tyre in the boot
    m1 = hl(1) * (1 - hl(2))
    tyre(c, 960, 500, 210, m1)
    c.text(960, 800, 'like a spare tyre: ready, and unworn', 40, MID_P, m1, w='Bold')
    m3 = hl(3)
    c.rr(1360, 360, 1780, 640, 28, CARD, m3, outline=MID_P, ow=4)
    c.text(1570, 440, 'middle pane', 38, DIM, m3, w='Bold', bg=CARD)
    c.text(1570, 520, '1.5×', 84, MID_P, m3, w='Bold', bg=CARD)
    c.text(1570, 600, 'normal pressure', 34, INK, m3, w='Bold', bg=CARD)
    c.text(1570, 690, 'Boeing 737 manual, via Gizmodo', 26, DIM, m3, w='Regular')

def s_fog(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A ', INK), ('second job', HOLE)], sw_out(T, 1))
    headline(c, [('Moist air ', WET), ('meets cold glass', OUT_P)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Trapped = ', INK), ('fog and frost', WET)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('The hole ', HOLE), ('lets it out', INK)], sw_in(T, 3))
    # left: the window front view fogs on line 2 and clears on line 3
    fog = hl(2) * (1 - fd(T(3), .6, 1.4)) if T(3) > -.1 else hl(2)
    window(c, 560, 520, 1.0, 1, t, hole=1 - .6 * fog, fog=fog)
    c.text(560, 812, 'mostly clear, not always perfectly', 30, DIM, hl(3), w='Regular')
    # right: droplets in the gap between middle and outer panes
    X0 = 1150
    c.rr(X0, PY0, X0 + 34, PY1, 8, OUT_P, 1); c.rr(X0 + 200, PY0, X0 + 234, HY - 14, 8, MID_P, 1); c.rr(X0 + 200, HY + 14, X0 + 234, PY1, 8, MID_P, 1)
    c.text(X0 + 17, PY0 - 40, 'outer', 30, OUT_P, 1, w='Bold'); c.text(X0 + 217, PY0 - 40, 'middle', 30, MID_P, 1, w='Bold')
    c.circ(X0 + 217, HY, 12, HOLE, 1)
    m1 = hl(1)
    rng = random.Random(2)
    out = fd(T(3), .3, 2.0) if T(3) > -.1 else 0.0
    for k in range(9):
        bx, by = rng.uniform(X0 + 70, X0 + 165), rng.uniform(340, 700)
        x = bx + (X0 + 300 - bx) * clamp(out * 1.3 - k * .05) ; y = by + (HY - by) * clamp(out * 2 - k * .1)
        drop(c, x + 4 * math.sin(t * 2 + k), y, 14, m1 * (1 - clamp(out * 1.3 - k * .05 - .7) / .3))
    c.text(X0 + 117, PY1 + 45, 'the gap', 32, WET, m1, w='Bold')
    m2 = hl(2) * (1 - hl(3))
    c.rr(1520, 380, 1800, 640, 24, (210, 220, 240), m2, outline=BEZEL, ow=6)
    c.text(1660, 510, 'mirror after', 30, DARK, m2, w='Bold', bg=(210, 220, 240)); c.text(1660, 552, 'a shower', 30, DARK, m2, w='Bold', bg=(210, 220, 240))

def s_payoff(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Not a ', INK), ('weak spot', PRES)], sw_out(T, 1))
    headline(c, [('It picks ', INK), ('the working pane', OUT_P)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('And keeps ', INK), ('a spare', MID_P)], sw_in(T, 2))
    window(c, 620, 540, 1.15, 1, t)
    c.cross(620, 540 + 205 * 1.15 * .74 - 6, 70, PRES, hl(0) * (1 - hl(1)) * .9)
    for k, (txt, col) in enumerate((('outer pane does the work', OUT_P), ('middle pane kept fresh', MID_P))):
        m = hl(k + 1); y = 420 + k * 200
        c.rr(1060, y - 70, 1760, y + 70, 30, CARD, m, outline=col, ow=5)
        c.text(1410, y, txt, 44, col, m, w='Bold', bg=CARD)

def s_recap(c, T, t):
    """Recap as three little cabin windows in a row (last recap used tear-off pages)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', HOLE)], 1)
    items = ((1, '3 panes', 'one is a shield', 'the inner scratch pane', IN_P),
             (2, 'hole', 'loads the outer', 'cabin air fills the gap', OUT_P),
             (3, 'spare', 'middle stays ready', 'and less fog', MID_P))
    for ln, big, l1, l2, col in items:
        m = hl(ln); x = 400 + (ln - 1) * 560; dy = 40 * (1 - m)
        c.rr(x - 150, 280 + dy, x + 150, 640 + dy, 120, BEZEL, m)
        c.rr(x - 122, 308 + dy, x + 122, 612 + dy, 100, SKY, m, bg=BEZEL)
        c.circ(x - 70, 300 + 330 + dy - 10, 0, None, 0)
        c.text(x, 400 + dy, str(ln), 44, CLOUD, m, w='Bold', bg=SKY)
        c.text(x, 500 + dy, big, 54 if ' ' in big else 64, INK, m, w='Bold', bg=SKY, stroke=3)
        c.text(x, 720 + dy, l1, 42, col, m, w='Bold')
        c.text(x, 780 + dy, l2, 30, DIM, m, w='Medium')
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """Bright, lit window on the dark background, hole circled in yellow."""
    window(c, 1530, 560, 1.45, 1, 3.0, hole=0)
    hx, hy = 1530, 560 + 205 * 1.45 * .74
    c.circ(hx, hy, 52, None, 1, outline=YE, ow=12)

SCENES = [
 ('THE HOLE', ["Next time you fly, look at the bottom of your window. There's a tiny hole.",
               "It looks like a flaw. It isn't.",
               "That hole is there on purpose, and it's part of what keeps the window safe."], s_hook),
 ('THREE PANES', ["A plane window isn't one sheet. It's three panes.",
                  "The outer pane faces the sky. The middle pane is the one with the hole.",
                  "The inner pane, the one you can touch, is just a scratch shield, like a screen protector on a phone. It carries no load."], s_panes),
 ('THE PRESSURE', ["Planes cruise at around thirty-five thousand feet, where the air is thin.",
                   "Out there, the air presses only about a third as hard as the air in the cabin.",
                   "The cabin is kept at about the pressure you'd feel on a mountain seven thousand feet high.",
                   "So the cabin air pushes outward on the window. That's about half a kilo on every patch the size of your fingertip."], s_pressure),
 ('THE JOB', ["Here's where the hole comes in.",
              "It lets cabin air into the gap between the middle and outer panes.",
              "Now the gap is at cabin pressure. The middle pane gets the same push from both sides, so it carries almost nothing.",
              "That leaves the outer pane to take the whole load."], s_job),
 ('QUICK QUESTION', ["Quick question. Why would engineers want just one pane to carry the load? A lighter window, or a spare? Have a guess."], s_quiz),
 ('THE SPARE', ["It keeps a spare.",
                "With the outer pane doing the work, the middle pane sits there rested, like a spare tyre in the boot.",
                "If the outer pane ever cracked, the middle pane is strong enough to take over.",
                "One Boeing seven-thirty-seven manual says it's built to handle one and a half times the normal pressure."], s_spare),
 ('THE FOG', ["The hole has a second job.",
              "Cabin air carries moisture, and the outer pane faces the cold outside.",
              "If that moisture were trapped between the panes, the window could fog up or frost over, like a bathroom mirror after a shower.",
              "The hole lets it escape, which helps keep your view clear. Not always perfectly, but mostly."], s_fog),
 ('THE PAYOFF', ["So that tiny hole isn't a weak spot.",
                 "It decides which pane does the work.",
                 "And it keeps a second pane fresh, just in case."], s_payoff),
 ('RECAP', ["Three things to keep.",
            "One: a plane window has three panes, and the one you touch is just a scratch shield.",
            "Two: the tiny hole lets cabin air into the gap, so the outer pane takes the load.",
            "Three: that keeps the middle pane ready as a spare, and helps stop fog.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    """Claim on screen from frame one; the hole pulses from t = 0."""
    headline(c, [('This hole is ', INK), ('on purpose', HOLE)], sw_out(T, 1), size=88)
    headline(c, [('3 panes. ', INK), ('Hole in the middle', MID_P)], sw_in(T, 1), size=80)
    sp = fd(T(1), .3, 1.0) if T(1) > -.1 else 0.0
    window(c, 960 - 300 * sp, 560, 1.15, 1, t)
    for k, (col, name) in enumerate(((OUT_P, 'outer'), (MID_P, 'middle'), (IN_P, 'inner'))):
        u = fd(T(1), .6 + .3 * k) if T(1) > -.1 else 0.0; y = 380 + k * 150
        c.rr(1060, y - 50, 1500, y + 50, 24, CARD, u, outline=col, ow=5); c.text(1280, y, name, 46, col, u, w='Bold', bg=CARD)
        if k == 1: c.circ(1460, y, 12, HOLE, u, bg=CARD)

def short_flow(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Cabin air ', PRES), ('pushes out', INK)], sw_out(T, 1), size=88)
    headline(c, [('The hole ', HOLE), ('fills the gap', INK)], sw_in(T, 1), size=88)
    outside(c, 1, t); cabin(c, 1, t)
    pane(c, 'outer', 1, OUT_P); pane(c, 'mid', 1, MID_P, hole=True); pane(c, 'inner', .35, IN_P, wdt=14)
    hole_ring(c, 1, t)
    push(c, 1500, 1230, (420, 540, 660), 1 - hl(1))
    flow(c, hl(1), t)

def short_spare(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Outer pane: ', OUT_P), ('the load', INK)], sw_out(T, 1), size=88)
    headline(c, [('Middle pane: ', MID_P), ('the spare', INK)], sw_in(T, 1), size=88)
    cr = fd(T(1), 3.0, .6) if T(1) > -.1 else 0.0        # the crack waits for 'If the outer pane ever cracked'
    outside(c, 1, t); cabin(c, 1, t, x0=1068, x1=1300, label=False)
    pane(c, 'outer', 1 - .55 * cr, OUT_P, glow=(1 - cr) * (.6 + .4 * math.sin(t * 4)), crack=fd(T(1), 3.0, 1.0) if T(1) > -.1 else 0)
    pane(c, 'mid', 1, MID_P, hole=True, glow=cr * (.6 + .4 * math.sin(t * 4))); pane(c, 'inner', .35, IN_P, wdt=14)
    for y in (380, 470, 560, 650):
        c.arrow(PX['mid'] - 40, y, PX['outer'] + 24, y, PRES, 9, 1 - cr, 22)
        c.arrow(1280, y, PX['mid'] + 24, y, PRES, 9, cr, 22)
    tyre(c, 1560, 540, 150, 1)

def short_fog(c, T, t):
    headline(c, [('Bonus: ', HOLE), ('less fog', WET)], 1, size=88)
    fog = 1 - fd(T(0), 1.2, 2.0) if T(0) > -.1 else 1
    window(c, 960, 540, 1.15, 1, t, fog=fog)
    for k in range(6):
        u = fd(T(0), .6 + .2 * k) if T(0) > -.1 else 0
        drop(c, 1240 + 60 * k + 80 * u, 640 - 160 * u - 30 * k, 14, 1 - u)

SHORT_SCENES = [
 ('THE HOLE', ["That tiny hole in a plane window is there on purpose.",
               "The window has three panes, and the hole is in the middle one."], short_hook),
 ('THE PUSH', ["Up high, the cabin air pushes outward much harder than the thin air outside.",
               "The hole lets cabin air into the gap, so the middle pane gets the same push on both sides."], short_flow),
 ('THE SPARE', ["That puts the whole load on the outer pane.",
                "And it keeps the middle pane rested as a spare. If the outer pane ever cracked, the middle one can take over."], short_spare),
 ('BONUS', ["It also lets moisture out of the gap, which helps stop the window fogging up."], short_fog),
 ('THE ANSWER', ["So the hole isn't a weak spot.",
                 "It's how the window keeps a backup."], card('Outer pane: takes the load.', 'Middle pane: the spare.')),
]
SHORT_HITS = [(4, 1, 0.0)]
