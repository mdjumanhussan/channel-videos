"""Episode: Why You Forget What You Study (and How to Fix It)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why You Forget What You Study'     # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {'Ebbinghouse': 'Ebbinghaus'}      # narration is spelled for the voice; captions show the real name
SHORT_HOOK = 'Why do you forget what you study?'   # headline on the vertical Short
HITS = [(0, 4, 0.2), (3, 4, 0.0), (8, 4, 0.0)]     # title card, the key result, the closing line
THUMB = ['WHY YOU', 'FORGET WHAT', 'YOU STUDY']

PAPER = (226, 231, 246); RULE = (120, 130, 172); RED = (235, 50, 60)
FIELD = (18, 52, 50); GRASS = (40, 110, 84); POT = (190, 110, 70); LEAF = (90, 225, 150)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def page(c, x0, y0, x1, y1, a=1.0, bg=BG, n=7, keep=1.0, hi=(), wrote=1.0, seed=0):
    """Sheet of paper with n ruled text lines. keep<1 fades lines away (bottom first). hi = line indexes with highlighter.
    wrote<1 shows only the first part of the text (being written)."""
    if a <= 0.01: return
    c.rr(x0, y0, x1, y1, 14, PAPER, a, bg=bg)
    pad = (x1 - x0) * .12; h = (y1 - y0 - 2 * pad) / max(1, n - 1) if n > 1 else 0
    for i in range(n):
        y = y0 + pad + i * h; wl = (x1 - x0 - 2 * pad) * (.62 + .38 * abs(math.sin(i * 2.3 + seed + 1)))
        la = clamp(keep * n - (n - 1 - i)) if keep < 1 else 1.0
        if wrote < 1:
            q = clamp(wrote * n - i); wl *= q
            if q <= 0: continue
        if i in hi: c.rr(x0 + pad - 6, y - 15, x0 + pad + wl + 6, y + 15, 6, YE, a * .75, bg=PAPER)
        c.line([(x0 + pad, y), (x0 + pad + wl, y)], RULE, 7, a * (.12 + .88 * la), PAPER)

def openbook(c, x, y, w, h, a=1.0, bg=BG, keep=1.0, scan=None):
    """Open book centred on x. scan (0..1) moves a reading marker down the pages."""
    if a <= 0.01: return
    c.rr(x - w / 2 - 14, y + 10, x + w / 2 + 14, y + h + 16, 18, (70, 82, 150), a, bg=bg)
    page(c, x - w / 2, y, x - 5, y + h, a, bg, 7, keep, seed=0)
    page(c, x + 5, y, x + w / 2, y + h, a, bg, 7, keep, seed=4)
    c.line([(x, y + 4), (x, y + h + 10)], (70, 82, 150), 6, a, bg)
    if scan is not None:
        side = 0 if scan < .5 else 1; q = (scan * 2) % 1
        xs = x - w / 2 + 16 if side == 0 else x + 21
        yy = y + h * (.1 + .8 * q)
        c.rr(xs, yy - 16, xs + w / 2 - 37, yy + 16, 8, CY, a * .45, bg=PAPER)

def closedbook(c, x, y, w, h, a=1.0, bg=BG, col=PU):
    if a <= 0.01: return
    c.rr(x - w / 2, y, x + w / 2, y + h, 14, col, a, bg=bg)
    c.rr(x - w / 2, y, x - w / 2 + w * .14, y + h, 14, mix(col, .6, (10, 12, 30)), a, bg=bg)
    c.rr(x - w * .2, y + h * .22, x + w * .34, y + h * .34, 6, PAPER, a * .9, bg=col)
    c.rr(x - w * .2, y + h * .42, x + w * .2, y + h * .5, 6, PAPER, a * .6, bg=col)

def axes(c, x0, y0, x1, y1, a=1.0, xl='Time', yl='Memory', bg=BG):
    c.arrow(x0, y1, x0, y0 - 20, DIM, 4, a, 14); c.arrow(x0, y1, x1 + 20, y1, DIM, 4, a, 14)
    c.text(x1 + 10, y1 + 38, xl, 30, DIM, a, 'rm', 'Medium', bg=bg)
    c.text(x0 + 16, y0 - 22, yl, 30, DIM, a, 'lm', 'Medium', bg=bg)

def decay(u, k=6.0, floor=.2): return floor + (1 - floor) * math.exp(-k * u)

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def rot(px, py, ox, oy, deg):
    q = math.radians(deg); dx, dy = px - ox, py - oy
    return ox + dx * math.cos(q) - dy * math.sin(q), oy + dx * math.sin(q) + dy * math.cos(q)

def bike(c, x, y, a=1.0, tilt=0.0, spin=0.0, bg=BG):
    """Bicycle with its wheels resting on height y."""
    R = 62; oy = y; P = lambda px, py: rot(px, py, x, oy, tilt)
    for wx in (x - 100, x + 100):
        cx, cy = P(wx, y - R); c.circ(cx, cy, R, None, a, outline=INK, ow=7, bg=bg)
        for k in range(4):
            q = spin + k * math.pi / 4
            c.line([(cx - (R - 6) * math.cos(q), cy - (R - 6) * math.sin(q)), (cx + (R - 6) * math.cos(q), cy + (R - 6) * math.sin(q))], DIM, 2, a * .7, bg)
    fr = [(x - 100, y - R), (x - 30, y - R - 95), (x + 62, y - R - 95), (x + 100, y - R)]
    c.line([P(*p) for p in fr], CY, 8, a, bg)
    c.line([P(x - 30, y - R - 95), P(x + 5, y - R), P(x - 100, y - R)], CY, 8, a, bg)
    c.line([P(x + 5, y - R), P(x + 62, y - R - 95)], CY, 8, a, bg)
    c.line([P(x - 52, y - R - 112), P(x - 8, y - R - 112)], INK, 10, a, bg)
    c.line([P(x - 30, y - R - 95), P(x - 30, y - R - 112)], CY, 8, a, bg)
    c.line([P(x + 62, y - R - 95), P(x + 70, y - R - 128), P(x + 100, y - R - 134)], INK, 8, a, bg)

def bar(c, x, base, w, hmax, val, p, col, a=1.0, lab='', bg=CARD):
    """Vertical bar for a percentage value (0-100), growing with p."""
    h = hmax * val / 100 * ease(p)
    c.rr(x - w / 2, base - h, x + w / 2, base, 10, col, a, bg=bg)
    if p > .85: c.text(x, base - h - 34, f'{val}%', 44, col, a * fd(p, .85, .3), w='Bold', bg=bg)
    if lab: c.text(x, base + 34, lab, 26, DIM, a, w='Medium', bg=bg)

def thumb_art(c):
    x0, y0, x1, y1 = 1190, 300, 1800, 760
    axes(c, x0, y0, x1, y1, 1, '', '')
    pts = [(x0 + (x1 - x0) * u / 60, y1 - (y1 - y0) * decay(u / 60, 6, .14)) for u in range(61)]
    c.line(pts, PK, 16)
    c.circ(pts[0][0], pts[0][1], 26, YE); c.circ(pts[-1][0], pts[-1][1], 22, PK)
    c.text(1560, 430, '?', 230, YE, 1, w='Bold')

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(4), 0, .5)
    if a > 0:
        # the common belief goes on screen from the first frame, then gets overturned
        top = a * (1 - fd(T(2), -.3, .4))
        c.text(960, 205, 'Read it 3 times.', 88, INK, top * fd(t, 0, .25), w='Bold')
        keep = 1 - .9 * ease(T(1, .3) / 2.2) if T(1) > 0 else 1.0
        n = min(3, 1 + int(t / 1.05)); reading = T(1) < 0
        openbook(c, 720, 330, 760, 400, a, BG, keep, ((t / 1.05) % 1) if reading and t < 3.15 else None)
        bm = a * fd(t, .2, .3) * (1 - fd(T(1), 0, .4))
        c.circ(1240, 400, 62, CY, bm); c.text(1240, 400, f'{n}x', 54, BG, bm, w='Bold', bg=CY)
        km = a * fd(T(0), 2.6) * (1 - fd(T(1), 0, .4))
        c.rr(1340, 480, 1800, 640, 34, CARD, km, outline=GR, ow=4)
        c.text(1570, 560, '"I know this."', 48, GR, km, w='Bold', bg=CARD)
        if T(1) > 0:
            m = a * fd(T(1))
            c.rr(1330, 330, 1810, 660, 26, CARD, m, outline=PK, ow=4)
            c.rr(1330, 330, 1810, 410, 26, PK, m)
            c.text(1570, 370, '1 WEEK LATER', 36, BG, m, w='Bold', bg=PK)
            c.text(1570, 520 + 8 * math.sin(t * 3), '?', 170, PK, m, w='Bold', bg=CARD)
            c.text(720, 810, 'Much of it is gone', 46, PK, m * fd(T(1), 1.0), w='Bold')
        if T(2) > 0:
            m = a * fd(T(2)) * (1 - fd(T(3), -.3, .4))
            c.text(960, 205, 'You are not bad at learning.', 76, GR, m, w='Bold')
        if T(3) > 0:
            m = a * fd(T(3))
            c.text(960, 205, 'Rereading feels better than it works.', 70, YE, m, w='Bold')
    if T(4) > 0:
        m = fd(T(4), .2, .7)
        c.text(960, 390 + 30 * (1 - m), 'Why You Forget', 130, INK, m, w='Bold')
        c.text(960, 550 + 30 * (1 - m), 'What You Study', 130, CY, m, w='Bold')
        c.line([(960 - 260 * m, 660), (960 + 260 * m, 660)], YE, 8, m)
        c.text(960, 735, 'and how to fix it', 48, DIM, fd(T(4), .8), w='Medium')

SYL = ['ZOF', 'KEB', 'DAX', 'MIP', 'WUB', 'LIR']
def s_curve(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 430, '1885', 260, YE, a0, w='Bold')
    c.text(960, 640, 'Forgetting gets measured', 54, INK, a0 * fd(T(0), .8), w='Bold')
    if T(1) < -.1: return
    aL = fd(T(1)) * (1 - fd(T(4), -.3, .4))
    c.text(470, 205, 'Hermann Ebbinghaus', 50, INK, aL, w='Bold')
    for i, s in enumerate(SYL):
        m = aL * fd(T(1), 1.2 + i * .35); x = 250 + (i % 3) * 220; y = 340 + (i // 3) * 150
        c.rr(x - 95, y - 58, x + 95, y + 58, 18, CARD, m, outline=PU, ow=3)
        c.text(x, y, s, 52, INK, m, w='Mono', bg=CARD)
    c.text(470, 590, 'Made-up syllables (examples)', 30, DIM, aL * fd(T(1), 2.4), w='Medium')
    if T(2) > 0:
        for i, lab in enumerate(['Minutes', 'Hours', 'Days']):
            m = aL * fd(T(2), .9 + i * .55); x = 250 + i * 220
            c.circ(x, 715, 46, None, m, outline=CY, ow=5)
            q = t * (2.4 - i * .7) + i
            c.line([(x, 715), (x + 30 * math.sin(q), 715 - 30 * math.cos(q))], CY, 5, m)
            c.line([(x, 715), (x, 692)], INK, 5, m)
            c.text(x, 800, lab, 34, INK, m, w='Medium')
    if T(3) > 0:
        m = fd(T(3)); x0, y0, x1, y1 = 1010, 260, 1760, 740
        axes(c, x0, y0, x1, y1, m)
        p = ease(T(3, .5) / 2.6); n = int(80 * p)
        pts = [(x0 + (x1 - x0) * u / 80, y1 - (y1 - y0 - 30) * decay(u / 80)) for u in range(n + 1)]
        c.line(pts, PK, 9, m)
        if pts: c.circ(pts[-1][0], pts[-1][1], 14, PK, m)
        c.text(1235, 330, 'Fast at first', 44, PK, m * fd(T(3), 1.9), 'lm', 'Bold')
        c.text(1320, 560, 'then it slows down', 44, CY, m * fd(T(3), 3.4), 'lm', 'Bold')
        c.text(1385, 838, 'Illustrative shape, after Ebbinghaus (1885)', 26, DIM, m * .9, w='Regular')
    if T(4) > 0:
        m = fd(T(4))
        c.rr(250, 250, 690, 800, 54, CARD, m, outline=DIM, ow=5)
        c.rr(400, 278, 540, 296, 9, (60, 70, 120), m, bg=CARD)
        c.text(470, 380, 'Heard once', 38, DIM, m, w='Medium', bg=CARD)
        for i, ch in enumerate('5550142'):
            x = 314 + i * 52; g = 1 - ease((T(4) - 1.0 - i * .32) / .9)
            c.text(x, 520, ch, 76, YE, m * (.1 + .9 * g), w='Mono', bg=CARD)
        c.text(470, 680, 'Fading fast', 44, PK, m * fd(T(4), 2.2), w='Bold', bg=CARD)

def s_illusion(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 430, 'Why does rereading', 100, INK, a0, w='Bold')
    c.text(960, 560, 'feel so good?', 100, YE, a0, w='Bold')
    aA = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    if T(1) > -.1 and aA > 0:
        hl = int(clamp(T(1, .4) / 2.4) * 4)
        page(c, 150, 220, 640, 800, aA, BG, 9, 1.0, hi=[1, 3, 4, 7][:hl], seed=2)
        c.text(395, 845, 'The page looks familiar', 32, DIM, aA * fd(T(1), .6), w='Medium')
        c.text(1000, 300, 'Familiar', 96, YE, aA * fd(T(1), 1.2), w='Bold')
        c.text(1000, 415, 'is not', 60, DIM, aA * fd(T(1), 2.2), w='Medium')
        c.text(1000, 530, 'known', 96, INK, aA * fd(T(1), 2.6), w='Bold')
        if T(2) > 0:
            m = aA * fd(T(2)); fall = T(2) - 3.0
            tilt = 0 if fall < 0 else 16 * math.sin(fall * 7) * clamp(fall / .5) + 10 * clamp(fall / 1.2)
            c.line([(1290, 762), (1800, 762)], DIM, 4, m)
            bike(c, 1545 + (40 * math.sin(t * .9) if fall < 0 else 0), 760, m, tilt, t * 4 if fall < 0 else 0)
            c.text(1545, 820, 'Looks easy' if fall < 0 else 'Until you try', 40, CY if fall < 0 else PK, m, w='Bold')
    if T(3) > -.1:
        m = fd(T(3))
        c.rr(330, 210, 1590, 800, 30, CARD, m, outline=(44, 52, 100), ow=4)
        c.text(960, 285, '2013 review of 10 study methods', 54, INK, m, w='Bold', bg=CARD)
        c.line([(420, 345), (1500, 345)], (60, 70, 120), 3, m, CARD)
        for i, lab in enumerate(['Rereading', 'Highlighting']):
            mm = m * fd(T(3), .9 + i * .4); y = 450 + i * 150
            c.rr(420, y - 56, 1500, y + 56, 20, (36, 44, 86), mm, bg=CARD)
            c.text(470, y, lab, 54, INK, mm, 'lm', 'Bold', bg=(36, 44, 86))
            pill(c, 1310, y, 'LOW UTILITY', PK, m * fd(T(3), 3.6 + i * 1.3), 34, (36, 44, 86))
        c.text(960, 742, 'Dunlosky and colleagues, 2013', 28, DIM, m * fd(T(3), 1.0), w='Regular', bg=CARD)

def s_test(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        pill(c, 960, 205, 'FIX 1', YE, a0, 40)
        c.text(960, 330, 'Test yourself', 120, INK, a0, w='Bold')
        closedbook(c, 640, 470, 300, 340, a0 * fd(T(0), 1.0))
        c.arrow(840, 640, 1020, 640, DIM, 6, a0 * fd(T(0), 1.6), 20)
        page(c, 1080, 460, 1400, 820, a0 * fd(T(0), 1.8), BG, 6, wrote=clamp((T(0) - 2.0) / 2.0), seed=1)
    aB = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    if T(1) > -.1 and aB > 0:
        c.text(960, 195, '2006 study: students read a short passage', 48, INK, aB, w='Bold')
        for i, (lab, sub, col) in enumerate([('Group A', 'Read it again', PU), ('Group B', 'Wrote down what they remembered', GR)]):
            m = aB * (fd(T(1), .6 + i * .3) * .35 + .65 * fd(T(2), .2 + i * 2.6)); x = 520 + i * 880
            c.rr(x - 390, 270, x + 390, 830, 30, CARD, m, outline=col, ow=5)
            c.text(x, 335, lab, 50, col, m, w='Bold', bg=CARD)
            if i == 0:
                page(c, x - 230, 400, x - 30, 690, m, CARD, 6, seed=3); page(c, x + 30, 400, x + 230, 690, m, CARD, 6, seed=3)
            else:
                closedbook(c, x - 150, 420, 200, 250, m, CARD)
                page(c, x + 10, 400, x + 230, 690, m, CARD, 6, wrote=clamp((T(2) - 3.2) / 2.2), seed=5)
            c.text(x, 765, sub, 38, INK, m, w='Medium', bg=CARD)
    if T(3) > -.1:
        legend = fd(T(3))
        c.circ(560, 200, 16, PU, legend); c.text(590, 200, 'Read again', 36, INK, legend, 'lm', 'Medium')
        c.circ(1010, 200, 16, GR, legend); c.text(1040, 200, 'Tested themselves', 36, INK, legend, 'lm', 'Medium')
        for i, (ttl, va, vb, k) in enumerate([('After 5 minutes', 81, 75, 3), ('After 1 week', 42, 56, 4)]):
            m = fd(T(k)); x = 520 + i * 880
            if m <= 0.01: continue
            win = i == 1
            c.rr(x - 390, 260, x + 390, 790, 30, CARD, m, outline=GR if win else (44, 52, 100), ow=5 if win else 4)
            c.text(x, 320, ttl, 46, YE if win else INK, m, w='Bold', bg=CARD)
            c.line([(x - 300, 720), (x + 300, 720)], DIM, 4, m, CARD)
            bar(c, x - 120, 718, 150, 380, va, (T(k) - .5) / 1.0, PU, m)
            bar(c, x + 120, 718, 150, 380, vb, (T(k) - .9) / 1.0, GR, m)
        c.text(960, 840, 'Share of the passage recalled. Roediger and Karpicke, 2006.', 28, DIM, legend * .95, w='Regular')

def s_why(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    c.text(960, 480, 'Why does this work?', 110, INK, a0, w='Bold')
    if T(1) < -.1: return
    m = fd(T(1)); x0, y0, x1, y1 = 130, 250, 1130, 770
    c.rr(x0, y0, x1, y1, 30, FIELD, m, outline=(30, 80, 70), ow=4)
    for i in range(46):
        gx = x0 + 40 + (i * 137) % (x1 - x0 - 80); gy = y0 + 46 + (i * 211) % (y1 - y0 - 80)
        c.line([(gx, gy), (gx + 6, gy - 20)], GRASS, 4, m * .9, FIELD)
    walks = max(0, T(1) - .8) / 1.7; nw = int(walks); u = walks % 1
    f = lambda q: (x0 + 150 + (x1 - x0 - 300) * q, (y0 + y1) / 2 + 90 * math.sin(q * 5.2))
    strength = clamp((nw + u) / 6)
    path = [f(i / 60) for i in range(61)]
    c.line(path, mix(YE, .25 + .75 * strength, FIELD), 5 + 22 * strength, m, FIELD)
    for q, lab, col in ((0, 'Question', CY), (1, 'Answer', GR)):
        px, py = f(q); c.circ(px, py, 44, col, m, bg=FIELD)
        c.text(px, py + 80, lab, 32, INK, m, w='Medium', bg=FIELD)
    wx, wy = f(ease(u)); c.circ(wx, wy, 17, INK, m * fd(T(1), .8), bg=FIELD)
    c.text(630, 200, 'Recalling = walking the path', 42, INK, m, w='Bold')
    c.text(630, 815, f'Recall {min(nw + 1, 9)}', 40, YE, m * fd(T(1), .8), w='Bold')
    c.text(630, 860, 'Illustration', 24, DIM, m * .8, w='Regular')
    if T(3) > 0:
        k = fd(T(3)); X = 1500
        c.rr(X - 290, 250, X + 290, 770, 22, PAPER, k)
        c.text(X, 310, 'Self-test', 44, BG, k, w='Bold', bg=PAPER)
        for i in range(4):
            y = 400 + i * 85; ok = i != 2; mm = k * fd(T(3), .5 + i * .35)
            c.line([(X - 230, y), (X + 60, y)], RULE, 8, k, PAPER)
            if ok: c.check(X + 180, y, 34, (30, 160, 100), mm, clamp((T(3) - .5 - i * .35) / .35))
            else: c.cross(X + 180, y, 44, RED, mm)
        pill(c, X, 825, 'Gap found', YE, k * fd(T(3), 1.9), 36)

DAYS = ['Mon', 'Tue', 'Wed', 'Thu']
def s_space(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        pill(c, 960, 320, 'FIX 2', YE, a0, 40)
        c.text(960, 470, 'Space it out', 130, INK, a0, w='Bold')
    aA = fd(T(1)) * (1 - fd(T(2), -.4, .4))
    if T(1) > -.1 and aA > 0:
        for j, d in enumerate(DAYS): c.text(760 + j * 250, 215, d, 40, DIM, aA, w='Medium')
        for i, (lab, col) in enumerate([('Cramming', PK), ('Spaced', GR)]):
            y = 400 + i * 300; m = aA * fd(T(1), i * 1.6)
            c.rr(150, y - 120, 1790, y + 120, 26, CARD, m)
            c.text(210, y - 24, lab, 56, col, m, 'lm', 'Bold', bg=CARD)
            c.text(210, y + 44, 'one long night' if i == 0 else 'four short sessions', 30, DIM, m, 'lm', 'Medium', bg=CARD)
            for j in range(4):
                x = 760 + j * 250
                c.rr(x - 100, y - 96, x + 100, y + 96, 14, (36, 44, 86), m, bg=CARD)
                if i == 1: c.rr(x - 44, y - 44, x + 44, y + 44, 10, col, m * fd(T(1), 1.9 + j * .3), bg=(36, 44, 86))
            if i == 0:
                for q in range(4):
                    xx = 1510 - 66 + (q % 2) * 90; yy = y - 66 + (q // 2) * 90
                    c.rr(xx - 20, yy - 20, xx + 62, yy + 62, 10, col, m * fd(T(1), .4 + q * .2), bg=(36, 44, 86))
        c.text(960, 850, 'Same total study time', 34, INK, aA * fd(T(1), 3.2), w='Medium')
    if T(2) > -.1:
        m = fd(T(2)); x0, y0, x1, y1 = 170, 260, 1230, 740; gw, gh = x1 - x0, y1 - y0 - 30
        axes(c, x0, y0, x1, y1, m)
        p = clamp(T(2, .4) / 6.5); segs = [(0.0, 9.0), (.22, 5.0), (.47, 2.8), (.74, 1.5)]
        ghost = [(x0 + gw * u / 80, y1 - gh * decay(u / 80, 9.0, .12)) for u in range(int(80 * p) + 1)]
        for i in range(0, len(ghost) - 1, 4): c.line(ghost[i:i + 3], DIM, 4, m * .7)
        for i, (s, k) in enumerate(segs):
            e = segs[i + 1][0] if i + 1 < len(segs) else 1.0
            if p <= s: break
            n = max(1, int(80 * (min(p, e) - s)))
            pts = [(x0 + gw * (s + (min(p, e) - s) * j / n), y1 - gh * decay((min(p, e) - s) * j / n, k, .12)) for j in range(n + 1)]
            if i > 0:
                prev = y1 - gh * decay(s - segs[i - 1][0], segs[i - 1][1], .12)
                c.line([(x0 + gw * s, prev), (x0 + gw * s, y1 - gh)], GR, 6, m)
                c.text(x0 + gw * s, y1 + 40, 'Review', 30, GR, m, w='Bold')
            c.line(pts, CY, 8, m)
        c.text(x0 + gw * .80, y1 - gh * .12 - 34, 'No review', 30, DIM, m * fd(T(2), 5.6), w='Medium')
        c.text(700, 195, 'Each review: forgetting slows', 42, INK, m * fd(T(3), .2), w='Bold')
        c.text(700, 838, 'Illustrative', 26, DIM, m * .9, w='Regular')
    if T(4) > 0:
        m = fd(T(4)); X = 1560; g = ease(T(4) / 3.2)
        poly(c, [(X - 105, 640), (X + 105, 640), (X + 78, 790), (X - 78, 790)], POT, m)
        c.rr(X - 122, 612, X + 122, 652, 10, POT, m)
        top = 612 - 250 * g
        c.line([(X, 612), (X + 10 * math.sin(t * 1.5), top)], LEAF, 11, m)
        for k, (side, fy) in enumerate([(-1, .35), (1, .6), (-1, .85)]):
            if g > fy * .8:
                ly = 612 - 250 * g * fy; s = 62 * clamp((g - fy * .8) / .3)
                lx = X + side * s * .62
                c.d.ellipse(((lx - s * .6) * c.k, (ly - s * .3) * c.k, (lx + s * .6) * c.k, (ly + s * .3) * c.k), fill=mix(LEAF, m))
        for k in range(3):
            dy = ((t * 150 + k * 70) % 210)
            c.circ(X - 70 + k * 70, 270 + dy, 9, CY, m * (1 - dy / 210) * .9)
        c.text(X, 838, 'A little, often', 40, GR, m, w='Bold')

def s_plan(c, T, t):
    c.text(960, 195, 'A simple plan', 76, INK, fd(T(0)), w='Bold')
    cards = [('1', 'Close the book', 'Write what you remember', CY), ('2', 'Check', 'What did you miss?', YE), ('3', 'Do it again', 'Example schedule', GR)]
    for i, (nn, a1, a2, col) in enumerate(cards):
        m = fd(T(i + 1)); x = 380 + i * 580; up = 22 * (1 - m)
        if m <= 0.01: continue
        c.rr(x - 265, 270 + up, x + 265, 640 + up, 28, CARD, m, outline=col, ow=5)
        c.circ(x - 200, 330 + up, 38, col, m, bg=CARD); c.text(x - 200, 330 + up, nn, 46, BG, m, w='Bold', bg=col)
        c.text(x + 30, 330 + up, a1, 44, INK, m, w='Bold', bg=CARD)
        if i == 0:
            closedbook(c, x - 95, 390 + up, 130, 160, m, CARD)
            page(c, x + 10, 385 + up, 160 + x, 555 + up, m, CARD, 5, wrote=clamp((T(1) - .8) / 1.8), seed=1)
        elif i == 1:
            page(c, x - 110, 385 + up, x + 110, 555 + up, m, CARD, 4, seed=2)
            c.check(x + 160, 430 + up, 30, GR, m, clamp((T(2) - .6) / .3)); c.cross(x + 160, 510 + up, 40, PK, m * fd(T(2), 1.0))
        else:
            c.line([(x - 190, 440 + up), (x + 190, 440 + up)], DIM, 5, m, CARD)
            for j, lab in enumerate(['Tomorrow', 'In a few days', 'Next week']):
                mm = m * fd(T(3), .7 + j * .75); xx = x - 190 + j * 190
                c.circ(xx, 440 + up, 20, col, mm, bg=CARD)
                c.text(xx, 500 + up + (j % 2) * 0, lab, 24, INK, mm, w='Medium', bg=CARD)
        c.text(x, 596 + up, a2, 30, DIM, m, w='Medium', bg=CARD)
    if T(4) > 0:
        m = fd(T(4)); ph = (T(4) % 2.4) / 2.4; front = ph < .5
        sx = abs(math.cos(ph * 2 * math.pi)) if (.2 < ph < .3 or .7 < ph < .8) else 1.0
        if .2 < ph < .3: front = ph < .25
        if .7 < ph < .8: front = ph >= .75
        col = CY if front else GR
        c.rr(660 - 150 * sx + 0, 700, 660 + 150 * sx, 850, 20, col, m)
        if sx > .6: c.text(660, 775, 'Question' if front else 'Answer', 44, BG, m, w='Bold', bg=col)
        c.text(860, 775, 'Flashcards work the same way', 44, INK, m, 'lm', 'Bold')

def s_warn(c, T, t):
    aA = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if aA > 0:
        c.text(960, 205, 'One warning', 80, YE, aA, w='Bold')
        u = (t * .35) % 1
        c.line([(250, 420), (880, 420)], DIM, 6, aA); c.circ(250 + 630 * u, 392, 26, DIM, aA)
        c.text(565, 500, 'Rereading feels easy', 42, DIM, aA, w='Medium')
        poly(c, [(1040, 760), (1670, 760), (1670, 470)], (36, 44, 86), aA)
        c.line([(1040, 760), (1670, 470)], YE, 6, aA)
        v = (t * .18) % 1; bx, by = 1040 + 630 * v, 760 - 290 * v
        c.circ(bx - 12, by - 28, 26, YE, aA)
        c.text(1330, 830, 'Self-testing feels harder', 42, YE, aA, w='Bold')
    aB = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    if T(1) > -.1 and aB > 0:
        for i, (lab, col) in enumerate([('Rereaders', PU), ('Self-testers', GR)]):
            x = 520 + i * 880
            c.rr(x - 390, 200, x + 390, 800, 30, CARD, aB, outline=col, ow=5)
            c.text(x, 270, lab, 54, col, aB, w='Bold', bg=CARD)
            m1 = aB * fd(T(1), .8)
            c.text(x, 365, 'How sure they felt', 30, DIM, m1, w='Medium', bg=CARD)
            c.text(x, 440, 'More confident' if i == 0 else 'Less confident', 54, YE if i == 0 else INK, m1, w='Bold', bg=CARD)
            if T(2) > 0:
                m2 = aB * fd(T(2), .3)
                c.line([(x - 300, 520), (x + 300, 520)], (60, 70, 120), 3, m2, CARD)
                c.text(x, 585, 'One week later', 30, DIM, m2, w='Medium', bg=CARD)
                c.text(x, 665, 'Remembered less' if i == 0 else 'Remembered more', 54, PK if i == 0 else GR, m2, w='Bold', bg=CARD)
                if i == 0: c.arrow(x, 715, x, 772, PK, 8, m2, 18)
                else: c.arrow(x, 772, x, 715, GR, 8, m2, 18)
        c.text(960, 845, 'Roediger and Karpicke, 2006', 28, DIM, aB, w='Regular')
    if T(3) > -.1:
        m = fd(T(3))
        c.text(960, 400, "Don't trust the easy feeling.", 92, INK, m, w='Bold')
        c.text(960, 570, 'Trust the test.', 120, YE, m * fd(T(3), 1.9), w='Bold')

REC = [('1', 'Forgetting is fast at first', PK), ('2', 'Test yourself', GR), ('3', 'Spread it over days', CY)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 250, 290 + up, x + 250, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 185, 355 + up, 40, col, m, bg=CARD); c.text(x - 185, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 530 + up
        if i == 0:
            p = (t * .35) % 1.3
            pts = [(x - 150 + 300 * u / 40, y + 90 - 190 * decay(u / 40, 6, .12)) for u in range(int(40 * clamp(p)) + 1)]
            c.line([(x - 150, y - 110), (x - 150, y + 95), (x + 160, y + 95)], DIM, 4, m, CARD)
            c.line(pts, col, 8, m, CARD)
        elif i == 1:
            page(c, x - 105, y - 115, x + 65, y + 100, m, CARD, 5, seed=1)
            c.check(x + 125, y, 44, col, m, clamp(((t * .8) % 2) / .5))
        else:
            for j in range(4):
                c.rr(x - 180 + j * 95, y - 45, x - 105 + j * 95, y + 30, 10, (36, 44, 86), m, bg=CARD)
                c.rr(x - 163 + j * 95, y - 28, x - 122 + j * 95, y + 13, 6, col, m * (.35 + .65 * (int(t * 1.5) % 4 >= j)), bg=(36, 44, 86))
        c.text(x, 715 + up, lab, 34, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        o2 = 1 - fd(T(5), -.3, .5)
        c.text(960, 420, 'A little effort now.', 110, INK, fd(T(4)) * o2, w='Bold')
        c.text(960, 590, 'A lot more memory later.', 84, CY, fd(T(4), 1.4) * o2, w='Bold')
    if T(5) > 0:
        m = fd(T(5), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, RED, m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=RED)
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(5), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(5), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["You read a chapter three times, and it feels like you know it.", "A week later, much of it is gone.",
            "You are not bad at learning.", "Rereading just feels better than it works.",
            "Here is why you forget, and how to fix it."], s_hook),
 ('1  ·  THE CURVE', ["Scientists have measured forgetting since 1885.",
            "A German psychologist, Hermann Ebbinghouse, memorised lists of made-up syllables.",
            "Then he tested himself after minutes, hours, and days.",
            "He found a curve. Forgetting is fast at first, then it slows down.",
            "Think of a phone number you hear once. It fades quickly."], s_curve),
 ('2  ·  THE ILLUSION', ["So why does rereading feel so good?", "Because the page looks familiar. And familiar feels like knowing.",
            "It is like watching someone ride a bike. It looks easy, until you try.",
            "A major 2013 review of ten study methods rated rereading and highlighting as low value."], s_illusion),
 ('3  ·  TEST YOURSELF', ["Fix number one. Close the book, and test yourself.", "In a 2006 study, students read a short passage.",
            "One group read it again. The other group wrote down everything they could remember.",
            "Five minutes later, the rereaders scored higher.",
            "But one week later, the group that tested themselves remembered more."], s_test),
 ('4  ·  WHY IT WORKS', ["Why does this work?", "Pulling a memory out makes it easier to find next time.",
            "It is like a path through grass. Each walk makes the path clearer.",
            "And a test shows you what you do not know yet."], s_why),
 ('5  ·  SPACE IT OUT', ["Fix number two. Spread your study out.",
            "Four short sessions on four days usually beat one long night of cramming.",
            "Each time you come back, you have forgotten a little.",
            "Recalling it again takes effort, and that effort helps the memory last.",
            "It is like watering a plant. A little, often, works better than a flood once."], s_space),
 ('6  ·  A SIMPLE PLAN', ["So here is a simple plan.", "After you read, close the book and write what you remember.",
            "Check what you missed.", "Then do it again tomorrow, in a few days, and next week.",
            "Flashcards work the same way."], s_plan),
 ('7  ·  ONE WARNING', ["One warning. This will feel harder than rereading.",
            "In that 2006 study, the rereaders felt more confident about what they had learned.",
            "But they remembered less a week later.", "So do not trust the easy feeling. Trust the test."], s_warn),
 ('RECAP', ["So remember three things.", "One. Forgetting is fast at first. That is normal.", "Two. Test yourself instead of rereading.",
            "Three. Spread your study over several days.", "A little effort now. A lot more memory later.",
            "If this helped, subscribe for more."], s_recap),
]
