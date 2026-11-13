"""Episode: Memory Champions Aren't Smarter. Try Their Trick (the memory palace / method of loci; the viewer memorises a list inside the video)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'The Memory Palace'                           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'How do memory champions remember?'            # headline on the vertical Short
HITS = [(0, 2, 0.0), (7, 3, 0.0), (9, 3, 0.0)]              # "the difference is a trick", 26 -> 62, the recall answer
THUMB = ['YOUR HOME', 'IS A MEMORY.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 2): 0.3, (2, 3): 0.3, (4, 0): 0.3, (4, 1): 1.5, (7, 3): 0.4, (9, 2): 3.2, (9, 3): 0.3, (10, 3): 0.2}
SHORT_PAUSES = {(0, 1): 0.2, (3, 1): 0.3}
CAPTION_FIXES = {'twenty seventeen': '2017', 'two thousand and three': '2003', 'twenty-six': '26', 'sixty-two': '62',
                 'seventy-two': '72', 'twenty-two': '22'}

# Colour code kept in every scene: places and the route are blue, the things to remember are yellow,
# brains and scans are purple, the answer and checks are green, the old legend is pink.
ROUTE = CY; ITEM = YE; BRN = PU; ANS = GR; OLD = PK
DARK = (20, 22, 38); WALL = (90, 104, 170); FLOOR = (24, 30, 60)
PAPER = (62, 42, 34); PINK_ = (60, 24, 44); PAPER_INK = INK; SHEET = (86, 60, 46)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=88, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

# ---------- the five things to remember (simple original icons) ----------
def milk(c, x, y, s, a, bg=BG):
    if a <= .01: return
    poly(c, [(x - 34 * s, y - 40 * s), (x, y - 78 * s), (x + 34 * s, y - 40 * s)], (210, 215, 235), a, bg)
    c.rr(x - 34 * s, y - 42 * s, x + 34 * s, y + 60 * s, 6 * s, (245, 246, 255), a, bg=bg)
    c.rr(x - 34 * s, y - 2 * s, x + 34 * s, y + 26 * s, 0, CY, a, bg=(245, 246, 255))

def battery(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 12 * s, y - 64 * s, x + 12 * s, y - 50 * s, 4 * s, (200, 200, 210), a, bg=bg)
    c.rr(x - 30 * s, y - 52 * s, x + 30 * s, y + 60 * s, 10 * s, ITEM, a, bg=bg)
    c.rr(x - 30 * s, y + 20 * s, x + 30 * s, y + 60 * s, 10 * s, (60, 60, 70), a, bg=ITEM)
    c.text(x, y - 14 * s, '+', 50 * s, DARK, a, w='Bold', bg=ITEM)

def banana(c, x, y, s, a, bg=BG):
    if a <= .01: return
    box = ((x - 70 * s) * c.k, (y - 90 * s) * c.k, (x + 70 * s) * c.k, (y + 50 * s) * c.k)
    c.d.arc(box, 20, 160, fill=mix(ITEM, a, bg), width=int(30 * s * c.k))
    c.circ(x - 64 * s, y - 6 * s, 7 * s, (110, 80, 40), a, bg=bg)

def sock(c, x, y, s, a, col=ITEM, bg=BG):
    if a <= .01: return
    poly(c, [(x - 22 * s, y - 70 * s), (x + 22 * s, y - 70 * s), (x + 22 * s, y + 10 * s), (x + 60 * s, y + 28 * s),
             (x + 56 * s, y + 62 * s), (x - 10 * s, y + 52 * s), (x - 22 * s, y + 30 * s)], col, a, bg)
    c.rr(x - 22 * s, y - 70 * s, x + 22 * s, y - 50 * s, 0, PK, a, bg=col)

def stamp(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 42 * s, y - 52 * s, x + 42 * s, y + 52 * s, 2 * s, (250, 250, 250), a, bg=bg)
    for k in range(7):
        for (px, py) in ((x - 42 * s + k * 14 * s, y - 52 * s), (x - 42 * s + k * 14 * s, y + 52 * s)):
            c.circ(px, py, 4 * s, bg, a, bg=bg)
    c.rr(x - 30 * s, y - 40 * s, x + 30 * s, y + 40 * s, 2 * s, ITEM, a, bg=(250, 250, 250))
    c.circ(x, y - 4 * s, 16 * s, PK, a, bg=ITEM)

ICONS = [milk, battery, banana, sock, stamp]
WORDS = ['milk', 'batteries', 'bananas', 'socks', 'stamps']

# ---------- the house: a floor plan with five stops on one route ----------
STOPS = [(470, 730, 'front door'), (760, 440, 'sofa'), (1150, 400, 'kitchen sink'), (1450, 560, 'bed'), (1190, 760, 'shower')]

def house(c, a, bg=BG, ox=0, oy=0, sc=1.0, labels=True, lit=None):
    """Top-down floor plan. lit: list of 0..1 per stop for a glow."""
    if a <= .01: return
    P = lambda x, y: (960 + (x - 960) * sc + ox, 580 + (y - 580) * sc + oy)
    x0, y0 = P(360, 300); x1, y1 = P(1600, 840)
    c.rr(x0, y0, x1, y1, 18 * sc, FLOOR, a, outline=WALL, ow=6, bg=bg)
    for (ax, ay, bx, by) in ((960, 300, 960, 520), (960, 640, 960, 840), (1300, 300, 1300, 470), (1300, 600, 1300, 840), (960, 600, 1300, 600)):
        p0, p1 = P(ax, ay), P(bx, by); c.line([p0, p1], WALL, 6, a, bg=FLOOR)
    dx, dy = P(470, 840); c.rr(dx - 60 * sc, dy - 8 * sc, dx + 60 * sc, dy + 8 * sc, 4, ROUTE, a, bg=FLOOR)   # front door gap
    for k, (sx, sy, lab) in enumerate(STOPS):
        px, py = P(sx, sy); g = lit[k] if lit else 0
        if g > .01: c.circ(px, py, 66 * sc, (40, 70, 110), a * g, bg=FLOOR)
        if labels: c.text(px, py + 92 * sc, lab, int(28 * sc), ROUTE if g > .5 else DIM, a, w='Bold', bg=FLOOR)
    return P

def route(c, P, p, a, bg=FLOOR, t=0.0, walker=True):
    """Dotted route through the stops, drawn up to progress p (0..1), with a walking dot."""
    if a <= .01 or p <= 0: return
    pts = [P(x, y) for x, y, _ in STOPS]
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(4)]; L = sum(seg)
    d = 0.0; target = L * clamp(p); n = 0
    while d < target:
        acc = 0.0
        for i in range(4):
            if d <= acc + seg[i]:
                f = (d - acc) / seg[i]; x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f; break
            acc += seg[i]
        c.circ(x, y, 6, ROUTE, a * .8, bg=bg); d += 26; n += 1
    if walker:
        d = target; acc = 0.0; x, y = pts[-1]
        for i in range(4):
            if d <= acc + seg[i]:
                f = (d - acc) / seg[i]; x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f; break
            acc += seg[i]
        c.circ(x, y, 18 + 3 * math.sin(t * 6), INK, a, outline=ROUTE, ow=5, bg=bg)

def stop_num(c, P, k, a, bg=FLOOR):
    if a <= .01: return
    x, y = P(STOPS[k][0], STOPS[k][1])
    c.circ(x, y, 26, ROUTE, a, bg=bg); c.text(x, y, str(k + 1), 30, DARK, a, w='Bold', bg=ROUTE)

def item_at(c, P, k, a, t, s=.9, bg=FLOOR):
    """The vivid picture for stop k, with a little motion so it feels strange and alive."""
    if a <= .01: return
    x, y = P(STOPS[k][0], STOPS[k][1]); y -= 10
    if k == 0:
        milk(c, x - 10, y - 30, s, a, bg)
        for j in range(5):
            u = (t * 1.2 + j / 5) % 1; c.circ(x + 20 + 10 * j, y + 20 + 50 * u, 7, (245, 246, 255), a * (1 - u), bg=bg)
    elif k == 1:
        battery(c, x, y, s * .8, a, bg)
        for j in range(4):
            ang = t * 3 + j * 1.57; c.text(x + 70 * math.cos(ang), y + 40 * math.sin(ang), 'z', 30, ITEM, a, w='Bold', bg=bg)
    elif k == 2:
        ang = t * 2.4; bx, by = x + 18 * math.cos(ang), y + 12 * math.sin(ang)
        banana(c, bx, by, s * .8, a, bg)
    elif k == 3:
        sock(c, x, y - 10, s * 1.25, a, bg=bg)
    else:
        for j in range(3): stamp(c, x - 60 + j * 60, y - 10 + (j % 2) * 30, s * .55, a, bg)

def brain(c, x, y, r, a, glow=0.0, spot=0.0, bg=BG):
    if a <= .01: return
    fill = tuple(int(CARD[j] + (BRN[j] - CARD[j]) * .35 * glow) for j in range(3))
    c.circ(x - r * .3, y, r * .8, fill, a, outline=BRN, ow=6, bg=bg); c.circ(x + r * .3, y, r * .8, fill, a, outline=BRN, ow=6, bg=bg)
    c.rr(x - r * .7, y - r * .2, x + r * .7, y + r * .6, r * .3, fill, a, bg=bg)
    c.line([(x, y - r * .75), (x, y + r * .55)], BRN, 5, a, bg=fill)
    for dx in (-1, 1):
        c.d.arc(((x + dx * r * .45 - r * .3) * c.k, (y - r * .35) * c.k, (x + dx * r * .45 + r * .3) * c.k, (y + r * .25) * c.k), 200, 340, fill=mix(BRN, a, fill), width=int(5 * c.k))
    if spot > .01:                                     # the place-and-route areas lighting up
        c.circ(x + r * .25, y + r * .3, r * .22, ROUTE, a * spot, bg=fill)
        c.circ(x - r * .35, y - r * .25, r * .14, ROUTE, a * spot, bg=fill)

def person(c, x, y, s, a, col=DIM, medal=False, bg=BG):
    if a <= .01: return
    c.circ(x, y - 120 * s, 46 * s, col, a, bg=bg)
    c.rr(x - 62 * s, y - 64 * s, x + 62 * s, y + 90 * s, 40 * s, col, a, bg=bg)
    if medal:
        c.line([(x - 22 * s, y - 64 * s), (x, y - 10 * s), (x + 22 * s, y - 64 * s)], PK, 8 * s, a, bg=col)
        c.circ(x, y, 22 * s, ITEM, a, bg=col)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Fact plus a promise; word cards already flying in the first frame."""
    hl = lambda i: hl_(T, i)
    headline(c, [('100 words', ITEM), (' in 5 minutes', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Same ', INK), ('brains', BRN), (' as yours', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('The difference: a ', INK), ('trick', ROUTE)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('You\'ll ', INK), ('try it', ANS), (' today', INK)], sw_in(T, 3))
    m0 = 1 - .85 * hl(1)
    n = min(100, int(4 + t * 22))
    random.seed(3)
    for k in range(18):                                 # word cards streaming in
        u = (t * .35 + k / 18) % 1; px = 160 + 1600 * u; py = 330 + (k * 97) % 470
        w = random.choice(['lamp', 'river', 'shoe', 'cloud', 'drum', 'tiger', 'salt', 'key', 'moon', 'chair'])
        c.rr(px - 70, py - 28, px + 70, py + 28, 14, CARD, m0 * .9 * math.sin(u * math.pi), outline=ITEM, ow=2)
        c.text(px, py, w, 30, INK, m0 * .9 * math.sin(u * math.pi), w='Bold', bg=CARD)
    c.rr(760, 470, 1160, 690, 30, DARK, m0, outline=ITEM, ow=5)
    c.text(960, 545, str(n), 110, ITEM, m0, w='Bold', bg=DARK); c.text(960, 640, 'words', 36, DIM, m0, w='Bold', bg=DARK)
    m1 = hl(1) * (1 - hl(2))
    brain(c, 640, 540, 150, m1); brain(c, 1280, 540, 150, m1)
    c.text(960, 540, '=', 120, ANS, m1, w='Bold')
    c.text(640, 760, 'memory champion', 34, DIM, m1, w='Bold'); c.text(1280, 760, 'you', 34, DIM, m1, w='Bold')
    m2 = hl(2)
    P = house(c, m2, sc=.62, oy=40, labels=False, lit=[m2] * 5)
    if P:
        route(c, P, fd(T(2), .2, 2.2), m2, t=t)
        for k in range(5): stop_num(c, P, k, m2 * fd(T(2), .3 + .4 * k))
    m3 = hl(3)
    c.circ(1640, 700, 60, ANS, m3); c.check(1640, 700, 54, DARK, m3, fd(T(3), .3, .5))

