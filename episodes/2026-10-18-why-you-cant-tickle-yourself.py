"""Episode: Why You Can't Tickle Yourself."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why You Can't Tickle Yourself"   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
SHORT_HOOK = "Why can't you tickle yourself?"     # headline on the vertical Short
HITS = [(0, 2, 0.0), (3, 1, 0.0), (5, 3, 0.0)]    # title card, the feeling is turned down, the delay brings the tickle back
THUMB = ['YOUR BRAIN', 'BLOCKS', 'THE TICKLE']
MUSIC_LEVEL = 0.006                               # music about 20 dB under the voice (lesson of 2026-10-14)
CAPTION_FIXES = {
    'nineteen ninety-eight': '1998', 'nineteen ninety-nine': '1999', 'two thousand and three': '2003',
    'forty percent': '40%', 'Sixteen people': '16 people',
}
# Applied lesson (learnings.md, 2026-10-18): open on the most visually interesting moment, not a build-up.
# Frame one already shows the robot copying a hand's movement onto a palm, and the surprising true fact
# (a fifth of a second of delay brings the tickle back) is said and shown inside the first ~5 seconds.

SKIN = (236, 192, 160); SKIN2 = (196, 150, 120); OTHER = (150, 110, 90)
METAL = (120, 130, 175); FOAM = (255, 225, 120)
SELF = CY; WORLD = PK; PRED = PU

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def palm(c, x, y, s, a=1.0, bg=BG, col=SKIN):
    """Open hand, palm facing us, fingers up; (x, y) is the palm centre, s its half-width."""
    if a <= 0.01: return
    for j, (dx, ln) in enumerate(((-.72, 1.05), (-.25, 1.25), (.22, 1.2), (.66, .95))):
        fx = x + dx * s
        c.rr(fx - s * .2, y - s * (.55 + ln), fx + s * .2, y - s * .3, s * .2, col, a, bg=bg)
    pts = [(x - s * .95, y + s * .1), (x - s * 1.45, y - s * .45)]
    c.line(pts, col, s * .38, a, bg); c.circ(pts[1][0], pts[1][1], s * .19, col, a, bg=bg)
    c.rr(x - s, y - s * .75, x + s, y + s * .9, s * .45, col, a, bg=bg)
    c.rr(x - s * .55, y + s * .75, x + s * .55, y + s * 1.5, s * .2, col, a, bg=bg)
    c.line([(x - s * .6, y - s * .1), (x + s * .3, y - s * .35)], SKIN2, max(2, s * .05), a * .7, col)
    c.line([(x - s * .5, y + s * .3), (x + s * .5, y + s * .05)], SKIN2, max(2, s * .05), a * .7, col)

def finger(c, x, y, s, ang, col=SKIN, a=1.0, bg=BG):
    """Pointing finger whose tip is at (x, y), coming in from direction ang (radians)."""
    if a <= 0.01: return
    bx, by = x + math.cos(ang) * s * 2.2, y + math.sin(ang) * s * 2.2
    c.line([(x, y), (bx, by)], col, s * .55, a, bg)
    c.circ(x, y, s * .28, col, a, bg=bg)
    c.circ(bx, by, s * .5, col, a, bg=bg)

def wiggles(c, x, y, r, t, col=YE, a=1.0, n=6, bg=BG):
    """Little 'tickle' marks bursting around a point."""
    if a <= 0.01: return
    for i in range(n):
        ang = i * 2 * math.pi / n + t * .8
        r0 = r * (1 + .12 * math.sin(t * 9 + i))
        p0 = (x + math.cos(ang) * r0, y + math.sin(ang) * r0)
        p1 = (x + math.cos(ang) * (r0 + r * .45), y + math.sin(ang) * (r0 + r * .45))
        c.line([p0, p1], col, max(3, r * .08), a, bg)

def meter(c, x, y, h, v, col, a=1.0, bg=BG, lab=None):
    """Vertical bar meter, bottom at y, height h, fill v in 0..1."""
    if a <= 0.01: return
    c.rr(x - 26, y - h, x + 26, y, 14, (40, 46, 84), a, bg=bg)
    if v > 0.02: c.rr(x - 26, y - h * clamp(v), x + 26, y, 14, col, a, bg=(40, 46, 84))
    if lab: c.text(x, y + 36, lab, 26, DIM, a, w='Medium', bg=bg)

def brain(c, x, y, s, a=1.0, bg=BG, cereb=0.0, touch=None, col=(214, 150, 190)):
    """Side view of a brain, facing left. cereb highlights the cerebellum; touch=(colour, alpha) lights the touch area."""
    if a <= 0.01: return
    c.circ(x + s * .62, y + s * .55, s * .32, mix(GR, cereb, col) if cereb > 0 else (190, 130, 170), a, bg=bg)
    c.rr(x + s * .15, y + s * .5, x + s * .38, y + s * 1.05, s * .1, (190, 130, 170), a, bg=bg)
    c.circ(x, y, s * .85, col, a, bg=bg)
    c.circ(x + s * .25, y + s * .12, s * .75, col, a, bg=bg)
    if touch:
        tc, ta = touch
        c.circ(x + s * .15, y - s * .55, s * .26, tc, a * ta, bg=col)
    for k in range(5):
        ang0 = -2.6 + k * .55
        pts = [(x + s * .1 + s * (.35 + .25 * (j % 2)) * math.cos(ang0 + j * .14), y + s * (.35 + .25 * (j % 2)) * math.sin(ang0 + j * .14)) for j in range(5)]
        c.line(pts, (170, 100, 150), max(2, s * .04), a, col)

def robot(c, x, y, s, t, a=1.0, bg=BG, sway=1.0):
    """Robot arm from a base on the left (x, y) reaching right; foam tip sways sideways. Returns tip position."""
    if a <= 0.01: return (x, y)
    c.rr(x - s * .35, y - s * .15, x + s * .35, y + s * .15, s * .08, METAL, a, bg=bg)
    j1 = (x, y - s * .9)
    tipx = x + s * 1.3 + s * .22 * math.sin(t * 2 * math.pi * .9) * sway
    tip = (tipx, y + s * .1)
    j2 = (x + s * .85, y - s * 1.05)
    c.line([(x, y - s * .1), j1, j2, (tipx, tip[1] - s * .45)], METAL, s * .16, a, bg)
    for p in (j1, j2): c.circ(p[0], p[1], s * .13, (80, 90, 140), a, bg=bg)
    c.rr(tipx - s * .14, tip[1] - s * .5, tipx + s * .14, tip[1], s * .1, FOAM, a, bg=bg)
    return tip

def handle_hand(c, x, y, s, t, a=1.0, bg=BG, col=SKIN):
    """A fist holding a small handle that moves side to side (the participant's moving hand)."""
    if a <= 0.01: return
    dx = s * .22 * math.sin(t * 2 * math.pi * .9)
    c.line([(x - s * 1.2, y), (x + s * 1.2, y)], (60, 66, 110), s * .12, a, bg)
    hx = x + dx
    c.rr(hx - s * .1, y - s * 1.35, hx + s * .1, y, s * .06, METAL, a, bg=bg)          # the handle
    c.rr(hx - s * .26, y + s * .05, hx + s * .26, y + s * .95, s * .16, col, a, bg=bg)    # wrist
    c.rr(hx - s * .42, y - s * .95, hx + s * .42, y + s * .2, s * .2, col, a, bg=bg)      # fist
    for j in range(4):                                                                    # curled fingers
        c.rr(hx - s * .02, y - s * .9 + j * s * .27, hx + s * .5, y - s * .66 + j * s * .27, s * .12, col, a, bg=bg)
        c.line([(hx + s * .05, y - s * .66 + j * s * .27), (hx + s * .45, y - s * .66 + j * s * .27)], SKIN2, max(2, s * .03), a, col)
    c.rr(hx - s * .5, y - s * .75, hx - s * .2, y - s * .2, s * .14, col, a, bg=bg)      # thumb

def eye(c, x, y, s, look=0.0, a=1.0, bg=BG):
    if a <= 0.01: return
    top = [(x - s + 2 * s * u / 20, y - s * .55 * math.sin(math.pi * u / 20)) for u in range(21)]
    bot = [(x - s + 2 * s * u / 20, y + s * .55 * math.sin(math.pi * u / 20)) for u in range(21)]
    c.d.polygon([(px * c.k, py * c.k) for px, py in top + bot[::-1]], fill=mix(INK, a, bg))
    ix = x + look * s * .45
    c.circ(ix, y, s * .38, (70, 140, 200), a, bg=INK)
    c.circ(ix, y, s * .18, (10, 12, 24), a, bg=(70, 140, 200))
    c.circ(ix + s * .1, y - s * .1, s * .06, INK, a, bg=(10, 12, 24))
    c.line(top, (60, 50, 70), max(3, s * .07), a, bg); c.line(bot, (60, 50, 70), max(2, s * .04), a, bg)

def bug(c, x, y, s, t, a=1.0, bg=BG):
    if a <= 0.01: return
    for sg in (-1, 1):
        for j in range(3):
            c.line([(x + (j - 1) * s * .45, y), (x + (j - 1) * s * .6, y + sg * s * (.75 + .1 * math.sin(t * 12 + j)))], (40, 30, 30), max(2, s * .1), a, bg)
    c.circ(x, y, s * .55, (200, 60, 60), a, bg=bg)
    c.circ(x + s * .6, y, s * .3, (40, 30, 30), a, bg=bg)
    c.line([(x - s * .5, y), (x + s * .4, y)], (40, 30, 30), max(2, s * .08), a, (200, 60, 60))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    palm(c, 1520, 640, 150)
    finger(c, 1500, 640, 70, -.5)
    c.circ(1500, 600, 230, None, 1, outline=PK, ow=16)
    c.line([(1340, 440), (1660, 760)], PK, 16, 1)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(2), 0, .5)
    if a > 0:
        # moving from frame one: a hand moves a handle, the robot copies the movement onto a palm
        handle_hand(c, 420, 640, 170, t, a)
        c.text(420, 850, 'your hand moves a handle', 34, DIM, a, w='Medium')
        for j in range(5):
            px = 640 + ((t * 1.2 + j / 5) % 1) * 380
            c.circ(px, 520, 9, CY, a * .9)
        c.arrow(640, 520, 1030, 520, CY, 5, a * .5, 18)
        palm(c, 1420, 640, 110, a)
        tip = robot(c, 1200, 690, 170, t, a)
        late = fd(T(1)) if T(1) > -.1 else 0.0
        c.text(1420, 875, 'a robot copies it onto your palm', 34, DIM, a, w='Medium')
        c.text(960, 170, 'Your own touch can tickle you...', 66, INK, a, w='Bold')
        if late > 0:
            pill(c, 830, 330, '+ 0.2 seconds late', YE, a * late, 46, h=84)
            wiggles(c, 1420, 660, 120, t, YE, a * late)
    if T(2) > 0:
        m = fd(T(2), .2, .7)
        c.text(960, 330 + 30 * (1 - m), "Why You Can't", 132, INK, m, w='Bold')
        c.text(960, 490 + 30 * (1 - m), 'Tickle Yourself', 132, YE, m, w='Bold')
        c.line([(960 - 330 * m, 600), (960 + 330 * m, 600)], CY, 8, m)
        k = fd(T(2), 1.0)
        palm(c, 960, 760, 55, k)
        finger(c, 975, 760, 26, -.6, a=k)

