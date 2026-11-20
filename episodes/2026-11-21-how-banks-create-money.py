"""Episode: Banks Don't Lend Out Your Savings (lending creates deposits; repaying destroys them; what limits it)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Where Money Comes From'                       # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Where does loan money come from?'              # headline on the vertical Short
HITS = [(0, 1, 0.0), (2, 2, 0.6), (5, 0, 0.0)]               # lending creates money, the new dollars appear, "It disappears"
THUMB = ['NOT YOUR', 'SAVINGS.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.3, (0, 1): 0.3, (1, 2): 0.3, (2, 2): 0.4, (4, 0): 3.4, (5, 0): 0.5, (6, 0): 0.3}
SHORT_PAUSES = {(0, 0): 0.2, (2, 0): 0.3}
CAPTION_FIXES = {'twenty thousand dollars': '$20,000', 'twenty thousand new dollars': '$20,000 of new money',
                 'twenty thousand': '$20,000', 'seventy-five billion dollars': '$75 billion', 'two trillion': '$2 trillion',
                 'twenty eighteen': '2018', 'twenty fourteen': '2014', 'a hundred dollars': '$100', 'four cents': '4 cents'}
CAPTION_FIXES['twenty thousand new dollars'] = '$20,000 new dollars'
CAPTION_FIXES = dict(sorted(CAPTION_FIXES.items(), key=lambda kv: -len(kv[0])))   # longest phrase first

# Colour code kept in every scene:
# money in your account is green, debt (what you owe) is pink, notes and coins are yellow,
# your bank is cyan, the other bank and the central bank are purple.
MONEY = GR; DEBT = PK; CASH = YE; BANK = CY; OTHER = PU
DARK = (20, 22, 38); QUIZ = (16, 58, 62); SKIN = (236, 190, 150); GREYC = (70, 78, 120)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    """3 to 7 word headline with one key word in colour (kept from 2026-11-13: most mobile viewers watch muted)."""
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def bank(c, x, y, s, a, col=BANK, label=None, bg=BG, glow=0.0):
    """A simple bank building: roof, four columns, steps. (x, y) is the centre of the base."""
    if a <= .01: return
    w = 220 * s; h = 150 * s
    if glow > .01: c.circ(x, y - h * .6, w * .78, None, a * glow, outline=col, ow=5, bg=bg)
    poly(c, [(x - w * .62, y - h), (x + w * .62, y - h), (x, y - h - 70 * s)], col, a, bg)
    c.rr(x - w * .58, y - h - 4, x + w * .58, y - h + 14 * s, 4, col, a, bg=bg)
    for k in range(4):
        cx = x - w * .42 + k * w * .28
        c.rr(cx - 13 * s, y - h + 16 * s, cx + 13 * s, y - 18 * s, 4, col, a * .85, bg=bg)
    c.rr(x - w * .64, y - 18 * s, x + w * .64, y, 4, col, a, bg=bg)
    if label: c.text(x, y + 38, label, 34, col, a, w='Bold', bg=bg)

def person(c, x, y, s, a, col=GREYC, bg=BG, label=None, lcol=DIM):
    """A plain figure: head and rounded body. (x, y) is the feet."""
    if a <= .01: return
    c.rr(x - 46 * s, y - 120 * s, x + 46 * s, y, 30 * s, col, a, bg=bg)
    c.circ(x, y - 152 * s, 32 * s, SKIN, a, bg=bg)
    if label: c.text(x, y + 36, label, 32, lcol, a, w='Bold', bg=bg)

def note(c, x, y, a, s=1.0, bg=BG):
    """A banknote."""
    if a <= .01: return
    c.rr(x - 70 * s, y - 36 * s, x + 70 * s, y + 36 * s, 8, CASH, a, bg=bg)
    c.rr(x - 60 * s, y - 27 * s, x + 60 * s, y + 27 * s, 6, None, a, outline=(150, 110, 30), ow=3, bg=CASH)
    c.circ(x, y, 17 * s, None, a, outline=(150, 110, 30), ow=3, bg=CASH)

def phone(c, x, y, a, amount, col=MONEY, sub='Your account', bg=BG, glow=0.0, tag=None):
    """A phone showing a bank balance."""
    if a <= .01: return
    if glow > .01: c.rr(x - 150, y - 260, x + 150, y + 260, 46, None, a * glow, outline=col, ow=6, bg=bg)
    c.rr(x - 135, y - 245, x + 135, y + 245, 38, (36, 40, 72), a, bg=bg)
    c.rr(x - 118, y - 215, x + 118, y + 215, 24, (12, 16, 34), a, bg=(36, 40, 72))
    c.text(x, y - 150, sub, 28, DIM, a, w='Bold', bg=(12, 16, 34))
    c.text(x, y - 70, amount, 58, col, a, w='Bold', bg=(12, 16, 34))
    if tag: c.rr(x - 70, y - 10, x + 70, y + 34, 18, col, a, bg=(12, 16, 34)); c.text(x, y + 12, tag, 26, DARK, a, w='Bold', bg=col)
    for k in range(3): c.rr(x - 90, y + 70 + k * 44, x + 90, y + 92 + k * 44, 10, (34, 40, 70), a, bg=(12, 16, 34))

def ledger_row(c, x0, y, w, label, amount, col, a, bg=CARD):
    if a <= .01: return
    c.rr(x0, y - 38, x0 + w, y + 38, 16, (18, 22, 48), a, outline=col, ow=4, bg=bg)
    c.text(x0 + 30, y, label, 40, INK, a, 'lm', 'Bold', bg=(18, 22, 48))
    c.text(x0 + w - 30, y, amount, 44, col, a, 'rm', 'Bold', bg=(18, 22, 48))

def card_cc(c, x, y, a, bal, bg=BG):
    """A credit card with its balance."""
    if a <= .01: return
    c.rr(x - 190, y - 120, x + 190, y + 120, 22, (90, 70, 170), a, bg=bg)
    c.rr(x - 150, y - 60, x - 90, y - 15, 8, CASH, a, bg=(90, 70, 170))
    for k in range(4): c.rr(x - 150 + k * 80, y + 40, x - 90 + k * 80, y + 58, 6, (200, 190, 255), a, bg=(90, 70, 170))
    c.text(x, y + 170, bal, 44, DEBT, a, w='Bold', bg=bg)

def sparks(c, x, y, a, t, col=MONEY, n=10, r=120, bg=BG):
    if a <= .01: return
    for k in range(n):
        ang = 6.283 * k / n + t * .8; d = r * (.7 + .3 * math.sin(t * 3 + k))
        c.circ(x + d * math.cos(ang), y + d * math.sin(ang), 6, col, a * (.5 + .5 * math.sin(t * 4 + k)), bg=bg)

def car(c, x, y, a, s=1.0, bg=BG):
    if a <= .01: return
    c.rr(x - 120 * s, y - 40 * s, x + 120 * s, y + 10 * s, 18, (120, 130, 180), a, bg=bg)
    poly(c, [(x - 70 * s, y - 40 * s), (x - 40 * s, y - 80 * s), (x + 50 * s, y - 80 * s), (x + 80 * s, y - 40 * s)], (120, 130, 180), a, bg)
    for dx in (-70, 70): c.circ(x + dx * s, y + 12 * s, 24 * s, (30, 34, 60), a, bg=bg)

# ---------- scenes ----------
def s_hook(c, T, t):
    """The payoff is on screen from frame one (lesson of 2026-11-21, vidIQ): new money arriving from a loan."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Not ', INK), ('your savings', CASH)], sw_out(T, 1))
    headline(c, [('Lending ', INK), ('creates', MONEY), (' money', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Central banks ', OTHER), ('say so', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('How it works. ', INK), ('What limits it.', DEBT)], sw_in(T, 3), size=76)
    m2 = hl(2) * (1 - hl(3))
    top = 1 - m2
    bank(c, 460, 700, 1.4, top, glow=.6 + .4 * math.sin(t * 2))
    c.text(460, 750, 'Your bank', 36, BANK, top, w='Bold')
    # a pulse travels from the bank to the phone, and the balance is already there from the first frame
    p = (t * .7) % 1.0
    c.arrow(700, 520, 1240, 520, MONEY, 6, top * .8)
    c.text(970, 480, 'loan', 38, MONEY, top, w='Bold')
    c.circ(700 + 540 * p, 520, 14, MONEY, top * (1 - p))
    phone(c, 1440, 540, top, '+$20,000', tag='NEW', glow=.5 + .5 * math.sin(t * 3))
    sparks(c, 1440, 540, top, t, r=270)
    c.text(1440, 840, 'Illustrative example', 28, DIM, top, w='Regular')
    # line 2: two plaques, text only
    for k, (nm, yr) in enumerate((('Bank of England', '2014'), ('Reserve Bank of Australia', '2018'))):
        x = 560 + k * 800; u = m2 * fd(T(2), .2 + .5 * k)
        c.rr(x - 340, 360, x + 340, 700, 26, CARD, u, outline=OTHER, ow=4)
        bank(c, x, 560, .9, u, col=OTHER, bg=CARD)
        c.text(x, 620, nm, 40, INK, u, w='Bold', bg=CARD); c.text(x, 668, yr, 32, DIM, u, w='Bold', bg=CARD)

def s_story(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('The story we ', INK), ('learned', CASH)], sw_out(T, 3))
    headline(c, [('It works the ', INK), ('other way', DEBT)], sw_in(T, 3))
    SX, BX, RX, Y = 330, 960, 1590, 760
    person(c, SX, Y, 1.2, 1, label='saver')
    bank(c, BX, Y, 1.3, 1, label='bank')
    person(c, RX, Y, 1.2, 1, col=(90, 80, 140), label='borrower')
    u = fd(T(1), .4, 2.4) if T(1) > -.1 else 0.0
    if T(1) > -.1:
        if u < .5: nx = SX + (BX - SX) * ease(u / .5); ny = 470
        else: nx = BX + (RX - BX) * ease((u - .5) / .5); ny = 470
        note(c, nx, ny - 40 * math.sin(math.pi * ((u * 2) % 1)), 1 - .6 * hl(3))
        c.text(nx, ny - 110, '$100', 40, CASH, 1 - hl(3), w='Bold', stroke=3)
    m2 = hl(2) * (1 - hl(3))
    c.arrow(SX + 90, 560, BX - 160, 560, CASH, 6, m2); c.arrow(BX + 160, 560, RX - 90, 560, CASH, 6, m2)
    c.rr(BX - 160, 290, BX + 160, 350, 24, CARD, m2, outline=CASH, ow=3); c.text(BX, 320, 'middleman?', 36, CASH, m2, w='Bold', bg=CARD)
    m3 = hl(3)
    c.cross(BX, 470, 90 * m3 + 1, DEBT, m3)
    c.text(BX, 860, 'Bank of England: the reverse of the textbook story', 30, DIM, m3, w='Regular')

def s_loan(c, T, t):
    """Illustrative car loan: nobody's account goes down; a new deposit appears with a matching debt."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Borrow ', INK), ('$20,000', DEBT)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Nobody else ', INK), ('loses', MONEY)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('New money', MONEY), (' appears', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Two new lines', BANK)], sw_in(T, 3))
    m0 = hl(0) * (1 - hl(1))
    car(c, 960, 520, m0, 2.2); c.text(960, 700, 'a car: $20,000', 44, INK, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    for k, bal in enumerate(('$5,200', '$830', '$12,400')):
        x = 480 + k * 480; u = m1 * fd(T(1), .2 * k)
        c.rr(x - 190, 360, x + 190, 660, 26, CARD, u, outline=GREYC, ow=3)
        person(c, x, 520, .6, u, bg=CARD)
        c.text(x, 580, bal, 46, MONEY, u, w='Bold', bg=CARD)
        c.check(x + 140, 400, 26, MONEY, u, fd(T(1), 1.0 + .2 * k))
    c.text(960, 740, "other people's savings: unchanged", 38, DIM, m1, w='Bold')
    m2 = hl(2) * (1 - hl(3))
    v = int(20000 * fd(T(2), 1.6, 1.2))
    bank(c, 560, 720, 1.4, m2, glow=m2)
    c.arrow(800, 520, 1220, 520, MONEY, 6, m2 * fd(T(2), .8))
    phone(c, 1440, 540, m2, f'${v:,}', glow=fd(T(2), 2.6), tag='NEW' if v >= 20000 else None)
    sparks(c, 1440, 540, m2 * fd(T(2), 2.6), t, r=270)
    m3 = hl(3)
    c.rr(380, 300, 1540, 760, 28, CARD, m3, outline=BANK, ow=4)
    c.text(960, 350, "The bank's books", 40, BANK, m3, w='Bold', bg=CARD)
    ledger_row(c, 440, 470, 1040, 'You owe the bank', '$20,000', DEBT, m3 * fd(T(3), .3))
    ledger_row(c, 440, 620, 1040, 'In your account', '$20,000', MONEY, m3 * fd(T(3), 2.2))
    c.text(960, 860, 'Illustrative example', 28, DIM, max(m0, m2, m3), w='Regular')

def s_most(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Real money: ', INK), ('tap and pay', MONEY)], sw_out(T, 1))
    headline(c, [('Notes and coins: ', CASH), ('$75 billion', CASH)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('All money: ', INK), ('about $2 trillion', MONEY)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Under ', INK), ('4¢', CASH), (' in every $1 is cash', INK)], sw_in(T, 3))
    m0 = hl(0) * (1 - hl(1))
    c.rr(560, 360, 900, 700, 28, (50, 56, 90), m0); c.rr(600, 400, 860, 520, 12, (12, 16, 34), m0, bg=(50, 56, 90))
    c.text(730, 460, 'APPROVED', 34, MONEY, m0 * fd(T(0), 1.2), w='Bold', bg=(12, 16, 34))
    tap = .5 + .5 * math.sin(t * 2.5)
    c.rr(1080 - 30 * tap, 420, 1460 - 30 * tap, 660, 22, (90, 70, 170), m0)
    for k in range(3): c.circ(990 - 30 * tap, 540, 30 + 30 * k, None, m0 * (1 - k * .3), outline=MONEY, ow=4)
    # lines 1-3: notes, then one bar drawn to scale (RBA figures, 2018)
    m1 = hl(1)
    for k in range(5):
        note(c, 380 + k * 14, 440 - k * 14, m1 * (1 - hl(2)) * fd(T(1), .2 * k), 1.3)
    c.text(420, 560, '$75 billion', 50, CASH, m1 * (1 - hl(2)), w='Bold')
    c.text(420, 610, 'notes and coins', 32, DIM, m1 * (1 - hl(2)), w='Bold')
    m2 = hl(2)
    X0, X1, Y = 260, 1660, 520
    if m2 > .01:
        g = fd(T(2), .2, 1.4)
        c.rr(X0, Y - 70, X0 + (X1 - X0) * g, Y + 70, 18, MONEY, m2)
        c.text(X0 + (X1 - X0) * g / 2 + 30, Y, 'bank deposits', 48, DARK, m2 * fd(T(2), 1.2), w='Bold', bg=MONEY)
        cw = (X1 - X0) * 75 / 2000
        c.rr(X0, Y - 70, X0 + cw, Y + 70, 8, CASH, m2, bg=MONEY)
        c.arrow(X0 + cw / 2, Y + 170, X0 + cw / 2, Y + 80, CASH, 5, m2)
        c.text(X0, Y + 205, 'notes and coins', 34, CASH, m2, 'lm', 'Bold')
        c.text(X1, Y - 110, 'about $2 trillion in all', 36, MONEY, m2, 'rm', 'Bold')
        c.text(1660, 860, 'Australia, 2018 (Reserve Bank of Australia). Bar drawn to scale.', 28, DIM, m2, 'rm', 'Regular')
    m3 = hl(3)
    c.rr(X0 - 12, Y - 82, X0 + (X1 - X0) * 75 / 2000 + 12, Y + 82, 12, None, m3 * (.6 + .4 * math.sin(t * 4)), outline=INK, ow=5)

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a teal pattern-interrupt background (lesson of 2026-10-13)."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Pay it back. ', INK), ('Then what?', CASH)], 1, bg=QUIZ)
    for k, (txt, col) in enumerate((('A  Goes to savers', INK), ('B  The bank keeps it', INK), ('C  It disappears', INK))):
        u = fd(t, .6 + .3 * k)
        c.rr(330, 330 + k * 150, 1250, 440 + k * 150, 26, (24, 80, 86), u, outline=(90, 160, 160), ow=3, bg=QUIZ)
        c.text(380, 385 + k * 150, txt, 46, col, u, 'lm', 'Bold', bg=(24, 80, 86))
    if T(0) > 0:
        e = T(0) - 5.2; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 5.0)
        c.circ(1530, 540, 96, CASH, u, bg=QUIZ); c.text(1530, 540, str(k) if k else '?', 88, DARK, u, w='Bold', bg=CASH)

def s_gone(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('It ', INK), ('disappears', DEBT)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Repaying ', INK), ('destroys', DEBT), (' money', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Same with a ', INK), ('credit card', OTHER)], sw_in(T, 2))
    m = 1 - hl(2)
    g = fd(T(0), .1, 1.6) if T(0) > -.1 else 0.0
    rem = 1 - g
    c.rr(300, 300, 1080, 760, 28, CARD, m, outline=BANK, ow=4)
    c.text(690, 350, "The bank's books", 38, BANK, m, w='Bold', bg=CARD)
    ledger_row(c, 340, 480, 700, 'You owe', f'${int(20000 * rem):,}', DEBT, m * (.25 + .75 * rem))
    ledger_row(c, 340, 640, 700, 'Your account', f'${int(20000 * rem):,}', MONEY, m * (.25 + .75 * rem))
    rnd = random.Random(3)
    for k in range(14):
        px = 1110 + rnd.random() * 90; py = 470 + rnd.random() * 180 - 200 * g * rnd.random()
        c.circ(px, py, 5 + 5 * rnd.random(), MONEY if k % 2 else DEBT, m * g * (1 - g) * 3 * .5)
    m1 = hl(1) * m
    c.text(1450, 430, 'loan made:', 40, DIM, m1, w='Bold'); c.text(1450, 490, 'money created', 48, MONEY, m1, w='Bold')
    c.text(1450, 600, 'loan repaid:', 40, DIM, m1 * fd(T(1), 1.2)); c.text(1450, 660, 'money destroyed', 48, DEBT, m1 * fd(T(1), 1.2), w='Bold')
    m2 = hl(2)
    v = 1 - fd(T(2), 2.4, 1.4)
    card_cc(c, 640, 500, m2, f'balance ${int(1500 * v):,}')
    c.arrow(900, 500, 1200, 500, DIM, 6, m2 * fd(T(2), 1.6))
    c.text(1420, 470, 'pay the bill', 46, INK, m2 * fd(T(2), 1.6), w='Bold')
    c.text(1420, 530, 'that money is gone', 40, DEBT, m2 * fd(T(2), 3.6), w='Bold')
    c.text(960, 860, 'Illustrative amounts', 28, DIM, max(m, m2), w='Regular')

def dial(c, x, y, r, a, val, bg=CARD):
    """An interest-rate dial; val 0..1 moves the needle."""
    if a <= .01: return
    for k in range(21):
        ang = math.pi * (1 + k / 20)
        col = DEBT if k > 13 else (CASH if k > 7 else MONEY)
        c.line([(x + r * .82 * math.cos(ang), y + r * .82 * math.sin(ang)), (x + r * math.cos(ang), y + r * math.sin(ang))], col, 7, a, bg=bg)
    ang = math.pi * (1 + val)
    c.line([(x, y), (x + r * .75 * math.cos(ang), y + r * .75 * math.sin(ang))], INK, 8, a, bg=bg); c.circ(x, y, 14, INK, a, bg=bg)

def s_limits(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Why not ', INK), ('endless', DEBT), (' money?', INK)], sw_out(T, 1))
    headline(c, [('Three ', INK), ('limits', CASH)], sw_in(T, 1))
    tiles = ((1, 'Loans must pay', 'Unpaid loans are losses', MONEY), (2, 'Rules on capital', 'A cushion for losses', BANK),
             (3, 'Interest rates', 'Higher rates, less borrowing', OTHER))
    m0 = hl(0) * (1 - hl(1))
    bank(c, 960, 700, 1.6, m0)
    rnd = random.Random(5)
    for k in range(14):
        ang = rnd.random() * 6.283; d = 240 + 80 * math.sin(t * 2 + k)
        note(c, 960 + d * math.cos(ang + t * .3), 520 + .6 * d * math.sin(ang + t * .3), m0 * .8, .6)
    for ln, head, sub, col in tiles:
        m = hl(ln); x0 = 160 + (ln - 1) * 540; dy = 40 * (1 - m)
        c.rr(x0, 290 + dy, x0 + 500, 800 + dy, 26, CARD, m, outline=col, ow=5)
        c.circ(x0 + 60, 345 + dy, 32, col, m, bg=CARD); c.text(x0 + 60, 345 + dy, str(ln), 40, DARK, m, w='Bold', bg=col)
        cx, cy = x0 + 250, 500 + dy
        if ln == 1:
            for j, (h, cc) in enumerate(((90, MONEY), (130, MONEY), (60, DEBT))):
                c.rr(cx - 130 + j * 95, cy + 80 - h, cx - 70 + j * 95, cy + 80, 8, cc, m, bg=CARD)
            c.line([(cx - 160, cy + 82), (cx + 160, cy + 82)], DIM, 4, m, bg=CARD)
        if ln == 2:
            c.rr(cx - 150, cy + 20, cx + 150, cy + 80, 30, BANK, m * .7, bg=CARD)
            for j in range(3): note(c, cx - 70 + j * 70, cy - 10 - 6 * j, m, .6, bg=CARD)
        if ln == 3:
            dial(c, cx, cy + 70, 120, m, .3 + .45 * fd(T(3), .8, 1.6))
        c.text(x0 + 250, 680 + dy, head, 40, col, m, w='Bold', bg=CARD)
        c.text(x0 + 250, 735 + dy, sub, 30, INK, m, w='Medium', bg=CARD)

def s_savings(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Do savings ', INK), ('matter?', MONEY)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Money moves ', INK), ('between banks', OTHER)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Deposits matter. ', MONEY), ('Not first.', INK)], sw_in(T, 2))
    YB = 720
    bank(c, 520, YB, 1.3, 1, label='your bank')
    m0 = hl(0) * (1 - hl(1))
    c.circ(960, 520, 70, MONEY, m0); c.check(960, 520, 58, DARK, m0, fd(T(0), 1.6, .5))
    m1 = hl(1)
    bank(c, 1400, YB, 1.3, m1, col=OTHER, label="seller's bank")
    car(c, 1400, 360, m1, 1.0)
    p = fd(T(1), .8, 1.4)
    c.arrow(720, 470, 1200, 470, MONEY, 6, m1 * fd(T(1), .5))
    c.circ(720 + 480 * p, 470, 16, MONEY, m1 * (1 - p * .5))
    c.text(960, 430, '$20,000', 40, MONEY, m1, w='Bold')
    m2 = hl(2)
    for k in range(3): person(c, 110 + k * 80, 470, .55, m2 * .9)
    c.text(190, 300, 'savers', 32, DIM, m2, w='Bold')
    for k in range(3):
        ph = (t * .5 + k * .33) % 1.0
        note(c, 230 + 170 * ph, 420 + 150 * ph, m2 * (1 - ph), .5)
    c.text(520, 820, 'needs deposits or other funding', 32, MONEY, m2, w='Bold')

def s_recap(c, T, t):
    """Recap as three ledger rows stacked down the screen."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', CASH)], 1)
    items = ((1, 'When a bank lends, it creates new money.', MONEY), (2, 'Repaying a loan makes that money disappear.', DEBT),
             (3, 'Profits, rules and interest rates set the limits.', OTHER))
    for ln, txt, col in items:
        m = hl(ln); y = 330 + (ln - 1) * 170; dx = 60 * (1 - m)
        c.rr(220 + dx, y - 65, 1700 + dx, y + 65, 26, CARD, m, outline=col, ow=5)
        c.circ(300 + dx, y, 40, col, m, bg=CARD); c.text(300 + dx, y, str(ln), 48, DARK, m, w='Bold', bg=col)
        c.text(380 + dx, y, txt, 50, INK, m, 'lm', 'Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    bank(c, 1330, 830, 1.2, 1, glow=1)
    phone(c, 1650, 470, 1, '+$20,000', tag='NEW', glow=1)
    c.arrow(1400, 600, 1500, 520, MONEY, 8, 1)

SCENES = [
 ('THE CLAIM', ["Banks don't lend out your savings.",
                "When a bank makes a loan, it creates new money in the borrower's account.",
                "That's how central banks describe it, including the Bank of England and the Reserve Bank of Australia.",
                "Here's how it works, and what keeps it in check."], s_hook),
 ('THE OLD STORY', ["Here's the story many of us learned.",
                    "You put a hundred dollars in the bank. The bank lends that same hundred to someone else.",
                    "So the bank is just a middleman, passing your cash along.",
                    "The Bank of England says real banking works the other way round."], s_story),
 ('A LOAN', ["Say you borrow twenty thousand dollars to buy a car.",
             "The bank doesn't take that money out of anyone else's account.",
             "It writes the loan, and at that same moment, twenty thousand new dollars appear in your account.",
             "Its books get two new lines. You owe the bank twenty thousand. And you have twenty thousand to spend."], s_loan),
 ('MOST MONEY', ["That new deposit is real money. You can tap your card and spend it.",
                 "And most money is just like this. In twenty eighteen, Australia had about seventy-five billion dollars in notes and coins.",
                 "But all the money, counting bank deposits, came to about two trillion.",
                 "So less than four cents in every dollar was cash. The rest was money in bank accounts."], s_most),
 ('QUICK QUESTION', ["Quick question. When you pay the loan back, where does that money go? Have a guess."], s_quiz),
 ('THE ANSWER', ["It disappears.",
                 "Repaying a loan destroys money, just as taking out the loan created it.",
                 "It's the same with a credit card. Pay the bill, and the money the card created is gone."], s_gone),
 ('THE LIMITS', ["So why don't banks just create money without end?",
                 "First, a loan has to make a profit. Loans that are never repaid are losses.",
                 "Second, rules make banks hold capital, a cushion to absorb those losses.",
                 "Third, the central bank sets interest rates. Higher rates mean people want to borrow less."], s_limits),
 ('YOUR SAVINGS', ["So do your savings matter to a bank? Yes.",
                   "When you pay the car seller, that money may move to the seller's bank.",
                   "So your bank needs deposits, or other funding, to cover the loan. Deposits still matter. They just don't come first."], s_savings),
 ('RECAP', ["Three things to keep.",
            "One: when a bank lends, it creates new money in your account.",
            "Two: repaying a loan makes that money disappear.",
            "Three: profits, rules and interest rates limit how much banks create.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('Where does ', INK), ('loan money', MONEY), (' come from?', INK)], sw_out(T, 1), size=76)
    headline(c, [('The bank ', BANK), ('creates it', MONEY)], sw_in(T, 1), size=92)
    bank(c, 460, 700, 1.4, 1, glow=.6 + .4 * math.sin(t * 2))
    p = (t * .7) % 1.0
    c.arrow(700, 520, 1240, 520, MONEY, 6, .8)
    c.circ(700 + 540 * p, 520, 14, MONEY, 1 - p)
    phone(c, 1440, 540, 1, '+$20,000', tag='NEW', glow=.5 + .5 * math.sin(t * 3))
    sparks(c, 1440, 540, 1, t, r=270)
    c.text(1440, 840, 'Illustrative example', 28, DIM, 1, w='Regular')

def short_limits(c, T, t):
    headline(c, [('Not ', INK), ('without limit', DEBT)], 1)
    for k, (head, col) in enumerate((('Loans must pay', MONEY), ('Capital rules', BANK), ('Interest rates', OTHER))):
        m = fd(T(0), .3 + 1.3 * k); x0 = 160 + k * 540
        c.rr(x0, 330, x0 + 500, 720, 26, CARD, m, outline=col, ow=5)
        c.circ(x0 + 250, 470, 60, col, m, bg=CARD); c.text(x0 + 250, 470, str(k + 1), 64, DARK, m, w='Bold', bg=col)
        c.text(x0 + 250, 630, head, 46, col, m, w='Bold', bg=CARD)

SHORT_SCENES = [
 ('THE QUESTION', ["Where does the money in a bank loan come from?",
                   "Not from other people's savings. The bank creates it."], short_hook),
 ('THE LOAN', ["Say you borrow twenty thousand dollars for a car.",
               "Nobody else's account goes down.",
               "The bank writes the loan, and twenty thousand new dollars appear in your account.",
               "You owe twenty thousand. And you have twenty thousand to spend."], s_loan),
 ('THE CATCH', ["Pay it back, and that money disappears.",
                "Repaying a loan destroys money, just as the loan created it."], s_gone),
 ('THE LIMITS', ["And banks can't do it without limit.",
                "Loans must make a profit, rules make banks hold capital, and interest rates cool borrowing."], short_limits),
 ('THE ANSWER', ["So most money is created when banks lend.",
                 "And paying a loan back makes it disappear."], card('Lending creates money.', 'Repaying destroys it.')),
]
SHORT_HITS = [(4, 0, 0.0)]