def s_scan(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Scanned in ', INK), ('2003', BRN)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('Not ', INK), ('smarter', ITEM), (' overall', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('Same ', INK), ('structure', BRN)], sw_in(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('Place', ROUTE), (' areas lit up', INK)], sw_in(T, 3) * sw_out(T, 4))
    headline(c, [('Walking a ', INK), ('place', ROUTE), (' in the mind', INK)], sw_in(T, 4))
    m0 = fd(T(0), .1)
    person(c, 290, 700, 1.1, m0, DIM, medal=True); c.text(290, 840, 'memory champions', 32, ITEM, m0, w='Bold')
    person(c, 1630, 700, 1.1, m0, DIM); c.text(1630, 840, 'ordinary people', 32, DIM, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    for k, x in enumerate((760, 1160)):
        c.rr(x - 50, 760 - 300, x + 50, 760, 10, CARD, m1, outline=ITEM if k == 0 else DIM, ow=3)
        c.rr(x - 40, 760 - 280 * fd(T(1), .3, .8), x + 40, 750, 8, ITEM if k == 0 else DIM, m1, bg=CARD)
    c.text(960, 820, 'general thinking tests', 30, DIM, m1, w='Bold')
    c.text(960, 610, '≈', 90, ANS, m1 * fd(T(1), 1.0), w='Bold')
    m2 = hl(2); spot = hl(3)
    brain(c, 760, 520, 130, m2, glow=spot, spot=spot); brain(c, 1160, 520, 130, m2)
    if m2 * (1 - spot) > .01: c.text(960, 720, 'no important difference in shape', 32, ANS, m2 * (1 - spot), w='Bold')
    c.text(960, 720, 'more activity in areas for places and routes', 32, ROUTE, spot * (1 - hl(4)), w='Bold')
    c.text(960, 770, 'including the hippocampus', 30, DIM, spot * (1 - hl(4)), w='Bold')
    m4 = hl(4)
    c.circ(620, 300, 30, CARD, m4); c.circ(660, 360, 18, CARD, m4)
    c.rr(480, 230, 900, 330, 50, CARD, 0)
    P = house(c, m4, sc=.28, ox=-300, oy=-320, labels=False)
    if P: route(c, P, (t * .3) % 1, m4, t=t, walker=True)

TX, TY = 860, 560
def s_legend(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('An ', INK), ('ancient', OLD), (' story', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('The hall ', INK), ('collapsed', OLD)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('No one ', INK), ('recognisable', OLD)], sw_in(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('He knew the ', INK), ('seats', ROUTE)], sw_in(T, 3) * sw_out(T, 4))
    headline(c, [('Legend? ', OLD), ('Method: real', ANS)], sw_in(T, 4))
    seats = [(TX - 330 + k * 132, TY - 170) for k in range(6)] + [(TX - 330 + k * 132, TY + 170) for k in range(6)]
    cols = [PK, CY, YE, GR, PU, (255, 150, 90)] * 2
    c.rr(TX - 380, TY - 90, TX + 380, TY + 90, 30, (90, 60, 50), 1)
    for k in range(6): c.circ(TX - 320 + k * 128, TY, 18, (230, 220, 200), .8, bg=(90, 60, 50))
    rub = fd(T(1), .3, 1.2); know = hl(3)
    for k, (sx, sy) in enumerate(seats):
        a = 1 - .85 * rub + .85 * know
        col = cols[k] if (rub < .5 or know > .5) else (110, 110, 120)
        c.circ(sx, sy, 40, col, a); c.circ(sx, sy - 5, 14, DARK, a * .5, bg=col)
        if hl(2) > .3 and know < .5: c.text(sx, sy, '?', 46, INK, hl(2), w='Bold', bg=(110, 110, 120))
        if know > .01: c.check(sx + 34, sy - 34, 18, ANS, know, fd(T(3), .2 + .07 * k, .3))
    # the poet walks out just before the collapse
    wx = 1300 + 380 * fd(T(0), 1.0, 2.5); person(c, wx, 760, .7, 1, OLD); c.text(wx, 860, 'Simonides', 30, OLD, 1, w='Bold')
    if rub > .01 and know < .9:
        random.seed(7)
        for k in range(40):
            bx = TX - 420 + random.random() * 840; by0 = TY - 340; by = by0 + (TY + 220 - by0) * clamp(rub * (1.2 - random.random() * .4))
            c.rr(bx - 20, by - 14, bx + 20, by + 14, 4, (120, 116, 130), rub * (1 - know) * .9)
    m4 = hl(4)
    c.rr(1340, 300, 1860, 420, 20, CARD, m4, outline=OLD, ow=3)
    c.text(1600, 340, 'told by Cicero, 1st century BC', 30, INK, m4, w='Bold', bg=CARD); c.text(1600, 386, 'probably a legend', 30, OLD, m4, w='Bold', bg=CARD)
    c.text(40, 858, 'Scene drawn for illustration', 28, DIM, 1, anchor='lm', w='Regular')

def s_method(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Loci', ROUTE), (' = places', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('A place ', INK), ('you know', ROUTE)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('Stops in a ', INK), ('fixed order', ROUTE)], sw_in(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('One ', INK), ('strange picture', ITEM), (' each', INK)], sw_in(T, 3) * sw_out(T, 4))
    headline(c, [('Recall: ', INK), ('walk it', ROUTE)], sw_in(T, 4))
    m0 = fd(T(0), .1)
    c.text(960, 300, 'the memory palace', 54, ROUTE, m0 * (1 - hl(1)), w='Bold')
    c.text(960, 380, 'also called the method of loci', 36, DIM, m0 * (1 - hl(1)), w='Bold')
    m1 = hl(1)
    lit = [fd(T(2), .4 + .55 * k, .3) for k in range(5)]
    P = house(c, m1, lit=lit)
    if P:
        for k in range(5): stop_num(c, P, k, lit[k] * (1 - hl(3)))
        if hl(3) > .01:
            for k in range(5): item_at(c, P, k, fd(T(3), .3 + .35 * k, .4), t, s=.7)
        if hl(4) > .01: route(c, P, fd(T(4), .2, 2.6), hl(4), t=t)

def s_try(c, T, t):
    """Pattern interrupt: a bright paper scene where the viewer is handed the list."""
    hl = lambda i: hl_(T, i)
    c.rr(0, 120, 1920, 900, 0, PAPER, 1)
    headline(c, [('Try it: ', ITEM), ('5 things to buy', PAPER_INK)], 1, bg=PAPER)
    c.rr(560, 260, 1360, 860, 24, SHEET, 1, outline=ITEM, ow=4, bg=PAPER)
    for k in range(5):
        y = 330 + k * 112
        c.line([(600, y + 52), (1320, y + 52)], (120, 92, 72), 3, 1, bg=SHEET)
        a = fd(T(1), .62 * k, .3)
        ICONS[k](c, 700, y + 4, .5, a, bg=SHEET)
        c.text(790, y, WORDS[k], 58, PAPER_INK, a, 'lm', 'Bold', bg=SHEET)

def s_place(c, T, t):
    hl = lambda i: hl_(T, i)
    labs = [('Door: ', ROUTE, 'milk', ITEM), ('Sofa: ', ROUTE, 'batteries', ITEM), ('Sink: ', ROUTE, 'bananas', ITEM),
            ('Bed: ', ROUTE, 'a giant sock', ITEM), ('Shower: ', ROUTE, 'stamps', ITEM)]
    for k, (a1, c1, a2, c2) in enumerate(labs):
        a = (sw_in(T, k) if k else 1) * (sw_out(T, k + 1) if k < 4 else 1)
        headline(c, [(a1, c1), (a2, c2)], a)
    lit = [hl(k) for k in range(5)]
    P = house(c, 1, lit=lit)
    for k in range(5):
        stop_num(c, P, k, 1 - lit[k])
        item_at(c, P, k, fd(T(k), .2, .4), t, s=.9 if k != 3 else 1.0)
    route(c, P, clamp(sum(fd(T(k), 0, .9) if T(k) > 0 else 0 for k in range(1, 5)) / 4 + .001), 1, t=t)
    c.text(1880, 858, 'Your own home works best', 28, DIM, 1, anchor='rm', w='Regular')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Why does it ', INK), ('work', ANS), ('?', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('A bare word ', INK), ('slips', OLD)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Picture', ITEM), (' + ', INK), ('address', ROUTE)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('The route keeps ', INK), ('the order', ROUTE)], sw_in(T, 3))
    m1 = hl(1)
    fl = (t * .5) % 1 if m1 > .01 else 0
    for k, w in enumerate(('milk', 'socks', 'stamps')):
        u = fd(T(1), .3 + .4 * k, 2.2)
        c.text(470 + 90 * math.sin(t + k), 420 + k * 120 - 200 * u, w, 56, DIM, m1 * (1 - u) * (1 - hl(2) * .5), w='Bold')
    m2 = hl(2)
    c.rr(980, 300, 1700, 640, 30, CARD, m2, outline=ROUTE, ow=4)
    milk(c, 1150, 480, 1.2, m2, bg=CARD)
    c.rr(1290, 380, 1640, 470, 16, DARK, m2, bg=CARD); c.text(1465, 425, '1  front door', 38, ROUTE, m2, w='Bold', bg=DARK)
    c.text(1465, 540, 'milk pouring out', 34, ITEM, m2, w='Bold', bg=CARD)
    m3 = hl(3)
    for k in range(5):
        x = 400 + k * 280; a = m3 * fd(T(3), .2 + .2 * k)
        c.circ(x, 760, 34, ROUTE, a); c.text(x, 760, str(k + 1), 34, DARK, a, w='Bold', bg=ROUTE)
        if k < 4: c.arrow(x + 44, 760, x + 236, 760, ROUTE, 5, a)
    c.text(1880, 858, 'Simplified explanation', 28, DIM, 1, anchor='rm', w='Regular')

