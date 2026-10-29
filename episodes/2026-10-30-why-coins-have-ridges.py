"""Episode: The Real Reason Coins Have Ridges (clipping silver coins, the milled edge, why ridges stay today)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "The Edge of a Coin"                         # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                          # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why do coins have ridges?"                   # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 2, 0.0), (5, 3, 0.0)]             # title card, the ridges vanish, quiz answer
THUMB = ['WHY COINS', 'HAVE RIDGES']
MUSIC_LEVEL = 0.006                                         # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                              # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.5, (2, 1): 0.4, (4, 2): 0.5, (5, 3): 0.6, (6, 2): 0.3}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'sixteen-nineties': '1690s', 'sixteen sixty-two': '1662', 'sixteen ninety-six': '1696',
                 'a hundred and nineteen': '119', 'a hundred and eighteen': '118'}

SIL = (205, 212, 228); SILD = (130, 138, 160); GOLD = (245, 195, 80); GOLDD = (170, 120, 40)
COP = (210, 130, 80); COPD = (140, 80, 45); SKIN = (225, 180, 150); STEEL = (110, 116, 150)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    """Deterministic pseudo-random number in [0, 1)."""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerpc(p, q, u): u = clamp(u); return tuple(int(p[i] + (q[i] - p[i]) * u) for i in range(3))

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def coin(c, x, y, r, col=SIL, a=1.0, ridges=True, clip=0.0, ca=0.0, wob=0.0, seed=1, spin=0.0, sym='1', bg=BG, n=72):
    """A coin seen face-on. clip = depth of the shaved-off edge (fraction of r) at angle ca.
    wob = how uneven a hand-made edge is. Ridges are short dark ticks round the rim."""
    if a <= .01: return
    dark = lerpc(col, (40, 40, 60), .45)
    ux, uy = math.cos(ca), math.sin(ca); d = r * (1 - clip)
    def rad(ang): return r * (1 + wob * (.05 * math.sin(3 * ang + seed) + .035 * math.sin(7 * ang + 2 * seed)))
    pts = []
    for k in range(144):
        ang = 2 * math.pi * k / 144; rr_ = rad(ang)
        px, py = rr_ * math.cos(ang), rr_ * math.sin(ang)
        s = px * ux + py * uy
        if clip > 0 and s > d: px -= (s - d) * ux; py -= (s - d) * uy
        pts.append((x + px, y + py))
    poly(c, pts, dark, a, bg)
    inner = [(x + (px - x) * .94, y + (py - y) * .94) for px, py in pts]
    poly(c, inner, col, a, bg)
    if ridges:
        for k in range(n):
            ang = 2 * math.pi * k / n + spin; rr_ = rad(ang)
            ox, oy = rr_ * math.cos(ang), rr_ * math.sin(ang)
            if clip > 0 and ox * ux + oy * uy > d - r * .02: continue
            c.line([(x + ox * .9, y + oy * .9), (x + ox * .995, y + oy * .995)], dark, max(2, r * .022), a, col)
    c.circ(x, y, r * .74, None, a, outline=dark, ow=max(2, r * .025), bg=col)
    if sym: c.text(x, y + r * .04, sym, int(r * .72), dark, a, w='Bold', bg=col)
    if clip > 0:   # the shaved edge, shown bright
        ex = x + d * ux; ey = y + d * uy; h = math.sqrt(max(0, r * r - d * d))
        c.line([(ex - h * uy, ey + h * ux), (ex + h * uy, ey - h * ux)], lerpc(col, INK, .5), max(3, r * .03), a, bg)

def sliver(c, x, y, r, a=1.0, col=SIL, ang=0.0, bg=BG):
    """A thin curved sliver of metal."""
    if a <= .01: return
    pts = [(x + r * math.cos(ang + u / 10 - .5), y + r * math.sin(ang + u / 10 - .5)) for u in range(11)]
    c.line(pts, col, max(4, r * .12), a, bg)

def edge_strip(c, x0, y0, x1, y1, a=1.0, ridges=1.0, col=SIL, shift=0.0, smooth=None, bg=BG):
    """A coin's rim seen side-on, very close up. ridges 0..1 fades the ridge lines in."""
    if a <= .01: return
    c.rr(x0, y0, x1, y1, 18, col, a, bg=bg)
    c.rr(x0, y0, x1, y0 + 16, 8, lerpc(col, INK, .4), a, bg=col)
    c.rr(x0, y1 - 16, x1, y1, 8, lerpc(col, (40, 40, 60), .3), a, bg=col)
    if ridges > .01:
        step = 26; k = 0
        xx = x0 + 12 + (shift % step)
        while xx < x1 - 8:
            if not (smooth and smooth[0] < xx < smooth[1]):
                c.line([(xx, y0 + 18), (xx, y1 - 18)], lerpc(col, (40, 40, 60), .5), 8, a * ridges, col)
            xx += step; k += 1

