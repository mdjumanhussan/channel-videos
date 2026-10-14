"""Episode: What SPF Really Means (SPF 50 vs SPF 30)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'What SPF Really Means'             # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {'U-V-A': 'UVA'}                   # spoken letter by letter, shown as one word
SHORT_HOOK = 'Is SPF 50 twice as strong as 30?'   # headline on the vertical Short
HITS = [(0, 1, 0.0), (0, 3, 0.0), (3, 2, 0.0)]    # 'it is not', title card, the quiz answer
THUMB = ['SPF 50 VS 30', 'REAL DIFFERENCE']
# Applied lesson (learnings.md, 2026-10-14): music bed set lower so it sits about 20 dB under the voice.
MUSIC_LEVEL = 0.006

SUNC = (255, 190, 60); SKIN = (232, 178, 140); SKIN2 = (200, 140, 105); BURN = (235, 80, 70)
UVB = PK; UVA = PU; LOTION = (245, 246, 255); BOT = (60, 190, 230)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def sun(c, x, y, r, a=1.0, t=0.0, bg=BG):
    if a <= 0.01: return
    for k in range(10):
        q = t * .4 + k * math.pi / 5
        c.line([(x + r * 1.3 * math.cos(q), y + r * 1.3 * math.sin(q)), (x + r * 1.7 * math.cos(q), y + r * 1.7 * math.sin(q))], SUNC, max(4, r * .12), a, bg)
    c.circ(x, y, r, SUNC, a, bg=bg)

def bottle(c, x, y, s, label, col=BOT, a=1.0, bg=BG, sub='SUNSCREEN'):
    """Sunscreen bottle; (x, y) is the bottom centre, s its height."""
    if a <= 0.01: return
    w = s * .46
    c.rr(x - w * .22, y - s * 1.08, x + w * .22, y - s * .92, 8, (230, 235, 250), a, bg=bg)     # cap
    c.rr(x - w / 2, y - s * .94, x + w / 2, y, s * .1, col, a, bg=bg)
    c.rr(x - w * .4, y - s * .7, x + w * .4, y - s * .22, 12, LOTION, a, bg=col)
    c.text(x, y - s * .52, label, max(18, s * .095), BG, a, w='Bold', bg=LOTION)
    c.text(x, y - s * .34, sub, max(12, s * (.035 if len(sub) > 10 else .045)), DIM, a, w='Bold', bg=LOTION)

def wave(c, x0, y0, x1, y1, col, a=1.0, amp=10, per=40, w=5, t=0.0, p=1.0):
    """Wavy ray from (x0, y0) toward (x1, y1); p = fraction drawn."""
    if a <= 0.01 or p <= 0: return
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    pts = []
    for i in range(int(60 * p) + 2):
        d = L * min(p, i / 60)
        o = amp * math.sin(d / per * 2 * math.pi - t * 6)
        pts.append((x0 + ux * d - uy * o, y0 + uy * d + ux * o))
    c.line(pts, col, w, a)

def skin_block(c, x0, y0, x1, y1, a=1.0, red=0.0, layers=False, bg=BG):
    """Side view of skin: top layer + deeper layer."""
    if a <= 0.01: return
    top = mix(BURN, red, SKIN)
    c.rr(x0, y0, x1, y1, 14, SKIN2, a, bg=bg)
    c.rr(x0, y0, x1, y0 + (y1 - y0) * .35, 14, top, a, bg=bg)
    if layers:
        c.text(x1 + 24, y0 + (y1 - y0) * .17, 'outer layer', 30, DIM, a, 'lm', 'Medium')
        c.text(x1 + 24, y0 + (y1 - y0) * .67, 'deeper layer', 30, DIM, a, 'lm', 'Medium')

def spoon(c, x, y, s, a=1.0, bg=BG, fill=True):
    if a <= 0.01: return
    c.line([(x + s * .35, y), (x + s * 1.3, y)], (200, 205, 225), s * .14, a, bg)
    c.circ(x, y, s * .42, (200, 205, 225), a, bg=bg)
    if fill: c.circ(x, y, s * .3, LOTION, a, bg=(200, 205, 225))

def person(c, x, y, s, a=1.0, bg=BG, col=SKIN):
    """Front-facing figure; (x, y) is the top of the head, s the height."""
    if a <= 0.01: return
    c.circ(x, y + s * .09, s * .09, col, a, bg=bg)
    c.rr(x - s * .16, y + s * .2, x + s * .16, y + s * .6, s * .05, col, a, bg=bg)           # body
    for sg in (-1, 1):
        c.line([(x + sg * s * .17, y + s * .24), (x + sg * s * .27, y + s * .55)], col, s * .07, a, bg)   # arms
        c.line([(x + sg * s * .08, y + s * .6), (x + sg * s * .1, y + s * .98)], col, s * .08, a, bg)      # legs

def cloud(c, x, y, s, a=1.0, col=(170, 180, 215), bg=BG):
    if a <= 0.01: return
    for dx, dy, r in ((-.45, .1, .32), (0, -.1, .45), (.45, .1, .32)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)
    c.rr(x - .75 * s, y + .05 * s, x + .75 * s, y + .42 * s, .18 * s, col, a, bg=bg)

def thumb_art(c):
    bottle(c, 1340, 930, 640, 'SPF 30', BOT)
    bottle(c, 1700, 930, 640, 'SPF 50', YE)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(3), 0, .5)
    if a > 0:
        # visible from the very first frame: the question as text, two bottles
        c.text(960, 210, 'Is SPF 50 twice as', 84, INK, a * fd(t, 0, .2), w='Bold')
        c.text(960, 315, 'strong as SPF 30?', 84, YE, a * fd(t, 0, .2), w='Bold')
        bottle(c, 620, 820, 400, 'SPF 30', BOT, a * fd(t, 0, .3))
        bottle(c, 1300, 820, 400, 'SPF 50', YE, a * fd(t, 0, .3))
        c.text(960, 620, '2x ?', 90, INK, a * fd(t, .2, .3), w='Bold')
        if T(1) > 0:
            k = a * fd(T(1))
            c.cross(960, 620, 120, PK, k)
            pill(c, 960, 455, 'No. Much closer than it looks', PK, k, 38, h=70)
        if T(2) > 0:
            k = a * fd(T(2))
            c.rr(1520, 470, 1840, 640, 24, CARD, k, outline=YE, ow=5)
            c.text(1680, 525, 'And a bigger', 32, INK, k, w='Bold', bg=CARD)
            c.text(1680, 580, 'problem...', 32, YE, k, w='Bold', bg=CARD)
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 380 + 30 * (1 - m), 'What SPF', 150, INK, m, w='Bold')
        c.text(960, 550 + 30 * (1 - m), 'Really Means', 150, YE, m, w='Bold')
        c.line([(960 - 300 * m, 665), (960 + 300 * m, 665)], SUNC, 8, m)
        c.text(960, 745, 'and the mistake most people make', 46, DIM, fd(T(3), .9), w='Medium')
        sun(c, 300, 300, 60, fd(T(3), 1.1), t)

def s_measure(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        for i, (L, rest) in enumerate([('S', 'un'), ('P', 'rotection'), ('F', 'actor')]):
            k = a0 * fd(T(0), .3 + i * .3); y = 330 + i * 170
            c.text(560, y, L, 150, YE, k, 'lm', 'Bold')
            c.text(700, y + 8, rest, 110, INK, k, 'lm', 'Bold')
    if T(1) > -.1:
        m = fd(T(1)) * (1 - fd(T(2), -.4, .4))
        if m > 0:
            c.text(960, 190, 'SPF measures one thing', 64, INK, m, w='Bold')
            sun(c, 330, 360, 80, m, t)
            for j in range(3):
                wave(c, 430, 380 + j * 40, 900, 640 + j * 20, UVB, m, 9, 36, 5, t, fd(T(1), .3 + j * .2, 1.0))
            red = ease(clamp(T(1, 1.6) / 2.5))
            skin_block(c, 820, 660, 1180, 820, m, red)
            c.text(1000, 860, 'skin', 30, DIM, m, w='Medium')
            c.text(1460, 380, 'UVB', 110, UVB, m * fd(T(1), .8), w='Bold')
            c.text(1460, 480, 'the rays that mainly', 40, INK, m * fd(T(1), 1.2), w='Bold')
            c.text(1460, 535, 'cause sunburn', 40, INK, m * fd(T(1), 1.2), w='Bold')
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 190, 'The lab test', 66, INK, m, w='Bold')
    # two timelines: bare skin vs protected skin
    x0, x1 = 520, 1680
    rows = [('No sunscreen', 10, PK, 2), ('With sunscreen', 300, GR, 2)]
    for i, (lab, mins, col, li) in enumerate(rows):
        y = 360 + i * 190; k = m * fd(T(2), .4 + i * .4)
        c.text(x0 - 30, y, lab, 38, INK, k, 'rm', 'Bold')
        c.rr(x0, y - 34, x1, y + 34, 17, CARD, k)
        if T(3) > -.1:
            p = ease(clamp(T(3, .3 + i * 1.2) / 1.4))
            xe = x0 + (x1 - x0) * (mins / 300) * p
            c.rr(x0, y - 34, max(x0 + 34, xe), y + 34, 17, col, k * fd(T(3), .3 + i * 1.2))
            c.text(min(x1, max(x0 + 34, xe)) + 20 if mins < 100 else x1 - 30, y, f'{mins} min', 40,
                   INK if mins < 100 else BG, k * fd(T(3), 1.0 + i * 1.2), 'lm' if mins < 100 else 'rm', 'Bold', bg=CARD if mins < 100 else col)
        c.text(x0, y + 66, 'time until skin goes red', 26, DIM, k, 'lm', 'Medium')
    if T(3) > 0:
        k = fd(T(3), 3.0)
        c.text(960, 720, '300 ÷ 10 = SPF 30', 72, YE, k, w='Bold')
        c.text(1680, 800, 'Illustrative numbers', 28, DIM, k, 'rm', 'Regular')
    if T(4) > 0:
        k = fd(T(4)); o = fd(T(4), 0, .4)
        c.rr(0, 140, 1920, 900, 0, BG, o * .97)
        c.text(960, 300, 'Lab maths, ideal conditions', 70, INK, k, w='Bold')
        for i, lab in enumerate(['Sweat', 'Water', 'Rubbing']):
            kk = k * fd(T(4), .8 + i * .35); x = 560 + i * 400
            c.rr(x - 160, 450, x + 160, 600, 30, CARD, kk, outline=PK, ow=4)
            c.text(x, 525, lab, 48, PK, kk, w='Bold', bg=CARD)
        c.text(960, 720, 'Real life gives less', 64, YE, k * fd(T(4), 1.8), w='Bold')

def s_percent(c, T, t):
    m = fd(T(0))
    c.text(960, 190, 'How much UVB is blocked', 66, INK, m, w='Bold')
    x0, x1 = 560, 1600
    rows = [('SPF 15', 93, DIM), ('SPF 30', 97, BOT), ('SPF 50', 98, YE)]
    for i, (lab, pc, col) in enumerate(rows):
        li = i + 1; y = 340 + i * 150
        if T(li) < -.1: continue
        k = fd(T(li)); p = ease(clamp(T(li, .2) / 1.2))
        c.text(x0 - 30, y, lab, 50, col, k, 'rm', 'Bold')
        c.rr(x0, y - 40, x1, y + 40, 20, CARD, k)
        c.rr(x0, y - 40, x0 + (x1 - x0) * pc / 100 * p, y + 40, 20, col, k)
        c.text(x1 + 30, y, f'{int(round(pc * p))}%', 56, INK, k, 'lm', 'Bold')
    if T(4) > 0:
        k = fd(T(4))
        y0, y1 = 490, 640
        xa, xb = x0 + (x1 - x0) * .97, x0 + (x1 - x0) * .98
        c.line([(xa, y0 - 60), (xa, y1 + 60)], INK, 3, k * .6)
        c.line([(xb, y1 - 60), (xb, y1 + 60)], YE, 3, k)
        pill(c, 1080, 790, 'From 30 to 50: about 1% more blocked', YE, k, 40, h=76)
    c.text(960, 870, 'Approximate lab figures', 26, DIM, m * fd(T(0), .6), w='Regular')

def dots(c, cx, cy, n_red, a, t, reveal=1.0):
    """10x10 grid of UVB 'units': blocked ones dim, the ones that get through in pink."""
    for j in range(100):
        x = cx - 180 + (j % 10) * 40; y = cy - 180 + (j // 10) * 40
        thru = j >= 100 - n_red
        col = UVB if (thru and reveal > 0) else (70, 80, 130)
        r = 13 + (4 * math.sin(t * 4) if thru and reveal > 0 else 0)
        c.circ(x, y, r, col, a * (1 if not thru else max(.35, reveal)))

def s_quiz(c, T, t):
    a0 = 1 - fd(T(2), -.4, .4)
    if a0 > 0:
        m = fd(T(0)) * a0
        c.text(960, 190, 'Quick question', 70, YE, m, w='Bold')
        c.circ(500, 520, 170, CARD, m, outline=YE, ow=6)
        c.text(500, 520, '?', 220, YE, m, w='Bold', bg=CARD)
        c.text(1260, 430, 'Is 1% more', 70, INK, m * fd(T(0), .4), w='Bold')
        c.text(1260, 530, 'worth anything?', 70, INK, m * fd(T(0), .4), w='Bold')
        for i, lab in enumerate(['A  Not really', 'B  Yes']):
            kk = m * fd(T(0), 1.2 + i * .3); x = 1060 + i * 400
            c.rr(x - 170, 640, x + 170, 720, 40, CARD, kk, outline=(60, 70, 120), ow=5)
            c.text(x, 680, lab, 36, INK, kk, w='Bold', bg=CARD)
        if T(1) > 0:
            p = clamp(T(1) / 2.2)
            pts = [(500 + 195 * math.sin(2 * math.pi * u / 60), 520 - 195 * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * (1 - p)) + 1)]
            c.line(pts, CY, 10, fd(T(1)) * a0)
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 190, 'Yes! Count what gets through', 66, GR, m, w='Bold')
    rv = fd(T(3), .4) if T(3) > -.1 else 0.0
    for i, (lab, n, col) in enumerate([('SPF 30', 3, BOT), ('SPF 50', 2, YE)]):
        cx = 620 + i * 680
        k = m * fd(T(2), .4 + i * .3)
        c.text(cx, 278, lab, 54, col, k, w='Bold')
        dots(c, cx, 500, n, k, t, rv)
        c.text(cx, 740, f'{n} in 100 get through', 42, UVB, k * fd(T(3), .8 + i * 1.6) if T(3) > -.1 else 0, w='Bold')
    if T(4) > 0:
        k = fd(T(4))
        pill(c, 960, 830, 'About a third less UVB reaches your skin', GR, k, 38, h=70)

def s_catch(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 440, 'Now', 120, INK, a0, w='Bold')
        c.text(960, 590, 'the catch', 140, YE, a0, w='Bold')
    if T(1) > -.1:
        m = fd(T(1)) * (1 - fd(T(3), -.4, .4))
        if m > 0:
            c.text(960, 190, 'How much the lab uses vs. what we use', 56, INK, m, w='Bold')
            for i, (lab, th, col, li) in enumerate([('Lab test', 70, GR, 1), ('Most people', 16, PK, 2)]):
                if T(li) < -.1: continue
                k = fd(T(li)) * m; x = 560 + i * 800
                skin_block(c, x - 260, 520, x + 260, 760, k)
                g = ease(clamp(T(li, .3) / 1.0))
                c.rr(x - 260, 520 - th * g, x + 260, 524, 10, LOTION, k)
                c.text(x, 330, lab, 52, col, k, w='Bold')
                c.text(x, 400, '2 mg per cm²' if i == 0 else 'a thin smear', 40, INK, k * fd(T(li), .6), w='Bold')
                c.text(x, 820, 'sunscreen layer (simplified)', 26, DIM, k, w='Regular')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 190, 'What you may really get', 64, INK, m, w='Bold')
    bottle(c, 430, 800, 460, 'SPF 50', YE, m)
    c.arrow(650, 540, 900, 540, DIM, 7, m * fd(T(3), .8), 22)
    c.text(1300, 430, 'a third to a quarter', 56, PK, m * fd(T(3), 1.0), w='Bold')
    c.text(1300, 500, 'of the label', 56, PK, m * fd(T(3), 1.0), w='Bold')
    c.text(1300, 580, 'one estimate, Medical Journal of Australia', 30, DIM, m * fd(T(3), 1.6), w='Medium')
    if T(4) > 0:
        k = fd(T(4))
        c.rr(980, 650, 1620, 820, 30, CARD, k, outline=PK, ow=5)
        c.text(1300, 705, 'may work more like', 40, INK, k, w='Bold', bg=CARD)
        c.text(1300, 775, 'SPF 15', 72, PK, k * fd(T(4), .6), w='Bold', bg=CARD)
        c.text(1300, 860, 'Estimate, varies by person', 26, DIM, k, w='Regular')

PARTS = [(-.3, .14, 'face + neck'), (0, .4, 'front'), (.3, .4, 'back'), (-.27, .38, 'arm'), (.27, .38, 'arm'), (-.09, .8, 'leg'), (.09, .8, 'leg')]
def s_amount(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(3), -.4, .4))
    if a0 > 0:
        c.text(960, 190, 'How much is enough?', 70, INK, a0, w='Bold')
        X, Y, Sz = 520, 250, 600
        person(c, X, Y, Sz, a0)
        if T(1) > -.1:
            k = fd(T(1)) * a0
            c.text(1340, 360, 'About 35 mL', 90, YE, k, w='Bold')
            c.text(1340, 450, 'for an adult\'s whole body', 40, INK, k * fd(T(1), .5), w='Medium')
            c.text(1340, 520, '(Cancer Council Australia)', 30, DIM, k * fd(T(1), .5), w='Regular')
            for i in range(7):
                spoon(c, 1060 + i * 90, 640, 40, k * fd(T(1), 1.4 + i * .18))
            c.text(1340, 730, 'around 7 teaspoons', 46, LOTION, k * fd(T(1), 2.4), w='Bold')
        if T(2) > -.1:
            k = fd(T(2)) * a0
            pts = [(X, Y + Sz * .09), (X - Sz * .06, Y + Sz * .36), (X + Sz * .06, Y + Sz * .46), (X - Sz * .24, Y + Sz * .42),
                   (X + Sz * .24, Y + Sz * .42), (X - Sz * .09, Y + Sz * .8), (X + Sz * .09, Y + Sz * .8)]
            for i, (px, py) in enumerate(pts):
                kk = k * fd(T(2), .3 + i * .35)
                c.circ(px, py, 24, YE, kk, bg=SKIN); c.text(px, py, str(i + 1), 26, BG, kk, w='Bold', bg=YE)
            c.text(1340, 800, 'at least 1 teaspoon per area, back too', 32, DIM, k, w='Medium')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 190, 'When to put it on', 66, INK, m, w='Bold')
    for i, (big, small, col, li) in enumerate([('20 min', 'before you go out', CY, 3), ('Every 2 hours', 'reapply', YE, 4)]):
        if T(li) < -.1: continue
        k = fd(T(li)); x = 560 + i * 800
        c.circ(x, 470, 150, CARD, k, outline=col, ow=8)
        ang = t * (.6 if i else .3)
        c.line([(x, 470), (x + 90 * math.sin(ang), 470 - 90 * math.cos(ang))], col, 10, k, CARD)
        c.line([(x, 470), (x + 60 * math.sin(ang / 12), 470 - 60 * math.cos(ang / 12))], INK, 10, k, CARD)
        c.circ(x, 470, 12, col, k, bg=CARD)
        c.text(x, 690, big, 64, col, k, w='Bold')
        c.text(x, 760, small, 38, INK, k, w='Medium')
    if T(4) > 0:
        k = fd(T(4), 1.4)
        c.text(1360, 840, '+ after swimming, sweating or towel drying', 32, DIM, k, w='Bold')

def s_uva(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 420, 'SPF only tells', 110, INK, a0, w='Bold')
        c.text(960, 560, 'half the story', 110, UVA, a0, w='Bold')
    if T(1) > -.1:
        m = fd(T(1)) * (1 - fd(T(4), -.4, .4))
        if m > 0:
            c.text(960, 190, 'Two kinds of UV', 66, INK, m, w='Bold')
            sun(c, 260, 330, 70, m, t)
            skin_block(c, 760, 560, 1300, 820, m, 0, layers=True)
            # UVB stops in the outer layer; UVA reaches deeper
            wave(c, 360, 380, 900, 600, UVB, m, 8, 30, 6, t, fd(T(1), .2, 1.0))
            wave(c, 360, 420, 1120, 760, UVA, m * fd(T(1), .3), 12, 60, 7, t, fd(T(1), .6, 1.2))
            c.text(560, 600, 'UVB', 48, UVB, m * fd(T(1), .4), w='Bold')
            c.text(560, 780, 'UVA', 48, UVA, m * fd(T(1), .8), w='Bold')
            pill(c, 1560, 330, 'UVA: up to 95% of UV', UVA, m * fd(T(1), 1.6), 34, fg=INK)
            if T(2) > -.1:
                k = fd(T(2)) * m
                c.text(1560, 430, 'goes deeper', 40, INK, k, w='Bold')
                c.text(1560, 485, 'linked to wrinkles', 40, INK, k * fd(T(2), .5), w='Bold')
                # window pane with a ray passing through
                kk = k * fd(T(2), 2.0)
                c.rr(1620, 560, 1820, 760, 8, (90, 140, 190), kk * .5, outline=(170, 200, 235), ow=6)
                c.line([(1720, 560), (1720, 760)], (170, 200, 235), 6, kk)
                wave(c, 1520, 600, 1880, 720, UVA, kk, 8, 40, 5, t)
                c.text(1720, 810, 'passes windows', 30, DIM, kk, w='Medium')
            if T(3) > 0:
                k = fd(T(3))
                pill(c, 1030, 470, 'Both raise skin cancer risk', PK, k, 38, h=70)
    if T(4) < -.1: return
    m = fd(T(4))
    c.text(960, 190, 'Look for these words', 66, INK, m, w='Bold')
    bottle(c, 640, 830, 560, 'SPF 50', YE, m, sub='BROAD SPECTRUM')
    k = m * fd(T(4), .8)
    pill(c, 1300, 420, 'BROAD SPECTRUM', GR, k, 52, h=96)
    c.text(1300, 540, 'protects against', 44, INK, k * fd(T(4), .6), w='Bold')
    c.text(1180, 620, 'UVA', 64, UVA, k * fd(T(4), 1.0), w='Bold')
    c.text(1300, 620, '+', 64, INK, k * fd(T(4), 1.0), w='Bold')
    c.text(1420, 620, 'UVB', 64, UVB, k * fd(T(4), 1.0), w='Bold')

def s_feel(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if a0 > 0:
        c.text(960, 190, 'You cannot see or feel UV', 66, INK, a0, w='Bold')
        # thermometer (cool) vs UV meter (high)
        kk = a0 * fd(T(1), 0) if T(1) > -.1 else 0.0
        X = 560
        c.rr(X - 30, 330, X + 30, 700, 30, CARD, a0, outline=DIM, ow=4)
        c.circ(X, 740, 60, CY, a0); c.rr(X - 14, 560, X + 14, 720, 10, CY, a0)
        c.text(X, 850, 'Feels cool', 44, CY, a0, w='Bold')
        cloud(c, 820, 360, 90, a0 * .9)
        X2 = 1360
        c.rr(X2 - 220, 330, X2 + 220, 760, 30, CARD, kk, outline=UVA, ow=5)
        c.text(X2, 400, 'UV index', 44, INK, kk, w='Bold', bg=CARD)
        lvl = ease(clamp(T(1, .5) / 1.6)) if T(1) > -.1 else 0
        c.text(X2, 560, str(int(round(2 + 6 * lvl))), 180, UVA, kk, w='Bold', bg=CARD)
        c.text(X2, 700, 'can still be high', 38, UVA, kk * fd(T(1), 1.2), w='Bold', bg=CARD)
        c.text(X2, 850, 'Example', 28, DIM, kk, w='Regular')
    if T(2) < -.1: return
    m = fd(T(2)) * (1 - fd(T(3), -.4, .4))
    if m > 0:
        c.text(960, 190, 'Check the UV index', 66, INK, m, w='Bold')
        # phone with a weather app
        c.rr(420, 280, 760, 860, 40, (40, 46, 80), m, outline=DIM, ow=5)
        c.rr(450, 330, 730, 810, 20, CARD, m, bg=(40, 46, 80))
        sun(c, 590, 440, 46, m, t, CARD)
        c.text(590, 580, 'UV  7', 64, YE, m * fd(T(2), .6), w='Bold', bg=CARD)
        c.text(590, 650, 'Example', 26, DIM, m * fd(T(2), .6), w='Regular', bg=CARD)
        k = m * fd(T(2), 1.2)
        c.text(1300, 430, 'UV index', 60, INK, k, w='Bold')
        c.text(1300, 570, '3 or above', 110, YE, k, w='Bold')
        c.text(1300, 690, 'protect your skin', 60, INK, k * fd(T(2), 1.8), w='Bold')
    if T(3) < -.1: return
    m = fd(T(3))
    c.text(960, 190, 'Cancer Council recommends', 64, INK, m, w='Bold')
    for i, (lab, col) in enumerate([('SPF 50 or 50+', YE), ('Broad spectrum', GR), ('Water resistant', CY)]):
        k = m * fd(T(3), .4 + i * .5); y = 330 + i * 110
        c.check(560, y, 34, col, k, fd(T(3), .5 + i * .5))
        c.text(620, y, lab, 50, col, k, 'lm', 'Bold')
    if T(4) > 0:
        k = fd(T(4))
        c.text(960, 680, 'plus', 40, DIM, k, w='Medium')
        for i, lab in enumerate(['Hat', 'Clothing', 'Sunglasses', 'Shade']):
            kk = k * fd(T(4), .3 + i * .3); x = 450 + i * 340
            c.rr(x - 140, 730, x + 140, 830, 50, CARD, kk, outline=SUNC, ow=4)
            c.text(x, 780, lab, 40, SUNC, kk, w='Bold', bg=CARD)

REC = [('1', 'SPF = sunburn (UVB) rays', YE), ('2', 'Amount matters most', LOTION), ('3', 'Broad spectrum + UV index', UVA)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 255, 290 + up, x + 255, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 190, 355 + up, 40, col, m, bg=CARD); c.text(x - 190, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 540 + up
        if i == 0:
            c.text(x, y - 60, 'SPF 30: 97%', 50, BOT, m, w='Bold', bg=CARD)
            c.text(x, y + 20, 'SPF 50: 98%', 50, YE, m, w='Bold', bg=CARD)
            c.text(x, y + 90, 'of UVB blocked', 30, DIM, m, w='Medium', bg=CARD)
        elif i == 1:
            for j in range(7): spoon(c, x - 190 + j * 58, y - 40, 22, m, CARD)
            c.text(x, y + 40, '~7 teaspoons', 44, LOTION, m, w='Bold', bg=CARD)
            c.text(x, y + 100, 'reapply every 2 hours', 30, DIM, m, w='Medium', bg=CARD)
        else:
            c.text(x, y - 40, 'UVA + UVB', 50, UVA, m, w='Bold', bg=CARD)
            c.text(x, y + 40, 'UV 3+: protect', 44, YE, m, w='Bold', bg=CARD)
            c.text(x, y + 100, 'not the temperature', 30, DIM, m, w='Medium', bg=CARD)
        c.text(x, 725 + up, lab, 30, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Is SPF 50 almost twice as strong as SPF 30?",
            "It is not. The difference is much smaller than you think.",
            "But the label hides a bigger problem.",
            "Here is what SPF really means."], s_hook),
 ('1  ·  WHAT SPF MEASURES', ["SPF stands for Sun Protection Factor.",
            "It measures how well a sunscreen blocks UVB, the rays that mainly cause sunburn.",
            "In a lab, testers time how long skin takes to go red, with and without it.",
            "If bare skin reddens in 10 minutes, and protected skin in 300, that is SPF 30.",
            "That is lab maths, in ideal conditions. Real life gives less."], s_measure),
 ('2  ·  THE PERCENTAGES', ["Now as percentages.",
            "SPF 15 blocks about 93 percent of UVB.",
            "SPF 30 blocks about 97 percent.",
            "SPF 50 blocks about 98 percent.",
            "From 30 to 50 adds only about one percent."], s_percent),
 ('3  ·  QUICK QUESTION', ["Quick question. Is that one extra percent worth anything?",
            "Three, two, one.",
            "Yes. Count what gets through instead.",
            "SPF 30 lets about 3 percent through. SPF 50 lets about 2.",
            "That is about a third less reaching your skin."], s_quiz),
 ('4  ·  THE CATCH', ["Now the catch.",
            "Lab tests use a thick layer: 2 milligrams per square centimeter of skin.",
            "Most people put on far less.",
            "One estimate in the Medical Journal of Australia: most people get a third to a quarter of the labeled protection.",
            "So a thin layer of SPF 50 may work more like SPF 15."], s_catch),
 ('5  ·  HOW MUCH', ["So how much is enough?",
            "Cancer Council Australia says an adult needs about 35 milliliters for the whole body. Around 7 teaspoons.",
            "At least a teaspoon each for face and neck, each arm, each leg, front, and back.",
            "Put it on 20 minutes before you go out.",
            "Reapply every 2 hours, and after swimming, sweating or towel drying."], s_amount),
 ('6  ·  THE OTHER RAYS', ["SPF only tells half the story.",
            "Sunlight also carries U-V-A, up to 95 percent of the UV reaching the ground.",
            "U-V-A goes deeper into skin, is linked to wrinkles, and passes through windows.",
            "Both U-V-A and UVB raise the risk of skin cancer.",
            "So look for broad spectrum. That means protection from both."], s_uva),
 ("7  ·  YOU CAN'T FEEL IT", ["One last trap. You cannot see or feel UV.",
            "The warmth you feel is heat, not UV. A cool day can have high UV.",
            "So check the UV index in a weather app. At 3 or above, protect your skin.",
            "Cancer Council recommends SPF 50 or 50 plus, broad spectrum, water resistant.",
            "And use it with a hat, clothing, sunglasses and shade."], s_feel),
 ('RECAP', ["So remember three things.",
            "One. SPF is about sunburn rays. 50 blocks about 98 percent, 30 about 97.",
            "Two. Amount matters most. About 7 teaspoons, reapplied every 2 hours.",
            "Three. Choose broad spectrum, and check the UV index, not the temperature.",
            "If this helped, subscribe for more."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-60 s.
SHORT_SCENES = [
 ('SPF 50 VS 30', ["Is SPF 50 almost twice as strong as SPF 30?", "It is not. The difference is much smaller than you think."], s_hook),
 ('THE PERCENTAGES', ["Look at the percentages.", "SPF 15 blocks about 93 percent of UVB.", "SPF 30 blocks about 97 percent.",
                      "SPF 50 blocks about 98 percent.", "From 30 to 50 adds only about one percent."], s_percent),
 ('THE CATCH', ["But here is the bigger catch.", "Lab tests use a thick layer.", "Most people put on far less.",
                "One estimate: most people get a third to a quarter of the labelled protection.",
                "So a thin layer of SPF 50 may work more like SPF 15."], s_catch),
 ('THE ANSWER', ["So the amount matters more than the number.", "For an adult's whole body, about 7 teaspoons. Reapply every 2 hours.", "Follow for more."],
               card('Amount beats the number', 'About 7 teaspoons')),
]
SHORT_HITS = [(3, 0, 0.0)]