def s_study(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Can ', INK), ('anyone', ANS), (' learn it?', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('30 min a day', ROUTE), (', 40 days', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('Before: ', INK), ('26', DIM), (' of 72', INK)], sw_in(T, 2) * sw_out(T, 3) * sw_out(T, 4))
    headline(c, [('After: ', INK), ('62', ANS)], sw_in(T, 3) * sw_out(T, 4))
    headline(c, [('Other groups: ', INK), ('+11, +7', DIM)], sw_in(T, 4))
    m0 = fd(T(0), .1)
    c.text(960, 280, 'Dresler and colleagues, 2017 (published in Neuron)', 32, DIM, m0, w='Bold')
    m1 = hl(1)
    for k in range(40):
        x = 300 + (k % 10) * 70; y = 360 + (k // 10) * 70
        a = m1 * (1 - hl(2)) * fd(T(1), .5 + k * .04, .2)
        c.rr(x, y, x + 56, y + 56, 8, CARD, a, outline=ROUTE, ow=2); c.check(x + 28, y + 28, 18, ROUTE, a, 1)
    c.text(650, 680, '40 days of practice', 36, ROUTE, m1 * (1 - hl(2)), w='Bold')
    base, top = 800, 340; sc = (base - top) / 72
    m2 = hl(2)
    c.line([(260, base), (1700, base)], DIM, 3, m2)
    c.text(230, base - 72 * sc, '72', 28, DIM, m2, 'rm', 'Bold'); c.line([(250, base - 72 * sc), (1700, base - 72 * sc)], (50, 58, 100), 2, m2)
    # memory palace group: before / after
    c.rr(380, base - 26 * sc * fd(T(2), .2, .6), 520, base, 10, DIM, m2); c.text(450, base - 26 * sc - 30, '26', 40, DIM, m2 * fd(T(2), .6), w='Bold')
    m3 = hl(3); h = 62 * sc * fd(T(3), .1, .8)
    c.rr(560, base - h, 700, base, 10, ANS, m3); c.text(630, base - h - 30, '62', 48, ANS, m3 * fd(T(3), .7), w='Bold')
    c.text(540, base + 40, 'memory palace', 30, ANS, m2, w='Bold')
    m4 = hl(4)
    for k, (lab, g) in enumerate((('short-term memory games', 11), ('no training', 7))):
        x = 1000 + k * 380; h2 = g * sc * fd(T(4), .3 + .5 * k, .6)
        c.rr(x, base - h2, x + 140, base, 10, DIM, m4); c.text(x + 70, base - h2 - 30, f'+{g}', 40, DIM, m4 * fd(T(4), .7 + .5 * k), w='Bold')
        c.text(x + 70, base + 40, lab, 28, DIM, m4, w='Bold')
    c.text(1880, 858, 'Words recalled from a list of 72; group averages', 28, DIM, m2, anchor='rm', w='Regular')

def s_later(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('4 months', ROUTE), (' later', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Still ', INK), ('+22 words', ANS)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Same brain, ', INK), ('new wiring', BRN)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('It takes ', INK), ('practice', ITEM)], sw_in(T, 3))
    m0 = fd(T(0), .1) * (1 - hl(2))
    for k in range(4):                                   # calendar pages
        x = 360 + k * 170; a = m0 * fd(T(0), .3 + .3 * k)
        c.rr(x - 70, 360, x + 70, 520, 14, CARD, a, outline=ROUTE, ow=3); c.rr(x - 70, 360, x + 70, 400, 14, ROUTE, a)
        c.text(x, 460, str(k + 1), 56, INK, a, w='Bold', bg=CARD)
    c.text(615, 580, 'no more training', 34, DIM, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    c.rr(1200, 330, 1660, 640, 30, CARD, m1, outline=ANS, ow=4)
    c.text(1430, 460, '+22', 120, ANS, m1, w='Bold', bg=CARD); c.text(1430, 580, 'words vs. before', 34, DIM, m1, w='Bold', bg=CARD)
    m2 = hl(2) * (1 - hl(3))
    random.seed(11)
    nodes = [(560 + 260 * math.cos(k * 2 * math.pi / 9), 560 + 200 * math.sin(k * 2 * math.pi / 9)) for k in range(9)]
    nodes2 = [(x + 800, y) for x, y in nodes]
    pairs = [(0, 3), (1, 5), (2, 7), (4, 8), (3, 6), (0, 5), (2, 4), (6, 8), (1, 7)]
    old = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8), (8, 0), (4, 5)]
    morph = fd(T(2), 1.0, 2.0)
    for (i, j) in old: c.line([nodes[i], nodes[j]], DIM, 4, m2 * (1 - morph))
    for (i, j) in pairs: c.line([nodes[i], nodes[j]], BRN, 5, m2 * morph)
    for (i, j) in pairs: c.line([nodes2[i], nodes2[j]], ITEM, 5, m2)
    for n in nodes: c.circ(n[0], n[1], 18, BRN, m2)
    for n in nodes2: c.circ(n[0], n[1], 18, ITEM, m2)
    c.text(560, 820, 'trained person', 32, BRN, m2, w='Bold'); c.text(1360, 820, 'champion pattern', 32, ITEM, m2, w='Bold')
    m3 = hl(3)
    c.text(300, 430, 'the study', 38, ROUTE, m3, 'lm', 'Bold'); c.rr(300, 470, 300 + 160 * fd(T(3), .2, .5), 540, 14, ROUTE, m3)
    c.text(300 + 180, 505, '40 days', 36, ROUTE, m3 * fd(T(3), .6), 'lm', 'Bold')
    c.text(300, 640, 'memory champions', 38, ITEM, m3, 'lm', 'Bold'); c.rr(300, 680, 300 + 1240 * fd(T(3), 1.2, 2.0), 750, 14, ITEM, m3)
    c.text(960, 830, 'months and years of practice', 36, ITEM, m3 * fd(T(3), 2.6), w='Bold')
    c.text(1880, 858, 'Connection patterns illustrative', 28, DIM, m2, anchor='rm', w='Regular')

