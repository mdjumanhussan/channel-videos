"""Episode: The Radioactive Speck Inside Many Smoke Alarms (ionisation chamber, why it is safe, photoelectric alarms, which fire each catches first)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Smoke Alarms'                                 # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Why is my smoke alarm radioactive?'            # headline on the vertical Short
HITS = [(0, 1, 0.0), (3, 2, 0.0), (5, 0, 0.0)]               # 'on purpose', the current drops, safe answer
THUMB = ['RADIOACTIVE.', 'ON PURPOSE.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.3, (0, 2): 0.3, (2, 2): 0.3, (3, 2): 0.4, (4, 0): 3.2, (5, 0): 0.3, (7, 2): 0.3}
SHORT_PAUSES = {(0, 1): 0.2, (3, 0): 0.3}
CAPTION_FIXES = {'americium two-forty-one': 'americium-241', 'four hundred and thirty-two': '432',
                 'thirty minutes': '30 minutes', 'New South Wales': 'NSW'}

# Colour code kept in every scene (lesson of 2026-11-01):
# americium and its alpha particles are yellow, ions are cyan, the current is green, smoke is grey,
# the photoelectric light beam is orange, the alarm going off is pink.
ALPHA = YE; ION = CY; CUR = GR; SMOKE = (150, 152, 165); BEAM = (255, 160, 60); ALARM = PK
DARK = (20, 22, 38); WHITE = (226, 230, 240); QUIZ = (60, 36, 24); PLATE = (170, 176, 200); BOX = (34, 40, 76)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

# Headlines of 2 to 5 words with one key word in colour (kept from 2026-11-13: most mobile viewers watch muted).
def headline(c, parts, a, size=88, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def trefoil(c, x, y, r, col, a, bg=BG):
    """The generic radiation warning sign: three blades around a dot."""
    if a <= .01: return
    for k in range(3):
        a0 = -90 + 120 * k - 30
        pts = [(x + r * .28 * math.cos(math.radians(a0 + s)), y + r * .28 * math.sin(math.radians(a0 + s))) for s in range(0, 61, 6)]
        pts += [(x + r * math.cos(math.radians(a0 + s)), y + r * math.sin(math.radians(a0 + s))) for s in range(60, -1, -6)]
        poly(c, pts, col, a, bg)
    c.circ(x, y, r * .18, col, a, bg=bg)

def alarm(c, x, y, r, a, speck=0.0, led=0.0, ring=0.0, t=0.0, bg=BG, beam=0.0):
    """A round ceiling smoke alarm seen from below; speck shows the americium inside, beam the light kind."""
    if a <= .01: return
    c.circ(x, y, r, WHITE, a, bg=bg)
    c.circ(x, y, r * .78, None, a, outline=(190, 196, 212), ow=4, bg=WHITE)
    for k in range(12):
        ang = 6.283 * k / 12
        c.line([(x + r * .82 * math.cos(ang), y + r * .82 * math.sin(ang)), (x + r * .94 * math.cos(ang), y + r * .94 * math.sin(ang))], (170, 176, 196), 4, a, bg=WHITE)
    c.circ(x + r * .5, y - r * .5, r * .06, ALARM if led > .5 and int(t * 4) % 2 == 0 else (120, 200, 140), a, bg=WHITE)
    if speck > .01:
        c.circ(x, y, r * .3, (70, 74, 96), a * speck, bg=WHITE)
        c.circ(x, y, r * .1, ALPHA, a * speck, bg=(70, 74, 96))
        c.circ(x, y, r * .1 + 8 + 4 * math.sin(t * 4), None, a * speck * .7, outline=ALPHA, ow=3, bg=(70, 74, 96))
    if beam > .01:
        c.rr(x - r * .4, y - r * .12, x + r * .4, y + r * .12, 10, (40, 40, 52), a * beam, bg=WHITE)
        c.line([(x - r * .34, y), (x + r * .34, y)], BEAM, 6, a * beam, bg=(40, 40, 52))
    if ring > .01:
        for k in range(3):
            rr_ = r + 30 + 40 * k + 20 * ((t * 2) % 1)
            c.circ(x, y, rr_, None, a * ring * (1 - k * .28), outline=ALARM, ow=6)

def ceiling(c, a, y=250):
    if a <= .01: return
    c.rr(120, y - 30, 1800, y, 6, (44, 50, 90), a)

def chamber(c, a, bg=BG):
    """The ionisation chamber: two charged plates with air between them, the speck on the left."""
    if a <= .01: return
    c.rr(480, 300, 1300, 780, 26, BOX, a, outline=(60, 70, 120), ow=4, bg=bg)
    c.rr(540, 330, 1240, 356, 8, PLATE, a, bg=BOX); c.text(1270, 343, '+', 46, PLATE, a, w='Bold', bg=BOX)
    c.rr(540, 724, 1240, 750, 8, PLATE, a, bg=BOX); c.text(1270, 737, '−', 46, PLATE, a, w='Bold', bg=BOX)
    c.rr(510, 510, 560, 570, 8, (90, 94, 120), a, bg=BOX); c.circ(548, 540, 12, ALPHA, a, bg=(90, 94, 120))

def battery(c, x, y, a):
    if a <= .01: return
    c.rr(x - 50, y - 90, x + 50, y + 90, 12, (60, 66, 110), a, outline=PLATE, ow=3)
    c.rr(x - 20, y - 106, x + 20, y - 90, 4, PLATE, a)
    c.text(x, y - 40, '+', 44, INK, a, w='Bold', bg=(60, 66, 110)); c.text(x, y + 40, '−', 44, INK, a, w='Bold', bg=(60, 66, 110))

def wires(c, a):
    if a <= .01: return
    c.line([(1240, 343), (1440, 343), (1440, 450)], PLATE, 4, a)
    c.line([(1240, 737), (1440, 737), (1440, 630)], PLATE, 4, a)

def alphas(c, t, a, n=10, reach=380, bg=BOX):
    """Alpha particles shooting out of the speck as short yellow dashes."""
    if a <= .01: return
    for k in range(n):
        ang = -0.55 + 1.1 * k / (n - 1)
        p = (t * .9 + k * .37) % 1
        d0 = 30 + p * reach; d1 = d0 + 34
        c.line([(548 + d0 * math.cos(ang), 540 + d0 * math.sin(ang)), (548 + d1 * math.cos(ang), 540 + d1 * math.sin(ang))], ALPHA, 5, a * (1 - p * .6), bg=bg)

ION_PTS = [(random.Random(k).uniform(620, 1200), random.Random(k + 99).uniform(400, 690)) for k in range(26)]
def ions(c, t, a, charged=1.0, flow=0.0, blocked=0.0, bg=BOX):
    """Air molecules (dim) that become ions (cyan, with a +); with flow they drift towards the plates."""
    if a <= .01: return
    for k, (x, y) in enumerate(ION_PTS):
        if k % 2 == 0: tgt = 724
        else: tgt = 356
        p = (t * .35 + k * .13) % 1 if flow > .01 else 0
        stop = blocked > .01 and k % 3 != 0
        yy = y + (tgt - y) * p * flow * (1 - (blocked if stop else 0))
        col = ION if charged > .5 else (90, 100, 140)
        cc = tuple(int(col[j] * (1 - .5 * blocked * stop)) for j in range(3)) if stop else col
        c.circ(x, yy, 11, cc, a, bg=bg)
        if charged > .5: c.text(x, yy - 1, '+' if k % 2 else '−', 18, DARK, a, w='Bold', bg=cc)

SMOKE_PTS = [(random.Random(k + 7).uniform(0, 1), random.Random(k + 70).uniform(380, 700), random.Random(k + 700).uniform(16, 34)) for k in range(16)]
def smoke(c, t, a, x0=480, x1=1300, bg=BOX):
    if a <= .01: return
    for k, (u, y, r) in enumerate(SMOKE_PTS):
        x = x0 + 40 + ((u + t * .05) % 1) * (x1 - x0 - 80)
        c.circ(x, y + 10 * math.sin(t + k), r, SMOKE, a * .85, bg=bg)

def meter(c, x, level, a, thresh=None, lab='current'):
    """A vertical gauge of the current, with an optional alarm line."""
    if a <= .01: return
    c.rr(x - 50, 340, x + 50, 740, 18, CARD, a, outline=(60, 70, 120), ow=3)
    h = 380 * clamp(level)
    col = CUR if (thresh is None or level > thresh) else ALARM
    c.rr(x - 36, 730 - h, x + 36, 730, 12, col, a, bg=CARD)
    if thresh is not None:
        yt = 730 - 380 * thresh
        c.line([(x - 70, yt), (x + 70, yt)], ALARM, 4, a); c.text(x + 80, yt, 'alarm', 28, ALARM, a, anchor='lm', w='Bold')
    c.text(x, 790, lab, 32, CUR, a, w='Bold')

def tag(c, x, y, txt, col, a, sub=None, bg=BG, w=300):
    if a <= .01: return
    c.rr(x - w / 2, y - 50, x + w / 2, y + 50, 22, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - (12 if sub else 0), txt, 44, col, a, w='Bold', bg=CARD)
    if sub: c.text(x, y + 28, sub, 26, DIM, a, w='Bold', bg=CARD)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: a surprising true statement about the viewer's own ceiling, shown not asked."""
    hl = lambda i: hl_(T, i)
    headline(c, [('On ', INK), ('your', CY), (' ceiling', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Radioactive. ', ALPHA), ('On purpose.', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('A speck', ALPHA), (' or ', INK), ('a light', BEAM)], sw_in(T, 2))
    m2 = hl(2)
    ceiling(c, 1)
    xs = 960 - 420 * m2
    c.line([(xs, 250), (xs, 300)], (44, 50, 90), 10, 1)
    alarm(c, xs, 480, 180, 1, speck=fd(T(0), 1.2, .6), t=t)
    m1 = hl(1) * (1 - m2)
    trefoil(c, 1360, 480, 110, ALPHA, m1)
    tag(c, 1360, 680, 'americium', ALPHA, m1, w=320)
    c.line([(xs + 60, 480), (1240, 480)], ALPHA, 4, m1)
    c.line([(1380, 250), (1380, 300)], (44, 50, 90), 10, m2)
    alarm(c, 1380, 480, 180, m2, beam=1, t=t)
    c.text(540, 720, 'ionisation', 40, ALPHA, m2, w='Bold'); c.text(1380, 720, 'photoelectric', 40, BEAM, m2, w='Bold')
    c.text(960, 480, 'or', 56, DIM, m2, w='Bold')

def s_speck(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Eraser', ALPHA), ('-sized cup', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Paper', INK), (' stops them', ALPHA)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('432 years', ALPHA), (' to halve', INK)], sw_in(T, 2))
    m0 = hl(0) * (1 - hl(1))
    # pencil with eraser beside the little metal cup
    c.rr(380, 500, 1060, 560, 10, (240, 190, 70), m0); poly(c, [(1060, 500), (1140, 530), (1060, 560)], (230, 200, 160), m0)
    c.rr(300, 500, 380, 560, 8, (250, 150, 160), m0)
    c.rr(1300, 470, 1420, 590, 18, (150, 156, 180), m0); c.circ(1360, 530, 22, ALPHA, m0, bg=(150, 156, 180))
    c.text(340, 620, 'eraser', 34, DIM, m0, w='Bold'); c.text(1360, 650, 'metal cup', 34, ALPHA, m0, w='Bold')
    c.text(960, 820, 'One microcurie or less of americium-241 (US NRC)', 30, DIM, m0, w='Regular')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        c.rr(420, 490, 520, 590, 14, (150, 156, 180), m1); c.circ(470, 540, 18, ALPHA, m1, bg=(150, 156, 180))
        for k in range(7):
            ang = -0.6 + 1.2 * k / 6; p = (t * 1.1 + k * .23) % 1
            d0 = 60 + p * 560; d1 = d0 + 40
            c.line([(470 + d0 * math.cos(ang), 540 + d0 * math.sin(ang)), (470 + d1 * math.cos(ang), 540 + d1 * math.sin(ang))], ALPHA, 6, m1 * (1 - p * .3))
        c.rr(1110, 300, 1140, 780, 4, (245, 245, 235), m1)
        c.text(1125, 820, 'a sheet of paper', 34, INK, m1, w='Bold')
        c.text(800, 300, 'alpha particles', 36, ALPHA, m1, w='Bold')
        c.text(1480, 540, 'nothing gets through', 34, DIM, m1, anchor='lm', w='Bold')
    m2 = hl(2)
    if m2 > .01:
        c.rr(360, 470, 1560, 590, 30, CARD, m2)
        f = 1 - .5 * fd(T(2), .4, 1.4)
        c.rr(372, 482, 372 + 1176 * f, 578, 24, ALPHA, m2, bg=CARD)
        c.text(960, 650, 'after 432 years, half is still there', 38, INK, m2, w='Bold')
        c.text(372, 430, 'now', 32, DIM, m2, anchor='lm', w='Bold'); c.text(1548, 430, '432 years later', 32, DIM, m2, anchor='rm', w='Bold')

def s_chamber(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Two ', INK), ('charged', CUR), (' plates', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Air turns into ', INK), ('ions', ION)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('A tiny ', INK), ('current', CUR)], sw_in(T, 2))
    chamber(c, 1); battery(c, 1440, 540, 1); wires(c, 1)
    m1 = hl(1); m2 = hl(2)
    alphas(c, t, m1 * (1 - .5 * m2))
    ions(c, t, 1, charged=m1, flow=m2)
    c.text(890, 820, 'air between the plates', 32, DIM, 1 - m1, w='Bold')
    c.text(890, 820, '+ and − bits of air: ions', 32, ION, m1 * (1 - m2), w='Bold')
    meter(c, 1690, .8 * fd(T(2), .3, .8), m2)
    c.text(890, 820, 'ions drift to the plates: a steady trickle', 32, CUR, m2, w='Bold')

