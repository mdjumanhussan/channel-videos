"""Episode: The 'I'm Not a Robot' Box Isn't About the Click (CAPTCHA: the reverse Turing test, reCAPTCHA's two words that digitised books, image grids, the 2014 checkbox, cookies and browser history, AI solving 100% of image puzzles)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "What 'I'm Not a Robot' Checks"                  # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "What does 'I'm not a robot' check?"              # headline on the vertical Short
HITS = [(0, 3, 0.0), (6, 3, 0.0), (7, 1, 0.0)]                 # title card, quiz answer, AI solves 100%
THUMB = ['THAT BOX', "ISN'T CHECKING", 'YOUR CLICK']
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.4, (0, 3): 0.5, (2, 2): 0.4, (6, 2): 0.3, (6, 3): 0.5, (7, 1): 0.5}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'ree-captcha': 'reCAPTCHA', 'captcha': 'CAPTCHA', 'a hundred million': '100 million',
                 'one hundred percent': '100%', 'seventy percent': '70%', 'E T H': 'ETH'}

# One object tells the story (lesson of 2026-11-02): the same "prove you're human" box sits at the centre of
# almost every scene and changes form as the years go by (wobbly letters -> two words -> photo grid -> tick box -> invisible).
# Colour code kept in every scene: known word / human = green, unknown word = yellow, bots and AI = pink, clues = cyan.
KNOWN = GR; UNKNOWN = YE; BOT = PK; HUMAN = GR; CLUE = CY
PAPER = (226, 216, 190); INKP = (90, 84, 70); FRAME = (70, 80, 140); SKY = (52, 76, 120); ROAD = (60, 62, 74)
COOKIE = (200, 145, 80)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def widget(c, x, y, w, h, a=1.0, year=None, dashed=False):
    """The 'prove you're human' box. Returns its inner box."""
    if a <= .01: return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if dashed:
        x0, y0, x1, y1 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
        for k in range(0, int(w), 40):
            c.line([(x0 + k, y0), (x0 + min(w, k + 22), y0)], FRAME, 5, a); c.line([(x0 + k, y1), (x0 + min(w, k + 22), y1)], FRAME, 5, a)
        for k in range(0, int(h), 40):
            c.line([(x0, y0 + k), (x0, y0 + min(h, k + 22))], FRAME, 5, a); c.line([(x1, y0 + k), (x1, y0 + min(h, k + 22))], FRAME, 5, a)
    else:
        c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 22, CARD, a, outline=FRAME, ow=4)
    if year:
        c.rr(x + w / 2 - 150, y - h / 2 - 26, x + w / 2 - 14, y - h / 2 + 22, 24, CY, a)
        c.text(x + w / 2 - 82, y - h / 2 - 2, year, 34, BG, a, w='Bold', bg=CY)
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)

def wobbly(c, x, y, word, size, col, a, t, seed=0, bg=CARD, smudge=0.0, strike=True):
    """A squashed, wavy CAPTCHA word centred on (x, y)."""
    if a <= .01: return
    ws = [c.tw(ch, size, 'Bold') * 1.04 for ch in word]; cx = x - sum(ws) / 2
    for i, ch in enumerate(word):
        dy = size * .16 * math.sin(i * 1.7 + seed + t * .8)
        sz = int(size * (.86 + .26 * rnd(i, seed)))
        c.text(cx + ws[i] / 2, y + dy, ch, sz, col, a, w='Bold', bg=bg); cx += ws[i]
    if strike:
        L = sum(ws)
        c.line([(x - L / 2 - 10 + (L + 20) * k / 30, y + size * .12 * math.sin(k * .5 + seed)) for k in range(31)], col, 4, a * .8, bg)
    if smudge > .01:
        for k in range(7):
            c.circ(x - sum(ws) / 2 + sum(ws) * rnd(k, seed + 5), y + size * (rnd(k, seed + 6) - .5) * .7, size * (.16 + .1 * rnd(k, 9)),
                   (120, 112, 96), a * smudge * .55, bg=bg)

def robot(c, x, y, s=1.0, a=1.0, bg=BG, col=BOT):
    if a <= .01: return
    c.line([(x, y - 48 * s), (x, y - 78 * s)], (150, 160, 200), 5 * s, a, bg); c.circ(x, y - 84 * s, 10 * s, col, a, bg=bg)
    c.rr(x - 58 * s, y - 50 * s, x + 58 * s, y + 46 * s, 18 * s, (120, 130, 175), a, bg=bg)
    c.circ(x - 24 * s, y - 10 * s, 13 * s, col, a, bg=(120, 130, 175)); c.circ(x + 24 * s, y - 10 * s, 13 * s, col, a, bg=(120, 130, 175))
    c.rr(x - 26 * s, y + 18 * s, x + 26 * s, y + 28 * s, 4 * s, BG, a, bg=(120, 130, 175))

def person(c, x, y, s=1.0, col=HUMAN, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x, y - 40 * s, 24 * s, (225, 180, 150), a, bg=bg)
    c.rr(x - 30 * s, y - 10 * s, x + 30 * s, y + 56 * s, 22 * s, col, a, bg=bg)

