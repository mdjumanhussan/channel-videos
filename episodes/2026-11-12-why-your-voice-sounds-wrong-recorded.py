"""Episode: Why Your Voice Sounds Wrong on Recordings (air conduction vs bone conduction; Hughes and Harrison 2013 self-rating study)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Your Voice Sounds Wrong'                 # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.94
SHORT_HOOK = 'Why do you sound weird recorded?'             # headline on the vertical Short
HITS = [(1, 2, 0.0), (5, 1, 0.0), (7, 2, 0.0)]              # the inside road, the answer, the twist
THUMB = ["THAT'S NOT", 'MY VOICE?', 'IT IS.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
# A short silence before each big reveal (lesson of 2026-11-12, TubeLab: 'silence before reveals').
PAUSES = {(0, 1): 0.3, (1, 0): 0.2, (2, 1): 0.3, (3, 0): 2.6, (4, 1): 0.3, (5, 0): 1.2, (6, 1): 0.3, (7, 1): 0.9, (8, 3): 0.2}
SHORT_PAUSES = {(0, 0): 0.2, (3, 0): 0.3}
CAPTION_FIXES = {'nineteen sixties': '1960s', 'twenty thirteen': '2013', 'eighty people': '80 people'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the air road is blue, the inside (bone) road and the deep sound it adds are yellow,
# the microphone / recording is pink, the answer is green.
AIR = CY; BONE = YE; MIC = PK; ANS = GR
DARK = (20, 22, 38); SKIN = (44, 52, 96); QUIZ = (52, 30, 74)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

# ---------- drawing helpers ----------
def head(c, x, y, s, a, bg=BG):
    """Side view of a head facing right. Returns key points: mouth, ear, inner ear."""
    if a > .01:
        c.circ(x, y - 40 * s, 230 * s, SKIN, a, outline=(90, 100, 160), ow=4, bg=bg)                       # skull
        c.rr(x - 60 * s, y + 60 * s, x + 200 * s, y + 230 * s, 90 * s, SKIN, a, bg=bg)                    # jaw
        c.rr(x - 110 * s, y + 150 * s, x + 30 * s, y + 380 * s, 40 * s, SKIN, a, bg=bg)                   # neck
        c.d.polygon([((x + 215 * s) * c.k, (y - 30 * s) * c.k), ((x + 285 * s) * c.k, (y + 60 * s) * c.k),
                     ((x + 210 * s) * c.k, (y + 70 * s) * c.k)], fill=mix(SKIN, a, bg))                    # nose
        c.circ(x + 150 * s, y - 70 * s, 14 * s, INK, a, bg=SKIN)                                          # eye
        c.line([(x + 175 * s, y + 130 * s), (x + 230 * s, y + 125 * s)], (200, 110, 140), 7 * s, a, bg=SKIN)  # mouth
        c.circ(x - 40 * s, y + 10 * s, 52 * s, None, a, outline=(150, 160, 210), ow=7 * s, bg=SKIN)         # ear
        c.circ(x - 40 * s, y + 10 * s, 14 * s, DARK, a, bg=SKIN)
    return dict(mouth=(x + 240 * s, y + 126 * s), ear=(x - 40 * s, y + 10 * s), inner=(x + 30 * s, y + 20 * s))

def cochlea(c, x, y, r, a, col=INK, bg=SKIN):
    if a <= .01: return
    pts = [(x + r * (1 - u / 3.2) * math.cos(u * 2.0), y + r * (1 - u / 3.2) * math.sin(u * 2.0)) for u in [k * .1 for k in range(31)]]
    c.line(pts, col, max(3, r * .22), a, bg=bg)

def waves(c, x, y, a, t, col=AIR, n=3, r0=30, dr=40, ang=0, spread=50, w=6, bg=BG):
    """Arcs spreading out from a point toward angle ang (degrees)."""
    if a <= .01: return
    for k in range(n):
        u = (t * .8 + k / n) % 1; r = r0 + dr * n * u
        box = ((x - r) * c.k, (y - r) * c.k, (x + r) * c.k, (y + r) * c.k)
        c.d.arc(box, ang - spread, ang + spread, fill=mix(col, a * (1 - u) * .95 + .05 * a, bg), width=int(w * c.k))

def dashed(c, pts, col, w, a, p=1.0, bg=BG, gap=3):
    """Polyline drawn up to fraction p, in dashes."""
    if a <= .01 or p <= 0: return
    n = max(1, int((len(pts) - 1) * clamp(p)))
    for i in range(0, n, gap):
        c.line(pts[i:i + 2], col, w, a, bg=bg)

def arc_pts(x0, y0, x1, y1, bulge, n=60):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L, dx / L
    cx, cy = mx + nx * bulge, my + ny * bulge
    return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1) for u in [k / n for k in range(n + 1)]]

def bars(c, x0, base, vals, cols, a, bw=70, gap=26, labels=None, bg=BG, maxh=320):
    for k, v in enumerate(vals):
        x = x0 + k * (bw + gap); h = maxh * v
        if h > 2: c.rr(x, base - h, x + bw, base, 10, cols[k], a, bg=bg)
    c.line([(x0 - 20, base), (x0 + len(vals) * (bw + gap), base)], DIM, 4, a, bg=bg)
    if labels:
        c.text(x0, base + 36, labels[0], 30, DIM, a, 'lm', 'Bold', bg=bg)
        c.text(x0 + len(vals) * (bw + gap) - gap, base + 36, labels[1], 30, DIM, a, 'rm', 'Bold', bg=bg)

LOW = [.55, .7, .8, .75, .6, .5, .42, .34, .28, .22]          # the air-only voice (illustrative)
BOOST = [.32, .28, .2, .12, .06, 0, 0, 0, 0, 0]               # extra deep sound from the inside road (illustrative)

def voice_bars(c, x0, base, a, boost=1.0, bg=BG, bw=70, maxh=320):
    cols = [AIR] * len(LOW)
    bars(c, x0, base, LOW, cols, a, bw=bw, labels=('low', 'high'), bg=bg, maxh=maxh)
    for k, b in enumerate(BOOST):
        if b * boost > .005:
            x = x0 + k * (bw + 26); h0 = maxh * LOW[k]; h = maxh * b * boost
            c.rr(x, base - h0 - h, x + bw, base - h0 + 6, 10, BONE, a, bg=bg)

def mic(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 45 * s, y - 120 * s, x + 45 * s, y + 20 * s, 45 * s, MIC, a, bg=bg)
    for k in range(3): c.line([(x - 30 * s, y - 80 * s + k * 28 * s), (x + 30 * s, y - 80 * s + k * 28 * s)], DARK, 4, a, bg=MIC)
    c.d.arc(((x - 70 * s) * c.k, (y - 60 * s) * c.k, (x + 70 * s) * c.k, (y + 60 * s) * c.k), 0, 180, fill=mix(MIC, a, bg), width=int(7 * s * c.k))
    c.line([(x, y + 60 * s), (x, y + 130 * s)], MIC, 7 * s, a, bg=bg); c.line([(x - 50 * s, y + 130 * s), (x + 50 * s, y + 130 * s)], MIC, 7 * s, a, bg=bg)

def phone(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 120 * s, y - 220 * s, x + 120 * s, y + 220 * s, 32 * s, (40, 44, 70), a, outline=(110, 120, 170), ow=4, bg=bg)
    c.rr(x - 102 * s, y - 190 * s, x + 102 * s, y + 180 * s, 16 * s, DARK, a, bg=(40, 44, 70))

def face_icon(c, x, y, r, a, mood=0, col=INK, bg=BG):
    """Simple round face. mood: 1 smile, 0 flat, -1 grimace."""
    if a <= .01: return
    c.circ(x, y, r, None, a, outline=col, ow=max(3, r * .08), bg=bg)
    c.circ(x - r * .35, y - r * .2, r * .09, col, a, bg=bg); c.circ(x + r * .35, y - r * .2, r * .09, col, a, bg=bg)
    if mood > 0: c.d.arc(((x - r * .45) * c.k, (y - r * .1) * c.k, (x + r * .45) * c.k, (y + r * .5) * c.k), 20, 160, fill=mix(col, a, bg), width=int(r * .08 * c.k))
    elif mood < 0:
        pts = [(x - r * .45 + k * r * .15, y + r * .35 + (8 if k % 2 else -8) * r / 100) for k in range(7)]
        c.line(pts, col, r * .08, a, bg=bg)
    else: c.line([(x - r * .35, y + r * .35), (x + r * .35, y + r * .35)], col, r * .08, a, bg=bg)

def hand(c, x, y, s, a, bg=BG):
    """A finger pressed into an ear: a rounded bar pointing at (x, y)."""
    if a <= .01: return
    c.rr(x - 30 * s, y - 20 * s, x + 30 * s, y + 160 * s, 28 * s, (230, 180, 150), a, bg=bg)
    c.rr(x - 60 * s, y + 120 * s, x + 60 * s, y + 280 * s, 50 * s, (230, 180, 150), a, bg=bg)

# ---------- scenes ----------
HX, HY, HS = 720, 530, .85
def s_hook(c, T, t):
    """Hook: a moment everyone has had, then the surprising true statement."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, '"Wait... is that really me?"', 88, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Yes. Everyone else hears that voice', 84, ANS, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'So why does it sound wrong to you?', 84, BONE, sw_in(T, 2), w='Bold')
    phone(c, 1240, 520, 1.15, 1)
    waves(c, 1240, 520, 1, t, MIC, n=3, r0=40, dr=50, ang=180, spread=40)
    for k in range(9):                                   # a playing voice clip on the phone, from the first frame
        h = 40 + 70 * abs(math.sin(t * 5 + k * .9))
        c.rr(1150 + k * 21, 520 - h / 2, 1162 + k * 21, 520 + h / 2, 6, MIC, 1, bg=DARK)
    c.text(1240, 700, 'your voice clip', 30, DIM, 1, w='Bold', bg=DARK)
    face_icon(c, 640, 500, 150, 1 - hl(1), -1)
    m1 = hl(1)
    for k in range(5):
        x = 420 + k * 105; face_icon(c, x, 520 + (k % 2) * 40, 52, m1 * fd(T(1), .15 * k), 1, AIR)
    c.text(630, 680, 'everyone else', 40, AIR, m1, w='Bold')
    m2 = hl(2)
    c.circ(630, 790, 46, BONE, m2); c.text(630, 790, '?', 66, DARK, m2, w='Bold', bg=BONE)

