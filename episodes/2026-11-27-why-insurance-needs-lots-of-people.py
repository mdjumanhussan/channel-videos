"""Episode: Why Insurance Only Works With Lots of People (risk pooling, the $2.50 split, ten cars vs 100,000, law of large numbers, what breaks the pool)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Insurance Really Works'                  # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.88                            # about 155 wpm at 0.88 (lesson of 2026-11-25)
SHORT_HOOK = 'Your house burns down. Who pays?'              # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 0, 0.0), (8, 0, 0.0)]              # "where does the rest come from?", "It's B", the answer
THUMB = ['1 HOUSE BURNS', 'WHO PAYS?']
THUMB_COLS = [PK, YE]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.9, (4, 0): 3.4, (3, 1): 0.6}
SHORT_PAUSES = {(0, 1): 0.5}
QZ = 11.2                                                    # length of the quiz line (set from tl.json after audio)
CAPTION_FIXES = {'three hundred thousand dollars': '$300,000', 'a thousand dollars': '$1,000', 'two dollars fifty': '$2.50',
                 'a hundred thousand': '100,000', 'two hundred and fifty': '250', 'ten thousand': '10,000'}

# Colour code kept in every scene:
# your house / your money pink, the pool of other people cyan, money yellow, predictable green, danger (correlated risk) purple-red.
YOU = PK; POOL = CY; CASH = YE; OK = GR; RISK = (255, 120, 80)
QUIZ = (46, 28, 74); DARK = (20, 22, 38); WALL = (70, 80, 130); ROOF = (120, 90, 170); SEA = (30, 70, 120)
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
def house(c, x, y, s, a, col=WALL, roof=ROOF, bg=BG, lit=False):
    """A simple house: body, stepped roof, door and window."""
    if a <= .01: return
    c.rr(x - 90 * s, y - 60 * s, x + 90 * s, y + 80 * s, 8 * s, col, a, bg=bg)
    for k in range(4):
        w = 110 - 26 * k
        c.rr(x - w * s, y - 70 * s - 26 * k * s, x + w * s, y - 48 * s - 26 * k * s, 6 * s, roof, a, bg=bg)
    c.rr(x - 22 * s, y + 10 * s, x + 22 * s, y + 80 * s, 6 * s, DARK, a, bg=col)
    c.rr(x + 36 * s, y - 30 * s, x + 72 * s, y + 4 * s, 4 * s, CASH if lit else DARK, a, bg=col)

def flames(c, x, y, s, a, t, bg=BG):
    """Flickering flames over a point (layered circles)."""
    if a <= .01: return
    for k in range(7):
        ph = t * 5 + k * 1.7
        dx = (k - 3) * 30 * s; r = (46 - abs(k - 3) * 8 + 8 * math.sin(ph)) * s
        c.circ(x + dx, y - r * .6, r, (255, 110, 60), a, bg=bg)
        c.circ(x + dx, y - r * .4, r * .6, (255, 200, 70), a, bg=(255, 110, 60))

def coin(c, x, y, r, a, bg=BG, lab='$'):
    if a <= .01: return
    c.circ(x, y, r, CASH, a, bg=bg); c.circ(x, y, r * .72, None, a, outline=(200, 150, 40), ow=max(2, r * .1), bg=CASH)
    if r > 14: c.text(x, y, lab, int(r * 1.1), (140, 100, 20), a, w='Bold', bg=CASH)

def person(c, x, y, s, a, col=POOL, bg=BG):
    if a <= .01: return
    c.circ(x, y - 34 * s, 16 * s, col, a, bg=bg)
    c.rr(x - 20 * s, y - 14 * s, x + 20 * s, y + 30 * s, 12 * s, col, a, bg=bg)

def pot(c, x, y, s, a, fill, bg=BG):
    """A big jar (the pool of premiums); `fill` 0..1 is how full it is."""
    if a <= .01: return
    c.rr(x - 150 * s, y - 170 * s, x + 150 * s, y + 150 * s, 50 * s, CARD, a, outline=POOL, ow=6, bg=bg)
    c.rr(x - 110 * s, y - 200 * s, x + 110 * s, y - 165 * s, 14 * s, POOL, a, bg=bg)
    h = 300 * s * clamp(fill)
    if h > 4: c.rr(x - 136 * s, y + 136 * s - h, x + 136 * s, y + 136 * s, 40 * s, CASH, a * .9, bg=CARD)

def car(c, x, y, s, a, col=POOL, bg=BG):
    if a <= .01: return
    c.rr(x - 60 * s, y - 20 * s, x + 60 * s, y + 14 * s, 12 * s, col, a, bg=bg)
    c.rr(x - 34 * s, y - 44 * s, x + 30 * s, y - 16 * s, 10 * s, col, a, bg=bg)
    c.circ(x - 34 * s, y + 16 * s, 13 * s, DARK, a, bg=bg); c.circ(x + 34 * s, y + 16 * s, 13 * s, DARK, a, bg=bg)

def swirl(c, x, y, r, a, t, bg=BG):
    """A storm drawn as a spinning spiral."""
    if a <= .01: return
    for arm in range(3):
        pts = []
        for k in range(40):
            u = k / 39; ang = t * 1.5 + arm * 2.094 + u * 5.0
            pts.append((x + r * u * math.cos(ang), y + r * u * math.sin(ang) * .8))
        c.line(pts, RISK, 10, a * .9, bg=bg)
    c.circ(x, y, r * .12, DIM, a, bg=bg)

# Simulated thefts for the bar charts (fixed seed so every frame matches): 10 cars and 100,000 cars, 1 in 10 a year.
_rng = random.Random(21)
SMALL = [sum(_rng.random() < .1 for _ in range(10)) for _ in range(12)]
_rng = random.Random(5)
BIG = [round(_rng.gauss(10000, 94.9)) for _ in range(12)]     # normal approximation, sd = sqrt(100000 x 0.1 x 0.9)

# ---------- scenes ----------
def s_hook(c, T, t):
    """The fire from frame one, then the two numbers that don't add up."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Your ', INK), ('house', YOU), (' burns down', INK)], sw_out(T, 1))
    headline(c, [('Rebuild: ', INK), ('$300,000', YOU)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Who pays ', INK), ('the rest', CASH), ('?', INK)], sw_in(T, 2))
    house(c, 560, 560, 1.6, 1, col=(80, 70, 90))
    flames(c, 560, 440, 1.6, 1, t)
    m1 = hl(1)
    if m1 > .01:
        c.rr(1060, 330, 1700, 470, 26, CARD, m1, outline=YOU, ow=4)
        c.text(1380, 400, 'rebuild: $300,000', 54, YOU, m1, w='Bold', bg=CARD)
        u = fd(T(1), 1.2) if T(1) > -.1 else 0
        c.rr(1060, 520, 1700, 660, 26, CARD, m1 * u, outline=CASH, ow=4)
        c.text(1380, 590, 'you paid: $1,000 a year', 50, CASH, m1 * u, w='Bold', bg=CARD)
    m2 = hl(2)
    if m2 > .01:
        c.text(1380, 760, '?', 140, CASH, m2, w='Bold')
    c.text(960, 860, 'illustrative numbers', 28, DIM, m1, w='Regular')

def s_pool(c, T, t):
    """A crowd of houses, each dropping a coin into one jar; one house is on fire and gets paid."""
    hl = lambda i: hl_(T, i)
    headline(c, [('From ', INK), ('everyone else', POOL)], sw_out(T, 1))
    headline(c, [('Most ', INK), ('never claim', OK), (' this year', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('They pay for ', INK), ('the few', YOU)], sw_in(T, 2))
    pot(c, 960, 560, 1.0, 1, .25 + .5 * hl(1))
    for k in range(10):
        x = 180 + k * 175 if k < 5 else 180 + (k - 5) * 175 + 1000
        x = [200, 330, 460, 590, 720][k] if k < 5 else [1200, 1330, 1460, 1590, 1720][k - 5]
        y = 380 if k % 2 == 0 else 640
        fire = (k == 7)
        house(c, x, y, .55, 1, col=(80, 70, 90) if fire else WALL)
        if fire: flames(c, x, y - 40, .55, 1, t)
        if not fire:   # coin falls toward the jar
            u = ((t * .35) + k * .13) % 1.0
            cx = x + (960 - x) * u; cy = y - 60 - 120 * math.sin(3.14 * u) + 80 * u
            coin(c, cx, cy, 16, hl(1) * (1 - u * .5) + .3 * (1 - hl(1)))
    m2 = hl(2)
    if m2 > .01:   # the jar pays the burning house
        c.arrow(1100, 520, 1420, 600, CASH, 8, m2, 26)
        c.text(1330, 780, 'paid from the pool', 40, CASH, m2, w='Bold')
    m1 = hl(1)
    c.text(960, 820, 'premiums from everyone, claims for a few', 34, POOL, m1 * (1 - m2), w='Bold')

def s_split(c, T, t):
    """100,000 people, 250 claims of $1,000: $250,000, or $2.50 each."""
    hl = lambda i: hl_(T, i)
    headline(c, [('100,000', POOL), (' people', INK)], sw_out(T, 1))
    headline(c, [('About ', INK), ('250', YOU), (' claim $1,000', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Cost each: ', INK), ('$2.50', CASH)], sw_in(T, 2))
    # a grid of dots (each dot = many people); a few light pink as claims
    lit = hl(1)
    for r in range(8):
        for k in range(25):
            x = 300 + k * 54; y = 300 + r * 54
            claim = (r * 25 + k) in (17, 63, 101, 144, 188)
            col = mix(YOU, lit, POOL) if claim else POOL
            c.circ(x, y, 16 if not claim else 16 + 6 * lit, col, .35 + .65 * (1 - hl(2) * .5))
    c.text(960, 760, 'each dot: 500 people (simplified)', 28, DIM, 1 - hl(2), w='Regular')
    m2 = hl(2)
    if m2 > .01:
        c.rr(560, 440, 1360, 820, 30, CARD, m2, outline=CASH, ow=5)
        c.text(960, 520, '250 x $1,000 = $250,000', 54, INK, m2, w='Bold', bg=CARD)
        c.text(960, 620, '$250,000 / 100,000 people', 46, DIM, m2, w='Medium', bg=CARD)
        c.text(960, 730, '= $2.50 each', 76, CASH, m2, w='Bold', bg=CARD)

def bars(c, vals, lo, hi, x0, y0, w, h, a, col, bg=BG, fmt=str):
    """Year-by-year bars between lo and hi."""
    n = len(vals); bw = w / n
    for k, v in enumerate(vals):
        u = fd(t_glob[0], .15 * k, .4)
        hh = h * clamp((v - lo) / (hi - lo)) * u
        c.rr(x0 + k * bw + 8, y0 - hh, x0 + (k + 1) * bw - 8, y0, 8, col, a, bg=bg)
        if u > .5: c.text(x0 + (k + .5) * bw, y0 - hh - 26, fmt(v), 26 if len(fmt(v)) > 3 else 34, INK, a, w='Bold', bg=bg)
t_glob = [0.0]

def s_small(c, T, t):
    """Ten cars, 1 in 10 stolen a year: some years none, some years two or three."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Now insure just ', INK), ('10 cars', POOL)], sw_out(T, 1))
    headline(c, [('Expect ', INK), ('1', OK), (' stolen a year', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Some years: ', INK), ('double', YOU)], sw_in(T, 2))
    for k in range(10):
        x = 330 + k * 140
        stolen = (k == 4) and hl(1) > .5
        car(c, x, 330, .9, 1, col=YOU if stolen else POOL)
    m12 = hl(1)
    if m12 > .01:
        t_glob[0] = max(0, T(1))
        bars(c, SMALL, 0, 4, 300, 800, 1320, 330, m12, OK)
        for k, v in enumerate(SMALL):
            if v >= 2 and hl(2) > .01:
                x = 300 + (k + .5) * 110
                c.circ(x, 800 - 330 * v / 4 - 26, 34, None, hl(2), outline=YOU, ow=5)
        c.text(960, 850, 'cars stolen each year, 12 simulated years (1 in 10 chance each)', 28, DIM, m12, w='Regular')
    c.text(960, 430, 'a 1 in 10 chance each, every year', 34, DIM, 1 - m12, w='Medium')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('100,000 cars', POOL), (': how close to 10,000?', INK)], 1, bg=QUIZ, size=68)
    for k, txt in enumerate(('A  Could be 5,000 or 15,000', 'B  Within a few hundred')):
        u = fd(t, .8 + .3 * k)
        c.rr(260, 360 + k * 200, 1200, 500 + k * 200, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(310, 430 + k * 200, txt, 54, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    for k in range(6):
        car(c, 1380 + (k % 3) * 130, 420 + (k // 3) * 110, .8, fd(t, .5), col=POOL, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - QZ; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), QZ - .3)
        c.circ(1510, 740, 80, CASH, u, bg=QUIZ); c.text(1510, 740, str(k) if k else '?', 76, DARK, u, w='Bold', bg=CASH)

def s_large(c, T, t):
    """The big group's bars all sit at almost the same height; then coin flips."""
    hl = lambda i: hl_(T, i)
    headline(c, [('B: ', INK), ('within a few hundred', OK)], sw_out(T, 1))
    headline(c, [('Big group, ', POOL), ('steady total', OK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('The ', INK), ('law of large numbers', OK)], sw_in(T, 2), size=78)
    m01 = 1 - hl(2)
    if m01 > .01:
        t_glob[0] = max(0, T(0))
        bars(c, BIG, 0, 12000, 300, 780, 1320, 440, m01, OK, fmt=lambda v: f'{v:,}')
        c.line([(300, 780 - 440 * 10000 / 12000), (1620, 780 - 440 * 10000 / 12000)], CASH, 4, m01 * .8)
        c.text(1700, 780 - 440 * 10000 / 12000, '10,000', 32, CASH, m01, w='Bold')
        c.text(960, 840, 'cars stolen each year out of 100,000, 12 simulated years', 28, DIM, m01, w='Regular')
    m2 = hl(2)
    if m2 > .01:
        for k, (n, h) in enumerate(((10, '7 heads'), (10000, '5,023 heads'))):
            x = 560 + k * 800
            c.text(x, 330, f'{n:,} coin flips', 50, INK, m2, w='Bold')
            for j in range(5):
                coin(c, x - 160 + j * 80, 450, 30, m2, lab='H' if (j + k) % 2 == 0 else 'T')
            c.text(x, 570, h, 60, YOU if k == 0 else OK, m2, w='Bold')
            c.text(x, 640, '70%: far from half' if k == 0 else '50.2%: almost exactly half', 38, DIM, m2, w='Medium')
        c.text(960, 760, 'example flips', 28, DIM, m2, w='Regular')

def s_premium(c, T, t):
    """What a premium pays for: a stacked bar that grows piece by piece (shares illustrative)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Your ', INK), ('premium', CASH), (' pays for...', INK)], sw_out(T, 1))
    headline(c, [('...costs, ', INK), ('profit', POOL), (', a cushion', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Aim: take in ', INK), ('more than they pay out', CASH)], sw_in(T, 2), size=74)
    parts = (('expected claims', CASH, 0, 800, 650), ('running costs', DIM, 1, 170, 650), ('profit', POOL, 1, 110, 710), ('cushion for a bad year', YOU, 1, 140, 770))
    x = 260
    for lab, col, line, w, ly in parts:
        u = hl(line) if line else fd(T(0), .5)
        if u > .01:
            c.rr(x, 430, x + w * u, 600, 14, col, 1)
            c.text(x + w / 2, ly, lab, 34, col, u, w='Bold')
        x += w + 6
    c.text(960, 375, 'one premium (sizes illustrative)', 38, INK, 1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        c.rr(360, 810, 1160, 875, 30, CARD, m2, outline=CASH, ow=4)
        c.text(760, 842, 'the extra buys you certainty', 34, INK, m2, w='Bold', bg=CARD)

def s_break(c, T, t):
    """A row of houses on one coast; a storm hits them all at once and the jar drains."""
    hl = lambda i: hl_(T, i)
    headline(c, [('It breaks when ', INK), ('everyone', RISK), (' claims', INK)], sw_out(T, 1))
    headline(c, [('One coast, ', INK), ('one storm', RISK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('So insurers ', INK), ('spread out', OK)], sw_in(T, 2))
    c.rr(0, 700, 1920, 880, 0, SEA, 1)
    m1 = hl(1) * (1 - hl(2))
    for k in range(7):
        x = 220 + k * 200
        hit = m1 > .5 and k < 7
        house(c, x, 600, .7, 1 - hl(2), col=(80, 70, 90) if hit else WALL)
    if m1 > .01:
        swirl(c, 900, 380, 220, m1, t)
    pot(c, 1720, 520, .55, 1, .7 * (1 - fd(T(1), .8, 1.5)) if T(1) > -.1 and hl(2) < .5 else .7)
    m2 = hl(2)
    if m2 > .01:
        c.rr(300, 380, 1620, 660, 30, CARD, m2, outline=OK, ow=4)
        for k, (lab, xx) in enumerate((('coast', 520), ('city', 800), ('hills', 1080), ('inland', 1360))):
            house(c, xx, 520, .5, m2, bg=CARD); c.text(xx, 600, lab, 30, OK, m2, w='Bold', bg=CARD)
    c.text(960, 820, 'a risk that hits everyone at once can empty the pool', 34, INK, 1 - m2, w='Bold', bg=SEA)

def s_answer(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Your ', INK), ('$1,000', YOU), (" didn't rebuild it", INK)], sw_out(T, 1))
    headline(c, [('Thousands of ', INK), ('quiet years', POOL), (' did', INK)], sw_in(T, 1))
    house(c, 960, 560, 1.4, 1, lit=True)
    for k in range(12):
        ang = k * 6.283 / 12 + t * .2; r = 380
        x = 960 + r * math.cos(ang); y = 540 + r * .7 * math.sin(ang)
        person(c, x, y, .9, hl(1) + .25 * (1 - hl(1)))
        u = ((t * .4) + k / 12) % 1.0
        coin(c, x + (960 - x) * u, y + (540 - y) * u, 14, hl(1) * (1 - u))

def s_recap(c, T, t):
    """Recap as three coins stacking, one per point."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', CASH)], 1)
    items = ((1, 'many pay a little', 'the few with losses get paid', POOL), (2, 'big groups are predictable', 'the law of large numbers', OK), (3, 'it breaks if all claim at once', 'so risk is spread out', RISK))
    for ln, l1, l2, col in items:
        m = hl(ln); y = 330 + (ln - 1) * 170; dx = 60 * (1 - m)
        coin(c, 400 + dx, y + 20, 44, .3 + .7 * m)
        c.text(490 + dx, y, str(ln) + '.  ' + l1, 54, col, .25 + .75 * m, 'lm', 'Bold')
        c.text(570 + dx, y + 58, l2, 36, DIM, m, 'lm', 'Medium')
    c.text(960, 860, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """One burning house in front of a crowd of small houses dropping coins."""
    for k in range(6):
        house(c, 1250 + (k % 3) * 220, 300 + (k // 3) * 170, .45, 1)
    house(c, 1500, 640, 1.2, 1, col=(80, 70, 90))
    flames(c, 1500, 540, 1.2, 1, 0.7)
    for k in range(3):
        coin(c, 1280 + k * 190, 470, 20, 1)

SCENES = [
 ('THE FIRE', ["Your house burns down.",
               "Rebuilding costs three hundred thousand dollars. You paid the insurer about a thousand dollars a year.",
               "So where does the rest come from?"], s_hook),
 ('THE POOL', ["From everyone else.",
               "An insurer collects premiums from a huge group of people, and in any one year, most of them never claim.",
               "Their money pays for the few who do. Like friends chipping in so whoever gets the unlucky bill isn't stuck with it."], s_pool),
 ('THE SPLIT', ["Here's a textbook example. An insurer covers a hundred thousand forty-year-olds.",
                "It expects about two hundred and fifty of them to die this year, each with a thousand-dollar policy.",
                "That's two hundred and fifty thousand dollars in claims. Split a hundred thousand ways, it's two dollars fifty each."], s_split),
 ('TEN CARS', ["But this only works with a big group. Say you insure just ten cars.",
               "Each has a one in ten chance of being stolen this year, so you expect one.",
               "Yet about one year in four, two or more go, and your bill doubles."], s_small),
 ('QUICK QUESTION', ["Quick question. Insure a hundred thousand cars instead. Will thefts land anywhere from five to fifteen thousand, or within a few hundred of ten thousand?"], s_quiz),
 ('LARGE NUMBERS', ["It's B. Within a few hundred.",
                    "One car is a gamble. A hundred thousand cars behave almost like clockwork.",
                    "That's the law of large numbers. Flip a coin ten times and you might get seven heads. Flip it ten thousand times, and you land very close to half."], s_large),
 ('THE PREMIUM', ["So your premium covers your share of the expected claims.",
                  "Plus running costs, profit, and a cushion in case it's a bad year.",
                  "Insurers aim to take in more than they pay out. What you buy is certainty."], s_premium),
 ('WHAT BREAKS IT', ["The pool breaks when everyone claims at once.",
                     "If one insurer covered every home along one stretch of coast, a single hurricane could empty it.",
                     "So insurers spread their risk across many places."], s_break),
 ('THE ANSWER', ["So your thousand dollars didn't rebuild your house.",
                 "Thousands of other people did, in a year when nothing happened to them."], s_answer),
 ('RECAP', ["Three things to keep.",
            "One: insurance pools money, so many people pay a little and the few with losses get paid.",
            "Two: big groups make losses predictable. That's the law of large numbers.",
            "Three: it breaks when everyone claims at once, so insurers spread their risk.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story (obstacle, then the answer) ----------
def short_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Your ', INK), ('house', YOU), (' burns down', INK)], sw_out(T, 1), size=84)
    headline(c, [('$300,000', YOU), (' vs ', INK), ('$1,000', CASH)], sw_in(T, 1), size=88)
    house(c, 560, 560, 1.6, 1, col=(80, 70, 90))
    flames(c, 560, 440, 1.6, 1, t)
    m1 = hl(1)
    c.rr(1060, 330, 1700, 470, 26, CARD, m1, outline=YOU, ow=4)
    c.text(1380, 400, 'rebuild: $300,000', 54, YOU, m1, w='Bold', bg=CARD)
    c.rr(1060, 520, 1700, 660, 26, CARD, m1, outline=CASH, ow=4)
    c.text(1380, 590, 'you paid: $1,000 a year', 50, CASH, m1, w='Bold', bg=CARD)
    c.text(960, 860, 'illustrative numbers', 28, DIM, 1, w='Regular')

def short_pool(c, T, t):
    s_pool(c, lambda i: T(0) + 3.0 if i <= 1 else (T(1) if i == 2 else -99), t)

def short_split(c, T, t):
    s_split(c, lambda i: (T(0) + 3.0 if i <= 1 else T(1)) if i <= 2 else -99, t)

def short_large(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('10 cars: ', INK), ('a gamble', YOU)], sw_out(T, 1), size=88)
    headline(c, [('100,000: ', POOL), ('clockwork', OK)], sw_in(T, 1), size=88)
    m0 = 1 - hl(1)
    if m0 > .01:
        t_glob[0] = max(0, T(0))
        bars(c, SMALL, 0, 4, 300, 800, 1320, 420, m0, YOU)
        c.text(960, 850, 'cars stolen out of 10, 12 simulated years', 28, DIM, m0, w='Regular')
    m1 = hl(1)
    if m1 > .01:
        t_glob[0] = max(0, T(1))
        bars(c, BIG, 0, 12000, 300, 800, 1320, 420, m1, OK, fmt=lambda v: f'{v:,}')
        c.text(960, 850, 'cars stolen out of 100,000, 12 simulated years', 28, DIM, m1, w='Regular')

SHORT_SCENES = [
 ('THE FIRE', ["Your house burns down.",
               "Rebuilding costs three hundred thousand dollars, but you only paid about a thousand a year. So who pays the rest?"], short_hook),
 ('THE POOL', ["Everyone else in the pool.",
               "Most customers never claim in a given year, and their premiums cover the few who do."], short_pool),
 ('THE SPLIT', ["In one textbook example, an insurer expects two hundred and fifty claims of a thousand dollars among a hundred thousand people.",
                "That's just two dollars fifty each."], short_split),
 ('LARGE NUMBERS', ["It only works with huge groups. Insure ten cars, and some years you lose none, some years three.",
                    "Insure a hundred thousand, and the total is almost perfectly predictable."], short_large),
 ('SO', ["So your premium doesn't pay for your house.",
         "It buys a tiny share of everyone's bad luck."], card('Many pay a little.', 'The few who need it get paid.')),
]
SHORT_HITS = [(4, 1, 0.0)]