def s_smoke(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Smoke', SMOKE), (' drifts in', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Smoke', SMOKE), (' blocks ions', ION)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Current ', CUR), ('drops', ALARM)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('It watches the ', INK), ('current', CUR)], sw_in(T, 3))
    chamber(c, 1); battery(c, 1440, 540, 1); wires(c, 1)
    s0 = fd(T(0), .2, 1.2)
    b = hl(1)
    ions(c, t, 1, charged=1, flow=1, blocked=b)
    smoke(c, t, s0)
    lvl = .8 - .25 * fd(T(1), .3, 1.5) - .35 * fd(T(2), 0, .8)
    meter(c, 1690, lvl, 1, thresh=.32)
    al = hl(2)
    if al > .01:
        for k in range(3):
            rr_ = 60 + 40 * k + 20 * ((t * 2) % 1)
            c.circ(1690, 260, rr_, None, al * (1 - k * .28), outline=ALARM, ow=6)
        c.text(1690, 260, 'BEEP', 34, ALARM, al, w='Bold')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a warm pattern-interrupt background (lesson of 2026-10-13)."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Dangerous', ALARM), ('?', INK)], 1, bg=QUIZ)
    alarm(c, 640, 540, 200, 1, speck=1, t=t, bg=QUIZ)
    trefoil(c, 1280, 540, 140, ALPHA, 1, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - 5.0; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 4.8)
        c.circ(960, 800, 60, ALPHA, u, bg=QUIZ); c.text(960, 800, str(k) if k else '?', 60, DARK, u, w='Bold', bg=ALPHA)

