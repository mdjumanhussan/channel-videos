"""Episode: Your Nerves Wrinkle Your Fingers (not soggy skin: 1930s nerve-damage clue, blood vessels narrow, skin buckles; rain treads idea, 2013 yes, 2014 no; 2025 same-pattern study)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Fingers Wrinkle'                            # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Why do fingers wrinkle in the bath?'             # headline on the vertical Short
HITS = [(0, 3, 0.0), (3, 0, 0.0), (6, 4, 0.0), (7, 3, 0.0)]    # title card, the key answer, quiz answer, how/why split
THUMB = ['NOT SOGGY.', 'YOUR NERVES', 'DID THAT']
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.5, (1, 3): 0.3, (2, 4): 0.3, (4, 1): 0.3, (6, 3): 0.3, (6, 4): 0.5, (7, 2): 0.4}
SHORT_PAUSES = {(0, 1): 0.3}
CAPTION_FIXES = {'nineteen thirties': '1930s', 'fifty-two': '52', 'twelve percent': '12%', 'thirty minutes': '30 minutes'}

# Colour code kept in every scene (lesson of 2026-11-01):
# water blue, nerves yellow, blood vessels pink, grooves green, the old 'soggy' idea purple.
WATER = CY; NERVE = YE; VESSEL = PK; GROOVE = GR; OLD = PU
VD = (205, 30, 95); WB = (18, 50, 96); SKIN = (232, 180, 150); DARK = (176, 116, 96); FLESH = (206, 130, 118); OUTER = (240, 200, 170)
TYRE = (46, 48, 60); ROCK = (70, 80, 120)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def bath(c, x0, y0, x1, y1, a, t):
    """A tank of bath water with a moving surface and rising bubbles."""
    if a <= .01: return
    top = [(x0 + (x1 - x0) * k / 40, y0 + 7 * math.sin(k * .55 + t * 2.2)) for k in range(41)]
    poly(c, top + [(x1, y1), (x0, y1)], WB, a)
    c.line(top, WATER, 5, a)
    for k in range(9):
        u = (t * .13 + rnd(k, 3)) % 1
        c.circ(x0 + 30 + (x1 - x0 - 60) * rnd(k, 7), lerp(y1 - 20, y0 + 26, u), 4 + 5 * rnd(k, 2), WATER, a * .55 * (1 - u), bg=WB)

def groove_lines(c, x, y, w, h, a, col, bg, seed=1, n=6):
    """Wavy grooves running down a fingertip pad."""
    if a <= .01: return
    for i in range(n):
        u = (i + .5) / n
        xx = x - w * .40 + w * .80 * u
        top = y + h * (.05 + .14 * abs(u - .5) * 2)
        pts = [(xx + w * .035 * math.sin(k * .9 + i * 1.7 + seed), top + (h * .40) * k / 14) for k in range(15)]
        c.line(pts, col, max(3, w * .032), a, bg)

def finger(c, x, y, w, h, wr=0.0, a=1.0, bg=BG, nerve=0.0, broken=False, t=0.0, seed=1, skin=SKIN, col=DARK):
    """A finger pointing up, seen from the pad side; (x, y) is the middle of the tip."""
    if a <= .01: return
    c.rr(x - w / 2, y, x + w / 2, y + h, w / 2, skin, a, bg=bg)
    groove_lines(c, x, y, w, h, a * wr, col, skin, seed)
    if nerve > .01:
        ym = y + h * .62
        if broken:
            c.line([(x, y + h - 10), (x, ym + 34)], NERVE, 7, a * nerve, skin)
            c.line([(x, ym - 34), (x, y + h * .2)], NERVE, 7, a * nerve * .3, skin)
            c.cross(x, ym, 56, VESSEL, a * nerve)
        else:
            c.line([(x, y + h - 10), (x, y + h * .12)], NERVE, 7, a * nerve, skin)
            u = (t * .8) % 1
            c.circ(x, lerp(y + h - 10, y + h * .12, u), 11, INK, a * nerve, bg=NERVE)

def hand(c, x, y, a, wrs, t, nerve=0.0, broken=(), bg=BG, s=1.0):
    """Four fingers on a palm. wrs: wrinkle amount per finger; broken: indices with a damaged nerve."""
    if a <= .01: return
    gap = 138 * s; w = 112 * s; hs = (360, 420, 400, 330)
    c.rr(x - 2.05 * gap, y + 330 * s, x + 2.05 * gap, y + 560 * s, 60 * s, SKIN, a, bg=bg)
    for i in range(4):
        fx = x + (i - 1.5) * gap; h = hs[i] * s
        finger(c, fx, y + 400 * s - h, w, h + 50 * s, wrs[i], a, bg, nerve, i in broken, t, seed=i + 1)

def surf(u, ys, p, amp=30):
    return ys + p * amp * (math.sin(u * 6 * math.pi) * .8 + .2)

VESS = [(.12, .62), (.28, .66), (.44, .60), (.60, .66), (.76, .62), (.90, .66)]
def section(c, x0, y0, x1, y1, p, a, t, drops=0.0, nerve=0.0, labels=True):
    """Close-up slice through a fingertip: water above, outer skin, blood vessels and a nerve below."""
    if a <= .01: return
    W_, H_ = x1 - x0, y1 - y0; ys = y0 + H_ * .28
    c.rr(x0, y0, x1, y1, 22, WB, a)
    pts = [(x0 + W_ * k / 90, surf(k / 90, ys, p)) for k in range(91)]
    poly(c, pts + [(x1, y1 - 12), (x0, y1 - 12)], OUTER, a, WB)
    poly(c, [(x, y + 34) for x, y in pts] + [(x1, y1 - 12), (x0, y1 - 12)], FLESH, a, OUTER)
    # blood vessels: thick when relaxed, thin once the nerve has told them to narrow
    th = lerp(36, 12, clamp(p)); ym = y0 + H_ * .74
    c.line([(x0 + 14, ym), (x1 - 14, ym)], VD, th, a, FLESH)
    for k, (u, v) in enumerate(VESS):
        px = x0 + W_ * u
        c.line([(px, ym), (px + 26 * math.sin(k * 2.1), y0 + H_ * .58), (px, y0 + H_ * .49)], VD, th * .7, a, FLESH)
    if nerve > .01:
        c.line([(x0 + W_ * .5, y1 - 14), (x0 + W_ * .5, ym + 30), (x0 + W_ * .3, ym + 18), (x0 + 30, ym + 18)], NERVE, 8, a * nerve, FLESH)
        c.line([(x0 + W_ * .5, ym + 30), (x0 + W_ * .75, ym + 18), (x1 - 30, ym + 18)], NERVE, 8, a * nerve, FLESH)
        for k in range(3):
            u = (t * .6 + k / 3) % 1
            c.circ(x0 + W_ * .5 + (W_ * .46) * u, ym + 28 - 12 * u, 9, INK, a * nerve, bg=NERVE)
            c.circ(x0 + W_ * .5 - (W_ * .46) * u, ym + 28 - 12 * u, 9, INK, a * nerve, bg=NERVE)
    if drops > .01:
        for k in range(16):
            u = (t * .35 + rnd(k, 5)) % 1; xx = x0 + 40 + (W_ - 80) * rnd(k, 8)
            c.circ(xx, lerp(y0 + 26, ys + 22, u), 7, WATER, a * drops * (1 - u * .5), bg=WB if u < .8 else OUTER)
    if labels:
        c.text(x0 + 24, y0 + 40, 'water', 34, WATER, a, anchor='lm', w='Bold', bg=WB)
        tag(c, x1 - 150, y1 - 44, 'blood vessels', VESSEL, a)

def balloon(c, x, y, r, p, a):
    pts = []
    for k in range(120):
        an = k / 120 * 2 * math.pi
        rr_ = r * (1 - .24 * p + .05 * p * math.sin(an * 15))
        pts.append((x + rr_ * math.cos(an), y + rr_ * math.sin(an) * 1.12))
    poly(c, pts, VESSEL, a)
    c.line([(x, y + r * 1.12 * (1 - .22 * p)), (x, y + r * 1.12 + 60)], DIM, 4, a)

def tag(c, x, y, txt, col, a):
    w = c.tw(txt, 34, 'Bold') / 2 + 24
    c.rr(x - w, y - 28, x + w, y + 28, 28, BG, a, bg=FLESH); c.text(x, y, txt, 34, col, a, w='Bold', bg=BG)

def thumb_art(c):
    """A huge wrinkled fingertip with its nerve lit, under a waterline."""
    bath(c, 1120, 760, 1880, 1060, 1.0, 1.0)
    finger(c, 1500, 120, 520, 1000, 1.0, 1.0, BG, 0, False, 0, seed=3)
    c.line([(1500, 1060), (1500, 300)], NERVE, 16, 1.0, SKIN)
    c.circ(1500, 300, 30, NERVE, 1.0, bg=SKIN)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Long bath? Prune fingers', 72, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'Water soaking in and swelling your skin?', 64, OLD, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'No. Your nerves are doing it', 72, NERVE, a * hl(2), w='Bold')
        bath(c, 330, 250, 1590, 850, a, t)
        wr = max(fd(t, .15, 2.4), 0)
        hand(c, 960, 300 + 12 * math.sin(t * 1.5), a, (wr,) * 4, t, hl(2), bg=WB, s=.98)
        if hl(1) > 0 and hl(2) < 1:
            k = a * hl(1) * (1 - hl(2))
            for j in range(5):
                u = (t * .9 + j * .2) % 1; x = 520 + j * 220
                c.arrow(x, 300 + 80 * u, x, 360 + 80 * u, OLD, 7, k * (1 - u * .4), 18)
            c.rr(640, 760, 1280, 830, 30, BG, k, outline=OLD, ow=3); c.text(960, 795, 'the usual guess', 40, OLD, k, w='Bold')
        if hl(2) > 0:
            c.cross(1500, 340, 90, VESSEL, a * hl(2) * fd(T(2), .1))
            c.text(1500, 430, 'soggy', 38, OLD, a * hl(2), w='Bold', bg=WB)
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 300 + 30 * (1 - m), 'Your Nerves', 124, NERVE, m, w='Bold')
        c.text(960, 450 + 30 * (1 - m), 'Wrinkle Your Fingers', 112, INK, m, w='Bold')
        c.line([(960 - 400 * m, 560), (960 + 400 * m, 560)], WATER, 8, m)
        for j, wr in enumerate((0.0, .5, 1.0)):
            finger(c, 720 + j * 240, 640, 130, 240, fd(T(3), .9 + j * .3) * wr, m * fd(T(3), .5 + j * .2), BG, m if j == 2 else 0, False, t)

def s_soggy(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Water does get into the outer layer of skin', 62, WATER, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'So a swollen finger should get bigger', 66, OLD, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Measure one: it has got smaller', 70, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'So what took the volume away?', 74, YE, hl(3), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        section(c, 300, 260, 1620, 840, 0.0, k * fd(T(0), -.2), t, drops=1.0)
        tag(c, 480, 490, 'outer skin', WATER, k)
    k1 = hl(1)
    if k1 > 0:
        dark = 1 - .55 * hl(3)
        # dry finger, expected swollen finger (dashed idea), measured finger
        cols = ((470, 200, 'dry finger', INK), (960, 236, 'if it swelled', OLD), (1450, 182, 'wrinkled finger', NERVE))
        for j, (x, w, lab, col) in enumerate(cols):
            if j == 1: kk = k1 * (1 - hl(2) * .55)
            elif j == 2: kk = k1 * hl(2)
            else: kk = k1
            kk *= dark
            finger(c, x, 270, w, 470, 1.0 if j == 2 else 0.0, kk, BG, 0, False, t, skin=SKIN if j != 1 else (130, 112, 190), col=DARK)
            c.text(x, 790, lab, 42, col, kk, w='Bold')
        c.text(1650, 846, 'Drawing not to scale', 28, DIM, k1 * .9, w='Regular')
    if hl(3) > 0:
        c.circ(960, 520, 150, BG, hl(3) * .9); c.circ(960, 520, 150, None, hl(3), outline=YE, ow=8)
        c.text(960, 520, '?', 180, YE, hl(3), w='Bold')

def s_clue(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The clue: doctors in the 1930s', 70, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Some patients had damaged finger nerves', 64, VESSEL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Healthy nerve: wrinkled. Damaged nerve: smooth', 58, GROOVE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Same water, same time. Only the nerve differs', 58, NERVE, hl(3) * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'So what does the nerve do?', 74, NERVE, hl(4), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        c.rr(760, 260, 1160, 370, 50, WATER, k * fd(T(0), .1)); c.text(960, 315, '1930s', 72, BG, k * fd(T(0), .1), w='Bold', bg=WATER)
        c.text(960, 470, 'Nerve damage in the fingers', 56, INK, k * fd(T(0), .6), w='Bold')
        for j in range(5):
            c.rr(610 + j * 150, 560, 720 + j * 150, 760, 16, CARD, k * fd(T(0), .8 + j * .1), outline=(70, 80, 130), ow=3)
            for q in range(4): c.rr(630 + j * 150, 590 + q * 38, 700 + j * 150 - 14 * (q % 2), 602 + q * 38, 5, (90, 100, 150), k * fd(T(0), .8 + j * .1), bg=CARD)
    k1 = hl(1)
    if k1 > 0:
        wet = fd(T(2), .1, 1.6) if T(2) > 0 else 0
        bath(c, 400, 250, 1520, 850, k1 * hl(2), t)
        bg = WB if hl(2) > .5 else BG
        hand(c, 960, 290, k1, (wet, wet, 0, 0), t, 1.0, broken=(2, 3), bg=bg, s=.96)
        if hl(2) > 0:
            for x, l1, l2, col in ((550, 'healthy', 'wrinkled', GROOVE), (1370, 'damaged', 'smooth', VESSEL)):
                c.rr(x - 125, 420, x + 125, 560, 26, col, hl(2)); c.text(x, 462, l1, 40, BG, hl(2), w='Bold', bg=col); c.text(x, 516, l2, 40, BG, hl(2), w='Bold', bg=col)

def s_squeeze(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'It tells your blood vessels to shrink', 68, VESSEL, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Under the skin: a web of tiny blood vessels', 62, VESSEL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'About 5 minutes in, nerves make them narrow', 62, NERVE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Like a balloon losing a little air', 68, INK, hl(3) * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'The skin stays the same size, so it buckles', 64, GROOVE, hl(4), w='Bold')
    p = fd(T(2), .8, 3.0) if T(2) > 0 else 0
    if T(4) > 0: p = max(p, 1.0)
    bl = hl(3) * (1 - hl(4))
    k = 1 - bl
    if k > 0:
        s_p = hl(4) if T(4) > 0 else 0
        draw_section_narrowing(c, k, p, s_p, t, hl(2))
        if hl(2) > 0 and hl(4) < 1:
            kk = k * hl(2) * (1 - hl(4))
            c.circ(1480, 480, 98, BG, kk, bg=WB); ring(c, 1480, 480, 88, clamp(T(2) / 3.0), NERVE, kk)
            c.text(1480, 462, '5', 70, NERVE, kk, w='Bold'); c.text(1480, 516, 'min', 32, NERVE, kk, w='Bold')
        if hl(4) > 0:
            for j in range(3):
                x = 280 + 1360 * (j + .5) / 6 * 2 + 22
                c.arrow(x, 330, x, 400, GROOVE, 7, hl(4) * fd(T(4), 1.0 + j * .2), 18)
            c.text(960, 300, 'grooves', 44, GROOVE, hl(4) * fd(T(4), 1.0), w='Bold', bg=WB)
    if bl > 0:
        q = fd(T(3), .3, 2.0)
        balloon(c, 620, 500, 190, 0.0, bl); c.text(620, 800, 'full', 44, INK, bl, w='Bold')
        c.arrow(860, 500, 1060, 500, DIM, 8, bl * fd(T(3), .3), 24)
        balloon(c, 1300, 500, 190, q, bl); c.text(1300, 800, 'a little less inside', 44, GROOVE, bl * q, w='Bold')

def draw_section_narrowing(c, k, p, s_p, t, nv):
    """Scene 3's slice: vessels narrow with p, the skin surface buckles with s_p."""
    x0, y0, x1, y1 = 280, 260, 1640, 840
    W_, H_ = x1 - x0, y1 - y0; ys = y0 + H_ * .28
    c.rr(x0, y0, x1, y1, 22, WB, k)
    pts = [(x0 + W_ * q / 90, surf(q / 90, ys, s_p, 34)) for q in range(91)]
    poly(c, pts + [(x1, y1 - 12), (x0, y1 - 12)], OUTER, k, WB)
    poly(c, [(x, y + 34) for x, y in pts] + [(x1, y1 - 12), (x0, y1 - 12)], FLESH, k, OUTER)
    th = lerp(36, 12, clamp(p)); ym = y0 + H_ * .74
    c.line([(x0 + 14, ym), (x1 - 14, ym)], VD, th, k, FLESH)
    for q, (u, v) in enumerate(VESS):
        px = x0 + W_ * u
        c.line([(px, ym), (px + 26 * math.sin(q * 2.1), y0 + H_ * .58), (px, y0 + H_ * .49)], VD, th * .7, k, FLESH)
    if nv > .01:
        mid = x0 + W_ * .5
        c.line([(mid, y1 - 14), (mid, ym + 34)], NERVE, 8, k * nv, FLESH)
        c.line([(x0 + 30, ym + 34), (x1 - 30, ym + 34)], NERVE, 8, k * nv, FLESH)
        for q in range(3):
            u = (t * .6 + q / 3) % 1
            c.circ(mid + (W_ * .46) * u, ym + 34, 10, INK, k * nv, bg=NERVE)
            c.circ(mid - (W_ * .46) * u, ym + 34, 10, INK, k * nv, bg=NERVE)
    c.text(x0 + 24, y0 + 40, 'water', 34, WATER, k, anchor='lm', w='Bold', bg=WB)
    tag(c, x1 - 150, y1 - 44, 'blood vessels', VESSEL, k)
    if nv > .01: tag(c, x0 + 100, y1 - 44, 'nerve', NERVE, k * nv)

