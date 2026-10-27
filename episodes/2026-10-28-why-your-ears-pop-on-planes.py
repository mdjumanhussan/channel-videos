"""Episode: Your Ears Have a Tiny Door. Here's Why They Pop (air pressure, the Eustachian tube, takeoff vs landing)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "The Tiny Door"                              # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                          # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why do your ears pop on planes?"             # headline on the vertical Short
HITS = [(0, 3, 0.0), (5, 3, 0.0), (6, 2, 0.0)]             # title card, quiz answer, the pop
THUMB = ['YOUR EARS', 'HAVE A', 'TINY DOOR']
MUSIC_LEVEL = 0.006                                         # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                              # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.5, (4, 1): 0.4, (5, 3): 0.6, (6, 2): 0.5}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'fifteen hundred to twenty-four hundred metres': '1,500 to 2,400 metres'}

AIR = (150, 200, 255); DRUM = (255, 150, 110); TUBE = (255, 205, 120); FLESH = (120, 70, 90); FLESH2 = (160, 95, 110)
BAG = (235, 120, 70); SKY = (40, 60, 120)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ell(c, x, y, rx, ry, fill=None, a=1.0, outline=None, ow=3, bg=BG):
    if a <= .01: return
    c.d.ellipse(((x - rx) * c.k, (y - ry) * c.k, (x + rx) * c.k, (y + ry) * c.k),
                fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None, width=int(ow * c.k))

def rnd(i, s):
    """Deterministic pseudo-random number in [0, 1)."""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def air(c, x0, y0, x1, y1, n, a, t, seed=1, col=AIR, bg=BG, r=6):
    """n jiggling air molecules inside a box."""
    if a <= .01: return
    for i in range(int(n)):
        px = x0 + r + (x1 - x0 - 2 * r) * rnd(i, seed) + 5 * math.sin(t * (2 + rnd(i, seed + 3) * 3) + i)
        py = y0 + r + (y1 - y0 - 2 * r) * rnd(i, seed + 7) + 5 * math.cos(t * (2 + rnd(i, seed + 5) * 3) + i * 1.7)
        c.circ(px, py, r, col, a, bg=bg)

def plane(c, x, y, s, a=1.0, ang=0.0, col=INK, bg=BG):
    """Side-view airliner, nose to the right, tilted by ang radians (positive = nose up)."""
    if a <= .01: return
    ca, sa = math.cos(-ang), math.sin(-ang)
    R = lambda pts: [(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts]
    poly(c, R([(-1, -.08), (.75, -.1), (1, 0), (.75, .1), (-1, .08)]), col, a, bg)
    poly(c, R([(-.85, -.07), (-1.02, -.45), (-.86, -.45), (-.6, -.07)]), col, a, bg)
    poly(c, R([(-.1, .02), (-.35, .45), (-.2, .45), (.25, .02)]), mix(col, .75, bg), a, bg)
    for k in range(6):
        c.circ(x + ((.55 - k * .18) * ca) * s, y + ((.55 - k * .18) * sa) * s - 0, s * .025, BG, a, bg=col)

def ear(c, x, y, s, a=1.0, bulge=0.0, door=0.0, n_in=14, n_out=14, t=0.0, hi=None, flow=0.0, bg=BG):
    """Side cross-section of the ear. Eardrum at x; ear canal to the left; middle ear to the right;
    the Eustachian tube runs down-right to the throat, where its 'door' sits.
    bulge: +1 = eardrum bulges outward (left), -1 = inward (right). door: 0 shut .. 1 open.
    flow: +1 air streams out of the middle ear down the tube, -1 streams in. hi: part to highlight."""
    if a <= .01: return
    # head tissue block
    c.rr(x - 520 * s, y - 230 * s, x + 470 * s, y + 330 * s, 50 * s, FLESH, a * .9, bg=bg)
    tb = mix(FLESH, .9, bg)
    # ear canal (outside air), opening at the left edge
    c.rr(x - 540 * s, y - 70 * s, x, y + 70 * s, 20 * s, BG, a, bg=tb)
    air(c, x - 520 * s, y - 62 * s, x - 18 * s, y + 62 * s, n_out, a, t, 3, bg=BG, r=6 * s)
    # middle ear chamber
    c.rr(x, y - 150 * s, x + 260 * s, y + 130 * s, 60 * s, (40, 28, 60), a, bg=tb)
    air(c, x + 16 * s, y - 135 * s, x + 245 * s, y + 115 * s, n_in, a, t, 9, bg=(40, 28, 60), r=6 * s)
    # Eustachian tube: chamber floor down to the throat
    tube = [(x + 180 * s, y + 110 * s), (x + 260 * s, y + 200 * s), (x + 360 * s, y + 280 * s)]
    tw = 34 * s
    for k in range(len(tube) - 1):
        c.line([tube[k], tube[k + 1]], (40, 28, 60), tw, a, tb)
    hc = TUBE if hi == 'tube' else (90, 70, 110)
    c.line(tube, hc, 5 * s, a * (1 if hi == 'tube' else .7), tb)
    # throat space and the door
    c.rr(x + 330 * s, y + 250 * s, x + 470 * s, y + 330 * s, 16 * s, BG, a, bg=tb)
    dx, dy = x + 352 * s, y + 272 * s
    dc = GR if door > .5 else (TUBE if hi == 'door' else (200, 170, 120))
    ang = -0.75 - 1.2 * clamp(door)
    c.line([(dx - 20 * s, dy - 18 * s), (dx - 20 * s + 46 * s * math.cos(ang + 1.6), dy - 18 * s + 46 * s * math.sin(ang + 1.6))], dc, 9 * s, a, BG)
    c.line([(dx + 20 * s, dy + 18 * s), (dx + 20 * s - 46 * s * math.cos(ang + 1.6), dy + 18 * s - 46 * s * math.sin(ang + 1.6))], dc, 9 * s, a, BG)
    # air flowing through the tube
    if abs(flow) > .01:
        for q in range(5):
            ph = (t * 1.2 + q / 5) % 1.0
            u = ph if flow > 0 else 1 - ph
            px = tube[0][0] + (tube[2][0] - tube[0][0]) * u; py = tube[0][1] + (tube[2][1] - tube[0][1]) * u
            c.circ(px, py, 9 * s, AIR, a * abs(flow), bg=(40, 28, 60))
    # eardrum (curved membrane)
    b = clamp(bulge, -1, 1)
    pts = [(x - b * 55 * s * math.sin(math.pi * u / 20), y - 90 * s + 180 * s * u / 20) for u in range(21)]
    c.line(pts, DRUM, (11 if hi == 'drum' else 8) * s, a, tb)

def gauge(c, x, y, r, v, a=1.0, lab='', col=CY, bg=BG):
    """Half-dial gauge, v in 0..1."""
    if a <= .01: return
    arc = [(x - r * math.cos(math.pi * u / 30), y - r * math.sin(math.pi * u / 30)) for u in range(31)]
    c.line(arc, (70, 80, 130), 10, a, bg)
    ang = math.pi * clamp(v)
    c.line([(x, y), (x - r * .85 * math.cos(ang), y - r * .85 * math.sin(ang))], col, 8, a, bg)
    c.circ(x, y, 12, col, a, bg=bg)
    if lab: c.text(x, y + 44, lab, 30, DIM, a, w='Bold', bg=bg)

def snackbag(c, x, y, w, h, puff, a=1.0, t=0.0, bg=BG):
    """Sealed snack bag; puff 0 = flat, 1 = puffed up (sides and faces bulge)."""
    if a <= .01: return
    bx = w * .28 * puff; by = h * .06 * puff
    top, bot = y - h / 2, y + h / 2
    left = [(x - w / 2 - bx * math.sin(math.pi * u / 16), top + h * u / 16) for u in range(17)]
    right = [(x + w / 2 + bx * math.sin(math.pi * u / 16), bot - h * u / 16) for u in range(17)]
    poly(c, [(x - w / 2, top - 18)] + left + [(x - w / 2, bot + 18), (x + w / 2, bot + 18)] + right + [(x + w / 2, top - 18)], BAG, a, bg)
    for k in range(9):
        xx = x - w / 2 + k * w / 8
        c.line([(xx, top - 18), (xx, top)], mix(BAG, .6, BG), 3, a, BAG)
        c.line([(xx, bot), (xx, bot + 18)], mix(BAG, .6, BG), 3, a, BAG)
    ell(c, x - w * .1, y - h * .15, w * .18 * (.3 + puff), h * .25 * (.3 + puff), (255, 170, 120), a * .5 * puff, bg=BAG)
    c.text(x, y - h * .28, 'CHIPS', int(w * .2), INK, a, w='Bold', bg=BAG)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    ear(c, 1430, 470, 0.95, 1.0, bulge=-.8, door=1.0, n_in=10, n_out=18, t=0.3, hi='door', flow=-1.0)
    c.text(1640, 870, 'POP!', 120, YE, 1, w='Bold', stroke=8)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        n1 = max(hl(1), hl(2))
        c.text(960, 150, 'Your ears have a tiny door', 70, INK, a * (1 - n1), w='Bold')
        c.text(960, 150, 'On a plane, it decides how your ears feel', 62, CY, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'It opens more easily one way', 66, YE, a * hl(2), w='Bold')
        # the ear is on screen from frame one; the door swings open on "swallow"
        sw = fd(T(0), 2.4, .3) * (1 - fd(T(0), 3.6, .3))
        k0 = a * (1 - n1)
        if k0 > 0:
            ear(c, 900, 470, 1.0, k0, door=sw, t=t, hi='door')
            c.text(1400, 650, 'opens when you swallow', 40, GR, k0 * fd(T(0), 2.4), 'lm', 'Bold')
        k1 = a * hl(1) * (1 - hl(2))
        if k1 > 0:
            path = lambda u: (260 + 1400 * u, 720 - 420 * math.sin(math.pi * clamp(u)) ** .6)
            c.line([path(u / 40) for u in range(41)], (70, 80, 130), 6, k1)
            u = clamp(T(1) / 4.0)
            px, py = path(u); qx, qy = path(min(1, u + .01))
            plane(c, px, py - 30, 90, k1, math.atan2(-(qy - py), qx - px) if u < .99 else -.15)
            c.text(560, 800, 'takeoff', 36, DIM, k1, w='Bold'); c.text(1360, 800, 'landing', 36, DIM, k1, w='Bold')
            c.text(700, 380, 'fine', 40, GR, k1 * fd(T(1), 1.8), w='Bold')
            c.text(1260, 380, 'blocked and sore?', 40, PK, k1 * fd(T(1), 2.8), w='Bold')
        k2 = a * hl(2)
        if k2 > 0:
            ear(c, 760, 470, .9, k2, door=.5 + .5 * math.sin(t * 3) ** 2, t=t, hi='door')
            c.arrow(1250, 640, 1250, 360, GR, 16, k2 * fd(T(2), .5), 40)
            c.text(1250, 300, 'air out: easy', 42, GR, k2 * fd(T(2), .5), w='Bold')
            c.arrow(1600, 360, 1600, 640, PK, 5, k2 * fd(T(2), 1.5), 20)
            c.text(1600, 700, 'air in: harder', 42, PK, k2 * fd(T(2), 1.5), w='Bold')
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 340 + 30 * (1 - m), 'Your Ears Have a Tiny Door', 108, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), "Here's Why They Pop", 108, YE, m, w='Bold')
        c.line([(960 - 320 * m, 590), (960 + 320 * m, 590)], CY, 8, m)

def s_air(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Air presses on you from every side', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Higher up: less air on top, less push', 64, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A plane cabin: like being up a mountain', 62, YE, hl(2), w='Bold')
    k = hl(0)
    if k <= 0: return
    if hl(2) < 1:
        k0 = k * (1 - hl(2))
        # sea level: tall column of air over a person
        c.rr(260, 780, 860, 800, 6, (60, 110, 170), k0)
        c.text(560, 840, 'sea level', 34, DIM, k0, w='Bold')
        c.circ(560, 690, 26, INK, k0); c.line([(560, 716), (560, 780)], INK, 10, k0)
        air(c, 470, 230, 650, 660, 60, k0 * .9, t, 21)
        for j in range(4):
            ang = j * math.pi / 2 + math.pi / 4
            c.arrow(560 + 110 * math.cos(ang), 690 + 110 * math.sin(ang) * .7, 560 + 50 * math.cos(ang), 690 + 50 * math.sin(ang) * .7, CY, 5, k0 * fd(T(0), .8), 16)
        k1 = k0 * hl(1)
        if k1 > 0:
            poly(c, [(1000, 800), (1400, 420), (1800, 800)], (80, 90, 120), k1)
            poly(c, [(1330, 486), (1400, 420), (1470, 486), (1400, 470)], INK, k1, bg=(80, 90, 120))
            c.circ(1400, 370, 22, INK, k1); c.line([(1400, 392), (1400, 418)], INK, 9, k1)
            air(c, 1320, 200, 1480, 330, 14, k1 * .9, t, 33)
            c.text(1400, 840, 'mountain top', 34, DIM, k1, w='Bold')
            c.text(1510, 250, 'fewer molecules', 30, CY, k1 * fd(T(1), 1.0), 'lm', 'Bold')
            c.text(1510, 292, 'pressing down', 30, CY, k1 * fd(T(1), 1.0), 'lm', 'Bold')
    k2 = hl(2)
    if k2 > 0:
        c.rr(220, 260, 1100, 760, 40, SKY, k2)
        plane(c, 660, 500, 330, k2, 0.0, INK, SKY)
        air(c, 420, 470, 900, 530, 18, k2, t, 41, col=CY, bg=INK, r=7)
        c.text(660, 700, 'the cabin is pressurised, but not to sea level', 30, INK, k2 * fd(T(2), .8), w='Medium', bg=SKY)
        gauge(c, 1450, 520, 170, .62, k2 * fd(T(2), 1.2), 'cabin pressure', YE)
        c.text(1450, 330, 'like 1,500 to 2,400 m up', 40, YE, k2 * fd(T(2), 1.8), w='Bold')
        c.text(1450, 640, 'also: lifts in tall buildings,', 30, DIM, k2 * fd(T(2), 2.6), w='Medium')
        c.text(1450, 680, 'mountain roads', 30, DIM, k2 * fd(T(2), 2.6), w='Medium')

def s_bag(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, "Proof you've seen: the puffed-up snack bag", 58, BAG, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Same air inside, less push outside', 64, INK, hl(1), w='Bold')
    k = hl(0)
    if k <= 0: return
    # altitude bar on the left, bag on the right
    alt = clamp(T(0) / 3.0)
    c.rr(250, 260, 290, 760, 18, (40, 46, 80), k)
    c.rr(250, 760 - 500 * alt, 290, 760, 18, CY, k)
    plane(c, 270, 760 - 500 * alt - 40, 50, k, .3)
    c.text(270, 810, 'height', 30, DIM, k, w='Bold')
    snackbag(c, 540, 520, 200, 300, 0.0, k * fd(T(0), .3))
    c.text(540, 760, 'on the ground', 34, DIM, k * fd(T(0), .3), w='Bold')
    puff = clamp(alt * 1.2)
    snackbag(c, 1050, 520, 200, 300, puff, k * fd(T(0), .8), t)
    c.text(1050, 760, 'at cruising height', 34, BAG, k * fd(T(0), .8), w='Bold')
    k1 = hl(1)
    if k1 > 0:
        # inside arrows push out; outside arrows shrink
        sh = 1 - .6 * fd(T(1), 1.0)
        for sx in (-1, 1):
            c.arrow(1050 + sx * 25, 560, 1050 + sx * 120, 560, INK, 8, k1, 24)
            c.arrow(1050 + sx * 330, 560, 1050 + sx * (330 - 60 * sh), 560, CY, 5, k1, 16)
        c.text(1050, 610, 'inside', 28, INK, k1, w='Bold', bg=BAG)
        c.rr(1430, 330, 1830, 700, 30, CARD, k1 * fd(T(1), 1.2), outline=CY, ow=3)
        c.text(1630, 400, 'inside: sealed at', 34, INK, k1 * fd(T(1), 1.2), w='Bold', bg=CARD)
        c.text(1630, 445, 'ground pressure', 34, INK, k1 * fd(T(1), 1.2), w='Bold', bg=CARD)
        c.text(1630, 540, 'outside: pushes', 34, CY, k1 * fd(T(1), 2.0), w='Bold', bg=CARD)
        c.text(1630, 585, 'less up high', 34, CY, k1 * fd(T(1), 2.0), w='Bold', bg=CARD)

def s_ear(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Your middle ear: a pocket of air', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'The eardrum: a thin skin, like a drum', 64, DRUM, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A narrow tube to your throat. Usually shut.', 60, TUBE, hl(2), w='Bold')
    k = hl(0)
    if k <= 0: return
    hi = 'tube' if hl(2) > .5 else ('drum' if hl(1) > .5 else None)
    ear(c, 820, 470, 1.0, k, t=t, hi=hi)
    c.text(400, 680, 'ear canal', 32, DIM, k * fd(T(0), .4), w='Bold')
    c.text(1060, 360, 'middle ear', 34, CY, k * fd(T(0), .8) * (1 - hl(1)), 'lm', 'Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.arrow(700, 470, 800, 470, CY, 7, k1 * fd(T(1), 1.2), 22)
        c.arrow(940, 470, 840, 470, CY, 7, k1 * fd(T(1), 1.2), 22)
        c.text(820, 300, 'eardrum', 36, DRUM, k1, w='Bold')
        c.rr(1350, 360, 1650, 600, 30, CARD, k1, outline=DRUM)
        ell(c, 1500, 420, 120, 30, (240, 225, 200), k1, bg=CARD)
        c.rr(1380, 420, 1620, 560, 10, (180, 60, 60), k1, bg=CARD)
        c.text(1500, 650, 'equal push both sides', 34, CY, k1 * fd(T(1), 1.6), w='Bold')
        c.text(1500, 695, 'works best', 34, CY, k1 * fd(T(1), 1.6), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        c.text(1500, 560, 'Eustachian tube', 40, TUBE, k2, w='Bold')
        c.text(1500, 610, 'to the back of your', 32, DIM, k2, w='Medium')
        c.text(1500, 650, 'nose and throat', 32, DIM, k2, w='Medium')
        c.arrow(1340, 590, 1220, 700, TUBE, 5, k2 * fd(T(2), .6), 18)

def s_up(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Takeoff: the eardrum bulges outward', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Extra air slips out by itself', 66, GR, hl(1), w='Bold')
    k = hl(0)
    if k <= 0: return
    b = fd(T(0), .6, 1.6)
    pop = fd(T(1), 2.2, .25)
    door = fd(T(1), 1.4, .3) * (1 - fd(T(1), 3.4, .4))
    bulge = b * (1 - pop)
    n_out = 14 - 6 * b
    ear(c, 760, 470, 1.0, k, bulge=bulge, door=door, n_in=14 - 6 * pop, n_out=n_out, t=t, hi='drum' if hl(1) < .5 else 'door',
        flow=door if T(1) > 0 else 0)
    plane(c, 1560, 360 - 60 * clamp(T(0) / 4), 110, k, .35)
    c.arrow(1700, 520, 1700, 300, CY, 6, k * fd(T(0), .4), 20)
    c.text(1560, 560, 'cabin pressure drops', 34, CY, k * fd(T(0), .4), w='Bold')
    c.text(400, 320, 'pushed out', 34, DRUM, k * b * (1 - pop), w='Bold')
    c.text(1560, 660, 'feels full, muffled', 34, DIM, k * fd(T(0), 2.2) * (1 - hl(1)), w='Bold')
    if pop > 0:
        s = 1 + .3 * (1 - pop)
        c.text(560, 470, 'POP', int(90 * s), YE, pop * (1 - fd(T(1), 4.0, .6) * .6), w='Bold', stroke=6)
        c.text(1560, 660, 'balanced again', 36, GR, pop, w='Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 215, 'Coming down to land, which way does your eardrum bend?', 42, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'B: inward', 70, GR, ans, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        plane(c, 960, 480, 200, k0, -.3)
        c.arrow(1220, 380, 1220, 640, CY, 6, k0 * fd(T(0), 1.0), 22)
        c.text(1220, 700, 'descending', 34, CY, k0 * fd(T(0), 1.0), w='Bold')
    kc = hl(1) * (1 - ans)
    if kc > 0:
        for j, (lab, l1, x, bl) in enumerate((('A', 'outward', 560, 1.0), ('B', 'inward', 1360, -1.0))):
            kk = kc * (.3 + .7 * fd(T(1), j * 1.2))
            c.rr(x - 330, 290, x + 330, 720, 34, CARD, kk, outline=CY, ow=3)
            c.circ(x - 270, 340, 38, CY, kk, bg=CARD); c.text(x - 270, 340, lab, 44, BG, kk, w='Bold', bg=CY)
            ear(c, x + 20, 470, .42, kk, bulge=bl * (.6 + .4 * math.sin(t * 3) ** 2), t=t, bg=CARD)
            c.text(x, 670, l1, 42, INK, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        ring(c, 960, 500, 70, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        ear(c, 760, 480, .95, ans, bulge=-fd(T(3), .3, 1.0), n_in=8, n_out=22, t=t, hi='drum')
        c.text(390, 330, 'more air out here', 32, CY, ans * fd(T(3), 1.0), w='Bold')
        c.text(1150, 300, 'less air in here', 32, PK, ans * fd(T(3), 1.6), w='Bold')
        c.rr(1380, 420, 1820, 620, 30, CARD, ans * fd(T(3), 2.4), outline=PK, ow=3)
        c.text(1600, 485, 'the cabin squeezes', 34, INK, ans * fd(T(3), 2.4), w='Bold', bg=CARD)
        c.text(1600, 545, 'the eardrum in', 34, INK, ans * fd(T(3), 2.4), w='Bold', bg=CARD)

def s_down(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, "Coming down, air can't push the tube open", 58, PK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'You open it: swallow or yawn', 66, GR, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Air rushes in. The eardrum snaps back.', 62, YE, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j, (lab, x, ok) in enumerate((('going up', 560, True), ('coming down', 1360, False))):
            kk = k0 * fd(T(0), j * 1.0)
            c.rr(x - 330, 260, x + 330, 760, 34, CARD, kk, outline=GR if ok else PK, ow=3)
            ear(c, x - 20, 470, .5, kk, bulge=.7 if ok else -.7, door=(.6 + .4 * math.sin(t * 4) ** 2) if ok else 0.0,
                n_in=12 if ok else 6, n_out=6 if ok else 14, t=t, flow=.9 if ok else 0, bg=CARD)
            c.text(x, 690, lab, 40, GR if ok else PK, kk, w='Bold', bg=CARD)
            if ok: c.check(x + 240, 330, 44, GR, kk, fd(T(0), 1.0))
            else: c.cross(x + 240, 330, 60, PK, kk * fd(T(0), 2.0))
        c.text(960, 820, 'the tube resists opening that way', 34, DIM, k0 * fd(T(0), 2.4), w='Medium')
    k1 = max(hl(1), 0)
    if k1 > 0:
        door = fd(T(1), 1.4, .3) if hl(2) < 1 else 1.0
        snap = fd(T(2), .6, .25)
        ear(c, 760, 470, 1.0, k1, bulge=-(1 - snap), door=door * (1 - fd(T(2), 2.6, .4)), n_in=6 + 8 * snap, n_out=14,
            t=t, flow=-door * (1 - snap * .7), hi='door')
        k1a = k1 * (1 - hl(2))
        if k1a > 0:
            # a throat swallowing: a glass of water and a yawn
            c.rr(1460, 380, 1560, 560, 12, (90, 150, 220), k1a * fd(T(1), .3))
            c.rr(1460, 440, 1560, 560, 12, CY, k1a * fd(T(1), .3))
            ell(c, 1700, 470, 70, 80, (225, 180, 150), k1a * fd(T(1), .9))
            ell(c, 1700, 500, 28, 36 * (.6 + .4 * math.sin(t * 2) ** 2), (80, 30, 40), k1a * fd(T(1), .9), bg=(225, 180, 150))
            c.text(1510, 620, 'swallow', 34, CY, k1a * fd(T(1), .3), w='Bold')
            c.text(1700, 620, 'yawn', 34, CY, k1a * fd(T(1), .9), w='Bold')
            c.text(1600, 720, 'landing: often harder', 36, PK, k1a * fd(T(1), 2.0), w='Bold')
        if snap > 0:
            s = 1 + .3 * (1 - snap)
            c.text(560, 470, 'POP', int(90 * s), YE, snap * (1 - fd(T(2), 4.0, .6) * .6), w='Bold', stroke=6)
            c.text(1580, 520, 'balanced again', 44, GR, hl(2) * snap, w='Bold')

def s_help(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'On the way down: help the tube open', 62, GR, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Stay awake for landing', 66, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, "Children's tubes: shorter and flatter", 62, CY, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Colds can block the tube', 66, PK, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        items = [('swallow', CY), ('yawn', CY), ('chew gum', GR), ('suck a sweet', YE)]
        for j, (lab, col) in enumerate(items):
            x = 330 + j * 420; kk = k0 * fd(T(0), .5 + j * .5)
            c.rr(x - 180, 300, x + 180, 720, 30, CARD, kk, outline=col, ow=3)
            if j == 0:
                c.rr(x - 50, 400, x + 50, 580, 12, (90, 150, 220), kk, bg=CARD); c.rr(x - 50, 460, x + 50, 580, 12, CY, kk, bg=CARD)
            elif j == 1:
                ell(c, x, 490, 90, 100, (225, 180, 150), kk, bg=CARD)
                ell(c, x, 520, 34, 44 * (.6 + .4 * math.sin(t * 2) ** 2), (80, 30, 40), kk, bg=(225, 180, 150))
                ell(c, x - 35, 450, 18, 6, (60, 40, 40), kk, bg=(225, 180, 150)); ell(c, x + 35, 450, 18, 6, (60, 40, 40), kk, bg=(225, 180, 150))
            elif j == 2:
                c.rr(x - 90, 450, x + 90, 530, 16, (240, 240, 245), kk, bg=CARD); c.rr(x - 90, 482, x + 90, 498, 4, GR, kk, bg=(240, 240, 245))
            else:
                ell(c, x, 490, 60, 60, YE, kk, bg=CARD)
                poly(c, [(x - 60, 490), (x - 120, 450), (x - 120, 530)], YE, kk, CARD); poly(c, [(x + 60, 490), (x + 120, 450), (x + 120, 530)], YE, kk, CARD)
            c.text(x, 660, lab, 38, INK, kk, w='Bold', bg=CARD)
        c.text(960, 800, 'each one helps the tube open', 32, DIM, k0 * fd(T(0), 2.6), w='Medium')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        ell(c, 760, 480, 150, 170, (225, 180, 150), k1)
        for sx in (-1, 1):
            c.line([(760 + sx * 70, 440), (760 + sx * 30, 440)], (60, 40, 40), 7, k1, (225, 180, 150))
        for q in range(3):
            c.text(960 + q * 60, 330 - q * 50, 'z', 50 + q * 14, DIM, k1 * (.4 + .6 * math.sin(t * 2 + q) ** 2), w='Bold')
        c.cross(1020, 290, 70, PK, k1 * fd(T(1), 1.0))
        c.text(1400, 440, 'asleep, you swallow less', 40, INK, k1 * fd(T(1), 1.4), w='Bold')
        c.text(1400, 510, 'and do not yawn', 40, INK, k1 * fd(T(1), 1.4), w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        for j, (lab, x, dx, dy) in enumerate((('adult', 560, 140, 160), ('young child', 1360, 130, 50))):
            kk = k2 * fd(T(2), j * .8)
            c.rr(x - 300, 280, x + 300, 720, 30, CARD, kk)
            c.rr(x - 200, 380, x - 80, 470, 30, (90, 60, 120), kk, bg=CARD)
            c.line([(x - 120, 460), (x - 120 + dx, 460 + dy)], TUBE, 30, kk, CARD)
            c.text(x, 670, lab, 40, INK, kk, w='Bold', bg=CARD)
        c.text(1360, 760, 'blocks more easily', 32, CY, k2 * fd(T(2), 1.4), w='Bold')
        c.text(960, 820, 'a bottle or pacifier at landing helps a baby swallow', 32, DIM, k2 * fd(T(2), 2.6), w='Medium')
    k3 = hl(3)
    if k3 > 0:
        ear(c, 760, 470, .95, k3, bulge=-.8, n_in=6, n_out=16, t=t)
        ell(c, 760 + 260 * .95, 470 + 200 * .95, 40, 30, (150, 200, 90), k3 * fd(T(3), .6), bg=FLESH)
        c.text(1500, 420, 'mucus can plug it', 40, PK, k3 * fd(T(3), .6), w='Bold')
        c.rr(1260, 500, 1760, 680, 30, CARD, k3 * fd(T(3), 2.6), outline=YE, ow=3)
        c.text(1510, 560, 'pain lasting more than', 32, INK, k3 * fd(T(3), 2.6), w='Bold', bg=CARD)
        c.text(1510, 610, 'a few days? See a doctor.', 32, YE, k3 * fd(T(3), 2.6), w='Bold', bg=CARD)

RECAPS = [('1', 'Equal push', 'both sides of', 'the eardrum', CY),
          ('2', 'Going up', 'extra air slips', 'out by itself', GR),
          ('3', 'Coming down', 'swallow or yawn', 'to open the tube', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 160, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, l1, l2, l3, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; dy = 40 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        c.rr(x - 240, 290 + dy, x + 240, 760 + dy, 36, CARD, m, outline=col, ow=4)
        c.circ(x, 370 + dy, 46, col, m, bg=CARD); c.text(x, 370 + dy, nn, 52, BG, m, w='Bold', bg=col)
        c.text(x, 490 + dy, l1, 52, col, m, w='Bold', bg=CARD)
        c.text(x, 580 + dy, l2, 38, INK, m, w='Bold', bg=CARD)
        c.text(x, 630 + dy, l3, 38, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Your ears have a tiny door, and you open it every time you swallow.",
            "On a plane, that door decides whether your ears feel fine, or blocked and sore.",
            "And it opens more easily one way than the other.",
            "Here's why your ears pop."], s_hook),
 ('1  ·  AIR PUSHES', ["Air is always pressing on you, from every side.",
            "At sea level, there's a tall stack of air above you. On a mountain, there's less air on top, so it presses less.",
            "A plane's cabin is kept at a pressure like being on a mountain, about fifteen hundred to twenty-four hundred metres up."], s_air),
 ('2  ·  THE SNACK BAG', ["You've seen the proof. A sealed bag of chips puffs up on a flight.",
            "The air inside was sealed in at ground pressure. Up high, the air outside pushes less, so the air inside spreads out."], s_bag),
 ('3  ·  INSIDE YOUR EAR', ["Your ear has a sealed pocket of air too. It's called the middle ear.",
            "Your eardrum, a thin skin like the top of a drum, sits in front of it. It works best when air pushes equally on both sides.",
            "A narrow tube links that pocket to the back of your nose and throat. Most of the time, it's shut."], s_ear),
 ('4  ·  GOING UP', ["On takeoff, the cabin pressure drops. The air in your middle ear now pushes harder, so your eardrum bulges outward.",
            "That feels full and muffled. But the extra air usually pushes the tube open and slips out by itself."], s_up),
 ('5  ·  QUICK QUESTION', ["Quick question. Coming down to land, which way does your eardrum bend?",
            "A: outward. Or B: inward.",
            "Three, two, one.",
            "B. Inward. The cabin air is getting denser, and your middle ear now has less air than the cabin."], s_quiz),
 ('6  ·  COMING DOWN', ["Now air has to get back in. But this time it can't simply push the tube open. The tube resists opening that way.",
            "You have to open it, by swallowing or yawning. That's why landing is often the harder part.",
            "When it opens, air rushes in, your eardrum snaps back, and you hear the pop."], s_down),
 ('7  ·  WHAT HELPS', ["So on the way down, swallow, yawn, chew gum, or suck a sweet. Each one helps the tube open.",
            "Stay awake for landing. Asleep, you swallow less, and you don't yawn.",
            "Young children's tubes are shorter and flatter, and block more easily. A bottle or pacifier helps a baby swallow.",
            "A cold can plug the tube with mucus. And if ear pain lasts more than a few days, see a doctor."], s_help),
 ('RECAP', ["So remember three things.",
            "One. Your eardrum works best when air pushes equally on both sides.",
            "Two. Going up, extra air slips out by itself.",
            "Three. Coming down, you have to open the tube. So swallow or yawn.",
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

# The Short: its own complete mini-story (hook -> the tube -> up -> down -> answer).
SHORT_SCENES = [
 ('THE DOOR', ["Why do your ears pop on a plane? Because your ears have a tiny door, and you open it every time you swallow.",
               "It's a narrow tube from the air pocket behind your eardrum to the back of your throat."],
              remap(s_ear, {0: 0, 1: (0, 2.6), 2: 1})),
 ('GOING UP', ["Going up, the cabin pressure drops, and the air behind your eardrum pushes it outward.",
               "That extra air usually slips out through the tube by itself. Pop."],
              remap(s_up, {0: 0, 1: 1})),
 ('COMING DOWN', ["Coming down, the cabin air pushes your eardrum inward. Now air has to get back in, through the tube.",
                  "But the tube won't just push open that way. You have to open it."],
                 remap(s_down, {0: 0, 1: (1, 0.0)})),
 ('THE ANSWER', ["So when you land, swallow or yawn.",
                 "The tube opens, air rushes in, and your ears pop."],
                card('Landing? Swallow or yawn.', 'The tube opens. Pop.')),
]
SHORT_HITS = [(3, 0, 0.0)]
