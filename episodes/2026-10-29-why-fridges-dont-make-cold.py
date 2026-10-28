"""Episode: Fridges Don't Make Cold (a fridge moves heat out: evaporation, compression, the refrigerant loop)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "The Heat Courier"                           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                          # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Does a fridge make cold?"                    # headline on the vertical Short
HITS = [(0, 3, 0.0), (6, 3, 0.0), (5, 0, 0.0)]             # title card, quiz answer, the heat drop-off
THUMB = ["FRIDGES", "DON'T MAKE", 'COLD']
MUSIC_LEVEL = 0.006                                         # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                              # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 2): 0.5, (2, 1): 0.4, (3, 3): 0.4, (6, 3): 0.6}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'minus twelve degrees Celsius': '−12 °C'}

HOT = (255, 140, 60); COLD = (90, 170, 255); SHELL = (200, 210, 232); CAV = (24, 46, 92); PIPE = (95, 105, 150)
SKIN = (225, 180, 150); FROST = (225, 240, 255)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    """Deterministic pseudo-random number in [0, 1)."""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerp(p, q, u): return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)
def lerpc(p, q, u): u = clamp(u); return tuple(int(p[i] + (q[i] - p[i]) * u) for i in range(3))

def heat(c, x, y, r, a=1.0, bg=BG):
    """A glowing dot of heat."""
    if a <= .01: return
    c.circ(x, y, r * 1.9, HOT, a * .22, bg=bg)
    c.circ(x, y, r, HOT, a, bg=bg)

def waves(c, x, y, h, a, t, col=HOT, n=3, bg=BG):
    """Rising wavy heat lines."""
    if a <= .01: return
    for k in range(n):
        xx = x + k * 34
        pts = [(xx + 10 * math.sin(u / 3 + t * 4 + k), y - h * u / 20) for u in range(21)]
        c.line(pts, col, 5, a * (.5 + .5 * math.sin(t * 3 + k) ** 2), bg)

def thermo(c, x, y, h, v, col, a=1.0, lab='', bg=BG):
    """Thermometer, v 0..1 fill."""
    if a <= .01: return
    c.rr(x - 16, y - h, x + 16, y, 16, (50, 58, 96), a, bg=bg)
    c.circ(x, y + 10, 30, col, a, bg=bg)
    c.rr(x - 8, y - (h - 20) * clamp(v) - 6, x + 8, y + 4, 8, col, a, bg=bg)
    if lab: c.text(x, y + 72, lab, 30, DIM, a, w='Bold', bg=bg)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def food(c, x, y, a, bg=CAV):
    """A bowl of fruit on a shelf."""
    if a <= .01: return
    c.circ(x - 34, y - 30, 26, (235, 80, 80), a, bg=bg); c.circ(x + 10, y - 38, 24, (120, 200, 90), a, bg=bg)
    c.circ(x + 44, y - 26, 22, (250, 190, 70), a, bg=bg)
    c.d.chord(((x - 80) * c.k, (y - 50) * c.k, (x + 80) * c.k, (y + 40) * c.k), 0, 180, fill=mix((240, 240, 250), a, bg))

# The fridge, seen from the side: door on the left, food inside, machinery on the back (right).
FX0, FY0, FX1, FY1 = 360, 240, 1010, 830
def fridge(c, a=1.0, door=0.0, t=0.0, cold=1.0, shelf_food=True, bg=BG):
    if a <= .01: return
    c.rr(FX0, FY0, FX1, FY1, 30, SHELL, a, bg=bg)
    cav = mix(CAV, cold, (70, 70, 80))
    c.rr(FX0 + 30, FY0 + 30, FX1 - 30, FY1 - 40, 18, cav, a, bg=SHELL)
    for y in (420, 600):
        c.line([(FX0 + 40, y), (FX1 - 40, y)], (120, 150, 200), 5, a * .8, cav)
    if shelf_food:
        food(c, 560, 600, a, cav)
        c.rr(470, 335, 560, 420, 10, (240, 240, 250), a, bg=cav); c.rr(470, 335, 560, 360, 10, (90, 150, 230), a, bg=(240, 240, 250))
        c.rr(620, 345, 720, 420, 12, (250, 230, 160), a, bg=cav)
    # door: closed = slab on the left; open = swung out towards the viewer's left
    if door < .5:
        c.rr(FX0 - 34, FY0, FX0 + 4, FY1, 14, mix(SHELL, .85, BG), a, bg=bg)
        c.rr(FX0 - 46, 380, FX0 - 30, 520, 6, (150, 160, 190), a, bg=bg)
    else:
        dp = [(FX0 - 4, FY0), (FX0 - 230, FY0 + 70), (FX0 - 230, FY1 - 70), (FX0 - 4, FY1)]
        c.d.polygon([(px * c.k, py * c.k) for px, py in dp], fill=mix(mix(SHELL, .8, BG), a, bg))
        c.line([(FX0 - 200, 420), (FX0 - 200, 560)], (150, 160, 190), 12, a, mix(SHELL, .8, BG))
    c.rr(FX0 + 30, FY1 - 30, FX1 - 30, FY1 + 24, 10, (60, 66, 90), a, bg=SHELL)

# The refrigerant loop: evaporator inside the fridge, down to the compressor, up the coils on the back,
# then through the narrow tube over the top and back inside.
def _loop():
    pts, zones = [], []
    def add(p, z): pts.append(p); zones.append(z)
    add((900, 215), 'cap'); add((900, 300), 'cap')
    for k in range(6):                                   # evaporator serpentine on the inner back wall
        y = 300 + k * 64
        add((870 if k % 2 == 0 else 955, y), 'evap'); add((955 if k % 2 == 0 else 870, y), 'evap')
    add((955, 700), 'suc'); add((955, 770), 'suc'); add((1070, 770), 'comp'); add((1150, 770), 'cond')
    for k in range(7):                                   # condenser coils on the back, going up
        y = 690 - k * 66
        add((1080 if k % 2 == 0 else 1220, y), 'cond'); add((1220 if k % 2 == 0 else 1080, y), 'cond')
    add((1080, 215), 'cap')
    add((900, 215), 'cap')
    L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + math.dist(pts[i - 1], pts[i]))
    return pts, zones, L
LP, LZ, LL = _loop()

def loop_at(u):
    """Point and zone at fraction u of the loop."""
    s = (u % 1.0) * LL[-1]
    for i in range(1, len(LP)):
        if LL[i] >= s:
            seg = LL[i] - LL[i - 1]; v = (s - LL[i - 1]) / seg if seg else 0
            return lerp(LP[i - 1], LP[i], v), LZ[i]
    return LP[-1], LZ[-1]

def zone_frac(u):
    """Where in its own zone a point sits (0..1)."""
    _, z = loop_at(u); s = (u % 1.0) * LL[-1]
    idx = [i for i in range(1, len(LP)) if LZ[i] == z]
    a = LL[idx[0] - 1]; b = LL[idx[-1]]
    return z, clamp((s - a) / max(1, b - a))

def machine(c, a=1.0, t=0.0, speed=.07, hi=None, carry=True, drop=True, pick=True, liquid=True, bg=BG):
    """Pipes, compressor, moving refrigerant dots and the heat they carry."""
    if a <= .01: return
    for i in range(1, len(LP)):
        z = LZ[i]
        w = 6 if z == 'cap' else 16
        col = PIPE
        if hi and z in hi: col = {'evap': COLD, 'cond': HOT, 'comp': HOT, 'cap': CY, 'suc': COLD}[z]
        c.line([LP[i - 1], LP[i]], mix(col, .9, BG), w, a, bg)
    # compressor
    hc = hi and 'comp' in hi
    c.rr(1030, 730, 1170, 820, 22, (70, 76, 110) if not hc else (150, 80, 50), a, bg=bg)
    c.rr(1060, 715, 1140, 735, 8, (110, 116, 150), a, bg=bg)
    for k in range(3):
        c.line([(1050 + k * 40, 760 + 4 * math.sin(t * 25 + k)), (1070 + k * 40, 760 - 4 * math.sin(t * 25 + k))], (200, 205, 230), 4, a * .7, (70, 76, 110))
    # refrigerant dots
    N = 26
    for i in range(N):
        u = (i / N + t * speed) % 1.0
        (x, y), _ = loop_at(u)
        z, f = zone_frac(u)
        if z in ('cap', 'evap', 'suc'): col = COLD
        elif z == 'comp': col = lerpc(COLD, HOT, f)
        else: col = lerpc(HOT, (240, 200, 160), f)
        r = 9 if z != 'cap' else 6
        if liquid and (z == 'cap' or (z == 'cond' and f > .6) or (z == 'evap' and f < .3)):
            c.circ(x, y, r * .8, col, a, bg=bg); c.circ(x, y - r * .7, r * .45, col, a, bg=bg)   # a liquid drop
        else:
            c.circ(x, y, r, col, a, bg=bg)
        if carry:
            on = (z == 'evap' and f > .25) or z in ('suc', 'comp') or (z == 'cond' and f < .5)
            if on: heat(c, x + 11, y - 11, 5, a, bg)
    # heat leaving the coils into the kitchen
    if drop:
        for q in range(10):
            ph = (t * .45 + q / 10) % 1.0
            heat(c, 1235 + 230 * ph, 690 - 440 * rnd(q, 2) - 60 * ph, 7, a * (1 - ph) * .95, bg)
        waves(c, 1290, 520, 140, a * .7, t, bg=bg)
    # heat moving from the food into the evaporator
    if pick:
        for q in range(7):
            ph = (t * .5 + q / 7) % 1.0
            sx, sy = (560, 560) if q % 2 else (670, 380)
            heat(c, sx + (860 - sx) * ph, sy + (330 + 50 * q - sy) * ph, 6, a * math.sin(math.pi * ph), CAV)

def hand(c, x, y, a, bg=BG):
    """A flat hand seen side-on, palm facing left."""
    if a <= .01: return
    c.rr(x + 20, y + 60, x + 90, y + 200, 24, SKIN, a, bg=bg)          # wrist
    c.rr(x, y - 40, x + 110, y + 90, 34, SKIN, a, bg=bg)               # palm
    for k in range(4):
        c.rr(x + 4 + k * 27, y - 130 + abs(k - 1.5) * 14, x + 26 + k * 27, y - 20, 11, SKIN, a, bg=bg)
    c.rr(x - 50, y - 10, x + 20, y + 22, 14, SKIN, a, bg=bg)           # thumb

def pump(c, x, y, p, a=1.0, t=0.0, bg=BG):
    """Bike pump cut open: piston at fraction p (0 = up, 1 = squeezed). Barrel warms as p rises."""
    if a <= .01: return
    top, bot = y - 260, y + 160
    py = top + 40 + (bot - top - 120) * p
    c.rr(x - 90, top, x + 90, bot, 20, lerpc((70, 80, 120), (200, 100, 60), p), a, bg=bg)
    inner = (20, 26, 52)
    c.rr(x - 70, top + 10, x + 70, bot - 10, 14, inner, a, bg=bg)
    c.rr(x - 66, py - 14, x + 66, py + 14, 6, (170, 175, 200), a, bg=inner)
    c.rr(x - 10, top - 120, x + 10, py, 4, (170, 175, 200), a, bg=bg)
    c.rr(x - 90, top - 140, x + 90, top - 110, 14, (90, 96, 130), a, bg=bg)
    h = (bot - 10) - (py + 14)
    for i in range(16):
        gx = x - 55 + 110 * rnd(i, 4) + 4 * math.sin(t * 9 + i)
        gy = py + 24 + (h - 30) * rnd(i, 8) + 4 * math.cos(t * 9 + i)
        c.circ(gx, gy, 8, lerpc(CY, HOT, p), a, bg=inner)
    c.line([(x + 90, bot - 30), (x + 200, bot - 30), (x + 200, bot + 40)], (90, 96, 130), 12, a, bg)

def house(c, x, y, a, t, bg=BG):
    """House with an air conditioner: cold indoors, hot unit outside."""
    if a <= .01: return
    c.d.polygon([((x - 300) * c.k, (y - 150) * c.k), (x * c.k, (y - 330) * c.k), ((x + 300) * c.k, (y - 150) * c.k)], fill=mix((120, 80, 70), a, bg))
    c.rr(x - 260, y - 150, x + 260, y + 200, 10, (40, 70, 120), a, bg=bg)
    c.rr(x - 200, y - 110, x + 30, y - 50, 10, (220, 225, 240), a, bg=(40, 70, 120))
    for k in range(4):
        c.line([(x - 180 + k * 10, y - 40 + 20 * ((t * .6 + k * .25) % 1)), (x - 120 + k * 10, y - 40 + 20 * ((t * .6 + k * .25) % 1))], COLD, 4, a, (40, 70, 120))
    c.text(x - 80, y + 70, 'cool inside', 32, COLD, a, w='Bold', bg=(40, 70, 120))
    c.rr(x + 310, y + 50, x + 470, y + 200, 14, (110, 116, 150), a, bg=bg)
    c.circ(x + 390, y + 125, 52, (60, 66, 100), a, bg=(110, 116, 150))
    for k in range(3):
        ang = t * 8 + k * 2.1
        c.line([(x + 390, y + 125), (x + 390 + 44 * math.cos(ang), y + 125 + 44 * math.sin(ang))], (180, 186, 210), 8, a, (60, 66, 100))
    for q in range(6):
        ph = (t * .5 + q / 6) % 1.0
        heat(c, x + 480 + 160 * ph, y + 70 + 110 * rnd(q, 9) - 40 * ph, 7, a * (1 - ph), bg)
    c.line([(x + 260, y - 80), (x + 390, y - 80), (x + 390, y + 50)], PIPE, 10, a, bg)

def thumb_art(c):
    """Simple fridge in the right third, with heat pouring out of its back."""
    c.rr(1180, 220, 1560, 860, 30, SHELL)
    c.rr(1210, 250, 1530, 820, 18, CAV, bg=SHELL)
    c.line([(1220, 480), (1520, 480)], (120, 150, 200), 5, 1, CAV)
    food(c, 1370, 680, 1.0)
    for k in range(6):
        y = 300 + k * 85
        c.line([(1575, y), (1640, y), (1640, y + 42), (1575, y + 42)], HOT, 12)
    waves(c, 1680, 760, 520, 1.0, .4)
    for q in range(9):
        heat(c, 1720 + 110 * rnd(q, 5), 260 + 560 * rnd(q, 7), 14, 1.0)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Feel the air behind your fridge', 70, INK, a * (1 - hl(1)) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'That heat came out of your food', 66, HOT, a * hl(1) * (1 - hl(2)), w='Bold')
        k0 = a * (1 - hl(2))
        if k0 > 0:
            # the fridge is on screen from frame one, with warm air rising behind it
            fridge(c, k0, t=t)
            waves(c, 1080, 760, 420, k0, t)
            hand(c, 1330, 500, k0)
            c.text(1560, 380, 'warm!', 64, HOT, k0, w='Bold')
            if hl(1) > 0:
                for q in range(9):
                    ph = (t * .6 + q / 9) % 1.0
                    sx, sy = (560, 560) if q % 2 else (670, 380)
                    x = sx + (1250 - sx) * ph; y = sy + (300 + 50 * (q % 6) - sy) * ph
                    heat(c, x, y, 9, k0 * hl(1) * math.sin(math.pi * ph), CAV if x < FX1 - 30 else BG)
        k2 = a * hl(2)
        if k2 > 0:
            c.text(960, 150, "A fridge doesn't make cold", 70, INK, k2, w='Bold')
            for j, (lab, x, ok) in enumerate((('makes cold', 560, False), ('moves heat out', 1360, True))):
                kk = k2 * fd(T(2), .2 + j * 1.2)
                c.rr(x - 330, 290, x + 330, 740, 34, CARD, kk, outline=GR if ok else PK, ow=4)
                if ok:
                    c.rr(x - 220, 380, x - 20, 640, 20, CAV, kk, bg=CARD)
                    for q in range(4):
                        ph = (t * .6 + q / 4) % 1.0
                        heat(c, x - 120 + 300 * ph, 510 + 40 * math.sin(q * 2), 10, kk * math.sin(math.pi * ph), CARD)
                    c.check(x + 230, 350, 46, GR, kk, fd(T(2), 1.6))
                else:
                    for k in range(6):
                        ang = k * math.pi / 3
                        c.line([(x, 500), (x + 110 * math.cos(ang), 500 + 110 * math.sin(ang))], COLD, 10, kk, CARD)
                    c.cross(x + 230, 350, 70, PK, kk * fd(T(2), .9))
                c.text(x, 690, lab, 44, GR if ok else PK, kk, w='Bold', bg=CARD)
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 340 + 30 * (1 - m), "Fridges Don't Make Cold", 112, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'They Move Heat Out', 108, HOT, m, w='Bold')
        c.line([(960 - 320 * m, 590), (960 + 320 * m, 590)], CY, 8, m)

def s_heat(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Cold = heat taken away', 70, COLD, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Heat flows by itself from warm to cool', 62, HOT, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A fridge pushes heat the wrong way', 64, YE, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j, (lab, x, n, v, col) in enumerate((('warm', 600, 22, .8, HOT), ('cold', 1320, 5, .2, COLD))):
            kk = k0 * fd(T(0), .3 + j * 1.2)
            c.rr(x - 260, 290, x + 160, 720, 30, CARD, kk, outline=col, ow=4)
            for i in range(n):
                heat(c, x - 220 + 340 * rnd(i, j + 3) + 5 * math.sin(t * 5 + i), 330 + 340 * rnd(i, j + 7) + 5 * math.cos(t * 4 + i), 9, kk, CARD)
            thermo(c, x + 240, 640, 300, v, col, kk)
            c.text(x - 50, 780, lab + (': lots of heat' if j == 0 else ': little heat'), 38, col, kk, w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        # a hot mug cooling down
        x, y = 700, 560
        c.rr(x - 120, y - 140, x + 120, y + 110, 26, (230, 230, 240), k1)
        c.rr(x + 110, y - 90, x + 180, y + 40, 30, None, k1, outline=(230, 230, 240), ow=18)
        c.rr(x - 100, y - 130, x + 100, y - 100, 10, (120, 70, 40), k1, bg=(230, 230, 240))
        waves(c, x - 40, y - 170, 120, k1, t, col=(200, 205, 230))
        for q in range(8):
            ph = (t * .5 + q / 8) % 1.0
            ang = -2.6 + q * .7
            heat(c, x + (90 + 260 * ph) * math.cos(ang), y - 40 + (90 + 220 * ph) * math.sin(ang) * .8, 8, k1 * (1 - ph))
        c.rr(1180, 300, 1760, 470, 28, CARD, k1 * fd(T(1), .8), outline=GR, ow=3)
        c.text(1300, 385, 'warm', 46, HOT, k1 * fd(T(1), .8), w='Bold', bg=CARD); c.text(1550, 385, 'cool', 46, COLD, k1 * fd(T(1), .8), w='Bold', bg=CARD)
        c.arrow(1375, 385, 1470, 385, INK, 6, k1 * fd(T(1), .8), 16)
        c.check(1680, 385, 40, GR, k1 * fd(T(1), .8), fd(T(1), 1.2))
        c.rr(1180, 520, 1760, 690, 28, CARD, k1 * fd(T(1), 2.4), outline=PK, ow=3)
        c.text(1300, 585, 'cool', 46, COLD, k1 * fd(T(1), 2.4), w='Bold', bg=CARD); c.text(1570, 585, 'warm', 46, HOT, k1 * fd(T(1), 2.4), w='Bold', bg=CARD)
        c.arrow(1365, 585, 1470, 585, INK, 6, k1 * fd(T(1), 2.4), 16)
        c.text(1440, 640, 'never by itself', 30, PK, k1 * fd(T(1), 2.4), w='Bold', bg=CARD)
    k2 = hl(2)
    if k2 > 0:
        # uphill: cold box at the bottom, warm kitchen at the top; heat has to be pushed up
        c.line([(300, 760), (1600, 330)], (70, 80, 130), 10, k2)
        c.rr(180, 640, 420, 820, 22, CAV, k2, outline=COLD, ow=4)
        c.text(300, 860, 'cold box', 36, COLD, k2, w='Bold')
        c.rr(1500, 220, 1760, 400, 22, (90, 50, 40), k2, outline=HOT, ow=4)
        c.text(1630, 440, 'warm kitchen', 36, HOT, k2, w='Bold')
        u = clamp(T(2) / 4.0) * .62 + .1
        hx, hy = 300 + 1300 * u, 760 - 430 * u
        heat(c, hx, hy - 40, 22, k2)
        c.rr(hx - 120, hy - 70, hx - 50, hy - 10, 12, (110, 116, 150), k2)
        c.arrow(hx - 50, hy - 40, hx - 25, hy - 40, INK, 6, k2, 14)
        c.text(960, 720, 'that takes energy', 44, YE, k2 * fd(T(2), 2.4), w='Bold')

def s_courier(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The refrigerant: a fluid in a loop of pipes', 60, CY, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'A courier: picks heat up inside, drops it outside', 56, YE, hl(1), w='Bold')
    k = hl(0)
    if k <= 0: return
    fridge(c, k, t=t)
    on = hl(1)
    machine(c, k, t=t, carry=on > .5, drop=on > .5, pick=on > .5, liquid=False)
    c.rr(1380, 300, 1840, 520, 30, CARD, k * fd(T(0), 1.2), outline=CY, ow=3)
    c.text(1610, 370, 'round and round', 40, CY, k * fd(T(0), 1.2), w='Bold', bg=CARD)
    c.text(1610, 440, 'the same fluid, forever', 32, DIM, k * fd(T(0), 1.8), w='Medium', bg=CARD)
    if on > 0:
        c.text(690, 740, 'PICK UP', 40, COLD, on * fd(T(1), .8), w='Bold', bg=CAV)
        c.text(1610, 640, 'DROP OFF', 48, HOT, on * fd(T(1), 2.2), w='Bold')
        c.arrow(1450, 640, 1300, 560, HOT, 6, on * fd(T(1), 2.2), 18)

def s_evap(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Trick one: evaporating takes heat', 66, COLD, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Out of the shower: why you feel cold', 62, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Isobutane boils at about −12 °C', 66, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Inside the fridge, it boils and soaks up heat', 58, COLD, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(2))
    if k0 > 0:
        # a stretch of wet skin; drops rise off as vapour, each carrying a heat dot away
        c.rr(260, 600, 1260, 760, 40, SKIN, k0)
        c.text(760, 690, 'skin', 40, (150, 100, 80), k0, w='Bold', bg=SKIN)
        for q in range(9):
            x = 330 + q * 110
            ph = (t * .35 + rnd(q, 1)) % 1.0
            c.circ(x, 585, 16, CY, k0 * (1 - ph * .6))
            y = 560 - 320 * ph
            c.circ(x + 12 * math.sin(t * 3 + q), y, 10 * (1 - ph * .5), (170, 200, 240), k0 * (1 - ph) * .7)
            heat(c, x + 12 * math.sin(t * 3 + q) + 16, y - 14, 6, k0 * (1 - ph))
        c.text(760, 260, 'water evaporating', 36, CY, k0 * fd(T(0), .6), w='Bold')
        k1 = hl(1) * (1 - hl(2))
        thermo(c, 1500, 680, 380, .7 - .35 * fd(T(1), 1.0, 2.0), lerpc(HOT, COLD, fd(T(1), 1.0, 2.0)), max(k0 * fd(T(0), 1.2), 0))
        c.text(1500, 820, 'your skin cools', 36, COLD, k1 * fd(T(1), 2.0), w='Bold')
        c.text(1500, 250, 'takes your heat', 36, HOT, k0 * fd(T(0), 1.6), w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        c.line([(400, 760), (1520, 760)], (70, 80, 130), 6, k2)
        for j, (lab, v, x, col) in enumerate((('water boils', 100, 640, CY), ('isobutane boils', -12, 1280, YE))):
            kk = k2 * fd(T(2), .3 + j * 1.2)
            yy = 680 - (v + 20) * 3.2
            c.circ(x, yy, 18, col, kk)
            c.line([(x, yy + 20), (x, 760)], col, 5, kk * .7)
            c.text(x, yy - 60, f'{v} °C'.replace('-', '−'), 56, col, kk, w='Bold')
            c.text(x, 820, lab, 38, col, kk, w='Bold')
        c.text(960, 620, 'at normal air pressure', 32, DIM, k2 * fd(T(2), 2.4), w='Medium')
    k3 = hl(3)
    if k3 > 0:
        fridge(c, k3, t=t)
        machine(c, k3, t=t, hi={'evap'}, drop=False)
        for q in range(6):
            bx = 880 + 70 * rnd(q, 6); by = 640 - ((t * 60 + q * 70) % 340)
            c.circ(bx, by, 7, (180, 220, 255), k3 * .8, bg=CAV)
        c.rr(1300, 330, 1840, 560, 30, CARD, k3 * fd(T(3), .8), outline=COLD, ow=3)
        c.text(1570, 400, 'boiling refrigerant', 38, COLD, k3 * fd(T(3), .8), w='Bold', bg=CARD)
        c.text(1570, 470, 'soaks up heat', 38, INK, k3 * fd(T(3), 1.4), w='Bold', bg=CARD)
        c.text(1570, 515, 'from your food', 30, DIM, k3 * fd(T(3), 1.4), w='Medium', bg=CARD)

def s_squeeze(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Trick two: squeeze a gas, it heats up', 64, HOT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Pump a bike tyre: the pump gets warm', 62, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'The compressor: hotter than your kitchen', 60, HOT, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(2))
    if k0 > 0:
        p = .5 + .5 * math.sin(t * 2.2 - 1.6) if hl(1) > 0 else fd(T(0), .6, 2.2)
        pump(c, 760, 640, p, k0, t)
        c.text(1000, 600, 'squeezed', 38, HOT, k0 * fd(T(0), 1.6), 'lm', 'Bold')
        c.text(1000, 650, 'gas', 38, HOT, k0 * fd(T(0), 1.6), 'lm', 'Bold')
        kk = k0 * hl(1)
        if kk > 0:
            waves(c, 560, 600, 140, kk, t)
            thermo(c, 1450, 680, 380, .35 + .4 * fd(T(1), .6, 1.6), lerpc(CY, HOT, fd(T(1), .6, 1.6)), kk, 'pump barrel')
    k2 = hl(2)
    if k2 > 0:
        fridge(c, k2, t=t)
        machine(c, k2, t=t, hi={'comp'}, drop=False, pick=False)
        c.arrow(1250, 820, 1180, 790, HOT, 6, k2 * fd(T(2), .6), 18)
        c.text(1270, 840, 'compressor', 36, HOT, k2 * fd(T(2), .6), 'lm', 'Bold')
        thermo(c, 1520, 650, 340, .9, HOT, k2 * fd(T(2), 1.6), 'refrigerant')
        thermo(c, 1740, 650, 340, .55, (200, 170, 140), k2 * fd(T(2), 2.2), 'kitchen')
        c.text(1630, 230, 'hotter', 40, HOT, k2 * fd(T(2), 2.8), w='Bold')

def s_dump(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The coils on the back: heat flows out', 62, HOT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Cooled down, it turns back into a liquid', 60, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A narrow tube: pressure drops, very cold', 60, CY, hl(2), w='Bold')
    k = hl(0)
    if k <= 0: return
    fridge(c, k, t=t)
    hi = {'cap'} if hl(2) > .5 else {'cond'}
    machine(c, k, t=t, hi=hi, pick=hl(2) > .5, liquid=hl(1) > .5)
    k0 = hl(0) * (1 - hl(1))
    c.rr(1480, 330, 1860, 560, 30, CARD, k0 * fd(T(0), 1.2), outline=HOT, ow=3)
    c.text(1580, 400, 'hot', 40, HOT, k0 * fd(T(0), 1.2), w='Bold', bg=CARD); c.text(1780, 400, 'cooler', 40, INK, k0 * fd(T(0), 1.2), w='Bold', bg=CARD)
    c.arrow(1625, 400, 1695, 400, INK, 5, k0 * fd(T(0), 1.2), 14)
    c.text(1670, 470, 'the normal way', 32, DIM, k0 * fd(T(0), 1.8), w='Medium', bg=CARD)
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.rr(1480, 330, 1860, 560, 30, CARD, k1, outline=INK, ow=3)
        c.circ(1580, 445, 26, (240, 200, 160), k1, bg=CARD); c.text(1660, 445, 'gas', 34, INK, k1, 'lm', 'Bold', bg=CARD)
        c.arrow(1580, 490, 1580, 520, DIM, 4, k1, 10)
        c.text(1670, 530, 'liquid', 34, CY, k1 * fd(T(1), .8), w='Bold', bg=CARD)
    k2 = hl(2)
    if k2 > 0:
        c.arrow(1290, 250, 1110, 222, CY, 6, k2 * fd(T(2), .6), 18)
        c.text(1300, 250, 'narrow tube', 34, CY, k2 * fd(T(2), .6), 'lm', 'Bold')
        c.rr(1480, 330, 1860, 600, 30, CARD, k2 * fd(T(2), 1.2), outline=CY, ow=3)
        c.text(1670, 400, 'pressure drops', 38, CY, k2 * fd(T(2), 1.2), w='Bold', bg=CARD)
        c.text(1670, 460, 'very cold', 38, COLD, k2 * fd(T(2), 2.0), w='Bold', bg=CARD)
        c.text(1670, 540, 'back inside for more', 30, DIM, k2 * fd(T(2), 3.0), w='Medium', bg=CARD)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 208, 'Hot day, fridge door left open. Does the kitchen get cooler?', 38, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'B: warmer', 70, HOT, ans, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        fridge(c, k0, door=1.0, t=t)
        for q in range(4):
            c.line([(FX0 - 40 - 60 * q, 600 + 30 * q), (FX0 - 110 - 60 * q, 630 + 30 * q)], COLD, 6, k0 * (.5 + .5 * math.sin(t * 3 + q) ** 2))
        c.text(1500, 400, 'a hot day', 44, HOT, k0 * fd(T(0), 1.0), w='Bold')
        c.circ(1500, 560, 70, YE, k0 * fd(T(0), 1.0))
    kc = hl(1) * (1 - ans)
    if kc > 0:
        for j, (lab, x, col) in enumerate((('A', 560, COLD), ('B', 1360, HOT))):
            kk = kc * (.3 + .7 * fd(T(1), j * 1.2))
            c.rr(x - 330, 290, x + 330, 720, 34, CARD, kk, outline=CY, ow=3)
            c.circ(x - 270, 340, 38, CY, kk, bg=CARD); c.text(x - 270, 340, lab, 44, BG, kk, w='Bold', bg=CY)
            thermo(c, x, 600, 230, .25 if j == 0 else .8, col, kk, bg=CARD)
            c.text(x, 670, 'cooler' if j == 0 else 'warmer', 44, col, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        ring(c, 960, 500, 70, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        fridge(c, ans, door=1.0, t=t)
        machine(c, ans, t=t, pick=False, liquid=False)
        # heat goes round in a circle: front of the room -> into the fridge -> out the back -> back to the front
        cx, cy = 800, 545
        pts = [(cx + 640 * math.cos(u / 40 * 2 * math.pi * fd(T(3), .4, 1.6)), cy + 300 * math.sin(u / 40 * 2 * math.pi * fd(T(3), .4, 1.6))) for u in range(41)]
        c.line(pts, YE, 6, ans * .8)
        c.text(1660, 420, '+ the motor\'s', 36, HOT, ans * fd(T(3), 3.0), w='Bold')
        c.text(1660, 470, 'own heat', 36, HOT, ans * fd(T(3), 3.0), w='Bold')
        heat(c, 1100, 775, 14, ans * fd(T(3), 3.0))

def s_back(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The warm back = heat from food + motor', 60, HOT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'An air conditioner: the same trick', 64, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Thick frost gets in the way', 66, FROST, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        # stacked bar (not to scale)
        x0 = 420
        c.rr(x0, 300, x0 + 520, 420, 18, COLD, k0 * fd(T(0), .3))
        c.text(x0 + 260, 360, 'heat from your food', 38, BG, k0 * fd(T(0), .3), w='Bold', bg=COLD)
        c.text(x0 + 600, 360, '+', 70, INK, k0 * fd(T(0), 1.4), w='Bold')
        c.rr(x0 + 680, 300, x0 + 1140, 420, 18, YE, k0 * fd(T(0), 1.4))
        c.text(x0 + 910, 360, "the motor's energy", 36, BG, k0 * fd(T(0), 1.4), w='Bold', bg=YE)
        c.text(990, 480, '=', 70, INK, k0 * fd(T(0), 2.4), w='Bold')
        c.rr(x0, 540, x0 + 1140, 660, 18, HOT, k0 * fd(T(0), 2.4))
        c.text(990, 600, 'heat out the back', 44, BG, k0 * fd(T(0), 2.4), w='Bold', bg=HOT)
        c.text(960, 720, 'the motor uses most of the electricity', 38, YE, k0 * fd(T(0), 4.0), w='Bold')
        c.text(1640, 820, 'not to scale', 28, DIM, k0 * fd(T(0), 2.4), w='Medium')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        house(c, 760, 560, k1, t)
        c.text(1500, 330, 'heat dumped', 40, HOT, k1 * fd(T(1), 1.4), w='Bold')
        c.text(1500, 380, 'outside', 40, HOT, k1 * fd(T(1), 1.4), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, x, fr) in enumerate((('clean pipe', 560, 0.0), ('thick frost', 1360, 1.0))):
            kk = k2 * fd(T(2), j * 1.0)
            c.rr(x - 330, 280, x + 330, 760, 34, CARD, kk, outline=COLD if j == 0 else FROST, ow=3)
            if fr: c.rr(x - 240, 470, x + 240, 590, 50, FROST, kk, bg=CARD)
            c.rr(x - 220, 500, x + 220, 560, 30, COLD, kk, bg=FROST if fr else CARD)
            for q in range(5):
                ph = (t * .6 + q / 5) % 1.0
                hx = x - 200 + 90 * q
                if not fr:
                    heat(c, hx, 330 + 160 * ph, 9, kk * (1 - ph * .8), CARD)
                else:
                    yy = 330 + 120 * (1 - abs(1 - 2 * ph))
                    heat(c, hx, yy, 9, kk, CARD)
            c.text(x, 690, lab, 40, COLD if j == 0 else FROST, kk, w='Bold', bg=CARD)
            if j == 0: c.check(x + 240, 330, 40, GR, kk, fd(T(2), .8))
        c.text(960, 820, 'a frosted-up fridge works less well', 34, DIM, k2 * fd(T(2), 2.0), w='Medium')

RECAPS = [('1', 'Not cold', 'a fridge moves', 'heat out', HOT),
          ('2', 'Two tricks', 'evaporating takes heat,', 'squeezing adds heat', CY),
          ('3', 'The warm back', 'is the heat', 'from your food', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 160, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, l1, l2, l3, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; dy = 40 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        c.rr(x - 250, 290 + dy, x + 250, 760 + dy, 36, CARD, m, outline=col, ow=4)
        c.circ(x, 370 + dy, 46, col, m, bg=CARD); c.text(x, 370 + dy, nn, 52, BG, m, w='Bold', bg=col)
        c.text(x, 490 + dy, l1, 52, col, m, w='Bold', bg=CARD)
        c.text(x, 580 + dy, l2, 36, INK, m, w='Bold', bg=CARD)
        c.text(x, 630 + dy, l3, 36, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Feel the air behind your fridge. It's warm.",
            "That warmth came out of your food.",
            "Because a fridge doesn't make cold. It moves heat out.",
            "Here's how."], s_hook),
 ('1  ·  WHAT COLD IS', ["Cold isn't something you can add. It's what's left when heat is taken away.",
            "And by itself, heat only flows from warm to cooler. A hot drink cools down. It never heats up on its own.",
            "So a fridge has to push heat the wrong way, out of a cold box and into a warmer kitchen. That takes energy."], s_heat),
 ('2  ·  THE COURIER', ["It uses a fluid that travels round a loop of pipes, called the refrigerant.",
            "Think of it as a courier. It picks up heat inside the fridge, and drops it off outside. Over and over."], s_courier),
 ('3  ·  TRICK ONE', ["Trick one. When a liquid evaporates, it takes heat with it.",
            "You've felt this. Step out of a shower and you feel cold, because the water drying off your skin takes your heat.",
            "Many home fridges use a refrigerant called isobutane. At normal air pressure, it boils at about minus twelve degrees Celsius.",
            "So in the pipes inside your fridge, it boils easily, and soaks up heat from your food."], s_evap),
 ('4  ·  TRICK TWO', ["Trick two. Squeeze a gas, and it heats up.",
            "Pump up a bike tyre, and the pump gets warm.",
            "In a fridge, a motor called the compressor squeezes the refrigerant until it's hotter than your kitchen."], s_squeeze),
 ('5  ·  THE DROP-OFF', ["Now the hot refrigerant flows through the coils on the back. Heat flows out into the room, the normal way.",
            "As it gives up its heat, it turns back into a liquid.",
            "Then it squeezes through a very narrow tube. Its pressure drops, it gets very cold, and it heads back inside for more heat."], s_dump),
 ('6  ·  QUICK QUESTION', ["Quick question. On a hot day, you leave the fridge door open. Does your kitchen get cooler, or warmer?",
            "A: cooler. Or B: warmer.",
            "Three, two, one.",
            "B. Warmer. The fridge just moves heat from its front to its back, in a circle. And its motor adds heat of its own."], s_quiz),
 ('7  ·  THE WARM BACK', ["So the warmth behind your fridge is the heat from your food, plus the energy the motor used. That motor uses most of the fridge's electricity.",
            "An air conditioner works almost the same way. It takes heat from inside your home, and dumps it outside.",
            "One more thing. Thick frost on the cold pipes blocks heat from moving, so a frosted-up fridge works less well."], s_back),
 ('RECAP', ["So remember three things.",
            "One. A fridge doesn't make cold. It moves heat out.",
            "Two. Evaporating takes heat in. Squeezing a gas makes it hot.",
            "Three. The warm back of your fridge is the heat from your food.",
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
    if T(1) < 0: remap(s_hook, {2: 0})(c, T, t)
    else: remap(s_hook, {0: 1, 1: (1, 0.0)})(c, T, t)

def short_drop(c, T, t):
    if T(1) < 0: remap(s_squeeze, {2: 0})(c, T, t)
    else: remap(s_dump, {0: 1})(c, T, t)

# The Short: its own complete mini-story (hook -> evaporating picks heat up -> squeezing drops it off -> answer).
SHORT_SCENES = [
 ('THE HOOK', ["Does a fridge make cold? No. A fridge can't make cold. It moves heat out of your food, and dumps it behind the fridge.",
               "Here's how it does it."],
              short_hook),
 ('PICK UP', ["A fluid runs round and round a loop of pipes. Inside the fridge, it evaporates.",
              "And evaporating soaks up heat, the same way water drying off your skin after a shower makes you feel cold."],
             remap(s_evap, {3: 0})),
 ('DROP OFF', ["Then a motor squeezes it, and squeezing a gas makes it hot. Hotter than your kitchen.",
               "So in the coils on the back, the heat flows out into the room."],
              short_drop),
 ('THE ANSWER', ["So that warm air you feel behind your fridge?",
                 "It's the heat that came out of your food."],
                card('The warm back of your fridge?', 'Heat from your food.')),
]
SHORT_HITS = [(3, 1, 0.0)]