def tickbox(c, x, y, a=1.0, p=0.0, s=1.0, year=None, bg=BG):
    """The 2014-style tick box: a square and 'I'm not a robot'."""
    if a <= .01: return
    widget(c, x, y, 640 * s, 170 * s, a, year)
    bx = x - 320 * s + 90 * s
    c.rr(bx - 40 * s, y - 40 * s, bx + 40 * s, y + 40 * s, 10 * s, (235, 238, 250) if p < .01 else (225, 250, 235), a, outline=(150, 160, 200), ow=4, bg=CARD)
    if p > 0: c.check(bx, y, 46 * s, (40, 170, 90), a, p)
    c.text(bx + 70 * s, y, "I'm not a robot", int(50 * s), INK, a, anchor='lm', w='Bold', bg=CARD)

def cursor(c, x, y, s=1.0, a=1.0, bg=BG):
    if a <= .01: return
    pts = [(x, y), (x, y + 52 * s), (x + 14 * s, y + 40 * s), (x + 26 * s, y + 64 * s), (x + 36 * s, y + 58 * s), (x + 24 * s, y + 36 * s), (x + 40 * s, y + 34 * s)]
    poly(c, pts, INK, a, bg); c.line(pts + [pts[0]], BG, 3 * s, a, INK)

def traffic_light(c, x, y, s=1.0, a=1.0, bg=SKY):
    if a <= .01: return
    c.line([(x, y + 40 * s), (x, y + 120 * s)], (150, 155, 170), 6 * s, a, bg)
    c.rr(x - 18 * s, y - 50 * s, x + 18 * s, y + 46 * s, 8 * s, (30, 32, 40), a, bg=bg)
    for k, col in enumerate(((235, 70, 70), (250, 200, 70), (80, 220, 120))):
        c.circ(x, y - 30 * s + k * 30 * s, 10 * s, col, a, bg=(30, 32, 40))

