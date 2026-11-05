"""Episode: Why the Sea Is Salty but Rivers Aren't (weathering by carbonic acid, river vs sea composition, evaporation, balance: USGS, Britannica, UW Oceanography, The Conversation)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why the Sea Is Salty but Rivers Aren't"          # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Why is the sea salty?'                           # headline on the vertical Short
HITS = [(0, 3, 0.0), (6, 0, 0.0), (7, 0, 0.0)]                 # the question, quiz answer, the twist
THUMB = ['RIVERS: FRESH', 'SEA: SALTY', 'WHY?']
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.15, (0, 1): 0.15, (0, 3): 0.5, (1, 2): 0.3, (2, 3): 0.3, (3, 3): 0.2, (4, 2): 0.3, (5, 2): 2.6, (6, 2): 0.3, (6, 5): 0.3, (7, 5): 0.3, (8, 2): 0.3, (8, 4): 0.3}
SHORT_PAUSES = {(0, 0): 0.2, (3, 1): 0.2}
CAPTION_FIXES = {'thirty-five grams': '35 grams', 'a tenth of a gram': '0.1 gram', 'three hundred': '300',
                 'four billion': '4 billion', 'eighty-five percent': '85%', 'a hundred and fifty metres': '150 metres',
                 'forty-storey': '40-storey'}

# Colour code kept in every scene (lesson of 2026-11-01):
# water blue, salts yellow, acid pink, the balance green.
WATER = CY; SALT = YE; ACID = PK; BAL = GR
LAND = (52, 58, 98); LAND2 = (74, 80, 126); SEA = (26, 96, 150); DARK = (20, 22, 38); QUIZ = (10, 82, 104)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def lerp(p, q, u): return p + (q - p) * u
def rnd(k, salt=0): return (math.sin((k + 1) * 12.9898 + salt * 78.233) * 43758.5453) % 1

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

RIV = [(560, 462), (660, 556), (780, 636), (900, 692), (1040, 742), (1160, 778), (1250, 806)]

def along(pts, u):
    u = clamp(u) * (len(pts) - 1); i = min(int(u), len(pts) - 2); f = u - i
    return lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)

def cloud(c, x, y, s, a=1.0, col=(205, 214, 240)):
    for dx, dy, r in ((-70, 8, 44), (-20, -16, 58), (40, -8, 50), (88, 12, 36)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a)
    c.rr(x - 112 * s, y + 4 * s, x + 122 * s, y + 46 * s, 20 * s, col, a)

def world(c, a=1.0, river=1.0):
    """The one map every long scene returns to: mountain, river, sea."""
    poly(c, [(1120, 806), (1920, 806), (1920, 880), (1120, 880)], SEA, a)
    c.line([(1250 + i * 34, 806 + 6 * math.sin(i * 1.1)) for i in range(21)], WATER, 6, a)
    poly(c, [(0, 880), (0, 640), (180, 520), (420, 320), (560, 430), (680, 540), (880, 660), (1120, 740), (1250, 806), (1310, 880)], LAND, a)
    poly(c, [(370, 362), (420, 320), (478, 366), (446, 386), (416, 368), (396, 384)], (200, 208, 236), a)
    if river > .01:
        c.line([along(RIV, k / 40) for k in range(int(40 * river) + 1)], WATER, 14, a)

def grains(c, t, n, a, speed=.07, r=8):
    for k in range(n):
        x, y = along(RIV, (t * speed + k / n) % 1)
        c.circ(x, y - 2, r, SALT, a)

def sea_dots(c, n, a, seed=7):
    for k in range(n):
        x = 1330 + rnd(k, seed) * 570; y = 824 + rnd(k, seed + 1) * 46
        c.circ(x, y, 6, SALT, a, bg=SEA)

def rainfall(c, t, a, col=WATER, n=16):
    for k in range(n):
        x = 240 + k * 34 % 420 + k * 7 % 40
        y = 318 + (t * 260 + k * 83) % 170
        c.line([(x, y), (x - 5, y + 24)], col, 6, a)

def kettle(c, x, y, a):
    c.rr(x - 120, y - 150, x + 120, y + 110, 40, (120, 130, 170), a)
    c.rr(x - 90, y - 180, x + 90, y - 145, 14, (90, 100, 140), a)
    c.line([(x + 120, y - 90), (x + 185, y - 90), (x + 185, y + 60), (x + 120, y + 60)], (120, 130, 170), 18, a)
    poly(c, [(x - 120, y - 110), (x - 185, y - 150), (x - 120, y - 60)], (120, 130, 170), a)
    c.rr(x - 96, y + 38, x + 96, y + 92, 14, DARK, a)
    for k in range(13):
        c.circ(x - 84 + k * 14, y + 74 - (k * 7 % 12), 10, (236, 232, 214), a, bg=DARK)

def pan(c, x, y, a, p=1.0):
    c.rr(x - 150, y - 60, x + 150, y + 40, 16, (120, 130, 170), a)
    c.line([(x + 150, y - 34), (x + 290, y - 54)], (120, 130, 170), 18, a)
    c.rr(x - 124, y - 18, x + 124, y + 22, 8, DARK, a)
    for k in range(int(16 * p)):
        c.circ(x - 112 + k * 15, y + 8 - (k * 5 % 10), 9, SALT, a, bg=DARK)

def shell(c, x, y, s, a):
    for k in range(5):
        ang = -2.5 + k * .47
        c.line([(x, y + 70 * s), (x + 110 * s * math.cos(ang), y + 40 * s + 110 * s * math.sin(ang))], INK, 8 * s, a, bg=CARD)
    pts = [(x + 118 * s * math.cos(-2.75 + k * .15), y + 40 * s + 118 * s * math.sin(-2.75 + k * .15)) for k in range(26)]
    c.line(pts, INK, 8 * s, a, bg=CARD)

# ---- scenes ----
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    u = 1 - hl(3) * .82
    world(c, u)
    cloud(c, 300, 250, 1.0, u); rainfall(c, t, u * (1 - hl(1)))
    c.text(960, 172, 'Rain is fresh', 84, WATER, hl(0) * (1 - hl(1)) * (1 - hl(3)), w='Bold')
    c.text(960, 172, 'Rivers taste fresh', 84, WATER, hl(1) * (1 - hl(2)) * (1 - hl(3)), w='Bold')
    c.text(960, 172, 'And rivers run to the sea', 84, INK, hl(2) * (1 - hl(3)), w='Bold')
    a = hl(3)
    c.text(960, 400, 'So why is', 128, INK, a, w='Bold'); c.text(960, 560, 'the sea salty?', 148, SALT, a, w='Bold')
    c.text(960, 720, 'One trip, from a mountain to the coast', 58, WATER, hl(4), w='Bold')

def s_amount(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - hl(3)
    c.text(960, 170, 'Salts in one kilo of water', 76, INK, a, w='Bold')
    for y, lab, col, grams, txt, m in ((360, 'Seawater', WATER, 35, '35 g', hl(0)), (540, 'River water', WATER, .12, '0.12 g', hl(1))):
        c.text(150, y, lab, 56, col, m * a, anchor='lm', w='Bold')
        c.rr(560, y - 46, 1640, y + 46, 18, (34, 40, 78), m * a)
        if m > .01: c.rr(560, y - 46, 560 + max(6, 1080 * grams / 35 * ease(clamp(max(T(0 if grams > 1 else 1), 0) / 1.0))), y + 46, 6, SALT, a)
        c.text(1680, y, txt, 58, SALT, m * a, anchor='lm', w='Bold')
    c.text(960, 690, 'Nearly 300 times less', 80, ACID, hl(1) * fd(T(1), 2.0) * a, w='Bold')
    c.text(960, 800, 'But not zero', 66, SALT, hl(2) * a, w='Bold')
    c.text(1880, 860, 'Bars to scale. World average river. Source: Britannica', 30, DIM, a, anchor='rm', w='Regular')
    b = hl(3)
    c.text(960, 170, 'Your kettle knows', 84, SALT, b, w='Bold')
    kettle(c, 620, 520, b)
    c.text(1330, 450, 'White crust', 84, INK, b, w='Bold')
    c.text(1330, 570, 'Minerals left by fresh water', 56, SALT, b, w='Bold')

def s_rain(c, T, t):
    hl = lambda i: hl_(T, i)
    world(c, 1, river=0)
    cloud(c, 300, 270, 1.0); cloud(c, 560, 300, .7)
    col = tuple(int(lerp(WATER[i], ACID[i], hl(2))) for i in range(3))
    rainfall(c, t, 1, col)
    c.text(960, 172, 'It starts in the sky', 80, INK, 1 - hl(1), w='Bold')
    c.text(960, 172, 'Rain is a very weak acid', 80, ACID, hl(1), w='Bold')
    c.rr(900, 250, 1830, 640, 28, CARD, hl(1), outline=(60, 70, 120), ow=3)
    c.text(1365, 330, 'Water + carbon dioxide', 58, WATER, hl(1), w='Bold', bg=CARD)
    c.text(1365, 430, 'Carbonic acid', 80, ACID, hl(2), w='Bold', bg=CARD)
    c.text(1365, 525, 'The same acid as in fizzy water', 46, INK, hl(2), w='Bold', bg=CARD)
    c.text(1365, 595, 'Natural rain: pH about 5.6', 42, DIM, hl(3), w='Medium', bg=CARD)

def s_rock(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'It eats at the rock', 80, ACID, 1 - hl(1), w='Bold')
    c.text(960, 172, 'Tiny charged pieces break free: ions', 72, SALT, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 172, 'Dissolved, like sugar in hot tea', 72, INK, hl(2), w='Bold')
    nx, ny, s = 15, 5, 96; x0 = 960 - nx * s / 2; y0 = 390
    cracks = fd(T(0), .4, 3.0)
    for j in range(ny):
        for i in range(nx):
            gone = ((i * 7 + j * 11) % 9 + j * 3) < cracks * 5 * (1 + hl(1)) and j < 2
            shade = 66 + (i * 13 + j * 29) % 26
            if not gone:
                c.rr(x0 + i * s + 4, y0 + j * s + 4, x0 + (i + 1) * s - 4, y0 + (j + 1) * s - 4, 10, (shade, shade + 6, shade + 44), 1)
    for k in range(10):
        x = x0 + 60 + k * 148; y = 250 + (t * 150 + k * 61) % 150
        c.line([(x, y), (x - 4, y + 22)], ACID, 6, 1 - hl(1) * .6)
    m = hl(1)
    for k in range(18):
        p = (t * .10 + k / 18) % 1
        x = x0 + 40 + (k * 83) % 1340 + 90 * math.sin(p * 6 + k); y = 440 - p * 170
        c.circ(x, y, 17, SALT, m * (1 - p * .3))
        c.text(x, y - 1, '+' if k % 2 else '-', 26, DARK, m, w='Bold', bg=SALT)

def s_river(c, T, t):
    hl = lambda i: hl_(T, i)
    world(c, 1)
    grains(c, t, 26, fd(T(0), .3))
    sea_dots(c, int(4 + 60 * clamp(T(1) / 9)), 1)
    c.text(960, 172, 'Downhill, all the way to the coast', 72, SALT, 1 - hl(2), w='Bold')
    c.text(1340, 300, 'Clear water,', 58, WATER, hl(1) * (1 - hl(2)), w='Bold')
    c.text(1340, 380, 'dissolved cargo', 58, SALT, hl(1) * (1 - hl(2)), w='Bold')
    m = hl(2)
    c.text(1240, 300, '4 billion tons', 112, SALT, m, w='Bold')
    c.text(1240, 410, 'of dissolved salts a year', 58, INK, m, w='Bold')
    c.text(1880, 760, 'Drawing simplified', 30, DIM, 1, anchor='rm', w='Regular')

def s_quiz(c, T, t):
    """Pattern interrupt: the frame fills with sea colour (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(560, 110, 1360, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK QUESTION', 78, SALT, 1, w='Bold', bg=DARK)
    c.text(960, 310, 'The sun lifts water off the sea. The salt?', 62, INK, hl(1), w='Bold', bg=QUIZ)
    for x, lab, txt, col in ((510, 'A', 'It rises too', ACID), (1410, 'B', 'It stays behind', WATER)):
        m = hl(2) if lab == 'A' else fd(T(2), 1.1)
        c.rr(x - 410, 400, x + 410, 800, 34, DARK, m, bg=QUIZ)
        c.text(x, 510, lab, 110, col, m, w='Bold', bg=DARK)
        c.text(x, 670, txt, 66, INK, m, w='Bold', bg=DARK)
    if T(2) > 3.4:
        q = clamp((T(2) - 3.4) / 2.4); n = 3 - int(min(q * 3, 2.9))
        c.circ(960, 600, 96, DARK, 1, bg=QUIZ); ring(c, 960, 600, 82, 1 - q, SALT, 1, 10)
        c.text(960, 600, str(n), 86, INK, 1, w='Bold', bg=DARK)

def s_trap(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - hl(3)
    if a > .01:
        c.text(960, 172, 'It stays. Only pure water rises', 76, WATER, a * (1 - hl(2)), w='Bold')
        c.text(960, 172, 'That water falls as fresh rain', 76, WATER, a * hl(2), w='Bold')
        poly(c, [(90, 620), (1000, 620), (1000, 850), (90, 850)], SEA, a)
        for k in range(26):
            c.circ(120 + rnd(k) * 850, 650 + rnd(k, 3) * 175, 10, SALT, a, bg=SEA)
        for k in range(5):
            x = 200 + k * 170; y = 560 - (t * 90 + k * 53) % 240
            c.arrow(x, y + 50, x, y - 10, WATER, 7, a * .9)
        cloud(c, 545, 310, .9, a * hl(2))
        m = hl(1) * a
        pan(c, 1400, 600, m, clamp(T(1) / 3))
        c.text(1400, 330, 'Boil a pan dry', 62, INK, m, w='Bold')
        for k in range(4):
            x = 1290 + k * 72; y = 520 - (t * 70 + k * 37) % 70
            c.line([(x, y), (x + 8, y - 26), (x, y - 52)], (190, 200, 230), 6, m * .7)
        c.text(1400, 760, 'The steam goes. The salt stays', 46, SALT, m, w='Bold')
    b = hl(3)
    if b > .01:
        c.text(960, 172, 'A pipe, and the end of the line', 76, INK, b, w='Bold')
        c.rr(120, 420, 860, 560, 40, CARD, b, outline=WATER, ow=6)
        for k in range(12):
            c.circ(150 + (t * 120 + k * 58) % 680, 490, 12, SALT, b, bg=CARD)
        c.arrow(60, 490, 118, 490, DIM, 7, b); c.arrow(866, 490, 920, 490, DIM, 7, b)
        c.text(490, 330, 'River', 70, WATER, b, w='Bold'); c.text(490, 640, 'Salts pass through', 54, SALT, b, w='Bold')
        m = hl(4)
        poly(c, [(1090, 420), (1780, 420), (1720, 800), (1150, 800)], SEA, m)

        n = int(10 + 90 * clamp(T(4) / 7))
        for k in range(n):
            c.circ(1180 + rnd(k, 5) * 510, 785 - (k / n) * 330 * rnd(k, 6), 12, SALT, m, bg=SEA)
        c.text(1435, 330, 'Sea', 70, WATER, m, w='Bold')
        c.text(1435, 850, 'Only water leaves upward', 44, SALT, m, w='Bold')
        c.text(490, 780, 'Dead Sea, Great Salt Lake:', 48, INK, hl(5), w='Bold')
        c.text(490, 845, 'no outlet, same trap', 48, SALT, hl(5), w='Bold')

def bar(c, y, segs, a, p):
    x = 300; W_ = 1460; lim = 300 + W_ * p
    for lab, v, col, ink in segs:
        w = W_ * v / 100
        if x < lim: c.rr(x + 2, y - 60, min(x + w, lim) - 2, y + 60, 8, col, a)
        if p > .95: c.text(x + w / 2, y + 92, lab, 36 if len(lab) < 18 else 32, ink, a, w='Bold')
        x += w

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - hl(3)
    c.text(960, 172, 'Different salts', 84, SALT, a, w='Bold')
    c.text(170, 340, 'Rivers', 54, WATER, hl(1) * a, w='Bold'); c.text(170, 570, 'Sea', 54, WATER, hl(2) * a, w='Bold')
    bar(c, 340, (('Bicarbonate 48%', 48, ACID, ACID), ('Calcium, sulfate, silica 33%', 33, (140, 150, 200), (180, 190, 230)), ('Others 19%', 19, (70, 78, 124), DIM)), hl(1) * a, fd(T(1), .1, 1.0))
    bar(c, 570, (('Chloride 55%', 55, SALT, SALT), ('Sodium 31%', 31, (240, 150, 60), (240, 150, 60)), ('Others 14%', 14, (70, 78, 124), DIM)), hl(2) * a, fd(T(2), .1, 1.0))
    c.text(1030, 770, 'About 85% sodium and chloride', 60, SALT, fd(T(2), 1.4) * a, w='Bold')
    c.text(1880, 860, 'By weight. Sources: Britannica; University of Washington', 30, DIM, a, anchor='rm', w='Regular')
    b = hl(3)
    c.text(960, 172, 'What leaves, and what stays', 78, INK, b, w='Bold')
    c.rr(120, 260, 900, 700, 28, CARD, b, outline=(60, 70, 120), ow=3)
    shell(c, 510, 360, .95, b)
    c.text(510, 540, 'Calcium, carbonate', 56, ACID, b, w='Bold', bg=CARD)
    c.text(510, 625, 'Into shells, then mud', 52, INK, b, w='Bold', bg=CARD)
    m = hl(4)
    c.rr(1020, 260, 1800, 700, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1410, 400, 'Sodium, chloride', 62, SALT, m, w='Bold', bg=CARD)
    c.text(1410, 500, 'Stay dissolved', 56, INK, m, w='Bold', bg=CARD)
    c.text(1410, 590, 'for millions of years', 56, INK, m, w='Bold', bg=CARD)
    c.text(960, 790, 'Also: undersea vents, and volcanoes for much of the chloride', 50, WATER, hl(5), w='Bold')

def s_balance(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - hl(3)
    c.text(960, 380, 'So is it getting saltier?', 100, INK, a * (1 - hl(1)), w='Bold')
    c.text(960, 172, 'In and out, the level holds', 84, BAL, a * hl(1), w='Bold')
    c.text(960, 530, 'For a very long time, no', 88, BAL, hl(0) * fd(T(0), 2.0) * (1 - hl(1)), w='Bold')
    m = hl(1) * a
    c.rr(300, 480, 1120, 800, 50, (120, 130, 170), m)
    c.rr(330, 500, 1090, 770, 36, SEA, m)
    c.rr(250, 390, 400, 416, 10, (190, 198, 226), m)
    c.rr(376, 400, 400, 470, 8, (190, 198, 226), m)
    for k in range(5):
        c.circ(388, 470 + (t * 150 + k * 13) % 60, 9, WATER, m)
    c.arrow(1030, 800, 1030, 868, WATER, 9, m)
    c.text(620, 620, 'Salt in', 56, SALT, m, w='Bold', bg=SEA); c.text(1210, 840, 'Salt out', 56, SALT, m, w='Bold')
    b = hl(2) * a
    c.text(1500, 420, 'Buried in sea-floor mud', 50, INK, b, w='Bold')
    c.text(1500, 520, 'Thick beds left when', 50, INK, b, w='Bold')
    c.text(1500, 585, 'shallow seas dry up', 50, INK, b, w='Bold')
    x = hl(3)
    c.text(960, 172, 'All the sea salt, spread over the land', 72, SALT, x, w='Bold')
    gy = 800; H_ = 460
    c.rr(120, gy, 1800, gy + 44, 6, LAND2, x)
    p = fd(T(3), 1.0, 1.6)
    c.rr(120, gy - H_ * p, 1800, gy, 8, mix(SALT, .86, BG), x)
    tx = x * fd(T(3), 2.0); c.rr(200, gy - 290, 1200, gy - 150, 24, DARK, tx, bg=mix(SALT, .86, BG)); c.text(700, gy - 220, 'Over 150 metres thick', 74, SALT, tx, w='Bold', bg=DARK)
    y = hl(4)
    c.rr(1340, gy - H_, 1640, gy, 8, CARD, y, bg=mix(SALT, .86, BG))
    for f in range(40):
        c.line([(1352, gy - 8 - f * (H_ - 8) / 40), (1628, gy - 8 - f * (H_ - 8) / 40)], (90, 100, 150), 3, y, CARD)
    c.text(1490, 250, '40 storeys', 60, INK, y, w='Bold')
    c.text(1880, 868, 'Drawing not to scale', 30, DIM, x, anchor='rm', w='Regular', bg=LAND2)

def s_recap(c, T, t):
    """Recap pinned onto the same map (layout change)."""
    hl = lambda i: hl_(T, i)
    world(c, .65)
    grains(c, t, 16, .7)
    cloud(c, 300, 260, .8, .6)
    pins = ((1, 110, 132, 900, '1  Rain frees minerals from rock', ACID, (430, 320)),
            (2, 590, 300, 1570, '2  Rivers bring them, the sea keeps them', WATER, (900, 690)),
            (3, 960, 520, 1860, '3  Salt in, salt out: about level', BAL, (1750, 810)))
    for ln, x0, y0, x1, txt, col, tip in pins:
        m = hl(ln)
        mid = (tip[0], y0 + 100) if ln != 1 else (430, y0 + 100)
        c.line([tip, mid], col, 5, m)
        c.circ(tip[0], tip[1], 12, col, m)
        c.rr(x0, y0, x1, y0 + 100, 22, CARD, m, outline=col, ow=4)
        c.text((x0 + x1) / 2, y0 + 50, txt, 42, col, m, w='Bold', bg=CARD)
    c.text(1370, 700, 'Short Story Long Thinking', 54, CY, hl(4), w='Bold')

def thumb_art(c):
    poly(c, [(1120, 700), (1900, 700), (1900, 1000), (1120, 1000)], SEA, 1)
    c.line([(1120 + i * 40, 700 + 10 * math.sin(i * 1.0)) for i in range(20)], WATER, 10, 1)
    cloud(c, 1490, 260, 1.9)
    for k in range(9):
        x = 1250 + k * 62; y = 430 + rnd(k) * 200
        c.circ(x, y, 26, SALT, 1)
    for k in range(34):
        c.circ(1160 + rnd(k) * 700, 760 + rnd(k, 3) * 210, 19, SALT, 1, bg=SEA)

SCENES = [
 ('THE HOOK', ["Rain is fresh.",
               "Rivers taste fresh.",
               "And rivers run to the sea.",
               "So why is the sea salty?",
               "The answer is one trip, from a mountain to the coast."], s_hook),
 ('HOW SALTY', ["Every kilo of seawater holds about thirty-five grams of salts.",
                "A kilo of river water holds about a tenth of a gram. Nearly three hundred times less.",
                "But almost none is not none.",
                "Your kettle shows it. That white crust came from minerals in ordinary fresh water. So where do they come from?"], s_amount),
 ('THE RAIN', ["They start with the sky.",
               "Falling rain picks up carbon dioxide from the air.",
               "That makes carbonic acid, the same weak acid as in fizzy water.",
               "You'd never notice it. But rock gets it, drop after drop, for millions of years."], s_rain),
 ('THE ROCK', ["Rain soaks into cracks and slowly eats at the minerals.",
               "Tiny charged pieces break free. They're called ions.",
               "They dissolve, and you can't see them, like sugar in hot tea.",
               "Now they can travel."], s_rock),
 ('THE RIVER', ["Streams carry them downhill.",
                "Rivers look clear, but they're hauling cargo.",
                "Every year, about four billion tons of dissolved salts reach the sea."], s_river),
 ('QUICK QUESTION', ["Quick question.",
                     "The sun lifts water off the sea. Does the salt go up with it?",
                     "A, it rises too. Or B, it stays behind."], s_quiz),
 ('THE TRAP', ["B. It stays. Only pure water rises.",
               "Boil a pan of salty water dry. The steam goes, the salt stays.",
               "That fresh water falls as rain, and the trip starts again.",
               "So a river is a pipe. Salts just pass through.",
               "The sea is the end of the line. Water leaves. The salts don't.",
               "Lakes with no outlet, like the Dead Sea, work the same way."], s_trap),
 ('THE TWIST', ["Here's the twist. River salts and sea salts are different.",
                "In rivers, the biggest part is bicarbonate.",
                "The sea is about eighty-five percent sodium and chloride.",
                "Why? Sea life uses calcium and carbonate for shells, and those end up in the mud.",
                "Sodium and chloride stay dissolved for millions of years.",
                "Rivers aren't the only supplier, either. Undersea vents add minerals, and much of the chloride came from volcanoes."], s_twist),
 ('THE BALANCE', ["So is the sea getting saltier? For a very long time, no.",
                  "Picture a bath with the tap on and the plug slightly out.",
                  "Salts leave too. They get buried in sea-floor mud, or left in thick beds when shallow seas dry up.",
                  "Still, that's a lot of salt. Spread over all the land, it would be more than a hundred and fifty metres thick.",
                  "About a forty-storey building."], s_balance),
 ('RECAP', ["Three things to keep.",
            "One: weak acid in rain frees minerals from rock.",
            "Two: rivers bring them, and the sea keeps them.",
            "Three: salt in and salt out stay about level.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    world(c, 1); cloud(c, 300, 250, 1.0); rainfall(c, t, 1)
    c.text(960, 172, 'Rain is fresh. Rivers taste fresh', 72, WATER, 1 - hl(1), w='Bold')
    c.text(960, 172, "Rivers aren't quite fresh", 80, SALT, hl(1), w='Bold')
    grains(c, t, 20, hl(1))

def short_acid(c, T, t):
    hl = lambda i: hl_(T, i)
    world(c, 1, river=0); cloud(c, 300, 250, 1.0); rainfall(c, t, 1, ACID)
    c.text(960, 172, 'Rain is a very weak acid', 80, ACID, 1, w='Bold')
    c.rr(900, 280, 1830, 620, 28, CARD, hl(0), outline=(60, 70, 120), ow=3)
    c.text(1365, 390, 'Over millions of years', 58, INK, hl(0), w='Bold', bg=CARD)
    c.text(1365, 500, 'It frees minerals from rock', 58, SALT, hl(1), w='Bold', bg=CARD)

def short_river(c, T, t):
    hl = lambda i: hl_(T, i)
    world(c, 1); grains(c, t, 26, 1); sea_dots(c, 40, 1)
    c.text(960, 172, 'Rivers carry them to the sea', 76, SALT, 1, w='Bold')
    c.text(1240, 320, '4 billion tons', 112, SALT, hl(0) * fd(T(0), 1.2), w='Bold')
    c.text(1240, 430, 'of dissolved salts a year', 58, INK, hl(0) * fd(T(0), 1.8), w='Bold')

def short_trap(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Only pure water rises', 80, WATER, 1 - hl(1), w='Bold')
    c.text(960, 172, 'That water falls as fresh rain', 76, WATER, hl(1), w='Bold')
    poly(c, [(160, 560), (1760, 560), (1760, 850), (160, 850)], SEA, 1)
    for k in range(44):
        c.circ(190 + rnd(k) * 1540, 590 + rnd(k, 3) * 240, 11, SALT, 1, bg=SEA)
    for k in range(8):
        x = 260 + k * 200; y = 510 - (t * 90 + k * 53) % 230
        c.arrow(x, y + 50, x, y - 10, WATER, 7, .9)
    cloud(c, 960, 320, 1.0, hl(1))

SHORT_SCENES = [
 ('THE HOOK', ["Rain is fresh. Rivers taste fresh. So why is the sea salty?",
               "Because rivers aren't quite fresh."], short_open),
 ('THE ACID', ["Rain is a very weak acid. Over millions of years, it wears away rock.",
               "That frees tiny pieces of minerals, and they dissolve in the water."], short_acid),
 ('THE RIVER', ["Rivers carry them to the sea. About four billion tons of dissolved salts, every year."], short_river),
 ('THE TRAP', ["Then the sun lifts water off the sea, but the salt stays behind.",
               "That fresh water falls as rain, and the trip starts again."], short_trap),
 ('THE ANSWER', ["Undersea vents and volcanoes added more.",
                 "So the sea is salty because salts keep arriving, and evaporation only takes the water."], card('Salts keep arriving.', 'Only water evaporates.')),
]
SHORT_HITS = [(4, 1, 0.0)]
