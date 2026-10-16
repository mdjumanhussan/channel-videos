"""Episode: How Noise-Cancelling Headphones Work."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Noise-Cancelling Headphones Work'   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
SHORT_HOOK = 'How do headphones cancel noise?'         # headline on the vertical Short
HITS = [(0, 2, 0.0), (2, 3, 0.0), (4, 2, 0.0)]         # title card, the waves cancel, quiz answer
THUMB = ['SILENCE', 'FROM MORE', 'SOUND']
MUSIC_LEVEL = 0.006                                    # keeps the music about 20 dB under the voice (lesson of 2026-10-14)
# Narration spells names and years so the voice reads them naturally; captions show them normally.
CAPTION_FIXES = {
    'Paul Loyg': 'Paul Lueg', 'the nineteen thirties': 'the 1930s', 'nineteen seventy-eight': '1978',
    'plus one and minus one': '+1 and −1',
}
# Applied lesson (learnings.md, 2026-10-17): first five seconds in very short sentences, no greeting,
# and a beat of silence right after the tension line ("By making more sound."), which is its own
# narration line so the engine's line gap gives the pause before the question.

NOISE = PK; ANTI = CY; QUIET = GR
CUP = (60, 66, 110); CUSH = (95, 100, 150); SKIN = (235, 190, 160)

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def wave(c, x0, x1, y, amp, wl, ph, col, a=1.0, w=6, bg=BG, env=None):
    """Sine wave from x0 to x1 (wavelength wl px, phase ph radians). env(u) scales amplitude, u in 0..1."""
    if a <= 0.01 or x1 <= x0: return
    n = max(8, int((x1 - x0) / 6)); pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; u = i / n
        e = env(u) if env else 1.0
        pts.append((x, y - amp * e * math.sin(2 * math.pi * (x - x0) / wl - ph)))
    c.line(pts, col, w, a, bg)

def headphones(c, x, y, s, a=1.0, bg=BG, col=CUP, glow=None):
    """Front view of over-ear headphones centred at (x, y); s = half-width."""
    if a <= 0.01: return
    pts = [(x + s * .78 * math.cos(math.pi + math.pi * u / 30), y - s * .1 + s * .85 * math.sin(math.pi + math.pi * u / 30)) for u in range(31)]
    c.line(pts, col, s * .12, a, bg)
    for sg in (-1, 1):
        cx = x + sg * s * .78
        c.rr(cx - s * .2, y - s * .25, cx + s * .2, y + s * .45, s * .16, col, a, bg=bg, outline=glow, ow=4)
        c.rr(cx - s * .1, y - s * .12, cx + s * .1, y + s * .32, s * .08, CUSH, a, bg=col)

def bus(c, x, y, s, col=(230, 170, 60), a=1.0, bg=BG):
    """Side view of a bus centred at (x, y), length 2s."""
    if a <= 0.01: return
    c.rr(x - s, y - s * .38, x + s, y + s * .28, s * .1, col, a, bg=bg)
    for j in range(4):
        wx = x - s * .82 + j * s * .42
        c.rr(wx, y - s * .28, wx + s * .32, y - s * .04, 6, (150, 200, 240), a, bg=col)
    for dx in (-.6, .6):
        c.circ(x + dx * s, y + s * .3, s * .14, (30, 30, 46), a, bg=bg)
        c.circ(x + dx * s, y + s * .3, s * .06, DIM, a, bg=(30, 30, 46))

def ear(c, x, y, s, a=1.0, bg=BG):
    """Simple ear outline (right-facing side of a head)."""
    if a <= 0.01: return
    pts = [(x + s * .45 * math.cos(u / 20 * math.pi * 1.6 - math.pi * .8), y + s * .62 * math.sin(u / 20 * math.pi * 1.6 - math.pi * .8)) for u in range(21)]
    c.line(pts, SKIN, s * .12, a, bg)
    c.circ(x + s * .05, y + s * .05, s * .12, SKIN, a, bg=bg)

def plane(c, x, y, s, col=(200, 210, 235), a=1.0, bg=BG):
    if a <= 0.01: return
    c.rr(x - s, y - s * .13, x + s, y + s * .13, s * .13, col, a, bg=bg)
    k = c.k
    for poly in ([(x - s * .1, y), (x + s * .25, y), (x - s * .25, y + s * .75), (x - s * .45, y + s * .75)],
                 [(x - s * .1, y), (x + s * .25, y), (x - s * .25, y - s * .75), (x - s * .45, y - s * .75)],
                 [(x - s * .85, y), (x - s * .7, y), (x - s * .95, y - s * .4), (x - s * 1.02, y - s * .4)]):
        c.d.polygon([(px * k, py * k) for px, py in poly], fill=mix(col, a, bg))
    for j in range(4):
        c.circ(x + s * .35 + j * s * .14, y - s * .02, s * .035, (60, 90, 140), a, bg=col)

def baby(c, x, y, s, a=1.0, bg=BG, cry=1.0, t=0.0):
    """Round baby face; cry opens the mouth and adds tears."""
    if a <= 0.01: return
    c.circ(x, y, s, SKIN, a, bg=bg)
    c.circ(x, y - s * 1.02, s * .12, SKIN, a, bg=bg)
    for sg in (-1, 1):
        c.line([(x + sg * s * .45, y - s * .2), (x + sg * s * .2, y - s * .12)], (60, 40, 40), s * .08, a, SKIN)
        if cry > .1:
            c.circ(x + sg * s * .38, y + s * (.05 + .2 * ((t * 1.5) % 1)), s * .07, CY, a * cry, bg=SKIN)
    c.circ(x, y + s * .42, s * (.12 + .14 * cry), (150, 50, 60), a, bg=SKIN)

def chip(c, x, y, s, a=1.0, bg=BG, col=(40, 46, 90), lab='CHIP'):
    if a <= 0.01: return
    for j in range(4):
        for sg in (-1, 1):
            c.line([(x - s * .6 + j * s * .4, y + sg * s * .55), (x - s * .6 + j * s * .4, y + sg * s * .85)], DIM, 4, a, bg)
            c.line([(x + sg * s * .55, y - s * .6 + j * s * .4), (x + sg * s * .85, y - s * .6 + j * s * .4)], DIM, 4, a, bg)
    c.rr(x - s * .7, y - s * .7, x + s * .7, y + s * .7, 10, col, a, bg=bg, outline=YE, ow=4)
    c.text(x, y, lab, s * .32, YE, a, w='Bold', bg=col)

def mic(c, x, y, s, col=INK, a=1.0, bg=BG):
    if a <= 0.01: return
    c.rr(x - s * .3, y - s * .6, x + s * .3, y + s * .2, s * .3, col, a, bg=bg)
    c.line([(x, y + s * .2), (x, y + s * .55)], col, max(3, s * .1), a, bg)
    c.line([(x - s * .3, y + s * .55), (x + s * .3, y + s * .55)], col, max(3, s * .1), a, bg)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    headphones(c, 1590, 560, 220, 1, glow=CY)
    wave(c, 1200, 1340, 600, 70, 140, 0, NOISE, 1, 11)
    c.line([(1800, 600), (1890, 600)], QUIET, 11, 1)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(2), 0, .5)
    if a > 0:
        # moving from the very first frame: noise rolls in from the left and comes out flat on the right
        headphones(c, 960, 460, 240, a, glow=mix(CY, fd(T(1)) if T(1) > -.1 else 0))
        wave(c, 120, 700, 460, 110, 150, t * 6, NOISE, a, 9, env=lambda u: .6 + .4 * u)
        c.line([(1220, 460), (1800, 460)], QUIET, 9, a)
        c.text(410, 650, 'NOISE', 48, NOISE, a, w='Bold')
        c.text(1510, 650, 'QUIET', 48, QUIET, a, w='Bold')
        c.text(960, 170, 'Quieter...', 80, INK, a, w='Bold')
        if T(1) > -.1:
            k = a * fd(T(1))
            c.text(960, 790, 'by making MORE sound', 70, YE, k, w='Bold')
    if T(2) > 0:
        m = fd(T(2), .2, .7)
        c.text(960, 300 + 30 * (1 - m), 'How Noise-Cancelling', 128, INK, m, w='Bold')
        c.text(960, 460 + 30 * (1 - m), 'Headphones Work', 128, YE, m, w='Bold')
        c.line([(960 - 320 * m, 570), (960 + 320 * m, 570)], CY, 8, m)
        k = fd(T(2), 1.0)
        wave(c, 560, 860, 720, 50, 90, t * 6, NOISE, k, 7)
        wave(c, 560, 860, 760, 50, 90, t * 6 + math.pi, ANTI, k * .8, 7)
        c.arrow(910, 740, 1010, 740, INK, 7, k, 20)
        c.line([(1060, 735), (1360, 735)], QUIET, 8, k)

def s_wave(c, T, t):
    a0 = 1 - fd(T(3), -.4, .4)
    m = fd(T(0))
    c.text(960, 160, 'Sound is a wave in the air', 62, INK, m, w='Bold')
    k1 = fd(T(1)) if T(1) > -.1 else 0.0
    shake = 4 * math.sin(t * 40) * k1
    bus(c, 330, 470 + shake, 200, a=m)
    # air molecules: columns that bunch up and spread out as the wave travels right
    if k1 > 0:
        for col in range(26):
            x0 = 580 + col * 38
            dx = 16 * math.sin(2 * math.pi * col / 9 - t * 5)
            for row in range(7):
                c.circ(x0 + dx, 340 + row * 42, 7, CY, k1 * fd(T(1), col * .04))
        k2 = fd(T(2)) if T(2) > -.1 else 0.0
        if k2 > 0:
            c.text(760, 670, 'squeezed', 38, YE, k2, w='Bold')
            c.text(1180, 670, 'spread out', 38, DIM, k2, w='Bold')
            wave(c, 580, 1560, 760, 50, 342, t * 5 - math.pi / 2, NOISE, k2, 6)
    if T(3) > -.1:
        k3 = fd(T(3))
        ear(c, 1720, 470, 170, k3)
        drum = 10 * math.sin(t * 5)
        c.rr(1640 + drum, 410, 1656 + drum, 530, 6, YE, k3)
        c.text(1680, 640, 'eardrum moves', 36, YE, k3, w='Bold')

def s_flip(c, T, t):
    m = fd(T(0))
    c.text(960, 150, 'Now flip the wave', 62, INK, m, w='Bold')
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    sum_k = hl(3)
    # top: the noise; middle: the opposite wave; bottom: what you hear
    y1, y2, y3 = 340, 520, 730
    wave(c, 380, 1540, y1, 70, 290, t * 3, NOISE, m, 8)
    c.text(250, y1, 'Noise', 40, NOISE, m, w='Bold')
    k = hl(0)
    wave(c, 380, 1540, y2, 70, 290, t * 3 + math.pi, ANTI, k, 8)
    c.text(250, y2, 'Opposite', 40, ANTI, k, w='Bold')
    # markers: where the noise squeezes, the opposite wave spreads
    for li, phase, lab1, lab2 in ((1, .25, 'squeeze', 'spread'), (2, .75, 'spread', 'squeeze')):
        kk = hl(li) * (1 - sum_k)
        if kk <= 0: continue
        x = 380 + ((phase + t * 3 / (2 * math.pi)) % 1) * 290 + 290
        c.line([(x, y1 - 95), (x, y2 + 95)], YE, 3, kk)
        c.text(x, y1 - 115, lab1, 30, YE, kk, w='Bold')
        c.text(x, y2 + 115, lab2, 30, YE, kk, w='Bold')
    if sum_k > 0:
        c.text(250, 630, 'add them', 34, INK, sum_k, w='Bold')
        flat = 70 * (1 - fd(T(3), .3, 1.2))
        wave(c, 380, 1540, y3, flat, 290, t * 3, QUIET, sum_k, 9)
        c.text(250, y3, 'You hear', 40, QUIET, sum_k, w='Bold')
        c.text(1720, y3, '≈ quiet', 46, QUIET, fd(T(3), 1.2), w='Bold')
    if T(4) > -.1:
        pill(c, 960, 840, '+1  +  (−1)  =  0', YE, fd(T(4)), 46, h=80)

def s_inside(c, T, t):
    m = fd(T(0))
    c.text(960, 150, 'Inside the earcup', 62, INK, m, w='Bold')
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    # big cut-away earcup: outside on the left, your ear on the right
    c.rr(700, 260, 1260, 820, 60, CUP, m, outline=(90, 100, 160), ow=5)
    c.rr(1230, 300, 1310, 780, 30, CUSH, m)
    ear(c, 1500, 540, 190, m)
    wave(c, 120, 600, 540, 60, 130, t * 6, NOISE, m, 7)
    c.text(330, 430, 'outside noise', 36, NOISE, m, w='Bold')
    k1 = hl(1)
    mic(c, 660, 400, 70, INK, k1)
    if k1 > 0: c.text(560, 300, 'outside mic', 30, INK, k1, w='Bold')
    k2 = hl(2)
    chip(c, 900, 420, 90, k2, bg=CUP, lab='FLIP')
    if k2 > 0:
        c.arrow(700, 400, 815, 410, YE, 5, k2, 16)
        wave(c, 830, 970, 560, 30, 70, t * 6 + math.pi, ANTI, k2, 5, CUP)
    k3 = hl(3)
    if k3 > 0:
        c.circ(1100, 560, 80, (30, 34, 60), k3, bg=CUP, outline=ANTI, ow=6)
        c.circ(1100, 560, 30 + 4 * math.sin(t * 20), ANTI, k3, bg=(30, 34, 60))
        c.text(1100, 680, 'speaker', 30, ANTI, k3, w='Bold', bg=CUP)
        c.text(1100, 730, 'flipped wave + music', 26, INK, k3, w='Medium', bg=CUP)
        c.arrow(970, 470, 1040, 520, YE, 5, k3, 16)
    k4 = hl(4)
    if k4 > 0:
        mic(c, 1190, 360, 50, GR, k4, CUP)
        c.text(1000, 300, 'inside mic checks', 28, GR, k4, w='Bold', bg=CUP)
        c.text(1000, 860, 'Two mics, one chip, one speaker', 34, DIM, k4, w='Medium')

def s_quiz(c, T, t):
    m = fd(T(0))
    ans = fd(T(2)) if T(2) > -.1 else 0.0
    c.text(960, 160, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 245, 'On a plane, which is easier to cancel?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 190, 'The engine hum', 70, INK, ans, w='Bold')
    c.text(960, 265, 'Steady, low sounds are the easiest', 44, GR, fd(T(2), .6) if T(2) > -.1 else 0, w='Bold')
    k = m * fd(T(0), 1.0)
    dimL = 1; dimR = 1 - ans * .6
    plane(c, 560, 470, 200, mix((200, 210, 235), dimL), k)
    wave(c, 380, 740, 700, 45, 220, t * 3, mix(NOISE, dimL), k, 7)
    c.text(560, 790, 'engine hum', 42, INK, k, w='Bold')
    k2 = m * fd(T(0), 1.3)
    baby(c, 1360, 470, 130, k2 * dimR, cry=1 - ans * .5, t=t)
    wave(c, 1180, 1540, 700, 45, 40 + 15 * math.sin(t * 3), t * 9, mix(NOISE, dimR), k2, 5)
    c.text(1360, 790, 'baby crying', 42, mix(INK, dimR), k2, w='Bold')
    if ans > 0:
        c.check(560, 860, 36, GR, ans, fd(T(2), .3))
    if T(1) > 0 and ans < 1:
        p = clamp(T(1) / 2.2)
        ring(c, 960, 520, 70, 1 - p, CY, fd(T(1)) * (1 - ans))
        c.text(960, 520, 'or', 44, DIM, fd(T(1)) * (1 - ans), w='Bold')

def s_low(c, T, t):
    m = fd(T(0))
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    c.text(960, 150, 'Why low sounds are easier', 62, INK, m, w='Bold')
    # top row: long slow wave, the flipped copy keeps up
    c.rr(160, 220, 1760, 500, 30, CARD, m, outline=GR, ow=4)
    c.text(330, 270, 'LOW HUM', 38, GR, m, w='Bold', bg=CARD)
    wave(c, 480, 1560, 360, 70, 520, t * 2, NOISE, m, 8, CARD)
    k1 = hl(1)
    wave(c, 480, 1560, 360, 70 * (1 - .9 * k1), 520, t * 2, QUIET, k1, 8, CARD)
    if k1 > 0:
        c.text(1020, 460, 'long, steady waves: easy to predict', 34, GR, k1, w='Bold', bg=CARD)
        c.check(1660, 360, 34, GR, k1, fd(T(1), .4))
    # bottom row: short fast waves, a tiny delay makes the flip miss
    k2 = hl(2)
    if k2 > 0:
        c.rr(160, 540, 1760, 830, 30, CARD, k2, outline=PK, ow=4)
        c.text(330, 590, 'HIGH SOUNDS', 38, PK, k2, w='Bold', bg=CARD)
        wave(c, 480, 1560, 680, 60, 70, t * 9, NOISE, k2, 5, CARD, env=lambda u: .5 + .5 * abs(math.sin(u * 7 + t)))
    k3 = hl(3)
    if k3 > 0:
        wave(c, 480, 1560, 680, 60, 70, t * 9 + math.pi + 1.7, ANTI, k3, 5, CARD)
        c.text(1020, 790, 'a tiny delay, and the flip misses', 34, PK, k3, w='Bold', bg=CARD)
        c.cross(1660, 680, 40, PK, k3)

def s_seal(c, T, t):
    m = fd(T(0))
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a0 = 1 - fd(T(3), -.4, .4)
    if a0 > 0:
        c.text(960, 150, 'The simple trick: a seal', 62, INK, m * a0, w='Bold')
        k1 = hl(1) * a0
        c.rr(980, 230, 1080, 790, 40, CUP, max(k1, .001))
        c.rr(1080, 260, 1180, 760, 45, CUSH, max(k1, .001))
        ear(c, 1330, 510, 190, m * a0)
        if k1 > 0: c.text(1130, 830, 'soft cushion seals', 36, INK, k1, w='Bold')
        k2 = hl(2) * a0
        if k2 > 0:
            # high sound bounces off the cushion
            for j in range(3):
                y = 360 + j * 110
                p = ((t * .6 + j * .3) % 1)
                xx = 300 + 650 * min(p, .5) * 2 if p < .5 else 950 - 650 * (p - .5) * 2
                wave(c, xx - 120, xx, y, 22, 30, t * 12, NOISE, k2 * .9, 4)
            c.text(560, 280, 'high sounds bounce off', 38, NOISE, k2, w='Bold')
            # low rumble rolls through
            wave(c, 200, 1400, 690, 40, 400, t * 2, (230, 170, 60), k2, 7)
            c.text(560, 780, 'low rumble gets through', 38, (230, 170, 60), k2, w='Bold')
    if T(3) < -.1: return
    k = fd(T(3))
    c.text(960, 150, 'A team of two', 62, INK, k, w='Bold')
    for i, (x, col, top, lab, sub) in enumerate(((560, CUSH, 'The seal', 'blocks high sounds', 'voices, clatter'),
                                                 (1360, YE, 'The chip', 'cancels low hum', 'engines, rumble'))):
        kk = k * fd(T(3), .3 + i * .5)
        c.rr(x - 330, 260, x + 330, 800, 30, CARD, kk, outline=col, ow=5)
        if i == 0:
            c.rr(x - 50, 340, x + 50, 560, 40, CUSH, kk, bg=CARD)
        else:
            chip(c, x, 450, 100, kk, bg=CARD)
        c.text(x, 640, top, 54, INK, kk, w='Bold', bg=CARD)
        c.text(x, 705, lab, 40, col if i else (170, 180, 230), kk, w='Bold', bg=CARD)
        c.text(x, 760, sub, 32, DIM, kk, w='Medium', bg=CARD)

def s_history(c, T, t):
    m = fd(T(0))
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    c.text(960, 150, 'An old idea', 62, INK, m, w='Bold')
    c.line([(200, 560), (1720, 560)], DIM, 5, m)
    items = [(1, 480, '1930s', 'Paul Lueg patents', 'sound cancelling'),
             (2, 1000, '1978', 'Amar Bose, on a flight,', 'starts working on it'),
             (3, 1480, 'First users', 'headsets', 'for pilots')]
    for li, x, yr, l1, l2 in items:
        k = hl(li)
        if k <= 0: continue
        c.circ(x, 560, 22, YE, k)
        c.text(x, 480, yr, 58, YE, k, w='Bold')
        c.text(x, 650, l1, 36, INK, k, w='Bold')
        c.text(x, 700, l2, 36, INK, k, w='Bold')
        if li == 1:
            c.rr(x - 70, 250, x + 70, 420, 10, (230, 225, 210), k)
            for j in range(5): c.line([(x - 45, 285 + j * 25), (x + 45, 285 + j * 25)], (150, 150, 170), 4, k, (230, 225, 210))
            c.circ(x + 35, 385, 20, PK, k, bg=(230, 225, 210))
        elif li == 2:
            plane(c, x, 330 + 6 * math.sin(t * 2), 130, a=k)
        else:
            headphones(c, x, 340, 110, k, glow=CY)
    c.text(960, 840, 'Lueg: filed 1933, US patent 1936  ·  Bose: first aviation headset sold 1989', 26, DIM, hl(3), w='Regular')

REC = [('1', 'Sound is a wave', NOISE), ('2', 'Play the opposite', ANTI), ('3', 'Chip + seal', GR)]
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
            wave(c, x - 180, x + 180, y, 60, 120, t * 4, NOISE, m, 7, CARD)
            c.text(x, y + 120, 'squeezed and stretched air', 28, DIM, m, w='Medium', bg=CARD)
        elif i == 1:
            wave(c, x - 180, x + 180, y - 50, 40, 120, t * 4, NOISE, m, 6, CARD)
            wave(c, x - 180, x + 180, y + 20, 40, 120, t * 4 + math.pi, ANTI, m, 6, CARD)
            c.line([(x - 180, y + 100), (x + 180, y + 100)], QUIET, 7, m, CARD)
        else:
            c.rr(x - 150, y - 90, x - 70, y + 90, 35, CUSH, m, bg=CARD)
            chip(c, x + 80, y, 80, m, bg=CARD)
            c.text(x, y + 130, 'high  ·  low', 32, DIM, m, w='Medium', bg=CARD)
        c.text(x, 740 + up, lab, 38, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Noise-cancelling headphones make the world quieter.",
            "By making more sound.",
            "So how does adding sound give you quiet? Here is how it works."], s_hook),
 ('1  ·  SOUND', ["First, what is sound?",
            "When a bus engine rumbles, it pushes the air in tiny waves.",
            "The air gets squeezed together, then spreads out, over and over.",
            "Those waves reach your ear, and push your eardrum in and out."], s_wave),
 ('2  ·  THE FLIP', ["Now imagine a second wave that is the exact opposite.",
            "Where the noise squeezes the air, the new wave spreads it out.",
            "Where the noise spreads it out, the new wave squeezes.",
            "Add them together, and they cancel. Scientists call this destructive interference.",
            "Like plus one and minus one making zero."], s_flip),
 ('3  ·  INSIDE', ["Your headphones do this all the time.",
            "A tiny microphone on the outside listens to the noise around you.",
            "A chip flips that wave upside down.",
            "The speaker plays the flipped wave, along with your music.",
            "Many headphones also have a microphone inside, to check what is left and fix it."], s_inside),
 ('4  ·  QUICK QUESTION', ["Quick question. On a plane, which is easier to cancel: the engine's hum, or a baby crying?",
            "Three, two, one.",
            "The engine hum. Steady, low sounds are the easiest to cancel."], s_quiz),
 ('5  ·  LOW VS HIGH', ["Here is why.",
            "Low sounds have long waves that repeat in a steady pattern, so the chip can predict them and keep up.",
            "High sounds, like voices and clatter, have short waves that change quickly.",
            "A tiny delay, and the flipped wave no longer lines up."], s_low),
 ('6  ·  THE SEAL', ["So for high sounds, headphones use a simpler trick.",
            "Soft cushions, or the rubber tips of earbuds, seal around your ear.",
            "That seal blocks high sounds well, but low rumble gets through.",
            "So they work as a team. The seal blocks high sounds. The chip cancels low hum."], s_seal),
 ('7  ·  AN OLD IDEA', ["The idea is older than you might think.",
            "A German physicist, Paul Loyg, patented sound cancelling in the nineteen thirties.",
            "In nineteen seventy-eight, on a flight, Amar Bose was annoyed by noise in his airline headphones, and started working on a fix.",
            "Some of the first noise-cancelling headsets were made for pilots."], s_history),
 ('RECAP', ["So remember three things.",
            "One. Sound is a wave of squeezed and stretched air.",
            "Two. Headphones play the opposite wave, so the two cancel out.",
            "Three. The chip cancels steady low hum, and the seal blocks high sounds.",
            "If this helped, subscribe for more."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('QUIET', ["Noise-cancelling headphones make the world quieter.",
            "By making more sound.",
            "So how does adding sound give you quiet?"], s_hook),
 ('THE FLIP', ["Sound is a wave. Your headphones make the exact opposite wave.",
               "Where the noise squeezes the air, the new wave spreads it out.",
               "Where the noise spreads it out, the new wave squeezes.",
               "Add them together, and they cancel."], s_flip),
 ('INSIDE', ["Here is how they do it.",
             "A tiny microphone on the outside listens to the noise.",
             "A chip flips that wave upside down.",
             "The speaker plays the flipped wave, along with your music.",
             "A second microphone inside checks what is left."], s_inside),
 ('THE ANSWER', ["That is the answer. Headphones go quiet by playing the opposite of the noise.",
                 "It works best on steady low hum, like a plane engine. Follow for more."],
                card('They play the opposite wave', 'Noise + opposite = quiet')),
]
SHORT_HITS = [(3, 0, 0.0)]
