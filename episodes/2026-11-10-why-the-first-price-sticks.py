"""Episode: Why the First Price You See Sticks (the anchoring effect: Tversky and Kahneman 1974, Northcraft and Neale 1987, Many Labs 1 2014, Guthrie and Orr)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why the First Price You See Sticks'       # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                          # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Why the first number sticks'                 # headline on the vertical Short
HITS = [(0, 0, 0.0), (1, 2, 0.0), (4, 2, 0.0)]             # the hook claim, the wheel result, the real answer to the sum
THUMB = ['FIRST', 'PRICE', 'WINS?']                        # 3 short words; price tag art on the right
MUSIC_LEVEL = 0.006                                        # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                             # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.4, (0, 1): 0.3, (1, 1): 0.4, (1, 2): 0.3, (2, 2): 0.4, (3, 1): 3.4, (4, 1): 0.4, (5, 1): 0.3, (6, 1): 0.3, (7, 1): 0.3, (8, 2): 0.3, (9, 3): 0.2}
SHORT_PAUSES = {(0, 1): 0.2, (1, 1): 0.2}
CAPTION_FIXES = {'nineteen seventy four': '1974', 'nineteen eighty seven': '1987', 'two thousand fourteen': '2014', 'sixty five': '65',
                 'twenty five percent': '25%', 'forty five percent': '45%', 'two thousand two hundred and fifty': '2,250', 'five hundred and twelve': '512',
                 'forty thousand three hundred and twenty': '40,320', 'thirty seven cents': '37 cents', 'twelve thousand feet': '12,000 feet',
                 'thirty four thousand': '34,000', 'two hundred dollars': '$200', 'ninety nine': '99', 'nought to a hundred': '0 to 100',
                 'eight times seven times six times five times four times three times two times one': '8 × 7 × 6 × 5 × 4 × 3 × 2 × 1',
                 'one times two times three': '1 × 2 × 3', ' ten ': ' 10 '}

# Colour code kept in every scene (lesson of 2026-11-01):
# the anchor number is always yellow, your guess is always blue, the true answer is always green, the pull / the error is always pink.
ANC = YE; GUESS = CY; TRUE = GR; PULL = PK
DARK = (20, 22, 38); PAPER = (236, 232, 220); QUIZ = (24, 60, 66)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def wheel(c, x, y, r, rot, a, hi=None, bg=BG):
    """An original 0-to-100 prize wheel in 20 segments; rot in degrees; the pointer sits at the top."""
    if a <= .01: return
    for k in range(20):
        a0 = -90 + k * 18 - 9 + rot
        col = (44, 52, 100) if k % 2 else (34, 40, 80)
        c.d.pieslice(((x - r) * c.k, (y - r) * c.k, (x + r) * c.k, (y + r) * c.k), a0, a0 + 18, fill=mix(col, a, bg), outline=mix((70, 80, 140), a, bg))
    for k in range(20):
        th = math.radians(-90 + k * 18 + rot); n = k * 5
        col = ANC if hi is not None and n == hi else INK
        c.text(x + .80 * r * math.cos(th), y + .80 * r * math.sin(th), str(n), int(r * .13), col, a, w='Bold', bg=(40, 46, 90))
    c.circ(x, y, r * .16, CARD, a, outline=(90, 100, 160), ow=4, bg=bg)
    poly(c, [(x - 26, y - r - 34), (x + 26, y - r - 34), (x, y - r + 14)], ANC, a, bg)

def wheel_rot(n, p, turns=2):
    """Rotation that brings number n to the pointer, spinning down as p goes 0 -> 1."""
    return -(n // 5) * 18 + 360 * turns * (1 - ease(p))

def numline(c, x0, x1, y, a, lo=0, hi=100, step=10, unit='%'):
    if a <= .01: return
    c.line([(x0, y), (x1, y)], DIM, 5, a)
    for v in range(lo, hi + 1, step):
        xx = x0 + (x1 - x0) * (v - lo) / (hi - lo)
        c.line([(xx, y - 14), (xx, y + 14)], DIM, 4, a)
        c.text(xx, y + 46, f'{v}{unit}', 30, DIM, a, w='Medium')

def nx(x0, x1, v, lo=0, hi=100): return x0 + (x1 - x0) * (v - lo) / (hi - lo)

def buoy(c, x, y, label, a, col=ANC, size=52):
    """The anchor number: a yellow disc with an anchor hook under it."""
    if a <= .01: return
    c.line([(x, y + 40), (x, y + 96)], col, 6, a)
    c.d.arc(((x - 30) * c.k, (y + 66) * c.k, (x + 30) * c.k, (y + 126) * c.k), 0, 180, fill=mix(col, a), width=int(6 * c.k))
    c.circ(x, y, 46, col, a)
    c.text(x, y, label, size if len(label) < 3 else size - 12, DARK, a, w='Bold', bg=col)

def pin(c, x, y, label, a, col=GUESS):
    """A guess marker: a blue pin with its value above."""
    if a <= .01: return
    poly(c, [(x - 22, y - 50), (x + 22, y - 50), (x, y)], col, a)
    c.circ(x, y - 62, 26, col, a)
    c.text(x, y - 126, label, 46, col, a, w='Bold')

def rope(c, x0, y0, x1, y1, a, col=PULL, sag=40):
    if a <= .01: return
    pts = [(x0 + (x1 - x0) * u / 20, y0 + (y1 - y0) * u / 20 + sag * math.sin(math.pi * u / 20)) for u in range(21)]
    c.line(pts, col, 4, a)

def tag(c, x, y, w, h, big, small, a, col=ANC, bg=BG, strike=False):
    """A shop price tag with a hole and string."""
    if a <= .01: return
    poly(c, [(x - w / 2 + 40, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2 + 40, y + h / 2), (x - w / 2, y)], PAPER, a, bg)
    c.circ(x - w / 2 + 34, y, 9, bg, a)
    c.text(x + 20, y - h * .2, small, int(h * .17), (90, 90, 110), a, w='Bold', bg=PAPER)
    c.text(x + 20, y + h * .14, big, int(h * .36), (30, 34, 60), a, w='Bold', bg=PAPER)
    if strike: c.line([(x - w / 2 + 70, y + h * .26), (x + w / 2 - 30, y - h * .02)], PULL, 8, a, bg=PAPER)

def house(c, x, y, s, a, bg=BG):
    if a <= .01: return
    poly(c, [(x - 170 * s, y - 40 * s), (x, y - 170 * s), (x + 170 * s, y - 40 * s)], (200, 110, 90), a, bg)
    c.rr(x - 140 * s, y - 40 * s, x + 140 * s, y + 140 * s, 6, (210, 200, 180), a, bg=bg)
    c.rr(x - 30 * s, y + 40 * s, x + 30 * s, y + 140 * s, 4, (110, 80, 60), a, bg=(210, 200, 180))
    for dx in (-90, 90):
        c.rr(x + (dx - 30) * s, y + 0 * s, x + (dx + 30) * s, y + 60 * s, 4, (120, 170, 220), a, bg=(210, 200, 180))

def die(c, x, y, s, n, a, bg=BG):
    if a <= .01: return
    c.rr(x - 50 * s, y - 50 * s, x + 50 * s, y + 50 * s, 16 * s, PAPER, a, bg=bg)
    spots = {1: [(0, 0)], 3: [(-1, -1), (0, 0), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
    for dx, dy in spots[n]: c.circ(x + dx * 25 * s, y + dy * 25 * s, 8 * s, (30, 34, 60), a, bg=PAPER)

def person(c, x, y, s, a, col=DIM):
    c.circ(x, y - 50 * s, 22 * s, col, a)
    c.d.pieslice(((x - 40 * s) * c.k, (y - 22 * s) * c.k, (x + 40 * s) * c.k, (y + 58 * s) * c.k), 180, 360, fill=mix(col, a))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

# ---- scenes ----
def s_hook(c, T, t):
    """Reaffirm the title, show the result, then signpost the value (lesson of 2026-11-10, Ali Abdaal's hook formula)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'The first price you see sticks', 88, ANC, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A spin of a wheel moved guesses 20 points', 76, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Why, and how to protect your wallet', 80, TRUE, sw_in(T, 2), w='Bold')
    m = 1 - hl(1)
    tag(c, 700, 520, 520, 300, '$200', 'WAS', m, strike=True)
    tag(c, 1240, 560, 520, 300, '$99', 'NOW', m * fd(t, .6))
    c.text(960, 800, '(example prices)', 32, DIM, m, w='Regular')
    m1 = hl(1)
    numline(c, 300, 1620, 620, m1)
    for n, g, dx in ((10, 25, 0), (65, 45, 1)):
        xa, xg = nx(300, 1620, n), nx(300, 1620, g)
        buoy(c, xa, 380, str(n), m1 * fd(T(1), .2 + dx * .5))
        pin(c, xg, 600, f'{g}%', m1 * fd(T(1), .9 + dx * .5))
        rope(c, xa, 420, xg, 540, m1 * fd(T(1), 1.1 + dx * .5) * .8)

def s_wheel(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, '1974: a rigged wheel of fortune', 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'What % of UN members are African countries?', 70, GUESS, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'The wheel pulled the guesses', 88, PULL, sw_in(T, 2), w='Bold')
    # two wheels: one lands on 10, one on 65
    m = 1 - hl(2) * .7
    p1 = clamp(T(0) / 3.2) if T(0) > 0 else 0
    wheel(c, 420, 530, 250, wheel_rot(10, p1), m, hi=10 if p1 >= 1 else None)
    wheel(c, 1500, 530, 250, wheel_rot(65, p1, 3), m, hi=65 if p1 >= 1 else None)
    c.text(960, 470, 'Secretly stops', 44, DIM, hl(0) * fd(T(0), 2.0) * (1 - hl(1)), w='Bold')
    c.text(960, 540, 'only on 10 or 65', 50, ANC, hl(0) * fd(T(0), 2.2) * (1 - hl(1)), w='Bold')
    c.text(960, 520, '?', 160, GUESS, hl(1) * (1 - hl(2)) * (.7 + .3 * math.sin(t * 4)), w='Bold')
    m2 = hl(2)
    for x, n, g in ((420, 10, 25), (1500, 65, 45)):
        c.rr(x - 250, 560, x + 250, 840, 26, CARD, m2, outline=GUESS, ow=4)
        c.text(x, 630, f'saw {n}', 50, ANC, m2, w='Bold', bg=CARD)
        c.text(x, 750, f'guessed {g}%', 66, GUESS, m2 * fd(T(2), .3 + (x > 900) * 2.2), w='Bold', bg=CARD)
    c.text(1880, 858, 'Source: Tversky and Kahneman 1974 (typical answers). Wheel drawn for this video', 28, DIM, 1, anchor='rm', w='Regular')

def s_adjust(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Start from the number in front of you', 80, ANC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Adjust until it feels about right', 84, GUESS, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'But you stop too early', 92, PULL, sw_in(T, 2), w='Bold')
    x0, x1, y = 260, 1660, 640
    numline(c, x0, x1, y, 1)
    xa = nx(x0, x1, 10)
    buoy(c, xa, 400, '10', 1)
    # "feels about right" zone and the true spot (illustrative)
    zr = hl(1)
    c.rr(nx(x0, x1, 22), y - 30, nx(x0, x1, 60), y + 30, 14, None, zr * .9, outline=TRUE, ow=4)
    c.text(nx(x0, x1, 41), y - 80, 'feels about right', 38, TRUE, zr, w='Bold')
    steps = 3 * hl(1) * fd(T(1), .3, 2.4)
    xs = xa
    for k in range(3):
        u = clamp(steps - k)
        if u <= 0: break
        nxp = xa + (nx(x0, x1, 25) - xa) * (k + u) / 3
        c.arrow(xs, y - 150 + k * 10, nxp, y - 150 + k * 10, GUESS, 6, 1, 18) if u > .1 else None
        xs = nxp
    xg = xa + (nx(x0, x1, 25) - xa) * clamp(steps / 3)
    pin(c, xg, y - 10, '', hl(1))
    m2 = hl(2)
    c.text(xg + 30, 820, 'stops at the near edge', 44, PULL, m2, 'lm', 'Bold')
    c.line([(xg, 790), (xg, 760)], PULL, 4, m2)
    c.text(1880, 858, 'Illustrative: the idea Tversky and Kahneman called anchoring and adjustment', 28, DIM, 1, anchor='rm', w='Regular')

SUM = '8 × 7 × 6 × 5 × 4 × 3 × 2 × 1'
def s_quiz(c, T, t):
    """Pattern interrupt: the frame fills with colour, with a 3-2-1 ring (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(560, 110, 1360, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK TEST', 78, ANC, 1, w='Bold', bg=DARK)
    c.text(960, 300, 'Guess fast. Three seconds. No calculator.', 54, INK, hl(0), w='Bold', bg=QUIZ)
    m = hl(1)
    c.rr(220, 400, 1700, 600, 30, PAPER, m, bg=QUIZ)
    c.text(960, 500, SUM + ' = ?', 92, (30, 34, 60), m, w='Bold', bg=PAPER)
    end = T(1) - 6.6
    if end > 0:
        q = clamp(end / 3.2); n = 3 - int(min(q * 3, 2.9))
        c.circ(960, 740, 84, DARK, 1, bg=QUIZ); ring(c, 960, 740, 70, 1 - q, ANC, 1, 10)
        c.text(960, 740, str(n), 76, INK, 1, w='Bold', bg=DARK)

def s_sum(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Starting with 8: typical guess 2,250', 80, GUESS, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Same sum, starting with 1: just 512', 80, GUESS, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'The real answer: 40,320', 92, TRUE, sw_in(T, 2), w='Bold')
    x0, wmax = 520, 1300
    rows = ((0, '8 × 7 × 6 ...', 2250, GUESS, '2,250'), (1, '1 × 2 × 3 ...', 512, GUESS, '512'), (2, 'Real answer', 40320, TRUE, '40,320'))
    for k, (ln, lab, v, col, txt) in enumerate(rows):
        m = hl(ln); yy = 360 + k * 170
        c.text(x0 - 30, yy, lab, 48, ANC if k < 2 else TRUE, m, 'rm', 'Bold')
        L = max(8, wmax * v / 40320 * fd(T(ln), .3, 1.6 if k == 2 else .6))
        c.rr(x0, yy - 42, x0 + L, yy + 42, 12, col, m)
        c.text(x0 + L + 24 if k < 2 else x0 + L - 24, yy, txt, 56, col if k < 2 else DARK, m, 'lm' if k < 2 else 'rm', 'Bold', bg=BG if k < 2 else col)
    m2 = hl(2) * fd(T(2), 2.2)
    c.text(960, 800, 'Both groups anchored on the first few steps', 46, PULL, m2, w='Bold')
    c.text(1880, 858, 'Source: Tversky and Kahneman 1974 (median guesses, 5 seconds to answer)', 28, DIM, 1, anchor='rm', w='Regular')

def s_house(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Experts too', 92, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Same house, different listing prices', 80, ANC, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, '"I didn\'t use the listing price"', 80, PULL, sw_in(T, 2) * sw_out(T, 3), w='Bold')
    c.text(960, 172, 'Legal experts, swayed by random numbers', 76, PULL, sw_in(T, 3), w='Bold')
    m = 1 - hl(3)
    house(c, 960, 560, 1.3, m * fd(T(0), .2))
    for k in range(3):
        person(c, 220 + k * 110, 640, 1.0, m * fd(T(0), .5 + k * .1), DIM)
    c.text(330, 730, 'students', 36, DIM, m, w='Bold')
    for k in range(3):
        person(c, 1480 + k * 110, 640, 1.0, m * fd(T(0), .8 + k * .1), GUESS)
    c.text(1590, 730, 'estate agents', 36, GUESS, m, w='Bold')
    mt = m * hl(1)
    tag(c, 560, 340, 300, 150, 'HIGH', 'LISTED', mt)
    tag(c, 1360, 340, 300, 150, 'LOW', 'LISTED', mt * fd(T(1), .8))
    c.text(960, 810, 'Estimates moved with the listing price, for both groups', 40, ANC, m * hl(1) * fd(T(1), 2.0), w='Bold')
    m2 = m * hl(2)
    c.rr(1400, 440, 1860, 550, 30, PAPER, m2)
    poly(c, [(1560, 550), (1620, 550), (1590, 580)], PAPER, m2)
    c.text(1630, 495, 'Not me.', 56, (30, 34, 60), m2, w='Bold', bg=PAPER)
    m3 = hl(3)
    c.rr(560, 360, 1360, 800, 30, CARD, m3, outline=PULL, ow=4)
    die(c, 760, 560, 1.6, 3, m3 * fd(T(3), .2), bg=CARD)
    die(c, 960, 560, 1.6, 6, m3 * fd(T(3), .4), bg=CARD)
    die(c, 1160, 560, 1.6, 1, m3 * fd(T(3), .6), bg=CARD)
    c.text(960, 730, 'prison-sentence decisions', 42, INK, m3, w='Bold', bg=CARD)
    c.text(1880, 858, 'Sources: Northcraft and Neale 1987; Englich, Mussweiler and Strack 2006', 28, DIM, 1, anchor='rm', w='Regular')

def s_daily(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Anchors are everywhere', 92, ANC, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A number in your head first', 88, ANC, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Opening offers pull the final deal', 82, PULL, sw_in(T, 2), w='Bold')
    m = 1 - hl(2)
    # three everyday anchors, dealt one by one
    p = T(1)
    a1 = m * fd(p, .2); a2 = m * fd(p, 1.8); a3 = m * fd(p, 4.0)
    c.rr(140, 300, 640, 800, 30, CARD, a1, outline=ANC, ow=4)
    tag(c, 390, 460, 360, 170, '$200', 'WAS', a1, strike=True, bg=CARD)
    c.text(390, 640, 'the "was" price', 46, INK, a1, w='Bold', bg=CARD)
    c.rr(710, 300, 1210, 800, 30, CARD, a2, outline=ANC, ow=4)
    c.rr(800, 340, 1120, 600, 12, PAPER, a2, bg=CARD)
    for j, (dish, pr) in enumerate((('Lobster', '$95'), ('Steak', '$42'), ('Pasta', '$24'))):
        col = (190, 40, 80) if j == 0 else (30, 34, 60)
        c.text(830, 400 + j * 72, dish, 36, col, a2, 'lm', 'Bold', bg=PAPER); c.text(1090, 400 + j * 72, pr, 36, col, a2, 'rm', 'Bold', bg=PAPER)
    c.text(960, 660, 'the top of the menu', 46, INK, a2, w='Bold', bg=CARD)
    c.text(960, 720, '(example)', 30, DIM, a2, w='Regular', bg=CARD)
    c.rr(1280, 300, 1780, 800, 30, CARD, a3, outline=ANC, ow=4)
    buoy(c, 1530, 430, '$', a3, size=60)
    c.text(1530, 640, 'the first salary', 46, INK, a3, w='Bold', bg=CARD)
    c.text(1530, 700, 'number', 46, INK, a3, w='Bold', bg=CARD)
    m2 = hl(2)
    c.rr(300, 330, 1620, 800, 34, CARD, m2, outline=PULL, ow=4)
    c.text(700, 480, '+$1', 150, ANC, m2, w='Bold', bg=CARD)
    c.text(700, 620, 'in the opening offer', 44, INK, m2, w='Bold', bg=CARD)
    c.arrow(1000, 520, 1120, 520, PULL, 8, m2 * fd(T(2), 1.0), 26)
    c.text(1340, 480, '+37¢', 150, PULL, m2 * fd(T(2), 2.4), w='Bold', bg=CARD)
    c.text(1340, 620, 'in the final deal', 44, INK, m2 * fd(T(2), 2.4), w='Bold', bg=CARD)
    c.text(960, 730, 'on average, across negotiation studies', 34, DIM, m2, w='Regular', bg=CARD)
    c.text(1880, 858, 'Source: Guthrie and Orr review, via Harvard Program on Negotiation', 28, DIM, 1, anchor='rm', w='Regular')

def s_limits(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'To be fair: not every result holds up', 80, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'But the pull on guesses is solid', 84, TRUE, sw_in(T, 1), w='Bold')
    m = 1 - hl(1)
    c.rr(360, 320, 1560, 780, 30, CARD, m, outline=(70, 80, 140), ow=3)
    c.text(960, 400, 'A random number changes what people will pay?', 46, INK, m, w='Bold', bg=CARD)
    for k, ok in enumerate((1, 1, 0, 0)):
        mm = m * fd(T(0), 1.0 + k * .35)
        x = 660 + k * 200
        (c.check if ok else c.cross)(x, 560, 50, TRUE if ok else PULL, mm)
    c.text(960, 680, 'repeats have been mixed', 52, PULL, m * fd(T(0), 2.8), w='Bold', bg=CARD)
    c.text(960, 740, '(ticks and crosses illustrative)', 28, DIM, m * fd(T(0), 2.8), w='Regular', bg=CARD)
    m1 = hl(1)
    base = 770; top = 300; hmax = 40000
    yv = lambda v: base - (base - top) * v / hmax
    c.line([(380, base), (1540, base)], DIM, 4, m1)
    poly(c, [(560, base), (900, yv(29032)), (1240, base)], (110, 120, 150), m1)
    poly(c, [(820, yv(26000)), (900, yv(29032)), (980, yv(26000))], PAPER, m1)
    c.line([(380, yv(29032)), (1540, yv(29032))], TRUE, 4, m1 * fd(T(1), 4.0))
    c.text(1560, yv(29032), 'real: 29,032 ft', 38, TRUE, m1 * fd(T(1), 4.0), 'lm', 'Bold')
    for x, v, lab, dl in ((420, 11800, 'after a low number', 1.8), (1380, 34500, 'after a high number', 2.8)):
        mm = m1 * fd(T(1), dl)
        c.rr(x - 40, yv(v) - 6, x + 40, base, 10, GUESS, mm)
        c.text(x, yv(v) - 44, f'{v / 1000:.1f}k ft', 40, GUESS, mm, w='Bold')
        c.text(x, base + 36, lab, 30, DIM, mm, w='Bold')
    c.text(1880, 858, 'Source: Many Labs replication, Klein et al. 2014 (average guesses), via LessWrong review', 28, DIM, 1, anchor='rm', w='Regular')

def s_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Knowing about it is not enough', 84, PULL, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Give your brain a second starting point', 78, TRUE, sw_in(T, 1), w='Bold')
    m = 1 - hl(1)
    x0, x1, y = 300, 1620, 600
    numline(c, x0, x1, y, m, 0, 200, 25, '')
    buoy(c, nx(x0, x1, 180, 0, 200), 360, '180', m * fd(T(0), .3), size=48)
    pin(c, nx(x0, x1, 150, 0, 200), 580, 'still pulled', m * fd(T(0), 1.2))
    rope(c, nx(x0, x1, 180, 0, 200), 400, nx(x0, x1, 150, 0, 200), 520, m * fd(T(0), 1.4))
    c.text(960, 800, 'Warned people still anchored (illustrative numbers)', 38, DIM, m, w='Regular')
    m1 = hl(1)
    numline(c, x0, x1, y, m1, 0, 200, 25, '')
    buoy(c, nx(x0, x1, 180, 0, 200), 360, '180', m1, size=48)
    buoy(c, nx(x0, x1, 90, 0, 200), 360, '90', m1 * fd(T(1), 1.0), col=TRUE)
    c.text(nx(x0, x1, 90, 0, 200), 260, 'your number', 40, TRUE, m1 * fd(T(1), 1.0), w='Bold')
    c.text(nx(x0, x1, 180, 0, 200), 260, "the shop's", 40, ANC, m1, w='Bold')
    c.text(960, 790, 'Price it elsewhere, or set your limit before you look', 46, TRUE, m1 * fd(T(1), 2.0), w='Bold')
    c.text(1880, 858, 'Sources: Wilson et al. 1996, via Wikipedia; Kahneman, Thinking, Fast and Slow', 28, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    """Recap as three price tags hung on a line (layout change)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 80, INK, sw_in(T, 0), w='Bold')
    c.line([(140, 300), (1780, 300)], DIM, 3, hl(1))
    rows = ((1, 'The first number becomes your starting point', ANC),
            (2, 'You adjust away from it, but stop too soon', PULL),
            (3, 'Bring your own number before you look', TRUE))
    for ln, txt, col in rows:
        m = hl(ln); x = (400, 960, 1520)[ln - 1]; sw = 6 * math.sin(t * 1.4 + ln) * m; dy = 40 * (1 - m)
        c.line([(x, 300), (x, 340 + dy)], DIM, 3, m)
        c.rr(x - 250 + sw, 340 + dy, x + 250 + sw, 760 + dy, 28, CARD, m, outline=col, ow=5)
        c.circ(x + sw, 420 + dy, 42, col, m, bg=CARD); c.text(x + sw, 420 + dy, str(ln), 48, DARK, m, w='Bold', bg=col)
        ls = wrap(c, txt, 46, 420, 'Bold')
        for j, l in enumerate(ls):
            c.text(x + sw, 590 + dy + (j - (len(ls) - 1) / 2) * 58, l, 46, INK, m, w='Bold', bg=CARD)
    c.text(960, 840, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    tag(c, 1500, 360, 560, 300, '$200', 'WAS', 1, strike=True)
    tag(c, 1540, 700, 560, 300, '$99', 'NOW', 1)

SCENES = [
 ('THE HOOK', ["The first price you see sticks in your head, and it changes what feels fair.",
               "In one famous test, a single spin of a wheel moved people's guesses by twenty points.",
               "Here's why, and one simple way to protect your wallet."], s_hook),
 ('THE WHEEL', ["In nineteen seventy four, Amos Tversky and Daniel Kahneman used a wheel of fortune, rigged to stop only on ten or sixty five.",
                "Then they asked: what percentage of United Nations members are African countries?",
                "People who saw ten typically guessed twenty five percent. Those who saw sixty five guessed forty five percent."], s_wheel),
 ('THE REASON', ["Here's the idea they proposed. You start from the number in front of you.",
                 "Then you adjust away from it, step by step, until the answer feels about right.",
                 "But you stop at the first answer that seems okay, too close to where you started."], s_adjust),
 ('QUICK TEST', ["Quick test. Guess fast. Three seconds.",
                 "What is eight times seven times six times five times four times three times two times one?"], s_quiz),
 ('THE ANSWER', ["People shown it starting with eight typically guessed two thousand two hundred and fifty.",
                 "People shown one times two times three, the same sum backwards, guessed just five hundred and twelve.",
                 "The real answer is forty thousand three hundred and twenty. Both groups anchored on the first few steps."], s_sum),
 ('EXPERTS TOO', ["It isn't just students.",
                  "In a nineteen eighty seven study, students and estate agents saw the same house with different listing prices. Both groups' estimates moved with that price.",
                  "The agents said they hadn't used it.",
                  "In another study, experienced legal experts setting prison sentences were swayed by plainly random numbers."], s_house),
 ('EVERY DAY', ["You meet anchors every day.",
                "A was price on a sale tag. The most expensive dish at the top of a menu. The first number in a salary talk.",
                "In negotiations, one review found each extra dollar in the opening offer raised the final deal by about thirty seven cents."], s_daily),
 ('THE LIMITS', ["To be fair, not every result holds up. Random numbers swaying what people will pay have had mixed repeats.",
                 "But the pull on guesses is solid. In a two thousand fourteen repeat with thousands of people, average Everest guesses were about twelve thousand feet after a low number, and thirty four thousand after a high one."], s_limits),
 ('THE FIX', ["Knowing about it isn't enough. In one study, people who were warned about the effect still anchored.",
              "So give your brain a second starting point. Check the price elsewhere, or set your own limit before you look."], s_fix),
 ('RECAP', ["Three things to keep.",
            "One: the first number you see becomes your starting point.",
            "Two: you adjust away from it, but you stop too soon.",
            "Three: bring your own number before you look at theirs.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    c.text(960, 172, 'The first number you see pulls your guess', 74, ANC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A wheel that stops only on 10 or 65', 80, INK, sw_in(T, 1), w='Bold')
    p = clamp(T(1) / 3.0) if T(1) > 0 else 0
    wheel(c, 560, 540, 270, wheel_rot(10, p), 1, hi=10 if p >= 1 else None)
    wheel(c, 1360, 540, 270, wheel_rot(65, p, 3), 1, hi=65 if p >= 1 else None)

def short_result(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'What % of UN members are African?', 80, GUESS, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Saw 10: guessed 25%. Saw 65: guessed 45%', 74, GUESS, sw_in(T, 1), w='Bold')
    numline(c, 300, 1620, 640, 1)
    for n, g, dx in ((10, 25, 0), (65, 45, 1)):
        xa, xg = nx(300, 1620, n), nx(300, 1620, g)
        buoy(c, xa, 380, str(n), fd(T(0), .2 + dx * .3))
        pin(c, xg, 620, f'{g}%', hl(1) * fd(T(1), .4 + dx * 1.4))
        rope(c, xa, 420, xg, 560, hl(1) * fd(T(1), .6 + dx * 1.4) * .8)

def short_reason(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'You start from the number you saw', 82, ANC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Then adjust, and stop too soon', 84, PULL, sw_in(T, 1), w='Bold')
    x0, x1, y = 260, 1660, 640
    numline(c, x0, x1, y, 1)
    xa = nx(x0, x1, 10); buoy(c, xa, 400, '10', 1)
    c.rr(nx(x0, x1, 22), y - 30, nx(x0, x1, 60), y + 30, 14, None, hl(1) * .9, outline=TRUE, ow=4)
    c.text(nx(x0, x1, 41), y - 80, 'feels about right', 38, TRUE, hl(1), w='Bold')
    xg = xa + (nx(x0, x1, 25) - xa) * hl(1) * fd(T(1), .3, 1.8)
    pin(c, xg, y - 10, '', 1)
    c.text(1880, 858, 'Illustrative', 28, DIM, 1, anchor='rm', w='Regular')

def short_daily(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A "was" price is an anchor too', 84, ANC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Bring your own number first', 88, TRUE, sw_in(T, 1), w='Bold')
    tag(c, 640, 520, 520, 300, '$200', 'WAS', 1, strike=True)
    tag(c, 1240, 560, 520, 300, '$99', 'NOW', fd(T(0), .8))
    c.text(960, 800, '(example prices)', 32, DIM, 1, w='Regular')

SHORT_SCENES = [
 ('THE HOOK', ["The first number you see pulls your guess. Even a random one.",
               "In one famous study, a wheel of fortune was rigged to stop only on ten or sixty five."], short_open),
 ('THE RESULT', ["Then people guessed what percentage of United Nations members are African countries.",
                 "Those who saw ten typically said twenty five percent. Those who saw sixty five said forty five percent."], short_result),
 ('THE REASON', ["Why? You start from the number in front of you.",
                 "Then you adjust, but you stop as soon as the answer feels okay. Too close to where you started."], short_reason),
 ('YOUR WALLET', ["That's why a was price on a sale tag is so powerful.",
                  "Before you look, check the price elsewhere, or set your own limit."], short_daily),
 ('THE ANSWER', ["So the first number becomes your starting point.",
                 "Pick your own number first."], card('The first number is your start.', 'Pick your own first.')),
]
SHORT_HITS = [(4, 1, 0.0)]
