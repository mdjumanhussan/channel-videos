"""Episode: How Compound Interest Works: Interest on Interest."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Compound Interest Works'       # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {'one thousand pounds': '£1,000', 'one thousand dollars': '$1,000', 'fifty-two dollars fifty': '$52.50',
                 'two thousand five hundred dollars': '$2,500', 'fifty dollars': '$50',
                 'seventy-two': '72', 'five percent': '5%', 'six percent': '6%', 'three percent': '3%', 'twenty percent': '20%'}
SHORT_HOOK = 'How does money grow by itself?'     # headline on the vertical Short
HITS = [(0, 4, 0.2), (3, 3, 0.0), (8, 4, 0.0)]    # title card, the key number, the closing line
THUMB = ['MONEY', 'MAKES', 'MONEY']               # 3 words only (lesson applied 2026-10-12)

GOLD = (255, 200, 70); GOLD2 = (200, 140, 30); RED = (235, 50, 60); SNOW = (226, 236, 255)
SLOT = (36, 44, 86); STEEL = (150, 160, 200)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def coin(c, x, y, r, a=1.0, bg=BG, col=GOLD, sym='$'):
    if a <= 0.01 or r < 2: return
    c.circ(x, y, r, col, a, bg=bg)
    c.circ(x, y, r * .76, None, a, outline=GOLD2 if col == GOLD else mix(col, .6, (10, 12, 30)), ow=max(2, r * .09), bg=bg)
    if sym and r > 14: c.text(x, y, sym, r * 1.0, BG, a, w='Bold', bg=col)

def stack(c, x, base, n, a=1.0, bg=BG, w=120, h=22, col=GOLD):
    """Pile of n flat coins seen from the side, resting on height base."""
    for i in range(int(n)):
        y = base - i * (h + 4)
        c.rr(x - w / 2, y - h, x + w / 2, y, h / 2, col, a, bg=bg)
        c.rr(x - w / 2 + 10, y - h + 6, x + w / 2 - 10, y - h + 10, 2, GOLD2 if col == GOLD else BG, a * .7, bg=col)

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def axes(c, x0, y0, x1, y1, a=1.0, xl='Years', yl='Balance', bg=BG):
    c.arrow(x0, y1, x0, y0 - 20, DIM, 4, a, 14); c.arrow(x0, y1, x1 + 20, y1, DIM, 4, a, 14)
    c.text(x1 + 10, y1 + 38, xl, 30, DIM, a, 'rm', 'Medium', bg=bg)
    c.text(x0 + 16, y0 - 22, yl, 30, DIM, a, 'lm', 'Medium', bg=bg)

def money(v): return '$' + format(int(round(v)), ',')

def loop_arrow(c, x, y, r, col, a=1.0, ph=0.0, bg=BG, w=7):
    """Circular arrow (three quarters of a turn) that slowly spins: 'goes back in'."""
    if a <= 0.01: return
    pts = [(x + r * math.cos(ph + q * 4.6 / 40), y + r * math.sin(ph + q * 4.6 / 40)) for q in range(41)]
    c.line(pts, col, w, a, bg)
    q = ph + 4.6; ex, ey = pts[-1]; tx, ty = -math.sin(q), math.cos(q)
    for da in (2.5, -2.5):
        ang = math.atan2(ty, tx) + da
        c.line([(ex, ey), (ex + 22 * math.cos(ang), ey + 22 * math.sin(ang))], col, w, a, bg)

def clock(c, x, y, r, t, col=CY, a=1.0, bg=BG):
    c.circ(x, y, r, None, a, outline=col, ow=max(4, r * .1), bg=bg)
    c.line([(x, y), (x + r * .62 * math.sin(t * 1.6), y - r * .62 * math.cos(t * 1.6))], col, max(4, r * .09), a, bg)
    c.line([(x, y), (x + r * .4 * math.sin(t * .2), y - r * .4 * math.cos(t * .2))], INK, max(4, r * .09), a, bg)
    c.circ(x, y, r * .09, INK, a, bg=bg)

def thumb_art(c):
    # one oversized subject: a pile of coins that keeps getting taller
    for i, n in enumerate([3, 6, 11]):
        stack(c, 1260 + i * 215, 860, n, 1, BG, 180, 40)
    c.arrow(1200, 640, 1700, 250, GR, 16, 1, 46)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(4), 0, .5)
    if a > 0:
        top = a * fd(t, 0, .2) * (1 - fd(T(2), -.3, .4))
        c.text(960, 200, 'One gift. 200 years.', 88, INK, top, w='Bold')
        # left card: the gift
        m = a * fd(t, 0, .25)
        c.rr(150, 300, 690, 760, 30, CARD, m, outline=CY, ow=5)
        c.rr(150, 300, 690, 390, 30, CY, m); c.text(420, 345, '1790', 52, BG, m, w='Bold', bg=CY)
        c.text(420, 500, '£1,000', 120, INK, m, w='Bold', bg=CARD)
        c.text(420, 625, 'left to the city of Boston', 34, DIM, m, w='Medium', bg=CARD)
        c.text(420, 690, 'by Benjamin Franklin', 34, DIM, m, w='Medium', bg=CARD)
        # the years tick by
        p = ease(T(1, -.2) / 2.6) if T(1) > -.2 else 0.0
        c.line([(730, 530), (730 + 420 * max(p, .001), 530)], YE, 8, a * fd(T(0), 2.4))
        if p > 0:
            yr = int(1790 + 200 * p)
            c.text(940, 470, str(yr), 60, YE, a * (1 - fd(T(1), 2.6, .4)), w='Bold')
            for k in range(5):
                c.line([(730 + 105 * k, 518), (730 + 105 * k, 542)], YE, 4, a * (p * 4 >= k))
        if T(1) > 0:
            m2 = a * fd(T(1), 1.8)
            c.rr(1190, 300, 1790, 760, 30, CARD, m2, outline=YE, ow=6)
            c.rr(1190, 300, 1790, 390, 30, YE, m2); c.text(1490, 345, '1990', 52, BG, m2, w='Bold', bg=YE)
            c.text(1490, 475, 'almost', 44, DIM, m2, w='Medium', bg=CARD)
            c.text(1490, 580, '$5 million', 104, YE, m2, w='Bold', bg=CARD)
            c.text(1490, 690, 'value of the fund', 34, DIM, m2, w='Medium', bg=CARD)
            c.text(960, 830, 'Boston\'s Franklin fund. Part of it was spent after the first 100 years.', 28, DIM, m2, w='Regular')
        if T(2) > 0:
            c.text(960, 200, 'The engine behind it has a name', 68, INK, a * fd(T(2)) * (1 - fd(T(3), -.3, .4)), w='Bold')
        if T(3) > 0:
            c.text(960, 200, 'Compound interest', 96, GR, a * fd(T(3)), w='Bold')
    if T(4) > 0:
        m = fd(T(4), .2, .7)
        c.text(960, 380 + 30 * (1 - m), 'How Compound', 130, INK, m, w='Bold')
        c.text(960, 540 + 30 * (1 - m), 'Interest Works', 130, GR, m, w='Bold')
        c.line([(960 - 260 * m, 650), (960 + 260 * m, 650)], YE, 8, m)
        c.text(960, 730, 'for you, and against you', 48, DIM, fd(T(4), .9), w='Medium')

def s_simple(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 440, 'Simple interest', 130, PU, a0, w='Bold')
    c.text(960, 590, 'the plain kind', 52, DIM, a0 * fd(T(0), .6), w='Medium')
    if T(1) < -.1: return
    m = fd(T(1))
    # the account
    c.rr(140, 250, 680, 620, 30, CARD, m, outline=(44, 52, 100), ow=4)
    c.text(410, 310, 'Your account', 36, DIM, m, w='Medium', bg=CARD)
    c.text(410, 430, '$1,000', 112, INK, m, w='Bold', bg=CARD)
    pill(c, 410, 550, '5% a year', CY, m * fd(T(1), 2.0), 38, CARD)
    # same interest every year
    if T(2) > 0:
        k = fd(T(2))
        c.text(1290, 215, 'Interest each year', 40, INK, k, w='Bold')
        for i in range(5):
            mm = k * fd(T(2), .9 + i * .45); x = 890 + i * 200
            c.rr(x - 84, 290, x + 84, 620, 20, CARD, mm, outline=PU, ow=3)
            c.text(x, 335, f'Year {i + 1}', 30, DIM, mm, w='Medium', bg=CARD)
            coin(c, x, 450, 52, mm, CARD)
            c.text(x, 565, '+$50', 44, PU, mm, w='Bold', bg=CARD)
        c.text(1290, 690, 'Always the same', 44, PU, k * fd(T(2), 3.6), w='Bold')
    # a tap that drips at a steady speed
    if T(3) > 0:
        k = fd(T(3)); X = 410
        c.rr(X - 150, 690, X + 20, 720, 10, STEEL, k); c.rr(X - 10, 690, X + 22, 760, 10, STEEL, k)
        c.rr(X - 80, 664, X - 40, 694, 6, STEEL, k); c.rr(X - 110, 650, X - 10, 668, 8, CY, k)
        for j in range(3):
            dy = ((t * 70 + j * 36) % 108)
            c.circ(X + 6, 772 + dy, 9, CY, k * (1 - dy / 130))
        c.text(X + 80, 800, 'Same drip, forever', 36, DIM, k, 'lm', 'Medium')

def s_compound(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 420, 'Compound interest', 120, GR, a0, w='Bold')
    c.text(960, 570, 'changes one thing', 64, INK, a0 * fd(T(0), .9), w='Bold')
    aA = fd(T(1)) * (1 - fd(T(2), -.4, .4))
    if T(1) > -.1 and aA > 0:
        # balance -> interest -> back into the balance
        c.rr(250, 330, 800, 700, 30, CARD, aA, outline=GR, ow=5)
        c.text(525, 395, 'Balance', 40, DIM, aA, w='Medium', bg=CARD)
        grow = clamp((T(1) - 2.2) / .6)
        c.text(525, 520, money(1000 + 50 * ease(grow)), 110, INK, aA, w='Bold', bg=CARD)
        c.text(525, 640, 'now a little bigger', 34, GR, aA * fd(T(1), 2.8), w='Medium', bg=CARD)
        u = ease(clamp((T(1) - 1.0) / 1.4))                      # the interest coin flies back into the balance
        cx = 1400 - 600 * u; cy = 515 - 230 * math.sin(math.pi * u)
        c.arrow(830, 600, 1250, 600, DIM, 5, aA * fd(T(1), .4), 18); c.text(1040, 640, 'earns', 32, DIM, aA * fd(T(1), .4), w='Medium')
        c.circ(1400, 515, 96, None, aA * fd(T(1), .5), outline=(60, 70, 120), ow=4)
        c.text(1400, 660, 'Interest', 40, YE, aA * fd(T(1), .5), w='Bold')
        if u < .98: coin(c, cx, cy, 70 - 20 * u, aA * fd(T(1), .5))
        loop_arrow(c, 1650, 515, 70, GR, aA * fd(T(1), 3.0), t * 1.2)
        c.text(960, 215, 'The interest goes back in', 54, INK, aA, w='Bold')
        c.text(960, 800, 'Then it earns interest too', 48, GR, aA * fd(T(1), 3.0), w='Bold')
    aB = fd(T(2)) * (1 - fd(T(3), -.4, .4))
    if T(2) > -.1 and aB > 0:
        rows = [('Year 1', '$1,000', '+$50.00', 0.0, INK), ('Year 2', '$1,050', '+$52.50', 2.4, YE)]
        c.text(600, 240, 'Balance', 34, DIM, aB, w='Medium'); c.text(1010, 240, 'x 5%', 34, DIM, aB, w='Medium'); c.text(1420, 240, 'Interest earned', 34, DIM, aB, w='Medium')
        for i, (yr, bal, inc, off, col) in enumerate(rows):
            m = aB * fd(T(2), off); y = 390 + i * 230
            c.rr(170, y - 95, 1750, y + 95, 26, CARD, m, outline=col if i else (44, 52, 100), ow=5 if i else 4)
            c.text(230, y, yr, 46, DIM, m, 'lm', 'Bold', bg=CARD)
            c.text(600, y, bal, 76, INK, m, w='Bold', bg=CARD)
            c.arrow(860, y, 1150, y, DIM, 5, m, 18)
            c.text(1420, y, inc, 84, col, m * fd(T(2), off + .7), w='Bold', bg=CARD)
        c.text(960, 800, 'The extra $2.50 is interest on interest', 44, GR, aB * fd(T(2), 4.0), w='Bold')
    if T(3) > -.1:
        m = fd(T(3)); x0, y0, x1, y1 = 260, 300, 1660, 760
        poly(c, [(x0, y0), (x1, y1), (x0, y1)], SLOT, m)
        c.line([(x0, y0), (x1, y1)], SNOW, 8, m)
        u = clamp(T(3, .3) / 6.0); r = 22 + 110 * u
        bx = x0 + (x1 - x0) * (.06 + .8 * u); by = y0 + (y1 - y0) * (.06 + .8 * u)
        nx, ny = .312, -.95                                    # points up, away from the slope
        cx, cy = bx + nx * r, by + ny * r
        c.circ(cx, cy, r, SNOW, m)
        for k in range(3):
            q = t * 3 + k * 2.1; c.circ(cx + r * .5 * math.cos(q), cy + r * .5 * math.sin(q), r * .12, (190, 204, 236), m, bg=SNOW)
        c.text(1330, 300, 'The bigger it gets,', 48, INK, m * fd(T(3), 2.2), w='Bold')
        c.text(1330, 370, 'the more it picks up', 48, CY, m * fd(T(3), 3.4), w='Bold')

def s_gap(c, T, t):
    m = fd(T(0)); x0, y0, x1, y1 = 230, 250, 1330, 770; gw, gh = x1 - x0, y1 - y0
    axes(c, x0, y0, x1, y1, m, xl='')
    c.text(x0 + gw / 2, y1 + 38, 'Years', 28, DIM, m, w='Medium')
    top = 4600.0; Y = lambda v: y1 - gh * v / top
    # line 0 draws the first 5 years, line 1 runs on to year 30
    yrs = 5 * ease(T(0, .5) / 2.0) if T(1) < 0 else 5 + 25 * ease(T(1, .3) / 3.2)
    n = max(1, int(yrs * 4))
    sim = [(x0 + gw * (yrs * i / n) / 30, Y(1000 + 50 * yrs * i / n)) for i in range(n + 1)]
    com = [(x0 + gw * (yrs * i / n) / 30, Y(1000 * 1.05 ** (yrs * i / n))) for i in range(n + 1)]
    for k in (10, 20, 30):
        c.line([(x0 + gw * k / 30, y1), (x0 + gw * k / 30, y1 + 12)], DIM, 3, m); c.text(x0 + gw * k / 30, y1 + 38, str(k), 28, DIM, m, w='Medium')
    c.line(sim, PU, 8, m); c.line(com, GR, 9, m)
    c.circ(sim[-1][0], sim[-1][1], 12, PU, m); c.circ(com[-1][0], com[-1][1], 13, GR, m)
    c.text(780, 195, '$1,000 at 5% a year', 46, INK, m, w='Bold')
    a5 = m * (1 - fd(T(1), 0, .4))
    c.text(x0 + gw * 5 / 30 + 30, Y(1250) - 46, 'Looks tiny', 40, DIM, a5 * fd(T(0), 2.2), 'lm', 'Bold')
    # legend / results on the right
    for i, (lab, col, val, k) in enumerate([('Simple', PU, '$2,500', 2), ('Compound', GR, 'about $4,300', 3)]):
        y = 350 + i * 230; mm = m
        c.rr(1420, y - 95, 1830, y + 95, 24, CARD, mm, outline=col, ow=5 if T(k) > 0 else 3)
        c.circ(1470, y - 48, 14, col, mm, bg=CARD); c.text(1500, y - 48, lab, 36, INK, mm, 'lm', 'Bold', bg=CARD)
        c.text(1625, y + 28, val, 60 if i == 0 else 46, col, mm * fd(T(k)), w='Bold', bg=CARD)
    if T(1) > 0: c.text(1625, 215, 'After 30 years', 38, YE, fd(T(1), 1.6), w='Bold')
    if T(4) > 0:
        k = fd(T(4))
        c.text(1625, 720, 'Same money.', 38, INK, k, w='Bold'); c.text(1625, 772, 'Same rate.', 38, INK, k * fd(T(4), .9), w='Bold')
        c.text(1625, 824, 'Different rule.', 38, GR, k * fd(T(4), 1.7), w='Bold')
    c.text(780, 848, 'Example only. Interest added once a year. No fees, tax or withdrawals.', 26, DIM, m * .95, w='Regular')

def s_rule(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 430, '72', 300, YE, a0, w='Bold')
    c.text(960, 650, 'The rule of 72', 60, INK, a0 * fd(T(0), 1.2), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1)); up = 1 - fd(T(3), -.4, .5)
    yy = 440 - 190 * (1 - up)
    # 72 / rate = years to double
    parts = [('72', YE, 0.0), ('÷', DIM, .5), ('rate', CY, .9)]
    xs = [520, 678, 900]
    for (s, col, off), x in zip(parts, xs): c.text(x, yy, s, 120, col, m * fd(T(1), off), w='Bold')
    c.text(1090, yy, '=', 120, DIM, m * fd(T(2), 0), w='Bold')
    c.text(1150, yy - 34, 'years to', 58, INK, m * fd(T(2), .2), 'lm', 'Bold'); c.text(1150, yy + 40, 'double', 58, GR, m * fd(T(2), .2), 'lm', 'Bold')
    c.text(960, 640, 'roughly', 46, DIM, m * fd(T(2), 1.3) * up, w='Medium')
    if T(3) > -.1:
        for i, (rate, yrs, off) in enumerate([('6%', '12', 0.0), ('3%', '24', 2.9)]):
            k = fd(T(3), off); x = 530 + i * 860
            if k <= 0.01: continue
            c.rr(x - 380, 400, x + 380, 760, 30, CARD, k, outline=CY, ow=4)
            c.text(x, 465, f'72 ÷ {rate[:-1]}', 60, INK, k, w='Bold', bg=CARD)
            c.text(x - 150, 610, yrs, 150, YE, k * fd(T(3), off + .5), w='Bold', bg=CARD)
            c.text(x - 30, 585, 'years', 44, INK, k * fd(T(3), off + .5), 'lm', 'Bold', bg=CARD)
            c.text(x - 30, 645, f'at {rate} a year', 34, DIM, k, 'lm', 'Medium', bg=CARD)
            stack(c, x + 250, 720, 3, k, CARD, 96, 20); stack(c, x + 250, 720 - 3 * 24 - 60 * (1 - fd(T(3), off + .9)), 3, k * fd(T(3), off + .9), CARD, 96, 20)
            c.text(x + 250, 520, 'x2', 44, GR, k * fd(T(3), off + 1.1), w='Bold', bg=CARD)
    if T(4) > 0:
        pill(c, 960, 830, 'An estimate, not an exact answer', YE, fd(T(4)), 36)

def s_time(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        clock(c, 960, 380, 130, t, CY, a0)
        c.text(960, 620, 'The biggest ingredient', 64, INK, a0, w='Bold')
        c.text(960, 730, 'Time', 110, CY, a0 * fd(T(0), 1.2), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1)); x0, x1 = 420, 1500; X = lambda age: x0 + (x1 - x0) * (age - 25) / 40
    c.text(960, 200, 'Two friends. $1,000 each. 5% a year.', 48, INK, m, w='Bold')
    for age in (25, 35, 45, 55, 65):
        c.text(X(age), 280, str(age), 32, DIM, m, w='Medium'); c.line([(X(age), 305), (X(age), 790)], (40, 48, 92), 3, m)
    c.text(x0 - 70, 280, 'Age', 32, DIM, m, 'rm', 'Medium')
    rows = [('Starts at 25', GR, 25, 7040, 'about $7,000'), ('Starts at 35', PU, 35, 4322, 'about $4,300')]
    p = ease(T(3, .2) / 3.0) if T(3) > -.2 else 0.0
    shown = [fd(T(3), 2.6), fd(T(4), 1.0)]
    for i, (lab, col, start, endv, txt) in enumerate(rows):
        k = m * fd(T(2), i * 1.9) if T(2) > -.1 else 0.0; y = 430 + i * 240
        if k <= 0.01: continue
        c.text(x0 - 70, y - 20, lab, 34, col, k, 'rm', 'Bold')
        c.text(x0 - 70, y + 24, 'saves $1,000 once', 24, DIM, k, 'rm', 'Medium')
        coin(c, X(start), y, 30, k)
        if p > 0:
            # the balance grows as a widening band along the timeline
            end_age = start + (65 - start) * p; n = 30
            topl = []; botl = []
            for j in range(n + 1):
                ag = start + (end_age - start) * j / n; v = 1000 * 1.05 ** (ag - start); hh = 8 + 78 * v / 7040
                topl.append((X(ag), y - hh)); botl.append((X(ag), y + hh))
            poly(c, topl + botl[::-1], col, k * .85)
            coin(c, X(start), y, 30, k)
            c.text(x1 + 40, y, txt, 46, col, k * shown[i], 'lm', 'Bold')
    if T(5) > 0:
        k = fd(T(5))
        c.line([(X(25), 318), (X(35), 318)], YE, 10, k)
        c.text(X(30), 348, '10 extra years', 30, YE, k, w='Bold')
    c.text(960, 836, 'Example only. Interest added once a year. No fees, tax or withdrawals.', 26, DIM, m * .95, w='Regular')

def s_debt(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 210, 'Now the warning', 84, PK, a0, w='Bold')
        c.rr(250, 330, 900, 760, 30, CARD, a0, outline=GR, ow=4); c.rr(1020, 330, 1670, 760, 30, CARD, a0 * fd(T(0), 1.4), outline=PK, ow=6)
        c.text(575, 400, 'When you save', 44, GR, a0, w='Bold', bg=CARD); c.arrow(575, 700, 575, 480, GR, 16, a0, 40)
        k = a0 * fd(T(0), 1.4)
        c.text(1345, 400, 'When you owe', 44, PK, k, w='Bold', bg=CARD); c.arrow(1345, 480, 1345, 700, PK, 16, k, 40)
    aA = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    if T(1) > -.1 and aA > 0:
        # a plain bank card (no brand), and the loop: unpaid interest joins the debt
        c.text(960, 215, 'On a debt, the same rule runs in reverse', 52, INK, aA, w='Bold')
        c.rr(210, 330, 800, 690, 28, (60, 44, 110), aA, outline=PU, ow=4)
        c.rr(210, 395, 800, 455, 0, (20, 22, 48), aA, bg=(60, 44, 110))
        c.rr(270, 500, 370, 570, 12, GOLD, aA, bg=(60, 44, 110))
        c.text(505, 630, 'What you owe', 36, INK, aA, w='Medium', bg=(60, 44, 110))
        steps = [('Unpaid interest', YE, 1, 0.3), ('is added to the debt', PK, 1, 1.5), ('Next time: interest on that too', INK, 2, 0.2)]
        for i, (s, col, li, off) in enumerate(steps):
            k = aA * fd(T(li), off); y = 380 + i * 130
            c.rr(900, y - 52, 1720, y + 52, 22, CARD, k, outline=col if i < 2 else GR, ow=4)
            c.text(1310, y, s, 42, col, k, w='Bold', bg=CARD)
            if i < 2: c.arrow(1310, y + 58, 1310, y + 76, DIM, 5, aA * fd(T(steps[i + 1][2]), steps[i + 1][3]), 12)
        loop_arrow(c, 505, 780, 44, PK, aA * fd(T(2), .2), t * 1.4)
        c.text(580, 780, 'and round again', 34, PK, aA * fd(T(2), .6), 'lm', 'Bold')
    if T(3) > -.1:
        m = fd(T(3)); base = 760; hmax = 400
        c.text(700, 210, 'A debt at 20% a year, nothing repaid', 46, INK, m, w='Bold')
        for i in range(5):
            v = 1.2 ** i; k = m * fd(T(3), .5 + i * .55); x = 300 + i * 200; h = hmax * v / 2.2 * ease(clamp((T(3) - .5 - i * .55) / .5))
            col = PK if v >= 2 else mix(PK, .45 + .12 * i, CARD)
            c.rr(x - 66, base - h, x + 66, base, 12, col, k)
            c.text(x, base + 34, 'Start' if i == 0 else f'Year {i}', 28, DIM, k, w='Medium')
            c.text(x, base - h - 30, f'{int(round(v * 100))}', 34, PK if v >= 2 else INK, k * fd(T(3), .9 + i * .55), w='Bold')
        yl = base - hmax * 2 / 2.2
        for xx in range(210, 1190, 36): c.line([(xx, yl), (xx + 18, yl)], YE, 4, m * fd(T(3), 3.0))
        c.text(1215, yl, 'double', 36, YE, m * fd(T(3), 3.0), 'lm', 'Bold')
        c.text(700, 848, 'Example only. Debt of 100, interest added once a year.', 26, DIM, m * .95, w='Regular')
        if T(4) > 0:
            k = fd(T(4)); r = 60 + 110 * ease(T(4) / 3.4); bx, by = 1600, 520 - r * .25
            c.line([(bx, by + r), (bx - 14, by + r + 90), (bx + 10, 800)], DIM, 4, k)
            c.circ(bx, by, r, PK, k); c.circ(bx - r * .35, by - r * .35, r * .16, (255, 190, 210), k, bg=PK)
            poly(c, [(bx - 12, by + r - 3), (bx + 12, by + r - 3), (bx, by + r + 16)], PK, k)
            c.text(bx, 838, 'It can balloon', 38, PK, k, w='Bold')

def s_levers(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 430, 'What makes compounding', 92, INK, a0, w='Bold'); c.text(960, 560, 'stronger?', 110, YE, a0, w='Bold')
    if T(1) < -.1: return
    out = 1 - fd(T(2), -.4, .4) * .0
    cards = [('A higher rate', CY, 0.0), ('More time', GR, 1.3), ('Added more often', YE, 2.3)]
    for i, (lab, col, off) in enumerate(cards):
        m = fd(T(1), off); x = 380 + i * 580; up = 22 * (1 - m)
        if m <= 0.01: continue
        c.rr(x - 255, 230 + up, x + 255, 640 + up, 28, CARD, m, outline=col, ow=5)
        y = 400 + up
        if i == 0:
            c.text(x, y, '%', 190, col, m, w='Bold', bg=CARD); c.arrow(x + 150, y + 70, x + 150, y - 80, col, 12, m, 30)
        elif i == 1:
            clock(c, x, y, 105, t, col, m, CARD)
        else:
            for j in range(12):
                on = int(t * 3) % 12 >= j
                xx = x - 165 + (j % 6) * 66; yy = y - 60 + (j // 6) * 100
                c.rr(xx - 26, yy - 38, xx + 26, yy + 38, 8, col if on else SLOT, m, bg=CARD)
        c.text(x, 585 + up, lab, 42, INK, m, w='Bold', bg=CARD)
    if T(2) > 0:
        k = fd(T(2))
        c.text(960, 715, 'Real rates change. Prices rise too.', 46, INK, k, w='Bold')
    if T(3) > 0:
        pill(c, 960, 815, 'The numbers in this video are examples', YE, fd(T(3)), 36)

REC = [('1', 'Interest on interest', GR), ('2', 'Longer means faster', CY), ('3', 'On debt, it works against you', PK)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 255, 290 + up, x + 255, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 190, 355 + up, 40, col, m, bg=CARD); c.text(x - 190, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 540 + up
        if i == 0:
            coin(c, x - 70, y, 70, m, CARD); coin(c, x + 90, y - 40, 34 + 4 * math.sin(t * 3), m, CARD)
            loop_arrow(c, x + 90, y - 40, 62, col, m, t * 1.5, CARD, 6)
        elif i == 1:
            c.line([(x - 160, y - 120), (x - 160, y + 100), (x + 170, y + 100)], DIM, 4, m, CARD)
            p = clamp(((t * .35) % 1.4))
            pts = [(x - 160 + 320 * u / 40, y + 92 - 6.5 * 1.09 ** u) for u in range(int(40 * p) + 1)]
            c.line(pts, col, 8, m, CARD)
        else:
            for j, v in enumerate([1, 1.5, 2.3]):
                c.rr(x - 150 + j * 110, y + 100 - 80 * v, x - 70 + j * 110, y + 100, 10, mix(col, .5 + .25 * j, CARD), m, bg=CARD)
            c.arrow(x - 150, y - 30, x + 150, y - 120, col, 8, m, 22)
        c.text(x, 720 + up, lab, 30 if i == 2 else 34, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        o2 = 1 - fd(T(5), -.3, .5)
        for i, (s, col) in enumerate([('Small numbers.', INK), ('Long time.', CY), ('Big difference.', YE)]):
            c.text(960, 350 + i * 150, s, 104, col, fd(T(4), i * 1.0) * o2, w='Bold')
    if T(5) > 0:
        m = fd(T(5), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, RED, m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=RED)
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(5), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(5), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["In 1790, Benjamin Franklin left one thousand pounds to the city of Boston.",
            "Two hundred years later, that fund was worth almost five million dollars.",
            "The engine behind that growth has a name.", "Compound interest.",
            "Here is how it works, for you, and against you."], s_hook),
 ('1  ·  SIMPLE INTEREST', ["Start with the simple kind.", "Put one thousand dollars in an account that pays five percent a year.",
            "With simple interest, you earn fifty dollars every year. Always the same.",
            "It is like a tap that drips at the same speed forever."], s_simple),
 ('2  ·  COMPOUND INTEREST', ["Compound interest changes one thing.",
            "The interest is added to your balance. Then it earns interest too.",
            "In year one, you earn fifty dollars. In year two, you earn fifty-two dollars fifty.",
            "It is like a snowball rolling downhill. The bigger it gets, the more snow it picks up."], s_compound),
 ('3  ·  THE GAP', ["At first, the difference looks tiny.", "But leave both accounts alone for thirty years.",
            "Simple interest gives you two thousand five hundred dollars.",
            "Compound interest gives you about four thousand three hundred.",
            "Same money. Same rate. Only the rule changed."], s_gap),
 ('4  ·  THE RULE OF 72', ["There is a quick shortcut, called the rule of seventy-two.", "Divide seventy-two by the interest rate.",
            "The answer is roughly how many years your money takes to double.",
            "At six percent, that is about twelve years. At three percent, about twenty-four.",
            "It is an estimate, not an exact answer."], s_rule),
 ('5  ·  TIME', ["So the biggest ingredient is time.", "Think of two friends. Each saves one thousand dollars, once, at five percent.",
            "One starts at twenty-five. The other waits until thirty-five.",
            "At sixty-five, the early saver has about seven thousand dollars.", "The late saver has about four thousand three hundred.",
            "Those ten extra years made the difference."], s_time),
 ('6  ·  THE WARNING', ["Now the warning. Compounding also works against you.", "On a debt, unpaid interest is added to what you owe.",
            "Then you pay interest on that interest.",
            "At twenty percent a year, a debt with nothing repaid doubles in under four years.",
            "This is how a small card balance can balloon."], s_debt),
 ('7  ·  WHAT CHANGES IT', ["So what makes compounding stronger?", "A higher rate. More time. And interest that is added more often.",
            "Real rates change, and prices rise too, so real results will differ.",
            "The numbers in this video are examples, to show the idea."], s_levers),
 ('RECAP', ["So remember three things.", "One. Compound interest is interest on interest.", "Two. The longer it runs, the faster it grows.",
            "Three. On debt, the same rule works against you.", "Small numbers. Long time. Big difference.",
            "If this helped, subscribe for more."], s_recap),
]