def thumbtip(c, x, y, a=1.0, ang=0.0, bg=BG):
    """A thumb (or fingertip) pointing left, tip at (x, y)."""
    if a <= .01: return
    c.rr(x, y - 55, x + 320, y + 55, 55, SKIN, a, bg=bg)
    c.rr(x + 20, y - 40, x + 110, y + 10, 22, (240, 205, 185), a, bg=SKIN)

def lock(c, x, y, s, a=1.0, col=YE, bg=BG):
    if a <= .01: return
    pts = [(x + s * .55 * math.cos(math.pi + math.pi * u / 20), y - s * .3 + s * .55 * math.sin(math.pi + math.pi * u / 20)) for u in range(21)]
    c.line(pts, col, s * .14, a, bg)
    c.rr(x - s * .8, y - s * .35, x + s * .8, y + s * .85, s * .15, col, a, bg=bg)
    c.circ(x, y + s * .2, s * .16, BG, a, bg=col); c.rr(x - s * .06, y + s * .2, x + s * .06, y + s * .55, 4, BG, a, bg=col)

def bar(c, x, y, w, h, a=1.0, col=SIL, bg=BG):
    """An ingot."""
    if a <= .01: return
    poly(c, [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x + w / 2 - h * .5, y - h / 2), (x - w / 2 + h * .5, y - h / 2)], lerpc(col, (40, 40, 60), .25), a, bg)
    poly(c, [(x - w / 2 + 10, y + h / 2 - 8), (x + w / 2 - 10, y + h / 2 - 8), (x + w / 2 - h * .5, y - h / 2 + 8), (x - w / 2 + h * .5, y - h / 2 + 8)], col, a, bg)

def pot(c, x, y, a=1.0, t=0.0, fill=0.5, bg=BG):
    """A melting pot over a flame."""
    if a <= .01: return
    for k in range(5):
        fx = x - 80 + k * 40; fh = 50 + 20 * math.sin(t * 9 + k * 1.7)
        poly(c, [(fx - 18, y + 150), (fx + 18, y + 150), (fx, y + 150 - fh)], (255, 140, 60), a, bg)
    c.rr(x - 130, y - 40, x + 130, y + 110, 30, STEEL, a, bg=bg)
    c.rr(x - 110, y - 30, x + 110, y - 30 + 40 * fill + 6, 14, lerpc(SIL, (255, 230, 200), .4 + .2 * math.sin(t * 4)), a, bg=STEEL)

def pizza(c, x, y, r, cut, a=1.0, bg=BG):
    """A pizza whose crust has been trimmed cut times (each a thin flat slice off one side)."""
    if a <= .01: return
    crust = (215, 150, 80); top = (230, 90, 60)
    pts = []
    for k in range(144):
        ang = 2 * math.pi * k / 144; px, py = r * math.cos(ang), r * math.sin(ang)
        for j in range(cut):
            ca = -1.2 + j * 2.1; ux, uy = math.cos(ca), math.sin(ca); d = r * .86
            s = px * ux + py * uy
            if s > d: px -= (s - d) * ux; py -= (s - d) * uy
        pts.append((x + px, y + py))
    poly(c, pts, crust, a, bg)
    poly(c, [(x + (px - x) * .84, y + (py - y) * .84) for px, py in pts], top, a, crust)
    for k in range(7):
        ang = k * 2.4; rr_ = r * .45 * rnd(k, 3) + r * .1
        c.circ(x + rr_ * math.cos(ang), y + rr_ * math.sin(ang), r * .09, (250, 230, 170), a, bg=top)

