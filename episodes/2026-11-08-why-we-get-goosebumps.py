"""Episode: Your Goosebumps Are Fluffing Fur You Don't Have (arrector pili muscle, sympathetic nerve, fur insulation and looking bigger, the 2020 Cell study in mice: NIH Research Matters, ScienceAlert, New Atlas, NPR, PopSci, Ask Dr. Universe, Science News)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Your Goosebumps Are Fluffing Fur You Don't Have"   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Why do we get goosebumps?'                       # headline on the vertical Short
HITS = [(0, 0, 0.0), (7, 0, 0.0), (7, 3, 0.0)]                 # the claim, quiz answer, the hair-growth payoff
THUMB = ['NO FUR.', 'STILL FLUFFING.']                         # 3 words (vidIQ: median 5 words)
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.4, (0, 2): 0.4, (1, 2): 0.3, (2, 2): 0.3, (3, 2): 0.3, (4, 2): 0.3, (5, 2): 0.4, (6, 2): 2.6, (7, 0): 0.3, (7, 3): 0.4, (8, 2): 0.3, (9, 1): 0.2}
SHORT_PAUSES = {(0, 0): 0.2, (3, 1): 0.2}
CAPTION_FIXES = {'twenty twenty': '2020'}

# Colour code kept in every scene (lesson of 2026-11-01):
# muscle pink, nerve yellow, cold cyan, trapped warm air orange, new hair / stem cells green, fear purple.
MUS = PK; NERVE = YE; COLD = CY; WARM = (255, 150, 70); GROW = GR; FEAR = PU
SKIN = (226, 170, 140); SKIN2 = (196, 132, 112); DERM = (150, 86, 96); HAIR = (120, 84, 60); FUR = (176, 132, 96)
DARK = (20, 22, 38); QUIZ = (70, 40, 96)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ell(c, x, y, rx, ry, fill=None, a=1.0, outline=None, ow=3, bg=BG):
    if a <= .01: return
    c.d.ellipse(((x - rx) * c.k, (y - ry) * c.k, (x + rx) * c.k, (y + ry) * c.k),
                fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None, width=max(1, int(ow * c.k)))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def skin_section(c, x0, x1, top, s, a=1.0, up=0.0, nerve=0.0, t=0.0, stem=0.0, hairs=(0.5,)):
    """Cross-section of skin. up: how far the muscles have pulled the hairs upright (0 lying flat, 1 standing).
    nerve: nerve fibre lit with travelling pulses. stem: stem cells at the follicle glowing green."""
    if a <= .01: return
    w = x1 - x0; ep = 46 * s
    # surface with bumps where each hair stands
    pts = [(x0, top + 330 * s)]
    for k in range(121):
        x = x0 + w * k / 120; y = top
        for h in hairs:
            hx = x0 + w * h; y -= up * 34 * s * math.exp(-((x - hx) / (70 * s)) ** 2)
        pts.append((x, y))
    pts.append((x1, top + 330 * s))
    poly(c, pts, DERM, a)
    pts2 = [(x, y) for x, y in pts[1:-1]] + [(x, y + ep) for x, y in reversed(pts[1:-1])]
    poly(c, pts2, SKIN, a)
    c.line(pts[1:-1], SKIN2, 4 * s, a)
    for h in hairs:
        hx = x0 + w * h
        ang = math.radians(lerp(58, 10, up))         # angle of the hair from vertical
        dx, dy = math.sin(ang), -math.cos(ang)
        bx, by = hx - dx * 150 * s, top + 190 * s      # root (bulb) of the follicle, deep in the skin
        sy = top - up * 34 * s
        # follicle pocket
        c.line([(bx, by), (hx, sy + ep * .2)], (110, 60, 70), 34 * s, a, bg=DERM)
        c.circ(bx, by, 24 * s, (130, 70, 80), a, bg=DERM)
        # hair shaft: root to well above the surface
        c.line([(bx, by), (hx + dx * 150 * s, sy + dy * 150 * s)], HAIR, 9 * s, a, bg=DERM)
        # stem cells sit on the side of the follicle
        sxp, syp = lerp(bx, hx, .45) + 22 * s, lerp(by, sy, .45)
        for j in range(3):
            c.circ(sxp + j * 3 * s, syp - 18 * s + j * 18 * s, 9 * s, mix(GROW, .35 + .65 * stem, DERM) if stem > .01 else (170, 110, 120), a, bg=DERM)
        if stem > .01:
            c.circ(sxp, syp, (34 + 4 * math.sin(t * 5)) * s, None, a * stem * .8, outline=GROW, ow=3 * s, bg=DERM)
        # the arrector pili muscle: from the follicle to just under the surface, on the side the hair leans
        mx0, my0 = lerp(bx, hx, .3) + 18 * s, lerp(by, sy, .3)
        mx1, my1 = hx + 120 * s, top + ep + 6 * s
        mw = lerp(14, 22, up) * s
        c.line([(mx0, my0), ((mx0 + mx1) / 2 + 10 * s * (1 - up), (my0 + my1) / 2 + 8 * s), (mx1, my1)], MUS, mw, a, bg=DERM)
        # nerve fibre from below to the muscle
        if nerve > .01:
            nx, ny = (mx0 + mx1) / 2 + 10 * s, (my0 + my1) / 2 + 8 * s
            npts = [(nx + 60 * s * math.sin(u * 3.2) * (1 - u) + 90 * s * (1 - u), ny + 220 * s * (1 - u)) for u in [k / 30 for k in range(31)]]
            c.line(npts, NERVE, 6 * s, a * nerve, bg=DERM)
            for j in range(3):
                u = (t * .7 + j / 3) % 1
                px, py = npts[int(u * 30)]
                c.circ(px, py, 10 * s, NERVE, a * nerve, bg=DERM)
            if stem > .01:
                c.line([npts[18], (sxp + 8 * s, syp + 10 * s)], NERVE, 5 * s, a * nerve * stem, bg=DERM)

def arm(c, x, y, s, a=1.0, bumps=0.0, t=0.0):
    """A forearm seen from the side, with hairs that stand and bumps that rise."""
    pts = [(x - 520 * s, y - 70 * s), (x + 380 * s, y - 95 * s), (x + 470 * s, y - 60 * s), (x + 470 * s, y + 70 * s),
           (x + 380 * s, y + 95 * s), (x - 520 * s, y + 80 * s)]
    poly(c, pts, SKIN, a)
    c.circ(x + 470 * s, y, 92 * s, SKIN, a)
    for k in range(26):
        hx = x - 480 * s + k * 34 * s; hy = y - 78 * s - 0.03 * (k * 34 * s)
        ang = math.radians(lerp(70, 8, bumps) + 6 * math.sin(k * 1.7))
        c.line([(hx, hy), (hx + 46 * s * math.sin(ang), hy - 46 * s * math.cos(ang))], HAIR, 4 * s, a, bg=BG)
        if bumps > .01:
            c.circ(hx, hy + 30 * s, 7 * s * bumps, SKIN2, a, bg=SKIN)
            c.circ(hx + 17 * s, hy + 70 * s, 6 * s * bumps, SKIN2, a, bg=SKIN)

def furry(c, x, y, s, a=1.0, fluff=0.0, t=0.0, air=0.0):
    """An original round furry animal (a snow monkey's head and shoulders, simplified)."""
    R = 190 * s
    n = 70
    for k in range(n):
        ang = 2 * math.pi * k / n
        L = (34 + 70 * fluff + 6 * math.sin(k * 2.3)) * s
        r0 = R - 10 * s
        c.line([(x + r0 * math.cos(ang), y + r0 * math.sin(ang)), (x + (r0 + L) * math.cos(ang), y + (r0 + L) * math.sin(ang))], FUR, 9 * s, a)
    c.circ(x, y, R, FUR, a)
    if air > .01:
        for k in range(18):
            ang = 2 * math.pi * k / 18 + t * .2
            rr_ = R + (20 + 40 * fluff) * s + 6 * s * math.sin(t * 3 + k)
            c.circ(x + rr_ * math.cos(ang), y + rr_ * math.sin(ang), 9 * s, WARM, a * air * .9)
    c.circ(x, y + 20 * s, 112 * s, (226, 150, 150), a, bg=FUR)
    for sx in (-1, 1):
        c.circ(x + sx * 42 * s, y - 2 * s, 14 * s, DARK, a, bg=(226, 150, 150))
    c.line([(x - 26 * s, y + 70 * s), (x, y + 80 * s), (x + 26 * s, y + 70 * s)], (150, 80, 80), 6 * s, a, bg=(226, 150, 150))

def cat(c, x, y, s, a=1.0, puff=0.0, t=0.0, col=(120, 120, 140)):
    """A generic side-on cat; puff raises the fur along the back and tail and arches the body."""
    arch = 50 * puff * s; sc = 1 + .18 * puff
    # tail
    tpts = [(x + 200 * s, y - 20 * s), (x + 290 * s, y - 120 * s - arch), (x + 300 * s, y - 230 * s - arch)]
    c.line(tpts, col, (26 + 34 * puff) * s, a)
    # legs
    for lx in (-130, -80, 110, 160):
        c.line([(x + lx * s, y + 40 * s), (x + lx * s, y + 170 * s)], col, 26 * s, a)
    ell(c, x + 20 * s, y - arch * .6, 200 * s * sc, (95 + 25 * puff) * s, col, a)
    if puff > .01:
        for k in range(22):
            u = k / 21; bx = x - 160 * s + u * 360 * s
            by = y - arch * .6 - (95 + 25 * puff) * s * math.sqrt(max(0, 1 - ((bx - x - 20 * s) / (200 * s * sc)) ** 2)) + 6 * s
            c.line([(bx, by), (bx + 4 * s, by - 42 * s * puff)], col, 10 * s, a)
    hx, hy = x - 230 * s, y - 70 * s - arch * .4
    c.circ(hx, hy, 80 * s, col, a)
    poly(c, [(hx - 70 * s, hy - 30 * s), (hx - 60 * s, hy - 120 * s), (hx - 15 * s, hy - 70 * s)], col, a)
    poly(c, [(hx + 70 * s, hy - 30 * s), (hx + 50 * s, hy - 120 * s), (hx + 10 * s, hy - 75 * s)], col, a)
    for sx in (-1, 1):
        ell(c, hx + sx * 30 * s, hy - 8 * s, 14 * s, (14 + 6 * puff) * s, (230, 220, 120), a, bg=col)
        c.circ(hx + sx * 30 * s, hy - 8 * s, 6 * s, DARK, a, bg=(230, 220, 120))
    c.circ(hx, hy + 22 * s, 8 * s, (230, 140, 160), a, bg=col)

def mouse(c, x, y, s, a=1.0, grow=0.0, t=0.0, cold=0.0):
    col = (170, 170, 186)
    c.line([(x + 170 * s, y + 30 * s), (x + 260 * s, y + 10 * s), (x + 330 * s, y + 50 * s)], (210, 160, 170), 8 * s, a)
    ell(c, x, y, 190 * s, 105 * s, col, a)
    c.circ(x - 150 * s, y - 70 * s, 50 * s, col, a); c.circ(x - 150 * s, y - 70 * s, 30 * s, (220, 170, 180), a, bg=col)
    ell(c, x - 200 * s, y + 20 * s, 85 * s, 62 * s, col, a)
    c.circ(x - 215 * s, y + 5 * s, 12 * s, DARK, a, bg=col)
    c.circ(x - 282 * s, y + 30 * s, 11 * s, (220, 140, 160), a, bg=col)
    if grow > .01:
        for k in range(16):
            u = k / 15; gx = x - 70 * s + u * 180 * s
            gy = y - 105 * s * math.sqrt(max(0, 1 - ((gx - x) / (190 * s)) ** 2)) + 8 * s
            c.line([(gx, gy), (gx + 5 * s, gy - 44 * s * grow)], GROW, 7 * s, a)
    if cold > .01:
        for k in range(5):
            fx, fy = x - 260 * s + k * 130 * s, y - 185 * s + 15 * s * math.sin(t * 1.5 + k)
            for j in range(3):
                ang = math.pi * j / 3
                c.line([(fx - 18 * s * math.cos(ang), fy - 18 * s * math.sin(ang)), (fx + 18 * s * math.cos(ang), fy + 18 * s * math.sin(ang))], COLD, 4 * s, a * cold)

def note(c, x, y, s, col, a):
    ell(c, x, y, 22 * s, 16 * s, col, a); c.line([(x + 20 * s, y), (x + 20 * s, y - 90 * s)], col, 6 * s, a)
    c.line([(x + 20 * s, y - 90 * s), (x + 50 * s, y - 70 * s)], col, 6 * s, a)

def heart(c, x, y, s, a, col, beat=0.0):
    k = 1 + .12 * beat
    c.circ(x - 26 * s * k, y - 14 * s * k, 30 * s * k, col, a); c.circ(x + 26 * s * k, y - 14 * s * k, 30 * s * k, col, a)
    poly(c, [(x - 54 * s * k, y - 4 * s * k), (x + 54 * s * k, y - 4 * s * k), (x, y + 62 * s * k)], col, a)

# ---- scenes ----
def s_hook(c, T, t):
    """Surprising true statement first, with the arm already on screen (lessons of 2026-10-16 and 2026-11-08)."""
    hl = lambda i: hl_(T, i)
    b = fd(t, .6, 1.2) if T(1) < 0 else 1.0
    arm(c, 860, 560, 1.15, 1 - hl(2), bumps=b, t=t)
    c.text(960, 172, "Fluffing fur you don't have", 92, WARM, sw_out(T, 1), w='Bold')
    # three triggers appear one by one
    m = sw_in(T, 1) * (1 - hl(2))
    c.text(960, 172, 'Cold. Fear. A song you love.', 88, INK, m, w='Bold')
    for k, (lab, col) in enumerate((('COLD', COLD), ('FEAR', FEAR), ('MUSIC', NERVE))):
        mm = m * fd(T(1), .3 + k * .7)
        c.rr(330 + k * 460, 760, 690 + k * 460, 850, 24, CARD, mm, outline=col, ow=4)
        c.text(510 + k * 460, 805, lab, 50, col, mm, w='Bold', bg=CARD)
    q = hl(2)
    c.text(960, 430, 'So why does your', 112, INK, q, w='Bold')
    c.text(960, 570, 'body still bother?', 112, WARM, q, w='Bold')
    c.text(960, 730, 'Start with a tiny muscle', 66, MUS, hl(3), w='Bold')

def s_muscle(c, T, t):
    hl = lambda i: hl_(T, i)
    up = hl(2) * fd(T(2), .4, 1.2)
    skin_section(c, 120, 1180, 470, 1.2, 1, up=up, t=t)
    c.text(960, 172, 'Each hair grows from a pocket: a follicle', 72, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'The arrector pili muscle', 84, MUS, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'It tightens. The hair stands up.', 80, MUS, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1280, 300, 1840, 640, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1560, 380, 'arrector pili', 58, MUS, m, w='Bold', bg=CARD)
    c.text(1560, 450, '"ah-REK-tor PILL-ee"', 40, DIM, m, w='Medium', bg=CARD)
    c.text(1560, 540, 'hair-raising', 50, INK, m, w='Bold', bg=CARD)
    c.text(1560, 595, 'muscle', 50, INK, m, w='Bold', bg=CARD)
    c.text(1520, 760, 'Many at once: goosebumps', 48, WARM, hl(3), w='Bold')
    c.text(1880, 860, 'Drawing simplified, not to scale', 30, DIM, 1, anchor='rm', w='Regular')

def s_nerve(c, T, t):
    hl = lambda i: hl_(T, i)
    nv = hl(1)
    skin_section(c, 120, 1100, 470, 1.15, 1, up=nv * fd(T(1), .8, 1.0), nerve=nv, t=t)
    c.text(960, 172, "You don't choose to do it", 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A nerve from your fight-or-flight system', 70, NERVE, sw_in(T, 1), w='Bold')
    m = hl(2)
    c.rr(1200, 300, 1840, 660, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1520, 370, 'The same system', 50, INK, m, w='Bold', bg=CARD)
    beat = abs(math.sin(t * 5)) if m > .01 else 0
    heart(c, 1520, 480, 1.0, m, PK, beat)
    c.text(1520, 610, 'speeds up your heart', 46, PK, m, w='Bold', bg=CARD)

def s_cold(c, T, t):
    hl = lambda i: hl_(T, i)
    fl = hl(1) * fd(T(1), .3, 1.4)
    furry(c, 520, 500, 1.0, 1, fluff=fl, t=t, air=hl(1) * fd(T(1), 1.4))
    for k in range(7):
        fx, fy = 150 + k * 140, 260 + 40 * math.sin(t * 1.2 + k) + (t * 40 + k * 60) % 120
        for j in range(3):
            ang = math.pi * j / 3
            c.line([(fx - 16 * math.cos(ang), fy - 16 * math.sin(ang)), (fx + 16 * math.cos(ang), fy + 16 * math.sin(ang))], COLD, 4, .8)
    c.text(960, 172, 'For a furry animal, it works', 80, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Raised fur traps a layer of air', 80, WARM, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Like a puffy jacket', 84, WARM, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1080, 300, 1840, 640, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1460, 380, 'Snow monkey, cold day', 50, COLD, m, w='Bold', bg=CARD)
    c.text(1460, 470, 'fur fluffs up', 56, INK, m, w='Bold', bg=CARD)
    c.text(1460, 560, 'warm air stays in', 56, WARM, m, w='Bold', bg=CARD)
    if hl(2) > .01:
        x0 = 1290; y0 = 700; m2 = hl(2)
        c.rr(x0, y0, x0 + 340, y0 + 150, 50, (70, 90, 150), m2)
        for k in range(4): c.line([(x0 + 40 + k * 85, y0 + 10), (x0 + 40 + k * 85, y0 + 140)], (50, 66, 120), 6, m2, bg=(70, 90, 150))
        for k in range(8): c.circ(x0 + 30 + k * 40, y0 + 75 + 20 * math.sin(t * 3 + k), 8, WARM, m2, bg=(70, 90, 150))

def s_fear(c, T, t):
    hl = lambda i: hl_(T, i)
    p = hl(1) * fd(T(1), .2, 1.0)
    cat(c, 620, 580, 1.15, 1, puff=p, t=t)
    c.text(960, 172, 'Fear flips the same switch', 84, FEAR, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A scared cat looks bigger', 84, FEAR, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A jump scare: same reflex', 84, FEAR, sw_in(T, 2), w='Bold')
    m = hl(2)
    c.rr(1200, 300, 1840, 640, 28, DARK, m, outline=FEAR, ow=4)
    for k in range(5): c.circ(1260 + k * 30, 330 + k * 8, 6, DIM, m, bg=DARK)
    c.text(1520, 420, 'BOO!', 120, FEAR, m * fd(T(2), .4, .2), w='Bold', bg=DARK)
    c.text(1520, 560, 'only a film', 50, INK, m, w='Bold', bg=DARK)
    c.text(1880, 860, 'Sources: NPR; PopSci; Ask Dr. Universe', 30, DIM, 1, anchor='rm', w='Regular')

def s_us(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'On you, the trick mostly fails', 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Too little body hair to trap much air', 76, COLD, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'The reflex fires anyway', 84, WARM, sw_in(T, 2), w='Bold')
    m1 = fd(T(0), .3); m2 = fd(T(0), .9)
    furry(c, 500, 520, .9, m1, fluff=1, t=t, air=1)
    c.text(500, 800, 'Lots of fur: warm', 52, WARM, m1, w='Bold')
    arm(c, 1440, 520, .75, m2, bumps=hl(2) * .9 + .1, t=t)
    c.text(1440, 800, 'Little hair: barely helps', 52, COLD, m2, w='Bold')
    for k in range(4):
        c.circ(1150 + k * 170, 400 + 10 * math.sin(t * 2 + k), 10, COLD, hl(1) * .8)

def s_quiz(c, T, t):
    """Pattern interrupt: the frame fills with colour (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(560, 110, 1360, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK QUESTION', 78, NERVE, 1, w='Bold', bg=DARK)
    c.text(960, 310, 'In mice, what else does the goosebump nerve do?', 56, INK, hl(1), w='Bold', bg=QUIZ)
    for x, lab, l1, l2, col in ((510, 'A', 'It stops the skin', 'drying out', COLD), (1410, 'B', 'It helps', 'grow new hair', GROW)):
        m = hl(2) if lab == 'A' else fd(T(2), 1.6)
        c.rr(x - 420, 400, x + 420, 800, 34, DARK, m, bg=QUIZ)
        c.text(x, 500, lab, 110, col, m, w='Bold', bg=DARK)
        c.text(x, 640, l1, 56, INK, m, w='Bold', bg=DARK)
        c.text(x, 715, l2, 56, INK, m, w='Bold', bg=DARK)
    end = T(2) - 4.0
    if end > 0:
        q = clamp(end / 2.4); n = 3 - int(min(q * 3, 2.9))
        c.circ(960, 600, 96, DARK, 1, bg=QUIZ); ring(c, 960, 600, 82, 1 - q, NERVE, 1, 10)
        c.text(960, 600, str(n), 86, INK, 1, w='Bold', bg=DARK)

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'B. It helps grow new hair', 84, GROW, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'The nerve also reaches the hair stem cells', 70, NERVE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'In the cold, new hair grew within two weeks', 68, GROW, sw_in(T, 2) * sw_out(T, 3), w='Bold')
    c.text(960, 172, 'Raise hair now, grow more hair later', 76, GROW, sw_in(T, 3), w='Bold')
    m0 = hl(0) * (1 - hl(1))
    c.rr(560, 330, 1360, 650, 28, CARD, m0, outline=(60, 70, 120), ow=3)
    c.text(960, 410, 'Cell, July 2020', 56, INK, m0, w='Bold', bg=CARD)
    c.text(960, 500, 'Ya-Chieh Hsu (Harvard)', 50, DIM, m0, w='Medium', bg=CARD)
    c.text(960, 570, 'Sung-Jan Lin (Taiwan)', 50, DIM, m0, w='Medium', bg=CARD)
    m1 = hl(1) * (1 - hl(2))
    skin_section(c, 200, 1300, 470, 1.15, m1, up=.8, nerve=1, t=t, stem=hl(1) * fd(T(1), 1.0))
    m2 = hl(2)
    mouse(c, 760, 520, 1.3, m2, grow=fd(T(2), 1.5, 2.5) * (1 - .0 * hl(3)), t=t, cold=m2)
    c.rr(1300, 330, 1840, 640, 28, CARD, m2, outline=(60, 70, 120), ow=3)
    c.text(1570, 410, 'Remove the nerve', 46, NERVE, m2, w='Bold', bg=CARD)
    c.text(1570, 470, 'or the muscle:', 46, MUS, m2, w='Bold', bg=CARD)
    c.text(1570, 560, 'new hair delayed', 50, INK, m2, w='Bold', bg=CARD)
    c.text(960, 780, 'Shown in mice. Not yet shown in people.', 54, WARM, hl(4), w='Bold')
    c.text(1880, 860, 'Sources: NIH Research Matters 2020; ScienceAlert', 30, DIM, 1, anchor='rm', w='Regular')

def s_emotion(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'And the song that gives you chills?', 80, NERVE, sw_out(T, 1), w='Bold')
    c.text(960, 172, "Why emotion does it: still not fully known", 70, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Often: chills, but no bumps', 80, NERVE, sw_in(T, 2), w='Bold')
    for k in range(6):
        x = 260 + k * 150 + 20 * math.sin(t * 1.5 + k); y = 520 - 60 * math.sin(t * 1.1 + k * 1.3)
        note(c, x, y, 1.0, NERVE if k % 2 == 0 else FEAR, fd(T(0), k * .2))
    m = hl(1)
    c.rr(1180, 300, 1840, 660, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1510, 380, 'Can trigger it:', 50, INK, m, w='Bold', bg=CARD)
    c.text(1510, 460, 'music', 52, NERVE, m, w='Bold', bg=CARD)
    c.text(1510, 530, 'a film', 52, FEAR, m, w='Bold', bg=CARD)
    c.text(1510, 600, 'a moment of awe', 52, WARM, m, w='Bold', bg=CARD)
    m2 = hl(2)
    c.rr(260, 700, 1100, 840, 28, DARK, m2, outline=NERVE, ow=3)
    c.text(680, 770, 'About half the time', 52, NERVE, m2, w='Bold', bg=DARK)
    c.text(1880, 860, 'Source: PopSci, Nov 2025', 30, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    """Recap as three bumps rising on the skin line (layout change)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 80, INK, sw_in(T, 0), w='Bold')
    pts = [(80, 760)]
    for k in range(121):
        x = 80 + 1760 * k / 120; y = 700
        for j, cx in enumerate((380, 960, 1540)):
            y -= 60 * hl(j + 1) * math.exp(-((x - cx) / 120) ** 2)
        pts.append((x, y))
    pts.append((1840, 760))
    poly(c, pts, SKIN, 1)
    rows = ((1, 'A tiny muscle pulls each hair upright', MUS),
            (2, 'Fur traps warm air and makes animals look bigger', WARM),
            (3, 'In mice, the same nerve helps grow new hair', GROW))
    for ln, txt, col in rows:
        m = hl(ln); x = (380, 960, 1540)[ln - 1]
        c.rr(x - 270, 260 + 30 * (1 - m), x + 270, 610 + 30 * (1 - m), 28, CARD, m, outline=col, ow=4)
        c.circ(x, 330 + 30 * (1 - m), 40, col, m, bg=CARD); c.text(x, 330 + 30 * (1 - m), str(ln), 46, DARK, m, w='Bold', bg=col)
        ls = wrap(c, txt, 44, 470, 'Bold')
        for j, l in enumerate(ls):
            c.text(x, 470 + 30 * (1 - m) + (j - (len(ls) - 1) / 2) * 54, l, 44, INK, m, w='Bold', bg=CARD)
        c.line([(x, 612 + 30 * (1 - m)), (x, 690 - 60 * m)], HAIR, 8, m)
    c.text(960, 830, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    cat(c, 1560, 560, .95, 1, puff=1, col=(150, 150, 170))
    arm(c, 1500, 260, .55, 1, bumps=1)

SCENES = [
 ('THE HOOK', ["Your goosebumps are trying to fluff up fur you don't have.",
               "A cold breeze, a scary film, a song you love. Tiny bumps rise.",
               "So why does your body still bother?",
               "It starts with a tiny muscle."], s_hook),
 ('THE MUSCLE', ["Each hair on your arm grows from a small pocket in your skin, called a follicle.",
                 "Attached to it is a tiny muscle, the arrector pili. The name means hair raiser.",
                 "When it tightens, it pulls the hair upright, and the skin around it bunches up.",
                 "Lots of them at once, and you get goosebumps."], s_muscle),
 ('THE SWITCH', ["You don't choose to do this. It's automatic.",
                 "The signal comes down a nerve from your sympathetic nervous system, the part that runs fight or flight.",
                 "It's the same system that speeds up your heart when you're scared."], s_nerve),
 ('THE COLD', ["For a furry animal, this trick is useful.",
               "When a snow monkey gets cold, its raised fur traps a layer of air that holds in warmth.",
               "Like a puffy jacket, the warmth sits in the trapped air."], s_cold),
 ('THE FEAR', ["Fear uses the same switch.",
               "A scared cat puffs up, so it looks bigger and stronger to whatever is scaring it.",
               "And to your body, a jump scare in a film isn't so different from a real threat."], s_fear),
 ('THE CATCH', ["But on you, the trick mostly fails.",
                "Humans have relatively little body hair, so raising it barely traps any air.",
                "The reflex fires anyway. So is it just a leftover?"], s_us),
 ('QUICK QUESTION', ["Quick question.",
                     "Scientists looked closely at the nerve behind goosebumps in mice. What else does it do?",
                     "A, it stops the skin drying out. Or B, it helps grow new hair."], s_quiz),
 ('THE TWIST', ["B. In twenty twenty, a team led by Ya-Chieh Hsu at Harvard and Sung-Jan Lin in Taiwan published a study in Cell.",
                "They found the same nerve that tightens the muscle also reaches the stem cells that grow new hair.",
                "In mice kept in the cold, new hair started growing in less than two weeks. Remove the nerve or the muscle, and new hair was delayed.",
                "So in mice, goosebumps raise hair now, and help grow more hair later.",
                "That's been shown in mice, not yet in people."], s_twist),
 ('THE CHILLS', ["And the song that gives you chills? Strong emotion can flip the same switch. Music, a film, a moment of awe.",
                 "Why emotion does it, scientists still don't fully know.",
                 "And about half the time, people feel the chill with no bumps at all."], s_emotion),
 ('RECAP', ["Three things to keep.",
            "One: a tiny muscle pulls each hair upright, and the skin bunches into a bump.",
            "Two: on furry animals, raised fur traps warm air and makes them look bigger.",
            "Three: in mice, the same nerve also helps grow new hair.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    arm(c, 860, 520, 1.1, 1, bumps=fd(t, .3, 1.0), t=t)
    c.text(960, 172, 'Why do we get goosebumps?', 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, "Fluffing fur you don't have", 84, WARM, sw_in(T, 1), w='Bold')

def short_muscle(c, T, t):
    hl = lambda i: hl_(T, i)
    skin_section(c, 160, 1760, 470, 1.2, 1, up=fd(T(0), 1.2, 1.2), nerve=hl(1), t=t, hairs=(.3, .7))
    c.text(960, 172, 'A tiny muscle pulls each hair up', 80, MUS, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A fight-or-flight nerve flips the switch', 72, NERVE, sw_in(T, 1), w='Bold')

def short_animals(c, T, t):
    hl = lambda i: hl_(T, i)
    furry(c, 470, 500, .85, 1, fluff=fd(T(0), .3, 1.2), t=t, air=fd(T(0), 1.2))
    cat(c, 1400, 560, .85, hl(1), puff=hl(1) * fd(T(1), .3, 1.0), t=t)
    c.text(960, 172, 'Cold: fur traps warm air', 80, WARM, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Fear: the cat looks bigger', 80, FEAR, sw_in(T, 1), w='Bold')

def short_us(c, T, t):
    hl = lambda i: hl_(T, i)
    arm(c, 760, 520, .8, 1 - hl(1), bumps=1, t=t)
    mouse(c, 900, 540, 1.3, hl(1), grow=fd(T(1), 1.0, 2.0), t=t, cold=hl(1))
    c.text(960, 172, 'We have too little hair for it to help', 72, COLD, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'In mice: the nerve helps grow new hair', 72, GROW, sw_in(T, 1), w='Bold')

SHORT_SCENES = [
 ('THE HOOK', ["Why do you get goosebumps?",
               "Your body is trying to fluff up fur you don't have."], short_open),
 ('THE MUSCLE', ["A tiny muscle at the root of each hair tightens, pulls the hair upright, and the skin bunches into a bump.",
                 "A nerve from your fight-or-flight system flips that switch."], short_muscle),
 ('THE ANIMALS', ["On a furry animal, raised fur traps warm air when it's cold.",
                  "And when it's scared, a cat puffs up to look bigger."], short_animals),
 ('THE CATCH', ["We have too little body hair for it to help us much. It barely traps any air.",
                "But in mice, that same nerve also helps grow new hair."], short_us),
 ('THE ANSWER', ["So goosebumps are a fur trick.",
                 "Your body still runs it, even with almost no fur."], card('Goosebumps fluff up fur.', 'We kept the reflex.')),
]
SHORT_HITS = [(4, 1, 0.0)]
