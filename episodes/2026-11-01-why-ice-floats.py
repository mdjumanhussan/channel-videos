"""Episode: Ice Breaks a Rule Almost Every Solid Follows (why ice floats: density, hydrogen bonds, the open lattice, icebergs, pipes, lakes)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why Ice Floats"                              # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                           # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why does ice float?"                          # headline on the vertical Short
HITS = [(0, 3, 0.0), (4, 2, 0.0), (5, 3, 0.0)]              # title card, the open-rings reveal, quiz answer
THUMB = ['MOST SOLIDS', 'SINK.', 'ICE FLOATS.']
MUSIC_LEVEL = 0.006                                         # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                              # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.4, (0, 2): 0.5, (4, 2): 0.5, (5, 2): 0.3, (5, 3): 0.6, (8, 2): 0.4}
SHORT_PAUSES = {(0, 0): 0.3}
CAPTION_FIXES = {'nine percent': '9%', 'ninety percent': '90%', 'four degrees': '4 °C'}

# Colour code, kept the same in every scene (lesson of 2026-11-01): one colour per idea.
WATER = (36, 92, 150)       # liquid water (the fill of every glass, lake, sea)
WATERL = (60, 140, 210)     # water surface line
ICE = (205, 238, 255)       # ice, always pale ice-white
ICED = (150, 200, 235)
OXY = CY                    # oxygen atom of a water molecule
HYD = INK                   # hydrogen atoms
BOND = YE                   # hydrogen bonds, always yellow
OTHER = PU                  # "most other substances", always purple
SINK = PK                   # sinking / packed tight
FLOAT = GR                  # floating / spread out
CORK = (190, 140, 90)
STEEL = (150, 160, 180)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def rnd(i, s):
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)

def lerp(p, q, u): return p + (q - p) * u
def lerpc(p, q, u): u = clamp(u); return tuple(int(p[i] + (q[i] - p[i]) * u) for i in range(3))

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def glass(c, x, y, w, h, a=1.0, level=.75, t=0.0):
    """A drinking glass, base centre at (x, y). Returns the water surface y and the inner box."""
    if a <= .01: return y - h * level, (x - w / 2, y - h, x + w / 2, y)
    top = y - h; surf = y - h * level
    pts = [(x - w / 2 + 6 * k / 20 * 0, surf + 4 * math.sin(t * 2 + k * .6)) for k in range(1)]
    c.rr(x - w / 2, surf, x + w / 2, y, 18, WATER, a)
    wave = [(x - w / 2 + w * k / 30, surf + 4 * math.sin(t * 2.2 + k * .7)) for k in range(31)]
    c.line(wave, WATERL, 5, a, WATER)
    c.line([(x - w / 2, top), (x - w / 2, y - 18), (x - w / 2 + 18, y), (x + w / 2 - 18, y), (x + w / 2, y - 18), (x + w / 2, top)], (170, 190, 230), 6, a)
    return surf, (x - w / 2, top, x + w / 2, y)

def cube(c, x, y, s, a=1.0, bg=BG, col=ICE, cold=ICED):
    """An ice cube (or any block) centred at (x, y)."""
    if a <= .01: return
    c.rr(x - s / 2, y - s / 2, x + s / 2, y + s / 2, s * .16, col, a, bg=bg)
    c.rr(x - s * .32, y - s * .34, x - s * .05, y - s * .22, 6, (255, 255, 255) if col == ICE else lerpc(col, INK, .4), a * .8, bg=col)
    c.line([(x + s * .3, y - s * .1), (x + s * .3, y + s * .3), (x - s * .1, y + s * .3)], cold, 4, a, col)

def molecule(c, x, y, s=1.0, ang=0.0, a=1.0, bg=BG):
    """One water molecule: a cyan oxygen with two white hydrogens in a V (104.5 degrees)."""
    if a <= .01: return
    for d in (-.912, .912):
        hx = x + 44 * s * math.sin(ang + d); hy = y + 44 * s * math.cos(ang + d)
        c.line([(x, y), (hx, hy)], (120, 200, 240), 7 * s, a, bg)
        c.circ(hx, hy, 15 * s, HYD, a, bg=bg)
    c.circ(x, y, 30 * s, OXY, a, bg=bg)

def dots(c, x0, y0, x1, y1, n, spread, a, col, t, seed=1, jig=1.0, r=12, bg=BG):
    """n particles in a box. spread 0 = packed tight at the bottom, 1 = filling the box."""
    if a <= .01: return
    cols = int(math.sqrt(n * (x1 - x0) / max(1, (y1 - y0)))) or 1
    for i in range(n):
        gx = (i % cols + .5) / cols; gy = (i // cols + .5) / math.ceil(n / cols)
        tx = x0 + (x1 - x0) * gx; ty = y1 - (y1 - y0) * (1 - gy) * (.45 + .55 * spread)
        jx = jig * 12 * spread * math.sin(t * (2 + rnd(i, seed) * 3) + i)
        jy = jig * 12 * spread * math.cos(t * (2 + rnd(i, seed + 1) * 3) + i * 1.3)
        c.circ(tx + jx, ty + jy, r, col, a, bg=bg)

def hexgrid(cx, cy, R, nx=4, ny=3):
    """Vertices and edges of a honeycomb of hexagons (pointy-top), centred on (cx, cy)."""
    verts = {}; edges = set(); centres = []
    w = math.sqrt(3) * R
    for j in range(ny):
        for i in range(nx):
            hx = cx + (i - (nx - 1) / 2) * w + (w / 2 if j % 2 else 0) - w / 4
            hy = cy + (j - (ny - 1) / 2) * 1.5 * R
            centres.append((hx, hy))
            ids = []
            for k in range(6):
                an = math.pi / 6 + k * math.pi / 3
                p = (round(hx + R * math.cos(an), 1), round(hy + R * math.sin(an), 1))
                key = (round(p[0] / 4), round(p[1] / 4))
                verts.setdefault(key, p); ids.append(key)
            for k in range(6):
                edges.add(tuple(sorted((ids[k], ids[(k + 1) % 6]))))
    return verts, edges, centres

def lattice(c, cx, cy, R, form, a=1.0, t=0.0, holes=0.0, nx=4, ny=3, bg=BG):
    """Water molecules moving from a jumbled liquid (form 0) to a locked honeycomb (form 1)."""
    if a <= .01: return
    verts, edges, centres = hexgrid(cx, cy, R, nx, ny)
    keys = sorted(verts)
    pos = {}
    for n, k in enumerate(keys):
        vx, vy = verts[k]
        lx = cx + (rnd(n, 7) - .5) * R * nx * 1.2 + 26 * math.sin(t * 2.4 + n)
        ly = cy + (rnd(n, 8) - .5) * R * ny * .9 + 26 * math.cos(t * 2.1 + n * 1.7)
        pos[k] = (lerp(lx, vx, form), lerp(ly, vy, form))
    if holes > .01:
        for (hx, hy) in centres:
            c.circ(hx, hy, R * .55, None, a * holes, outline=FLOAT, ow=4, bg=bg)
    for e in edges:
        p, q = pos[e[0]], pos[e[1]]
        ba = a * form if form > .6 else a * .5 * (0.5 + .5 * math.sin(t * 7 + p[0]))   # liquid: bonds flicker
        if math.hypot(p[0] - q[0], p[1] - q[1]) < R * 1.6:
            c.line([p, q], BOND, 4, ba * (.6 if form < .6 else 1), bg)
    for n, k in enumerate(keys):
        molecule(c, pos[k][0], pos[k][1], .48, rnd(n, 3) * 6.28 * (1 - form) + (math.pi if n % 2 else 0) * form, a, bg)

def iceberg(c, x, wl, a=1.0, t=0.0, under=1.0):
    """An iceberg floating with its waterline at y = wl. under fades in the hidden part."""
    if a <= .01: return
    bob = 6 * math.sin(t * 1.3)
    c.rr(260, wl, 1660, 860, 20, WATER, a)
    below = [(x - 120, wl + bob), (x + 150, wl + bob), (x + 260, wl + 140 + bob), (x + 190, wl + 300 + bob), (x - 60, wl + 340 + bob), (x - 250, wl + 210 + bob)]
    poly(c, below, lerpc(WATER, ICED, .75), a * under, WATER)
    above = [(x - 120, wl + bob), (x - 60, wl - 70 + bob), (x + 10, wl - 50 + bob), (x + 60, wl - 110 + bob), (x + 150, wl + bob)]
    poly(c, above, ICE, a)
    c.line([(260 + k * 1400 / 40, wl + 4 * math.sin(t * 2 + k * .5)) for k in range(41)], WATERL, 5, a, WATER)

def fish(c, x, y, s=1.0, a=1.0, d=1, bg=WATER):
    if a <= .01: return
    c.circ(x, y, 26 * s, (255, 170, 80), a, bg=bg)
    poly(c, [(x - d * 20 * s, y), (x - d * 52 * s, y - 20 * s), (x - d * 52 * s, y + 20 * s)], (255, 140, 60), a, bg)
    c.circ(x + d * 12 * s, y - 6 * s, 5 * s, BG, a, bg=(255, 170, 80))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def person(c, x, y, s, col, a=1.0, bg=BG):
    c.circ(x, y - 30 * s, 16 * s, (225, 180, 150), a, bg=bg)
    c.rr(x - 15 * s, y - 12 * s, x + 15 * s, y + 34 * s, 12 * s, col, a, bg=bg)

def thumb_art(c):
    """A glass: the ice cube floats, a purple solid lies on the bottom."""
    surf, box = glass(c, 1530, 960, 520, 760, 1.0, .82)
    cube(c, 1440, surf + 30, 190, 1.0, bg=WATER)
    cube(c, 1650, 960 - 90, 150, 1.0, bg=WATER, col=OTHER, cold=lerpc(OTHER, BG, .4))
    c.check(1440, 300, 70, FLOAT); c.arrow(1650, 470, 1650, 720, SINK, 10, 1.0, 34)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(3), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Ice floats in your drink', 80, ICE, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'But most solids sink in their own liquid', 64, OTHER, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'Ice breaks the rule, and fish live because of it', 58, YE, a * hl(2), w='Bold')
        surf, _ = glass(c, 620, 790, 360, 500, a, .78, t)
        cube(c, 600, surf + 20 + 6 * math.sin(t * 1.6), 120, a, bg=WATER)
        cube(c, 690, surf + 26 + 6 * math.sin(t * 1.6 + 1), 90, a, bg=WATER)
        c.text(620, 835, 'ice in a drink', 40, ICE, a * fd(T(0), .8), w='Bold')
        k1 = a * hl(1) * (1 - hl(2))
        if k1 > 0:
            s2, _ = glass(c, 1300, 790, 360, 500, k1, .78, t + 1)
            fall = fd(T(1), .3, 1.4)
            cube(c, 1300, lerp(s2 + 10, 790 - 60, fall), 110, k1, bg=WATER, col=OTHER, cold=lerpc(OTHER, BG, .4))
            c.text(1300, 835, 'most other solids', 40, OTHER, k1, w='Bold')
            c.arrow(1520, 420, 1520, 680, SINK, 8, k1 * fall, 26)
        if hl(1) > 0: c.check(620, 240, 46, FLOAT, a * hl(1), fd(T(1), .8))
        k2 = a * hl(2)
        if k2 > 0:
            px0, px1, py0, py1 = 1060, 1600, 380, 790
            c.rr(px0, py0, px1, py1, 30, WATER, k2)
            c.rr(px0, py0, px1, py0 + 50, 16, ICE, k2, bg=WATER)
            for j in range(3):
                fish(c, px0 + 120 + ((t * 60 + j * 170) % 320), 520 + j * 80, .8, k2 * fd(T(2), .4 + j * .3), 1)
            c.text(1330, 835, 'a frozen lake', 40, ICE, k2, w='Bold')
    if T(3) > 0:
        m = fd(T(3), .2, .7)
        c.text(960, 330 + 30 * (1 - m), 'Ice Breaks a Rule', 116, INK, m, w='Bold')
        c.text(960, 470 + 30 * (1 - m), 'Almost Every Solid Follows', 100, YE, m, w='Bold')
        c.line([(960 - 380 * m, 580), (960 + 380 * m, 580)], CY, 8, m)
        cube(c, 820, 720, 110, m * fd(T(3), .5))
        c.arrow(820, 640, 820, 600, FLOAT, 8, m * fd(T(3), .7), 22)
        cube(c, 1100, 720, 110, m * fd(T(3), .8), col=OTHER, cold=lerpc(OTHER, BG, .4))
        c.arrow(1100, 800, 1100, 840, SINK, 8, m * fd(T(3), 1.0), 22)

def s_density(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Floating is about how tightly packed it is', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'A cork: much lighter than the same water', 64, CORK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Looser than water floats. Tighter sinks.', 66, YE, hl(2), w='Bold')
    k = 1 - hl(2)
    if k > 0:
        x0, y0, x1, y1 = 260, 250, 900, 780
        c.rr(x0, y0, x1, y1, 30, CARD, k * hl(0), outline=(60, 70, 120), ow=3)
        dots(c, x0 + 40, y0 + 40, x1 - 40, y1 - 40, 30, .9, k * hl(0), WATERL, t, bg=CARD)
        c.text(580, 825, 'water, up close (simplified)', 38, WATERL, k * hl(0), w='Bold')
        k1 = k * hl(1)
        if k1 > 0:
            c.rr(1000, 520, 1700, 820, 20, WATER, k1)
            c.line([(1000 + q * 700 / 30, 520 + 4 * math.sin(t * 2 + q * .6)) for q in range(31)], WATERL, 5, k1, WATER)
            bob = 6 * math.sin(t * 1.5)
            c.rr(1270, 440 + bob, 1430, 560 + bob, 26, CORK, k1)
            for q in range(5): c.circ(1300 + q * 28, 470 + bob + 30 * rnd(q, 2), 6, (150, 105, 65), k1, bg=CORK)
            c.text(1350, 380, 'cork', 52, CORK, k1 * fd(T(1), .5), w='Bold')
            c.arrow(1350, 330, 1350, 260, FLOAT, 8, k1 * fd(T(1), 1.0), 24)
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, n, col, x, up) in enumerate((('packed looser', 9, FLOAT, 560, True), ('packed tighter', 42, SINK, 1360, False))):
            kk = k2 * fd(T(2), j * 1.2)
            c.rr(x - 260, 300, x + 260, 720, 30, CARD, kk, outline=col, ow=4)
            dots(c, x - 220, 340, x + 220, 680, n, .9, kk, col, t, seed=j + 3, r=13, bg=CARD)
            c.text(x, 770, lab, 48, col, kk, w='Bold')
            c.text(x, 840, 'floats' if up else 'sinks', 52, INK, kk * fd(T(2), j * 1.2 + .6), w='Bold')

def s_solids(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Most substances: the solid is packed tighter', 62, OTHER, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Cooling slows molecules. They squeeze closer', 62, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Heavier for its size, so the solid sinks', 66, SINK, hl(2), w='Bold')
    k = 1 - hl(2)
    if k > 0:
        stages = (('warm liquid', 1.0, 1.6), ('cool liquid', .6, .7), ('solid', .0, 0.0))
        for j, (lab, sp, jig) in enumerate(stages):
            x = 420 + j * 540
            kk = k * (hl(0) if j == 0 else hl(1) * fd(T(1), .3 + (j - 1) * 1.6))
            if kk <= .01: continue
            c.rr(x - 220, 300, x + 220, 760, 26, CARD, kk, outline=OTHER, ow=3)
            if sp > 0: dots(c, x - 180, 340, x + 180, 720, 24, sp, kk, OTHER, t, seed=j + 2, jig=jig, r=14, bg=CARD)
            else:
                for q in range(24):
                    c.circ(x - 165 + (q % 6) * 66, 720 - 16 - (q // 6) * 32, 15, OTHER, kk, bg=CARD)
            c.text(x, 810, lab, 44, OTHER, kk, w='Bold')
            if j < 2: c.arrow(x + 240, 530, x + 300, 530, DIM, 6, kk * hl(1), 18)
    k2 = hl(2)
    if k2 > 0:
        surf, _ = glass(c, 960, 840, 420, 560, k2, .8, t)
        fall = fd(T(2), .4, 1.6)
        cube(c, 960, lerp(surf + 10, 840 - 70, fall), 130, k2, bg=WATER, col=OTHER, cold=lerpc(OTHER, BG, .4))
        c.text(1450, 520, 'a solid piece', 50, OTHER, k2 * fd(T(2), .3), w='Bold')
        c.text(1450, 600, 'in its own liquid', 44, INK, k2 * fd(T(2), .6), w='Bold')
        c.arrow(1250, 420, 1250, 720, SINK, 8, k2 * fall, 26)

def s_molecule(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, "Water is different because of its shape", 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'One oxygen, two hydrogens: a tiny letter V', 64, OXY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Neighbours pull on each other: hydrogen bonds', 60, BOND, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'In liquid water, the bonds keep breaking', 64, WATERL, hl(3), w='Bold')
    k = 1 - hl(3)
    if k > 0:
        if hl(2) < .01:
            sc = 1.0 + 1.6 * hl(0)
            molecule(c, 960, 520, sc + .05 * math.sin(t * 2), .0 + .15 * math.sin(t), k * hl(0))
            if hl(1) > 0:
                c.text(960, 380, 'oxygen', 46, OXY, k * hl(1), w='Bold')
                c.text(700, 760, 'hydrogen', 42, HYD, k * fd(T(1), .5), w='Bold')
                c.text(1220, 760, 'hydrogen', 42, HYD, k * fd(T(1), .8), w='Bold')
                c.text(960, 840, 'H2O', 50, DIM, k * fd(T(1), 1.4), w='Bold')
        else:
            k2 = k * hl(2)
            pts = [(700, 420, 0.3), (1220, 420, -2.6), (960, 700, 3.1)]
            for (x, y, an) in pts: molecule(c, x, y, 1.3, an, k2)
            for (x0, y0, x1, y1) in ((775, 470, 1140, 440), (1020, 650, 1180, 500), (900, 650, 760, 500)):
                n = 9
                for q in range(n):
                    if q % 2 == 0:
                        f0, f1 = q / n, (q + 1) / n
                        c.line([(lerp(x0, x1, f0), lerp(y0, y1, f0)), (lerp(x0, x1, f1), lerp(y0, y1, f1))], BOND, 7, k2 * fd(T(2), .8))
            c.text(1550, 700, 'weak pull', 44, BOND, k2 * fd(T(2), 1.2), w='Bold')
            c.text(1550, 760, '= hydrogen bond', 40, INK, k2 * fd(T(2), 1.6), w='Bold')
    k3 = hl(3)
    if k3 > 0:
        lattice(c, 760, 520, 120, 0.0, k3, t)
        c.text(1500, 450, 'molecules jostle', 50, WATERL, k3 * fd(T(3), .4), w='Bold')
        c.text(1500, 530, 'and crowd close', 50, WATERL, k3 * fd(T(3), .9), w='Bold')
        c.text(1500, 620, 'bonds break and re-form', 38, BOND, k3 * fd(T(3), 1.6), w='Medium')

def s_freeze(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Freeze it, and the bonds lock in place', 66, BOND, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Six-sided rings, like a honeycomb', 70, ICE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Open space inside: ice takes about 9% more room', 58, FLOAT, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'A crowd in a lift vs. the same crowd in a ring', 58, YE, hl(3), w='Bold')
    k = 1 - hl(3)
    if k > 0:
        form = fd(T(0), .3, 2.2)
        lattice(c, lerp(960, 720, hl(1)), 520, 120, form, k, t, holes=hl(2) * fd(T(2), .2, 1.0))
        if hl(1) > 0 and hl(2) < 1:
            c.text(1620, 480, 'hexagons', 50, ICE, k * hl(1) * (1 - hl(2)), w='Bold')
            c.text(1620, 550, 'held at arm\'s length', 38, BOND, k * hl(1) * (1 - hl(2)) * fd(T(1), .8), w='Medium')
        k2 = k * hl(2)
        if k2 > 0:
            bx = 1480
            c.rr(bx - 150, 760 - 300, bx - 30, 760, 14, WATER, k2 * fd(T(2), .6))
            c.text(bx - 90, 800, 'water', 34, WATERL, k2 * fd(T(2), .6), w='Bold')
            hh = 300 * 1.09 * fd(T(2), 1.0, 1.0) if T(2) > 1.0 else 0
            c.rr(bx + 50, 760 - max(hh, 1), bx + 170, 760, 14, ICE, k2 * fd(T(2), 1.0))
            c.text(bx + 110, 800, 'ice', 34, ICE, k2 * fd(T(2), 1.0), w='Bold')
            c.text(bx + 230, 760 - 320, '+9%', 46, FLOAT, k2 * fd(T(2), 2.0), 'lm', 'Bold')
            c.text(bx + 10, 845, 'same amount of water', 30, DIM, k2 * fd(T(2), 1.4), w='Medium')
    k3 = hl(3)
    if k3 > 0:
        c.rr(330, 300, 750, 780, 20, CARD, k3, outline=SINK, ow=4)
        for q in range(12):
            person(c, 400 + (q % 4) * 95 + 6 * math.sin(t * 3 + q), 400 + (q // 4) * 140, 1.2, SINK, k3, bg=CARD)
        c.text(540, 830, 'in a lift: packed tight', 40, SINK, k3, w='Bold')
        kk = k3 * fd(T(3), 1.2)
        for q in range(12):
            an = q / 12 * 2 * math.pi
            px, py = 1360 + 220 * math.cos(an), 540 + 220 * math.sin(an)
            nx_, ny_ = 1360 + 220 * math.cos(an + math.pi / 6), 540 + 220 * math.sin(an + math.pi / 6)
            c.line([(px, py), (nx_, ny_)], BOND, 4, kk)
            person(c, px, py, 1.2, ICED, kk)
        c.text(1360, 830, 'holding hands in a ring', 40, ICE, kk, w='Bold')
        c.text(1360, 540, 'space', 40, FLOAT, kk * fd(T(3), 2.0), w='Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 208, 'How much of an iceberg is under the water?', 44, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'B: around 90% is hidden below', 68, FLOAT, ans, w='Bold')
    wl = 420
    iceberg(c, 960, wl, m, t, under=ans)
    if ans < 1 and m > 0:
        c.text(960, wl + 200, '?', 120, YE, m * fd(T(0), 1.0) * (1 - ans), w='Bold', bg=WATER)
    kc = hl(1) * (1 - ans)
    if kc > 0:
        for j, (lab, txt, x) in enumerate((('A', 'about half', 470), ('B', 'about nine tenths', 1450))):
            kk = kc * fd(T(1), j * 1.4)
            c.rr(x - 250, 260, x + 250, 360, 30, CARD, kk, outline=CY, ow=3)
            c.circ(x - 200, 310, 30, CY, kk, bg=CARD); c.text(x - 200, 310, lab, 38, BG, kk, w='Bold', bg=CY)
            c.text(x + 30, 310, txt, 38, INK, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        ring(c, 1700, 600, 60, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        c.line([(1260, wl), (1260, wl + 340)], FLOAT, 6, ans, WATER)
        c.text(1290, wl + 170, '~90%', 52, FLOAT, ans * fd(T(3), .6), 'lm', 'Bold', bg=WATER)
        c.text(1290, wl - 50, '~10%', 40, ICE, ans * fd(T(3), .9), 'lm', 'Bold')

def s_pipe(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'That extra 9% pushes hard', 72, FLOAT, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, "Water freezing in a pipe has nowhere to go", 62, ICE, hl(1), w='Bold')
    x0, x1, yc, r = 260, 1660, 520, 90
    c.rr(x0, yc - r - 26, x1, yc + r + 26, 40, STEEL, 1.0)
    grow = fd(T(0), .3, 2.0) * .5 + .5 * fd(T(1), .2, 2.4)
    c.rr(x0 + 10, yc - r, x1 - 10, yc + r, 30, WATER, 1.0, bg=STEEL)
    iw = (x1 - x0 - 20) * grow
    if iw > 20:
        c.rr(960 - iw / 2, yc - r, 960 + iw / 2, yc + r, 30, ICE, 1.0, bg=STEEL)
        for q in range(int(iw / 120)):
            xx = 960 - iw / 2 + 60 + q * 120
            c.line([(xx, yc - 50), (xx + 30, yc + 40)], ICED, 4, 1.0, ICE)
    if grow > .3:
        for d in (-1, 1):
            c.arrow(960 + d * iw / 2 - d * 40, yc, 960 + d * iw / 2 + d * 40, yc, FLOAT, 7, clamp((grow - .3) * 3), 20)
    if hl(1) > 0:
        cr = fd(T(1), 2.2, .6)
        if cr > 0:
            pts = [(1080, yc - r - 26), (1060, yc - r - 70 * cr), (1100, yc - r - 110 * cr), (1075, yc - r - 160 * cr)]
            c.line(pts, SINK, 8, cr)
            c.text(1260, yc - r - 140, 'crack!', 56, SINK, cr, 'lm', 'Bold')
        c.text(960, 780, 'why water pipes can burst in a hard frost', 44, INK, fd(T(1), 1.0), w='Bold')
        c.text(960, 840, 'simplified drawing', 28, DIM, fd(T(1), 1.4), w='Medium')

def s_lake(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Winter: a lake cools from the top', 70, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Water is densest at about 4 °C: it sinks', 64, WATERL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Colder water stays on top and freezes', 66, ICE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Under the lid of ice, fish stay alive', 66, FLOAT, hl(3), w='Bold')
    x0, x1, y0, y1 = 260, 1660, 330, 830
    c.rr(x0, y0, x1, y1, 30, WATER, 1.0)
    c.rr(x0, y1 - 140, x1, y1, 30, (60, 50, 40), 1.0, bg=WATER)
    if hl(0) > 0:
        for q in range(6):
            yy = y0 + 20 + ((t * 60 + q * 40) % 120)
            c.arrow(400 + q * 230, y0 - 50, 400 + q * 230, y0 - 10, ICED, 5, hl(0) * (1 - hl(2)) * .8, 14)
        c.text(1780, y0 - 30, 'icy air', 34, ICED, hl(0) * (1 - hl(2)), 'mm', 'Bold')
    if hl(1) > 0:
        k1 = hl(1)
        c.rr(x0 + 10, y1 - 260, x1 - 10, y1 - 150, 20, (30, 76, 130), k1, bg=WATER)
        c.text(960, y1 - 205, '4 °C: the densest water sinks', 40, INK, k1 * fd(T(1), .4), w='Bold', bg=(30, 76, 130))
        for q in range(4):
            yy = y0 + 60 + ((t * 70 + q * 50) % 180)
            c.arrow(500 + q * 300, yy, 500 + q * 300, yy + 40, WATERL, 5, k1 * (1 - hl(2)), 14)
    if hl(2) > 0:
        th = 60 * fd(T(2), .3, 1.6)
        c.rr(x0, y0, x1, y0 + th, 16, ICE, hl(2), bg=WATER)
        c.text(960, y0 + 32, '0 °C ice', 36, BG, hl(2) * fd(T(2), 1.4), w='Bold', bg=ICE)
    if hl(3) > 0:
        for j in range(4):
            fx = 400 + ((t * 70 * (1 + j * .2) + j * 300) % 1100)
            fish(c, fx, 560 + j * 40 - (j % 2) * 120, .9, hl(3) * fd(T(3), j * .3), 1)

RECAPS = [('1', 'Most solids sink:', 'freezing packs', 'them tighter', OTHER),
          ('2', 'Ice locks into', 'open rings, so it', 'takes more space', ICE),
          ('3', 'Icebergs, pipes,', 'and fish under', 'the ice', FLOAT)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 150, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    c.rr(120, 640, 1800, 860, 24, WATER, fd(T(0)) * out)
    c.line([(120 + q * 1680 / 50, 640 + 5 * math.sin(t * 2 + q * .5)) for q in range(51)], WATERL, 5, fd(T(0)) * out, WATER)
    for i, (nn, l1, l2, l3, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 420 + i * 540
        if m <= .01: continue
        bob = 8 * math.sin(t * 1.4 + i) + 60 * (1 - fd(T(i + 1)))
        yt = 330 + bob
        c.rr(x - 220, yt, x + 220, yt + 380, 40, CARD, m, outline=col, ow=5)
        c.circ(x, yt + 50, 34, col, m, bg=CARD); c.text(x, yt + 50, nn, 40, BG, m, w='Bold', bg=col)
        c.text(x, yt + 140, l1, 40, col, m, w='Bold', bg=CARD)
        c.text(x, yt + 205, l2, 36, INK, m, w='Bold', bg=CARD)
        c.text(x, yt + 260, l3, 36, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Drop an ice cube in a drink, and it floats. That's actually strange.",
            "For most substances, the solid sinks in its own liquid.",
            "Ice breaks that rule. And every winter, fish stay alive because of it.",
            "Here's why ice floats."], s_hook),
 ('1  ·  FLOATING', ["First, what decides if something floats? How tightly it's packed.",
            "A cork floats because it's much lighter than the same amount of water.",
            "Anything packed looser than water floats. Anything packed tighter sinks."], s_density),
 ('2  ·  MOST SOLIDS', ["For most substances, the solid is packed tighter than the liquid.",
            "As a liquid cools, its molecules slow down and squeeze closer. When it freezes, they pack tighter still.",
            "So the solid is heavier for its size, and it sinks."], s_solids),
 ('3  ·  THE WATER MOLECULE', ["Water is different, because of its shape.",
            "Each water molecule is one oxygen and two hydrogens, a bit like a tiny letter V.",
            "The hydrogens of one molecule are pulled toward the oxygen of its neighbours. These weak pulls are called hydrogen bonds.",
            "In liquid water, those bonds keep breaking and forming again, so the molecules jostle and crowd close."], s_molecule),
 ('4  ·  FREEZING', ["When water freezes, the bonds lock in place.",
            "They hold every molecule at arm's length, in six-sided rings, like a honeycomb.",
            "Those rings have open space in the middle. So ice takes up about nine percent more room than the same water.",
            "Think of a crowd squeezed into a lift, and the same people holding hands in a big ring."], s_freeze),
 ('5  ·  QUICK QUESTION', ["Quick question. An iceberg floats. How much of it is under the water?",
            "A, about half. Or B, about nine tenths.",
            "Three, two, one.",
            "B. Around ninety percent of an iceberg is hidden below. Ice is only a little lighter than water, so most of it sits low."], s_quiz),
 ('6  ·  BURST PIPES', ["That extra nine percent pushes hard.",
            "It's why water pipes can burst in a hard frost. The freezing water has to expand, and inside a pipe, it has nowhere to go."], s_pipe),
 ('7  ·  FROZEN LAKES', ["It matters for life, too. In winter, a lake cools from the top.",
            "Water is densest at about four degrees, so that water sinks to the bottom.",
            "Colder water stays on top, and freezes into a lid of ice.",
            "Underneath, the water stays liquid all winter, and the fish survive."], s_lake),
 ('RECAP', ["So remember three things.",
            "One. Most solids sink, because freezing packs their molecules tighter.",
            "Two. Water's hydrogen bonds lock into open rings, so ice takes more space, and floats.",
            "Three. That's why icebergs hide most of their size, pipes can burst, and fish survive under the ice.",
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
    if T(1) < 0: remap(s_hook, {0: (0, -9), 1: 0})(c, T, t)
    else: remap(s_freeze, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

def short_mol(c, T, t):
    if T(1) < 0: remap(s_molecule, {0: (0, -9), 1: (0, -9), 2: 0})(c, T, t)
    else: remap(s_molecule, {0: (1, -9), 1: (1, -9), 2: (1, -9), 3: 1})(c, T, t)

def short_freeze(c, T, t):
    if T(1) < 0: remap(s_freeze, {0: 0, 1: (0, 2.2)})(c, T, t)
    else: remap(s_freeze, {0: (1, -9), 1: (1, -9), 2: 1})(c, T, t)

# The Short: its own complete mini-story (hook -> hydrogen bonds -> open rings when frozen -> answer).
SHORT_SCENES = [
 ('THE HOOK', ["Why does ice float, when most solids sink in their own liquid?",
               "The answer is strange. When water freezes, it takes up more space, not less."],
              short_hook),
 ('THE BONDS', ["Water molecules pull on each other with weak links, called hydrogen bonds.",
                "In liquid water, those bonds keep breaking and forming again, so the molecules tumble around and crowd close together."],
               short_mol),
 ('THE RINGS', ["When water freezes, the bonds lock the molecules into open, six-sided rings, like a honeycomb.",
                "That leaves gaps. So ice takes up about nine percent more room than the same water."],
               short_freeze),
 ('THE ANSWER', ["So why does ice float?",
                 "Its molecules are locked far apart, so a piece of ice is lighter than the same amount of water. And lighter things float."],
                card('Why does ice float?', 'Freezing spreads water out.')),
]
SHORT_HITS = [(3, 1, 0.0)]