def s_roads(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Your voice takes two roads to your inner ear', 74, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Road 1: through the air, into the ear', 78, AIR, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Road 2: through the bones of your head', 78, BONE, sw_in(T, 2), w='Bold')
    P = head(c, HX, HY, HS, 1)
    cochlea(c, *P['inner'], 26, 1, INK)
    c.text(P['ear'][0], P['ear'][1] + 90, 'inner ear', 28, INK, 1, w='Bold', bg=SKIN)
    m1 = hl(1)
    mx, my = P['mouth']; ex, ey = P['ear']
    road1 = arc_pts(mx, my, ex - 50, ey + 26, -400)
    dashed(c, road1, AIR, 9, m1, fd(T(1), .2, 2.0), gap=2)
    waves(c, mx, my, m1, t, AIR, ang=0, spread=45)
    if T(1) > 2.2: c.line([(ex - 50, ey + 26), P['inner']], AIR, 7, m1 * fd(T(1), 2.2), bg=SKIN)
    c.text(1360, 520, 'air', 48, AIR, m1, w='Bold')
    m2 = hl(2)
    p2 = fd(T(2), .3, 1.6)
    ix, iy = P['inner']; sx, sy = HX + 160 * HS, HY + 110 * HS
    c.line([(sx, sy), (sx + (ix - sx) * p2, sy + (iy - sy) * p2)], BONE, 14, m2, bg=SKIN)
    for k in range(4):                                    # vibration ticks along the inside road
        u = ((t * .9 + k / 4) % 1) * p2; px, py = sx + (ix - sx) * u, sy + (iy - sy) * u
        c.circ(px, py, 12, BONE, m2, bg=SKIN)
    c.text(HX + 60 * HS, HY - 170 * HS, 'bone and tissue', 34, BONE, m2, w='Bold', bg=SKIN)
    m3 = hl(3)
    c.rr(1180, 640, 1860, 800, 24, CARD, m3, outline=(70, 80, 140), ow=3)
    c.text(1520, 690, 'air conduction', 44, AIR, m3, w='Bold', bg=CARD); c.text(1520, 750, 'bone conduction', 44, BONE, m3, w='Bold', bg=CARD)
    c.text(1880, 858, 'Simplified drawing, not to scale', 28, DIM, 1, anchor='rm', w='Regular')

def s_bass(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'The inside road changes the sound', 84, BONE, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Your head carries the deep, low parts best', 78, BONE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'In your head, you sound fuller and deeper', 78, INK, sw_in(T, 2), w='Bold')
    head(c, 360, 470, .62, 1)
    c.line([(360 + .62 * 160, 470 + .62 * 110), (360 + .62 * 30, 470 + .62 * 20)], BONE, 9, 1, bg=SKIN)
    c.rr(700, 270, 1700, 800, 30, CARD, 1, outline=(70, 80, 140), ow=3)
    c.text(1200, 320, 'your voice, by pitch', 36, DIM, 1, w='Bold', bg=CARD)
    boost = hl(1) * fd(T(1), .6, 1.4)
    voice_bars(c, 760, 700, 1, boost, bg=CARD, bw=66)
    c.text(890, 360, '+ deep boost', 38, BONE, boost, w='Bold', bg=CARD)
    m2 = hl(2)
    c.text(1200, 760, 'what you hear when you talk', 34, INK, m2, w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative bars, not measurements', 28, DIM, 1, anchor='rm', w='Regular')

def s_try(c, T, t):
    """Mid-video 'try it now' check (lesson of 2026-10-13: one mid-video question)."""
    hl = lambda i: hl_(T, i)
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    c.text(960, 172, 'TRY IT: fingers in your ears, then hum', 80, INK, sw_out(T, 1), w='Bold', bg=QUIZ)
    c.text(960, 172, 'Still loud. Even deeper. That is road 2', 82, BONE, sw_in(T, 1), w='Bold', bg=QUIZ)
    P = head(c, 820, 530, .85, 1, bg=QUIZ)
    ex, ey = P['ear']
    press = fd(T(0), .4, .8)
    hand(c, ex - 40, ey + 40 + 120 * (1 - press), .9, press, bg=QUIZ)
    cochlea(c, *P['inner'], 24, 1, INK)
    m0 = fd(T(0), 1.4)
    c.text(1300, 600, 'Mmmm', 70, AIR, m0 * (1 - hl(1)), w='Bold', bg=QUIZ)
    waves(c, *P['mouth'], m0 * (1 - hl(1)) * .6, t, AIR, ang=0, spread=40, bg=QUIZ)
    if 0 < T(0) and T(1) < 0:                            # countdown while the viewer tries it
        k = max(0, 3 - int(max(0, T(0) - 2.4) / .9)); u = fd(T(0), 2.4)
        c.circ(1560, 500, 90, BONE, u, bg=QUIZ); c.text(1560, 500, str(k) if k else 'hum', 80 if k else 56, DARK, u, w='Bold', bg=BONE)
    m1 = hl(1)
    ix, iy = P['inner']; sx, sy = 820 + .85 * 160, 530 + .85 * 110
    c.line([(sx, sy), (ix, iy)], BONE, 14, m1, bg=SKIN)
    for k in range(5):
        u = (t * 1.1 + k / 5) % 1; c.circ(sx + (ix - sx) * u, sy + (iy - sy) * u, 13, BONE, m1, bg=SKIN)
    c.cross(ex - 40, ey - 90, 50, AIR, m1)
    c.text(ex - 40, ey - 160, 'air road blocked', 32, AIR, m1, w='Bold', bg=QUIZ)

def s_mic(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A microphone has only one road: the air', 78, MIC, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'No inside road. No deep boost', 84, BONE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'So you sound higher and thinner', 86, MIC, sw_in(T, 2), w='Bold')
    m = 1 - hl(1)
    P = head(c, 330, 460, .7, 1)
    waves(c, *P['mouth'], 1, t, AIR, ang=0, spread=35)
    mic(c, 760, 560, 1.0, 1)
    c.text(760, 760, 'microphone', 34, MIC, 1, w='Bold')
    c.line([(P['mouth'][0] + 40, P['mouth'][1]), (690, 500)], AIR, 6, 1)
    c.rr(980, 270, 1820, 800, 30, CARD, 1, outline=(70, 80, 140), ow=3)
    c.text(1400, 320, 'what the recording keeps', 36, DIM, 1, w='Bold', bg=CARD)
    boost = 1 - hl(1) * fd(T(1), .5, 1.2)
    voice_bars(c, 1030, 700, 1, boost, bg=CARD, bw=56)
    if hl(1) > .01:
        c.cross(1120, 420, 70, MIC, hl(1) * fd(T(1), 1.4)); c.text(1260, 420, 'deep boost', 34, BONE, hl(1) * fd(T(1), 1.4), 'lm', 'Bold', bg=CARD)
    c.text(1400, 760, 'higher, thinner', 38, MIC, hl(2), w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative bars, not measurements', 28, DIM, 1, anchor='rm', w='Regular')

def s_answer(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'So which voice is the real you?', 86, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'To everyone else: the recorded one', 86, ANS, sw_in(T, 1), w='Bold')
    m1 = hl(1)
    for k, (lab, sub, col, boost) in enumerate((('In your head', 'air + bone', BONE, 1.0), ('In the room', 'air only', AIR, 0.0))):
        x0 = 230 + k * 780; win = k == 1
        oc = ANS if (win and m1 > .5) else (70, 80, 140)
        c.rr(x0, 270, x0 + 680, 800, 30, CARD, 1, outline=oc, ow=6 if win else 3)
        c.text(x0 + 340, 320, lab, 52, col, 1, w='Bold', bg=CARD)
        c.text(x0 + 340, 372, sub, 34, DIM, 1, w='Bold', bg=CARD)
        voice_bars(c, x0 + 60, 700, 1 - .5 * m1 * (not win), boost, bg=CARD, bw=36, maxh=260)
    c.circ(1600, 470, 70, ANS, m1, bg=CARD); c.check(1600, 470, 54, DARK, m1, fd(T(1), .3, .6))
    c.text(1350, 760, 'what other people hear', 34, ANS, m1, w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative bars', 28, DIM, 1, anchor='rm', w='Regular')

def s_cringe(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Then why does it feel so bad?', 86, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'You have only ever heard the mix', 86, BONE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Studied since the 1960s', 86, MIC, sw_in(T, 2), w='Bold')
    m0 = 1 - hl(1)
    face_icon(c, 960, 520, 190, m0, -1)
    for k in range(3):
        a = m0 * fd(T(0), .3 + .2 * k); c.text(1220 + k * 40, 380 - k * 60, '!', 70 + 10 * k, MIC, a, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    c.text(300, 340, 'every day of your life', 38, DIM, m1, 'lm', 'Bold')
    n = int(30 * fd(T(1), .2, 2.2))
    for k in range(30):
        x = 300 + (k % 10) * 135; y = 430 + (k // 10) * 130
        a = m1 * (1 if k < n else .25)
        c.rr(x, y, x + 110, y + 100, 16, CARD, m1)
        c.rr(x + 14, y + 30, x + 50, y + 74, 8, AIR, a, bg=CARD); c.rr(x + 60, y + 30, x + 96, y + 74, 8, BONE, a, bg=CARD)
    c.text(960, 840, 'air + bone, never air alone', 40, INK, m1, w='Bold')
    m2 = hl(2)
    c.rr(560, 330, 1360, 760, 30, CARD, m2, outline=MIC, ow=4)
    c.text(960, 420, 'Psychologists call it', 44, DIM, m2, w='Bold', bg=CARD)
    c.text(960, 520, '"voice confrontation"', 70, MIC, m2, w='Bold', bg=CARD)
    face_icon(c, 960, 660, 60, m2, -1, INK, bg=CARD)

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A 2013 study: 80 people rated voices', 82, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Their own voice was hidden in the mix', 82, BONE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'They rated it higher than others did', 82, ANS, sw_in(T, 2), w='Bold')
    you = 4
    for k in range(8):
        x = 250 + (k % 4) * 370; y = 300 + (k // 4) * 270
        own = k == you
        oc = BONE if (own and hl(1) > .3) else (70, 80, 140)
        c.rr(x, y, x + 320, y + 220, 24, CARD, fd(T(0), .1 * k), outline=oc, ow=5 if own else 3)
        for j in range(7):
            h = 20 + 50 * abs(math.sin(k * 1.7 + j * 1.1 + t * (3 if T(0) > 0 else 0)))
            c.rr(x + 40 + j * 36, y + 80 - h / 2, x + 60 + j * 36, y + 80 + h / 2, 5, AIR, fd(T(0), .1 * k), bg=CARD)
        if own: c.text(x + 160, y + 30, 'you', 30, BONE, hl(1), w='Bold', bg=CARD)
        sc = (3 if not own else 3) + (1.5 if own else 0) * hl(2) * fd(T(2), .5)
        for j in range(5):
            on = j < round(sc); col = ANS if (own and hl(2) > .3) else YE
            c.circ(x + 80 + j * 40, y + 170, 13, col if on else (60, 66, 100), fd(T(0), .1 * k), bg=CARD)
    m3 = hl(3)
    c.rr(250, 808, 1000, 864, 20, CARD, m3, outline=ANS, ow=3)
    c.text(625, 836, 'unconscious self-enhancement', 34, ANS, m3, w='Bold', bg=CARD)
    c.text(1880, 858, 'Hughes and Harrison, Perception, 2013. Star scores illustrative', 28, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 92, INK, 1, w='Bold')
    rows = ((1, 'You hear yourself through air and bone', BONE), (2, 'Bone adds deep sound, so you sound fuller', BONE),
            (3, 'A recording is air only: what others hear', ANS))
    for ln, txt, col in rows:
        m = hl(ln); y = 300 + (ln - 1) * 170; dx = 60 * (1 - m)
        c.rr(240 + dx, y, 1680 + dx, y + 130, 30, CARD, m, outline=col, ow=5)
        c.circ(320 + dx, y + 65, 46, col, m, bg=CARD); c.text(320 + dx, y + 65, str(ln), 52, DARK, m, w='Bold', bg=col)
        c.text(400 + dx, y + 65, txt, 50, INK, m, 'lm', 'Bold', bg=CARD)
    c.text(960, 840, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    P = head(c, 1420, 470, .9, 1)
    c.line([(1420 + .9 * 160, 470 + .9 * 110), P['inner']], BONE, 12, 1, bg=SKIN)
    cochlea(c, *P['inner'], 24, 1, INK)
    mic(c, 1760, 820, .6, 1)

SCENES = [
 ('THE HOOK', ["You hear your voice in a video, and you think: wait, is that really me?",
               "It is. That's the voice everyone else hears, every day.",
               "So why does it sound so wrong to you?"], s_hook),
 ('TWO ROADS', ["When you talk, your voice reaches your inner ear by two roads.",
                "Road one is the air. The sound leaves your mouth, travels round to your ear, and goes in, the way any sound does.",
                "Road two is inside you. The vibrations travel through the bones and tissues of your head, straight to your inner ear.",
                "Scientists call road one air conduction, and road two bone conduction."], s_roads),
 ('THE DEEP BOOST', ["That inside road changes the sound.",
                     "Your head carries the deep, low parts of your voice especially well.",
                     "So the voice you hear when you talk sounds fuller and deeper than the one in the room."], s_bass),
 ('TRY IT', ["Try this now. Put your fingers in your ears, and hum.",
             "You can still hear yourself. It's even louder and deeper. That's road two, with road one blocked."], s_try),
 ('THE MICROPHONE', ["A microphone only has one road. It picks up your voice through the air, like the people around you.",
                     "It gets no inside road, so the deep boost is gone.",
                     "That's why you sound higher and thinner on a recording."], s_mic),
 ('THE ANSWER', ["So which voice is the real you?",
                 "For everyone else, it's the one on the recording. The air-only voice is the one they hear.",
                 "It's much closer to their version than the voice inside your head."], s_answer),
 ('THE CRINGE', ["Then why does it feel so bad to hear?",
                 "Because you've never heard it on its own. Your whole life, you've heard the mix of both roads.",
                 "Psychologists have studied this cringe since the nineteen sixties. They call it voice confrontation."], s_cringe),
 ('THE TWIST', ["Here's a twist. In a twenty thirteen study, eighty people rated how attractive a set of recorded voices sounded.",
                "Their own voice was secretly mixed in, and most didn't realise.",
                "They rated their own voice as more attractive than other people rated it.",
                "The researchers saw it as unconscious self-enhancement. Deep down, we tend to like our own voice."], s_twist),
 ('RECAP', ["Three things to keep.",
            "One: you hear yourself through the air and through the bones of your head.",
            "Two: the bone road adds deep sound, so you sound fuller to yourself.",
            "Three: a recording only has the air road. That's close to what everyone else hears.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Why do you sound weird recorded?', 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'You normally hear it two ways at once', 80, BONE, sw_in(T, 1), w='Bold')
    m = 1 - hl(1)
    phone(c, 1300, 520, 1.1, m)
    for k in range(9):
        h = 40 + 70 * abs(math.sin(t * 5 + k * .9))
        c.rr(1215 + k * 21, 520 - h / 2, 1227 + k * 21, 520 + h / 2, 6, MIC, m, bg=DARK)
    face_icon(c, 640, 500, 170, m, -1)
    P = head(c, HX, HY, HS, hl(1))
    mx, my = P['mouth']; ex, ey = P['ear']
    dashed(c, arc_pts(mx, my, ex - 50, ey + 26, -400), AIR, 9, hl(1), 1.0, gap=2)
    c.line([(HX + 160 * HS, HY + 110 * HS), P['inner']], BONE, 14, hl(1), bg=SKIN)

def short_roads(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Air, into your ears', 88, AIR, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'And bone, straight to your inner ear', 82, BONE, sw_in(T, 1), w='Bold')
    P = head(c, HX, HY, HS, 1)
    cochlea(c, *P['inner'], 26, 1, INK)
    mx, my = P['mouth']; ex, ey = P['ear']
    dashed(c, arc_pts(mx, my, ex - 50, ey + 26, -400), AIR, 9, 1, fd(T(0), .2, 1.6), gap=2)
    waves(c, mx, my, 1, t, AIR, ang=0, spread=45)
    m1 = hl(1); p2 = fd(T(1), .2, 1.2); ix, iy = P['inner']; sx, sy = HX + 160 * HS, HY + 110 * HS
    c.line([(sx, sy), (sx + (ix - sx) * p2, sy + (iy - sy) * p2)], BONE, 14, m1, bg=SKIN)
    for k in range(4):
        u = ((t * .9 + k / 4) % 1) * p2; c.circ(sx + (ix - sx) * u, sy + (iy - sy) * u, 12, BONE, m1, bg=SKIN)
    c.text(1880, 858, 'Simplified drawing', 28, DIM, 1, anchor='rm', w='Regular')

def short_boost(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'The bone road boosts the deep sounds', 80, BONE, 1, w='Bold')
    c.rr(460, 270, 1460, 800, 30, CARD, 1, outline=(70, 80, 140), ow=3)
    boost = fd(T(0), 1.2, 1.4)
    voice_bars(c, 520, 700, 1, boost, bg=CARD, bw=66)
    c.text(650, 360, '+ deep boost', 38, BONE, boost, w='Bold', bg=CARD)
    c.text(960, 760, 'fuller and deeper, in your head', 34, INK, hl(1), w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative bars', 28, DIM, 1, anchor='rm', w='Regular')

def short_mic(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A microphone only hears the air', 84, MIC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'And that is what everyone else hears', 82, ANS, sw_in(T, 1), w='Bold')
    P = head(c, 330, 460, .7, 1)
    waves(c, *P['mouth'], 1, t, AIR, ang=0, spread=35)
    mic(c, 760, 560, 1.0, 1)
    c.rr(980, 270, 1820, 800, 30, CARD, 1, outline=ANS if hl(1) > .5 else (70, 80, 140), ow=5)
    boost = 1 - fd(T(0), 1.0, 1.0)
    voice_bars(c, 1030, 700, 1, boost, bg=CARD, bw=56)
    c.text(1400, 330, 'higher, thinner', 40, MIC, fd(T(0), 2.0), w='Bold', bg=CARD)
    m1 = hl(1)
    for k in range(4): face_icon(c, 1250 + k * 100, 845, 32, m1 * fd(T(1), .15 * k), 1, ANS)
    c.text(1880, 858, 'Illustrative bars', 28, DIM, 1, anchor='rm', w='Regular')

SHORT_SCENES = [
 ('THE HOOK', ["Why does your voice sound so weird on a recording?",
               "Because when you talk, you hear it two ways at once."], short_open),
 ('TWO ROADS', ["Part of the sound travels through the air, into your ears.",
                "Part travels through the bones of your head, straight to your inner ear. That's called bone conduction."], short_roads),
 ('THE DEEP BOOST', ["That bone road carries the deep, low sounds especially well.",
                     "So in your own head, you sound fuller and deeper."], short_boost),
 ('THE MICROPHONE', ["A microphone only hears the air. The deep boost is gone, so you sound higher and thinner.",
                     "And that air-only voice is the one everyone else hears."], short_mic),
 ('THE ANSWER', ["So the recording isn't wrong.",
                 "It's just missing the bass your own head adds."], card('The recording is right.', 'It just lacks your skull\'s bass.')),
]
SHORT_HITS = [(4, 0, 0.0)]