SOFAR = [('Not soggy skin:', 'the finger gets smaller', OLD),
         ('Nerves make blood vessels', 'narrow', NERVE),
         ('The skin on top', 'buckles into grooves', GROOVE)]
def s_sofar(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'So far', 74, INK, 1 - hl(1), w='Bold')
    c.text(960, 150, 'That explains how. But why bother?', 70, YE, hl(1), w='Bold')
    k = 1 - hl(1) * .75
    for j, (l1, l2, col) in enumerate(SOFAR):
        y = 350 + j * 170; m = k * fd(T(0), .3 + j * 1.1)
        c.rr(360, y - 72, 1560, y + 72, 24, CARD, m, outline=col, ow=4)
        c.check(460, y, 50, col, m, fd(T(0), .5 + j * 1.1))
        c.text(550, y - 26, l1, 44, col, m, anchor='lm', w='Bold', bg=CARD)
        c.text(550, y + 28, l2, 44, INK, m, anchor='lm', w='Bold', bg=CARD)
    if hl(1) > 0:
        c.circ(960, 520, 130, BG, hl(1)); c.circ(960, 520, 130, None, hl(1), outline=YE, ow=8)
        c.text(960, 520, 'why?', 76, YE, hl(1), w='Bold')

def mountain(c, x, y, s, a, p, t):
    poly(c, [(x - 420 * s, y + 260 * s), (x, y - 240 * s), (x + 420 * s, y + 260 * s)], ROCK, a)
    for k in range(7):
        dx = (k - 3) * 118 * s
        n = 16; pts = []
        for q in range(n + 1):
            u = q / n * clamp(p)
            pts.append((x + dx * u + 26 * s * math.sin(u * 9 + k * 1.9), y - 220 * s + 470 * s * u))
        c.line(pts, WATER, 7 * s, a, ROCK)

