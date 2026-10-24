"""Episode: Your Memory Has a Weak Spot: The Middle of a List (the serial position effect)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "The Middle Goes Missing"                 # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                       # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why do we forget the middle?"             # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 3, 0.0), (6, 3, 0.0)]           # title card, quiz answer, Asch reveal
THUMB = ['FIRST: REMEMBERED.', 'LAST: REMEMBERED.', 'MIDDLE: GONE.']
MUSIC_LEVEL = 0.006                                      # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                           # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.6, (4, 3): 0.6, (6, 3): 0.5}
SHORT_PAUSES = {(0, 2): 0.3}
CAPTION_FIXES = {'fifteen words': '15 words', 'over a hundred': '100+', 'ten to forty': '10 to 40',
                 'thirty seconds': '30 seconds', 'word ten': 'word 10'}

WORDS = ['CAT', 'DOOR', 'MILK', 'TREE', 'BOOK', 'SHOE', 'RAIN', 'LAMP', 'FISH', 'COIN', 'BELL', 'SALT', 'ROPE', 'CUP', 'STAR']
N = len(WORDS)
GREY = (70, 78, 120)

def p_u(i):        # illustrative U-shaped recall curve
    return .33 + .45 * math.exp(-i / 1.8) + .55 * math.exp(-(N - 1 - i) / 1.5)
def p_delay(i):    # illustrative: after 30 s of counting the end advantage is gone
    return .33 + .45 * math.exp(-i / 1.8)
def p_slow(i):     # illustrative: slower reading lifts start and middle, end barely changes
    return p_u(i) + .14 * clamp((12 - i) / 12)

# ---------------------------------------------------------------- drawing helpers
def tile(c, x, y, word, col=CY, a=1.0, w=98, h=70, size=27, bg=BG, fill=CARD):
    if a <= .01: return
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 14, fill, a, outline=col, ow=3, bg=bg)
    c.text(x, y, word, size, col, a, w='Bold', bg=fill)

def tx(i): return 180 + i * 111

def bars(c, fn, x0=360, step=86, base=740, hmax=400, a=1.0, col=CY, grow=1.0, labels=True, colf=None, outline_only=False):
    for i in range(N):
        h = hmax * fn(i) * ease(clamp(grow * 1.6 - i * .04))
        cc = colf(i) if colf else col
        x = x0 + i * step
        if outline_only:
            c.rr(x - 28, base - h, x + 28, base, 10, None, a, outline=cc, ow=3)
        elif h > 2:
            c.rr(x - 28, base - h, x + 28, base, 10, cc, a)
        if labels: c.text(x, base + 34, WORDS[i], 21, DIM, a, w='Bold')
    c.line([(x0 - 50, base), (x0 + (N - 1) * step + 50, base)], DIM, 3, a)

def curve(c, fn, x0=360, step=86, base=740, hmax=400, col=YE, a=1.0, p=1.0, w=6):
    pts = []
    m = int(140 * clamp(p))
    for k in range(m + 1):
        u = k / 140 * (N - 1); i0 = int(u); i1 = min(N - 1, i0 + 1); f = u - i0
        v = fn(i0) * (1 - f) + fn(i1) * f
        pts.append((x0 + u * step, base - hmax * v))
    c.line(pts, col, w, a)

def head(c, x, y, r, col=INK, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, col, a, bg=bg)
    c.rr(x - r * .55, y + r * .7, x + r * .55, y + r * 1.25, r * .2, col, a, bg=bg)
    c.rr(x - r * 1.1, y + r * 1.1, x + r * 1.1, y + r * 1.9, r * .5, col, a, bg=bg)
    c.circ(x + r * .35, y - r * .1, r * .1, BG, a, bg=col)

def bubble(c, x0, y0, x1, y1, a=1.0, col=CARD, tailx=None, taily=None):
    if a <= .01: return
    c.rr(x0, y0, x1, y1, 40, col, a, outline=(70, 84, 140), ow=3)
    if tailx is not None:
        for k, r in enumerate((26, 18, 11)):
            c.circ(tailx - k * 40, taily + k * 34, r, col, a, outline=(70, 84, 140), ow=3)

def echo(c, x, y, t, col=YE, a=1.0, rmax=360):
    for k in range(4):
        ph = ((t * .45 + k / 4) % 1.0)
        c.circ(x, y, 60 + ph * rmax, None, a * (1 - ph) * .7, outline=col, ow=4)

def loop_icon(c, x, y, r, t, col=CY, a=1.0, bg=CARD):
    if a <= .01: return
    pts = [(x + r * math.cos(u / 40 * 5.2 + t * 2), y + r * math.sin(u / 40 * 5.2 + t * 2)) for u in range(41)]
    c.line(pts, col, max(4, r * .16), a, bg)
    ex, ey = pts[-1]; ang = 5.2 + t * 2 + math.pi / 2
    for da in (2.5, -2.5):
        c.line([(ex, ey), (ex + r * .45 * math.cos(ang + da), ey + r * .45 * math.sin(ang + da))], col, max(4, r * .16), a, bg)

def face(c, x, y, r, mood, col, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, col, a, bg=bg)
    for sx in (-.35, .35): c.circ(x + r * sx, y - r * .2, r * .11, BG, a, bg=col)
    pts = [(x + r * .5 * (u / 10 - 1), y + r * .3 + mood * r * .25 * (1 - (u / 10 - 1) ** 2)) for u in range(21)]
    c.line(pts, BG, max(3, r * .1), a, col)

def remap(fn, mp):
    """Reuse a long-video scene with a different line order: mp maps the scene's line index -> narration line index."""
    def g(c, T, t):
        def T2(i, off=0.0):
            return T(mp[i], off) if i in mp else -99
        fn(c, T2, t)
    return g