def grid(c, x, y, cell, a, t, sel=0.0, lights=(1, 3, 4, 8), head=True, ticks=True):
    """3x3 picture puzzle with its top-left corner at (x, y)."""
    if a <= .01: return
    g = 8; W3 = 3 * cell + 2 * g
    if head:
        c.rr(x, y - 110, x + W3, y - 14, 14, CY, a)
        c.text(x + W3 / 2, y - 76, 'Select all squares with', 32, BG, a, w='Medium', bg=CY)
        c.text(x + W3 / 2, y - 40, 'traffic lights', 40, BG, a, w='Bold', bg=CY)
    for k in range(9):
        cx0 = x + (k % 3) * (cell + g); cy0 = y + (k // 3) * (cell + g)
        c.rr(cx0, cy0, cx0 + cell, cy0 + cell, 8, SKY, a)
        c.rr(cx0, cy0 + cell * .72, cx0 + cell, cy0 + cell, 6, ROAD, a, bg=SKY)
        if k in lights: traffic_light(c, cx0 + cell * .5, cy0 + cell * .32, cell / 190, a)
        elif k % 2 == 0:
            c.rr(cx0 + cell * .15, cy0 + cell * .3, cx0 + cell * .6, cy0 + cell * .72, 6, (110, 90, 120), a, bg=SKY)
            c.rr(cx0 + cell * .25, cy0 + cell * .4, cx0 + cell * .35, cy0 + cell * .5, 3, YE, a * .8, bg=(110, 90, 120))
        else:
            c.circ(cx0 + cell * .7, cy0 + cell * .42, cell * .18, (60, 150, 100), a, bg=SKY)
            c.line([(cx0 + cell * .7, cy0 + cell * .55), (cx0 + cell * .7, cy0 + cell * .72)], (110, 80, 60), 6, a, SKY)
        if ticks and k in lights:
            n = lights.index(k)
            p = clamp(sel * len(lights) - n)
            if p > 0:
                c.rr(cx0, cy0, cx0 + cell, cy0 + cell, 8, None, a * p, outline=CY, ow=7, bg=SKY)
                c.circ(cx0 + 26, cy0 + 26, 20, CY, a * p, bg=SKY); c.check(cx0 + 26, cy0 + 26, 22, BG, a * p, 1)

def page(c, x0, y0, x1, y1, a, hi=0.0, seed=2):
    """An old scanned page; one word is smudged. Returns the smudged word's centre."""
    if a <= .01: return (0, 0)
    c.rr(x0, y0, x1, y1, 10, PAPER, a)
    c.rr(x0 + 30, y0 + 28, x1 - 30, y0 + 70, 6, INKP, a * .9, bg=PAPER)
    rows = int((y1 - y0 - 110) / 34); spot = None
    for r in range(rows):
        yy = y0 + 100 + r * 34; xx = x0 + 30
        while xx < x1 - 60:
            ln = 30 + 70 * rnd(r * 13 + int(xx), seed)
            if xx + ln > x1 - 30: break
            if r == rows // 2 and spot is None and xx > (x0 + x1) / 2 - 60:
                spot = (xx + 60, yy); c.circ(xx + 30, yy, 16, (130, 122, 100), a, bg=PAPER); c.circ(xx + 70, yy + 4, 20, (150, 140, 115), a, bg=PAPER)
                c.rr(xx, yy - 8, xx + 120, yy + 8, 4, INKP, a * .5, bg=PAPER); xx += 140; continue
            c.rr(xx, yy - 7, xx + ln, yy + 7, 4, INKP, a * .55, bg=PAPER); xx += ln + 16
    if spot and hi > .01:
        c.rr(spot[0] - 80, spot[1] - 28, spot[0] + 80, spot[1] + 28, 12, None, a * hi, outline=UNKNOWN, ow=6, bg=PAPER)
    return spot or ((x0 + x1) / 2, (y0 + y1) / 2)

def cookie(c, x, y, r, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, COOKIE, a, bg=bg)
    for k in range(6):
        an = k * 1.1 + .4; d = r * (.25 + .4 * rnd(k, 4))
        c.circ(x + d * math.cos(an), y + d * math.sin(an), r * .12, (90, 55, 30), a, bg=COOKIE)

def browser(c, x, y, w, h, a=1.0, rows=4, bg=BG, col=CLUE):
    """A browser window with history rows."""
    if a <= .01: return
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 16, CARD, a, outline=col, ow=4, bg=bg)
    c.rr(x - w / 2, y - h / 2, x + w / 2, y - h / 2 + 40, 14, (44, 52, 100), a, bg=CARD)
    for k, cc in enumerate(((235, 90, 90), (250, 200, 70), (80, 210, 120))):
        c.circ(x - w / 2 + 28 + k * 26, y - h / 2 + 20, 8, cc, a, bg=(44, 52, 100))
    for r in range(rows):
        yy = y - h / 2 + 70 + r * (h - 90) / max(1, rows)
        c.circ(x - w / 2 + 34, yy, 8, col, a, bg=CARD)
        c.rr(x - w / 2 + 56, yy - 7, x - w / 2 + 56 + (w - 100) * (.5 + .45 * rnd(r, 3)), yy + 7, 5, (90, 100, 150), a, bg=CARD)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    """The tick box, with a cookie and a browser window glowing behind it."""
    browser(c, 1560, 380, 520, 360, 1.0, rows=5)
    cookie(c, 1760, 690, 110)
    tickbox(c, 1480, 760, 1.0, 1.0, s=.95)
    cursor(c, 1290, 790, 1.4)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'You may have helped read old newspapers', 66, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, "One word came from a page computers couldn't read", 56, UNKNOWN, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'Now you just tick a box. How does it know?', 64, CY, a * hl(2), w='Bold')
        k = a * (1 - hl(2))
        if k > 0:
            spot = page(c, 1180, 250, 1700, 840, k, hl(1))
            box = widget(c, 620, 520, 760, 300, k)
            wobbly(c, 450, 520, 'harbour', 70, KNOWN, k, t, 1)
            wobbly(c, 800, 520, 'quietly', 70, UNKNOWN if hl(1) > .5 else INK, k, t, 3, smudge=1.0)
            c.text(620, 720, 'type the two words', 40, DIM, k, w='Bold')
            if hl(1) > 0:
                c.rr(680, 470, 920, 572, 14, None, k * hl(1), outline=UNKNOWN, ow=6, bg=CARD)
                c.arrow(spot[0] - 90, spot[1], 940, 520, UNKNOWN, 7, k * fd(T(1), .5), 22)
        k2 = a * hl(2)
        if k2 > 0:
            tickbox(c, 960, 560, k2, fd(T(2), 1.0, .5))
            cursor(c, 760 + 40 * (1 - fd(T(2), .3, .8)), 590 + 40 * (1 - fd(T(2), .3, .8)), 1.0, k2)
            person(c, 380, 560, 1.6, HUMAN, k2); robot(c, 1540, 560, 1.4, k2)
            c.text(380, 740, 'human?', 44, HUMAN, k2, w='Bold'); c.text(1540, 740, 'robot?', 44, BOT, k2, w='Bold')
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 300 + 30 * (1 - m), "The 'I'm Not a Robot' Box", 108, INK, m, w='Bold')
        c.text(960, 440 + 30 * (1 - m), "Isn't About the Click", 104, YE, m, w='Bold')
        c.line([(960 - 380 * m, 545), (960 + 380 * m, 545)], CY, 8, m)
        tickbox(c, 760, 720, m * fd(T(3), .5), 1.0, s=.8)
        cookie(c, 1260, 720, 56, m * fd(T(3), .8))
        browser(c, 1440, 720, 200, 150, m * fd(T(3), 1.0), rows=3)