def s_safe(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Normal use: ', INK), ('safe', CUR)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Less than ', INK), ('background', CUR)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Never ', ALARM), ('open it', INK)], sw_in(T, 2))
    m0 = hl(0) * (1 - hl(1))
    if m0 > .01:
        c.rr(560, 330, 1360, 750, 60, WHITE, m0); c.rr(590, 360, 1330, 720, 46, (60, 66, 96), m0, bg=WHITE)
        c.rr(900, 500, 1000, 580, 10, (150, 156, 180), m0, bg=(60, 66, 96)); c.circ(950, 540, 16, ALPHA, m0, bg=(150, 156, 180))
        for k in range(8):
            ang = 6.283 * k / 8 + .3; p = (t * 1.2 + k * .19) % 1
            d0 = 60 + p * 150
            c.line([(950 + d0 * math.cos(ang), 540 + d0 * math.sin(ang) * .8), (950 + (d0 + 26) * math.cos(ang), 540 + (d0 + 26) * math.sin(ang) * .8)], ALPHA, 5, m0, bg=(60, 66, 96))
        c.text(960, 800, 'the plastic case stops the alpha particles', 34, INK, m0, w='Bold')
        c.circ(1500, 400, 50, CUR, m0); c.check(1500, 400, 44, DARK, m0, fd(T(0), .5, .5))
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        c.rr(300, 300, 1620, 760, 26, CARD, m1 * .9)
        for k, (lab, h, col) in enumerate((('natural background', 290, DIM), ('a smoke alarm', 40, CUR))):
            x = 700 + k * 520; hh = h * fd(T(1), .2 + .2 * k, .6)
            c.rr(x - 110, 690 - hh, x + 110, 690, 14, col, m1, bg=CARD)
            c.text(x, 725, lab, 34, col, m1, w='Bold', bg=CARD)
        c.text(960, 330, 'yearly radiation dose', 34, INK, m1, w='Bold', bg=CARD)
        c.text(1620, 800, 'Illustrative heights. Source: EPA NSW', 28, DIM, m1, anchor='rm', w='Regular')
    m2 = hl(2)
    if m2 > .01:
        c.rr(640, 420, 860, 640, 20, (150, 156, 180), m2)
        c.line([(700, 420), (760, 520), (720, 580), (780, 640)], DARK, 6, m2, bg=(150, 156, 180))
        for k in range(14):
            rnd = random.Random(k); x = 900 + rnd.random() * 260; y = 380 + rnd.random() * 300
            c.circ(x + 12 * math.sin(t + k), y, 6, ALPHA, m2 * .9)
        c.cross(1320, 530, 70, ALARM, m2)
        c.text(960, 760, 'only the dust is the danger: breathed in or swallowed', 34, INK, m2, w='Bold')

