"""Episode: There's No Heat in Chilli. So What Burns? (capsaicin opens the TRPV1 heat sensor; menthol and TRPM8; why milk beats water)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Chilli Burns'                            # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Why does chilli burn?'                        # headline on the vertical Short
HITS = [(0, 2, 0.0), (2, 1, 0.0), (6, 1, 0.0)]              # the trick, the gate pops open, the milk answer
THUMB = ['NO HEAT.', 'STILL BURNS.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 2): 0.3, (1, 3): 0.3, (2, 1): 0.4, (5, 0): 3.2, (6, 3): 0.2, (8, 3): 0.2}
SHORT_PAUSES = {(0, 1): 0.2, (4, 0): 0.3}
CAPTION_FIXES = {'T R P V 1': 'TRPV1', 'T R P M 8': 'TRPM8', 'forty-three degrees Celsius': '43 °C',
                 'nineteen ninety-seven': '1997', 'twenty twenty-one': '2021', 'twenty nineteen': '2019'}

# Colour code kept in every scene (lesson of 2026-11-01):
# capsaicin and the burn are red, the heat gate (TRPV1) is yellow, nerve signals and the brain are purple,
# cold and water are blue, menthol, milk and the answer are green.
RED = (255, 88, 64); GATE = YE; NERVE = PU; COLD = CY; ANS = GR
DARK = (20, 22, 38); MEM = (70, 80, 140); QUIZ = (64, 30, 44); MILK = (236, 238, 248)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

# On-screen headlines are 3 to 5 words with the one key word in colour
# (lesson of 2026-11-13, Bytecap: most mobile viewers watch muted; keep on-screen text to 3-5 words, key word coloured).
def headline(c, parts, a, size=92, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def chilli(c, x, y, s, a, ang=0.0, bg=BG):
    """A chilli lying on its side, stem at (x, y), tip to the right and curling down."""
    if a <= .01: return
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda px, py: (x + px * ca - py * sa, y + px * sa + py * ca)
    L = 330 * s; n = 30
    cen = [(L * u, 80 * s * math.sin(u * math.pi * .75) ** 1.4) for u in [k / n for k in range(n + 1)]]
    top, bot = [], []
    for k in range(n + 1):
        u = k / n; px, py = cen[k]; qx, qy = cen[min(n, k + 1)] if k < n else cen[k]
        if k == n: qx, qy = cen[k]; px0, py0 = cen[k - 1]; dx, dy = px - px0, py - py0
        else: dx, dy = qx - px, qy - py
        Ln = math.hypot(dx, dy) or 1; nx, ny = -dy / Ln, dx / Ln
        w = 56 * s * (1 - u ** 1.8) + 3 * s
        top.append(P(px + nx * w, py + ny * w)); bot.append(P(px - nx * w, py - ny * w))
    poly(c, top + bot[::-1], RED, a, bg)
    c.line([P(cen[k][0], cen[k][1] - 30 * s * (1 - (k / n) ** 1.8)) for k in range(3, 18)], (255, 160, 140), 7 * s, a * .8, bg=RED)
    c.rr(*P(-30 * s, -40 * s), *P(8 * s, 40 * s), 14 * s, (70, 170, 90), a, bg=bg)
    c.line([P(-20 * s, 0), P(-60 * s, -20 * s), P(-80 * s, -60 * s)], (70, 170, 90), 12 * s, a, bg=bg)

def thermo(c, x, y, h, lev, col, a, bg=BG, label=None, lcol=DIM):
    """Thermometer standing on (x, y); lev 0..1."""
    if a <= .01: return
    c.rr(x - 18, y - h, x + 18, y + 4, 18, DARK, a, outline=(110, 120, 170), ow=4, bg=bg)
    c.rr(x - 8, y - max(20, h * lev), x + 8, y + 4, 8, col, a, bg=DARK)
    c.circ(x, y + 22, 32, col, a, outline=(110, 120, 170), ow=4, bg=bg)
    for k in range(5): c.line([(x + 22, y - h * (k + 1) / 6), (x + 36, y - h * (k + 1) / 6)], (110, 120, 170), 3, a, bg=bg)
    if label: c.text(x, y + 84, label, 30, lcol, a, w='Bold', bg=bg)

def flame(c, x, y, s, a, t=0.0, bg=BG):
    if a <= .01: return
    f = 1 + .08 * math.sin(t * 9 + x)
    o = [(x, y - 70 * s * f), (x + 26 * s, y - 24 * s), (x + 34 * s, y + 10 * s), (x + 20 * s, y + 34 * s), (x, y + 40 * s),
         (x - 20 * s, y + 34 * s), (x - 34 * s, y + 10 * s), (x - 26 * s, y - 24 * s)]
    poly(c, o, RED, a, bg)
    poly(c, [(px * .55 + x * .45, py * .55 + (y + 16 * s) * .45) for px, py in o], YE, a, RED)

def mouth(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 200 * s, y - 110 * s, x + 200 * s, y + 110 * s, 110 * s, (60, 18, 36), a, outline=PK, ow=14 * s, bg=bg)
    c.circ(x, y + 160 * s, 150 * s, None, 0)
    c.d.chord(((x - 150 * s) * c.k, (y - 10 * s) * c.k, (x + 150 * s) * c.k, (y + 150 * s) * c.k), 180, 360, fill=mix((225, 95, 125), a, bg))
    c.rr(x - 150 * s, y + 60 * s, x + 150 * s, y + 94 * s, 16 * s, (225, 95, 125), a, bg=bg)
    for k in range(5): c.rr(x - 130 * s + k * 56 * s, y - 104 * s, x - 90 * s + k * 56 * s, y - 70 * s, 8 * s, INK, a, bg=(60, 18, 36))

def gate(c, x, y, o, a, t=0.0, col=GATE, bg=BG, s=1.0, ions=True, half=420):
    """A gate (ion channel) in a nerve-cell membrane. o: 0 shut, 1 open."""
    if a <= .01: return
    for row in (-1, 1):
        for k in range(-int(half / 34), int(half / 34) + 1):
            px = x + k * 34 * s
            if abs(px - x) < 90 * s: continue
            c.line([(px, y + row * 40 * s), (px, y + row * 8 * s)], (60, 66, 110), 4, a, bg=bg)
            c.circ(px, y + row * 42 * s, 15 * s, MEM, a, bg=bg)
    sh = 34 * s * o
    c.rr(x - 74 * s - sh, y - 82 * s, x - 6 * s - sh, y + 82 * s, 24 * s, col, a, bg=bg)
    c.rr(x + 6 * s + sh, y - 82 * s, x + 74 * s + sh, y + 82 * s, 24 * s, col, a, bg=bg)
    if ions and o > .3:
        for k in range(4):
            u = (t * 1.1 + k / 4) % 1; c.circ(x, y - 150 * s + 300 * s * u, 11 * s, NERVE, a * clamp((o - .3) * 2), bg=bg)

def brain(c, x, y, r, a, glow=0.0, bg=BG):
    if a <= .01: return
    fill = tuple(int(CARD[j] + (NERVE[j] - CARD[j]) * .45 * glow) for j in range(3))
    c.circ(x - r * .3, y, r * .8, fill, a, outline=NERVE, ow=6, bg=bg); c.circ(x + r * .3, y, r * .8, fill, a, outline=NERVE, ow=6, bg=bg)
    c.rr(x - r * .7, y - r * .2, x + r * .7, y + r * .6, r * .3, fill, a, bg=bg)
    c.line([(x, y - r * .75), (x, y + r * .55)], NERVE, 5, a, bg=fill)
    for dx in (-1, 1):
        c.d.arc(((x + dx * r * .45 - r * .3) * c.k, (y - r * .35) * c.k, (x + dx * r * .45 + r * .3) * c.k, (y + r * .25) * c.k), 200, 340, fill=mix(NERVE, a, fill), width=int(5 * c.k))

def nerve(c, pts, a, fire, t, bg=BG):
    if a <= .01: return
    c.line(pts, (80, 70, 140), 8, a, bg=bg)
    if fire > .05:
        L = len(pts) - 1
        for k in range(3):
            u = (t * .9 + k / 3) % 1; i = min(L - 1, int(u * L)); f = u * L - i
            px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
            c.circ(px, py, 14, NERVE, a * fire, bg=bg)

def molecule(c, x, y, s, a, col=RED, tail=True, bg=BG):
    """A simple ring with a zig-zag tail: a stand-in for capsaicin (red) or menthol (green). Not a real structure."""
    if a <= .01: return
    hexa = [(x + 26 * s * math.cos(math.pi / 3 * k + math.pi / 6), y + 26 * s * math.sin(math.pi / 3 * k + math.pi / 6)) for k in range(7)]
    c.line(hexa, col, 6 * s, a, bg=bg)
    if tail:
        zz = [(x + 26 * s + k * 16 * s, y + (8 * s if k % 2 else -8 * s)) for k in range(5)]
        c.line(zz, col, 6 * s, a, bg=bg)

def glass(c, x, y, s, a, col, lev=.75, bg=BG):
    """A drinking glass standing on (x, y)."""
    if a <= .01: return
    w0, w1, h = 60 * s, 46 * s, 190 * s
    poly(c, [(x - w1 + 3, y - 3), (x + w1 - 3, y - 3), (x + w1 + (w0 - w1) * lev - 3, y - h * lev), (x - w1 - (w0 - w1) * lev + 3, y - h * lev)], col, a, bg)
    c.line([(x - w0, y - h), (x - w1, y), (x + w1, y), (x + w0, y - h)], (170, 180, 220), 5 * s, a, bg=bg)

def mouse(c, x, y, s, a, bg=BG):
    if a <= .01: return
    g = (150, 150, 170)
    c.line([(x - 90 * s, y + 20 * s), (x - 150 * s, y - 10 * s), (x - 190 * s, y + 20 * s)], g, 6 * s, a, bg=bg)
    c.d.ellipse(((x - 100 * s) * c.k, (y - 50 * s) * c.k, (x + 60 * s) * c.k, (y + 50 * s) * c.k), fill=mix(g, a, bg))
    c.circ(x + 70 * s, y - 10 * s, 40 * s, g, a, bg=bg); c.circ(x + 50 * s, y - 50 * s, 24 * s, (200, 160, 175), a, bg=bg)
    c.circ(x + 84 * s, y - 18 * s, 6 * s, DARK, a, bg=g); c.circ(x + 110 * s, y - 2 * s, 7 * s, PK, a, bg=g)

def bird(c, x, y, s, a, bg=BG):
    if a <= .01: return
    b = (90, 170, 255)
    c.d.ellipse(((x - 80 * s) * c.k, (y - 45 * s) * c.k, (x + 50 * s) * c.k, (y + 45 * s) * c.k), fill=mix(b, a, bg))
    poly(c, [(x - 70 * s, y - 10 * s), (x - 140 * s, y - 40 * s), (x - 130 * s, y + 10 * s)], b, a, bg)
    c.circ(x + 50 * s, y - 40 * s, 34 * s, b, a, bg=bg)
    poly(c, [(x + 80 * s, y - 50 * s), (x + 120 * s, y - 36 * s), (x + 80 * s, y - 26 * s)], YE, a, bg)
    c.circ(x + 58 * s, y - 48 * s, 6 * s, DARK, a, bg=b)
    poly(c, [(x - 30 * s, y - 20 * s), (x + 20 * s, y - 10 * s), (x - 20 * s, y + 30 * s)], (60, 130, 220), a, b)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: a surprising true statement, with the cold chilli moving in the first frame."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Cold ', COLD), ('chilli', RED)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Mouth ', INK), ('on fire', RED)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Nothing', ANS), (' is hot', INK)], sw_in(T, 2))
    chilli(c, 220, 470, 1.15, 1, .06 * math.sin(t * 1.6))
    for k in range(14):                                   # fridge-cold frost drifting off the chilli
        u = (t * .25 + k / 14) % 1; px = 230 + (k * 53) % 380; py = 640 - 260 * u
        c.circ(px, py, 5 + (k % 3) * 2, COLD, (1 - u) * (1 - .6 * hl(1)))
    thermo(c, 760, 720, 360, .14, COLD, 1, label='fridge cold', lcol=COLD)
    m1 = hl(1)
    mouth(c, 1300, 560, .95, m1)
    for k in range(4): flame(c, 1130 + k * 115, 380 - (k % 2) * 30, .9, m1 * fd(T(1), .2 + .12 * k), t)
    m2 = hl(2)
    thermo(c, 1690, 720, 360, .42, ANS, m2, label='mouth: normal', lcol=ANS)
    c.circ(1780, 330, 44, ANS, m2); c.check(1780, 330, 40, DARK, m2, fd(T(2), .3, .5))

GX, GY = 860, 560
def s_sensor(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Tiny ', INK), ('heat sensors', GATE)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('TRPV1', GATE), (': a gate', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Normal: ', INK), ('shut', DIM)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('43 °C', RED), (': it opens', INK)], sw_in(T, 3))
    m0 = fd(T(0), .1)
    # the tongue with dots for sensors, then zoom in to one gate
    zoom = hl(1)
    c.d.chord(((250) * c.k, (560) * c.k, (1450) * c.k, (1120) * c.k), 180, 360, fill=mix((225, 95, 125), m0 * (1 - zoom)))
    for k in range(18):
        px = 330 + (k % 9) * 130 + (k // 9) * 60; py = 700 + (k // 9) * 70
        c.circ(px, py, 12, GATE, m0 * (1 - zoom) * fd(T(0), .3 + .06 * k))
    c.text(850, 860, 'nerve endings in your tongue', 32, DIM, m0 * (1 - zoom), w='Bold')
    o = fd(T(3), 1.6, .6)
    hot = fd(T(3), .2, 1.4)
    gate(c, GX, GY, o, zoom, t)
    c.text(GX + 260, GY - 120, 'TRPV1', 40, GATE, zoom, w='Bold')
    c.text(GX - 300, GY - 100, 'outside', 28, DIM, zoom, w='Bold'); c.text(GX - 300, GY + 110, 'inside the nerve', 28, DIM, zoom, w='Bold')
    lev = .42 + .4 * hot
    thermo(c, 240, 760, 440, lev, RED if hot > .5 else ANS, zoom, label=('43 °C' if hot > .5 else '37 °C'), lcol=RED if hot > .5 else ANS)
    if hl(2) > .01 and o < .1: c.text(GX, GY + 180, 'shut', 40, DIM, hl(2) * (1 - hot), w='Bold')
    brain(c, 1640, 420, 110, zoom, glow=o)
    nerve(c, [(GX, GY + 150), (GX + 300, GY + 230), (1400, 600), (1560, 500)], zoom, o, t)
    c.text(1640, 600, 'HOT!', 64, RED, o, w='Bold')
    c.text(1880, 858, 'Simplified drawing, not to scale', 28, DIM, zoom, anchor='rm', w='Regular')

def s_trick(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Capsaicin', RED), (' in chilli', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('It opens the ', INK), ('gate', GATE)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Same ', INK), ('hot', RED), (' message', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Brain: ', NERVE), ('burn!', RED)], sw_in(T, 3))
    chilli(c, 120, 300, .6, 1, .1)
    o = fd(T(1), .5, .5)
    # capsaicin molecules drift from the chilli to the gate
    m0 = fd(T(0), .2)
    for k in range(5):
        u = clamp(fd(T(0), .3 + .2 * k, 2.2) + 0); sx, sy = 420, 360 + k * 18
        tx, ty = GX - 20 + (k - 2) * 110, GY - 150 - abs(k - 2) * 30
        if k == 2: tx, ty = GX - 26, GY - 70 * (1 - .4 * o)
        px = sx + (tx - sx) * u; py = sy + (ty - sy) * u + 20 * math.sin(t * 2 + k) * (1 - u)
        molecule(c, px, py, 1.0, m0)
    c.text(520, 300, 'capsaicin', 38, RED, m0, w='Bold')
    gate(c, GX, GY, o, 1, t)
    thermo(c, 180, 800, 300, .42, ANS, 1, label='no extra heat', lcol=ANS)
    brain(c, 1640, 420, 110, 1, glow=o * hl(2))
    nerve(c, [(GX, GY + 150), (GX + 300, GY + 230), (1400, 600), (1560, 500)], 1, o * max(.4, hl(2)), t)
    m2 = hl(2)
    c.rr(1380, 620, 1880, 720, 22, CARD, m2, outline=RED, ow=3); c.text(1630, 670, '"HOT!" (it isn\'t)', 40, RED, m2, w='Bold', bg=CARD)
    m3 = hl(3)
    for k in range(3): flame(c, 1520 + k * 120, 270, .7, m3 * fd(T(3), .1 * k), t)
    for k in range(3):                                   # sweat drops
        u = (t * .6 + k / 3) % 1
        c.circ(1500 + k * 140, 760 + 60 * u, 12, COLD, m3 * fd(T(3), 2.0) * (1 - u))
    c.text(1880, 858, 'Simplified drawing; molecules not to scale', 28, DIM, 1, anchor='rm', w='Regular')

def s_found(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Found in ', INK), ('1997', GATE)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Millions of ', INK), ('DNA pieces', NERVE)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('One gene', GATE), (' reacted', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Nobel Prize', GATE), (', 2021', INK)], sw_in(T, 3))
    m0 = fd(T(0), .1); win = 17
    lit = hl(2) * fd(T(2), .3, .5)
    for k in range(32):
        px = 260 + (k % 8) * 125; py = 330 + (k // 8) * 125
        a = m0 * fd(T(0), .03 * k) * (1 - .5 * lit * (k != win))
        oc = GATE if (k == win and lit > .3) else MEM
        c.circ(px, py, 48, CARD if not (k == win and lit > .3) else (70, 60, 30), a, outline=oc, ow=5 if k == win else 3)
        if hl(1) > .01 and fd(T(1), .04 * k, .3) > .1:
            c.d.arc(((px - 22) * c.k, (py - 16) * c.k, (px + 22) * c.k, (py + 16) * c.k), 200, 340, fill=mix(NERVE, a * fd(T(1), .04 * k, .3), CARD), width=int(5 * c.k))
            molecule(c, px - 6, py + 16, .38, a * hl(1) * .8)
    if lit > .3: c.check(260 + (win % 8) * 125, 330 + (win // 8) * 125, 40, GATE, lit, fd(T(2), .6, .5))
    c.text(760, 840, 'cells that normally ignore capsaicin', 32, DIM, m0 * (1 - hl(3)), w='Bold')
    m3 = hl(3)
    c.line([(1520, 260), (1480, 400)], PK, 18, m3); c.line([(1640, 260), (1680, 400)], CY, 18, m3)
    c.circ(1580, 520, 150, GATE, m3, outline=(255, 230, 150), ow=8)
    c.text(1580, 490, 'Nobel', 56, DARK, m3, w='Bold', bg=GATE); c.text(1580, 560, '2021', 52, DARK, m3, w='Bold', bg=GATE)
    c.text(1580, 730, 'David Julius,', 36, INK, m3, w='Bold'); c.text(1580, 776, 'shared with Ardem Patapoutian', 30, DIM, m3, w='Bold')
    c.text(1880, 858, 'Cells and medal drawn for illustration', 28, DIM, 1, anchor='rm', w='Regular')

def s_mint(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Works for ', INK), ('cold', COLD), (', too', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Menthol', ANS), (' opens TRPM8', COLD)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Feels cool. ', COLD), ('Isn\'t.', INK)], sw_in(T, 2))
    for k, (x, col, mol, lab, sub, on) in enumerate(((520, GATE, RED, 'heat gate', 'TRPV1 + capsaicin', 1.0),
                                                       (1400, COLD, ANS, 'cold gate', 'TRPM8 + menthol', hl(1)))):
        c.rr(x - 380, 280, x + 380, 820, 30, CARD, 1, outline=col if (k == 0 or on > .5) else MEM, ow=4)
        o = fd(T(0), .4, .5) if k == 0 else fd(T(1), 1.2, .5)
        gate(c, x, 560, o, 1, t, col=col, bg=CARD, s=.8, half=300)
        mol_a = 1 if k == 0 else on
        molecule(c, x - 20, 420 + 40 * o, .9, mol_a, mol, bg=CARD)
        c.text(x, 330, lab, 46, col, 1, w='Bold', bg=CARD); c.text(x, 760, sub, 32, DIM, 1, w='Bold', bg=CARD)
    m2 = hl(2)
    c.rr(1480, 120 + 590, 1760, 120 + 640, 16, DARK, 0)
    for k in range(6):
        u = (t * .4 + k / 6) % 1
        c.text(1680 + 40 * math.sin(k * 2.1), 640 - 240 * u, '*', 50, COLD, m2 * (1 - u), w='Bold', bg=CARD)
    c.text(1880, 858, 'Simplified drawing; molecules not real structures', 28, DIM, 1, anchor='rm', w='Regular')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a bright pattern-interrupt background (lesson of 2026-10-13)."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Water', COLD), (' or ', INK), ('milk', MILK), ('?', INK)], 1, bg=QUIZ)
    glass(c, 640, 720, 1.5, 1, COLD, bg=QUIZ); glass(c, 1280, 720, 1.5, 1, MILK, bg=QUIZ)
    c.text(640, 790, 'water', 46, COLD, 1, w='Bold', bg=QUIZ); c.text(1280, 790, 'milk', 46, MILK, 1, w='Bold', bg=QUIZ)
    for k in range(3): flame(c, 860 + k * 100, 360 + (k % 2) * 20, .8, fd(t, .2 * k), t, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - 3.2; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 3.0)
        c.circ(960, 560, 80, GATE, u, bg=QUIZ); c.text(960, 560, str(k) if k else '?', 76, DARK, u, w='Bold', bg=GATE)

def s_milk(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Water', COLD), (' spreads it', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Casein', ANS), (' grabs it', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('7 drinks', GATE), (' tested', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Protein', ANS), (', not fat', INK)], sw_in(T, 3))
    m01 = 1 - hl(2)
    # left: water just moves the oily capsaicin around
    c.rr(160, 270, 900, 800, 30, CARD, m01, outline=COLD, ow=4)
    c.text(530, 320, 'water', 46, COLD, m01, w='Bold', bg=CARD)
    for k in range(12):
        bx = 300 + (k % 4) * 140 + 30 * math.sin(t * 1.3 + k); by = 440 + (k // 4) * 110 + 20 * math.cos(t * 1.1 + k)
        molecule(c, bx, by, .7, m01 * fd(T(0), .1 * k), RED, bg=CARD)
    for k in range(5):
        u = (t * .5 + k / 5) % 1; c.circ(240 + k * 140, 760 - 40 * math.sin(u * 3.14), 9, COLD, m01 * .7, bg=CARD)
    c.text(530, 770, 'still on your tongue', 32, RED, m01 * fd(T(0), 2.0), w='Bold', bg=CARD)
    # right: casein grabs capsaicin and carries it off
    m1 = hl(1) * m01
    c.rr(1020, 270, 1760, 800, 30, CARD, m01, outline=ANS if hl(1) > .5 else MEM, ow=4)
    c.text(1390, 320, 'milk', 46, MILK, m01, w='Bold', bg=CARD)
    for k in range(3):
        u = fd(T(1), 1.0 + .3 * k, 2.0); cx = 1200 + k * 190; cy = 520 + k % 2 * 80 - 120 * u
        c.circ(cx, cy, 58, (40, 80, 64), m1, outline=ANS, ow=5, bg=CARD)
        for j in range(3):
            molecule(c, cx - 30 + j * 22, cy - 20 + j * 18, .45, m1, RED, tail=False, bg=(40, 80, 64))
    c.text(1390, 770, 'casein carries it away', 32, ANS, m1, w='Bold', bg=CARD)
    m2 = hl(2) * (1 - hl(3))
    labs = [('water', COLD, 0), ('fizzy water', COLD, 0), ('soda', PK, 0), ('cherry drink', RED, .5), ('beer, 0%', YE, 0), ('skim milk', MILK, 1), ('whole milk', MILK, 1)]
    for k, (lab, col, ok) in enumerate(labs):
        x = 280 + k * 226; a = m2 * fd(T(2), .12 * k)
        glass(c, x, 640, 1.0, a, col)
        c.text(x, 690, lab, 28, DIM, a, w='Bold')
        if ok: c.circ(x, 400, 34, ANS, a * (.5 + .5 * ok)); c.check(x, 400, 30, DARK, a * (.5 + .5 * ok), fd(T(2), 1.6 + .2 * k, .4))
    c.text(960, 790, 'only milk and the sweet cherry drink made a clear difference', 32, INK, m2 * fd(T(2), 2.2), w='Bold')
    m3 = hl(3)
    glass(c, 700, 700, 1.6, m3, MILK); glass(c, 1220, 700, 1.6, m3, MILK, lev=.75)
    c.text(700, 770, 'skim', 46, MILK, m3, w='Bold'); c.text(1220, 770, 'whole', 46, MILK, m3, w='Bold')
    c.text(960, 560, '=', 120, ANS, m3, w='Bold')
    c.text(1880, 858, 'Drinks from a 2019 study; icons illustrative', 28, DIM, 1, anchor='rm', w='Regular')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Why make ', INK), ('capsaicin', RED), ('?', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Birds', COLD), (' feel nothing', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Birds ', COLD), ('spread seeds', ANS)], sw_in(T, 2))
    sway = .05 * math.sin(t * 1.2)
    chilli(c, 800, 330, .7, 1, .9 + sway)
    m1 = hl(1)
    mouse(c, 420, 600, 1.2, m1)
    for k in range(2): flame(c, 560 + k * 70, 460, .6, m1 * fd(T(1), .5 + .2 * k), t)
    c.text(400, 760, 'mammals: burn', 40, RED, m1, w='Bold')
    bird(c, 1340, 560, 1.3, m1 * fd(T(1), 1.6))
    c.circ(1500, 400, 40, ANS, m1 * fd(T(1), 2.2)); c.check(1500, 400, 36, DARK, m1 * fd(T(1), 2.2), fd(T(1), 2.4, .4))
    c.text(1340, 760, 'birds: no burn', 40, COLD, m1 * fd(T(1), 1.6), w='Bold')
    m2 = hl(2)
    for k in range(9):
        u = fd(T(2), .3 + .15 * k, .8); px = 1240 - k * 70; py = 600 + 90 * u + (k % 2) * 20
        c.circ(px, py, 9, (240, 220, 160), m2 * u)
    c.text(1880, 858, 'Two ideas: seed spreading, and protection from fungus', 28, DIM, m2, anchor='rm', w='Bold')

def s_recap(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', GATE)], 1)
    items = ((1, 'No heat. Capsaicin opens a heat gate.', RED), (2, 'Your brain reads it as burning.', NERVE),
             (3, 'Water spreads it. Milk carries it away.', ANS))
    for ln, txt, col in items:
        m = hl(ln); x0 = 140 + (ln - 1) * 560; dy = 50 * (1 - m)
        c.rr(x0, 290 + dy, x0 + 520, 800 + dy, 30, CARD, m, outline=col, ow=5)
        c.circ(x0 + 260, 380 + dy, 50, col, m, bg=CARD); c.text(x0 + 260, 380 + dy, str(ln), 56, DARK, m, w='Bold', bg=col)
        if ln == 1: gate(c, x0 + 260, 530 + dy, 1, m, t, bg=CARD, s=.55, ions=False, half=200); molecule(c, x0 + 245, 480 + dy, .6, m, bg=CARD)
        if ln == 2: brain(c, x0 + 260, 530 + dy, 70, m, glow=1, bg=CARD); flame(c, x0 + 360, 500 + dy, .5, m, t, bg=CARD)
        if ln == 3: glass(c, x0 + 190, 600 + dy, .7, m, COLD, bg=CARD); glass(c, x0 + 330, 600 + dy, .7, m, MILK, bg=CARD)
        for j, l in enumerate(wrap(c, txt, 40, 460, 'Bold')):
            c.text(x0 + 260, 665 + dy + j * 50, l, 40, INK, m, w='Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    chilli(c, 1250, 360, 1.25, 1, .35)
    thermo(c, 1780, 860, 520, .16, COLD, 1)
    for k in range(3): flame(c, 1300 + k * 140, 820, 1.1, 1, k * .7)

SCENES = [
 ('THE HOOK', ["A chilli straight from the fridge is cold.",
               "Bite it, and your mouth feels like it's on fire.",
               "But nothing in your mouth is hot. Your nerves are being tricked."], s_hook),
 ('THE SENSOR', ["Your tongue has tiny heat sensors on its nerve endings.",
                 "One of them is called T R P V 1. Think of it as a gate.",
                 "At normal body temperature, the gate stays shut.",
                 "Near forty-three degrees Celsius, where heat starts to hurt, it swings open, and the nerve fires a warning: hot!"], s_sensor),
 ('THE TRICK', ["Chilli contains a molecule called capsaicin.",
                "Capsaicin fits that same gate and pops it open, with no heat at all.",
                "So the nerve sends the same message as if you'd touched something hot.",
                "Your brain believes it. You feel the burn, and some people even start to sweat."], s_trick),
 ('THE DISCOVERY', ["Scientists found this gate in nineteen ninety-seven.",
                    "David Julius and his team took millions of pieces of DNA, and tried genes in cells that normally ignore capsaicin.",
                    "One gene made the cells react. That gene builds the heat sensor.",
                    "In twenty twenty-one, this work won a share of the Nobel Prize."], s_found),
 ('THE COLD TRICK', ["The same trick works with cold.",
                     "Menthol, from mint, opens a different gate, called T R P M 8. It senses cold.",
                     "That's why a mint can feel cool, even though it isn't cold."], s_mint),
 ('QUICK QUESTION', ["Quick question. Your mouth is burning. Do you grab water, or milk?"], s_quiz),
 ('THE FIX', ["Most people grab water. But capsaicin is oily. It doesn't dissolve in water, so water mostly spreads it around.",
              "Milk has a protein called casein. It grabs capsaicin and carries it away, a bit like soap lifting grease.",
              "In a twenty nineteen study of seven drinks, only milk and a sweet cherry drink made a clear difference.",
              "And skim milk worked just as well as whole milk. So it's the protein, not the fat."], s_milk),
 ('WHY CHILLI?', ["So why would a plant make capsaicin at all?",
                  "Mammals, like us and mice, have this heat gate. But birds can eat chillies and feel no burn.",
                  "One idea is that birds eat the chillies and spread the seeds far and wide. Another is protection from fungus."], s_why),
 ('RECAP', ["Three things to keep.",
            "One: chilli has no heat. Capsaicin opens your heat gate, T R P V 1.",
            "Two: your brain reads that as burning, so you feel heat that isn't there.",
            "Three: water spreads capsaicin around. Milk's casein carries it away.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('No ', INK), ('heat', RED), ('. Still burns', INK)], sw_out(T, 1), size=96)
    headline(c, [('A ', INK), ('heat sensor', GATE), (' is tricked', INK)], sw_in(T, 1), size=92)
    chilli(c, 220, 470, 1.15, 1, .06 * math.sin(t * 1.6))
    thermo(c, 760, 720, 360, .14, COLD, 1, label='fridge cold', lcol=COLD)
    mouth(c, 1340, 560, .95, 1)
    for k in range(4): flame(c, 1170 + k * 115, 380 - (k % 2) * 30, .9, fd(t, .1 + .1 * k), t)

def short_gate(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Shut', DIM), (' at body heat', INK)], sw_out(T, 1), size=96)
    headline(c, [('Opens', RED), (' near 43 °C', INK)], sw_in(T, 1), size=96)
    o = fd(T(1), 1.4, .5); hot = fd(T(1), .2, 1.2)
    gate(c, GX, GY, o, 1, t)
    c.text(GX + 260, GY - 120, 'TRPV1', 44, GATE, 1, w='Bold')
    thermo(c, 240, 760, 440, .42 + .4 * hot, RED if hot > .5 else ANS, 1, label=('43 °C' if hot > .5 else '37 °C'), lcol=RED if hot > .5 else ANS)
    brain(c, 1640, 420, 110, 1, glow=o)
    nerve(c, [(GX, GY + 150), (GX + 300, GY + 230), (1400, 600), (1560, 500)], 1, o, t)
    c.text(1640, 600, 'HOT!', 64, RED, o, w='Bold')

def short_trick(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Capsaicin', RED), (' opens it', INK)], sw_out(T, 1), size=96)
    headline(c, [('Brain: ', NERVE), ('"hot!"', RED)], sw_in(T, 1), size=96)
    chilli(c, 120, 300, .6, 1, .1)
    o = fd(T(0), 2.4, .5)
    for k in range(5):
        u = fd(T(0), .2 + .2 * k, 2.0); sx, sy = 420, 360 + k * 18
        tx, ty = GX - 20 + (k - 2) * 110, GY - 150 - abs(k - 2) * 30
        if k == 2: tx, ty = GX - 26, GY - 70 * (1 - .4 * o)
        molecule(c, sx + (tx - sx) * u, sy + (ty - sy) * u, 1.0, 1)
    gate(c, GX, GY, o, 1, t)
    thermo(c, 180, 800, 300, .42, ANS, 1, label='no heat', lcol=ANS)
    brain(c, 1640, 420, 110, 1, glow=o)
    nerve(c, [(GX, GY + 150), (GX + 300, GY + 230), (1400, 600), (1560, 500)], 1, o, t)
    for k in range(3): flame(c, 1520 + k * 120, 270, .7, hl(1) * fd(T(1), .1 * k), t)

def short_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Water', COLD), (' won\'t wash it', INK)], sw_out(T, 1), size=96)
    headline(c, [('Milk', MILK), (' carries it off', ANS)], sw_in(T, 1), size=96)
    c.rr(160, 270, 900, 800, 30, CARD, 1, outline=COLD, ow=4); c.text(530, 320, 'water', 50, COLD, 1, w='Bold', bg=CARD)
    for k in range(12):
        molecule(c, 300 + (k % 4) * 140 + 30 * math.sin(t * 1.3 + k), 440 + (k // 4) * 110 + 20 * math.cos(t * 1.1 + k), .7, 1, RED, bg=CARD)
    m1 = hl(1)
    c.rr(1020, 270, 1760, 800, 30, CARD, 1, outline=ANS if m1 > .5 else MEM, ow=4); c.text(1390, 320, 'milk', 50, MILK, 1, w='Bold', bg=CARD)
    for k in range(3):
        u = fd(T(1), .6 + .3 * k, 2.0); cx = 1200 + k * 190; cy = 520 + k % 2 * 80 - 120 * u
        c.circ(cx, cy, 58, (40, 80, 64), m1, outline=ANS, ow=5, bg=CARD)
        for j in range(3): molecule(c, cx - 30 + j * 22, cy - 20 + j * 18, .45, m1, RED, tail=False, bg=(40, 80, 64))
    c.text(1390, 770, 'casein', 44, ANS, m1, w='Bold', bg=CARD)

SHORT_SCENES = [
 ('THE HOOK', ["Why does chilli burn your mouth, when it isn't even hot?",
               "Because it tricks a heat sensor on your nerves."], short_hook),
 ('THE SENSOR', ["The sensor, called T R P V 1, works like a gate. At body temperature, it stays shut.",
                 "Near forty-three degrees Celsius, where heat starts to hurt, it opens, and the nerve shouts: hot!"], short_gate),
 ('THE TRICK', ["Chilli's molecule, capsaicin, fits that gate and opens it, with no heat at all.",
                "So your brain gets the same message as touching something hot."], short_trick),
 ('THE FIX', ["And capsaicin is oily, so water just spreads it around.",
              "Milk's protein, casein, grabs it and carries it away."], short_fix),
 ('THE ANSWER', ["So the burn is real. The heat isn't.",
                 "Chilli just flips your heat switch."], card('The burn is real.', 'The heat is not.')),
]
SHORT_HITS = [(4, 0, 0.0)]
