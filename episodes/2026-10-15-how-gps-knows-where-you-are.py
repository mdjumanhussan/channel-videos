"""Episode: How GPS Knows Where You Are."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How GPS Knows Where You Are'      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
SHORT_HOOK = 'How does GPS know where you are?'  # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 2, 0.0), (6, 2, 0.0)]  # title card, quiz answer, Einstein's 38 millionths
THUMB = ['HOW GPS', 'FINDS YOU']
MUSIC_LEVEL = 0.006                              # keeps the music about 20 dB under the voice (lesson of 2026-10-14)
# Applied lesson (learnings.md, 2026-10-15): motion in the very first second. The opening frame already
# has satellites drifting and signal pulses travelling to the phone, with the hook text on screen from t = 0.

SAT = (210, 215, 235); PANEL = (70, 140, 230); OCEAN = (40, 105, 200); LAND = (80, 190, 120)
SIG = CY; DOT = (70, 150, 255)

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def sat(c, x, y, s, a=1.0, bg=BG, hi=None):
    """Satellite: body with two solar panels. s = overall half-width."""
    if a <= 0.01: return
    b = s * .28
    c.line([(x - s, y), (x + s, y)], (120, 130, 170), max(2, s * .06), a, bg)
    for sg in (-1, 1):
        c.rr(x + sg * s * .42 - s * .3, y - s * .22, x + sg * s * .42 + s * .3, y + s * .22, 3, PANEL, a, bg=bg)
        c.line([(x + sg * s * .42, y - s * .22), (x + sg * s * .42, y + s * .22)], (40, 80, 150), max(1, s * .03), a, bg)
    c.rr(x - b, y - b, x + b, y + b, 4, hi or SAT, a, bg=bg)
    c.line([(x, y + b), (x, y + b + s * .2)], SAT, max(2, s * .05), a, bg)
    c.circ(x, y + b + s * .24, s * .07, hi or SAT, a, bg=bg)

def phone(c, x, y, h, a=1.0, bg=BG, t=0.0, dot=True, glow=0.0):
    """Phone centred on (x, y), height h, with a pulsing blue location dot."""
    if a <= 0.01: return
    w = h * .5
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h * .09, (44, 50, 88), a, outline=mix(SIG, glow, (90, 100, 150)), ow=max(3, h * .015), bg=bg)
    c.rr(x - w / 2 + h * .04, y - h / 2 + h * .07, x + w / 2 - h * .04, y + h / 2 - h * .07, h * .05, (24, 40, 64), a, bg=(44, 50, 88))
    sc = (24, 40, 64)
    for k in range(3):                                                   # simple map lines
        c.line([(x - w / 2 + h * .05, y - h * .2 + k * h * .17), (x + w / 2 - h * .05, y - h * .12 + k * h * .17)], (50, 70, 100), max(2, h * .012), a, sc)
    if dot:
        p = (t * .9) % 1
        c.circ(x, y, h * (.05 + .1 * p), None, a * (1 - p), outline=DOT, ow=max(2, h * .01), bg=sc)
        c.circ(x, y, h * .045, DOT, a, outline=INK, ow=max(2, h * .01), bg=sc)

def earth(c, x, y, r, a=1.0, bg=BG, t=0.0):
    if a <= 0.01: return
    c.circ(x, y, r * 1.06, None, a * .5, outline=CY, ow=max(2, r * .02), bg=bg)
    c.circ(x, y, r, OCEAN, a, bg=bg)
    for dx, dy, rr_ in ((-.35, -.3, .32), (-.15, -.05, .25), (.38, .1, .28), (.25, .45, .2), (-.4, .4, .15)):
        xx = x + r * (dx + .04 * math.sin(t * .3))
        c.circ(xx, y + r * dy, r * rr_, LAND, a * .9, bg=OCEAN)

def packets(c, x0, y0, x1, y1, t, col=SIG, a=1.0, n=3, speed=.7, r=7, line=True):
    """Signal travelling from (x0, y0) to (x1, y1): faint path plus moving pulses."""
    if a <= 0.01: return
    if line: c.line([(x0, y0), (x1, y1)], col, 2, a * .25)
    for k in range(n):
        p = (t * speed + k / n) % 1
        c.circ(x0 + (x1 - x0) * p, y0 + (y1 - y0) * p, r, col, a * math.sin(math.pi * p))

def clock(c, x, y, r, col, a=1.0, t=0.0, bg=BG, speed=1.0):
    if a <= 0.01: return
    c.circ(x, y, r, CARD, a, outline=col, ow=max(3, r * .07), bg=bg)
    for k in range(12):
        q = k * math.pi / 6
        c.line([(x + r * .78 * math.sin(q), y - r * .78 * math.cos(q)), (x + r * .88 * math.sin(q), y - r * .88 * math.cos(q))], DIM, max(2, r * .03), a, CARD)
    q1 = t * speed; q2 = t * speed / 12
    c.line([(x, y), (x + r * .65 * math.sin(q1), y - r * .65 * math.cos(q1))], col, max(3, r * .06), a, CARD)
    c.line([(x, y), (x + r * .42 * math.sin(q2), y - r * .42 * math.cos(q2))], INK, max(3, r * .08), a, CARD)
    c.circ(x, y, r * .07, col, a, bg=CARD)

def opt(cx, cy, rx, ry, tilt, th):
    x, y = rx * math.cos(th), ry * math.sin(th)
    return cx + x * math.cos(tilt) - y * math.sin(tilt), cy + x * math.sin(tilt) + y * math.cos(tilt)

def orbit(c, cx, cy, rx, ry, tilt, a=1.0, col=(60, 70, 120)):
    c.line([opt(cx, cy, rx, ry, tilt, k * math.pi / 40) for k in range(81)], col, 2, a)

def pin(c, x, y, s, col, a=1.0, bg=BG):
    """Map pin with its tip at (x, y)."""
    if a <= 0.01: return
    c.d.polygon([((x - s * .5) * c.k, (y - s * 1.1) * c.k), ((x + s * .5) * c.k, (y - s * 1.1) * c.k), (x * c.k, y * c.k)], fill=mix(col, a, bg))
    c.circ(x, y - s * 1.25, s * .55, col, a, bg=bg)
    c.circ(x, y - s * 1.25, s * .22, BG, a, bg=col)

def building(c, x0, w, h, a=1.0, base=820):
    c.rr(x0, base - h, x0 + w, base, 6, (48, 56, 98), a)
    for i in range(int(h // 60)):
        for j in range(int(w // 50)):
            c.rr(x0 + 14 + j * 50, base - h + 18 + i * 60, x0 + 36 + j * 50, base - h + 44 + i * 60, 3, (90, 100, 150), a * .7, bg=(48, 56, 98))

def thumb_art(c):
    earth(c, 1500, 1020, 420)
    for x, y in ((1220, 230), (1500, 150), (1780, 260)):
        packets(c, x, y, 1500, 640, 0.0, SIG, 1, 3, r=12)
        sat(c, x, y, 95)
    phone(c, 1500, 640, 330, glow=1)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(3), 0, .5)
    if a > 0:
        # moving from the very first frame: satellites drift, pulses travel to the phone
        sats = [(360 + 14 * t, 230 + 25 * math.sin(t * .5)), (960 + 10 * t, 180), (1560 + 14 * t, 240 - 25 * math.sin(t * .5))]
        for i, (x, y) in enumerate(sats):
            packets(c, x, y + 30, 960, 430, t + i * .2, SIG, a, 3, .55, 8)
            sat(c, x, y, 70, a)
        listen = fd(T(2)) if T(2) > -.1 else 0.0
        phone(c, 960, 520, 300, a, t=t, glow=listen)
        k0 = a * (1 - (fd(T(1), 0, .4) if T(1) > -.1 else 0))
        c.text(960, 780, 'Your phone knows where you are', 70, INK, k0, w='Bold')
        if T(1) > -.1:
            k = a * fd(T(1)) * (1 - (fd(T(2), 0, .4) if T(2) > -.1 else 0))
            for dx in (-140, 140):
                c.arrow(960 + dx, 560, 960 + dx * 1.6, 400, PK, 7, k, 22)
            c.cross(960 + 1.3 * 140, 470, 70, PK, k); c.cross(960 - 1.3 * 140, 470, 70, PK, k)
            pill(c, 960, 780, 'It sends nothing to space', PK, k, 44, h=80)
        if T(2) > -.1:
            pill(c, 960, 780, 'It only listens', GR, a * fd(T(2)), 48, h=84)
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 370 + 30 * (1 - m), 'How GPS', 160, INK, m, w='Bold')
        c.text(960, 545 + 30 * (1 - m), 'Knows Where You Are', 120, YE, m, w='Bold')
        c.line([(960 - 320 * m, 650), (960 + 320 * m, 650)], CY, 8, m)
        sat(c, 1640, 250, 80, fd(T(3), .9))
        packets(c, 1640, 290, 1400, 480, t, SIG, fd(T(3), .9), 3, .6, 7)
        c.text(960, 740, 'by only listening', 46, DIM, fd(T(3), 1.1), w='Medium')

def s_sats(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(3), -.4, .4))
    EX, EY = 960, 520
    orbs = [(330, 150, -.35), (330, 150, .35), (300, 300, 0)]
    if a0 > 0:
        for (rx, ry, tl_) in orbs: orbit(c, EX, EY, rx, ry, tl_, a0)
        earth(c, EX, EY, 150, a0, t=t)
        pos = []
        for oi, (rx, ry, tl_) in enumerate(orbs):
            for k in range(4):
                th = t * .25 + k * math.pi / 2 + oi * .6
                x, y = opt(EX, EY, rx, ry, tl_, th); pos.append((x, y))
        hl = fd(T(2)) if T(2) > -.1 else 0.0
        # the four satellites closest to the person at the top of the Earth light up
        near = sorted(range(len(pos)), key=lambda i: math.hypot(pos[i][0] - EX, pos[i][1] - (EY - 150)))[:4]
        for i, (x, y) in enumerate(pos):
            if i in near and hl > 0:
                c.line([(EX, EY - 150), (x, y)], YE, 3, a0 * hl * .8)
            sat(c, x, y, 30, a0, hi=YE if (i in near and hl > .5) else None)
        if hl > 0:
            c.circ(EX, EY - 150, 12, YE, a0 * hl, bg=LAND)
        k = a0 * fd(T(0), .4)
        c.text(240, 420, '30+', 140, YE, k, w='Bold')
        c.text(240, 520, 'GPS satellites', 40, INK, k, w='Bold')
        if T(1) > -.1:
            k = a0 * fd(T(1))
            c.text(1680, 380, '~20,200 km', 64, CY, k, w='Bold')
            c.text(1680, 440, 'above the ground', 36, INK, k, w='Medium')
            c.text(1680, 560, '2 laps', 64, CY, k * fd(T(1), 1.2), w='Bold')
            c.text(1680, 620, 'around Earth a day', 36, INK, k * fd(T(1), 1.2), w='Medium')
        if T(2) > -.1:
            pill(c, 960, 840, 'At least 4 in view from almost anywhere', YE, a0 * fd(T(2), .4), 36, h=70)
        c.text(1880, 870, 'Not to scale', 26, DIM, a0, 'rm', 'Regular')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 190, 'What every satellite broadcasts', 62, INK, m, w='Bold')
    sat(c, 470, 500, 190, m)
    c.rr(345, 690, 595, 760, 35, GR, m * fd(T(3), .6))
    c.text(470, 725, 'atomic clock', 30, BG, m * fd(T(3), .6), w='Bold', bg=GR)
    packets(c, 690, 500, 930, 500, t, SIG, m, 3, .8, 9)
    c.rr(980, 330, 1760, 660, 30, CARD, m, outline=SIG, ow=5)
    c.text(1030, 400, '1.  Where I am', 52, INK, m * fd(T(3), .9), 'lm', 'Bold', bg=CARD)
    c.text(1030, 500, '2.  The exact time', 52, YE, m * fd(T(3), 2.2), 'lm', 'Bold', bg=CARD)
    c.text(1030, 580, '     09:41:07.000000000', 40, DIM, m * fd(T(3), 2.6), 'lm', 'Mono', bg=CARD)
    c.text(1370, 720, 'Simplified, example time', 26, DIM, m, w='Regular')

def s_signal(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if a0 > 0:
        c.text(960, 190, 'Flash first, thunder later', 62, INK, a0, w='Bold')
        # storm cloud
        for dx, dy, r in ((-.45, .1, .32), (0, -.1, .45), (.45, .1, .32)):
            c.circ(420 + dx * 220, 350 + dy * 220, r * 220, (90, 98, 140), a0)
        c.rr(420 - 165, 361, 420 + 165, 442, 40, (90, 98, 140), a0)
        tb = T(1)
        flash = 0.0 if tb < .2 else max(0, 1 - (tb - .2) / .5)
        bolt = [(440, 440), (380, 560), (430, 560), (370, 700), (500, 530), (445, 530), (500, 440)]
        c.d.polygon([(x * c.k, y * c.k) for x, y in bolt], fill=mix(YE, a0 * max(.25, flash)))
        # person
        X = 1500
        c.circ(X, 520, 34, (230, 235, 250), a0)
        c.rr(X - 40, 565, X + 40, 700, 20, (230, 235, 250), a0)
        if tb > 0:
            p = clamp((tb - .2) / 3.2)
            for k in range(3):
                pr = p - k * .06
                if 0 < pr < 1:
                    rx = 540 + (X - 600) * pr
                    c.line([(rx - 10, 470), (rx + 25, 560), (rx - 10, 650)], PK, 6, a0 * (1 - k * .3))
            n = min(3, int(clamp((tb - .2) / 3.2) * 3 + .001) + (1 if tb > .2 else 0))
            nn = max(1, min(3, n)); c.text(960, 790, (f'{nn} second' + ('s' if nn > 1 else '')) if tb > .2 else '', 60, YE, a0, w='Bold')
            c.text(960, 850, 'longer wait = farther away', 32, DIM, a0 * fd(tb, 1.5), w='Medium')
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 190, 'GPS times a radio signal', 62, INK, m * (1 - fd(T(4), -.4, .4)), w='Bold')
    a1 = m * (1 - fd(T(4), -.4, .4))
    if a1 > 0:
        sat(c, 420, 380, 110, a1)
        phone(c, 1460, 520, 300, a1, t=t)
        packets(c, 470, 420, 1400, 470, t, SIG, a1, 4, .5, 10)
        if T(3) > -.1:
            k = fd(T(3)) * a1
            c.rr(250, 560, 760, 700, 24, CARD, k, outline=SIG, ow=4)
            c.text(505, 600, 'Sent', 34, DIM, k, w='Medium', bg=CARD)
            c.text(505, 655, '09:41:07.000', 46, INK, k, w='Bold', bg=CARD)
            kk = k * fd(T(3), 1.4)
            c.rr(1160, 720, 1760, 860, 24, CARD, kk, outline=YE, ow=4)
            c.text(1460, 760, 'Arrived', 34, DIM, kk, w='Medium', bg=CARD)
            c.text(1460, 815, '09:41:07.070', 46, YE, kk, w='Bold', bg=CARD)
            c.text(505, 750, 'Example times', 26, DIM, k, w='Regular')
    if T(4) < -.1: return
    m = fd(T(4))
    c.text(960, 190, 'Delay becomes distance', 64, INK, m, w='Bold')
    c.rr(260, 330, 1660, 520, 30, CARD, m, outline=YE, ow=5)
    c.text(960, 425, 'delay  ×  speed of light  =  distance', 58, YE, m, w='Bold', bg=CARD)
    k = m * fd(T(4), 1.2)
    c.text(960, 630, '0.07 s  ×  300,000 km/s  ≈  21,000 km', 54, INK, k, w='Bold')
    c.text(960, 710, 'Example', 28, DIM, k, w='Regular')

A_, B_, C_, P_ = (640, 470), (1280, 470), (1150, 615), (960, 560)
def _r(o): return math.hypot(o[0] - P_[0], o[1] - P_[1])
Q_ = (P_[0], 2 * A_[1] - P_[1])        # the other place where circles A and B meet
def s_pin(c, T, t):
    m = fd(T(0))
    c.text(960, 190, 'One distance is not enough', 56, INK, m * (1 - fd(T(1), -.3, .4)), w='Bold')
    for i, (o, li, col) in enumerate([(A_, 1, CY), (B_, 2, PU), (C_, 3, PK)]):
        if T(li) < -.1: continue
        k = fd(T(li)); g = ease(clamp(T(li) / 1.2))
        r = _r(o)
        pts = [(o[0] + r * math.cos(u * 2 * math.pi * g / 90 - math.pi / 2), o[1] + r * math.sin(u * 2 * math.pi * g / 90 - math.pi / 2)) for u in range(91)]
        c.line(pts, col, 5, k)
        sat(c, o[0], o[1], 46, k)
    if T(1) > -.1 and T(2) < .5:
        k = fd(T(1), 1.0) * (1 - fd(T(2), 0, .5))
        c.text(1700, 160, 'You could be', 40, CY, k, w='Bold'); c.text(1700, 215, 'anywhere on this', 40, CY, k, w='Bold')
    if T(2) > -.1:
        k = fd(T(2), 1.0)
        qa = k * (1 - (fd(T(3), 1.0) if T(3) > -.1 else 0))
        pk = fd(T(3), 1.1) if T(3) > -.1 else 0.0
        for (x, y), aa in ((P_, k * (1 - pk)), (Q_, qa)):
            c.circ(x, y, 16 + 4 * math.sin(t * 5), YE, aa)
        c.text(1890, 850, '2 possible spots', 40, YE, k * (1 - (fd(T(3), 1.0) if T(3) > -.1 else 0)), 'rm', 'Bold')
    if T(3) > -.1:
        k = fd(T(3), 1.1)
        pin(c, P_[0], P_[1], 40, YE, k)
        c.text(1890, 850, 'One spot left', 44, GR, k, 'rm', 'Bold')
    if T(4) > 0:
        pill(c, 1620, 190, 'Trilateration', YE, fd(T(4)), 48, h=80)
    c.text(40, 870, 'Drawn flat, simplified', 26, DIM, m, 'lm', 'Regular')

def s_quiz(c, T, t):
    a0 = 1 - fd(T(2), -.4, .4)
    if a0 > 0:
        m = fd(T(0)) * a0
        c.text(960, 190, 'Quick question', 70, YE, m, w='Bold')
        c.text(960, 300, 'Three satellites find your spot.', 52, INK, m * fd(T(0), .3), w='Bold')
        c.text(960, 370, 'Why does your phone need a fourth?', 52, INK, m * fd(T(0), .8), w='Bold')
        for i in range(4):
            x = 420 + i * 360; kk = m * fd(T(0), 1.2 + i * .25)
            sat(c, x, 560, 80, kk, hi=YE if i == 3 else None)
            if i < 3: c.check(x, 700, 40, GR, kk, fd(T(0), 1.4 + i * .25))
            else: c.text(x, 705, '?', 90, YE, kk, w='Bold')
        if T(1) > 0:
            p = clamp(T(1) / 2.2)
            pts = [(1500 + 72 * math.sin(2 * math.pi * u / 60), 700 - 72 * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * (1 - p)) + 1)]
            c.line(pts, CY, 10, fd(T(1)) * a0)
    if T(2) < -.1: return
    m = fd(T(2))
    clock(c, 620, 500, 220, YE, m, t * 3)
    c.text(1240, 430, 'THE', 90, INK, m, w='Bold')
    c.text(1240, 560, 'CLOCK', 150, YE, m * fd(T(2), .3), w='Bold')

def s_clock(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 190, 'Two very different clocks', 62, INK, a0, w='Bold')
        sat(c, 560, 360, 110, a0)
        clock(c, 560, 600, 130, GR, a0, t * 2)
        c.text(560, 800, 'Atomic clock', 48, GR, a0, w='Bold')
        phone(c, 1360, 360, 200, a0 * fd(T(0), .5), t=t)
        clock(c, 1360, 600, 130, PK, a0 * fd(T(0), .5), t * 2 + .3 * math.sin(t * 3))
        c.text(1360, 800, 'Cheap quartz clock', 48, PK, a0 * fd(T(0), .5), w='Bold')
    if T(1) > -.1:
        a1 = fd(T(1)) * (1 - fd(T(3), -.4, .4))
        if a1 > 0 and T(2) < .5:
            k = a1 * (1 - fd(T(2), 0, .5))
            c.text(960, 190, 'How fast is light?', 62, INK, k, w='Bold')
            c.line([(560, 450), (1360, 450)], DIM, 6, k)
            for j in range(11): c.line([(560 + j * 80, 430), (560 + j * 80, 470)], DIM, 4, k)
            p = (t * .6) % 1
            c.circ(560 + 800 * p, 450, 20, YE, k)
            c.text(960, 560, '30 cm', 110, YE, k, w='Bold')
            c.text(960, 670, 'in one billionth of a second', 48, INK, k, w='Bold')
        if T(2) > -.1:
            k = a1 * fd(T(2))
            c.text(960, 190, 'Clock off by 1 millionth of a second', 56, INK, k, w='Bold')
            for j in range(9):
                c.line([(360 + j * 150, 290), (360 + j * 150, 760)], (40, 48, 86), 3, k)
            for j in range(4):
                c.line([(360, 290 + j * 156), (1560, 290 + j * 156)], (40, 48, 86), 3, k)
            pin(c, 640, 640, 40, GR, k)
            c.text(640, 700, 'real spot', 32, GR, k, w='Bold')
            kk = k * fd(T(2), 1.6)
            pin(c, 1280, 640, 40, PK, kk)
            c.text(1280, 700, 'calculated', 32, PK, kk, w='Bold')
            c.arrow(690, 540, 1230, 540, YE, 6, kk, 20); c.arrow(1230, 540, 690, 540, YE, 6, kk, 20)
            c.text(960, 490, 'about 300 m off', 56, YE, kk, w='Bold')
            c.text(960, 830, '1 millionth of a second × speed of light ≈ 300 m', 30, DIM, kk, w='Medium')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 190, 'The fourth satellite fixes the clock', 58, INK, m, w='Bold')
    phone(c, 960, 640, 230, m, t=t)
    for i in range(4):
        x = 360 + i * 400; kk = m * fd(T(3), .3 + i * .3)
        sat(c, x, 330, 60, kk, hi=YE if i == 3 else None)
        packets(c, x, 360, 960, 560, t + i * .25, YE if i == 3 else SIG, kk, 3, .6, 7)
    k = m * fd(T(3), 2.0)
    c.rr(1200, 560, 1760, 780, 26, CARD, k, outline=GR, ow=5)
    c.text(1480, 610, '4 measurements', 40, INK, k, w='Bold', bg=CARD)
    c.text(1480, 670, 'position + clock error', 36, GR, k, w='Bold', bg=CARD)
    c.check(1480, 735, 26, GR, k, fd(T(3), 2.4))
    c.rr(160, 560, 720, 780, 26, CARD, k, outline=(60, 70, 120), ow=4)
    c.text(440, 640, 'Error found', 44, INK, k, w='Bold', bg=CARD)
    c.text(440, 700, 'and removed', 44, GR, k, w='Bold', bg=CARD)

def s_einstein(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 420, 'A twist from', 100, INK, a0, w='Bold')
        c.text(960, 560, 'Einstein', 150, YE, a0, w='Bold')
    if T(1) > -.1:
        m = fd(T(1)) * (1 - fd(T(3), -.4, .4))
        if m > 0:
            c.text(960, 190, 'Satellite clocks drift', 62, INK, m, w='Bold')
            earth(c, 330, 640, 180, m, t=t)
            sat(c, 760, 320, 90, m)
            clock(c, 760, 500, 70, YE, m, t * 2)
            c.arrow(500, 520, 690, 420, DIM, 4, m * .6, 14)
            k1 = m * fd(T(1), .5)
            c.rr(1000, 290, 1780, 420, 26, CARD, k1, outline=GR, ow=4)
            c.text(1040, 330, 'Weaker gravity', 40, GR, k1, 'lm', 'Bold', bg=CARD)
            c.text(1040, 385, 'ticks faster:  +45', 36, INK, k1, 'lm', 'Bold', bg=CARD)
            k2 = m * fd(T(1), 3.0)
            c.rr(1000, 450, 1780, 580, 26, CARD, k2, outline=PK, ow=4)
            c.text(1040, 490, 'Moving fast', 40, PK, k2, 'lm', 'Bold', bg=CARD)
            c.text(1040, 545, 'ticks slower:  −7', 36, INK, k2, 'lm', 'Bold', bg=CARD)
            if T(2) > -.1:
                k = m * fd(T(2))
                c.text(1390, 660, '+38', 110, YE, k, w='Bold')
                c.text(1390, 750, 'millionths of a second a day', 34, INK, k, w='Bold')
            c.text(1390, 830, 'in millionths of a second per day (Penn State GEOG 862)', 24, DIM, k1, w='Regular')
    if T(3) < -.1: return
    m = fd(T(3)) * (1 - fd(T(4), -.4, .4))
    if m > 0:
        c.text(960, 190, 'If nobody corrected it', 62, INK, m, w='Bold')
        c.line([(260, 600), (1660, 600)], (60, 70, 120), 14, m)
        pin(c, 360, 580, 40, GR, m)
        p = ease(clamp(T(3, .4) / 2.5))
        pin(c, 360 + 1200 * p, 580, 40, PK, m)
        c.text(960, 720, 'more than 10 km', 90, PK, m * fd(T(3), 2.0), w='Bold')
        c.text(960, 810, 'of error, every day', 46, INK, m * fd(T(3), 2.3), w='Bold')
        c.text(960, 470, '38 millionths of a second × speed of light ≈ 11 km', 32, DIM, m * fd(T(3), 1.0), w='Medium')
    if T(4) < -.1: return
    m = fd(T(4))
    c.text(960, 190, 'The fix', 66, INK, m, w='Bold')
    sat(c, 560, 420, 150, m)
    clock(c, 560, 690, 110, GR, m, t * 1.2)
    c.text(1300, 430, 'Set to tick', 72, INK, m * fd(T(4), .5), w='Bold')
    c.text(1300, 530, 'slightly slower', 72, GR, m * fd(T(4), .5), w='Bold')
    c.text(1300, 630, 'before launch', 72, INK, m * fd(T(4), .5), w='Bold')
    c.check(1300, 750, 46, GR, m, fd(T(4), 1.2))

def s_real(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if a0 > 0:
        c.text(960, 190, 'How close does it get?', 62, INK, a0, w='Bold')
        if T(1) > -.1:
            k = a0 * fd(T(1))
            for i, x in enumerate((420, 960, 1500)):
                sat(c, x, 300, 50, k)
                packets(c, x, 330, 960, 600, t + i * .3, SIG, k, 3, .6, 6)
            c.circ(960, 680, 110, (40, 80, 150), k * .5, outline=GR, ow=4)
            c.circ(960, 680, 18, DOT, k, outline=INK, ow=4)
            c.text(960, 840, 'Open sky: typically within about 5 m', 48, GR, k * fd(T(1), .8), w='Bold')
            c.text(1180, 680, '~5 m', 44, GR, k * fd(T(1), .8), 'lm', 'Bold')
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 190, 'In a city', 62, INK, m, w='Bold')
    for x0, w, h in ((300, 220, 470), (560, 180, 360), (1180, 200, 520), (1420, 240, 400)):
        building(c, x0, w, h, m)
    sat(c, 960, 280, 60, m)
    # blocked path
    k = m * fd(T(2), .6)
    sat(c, 1760, 300, 50, k)
    c.line([(1720, 330), (1600, 420)], SIG, 4, k)
    c.cross(1600, 420, 50, PK, k)
    c.text(1700, 470, 'blocked', 32, PK, k, w='Bold')
    # bounced path off a wall
    kk = m * fd(T(2), 1.4)
    sat(c, 160, 300, 50, kk)
    c.line([(190, 330), (740, 560), (960, 760)], YE, 4, kk)
    c.text(340, 520, 'bounced', 32, YE, kk, w='Bold')
    wob = (fd(T(3)) if T(3) > -.1 else 0.0)
    dx, dy = 70 * wob * math.sin(t * 1.3), 30 * wob * math.sin(t * 2.1)
    c.circ(960 + dx, 780 + dy, 18, DOT, m, outline=INK, ow=4)
    if T(3) > -.1:
        c.text(960, 860, 'Your blue dot can wander', 44, DOT, fd(T(3), .5), w='Bold')

REC = [('1', 'It only listens', CY), ('2', 'Delay = distance', YE), ('3', 'Einstein matters', GR)]
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
            sat(c, x + 60, y - 120, 50, m, CARD)
            phone(c, x, y + 40, 150, m, CARD, t)
            packets(c, x + 60, y - 95, x, y - 30, t, SIG, m, 2, .7, 6, False)
            c.text(x, y + 150, 'no signal sent to space', 28, DIM, m, w='Medium', bg=CARD)
        elif i == 1:
            c.text(x, y - 60, 'delay × light speed', 36, YE, m, w='Bold', bg=CARD)
            c.text(x, y + 10, '= distance', 36, YE, m, w='Bold', bg=CARD)
            c.text(x, y + 90, '4 satellites:', 34, INK, m, w='Bold', bg=CARD)
            c.text(x, y + 140, 'spot + clock', 34, INK, m, w='Bold', bg=CARD)
        else:
            c.text(x, y - 40, '+38 µs a day', 50, GR, m, w='Bold', bg=CARD)
            c.text(x, y + 30, 'built into', 34, INK, m, w='Bold', bg=CARD)
            c.text(x, y + 80, 'the satellite clocks', 34, INK, m, w='Bold', bg=CARD)
        c.text(x, 740 + up, lab, 34, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Your phone knows where you are, to within a few metres.",
            "But to use GPS, it sends nothing to space.",
            "It only listens.",
            "So how does it know? Here is how GPS works."], s_hook),
 ('1  ·  THE SATELLITES', ["More than thirty GPS satellites circle the Earth.",
            "Each one flies about 20,000 kilometres up, and goes around twice a day.",
            "From almost anywhere on Earth, at least four are in view.",
            "Each carries an atomic clock, and keeps broadcasting two things: where it is, and the exact time."], s_sats),
 ('2  ·  THE SIGNAL', ["Think of a thunderstorm.",
            "You see the lightning, count the seconds until the thunder, and you know how far away it is.",
            "GPS does the same, with radio waves instead of sound.",
            "Your phone checks when each signal was sent, and when it arrived.",
            "The delay, times the speed of light, gives the distance to that satellite."], s_signal),
 ('3  ·  PINNING YOU DOWN', ["But one distance is not enough.",
            "It only tells you how far you are from that satellite. You could be anywhere at that distance.",
            "A second distance narrows it down a lot.",
            "A third narrows it to one spot near Earth.",
            "This is called trilateration."], s_pin),
 ('4  ·  QUICK QUESTION', ["Quick question. If three satellites find your spot, why does your phone need a fourth?",
            "Three, two, one.",
            "The answer is the clock."], s_quiz),
 ('5  ·  THE CLOCK', ["Satellites have atomic clocks. Your phone has a cheap quartz clock.",
            "Light travels about 30 centimetres in a billionth of a second.",
            "So if your phone's clock is off by just a millionth of a second, your distance is off by about 300 metres.",
            "The fourth satellite adds one more measurement, so your phone can work out its own clock error and remove it."], s_clock),
 ("6  ·  EINSTEIN'S TWIST", ["Then there is a twist from Einstein.",
            "High up, gravity is weaker, so satellite clocks tick a little faster. Their speed slows them a little.",
            "Together, they gain about 38 millionths of a second every day.",
            "Times the speed of light, that would add more than 10 kilometres of error each day.",
            "So the satellite clocks are set to tick slightly slower before launch."], s_einstein),
 ('7  ·  REAL LIFE', ["So in real life, how close does it get?",
            "Under open sky, a phone is typically accurate to about 5 metres.",
            "Near tall buildings, bridges and trees, signals get blocked, or bounce off walls.",
            "That is why your blue dot can wander in a city."], s_real),
 ('RECAP', ["So remember three things.",
            "One. GPS works by listening. Satellites broadcast where they are, and the time.",
            "Two. Signal delay times the speed of light gives distance. Four satellites fix your spot and your clock.",
            "Three. Even Einstein matters. Satellite clocks are adjusted for relativity.",
            "If this helped, subscribe for more."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-60 s.
SHORT_SCENES = [
 ('GPS', ["Your phone knows where you are, to within a few metres.",
          "But to use GPS, it sends nothing to space.",
          "It only listens."], s_hook),
 ('THE SIGNAL', ["Think of a thunderstorm.",
                 "You see the lightning, count the seconds until the thunder, and you know how far away it is.",
                 "GPS does the same, with radio waves.",
                 "Each satellite sends its position and the exact time. Your phone notes when the signal arrives.",
                 "The delay, times the speed of light, gives the distance."], s_signal),
 ('THE ANSWER', ["Now measure the distance to at least four satellites.",
                 "Only one spot fits all those distances, and the fourth one even corrects your phone's clock.",
                 "That is how GPS finds you, just by listening. Follow for more."],
               card('Distance to 4 satellites', 'Pins your exact spot')),
]
SHORT_HITS = [(2, 0, 0.0)]