def s_try(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    k0 = hl(0)
    for i, (x, col, who, li) in enumerate(((520, SELF, 'YOU', 0), (1400, WORLD, 'SOMEONE ELSE', 2))):
        k = hl(li)
        if k <= 0: continue
        c.rr(x - 380, 200, x + 380, 770, 30, CARD, k, outline=col, ow=5)
        c.text(x, 245, who, 44, col, k, w='Bold', bg=CARD)
        palm(c, x - 60, 500, 100, k, bg=CARD)
        stroke = 30 * math.sin(t * 5)
        finger(c, x - 60 + stroke, 500, 34, -.45 if i == 0 else -2.6, SKIN if i == 0 else OTHER, k, CARD)
        if i == 0:
            v = .12 + .03 * math.sin(t * 6)
            km = hl(1)
            meter(c, x + 270, 680, 340, v, SELF, km, CARD, 'tickle')
            if km > 0: c.text(x - 60, 720, 'almost nothing', 36, DIM, km, w='Bold', bg=CARD)
        else:
            v = .9 + .05 * math.sin(t * 6)
            meter(c, x + 270, 680, 340, v * k, WORLD, k, CARD, 'tickle')
            wiggles(c, x - 60, 480, 120, t, YE, k, bg=CARD)
            c.text(x - 60, 720, 'you squirm', 36, YE, k, w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        c.rr(960 - 330, 830 - 40, 960 + 330, 830 + 40, 40, BG, k3, outline=YE, ow=4)
        c.text(960, 830, 'Same touch. Same skin.', 42, YE, k3, w='Bold')
        c.text(960, 145, 'So the difference is in your brain', 54, INK, k3, w='Bold')

def s_predict(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0)
    c.text(960, 150, 'Your brain is always predicting', 60, INK, m, w='Bold')
    brain(c, 420, 470, 200, m)
    k1 = hl(1)
    if k1 > 0:
        palm(c, 1520, 560, 95, k1)
        finger(c, 1530, 560, 30, -.5, a=k1)
        c.arrow(640, 430, 1330, 430, CY, 7, k1, 22)
        p = (t * .7) % 1
        c.rr(640 + p * 640, 405, 700 + p * 640, 455, 10, CY, k1)
        c.text(985, 380, 'command: move', 36, CY, k1, w='Bold')
    k2 = hl(2)
    if k2 > 0:
        c.line([(800, 430), (900, 640)], PRED, 6, k2)
        c.rr(700, 640, 1300, 840, 26, CARD, k2, outline=PRED, ow=5)
        c.text(810, 690, 'COPY', 38, PRED, k2, w='Bold', bg=CARD); c.arrow(880, 690, 950, 690, PRED, 5, k2, 14); c.text(1100, 690, 'PREDICTION', 38, PRED, k2, w='Bold', bg=CARD)
        k3 = hl(3)
        if k3 > 0:
            c.text(1000, 760, '"a light touch on my palm"', 34, INK, k3, w='Medium', bg=CARD)
            c.text(1000, 805, 'scientists: an efference copy', 28, DIM, k3, w='Medium', bg=CARD)

def s_cancel(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    a1 = 1 - fd(T(3), -.4, .4)
    if a1 > 0:
        m = hl(0)
        c.text(960, 150, 'Prediction vs. the real feeling', 60, INK, m * a1, w='Bold')
        a2 = 1 - fd(T(2), -.3, .4)      # match + volume, then the inbox
        if a2 > 0:
            slide = fd(T(0), .3, 1.2)
            for j, (lab, col, y0) in enumerate((('PREDICTED', PRED, 330), ('FELT', SELF, 600))):
                yy = y0 + (465 - y0) * slide * .45
                c.rr(260, yy - 75, 860, yy + 75, 26, CARD, m * a1 * a2, outline=col, ow=5)
                c.text(400, yy, lab, 40, col, m * a1 * a2, w='Bold', bg=CARD)
                for q in range(6):
                    c.line([(560 + q * 45, yy + 25 * math.sin(q * 1.3)), (580 + q * 45, yy - 25 * math.sin(q * 1.3 + 1))], col, 6, m * a1 * a2, CARD)
            k1 = hl(1)
            if k1 > 0:
                c.check(980, 465, 70, GR, k1 * a1 * a2, fd(T(1), 0, .6))
                c.text(980, 570, 'match', 40, GR, k1 * a1 * a2, w='Bold')
            v = 1 - .8 * fd(T(1), .4, 1.2) if T(1) > -.1 else 1.0
            meter(c, 1400, 760, 470, v, SELF, m * a1 * a2, lab=None)
            c.text(1400, 805, 'feeling volume', 32, DIM, m * a1 * a2, w='Medium')
            if T(1) > .6: c.text(1560, 760 - 470 * v, 'turned down', 34, YE, k1 * a1 * a2, 'lm', 'Bold')
        k2 = hl(2) * a1
        if k2 > 0:
            c.rr(560, 230, 1360, 820, 30, CARD, k2, outline=DIM, ow=3)
            c.text(960, 280, 'INBOX: things you feel', 36, DIM, k2, w='Bold', bg=CARD)
            sink = fd(T(2), .6, 1.4)
            # (label, colour, own?, start row, end row): your own touch sinks from the top to the bottom
            rows = [('Your own hand', SELF, True, 0, 3), ('Someone tickles you!', WORLD, False, 1, 0),
                    ('A bug lands on your arm!', WORLD, False, 2, 1), ('Your socks', DIM, True, 3, 2)]
            for lab, col, own, start, end in rows:
                yy = 360 + (start + (end - start) * sink) * 105
                aa = k2 * (1 - .55 * sink if own else 1)
                c.rr(620, yy - 40, 1300, yy + 40, 18, (40, 46, 84), aa, bg=CARD)
                c.circ(670, yy, 14, col, aa, bg=(40, 46, 84))
                c.text(710, yy, lab, 34, INK, aa, 'lm', 'Bold' if not own else 'Medium', bg=(40, 46, 84))
            c.text(960, 845, 'Expected messages sink to the bottom', 32, YE, k2 * sink, w='Bold')
    if T(3) > -.1:
        k = fd(T(3))
        c.text(960, 150, 'Brain scans, 1998', 60, INK, k, w='Bold')
        for j, (x, lab, col, act) in enumerate(((560, 'Touched by a robot', WORLD, .95), (1360, 'Touching yourself', SELF, .3))):
            kk = k * fd(T(3), .3 + j * .5)
            brain(c, x - 30, 460, 170, kk, touch=(YE, act))
            c.text(x, 700, lab, 40, col, kk, w='Bold')
            c.text(x, 755, 'touch area: ' + ('busy' if j == 0 else 'quieter'), 34, YE if j == 0 else DIM, kk, w='Medium')
        k4 = hl(4)
        if k4 > 0:
            brain(c, 1360 - 30, 460, 170, k4, cereb=.5 + .5 * math.sin(t * 4) ** 2, touch=(YE, .3))
            c.text(1640, 600, 'cerebellum', 38, GR, k4, 'lm', 'Bold')
            c.arrow(1630, 600, 1475, 560, GR, 5, k4, 16)
            c.text(960, 845, 'The cerebellum seems to make the prediction', 32, GR, k4, w='Bold')

def s_quiz(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0); ans = hl(3)
    c.text(960, 150, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 230, 'Why turn down your own touch?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 180, 'To notice the world', 72, GR, ans, w='Bold')
    k1 = hl(1)
    for j, (x, lab, col) in enumerate(((560, 'Save energy', DIM), (1360, 'Notice the world', WORLD))):
        kk = k1 * fd(T(1), j * .6)
        if kk <= 0: continue
        dim = 1 - .6 * ans if j == 0 else 1
        c.rr(x - 300, 320, x + 300, 800, 30, CARD, kk * dim, outline=GR if (j == 1 and ans > 0) else col, ow=5)
        c.text(x - 230, 375, 'AB'[j], 46, col, kk * dim, w='Bold', bg=CARD)
        if j == 0:
            c.rr(x - 110, 470, x + 90, 600, 16, None, kk * dim, outline=INK, ow=7, bg=CARD)
            c.rr(x + 90, 510, x + 115, 560, 6, INK, kk * dim, bg=CARD)
            c.rr(x - 95, 485, x - 30, 585, 8, GR, kk * dim, bg=CARD)
        else:
            c.rr(x - 220, 520, x + 220, 600, 40, SKIN, kk, bg=CARD)
            bug(c, x + 40 + 10 * math.sin(t * 3), 500, 60, t, kk, SKIN)
        c.text(x, 720, lab, 46, INK, kk * dim, w='Bold', bg=CARD)
        if j == 1 and ans > 0: c.check(x + 230, 375, 40, GR, ans, fd(T(3), .2))
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 560, 70, 1 - p, CY, fd(T(2)) * (1 - ans))
        c.text(960, 560, 'or', 44, DIM, fd(T(2)) * (1 - ans), w='Bold')
    if ans > 0:
        c.text(960, 860, 'Outside touches matter more than your own', 34, DIM, fd(T(3), .8), w='Medium')

DELAYS = ['0', '0.1 s', '0.2 s', '0.3 s']
def s_robot(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0)
    c.text(960, 140, 'The robot test, 1999', 60, INK, m, w='Bold')
    k1 = hl(1)
    handle_hand(c, 380, 520, 140, t, m)
    c.text(380, 700, 'one hand moves a handle', 30, DIM, m, w='Medium')
    if k1 > 0:
        c.arrow(560, 420, 960, 420, CY, 6, k1, 20)
        c.text(760, 380, 'robot copies it', 30, CY, k1, w='Bold')
        palm(c, 1390, 520, 90, k1)
        robot(c, 1210, 500, 140, t, k1)
        c.text(1390, 690, 'soft foam on the other palm', 30, DIM, k1, w='Medium')
    k2 = hl(2)
    if k2 > 0:
        # delay slider: 0 at line 2, slides to 0.2 s at line 3
        pos = 2 * fd(T(3), .2, 1.0) if T(3) > -.1 else 0.0
        x0, x1, y = 300, 1000, 800
        c.line([(x0, y), (x1, y)], (60, 66, 110), 10, k2)
        for j, lab in enumerate(DELAYS):
            xx = x0 + j * (x1 - x0) / 3
            c.circ(xx, y, 8, DIM, k2); c.text(xx, y + 42, lab, 28, DIM, k2, w='Medium')
        kx = x0 + pos * (x1 - x0) / 3
        c.circ(kx, y, 24, YE, k2)
        c.text(200, y, 'delay', 32, INK, k2, 'rm', 'Bold')
        tick = .15 + .65 * clamp(pos / 2)
        meter(c, 1700, 840, 330, tick, YE, k2, lab=None)
        c.text(1700, 470, 'tickly?', 30, DIM, k2, w='Medium')
        c.text(1700, 880, 'Illustrative', 22, DIM, k2, w='Regular')
        if pos > 1.6:
            wiggles(c, 1390, 500, 110, t, YE, k2 * fd(T(3), 1.0))
    k4 = hl(4)
    if k4 > 0:
        pill(c, 960, 245, 'Twist the direction: tickly too', PU, k4, 32, h=64, fg=INK)

def s_eyes(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0)
    c.text(960, 150, 'The same trick, with your eyes', 60, INK, m, w='Bold')
    k3 = hl(3)
    shake = 22 * math.sin(t * 22) * k3 * (0.5 + 0.5 * math.sin(t * 3) ** 2)
    # the room the eye is looking at
    rx, ry = 960 + shake, 420
    c.rr(rx - 480, ry - 180, rx + 480, ry + 180, 20, (34, 40, 76), m, outline=DIM, ow=3)
    c.rr(rx - 400, ry - 120, rx - 200, ry + 40, 8, (90, 140, 210), m, bg=(34, 40, 76))
    c.line([(rx - 300, ry - 120), (rx - 300, ry + 40)], (34, 40, 76), 6, m, (90, 140, 210))
    c.rr(rx - 40, ry - 110, rx + 120, ry + 10, 6, YE, m, bg=(34, 40, 76))
    c.circ(rx + 40, ry - 50, 30, PK, m, bg=YE)
    c.line([(rx + 330, ry + 170), (rx + 330, ry - 60)], DIM, 8, m, (34, 40, 76))
    c.circ(rx + 330, ry - 80, 50, (255, 230, 150), m, bg=(34, 40, 76))
    k1 = hl(1)
    targets = [-.9, .2, .9, -.3]
    look = targets[int(t * 1.2) % 4] if k1 > 0 else 0
    eye(c, 960, 740, 120, look, m)
    if k1 > 0 and k3 < .5:
        c.text(1300, 740, 'eyes jump', 36, CY, k1 * (1 - k3 * 2), 'lm', 'Bold')
        c.text(1300, 790, 'room stays still', 36, GR, hl(2) * (1 - k3 * 2), 'lm', 'Bold')
        c.check(1250, 790, 26, GR, hl(2) * (1 - k3 * 2), fd(T(2), .2))
    if k3 > 0:
        finger(c, 1080 - 20 * k3, 740, 40, 0.2, a=k3)
        c.text(560, 740, 'a finger nudges it:', 34, PK, k3, 'rm', 'Bold')
        c.text(560, 790, 'the world jumps', 34, PK, k3, 'rm', 'Bold')

def s_push(c, T, t):
    hl = lambda i: fd(T(i)) if T(i) > -.1 else 0.0
    m = hl(0)
    c.text(960, 150, 'A funny side effect', 60, INK, m, w='Bold')
    k1 = hl(1)
    # two fingers press on a plate from left and right, in turns
    turn = int(T(1) / 1.4) % 2 if T(1) > 0 else 0
    pressL = (1 if turn == 0 else 0) * k1; pressR = (1 if turn == 1 else 0) * k1
    c.rr(940, 300, 980, 520, 10, METAL, m)
    finger(c, 930 - 14 * pressL, 410, 70, math.pi, SKIN, m)
    finger(c, 990 + 14 * pressR, 410, 70, 0, OTHER, m)
    c.text(640, 530, 'Person A', 36, CY, m, w='Bold'); c.text(1280, 530, 'Person B', 36, PK, m, w='Bold')
    k2 = hl(2)
    if k1 > 0:
        c.text(960, 235, 'press back with the force you just felt', 34, DIM, k1, w='Medium')
    if k2 > 0:
        vals = [1, 1.4, 1.96, 2.74]
        for j, v in enumerate(vals):
            kk = k2 * fd(T(2), j * .35)
            x = 560 + j * 270; h = 50 * v
            col = CY if j % 2 == 0 else PK
            c.rr(x - 50, 820 - h, x + 50, 820, 10, col, kk)
            c.text(x, 845, f'turn {j + 1}', 24, DIM, kk, w='Medium')
        c.text(1520, 700, '≈ +40% each turn', 38, YE, k2, 'lm', 'Bold')
        c.text(1520, 750, 'Illustrative', 22, DIM, k2, 'lm', 'Regular')
    k3 = hl(3)
    if k3 > 0:
        pill(c, 960, 625, 'Your own push feels weaker than it is', YE, k3, 36, h=70)

REC = [('1', 'Your brain predicts', PRED), ('2', 'A match is turned down', SELF), ('3', 'Surprise = tickle', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 255, 290 + up, x + 255, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 190, 355 + up, 40, col, m, bg=CARD); c.text(x - 190, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 530 + up
        if i == 0:
            brain(c, x - 20, y - 20, 95, m, bg=CARD)
            c.rr(x + 60, y - 110, x + 210, y - 50, 14, PRED, m, bg=CARD)
            c.text(x + 135, y - 80, 'guess', 26, BG, m, w='Bold', bg=PRED)
        elif i == 1:
            meter(c, x - 60, y + 110, 220, .2, SELF, m, CARD)
            meter(c, x + 60, y + 110, 220, .9, PK, m * .5, CARD)
            c.check(x - 60, y - 140, 26, GR, m)
        else:
            palm(c, x, y + 20, 70, m, bg=CARD)
            wiggles(c, x, y - 10, 90, t, YE, m, bg=CARD)
        c.text(x, 740 + up, lab, 38, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["A robot can make your own touch tickle you.",
            "It just has to arrive a fifth of a second late.",
            "So why can't you tickle yourself in the first place?"], s_hook),
 ('1  ·  TRY IT', ["Try it. Run your fingertips lightly over your own palm.",
            "It feels like almost nothing.",
            "But when someone else does the exact same thing, you squirm.",
            "Same touch, same skin. The difference is in your brain."], s_try),
 ('2  ·  PREDICTION', ["Your brain is always predicting.",
            "Every time you move, it sends a command to your muscles.",
            "And it keeps a copy of that command.",
            "From that copy, it predicts what the movement will feel like. Scientists call this an efference copy."], s_predict),
 ('3  ·  THE MATCH', ["When the real feeling arrives, your brain checks it against the prediction.",
            "If they match, it turns the feeling down.",
            "Like a spam filter. Messages you expected sink to the bottom of the pile.",
            "Brain scans in nineteen ninety-eight backed this up. Touching your own hand made the brain's touch areas less active.",
            "A part at the back of the brain, the cerebellum, seems to make that prediction."], s_cancel),
 ('4  ·  QUICK QUESTION', ["Quick question. Why would your brain turn down your own touch?",
            "To save energy? Or to notice what the world is doing to you?",
            "Three, two, one.",
            "To notice the world. A bug landing on your arm matters more than your own hand resting there."], s_quiz),
 ('5  ·  THE ROBOT', ["In nineteen ninety-nine, the same team tested this with a robot.",
            "Sixteen people moved a handle, and a robot copied the movement onto their other palm, with soft foam.",
            "With no delay, it barely tickled.",
            "Delay it by a fifth of a second, and it tickled about as much as a robot moving on its own.",
            "Twisting the direction of the movement worked too. A surprise brings the tickle back."], s_robot),
 ('6  ·  YOUR EYES', ["Your eyes use the same trick, all day long.",
            "When you look around a room, your eyes jump, but the room stays still.",
            "Your brain predicted each jump, so it cancels the movement out.",
            "But if a finger nudges the eye, the world seems to jump. No command, no prediction."], s_eyes),
 ('7  ·  SIDE EFFECT', ["This prediction has a funny side effect.",
            "In a two thousand and three study, pairs took turns pressing each other's finger, matching the force they had just felt.",
            "Each one pressed back about forty percent harder, without meaning to.",
            "Their own push felt weaker than it was. So when two kids both say, you pushed harder, each may mean it."], s_push),
 ('RECAP', ["So remember three things.",
            "One. Your brain predicts what your own movements will feel like.",
            "Two. When the feeling matches, it is turned down. So you can't tickle yourself.",
            "Three. Add a surprise, like a tiny delay, and the tickle comes back.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('TRY IT', ["Why can't you tickle yourself?",
             "Run your fingers over your own palm. Almost nothing.",
             "But when someone else does it, you squirm."], s_try),
 ('PREDICTION', ["Here is why. Your brain is always predicting.",
                 "Every move starts with a command to your muscles.",
                 "Your brain keeps a copy, and predicts how the move will feel."], s_predict),
 ('THE MATCH', ["When the touch arrives, it matches the prediction.",
                "So your brain turns the feeling down."], s_cancel),
 ('THE ROBOT', ["Scientists tested it with a robot.",
                "People moved a handle, and a robot copied the touch onto their other palm.",
                "No delay: it barely tickled.",
                "A fifth of a second late, and it tickled again."], s_robot),
 ('THE ANSWER', ["That's the answer. Your brain predicts your own touch, and turns it down.",
                 "No surprise, no tickle. Follow for more."],
                card('Your brain predicts your own touch', 'No surprise, no tickle')),
]
SHORT_HITS = [(4, 0, 0.0)]
