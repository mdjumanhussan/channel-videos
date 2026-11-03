"""Episode: The Zipper Test (illusion of explanatory depth: Rozenblit & Keil 2002, Lawson 2006 bicycle chain, warned group, facts vs how-things-work, Meyers 2023, the explain-out-loud fix)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'The Zipper Test'                                # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Can you explain how a zipper works?'             # headline on the vertical Short
HITS = [(0, 4, 0.0), (2, 3, 0.0), (4, 3, 0.0), (6, 3, 0.0)]    # title card, the name, quiz answer, 'in the bike, not in their heads'
THUMB = ['CAN YOU', 'EXPLAIN', 'A ZIPPER?']
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.25, (1, 3): 0.3, (2, 1): 0.3, (3, 1): 0.5, (4, 1): 0.3, (4, 2): 0.2, (6, 2): 0.4, (8, 1): 0.3}
SHORT_PAUSES = {(0, 0): 0.3, (4, 0): 0.3}
CAPTION_FIXES = {'forty-four percent': '44%', 'twelve percent': '12%', 'three point nine': '3.9', 'three point one': '3.1', 'two and a half': '2.5'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the feeling of knowing yellow, real understanding green, wrong or gaps pink, the real-world object blue.
FEEL = YE; REAL = GR; WRONG = PK; WORLD = CY
TAPE = (58, 66, 118); TA = (222, 228, 245); TB = (158, 170, 212); METAL = (196, 204, 232); DARK = (10, 12, 26); PAPER = (38, 44, 84)
PAPINK = (205, 212, 240)

hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def bike(c, x, y, s, a, chain='rear', chcol=REAL, col=WORLD, t=0.0, bg=BG, show_chain=1.0):
    """Side view of a bicycle. chain: 'rear' (the real path, pedals to back wheel) or 'both' (the common mistake)."""
    if a <= .01: return
    R = 165 * s; rx, fx = x - 270 * s, x + 270 * s; bbx, bby = x - 30 * s, y + 24 * s
    st = (x - 120 * s, y - 196 * s); hd = (x + 170 * s, y - 205 * s); hb = (x + 186 * s, y - 158 * s)
    for wx in (rx, fx):
        c.circ(wx, y, R, None, a, outline=(120, 130, 175), ow=max(5, 13 * s), bg=bg)
        for k in range(10):
            an = t * .9 + k * math.pi / 5
            c.line([(wx, y), (wx + (R - 8 * s) * math.cos(an), y + (R - 8 * s) * math.sin(an))], (70, 78, 120), max(2, 3 * s), a, bg)
        c.circ(wx, y, 16 * s, (120, 130, 175), a, bg=bg)
    fw = max(5, 13 * s)
    c.line([(rx, y), st, (bbx, bby), (rx, y)], col, fw, a, bg)
    c.line([st, hd], col, fw, a, bg); c.line([hb, (bbx, bby)], col, fw, a, bg)
    c.line([hd, hb, (fx, y)], col, fw, a, bg)
    c.line([hd, (hd[0] - 8 * s, y - 262 * s), (hd[0] + 72 * s, y - 276 * s)], col, fw, a, bg)
    c.line([st, (st[0] - 12 * s, y - 244 * s)], col, fw, a, bg)
    c.rr(st[0] - 74 * s, y - 266 * s, st[0] + 56 * s, y - 238 * s, 13 * s, (120, 130, 175), a, bg=bg)
    if show_chain > .01:
        k = a * show_chain; lw = max(4, 10 * s)
        if chain == 'rear':
            c.line([(rx, y - 18 * s), (bbx, bby - 38 * s)], chcol, lw, k, bg); c.line([(rx, y + 18 * s), (bbx, bby + 38 * s)], chcol, lw, k, bg)
            pts = [(rx, y - 18 * s), (bbx, bby - 38 * s), (bbx, bby + 38 * s), (rx, y + 18 * s)]
        else:
            c.line([(rx, y - 24 * s), (fx, y - 24 * s)], chcol, lw, k, bg); c.line([(rx, y + 24 * s), (fx, y + 24 * s)], chcol, lw, k, bg)
            c.circ(fx, y, 26 * s, None, k, outline=chcol, ow=lw, bg=bg); c.circ(rx, y, 26 * s, None, k, outline=chcol, ow=lw, bg=bg)
    c.circ(bbx, bby, 38 * s, None, a, outline=METAL, ow=max(4, 8 * s), bg=bg)
    an = t * 1.4
    for sg in (1, -1):
        px, py = bbx + sg * 66 * s * math.cos(an), bby + sg * 66 * s * math.sin(an)
        c.line([(bbx, bby), (px, py)], METAL, max(4, 8 * s), a, bg)
        c.rr(px - 24 * s, py - 7 * s, px + 24 * s, py + 7 * s, 4, INK, a, bg=bg)

def zipper(c, cx, y0, y1, ys, a, cut=0.0, bg=BG, tw=44, gap=1.0, tab=1.0):
    """Close-up of a vertical zipper. Below the slider (y > ys) the rows are locked; above it they splay apart."""
    if a <= .01: return
    pitch = 34; n = int((y1 - y0) / pitch) + 1
    def d(y): return min(250, max(0, (ys - 66 - y)) * .62 + 42) * gap if y < ys else 0.0
    edgeL = [(cx - d(y0 + i * 10) - tw - 44, y0 + i * 10) for i in range(int((y1 - y0) / 10) + 1)]
    edgeR = [(cx + d(y0 + i * 10) + tw + 44, y0 + i * 10) for i in range(int((y1 - y0) / 10) + 1)]
    c.line(edgeL, TAPE, 92, a, bg); c.line(edgeR, TAPE, 92, a, bg)
    for i in range(n):
        y = y0 + i * pitch; dd = d(y)
        xl = cx - dd; xr = cx + d(y + pitch / 2)
        c.rr(xl - tw - 6, y - 11, xl + tw * .42, y + 11, 8, TA, a, bg=TAPE)
        c.circ(xl + tw * .42, y, 11, TA, a, bg=TAPE)
        c.rr(xr - tw * .42, y + pitch / 2 - 11, xr + tw + 6, y + pitch / 2 + 11, 8, TB, a, bg=TAPE)
        c.circ(xr - tw * .42, y + pitch / 2, 11, TB, a, bg=TAPE)
    body = [(cx - 118, ys - 84), (cx + 118, ys - 84), (cx + 92, ys + 70), (cx - 92, ys + 70)]
    poly(c, body, METAL, a, bg)
    c.line(body + [body[0]], (240, 244, 255), 4, a, bg)
    if cut > .01:
        k = a * cut
        poly(c, [(cx - 104, ys - 76), (cx + 104, ys - 76), (cx + 80, ys + 62), (cx - 80, ys + 62)], DARK, k, METAL)
        for sg in (-1, 1):
            c.line([(cx + sg * 72, ys - 76), (cx + sg * 8, ys - 4)], REAL, 34, k, DARK)
        c.line([(cx, ys - 6), (cx, ys + 60)], REAL, 42, k, DARK)
    if tab > .01:
        c.circ(cx, ys + 8, 15, (240, 244, 255), a * (1 - cut) * tab, bg=METAL)
        c.rr(cx - 30, ys + 30, cx + 30, ys + 168, 16, METAL, a * (1 - cut) * tab, outline=(240, 244, 255), ow=4)

def meter(c, x, y, w, val, col, a, bg=BG, lab=True):
    """A one-to-seven confidence scale; val is 1..7."""
    if a <= .01: return
    c.rr(x, y - 16, x + w, y + 16, 16, (44, 52, 94), a, bg=bg)
    c.rr(x, y - 16, x + max(32, w * (val - 1) / 6), y + 16, 16, col, a, bg=bg)
    if lab:
        c.text(x - 28, y, '1', 34, DIM, a, w='Bold', bg=bg); c.text(x + w + 28, y, '7', 34, DIM, a, w='Bold', bg=bg)

def toilet(c, x, y, s, a, col=WORLD, bg=CARD):
    c.rr(x + 14 * s, y - 92 * s, x + 74 * s, y - 2 * s, 8 * s, col, a, bg=bg)
    c.rr(x - 72 * s, y - 16 * s, x + 44 * s, y + 18 * s, 14 * s, col, a, bg=bg)
    poly(c, [(x - 52 * s, y + 14 * s), (x + 34 * s, y + 14 * s), (x + 18 * s, y + 70 * s), (x - 26 * s, y + 70 * s)], col, a, bg)

def sewing(c, x, y, s, a, col=WORLD, bg=CARD):
    c.rr(x - 90 * s, y + 42 * s, x + 90 * s, y + 66 * s, 8 * s, col, a, bg=bg)
    c.rr(x + 38 * s, y - 60 * s, x + 80 * s, y + 46 * s, 10 * s, col, a, bg=bg)
    c.rr(x - 78 * s, y - 72 * s, x + 80 * s, y - 34 * s, 12 * s, col, a, bg=bg)
    c.rr(x - 72 * s, y - 34 * s, x - 42 * s, y + 4 * s, 4 * s, col, a, bg=bg)
    c.line([(x - 57 * s, y + 4 * s), (x - 57 * s, y + 36 * s)], INK, max(3, 5 * s), a, bg)

def mini_zip(c, x, y, s, a, col=WORLD, bg=CARD):
    for k in range(7):
        yy = y - 66 * s + k * 22 * s
        c.rr(x - 26 * s, yy - 6 * s, x + 2 * s, yy + 2 * s, 3, col, a, bg=bg)
        c.rr(x - 2 * s, yy + 3 * s, x + 26 * s, yy + 11 * s, 3, col, a, bg=bg)
    c.rr(x - 30 * s, y - 92 * s, x + 30 * s, y - 62 * s, 8 * s, INK, a, bg=bg)

def snowflake(c, x, y, r, col, a, t=0.0):
    for k in range(6):
        an = k * math.pi / 3 + t * .15
        ex, ey = x + r * math.cos(an), y + r * math.sin(an)
        c.line([(x, y), (ex, ey)], col, 9, a)
        mx, my = x + r * .62 * math.cos(an), y + r * .62 * math.sin(an)
        for sg in (-1, 1):
            c.line([(mx, my), (mx + r * .26 * math.cos(an + sg * .9), my + r * .26 * math.sin(an + sg * .9))], col, 7, a)

def head(c, x, y, s, a, col=(44, 52, 94), bg=BG):
    """A simple head in profile facing right."""
    if a <= .01: return
    c.circ(x, y, 120 * s, col, a, bg=bg)
    poly(c, [(x + 108 * s, y - 16 * s), (x + 152 * s, y + 26 * s), (x + 104 * s, y + 42 * s)], col, a, bg)
    c.rr(x - 62 * s, y + 90 * s, x + 56 * s, y + 200 * s, 24 * s, col, a, bg=bg)

def paper(c, x0, y0, x1, y1, a, bg=BG):
    c.rr(x0, y0, x1, y1, 14, PAPER, a, bg=bg)

def thumb_art(c):
    """A huge zipper with its slider part way up, the rows splayed above."""
    zipper(c, 1510, 40, 1050, 620, 1.0, 0.0, BG, tw=52, gap=.82)
    c.circ(1510, 210, 90, BG, .92); c.text(1510, 210, '?', 130, FEEL, 1, w='Bold')

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(4), 0.0, .5)
    if a > 0:
        c.text(960, 150, 'Over a third said: the chain goes around both wheels', 56, WRONG, a * (1 - hl(1)), w='Bold')
        c.text(960, 150, 'A bike like that could never steer', 70, WRONG, a * hl(1) * (1 - hl(2)), w='Bold')
        c.text(960, 150, 'Nearly all had learned to ride as kids', 66, FEEL, a * hl(2) * (1 - hl(3)), w='Bold')
        c.text(960, 150, 'One test. One reason. One fix.', 72, INK, a * hl(3), w='Bold')
        k = a * (1 - hl(3))
        if k > 0:
            bike(c, 960, 580, 1.25, k, 'both', WRONG, WORLD, t * (1 - hl(1)))
            c.rr(650, 802, 1270, 866, 30, BG, k * (1 - hl(1)), outline=DIM, ow=3); c.text(960, 834, 'Study of non-cyclists', 38, DIM, k * (1 - hl(1)), w='Bold')
            if hl(1) > 0:
                c.cross(960 + 337, 580, 80, WRONG, k * hl(1))
                c.text(1640, 580, 'jammed', 46, WRONG, k * hl(1), w='Bold')
            if hl(2) > 0:
                c.text(960, 836, 'Over 96% in the study learned as children', 42, FEEL, k * hl(2), w='Bold')
        if hl(3) > 0:
            for j, (big, lab, col) in enumerate((('1', 'test', FEEL), ('1', 'reason', WORLD), ('1', 'fix', REAL))):
                m = a * fd(T(3), .2 + j * .55)
                x = 420 + j * 540
                c.rr(x - 220, 320, x + 220, 780, 30, CARD, m, outline=col, ow=5)
                c.text(x, 470, big, 170, col, m, w='Bold', bg=CARD); c.text(x, 660, lab, 70, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .1, .6)
        c.text(960, 230 + 30 * (1 - m), 'The Zipper Test', 132, FEEL, m, w='Bold')
        c.text(960, 370 + 30 * (1 - m), 'You know less than you feel', 74, INK, m, w='Bold')
        c.line([(960 - 400 * m, 450), (960 + 400 * m, 450)], WORLD, 8, m)
        zipper(c, 960, 500, 880, lerp(820, 640, fd(T(4), .4, 1.6)), m, 0.0, BG, tw=38, gap=.8, tab=0)

def s_test(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The test comes from Yale, 2002', 70, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Graduate students rated their understanding', 62, FEEL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Everyday things, from 1 to 7', 70, FEEL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Now explain it, step by step, in writing', 64, WORLD, hl(3) * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'What happened to the scores?', 72, YE, hl(4), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        c.rr(690, 340, 1230, 460, 60, WORLD, k * fd(T(0), .1)); c.text(960, 400, 'Yale, 2002', 76, BG, k * fd(T(0), .1), w='Bold', bg=WORLD)
        for j in range(4):
            m = k * fd(T(0), .7 + j * .12); x = 420 + j * 360
            c.circ(x, 610, 62, CARD, m, outline=(90, 100, 150), ow=4)
            c.rr(x - 60, 690, x + 60, 820, 30, CARD, m, outline=(90, 100, 150), ow=4)
    k1 = hl(1) * (1 - hl(3))
    if k1 > 0:
        rows = ((mini_zip, 'zipper', 6.0), (toilet, 'flush toilet', 5.6), (sewing, 'sewing machine', 5.0))
        for j, (fn, lab, v) in enumerate(rows):
            y = 340 + j * 190; m = k1 * (1 if j == 0 else hl(2) * fd(T(2), .5 * j))
            c.rr(280, y - 84, 1640, y + 84, 22, CARD, m, outline=(60, 70, 120), ow=3)
            fn(c, 390, y, .95, m)
            c.text(500, y, lab, 46, INK, m, anchor='lm', w='Bold', bg=CARD)
            meter(c, 980, y, 560, lerp(1, v, fd(T(1), .4 + j * .2, 1.2) if j == 0 else fd(T(2), .4 * j, 1.1)), FEEL, m, CARD)
        c.text(1640, 856, 'Illustrative scores', 30, DIM, k1, anchor='rm', w='Regular')
    k3 = hl(3)
    if k3 > 0:
        paper(c, 520, 260, 1400, 850, k3)
        for j, (txt, tc) in enumerate((('How a zipper works', INK), ('Step 1: pull the tab', PAPINK), ('Step 2: the teeth...', PAPINK), ('Step 3: ...', WRONG))):
            if j == 3: tc = WRONG
            m = k3 * fd(T(3), .4 + j * .5)
            c.text(590, 340 + j * 118, txt, 56 if j == 0 else 52, tc, m, anchor='lm', w='Bold', bg=PAPER)
        if T(4) > 0:
            c.circ(1290, 650, 92, FEEL, hl(4), bg=PAPER); c.text(1290, 650, '?', 130, BG, hl(4), w='Bold', bg=FEEL)

STEPS = [('Before', 3.9, FEEL), ('After explaining', 3.1, WORLD), ('After one question', 2.5, WRONG)]
def s_drop(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'They fell', 84, WRONG, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'One sharp question: how would you pick a lock?', 58, WRONG, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Nobody said they were wrong', 72, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'The illusion of explanatory depth', 72, YE, hl(3), w='Bold')
    k = 1 - hl(3)
    if k > 0:
        base = 800; x0 = 420; unit = 88
        c.line([(x0 - 60, base), (1560, base)], (90, 100, 150), 4, k)
        for v in (1, 3, 5, 7):
            yy = base - (v - 1) * unit
            c.line([(x0 - 60, yy), (x0 - 40, yy)], DIM, 3, k); c.text(x0 - 90, yy, str(v), 34, DIM, k, w='Bold')
        vis = (fd(T(0), -.2, .3), fd(T(0), .4, .6), fd(T(1), 1.2, .6))
        for j, (lab, v, col) in enumerate(STEPS):
            x = x0 + 160 + j * 390; m = k * vis[j]
            hh = (v - 1) * unit * m
            c.rr(x - 100, base - hh, x + 100, base, 12, col, m)
            c.text(x, base - hh - 44, f'{v:.1f}', 62, col, m, w='Bold')
            c.text(x, base + 38, lab, 36, INK, m, w='Bold')
        c.text(1560, 275, 'One group, average self-rating, 1 to 7', 32, DIM, k, anchor='rm', w='Regular')
    if hl(3) > 0:
        m = hl(3)
        c.rr(300, 290, 1620, 800, 30, CARD, m, outline=FEEL, ow=5)
        c.text(960, 400, 'Feels deep', 76, FEEL, m, w='Bold', bg=CARD)
        c.text(960, 480, 'until you try to explain it', 50, INK, m, w='Bold', bg=CARD)
        # a wide shallow pool: looks deep from above, shallow from the side
        poly(c, [(520, 590), (1400, 590), (1400, 640), (520, 640)], WORLD, m * fd(T(3), .8), CARD)
        c.line([(520, 590), (520, 750), (1400, 750), (1400, 590)], (90, 100, 150), 6, m * fd(T(3), .8), CARD)
        c.text(960, 700, 'real depth', 40, DIM, m * fd(T(3), 1.0), w='Bold', bg=CARD)

def s_zip(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Try it. Pull the tab, two rows of teeth close', 62, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'But how? Why don\'t they just jam?', 68, FEEL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A Y-shaped channel tilts each tooth into place', 60, REAL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Did you know that, or just feel you did?', 64, YE, hl(3), w='Bold')
    k = 1 - hl(3)
    ys = lerp(760, 540, fd(T(0), .3, 3.4)) if T(1) < 0 else 540
    if k > 0:
        zipper(c, 960, 240, 850, ys, k, hl(2) * fd(T(2), .0, .9), BG, gap=.92)
        if hl(1) > 0 and hl(2) < 1:
            c.circ(1460, 520, 96, BG, hl(1) * (1 - hl(2)), outline=FEEL, ow=7)
            c.text(1460, 520, '?', 130, FEEL, hl(1) * (1 - hl(2)), w='Bold')
        if hl(2) > 0:
            m = k * hl(2)
            c.arrow(1340, 500, 1120, 500, REAL, 8, m, 22)
            c.text(1500, 470, 'Y-shaped', 54, REAL, m, w='Bold'); c.text(1500, 534, 'channel', 54, REAL, m, w='Bold')
            c.text(420, 470, 'Each tooth tilts', 46, INK, m * fd(T(2), 1.5), w='Bold'); c.text(420, 530, 'and hooks in', 46, INK, m * fd(T(2), 1.5), w='Bold')
            c.text(1640, 856, 'Simplified drawing', 30, DIM, k * hl(2), anchor='rm', w='Regular')
    if hl(3) > 0:
        for x, big, col in ((540, 'I knew that', REAL), (1380, 'I felt I knew', FEEL)):
            m = hl(3)
            c.rr(x - 360, 340, x + 360, 720, 30, CARD, m, outline=col, ow=5)
            if col == REAL: c.check(x, 470, 80, col, m, 1)
            else: c.text(x, 470, '?', 150, col, m, w='Bold', bg=CARD)
            c.text(x, 620, big, 62, col, m, w='Bold', bg=CARD)

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    ans = hl(3)
    c.text(960, 150, 'One group was warned first', 72, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Quick question', 74, YE, hl(1) * (1 - ans), w='Bold')
    c.text(960, 240, 'Did the warning stop the illusion?', 54, INK, hl(1) * (1 - ans), w='Bold')
    c.text(960, 150, 'No. It shrank, but it held', 76, WRONG, ans * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'Another university: same pattern', 70, INK, hl(4), w='Bold')
    k = 1 - hl(1)
    if k > 0:
        paper(c, 440, 280, 1480, 800, k)
        c.text(960, 400, 'NOTICE', 76, WRONG, k * fd(T(0), .3), w='Bold', bg=PAPER)
        c.text(960, 540, 'You will have to explain', 66, INK, k * fd(T(0), .7), w='Bold', bg=PAPER)
        c.text(960, 630, 'some of these, in detail', 66, INK, k * fd(T(0), .7), w='Bold', bg=PAPER)
    k2 = hl(1) * (1 - ans)
    if k2 > 0:
        for j, (lab, x, col) in enumerate((('A  Yes, gone', 560, REAL), ('B  No, still there', 1360, WRONG))):
            m = k2 * fd(T(1), 1.0 + j * .5)
            c.rr(x - 340, 340, x + 340, 780, 30, CARD, m, outline=(70, 80, 130), ow=3)
            c.text(x, 440, lab, 56, INK, m, w='Bold', bg=CARD)
            if j == 0: c.circ(x, 620, 90, None, m, outline=DIM, ow=6, bg=CARD)
            else: c.circ(x, 620, 90, FEEL, m, bg=CARD)
    if T(2) > 0 and ans < .99:
        p = clamp(T(2) / 1.6); n = 3 - min(2, int(T(2) / .55)); m = 1 - ans
        c.circ(960, 580, 90, BG, m); ring(c, 960, 580, 82, p, YE, m); c.text(960, 580, str(n), 90, YE, m, w='Bold')
    k3 = ans * (1 - hl(4))
    if k3 > 0:
        for x, r, lab in ((560, 210, 'no warning'), (1360, lerp(210, 130, fd(T(3), .3, 1.0)), 'warned')):
            c.circ(x, 540, r, FEEL, k3 * .9)
            c.text(x, 540, 'illusion', 52 if r > 150 else 44, BG, k3, w='Bold', bg=FEEL)
            c.text(x, 800, lab, 46, INK, k3, w='Bold')
        c.text(1640, 856, 'Drawing, not data', 30, DIM, k3, anchor='rm', w='Regular')
    k4 = hl(4)
    if k4 > 0:
        for j, (lab, x) in enumerate((('Yale', 560), ('A less selective university', 1360))):
            m = k4 * fd(T(4), .2 + j * .7)
            c.rr(x - 380, 320, x + 380, 790, 30, CARD, m, outline=(70, 80, 130), ow=3)
            c.text(x, 400, lab, 48, INK, m, w='Bold', bg=CARD)
            c.arrow(x - 120, 480, x + 120, 720, WRONG, 16, m, 44)
        c.text(960, 850, 'Confidence fell in both', 44, WRONG, k4, w='Bold')

def s_spares(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'It doesn\'t hit everything', 74, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Capitals: confidence fell much less', 68, REAL, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Cookies and movie plots: no drop at all', 64, REAL, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'It strikes hardest on how things work', 66, WRONG, hl(3), w='Bold')
    rows = (('How things work', 'big drop', 120, WRONG, 0), ('Country capitals', 'small drop', 34, FEEL, 1), ('Baking cookies', 'no drop', 0, REAL, 2), ('Movie plots', 'no drop', 0, REAL, 2))
    for j, (lab, res, drop, col, g) in enumerate(rows):
        x = 280 + j * 453
        m = (fd(T(0), .3) if g == 0 else hl(g))
        if j == 3: m *= fd(T(2), .9)
        if hl(3) > 0 and j != 0: m *= 1 - .6 * hl(3)
        c.rr(x - 205, 260, x + 205, 830, 26, CARD, m, outline=col, ow=4)
        c.text(x, 330, lab, 44, INK, m, w='Bold', bg=CARD)
        gg = fd(T(g), .5, .9)
        c.line([(x - 130, 460), (x + 130, 460 + drop * 2 * gg)], col, 16, m, CARD)
        c.circ(x - 130, 460, 18, col, m, bg=CARD); c.circ(x + 130, 460 + drop * 2 * gg, 18, col, m, bg=CARD)
        c.text(x, 760, res, 52, col, m, w='Bold', bg=CARD)
    c.text(1640, 856, 'Pattern only, not to scale', 30, DIM, 1, anchor='rm', w='Regular')

def groups(c, m0, m1, g0, g1):
    """The two chain-error bars, as whole people out of ten is avoided: plain bars with exact percentages."""
    for x, m, g, v, lab, col in ((560, m0, g0, 44, 'no bike to look at', WRONG), (1360, m1, g1, 12, 'real bike in front of them', REAL)):
        if m <= .01: continue
        hh = v * 7.6 * g
        c.rr(x - 150, 780 - hh, x + 150, 780, 14, col, m)
        c.text(x, 780 - hh - 52, f'{int(round(v * g))}%', 84, col, m, w='Bold')
        c.text(x, 826, lab, 44, INK, m, w='Bold')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Why? Back to the bike', 74, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Chain drawn wrong, non-cyclists', 66, WRONG, hl(1) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'The knowledge was in the bike', 72, WORLD, hl(3) * (1 - hl(4)), w='Bold')
    c.text(960, 150, 'You see the parts, and file it as "I understand"', 58, FEEL, hl(4) * (1 - hl(5)), w='Bold')
    c.text(960, 150, 'And nothing ever tests you', 72, YE, hl(5), w='Bold')
    k0 = 1 - hl(1)
    if k0 > 0:
        bike(c, 960, 590, 1.2, k0, 'rear', REAL, WORLD, t, show_chain=fd(T(0), 1.0))
    k1 = hl(1) * (1 - hl(3))
    if k1 > 0:
        groups(c, k1, k1 * hl(2), fd(T(1), .3, 1.0), fd(T(2), .3, 1.0))
        c.text(1640, 275, 'Two separate groups', 32, DIM, k1, anchor='rm', w='Regular')
    k3 = hl(3) * (1 - hl(4))
    if k3 > 0:
        head(c, 480, 460, 1.3, k3)
        c.text(480, 460, 'fuzzy', 44, DIM, k3, w='Bold', bg=(44, 52, 94))
        bike(c, 1330, 590, .95, k3, 'rear', REAL, WORLD, t)
        c.text(1330, 300, 'the facts are here', 46, WORLD, k3 * fd(T(3), .8), w='Bold')
        c.arrow(1040, 540, 760, 540, WORLD, 9, k3 * fd(T(3), .5), 26)
    k4 = hl(4) * (1 - hl(5))
    if k4 > 0:
        for j, (lab, x, col) in enumerate((('I can see it', 500, WORLD), ('I understand it', 1420, FEEL))):
            c.rr(x - 320, 380, x + 320, 690, 30, CARD, k4, outline=col, ow=5)
            c.text(x, 535, lab, 66, col, k4 * fd(T(4), j * 1.2), w='Bold', bg=CARD)
        c.arrow(840, 535, 1080, 535, INK, 10, k4 * fd(T(4), 1.0), 28)
    k5 = hl(5)
    if k5 > 0:
        c.rr(420, 320, 1500, 780, 30, CARD, k5, outline=FEEL, ow=5)
        c.text(960, 430, 'Times this year someone asked you', 54, INK, k5, w='Bold', bg=CARD)
        c.text(960, 510, 'to explain a zipper', 54, INK, k5, w='Bold', bg=CARD)
        c.text(960, 660, '0', 150, FEEL, k5 * fd(T(5), .7), w='Bold', bg=CARD)

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, '2023: explain one thing, like a zipper', 66, INK, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Then rate something unrelated: how snow forms', 60, WORLD, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A small effect, but it spread', 72, YE, hl(2), w='Bold')
    zipper(c, 500, 270, 830, 620, fd(T(0), -.2), 0, BG, tw=30, gap=.6)
    snow_a = hl(1)
    if snow_a > 0:
        snowflake(c, 1340, 430, 130, WORLD, snow_a, t)
        v = lerp(5.0, 4.2, fd(T(1), 1.4, 1.2))
        meter(c, 1100, 680, 480, v, FEEL, snow_a)
        c.text(1340, 620, 'I know how snow forms', 42, FEEL, snow_a, w='Bold')
        c.text(1640, 856, 'Illustrative scale', 30, DIM, snow_a, anchor='rm', w='Regular')
        c.arrow(760, 520, 1000, 480, DIM, 8, snow_a, 24)

def s_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Before you trust it, explain it', 72, REAL, (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Close the book. Talk to an empty chair', 68, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Where you get stuck is what to study', 68, WRONG, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 150, 'Useful, but self-testing rates higher', 66, REAL, hl(3), w='Bold')
    k = 1 - hl(2)
    if k > 0:
        # closed book
        m = k * fd(T(0), -.2)
        c.rr(280, 380, 720, 720, 16, (70, 84, 170), m); c.rr(300, 400, 700, 700, 12, (86, 100, 190), m)
        c.text(500, 550, 'NOTES', 66, INK, m, w='Bold', bg=(86, 100, 190))
        if hl(1) > 0:
            m = k * hl(1); x = 1390
            c.line([(x - 140, 300), (x - 140, 780)], WORLD, 18, m); c.line([(x - 140, 560), (x + 140, 560)], WORLD, 18, m)
            c.line([(x + 140, 560), (x + 140, 780)], WORLD, 18, m); c.line([(x - 140, 300), (x + 40, 300)], WORLD, 18, m)
            c.rr(830, 330, 1190, 500, 40, CARD, m, outline=REAL, ow=4); c.text(1010, 415, 'So first...', 54, REAL, m, w='Bold', bg=CARD)
            c.text(1390, 836, 'an empty chair', 40, WORLD, m, w='Bold')
    k2 = hl(2) * (1 - hl(3))
    if k2 > 0:
        paper(c, 480, 260, 1440, 840, k2)
        for j, (txt, col) in enumerate((('Step 1: makes sense', REAL), ('Step 2: makes sense', REAL), ('Step 3: ...stuck', WRONG))):
            m = k2 * fd(T(2), .3 + j * .5); y = 370 + j * 130
            c.text(560, y, txt, 62, col, m, anchor='lm', w='Bold', bg=PAPER)
        c.rr(540, 700, 1380, 800, 12, (120, 40, 76), k2 * fd(T(2), 1.6), bg=PAPER)
        c.text(960, 750, 'Study this next', 56, INK, k2 * fd(T(2), 1.6), w='Bold', bg=(120, 40, 76))
    k3 = hl(3)
    if k3 > 0:
        for j, (lab, res, col, v) in enumerate((('Explaining it to yourself', 'moderate', FEEL, 5), ('Testing yourself', 'high', REAL, 8))):
            y = 400 + j * 220
            c.text(420, y - 52, lab, 50, INK, k3, anchor='lm', w='Bold')
            c.rr(420, y, 420 + 110 * v * fd(T(3), .3 + j * .4, .9), y + 60, 12, col, k3)
            c.text(1360, y + 30, res, 54, col, k3 * fd(T(3), 1.2), anchor='lm', w='Bold')

RECAP = [('Feeling you understand', "isn't understanding", FEEL),
         ('Seeing the parts', 'fools your brain', WORLD),
         ('Explain it out loud', 'and the gaps show up', REAL)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 150, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    zipper(c, 330, 240, 860, 640, fd(T(0)) * out, 0, BG, tw=30, gap=.55)
    for i, (l1, l2, col) in enumerate(RECAP):
        m = fd(T(i + 1)) * out; y = 340 + i * 190
        if m <= .01: continue
        c.rr(640, y - 80, 1700, y + 80, 22, CARD, m, outline=col, ow=4)
        c.text(690, y - 30, l1, 50, col, m, anchor='lm', w='Bold', bg=CARD)
        c.text(690, y + 32, l2, 48, INK, m, anchor='lm', w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

# Lesson of 2026-11-04: open on one surprising fact, then a one-line roadmap, then a fresh surprise in each scene.
SCENES = [
 ('INTRO', ["In one study, over a third of non-cyclists said a bike chain loops around both wheels.",
            "A bike like that could never steer.",
            "Yet nearly all had learned to ride as kids.",
            "So here's one test, one reason, and one fix.",
            "Because your brain is fooling you too."], s_hook),
 ('1  ·  THE TEST', ["It comes from Yale, in 2002.",
            "Graduate students rated how well they understood everyday things, from one to seven.",
            "A zipper. A flush toilet. A sewing machine.",
            "Then the hard part. Explain it, step by step, in writing.",
            "What happened to their scores?"], s_test),
 ('2  ·  THE DROP', ["They fell. In one group, the average dropped from about three point nine to three point one.",
            "Then one sharp question, like how would you pick a lock? Two and a half.",
            "Nobody told them they were wrong. Trying to explain was enough.",
            "It's called the illusion of explanatory depth."], s_drop),
 ('3  ·  YOUR TURN', ["Try it. You pull a zipper's tab, and two rows of teeth close.",
            "But how? Why don't they just jam?",
            "The slider hides a Y-shaped channel. It tilts each tooth so it hooks into its neighbours.",
            "Did you know that, or only feel you did?"], s_zip),
 ('4  ·  QUICK QUESTION', ["Some students were warned first: you will have to explain these.",
            "Quick question. Did that warning stop the illusion?",
            "Three, two, one.",
            "No. It shrank, but it held.",
            "Students at a less selective university showed the same pattern. This isn't about being clever."], s_quiz),
 ('5  ·  THE EXCEPTIONS', ["But it doesn't hit everything.",
            "Country capitals? Confidence fell much less. You know it or you don't.",
            "Baking cookies? Movie plots? No drop at all.",
            "It strikes hardest on how things work."], s_spares),
 ('6  ·  THE REASON', ["So why? Back to the bike.",
            "With no bike to look at, forty-four percent of one group drew the chain wrong.",
            "A different group had a real bike right there. Just twelve percent.",
            "The knowledge was in the bike, not in their heads.",
            "You see the parts every day, and your brain files that as understanding.",
            "And nobody ever asks you to explain, so nothing corrects it."], s_why),
 ('7  ·  THE SPREAD', ["In 2023, researchers had people explain one thing, like a zipper.",
            "Afterwards, they said they knew less about unrelated things, like how snow forms.",
            "The effect was small, but it seems to spread."], s_twist),
 ('8  ·  THE FIX', ["Here's the fix. Before you trust that you know something, explain it.",
            "Close the book. Say it out loud, step by step, to an empty chair.",
            "Wherever you get stuck, that's exactly what to study next.",
            "A big review rated this moderately useful. Testing yourself rated higher, so do both."], s_fix),
 ('RECAP', ["So remember three things.",
            "One. Feeling you understand isn't the same as understanding.",
            "Two. Seeing the parts fools your brain.",
            "Three. Explain it out loud, and the gaps show up.",
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

def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'Do you really know how a zipper works?', 68, FEEL, 1 - hl(1), w='Bold')
    c.text(960, 170, 'You feel you do, until you try to explain it', 64, INK, hl(1), w='Bold')
    zipper(c, 960, 290, 860, lerp(800, 560, fd(t, .1, 3.0)), 1.0, 0, BG, gap=.9, tab=1)
    if hl(1) > 0:
        c.circ(1470, 520, 100, BG, hl(1), outline=FEEL, ow=7); c.text(1470, 520, '?', 130, FEEL, hl(1), w='Bold')

def short_drop(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'People rated how well they understood', 66, FEEL, 1 - hl(1), w='Bold')
    c.text(960, 170, 'Then they had to explain it. Scores fell', 66, WRONG, hl(1), w='Bold')
    rows = ((mini_zip, 'zipper'), (toilet, 'flush toilet'))
    for j, (fn, lab) in enumerate(rows):
        y = 400 + j * 230; m = fd(T(0), .3 + j * .4)
        c.rr(240, y - 100, 1680, y + 100, 22, CARD, m, outline=(60, 70, 120), ow=3)
        fn(c, 360, y, 1.05, m)
        c.text(480, y, lab, 54, INK, m, anchor='lm', w='Bold', bg=CARD)
        v = lerp(lerp(1, 5.8 - j * .4, fd(T(0), .8, 1.0)), 3.2 - j * .3, fd(T(1), 2.0, 1.4) if T(1) > 0 else 0)
        meter(c, 1040, y, 540, v, FEEL if T(1) < 2.0 else WRONG, m, CARD)
    c.text(1680, 856, 'Illustrative scores', 30, DIM, 1, anchor='rm', w='Regular')

def short_name(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'The illusion of explanatory depth', 72, YE, 1 - hl(1), w='Bold')
    c.text(960, 170, 'You see the parts, and file it as understanding', 58, FEEL, hl(1), w='Bold')
    for j, (lab, x, col) in enumerate((('I can see it', 500, WORLD), ('I understand it', 1420, FEEL))):
        m = fd(T(0), .3) if j == 0 else hl(1)
        c.rr(x - 330, 340, x + 330, 720, 30, CARD, m, outline=col, ow=5)
        c.text(x, 530, lab, 68, col, m, w='Bold', bg=CARD)
    c.arrow(840, 530, 1080, 530, INK, 10, hl(1), 28)

def short_proof(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'Chain drawn wrong, non-cyclists', 68, WRONG, 1, w='Bold')
    groups(c, fd(T(0), .1), hl(1), fd(T(0), .3, 1.0), fd(T(1), .3, 1.0))
    c.text(1640, 275, 'Two separate groups', 32, DIM, 1, anchor='rm', w='Regular')

def short_answer(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'A Y-shaped channel tilts each tooth into place', 60, REAL, 1 - hl(1), w='Bold')
    c.text(960, 170, 'If you couldn\'t explain that, you felt the illusion', 56, FEEL, hl(1), w='Bold')
    zipper(c, 760 if hl(1) == 0 else lerp(760, 560, hl(1)), 290, 860, 560, 1.0, fd(T(0), .3, .8), BG, gap=.9)
    c.text(1400, 500, 'Y-shaped', 62, REAL, fd(T(0), .8), w='Bold'); c.text(1400, 572, 'channel', 62, REAL, fd(T(0), .8), w='Bold')

# The Short: its own complete mini-story (hook -> the test -> the name and reason -> proof -> the zipper answer, then 'Can you explain it?').
SHORT_SCENES = [
 ('THE HOOK', ["Can you explain how a zipper works?",
               "Most people feel they can, until they try."], short_open),
 ('THE TEST', ["At Yale, students rated how well they understood things like zippers and toilets.",
               "Then they had to explain each one, step by step. Their scores fell."], short_drop),
 ('THE NAME', ["It's called the illusion of explanatory depth.",
               "You see the parts every day, and your brain files that as understanding."], short_name),
 ('PROOF', ["In one study, forty-four percent of non-cyclists drew a bike chain wrong.",
            "With a real bike in front of them, just twelve percent did."], short_proof),
 ('THE ANSWER', ["So how does a zipper work? A Y-shaped channel in the slider tilts each tooth, so it hooks in.",
                 "Could you have explained that? If not, you just felt the illusion."], short_answer),
]
SHORT_HITS = [(4, 0, 0.0)]
