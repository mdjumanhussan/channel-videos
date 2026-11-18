"""Episode: Sore Two Days Later? It's Not Lactic Acid (the timing mismatch, the downhill clue, braking movements, tiny damage and repair, fast adaptation)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why soreness waits'                           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Why do muscles hurt days later?'               # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 0, 0.0), (6, 2, 0.0)]               # 'long gone', the quiz answer (down), 'that's the delay'
THUMB = ['SORE 2 DAYS LATER?', "IT'S NOT", 'LACTIC ACID']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.3, (1, 2): 0.3, (2, 2): 0.3, (3, 1): 0.3, (4, 0): 3.2, (5, 0): 0.3, (6, 1): 0.3, (7, 1): 0.3}
SHORT_PAUSES = {(0, 1): 0.3, (1, 2): 0.3}
CAPTION_FIXES = {'nineteen eighty-three': '1983', 'six to eight hours': '6 to 8 hours'}

# Colour code kept in every scene (lesson of 2026-11-01):
# lactic acid is purple, soreness/pain is pink, braking (eccentric) movements are yellow,
# repair is green, time and the body are cyan / pale blue.
LAC = PU; SORE = PK; BRAKE = YE; FIX = GR; TIME = CY
DARK = (20, 22, 38); QUIZ = (24, 52, 60); MUS = (176, 72, 92); MUS_L = (214, 112, 128); TEND = (226, 222, 210)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0
# A new visual element every 2 to 4 seconds (lesson applied 2026-11-19, OpusClip): staged reveals use st(T, i, offset).
st = lambda T, i, off=0.0, d=.45: fd(T(i), off, d) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def walker(c, x, y, s, col, a, ph=0.0, face=1, bg=BG, lean=0.0, sore=0.0):
    """Stick figure standing on (x, y), height s. ph animates the stride; sore > 0 flashes the thighs pink."""
    if a <= .01: return
    w = max(4, int(s * .07)); hip = (x + lean * s * .1, y - s * .45); neck = (x + lean * s * .2, y - s * .8)
    c.circ(neck[0] + face * s * .02, neck[1] - s * .11, s * .1, col, a, bg=bg)
    c.line([neck, hip], col, w, a, bg=bg)
    sw = math.sin(ph) * .22
    for k, sg in enumerate((1, -1)):
        kx = hip[0] + face * s * (sg * sw + .06); ky = hip[1] + s * .22
        fx = hip[0] + face * s * (sg * sw * 1.4 - .02); fy = y
        lc = mix(SORE, sore, col) if sore > .01 else col
        c.line([hip, (kx, ky)], lc, w + (3 if sore > .01 else 0), a, bg=bg)
        c.line([(kx, ky), (fx, fy)], col, w, a, bg=bg)
    for sg in (1, -1):
        c.line([(neck[0], neck[1] + s * .06), (neck[0] + face * s * (-sg * sw * .9), neck[1] + s * .3)], col, w, a, bg=bg)

def stairs(c, x0, y0, n, sw, sh, a, col=(58, 66, 110), down=False, bg=BG):
    """Staircase whose base runs from x0 rightwards at floor y0. Rises to the right (or falls if down)."""
    if a <= .01: return
    pts = [(x0, y0)]
    for k in range(n):
        lvl = (n - k) if down else (k + 1)
        x = x0 + k * sw
        pts += [(x, y0 - lvl * sh), (x + sw, y0 - lvl * sh)]
    pts += [(x0 + n * sw, y0)]
    poly(c, pts, col, a, bg)

def step_pos(x0, y0, n, sw, sh, u, down=False):
    """Position on the staircase tread at progress u (0..1)."""
    k = min(n - 1, int(u * n)); lvl = (n - k) if down else (k + 1)
    return x0 + (k + .5) * sw, y0 - lvl * sh

def capsule_muscle(c, x0, y, x1, h, a, tears=0.0, fibres=6, bg=BG, t=0.0, glow=0.0):
    """Side view of a muscle: a pink capsule with fibre lines and pale tendons at both ends.
    tears: 0..1 draws tiny pink breaks in the fibres; glow: 0..1 adds a soft pink halo (soreness)."""
    if a <= .01: return
    if glow > .01:
        for r in (3, 2, 1):
            c.rr(x0 - 8 * r, y - h / 2 - 8 * r, x1 + 8 * r, y + h / 2 + 8 * r, h / 2 + 8 * r, SORE, a * glow * .12 * (1 + .3 * math.sin(t * 4)), bg=bg)
    c.rr(x0 - 90, y - h * .12, x0 + 20, y + h * .12, h * .12, TEND, a, bg=bg)
    c.rr(x1 - 20, y - h * .12, x1 + 90, y + h * .12, h * .12, TEND, a, bg=bg)
    c.rr(x0, y - h / 2, x1, y + h / 2, h / 2, MUS, a, bg=bg)
    for k in range(fibres):
        yy = y - h / 2 + h * (k + 1) / (fibres + 1)
        inset = h / 2 * (1 - math.sqrt(max(0, 1 - ((yy - y) / (h / 2)) ** 2))) + 18
        c.line([(x0 + inset, yy), (x1 - inset, yy)], MUS_L, max(3, int(h / 40)), a, bg=MUS)
    if tears > .01:
        rnd = random.Random(7)
        for k in range(9):
            fx = rnd.uniform(x0 + h * .5, x1 - h * .5); fk = rnd.randint(1, fibres - 1)
            yy = y - h / 2 + h * fk / (fibres + 1) + h / (fibres + 1) / 2
            ta = a * clamp(tears * 9 - k)
            c.line([(fx - 14, yy - 10), (fx - 4, yy + 8), (fx + 6, yy - 8), (fx + 14, yy + 10)], SORE, 5, ta, bg=MUS)

def tag(c, x, y, txt, col, a, sub=None, bg=BG, w=300, size=40):
    if a <= .01: return
    c.rr(x - w / 2, y - 48, x + w / 2, y + 48, 22, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - (12 if sub else 0), txt, size, col, a, w='Bold', bg=CARD)
    if sub: c.text(x, y + 26, sub, 26, DIM, a, w='Bold', bg=CARD)

def day_tile(c, x, y, day, note, col, a, w=280, bg=BG, icon=None, t=0.0):
    if a <= .01: return
    c.rr(x - w / 2, y - 110, x + w / 2, y + 110, 26, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - 70, day, 36, DIM, a, w='Bold', bg=CARD)
    c.text(x, y + 70, note, 40, col, a, w='Bold', bg=CARD)
    if icon == 'hike':   # a little hill with a flag
        poly(c, [(x - 90, y + 32), (x - 10, y - 14), (x + 30, y + 8), (x + 60, y - 4), (x + 100, y + 32)], (60, 120, 100), a, CARD)
        c.line([(x - 10, y - 14), (x - 10, y - 40)], INK, 4, a, bg=CARD); poly(c, [(x - 10, y - 40), (x + 18, y - 32), (x - 10, y - 24)], YE, a, CARD)
    if icon == 'ok': c.check(x, y - 6, 40, GR, a)
    if icon == 'ouch':
        r = 34 * (1 + .12 * math.sin(t * 6))
        for k in range(8):
            ang = k * math.pi / 4
            c.line([(x + math.cos(ang) * r * .6, y - 6 + math.sin(ang) * r * .6), (x + math.cos(ang) * r * 1.3, y - 6 + math.sin(ang) * r * 1.3)], SORE, 6, a, bg=CARD)
        c.circ(x, y - 6, r * .45, SORE, a, bg=CARD)

def dots(c, cx, cy, rx, ry, n, col, a, t=0.0, seed=3, drift=0.0, bg=BG):
    """A cloud of small molecules (used for lactic acid). drift > 0 floats them up and away."""
    if a <= .01: return
    rnd = random.Random(seed)
    for k in range(n):
        x = cx + rnd.uniform(-rx, rx) + 6 * math.sin(t * 2 + k); y = cy + rnd.uniform(-ry, ry) + 6 * math.cos(t * 1.7 + k)
        y -= drift * rnd.uniform(40, 110); aa = a * (1 - drift) ** 2 if drift else a
        c.circ(x, y, rnd.uniform(9, 15), col, aa, bg=bg)

def clock(c, x, y, r, a, hours=1.0, col=TIME, bg=BG, label=None):
    """Clock face; the hand sweeps 'hours' turns (one turn = one hour on this dial)."""
    if a <= .01: return
    c.circ(x, y, r, CARD, a, outline=col, ow=5, bg=bg)
    for k in range(12):
        ang = k * math.pi / 6
        c.line([(x + math.sin(ang) * r * .78, y - math.cos(ang) * r * .78), (x + math.sin(ang) * r * .9, y - math.cos(ang) * r * .9)], DIM, 3, a, bg=CARD)
    ang = hours * 2 * math.pi
    c.line([(x, y), (x + math.sin(ang) * r * .72, y - math.cos(ang) * r * .72)], col, 6, a, bg=CARD)
    c.circ(x, y, 7, col, a, bg=CARD)
    if label: c.text(x, y + r + 34, label, 32, col, a, w='Bold')

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: the familiar delay, shown as three day tiles, then the myth and why it fails."""
    headline(c, [('Day 2: ', INK), ('the stairs hurt', SORE)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Blame ', INK), ('lactic acid', LAC), ('?', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('By then it\'s ', INK), ('long gone', LAC)], sw_in(T, 2))
    for k, (day, note, col, icon) in enumerate((('SATURDAY', 'long hike', TIME, 'hike'), ('SUNDAY', 'fine', GR, 'ok'), ('MONDAY', 'ouch', SORE, 'ouch'))):
        a = st(T, 0, .1 + 1.1 * k)
        day_tile(c, 330 + k * 320, 430 + 20 * (1 - a), day, note, col, a, icon=icon, t=t)
    # stairs on the right with a walker climbing slowly
    sa = st(T, 0, .6)
    stairs(c, 1270, 820, 5, 110, 70, sa)
    u = clamp(.2 + .12 * t, 0, .9); px, py = step_pos(1270, 820, 5, 110, 70, u)
    walker(c, px, py, 220, INK, sa, ph=t * 2.2, sore=st(T, 0, 3.0) * (.6 + .4 * math.sin(t * 5) ** 2))
    # lactic acid molecules near the legs, then drifting away
    m1 = st(T, 1); m2 = st(T, 2, 0, 1.6)
    if m1 > .01:
        dots(c, 650, 700, 260, 60, 18, LAC, m1, t=t, drift=m2 * .95)
        c.text(650, 800, 'lactic acid', 40, LAC, m1 * (1 - m2), w='Bold')
    if T(2) > -.1:
        tag(c, 650, 760, 'back to normal in about an hour', LAC, st(T, 2, 1.0), w=620, size=36)