def thumb_art(c):
    for i, w in enumerate(['CAT', 'DOOR', 'MILK', 'TREE', 'BOOK', 'STAR']):
        y = 150 + i * 135
        mid = 2 <= i <= 3
        col = GREY if mid else GR
        tile(c, 1500, y, '?' if mid else w, col, .45 if mid else 1, w=300, h=104, size=56)
    c.check(1720, 150, 80, GR); c.check(1720, 825, 80, GR)
    c.cross(1720, 420, 90, PK); c.cross(1720, 555, 90, PK)

# ---------------------------------------------------------------- scenes
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 1.0, .5)
    if a > 0:
        # motion from frame one: the words land one by one with the hook text already on screen
        c.text(960, 170, '15 words. Which ones stick?', 70, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 170, 'First few. Last few.', 70, GR, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 170, 'The middle? Mostly gone.', 70, PK, a * hl(2), w='Bold')
        for i, wd in enumerate(WORDS):
            k = fd(t, i * .18, .3)
            end = i < 3 or i > N - 4
            gone = hl(2) * (0 if end else 1)
            col = GR if (end and hl(1) > .3) else CY
            if gone > .5: col = GREY
            y = 440 + 8 * math.sin(t * 2 + i) + 40 * (1 - k) + 50 * gone
            tile(c, tx(i), y, wd if gone < .5 else '?', col, a * k * (1 - .55 * gone))
        if hl(1) > 0:
            for i in list(range(3)) + list(range(N - 3, N)):
                c.check(tx(i), 560, 44, GR, a * hl(1), fd(T(1), .3 + (i % 3) * .2, .4))
        if hl(3) > 0:
            c.text(960, 720, '2 experiments from the 1960s explain why', 48, YE, a * hl(3), w='Bold')
    if T(3) > 1.0:
        m = fd(T(3), 1.3, .7)
        c.text(960, 330 + 30 * (1 - m), 'The Middle', 128, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'Goes Missing', 128, YE, m, w='Bold')
        c.line([(960 - 340 * m, 590), (960 + 340 * m, 590)], CY, 8, m)
        c.text(960, 680, 'Why your memory has a weak spot', 46, DIM, fd(T(3), 1.9), w='Medium')

