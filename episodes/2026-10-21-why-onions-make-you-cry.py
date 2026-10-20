"""Episode: The Onion's Chemical Trap: Why Cutting It Makes You Cry"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why Onions Make You Cry"                 # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.97
SHORT_HOOK = "Why do onions make you cry?"              # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 2, 0.0), (6, 2, 0.0)]          # title card, the missing second enzyme, quiz answer
THUMB = ['CUT IT, AND', 'THE ONION', 'FIGHTS BACK']
MUSIC_LEVEL = 0.006                                     # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                          # no dead air before the first word (lesson of 2026-10-19)
CAPTION_FIXES = {'sin-propane-thial S-oxide': 'syn-propanethial-S-oxide', 'thirty seconds': '30 seconds',
                 'Ig Nobel': 'Ig Nobel', 'two thousand and two': '2002'}
# Applied lesson (learnings.md, 2026-10-21): carry ONE plain everyday example through the whole video
# (outlier economics explainer whose viewers said the single everyday example "really clicked").
# Here: the glow stick. Two things kept apart until you break it; it returns in the cell scene, the Short and the recap.

SKIN = (214, 146, 78); SKIN_D = (160, 96, 46); FLESH = (246, 236, 214); RING = (214, 190, 150)
LEAF = (110, 200, 120); SOIL = (74, 52, 40); GAS = (170, 255, 140); WALL = (120, 200, 150)
STEEL = (200, 206, 224); HANDLE = (92, 64, 52); GARLIC = (236, 232, 220)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def ell(c, x, y, rx, ry, fill=None, a=1.0, outline=None, ow=3, bg=BG):
    if a <= 0.01: return
    c.d.ellipse(((x - rx) * c.k, (y - ry) * c.k, (x + rx) * c.k, (y + ry) * c.k),
                fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None, width=int(ow * c.k))

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, BG, a, w='Bold', bg=col)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def onion(c, x, y, r, a=1.0, bg=BG):
    """Whole onion: bulb, papery tip, roots."""
    if a <= 0.01: return
    poly(c, [(x - r * .42, y - r * .78), (x - r * .08, y - r * 1.42), (x + r * .08, y - r * 1.42), (x + r * .42, y - r * .78)], SKIN, a, bg)
    for dx in (-.25, 0, .22):
        c.line([(x + r * dx, y + r * .92), (x + r * dx * 1.5, y + r * 1.12)], SKIN_D, max(2, r * .03), a, bg)
    c.circ(x, y, r, SKIN, a, bg=bg)
    for k in (.38, .72):
        ell(c, x, y, r * k, r * .98, None, a * .8, outline=SKIN_D, ow=max(2, r * .025), bg=SKIN)
    ell(c, x - r * .35, y - r * .35, r * .16, r * .1, (240, 190, 130), a * .7, bg=SKIN)

def half(c, x, y, r, a=1.0, bg=BG):
    """Onion cut in half, seen from the cut face: rings."""
    if a <= 0.01: return
    ell(c, x, y, r, r * .9, SKIN, a, bg=bg)
    ell(c, x, y, r * .93, r * .83, FLESH, a, bg=SKIN)
    for k in (.75, .55, .36, .18):
        ell(c, x, y + r * .05 * (1 - k), r * .93 * k, r * .83 * k, None, a, outline=RING, ow=max(2, r * .03), bg=FLESH)

def knife(c, x, y, s, a=1.0, bg=BG, dull=False):
    """Knife, blade pointing left, edge at the bottom. (x, y) = where blade meets handle."""
    if a <= 0.01: return
    poly(c, [(x, y - s * .28), (x - s * 1.6, y - s * .1), (x - s * 1.75, y + s * .1), (x, y + s * .1)], STEEL, a, bg)
    if not dull:
        c.line([(x - s * 1.7, y + s * .08), (x, y + s * .08)], (250, 252, 255), max(2, s * .03), a, bg)
    else:
        for j in range(6):
            xx = x - s * (.2 + j * .26)
            c.line([(xx, y + s * .1), (xx + s * .05, y + s * .02)], (130, 136, 160), max(2, s * .03), a, STEEL)
    c.rr(x, y - s * .2, x + s * .9, y + s * .12, s * .1, HANDLE, a, bg=bg)

def wisp(c, x, y, h, t, a=1.0, col=GAS, n=3, spread=60, speed=60, bg=BG, drift=0.0):
    """Rising gas: wavy strands that move upward and fade (drift > 0 bends them to the right)."""
    if a <= 0.01: return
    for j in range(n):
        ph = (t * speed / h + j / n) % 1.0
        x0 = x + (j - (n - 1) / 2) * spread
        pts = []
        for u in range(9):
            q = u / 8; yy = y - h * (ph * .6 + q * .4)
            pts.append((x0 + 14 * math.sin(q * 6 + t * 3 + j) + drift * (ph * .6 + q * .4), yy))
        c.line(pts, col, 7, a * (1 - ph) * .9, bg)

def eye(c, x, y, s, a=1.0, red=0.0, t=0.0, bg=BG, tears=0.0):
    """Front view of an open eye. red: irritation 0..1. tears: falling drops 0..1."""
    if a <= 0.01: return
    N = 24
    top = [(x - s + 2 * s * i / N, y - s * .55 * math.sin(math.pi * i / N)) for i in range(N + 1)]
    bot = [(x + s - 2 * s * i / N, y + s * .5 * math.sin(math.pi * i / N)) for i in range(N + 1)]
    sclera = tuple(int(v * (1 - red * .35) + w * red * .35) for v, w in zip((236, 239, 250), (255, 120, 140)))
    poly(c, top + bot, sclera, a, bg)
    c.line(top, (60, 40, 50), max(3, s * .05), a, bg)
    c.line(bot, (90, 60, 70), max(2, s * .03), a, bg)
    c.circ(x, y, s * .42, (70, 120, 190), a, bg=sclera)
    c.circ(x, y, s * .2, (12, 14, 28), a, bg=(70, 120, 190))
    c.circ(x - s * .12, y - s * .12, s * .07, INK, a, bg=(12, 14, 28))
    if tears > .01:
        for j in range(3):
            ph = (t * .7 + j / 3) % 1
            xx = x + s * (.25 + .2 * j); yy = y + s * .45 + ph * s * .9
            drop(c, xx, yy, s * .06, CY, a * tears * (1 - ph * .6))

def drop(c, x, y, r, col, a=1.0, bg=BG):
    if a <= 0.01: return
    poly(c, [(x - r * .8, y - r * .3), (x, y - r * 2.2), (x + r * .8, y - r * .3)], col, a, bg)
    c.circ(x, y, r, col, a, bg=bg)

S_DOTS = [(470 + 560 * ((i * .618034 + .1) % 1), 260 + 400 * ((i * .414214 + .3) % 1)) for i in range(16)]
def cell(c, x0, y0, x1, y1, a=1.0, burst=0.0, react=0.0, t=0.0, labels=True, bg=BG):
    """One onion cell. Yellow = sulfur compounds; cyan = enzyme inside a sealed pocket (right).
    burst 0..1: pocket bursts and the enzyme spreads; react 0..1: the yellow dots turn pink (the unstable acid)."""
    if a <= 0.01: return
    w, h = x1 - x0, y1 - y0
    c.rr(x0, y0, x1, y1, 40, (30, 52, 50), a, outline=WALL, ow=6, bg=bg)
    inner = (30, 52, 50)
    px, py, pr = x0 + w * .78, y0 + h * .5, h * .27
    for i, (sx, sy) in enumerate(S_DOTS):
        xx = x0 + (sx - 470) / 560 * w * .55 + w * .06 + 6 * math.sin(t * 1.5 + i)
        yy = y0 + (sy - 260) / 400 * h * .8 + h * .1 + 6 * math.cos(t * 1.3 + i)
        k = clamp(react * 1.6 - (i / 16) * .6)
        col = tuple(int(YE[j] + (PK[j] - YE[j]) * k) for j in range(3))
        c.circ(xx, yy, max(8, h * .028), col, a, bg=inner)
    ok = 1 - fd(burst, 0, .25)
    if ok > .01:
        c.circ(px, py, pr, (24, 60, 78), a * ok, outline=CY, ow=5, bg=inner)
    for i in range(8):
        ang = i * math.pi / 4 + t * .6
        rr = pr * .55 + burst * (w * .45) * (.5 + .5 * ((i * 37) % 7) / 7)
        xx = px + rr * math.cos(ang) * (1.4 if math.cos(ang) < 0 else .25)
        yy = py + min(h * .4, rr * .6) * math.sin(ang)
        c.circ(xx, yy, max(9, h * .03), CY, a, bg=inner)
        c.line([(xx - h * .02, yy), (xx + h * .02, yy)], BG, 3, a, CY)
    if labels:
        c.text(x0 + w * .33, y1 + 40, 'sulfur compounds', 32, YE, a * (1 - react), w='Bold')
        c.text(x0 + w * .33, y1 + 40, 'an unstable acid', 32, PK, a * react, w='Bold')
        c.text(px, y1 + 40, 'enzyme (alliinase)', 32, CY, a, w='Bold')

def glowstick(c, x, y, L, a=1.0, snap=0.0, glow=0.0, t=0.0, bg=BG):
    """Horizontal glow stick centred at (x, y). snap: inner vial cracks; glow: lights up."""
    if a <= 0.01: return
    ang = .14 * math.sin(math.pi * clamp(snap)) if snap < 1 else 0
    th = L * .09
    if glow > .01:
        for k, al in ((2.6, .12), (1.8, .2)):
            c.rr(x - L / 2 - th * k * .4, y - th * k, x + L / 2 + th * k * .4, y + th * k, th * k, GR, a * glow * al)
    tube = tuple(int(v) for v in mix(GR, .25 + .75 * glow, (60, 70, 110)))
    def seg(x0, x1, dy0, dy1):
        poly(c, [(x0, y - th / 2 + dy0), (x1, y - th / 2 + dy1), (x1, y + th / 2 + dy1), (x0, y + th / 2 + dy0)], tube, a, bg)
    bend = L * .5 * ang
    seg(x - L / 2, x, bend, 0); seg(x, x + L / 2, 0, bend)
    c.circ(x - L / 2, y + bend, th / 2, tube, a, bg=bg); c.circ(x + L / 2, y + bend, th / 2, tube, a, bg=bg)
    if glow < .99:
        va = a * (1 - glow)
        vx0, vx1 = x - L * .3, x + L * .3
        if snap < .5:
            c.rr(vx0, y - th * .22, vx1, y + th * .22, th * .2, (240, 220, 120), va, bg=tube)
        else:
            c.rr(vx0, y - th * .22, x - 8, y + th * .22, th * .2, (240, 220, 120), va, bg=tube)
            c.rr(x + 8, y - th * .22, vx1, y + th * .22, th * .2, (240, 220, 120), va, bg=tube)
            c.line([(x - 10, y - th * .4), (x + 6, y), (x - 6, y + th * .1), (x + 10, y + th * .4)], INK, 4, va, tube)

def garlic(c, x, y, r, a=1.0, bg=BG):
    if a <= 0.01: return
    poly(c, [(x - r * .3, y - r * .7), (x, y - r * 1.35), (x + r * .3, y - r * .7)], GARLIC, a, bg)
    c.circ(x, y, r, GARLIC, a, bg=bg)
    for k in (-.55, -.2, .2, .55):
        ell(c, x + r * k * .9, y, r * .22, r * .9, None, a, outline=(200, 194, 178), ow=max(2, r * .03), bg=GARLIC)

def brain(c, x, y, s, a=1.0, hot=0.0, bg=BG):
    if a <= 0.01: return
    col = tuple(int(v) for v in mix(PK, .55 + .45 * hot, (90, 70, 110)))
    for dx, dy, r in ((-.45, .05, .5), (.0, -.15, .58), (.45, .05, .5), (-.2, .3, .45), (.25, .3, .45)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)
    c.line([(x, y - s * .7), (x, y + s * .6)], mix(BG, .5, col), max(3, s * .05), a, col)
    for j in range(3):
        yy = y - s * .3 + j * s * .3
        c.line([(x - s * .7, yy), (x - s * .4, yy - s * .1), (x - s * .15, yy)], mix(BG, .4, col), max(2, s * .04), a, col)
        c.line([(x + s * .15, yy), (x + s * .4, yy - s * .1), (x + s * .7, yy)], mix(BG, .4, col), max(2, s * .04), a, col)

def snowflake(c, x, y, r, a=1.0, bg=BG, col=CY):
    for k in range(6):
        u = k * math.pi / 3
        x1, y1 = x + r * math.cos(u), y + r * math.sin(u)
        c.line([(x, y), (x1, y1)], col, max(3, r * .1), a, bg)
        for s_ in (.55,):
            bx, by = x + r * s_ * math.cos(u), y + r * s_ * math.sin(u)
            for d in (.6, -.6):
                c.line([(bx, by), (bx + r * .28 * math.cos(u + d), by + r * .28 * math.sin(u + d))], col, max(3, r * .08), a, bg)

def fan(c, x, y, r, a=1.0, t=0.0, bg=BG):
    if a <= 0.01: return
    c.circ(x, y, r, None, a, outline=DIM, ow=5, bg=bg)
    for k in range(3):
        u = t * 6 + k * 2 * math.pi / 3
        pts = [(x, y), (x + r * .85 * math.cos(u - .35), y + r * .85 * math.sin(u - .35)), (x + r * .9 * math.cos(u), y + r * .9 * math.sin(u)),
               (x + r * .85 * math.cos(u + .35), y + r * .85 * math.sin(u + .35))]
        poly(c, pts, CY, a, bg)
    c.circ(x, y, r * .12, INK, a, bg=CY)
    c.rr(x - 8, y + r, x + 8, y + r * 1.5, 4, DIM, a, bg=bg); c.rr(x - r * .5, y + r * 1.5, x + r * .5, y + r * 1.62, 6, DIM, a, bg=bg)

def grub(c, x, y, s, a=1.0, t=0.0, bg=BG):
    if a <= 0.01: return
    for j in range(5):
        c.circ(x + j * s * .55, y + 6 * math.sin(t * 4 + j), s * (.5 - j * .05), (230, 200, 170), a, bg=bg)
    c.circ(x - s * .15, y - s * .15, s * .08, BG, a, bg=(230, 200, 170))

def thumb_art(c):
    half(c, 1500, 560, 260, 1)
    wisp(c, 1500, 420, 340, 1.3, 1, n=4, spread=90)
    eye(c, 1500, 190, 150, 1, red=.8)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), .3, .5)
    if a > 0:
        cut = fd(T(1), .2, .5) if T(1) > -.1 else 0.0
        # motion from frame one: the knife bobs above the onion, the eye watches
        kx = 720 + 30 * math.sin(t * 2.2) * (1 - cut); ky = 270 + 40 * math.sin(t * 3.1) * (1 - cut) + 190 * cut
        if cut < 1:
            onion(c, 640, 560, 170 * (1 - cut * .15), a * (1 - cut))
        if cut > 0:
            half(c, 520 - 40 * cut, 600, 150, a * cut); half(c, 800 + 40 * cut, 600, 150, a * cut)
            wisp(c, 660, 500, 330, t, a * fd(T(1), .8, 1.2), n=4, spread=80, drift=420)
        knife(c, kx + 300, ky, 150, a * (1 - .7 * cut))
        red = fd(T(1), 1.5, 2.0) if T(1) > -.1 else 0.0
        eye(c, 1420, 430, 190, a, red=red, t=t, tears=fd(T(1), 2.4, 1.0) if T(1) > -.1 else 0)
        c.text(960, 150, 'A whole onion: no tears.' if cut < .5 else 'Cut it: tears in about 30 s.', 62, INK if cut < .5 else YE, a, w='Bold')
        if T(1) > -.1:
            p = clamp(T(1) / 2.6)
            ring(c, 1420, 760, 52, p, YE, a * hl(1), 9)
            c.text(1420, 760, f'{int(30 * p)} s', 30, YE, a * hl(1), w='Bold')
    if T(2) > 0:
        m = fd(T(2), .45, .7)
        c.text(960, 330 + 30 * (1 - m), "The Onion's", 130, INK, m, w='Bold')
        c.text(960, 490 + 30 * (1 - m), 'Chemical Trap', 130, YE, m, w='Bold')
        c.line([(960 - 380 * m, 600), (960 + 380 * m, 600)], GAS, 8, m)
        c.text(960, 690, 'Why cutting one makes you cry', 46, DIM, fd(T(2), 1.2), w='Medium')

def s_glow(c, T, t):
    hl = lambda i: hl_(T, i)
    k2 = hl(2)
    c.text(960, 140, 'Think of a glow stick', 66, INK, hl(0) * (1 - k2), w='Bold')
    c.text(960, 140, 'An onion works the same way', 66, INK, k2, w='Bold')
    snap = clamp(T(1) / 1.2) if T(1) > -.1 else 0.0
    glow = fd(T(1), 1.4, 1.0) if T(1) > -.1 else 0.0
    gx = 960 - 420 * fd(T(2), 0, .8) if T(2) > -.1 else 960
    L = 900 - 420 * (fd(T(2), 0, .8) if T(2) > -.1 else 0)
    glowstick(c, gx, 440, L, hl(0), snap, glow, t)
    if k2 <= 0:
        c.text(960, 640, 'two liquids, kept apart: nothing happens', 40, DIM, hl(0) * (1 - hl(1)), w='Bold')
        c.text(960, 640, 'snap: they mix, and it lights up', 44, GR, hl(1), w='Bold')
    else:
        c.text(540, 640, 'snap + mix = light', 40, GR, k2, w='Bold')
        half(c, 1380, 440, 190, k2)
        knife(c, 1560 + 30 * math.sin(t * 2.5), 300, 110, k2)
        c.text(1380, 640, 'cut + mix = stinging gas', 40, GAS, k2 * fd(T(2), .6), w='Bold')
        c.text(960, 780, 'Every cell keeps two ingredients apart', 44, INK, k2 * fd(T(2), 1.2), w='Bold')

def s_cell(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Inside one onion cell', 66, INK, hl(0), w='Bold')
    burst = fd(T(2), .6, 1.4) if T(2) > -.1 else 0.0
    react = fd(T(2), 1.8, 1.6) if T(2) > -.1 else 0.0
    cell(c, 420, 210, 1500, 700, hl(0), burst, react, t, labels=False)
    lo = 1 - (fd(T(2), 1.6, .3) if T(2) > -.1 else 0.0); li = fd(T(2), 2.0, .4) if T(2) > -.1 else 0.0
    c.text(430, 750, 'sulfur compounds', 38, YE, hl(0) * fd(T(0), 1.0) * lo, 'lm', 'Bold')
    c.text(430, 805, 'harmless on their own', 32, DIM, hl(0) * fd(T(0), 1.8) * lo, 'lm', 'Medium')
    c.text(430, 750, 'they react', 38, PK, li, 'lm', 'Bold')
    bo = 1 - (fd(T(2), .4, .3) if T(2) > -.1 else 0.0); bi = fd(T(2), .8, .4) if T(2) > -.1 else 0.0
    c.text(1490, 750, 'enzyme, sealed in a pocket', 34, CY, hl(1) * bo, 'rm', 'Bold')
    c.text(1490, 750, 'pocket bursts', 38, CY, bi, 'rm', 'Bold')
    if T(2) > -.1:
        p = fd(T(2), 0, .7)
        c.line([(1580, 160), (1580 - 520 * p, 160 + 640 * p)], INK, 6, hl(2) * (1 - fd(T(2), 1.2, .5)))
        if 0 < p < 1: knife(c, 1580 - 520 * p + 120, 160 + 640 * p - 20, 90, 1)
    c.text(1490, 820, 'alliinase', 40, CY, hl(1) * (1 - hl(2)), 'rm', 'Bold')

def s_gas(c, T, t):
    hl = lambda i: hl_(T, i)
    out = 1 - fd(T(2), -.1, .4)
    c.text(960, 130, 'From acid to gas', 66, INK, hl(0) * out, w='Bold')
    if out > 0:
        nodes = [(380, 'sulfur + enzyme', YE, 0), (960, 'unstable acid', PK, 0), (1540, 'stinging gas', GAS, 1)]
        for j, (x, lab, col, li) in enumerate(nodes):
            k = (hl(0) * fd(T(0), j * .9) if j < 2 else hl(1) * fd(T(1), 2.4)) * out
            if k <= 0: continue
            c.rr(x - 230, 300, x + 230, 470, 30, CARD, k, outline=col, ow=5)
            c.text(x, 385, lab, 42, col, k, w='Bold', bg=CARD)
            if j: c.arrow(x - 345, 385, x - 245, 385, DIM, 6, k, 22)
        k1 = hl(1) * out
        if k1 > 0:
            c.text(1250, 540, 'second enzyme', 36, CY, k1, w='Bold')
            wisp(c, 1540, 290, 160, t, k1 * fd(T(1), 2.6), n=3, spread=70)
            c.text(960, 690, 'syn-propanethial-S-oxide', 56, GAS, k1 * fd(T(1), 3.0), w='Bold')
            c.text(960, 760, 'it evaporates easily: a gas', 34, DIM, k1 * fd(T(1), 3.5), w='Medium')
    if T(2) > -.1:
        m = fd(T(2), .1)
        c.text(960, 130, 'Up off the board', 66, INK, m, w='Bold')
        c.rr(220, 690, 860, 740, 18, (120, 84, 60), m)
        half(c, 540, 630, 140, m)
        wisp(c, 540, 560, 360, t, m, n=4, spread=80)
        # simplified curve: gas released over time, peaking about 30 s after the cut
        ox, oy, gw, gh = 1060, 760, 640, 400
        c.line([(ox, oy - gh), (ox, oy), (ox + gw, oy)], DIM, 4, m)
        pts = []
        p = fd(T(2), .6, 2.2)
        for u in range(0, int(60 * p) + 1):
            s_ = u / 60 * 120                          # seconds after the cut
            v = (s_ / 30) * math.exp(1 - s_ / 30)
            pts.append((ox + gw * u / 60, oy - gh * .85 * v))
        c.line(pts, GAS, 7, m)
        pk_x = ox + gw * 30 / 120
        kk = m * fd(T(2), 1.6)
        c.line([(pk_x, oy), (pk_x, oy - gh * .85)], YE, 3, kk)
        c.text(pk_x + 20, oy - gh * .9, 'peak: about 30 s after the cut', 32, YE, kk, 'lm', 'Bold')
        c.text(ox + gw, oy + 36, 'time', 28, DIM, m, 'rm', 'Medium')
        c.text(ox, oy + 36, 'cut', 28, DIM, m, 'mm', 'Medium')
        c.text(ox + gw / 2, oy + 90, 'simplified', 28, DIM, m, 'mm', 'Medium')

def s_eyes(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'What it does to your eyes', 66, INK, hl(0), w='Bold')
    k0 = hl(0)
    fire = fd(T(1), .6, .6) if T(1) > -.1 else 0.0
    tears = fd(T(2), .8, .8) if T(2) > -.1 else 0.0
    ex, ey, s = 700, 480, 330
    eye(c, ex, ey, s, k0, red=fire * .8, t=t, tears=tears)
    # nerve endings on the cornea
    for j in range(9):
        u = j * 2 * math.pi / 9 + .3
        r0 = s * .3
        x0, y0 = ex + r0 * math.cos(u), ey + r0 * .8 * math.sin(u)
        x1, y1 = ex + r0 * 1.45 * math.cos(u), ey + r0 * 1.2 * math.sin(u)
        flick = .5 + .5 * math.sin(t * 14 + j * 2) if fire > 0 else 1
        col = YE if fire > 0 else (200, 190, 120)
        c.line([(x0, y0), (x1, y1)], col, 4, k0 * fd(T(0), 1.0) * (.6 + .4 * flick), (70, 120, 190))
        c.line([(x1, y1), (x1 + 16 * math.cos(u + .6), y1 + 16 * math.sin(u + .6))], col, 3, k0 * fd(T(0), 1.0) * (.6 + .4 * flick))
    c.text(ex, 840, 'cornea: packed with nerve endings', 38, YE, k0 * fd(T(0), 1.2) * (1 - hl(1)), w='Bold')
    if T(1) > -.1:
        k1 = hl(1)
        wisp(c, ex - 420, ey + 300, 360, t, k1 * (1 - tears), n=3, spread=70, drift=300)
        bx, by = 1500, 380
        brain(c, bx, by, 150, k1, hot=fire)
        pts = [(ex + s * .95, ey - s * .1), (1150, 420), (bx - 150, by + 40)]
        c.line(pts, (120, 110, 160), 5, k1)
        for j in range(3):
            q = (t * 1.2 + j / 3) % 1
            sx = pts[0][0] + (pts[2][0] - pts[0][0]) * q; sy = pts[0][1] + (pts[2][1] - pts[0][1]) * q + 30 * math.sin(math.pi * q)
            c.circ(sx, sy, 10, YE, k1 * fire)
        c.text(bx, by + 220, 'brain: "burning!"', 44, PK, k1 * fire * (1 - hl(2)), w='Bold')
    if T(2) > -.1:
        k2 = hl(2)
        c.text(1500, 600, 'reflex tears', 50, CY, k2, w='Bold')
        c.text(1500, 670, 'wash the irritant away', 36, INK, k2 * fd(T(2), .5), w='Medium')

def s_missing(c, T, t):
    hl = lambda i: hl_(T, i)
    out = 1 - fd(T(2), -.1, .4)
    c.text(960, 130, 'The missing piece', 66, INK, hl(0) * out, w='Bold')
    if out > 0:
        k0 = hl(0) * out
        c.text(960, 250, 'Old idea: the first enzyme alone makes the gas', 40, DIM, k0, w='Bold')
        k1 = hl(1) * out
        if k1 > 0:
            garlic(c, 600, 560, 150, k1)
            onion(c, 1320, 560, 150, k1)
            c.text(600, 800, 'garlic: same first enzyme', 36, INK, k1, w='Bold')
            c.text(600, 850, 'no tears', 40, GR, k1 * fd(T(1), 1.0), w='Bold')
            c.text(1320, 800, 'onion', 36, INK, k1, w='Bold')
            c.text(1320, 850, 'tears', 40, PK, k1 * fd(T(1), 1.0), w='Bold')
            c.text(960, 560, '?', 140, YE, k1 * fd(T(1), 1.6), w='Bold')
    if T(2) > -.1:
        m = fd(T(2), .1)
        k3 = hl(3)
        c.rr(300, 210, 1620, 640, 30, CARD, m, outline=GAS, ow=5)
        c.text(960, 290, '2002  ·  a team in Japan  ·  published in Nature', 38, DIM, m, w='Medium', bg=CARD)
        c.text(960, 400, 'a second enzyme', 72, GAS, m, w='Bold', bg=CARD)
        c.text(960, 490, 'lachrymatory-factor synthase', 46, INK, m * fd(T(2), .8), w='Bold', bg=CARD)
        c.text(960, 560, '("lachrymatory" = tear-making)', 32, DIM, m * fd(T(2), 1.4), w='Medium', bg=CARD)
        if k3 > 0:
            c.circ(780, 770, 50, YE, k3)
            c.circ(780, 770, 34, (200, 150, 40), k3, bg=YE)
            c.text(1000, 770, 'Ig Nobel Prize, 2013', 44, YE, k3, 'lm', 'Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(2)
    c.text(960, 130, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 210, 'Which knife makes you cry more?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 170, 'The dull one: it crushes more cells', 62, PK, ans, w='Bold')
    for j, x in enumerate((560, 1360)):
        kk = m * fd(T(0), 1.0 + j * 1.2)
        if kk <= 0: continue
        dull = j == 1
        dim = 1 - (.45 * ans if not dull else 0)
        c.rr(x - 330, 280, x + 330, 820, 30, CARD, kk * dim, outline=(PK if ans > 0 else YE) if dull else CY, ow=5)
        c.text(x - 270, 340, 'AB'[j], 46, CY if not dull else YE, kk * dim, w='Bold', bg=CARD)
        knife(c, x + 170, 420, 150, kk * dim, CARD, dull=dull)
        c.text(x, 520, 'dull knife' if dull else 'sharp knife', 44, INK, kk * dim, w='Bold', bg=CARD)
        # a row of cells: burst ones turn pink and leak gas after the answer
        for q in range(6):
            cx = x - 250 + q * 100; cy = 660
            broken = (q in (2, 3)) if not dull else True
            col = PK if (broken and ans > 0) else WALL
            c.rr(cx - 42, cy - 48, cx + 42, cy + 48, 14, (30, 52, 50), kk * dim, outline=col, ow=4, bg=CARD)
            if broken and ans > 0:
                for d in range(2):
                    ph = (t * .8 + q * .37 + d * .5) % 1
                    c.circ(cx + 10 * math.sin(t * 3 + q + d), cy - 50 - 50 * ph, 7, GAS, ans * dim * (1 - ph), bg=CARD)
        c.text(x, 760, '2 cells cut' if not dull else 'many cells crushed', 32, (GR if not dull else PK), ans * dim, w='Bold', bg=CARD)
        if ans > 0 and dull:
            pill(c, x + 170, 340, 'MORE TEARS', PK, ans, 28, bg=CARD, h=54)
    if T(1) > 0 and ans < 1:
        p = clamp(T(1) / 2.0)
        ring(c, 960, 550, 60, 1 - p, CY, fd(T(1)) * (1 - ans))
        c.text(960, 550, 'or', 40, DIM, fd(T(1)) * (1 - ans), w='Bold')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Why would an onion do this?', 66, INK, hl(0), w='Bold')
    k = hl(0)
    # ground cross-section
    c.rr(160, 520, 1760, 860, 20, SOIL, k)
    for j in range(5):
        u = t * 2 + j
        c.line([(860 + j * 40 - 40, 520), (850 + j * 40 - 40 + 14 * math.sin(u), 400 - j % 2 * 30)], LEAF, 14, k)
    onion(c, 960, 660, 120, k, bg=SOIL)
    bite = fd(T(2), .2, 1.0) if T(2) > -.1 else 0.0
    back = fd(T(2), 1.6, 1.0) if T(2) > -.1 else 0.0
    gx = 1500 - 360 * bite * (1 - back) + 120 * back
    grub(c, gx, 700, 70, hl(1), t, bg=SOIL)
    if hl(1) > 0:
        c.text(960, 220, "It can't run away", 46, DIM, hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 290, 'Chemists call it a chemical defence', 46, GAS, hl(1) * fd(T(1), 1.2), w='Bold')
    if bite > .6:
        wisp(c, 1090, 640, 160, t, fd(T(2), .8, .4) * (1 - fd(T(2), 2.6, .8)), n=3, spread=40, bg=SOIL)
        c.text(1300, 580, 'bite = break the cells', 34, YE, fd(T(2), 1.0), 'mm', 'Bold', bg=SOIL)

def s_tips(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'How to cry less', 66, INK, hl(0), w='Bold')
    tips = [(1, 'Chill it first', 'cold gas spreads more slowly', CY),
            (2, 'Use a sharp knife', 'fewer cells burst', YE),
            (3, 'Add a breeze', 'a fan or an open window', GR)]
    for j, (li, title, sub, col) in enumerate(tips):
        k = hl(li); up = 24 * (1 - k)
        if k <= 0: continue
        x = 400 + j * 560
        c.rr(x - 260, 240 + up, x + 260, 800 + up, 30, CARD, k, outline=col, ow=5)
        y = 450 + up
        if j == 0:
            onion(c, x - 60, y + 30, 90, k, CARD)
            snowflake(c, x + 120, y - 60, 60, k, CARD)
        elif j == 1:
            knife(c, x + 40, y - 20, 120, k, CARD)
            half(c, x - 60, y + 100, 75, k, CARD)
        else:
            fan(c, x - 90, y - 20, 90, k, t, CARD)
            wisp(c, x + 60, y + 110, 160, t, k, n=3, spread=40, bg=CARD, drift=140)
        c.text(x, 670 + up, title, 40, col, k, w='Bold', bg=CARD)
        c.text(x, 730 + up, sub, 28, INK, k, w='Medium', bg=CARD)

REC = [('1', 'Cutting mixes 2 ingredients', YE), ('2', 'Two enzymes make a gas', GAS), ('3', 'Eye nerves fire: tears', CY)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 540 + up
        if i == 0:
            glowstick(c, x, y - 40, 300, m, 1, .5 + .5 * math.sin(t * 2), t, CARD)
        elif i == 1:
            half(c, x, y + 30, 100, m, CARD)
            wisp(c, x, y - 20, 160, t, m, n=3, spread=50, bg=CARD)
        else:
            eye(c, x, y - 20, 140, m, red=.6, t=t, bg=CARD, tears=1)
        c.text(x, 740 + up, lab, 32, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["A whole onion can sit on your counter for weeks, and it never makes you cry.",
            "Cut it, and within about thirty seconds, your eyes sting.",
            "So what changes when you cut it? The onion springs a chemical trap."], s_hook),
 ('1  ·  THE GLOW STICK', ["Think of a glow stick. Two liquids sit apart inside it, so nothing happens.",
            "Bend it, the inner tube snaps, the liquids mix, and it lights up.",
            "An onion works the same way. Every cell keeps two ingredients apart, until a knife breaks it."], s_glow),
 ('2  ·  INSIDE A CELL', ["Inside each cell are sulfur compounds. On their own, they're harmless.",
            "Sealed away in a tiny pocket is an enzyme, a natural chemical helper, called alliinase.",
            "The knife bursts the pocket. The enzyme meets the sulfur compounds, and they react."], s_cell),
 ('3  ·  THE GAS', ["Together, they make an unstable acid.",
            "Then a second enzyme turns that acid into a gas, called sin-propane-thial S-oxide.",
            "It drifts up off the chopping board, toward your face. Gas production peaks about thirty seconds after the cut."], s_gas),
 ('4  ·  YOUR EYES', ["The front of your eye, the cornea, is packed with tiny nerve endings.",
            "When the gas lands there, those nerves fire, and your brain reads the signal as burning.",
            "So it tells your tear glands to flood your eyes and wash the irritant away. That's the crying."], s_eyes),
 ('5  ·  THE MISSING PIECE', ["For years, scientists blamed the first enzyme alone.",
            "But garlic has that enzyme too, and chopping garlic doesn't make you cry.",
            "In two thousand and two, a team in Japan found the missing piece: the second enzyme, the one that actually makes the stinging gas.",
            "Their paper later won an Ig Nobel Prize."], s_missing),
 ('6  ·  QUICK QUESTION', ["Quick question. Which knife makes you cry more, a sharp one or a dull one?",
            "Three, two, one.",
            "The dull one. It crushes more cells instead of slicing cleanly, so more pockets burst."], s_quiz),
 ('7  ·  WHY?', ["Why would an onion do this?",
            "It grows in the soil, and it can't run away. Chemists describe this as a chemical defence.",
            "The onion stays harmless until something bites it. Then it fights back."], s_why),
 ('8  ·  CRY LESS', ["So how do you cut one without crying?",
            "Chill the onion first. The gas spreads more slowly when it's cold.",
            "Use your sharpest knife, so fewer cells burst.",
            "And cut near a fan or an open window, so the gas blows away before it reaches you."], s_tips),
 ('RECAP', ["So remember three things.",
            "One. Cutting bursts the cells and mixes two ingredients, like snapping a glow stick.",
            "Two. Two enzymes turn them into a gas that floats up to your eyes.",
            "Three. Nerves in your eye read it as burning, and tears wash it away.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["A whole onion never makes you cry.",
                 "Cut it, and within about thirty seconds, your eyes sting.",
                 "So what changes? The onion springs a chemical trap."], s_hook),
 ('THE TRAP', ["Each onion cell holds sulfur compounds.",
               "And a tiny sealed pocket holds an enzyme.",
               "A knife bursts the pocket, and the two mix, like snapping a glow stick."], s_cell),
 ('THE GAS', ["They make an unstable acid.",
              "A second enzyme turns it into a gas.",
              "It floats up, toward your face."], s_gas),
 ('YOUR EYES', ["Your cornea is packed with nerve endings.",
                "The gas makes them fire, and your brain reads it as burning.",
                "So your tear glands flush it away."], s_eyes),
 ('THE ANSWER', ["That's why you cry. The gas only forms once you cut.",
                 "A sharp knife and a cold onion help. Follow for more."],
                card('Cutting makes the gas', 'Sharp knife + cold onion help')),
]
SHORT_HITS = [(4, 0, 0.0)]