def s_light(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Or use ', INK), ('light', BEAM)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('The ', INK), ('beam', BEAM), (' misses', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Smoke', SMOKE), (' bounces it', BEAM)], sw_in(T, 2))
    c.rr(380, 320, 1540, 560, 24, (24, 26, 40), 1, outline=(60, 70, 120), ow=4)       # top of the T
    c.rr(860, 560, 1060, 800, 0, (24, 26, 40), 1)                                      # stem of the T
    c.line([(860, 560), (860, 800), (1060, 800), (1060, 560)], (60, 70, 120), 4, 1)
    c.rr(400, 410, 470, 470, 10, BEAM, 1, bg=(24, 26, 40)); c.text(435, 380, 'light', 30, BEAM, 1, w='Bold', bg=(24, 26, 40))
    c.rr(910, 740, 1010, 790, 10, (80, 84, 110), 1, bg=(24, 26, 40))
    m1 = hl(1); m2 = hl(2)
    lit = fd(T(2), 1.0, .6)
    c.rr(910, 740, 1010, 790, 10, CUR, lit, bg=(24, 26, 40)); c.text(960, 840, 'light sensor', 32, CUR if lit > .5 else DIM, 1, w='Bold')
    bw = fd(T(0), .5, .8)
    c.line([(470, 440), (470 + 1040 * bw, 440)], BEAM, 10, 1, bg=(24, 26, 40))
    c.text(1300, 500, 'straight past the sensor', 30, DIM, m1 * (1 - m2), w='Bold', bg=(24, 26, 40))
    if m2 > .01:
        for k, x in enumerate((760, 900, 1010, 1150, 1290)):
            c.circ(x + 8 * math.sin(t * 2 + k), 440 + 14 * math.cos(t + k), 24, SMOKE, m2 * .9, bg=(24, 26, 40))
        for k, x in enumerate((900, 1010)):
            p = fd(T(2), .4 + .2 * k, .6)
            c.line([(x, 440), (x + (960 - x) * p, 440 + (740 - 440) * p)], BEAM, 5, m2, bg=(24, 26, 40))
        alarm(c, 1700, 560, 70, lit, led=1, ring=lit, t=t)
        c.text(960, 270, 'like dust glowing in a sunbeam', 34, BEAM, m2, w='Bold')

