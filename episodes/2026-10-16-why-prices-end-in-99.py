"""Episode: Why Prices End in .99 (The Left-Digit Effect)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Prices End in .99'            # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
SHORT_HOOK = 'Why do prices end in 99?'          # headline on the vertical Short
HITS = [(0, 2, 0.0), (3, 2, 0.0), (4, 2, 0.0)]   # title card, the car-price jump, quiz answer
THUMB = ['$2.99', 'FEELS', 'LIKE $2']
MUSIC_LEVEL = 0.006                              # keeps the music about 20 dB under the voice (lesson of 2026-10-14)
# Narration spells prices in words so the voice reads them naturally; captions show them as numbers.
CAPTION_FIXES = {
    'Two dollars ninety-nine, and three dollars': '$2.99, and $3.00',
    'two ninety-nine': '$2.99', 'Three dollars to': '$3.00 to', 'three dollars': '$3', 'Three sixty to three fifty-nine': '$3.60 to $3.59',
    'thirty-four, thirty-nine, or forty-four dollars': '$34, $39, or $44', 'Thirty-nine.': '$39.',
    'one hundred dollars': '$100', 'ninety-eight seventy-six': '$98.76', 'nineteen ninety-nine': '$19.99',
    'seventy-nine thousand nine hundred': '79,900', 'seventy-nine thousand eight hundred': '79,800',
    'about 200 dollars': 'about $200', 'about ten dollars': 'about $10', 'end in 99': 'end in .99',
}
# Applied lesson (learnings.md, 2026-10-16): open on a bold, true claim and prove it at once with one
# simple visual (two price tags one cent apart, moving from the first frame), instead of a question alone.

TAG = (250, 236, 200); TAGINK = (40, 34, 60); GOLD = (235, 190, 90)

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def digits(c, x, y, s, size, a=1.0, cols=None, bg=BG, w='Bold'):
    """Draw string s centred at (x, y), one colour per character (cols: list or None)."""
    if a <= 0.01: return
    ws = [c.tw(ch, size, w) for ch in s]; x0 = x - sum(ws) / 2
    for i, ch in enumerate(s):
        col = cols[i] if cols else INK
        c.text(x0, y, ch, size, col, a, 'lm', w, bg=bg); x0 += ws[i]

def tag(c, x, y, wd, ht, price, a=1.0, cols=None, size=None, fill=TAG, edge=None, string=True):
    """Paper price tag centred at (x, y) with a pointed left end, a hole and a string."""
    if a <= 0.01: return
    k = c.k; p = ht * .38
    pts = [(x - wd / 2 + p, y - ht / 2), (x + wd / 2, y - ht / 2), (x + wd / 2, y + ht / 2), (x - wd / 2 + p, y + ht / 2), (x - wd / 2, y)]
    if string:
        c.line([(x - wd / 2 + p * .8, y), (x - wd / 2 - p * .2, y - ht * .9)], DIM, 3, a)
    c.d.polygon([(px * k, py * k) for px, py in pts], fill=mix(fill, a), outline=mix(edge, a) if edge else None, width=int(4 * k) if edge else 0)
    c.circ(x - wd / 2 + p * .8, y, ht * .07, BG, a, bg=fill)
    digits(c, x + p * .35, y + ht * .04, price, size or ht * .5, a, cols or [TAGINK] * len(price), fill)

def snack(c, x, y, s, col, a=1.0):
    """Crisp packet: crimped top and bottom, round label."""
    if a <= 0.01: return
    c.rr(x - s * .55, y - s * .8, x + s * .55, y + s * .8, s * .12, col, a)
    for yy in (y - s * .8, y + s * .8):
        for j in range(7):
            xx = x - s * .5 + j * s * .166
            c.line([(xx, yy - s * .05), (xx + s * .08, yy + s * .05)], mix(col, .5), max(2, s * .03), a, col)
    c.circ(x, y, s * .32, INK, a, bg=col)
    c.circ(x, y, s * .2, YE, a, bg=INK)

def car(c, x, y, s, col, a=1.0, bg=BG):
    """Side view of a car, centred at (x, y), length 2s."""
    if a <= 0.01: return
    c.rr(x - s, y - s * .22, x + s, y + s * .22, s * .14, col, a, bg=bg)
    c.d.polygon([((x - s * .55) * c.k, (y - s * .2) * c.k), ((x - s * .3) * c.k, (y - s * .55) * c.k),
                 ((x + s * .35) * c.k, (y - s * .55) * c.k), ((x + s * .62) * c.k, (y - s * .2) * c.k)], fill=mix(col, a, bg))
    for sg in (-1, 1):
        c.rr(x + sg * s * .03 - (s * .26 if sg < 0 else 0) + (s * .02 if sg > 0 else -s * .02), y - s * .48,
             x + sg * s * .03 + (s * .26 if sg > 0 else 0), y - s * .24, 6, (150, 200, 240), a, bg=col)
    for dx in (-.58, .58):
        c.circ(x + dx * s, y + s * .22, s * .18, (30, 30, 46), a, bg=bg)
        c.circ(x + dx * s, y + s * .22, s * .08, DIM, a, bg=(30, 30, 46))

def odo(c, x, y, s, a=1.0, hi=0.0, w=300):
    """Odometer box showing s (digits); hi fades the first digit to yellow."""
    if a <= 0.01: return
    c.rr(x - w / 2, y - 42, x + w / 2, y + 42, 12, (8, 10, 24), a, outline=(80, 90, 140), ow=3)
    cols = [mix(YE, hi, INK) if i == 0 else INK for i in range(len(s))]
    digits(c, x, y + 2, s, 54, a, cols, (8, 10, 24), 'Mono')

def dress(c, x, y, s, col, a=1.0):
    if a <= 0.01: return
    c.d.polygon([((x - s * .28) * c.k, (y - s * .5) * c.k), ((x + s * .28) * c.k, (y - s * .5) * c.k),
                 ((x + s * .6) * c.k, (y + s * .6) * c.k), ((x - s * .6) * c.k, (y + s * .6) * c.k)], fill=mix(col, a))
    c.rr(x - s * .28, y - s * .72, x + s * .28, y - s * .38, 8, col, a)
    for sg in (-1, 1):
        c.line([(x + sg * s * .18, y - s * .72), (x + sg * s * .14, y - s * .9)], col, max(3, s * .05), a)

def register(c, x, y, s, a=1.0, open_=0.0):
    """Old cash register; open_ slides the cash drawer out."""
    if a <= 0.01: return
    dy = s * .28 * open_
    c.rr(x - s * .9, y + s * .3, x + s * .9, y + s * .6 + dy, 10, (70, 60, 50), a)        # drawer
    if open_ > .05:
        for j in range(4):
            c.circ(x - s * .5 + j * s * .33, y + s * .48 + dy, s * .1, GOLD, a * open_, bg=(70, 60, 50))
    c.rr(x - s, y - s * .5, x + s, y + s * .35, 18, (120, 90, 70), a)                       # body
    c.rr(x - s * .55, y - s * .95, x + s * .55, y - s * .5, 12, (100, 76, 60), a)             # display
    c.rr(x - s * .45, y - s * .88, x + s * .45, y - s * .58, 8, (20, 30, 24), a, bg=(100, 76, 60))
    c.text(x, y - s * .73, '0.99', s * .2, GR, a, w='Mono', bg=(20, 30, 24))
    for i in range(3):
        for j in range(5):
            c.rr(x - s * .78 + j * s * .32, y - s * .35 + i * s * .2, x - s * .58 + j * s * .32, y - s * .22 + i * s * .2, 4, (230, 220, 200), a, bg=(120, 90, 70))

def camera(c, x, y, s, col, a=1.0):
    if a <= 0.01: return
    c.rr(x - s * .32, y - s * .62, x + s * .05, y - s * .42, 6, col, a)
    c.rr(x - s * .7, y - s * .45, x + s * .7, y + s * .45, s * .12, col, a)
    c.circ(x, y, s * .32, (30, 34, 60), a, bg=col)
    c.circ(x, y, s * .2, (70, 110, 180), a, bg=(30, 34, 60))
    c.circ(x + s * .5, y - s * .3, s * .07, YE, a, bg=col)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    tag(c, 1500, 380, 560, 240, '$3.00', 1, size=130)
    tag(c, 1500, 720, 560, 240, '$2.99', 1, [TAGINK, (215, 60, 90), TAGINK, TAGINK, TAGINK], size=130, edge=YE)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(2), 0, .5)
    if a > 0:
        # moving from the very first frame: both tags swing gently on their strings
        b1, b2 = 14 * math.sin(t * 2.2), 14 * math.sin(t * 2.2 + 1.3)
        brain = fd(T(1)) if T(1) > -.1 else 0.0
        tag(c, 600, 400 + b1, 520, 220, '$3.00', a, size=118)
        red = mix((215, 60, 90), brain, TAGINK)
        tag(c, 1320, 400 + b2, 520, 220, '$2.99', a, [TAGINK, red, TAGINK, TAGINK, TAGINK], size=118, edge=mix(YE, brain, TAG))
        c.text(960, 170, 'Just 1 cent apart', 76, INK, a, w='Bold')
        c.text(960, 405, '−1¢', 52, YE, a * (1 - brain), w='Bold')
        if brain > 0:
            k = a * brain
            c.text(960, 620, 'Your brain:', 44, DIM, k, w='Medium')
            c.text(600, 720, '"three dollars"', 50, INK, k, w='Bold')
            c.text(1320, 720, '"two-something"', 50, YE, k, w='Bold')
            c.text(960, 820, 'not one cent apart', 54, PK, a * fd(T(1), .8), w='Bold')
    if T(2) > 0:
        m = fd(T(2), .2, .7)
        c.text(960, 330 + 30 * (1 - m), 'Why Prices', 150, INK, m, w='Bold')
        c.text(960, 500 + 30 * (1 - m), 'End in .99', 150, YE, m, w='Bold')
        c.line([(960 - 320 * m, 610), (960 + 320 * m, 610)], CY, 8, m)
        k = fd(T(2), 1.0)
        tag(c, 960, 730 + 8 * math.sin(t * 2), 300, 120, '$2.99', k, [TAGINK, (215, 60, 90), TAGINK, TAGINK, TAGINK], size=64)

def s_cent(c, T, t):
    m0 = fd(T(0))
    c.text(960, 170, 'Same snack, two tags', 62, INK, m0, w='Bold')
    for i, (x, col) in enumerate(((600, (220, 80, 80)), (1320, (220, 80, 80)))):
        snack(c, x, 380 + 6 * math.sin(t * 1.5 + i), 150, col, m0 * fd(T(0), .2 + i * .2))
    if T(1) > -.1:
        tag(c, 600, 620, 360, 130, '$3.00', fd(T(1)), size=72, string=False)
        tag(c, 1320, 620, 360, 130, '$2.99', fd(T(1), .8), size=72, string=False)
    if T(2) > -.1:
        k = fd(T(2)) * (1 - fd(T(3), -.3, .4))
        c.circ(960, 470, 70, GOLD, k, outline=(180, 140, 60), ow=6)
        c.text(960, 472, '1¢', 56, TAGINK, k, w='Bold', bg=GOLD)
        c.text(960, 580, 'the whole difference', 34, DIM, k, w='Medium')
    if T(3) > -.1:
        k = fd(T(3))
        for x, txt, col in ((600, '"About 3 dollars"', INK), (1320, '"2 dollars and something"', YE)):
            c.rr(x - 300, 740, x + 300, 830, 45, CARD, k, outline=col, ow=4)
            c.text(x, 785, txt, 40, col, k, w='Bold', bg=CARD)

def s_left(c, T, t):
    a0 = 1 - fd(T(3), -.4, .4)
    if a0 > 0:
        pill(c, 960, 180, 'The left-digit effect', YE, a0 * fd(T(0)), 56, h=96)
        if T(1) > -.1:
            k = a0 * fd(T(1))
            p = clamp(T(1, .3) / 2.4)                         # reading progress, left to right
            s = '$2.99'; n = len(s)
            cols = []
            for i in range(n):
                seen = p * n > i
                cols.append(YE if (i == 1 and seen) else (INK if seen else (70, 78, 120)))
            digits(c, 960, 470, s, 230, k, cols)
            x = 600 + 720 * p
            c.arrow(600, 640, x, 640, CY, 7, k, 22)
            c.text(960, 330, 'We read left to right', 44, CY, k, w='Bold')
        if T(2) > -.1:
            k = a0 * fd(T(2))
            c.rr(1360, 700, 1840, 830, 26, CARD, k, outline=YE, ow=5)
            c.text(1600, 742, 'Brain\'s first guess', 32, DIM, k, w='Medium', bg=CARD)
            c.text(1600, 795, '"about 2"', 48, YE, k, w='Bold', bg=CARD)
            c.text(380, 765, 'judged before the end', 36, INK, k, w='Bold')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 170, 'It works when the first digit changes', 56, INK, m, w='Bold')
    c.text(960, 235, 'New York University study, 2005', 30, DIM, m, w='Medium')
    rows = [(360, '$3.00', '$2.99', 'feels cheaper', GR, True), (620, '$3.60', '$3.59', 'much less pull', DIM, False)]
    for j, (y, p0, p1, lab, col, big) in enumerate(rows):
        k = m * (fd(T(3), .6) if j == 0 else (fd(T(4), .3) if T(4) > -.1 else 0))
        if k <= 0.01: continue
        tag(c, 470, y, 330, 130, p0, k, size=70, string=False)
        c.arrow(680, y, 820, y, DIM, 6, k, 20)
        hc = [TAGINK, (215, 60, 90) if big else TAGINK, TAGINK, TAGINK, TAGINK]
        tag(c, 1040, y, 330, 130, p1, k, hc, size=70, string=False, edge=YE if big else None)
        c.text(1290, y - 4, lab, 46, col, k, 'lm', 'Bold')
        if big: c.check(1290 + c.tw(lab, 46, 'Bold') + 50, y, 34, GR, k, fd(T(3), 1.2))
    if T(4) > -.1:
        c.text(960, 800, 'Same 1-cent cut. Only one changes the first digit.', 38, YE, fd(T(4), 1.2), w='Bold')

def s_cars(c, T, t):
    a0 = 1 - fd(T(2), -.4, .4)
    if a0 > 0:
        m = fd(T(0)) * a0
        snack(c, 760 - 300 * fd(T(0), .8), 450, 110, (220, 80, 80), m * (1 - fd(T(0), .8)))
        car(c, 1900 - 940 * ease(clamp(T(0) / 1.4)), 470, 230, CY, m)
        c.text(960, 170, 'Not just snacks', 62, INK, m, w='Bold')
        if T(1) > -.1:
            k = fd(T(1)) * a0
            c.text(960, 170, 'Not just snacks', 62, INK, 0, w='Bold')
            c.text(500, 720, '22 million+', 92, YE, k, w='Bold')
            c.text(500, 800, 'used car auction sales', 38, INK, k, w='Bold')
            c.text(1420, 760, 'Lacetera, Pope & Sydnor (NBER)', 30, DIM, k, w='Medium')
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 160, 'Same kind of car, different mileage', 54, INK, m, w='Bold')
    cars = [(400, '79,850', 0.0), (960, '79,950', 0.0), (1520, '80,050', 0.0)]
    hi = fd(T(4)) if T(4) > -.1 else 0.0
    base, top = 820, 520
    vis = [fd(T(3)) if T(3) > -.1 else 0.0, fd(T(2), .2), fd(T(2), .6)]
    heights = [270, 262, 150]                      # 79,850 ≈ 79,950 (about $10 apart); 80,050 about $200 lower
    for i, (x, s, _) in enumerate(cars):
        k = m * vis[i]
        if k <= 0.01: continue
        car(c, x, 290, 120, (90, 160, 230) if i < 2 else PK, k)
        odo(c, x, 420, s, k, hi)
        col = GR if i < 2 else PK
        c.rr(x - 90, base - heights[i] * ease(clamp((T(2) if i else T(3)) / 1.0)), x + 90, base, 10, col, k)
    k = m * fd(T(2), 1.2)
    c.arrow(1150, 600, 1330, 690, PK, 6, k, 20)
    c.text(1240, 560, 'about $200 less', 40, PK, k, w='Bold')
    if T(3) > -.1:
        kk = m * fd(T(3), .8)
        c.text(680, 520, 'only about $10', 36, GR, kk, w='Bold')
    c.text(960, 860, 'Example readings. Bars not to scale.', 26, DIM, m, w='Regular')

PRICES = [(560, '$34'), (960, '$39'), (1360, '$44')]
def s_quiz(c, T, t):
    m = fd(T(0))
    ans = fd(T(2)) if T(2) > -.1 else 0.0
    c.text(960, 160, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 245, 'Which price sold the most dresses?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 190, 'The $39 dress sold the most', 64, INK, ans, w='Bold')
    c.text(960, 255, 'It even beat the cheaper $34', 44, GR, fd(T(2), .6) if T(2) > -.1 else 0, w='Bold')
    for i, (x, p) in enumerate(PRICES):
        k = m * fd(T(0), 1.0 + i * .3)
        win = i == 1
        dim = (1 - ans * .6) if not win else 1
        dress(c, x, 470 + 6 * math.sin(t * 2 + i), 150, mix(PU if not win else PK, dim), k)
        tag(c, x + 20, 690, 230, 100, p, k, [mix(TAGINK, dim, TAG)] * 3, size=60, string=False, edge=YE if (win and ans > .5) else None)
        if win and ans > 0:
            c.check(x, 810, 36, GR, ans, fd(T(2), .3))
    if T(1) > 0 and ans < 1:
        p = clamp(T(1) / 2.2)
        ring(c, 1700, 560, 70, 1 - p, CY, fd(T(1)) * (1 - ans))
    c.text(960, 860, 'Anderson & Simester (MIT), clothing catalog test', 26, DIM, m, w='Regular')

GRID = ['$9.99', '$4.99', '$19', '$2.49', '$99', '$1.99', '$29.99', '$5.99']
def s_every(c, T, t):
    a0 = 1 - fd(T(2), -.4, .4)
    if a0 > 0:
        c.text(960, 160, 'Nines are everywhere', 62, INK, a0 * fd(T(0)), w='Bold')
        for i, p in enumerate(GRID):
            x = 330 + (i % 4) * 420; y = 340 + (i // 4) * 170
            tag(c, x, y + 5 * math.sin(t * 2 + i), 300, 110, p, a0 * fd(T(0), .2 + i * .12), size=58, string=False)
        if T(1) > -.1:
            k = a0 * fd(T(1))
            for j in range(10):
                x = 560 + j * 90
                c.rr(x - 32, 640, x + 32, 720, 10, YE if j < 6 else (60, 68, 110), k * fd(T(1), .3 + j * .08))
            c.text(960, 790, 'About 6 in 10 advertised prices ended in 9', 46, YE, k * fd(T(1), 1.0), w='Bold')
            c.text(960, 850, '1997 survey (Marketing Bulletin)', 26, DIM, k, w='Regular')
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 160, 'A popular story', 62, INK, m, w='Bold')
    op = fd(T(3), .4, .8) if T(3) > -.1 else 0.0
    register(c, 620, 520, 260, m, op)
    if T(3) > -.1:
        k = fd(T(3))
        steps = ['Odd price', 'Cashier gives change', 'Till must open', 'Sale is recorded']
        for j, s in enumerate(steps):
            kk = k * fd(T(3), .4 + j * .5)
            c.rr(1080, 300 + j * 120, 1700, 380 + j * 120, 20, CARD, kk, outline=CY, ow=3)
            c.text(1390, 340 + j * 120, s, 40, INK, kk, w='Bold', bg=CARD)
    if T(4) > -.1:
        k = fd(T(4))
        pill(c, 1390, 820, 'Only a theory', PK, k, 48, h=86)

def s_round(c, T, t):
    m = fd(T(0))
    c.text(960, 160, 'When shops skip the nines', 62, INK, m * (1 - fd(T(1), -.3, .4)), w='Bold')
    a0 = 1 - fd(T(1), -.3, .4)
    if a0 > 0:
        tag(c, 960, 470, 560, 230, '$100', m * a0, [TAGINK] * 4, size=140, fill=GOLD, string=True)
        for j in range(5):
            q = t * 1.3 + j * 1.25
            c.circ(960 + 360 * math.cos(q), 470 + 170 * math.sin(q), 8 + 4 * math.sin(t * 4 + j), YE, m * a0)
        c.text(960, 740, 'Fancy shops often use round prices', 46, YE, m * a0 * fd(T(0), .8), w='Bold')
    if T(1) < -.1: return
    k1 = fd(T(1))
    c.text(960, 160, 'Round or exact? It depends', 62, INK, k1, w='Bold')
    c.text(960, 225, 'Wadhwa & Zhang, Journal of Consumer Research, 2015', 28, DIM, k1, w='Medium')
    c.rr(180, 290, 900, 850, 30, CARD, k1, outline=YE, ow=5)
    camera(c, 420, 450, 150, (230, 120, 90), k1)
    c.circ(780, 380, 40, YE, k1, bg=CARD)
    c.text(540, 600, 'Holiday camera', 44, INK, k1, w='Bold', bg=CARD)
    tag(c, 560, 700, 280, 100, '$100', k1 * fd(T(1), .6), size=60, string=False, fill=GOLD)
    c.text(540, 800, 'feels right', 40, YE, k1 * fd(T(1), 1.0), w='Bold', bg=CARD)
    if T(2) > -.1:
        k2 = fd(T(2))
        c.rr(1020, 290, 1740, 850, 30, CARD, k2, outline=CY, ow=5)
        camera(c, 1260, 450, 150, (120, 140, 180), k2)
        for j in range(3):
            c.check(1560, 380 + j * 60, 20, GR, k2, 1); c.line([(1590, 380 + j * 60), (1680, 380 + j * 60)], DIM, 5, k2, CARD)
        c.text(1380, 600, 'Class project camera', 44, INK, k2, w='Bold', bg=CARD)
        tag(c, 1400, 700, 300, 100, '$98.76', k2 * fd(T(2), .6), size=56, string=False)
        c.text(1380, 800, 'think it through', 40, CY, k2 * fd(T(2), 1.0), w='Bold', bg=CARD)

def s_beat(c, T, t):
    m = fd(T(0))
    c.text(960, 160, 'Beat the trick: round up', 62, INK, m, w='Bold')
    rows = [(1, 360, '$2.99', '$3'), (2, 560, '$19.99', '$20')]
    for li, y, p0, p1 in rows:
        if T(li) < -.1: continue
        k = fd(T(li))
        tag(c, 560, y, 380, 140, p0, k, size=76, string=False)
        p = ease(clamp(T(li, .4) / .8))
        c.arrow(800, y, 800 + 260 * p, y, YE, 8, k, 24)
        c.text(1330, y, '≈ ' + p1, 100, YE, k * fd(T(li), .9), w='Bold')
    if T(3) > -.1:
        k = fd(T(3))
        c.rr(360, 680, 1560, 830, 30, CARD, k, outline=GR, ow=5)
        c.text(960, 735, 'Compare the full prices,', 46, INK, k, w='Bold', bg=CARD)
        c.text(960, 790, 'not the first digits', 46, GR, k, w='Bold', bg=CARD)

REC = [('1', 'Left digit counts most', YE), ('2', 'Real money moves', PK), ('3', 'Round up in your head', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 255, 290 + up, x + 255, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 190, 355 + up, 40, col, m, bg=CARD); c.text(x - 190, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 520 + up
        if i == 0:
            digits(c, x, y - 20, '$2.99', 110, m, [INK, YE, INK, INK, INK], CARD)
            c.arrow(x - 150, y + 70, x + 150, y + 70, CY, 6, m, 18)
            c.text(x, y + 130, 'read left to right', 30, DIM, m, w='Medium', bg=CARD)
        elif i == 1:
            car(c, x, y - 30, 120, (90, 160, 230), m, CARD)
            c.text(x, y + 70, '79,9xx vs 80,0xx', 36, INK, m, w='Bold', bg=CARD)
            c.text(x, y + 130, 'about $200 apart', 34, PK, m, w='Bold', bg=CARD)
        else:
            c.text(x, y - 40, '$19.99', 60, INK, m, w='Bold', bg=CARD)
            c.text(x, y + 50, '≈ $20', 72, GR, m, w='Bold', bg=CARD)
        c.text(x, 740 + up, lab, 34, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Two dollars ninety-nine, and three dollars. Just one cent apart.",
            "But your brain does not treat them as one cent apart.",
            "So why do so many prices end in 99? Here is the answer."], s_hook),
 ('1  ·  ONE CENT', ["Picture the same snack with two price tags.",
            "One says three dollars. The other says two ninety-nine.",
            "The difference is one cent. Less than most people would bend down to pick up.",
            "Yet the first feels like about three dollars, and the second like two dollars and something."], s_cent),
 ('2  ·  LEFT TO RIGHT', ["Researchers call this the left-digit effect.",
            "We read numbers from left to right, so the first digit lands first.",
            "Our brain starts judging the price before it has finished reading it.",
            "A 2005 study from New York University found the one-cent cut matters most when it changes that first digit.",
            "Three dollars to two ninety-nine feels cheaper. Three sixty to three fifty-nine changes no first digit, so it has much less pull."], s_left),
 ('3  ·  THE CAR TEST', ["And it is not just snacks.",
            "Economists looked at more than 22 million used car sales at auctions.",
            "Cars with just under 80,000 miles sold for about 200 dollars more than cars just over it.",
            "Yet going from seventy-nine thousand nine hundred down to seventy-nine thousand eight hundred changed the price by only about ten dollars.",
            "The first digit on the odometer did most of the work."], s_cars),
 ('4  ·  QUICK QUESTION', ["Quick question. A clothing catalog tested a dress at thirty-four, thirty-nine, or forty-four dollars. Which price sold the most?",
            "Three, two, one.",
            "Thirty-nine. It even beat the cheaper price."], s_quiz),
 ('5  ·  EVERYWHERE', ["That is why nines are everywhere.",
            "One study of advertised prices found that about six in ten ended in nine.",
            "There is also a popular story about how it started.",
            "An odd price meant the cashier had to open the till to give change, so the sale was recorded.",
            "It is a nice story. But it is only a theory."], s_every),
 ('6  ·  ROUND NUMBERS', ["So why do fancy shops often use round prices?",
            "A 2015 study found that round prices, like one hundred dollars, feel right when we buy with our feelings, like a camera for a holiday.",
            "Exact prices, like ninety-eight seventy-six, nudge us to think it through, like a camera for a class project."], s_round),
 ('7  ·  BEAT THE TRICK', ["So how do you beat the trick? Round up in your head.",
            "Read two ninety-nine as three dollars.",
            "Read nineteen ninety-nine as twenty.",
            "Then compare the full prices, not the first digits."], s_beat),
 ('RECAP', ["So remember three things.",
            "One. We read prices from the left, and the first digit counts most.",
            "Two. It moves real money. Even used car prices jump at the first digit of the mileage.",
            "Three. Round up in your head, and compare the full price.",
            "If this helped, subscribe for more."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('.99', ["Two dollars ninety-nine, and three dollars. Just one cent apart.",
          "But your brain does not treat them as one cent apart.",
          "So why do so many prices end in 99?"], s_hook),
 ('LEFT TO RIGHT', ["It is called the left-digit effect.",
                    "We read numbers from left to right, so the first digit lands first.",
                    "Our brain judges the price before it has finished reading it.",
                    "So a one-cent cut that changes the first digit feels much bigger.",
                    "Three dollars to two ninety-nine feels cheaper. Three sixty to three fifty-nine, much less."], s_left),
 ('THE ANSWER', ["That is the answer. Shops end prices in 99 because your brain reads the first digit first.",
                 "So two ninety-nine feels like two. Beat it by rounding up in your head. Follow for more."],
                card('Your brain reads the first digit', 'So $2.99 feels like $2')),
]
SHORT_HITS = [(2, 0, 0.0)]