ACRO = ['Completely', 'Automated', 'Public', 'Turing', 'test', 'to', 'tell', 'Computers', 'and', 'Humans', 'Apart']
def s_test(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'What is this test? A CAPTCHA', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Named in 2003, at Carnegie Mellon University', 62, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'The name is a long acronym', 66, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'A computer testing you, to keep out bots', 64, CY, hl(3) * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'Early tests: squashed, wobbly letters', 66, INK, hl(4), w='Bold')
    k = 1 - hl(3)
    if k > 0:
        word = 'CAPTCHA'; n = len(word)
        for i, ch in enumerate(word):
            m = k * fd(T(0), .3 + i * .12)
            c.text(960 + (i - (n - 1) / 2) * 150, 400 + 30 * (1 - m), ch, 170, YE if hl(2) > .5 else INK, m, w='Bold')
        if hl(1) > 0 and hl(2) < 1:
            kk = k * hl(1) * (1 - hl(2))
            c.rr(810, 560, 1110, 640, 40, CY, kk); c.text(960, 600, '2003', 52, BG, kk, w='Bold', bg=CY)
            c.text(960, 720, 'Luis von Ahn and colleagues', 50, INK, kk * fd(T(1), .5), w='Bold')
        if hl(2) > 0:
            kk = k * hl(2)
            rows = (ACRO[:5], ACRO[5:])
            for r, ws in enumerate(rows):
                tot = sum(c.tw(w + ' ', 58, 'Bold') for w in ws); x = 960 - tot / 2; y = 610 + r * 90
                for j, w in enumerate(ws):
                    idx = ACRO.index(w); m = kk * fd(T(2), .2 + idx * .18)
                    big = w[0].isupper() and w not in ('test',)
                    c.text(x, y, w[0], 58, YE if big else INK, m, anchor='lm', w='Bold')
                    c.text(x + c.tw(w[0], 58, 'Bold'), y, w[1:], 58, INK, m, anchor='lm', w='Bold')
                    x += c.tw(w + ' ', 58, 'Bold')
    k3 = hl(3) * (1 - hl(4))
    if k3 > 0:
        for j, (lab, l, r) in enumerate((('the usual Turing test', 'person', 'computer'), ('a CAPTCHA', 'computer', 'person'))):
            y = 360 + j * 260; kk = k3 * fd(T(3), j * 1.4)
            c.rr(260, y - 100, 1660, y + 100, 26, CARD, kk, outline=YE if j else FRAME, ow=4)
            for side, who in ((520, l), (1400, r)):
                if who == 'person': person(c, side, y, 1.2, HUMAN, kk, bg=CARD)
                else:
                    c.rr(side - 70, y - 60, side + 70, y + 40, 10, (90, 100, 150), kk, bg=CARD); c.rr(side - 20, y + 40, side + 20, y + 62, 4, (90, 100, 150), kk, bg=CARD)
            c.arrow(640, y, 1270, y, YE if j else DIM, 8, kk, 26)
            c.text(955, y - 40, 'tests', 40, INK, kk, w='Bold', bg=CARD); c.text(955, y + 50, lab, 36, YE if j else DIM, kk, w='Bold', bg=CARD)
        kk = k3 * fd(T(3), 3.0)
        c.text(960, 820, 'keeps out spam bots', 42, BOT, kk, w='Bold')
    k4 = hl(4)
    if k4 > 0:
        widget(c, 960, 430, 820, 300, k4, '2003')
        wobbly(c, 960, 430, 'xK7pQm', 120, INK, k4, t, 5)
        for j, (x, ok, lab) in enumerate(((560, True, 'people: easy'), (1360, False, 'programs then: mostly stuck'))):
            kk = k4 * fd(T(4), 1.0 + j * 1.2)
            if ok: person(c, x - 120, 720, 1.0, HUMAN, kk); c.check(x + 40, 720, 50, HUMAN, kk, fd(T(4), 1.4, .5))
            else: robot(c, x - 140, 730, .9, kk); c.cross(x + 20, 720, 50, BOT, kk)
            c.text(x, 830, lab, 40, HUMAN if ok else BOT, kk, w='Bold')

def s_two(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, '2007: reCAPTCHA adds a twist', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Two words. The computer knows one: the real test', 58, KNOWN, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, "The other: from a scanned page it couldn't read", 58, UNKNOWN, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'One marked question, one nobody can answer yet', 58, YE, hl(3), w='Bold')
    k = 1 - hl(3)
    if k > 0:
        widget(c, 700, 470, 880, 320, k, '2007')
        wobbly(c, 490, 470, 'morning', 76, KNOWN if hl(1) > .3 else INK, k * fd(T(0), .3), t, 2)
        wobbly(c, 910, 470, 'upon', 76, UNKNOWN if hl(2) > .3 else INK, k * fd(T(0), .6), t, 4, smudge=fd(T(0), .6))
        if hl(1) > 0:
            c.rr(320, 410, 660, 530, 16, None, k * hl(1), outline=KNOWN, ow=6, bg=CARD)
            c.text(490, 700, 'known word', 44, KNOWN, k * hl(1), w='Bold'); c.check(490, 780, 46, KNOWN, k * hl(1), fd(T(1), .4))
        if hl(2) > 0:
            c.rr(780, 410, 1040, 530, 16, None, k * hl(2), outline=UNKNOWN, ow=6, bg=CARD)
            c.text(910, 700, 'unknown word', 44, UNKNOWN, k * hl(2), w='Bold'); c.text(910, 790, '?', 90, UNKNOWN, k * hl(2), w='Bold')
            spot = page(c, 1300, 290, 1760, 820, k * hl(2), hl(2))
            c.arrow(spot[0] - 90, spot[1], 1060, 470, UNKNOWN, 7, k * fd(T(2), .6), 22)
            c.text(1530, 860, 'a scanned old page', 36, PAPER, k * hl(2), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        c.rr(560, 260, 1360, 860, 24, PAPER, k3)
        c.text(960, 320, 'QUIZ', 52, INKP, k3, w='Bold', bg=PAPER)
        for j, (q, col, sym) in enumerate((('Q1: answer known', (40, 150, 80), 'check'), ('Q2: nobody knows', (200, 140, 20), '?'))):
            y = 470 + j * 220; kk = k3 * fd(T(3), .4 + j * 1.0)
            c.rr(620, y - 70, 1300, y + 70, 14, (240, 232, 210), kk, outline=col, ow=5, bg=PAPER)
            c.text(660, y, q, 44, INKP, kk, anchor='lm', w='Bold', bg=(240, 232, 210))
            if sym == 'check': c.check(1240, y, 46, col, kk, fd(T(3), 1.0))
            else: c.text(1240, y, '?', 70, col, kk, w='Bold', bg=(240, 232, 210))

def s_votes(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Each answer is a vote. Enough agree: accepted', 60, KNOWN, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Old newspapers and books, read by people', 64, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Google bought it in 2009', 68, CY, hl(2), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        wobbly(c, 960, 265, 'upon', 80, UNKNOWN, k, t, 4, bg=BG, smudge=1.0)
        for j in range(3):
            x = 520 + j * 440; kk = k * fd(T(0), .4 + j * .6)
            person(c, x, 520, 1.3, HUMAN, kk)
            c.rr(x - 110, 390, x + 110, 450, 16, CARD, kk, outline=KNOWN, ow=3)
            c.text(x, 420, 'upon', 40, INK, kk, w='Bold', bg=CARD)
        fill = fd(T(0), 1.8, 1.4)
        c.rr(560, 690, 1360, 740, 25, CARD, k * fd(T(0), 1.6), outline=FRAME, ow=3)
        if fill > 0: c.rr(564, 694, 564 + 792 * fill, 736, 22, KNOWN, k, bg=CARD)
        c.text(960, 800, 'ACCEPTED', 64, KNOWN, k * fd(T(0), 3.0), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        for j in range(4):
            page(c, 230 + j * 26, 290 + j * 22, 640 + j * 26, 760 + j * 22, k1 * fd(T(1), j * .15), 0, seed=j + 3)
        c.arrow(780, 530, 1010, 530, CY, 10, k1 * fd(T(1), .8), 30)
        browser(c, 1340, 520, 560, 440, k1 * fd(T(1), 1.0), rows=6)
        c.text(470, 850, 'The New York Times archive', 40, PAPER, k1 * fd(T(1), .4), w='Bold')
        c.text(1340, 850, 'later: Google Books', 40, CY, k1 * fd(T(1), 1.8), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        widget(c, 600, 500, 620, 300, k2, '2009')
        wobbly(c, 600, 500, 'upon', 90, INK, k2, t, 4)
        n = int(100_000_000 * fd(T(2), 2.0, 2.2))
        c.text(1310, 420, f'{n:,}+', 84, YE, k2 * fd(T(2), 1.8), w='Bold')
        c.text(1310, 520, 'tests a day, by 2010', 48, INK, k2 * fd(T(2), 2.2), w='Bold')

def s_photos(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Computers got good at reading text', 66, BOT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, '2012: photos from Google Street View', 66, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Then the grid: pick every traffic light', 66, CY, hl(2), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        widget(c, 700, 500, 760, 300, k)
        wobbly(c, 700, 500, 'xK7pQm', 100, INK, k, t, 5)
        robot(c, 1400, 500, 1.6, k)
        c.rr(1220, 680, 1580, 760, 18, CARD, k * fd(T(0), .8), outline=BOT, ow=4)
        c.text(1400, 720, 'xK7pQm', 46, BOT, k * fd(T(0), 1.2), w='Bold', bg=CARD)
        c.check(1640, 720, 46, BOT, k * fd(T(0), 1.6), fd(T(0), 1.6))
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        x0, y0, x1, y1 = 360, 260, 1560, 820
        c.rr(x0, y0, x1, y1, 20, SKY, k1)
        for j, (hx, hw, hh, col) in enumerate(((420, 260, 300, (120, 90, 110)), (720, 220, 360, (90, 110, 140)), (1180, 300, 280, (130, 100, 80)))):
            c.rr(hx, 640 - hh, hx + hw, 640, 8, col, k1, bg=SKY)
            for q in range(4): c.rr(hx + 30 + (q % 2) * (hw / 2), 640 - hh + 40 + (q // 2) * 90, hx + 30 + (q % 2) * (hw / 2) + 50, 640 - hh + 100 + (q // 2) * 90, 4, YE, k1 * .8, bg=col)
        c.rr(x0, 640, x1, y1, 16, ROAD, k1, bg=SKY)
        for q in range(7): c.rr(820 + q * 50, 690, 850 + q * 50, 800, 4, INK, k1 * fd(T(1), .6), bg=ROAD)
        traffic_light(c, 1040, 470, 1.2, k1 * fd(T(1), .9))
        c.line([(1480, 640), (1480, 380), (1420, 380)], (170, 175, 190), 8, k1 * fd(T(1), 1.1), SKY)
        c.circ(1420, 392, 16, YE, k1 * fd(T(1), 1.1), bg=SKY)
        c.text(960, 860, 'crossings and street lights', 40, CY, k1 * fd(T(1), 1.4), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        grid(c, 700, 330, 168, k2, t, fd(T(2), .8, 2.4))
        cursor(c, 1280 - 120 * fd(T(2), .6, 2.0), 700 - 200 * fd(T(2), .6, 2.0), 1.1, k2)

def s_box(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, "2014: the tick box. I'm not a robot", 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Low risk: one tick. Not sure: a puzzle', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'The tick is a moment to check clues', 66, CLUE, hl(2), w='Bold')
    p = fd(T(0), 1.2, .5)
    if hl(1) < .01 or hl(2) > 0:
        tickbox(c, 960, 520, 1.0 if hl(0) > 0 else 0, p if hl(2) < .01 else 1.0, year='2014' if hl(2) < .01 else None)
        cursor(c, 720 + 60 * (1 - fd(T(0), .3, .8)), 550 + 60 * (1 - fd(T(0), .3, .8)), 1.0, hl(0) * (1 - hl(2)))
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        tickbox(c, 520, 330, k1, 1.0, s=.8, year='2014')
        c.arrow(520, 420, 300, 560, KNOWN, 8, k1 * fd(T(1), .3), 24)
        c.arrow(520, 420, 860, 560, YE, 8, k1 * fd(T(1), 1.2), 24)
        c.text(300, 610, 'low risk', 46, KNOWN, k1 * fd(T(1), .4), w='Bold'); c.check(300, 700, 56, KNOWN, k1 * fd(T(1), .6), fd(T(1), .6))
        c.text(300, 790, 'done', 44, INK, k1 * fd(T(1), .8), w='Bold')
        c.text(860, 610, 'not sure', 46, YE, k1 * fd(T(1), 1.3), w='Bold')
        grid(c, 1180, 400, 120, k1 * fd(T(1), 1.6), t, 0, head=True, ticks=False)
        c.arrow(990, 620, 1150, 560, YE, 6, k1 * fd(T(1), 1.6), 20)
    k2 = hl(2)
    if k2 > 0:
        clues = ((420, 320, 'cookies'), (1500, 320, 'browser history'), (420, 760, 'browser details'), (1500, 760, 'how you use the page'))
        for j, (x, y, lab) in enumerate(clues):
            kk = k2 * fd(T(2), .4 + j * .4)
            c.line([(960 + (x - 960) * .3, 520 + (y - 520) * .3), (x + (90 if x < 960 else -90), y)], CLUE, 4, kk * .7)
            if j == 0: cookie(c, x, y - 20, 62, kk)
            elif j == 1: browser(c, x, y - 20, 200, 140, kk, rows=3)
            elif j == 2:
                c.rr(x - 90, y - 80, x + 90, y + 30, 12, CARD, kk, outline=CLUE, ow=4)
                for q in range(3): c.rr(x - 60, y - 55 + q * 28, x + 20 + 30 * q, y - 43 + q * 28, 4, (90, 100, 150), kk, bg=CARD)
            else:
                c.circ(x, y - 25, 58, None, kk, outline=CLUE, ow=6); c.circ(x, y - 25, 22, CLUE, kk)
            c.text(x, y + 70, lab, 38, CLUE, kk, w='Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Quick question', 74, YE, 1 - hl(3), w='Bold')
    c.text(960, 240, 'When you tick the box, what does it lean on most?', 52, INK, hl(0) * (1 - hl(3)), w='Bold')
    ans = hl(3)
    c.text(960, 150, 'B: your browser and its history', 70, CLUE, ans * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'A VPN can earn you extra puzzles', 70, YE, hl(4), w='Bold')
    for j, (lab, x) in enumerate((('A  your mouse movement', 560), ('B  your browser and cookies', 1360))):
        a = hl(1) * fd(T(1), j * 1.3)
        if a <= .01: continue
        win = j == 1
        dim = 1 - .7 * ans if not win else 1.0
        y0, y1 = 330, 790
        c.rr(x - 340, y0, x + 340, y1, 30, CARD, a * dim, outline=CLUE if (win and ans > .5) else (70, 80, 130), ow=6 if win and ans > .5 else 3)
        c.text(x, 400, lab, 44, INK, a * dim, w='Bold', bg=CARD)
        if j == 0:
            c.rr(x - 70, 470, x + 70, 690, 70, (90, 100, 150), a * dim, bg=CARD)
            c.line([(x, 470), (x, 560)], CARD, 6, a * dim, (90, 100, 150))
            for q in range(5): c.circ(x - 250 + 40 * q, 740 - 25 * math.sin(q * .9 + t), 6, DIM, a * dim * .7, bg=CARD)
        else:
            browser(c, x - 80, 590, 300, 230, a * dim, rows=3, bg=CARD)
            cookie(c, x + 170, 650, 70, a * dim, bg=CARD)
        if ans > 0 and not win: c.cross(x, 600, 120, BOT, ans * .8)
        if ans > 0 and win: c.check(x - 270, 745, 50, CLUE, ans, fd(T(3), .3))
    if T(2) > 0 and ans < .99:
        p = clamp(T(2) / 1.6)
        n = 3 - min(2, int(T(2) / .55))
        c.circ(960, 560, 90, BG, (1 - ans))
        ring(c, 960, 560, 82, p, YE, (1 - ans))
        c.text(960, 560, str(n), 90, YE, (1 - ans), w='Bold')
    if hl(4) > 0:
        c.rr(660, 820, 1260, 870, 25, YE, hl(4)); c.text(960, 845, 'more risk -> more puzzles', 34, BG, hl(4), w='Bold', bg=YE)

def s_ai(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, '2024: researchers train an image AI on the grids', 58, BOT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'It solved 100% of the picture puzzles', 66, BOT, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'It needed about as many puzzles as people', 64, INK, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Newest version: usually no puzzle at all', 64, CLUE, hl(3), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        grid(c, 420, 340, 150, k, t, fd(T(0), 1.0, 2.0))
        robot(c, 1400, 520, 1.8, k)
        c.text(1400, 740, 'ETH Zurich study', 44, BOT, k * fd(T(0), .5), w='Bold')
        for q in range(4):
            u = (t * .7 + q * .25) % 1
            c.circ(lerp(1260, 920, u), 520 + 30 * math.sin(q), 8, BOT, k * hl(0) * (1 - abs(u - .5) * 2))
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        base = 800; H0 = 460
        for j, (lab, v, col, txt) in enumerate((('earlier attempts', .70, DIM, 'about 70%'), ('2024 AI', 1.0, BOT, '100%'))):
            x = 720 + j * 480; g = fd(T(1), .3 + j * .9, 1.0)
            c.rr(x - 120, base - H0 * v * g, x + 120, base, 14, col, k1 * fd(T(1), j * .9))
            c.text(x, base - H0 * v * g - 50, txt, 60, col, k1 * g, w='Bold')
            c.text(x, base + 50, lab, 40, INK, k1 * fd(T(1), j * .9), w='Bold')
        c.line([(520, base), (1400, base)], (90, 100, 150), 4, k1)
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        for j, (x, who) in enumerate(((620, 'people'), (1300, 'the AI'))):
            kk = k2 * fd(T(2), j * .7)
            if j == 0: person(c, x, 420, 1.6, HUMAN, kk)
            else: robot(c, x, 420, 1.5, kk)
            for q in range(3):
                grid(c, x - 150 + q * 100, 580, 28, kk * fd(T(2), .6 + q * .3 + j * .7), t, 0, head=False, ticks=False)
            c.text(x, 740, who, 44, HUMAN if j == 0 else BOT, kk, w='Bold')
        c.text(960, 630, '=', 110, YE, k2 * fd(T(2), 1.8), w='Bold')
        c.text(960, 840, 'puzzles needed: about the same', 40, YE, k2 * fd(T(2), 2.0), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        browser(c, 800, 520, 900, 560, k3, rows=6)
        widget(c, 1550, 520, 380, 160, k3 * (.5 + .3 * math.sin(t * 2)), dashed=True)
        c.text(1550, 520, 'no puzzle', 44, DIM, k3, w='Bold')
        sweep = (t * .5) % 1
        c.line([(360 + 880 * sweep, 290), (360 + 880 * sweep, 780)], CLUE, 4, k3 * .6, CARD)
        c.text(960, 850, 'it checks quietly in the background', 40, CLUE, k3 * fd(T(3), .8), w='Bold')

RECAPS = [('A computer tests you,', 'to tell humans from bots', HUMAN),
          ('Two-word tests helped', 'digitise books and papers', UNKNOWN),
          ('Today the box mostly', 'checks your browser clues', CLUE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 150, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    widget(c, 960, 540, 1300, 620, fd(T(0)) * out)
    for i, (l1, l2, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; y = 340 + i * 200
        if m <= .01: continue
        bx = 420
        c.rr(bx - 46, y - 46, bx + 46, y + 46, 12, (235, 238, 250), m, outline=(150, 160, 200), ow=4, bg=CARD)
        c.check(bx, y, 52, col, m, fd(T(i + 1), .3, .5))
        c.text(bx + 100, y - 30, l1, 50, col, m, anchor='lm', w='Bold', bg=CARD)
        c.text(bx + 100, y + 32, l2, 46, INK, m, anchor='lm', w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["For years, logging in might have meant helping to read old newspapers.",
            "Those wobbly words you typed? One came from a scanned page computers couldn't read.",
            "Now you mostly just tick a box. So how does it know you're human?",
            "It's not really about your click."], s_hook),
 ('1  ·  THE TEST', ["First, what is this test? It's called a captcha.",
            "The name was coined in 2003, by Luis von Ahn and colleagues at Carnegie Mellon.",
            "It stands for a Completely Automated Public Turing test to tell Computers and Humans Apart.",
            "Normally, a person tests a computer. Here, a computer tests you, to keep out spam bots.",
            "Early tests showed wobbly letters. People could read them. Programs mostly couldn't."], s_test),
 ('2  ·  TWO WORDS', ["In 2007, his team launched ree-captcha, with a twist.",
            "It showed two words. The computer knew one. That was the real test.",
            "The other came from a scanned page that software couldn't read. So it asked you.",
            "Like a quiz with one marked question, and one nobody can answer yet."], s_two),
 ('3  ·  TEAMWORK', ["Each answer was a vote. When enough people agreed, the word was accepted.",
            "That helped digitise the archive of The New York Times, and later, pages for Google Books.",
            "Google bought it in 2009. By 2010, it showed over a hundred million tests a day."], s_votes),
 ('4  ·  PICTURES', ["But computers got good at reading text. So the test changed.",
            "From 2012, it started using photos from Google Street View.",
            "Later came the grid you know. Select every square with a traffic light."], s_photos),
 ('5  ·  THE TICK BOX', ["In 2014, Google launched the tick box. I'm not a robot.",
            "Judged low risk? One tick is enough. If it isn't sure, you get a picture puzzle.",
            "So the tick is mostly a moment to check clues already there."], s_box),
 ('6  ·  QUICK QUESTION', ["Quick question. When you tick that box, what does it lean on most?",
            "A, the way you move your mouse. Or B, your browser and its history, like cookies.",
            "Three, two, one.",
            "B. A 2024 study found it relies heavily on cookies and browser history. Mouse movement seems to matter less."], s_quiz),
 ('7  ·  THE AI TWIST', ["Here's the twist. In that study, researchers at E T H Zurich trained an image AI on these grids.",
            "It solved one hundred percent of the picture puzzles. Earlier attempts managed around seventy percent.",
            "And it needed about as many puzzles as real people did.",
            "So the newest version usually shows no puzzle at all. It just checks quietly in the background."], s_ai),
 ('RECAP', ["So remember three things.",
            "One. A captcha is a test a computer gives you, to tell humans from bots.",
            "Two. Those two-word tests helped digitise books and newspapers.",
            "Three. Today the tick box mostly checks your browser, because AI can solve the picture puzzles.",
            "If you learned something, subscribe to Short Story Long Thinking."], s_recap),
]

def remap(fn, mp):
    """Reuse a long-video scene with a different line order: mp maps the scene's line index -> narration line index."""
    def g(c, T, t):
        def T2(i, off=0.0):
            if i not in mp: return -99
            j, o = mp[i] if isinstance(mp[i], tuple) else (mp[i], 0.0)
            return T(j, off + o)
        fn(c, T2, t)
    return g

def short_hook(c, T, t):
    if T(1) < 0: remap(s_box, {0: 0})(c, T, t)
    else: remap(s_box, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

def short_clues(c, T, t):
    if T(1) < 0: remap(s_quiz, {0: (0, -9), 1: (0, -9), 2: (0, -9), 3: 0})(c, T, t)
    else: remap(s_quiz, {0: (1, -9), 1: (1, -9), 2: (1, -9), 3: (1, -9), 4: 1})(c, T, t)

def short_ai(c, T, t):
    if T(1) < 0: remap(s_ai, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_ai, {0: (1, -9), 1: (1, -9), 2: (1, -9), 3: 1})(c, T, t)

# The Short: its own complete mini-story (hook -> what the box really checks -> why puzzles are a backup -> answer).
SHORT_SCENES = [
 ('THE HOOK', ["When you tick I'm not a robot, what is it actually checking?",
               "Mostly not your click. It's checking clues that are already sitting in your browser."],
              short_hook),
 ('THE CLUES', ["A 2024 study found it relies heavily on cookies and your browser history, things you never see.",
                "Hidden connections, like a VPN, get rated as riskier. That can mean extra puzzles."],
               short_clues),
 ('THE BACKUP', ["The picture puzzles are only a backup, for when it isn't sure. And those researchers built an AI that solved one hundred percent of them.",
                 "So the newest version usually shows no puzzle at all."],
                short_ai),
 ('THE ANSWER', ["So what does that box check?",
                 "Mostly your browser and its history. Not the click itself."],
                card('What does the box check?', 'Your browser, not your click.')),
]
SHORT_HITS = [(3, 1, 0.0)]