def jar(c, x, y, a=1.0, broken=0.0, t=0.0, bg=BG):
    """A jam jar with a paper seal over the lid; broken 0..1 tears it."""
    if a <= .01: return
    c.rr(x - 120, y - 110, x + 120, y + 170, 40, (200, 215, 240), a, bg=bg)
    c.rr(x - 100, y - 70, x + 100, y + 150, 30, (180, 40, 70), a, bg=(200, 215, 240))
    c.rr(x - 130, y - 170, x + 130, y - 105, 14, (220, 180, 70), a, bg=bg)
    sc = lerpc(GR, PK, broken)
    if broken < .5:
        c.rr(x - 30, y - 200, x + 30, y - 40, 8, sc, a, bg=bg)
    else:
        c.rr(x - 30, y - 200, x + 30, y - 140, 8, sc, a, bg=bg)
        poly(c, [(x - 30, y - 120), (x + 30, y - 110), (x + 50, y - 40), (x - 10, y - 50)], sc, a, (180, 40, 70))
        for k in range(4):
            c.line([(x - 30 + 20 * k, y - 140), (x - 20 + 20 * k, y - 128)], sc, 5, a, bg)

def press(c, x, y, p, a=1.0, bg=BG):
    """A coin press: upper and lower dies close round a blank (p 0..1)."""
    if a <= .01: return
    top = y - 240 + 160 * p
    c.rr(x - 20, y - 330, x + 20, top - 60, 8, STEEL, a, bg=bg)
    c.rr(x - 150, top - 80, x + 150, top, 18, (150, 156, 190), a, bg=bg)
    c.rr(x - 150, y + 60, x + 150, y + 140, 18, (150, 156, 190), a, bg=bg)
    c.rr(x - 220, y + 140, x + 220, y + 190, 14, STEEL, a, bg=bg)

def apple(c, x, y, r, a=1.0, bg=BG):
    if a <= .01: return
    c.circ(x - r * .3, y, r * .75, (220, 60, 60), a, bg=bg); c.circ(x + r * .3, y, r * .75, (220, 60, 60), a, bg=bg)
    c.line([(x, y - r * .6), (x + r * .15, y - r * 1.05)], (110, 70, 40), r * .12, a, bg)
    poly(c, [(x + r * .1, y - r * .8), (x + r * .6, y - r * 1.05), (x + r * .25, y - r * .65)], GR, a, bg)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    """A big ridged silver coin, and a clipped one with its sliver."""
    coin(c, 1450, 470, 330, SIL, spin=.05, sym='1')
    coin(c, 1720, 820, 150, SIL, clip=.16, ca=-.5, wob=.8, seed=3, sym='1')
    sliver(c, 1890, 700, 150, 1.0, SIL, ang=-.5)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Feel the edge of a coin', 72, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'Those ridges were a security system', 66, YE, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'Against a trick called clipping', 70, PK, a * hl(2), w='Bold')
        k0 = a * (1 - hl(2))
        if k0 > 0:
            # a big coin turning slowly, with a thumb running along its rim from frame one
            coin(c, 760, 540, 300, SIL, k0, spin=t * .25)
            ty = 540 + 120 * math.sin(t * 2.2)
            tx = 760 + math.sqrt(max(0, 300 ** 2 - (ty - 540) ** 2)) + 6
            thumbtip(c, tx, ty, k0)
            c.text(1500, 330, 'tiny ridges', 52, CY, k0 * fd(T(0), .8), w='Bold')
            c.arrow(1400, 360, 1080, 440, CY, 6, k0 * fd(T(0), .8), 18)
            if hl(1) > 0: lock(c, 1560, 700, 110, k0 * hl(1))
        k2 = a * hl(2)
        if k2 > 0:
            cl = .16 * fd(T(2), .3, 1.4)
            coin(c, 760, 540, 300, SIL, k2, clip=cl, ca=0.0, wob=.6, seed=2)
            ph = fd(T(2), 1.0, 1.6)
            sliver(c, 1080 + 380 * ph, 540 - 80 * ph, 300, k2 * fd(T(2), 1.0), SIL, ang=0.0)
            c.text(1420, 760, 'shaved off', 46, PK, k2 * fd(T(2), 1.6), w='Bold')
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 330 + 30 * (1 - m), 'The Real Reason', 112, INK, m, w='Bold')
        c.text(960, 470 + 30 * (1 - m), 'Coins Have Ridges', 112, YE, m, w='Bold')
        c.line([(960 - 340 * m, 580), (960 + 340 * m, 580)], CY, 8, m)
        for j in range(5):
            coin(c, 560 + j * 200, 720, 56, SIL if j % 2 else GOLD, m * fd(T(3), .4 + j * .12), spin=t * .4, sym='')