SHOP = ['eggs', 'bread', 'milk', 'rice', 'apples', 'soap', 'tea', 'onions', 'butter']
def s_curve(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'The serial position effect', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 140, 'High start. Dip. High end.', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 140, '1962: 103 students, lists of 10 to 40 words', 54, CY, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 140, 'Your shopping list, too', 64, PK, hl(3), w='Bold')
    k = hl(0) * (1 - hl(3))
    if k > 0:
        g = clamp(T(1) / 2.5) if T(1) > 0 else 0.0
        colf = lambda i: GR if (i < 3 or i > N - 4) else (90, 110, 170)
        bars(c, p_u, a=k, grow=g if T(1) > 0 else 0.0, colf=colf)
        if g <= 0:
            for i in range(N):
                c.text(360 + i * 86, 700, '?', 40, DIM, k * (.5 + .5 * math.sin(t * 3 + i)), w='Bold')
        curve(c, p_u, a=k * hl(1), p=clamp((T(1) - 1.2) / 2.0) if T(1) > 0 else 0)
        k2l = k * (1 - hl(2))
        c.text(470, 310, 'START', 34, GR, k2l * fd(T(1), 2.4), w='Bold')
        c.text(960, 530, 'MIDDLE', 34, PK, k2l * fd(T(1), 3.2), w='Bold')
        c.text(1460, 290, 'END', 34, GR, k2l * fd(T(1), 4.0), w='Bold')
        c.text(1840, 850, 'Illustrative shape', 26, DIM, k, 'rm', 'Medium')
        if hl(2) > 0:
            for j, (lab, n) in enumerate((('10 words', 10), ('20 words', 20), ('40 words', 40))):
                x = 560 + j * 400; kk = hl(2) * fd(T(2), .4 + j * .5)
                c.rr(x - 150, 200, x + 150, 290, 20, CARD, kk, outline=CY, ow=3)
                pts = []
                for u in range(31):
                    i = u / 30 * (n - 1)
                    v = .3 + .4 * math.exp(-i / 1.8) + .5 * math.exp(-(n - 1 - i) / 2.5)
                    pts.append((x - 120 + u * 8, 282 - 50 * v))
                c.line(pts, YE, 4, kk, CARD)
                c.text(x, 222, lab, 22, DIM, kk, w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        c.rr(660, 230, 1260, 850, 24, (235, 232, 220), k3)
        c.text(960, 285, 'SHOPPING LIST', 34, BG, k3, w='Bold', bg=(235, 232, 220))
        for i, it in enumerate(SHOP):
            y = 350 + i * 56; mid = 3 <= i <= 6
            fade = fd(T(3), 1.0 + (i - 3) * .3, .6) if mid else 0
            col = mix(BG, 1 - .7 * fade, (235, 232, 220))
            c.text(740, y, '- ' + it, 36, BG, k3 * (1 - .75 * fade), 'lm', 'Bold', bg=(235, 232, 220))
            if mid and fade > .5:
                c.text(1080, y, '?', 40, PK, k3 * fade, w='Bold', bg=(235, 232, 220))
            elif not mid:
                c.check(1100, y, 34, GR, k3, fd(T(3), .5 + i * .1, .3))

def s_start(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'Why is the start strong?', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 140, 'Full attention: you repeat it', 64, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 140, 'By word 10: juggling a pile', 64, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 140, 'Early words get the most repeats', 64, GR, hl(3), w='Bold')
    k = max(hl(0), hl(1)) * (1 - hl(3))
    if k > 0:
        head(c, 400, 470, 120, (90, 110, 170), k)
        bubble(c, 700, 240, 1760, 720, k * hl(1), tailx=640, taily=420)
        if hl(1) == 0:
            tile(c, 1230, 480, 'CAT', GR, k * (.7 + .3 * math.sin(t * 4)), w=200, h=110, size=54)
        k1 = hl(1) * (1 - hl(2))
        if k1 > 0:
            reps = int(clamp(T(1) / 3.6) * 6) + 1
            for j in range(reps):
                tile(c, 860 + j * 150, 480 + 20 * math.sin(t * 3 + j), 'CAT', GR, k1 * fd(T(1), j * .6, .3), w=130, h=84, size=36)
            c.text(1230, 640, 'x' + str(reps), 44, GR, k1, w='Bold', bg=CARD)
        k2 = hl(2)
        if k2 > 0:
            shown = 10
            for j in range(shown):
                x = 830 + (j % 5) * 205; y = 360 + (j // 5) * 150 + 10 * math.sin(t * 3 + j * 1.3)
                newest = (j == shown - 1)
                col = YE if newest else CY
                flash = (.5 + .5 * math.sin(t * 9)) if newest else 1.0
                tile(c, x, y, WORDS[j], col, k2 * fd(T(2), j * .12, .3) * (flash if newest else .8), w=170, h=90, size=40)
            c.text(1230, 650, 'each new word: a quick look', 38, YE, k2 * fd(T(2), 1.5), w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        r = lambda i: 1.3 + 3.4 * math.exp(-i / 2.5)
        bars(c, lambda i: r(i) / 5.0, a=k3, grow=clamp(T(3) / 2.2), colf=lambda i: GR if i < 3 else (CY if i < N - 3 else YE))
        c.text(480, 290, '4 to 5 repeats', 38, GR, k3 * fd(T(3), 1.6), w='Bold')
        c.text(1440, 560, '1 to 2', 38, YE, k3 * fd(T(3), 2.4), w='Bold')
        c.text(960, 230, 'Rundus, 1971: people rehearsed out loud', 36, DIM, k3 * fd(T(3), .6), w='Medium')
        c.text(1840, 850, 'Illustrative bars', 26, DIM, k3, 'rm', 'Medium')

def s_end(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'Why is the end strong?', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 140, 'Still in short-term memory', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 140, 'Say it now: easy. Wait: it slips.', 64, PK, hl(2), w='Bold')
    k = hl(0) * (1 - hl(2))
    if k > 0:
        if hl(1) == 0:
            for i, wd in enumerate(WORDS):
                end = i > N - 4
                tile(c, tx(i), 470 + 6 * math.sin(t * 2 + i), wd, YE if end else GREY, k * (1 if end else .5))
        k1 = hl(1)
        if k1 > 0:
            echo(c, 960, 480, t, YE, k1, rmax=230)
            c.rr(560, 330, 1360, 630, 40, CARD, k1, outline=YE, ow=5)
            c.text(960, 380, 'SHORT-TERM MEMORY', 32, DIM, k1, w='Bold', bg=CARD)
            for j, wd in enumerate(WORDS[-4:]):
                tile(c, 690 + j * 180, 500, wd, YE, k1 * fd(T(1), .4 + j * .25), w=150, h=90, size=40, bg=CARD)
            c.text(960, 720, 'like an echo', 44, YE, k1 * fd(T(1), 1.6), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        dig = ['7', '3', '9', '5']
        fade = fd(T(2), 4.0, 1.6)
        for j, d in enumerate(dig):
            x = 600 + j * 240 + 12 * fade * math.sin(t * 7 + j)
            col = GR if fade < .5 else PK
            c.rr(x - 90, 300, x + 90, 520, 30, CARD, k2 * fd(T(2), j * .25), outline=col, ow=4)
            c.text(x, 410, d, 130, col, k2 * fd(T(2), j * .25) * (1 - .75 * fade), w='Bold', bg=CARD)
        c.text(960, 640, 'right away: easy', 48, GR, k2 * fd(T(2), 1.2) * (1 - fade), w='Bold')
        c.text(960, 640, 'a little later: slipping away', 48, PK, k2 * fade, w='Bold')
        clock_r = 50
        c.circ(1640, 410, clock_r, None, k2 * fade, outline=PK, ow=6)
        ang = t * 3
        c.line([(1640, 410), (1640 + 36 * math.sin(ang), 410 - 36 * math.cos(ang))], PK, 6, k2 * fade)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3); slow = hl(4)
    proof = T(1) < -50 and T(2) < -50          # the Short reuses this scene without the A/B choice
    c.text(960, 120, 'The proof' if proof else 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 195, '1966: count out loud for 30 s, then recall', 44, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 140, ('The last words lost their edge' if proof else 'B: the last words lost their edge'), 60, GR, ans * (1 - slow), w='Bold')
    c.text(960, 140, 'Read slowly: start and middle gain', 58, CY, slow, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        n = 1 + int(clamp(T(0) / 6.0) * 29)
        c.circ(960, 520, 170, CARD, k0, outline=YE, ow=6)
        c.text(960, 510, str(n), 150, YE, k0, w='Bold', bg=CARD)
        c.text(960, 610, 'counting...', 34, DIM, k0, w='Bold', bg=CARD)
        ring(c, 960, 520, 200, n / 30, YE, k0, 8)
    kc = hl(1) * (1 - ans)
    if kc > 0 or (hl(1) > 0 and ans < 1):
        for j, (lab, l1, idx, x) in enumerate((('A', 'the first words', range(3), 560), ('B', 'the last words', range(N - 3, N), 1360))):
            kk = hl(1) * (.3 + .7 * fd(T(1), j * 1.6)) * (1 - ans)
            c.rr(x - 300, 290, x + 300, 720, 34, CARD, kk, outline=CY, ow=3)
            c.circ(x - 230, 350, 42, CY, kk, bg=CARD); c.text(x - 230, 350, lab, 48, BG, kk, w='Bold', bg=CY)
            for q, i in enumerate(idx):
                tile(c, x - 150 + q * 150, 500, WORDS[i], CY, kk, w=130, h=84, size=34, bg=CARD)
            c.text(x, 640, l1, 42, INK, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 500, 70, 1 - p, YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        g = clamp(T(3) / 2.0)
        fn = (lambda i: p_u(i) * (1 - g) + p_delay(i) * g)
        if slow > 0:
            bars(c, p_u, a=ans * .5, grow=1, col=GREY, outline_only=True)
            gs = clamp(T(4) / 2.0)
            bars(c, lambda i: p_u(i) * (1 - gs) + p_slow(i) * gs, a=slow, grow=1,
                 colf=lambda i: CY if i < N - 3 else YE)
            c.text(1500, 260, 'end: barely changes', 34, YE, slow * fd(T(4), 1.6), w='Bold')
        else:
            bars(c, p_u, a=ans * .6, grow=1, col=GREY, outline_only=True)
            bars(c, fn, a=ans, grow=1, colf=lambda i: GR if i < 3 else (PK if i > N - 4 else (90, 110, 170)))
            c.text(1450, 330, 'end advantage: gone', 36, PK, ans * fd(T(3), 1.6), w='Bold')
            c.text(500, 330, 'start: stays', 36, GR, ans * fd(T(3), 2.4), w='Bold')
        c.text(1840, 850, 'Illustrative shape (Glanzer & Cunitz, 1966)', 26, DIM, ans, 'rm', 'Medium')

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def s_sofar(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'So far', 70, CY, hl(0), w='Bold')
    c.text(960, 220, 'Strong start and strong end, for different reasons', 40, DIM, hl(0), w='Medium')
    items = [('THE START', 'practised into longer-lasting memory', CY, 1), ('THE END', 'still fresh in short-term memory', YE, 2)]
    for j, (lab, txt, col, li) in enumerate(items):
        kk = hl(li)
        y = 400 + j * 210
        c.rr(260, y - 85, 1660, y + 85, 34, CARD, kk, outline=col, ow=4)
        if j == 0: loop_icon(c, 380, y, 46, t, col, kk)
        else: echo(c, 380, y, t, col, kk * .8, rmax=40); c.circ(380, y, 20, col, kk, bg=CARD)
        c.text(480, y - 30, lab, 40, col, kk, 'lm', 'Bold', bg=CARD)
        c.text(480, y + 28, txt, 40, INK, kk, 'lm', 'Bold', bg=CARD)
    c.text(960, 800, 'Researchers still debate the fine details. The pattern itself is very well established.', 30, DIM, fd(T(2), 2.6), w='Medium')

TRAITS = ['intelligent', 'industrious', 'impulsive', 'critical', 'stubborn', 'envious']
def s_asch(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'Order matters for people, too', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 140, '1946: Solomon Asch, six traits', 64, CY, hl(1) * (1 - hl(3)), w='Bold')
    c.text(960, 140, 'Same words. Different order.', 64, YE, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        head(c, 960, 430, 110, (90, 110, 170), k0)
        c.text(960, 330, '?', 90, YE, k0 * (.6 + .4 * math.sin(t * 4)), w='Bold')
    for j, (order, x, li) in enumerate(((TRAITS, 560, 1), (TRAITS[::-1], 1360, 2))):
        kk = hl(li)
        if kk <= 0: continue
        c.rr(x - 270, 220, x + 270, 680, 30, CARD, kk, outline=CY, ow=3)
        c.text(x, 265, 'Group ' + 'AB'[j], 32, DIM, kk, w='Bold', bg=CARD)
        for q, tr in enumerate(order):
            good = tr in ('intelligent', 'industrious')
            col = GR if good else (PK if tr in ('stubborn', 'envious') else YE)
            c.text(x, 330 + q * 58, tr, 40, col, kk * fd(T(li), q * .25, .3), w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        face(c, 420, 770, 55, 1, GR, k3 * fd(T(3), .4))
        c.text(500, 770, 'judged more kindly', 38, GR, k3 * fd(T(3), .8), 'lm', 'Bold')
        face(c, 1220, 770, 55, -1, PK, k3 * fd(T(3), 1.2))
        c.text(1300, 770, 'judged less kindly', 38, PK, k3 * fd(T(3), 1.6), 'lm', 'Bold')

TIPS = [('1', 'Put what matters first or last', GR), ('2', 'Review the middle first next time', CY), ('3', 'Long list? Write it down', YE)]
def s_tips(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'How to use it', 70, INK, hl(0), w='Bold')
    for i, (nn, lab, col) in enumerate(TIPS):
        kk = hl(i + 1); y = 320 + i * 175; up = 20 * (1 - kk)
        c.rr(330, y - 70 + up, 1590, y + 70 + up, 34, CARD, kk, outline=col, ow=4)
        c.circ(420, y + up, 42, col, kk, bg=CARD); c.text(420, y + up, nn, 48, BG, kk, w='Bold', bg=col)
        c.text(500, y + up, lab, 50, INK, kk, 'lm', 'Bold', bg=CARD)

RECAPS = [('1', 'Start and end stick. The middle slips', YE), ('2', 'Start: most practice. End: still fresh', CY), ('3', 'Put it first or last; review the middle', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 520 + up
        if i == 0:
            pts = [(x - 160 + u * 16, y - 70 + 140 * (1 - (abs(u - 10) / 10) ** 2) * .8) for u in range(21)]
            c.line(pts, YE, 8, m, CARD)
        elif i == 1:
            loop_icon(c, x - 80, y, 50, t, CY, m)
            c.circ(x + 90, y, 22, YE, m, bg=CARD); echo(c, x + 90, y, t, YE, m * .7, rmax=50)
        else:
            for q in range(5):
                cc = GR if q in (0, 4) else GREY
                tile(c, x - 180 + q * 90, y, '', cc, m, w=70, h=70, bg=CARD)
        ls = wrap(c, lab, 32, 470, 'Bold')
        for j, l in enumerate(ls): c.text(x, 700 + up + j * 42 - (len(ls) - 1) * 21, l, 32, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Someone reads you fifteen words, and you try to say them back.",
            "You'll probably get the first few. And the last few.",
            "The middle? Mostly gone.",
            "Two experiments from the 1960s explain why. And you can use it."], s_hook),
 ('1  ·  THE U SHAPE', ["Psychologists call this the serial position effect.",
            "Mark which words people remember, and you get a U shape: high at the start, high at the end, and a dip in the middle.",
            "In 1962, Bennet Murdock tested over a hundred students with lists of ten to forty words. Short lists or long, the U appeared.",
            "It's why, when you try to remember a shopping list, the middle items are the ones that slip."], s_curve),
 ('2  ·  THE START', ["So why is the start strong?",
            "When the first word arrives, it gets your full attention. You repeat it in your head.",
            "By word ten, you're juggling a pile, and each new word gets a quick look.",
            "In 1971, a study had people rehearse out loud. Early words got about four or five repeats. Late words, one or two."], s_start),
 ('3  ·  THE END', ["And why is the end strong?",
            "The last words are still sitting in your short-term memory, like an echo.",
            "Like a number someone just read out. Say it right away: easy. Wait, and it slips."], s_end),
 ('4  ·  QUICK QUESTION', ["Quick question. In 1966, researchers had people count out loud for thirty seconds before recalling.",
            "Which words lost their advantage? A, the first words. Or B, the last words.",
            "Three, two, one.",
            "B. The last words. Thirty seconds of counting wiped out their edge. The first words held on.",
            "And reading the words more slowly helped the start and middle, but barely the end."], s_quiz),
 ('5  ·  SO FAR', ["So far: the start and the end are strong for different reasons.",
            "The first words got practised into longer-lasting memory.",
            "The last words are simply still fresh. Researchers still debate the details, but the pattern is solid."], s_sofar),
 ('6  ·  FIRST IMPRESSIONS', ["Order matters beyond word lists, too.",
            "In 1946, Solomon Asch described a person with six traits: intelligent, industrious, impulsive, critical, stubborn, envious.",
            "Another group heard them in reverse order.",
            "When the good traits came first, people judged the person more kindly. Same words. Different order."], s_asch),
 ('7  ·  USE IT', ["So how can you use this?",
            "Put what matters at the start or the end of a talk, a message, or a study session.",
            "When you review, start with the middle, because it got the least practice.",
            "And for a long shopping list? Just write it down."], s_tips),
 ('RECAP', ["So remember three things.",
            "One. We remember the start and end of a list, and lose the middle.",
            "Two. The start gets the most practice. The end is still fresh.",
            "Three. Put what matters first or last, and review the middle.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story; the answer (start = practice, end = still fresh) lands by about 20 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["Someone reads you fifteen words.",
                 "You'll remember the first few, and the last few.",
                 "The middle mostly vanishes. Here's why."], s_hook),
 ('THE START', ["The first word gets your full attention, so you repeat it in your head.",
                "By word ten, you're juggling a pile.",
                "So early words get the most practice, and they stick."], remap(s_start, {1: 0, 2: 1, 3: 2})),
 ('THE END', ["The last words are still in your short-term memory, like an echo."], remap(s_end, {0: 0, 1: 0})),
 ('THE PROOF', ["Proof: in 1966, people counted out loud for thirty seconds before recalling.",
                "The last words lost their edge. The first words held on."], remap(s_quiz, {0: 0, 3: 1})),
 ('THE ANSWER', ["So the start sticks because it's practised. The end sticks because it's fresh.",
                 "The middle gets neither.",
                 "So put what matters first or last. Follow for more."],
                card('Start: practised. End: fresh.', 'The middle gets neither.', 'Put it first or last.')),
]
SHORT_HITS = [(4, 1, 0.0)]