def tread(c, x, y, w, h, a, t):
    """A tyre's contact patch seen from above; blue water runs down its grooves."""
    if a <= .01: return
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 34, TYRE, a)
    for k in range(5):
        gx = x - w * .36 + k * w * .18
        pts = [(gx + 18 * math.sin(q * .9 + k), y - h / 2 + 10 + (h - 20) * q / 14) for q in range(15)]
        c.line(pts, (12, 14, 24), 26, a, TYRE)
        for q in range(4):
            u = (t * .5 + q / 4 + k * .13) % 1; idx = u * 14
            c.circ(gx + 18 * math.sin(idx * .9 + k), y - h / 2 + 10 + (h - 20) * u, 8, WATER, a, bg=(12, 14, 24))

def s_treads(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'In 2011, Mark Changizi studied the pattern', 62, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Grooves like rivers running off a mountain', 62, WATER, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Tyre treads give rain somewhere to go', 66, GROOVE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Wrinkles only appear when hands are wet', 62, YE, hl(3), w='Bold')
    k0 = 1 - hl(2)
    if k0 > 0:
        finger(c, 520, 270, 340, 560, 1.0, k0 * fd(T(0), -.2), BG, 0, False, t, seed=3, col=GROOVE)
        if hl(1) > 0:
            mountain(c, 1320, 530, 1.0, k0 * hl(1), fd(T(1), .2, 2.4), t)
            c.text(1320, 840, 'water runs off along channels', 40, WATER, k0 * hl(1), w='Bold')
            c.arrow(760, 520, 870, 520, DIM, 7, k0 * hl(1), 20)
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        tread(c, 560, 540, 620, 520, k2, t); c.text(560, 840, 'a tyre in the rain', 42, WATER, k2, w='Bold')
        finger(c, 1340, 270, 320, 520, 1.0, k2 * fd(T(2), 1.2), BG, 0, False, t, seed=3, col=GROOVE)
        c.text(1100, 540, '=', 100, YE, k2 * fd(T(2), 1.6), w='Bold')
        c.text(1340, 840, 'the same idea?', 42, GROOVE, k2 * fd(T(2), 1.6), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        bath(c, 1000, 280, 1660, 830, k3, t)
        finger(c, 600, 300, 300, 510, 0.0, k3); c.text(600, 850, 'dry: smooth', 44, INK, k3, w='Bold')
        finger(c, 1330, 300, 300, 510, fd(T(3), .4, 1.2), k3, WB, 0, False, t, seed=3, col=GROOVE)
        c.text(1330, 850, 'wet: grooves', 44, GROOVE, k3, w='Bold')

def containers(c, a, t, p):
    """Two containers with marbles travelling from one to the other."""
    for x, lab in ((560, 'from'), (1360, 'to')):
        c.rr(x - 180, 560, x + 180, 790, 20, CARD, a, outline=(90, 100, 150), ow=5)
        c.text(x, 830, lab, 38, DIM, a, w='Bold')
    for k in range(8):
        u = clamp(p * 9 - k)
        sx = 480 + (k % 4) * 54; sy = 750 - (k // 4) * 54
        ex = 1280 + (k % 4) * 54; ey = 750 - (k // 4) * 54
        x = lerp(sx, ex, u); y = lerp(sy, ey, u) - 300 * math.sin(math.pi * u)
        c.circ(x, y, 26, WATER, a, bg=CARD if 0 < u < 1 else CARD)
        c.circ(x - 8, y - 8, 7, INK, a * .8, bg=WATER)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    ans = hl(4)
    c.text(960, 150, '2013: 20 volunteers soak for 30 minutes', 62, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Then they move wet marbles across', 66, WATER, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Quick question', 74, YE, hl(2) * (1 - ans), w='Bold')
    c.text(960, 240, 'Were wrinkled fingers faster?', 54, INK, hl(2) * (1 - ans), w='Bold')
    c.text(960, 150, 'Faster: about 12%. Dry objects: no difference', 60, GROOVE, ans, w='Bold')
    k = 1 - hl(2)
    if k > 0:
        if hl(1) < 1:
            kk = k * (1 - hl(1))
            bath(c, 460, 280, 1460, 830, kk, t)
            for j in range(4):
                person_x = 620 + j * 226
                finger(c, person_x, 340, 130, 420, fd(T(0), 1.0 + j * .2, 1.4), kk, WB, 0, False, t, seed=j + 2)
            ring(c, 1620, 360, 70, clamp(T(0) / 4), WATER, kk)
            c.text(1620, 360, '30', 54, WATER, kk, w='Bold'); c.text(1620, 462, 'minutes', 34, WATER, kk, w='Bold')
        if hl(1) > 0:
            containers(c, k * hl(1), t, fd(T(1), .2, 3.0))
    k2 = hl(2) * (1 - ans)
    if k2 > 0 or (ans > 0 and ans < 1):
        for j, (lab, x) in enumerate((('A  faster', 560), ('B  no different', 1360))):
            kk = k2 * fd(T(2), .6 + j * .6)
            c.rr(x - 320, 340, x + 320, 760, 30, CARD, kk, outline=(70, 80, 130), ow=3)
            c.text(x, 420, lab, 56, INK, kk, w='Bold', bg=CARD)
            finger(c, x, 490, 130, 230, 1.0, kk, CARD, 0, False, t, seed=j + 2, col=GROOVE)
            if j == 0:
                c.arrow(x + 110, 620, x + 260, 620, GROOVE, 8, kk, 22)
            else:
                c.line([(x + 110, 610), (x + 240, 610)], DIM, 8, kk, CARD); c.line([(x + 110, 640), (x + 240, 640)], DIM, 8, kk, CARD)
    if T(3) > 0 and ans < .99:
        p = clamp(T(3) / 1.6); n = 3 - min(2, int(T(3) / .55)); m = 1 - ans
        c.circ(960, 560, 90, BG, m); ring(c, 960, 560, 82, p, YE, m); c.text(960, 560, str(n), 90, YE, m, w='Bold')
    if ans > 0:
        c.text(520, 270, 'wet objects', 48, WATER, ans, w='Bold')
        c.text(1400, 270, 'dry objects', 48, INK, ans, w='Bold')
        base = 360
        for g, (x0, vals) in enumerate(((180, ((1.0, DIM, 'smooth'), (.88, GROOVE, 'wrinkled'))), (1060, ((1.0, DIM, 'smooth'), (1.0, GROOVE, 'wrinkled'))))):
            for j, (v, col, lab) in enumerate(vals):
                y = 390 + j * 190; gg = fd(T(4), .3 + j * .4, .9); L = 560 * v * gg
                c.text(x0, y - 58, lab, 38, col, ans, anchor='lm', w='Bold')
                c.rr(x0, y - 28, x0 + L, y + 32, 12, col, ans)
        c.text(960, 780, 'bar = time taken', 36, DIM, ans, w='Medium')
        c.text(520, 840, '12% less time', 46, GROOVE, ans * fd(T(4), 1.0), w='Bold')
        c.text(1400, 840, 'no difference', 46, DIM, ans * fd(T(4), 1.0), w='Bold')

def study_cards(c, a1, a2):
    for x, yr, l1, l2, col, ok, a in ((540, '2013', '20 volunteers', 'better on wet objects', GROOVE, True, a1),
                                     (1380, '2014', '40 volunteers, 52 objects', 'no advantage', VESSEL, False, a2)):
        if a <= .01: continue
        c.rr(x - 360, 280, x + 360, 800, 30, CARD, a, outline=col, ow=5)
        c.rr(x - 100, 310, x + 100, 390, 40, col, a, bg=CARD); c.text(x, 350, yr, 48, BG, a, w='Bold', bg=col)
        if ok: c.check(x, 520, 100, col, a, 1)
        else: c.cross(x, 520, 100, col, a)
        c.text(x, 660, l1, 44, INK, a, w='Bold', bg=CARD); c.text(x, 730, l2, 44, col, a, w='Bold', bg=CARD)

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Case closed? Not quite', 74, YE, (1 - hl(1)), w='Bold')
    c.text(960, 150, '2014: a bigger test in Berlin', 70, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'No grip advantage, wet or dry', 70, VESSEL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'The how is settled. The why is still open', 64, YE, hl(3), w='Bold')
    k = 1 - hl(3)
    if k > 0: study_cards(c, k * fd(T(0), -.2), k * hl(1))
    k3 = hl(3)
    if k3 > 0:
        for j, (x, big, l1, l2, col) in enumerate(((540, 'HOW', 'nerves and blood vessels', 'settled', GROOVE), (1380, 'WHY', 'grip? the tests disagree', 'still open', YE))):
            m = k3 * fd(T(3), j * 1.4)
            c.rr(x - 380, 280, x + 380, 800, 30, CARD, m, outline=col, ow=5)
            c.text(x, 400, big, 120, col, m, w='Bold', bg=CARD)
            if j == 0: c.check(x, 545, 90, col, m, fd(T(3), .3))
            else: c.text(x, 545, '?', 140, col, m, w='Bold', bg=CARD)
            c.text(x, 670, l1, 42, INK, m, w='Bold', bg=CARD); c.text(x, 740, l2, 46, col, m, w='Bold', bg=CARD)

def vessels_on(c, x, y, w, h, a):
    """Faint blood vessels running under the fingertip's grooves."""
    if a <= .01: return
    for i in range(6):
        u = (i + .5) / 6; xx = x - w * .40 + w * .80 * u
        top = y + h * (.05 + .14 * abs(u - .5) * 2)
        pts = [(xx + w * .035 * math.sin(k * .9 + i * 1.7 + 3) + 6, top + (h * .40) * k / 14) for k in range(15)]
        c.line(pts, VESSEL, 5, a, SKIN)

def s_map(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, '2025: the same hands, soaked twice', 66, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'The wrinkles came back almost the same', 64, GROOVE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Just 3 people. But folds followed the vessels', 60, VESSEL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Not random: they seem to trace what is below', 60, YE, hl(3), w='Bold')
    k = 1 - hl(2)
    if k > 0:
        for j, (x, lab) in enumerate(((560, 'first soak'), (1360, 'at least a day later'))):
            kk = k * fd(T(0), .4 + j * 1.4)
            finger(c, x, 270, 340, 560, fd(T(0), .8 + j * 1.4, 1.0), kk, BG, 0, False, t, seed=3, col=GROOVE)
            c.text(x, 860, lab, 42, INK, kk, w='Bold')
        c.text(960, 530, '=', 120, GROOVE, k * hl(1), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        x, y, w, h = 960, 250, 420, 620
        finger(c, x, y, w, h, 1.0, k2, BG, 0, False, t, seed=3, col=(GROOVE if hl(3) < .5 else DARK))
        vessels_on(c, x, y, w, h, k2 * fd(T(2), .8))
        c.arrow(620, 380, 790, 380, VESSEL, 7, k2 * fd(T(2), 1.0), 20); c.text(430, 380, 'blood vessels', 44, VESSEL, k2 * fd(T(2), 1.0), w='Bold')
        c.arrow(1300, 460, 1120, 460, GROOVE, 7, k2 * fd(T(2), 1.4), 20); c.text(1470, 460, 'the folds', 44, GROOVE, k2 * fd(T(2), 1.4), w='Bold')
        c.text(1520, 760, 'small study', 38, DIM, k2, w='Medium')

RECAP = [('Not soggy skin:', 'a wrinkled finger is smaller', OLD),
         ('Nerves shrink the vessels,', 'and the skin buckles', NERVE),
         ('Grip may be why,', 'but the tests disagree', GROOVE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 150, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    finger(c, 340, 250, 340, 620, 1.0, fd(T(0)) * out, BG, 0, False, t, seed=3)
    for i, (l1, l2, col) in enumerate(RECAP):
        m = fd(T(i + 1)) * out; y = 340 + i * 190
        if m <= .01: continue
        c.line([(470, 300 + i * 60), (640, y)], col, 5, m)
        c.circ(470, 300 + i * 60, 12, col, m, bg=SKIN)
        c.rr(640, y - 80, 1680, y + 80, 22, CARD, m, outline=col, ow=4)
        c.text(690, y - 30, l1, 50, col, m, anchor='lm', w='Bold', bg=CARD)
        c.text(690, y + 32, l2, 48, INK, m, anchor='lm', w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

# Lesson of 2026-11-03: every scene ends on an open question or peak, and the next scene starts on its answer, mid-action.
SCENES = [
 ('INTRO', ["Stay in the bath long enough, and your fingertips turn into prunes.",
            "Most people think that's water soaking in and swelling your skin.",
            "It isn't. Your nerves are doing it.",
            "But why would your body bother?"], s_hook),
 ('1  ·  THE SOGGY IDEA', ["Water does get into the outer layer of your skin.",
            "But if swelling were the whole story, a wrinkled finger should get bigger.",
            "Measure one, and it has got smaller.",
            "So what took the volume away?"], s_soggy),
 ('2  ·  THE CLUE', ["The clue came from doctors, in the nineteen thirties.",
            "Some of their patients had damaged nerves in their fingers.",
            "In water, healthy fingers wrinkled. Fingers with nerve damage stayed smooth.",
            "Same water. Same time. The only difference was the nerve.",
            "So what is that nerve actually doing?"], s_clue),
 ('3  ·  THE SQUEEZE', ["It tells your blood vessels to shrink.",
            "Under your fingertip sits a web of tiny blood vessels.",
            "After about five minutes in water, your nerves make them narrow.",
            "The fingertip loses a little volume, like a balloon losing air.",
            "But the skin on top stays the same size. So it buckles into grooves."], s_squeeze),
 ('4  ·  SO FAR', ["So far: not soggy skin. Narrowed vessels. Buckled skin.",
            "That explains how. But why would your body do it at all?"], s_sofar),
 ('5  ·  RAIN TREADS', ["In 2011, scientist Mark Changizi looked closely at the pattern.",
            "The grooves looked like rivers running off a mountain, as if built to carry water away.",
            "Think of car tyres in the rain. Treads give the water somewhere to go, so the rubber can grip.",
            "And wrinkles only appear when your hands are wet. Just when you'd want treads."], s_treads),
 ('6  ·  QUICK QUESTION', ["In 2013, a team tested that. Twenty volunteers soaked their fingers for thirty minutes.",
            "Then they moved wet marbles from one container to another.",
            "Quick question. Were wrinkled fingers faster, or no different?",
            "Three, two, one.",
            "Faster. By about twelve percent. And with dry objects, no difference at all."], s_quiz),
 ('7  ·  THE TWIST', ["Case closed? Not quite.",
            "In 2014, a team in Berlin tested forty volunteers, with fifty-two objects.",
            "They found no grip advantage at all, wet or dry.",
            "So how your fingers wrinkle is settled. Why they wrinkle is still open. Grip is the famous idea, but the tests disagree."], s_twist),
 ('8  ·  YOUR PATTERN', ["One more surprise. In 2025, researchers soaked the same hands twice, at least a day apart.",
            "The wrinkles came back almost exactly the same.",
            "It was a tiny study, just three people. But the folds followed the blood vessels underneath.",
            "So those wrinkles aren't random. They seem to trace what's below your skin."], s_map),
 ('RECAP', ["So remember three things.",
            "One. It's not soggy skin. A wrinkled finger is smaller, not bigger.",
            "Two. Your nerves narrow the blood vessels, and the skin buckles.",
            "Three. Better grip may be the reason, but the tests disagree.",
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
    if T(1) < 0: remap(s_hook, {0: 0})(c, T, t)
    else: remap(s_hook, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

def short_clue(c, T, t):
    if T(1) < 0: remap(s_clue, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_clue, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

def short_how(c, T, t):
    if T(1) < 0: remap(s_squeeze, {0: (0, -9), 1: (0, -9), 2: 0})(c, T, t)
    else: remap(s_squeeze, {0: (1, -9), 1: (1, -9), 2: (1, -9), 3: (1, -9), 4: 1})(c, T, t)

def short_why(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'One idea: treads for wet hands', 68, GROOVE, 1 - hl(1), w='Bold')
    c.text(960, 150, 'A later test: no advantage. Still open', 64, YE, hl(1), w='Bold')
    study_cards(c, fd(T(0), .8), hl(1))

# The Short: its own complete mini-story (hook + answer -> the clue -> how it works -> the honest open question -> answer card).
SHORT_SCENES = [
 ('THE HOOK', ["Why do your fingers wrinkle in the bath?",
               "It isn't soggy skin. Your nerves do it."], short_hook),
 ('THE CLUE', ["In the nineteen thirties, doctors noticed fingers with damaged nerves stayed smooth in water.",
               "Healthy fingers wrinkled. The only difference was the nerve."], short_clue),
 ('HOW', ["After about five minutes, those nerves make the blood vessels under your fingertip narrow.",
          "The fingertip shrinks, but the skin on top doesn't. So it buckles into grooves."], short_how),
 ('WHY', ["One idea is treads for wet hands. One test found wet objects were moved twelve percent faster.",
          "A later test found no advantage. So that part is still open."], short_why),
 ('THE ANSWER', ["So why do fingers wrinkle? Not because water swells them.",
                 "Your nerves shrink the blood vessels, and the skin buckles."],
                card('Not soggy skin.', 'Your nerves did it.')),
]
SHORT_HITS = [(4, 1, 0.0)]
