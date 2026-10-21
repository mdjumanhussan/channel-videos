"""Episode: Caffeine Doesn't Give You Energy. It Hides Tiredness"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "How Caffeine Works"                      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                  # about 158 wpm while speaking (lesson of 2026-10-22: 150-160)
SHORT_HOOK = "Does coffee give you energy?"             # headline on the vertical Short
HITS = [(0, 2, 0.0), (3, 2, 0.0), (5, 2, 0.0)]          # title card, the block, quiz answer
THUMB = ['CAFFEINE ADDS', 'NO ENERGY']
MUSIC_LEVEL = 0.006                                     # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                          # no dead air before the first word (lesson of 2026-10-19)
# Applied lesson (learnings.md, 2026-10-22): slow down and leave a beat after the key concept so it can land.
# PAUSES adds silence after a line (engine default: none). Used after the core reveal, the quiz answer and the twist.
PAUSES = {(0, 1): 0.5, (3, 2): 0.8, (5, 2): 0.7, (6, 2): 0.6}
SHORT_PAUSES = {(2, 2): 0.6}
CAPTION_FIXES = {'thirty minutes': '30 minutes', 'four hundred milligrams': '400 milligrams',
                 'twenty thirteen': '2013', 'twelve to twenty-four hours': '12 to 24 hours'}

COFFEE = (150, 96, 60); CREAM = (226, 196, 160); MUG = (236, 238, 250); AMBER = (255, 170, 40)
TAPE = (214, 200, 150); ADE = PU; CAF = (232, 150, 70); CELL = (36, 50, 92); REC = (120, 200, 240)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, BG, a, w='Bold', bg=col)

def mug(c, x, y, s, a=1.0, t=0.0, bg=BG, steam=True):
    """Coffee mug, (x, y) = centre of the body, s = body half-width."""
    if a <= 0.01: return
    c.circ(x + s * 1.05, y, s * .45, None, a, outline=MUG, ow=max(4, s * .16), bg=bg)
    c.rr(x - s, y - s * 1.1, x + s, y + s * 1.1, s * .25, MUG, a, bg=bg)
    c.rr(x - s * .84, y - s * 1.02, x + s * .84, y - s * .78, s * .12, COFFEE, a, bg=MUG)
    c.rr(x - s * .5, y - s * .1, x + s * .5, y + s * .25, s * .1, CREAM, a * .6, bg=MUG)
    if steam:
        for j in range(3):
            ph = (t * .5 + j / 3) % 1
            x0 = x + (j - 1) * s * .45
            pts = [(x0 + s * .12 * math.sin(q * 6 + t * 3 + j), y - s * 1.25 - q * s * 1.3 - ph * s * .5) for q in [u / 8 for u in range(9)]]
            c.line(pts, (200, 205, 230), max(3, s * .06), a * (1 - ph) * .8, bg)

def gauge(c, x, y, r, a=1.0, level=0.1, light=1.0, tape=0.0, t=0.0, bg=BG):
    """Fuel gauge with a warning light under it. light: 0..1 lamp on; tape: 0..1 tape slid over the lamp."""
    if a <= 0.01: return
    c.circ(x, y, r, CARD, a, outline=DIM, ow=6, bg=bg)
    pts = [(x + r * .82 * math.cos(math.pi * (1 + u / 30)), y + r * .82 * math.sin(math.pi * (1 + u / 30))) for u in range(31)]
    c.line(pts, DIM, 6, a, CARD)
    c.text(x - r * .72, y + r * .2, 'E', r * .2, PK, a, w='Bold', bg=CARD)
    c.text(x + r * .72, y + r * .2, 'F', r * .2, INK, a, w='Bold', bg=CARD)
    ang = math.pi * (1 + clamp(level))
    c.line([(x, y), (x + r * .7 * math.cos(ang), y + r * .7 * math.sin(ang))], PK, max(5, r * .05), a, CARD)
    c.circ(x, y, r * .08, INK, a, bg=CARD)
    lx, ly, lr = x, y + r * .55, r * .17
    blink = .55 + .45 * math.sin(t * 6)
    c.circ(lx, ly, lr, (60, 50, 40), a, bg=CARD)
    if light > .01:
        c.circ(lx, ly, lr * 1.6, AMBER, a * light * .18 * blink, bg=CARD)
        c.circ(lx, ly, lr, AMBER, a * light * (.6 + .4 * blink), bg=CARD)
        c.text(lx, ly, '!', lr * 1.3, BG, a * light, w='Bold', bg=AMBER)
    if tape > .01:
        w = lr * 3.0; xx = lx - w / 2 + (1 - clamp(tape)) * r * 1.6
        poly(c, [(xx, ly - lr * 1.2), (xx + w, ly - lr * 1.0), (xx + w, ly + lr * 1.25), (xx, ly + lr * 1.05)], TAPE, a * clamp(tape * 2), CARD)

def neuron(c, x0, y0, x1, y1, n, a=1.0, bg=BG, cols=None):
    """Brain cell seen side-on: a long body with n receptor cups along its top. Returns receptor centres."""
    if a <= 0.01: return []
    c.rr(x0, y0, x1, y1, 50, CELL, a, outline=(70, 90, 150), ow=5, bg=bg)
    pts = []
    for i in range(n):
        rx = x0 + (x1 - x0) * (i + .5) / n; ry = y0
        col = (cols[i] if cols else REC)
        c.line([(rx - 26, ry - 30), (rx - 26, ry), (rx + 26, ry), (rx + 26, ry - 30)], col, 8, a, bg)
        pts.append((rx, ry - 18))
    return pts

def ade(c, x, y, a=1.0, bg=BG, r=17):
    """Adenosine: purple ball."""
    c.circ(x, y, r, ADE, a, bg=bg); c.circ(x - r * .3, y - r * .3, r * .3, (200, 180, 255), a, bg=ADE)

def caf(c, x, y, a=1.0, bg=BG, r=19):
    """Caffeine: orange hexagon."""
    if a <= 0.01: return
    poly(c, [(x + r * math.cos(k * math.pi / 3 + math.pi / 6), y + r * math.sin(k * math.pi / 3 + math.pi / 6)) for k in range(6)], CAF, a, bg)
    c.circ(x, y, r * .35, (120, 70, 30), a, bg=CAF)

def meter(c, x, y, h, v, a=1.0, label='SLEEPY', col=ADE, bg=BG):
    """Vertical meter, bottom at y."""
    if a <= 0.01: return
    c.rr(x - 34, y - h, x + 34, y, 18, CARD, a, outline=DIM, ow=4, bg=bg)
    fh = (h - 12) * clamp(v)
    if fh > 6: c.rr(x - 26, y - 6 - fh, x + 26, y - 6, 12, col, a, bg=CARD)
    c.text(x, y + 36, label, 28, col, a, w='Bold')

def clock(c, x, y, r, hrs, a=1.0, bg=BG):
    if a <= 0.01: return
    c.circ(x, y, r, CARD, a, outline=INK, ow=5, bg=bg)
    for k in range(12):
        u = k * math.pi / 6
        c.line([(x + r * .8 * math.sin(u), y - r * .8 * math.cos(u)), (x + r * .92 * math.sin(u), y - r * .92 * math.cos(u))], DIM, 3, a, CARD)
    u = hrs / 12 * 2 * math.pi
    c.line([(x, y), (x + r * .5 * math.sin(u / 12), y - r * .5 * math.cos(u / 12))], INK, 6, a, CARD)
    c.line([(x, y), (x + r * .75 * math.sin(u), y - r * .75 * math.cos(u))], CY, 4, a, CARD)

def bed(c, x, y, s, a=1.0, bg=BG, col=CY):
    if a <= 0.01: return
    c.rr(x - s, y - s * .2, x + s, y + s * .15, 10, col, a, bg=bg)
    c.rr(x - s, y - s * .55, x - s * .9, y + s * .4, 6, col, a, bg=bg)
    c.rr(x + s * .9, y - s * .35, x + s, y + s * .4, 6, col, a, bg=bg)
    c.rr(x - s * .85, y - s * .42, x - s * .45, y - s * .2, 12, INK, a, bg=bg)

def head(c, x, y, s, a=1.0, ache=0.0, t=0.0, bg=BG):
    if a <= 0.01: return
    c.circ(x, y, s, (230, 200, 170), a, bg=bg)
    c.line([(x - s * .45, y - s * .1), (x - s * .15, y - s * .2)], BG, 6, a, (230, 200, 170))
    c.line([(x + s * .15, y - s * .2), (x + s * .45, y - s * .1)], BG, 6, a, (230, 200, 170))
    c.line([(x - s * .3, y + s * .45), (x, y + s * .35), (x + s * .3, y + s * .45)], BG, 6, a, (230, 200, 170))
    if ache > .01:
        for j in range(3):
            u = -math.pi / 2 + (j - 1) * .6
            p = .5 + .5 * math.sin(t * 8 + j)
            x0, y0 = x + s * 1.15 * math.cos(u), y + s * 1.15 * math.sin(u)
            x1, y1 = x + s * (1.45 + .1 * p) * math.cos(u), y + s * (1.45 + .1 * p) * math.sin(u)
            c.line([(x0, y0), (x1, y1)], PK, 8, a * ache)

def thumb_art(c):
    mug(c, 1400, 660, 160, 1, 1.0)
    gauge(c, 1640, 250, 160, 1, level=.05, light=1, tape=1, t=0.3)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), .3, .5)
    if a > 0:
        # motion from frame one: steam rising, coffee flowing toward an energy bar that never fills
        mug(c, 560, 520, 150, a, t)
        for j in range(5):
            ph = (t * .9 + j / 5) % 1
            c.circ(760 + ph * 380, 470 - 60 * math.sin(math.pi * ph), 12, COFFEE, a * (1 - ph * .5))
        bx = 1300
        c.rr(bx - 70, 270, bx + 70, 700, 26, CARD, a, outline=INK, ow=6)
        c.rr(bx - 30, 245, bx + 30, 270, 8, INK, a)
        c.rr(bx - 54, 640, bx + 54, 684, 14, PK, a, bg=CARD)
        c.text(bx, 760, 'energy added: 0', 40, PK, a * hl(0), w='Bold')
        c.text(960, 150, 'Caffeine adds no energy', 66, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'It hides how tired you are', 66, YE, a * hl(1), w='Bold')
        if T(1) > -.1:
            k = hl(1)
            gauge(c, 1640, 470, 150, a * k, level=.06, light=1, tape=fd(T(1), .8, .8), t=t)
    if T(2) > 0:
        m = fd(T(2), .45, .7)
        c.text(960, 330 + 30 * (1 - m), 'The Coffee', 130, INK, m, w='Bold')
        c.text(960, 490 + 30 * (1 - m), 'Trick', 130, YE, m, w='Bold')
        c.line([(960 - 300 * m, 600), (960 + 300 * m, 600)], CAF, 8, m)
        c.text(960, 690, 'How caffeine hides your tiredness', 46, DIM, fd(T(2), 1.2), w='Medium')

def s_light(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'A warning light', 66, INK, hl(0) * (1 - hl(3)), w='Bold')
    c.text(960, 130, 'Caffeine is the tape', 66, YE, hl(3), w='Bold')
    tape = fd(T(1), .3, .9) if T(1) > -.1 else 0.0
    gauge(c, 620, 470, 260, hl(0), level=.06 + .02 * math.sin(t), light=1, tape=tape, t=t)
    c.text(620, 850, 'fuel: almost empty', 36, PK, hl(0) * fd(T(0), 1.2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    c.text(1340, 380, 'The light fixes nothing.', 44, INK, k0 * fd(T(0), 1.0), 'mm', 'Bold')
    c.text(1340, 450, 'It just says: stop soon.', 44, AMBER, k0 * fd(T(0), 2.0), 'mm', 'Bold')
    k1 = hl(1) * (1 - hl(2))
    c.text(1340, 420, 'Cover the light with tape...', 46, TAPE, k1, 'mm', 'Bold')
    k2 = hl(2)
    if k2 > 0:
        c.text(1340, 330, 'You feel fine.', 50, GR, k2, 'mm', 'Bold')
        c.text(1340, 420, 'The tank is just as empty.', 46, PK, k2 * fd(T(2), 1.0), 'mm', 'Bold')
    if T(3) > -.1:
        caf(c, 1340, 600, hl(3), r=48)
        c.arrow(1280, 600, 900, 600, CAF, 6, hl(3) * fd(T(3), .4), 22)

def s_signal(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, "Your brain's warning light", 66, INK, hl(0), w='Bold')
    pts = neuron(c, 260, 600, 1360, 780, 6, hl(0))
    c.text(810, 690, 'brain cell', 36, DIM, hl(0), w='Bold', bg=CELL)
    ade(c, 1520, 250, hl(0), r=30)
    c.text(1570, 250, 'adenosine', 44, ADE, hl(0), 'lm', 'Bold')
    # hours awake: more and more adenosine floats around
    p = fd(T(1), 0, 3.0) if T(1) > -.1 else 0.0
    clock(c, 1640, 400, 80, 8 + 14 * p, hl(1))
    c.text(1640, 515, f'awake {int(1 + 15 * p)} h', 34, CY, hl(1), w='Bold')
    nfree = int(4 + 18 * p)
    for i in range(nfree):
        x = 300 + ((i * 197) % 1000) + 14 * math.sin(t * 1.4 + i)
        y = 260 + ((i * 113) % 230) + 12 * math.cos(t * 1.2 + i)
        ade(c, x, y, hl(0) * fd(T(0), .8))
    # docking: adenosine lands in receptors
    q = fd(T(2), .4, 2.0) if T(2) > -.1 else 0.0
    for j, (rx, ry) in enumerate(pts):
        k = clamp(q * 6 - j)
        if k > 0: ade(c, rx, ry - 80 * (1 - k), hl(2) * clamp(k * 2))
    c.text(810, 860, 'receptors', 34, REC, hl(2) * (1 - q), w='Bold')
    meter(c, 1640, 790, 190, .1 + .25 * p + .6 * q, hl(1))

def s_block(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Caffeine takes the seats', 66, INK, hl(0) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'The tiredness signal is blocked', 66, YE, hl(2), w='Bold')
    pts = neuron(c, 200, 600, 1300, 780, 6, hl(0))
    q = fd(T(0), .5, 2.0) if T(0) > -.1 else 0.0
    for j, (rx, ry) in enumerate(pts):
        k = clamp(q * 6 - j)
        if k > 0: caf(c, rx, ry - 90 * (1 - k), hl(0) * clamp(k * 2))
    # adenosine tries to land and bounces off
    for i in range(7):
        ph = (t * .6 + i / 7) % 1
        x = 260 + i * 150 + 20 * math.sin(t + i)
        b = abs(math.sin(math.pi * ph))
        ade(c, x, 520 - 220 * b, hl(0) * fd(T(0), 1.0))
    c.text(750, 835, 'orange = caffeine   purple = adenosine', 32, DIM, hl(0), w='Bold')
    # key that fits but won't turn
    k1 = hl(1)
    if k1 > 0:
        lx, ly = 1620, 360
        c.rr(lx - 110, ly - 40, lx + 110, ly + 170, 30, (120, 128, 160), k1)
        c.line([(lx - 70, ly - 40), (lx - 70, ly - 120), (lx + 70, ly - 120), (lx + 70, ly - 40)], (120, 128, 160), 24, k1)
        c.circ(lx, ly + 50, 24, BG, k1, bg=(120, 128, 160))
        wig = 8 * math.sin(t * 9) * fd(T(1), 1.0)
        c.rr(lx - 200, ly + 40 + wig * .2, lx - 10, ly + 60 + wig * .2, 6, CAF, k1)
        c.circ(lx - 220, ly + 50, 34, CAF, k1); c.circ(lx - 220, ly + 50, 14, BG, k1, bg=CAF)
        c.text(lx, ly + 230, 'fits, but won\'t turn', 38, CAF, k1, w='Bold')
    meter(c, 1620, 790, 150, .85 * (1 - (fd(T(2), .3, 1.2) if T(2) > -.1 else 0)) + .05, hl(0))

def s_timing(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'How long it lasts', 66, INK, hl(0), w='Bold')
    ox, oy, gw, gh = 300, 770, 1320, 520
    m = hl(0)
    c.line([(ox, oy - gh), (ox, oy), (ox + gw, oy)], DIM, 4, m)
    for hrs in range(0, 13, 2):
        c.text(ox + gw * hrs / 12, oy + 36, f'{hrs} h', 26, DIM, m, w='Medium')
    c.text(ox - 20, oy - gh - 60, 'caffeine in your body', 30, CAF, m, 'lm', 'Bold')
    # simplified: rise over about 45 min, half-life 5 h
    def lvl(h):
        rise = clamp(h / .75)
        return rise * (0.5 ** (h / 5)) if h > 0 else 0
    p = (fd(T(0), 0, 1.0) if T(0) > -.1 else 0) * .15 + (fd(T(1), 0, 2.5) if T(1) > -.1 else 0) * .85
    pts = [(ox + gw * u / 120 * 12 / 12, oy - gh * .9 * lvl(u / 10)) for u in range(0, int(120 * clamp(p)) + 1)]
    c.line(pts, CAF, 8, m)
    k0 = m * fd(T(0), .8)
    x30 = ox + gw * .5 / 12
    c.line([(x30, oy), (x30, oy - gh * .97)], YE, 3, k0)
    c.text(x30 + 70, oy - gh * .97, 'kicks in: about 30 min', 32, YE, k0, 'lm', 'Bold')
    if T(1) > -.1:
        k1 = hl(1) * fd(T(1), 1.6)
        x5 = ox + gw * 5 / 12
        c.line([(x5, oy), (x5, oy - gh * .66)], GR, 3, k1)
        c.text(x5 + 20, oy - gh * .66, 'half gone: about 5 h', 32, GR, k1, 'lm', 'Bold')
        c.text(x5 + 20, oy - gh * .66 + 44, '(average adult)', 26, DIM, k1, 'lm', 'Medium')
    if T(2) > -.1:
        k2 = hl(2)
        x2, x12 = ox + gw * 2 / 12, ox + gw * 12 / 12
        c.rr(x2, oy - 70, x12, oy - 20, 20, (60, 70, 110), k2 * .8)
        c.text((x2 + x12) / 2, oy - 45, 'half-life varies: 2 to 12 hours', 30, INK, k2, w='Bold', bg=(48, 56, 92))
    c.text(ox + gw, oy - gh - 30, 'simplified', 26, DIM, m, 'rm', 'Medium')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(2)
    c.text(960, 120, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 195, 'Caffeine 6 hours before bed. What happened?', 46, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 160, 'More than 1 hour less sleep', 62, PK, ans, w='Bold')
    opts = [('A', 'Slept as usual', GR), ('B', 'Slept over an hour less', PK)]
    for j, (lab, txt, col) in enumerate(opts):
        x = 560 + j * 800
        kk = m * fd(T(0), 1.2 + j * 1.0)
        if kk <= 0: continue
        dim = 1 - (.55 * ans if j == 0 else 0)
        c.rr(x - 330, 270, x + 330, 720, 30, CARD, kk * dim, outline=(PK if (ans > 0 and j == 1) else DIM), ow=5)
        c.text(x - 270, 330, lab, 46, YE, kk * dim, w='Bold', bg=CARD)
        bed(c, x, 470, 170, kk * dim, CARD, col=col)
        mug(c, x + 200, 380, 34, kk * dim, t, CARD, steam=False)
        c.text(x, 620, txt, 40, INK, kk * dim, w='Bold', bg=CARD)
    if ans > 0:
        c.text(960, 790, "...and they didn't notice", 48, YE, fd(T(2), 1.4), w='Bold')
        c.text(960, 850, '2013 study, 12 people, 400 mg (about 2 to 3 cups of coffee)', 28, DIM, ans, w='Medium')
    if T(1) > 0 and ans < 1:
        p = clamp(T(1) / 2.0)
        ring(c, 960, 500, 60, 1 - p, CY, fd(T(1)) * (1 - ans))
        c.text(960, 500, 'or', 40, DIM, fd(T(1)) * (1 - ans), w='Bold')

def s_tape(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Adenosine keeps piling up', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'The tape comes off', 66, YE, hl(1), w='Bold')
    off = fd(T(1), .2, 1.6) if T(1) > -.1 else 0.0
    pts = neuron(c, 200, 620, 1200, 790, 5, hl(0))
    for j, (rx, ry) in enumerate(pts):
        k = clamp(off * 5 - j)
        caf(c, rx + 300 * k, ry - 300 * k, hl(0) * (1 - k))
        if k > .6: ade(c, rx, ry - 60 * (1 - k), hl(0) * clamp((k - .6) * 3))
    pile = fd(T(0), 0, 3.0) if T(0) > -.1 else 0.0
    n = int(6 + 26 * pile)
    for i in range(n):
        x = 250 + ((i * 173) % 900) + 10 * math.sin(t * 1.3 + i)
        y = 540 - ((i * 7) % 5) * 46 - (i // 12) * 30 + 8 * math.cos(t + i)
        ade(c, x, y, hl(0) * (1 - .6 * off))
    gauge(c, 1560, 420, 190, hl(0), level=.04, light=1, tape=1 - off, t=t)
    k2 = hl(2)
    c.text(1560, 700, 'The tiredness', 44, INK, k2, w='Bold')
    c.text(1560, 760, 'was there all along', 44, PK, k2 * fd(T(2), .6), w='Bold')

def s_tolerance(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Why it stops working so well', 66, INK, hl(0) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'And if you stop suddenly', 66, PK, hl(2), w='Bold')
    grow = fd(T(1), .4, 2.0) if T(1) > -.1 else 0.0
    n = 5 + int(round(4 * grow))
    k = hl(0) * (1 - .6 * hl(2))
    pts = neuron(c, 200, 640, 1240, 800, n, k, cols=[REC if i < 5 else YE for i in range(n)])
    for j, (rx, ry) in enumerate(pts):
        if j < 5: caf(c, rx, ry, k)
    c.text(720, 870, 'heavy daily use: more receptors can grow', 34, YE, hl(1) * (1 - hl(2)), w='Bold')
    for j in range(3):
        mug(c, 420 + j * 300, 380, 70, hl(0) * fd(T(0), .3 + j * .3) * (1 - .6 * hl(2)), t + j)
    c.text(720, 220, 'same coffee, less effect', 40, CAF, hl(1) * fd(T(1), 1.2) * (1 - hl(2)), w='Bold')
    if T(2) > -.1:
        k2 = hl(2)
        head(c, 1560, 420, 150, k2, ache=fd(T(2), .8), t=t)
        c.text(1560, 680, 'withdrawal headache', 42, PK, k2, w='Bold')
        c.text(1560, 740, 'often starts in 12 to 24 hours', 34, INK, k2 * fd(T(2), .8), w='Medium')

def s_tips(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 120, 'Use the trick well', 66, INK, hl(0), w='Bold')
    tips = [(1, 'Up to 400 mg a day', 'most healthy adults (FDA)', CAF),
            (2, 'Last cup 8+ hours', 'before bed (sleep experts)', CY),
            (3, 'Only sleep', 'fills the tank', GR)]
    for j, (li, title, sub, col) in enumerate(tips):
        k = hl(li); up = 24 * (1 - k)
        if k <= 0: continue
        x = 400 + j * 560
        c.rr(x - 260, 210 + up, x + 260, 740 + up, 30, CARD, k, outline=col, ow=5)
        y = 420 + up
        if j == 0:
            for q in range(3): mug(c, x - 130 + q * 130, y + 30, 42, k * (1 if q < 2 else .55), t + q, CARD)
            c.text(x, y - 120, 'about 2 to 3 big mugs', 28, DIM, k, w='Medium', bg=CARD)
        elif j == 1:
            clock(c, x - 80, y, 80, 2 + 6 * fd(T(2), 0, 2.0), k, CARD)
            bed(c, x + 110, y + 50, 90, k, CARD)
        else:
            bed(c, x - 70, y + 60, 120, k, CARD, col=GR)
            gauge(c, x + 130, y - 40, 80, k, level=.15 + .8 * fd(T(3), .5, 2.0), light=0, t=t, bg=CARD)
        c.text(x, 615 + up, title, 40, col, k, w='Bold', bg=CARD)
        c.text(x, 675 + up, sub, 30, INK, k, w='Medium', bg=CARD)
    c.text(960, 800, 'Pregnant, or on medication? Ask your doctor about caffeine.', 30, DIM, hl(1), w='Medium')

RECAPS = [('1', 'It blocks the tiredness signal', CAF), ('2', 'It lasts for hours', CY), ('3', 'Only sleep fills the tank', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 540 + up
        if i == 0:
            gauge(c, x, y - 30, 130, m, level=.05, light=1, tape=1, t=t, bg=CARD)
        elif i == 1:
            clock(c, x, y - 20, 110, 3 + t * .5, m, CARD)
        else:
            bed(c, x, y, 150, m, CARD, col=GR)
        c.text(x, 740 + up, lab, 32, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Here's a surprise. Caffeine doesn't give you any energy.",
            "It hides how tired you already are.",
            "To see how, picture the warning light on a car's dashboard."], s_hook),
 ('1  ·  THE WARNING LIGHT', ["When the fuel runs low, a light comes on. It doesn't fix anything. It just tells you to stop soon.",
            "Now imagine putting tape over that light.",
            "You'd keep driving, feeling fine. But the tank is just as empty.",
            "Caffeine is that tape."], s_light),
 ('2  ·  THE TIREDNESS SIGNAL', ["Your brain has its own warning light. It's a chemical called adenosine.",
            "The longer you're awake, the more adenosine builds up in your brain.",
            "It lands on tiny receivers on your brain cells, called receptors. The more it lands, the sleepier you feel."], s_signal),
 ('3  ·  THE BLOCKER', ["Caffeine fits into those same receptors.",
            "But it doesn't switch them on. It just sits there, like a key that fits a lock, but won't turn.",
            "So adenosine can't land, and the tiredness signal can't get through."], s_block),
 ('4  ·  HOW LONG IT LASTS', ["Caffeine usually starts working about thirty minutes after you drink it.",
            "Then your body slowly clears it. In an average adult, half of it is gone after about five hours.",
            "But that varies a lot, from about two hours to twelve."], s_timing),
 ('5  ·  QUICK QUESTION', ["Quick question. In a twenty thirteen study, people took caffeine six hours before bed. About as much as two or three cups of coffee. What happened to their sleep?",
            "Three, two, one.",
            "They slept more than an hour less. And they didn't notice."], s_quiz),
 ('6  ·  THE TAPE COMES OFF', ["Meanwhile, the longer you stay awake, the more adenosine builds up.",
            "When the caffeine wears off, the tape comes off the light.",
            "And the tiredness you were hiding is still there."], s_tape),
 ('7  ·  WHY IT FADES', ["Drink a lot of caffeine every day, and your brain adjusts.",
            "Heavy daily use can lead it to make more adenosine receptors. So the same coffee does less.",
            "And if you stop suddenly, many people get a withdrawal headache, usually starting within twelve to twenty-four hours."], s_tolerance),
 ('8  ·  USE IT WELL', ["So how do you use the trick well?",
            "The FDA says most healthy adults can have up to four hundred milligrams a day. That's about two to three big mugs of coffee.",
            "Sleep experts suggest having your last caffeine at least eight hours before bed.",
            "And remember, only sleep actually fills the tank."], s_tips),
 ('RECAP', ["So remember three things.",
            "One. Caffeine doesn't add energy. It blocks your brain's tiredness signal.",
            "Two. It lasts for hours, so an afternoon coffee can steal sleep without you noticing.",
            "Three. When it wears off, the tiredness is still there. Only sleep fills the tank.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["Caffeine doesn't give you any energy.",
                 "It hides how tired you already are.",
                 "Here's the trick."], s_hook),
 ('THE SIGNAL', ["Your brain makes a tiredness chemical, called adenosine.",
                 "The longer you're awake, the more builds up.",
                 "It lands on receptors on your brain cells, and you feel sleepy."], s_signal),
 ('THE BLOCK', ["Caffeine fits into those same receptors.",
                "But it doesn't switch them on, like a key that won't turn.",
                "So the tiredness signal can't get through."], s_block),
 ('THE CATCH', ["But adenosine keeps building up.",
                "When the caffeine wears off,",
                "the tiredness is still there."], s_tape),
 ('THE ANSWER', ["So caffeine doesn't fill your tank. It covers the warning light.",
                 "Only sleep fills the tank. Follow for more."],
                card('Caffeine hides tiredness', 'Only sleep fills the tank')),
]
SHORT_HITS = [(4, 0, 0.0)]
