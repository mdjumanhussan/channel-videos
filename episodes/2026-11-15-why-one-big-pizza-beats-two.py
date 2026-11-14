"""Episode: Why One 18-Inch Pizza Beats Two 12-Inch Pizzas (area grows with the square of the width; price per square inch; the crust twist)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Pizza Math'                                   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'One big pizza or two?'                         # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 0, 0.0), (7, 1, 0.0)]               # the answer, quiz answer (4x), crust twist
THUMB = ['ONE BEATS', 'TWO.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.3, (0, 2): 0.3, (2, 1): 0.3, (3, 3): 0.4, (4, 0): 3.2, (5, 0): 0.3, (7, 0): 0.3}
SHORT_PAUSES = {(0, 1): 0.2, (3, 0): 0.3}
CAPTION_FIXES = {'eighteen-inch': '18-inch', 'twelve-inch': '12-inch', 'sixteen-inch': '16-inch', 'eight-inch': '8-inch',
                 'fourteen-inch': '14-inch', 'sixty-five-inch': '65-inch', 'fifty-inch': '50-inch', 'nine-inch': '9-inch',
                 'two hundred and fifty-four': '254', 'two hundred and twenty-six': '226', 'one hundred and thirteen': '113',
                 'twenty twenty-four': '2024', 'twenty fourteen': '2014', 'seventy-four thousand, four hundred and seventy-six': '74,476',
                 'three thousand, six hundred and seventy-eight': '3,678', 'four hundred': '400', 'one hundred': '100',
                 'twenty-eight': '28', 'seventy percent': '70%', 'one and a half': '1.5'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the width you order is cyan, the area you eat is yellow, crust is orange-brown, price is pink, the answer is green.
WID = CY; AREA = YE; CRUST = (214, 140, 70); PRICE = PK; ANS = GR
DARK = (20, 22, 38); CHEESE = (255, 214, 110); PEP = (200, 60, 60); QUIZ = (60, 36, 24); TILE = (60, 70, 120)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0
K = 25.0                                                     # drawing scale: pixels per inch of pizza

# Short headlines with one key word in colour (kept from 2026-11-13: most mobile viewers watch muted).
def headline(c, parts, a, size=88, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def pizza(c, x, y, inches, a, slices=8, glow=0.0, bg=BG, crust_hi=0.0, spin=0.0):
    """A pizza seen from above, drawn to scale (K px per inch)."""
    if a <= .01: return
    r = inches / 2 * K
    ccol = tuple(int(CRUST[j] + (255 - CRUST[j]) * .35 * crust_hi) for j in range(3))
    if glow > .01: c.circ(x, y, r + 14, None, a * glow, outline=AREA, ow=6, bg=bg)
    c.circ(x, y, r, ccol, a, bg=bg)
    c.circ(x, y, r * .86, CHEESE, a, bg=ccol)
    rnd = random.Random(int(inches * 10))
    n = int(4 + inches * .9)
    for k in range(n):
        ang = rnd.random() * 6.283; d = math.sqrt(rnd.random()) * r * .7
        c.circ(x + d * math.cos(ang), y + d * math.sin(ang), max(6, r * .09), PEP, a, bg=CHEESE)
    for k in range(slices):
        ang = spin + 6.283 * k / slices
        c.line([(x, y), (x + r * .86 * math.cos(ang), y + r * .86 * math.sin(ang))], (230, 180, 90), 3, a, bg=CHEESE)

def width_bar(c, x, y, inches, a, lab=None, col=WID, bg=BG):
    """A measuring bar straight across a pizza (the diameter)."""
    if a <= .01: return
    r = inches / 2 * K
    c.line([(x - r, y), (x + r, y)], col, 7, a, bg=bg)
    for s in (-1, 1): c.line([(x + s * r, y - 18), (x + s * r, y + 18)], col, 7, a, bg=bg)
    if lab: c.text(x, y - 40, lab, 40, col, a, w='Bold', bg=bg, stroke=3)

def tiles(c, x0, y0, n, cell, a, col=TILE, lit=0.0, bg=BG, grow=1.0):
    """An n x n square of tiles, top-left at (x0, y0); grow reveals rows."""
    if a <= .01: return
    rows = max(0, min(n, int(math.ceil(n * grow))))
    for i in range(rows):
        for j in range(n):
            cc = AREA if lit > .5 else col
            c.rr(x0 + j * cell + 1, y0 + i * cell + 1, x0 + (j + 1) * cell - 1, y0 + (i + 1) * cell - 1, 3, cc, a, bg=bg)

def tag(c, x, y, txt, col, a, sub=None, bg=BG, w=300):
    if a <= .01: return
    c.rr(x - w / 2, y - 50, x + w / 2, y + 50, 22, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - (12 if sub else 0), txt, 46, col, a, w='Bold', bg=CARD)
    if sub: c.text(x, y + 28, sub, 26, DIM, a, w='Bold', bg=CARD)

def tv(c, x, y, diag, a, col=WID, bg=BG):
    """A 16:9 screen with the given diagonal (in inches), centred at (x, y)."""
    if a <= .01: return
    s = 7.0; w = diag * .8716 * s; h = diag * .4903 * s
    c.rr(x - w / 2 - 10, y - h / 2 - 10, x + w / 2 + 10, y + h / 2 + 10, 12, (50, 56, 90), a, bg=bg)
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 6, (30, 70, 110), a, bg=(50, 56, 90))
    c.line([(x - w / 2, y + h / 2), (x + w / 2, y - h / 2)], col, 4, a * .8, bg=(30, 70, 110))
    c.line([(x - 40, y + h / 2 + 10), (x - 60, y + h / 2 + 40)], (50, 56, 90), 8, a, bg=bg)
    c.line([(x + 40, y + h / 2 + 10), (x + 60, y + h / 2 + 40)], (50, 56, 90), 8, a, bg=bg)

def tin(c, x, y, inches, a, fill=0.0, bg=BG):
    """A round cake tin seen from above, drawn at 2.4x the pizza scale."""
    if a <= .01: return
    r = inches / 2 * K * 2.0
    c.circ(x, y, r + 10, (120, 126, 150), a, bg=bg)
    c.circ(x, y, r, (40, 44, 70), a, bg=(120, 126, 150))
    if fill > .01: c.circ(x, y, r * .97, (232, 196, 140), a * fill, bg=(40, 44, 70))

# ---------- scenes ----------
L1, L2, BIGX, PY = 330, 690, 1440, 560
def s_hook(c, T, t):
    """Hook: the question with the two choices already on screen, then the surprising answer."""
    hl = lambda i: hl_(T, i)
    headline(c, [('One ', INK), ('big', AREA), (' or two?', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Two', WID), (' sounds like more', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('One', ANS), (' big pizza wins', INK)], sw_in(T, 2))
    win = hl(2)
    for x in (L1, L2): pizza(c, x, PY + 6 * math.sin(t * 1.4 + x), 12, 1, spin=.1 * t)
    pizza(c, BIGX, PY, 18, 1, glow=win, spin=-.08 * t)
    c.text(510, 830, 'two 12-inch', 44, WID, 1, w='Bold'); c.text(BIGX, 860, 'one 18-inch', 44, WID, 1, w='Bold')
    c.text(1060, PY, 'or', 56, DIM, 1, w='Bold')
    m1 = hl(1) * (1 - win)
    c.text(510, 300, '2 > 1 ?', 60, WID, m1, w='Bold')
    tag(c, 510, 300, '226 sq in', DIM, win, w=280)
    tag(c, BIGX, 272, '254 sq in', ANS, win, w=300)
    c.circ(BIGX + 210, 360, 44, ANS, win); c.check(BIGX + 210, 360, 40, DARK, win, fd(T(2), .3, .5))

def s_trap(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Size = ', INK), ('width', WID)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('18 is ', INK), ('1.5×', WID), (' 12', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('You eat the ', INK), ('area', AREA)], sw_in(T, 2))
    m2 = hl(2)
    pizza(c, 560, 540, 12, 1, glow=m2); pizza(c, 1300, 540, 18, 1, glow=m2)
    wa = fd(T(0), .3, .8) * (1 - .6 * m2)
    width_bar(c, 560, 540, 12, wa, '12 in'); width_bar(c, 1300, 540, 18, wa, '18 in')
    m1 = hl(1) * (1 - m2)
    c.rr(700, 820, 1220, 870, 20, CARD, m1, outline=WID, ow=3); c.text(960, 845, 'feels like 1.5 times the pizza', 32, WID, m1, w='Bold', bg=CARD)
    c.rr(700, 820, 1220, 870, 20, CARD, m2, outline=AREA, ow=3); c.text(960, 845, 'but the cheese covers a surface', 32, AREA, m2, w='Bold', bg=CARD)

def s_square(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('10 by 10 = ', INK), ('100', AREA)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Double the side: ', INK), ('400', AREA)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Size × size', AREA)], sw_in(T, 2))
    cell = 26
    tiles(c, 260, 330, 10, cell, 1, grow=fd(T(0), .2, 1.2), lit=hl(2))
    c.text(260 + 5 * cell, 330 + 10 * cell + 40, '10 by 10: 100 tiles', 34, DIM, 1, w='Bold')
    m1 = hl(1)
    tiles(c, 900, 290, 20, cell, m1, grow=fd(T(1), .3, 1.6), lit=hl(2))
    c.text(900 + 10 * cell, 290 + 20 * cell + 36, '20 by 20: 400 tiles', 34, AREA, m1, w='Bold')
    c.line([(900, 270), (900 + 20 * cell, 270)], WID, 6, m1); c.text(900 + 10 * cell, 246, '2× wider', 32, WID, m1, w='Bold')
    c.text(1640, 560, '4×', 120, AREA, m1 * fd(T(1), 1.8), w='Bold')
    m2 = hl(2)
    c.text(520, 760, 'circles work the same way', 34, INK, m2, w='Bold')

def s_math(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Area = ', INK), ('π × r × r', AREA)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('12-inch: ', WID), ('113', AREA)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Two of them: ', WID), ('226', AREA)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('18-inch: ', WID), ('254', ANS)], sw_in(T, 3))
    m0 = fd(T(0), .1)
    # left: one 12-inch with its radius, then a second copy slides in
    pizza(c, L1, PY, 12, m0)
    rA = fd(T(0), .6, .5)
    c.line([(L1, PY), (L1 + 6 * K * .99, PY)], WID, 6, m0 * rA, bg=CHEESE); c.text(L1 + 3 * K, PY - 28, 'r = 6', 34, DARK, m0 * rA, w='Bold', bg=CHEESE)
    m2 = hl(2)
    pizza(c, L1 + (L2 - L1) * fd(T(2), 0, .6), PY, 12, m2)
    tag(c, L1, 250, '113 sq in', AREA, hl(1) * (1 - m2), w=260)
    tag(c, 470, 262, '113 + 113 = 226', AREA, m2, w=400)
    m3 = hl(3)
    pizza(c, BIGX, PY, 18, m3, glow=m3)
    c.line([(BIGX, PY), (BIGX + 9 * K * .99, PY)], WID, 6, m3, bg=CHEESE); c.text(BIGX + 4.5 * K, PY - 28, 'r = 9', 34, DARK, m3, w='Bold', bg=CHEESE)
    tag(c, BIGX, 250, '254 sq in', ANS, m3, w=280)
    c.text(960, 860, 'Areas rounded to the nearest square inch', 28, DIM, m0, w='Regular')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a warm pattern-interrupt background (lesson of 2026-10-13)."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('16-inch', WID), (' vs ', INK), ('8-inch', WID)], 1, bg=QUIZ)
    pizza(c, 560, 560, 8, 1, bg=QUIZ); pizza(c, 1300, 540, 16, 1, bg=QUIZ)
    c.text(560, 760, '8 in', 44, WID, 1, w='Bold', bg=QUIZ); c.text(1300, 820, '16 in', 44, WID, 1, w='Bold', bg=QUIZ)
    c.text(560, 340, '2×?  or more?', 46, INK, fd(t, .8), w='Bold', bg=QUIZ)
    if T(0) > 0:
        e = T(0) - 8.0; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 7.8)
        c.circ(900, 560, 76, AREA, u, bg=QUIZ); c.text(900, 560, str(k) if k else '?', 72, DARK, u, w='Bold', bg=AREA)

def s_four(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Four', ANS), (' times the pizza', INK)], sw_out(T, 1))
    headline(c, [('12 vs 8: ', WID), ('2.25×', ANS)], sw_in(T, 1))
    m0 = 1 - hl(1)
    pizza(c, 1300, 540, 16, m0, slices=4)
    h8 = 4 * K
    c.rr(520 - h8, 540 - h8, 520 + h8, 540 + h8, 4, None, m0 * fd(T(0), .3), outline=AREA, ow=5)
    for k, (dx, dy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        u = fd(T(0), .5 + .35 * k, .5)
        cx, cy = 1300 + dx * h8, 540 + dy * h8
        c.rr(cx - h8, cy - h8, cx + h8, cy + h8, 4, None, m0 * u, outline=AREA, ow=5)
        c.text(cx + dx * h8 * .55, cy + dy * h8 * .55, str(k + 1), 52, AREA, m0 * u, w='Bold', stroke=3)
    pizza(c, 520, 540, 8, m0); c.text(520, 700, '8 in', 40, WID, m0, w='Bold'); c.text(1300, 790, '16 in', 40, WID, m0, w='Bold')
    m1 = hl(1)
    pizza(c, 600, 540, 8, m1); pizza(c, 1260, 540, 12, m1, glow=m1)
    c.text(600, 700, 'small, 8 in: 50', 38, WID, m1, w='Bold'); c.text(1260, 760, 'medium, 12 in: 113', 38, WID, m1, w='Bold')
    tag(c, 1260, 300, 'more than 2×', ANS, m1 * fd(T(1), .8), w=340)
    c.text(960, 860, 'Areas in square inches, rounded', 28, DIM, m1, w='Regular')

def s_price(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('74,476', PRICE), (' prices', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Bigger', ANS), (' = cheaper per inch', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Price ÷ ', PRICE), ('area', AREA)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Check the ', INK), ('inches', WID)], sw_in(T, 3))
    m0 = hl(0) * (1 - hl(1))
    # US map stand-in: a field of pins for pizza places
    rnd = random.Random(7)
    for k in range(60):
        px = 260 + rnd.random() * 1400; py = 300 + rnd.random() * 420
        c.circ(px, py, 9, PRICE, m0 * fd(T(0), .02 * k, .3))
    c.text(960, 800, '3,678 US pizza places (NPR, 2014)', 36, DIM, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    # bars: price per square inch falling with size (shape only, illustrative)
    if m1 > .01:
        c.rr(250, 260, 1670, 760, 26, CARD, m1 * .9)
        for k, (lab, h) in enumerate((('small', 300), ('medium', 220), ('large', 170), ('extra large', 140))):
            x = 450 + k * 340; hh = h * fd(T(1), .2 + .15 * k, .6)
            c.rr(x - 70, 700 - hh, x + 70, 700, 12, ANS if k == 3 else PRICE, m1, bg=CARD)
            c.text(x, 735, lab, 30, DIM, m1, w='Bold', bg=CARD)
        c.text(960, 300, 'cost per square inch', 34, PRICE, m1, w='Bold', bg=CARD)
        c.text(1640, 790, 'Illustrative shape, not NPR\'s data', 28, DIM, m1, anchor='rm', w='Regular')
    m2 = hl(2) * (1 - hl(3))
    pizza(c, 560, 520, 12, m2); pizza(c, 1340, 520, 18, m2, glow=m2)
    tag(c, 560, 780, '$12 ÷ 113 = 10.6¢', PRICE, m2, sub='per square inch', w=420)
    tag(c, 1340, 780, '$18 ÷ 254 = 7.1¢', ANS, m2, sub='per square inch', w=420)
    c.text(960, 300, 'Illustrative prices', 32, DIM, m2, w='Bold')
    m3 = hl(3)
    pizza(c, 440, 540, 14, m3)
    for x in (1240, 1560): pizza(c, x, 540, 12, m3)
    c.text(440, 760, 'one 14-inch: 154', 38, WID, m3, w='Bold'); c.text(1400, 760, 'two 12-inch: 226', 38, ANS, m3, w='Bold')
    c.text(960, 860, 'Size names vary: a "large" is often only 14 inches', 28, DIM, m3, w='Regular')

def s_crust(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Love ', INK), ('crust', CRUST), ('?', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Crust is the ', INK), ('edge', CRUST)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Two', CRUST), (': a third more crust', INK)], sw_in(T, 2))
    hi = .5 + .5 * math.sin(t * 3)
    m1 = hl(1)
    for x in (L1, L2): pizza(c, x, PY, 12, 1, crust_hi=m1 * hi)
    pizza(c, BIGX, PY, 18, 1, crust_hi=m1 * hi)
    for x, d in ((L1, 12), (L2, 12), (BIGX, 18)): c.circ(x, PY, d / 2 * K + 6, None, m1 * (.6 + .4 * hi), outline=(255, 236, 170), ow=12)
    m2 = hl(2)
    # unrolled crust lengths as bars
    c.rr(260, 800, 260 + 75.4 * 9, 830, 14, CRUST, m2 * fd(T(2), .3, 1.0)); c.text(260 + 75.4 * 9 + 20, 815, '75 in', 32, CRUST, m2, anchor='lm', w='Bold')
    c.rr(1100, 800, 1100 + 56.5 * 9, 830, 14, CRUST, m2 * fd(T(2), .3, 1.0)); c.text(1100 + 56.5 * 9 + 20, 815, '57 in', 32, CRUST, m2, anchor='lm', w='Bold')
    c.text(960, 860, 'Edge length = π × width', 28, DIM, m1, w='Regular')

def s_everywhere(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('The ', INK), ('square rule', AREA), (' is everywhere', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('65 vs 50 inch: ', WID), ('+70%', ANS)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('9 vs 8 inch tin: ', WID), ('+25%', ANS)], sw_in(T, 2))
    m0 = hl(0) * (1 - hl(1))
    for k, x in enumerate((420, 820, 1400)):
        h = 55 * (k + 1); a = m0 * fd(T(0), .2 + .25 * k)
        c.rr(x - h, 560 - h, x + h, 560 + h, 8, TILE, a, outline=AREA, ow=4)
        c.text(x, 560, f'{(k + 1) ** 2}×', 44 + 10 * k, AREA, a, w='Bold', bg=TILE)
        c.text(x, 560 + h + 50, f'width {k + 1}', 34, WID, a, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    tv(c, 560, 520, 50, m1); tv(c, 1330, 500, 65, m1)
    c.text(560, 760, '50-inch', 40, WID, m1, w='Bold'); c.text(1330, 790, '65-inch', 40, ANS, m1, w='Bold')
    c.text(1880, 858, 'Same shape of screen; diagonals drawn to scale', 28, DIM, m1, anchor='rm', w='Regular')
    m2 = hl(2)
    tin(c, 600, 530, 8, m2, fill=fd(T(2), .4, 1.0)); tin(c, 1320, 530, 9, m2, fill=fd(T(2), .8, 1.2))
    c.text(600, 790, '8-inch tin', 40, WID, m2, w='Bold'); c.text(1320, 820, '9-inch tin', 40, ANS, m2, w='Bold')

def s_recap(c, T, t):
    """Recap as three pizza boxes, opened one by one."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', AREA)], 1)
    items = ((1, 'Size is the width. You eat the area.', WID), (2, 'Double the width: four times the pizza.', AREA),
             (3, 'Compare price per square inch.', ANS))
    for ln, txt, col in items:
        m = hl(ln); x0 = 140 + (ln - 1) * 560; dy = 50 * (1 - m)
        c.rr(x0, 280 + dy, x0 + 520, 810 + dy, 14, (190, 150, 100), m)          # cardboard box
        c.rr(x0 + 20, 300 + dy, x0 + 500, 790 + dy, 10, CARD, m, outline=col, ow=5, bg=(190, 150, 100))
        c.circ(x0 + 70, 350 + dy, 36, col, m, bg=CARD); c.text(x0 + 70, 350 + dy, str(ln), 44, DARK, m, w='Bold', bg=col)
        if ln == 1: pizza(c, x0 + 260, 500 + dy, 7, m, bg=CARD); width_bar(c, x0 + 260, 500 + dy, 7, m, bg=CARD)
        if ln == 2:
            pizza(c, x0 + 170, 520 + dy, 4, m, bg=CARD); pizza(c, x0 + 330, 500 + dy, 8, m, bg=CARD)
            c.text(x0 + 170, 440 + dy, '1×', 36, AREA, m, w='Bold', bg=CARD); c.text(x0 + 430, 410 + dy, '4×', 40, AREA, m, w='Bold', bg=CARD)
        if ln == 3: c.text(x0 + 260, 500 + dy, '¢ / sq in', 60, PRICE, m, w='Bold', bg=CARD)
        for j, l in enumerate(wrap(c, txt, 38, 440, 'Bold')):
            c.text(x0 + 260, 670 + dy + j * 48, l, 38, INK, m, w='Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    pizza(c, 1560, 380, 15, 1, glow=1)
    for k, y in enumerate((830, 830)):
        pizza(c, 1330 + k * 300, y, 9, 1)
    c.text(1480, 700, 'vs', 60, DIM, 1, w='Bold')

SCENES = [
 ('THE QUESTION', ["One eighteen-inch pizza, or two twelve-inch pizzas. Which gives you more pizza?",
                   "Most people pick the two. Two sounds like more.",
                   "But the one big pizza wins. And the reason changes how you should compare sizes."], s_hook),
 ('THE TRAP', ["Pizza size is measured straight across the middle. That's the width.",
               "Eighteen is only one and a half times twelve. So it feels like one and a half times the pizza.",
               "But you don't eat the width. You eat the surface, the area."], s_trap),
 ('THE SQUARE RULE', ["Picture a square of tiles, ten by ten. That's one hundred tiles.",
                      "Make it twice as wide, twenty by twenty, and it holds four hundred. Four times as many.",
                      "Area grows with the size times itself. Circles follow the same rule."], s_square),
 ('THE NUMBERS', ["A circle's area is pi, times the radius, times the radius again.",
                  "A twelve-inch pizza has a radius of six. That's about one hundred and thirteen square inches.",
                  "Two of them make about two hundred and twenty-six.",
                  "An eighteen-inch pizza has a radius of nine. That's about two hundred and fifty-four. One pizza, more food."], s_math),
 ('QUICK QUESTION', ["Quick question. A sixteen-inch pizza, or an eight-inch one. Is the big one twice as much pizza? Or more?"], s_quiz),
 ('THE ANSWER', ["It's four times as much. Double the width, and you get four times the pizza.",
                 "Even a twelve-inch medium is more than twice an eight-inch small."], s_four),
 ('THE PRICE', ["Prices rarely grow that fast. In twenty fourteen, NPR looked at seventy-four thousand, four hundred and seventy-six prices from three thousand, six hundred and seventy-eight American pizza places.",
                "The bigger pizza was almost always a much better deal, per square inch.",
                "So the fair test is the price, divided by the area.",
                "And check the inches, not the names. A fourteen-inch large is less pizza than two twelve-inch mediums."], s_price),
 ('THE TWIST', ["One twist. If you love the crust, two pizzas win.",
                "The crust is the edge, and the edge only grows with the width.",
                "So two twelve-inch pizzas have about a third more crust than one eighteen-inch."], s_crust),
 ('EVERYWHERE', ["This square rule is everywhere.",
                 "A sixty-five-inch TV has about seventy percent more screen than a fifty-inch one.",
                 "And a nine-inch cake tin needs about a quarter more batter than an eight-inch tin."], s_everywhere),
 ('RECAP', ["Three things to keep.",
            "One: pizza size is the width, but you eat the area.",
            "Two: double the width, and you get four times the pizza.",
            "Three: compare the price per square inch. Unless you're in it for the crust.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('One ', INK), ('big', AREA), (' or two?', INK)], sw_out(T, 1), size=96)
    headline(c, [('One', ANS), (' big wins', INK)], sw_in(T, 1), size=96)
    win = hl_(T, 1)
    for x in (L1, L2): pizza(c, x, PY, 12, 1, spin=.1 * t)
    pizza(c, BIGX, PY, 18, 1, glow=win, spin=-.08 * t)
    c.text(510, 830, 'two 12-inch', 46, WID, 1, w='Bold'); c.text(BIGX, 860, 'one 18-inch', 46, WID, 1, w='Bold')
    c.text(1060, PY, 'or', 56, DIM, 1, w='Bold')
    tag(c, BIGX, 250, '254 sq in', ANS, win, w=300); tag(c, 510, 300, '226 sq in', DIM, win, w=280)

def short_square(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('2× wider = ', WID), ('4× area', AREA)], 1, size=96)
    cell = 26
    tiles(c, 260, 330, 10, cell, 1, lit=hl(1))
    c.text(260 + 5 * cell, 330 + 10 * cell + 40, '100 tiles', 40, DIM, 1, w='Bold')
    tiles(c, 900, 290, 20, cell, 1, grow=fd(T(0), 1.0, 1.6), lit=hl(1))
    c.text(900 + 10 * cell, 290 + 20 * cell + 36, '400 tiles', 40, AREA, 1, w='Bold')

SHORT_SCENES = [
 ('THE QUESTION', ["One eighteen-inch pizza, or two twelve-inch pizzas. Which is more?",
                   "The one big pizza. And it's not close."], short_hook),
 ('THE RULE', ["You order by the width, but you eat the area. Make a square of tiles twice as wide, and it holds four times as many.",
               "Area grows with the size times itself. Circles too."], short_square),
 ('THE NUMBERS', ["Area is pi, times the radius, times the radius again.",
                  "So a twelve-inch pizza is about one hundred and thirteen square inches.",
                  "Two of them make about two hundred and twenty-six.",
                  "And one eighteen-inch pizza is about two hundred and fifty-four. More food, from one box."], s_math),
 ('THE ANSWER', ["So compare the price per square inch, not the number of boxes.",
                 "One big pizza beats two."], card('Compare the area.', 'One big beats two.')),
]
SHORT_HITS = [(3, 1, 0.0)]