def bars(c, x, title, vals, a, unit, t0, T, win):
    """Two bars: time to the first alarm (shorter is faster), the faster one in green."""
    if a <= .01: return
    c.rr(x - 380, 290, x + 380, 830, 26, CARD, a * .9)
    c.text(x, 330, title, 38, INK, a, w='Bold', bg=CARD)
    mx = max(v for _, v, _ in vals)
    for k, (lab, v, col) in enumerate(vals):
        y = 450 + k * 170; w = 600 * v / mx * fd(T, t0 + .3 * k, .6)
        c.rr(x - 330, y, x - 330 + max(8, w), y + 70, 12, CUR if k == win else col, a, bg=CARD)
        c.text(x - 330, y - 26, lab, 30, col, a, anchor='lm', w='Bold', bg=CARD)
        c.text(x - 330 + max(8, w) + 14, y + 35, unit(v), 32, INK, a * fd(T, t0 + .3 * k + .4), anchor='lm', w='Bold', bg=CARD)

def s_race(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Which ', INK), ('fire', ALARM), ('?', INK)], sw_out(T, 1) * sw_out(T, 3))
    headline(c, [('Flaming', ALARM), (': ionisation', ALPHA)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Smouldering', SMOKE), (': photo', BEAM)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Toast', BEAM), (' sets it off', INK)], sw_in(T, 3) * sw_out(T, 4))
    headline(c, [('NSW', CY), (' picks ', INK), ('photo', BEAM)], sw_in(T, 4))
    m0 = 1 - hl(1)
    alarm(c, 620, 520, 170, m0, speck=1, t=t); alarm(c, 1300, 520, 170, m0, beam=1, t=t)
    c.text(620, 760, 'ionisation', 42, ALPHA, m0, w='Bold'); c.text(1300, 760, 'photoelectric', 42, BEAM, m0, w='Bold')
    v = (('ionisation', 47, ALPHA), ('photoelectric', 94, BEAM))
    m12 = hl(1) * (1 - hl(3))
    bars(c, 520, 'Flaming fire', v, m12, lambda s: f'{s} s', 0, T(1), 0)
    v2 = (('ionisation', 4010, ALPHA), ('photoelectric', 2219, BEAM))
    bars(c, 1400, 'Smouldering fire', v2, m12 * hl(2), lambda s: f'{round(s / 60)} min', 0, T(2), 1)
    c.text(960, 860, 'Average time to first alarm, NIST home tests', 28, DIM, m12, w='Regular')
    m3 = hl(3) * (1 - hl(4))
    if m3 > .01:
        c.rr(560, 560, 900, 780, 30, (200, 200, 214), m3)          # toaster
        c.rr(620, 520, 720, 580, 10, (60, 40, 30), m3); c.rr(740, 520, 840, 580, 10, (60, 40, 30), m3)
        for k in range(5):
            c.circ(700 + 30 * k + 14 * math.sin(t * 2 + k), 460 - 30 * ((t * .6 + k * .2) % 1) * 4, 22, SMOKE, m3 * .7)
        alarm(c, 1320, 470, 150, m3, speck=1, ring=1, led=1, t=t)
        c.text(1320, 830, 'more cooking false alarms', 36, ALPHA, m3, w='Bold')
    m4 = hl(4)
    alarm(c, 960, 500, 200, m4, beam=1, t=t)
    c.text(960, 780, 'Fire and Rescue NSW recommends photoelectric alarms', 36, INK, m4, w='Bold')

