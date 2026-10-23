"""Episode: Why Airlines Sell More Tickets Than There Are Seats"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why Airlines Overbook"                   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                       # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why sell more tickets than seats?"        # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 2, 0.0), (5, 3, 0.0)]           # title card, law of large numbers, quiz answer
THUMB = ['180 SEATS.', '185 TICKETS.', 'ON PURPOSE.']
MUSIC_LEVEL = 0.006                                      # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                           # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.5, (4, 2): 0.7, (4, 3): 0.5, (5, 3): 0.5}
SHORT_PAUSES = {(0, 2): 0.4, (1, 2): 0.4}
CAPTION_FIXES = {'ten thousand': '10,000', 'thirty-seven thousand': '37,000', 'twenty chairs': '20 chairs',
                 'twenty-four friends': '24 friends', 'ten US airlines': '10 US airlines'}

SEAT = (62, 74, 130); SKY = (120, 190, 255); BROWN = (150, 105, 70)
EMPTY = [(3, 1), (8, 4), (14, 0), (19, 5), (25, 2)]       # the five illustrative no-show seats

# ---------------------------------------------------------------- drawing helpers
def seat_xy(x0, y0, j, k, sz=34, gap=6):
    return x0 + j * (sz + gap) + sz / 2, y0 + k * (sz + gap) + (26 if k >= 3 else 0) + sz / 2

def cabin(c, x0, y0, cols=30, sz=34, gap=6, state=None, a=1.0, bg=BG, fus=True):
    """Top view of a cabin: cols rows of 6 seats with an aisle. state(j, k) -> 'full' | 'empty' | colour tuple."""
    if a <= .01: return
    w = cols * (sz + gap); h = 6 * (sz + gap) + 26
    if fus:
        c.rr(x0 - 90, y0 - 40, x0 + w + 40, y0 + h + 34, (h + 74) / 2, (24, 30, 62), a, outline=(70, 84, 140), ow=4, bg=bg)
    for j in range(cols):
        for k in range(6):
            x, y = seat_xy(x0, y0, j, k, sz, gap)
            st = state(j, k) if state else 'full'
            if st == 'empty':
                c.rr(x - sz / 2, y - sz / 2, x + sz / 2, y + sz / 2, 7, None, a, outline=DIM, ow=2, bg=(24, 30, 62))
            else:
                col = st if isinstance(st, tuple) else SEAT
                c.rr(x - sz / 2, y - sz / 2, x + sz / 2, y + sz / 2, 7, col, a, bg=(24, 30, 62))
                c.circ(x, y, sz * .26, INK if st == 'full' else BG, a * .9, bg=col)

def plane_side(c, x, y, w, a=1.0, bg=BG, col=SKY):
    if a <= .01: return
    h = w * .16
    c.d.polygon([((x - w * .42) * c.k, (y - h * .3) * c.k), ((x - w * .5) * c.k, (y - h * 1.5) * c.k),
                 ((x - w * .38) * c.k, (y - h * 1.5) * c.k), ((x - w * .25) * c.k, (y - h * .3) * c.k)], fill=mix(col, a * .8, bg))
    c.rr(x - w * .48, y - h / 2, x + w * .5, y + h / 2, h / 2, col, a, bg=bg)
    c.d.polygon([((x - w * .05) * c.k, (y + h * .1) * c.k), ((x - w * .2) * c.k, (y + h * 1.6) * c.k),
                 ((x - w * .1) * c.k, (y + h * 1.6) * c.k), ((x + w * .15) * c.k, (y + h * .1) * c.k)], fill=mix(mix(col, .75, BG), a, bg))
    for i in range(12):
        c.circ(x - w * .3 + i * w * .055, y - h * .12, h * .1, BG, a, bg=col)

def ticket(c, x, y, w, col=YE, a=1.0, bg=BG, label=''):
    if a <= .01: return
    h = w * .48
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, w * .08, col, a, bg=bg)
    for sy in (-1, 1): c.circ(x + w * .22, y + sy * h / 2, w * .06, bg, a, bg=col)
    for i in range(4): c.line([(x + w * .22, y - h * .3 + i * h * .2), (x + w * .22, y - h * .2 + i * h * .2)], bg, max(2, w * .02), a, col)
    if label: c.text(x - w * .12, y, label, max(14, int(w * .2)), BG, a, w='Bold', bg=col)

def person(c, x, y, s, col=INK, a=1.0, bg=BG, arm=0.0):
    if a <= .01: return
    c.circ(x, y - s * .55, s * .22, col, a, bg=bg)
    c.rr(x - s * .28, y - s * .28, x + s * .28, y + s * .45, s * .14, col, a, bg=bg)
    if arm > 0:
        c.line([(x + s * .22, y - s * .2), (x + s * .45, y - s * .2 - s * .55 * arm)], col, s * .1, a, bg)

def runner(c, x, y, s, t, col=PK, a=1.0):
    if a <= .01: return
    c.circ(x, y - s * .55, s * .16, col, a)
    c.line([(x, y - s * .38), (x - s * .08, y + s * .05)], col, s * .09, a)
    ph = math.sin(t * 9)
    c.line([(x - s * .08, y + s * .05), (x - s * .08 + s * .25 * ph, y + s * .5)], col, s * .09, a)
    c.line([(x - s * .08, y + s * .05), (x - s * .08 - s * .25 * ph, y + s * .5)], col, s * .09, a)
    c.line([(x - s * .03, y - s * .3), (x + s * .25 * ph, y - s * .05)], col, s * .08, a)
    c.line([(x - s * .03, y - s * .3), (x - s * .25 * ph, y - s * .05)], col, s * .08, a)

def clock(c, x, y, r, t, col=YE, a=1.0):
    if a <= .01: return
    c.circ(x, y, r, None, a, outline=col, ow=max(3, r * .12))
    ang = t * 2.5
    c.line([(x, y), (x + r * .7 * math.sin(ang), y - r * .7 * math.cos(ang))], col, max(3, r * .1), a)
    c.line([(x, y), (x + r * .45 * math.sin(ang / 12), y - r * .45 * math.cos(ang / 12))], col, max(3, r * .12), a)

def chair(c, x, y, s, col=SEAT, a=1.0, bg=BG):
    if a <= .01: return
    c.rr(x - s * .35, y - s * .6, x + s * .35, y - s * .05, s * .08, col, a, bg=bg)
    c.rr(x - s * .4, y - s * .08, x + s * .4, y + s * .08, s * .05, col, a, bg=bg)
    c.line([(x - s * .32, y + s * .05), (x - s * .32, y + s * .5)], col, s * .08, a, bg)
    c.line([(x + s * .32, y + s * .05), (x + s * .32, y + s * .5)], col, s * .08, a, bg)

def coin_flip(c, x, y, r, t, a=1.0, heads=True, spin=True):
    if a <= .01: return
    sx = abs(math.cos(t * 7)) if spin else 1.0
    face = (math.cos(t * 7) > 0) if spin else heads
    col = YE if face else (220, 160, 60)
    c.d.ellipse(((x - r * max(.08, sx)) * c.k, (y - r) * c.k, (x + r * max(.08, sx)) * c.k, (y + r) * c.k), fill=mix(col, a))
    if sx > .45: c.text(x, y, 'H' if face else 'T', int(r * .9), BG, a, w='Bold', bg=col)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def briefcase(c, x, y, s, a=1.0, bg=CARD):
    c.rr(x - s * .2, y - s * .62, x + s * .2, y - s * .38, s * .06, None, a, outline=BROWN, ow=max(3, s * .07), bg=bg)
    c.rr(x - s * .6, y - s * .42, x + s * .6, y + s * .42, s * .1, BROWN, a, bg=bg)
    c.line([(x - s * .6, y - s * .05), (x + s * .6, y - s * .05)], mix(BROWN, .55, BG), s * .05, a, BROWN)

def suitcase(c, x, y, s, a=1.0, bg=CARD):
    c.circ(x + s * .55, y - s * .55, s * .22, YE, a, bg=bg)
    for i in range(8):
        ang = i * math.pi / 4
        c.line([(x + s * .55 + s * .3 * math.cos(ang), y - s * .55 + s * .3 * math.sin(ang)),
                (x + s * .55 + s * .38 * math.cos(ang), y - s * .55 + s * .38 * math.sin(ang))], YE, s * .04, a, bg)
    c.rr(x - s * .15, y - s * .52, x + s * .15, y - s * .3, s * .05, None, a, outline=CY, ow=max(3, s * .06), bg=bg)
    c.rr(x - s * .4, y - s * .32, x + s * .4, y + s * .5, s * .1, CY, a, bg=bg)
    for sx in (-.18, .18): c.line([(x + s * sx, y - s * .25), (x + s * sx, y + s * .43)], mix(CY, .5, BG), s * .05, a, CY)

_DOTS = {}
def dot_field(c, x0, y0, cols, rows, sp, a=1.0, col=DIM):
    """Pre-rendered field of cols*rows tiny dots (cached), pasted with alpha a."""
    if a <= .01: return
    key = (cols, rows, sp, c.k)
    if key not in _DOTS:
        m = Image.new('L', (int(cols * sp * c.k) + 2, int(rows * sp * c.k) + 2), 0); d = ImageDraw.Draw(m)
        r = sp * .32 * c.k
        for j in range(cols):
            for i in range(rows):
                cx, cy = (j + .5) * sp * c.k, (i + .5) * sp * c.k
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        _DOTS[key] = m
    m = _DOTS[key]
    c.img.paste(Image.new('RGB', m.size, col), (int(x0 * c.k), int(y0 * c.k)), m.point(lambda v: int(v * clamp(a))))

def thumb_art(c):
    for i in range(6):
        ang = (i - 2.5) * 9
        img = Image.new('RGB', (int(330 * c.k), int(200 * c.k)), BG); cc = C(img, c.k)
        ticket(cc, 165, 100, 300, YE if i < 5 else PK, 1, label='SEAT' if i < 5 else '???')
        img = img.rotate(ang, resample=Image.BICUBIC, fillcolor=BG)
        c.img.paste(img, (int((1340 + i * 40) * c.k), int((300 + abs(i - 2.5) * 30 + i * 25) * c.k)))
    plane_side(c, 1560, 200, 520)

# ---------------------------------------------------------------- scenes
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 1.0, .5)
    if a > 0:
        # motion from frame one: the plane glides in, the ticket counter keeps ticking past the seat count
        plane_side(c, 520 + 40 * math.sin(t * .8), 300 + 10 * math.sin(t * 1.3), 760, a)
        c.rr(260, 480, 780, 760, 30, CARD, a, outline=CY, ow=4)
        c.text(520, 540, 'SEATS', 40, DIM, a, w='Bold', bg=CARD)
        c.text(520, 650, '180', 150, CY, a, w='Bold', bg=CARD)
        k1 = fd(t, 0, .3)
        n = int(172 + 13 * ease(clamp((t - 1.0) / 4.0)))
        over = n > 180
        c.rr(1060, 480, 1580, 760, 30, CARD, a * k1, outline=PK if over else YE, ow=4)
        c.text(1320, 540, 'TICKETS SOLD', 40, DIM, a * k1, w='Bold', bg=CARD)
        c.text(1320, 650, str(n), 150, PK if over else YE, a * k1, w='Bold', bg=CARD)
        for i in range(6):
            tx = 1100 + i * 92 + 14 * math.sin(t * 2 + i); ty = 300 - 50 * math.sin(t * 1.6 + i * .9) + (i % 2) * 60
            ticket(c, tx, ty, 80, YE, a * k1 * .9)
        c.text(960, 830, 'not a mistake: on purpose', 52, YE, a * hl(2), w='Bold')
        c.text(1840, 850, 'Illustrative', 26, DIM, a, 'rm', 'Medium')
    if T(3) > 1.0:
        m = fd(T(3), 1.3, .7)
        c.text(960, 330 + 30 * (1 - m), 'More Tickets', 124, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'Than Seats', 124, YE, m, w='Bold')
        c.line([(960 - 320 * m, 590), (960 + 320 * m, 590)], CY, 8, m)
        c.text(960, 680, 'Why airlines overbook, on purpose', 46, DIM, fd(T(3), 1.9), w='Medium')

CX0, CY0 = 380, 400
def s_empty(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Some passengers never arrive', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'An empty seat earns $0', 64, PK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'So: sell a few extra tickets', 64, GR, hl(2), w='Bold')
    gone = fd(T(0), 1.0, .8)
    fill = [fd(T(2), 1.0 + i * .35, .9) if T(2) > -.1 else 0.0 for i in range(5)]
    def st(j, k):
        if (j, k) in EMPTY:
            i = EMPTY.index((j, k))
            if fill[i] > .95: return GR
            if gone > .5: return 'empty'
        return 'full'
    cabin(c, CX0, CY0, state=st, a=hl(0))
    if T(1) < 0 or True:
        for i, (j, k) in enumerate(EMPTY):
            x, y = seat_xy(CX0, CY0, j, k)
            if hl(1) > 0 and fill[i] < .95:
                pul = .6 + .4 * math.sin(t * 6 + i)
                c.rr(x - 21, y - 21, x + 21, y + 21, 8, None, hl(1) * pul, outline=PK, ow=4, bg=(24, 30, 62))
    # line 0: someone running late to a gate
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        runner(c, 700 + 60 * math.sin(t * .7), 790, 110, t, PK, k0)
        clock(c, 880, 760, 40, t, YE, k0)
        c.text(960, 780, 'most no-shows are running late', 40, DIM, k0 * fd(T(0), 1.6), 'lm', 'Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.text(960, 760, 'empty seats: $0 each', 46, PK, k1, w='Bold')
        c.text(960, 820, 'doors closed: the seat can never be sold again', 38, INK, k1 * fd(T(1), 1.2), w='Bold')
    # line 2: five extra tickets fly into the empty seats
    for i, (j, k) in enumerate(EMPTY):
        if T(2) > -.1 and .02 < fill[i] < .98:
            x, y = seat_xy(CX0, CY0, j, k); p = ease(fill[i])
            ticket(c, 1700 + (x - 1700) * p, 820 + (y - 820) * p - 120 * math.sin(math.pi * p), 70, YE, 1)
    if T(2) > -.1:
        c.text(960, 800, '5 extra tickets fill 5 empty seats', 42, GR, hl(2) * fd(T(2), 2.6), w='Bold')
    c.text(1840, 860, 'Illustrative', 26, DIM, hl(0), 'rm', 'Medium')

def s_party(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'You already do this', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, '20 chairs, 24 invitations', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'Same idea, bigger numbers', 64, CY, hl(2), w='Bold')
    # chairs
    for i in range(20):
        x = 300 + (i % 10) * 100; y = 420 + (i // 10) * 190
        kk = hl(0) * fd(T(0), .3 + i * .04)
        chair(c, x, y, 80, SEAT, kk)
        sit = fd(T(1), 2.4 + i * .06, .5) if T(1) > -.1 else 0.0
        if sit > 0: person(c, x, y - 40, 70, [CY, GR, YE, PK][i % 4], kk * sit)
    # invitations: 24 envelopes, four crossed out
    k1 = hl(1)
    if k1 > 0:
        for i in range(24):
            x = 1430 + (i % 4) * 100; y = 290 + (i // 4) * 85
            kk = k1 * fd(T(1), i * .05)
            c.rr(x - 38, y - 26, x + 38, y + 26, 6, INK, kk)
            c.line([(x - 38, y - 26), (x, y + 4), (x + 38, y - 26)], DIM, 3, kk, INK)
            if i in (3, 9, 14, 22):
                c.cross(x, y, 60, PK, kk * fd(T(1), 1.6))
        c.text(1580, 830, '4 can\'t make it', 40, PK, k1 * fd(T(1), 1.8), w='Bold')
    if hl(2) > 0:
        c.text(760, 830, 'every chair filled', 40, GR, hl(2), w='Bold')

def s_predict(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'How many won\'t show?', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'Records of many past flights', 64, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'A forecast for every flight', 64, YE, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for i in range(5):
            person(c, 560 + i * 200, 520 + 10 * math.sin(t * 2 + i), 150, INK, k0 * fd(T(0), i * .1))
            c.text(560 + i * 200, 360, '?', 70, YE, k0 * (.5 + .5 * math.sin(t * 4 + i)), w='Bold')
    k1 = hl(1)
    if k1 > 0:
        labs = [('ROUTE', CY), ('TIME OF DAY', YE), ('BOOKED WHEN', PK)]
        for i in range(6):
            o = (5 - i) * 14
            c.rr(260 + o, 300 - o, 860 + o, 760 - o, 20, mix(CARD, 1, BG), k1 * fd(T(1), i * .08), outline=(60, 70, 120), ow=2)
        for j, (lab, col) in enumerate(labs):
            y = 400 + j * 120
            kk = k1 * fd(T(1), 1.0 + j * .8)
            c.text(300, y, lab, 34, col, kk, 'lm', 'Bold', bg=CARD)
            for b in range(5):
                c.rr(660 + b * 36, y - 15, 688 + b * 36, y + 15, 5, col, kk * (.35 + .65 * ((b * 7 + j * 3) % 5) / 4), bg=CARD)
        c.text(560, 820, 'past departures', 34, DIM, k1, w='Medium')
    k2 = hl(2)
    if k2 > 0:
        c.arrow(900, 530, 1060, 530, DIM, 6, k2, 24)
        c.rr(1090, 420, 1330, 640, 26, CARD, k2, outline=CY, ow=5)
        for g in range(3):
            ang = t * 1.6 + g * 2.09
            c.circ(1210 + 40 * math.cos(ang), 530 + 40 * math.sin(ang), 14, [CY, YE, PK][g], k2, bg=CARD)
        c.text(1210, 690, 'model', 36, CY, k2, w='Bold')
        c.arrow(1360, 530, 1460, 530, DIM, 6, k2 * fd(T(2), 1.0), 24)
        kk = k2 * fd(T(2), 1.4)
        c.rr(1480, 410, 1800, 650, 26, YE, kk)
        c.text(1640, 470, 'Flight 123', 32, BG, kk, w='Bold', bg=YE)
        c.text(1640, 545, '~5', 80, BG, kk, w='Bold', bg=YE)
        c.text(1640, 615, 'no-shows expected', 28, BG, kk, w='Bold', bg=YE)
        c.text(1640, 700, 'Illustrative', 26, DIM, kk, w='Medium')

_RNG = np.random.default_rng(7)
FLIPS = _RNG.random(1000) < .5
HEADS_CUM = np.cumsum(FLIPS)
def s_crowd(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'One person: impossible to call', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'One coin vs a thousand coins', 62, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'The law of large numbers', 62, GR, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 130, 'So far', 62, CY, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        person(c, 960, 560, 260, INK, k0)
        flip = math.sin(t * 5) > 0
        if flip: c.check(1180, 420, 90, GR, k0)
        else: c.cross(1180, 420, 110, PK, k0)
        c.text(1180, 560, 'shows up?', 40, DIM, k0, w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        coin_flip(c, 420, 480, 120, t, k1)
        c.text(420, 680, '1 coin: anything', 40, PK, k1, w='Bold')
        shown = int(1000 * clamp(T(1) / 4.5)) if T(1) > 0 else 0
        for i in range(shown):
            x = 860 + (i % 40) * 23; y = 280 + (i // 40) * 20
            c.circ(x, y, 8, YE if FLIPS[i] else (200, 140, 50), k1)
        if shown > 0:
            h = int(HEADS_CUM[shown - 1]); pct = 100 * h / shown
            c.text(1310, 820, f'{shown} coins: {pct:.0f}% heads', 44, GR if shown > 200 else INK, k1, w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        # illustrative: how many of 180 ticket holders miss a flight, over many simulated flights
        from math import comb
        p = .03; ps = [comb(180, x) * p ** x * (1 - p) ** (180 - x) for x in range(15)]
        mx = max(ps); base = 760
        for x, pr in enumerate(ps):
            hh = 420 * pr / mx * fd(T(2), .2 + x * .06, .6)
            bx = 480 + x * 68
            c.rr(bx - 26, base - hh, bx + 26, base, 8, GR if 3 <= x <= 8 else (60, 120, 100), k2 * (1 if hh > 3 else 0))
            c.text(bx, base + 36, str(x), 28, DIM, k2, w='Medium')
        c.line([(440, base), (1460, base)], DIM, 3, k2)
        c.text(960, 840, 'no-shows per flight, many flights of 180  (Illustrative)', 32, DIM, k2, w='Medium')
        c.text(1570, 400, 'most flights:', 38, INK, k2 * fd(T(2), 1.6), 'lm', 'Bold')
        c.text(1570, 450, '3 to 8', 52, GR, k2 * fd(T(2), 1.6), 'lm', 'Bold')
    k3 = hl(3)
    if k3 > 0:
        items = [('Some passengers always miss flights', PK), ('With a full plane, how many is predictable', GR)]
        for i, (lab, col) in enumerate(items):
            kk = k3 * fd(T(3), .3 + i * 1.6)
            y = 400 + i * 200
            c.rr(300, y - 70, 1620, y + 70, 30, CARD, kk, outline=col, ow=4)
            c.check(400, y, 70, col, kk, fd(T(3), .5 + i * 1.6, .6))
            c.text(480, y, lab, 50, INK, kk, 'lm', 'Bold', bg=CARD)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 120, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 195, 'Which flight would the airline overbook more?', 44, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'A: more business travellers miss flights', 56, GR, ans, w='Bold')
    cards = [('A', 'Monday morning', 'business trip', briefcase, 560), ('B', 'Home after a', 'long weekend', suitcase, 1360)]
    for j, (lab, l1, l2, icon, x) in enumerate(cards):
        kk = m * (.3 + .7 * (fd(T(1), j * 1.6) if T(1) > -.1 else 0.0))
        win = (j == 0)
        dim = 1 - .6 * ans * (not win)
        col = GR if (ans > 0 and win) else CY
        c.rr(x - 300, 280, x + 300, 760, 34, CARD, kk * dim, outline=col, ow=6 if ans > 0 and win else 3)
        c.circ(x - 230, 340, 42, col, kk * dim, bg=CARD); c.text(x - 230, 340, lab, 48, BG, kk * dim, w='Bold', bg=col)
        icon(c, x, 470, 150, kk * dim)
        c.text(x, 640, l1, 42, INK, kk * dim, w='Bold', bg=CARD)
        c.text(x, 695, l2, 42, INK, kk * dim, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 520, 70, 1 - p, YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        c.text(560, 820, 'more likely to be no-shows', 38, GR, fd(T(3), 1.0), w='Bold')
        c.text(1360, 820, 'more likely to show up', 38, DIM, hl(4), w='Bold')

def s_bump(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Sometimes everyone shows up', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'First: ask for volunteers', 64, GR, hl(1) * (1 - hl(3)), w='Bold')
    c.text(960, 130, 'Nobody agrees? Bumped', 64, PK, hl(3), w='Bold')
    k = hl(0)
    cabin(c, 330, 250, cols=30, sz=22, gap=4, a=k)
    c.text(1190, 370, 'all 180 seats full', 34, CY, k * fd(T(0), .8), 'lm', 'Bold')
    # the gate: five extra passengers waiting
    for i in range(5):
        x = 640 + i * 150
        vol = (i == 1 and T(1) > -.1)
        bumped = (i == 3 and T(3) > -.1)
        col = GR if vol and hl(1) > .5 else (PK if bumped and hl(3) > .5 else INK)
        arm = fd(T(1), 1.0, .5) if vol else 0.0
        person(c, x, 690 + 6 * math.sin(t * 2 + i), 120, col, k * fd(T(0), 1.0 + i * .15), arm=arm)
        if not vol and not bumped and hl(1) < .5:
            c.text(x, 590, '?', 46, YE, k * fd(T(0), 1.5) * (1 - hl(1)), w='Bold')
    c.rr(560, 770, 1360, 800, 10, (60, 70, 120), k)
    c.text(1190, 420, 'Illustrative', 26, DIM, k, 'lm', 'Medium')
    if hl(1) > 0:
        kk = hl(1) * fd(T(1), 1.6)
        p = fd(T(1), 1.6, 1.0)
        ticket(c, 1600 - (1600 - 790) * p, 640 - (640 - 540) * p - 80 * math.sin(math.pi * p), 110, GR, kk, label='$')
        c.text(1600, 560, 'voucher or money', 38, GR, kk * (1 - hl(3)), w='Bold')
        c.text(1600, 615, 'US rules: volunteers first', 32, DIM, hl(2) * (1 - hl(3)), w='Medium')
    if hl(3) > 0:
        c.text(1560, 560, 'bumped against their will', 36, PK, hl(3) * fd(T(3), 1.4), w='Bold')
        c.text(1560, 615, 'US and EU: usually compensated', 32, DIM, hl(3) * fd(T(3), 3.4), w='Medium')

def s_rare(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'How often does it happen?', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 130, 'Bumped against their will (US)', 64, PK, hl(1) * (1 - hl(3)), w='Bold')
    c.text(960, 130, 'And fewer empty seats', 64, GR, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for i in range(7):
            person(c, 420 + i * 180, 560, 150, [CY, YE, GR, INK, PK, CY, YE][i], k0 * fd(T(0), i * .08))
        c.text(960, 380, '?', 120, YE, k0 * (.6 + .4 * math.sin(t * 4)), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.text(960, 430, '0.27', 220, PK, k1, w='Bold')
        c.text(960, 590, 'in every 10,000 passengers', 56, INK, k1 * fd(T(1), 1.2), w='Bold')
        c.text(960, 680, '10 US reporting airlines, Jan to Mar 2024 (US DOT)', 32, DIM, k1 * fd(T(1), 2.0), w='Medium')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        cols, rows, sp = 300, 124, 4.6
        x0, y0 = 960 - cols * sp / 2, 220
        dot_field(c, x0, y0, cols, rows, sp, k2 * .8, (90, 100, 150))
        px, py = x0 + 210.5 * sp, y0 + 50.5 * sp
        pul = .5 + .5 * math.sin(t * 5)
        c.circ(px, py, 10 + 30 * pul, None, k2 * fd(T(2), 1.0) * (1 - .5 * pul), outline=PK, ow=4)
        c.circ(px, py, 9, PK, k2 * fd(T(2), 1.0))
        c.rr(620, 790, 1300, 870, 30, CARD, k2 * fd(T(2), 1.4))
        c.text(960, 830, '1 person in about 37,000', 44, PK, k2 * fd(T(2), 1.4), w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        cabin(c, 380, 330, a=k3)
        c.text(960, 720, 'analysts: helps keep fares lower', 48, GR, k3 * fd(T(3), 1.4), w='Bold')
        c.text(960, 790, 'empty seats cost money; overbooking fills them', 34, DIM, k3 * fd(T(3), 2.6), w='Medium')

RECAPS = [('1', 'An empty seat earns nothing', PK), ('2', 'Big crowds are predictable', GR), ('3', 'Volunteers first; bumping is rare', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 520 + up
        if i == 0:
            c.rr(x - 50, y - 50, x + 50, y + 50, 14, None, m, outline=DIM, ow=4, bg=CARD)
            c.text(x, y - 90, '$0', 50, PK, m * (.6 + .4 * math.sin(t * 4)), w='Bold', bg=CARD)
        elif i == 1:
            for j in range(9):
                coin_flip(c, x - 120 + (j % 3) * 120, y - 80 + (j // 3) * 80, 30, t + j * .7, m)
        else:
            person(c, x, y + 40, 150, GR, m, CARD, arm=.6 + .4 * math.sin(t * 3))
        ls = wrap(c, lab, 32, 470, 'Bold')
        for j, l in enumerate(ls): c.text(x, 700 + up + j * 42 - (len(ls) - 1) * 21, l, 32, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["This plane has 180 seats.",
            "The airline sold 185 tickets.",
            "That's not a mistake. It's on purpose.",
            "So why would an airline sell seats it doesn't have?"], s_hook),
 ('1  ·  THE EMPTY SEAT', ["Some passengers never make it to the gate. Most of them are simply running late.",
            "Once the doors close, an empty seat earns nothing. It can never be sold again, like a concert ticket after the show.",
            "So the airline sells a few extra tickets, to fill the seats it expects to sit empty."], s_empty),
 ('2  ·  THE PARTY', ["You already do this when you throw a party.",
            "You have twenty chairs, but you invite twenty-four friends, because a few always can't make it.",
            "Airlines do the same thing, just with bigger numbers."], s_party),
 ('3  ·  THE FORECAST', ["But how do they know how many won't come?",
            "They study records of huge numbers of past flights: the route, the time of day, and how far ahead people booked.",
            "A computer model turns that into a forecast for each flight."], s_predict),
 ('4  ·  BIG NUMBERS', ["Here's the clever part. You can't tell if one person will show up.",
            "Flip one coin, and anything can happen. Flip a thousand, and you'll land close to half heads.",
            "That's the law of large numbers. The bigger the crowd, the steadier the total.",
            "So far: some passengers always miss flights. And with a full plane, how many is predictable."], s_crowd),
 ('5  ·  QUICK QUESTION', ["Quick question. Which flight would an airline overbook more?",
            "A, a Monday-morning business trip. Or B, a flight home after a long weekend.",
            "Three, two, one.",
            "A. Business travellers are more likely to be no-shows.",
            "People heading home after a long weekend are more likely to show up."], s_quiz),
 ('6  ·  WHEN EVERYONE COMES', ["But sometimes, everyone shows up.",
            "Then the airline asks for volunteers to take a later flight, usually for a travel voucher or money.",
            "In the US, the rules say volunteers must be asked first.",
            "Only if nobody agrees is someone bumped against their will. In the US and Europe, that person is usually owed compensation."], s_bump),
 ('7  ·  HOW RARE', ["So how often are people bumped against their will?",
            "In early 2024, the ten US airlines that report it bumped about 0.27 passengers in every ten thousand.",
            "That's roughly one person in thirty-seven thousand.",
            "And analysts argue overbooking helps keep fares lower, because fewer seats fly empty."], s_rare),
 ('RECAP', ["So remember three things.",
            "One. Some passengers always miss flights, and an empty seat earns nothing.",
            "Two. With a big crowd, the number of no-shows is predictable.",
            "Three. When the guess is wrong, volunteers are asked first, and being bumped against your will is rare.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story; the core answer ("some passengers never show up") lands in the first ~7 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["This plane has 180 seats.",
                 "The airline sold 185 tickets.",
                 "On purpose. Because some passengers never show up."], s_hook),
 ('PREDICTABLE', ["You can't predict one person.",
                  "But flip one coin, and anything can happen. Flip a thousand, and you land close to half heads.",
                  "Same with a full plane: the number of no-shows is steady enough to forecast."], s_crowd),
 ('IF EVERYONE COMES', ["And if everyone does show up?",
                        "The airline asks for volunteers to take a later flight, usually for a voucher or money."], s_bump),
 ('THE ANSWER', ["So airlines oversell because an empty seat earns nothing.",
                 "And in a big crowd, no-shows are predictable.",
                 "Being bumped against your will is rare: about one in thirty-seven thousand US passengers in early 2024. Follow for more."],
                card('Empty seats earn nothing', 'Big crowds are predictable', 'Bumped: about 1 in 37,000')),
]
SHORT_HITS = [(3, 0, 0.0)]