def s_metal(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Coins were made of real silver and gold', 64, GOLD, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'A coin was worth the metal inside it', 66, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Less metal = less value', 72, PK, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j, (col, lab, x) in enumerate(((SIL, 'silver', 640), (GOLD, 'gold', 1280))):
            kk = k0 * fd(T(0), .3 + j * 1.0)
            coin(c, x, 500, 210, col, kk, spin=t * .2 * (1 if j else -1), sym='1')
            c.text(x, 790, lab, 52, col, kk, w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        coin(c, 560, 500, 210, SIL, k1, spin=t * .2)
        c.text(960, 500, '=', 120, INK, k1 * fd(T(1), .8), w='Bold')
        bar(c, 1380, 500, 420, 150, k1 * fd(T(1), 1.4))
        c.text(1380, 680, 'a tiny bar of silver', 44, SIL, k1 * fd(T(1), 1.4), w='Bold')
        c.text(1380, 740, 'with a stamp on it', 36, DIM, k1 * fd(T(1), 2.2), w='Medium')
    k2 = hl(2)
    if k2 > 0:
        for j, (cl, v, lab) in enumerate(((0.0, 1.0, 'full coin'), (.18, .8, 'a little shaved'))):
            x = 560 + j * 800; kk = k2 * fd(T(2), j * .9)
            coin(c, x, 450, 190, SIL, kk, clip=cl, ca=-.6, spin=t * .15)
            c.rr(x - 220, 700, x + 220, 750, 20, CARD, kk)
            c.rr(x - 220, 700, x - 220 + 440 * v * fd(T(2), .4 + j * .9, 1.0), 750, 20, GR if j == 0 else PK, kk)
            c.text(x, 800, lab, 40, INK, kk, w='Bold')
        c.text(960, 450, '?', 120, YE, k2 * fd(T(2), 2.4), w='Bold')
        c.text(960, 560, 'would you notice?', 36, YE, k2 * fd(T(2), 2.4), w='Bold')

def s_clip(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Hand-struck coins: uneven edges', 68, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Shave a sliver, spend it at full value', 64, PK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Melt the slivers, sell the silver', 68, SIL, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        # a hammer comes down on a blank between two dies
        hp = abs(math.sin(t * 2.0))
        hy = 400 + 150 * (1 - hp)
        c.rr(470, hy - 170, 510, hy + 60, 10, (150, 100, 60), k0)
        c.rr(400, hy - 210, 600, hy - 130, 16, STEEL, k0)
        c.rr(430, 660, 570, 720, 10, (150, 156, 190), k0)
        coin(c, 500, 620, 90, SIL, k0, ridges=False, wob=1.0, seed=5, sym='')
        for j in range(3):
            kk = k0 * fd(T(0), .8 + j * .5)
            coin(c, 980 + j * 330, 520, 140, SIL, kk, ridges=False, wob=1.2, seed=j * 3 + 1)
        c.text(1310, 760, 'no two the same shape', 42, DIM, k0 * fd(T(0), 2.2), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        cl = .17 * fd(T(1), .4, 1.6)
        coin(c, 620, 520, 260, SIL, k1, ridges=False, clip=cl, ca=0.0, wob=1.0, seed=2)
        ph = fd(T(1), 1.4, 1.4)
        sliver(c, 885 + 300 * ph, 520 + 160 * ph, 260, k1 * fd(T(1), 1.4), SIL)
        c.rr(1250, 260, 1830, 520, 30, CARD, k1 * fd(T(1), 2.6), outline=GR, ow=3)
        c.text(1540, 335, 'still spent', 48, INK, k1 * fd(T(1), 2.6), w='Bold', bg=CARD)
        c.text(1540, 410, 'at full value', 48, GR, k1 * fd(T(1), 2.6), w='Bold', bg=CARD)
        c.check(1760, 470, 36, GR, k1 * fd(T(1), 2.6), fd(T(1), 3.0))
        c.text(1300, 780, 'keep the sliver', 42, PK, k1 * fd(T(1), 1.8), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        for q in range(9):
            sliver(c, 330 + 40 * rnd(q, 1), 470 + 22 * q, 90, k2 * fd(T(2), q * .08), SIL, ang=-.3 + .6 * rnd(q, 2))
        c.text(370, 760, 'slivers', 40, SIL, k2, w='Bold')
        c.arrow(560, 560, 700, 560, INK, 6, k2 * fd(T(2), .8), 18)
        pot(c, 900, 520, k2 * fd(T(2), .8), t, fill=fd(T(2), 1.0, 1.5))
        c.text(900, 760, 'melted', 40, YE, k2 * fd(T(2), .8), w='Bold')
        c.arrow(1100, 560, 1250, 560, INK, 6, k2 * fd(T(2), 2.0), 18)
        bar(c, 1500, 560, 360, 130, k2 * fd(T(2), 2.0))
        c.text(1500, 760, 'sold as silver', 40, GR, k2 * fd(T(2), 2.4), w='Bold')

def s_shrink(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Passed on... and clipped again', 70, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Like a pizza trimmed at every hand-off', 64, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'England, 1690s: clipped and badly worn', 64, PK, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j in range(4):
            kk = k0 * fd(T(0), j * .9)
            x = 330 + j * 420
            coin(c, x, 500, 150, SIL, kk, ridges=False, clip=.06 * j, ca=-.4 + j * 1.9, wob=1.0, seed=4)
            # a second, overlapping cut from the earlier hand-offs
            if j >= 2: coin(c, x, 500, 150, SIL, kk, ridges=False, clip=.05 * (j - 1), ca=1.4 + j, wob=1.0, seed=4)
            c.text(x, 720, ['first owner', 'second', 'third', 'fourth'][j], 38, DIM, kk, w='Bold')
            if j < 3: c.arrow(x + 180, 500, x + 240, 500, CY, 6, k0 * fd(T(0), j * .9 + .5), 16)
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        n = 1 + int(clamp(T(1) / 1.2) * 3)
        pizza(c, 760, 520, 280, n, k1)
        c.text(1450, 420, 'each person', 48, INK, k1 * fd(T(1), .8), w='Bold')
        c.text(1450, 490, 'trims a little crust', 48, YE, k1 * fd(T(1), .8), w='Bold')
        c.text(1450, 620, 'nobody takes much...', 40, DIM, k1 * fd(T(1), 2.0), w='Medium')
        c.text(1450, 680, 'but it adds up', 44, PK, k1 * fd(T(1), 3.0), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        for i in range(12):
            x = 330 + (i % 6) * 252; y = 390 + (i // 6) * 260
            kk = k2 * fd(T(2), .1 * i)
            coin(c, x, y, 105, SIL if i % 3 else lerpc(SIL, (120, 120, 130), .3), kk, ridges=False,
                 clip=.08 + .12 * rnd(i, 4), ca=6.28 * rnd(i, 5), wob=1.4, seed=i, sym='')
        c.text(960, 800, 'much of the silver money', 40, DIM, k2 * fd(T(2), 1.6), w='Bold')

def s_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The fix: make the edge part of the design', 62, CY, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Machine-pressed: round, with ridges', 66, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Shave it, and the ridges are gone', 68, PK, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Like the seal on a jar of jam', 70, GR, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        edge_strip(c, 260, 380, 1660, 620, k0, ridges=fd(T(0), .8, 1.6), shift=t * 30)
        c.text(960, 720, 'the rim, close up', 40, DIM, k0 * fd(T(0), .5), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        p = fd(T(1), .3, 1.0) * (1 - fd(T(1), 1.6, .6))
        press(c, 560, 560, p, k1)
        coin(c, 560, 560 + 0, 130, SIL, k1 if T(1) > 1.6 else k1 * .5, ridges=T(1) > 1.6, sym='' if T(1) < 1.6 else '1')
        kk = k1 * fd(T(1), 2.2)
        coin(c, 1350, 500, 240, SIL, kk, spin=t * .3)
        c.text(1350, 800, 'perfectly round, ridged', 40, CY, kk, w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        cl = .15 * fd(T(2), .3, 1.2)
        coin(c, 760, 520, 280, SIL, k2, clip=cl, ca=0.0, spin=0.0)
        hv = fd(T(2), 1.4)
        c.circ(760 + 280 * (1 - cl) - 10, 520, 170, None, k2 * hv, outline=PK, ow=8)
        c.text(1450, 430, 'smooth patch', 52, PK, k2 * hv, w='Bold')
        c.text(1450, 500, '= shaved!', 52, PK, k2 * hv, w='Bold')
        c.text(1450, 620, 'anyone can see it', 40, INK, k2 * fd(T(2), 2.2), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        for j, (x, br, lab) in enumerate(((620, 0.0, 'seal intact'), (1300, 1.0, 'seal broken'))):
            kk = k3 * fd(T(3), j * 1.0)
            jar(c, x, 520, kk, broken=br * fd(T(3), 1.0, .6), t=t)
            c.text(x, 790, lab, 44, GR if j == 0 else PK, kk, w='Bold')
            if j == 0: c.check(x + 180, 330, 40, GR, kk, fd(T(3), .5))
            else: c.cross(x + 180, 330, 60, PK, kk * fd(T(3), 1.6))

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 208, 'A shopkeeper gets two silver coins. Which should she refuse?', 40, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'B: silver was shaved off', 68, PK, ans, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        # a counter with two coins, before the choices appear
        c.rr(360, 640, 1560, 700, 16, (120, 80, 50), k0)
        coin(c, 760, 520, 110, SIL, k0 * fd(T(0), 1.0), spin=t * .2)
        coin(c, 1160, 520, 110, SIL, k0 * fd(T(0), 1.4), clip=.12, ca=-.3, spin=t * .2)
    kc = hl(1)
    if kc > 0:
        for j, (lab, x, cl, txt) in enumerate((('A', 560, 0.0, 'ridges all round'), ('B', 1360, .13, 'one smooth patch'))):
            kk = kc * (.3 + .7 * fd(T(1), j * 1.4))
            good = ans * (1 if j == 1 else 0)
            col = PK if good > .5 else (DIM if ans > .5 else CY)
            c.rr(x - 330, 290, x + 330, 760, 34, CARD, kk, outline=col, ow=4 if good > .5 else 3)
            c.circ(x - 270, 340, 38, CY, kk, bg=CARD); c.text(x - 270, 340, lab, 44, BG, kk, w='Bold', bg=CY)
            coin(c, x, 500, 150, SIL, kk, clip=cl, ca=-.3, spin=t * .15, bg=CARD)
            c.text(x, 700, txt, 42, INK, kk, w='Bold', bg=CARD)
            if ans > 0:
                if j == 1: c.cross(x + 250, 350, 70, PK, ans)
                else: c.check(x + 250, 350, 46, GR, ans, fd(T(3), .4))
    if T(2) > 0 and ans < 1:
        ring(c, 960, 520, 70, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        c.text(960, 830, 'worth less than it says', 40, PK, ans * fd(T(3), 2.0), w='Bold')

def s_newton(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'England: milled-edge coins after 1662', 64, CY, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'But old hand-made coins stayed in use', 64, PK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, '1696: replace the old silver coins', 68, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Yes, that Isaac Newton', 72, INK, hl(3), w='Bold')
    k = hl(0) * (1 - hl(3))
    if k > 0:
        # a timeline
        c.line([(220, 640), (1700, 640)], (70, 80, 130), 8, k)
        for yr, x, col, kk in (('1662', 520, CY, k), ('1696', 1300, YE, k * hl(2))):
            c.circ(x, 640, 20, col, kk); c.text(x, 700, yr, 52, col, kk, w='Bold')
        coin(c, 520, 450, 120, SIL, k * fd(T(0), .8), spin=t * .2)
        c.text(520, 790, 'machine-made', 36, CY, k * fd(T(0), 1.2), w='Bold')
        k1 = k * hl(1)
        if k1 > 0:
            for j in range(3):
                x = 760 + j * 150
                coin(c, x, 450, 70, SIL, k1 * fd(T(1), j * .3), ridges=False, clip=.12 * fd(T(1), 1.4 + j * .3, .6), ca=-.5 + j * 2, wob=1.2, seed=j + 7, sym='')
            c.text(910, 560, 'hand-made, still clipped', 34, PK, k1 * fd(T(1), 1.0), w='Bold')
        k2 = k * hl(2)
        if k2 > 0:
            c.rr(1200, 260, 1860, 540, 30, CARD, k2 * fd(T(2), .6), outline=YE, ow=3)
            c.text(1530, 330, 'the Great Recoinage', 44, YE, k2 * fd(T(2), .6), w='Bold', bg=CARD)
            c.text(1530, 410, 'warden of the Royal Mint:', 36, DIM, k2 * fd(T(2), 2.6), w='Medium', bg=CARD)
            c.text(1530, 475, 'Isaac Newton', 54, INK, k2 * fd(T(2), 3.6), w='Bold', bg=CARD)
    k3 = hl(3)
    if k3 > 0:
        # the apple falls onto a stack of new coins
        y = 260 + 300 * fd(T(3), .2, .9)
        apple(c, 960, y, 60, k3)
        coin(c, 960, 700, 150, SIL, k3, spin=t * .1)
        c.text(1500, 480, 'gravity... and coins', 46, YE, k3 * fd(T(3), 1.2), w='Bold')

def s_today(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Today: cheaper metals, no clipping', 66, COP, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Ridges make coins harder to fake', 68, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Tell coins apart by touch', 72, GR, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Counted ridges', 72, YE, hl(3), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        coin(c, 700, 500, 230, lerpc(SIL, COP, .25), k0, spin=t * .2)
        for j, (lab, col) in enumerate((('copper', COP), ('nickel', SIL))):
            kk = k0 * fd(T(0), 1.0 + j * .7)
            c.circ(1250, 400 + j * 160, 44, col, kk); c.text(1330, 400 + j * 160, lab, 52, col, kk, 'lm', 'Bold')
        c.cross(700, 500, 120, PK, k0 * fd(T(0), 3.0) * .0)
        c.text(700, 800, 'no silver to steal', 42, DIM, k0 * fd(T(0), 2.4), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        edge_strip(c, 260, 400, 1160, 600, k1, shift=t * 25)
        c.circ(860, 500, 170, None, k1 * fd(T(1), .6), outline=CY, ow=10)
        c.line([(980, 620), (1100, 760)], CY, 22, k1 * fd(T(1), .6))
        c.rr(1260, 360, 1780, 600, 30, CARD, k1 * fd(T(1), 1.2), outline=CY, ow=3)
        c.text(1520, 440, 'fine, even ridges', 40, INK, k1 * fd(T(1), 1.2), w='Bold', bg=CARD)
        c.text(1520, 520, 'harder to copy', 44, CY, k1 * fd(T(1), 1.8), w='Bold', bg=CARD)
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        for j, (lab, col, rid, x) in enumerate((('dime: ridged', SIL, 1.0, 520), ('penny: smooth', COP, 0.0, 1340))):
            kk = k2 * fd(T(2), 2.6 + j * 1.0)
            edge_strip(c, x - 300, 430, x + 300, 590, kk, ridges=rid, col=col, shift=t * 20)
            thumbtip(c, x + 120, 380 + 10 * math.sin(t * 3 + j), kk)
            c.text(x, 700, lab, 48, col, kk, w='Bold')
        c.text(960, 800, 'helps people who can\'t see well', 40, GR, k2 * fd(T(2), .4), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        for j, (lab, n, x, r) in enumerate((('US quarter', '119', 620, 200), ('US dime', '118', 1300, 160))):
            kk = k3 * fd(T(3), j * 1.6)
            coin(c, x, 470, r, SIL, kk, spin=t * .3, sym='', n=int(n))
            c.text(x, 470, n, 96, YE, kk, w='Bold', bg=SIL, stroke=4)
            c.text(x, 760, lab, 44, INK, kk, w='Bold')
        c.text(960, 840, 'ridges each', 36, DIM, k3 * fd(T(3), 2.0), w='Medium')

RECAPS = [('1', 'Silver coins', 'shaving the edge stole real value', SIL),
          ('2', 'Ridges', 'made a shaved coin easy to spot', CY),
          ('3', 'Today', 'harder to fake, easier to feel', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 160, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, l1, l2, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; y = 330 + i * 175; dx = 60 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        c.rr(300 + dx, y - 70, 1620 + dx, y + 70, 36, CARD, m, outline=col, ow=4)
        c.circ(390 + dx, y, 44, col, m, bg=CARD); c.text(390 + dx, y, nn, 50, BG, m, w='Bold', bg=col)
        c.text(480 + dx, y, l1, 50, col, m, 'lm', 'Bold', bg=CARD)
        c.text(1560 + dx, y, l2, 40, INK, m, 'rm', 'Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Run your thumb around the edge of a coin. Feel those tiny ridges?",
            "They started as a security system.",
            "Against a trick called clipping.",
            "Here's the real reason coins have ridges."], s_hook),
 ('1  ·  METAL MONEY', ["Hundreds of years ago, many coins were made of real silver and gold.",
            "A coin was worth the metal inside it. Like a tiny bar of silver, with a stamp on it.",
            "So less metal meant less value. But only if someone noticed."], s_metal),
 ('2  ·  CLIPPING', ["Many coins were struck by hand, so their edges were never perfectly round.",
            "So someone could shave a thin sliver off the edge, and still spend the coin at full value.",
            "Then they saved the slivers, melted them down, and sold the silver."], s_clip),
 ('3  ·  SHRINKING MONEY', ["The clipped coin was passed on. And the next person could clip it again.",
            "It's like a pizza that gets a little crust trimmed off every time it's handed along.",
            "In England, by the sixteen-nineties, much of the silver money was clipped and badly worn."], s_shrink),
 ('4  ·  THE FIX', ["The fix was clever. Make the edge part of the design.",
            "Machines pressed coins that were perfectly round, with a pattern of ridges around the edge.",
            "Now if someone shaved the edge, the ridges were gone, and anyone could see it.",
            "Like the seal on a jar of jam. Once it's broken, you know."], s_fix),
 ('5  ·  QUICK QUESTION', ["Quick question. A shopkeeper is handed two silver coins. Which one should she refuse?",
            "A, with ridges all the way round. Or B, with one smooth patch.",
            "Three, two, one.",
            "B. That smooth patch means silver was shaved off. The coin is worth less than it says."], s_quiz),
 ('6  ·  ENGLAND', ["In England, machine-made coins with a milled edge arrived after sixteen sixty-two.",
            "But the old hand-made coins stayed in use, and they kept getting clipped.",
            "So in sixteen ninety-six, England began replacing its old silver coins. The warden of the Royal Mint was asked to help. His name was Isaac Newton.",
            "Yes. The same Newton who worked out gravity."], s_newton),
 ('7  ·  TODAY', ["Today, everyday coins are made of cheaper metals, like copper and nickel. There's no silver to steal.",
            "But the ridges stayed, partly out of tradition. And they make coins harder to fake.",
            "They also help people who can't see well tell coins apart by touch. In the US, a dime has ridges. A penny is smooth.",
            "A US quarter has a hundred and nineteen ridges. A dime has a hundred and eighteen."], s_today),
 ('RECAP', ["So remember three things.",
            "One. Old coins were made of silver and gold, so shaving the edge stole real value.",
            "Two. Ridges made a shaved coin easy to spot.",
            "Three. Today, ridges make coins harder to fake, and easier to tell apart by touch.",
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

def short_clip(c, T, t):
    if T(1) < 0: remap(s_metal, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_clip, {0: (1, -9), 1: 1})(c, T, t)

def short_fix(c, T, t):
    if T(1) < 0: remap(s_fix, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_fix, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

# The Short: its own complete mini-story (hook -> silver coins got shaved -> ridges expose it -> answer).
SHORT_SCENES = [
 ('THE HOOK', ["Why do coins have ridges on the edge?",
               "They began as a defence against a trick called clipping. Here's how it worked."],
              short_hook),
 ('CLIPPING', ["Hundreds of years ago, coins were made of real silver, so a coin was worth the metal inside it.",
               "People shaved thin slivers off the edges, still spent the coins at full value, then melted the slivers and sold the silver."],
              short_clip),
 ('THE FIX', ["So coins were pressed by machine, perfectly round, with ridges around the edge.",
              "Shave the edge, and the ridges disappear. Anyone could see the coin had been cut, like a broken seal on a jar."],
             short_fix),
 ('THE ANSWER', ["So the ridges on your coins?",
                 "They were made to show if someone stole the silver. Today, they also help stop fakes."],
                card('The ridges on your coins?', 'Made to expose stolen silver.')),
]
SHORT_HITS = [(3, 1, 0.0)]