def s_myth(c, T, t):
    headline(c, [('Work hard, make ', INK), ('lactate', LAC)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('It ', INK), ('builds up', LAC), (' while you push', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Then it ', INK), ('clears fast', LAC)], sw_in(T, 2))
    # left: someone running for a bus
    a0 = st(T, 0)
    c.rr(120, 500, 600, 700, 30, (60, 110, 170), a0 * fd(T(0), .4)); c.rr(150, 530, 560, 600, 12, (150, 200, 240), a0 * fd(T(0), .4), bg=(60, 110, 170))
    for wx in (210, 500): c.circ(wx, 710, 36, DARK, a0 * fd(T(0), .4)); c.circ(wx, 710, 14, DIM, a0 * fd(T(0), .4), bg=DARK)
    c.text(360, 470, 'BUS', 34, INK, a0 * fd(T(0), .6), w='Bold')
    walker(c, 760, 740, 260, INK, st(T, 0, 1.2), ph=t * 9, face=-1, lean=-1.2)
    # right: a muscle filling with lactate, then emptying
    ma = st(T, 0, 2.2)
    capsule_muscle(c, 1060, 420, 1700, 200, ma)
    fill = st(T, 1, 0, 2.0) * (1 - st(T, 2, 1.2, 2.5))
    if fill > .01: dots(c, 1380, 420, 280, 60, int(6 + 22 * fill), LAC, ma * clamp(fill * 2), t=t, seed=5, bg=MUS)
    c.text(1380, 580, 'lactate (often called lactic acid)', 32, LAC, st(T, 0, 2.8), w='Bold')
    if T(2) > -.1:
        clock(c, 1380, 740, 70, st(T, 2, .4), hours=clamp(T(2) / 3.0), label=None)
        c.text(1560, 740, 'about 1 hour', 40, LAC, st(T, 2, 1.6), 'lm', 'Bold')
        c.text(960, 870, 'Schwane et al., 1983: back to pre-exercise levels within an hour', 26, DIM, st(T, 2, 2.0), w='Regular')

def s_timeline(c, T, t):
    headline(c, [('Compare the ', INK), ('timing', TIME)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Lactic acid: ', LAC), ('gone in about an hour', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3), size=72)
    headline(c, [('Soreness: ', SORE), ('peaks about 2 days later', INK)], sw_in(T, 2) * sw_out(T, 3), size=72)
    headline(c, [('They ', INK), ("don't line up", BRAKE)], sw_in(T, 3))
    x0, x1, y0 = 300, 1660, 720; a0 = st(T, 0)
    X = lambda h: x0 + (x1 - x0) * h / 72.0
    c.line([(x0, y0), (x1, y0)], DIM, 4, a0); c.line([(x0, y0), (x0, 300)], DIM, 4, a0)
    for h, lab in ((0, 'workout'), (24, 'day 1'), (48, 'day 2'), (72, 'day 3')):
        c.line([(X(h), y0), (X(h), y0 + 16)], DIM, 4, a0); c.text(X(h), y0 + 48, lab, 32, DIM, a0, w='Bold')
    # lactate: a quick spike right after exercise (gone within an hour, so it is a sliver at this scale)
    m1 = st(T, 1)
    if m1 > .01:
        pts = [(X(0), y0), (X(.25), y0 - 330 * m1), (X(1.0), y0)]
        poly(c, pts, LAC, m1)
        c.arrow(X(5) + 70, y0 - 300, X(1.2) + 8, y0 - 300, LAC, 5, st(T, 1, .6))
        c.text(X(5) + 80, y0 - 300, 'lactic acid', 36, LAC, st(T, 1, .6), 'lm', 'Bold')
    # soreness: starts hours later, builds to a peak around day 2 (illustrative shape)
    m2 = st(T, 2, 0, 2.6)
    if m2 > .01:
        pts = []
        for k in range(73):
            h = k
            if h > 72 * m2: break
            v = 0 if h < 7 else math.sin(clamp((h - 7) / 70.0) * math.pi * .78) ** 1.4
            pts.append((X(h), y0 - 330 * v))
        if len(pts) > 1: c.line(pts, SORE, 9, 1)
        c.text(X(40), y0 - 380, 'soreness', 36, SORE, st(T, 2, 1.4), w='Bold')
        c.text(X(2), y0 - 110, 'starts 6 to 8 h later', 26, SORE, st(T, 2, .4), 'lm', 'Bold')
        c.text(1660, 300, 'Illustrative shape', 26, DIM, st(T, 2, .2), 'rm', 'Regular')
    m3 = st(T, 3)
    if m3 > .01:
        c.line([(X(1), y0 - 420), (X(45), y0 - 420)], BRAKE, 5, m3)
        for xx in (X(1), X(45)): c.line([(xx, y0 - 440), (xx, y0 - 400)], BRAKE, 5, m3)
        c.text(X(23), y0 - 455, 'about 2 days apart', 34, BRAKE, m3, w='Bold')

def slope(c, a, bg=BG):
    poly(c, [(220, 400), (1140, 790), (1140, 840), (220, 840)], (50, 96, 84), a, bg)

def s_clue(c, T, t):
    headline(c, [('A clue: ', INK), ('running downhill', BRAKE)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Lactic acid: ', LAC), ('no rise', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Soreness: ', SORE), ('some of the worst', INK)], sw_in(T, 2))
    a0 = st(T, 0)
    slope(c, a0)
    u = (t * .07) % 1.0; px = 300 + 760 * u; py = 400 + (790 - 400) * (px - 220) / 920
    walker(c, px, py, 200, INK, a0 * fd(T(0), .5), ph=t * 8, face=1, lean=.6, sore=st(T, 2, .5) * (.6 + .4 * math.sin(t * 5) ** 2))
    c.text(680, 870, 'Schwane et al., 1983', 26, DIM, st(T, 0, 2.0), w='Regular')
    # right: blood test card with a flat lactate line
    m1 = st(T, 1)
    if m1 > .01:
        c.rr(1260, 300, 1740, 560, 26, CARD, m1, outline=LAC, ow=4)
        c.text(1500, 345, 'blood lactic acid', 34, LAC, m1, w='Bold', bg=CARD)
        c.line([(1300, 480), (1700, 480)], (70, 80, 130), 3, m1, bg=CARD)
        pr = st(T, 1, .3, 1.6); c.line([(1300, 470), (1300 + 400 * pr, 470)], LAC, 7, m1, bg=CARD)
        c.text(1500, 520, 'flat', 32, INK, st(T, 1, 1.4), w='Bold', bg=CARD)
    m2 = st(T, 2, .3)
    if m2 > .01:
        c.rr(1260, 600, 1740, 820, 26, CARD, m2, outline=SORE, ow=4)
        c.text(1500, 645, 'soreness after', 34, SORE, m2, w='Bold', bg=CARD)
        for k in range(5):
            on = k < int(1 + 4 * st(T, 2, .8, 1.6))
            c.rr(1320 + k * 76, 700, 1380 + k * 76, 780, 12, SORE if on else (60, 66, 100), m2, bg=CARD)

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a teal pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Sorer later: walking ', INK), ('up', TIME), (' or ', INK), ('down', BRAKE), ('?', INK)], 1, bg=QUIZ, size=74)
    for k, (lab, col, down) in enumerate((('Up the stairs', TIME, False), ('Down the stairs', BRAKE, True))):
        x = 560 + k * 800
        c.rr(x - 320, 290, x + 320, 700, 30, CARD, 1, outline=col, ow=5, bg=QUIZ)
        stairs(c, x - 220, 580, 4, 110, 55, 1, (58, 66, 110), down=down, bg=CARD)
        u = (t * .25) % 1.0; px, py = step_pos(x - 220, 580, 4, 110, 55, u, down=down)
        walker(c, px, py, 150, col, 1, ph=t * 4, bg=CARD)
        c.text(x, 650, lab, 44, col, 1, w='Bold', bg=CARD)
    if T(0) > 0:
        e = T(0) - 5.2; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 5.0)
        c.circ(960, 790, 60, BRAKE, u, bg=QUIZ); c.text(960, 790, str(k) if k else '?', 60, DARK, u, w='Bold', bg=BRAKE)

def s_brake(c, T, t):
    headline(c, [('Down', BRAKE), (' is worse', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Working while ', INK), ('stretching', BRAKE)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Braking', BRAKE), (' movements', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('More ', INK), ('tiny damage', SORE)], sw_in(T, 3))
    m1 = st(T, 1)
    m0 = 1 - m1
    if m0 > .01:
        for k, (lab, col, down) in enumerate((('up', DIM, False), ('down', BRAKE, True))):
            x = 560 + k * 800; a = m0 * st(T, 0, .3 * k)
            stairs(c, x - 260, 760, 5, 104, 64, a, down=down)
            u = (t * .2) % 1.0; px, py = step_pos(x - 260, 760, 5, 104, 64, u, down=down)
            walker(c, px, py, 190, INK if k else DIM, a, ph=t * 4, sore=(st(T, 0, 1.2) * (.6 + .4 * math.sin(t * 5) ** 2)) if k else 0)
            c.text(x, 820, lab, 44, col, a, w='Bold')
        c.text(960, 520, 'feels harder', 34, DIM, m0 * st(T, 0, 2.0), w='Bold'); c.arrow(860, 520, 700, 520, DIM, 4, m0 * st(T, 0, 2.0))
    if m1 > .01:
        # a muscle that lengthens while it works, with yellow brake arrows
        stretch = .5 + .5 * math.sin(t * 1.6)
        L = 260 + 120 * stretch
        capsule_muscle(c, 960 - L, 440, 960 + L, 170 - 30 * stretch, m1, tears=st(T, 3, .4, 2.0), t=t)
        for s in (-1, 1):
            c.arrow(960 + s * (L + 130), 440, 960 + s * (L + 230), 440, BRAKE, 7, m1)
        c.text(960, 560, 'pulling while being pulled longer', 34, BRAKE, m1 * st(T, 1, 1.2), w='Bold')
        m2 = st(T, 2)
        if m2 > .01:
            for k, lab in enumerate(('walking downhill', 'going down stairs', 'lowering a heavy box')):
                tag(c, 420 + k * 540, 690, lab, BRAKE, m2 * st(T, 2, .8 + .7 * k), w=480, size=34)
            c.text(960, 790, 'scientists call these eccentric movements', 30, DIM, m2 * st(T, 2, 2.2), w='Bold')
        if T(3) > -.1:
            c.text(960, 860, 'More muscle cell damage than shortening (lifting) movements', 26, DIM, st(T, 3, .6), w='Regular')

def s_repair(c, T, t):
    headline(c, [('Tiny damage', SORE), (' in the muscle', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Repair', FIX), (' and ', INK), ('touchy nerves', TIME)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Repair takes ', FIX), ('a day or two', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('The timing points ', INK), ('here', FIX)], sw_in(T, 3))
    a0 = st(T, 0)
    glow = st(T, 1, 1.2, 1.5)
    capsule_muscle(c, 420, 440, 1500, 220, a0, tears=st(T, 0, .8, 2.0), t=t, glow=glow)
    c.text(300, 600, 'tendon', 30, TEND, st(T, 0, 2.4), w='Bold'); c.text(960, 600, 'muscle fibres', 30, MUS_L, st(T, 0, 2.4), w='Bold')
    m1 = st(T, 1)
    if m1 > .01:
        rnd = random.Random(11)
        for k in range(14):
            sx, sy = rnd.uniform(500, 1420), rnd.uniform(380, 500)
            ox, oy = rnd.uniform(-200, 200), rnd.uniform(-260, 260)
            g = st(T, 1, .2 + .08 * k, 1.0)
            c.circ(sx + ox * (1 - g), sy + oy * (1 - g), 11, FIX, m1 * g, bg=MUS)
        # a nerve line that lights up
        pts = [(380 + k * 40, 300 + 18 * math.sin(k * 1.3)) for k in range(30)]
        c.line(pts, mix(TIME, .4 + .6 * glow * (.6 + .4 * math.sin(t * 6) ** 2)), 6, m1 * st(T, 1, 1.0))
        c.text(1560, 300, 'nerve endings', 32, TIME, m1 * st(T, 1, 1.4), 'lm', 'Bold')
    m2 = st(T, 2)
    if m2 > .01:
        c.rr(460, 700, 1460, 760, 30, CARD, m2, outline=(70, 80, 130), ow=3)
        c.rr(466, 706, 466 + 988 * st(T, 2, .3, 3.0), 754, 26, FIX, m2, bg=CARD)
        for k, lab in enumerate(('workout', 'day 1', 'day 2')):
            c.text(470 + k * 495, 800, lab, 30, DIM, m2, w='Bold')
    m3 = st(T, 3)
    if m3 > .01:
        c.text(960, 860, 'The exact details are still debated. Most research points to tiny muscle damage.', 26, DIM, m3, w='Regular')

def s_adapt(c, T, t):
    headline(c, [('Muscles ', INK), ('adapt fast', FIX)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Second time: ', INK), ('much less sore', FIX)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Soreness is ', INK), ('not a score', BRAKE)], sw_in(T, 2))
    m2 = st(T, 2); mb = 1 - m2
    if mb > .01:
        for k, (lab, v, sub) in enumerate((('first hike', .9, ''), ('same hike again', .3, 'within ~2 weeks'))):
            x = 640 + k * 640; a = mb * st(T, 0 if k == 0 else 1, .3)
            hh = 380 * v * st(T, 0 if k == 0 else 1, .5, .9)
            c.rr(x - 120, 780 - max(hh, 8), x + 120, 780, 18, SORE, a)
            c.text(x, 820, lab, 38, INK, a, w='Bold')
            if sub: c.text(x, 862, sub, 28, FIX, a, w='Bold')
            c.text(x, 780 - max(hh, 8) - 34, 'soreness', 30, SORE, a * st(T, 0 if k == 0 else 1, 1.0), w='Bold')
        c.text(1700, 300, 'Illustrative', 26, DIM, mb * st(T, 0, .5), 'rm', 'Regular')
    if m2 > .01:
        # a scoreboard crossed out, and a stronger arm
        c.rr(300, 330, 860, 700, 30, CARD, m2, outline=SORE, ow=4)
        c.text(580, 420, 'SORENESS', 44, SORE, m2, w='Bold', bg=CARD); c.text(580, 540, '10 / 10', 80, INK, m2, w='Bold', bg=CARD)
        c.line([(330, 680), (830, 350)], SORE, 10, m2 * st(T, 2, .8))
        tag(c, 1340, 470, 'muscles can grow', FIX, m2 * st(T, 2, 1.4), w=620, size=44)
        tag(c, 1340, 600, 'without much soreness', FIX, m2 * st(T, 2, 2.0), w=620, size=44)

def s_recap(c, T, t):
    """Recap as three stops on a path (the last recap used stacked rows)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', BRAKE)], 1)
    items = ((1, ['Lactic acid clears', 'within about an hour'], LAC), (2, ['Braking movements', 'make the most soreness'], BRAKE),
             (3, ['The ache is repair,', 'and muscles adapt fast'], FIX))
    c.line([(380, 400), (1540, 400)], (60, 70, 120), 6, 1)
    c.line([(380, 400), (380 + 1160 * clamp(hl(1) * .1 + hl(2) * .45 + hl(3) * .45), 400)], INK, 6, hl(1))
    for ln, txt, col in items:
        m = hl(ln); x = 380 + (ln - 1) * 580
        c.circ(x, 400, 56, col, m); c.text(x, 400, str(ln), 60, DARK, m, w='Bold', bg=col)
        c.rr(x - 270, 500, x + 270, 720, 28, CARD, m, outline=col, ow=4)
        for j, s in enumerate(txt): c.text(x, 570 + j * 76 + 20 * (1 - m), s, 38, INK if j else col, m, w='Bold', bg=CARD)
    c.text(960, 840, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    stairs(c, 1180, 900, 5, 130, 90, 1)
    px, py = step_pos(1180, 900, 5, 130, 90, .5)
    walker(c, px, py, 330, INK, 1, ph=.8, sore=1)
    for k in range(8):
        ang = k * math.pi / 4; x, y = px + 10, py - 190
        c.line([(x + math.cos(ang) * 50, y + math.sin(ang) * 50), (x + math.cos(ang) * 95, y + math.sin(ang) * 95)], SORE, 9, 1)

SCENES = [
 ('THE DELAY', ["The day after a long hike, your legs feel fine. Then, on day two, the stairs hurt.",
                "Most people blame lactic acid.",
                "But by then, the lactic acid has been gone for more than a day."], s_hook),
 ('LACTIC ACID', ["When you work hard, like sprinting for a bus, your muscles make lactate. People often call it lactic acid.",
                  "It builds up while you push hard.",
                  "But it clears fast. A study in nineteen eighty-three found it back to normal levels within about an hour."], s_myth),
 ('THE TIMING', ["Now compare the timing.",
                 "Lactic acid: gone within about an hour.",
                 "Soreness: it usually starts six to eight hours later, and peaks about two days after.",
                 "The two don't line up. So something else is going on."], s_timeline),
 ('THE CLUE', ["Here's a clue from that same study. Some people ran downhill.",
               "Their blood showed no rise in lactic acid.",
               "Yet downhill running causes some of the worst soreness there is."], s_clue),
 ('QUICK QUESTION', ["Quick question. Which makes your legs sorer the next day: walking up a long flight of stairs, or walking down it?"], s_quiz),
 ('THE BRAKES', ["Walking down. Even though going up feels harder.",
                 "Going down, your thigh muscles work while they are being pulled longer. They act like brakes.",
                 "Scientists call these eccentric movements. Walking downhill and lowering a heavy box are the same.",
                 "And these braking movements cause more tiny damage to muscle cells than lifting does."], s_brake),
 ('WHAT HURTS', ["So what actually hurts? Most research points to tiny damage in the muscle, and where it joins the tendon.",
                 "Your body starts repairing it. Fluid and chemicals gather, and nerve endings become more sensitive.",
                 "That repair takes a day or two to build. That's the delay.",
                 "Scientists still debate the fine details. But the timing points here, not to lactic acid."], s_repair),
 ('GOOD NEWS', ["The good news? Muscles adapt fast.",
                "Do the same hike again within about two weeks, and you'll feel much less sore.",
                "And soreness isn't a score. Muscles can grow stronger without much soreness at all."], s_adapt),
 ('RECAP', ["Three things to keep.",
            "One: lactic acid clears within about an hour, long before the soreness starts.",
            "Two: braking movements, like walking downhill, cause the most soreness.",
            "Three: the ache is your muscles repairing tiny damage, and they adapt fast.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('Sore ', SORE), ('2 days later?', INK)], 1, size=96)
    for k, (day, note, col, icon) in enumerate((('DAY 0', 'workout', TIME, 'hike'), ('DAY 1', 'fine', GR, 'ok'), ('DAY 2', 'ouch', SORE, 'ouch'))):
        a = fd(t, .2 + .9 * k)
        day_tile(c, 520 + k * 440, 470 + 20 * (1 - a), day, note, col, a, w=360, icon=icon, t=t)
    m1 = st(T, 1)
    if m1 > .01:
        dots(c, 960, 720, 300, 50, 16, LAC, m1, t=t)
        c.text(960, 820, 'lactic acid?', 46, LAC, m1, w='Bold')

SHORT_SCENES = [
 ('THE QUESTION', ["Why do your muscles hurt two days after a workout, and not right away?",
                   "Most people blame lactic acid."], short_hook),
 ('THE TIMING', ["But compare the timing.",
                 "Lactic acid is back to normal within about an hour.",
                 "Soreness starts hours later, and peaks about two days after.",
                 "They don't line up."], s_timeline),
 ('THE CAUSE', ["The real clue is going downhill, or down stairs.",
                "Your muscles work while being pulled longer, like brakes.",
                "These braking movements cause the most soreness.",
                "They leave tiny damage in the muscle."], s_brake),
 ('THE ANSWER', ["Your body repairs that damage, and the repair takes a day or two to build.",
                 "That's the delay. Not lactic acid."],
  card('Tiny damage, slow repair.', "That's the 2-day delay.")),
]
SHORT_HITS = [(3, 1, 0.0)]