def s_recap(c, T, t):
    """Recap as three stacked rows with an icon each."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', ALPHA)], 1)
    items = ((1, 'A sealed speck of americium. Safe in normal use.', ALPHA),
             (2, 'It makes a tiny current. Smoke makes it drop.', CUR),
             (3, 'Light-based alarms catch smouldering fires sooner.', BEAM))
    for ln, txt, col in items:
        m = hl(ln); y = 300 + (ln - 1) * 180; dx = 60 * (1 - m)
        c.rr(260 + dx, y, 1660 + dx, y + 150, 24, CARD, m, outline=col, ow=4)
        c.circ(350 + dx, y + 75, 46, col, m, bg=CARD); c.text(350 + dx, y + 75, str(ln), 50, DARK, m, w='Bold', bg=col)
        c.text(440 + dx, y + 75, txt, 40, INK, m, anchor='lm', w='Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    c.rr(1150, 120, 1850, 160, 6, (44, 50, 90), 1)
    c.line([(1500, 160), (1500, 220)], (44, 50, 90), 12, 1)
    alarm(c, 1500, 470, 260, 1, speck=1, t=0)
    trefoil(c, 1500, 470, 70, ALPHA, 1, bg=(70, 74, 96))

SCENES = [
 ('THE SPECK', ["The smoke alarm on your ceiling might hold a speck of radioactive metal.",
                "It's called americium. And it's there on purpose.",
                "Here's how that speck smells smoke, and why some alarms use light instead."], s_hook),
 ('HOW MUCH', ["The speck is tiny. It sits in a little metal cup, about the size of a pencil eraser.",
               "It gives off tiny particles, called alpha particles. They only travel a few inches through air. A sheet of paper stops them.",
               "And it lasts. After four hundred and thirty-two years, half of it is still there."], s_speck),
 ('THE CHAMBER', ["Inside the alarm is a small chamber of air, between two metal plates. The battery charges the plates.",
                  "The alpha particles knock tiny bits off the air molecules. That turns the air into charged bits, called ions.",
                  "The plates pull the ions across. So a tiny, steady current flows through the air. Like a slow trickle of water in a pipe."], s_chamber),
 ('THE SMOKE', ["Now, smoke drifts in.",
                "The smoke gets in the way of the ions, like traffic jamming a road. Fewer of them reach the plates.",
                "So the current drops. When it falls below a set level, the alarm sounds.",
                "The alarm doesn't sniff the smoke. It watches the current."], s_smoke),
 ('QUICK QUESTION', ["Quick question. A speck of radioactive metal, on your ceiling. Is that dangerous?"], s_quiz),
 ('THE ANSWER', ["In normal use, no. The alpha particles can't even get through the alarm's plastic case.",
                 "The New South Wales Environment Protection Authority says the dose can be less than natural background radiation.",
                 "The danger is only if the source is broken open, and its dust is breathed in or swallowed. So never take one apart."], s_safe),
 ('THE OTHER KIND', ["Many alarms skip the americium, and use light instead. These are photoelectric alarms.",
                     "A small light shines across a dark chamber. The light sensor sits off to the side, where the beam never reaches it.",
                     "When smoke drifts in, it scatters the light, like dust glowing in a sunbeam. Some light bounces onto the sensor, and the alarm sounds."], s_light),
 ('WHICH IS FASTER', ["The two kinds notice different fires first.",
                      "In home fire tests by the US National Institute of Standards and Technology, ionisation alarms went off sooner for fast, flaming fires.",
                      "But photoelectric alarms caught slow, smouldering fires, on average about thirty minutes earlier.",
                      "Ionisation alarms are also more likely to go off from cooking, like a slice of burnt toast.",
                      "Fire and Rescue New South Wales recommends photoelectric alarms for homes."], s_race),
 ('RECAP', ["Three things to keep.",
            "One: many smoke alarms hold a sealed speck of americium. In normal use, it's safe.",
            "Two: it makes a tiny current in the air, and smoke makes that current drop.",
            "Three: photoelectric alarms use light instead, and catch smouldering fires sooner.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('Radioactive. ', ALPHA), ('On purpose.', INK)], 1, size=96)
    ceiling(c, 1)
    c.line([(760, 250), (760, 300)], (44, 50, 90), 10, 1)
    alarm(c, 760, 500, 190, 1, speck=1, t=t)
    trefoil(c, 1300, 500, 110, ALPHA, 1)
    tag(c, 1300, 700, 'americium', ALPHA, 1, w=320)

SHORT_SCENES = [
 ('THE SPECK', ["Many smoke alarms hold a speck of radioactive metal. On purpose.",
                "It's called americium, and it's how the alarm smells smoke."], short_hook),
 ('THE CHAMBER', ["Inside is a small chamber of air, between two charged metal plates.",
                  "The americium fires out tiny alpha particles. They turn the air into charged bits, called ions.",
                  "The plates pull the ions across, so a tiny, steady current flows."], s_chamber),
 ('THE SMOKE', ["Then smoke drifts in.",
                "It gets in the way of the ions, like traffic on a road.",
                "So the current drops, and the alarm sounds."], s_smoke),
 ('THE ANSWER', ["So the alarm doesn't sniff smoke. It watches a current.",
                 "And the speck is safe in normal use. Its particles can't get through the plastic case."], card('It watches a current.', 'Safe in its case.')),
]
SHORT_HITS = [(3, 0, 0.0)]