def s_recall(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Now ', INK), ('walk back', ROUTE), (' through', INK)], sw_out(T, 2))
    headline(c, [('What did you ', INK), ('need', ITEM), ('?', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('You ', INK), ('remembered', ANS)], sw_in(T, 3))
    lit = [fd(T(1), .3 + .7 * k, .3) for k in range(5)]
    P = house(c, 1, lit=lit)
    route(c, P, fd(T(1), .1, 3.4) if T(1) > 0 else fd(T(0), .3, 1.0) * .05, 1, t=t)
    for k in range(5): stop_num(c, P, k, 1 - hl(3))
    q = hl(2) * (1 - hl(3))
    if q > .01 and T(2) > 0:
        e = T(2) - 2.0; n = 3 - int(max(0, e) / 1.0) if e > 0 else 3
        c.circ(1760, 360, 70, ITEM, q * fd(T(2), 1.6)); c.text(1760, 360, str(max(1, n)), 70, DARK, q * fd(T(2), 1.6), w='Bold', bg=ITEM)
    for k in range(5):
        a = fd(T(3), .1 + .45 * k, .3) if T(3) > 0 else 0
        item_at(c, P, k, a, t, s=.9)
        if a > .01:
            x, y = P(STOPS[k][0], STOPS[k][1]); c.circ(x + 60, y - 60, 22, ANS, a, bg=FLOOR); c.check(x + 60, y - 60, 20, DARK, a, 1)

def s_recap(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', ITEM)], 1)
    items = ((1, 'Champions aren\'t born with different brains.', BRN), (2, 'Pictures in places you know, in order.', ROUTE),
             (3, 'In 40 days, recall more than doubled.', ANS))
    for ln, txt, col in items:
        m = hl(ln); x0 = 140 + (ln - 1) * 560; dy = 50 * (1 - m)
        c.rr(x0, 290 + dy, x0 + 520, 800 + dy, 30, CARD, m, outline=col, ow=5)
        c.circ(x0 + 260, 380 + dy, 50, col, m, bg=CARD); c.text(x0 + 260, 380 + dy, str(ln), 56, DARK, m, w='Bold', bg=col)
        if ln == 1: brain(c, x0 + 190, 530 + dy, 60, m, bg=CARD); brain(c, x0 + 330, 530 + dy, 60, m, bg=CARD)
        if ln == 2: milk(c, x0 + 200, 540 + dy, .8, m, bg=CARD); c.circ(x0 + 320, 540 + dy, 30, ROUTE, m, bg=CARD); c.text(x0 + 320, 540 + dy, '1', 36, DARK, m, w='Bold', bg=ROUTE)
        if ln == 3:
            c.rr(x0 + 170, 600 + dy - 50, x0 + 230, 600 + dy, 6, DIM, m, bg=CARD); c.rr(x0 + 290, 600 + dy - 120, x0 + 350, 600 + dy, 6, ANS, m, bg=CARD)
        for j, l in enumerate(wrap(c, txt, 38, 460, 'Bold')):
            c.text(x0 + 260, 665 + dy + j * 48, l, 38, INK, m, w='Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    P = lambda x, y: (1500 + (x - 960) * .42, 560 + (y - 580) * .55)
    x0, y0 = P(360, 300); x1, y1 = P(1600, 840)
    c.rr(x0, y0, x1, y1, 14, FLOOR, 1, outline=WALL, ow=6)
    pts = [P(x, y) for x, y, _ in STOPS]
    for i in range(4): c.line([pts[i], pts[i + 1]], ROUTE, 8, 1, bg=FLOOR)
    for k, (x, y) in enumerate(pts):
        c.circ(x, y, 34, ROUTE, 1, bg=FLOOR); c.text(x, y, str(k + 1), 36, DARK, 1, w='Bold', bg=ROUTE)
    milk(c, pts[0][0] - 70, pts[0][1] - 40, 1.0, 1, bg=FLOOR); banana(c, pts[2][0], pts[2][1] - 70, .9, 1, bg=FLOOR)
    sock(c, pts[3][0] + 70, pts[3][1] - 40, .9, 1, bg=FLOOR)

SCENES = [
 ('THE HOOK', ["Top memory competitors can learn about a hundred words in five minutes.",
               "But brain scans suggest their brains are built much like yours.",
               "The difference is a trick.",
               "And you'll use it in this video."], s_hook),
 ('NOT SMARTER', ["In two thousand and three, scientists scanned memory champions and ordinary people.",
                  "The champions weren't smarter overall.",
                  "And their brain structure showed no important difference.",
                  "But while memorising, they used more of the brain's areas for places and routes.",
                  "Most were walking through a place in their mind."], s_scan),
 ('THE LEGEND', ["The trick is ancient. Its story starts with a Greek poet, Simonides.",
                 "He stepped out of a banquet, just before the hall collapsed.",
                 "No one could recognise the guests.",
                 "But Simonides remembered where each person had been sitting.",
                 "The Roman writer Cicero told this story. It's probably a legend. But the method is real."], s_legend),
 ('THE METHOD', ["It's called the memory palace, or the method of loci. Loci means places.",
                 "First, pick a place you know well, like your home.",
                 "Choose stops in a fixed order. Front door. Sofa. Kitchen sink. Bed. Shower.",
                 "Put one thing at each stop, as a strange, vivid picture.",
                 "To remember, you walk the route in your mind."], s_method),
 ('TRY IT', ["Let's try it. Here are five things to buy.",
             "Milk. Batteries. Bananas. Socks. Stamps."], s_try),
 ('YOUR HOUSE', ["Front door: milk pours out of the letterbox.",
                 "Sofa: batteries buzz like bees in the cushions.",
                 "Kitchen sink: bananas spin down the drain.",
                 "Bed: a giant sock is your blanket.",
                 "Shower: the walls are covered in stamps."], s_place),
 ('WHY IT WORKS', ["Why does this work?",
                   "A bare word is easy to lose.",
                   "The method turns each word into a picture, and gives every picture an address.",
                   "And the route keeps them in order."], s_why),
 ('THE TEST', ["Can ordinary people learn it? A twenty seventeen study tested that.",
               "People with normal memories trained for thirty minutes a day, for forty days.",
               "Before training, they recalled about twenty-six words from a list of seventy-two.",
               "After the memory palace training, about sixty-two.",
               "A group doing short-term memory games gained about eleven. No training, about seven."], s_study),
 ('THE CATCH', ["Four months later, with no more training,",
                "the memory palace group still recalled over twenty-two more words than at the start.",
                "Brain shape didn't change. But their connection patterns became more like the champions'.",
                "The catch: it takes practice. Champions trained for months and years."], s_later),
 ('YOUR TURN', ["Now, walk back through your home.",
                "Front door. Sofa. Kitchen sink. Bed. Shower.",
                "What did you need to buy?",
                "Milk, batteries, bananas, socks and stamps. You just used a memory palace."], s_recall),
 ('RECAP', ["Three things to keep.",
            "One: memory champions aren't born with different brains.",
            "Two: they put vivid pictures in places they know, in a fixed order.",
            "Three: in forty days, ordinary people more than doubled their recall.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('100 words', ITEM), (' in 5 minutes', INK)], sw_out(T, 1), size=96)
    headline(c, [('Not ', INK), ('smarter', BRN), ('. A ', INK), ('trick', ROUTE)], sw_in(T, 1), size=92)
    n = min(100, int(4 + t * 30))
    c.rr(760, 380, 1160, 600, 30, DARK, 1 - hl(1), outline=ITEM, ow=5)
    c.text(960, 455, str(n), 110, ITEM, 1 - hl(1), w='Bold', bg=DARK); c.text(960, 550, 'words', 36, DIM, 1 - hl(1), w='Bold', bg=DARK)
    random.seed(3)
    for k in range(14):
        u = (t * .35 + k / 14) % 1; px = 160 + 1600 * u; py = 300 + (k * 97) % 500
        if 700 < px < 1220 and 340 < py < 640: continue
        c.rr(px - 66, py - 26, px + 66, py + 26, 14, CARD, .9 * math.sin(u * math.pi), outline=ITEM, ow=2)
    m1 = hl(1)
    brain(c, 640, 560, 140, m1, spot=m1); brain(c, 1280, 560, 140, m1)
    c.text(960, 560, '=', 110, ANS, m1, w='Bold')

def short_route(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A place ', INK), ('you know', ROUTE)], sw_out(T, 1), size=96)
    headline(c, [('Stops ', INK), ('in order', ROUTE)], sw_in(T, 1), size=96)
    lit = [fd(T(1), .6 + .55 * k, .3) for k in range(5)]
    P = house(c, 1, lit=lit)
    for k in range(5): stop_num(c, P, k, lit[k])
    route(c, P, fd(T(1), .6, 2.8), hl(1), t=t)

def short_pics(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('One ', INK), ('strange picture', ITEM), (' each', INK)], sw_out(T, 1), size=92)
    headline(c, [('Walk it', ROUTE), (' to recall', INK)], sw_in(T, 1), size=96)
    P = house(c, 1, lit=[1] * 5)
    for k in range(5): item_at(c, P, k, fd(T(0), 1.6 + .5 * k, .4), t, s=.9)
    route(c, P, fd(T(1), .2, 2.6) if T(1) > 0 else 0, 1, t=t)

def short_study(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('40 days', ROUTE), (' of training', INK)], sw_out(T, 1), size=96)
    headline(c, [('26', DIM), (' words to ', INK), ('62', ANS)], sw_in(T, 1), size=100)
    base, top = 800, 320; sc = (base - top) / 72
    c.line([(400, base), (1520, base)], DIM, 3, 1)
    c.rr(620, base - 26 * sc, 860, base, 12, DIM, 1); c.text(740, base - 26 * sc - 40, '26', 54, DIM, 1, w='Bold')
    h = 62 * sc * fd(T(1), .3, .9)
    c.rr(1060, base - h, 1300, base, 12, ANS, hl(1)); c.text(1180, base - h - 40, '62', 64, ANS, hl(1) * fd(T(1), .9), w='Bold')
    c.text(740, base + 40, 'before', 36, DIM, 1, w='Bold'); c.text(1180, base + 40, 'after', 36, ANS, hl(1), w='Bold')
    c.text(960, 280, 'words recalled from a list of 72 (Dresler et al., 2017)', 32, DIM, 1, w='Bold')

SHORT_SCENES = [
 ('THE HOOK', ["How do memory champions learn about a hundred words in five minutes?",
               "Their brains aren't built differently. They use a trick called the memory palace."], short_hook),
 ('THE PLACE', ["Pick a place you know well, like your home.",
                "Choose stops in a fixed order: front door, sofa, kitchen sink, bed, shower."], short_route),
 ('THE PICTURES', ["Turn each thing you need to remember into a strange picture at one stop. Milk pouring from the door. Batteries buzzing in the sofa.",
                   "To remember, walk the route in your mind."], short_pics),
 ('THE PROOF', ["In a twenty seventeen study, ordinary people practised this for forty days.",
                "Their recall went from about twenty-six words to sixty-two."], short_study),
 ('THE ANSWER', ["So the secret isn't a special brain.",
                 "It's pictures, in places you know."], card('Not a special brain.', 'Pictures in places.')),
]
SHORT_HITS = [(4, 1, 0.0)]
