"""Episode: That Stomach Growl? Your Gut Is Cleaning House (borborygmi, muscle waves, muffling, the migrating motor complex)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Your Stomach Growls'                      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.88                            # lesson of 2026-11-25: speech measured 164 wpm at 0.94; 0.88 brings it into 140-155
SHORT_HOOK = 'Why does your stomach growl?'                  # headline on the vertical Short
HITS = [(0, 1, 0.0), (5, 0, 0.0), (8, 1, 0.0)]               # "cleaning house", "It's B", the answer
THUMB = ['GROWL =', 'CLEAN-UP']
THUMB_COLS = [YE, GR]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.6, (4, 0): 3.4, (8, 0): 0.5}
SHORT_PAUSES = {(0, 0): 0.4}
QZ = 10.4                                                    # length of the quiz line (set from tl.json after audio)
CAPTION_FIXES = {'forty-five to sixty minutes': '45 to 60 minutes', 'five to fifteen minutes': '5 to 15 minutes',
                 'one to two hours': '1 to 2 hours', 'ten minutes': '10 minutes'}
CAPTION_FIXES = dict(sorted(CAPTION_FIXES.items(), key=lambda kv: -len(kv[0])))

# Colour code kept in every scene:
# muscle squeeze pink, gas bubbles cyan, food orange, the cleaning wave green, sound yellow, the hormone purple.
MUS = PK; GAS = CY; FOOD = (245, 150, 70); CLEAN = GR; SND = YE; HORM = PU
WALL = (120, 62, 88); LUMEN = (48, 26, 44); SKIN = (60, 70, 120); QUIZ = (46, 28, 74); DARK = (20, 22, 38)
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
def resample(pts, step=7):
    """Points every `step` px along a polyline, with their arc length."""
    out = [(pts[0][0], pts[0][1], 0.0)]; s = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.dist((x0, y0), (x1, y1)); n = max(1, int(d / step))
        for k in range(1, n + 1):
            q = k / n; s += d / n; out.append((x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, s))
    return out

def at(rs, s):
    """(x, y) at arc length s along resampled points."""
    s = clamp(s, 0, rs[-1][2])
    for x, y, d in rs:
        if d >= s: return x, y
    return rs[-1][0], rs[-1][1]

def tube(c, rs, r, a, squeeze=None, sw=55, depth=.5, fill=LUMEN, bg=BG):
    """A soft gut tube along resampled points; an optional pink ring of muscle squeezes it at arc length `squeeze`."""
    if a <= .01: return
    def rad(d):
        g = math.exp(-((d - squeeze) / sw) ** 2) if squeeze is not None else 0
        return r * (1 - depth * g), g
    for x, y, d in rs:
        rr, g = rad(d); c.circ(x, y, rr, mix(MUS, g, WALL), a, bg=bg)
    for x, y, d in rs:
        rr, g = rad(d); c.circ(x, y, rr * .6, fill, a, bg=mix(MUS, g, WALL))

def bubbles(c, rs, a, s0, s1, r, n=6, seed=1, col=GAS, bg=LUMEN, t=0.0):
    if a <= .01: return
    rng = random.Random(seed)
    for k in range(n):
        s = s0 + (s1 - s0) * (k + .5) / n
        x, y = at(rs, s); dy = rng.uniform(-.25, .25) * r + 3 * math.sin(t * 4 + k)
        c.circ(x, y + dy, r * rng.uniform(.22, .32), col, a, bg=bg)

def arcs(c, x, y, a, t, col=SND, n=3, r0=50, gap=38, side=1, spread=.75, bg=BG, w=7):
    """Pulsing sound arcs to the right (side=1) or left (side=-1) of a point."""
    if a <= .01: return
    for k in range(n):
        ph = (t * 1.6 + k / n) % 1.0; rr = r0 + gap * k + 18 * ph
        base = 0 if side > 0 else math.pi
        pts = [(x + rr * math.cos(base + u), y + rr * math.sin(base + u)) for u in [spread * (j / 10 - .5) * 2 for j in range(11)]]
        c.line(pts, col, w, a * (1 - .55 * ph), bg=bg)

def stomach(c, x, y, s, a, col=WALL, inner=LUMEN, bg=BG, glow=0.0):
    """A simple J-shaped stomach made of overlapping circles (not anatomical detail)."""
    if a <= .01: return
    blobs = ((-30, -70, 46), (-10, -10, 70), (30, 40, 66), (80, 70, 48), (128, 64, 34))
    for dx, dy, r in blobs: c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)
    for dx, dy, r in blobs: c.circ(x + dx * s, y + dy * s, r * s * .62, inner, a, bg=col)
    if glow > .01:
        for dx, dy, r in blobs[1:3]: c.circ(x + dx * s, y + dy * s, r * s * .3, CLEAN, a * glow, bg=inner)

def person(c, x, y, s, a, bg=BG):
    """A generic seated-height figure: head and body, belly area left open for the stomach."""
    if a <= .01: return
    c.circ(x, y - 250 * s, 70 * s, SKIN, a, bg=bg)
    c.rr(x - 140 * s, y - 165 * s, x + 140 * s, y + 230 * s, 70 * s, SKIN, a, bg=bg)

def clock(c, x, y, r, a, frac, col=INK, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, CARD, a, outline=col, ow=6, bg=bg)
    for k in range(12):
        ang = 6.283 * k / 12; c.circ(x + r * .8 * math.cos(ang), y + r * .8 * math.sin(ang), 4, DIM, a, bg=CARD)
    ang = -1.571 + 6.283 * frac
    c.line([(x, y), (x + r * .7 * math.cos(ang), y + r * .7 * math.sin(ang))], col, 7, a, bg=CARD)
    c.line([(x, y), (x, y - r * .45)], DIM, 7, a, bg=CARD); c.circ(x, y, 8, col, a, bg=CARD)

def apple(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.circ(x - 26 * s, y, 56 * s, (220, 70, 80), a, bg=bg); c.circ(x + 26 * s, y, 56 * s, (220, 70, 80), a, bg=bg)
    c.line([(x, y - 50 * s), (x + 8 * s, y - 86 * s)], (130, 90, 60), 8 * s, a, bg=bg)
    c.circ(x + 30 * s, y - 80 * s, 18 * s, GR, a, bg=bg)

def switch(c, x, y, a, on, bg=BG):
    """A toggle: knob right and green when on, left and grey when off."""
    if a <= .01: return
    col = mix(CLEAN, on, (80, 86, 120))
    c.rr(x - 120, y - 56, x + 120, y + 56, 56, col, a, bg=bg)
    kx = x - 64 + 128 * on
    c.circ(kx, y, 44, INK, a, bg=col)
    c.text(x, y + 100, 'ON' if on > .5 else 'OFF', 40, CLEAN if on > .5 else DIM, a, w='Bold', bg=bg)

def debris(c, rs, a, wave_s, seed=4, n=14, s0=0, bg=LUMEN, r=11):
    """Crumbs (orange), mucus (cyan) and bacteria (purple) that the green wave pushes ahead of itself."""
    if a <= .01: return
    rng = random.Random(seed); L = rs[-1][2]
    for k in range(n):
        s = s0 + (L - s0) * rng.uniform(.05, .98); col = (FOOD, GAS, HORM)[k % 3]
        if wave_s is not None and wave_s + 18 > s: s = min(L, wave_s + 18 + 6 * (k % 4))
        px, py = at(rs, s); c.circ(px, py + rng.uniform(-8, 8), r, col, a, bg=bg)

def wave_glow(c, rs, a, s, r, bg=LUMEN):
    """The green cleaning wave: a bright band at arc length s."""
    if a <= .01: return
    for k in range(8):
        x, y = at(rs, s - k * 9); c.circ(x, y, r * (1 - k / 10), CLEAN, a * (1 - k / 8), bg=bg)

def gut_path():
    """Stomach outlet on the left, then the small intestine folded into three rows (a simplified map)."""
    pts = [(470, 470)]
    rows = (470, 600, 730); xl, xr = 560, 1700
    pts += [(xr, rows[0])]
    for k, (ya, yb) in enumerate(zip(rows, rows[1:])):
        side = xr if k % 2 == 0 else xl; sgn = 1 if k % 2 == 0 else -1
        for j in range(1, 10):
            ang = -1.571 + 3.1416 * j / 9
            pts.append((side + sgn * 65 * math.cos(ang), (ya + yb) / 2 + 65 * math.sin(ang)))
        pts.append((xl if k % 2 == 0 else xr, yb))
    return pts

GUT = resample(gut_path(), 7)
LINE_RS = resample([(160, 560), (1760, 560)], 7)

# ---------- scenes ----------
def s_hook(c, T, t):
    """A figure in a quiet room, sound arcs from the belly from frame one; then the gut's clean-up wave; then empty."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Grrrrr...', SND)], sw_out(T, 1), size=96)
    headline(c, [('Your gut is ', INK), ('cleaning house', CLEAN)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Loudest when ', INK), ('empty', GAS)], sw_in(T, 2))
    person(c, 520, 600, 1.0, 1)
    stomach(c, 500, 600, .9, 1, bg=SKIN, glow=hl(1))
    arcs(c, 680, 620, 1, t, n=3, r0=60, gap=40)
    arcs(c, 360, 620, 1, t + .3, n=3, r0=60, gap=40, side=-1)
    m1 = hl(1)
    if m1 > .01:
        L = GUT[-1][2]; s = ((t - 0) * 260) % (L + 200) - 100
        sub = [(1000 + (x - 160) * .5, 300 + y * .5, d) for x, y, d in GUT]
        tube(c, sub, 24, m1)
        debris(c, sub, m1, s * 1.0, r=6, n=12)
        wave_glow(c, sub, m1, s, 14)
        c.text(1430, 720, 'a cleaning wave', 40, CLEAN, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        c.rr(1060, 760, 1800, 850, 26, CARD, m2, outline=GAS, ow=4)
        c.text(1430, 805, 'nothing inside = nothing to muffle it', 32, GAS, m2, w='Bold', bg=CARD)

def s_name(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('It has a ', INK), ('name', SND)], sw_out(T, 1))
    headline(c, [('Greek for ', INK), ('rumbling', SND)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Stomach ', INK), ('and', DIM), (' small intestine', MUS)], sw_in(T, 2), size=78)
    m01 = 1 - hl(2)
    if m01 > .01:
        syl = ('bor', 'bo', 'ryg', 'mi'); x = 960 - sum(c.tw(s_, 150, 'Bold') for s_ in syl) / 2 - 30
        for k, s_ in enumerate(syl):
            on = fd(T(0), .4 + .35 * k) if T(0) > -.1 else 0
            wob = 10 * math.sin(t * 9 + k) * hl(1)
            c.text(x, 450 + wob, s_, 150, mix(SND, .35 + .65 * on, INK), m01, 'lm', 'Bold'); x += c.tw(s_, 150, 'Bold') + 20
        c.text(960, 600, 'say it out loud: it sounds like the noise', 40, DIM, m01 * hl(1), w='Medium')
        for k in range(28):     # a rumble waveform under the word
            xx = 360 + k * 44; h = 30 + 26 * abs(math.sin(t * 6 + k * .7)) * (.4 + .6 * hl(1))
            c.rr(xx, 740 - h, xx + 24, 740 + h, 12, SND, m01 * .8)
    m2 = hl(2)
    if m2 > .01:
        stomach(c, 520, 520, 1.6, m2)
        arcs(c, 760, 520, m2, t, n=3)
        rs = resample([(1100, 420), (1700, 420), (1760, 480), (1700, 540), (1100, 540), (1040, 600), (1100, 660), (1700, 660)], 7)
        tube(c, rs, 30, m2)
        arcs(c, 1780, 660, m2, t + .4, n=3, r0=40, gap=32)
        c.text(520, 800, 'stomach', 44, INK, m2, w='Bold'); c.text(1400, 800, 'small intestine', 44, MUS, m2, w='Bold')
        c.text(960, 860, 'just as often', 32, DIM, m2, w='Medium')

def s_squeeze(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A long tube of ', INK), ('muscle', MUS)], sw_out(T, 1))
    headline(c, [('Rings ', MUS), ('squeeze in waves', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Squeezed gas ', GAS), ('gurgles', SND)], sw_in(T, 2))
    L = LINE_RS[-1][2]
    sq = (t * 330) % (L + 300) - 150 if hl(1) > .01 else None
    tube(c, LINE_RS, 120, 1, squeeze=sq, sw=70, depth=.55)
    # contents ahead of the ring: food, liquid, gas
    if sq is not None:
        rng = random.Random(2)
        for k in range(9):
            s = (sq + 90 + k * 55) % (L + 300) - 30
            if 0 < s < L:
                x, y = at(LINE_RS, s); col = (FOOD, GAS, (90, 140, 220))[k % 3]
                c.circ(x, y + rng.uniform(-30, 30), 22, col, 1, bg=LUMEN)
    else:
        bubbles(c, LINE_RS, 1, 200, L - 200, 120, n=9, t=t)
    m0 = 1 - hl(1)
    c.text(960, 760, 'your gut: a long, muscly tube', 42, INK, m0, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        # toothpaste analogy, small and below
        c.rr(640, 740, 1180, 800, 30, (200, 205, 225), m1); c.rr(1180, 755, 1240, 785, 8, (160, 165, 190), m1)
        c.rr(820, 735, 880, 805, 20, MUS, m1)
        c.text(1300, 770, 'like toothpaste', 40, INK, m1, 'lm', 'Bold')
    m2 = hl(2)
    if m2 > .01 and sq is not None:
        x, y = at(LINE_RS, clamp(sq, 0, L)); arcs(c, x, y - 150, m2, t, n=3, r0=30, gap=28, spread=.5)
        c.text(960, 780, 'gas + liquid through a tight spot = gurgle', 40, SND, m2, w='Bold')

def s_muffle(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Full: ', INK), ('muffled', FOOD)], sw_out(T, 1))
    headline(c, [('Empty: ', INK), ('more air', GAS), (' than food', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('So it ', INK), ('rings out', SND)], sw_in(T, 2))
    L = 680; sq = (t * 240) % (L + 200) - 100
    full = resample([(160, 430), (840, 430)], 7); empty = resample([(1080, 430), (1760, 430)], 7)
    tube(c, full, 90, 1, squeeze=sq, sw=55, depth=.45, fill=FOOD)
    c.text(500, 560, 'after a meal', 40, FOOD, 1, w='Bold')
    x, y = at(full, clamp(sq, 0, L)); arcs(c, x, y - 120, .45, t, n=1, r0=24, spread=.4, w=4)
    me = hl(1)
    tube(c, empty, 90, .35 + .65 * me, squeeze=sq if me > .01 else None, sw=55, depth=.45)
    bubbles(c, empty, me, 60, L - 60, 90, n=7, t=t)
    c.text(1420, 560, 'empty', 40, GAS, .35 + .65 * me, w='Bold')
    if me > .01:
        x, y = at(empty, clamp(sq, 0, L)); arcs(c, x, y - 110, me, t, n=3, r0=30, gap=36, spread=.55)
    m0 = 1 - hl(2)
    if m0 > .01:   # pillow over a speaker
        c.rr(380, 650, 620, 840, 30, (70, 78, 120), m0); c.circ(500, 745, 60, DARK, m0, bg=(70, 78, 120))
        c.rr(330, 620, 670, 720, 50, (225, 225, 240), m0 * fd(T(0), 1.5) if T(0) > -.1 else 0)
        c.text(830, 745, 'like a pillow on a speaker', 34, DIM, m0, 'lm', 'Bold')
    m2 = hl(2)
    if m2 > .01:   # empty box vs full box
        for k, (lab, col, n) in enumerate((('full box: thud', FOOD, 1), ('empty box: knock!', SND, 3))):
            bx = 560 + k * 800
            c.rr(bx - 120, 620, bx + 120, 770, 14, (150, 110, 70), m2, outline=(200, 160, 110), ow=4)
            if k == 0: c.rr(bx - 100, 650, bx + 100, 750, 10, FOOD, m2, bg=(150, 110, 70))
            arcs(c, bx + 140, 695, m2 * (.4 if k == 0 else 1), t, n=n, r0=30, gap=28, spread=.5)
            c.text(bx, 815, lab, 34, col, m2, w='Bold')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Skip lunch. How often does the ', INK), ('wave', CLEAN), (' come?', INK)], 1, bg=QUIZ, size=68)
    for k, txt in enumerate(('A  Every 10 minutes', 'B  Every 1 to 2 hours')):
        u = fd(t, .8 + .3 * k)
        c.rr(260, 360 + k * 200, 1120, 500 + k * 200, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(310, 430 + k * 200, txt, 52, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    clock(c, 1460, 470, 130, fd(t, .5), (t * .25) % 1.0, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - QZ; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), QZ - .3)
        c.circ(1460, 730, 80, SND, u, bg=QUIZ); c.text(1460, 730, str(k) if k else '?', 76, DARK, u, w='Bold', bg=SND)

def s_sweep(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('B: every ', INK), ('1 to 2 hours', CLEAN)], sw_out(T, 1))
    headline(c, [('The ', INK), ('migrating motor complex', CLEAN)], sw_in(T, 1) * sw_out(T, 2), size=76)
    headline(c, [('It ', INK), ('sweeps', CLEAN), (' out leftovers', INK)], sw_in(T, 2))
    stomach(c, 330, 470, 1.2, 1, glow=hl(1))
    tube(c, GUT, 38, 1)
    L = GUT[-1][2]
    s = (fd(T(1), 0, 5.5) if T(1) > -.1 else 0) * (L + 40) if hl(2) < .01 else ((t * 280) % (L + 200))
    w = hl(1)
    debris(c, GUT, 1, s if w > .01 else None, n=18)
    wave_glow(c, GUT, w, s, 22)
    m0 = 1 - hl(1)
    if m0 > .01: clock(c, 1640, 330, 70, m0, (t * .3) % 1, col=CLEAN)
    c.text(330, 650, 'stomach', 34, INK, 1, w='Bold')
    c.text(1130, 820, 'small intestine (simplified)', 32, DIM, 1, w='Medium')
    m2 = hl(2)
    if m2 > .01:
        for k, (lab, col) in enumerate((('leftover food', FOOD), ('mucus', GAS), ('bacteria', HORM))):
            x = 760 + k * 340; c.circ(x - 20, 320, 14, col, m2); c.text(x, 320, lab, 34, col, m2, 'lm', 'Bold')

def s_cycle(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Quiet for ', INK), ('45 to 60 minutes', DIM)], sw_out(T, 1))
    headline(c, [('Then a ', INK), ('burst', MUS), (' of strong waves', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Noisy', SND), (': a big cause of the growl', INK)], sw_in(T, 2), size=78)
    x0, x1, y = 200, 1720, 470; tot = 100.0
    segs = (('quiet', 52, (80, 86, 120), '45 to 60 min'), ('building', 32, CLEAN, 'about 30 min'), ('burst', 10, MUS, '5 to 15 min'), ('', 6, (110, 90, 120), ''))
    x = x0
    for k, (lab, mins, col, sub) in enumerate(segs):
        w = (x1 - x0) * mins / tot
        u = 1 if k == 0 else (hl(1) if k < 3 else hl(1) * .7)
        if k == 2: u = fd(T(1), 1.2) if T(1) > -.1 else 0
        c.rr(x, y - 50, x + w - 6, y + 50, 18, col, u)
        if lab:
            c.text(x + w / 2, y - 90, lab, 38 if k < 2 else 34, col if k else INK, u, w='Bold')
            c.text(x + w / 2, y + 90, sub, 30, DIM, u, w='Medium')
        x += w
    # the build-up drawn as rising bars inside the green part
    if hl(1) > .01:
        xs = x0 + (x1 - x0) * .52
        for k in range(10):
            h = 8 + 4 * k; c.rr(xs + 14 + k * 46, y + 40 - h * 2, xs + 40 + k * 46, y + 40, 6, (40, 120, 80), hl(1) * .9, bg=CLEAN)
    # repeat arrow
    c.line([(x1 - 30, y + 150), (x1 - 30, y + 200), (x0 + 30, y + 200), (x0 + 30, y + 150)], DIM, 5, hl(1))
    c.arrow(x0 + 30, y + 170, x0 + 30, y + 140, DIM, 5, hl(1))
    c.text(960, y + 240, 'then it repeats, until you eat', 34, DIM, hl(1), w='Medium')
    m2 = hl(2)
    if m2 > .01:
        bx = x0 + (x1 - x0) * .89; arcs(c, bx, y - 40, m2, t, n=3, r0=40, gap=34, spread=.6)
        c.text(960, 820, 'times are typical ranges; simplified timeline', 26, DIM, m2, w='Regular')

def s_switch(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A hormone: ', INK), ('motilin', HORM)], sw_out(T, 1))
    headline(c, [('Eating ', FOOD), ('switches it off', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('A snack ', FOOD), ('quiets the growl', INK)], sw_in(T, 2))
    stomach(c, 520, 520, 1.5, 1, glow=1 - hl(1))
    m0 = 1 - hl(1)
    if m0 > .01:
        for k in range(7):
            ang = t * .7 + k * .9; r = 260 + 20 * math.sin(t * 2 + k)
            x, y = 520 + r * math.cos(ang), 520 + r * .7 * math.sin(ang)
            c.circ(x, y, 26, HORM, m0); c.text(x, y, 'M', 26, INK, m0, w='Bold', bg=HORM)
        c.text(1300, 430, 'helps set the rhythm', 44, HORM, m0, w='Bold')
        c.text(1300, 500, 'of the cleaning waves', 40, INK, m0, w='Bold')
    on = 1 - (fd(T(1), .8, .5) if T(1) > -.1 else 0)
    m12 = hl(1)
    if m12 > .01:
        drop = fd(T(1), 0, .8) if T(1) > -.1 else 0
        apple(c, 980 - 200 * drop, 345, 1.0, m12)
        switch(c, 1300, 470, m12, on)
        c.text(1300, 700, 'normal, gentler digestion pattern', 36, FOOD, m12 * (1 - on), w='Bold')
    m2 = hl(2)
    if m2 > .01:
        arcs(c, 760, 560, m2 * .3, 0, n=1, r0=30, spread=.4, w=4)
        c.rr(1060, 770, 1540, 850, 26, CARD, m2, outline=FOOD, ow=4)
        c.text(1300, 810, 'usually, the growl fades', 32, INK, m2, w='Bold', bg=CARD)

def s_payoff(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Between meals: ', INK), ('normal', CLEAN)], sw_out(T, 1))
    headline(c, [('An empty gut, ', GAS), ('sweeping itself clean', CLEAN)], sw_in(T, 1), size=78)
    person(c, 520, 600, 1.0, 1)
    stomach(c, 500, 600, .9, 1, bg=SKIN, glow=.5 + .5 * math.sin(t * 3))
    arcs(c, 680, 620, 1, t, n=3, r0=60, gap=40)
    c.check(1300, 470, 140, CLEAN, hl(0), fd(T(0), .3, .6) if T(0) > -.1 else 0)
    m1 = hl(1)
    if m1 > .01:
        rs = resample([(1000, 700), (1700, 700)], 7); L = rs[-1][2]; s = (t * 260) % (L + 120)
        tube(c, rs, 50, m1); debris(c, rs, m1, s, n=8, r=8); wave_glow(c, rs, m1, s, 24)
        c.text(1350, 800, 'no food inside to muffle it', 34, GAS, m1, w='Bold')

def s_recap(c, T, t):
    """Recap as three tall cards, each with its own little picture."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', SND)], 1)
    items = ((1, 'muscle squeezes', 'gas and liquid', MUS), (2, 'loudest empty', 'no food to muffle', GAS), (3, 'every 1 to 2 hours', 'a wave, until you eat', CLEAN))
    for ln, l1, l2, col in items:
        m = hl(ln); x = 400 + (ln - 1) * 560; dy = 40 * (1 - m)
        c.rr(x - 250, 290 + dy, x + 250, 820 + dy, 30, CARD, m, outline=col, ow=4)
        c.text(x, 340 + dy, str(ln), 48, col, m, w='Bold', bg=CARD)
        if ln == 1:
            rs = resample([(x - 160, 500 + dy), (x + 160, 500 + dy)], 7)
            tube(c, rs, 54, m, squeeze=(t * 200) % 320, sw=40, bg=CARD); bubbles(c, rs, m, 40, 280, 54, n=4, t=t)
        elif ln == 2:
            stomach(c, x - 40, 510 + dy, .8, m, bg=CARD); arcs(c, x + 90, 510 + dy, m, t, n=3, r0=30, gap=26, bg=CARD)
        else:
            clock(c, x, 500 + dy, 95, m, (t * .3) % 1, col=CLEAN, bg=CARD)
        c.text(x, 680 + dy, l1, 40, col, m, w='Bold', bg=CARD)
        c.text(x, 740 + dy, l2, 30, DIM, m, w='Medium', bg=CARD)
    c.text(960, 870, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """A big stomach with a green cleaning wave inside and loud yellow sound arcs."""
    stomach(c, 1460, 520, 2.6, 1, glow=1.0)
    arcs(c, 1780, 560, 1, .2, n=3, r0=60, gap=46, w=12)
    arcs(c, 1240, 400, 1, .5, n=2, r0=50, gap=40, side=-1, w=12)

SCENES = [
 ('THE GROWL', ["That loud growl from your belly, right when the room goes quiet?",
                "It's the sound of your gut cleaning house.",
                "And it's loudest when there's nothing inside."], s_hook),
 ('THE NAME', ["It even has a name: borborygmi.",
               "The ancient Greeks picked a word that sounds like the rumble itself.",
               "And it doesn't only come from your stomach. Just as often, it comes from your small intestine."], s_name),
 ('THE SQUEEZE', ["Your gut is a long tube wrapped in muscle.",
                  "Rings of that muscle squeeze in waves, pushing food, liquid and gas along, like squeezing toothpaste through its tube.",
                  "When gas and liquid get pushed through a tight spot, they gurgle."], s_squeeze),
 ('THE MUFFLE', ["This squeezing goes on after a meal too. But food muffles the sound, like a pillow over a speaker.",
                 "When you're empty, there's more air than food inside.",
                 "So the same squeeze rings out, like knocking on an empty box instead of a full one."], s_muffle),
 ('QUICK QUESTION', ["Quick question. If you skip lunch, how often does your gut start a big cleaning wave? Every ten minutes, or every one to two hours? Have a guess."], s_quiz),
 ('THE SWEEP', ["It's B. Every one to two hours.",
                "It's called the migrating motor complex: a strong wave that starts in the stomach and sweeps all the way along the small intestine.",
                "It clears out leftover food, mucus and bacteria, like a cleaner sweeping a hallway after everyone has gone home."], s_sweep),
 ('THE CYCLE', ["Each cycle starts with a quiet spell of about forty-five to sixty minutes.",
                "Then the squeezing builds, and ends with a burst of strong waves lasting five to fifteen minutes.",
                "These cleaning waves can be noisy. They're a big cause of the growling."], s_cycle),
 ('THE OFF SWITCH', ["A gut hormone called motilin is thought to help set this rhythm.",
                     "And eating switches the cleaning wave off. Food brings back the normal, gentler pattern of digestion.",
                     "That's why a snack can usually quiet the growl."], s_switch),
 ('THE ANSWER', ["So a growl between meals is normal.",
                 "It's your empty gut sweeping itself clean, with no food inside to muffle the sound."], s_payoff),
 ('RECAP', ["Three things to keep.",
            "One: the growl is muscle squeezing gas and liquid through your stomach and small intestine.",
            "Two: it's loudest when you're empty, because no food muffles it.",
            "Three: about every one to two hours, a cleaning wave sweeps through, until you eat.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_squeeze(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Muscle ', MUS), ('squeezes gas', GAS)], sw_out(T, 1) * sw_out(T, 2), size=88)
    headline(c, [('It ', INK), ('gurgles', SND)], sw_in(T, 1) * sw_out(T, 2), size=88)
    headline(c, [('Empty = ', INK), ('nothing muffles it', GAS)], sw_in(T, 2), size=80)
    L = LINE_RS[-1][2]; sq = (t * 330) % (L + 300) - 150
    tube(c, LINE_RS, 140, 1, squeeze=sq, sw=70, depth=.55)
    bubbles(c, LINE_RS, 1, max(0, sq + 80), min(L, sq + 600), 140, n=6, t=t)
    x, y = at(LINE_RS, clamp(sq, 0, L)); arcs(c, x, y - 170, .4 + .6 * max(hl(1), hl(2)), t, n=3, r0=30, gap=30, spread=.5)
    c.text(960, 790, 'stomach and small intestine', 44, MUS, 1 - hl(2), w='Bold')
    c.text(960, 790, 'no food inside', 44, GAS, hl(2), w='Bold')

def short_sweep(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A ', INK), ('cleaning wave', CLEAN)], sw_out(T, 2), size=88)
    headline(c, [('Leftovers ', FOOD), ('swept out', CLEAN)], sw_in(T, 2), size=88)
    stomach(c, 330, 470, 1.2, 1, glow=1)
    tube(c, GUT, 38, 1)
    L = GUT[-1][2]; s = (t * 300) % (L + 200)
    debris(c, GUT, 1, s, n=18); wave_glow(c, GUT, 1, s, 22)
    m = hl(1) * (1 - hl(2))
    if m > .01:
        clock(c, 1640, 320, 70, m, (t * .3) % 1, col=CLEAN)
        c.text(1640, 430, 'every 1 to 2 hours', 34, CLEAN, m, w='Bold')

def short_switch(c, T, t):
    headline(c, [('Eat', FOOD), (' and it switches off', INK)], 1, size=84)
    drop = fd(T(0), 0, .8) if T(0) > -.1 else 0
    stomach(c, 520, 560, 1.5, 1, glow=1 - drop)
    apple(c, 980 - 200 * drop, 360, 1.0, 1)
    switch(c, 1300, 500, 1, 1 - (fd(T(0), 1.0, .5) if T(0) > -.1 else 0))

SHORT_SCENES = [
 ('THE GROWL', ["That growl from your empty belly?",
                "It's the sound of your gut cleaning house.",
                "And it's loudest when there's nothing inside."], s_hook),
 ('THE SQUEEZE', ["Rings of muscle squeeze in waves, pushing gas and liquid along your stomach and small intestine.",
                  "The gas gurgles as it's squeezed through.",
                  "After a meal, food muffles the sound. When you're empty, nothing does."], short_squeeze),
 ('THE SWEEP', ["When you haven't eaten for a while, a strong cleaning wave sweeps through.",
                "It comes about every one to two hours. It's called the migrating motor complex.",
                "It clears out leftover food, mucus and bacteria."], short_sweep),
 ('OFF SWITCH', ["Eat something, and that wave switches off."], short_switch),
 ('THE ANSWER', ["So the growl is your empty gut, sweeping itself clean.",
                 "And a snack can usually quiet it."], card('Your gut, cleaning house.', 'A snack usually quiets it.')),
]
SHORT_HITS = [(4, 0, 0.0)]
