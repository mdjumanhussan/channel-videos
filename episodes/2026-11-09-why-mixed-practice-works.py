"""Episode: Mixed Practice Feels Worse. It Works Better. (interleaved vs blocked practice: Rohrer and Taylor 2007, Kornell and Bjork 2008 via Kang 2023, Brunmair and Richter 2019 meta-analysis)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Mixed Practice Feels Worse. It Works Better.'   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Why shuffled practice wins'                      # headline on the vertical Short
HITS = [(0, 0, 0.0), (4, 0, 0.0), (7, 1, 0.0)]                 # the hook claim, the test result, the painting result
THUMB = ['MIX', 'IT UP.']                                      # 7 letters (lesson of 2026-11-09, 1of10: under 10 characters)
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.4, (0, 2): 0.4, (1, 2): 0.3, (2, 2): 0.3, (3, 2): 0.5, (4, 1): 0.3, (4, 2): 0.3, (5, 2): 0.4, (6, 2): 2.6, (7, 0): 0.3, (7, 3): 0.3, (8, 2): 0.3, (9, 3): 0.2}
SHORT_PAUSES = {(0, 1): 0.2, (2, 1): 0.2}
CAPTION_FIXES = {'Eighty nine percent': '89%', 'Fifty nine percent': '59%', 'two thousand seven': '2007', 'eighty nine percent': '89%', 'sixty percent': '60%', 'sixty three percent': '63%',
                 'twenty percent': '20%', 'fifty nine percent': '59%', 'thirty six percent': '36%', 'fifty nine studies': '59 studies'}

# Colour code kept in every scene (lesson of 2026-11-01):
# blocked practice blue, mixed practice orange, the "which kind is this?" choice yellow, right/learned green, mistakes pink.
BLK = CY; MIXC = (255, 150, 70); CHOICE = YE; OK = GR; BAD = PK
DARK = (20, 22, 38); PAPER = (236, 232, 220); PINK2 = (60, 30, 70); QUIZ = (70, 44, 26)
SHAPE_COLS = [(150, 120, 255), (150, 120, 255), (150, 120, 255), (150, 120, 255)]
SHAPE_NAMES = ['wedge', 'spherical cone', 'spheroid', 'half cone']
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0
BLOCKED = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
MIXED = [2, 0, 3, 1, 0, 2, 1, 3, 3, 1, 0, 2, 1, 3, 2, 0]

def poly(c, pts, fill, a=1.0, bg=BG, outline=None):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None)

def ell(c, x, y, rx, ry, fill=None, a=1.0, outline=None, ow=3, bg=BG):
    if a <= .01: return
    c.d.ellipse(((x - rx) * c.k, (y - ry) * c.k, (x + rx) * c.k, (y + ry) * c.k),
                fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None, width=max(1, int(ow * c.k)))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def shape(c, kind, x, y, s, a=1.0, col=PU, bg=BG):
    """The four unusual solids from the 2007 study, drawn as simple flat icons."""
    if a <= .01: return
    if kind == 0:     # wedge
        poly(c, [(x - 40 * s, y + 28 * s), (x + 22 * s, y + 28 * s), (x + 22 * s, y - 30 * s)], col, a, bg)
        poly(c, [(x + 22 * s, y + 28 * s), (x + 40 * s, y + 16 * s), (x + 40 * s, y - 42 * s), (x + 22 * s, y - 30 * s)], mix(col, .65, bg), a, bg)
    elif kind == 1:   # spherical cone (ice-cream shape)
        poly(c, [(x - 30 * s, y - 8 * s), (x + 30 * s, y - 8 * s), (x, y + 40 * s)], col, a, bg)
        c.d.pieslice(((x - 30 * s) * c.k, (y - 38 * s) * c.k, (x + 30 * s) * c.k, (y + 22 * s) * c.k), 180, 360, fill=mix(mix(col, .75, bg), a, bg))
    elif kind == 2:   # spheroid
        ell(c, x, y, 42 * s, 26 * s, col, a, bg=bg)
        ell(c, x - 12 * s, y - 8 * s, 12 * s, 6 * s, mix(INK, .5, col), a, bg=bg)
    else:             # half cone
        poly(c, [(x - 34 * s, y + 30 * s), (x + 2 * s, y + 30 * s), (x + 2 * s, y - 38 * s)], col, a, bg)
        c.d.pieslice(((x - 34 * s) * c.k, (y + 20 * s) * c.k, (x + 38 * s) * c.k, (y + 40 * s) * c.k), 0, 180, fill=mix(mix(col, .7, bg), a, bg))

def strip(c, kinds, x, y, gap, s, a, col, n=None, p=1.0, bg=BG):
    """A row of practice problems (one shape icon each) on a coloured rail."""
    n = n or len(kinds)
    c.rr(x - 50 * s, y - 56 * s, x + gap * (n - 1) + 50 * s, y + 56 * s, 22 * s, CARD, a, outline=col, ow=4, bg=bg)
    for k in range(n):
        m = a * clamp(p * n - k)
        shape(c, kinds[k], x + gap * k, y, s, m, bg=CARD)

def bar(c, x, base, w, hmax, val, col, a, p=1.0, label=None, top=None):
    if a <= .01: return
    h = hmax * val / 100 * clamp(p)
    c.rr(x - w / 2, base - h, x + w / 2, base, 14, col, a)
    if p > .05: c.text(x, base - h - 44, f'{int(round(val * clamp(p)))}%', 56, col, a, w='Bold')
    if label: c.text(x, base + 42, label, 40, INK, a, w='Bold')

def sheet(c, x, y, w, h, kinds, a, title=None, ticks=0.0, title_col=BLK):
    """A sheet of homework: a header and a column of problems with shape icons."""
    if a <= .01: return
    c.rr(x, y, x + w, y + h, 18, PAPER, a)
    if title: c.text(x + w / 2, y + 44, title, 34, title_col if title_col != BLK else (30, 90, 140), a, w='Bold', bg=PAPER)
    rows = len(kinds); rh = (h - (90 if title else 30)) / rows
    for k, kd in enumerate(kinds):
        yy = y + (90 if title else 30) + rh * (k + .5)
        c.text(x + 36, yy, f'{k + 1}.', 26, (90, 90, 110), a, 'lm', 'Bold', bg=PAPER)
        shape(c, kd, x + 100, yy, .42, a, (110, 90, 200), bg=PAPER)
        c.line([(x + 140, yy + 6), (x + w - 70, yy + 6)], (190, 186, 176), 4, a, bg=PAPER)
        if ticks * rows > k:
            c.check(x + w - 40, yy, 20, (40, 160, 90), a * clamp(ticks * rows - k), clamp(ticks * rows - k))

def painting(c, x, y, w, h, style, a, seed=0, bg=BG):
    """Small original canvases in two invented 'styles': 0 = soft dabs, 1 = long horizontal strokes."""
    if a <= .01: return
    c.rr(x - w / 2 - 10, y - h / 2 - 10, x + w / 2 + 10, y + h / 2 + 10, 8, (120, 92, 60), a, bg=bg)
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 4, (40, 60, 90) if style == 0 else (90, 70, 60), a, bg=bg)
    rng = np.random.default_rng(seed)
    if style == 0:
        for _ in range(46):
            px, py = rng.uniform(-.45, .45) * w, rng.uniform(-.42, .42) * h
            col = [(120, 170, 220), (200, 220, 160), (240, 210, 140), (150, 200, 190)][rng.integers(4)]
            c.circ(x + px, y + py, rng.uniform(3, 7) * w / 160, col, a)
    else:
        for _ in range(14):
            py = rng.uniform(-.42, .42) * h; px = rng.uniform(-.45, .1) * w
            col = [(220, 140, 90), (240, 190, 120), (180, 110, 90), (250, 220, 170)][rng.integers(4)]
            c.line([(x + px, y + py), (x + px + rng.uniform(.25, .45) * w, y + py + rng.uniform(-4, 4))], col, rng.uniform(4, 9) * w / 160, a)

def person(c, x, y, s, a, col=DIM):
    c.circ(x, y - 50 * s, 22 * s, col, a)
    c.d.pieslice(((x - 40 * s) * c.k, (y - 22 * s) * c.k, (x + 40 * s) * c.k, (y + 58 * s) * c.k), 180, 360, fill=mix(col, a))

# ---- scenes ----
def s_hook(c, T, t):
    """Surprising true statement with its proof on screen from frame one (lessons of 2026-10-16 and 2026-10-15)."""
    hl = lambda i: hl_(T, i)
    q = hl(2)
    m = 1 - q
    c.text(960, 172, 'Did worse in practice. Scored 3x higher.', 76, MIXC, sw_out(T, 1) * m, w='Bold')
    c.text(960, 172, 'Same problems. Only the order changed.', 76, INK, sw_in(T, 1) * m, w='Bold')
    strip(c, BLOCKED, 200, 440, 76, .8, m, BLK, n=12)
    c.text(150, 340, 'In blocks', 40, BLK, m, 'lm', 'Bold')
    strip(c, MIXED, 200, 680, 76, .8, m, MIXC, n=12)
    c.text(150, 580, 'Shuffled', 40, MIXC, m, 'lm', 'Bold')
    grow = fd(t, .2, 1.4)
    c.text(1600, 300, 'TEST, ONE WEEK LATER', 36, DIM, m, w='Bold')
    bar(c, 1490, 800, 150, 600, 20, BLK, m, grow)
    bar(c, 1710, 800, 150, 600, 63, MIXC, m, grow)
    c.line([(1380, 800), (1820, 800)], DIM, 4, m)
    c.text(960, 430, 'So what were they', 112, INK, q, w='Bold')
    c.text(960, 570, 'doing differently?', 112, MIXC, q, w='Bold')

def s_homework(c, T, t):
    hl = lambda i: hl_(T, i)
    sheet(c, 160, 250, 520, 620, [0] * 10, 1, 'Chapter 4: Wedges', ticks=hl(1) * fd(T(1), .3, 3.0))
    c.text(960, 172, 'End-of-chapter homework', 84, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Learn the method once, repeat it', 80, BLK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Blocked practice', 92, BLK, sw_in(T, 2), w='Bold')
    m = hl(2)
    c.rr(820, 300, 1800, 640, 28, CARD, m, outline=BLK, ow=4)
    for k, (lab, kd) in enumerate((('AAAA', 0), ('BBBB', 1), ('CCCC', 2))):
        c.text(1000 + k * 300, 400, lab, 70, BLK, m, w='Bold', bg=CARD)
    c.text(1310, 520, 'one kind at a time', 50, INK, m, w='Bold', bg=CARD)
    # speed gauge: it feels smooth and fast
    g = hl(2) * fd(T(2), .6, 1.2)
    c.circ(1310, 790, 70, CARD, g, outline=BLK, ow=4)
    ang = math.radians(-120 + 200 * g)
    c.line([(1310, 790), (1310 + 56 * math.sin(ang), 790 - 56 * math.cos(ang))], BLK, 8, g, bg=CARD)
    c.text(1430, 790, 'feels fast', 46, BLK, g, 'lm', 'Bold')

def s_experiment(c, T, t):
    hl = lambda i: hl_(T, i)
    m0 = 1 - hl(1)
    c.text(960, 172, 'A test with 18 university students', 80, INK, sw_out(T, 1), w='Bold')
    c.rr(560, 330, 1360, 650, 28, CARD, m0, outline=(60, 70, 120), ow=3)
    c.text(960, 410, '2007, University of South Florida', 50, INK, m0, w='Bold', bg=CARD)
    c.text(960, 500, 'Doug Rohrer', 50, DIM, m0, w='Medium', bg=CARD)
    c.text(960, 570, 'Kelli Taylor', 50, DIM, m0, w='Medium', bg=CARD)
    m1 = hl(1) * (1 - hl(2))
    c.text(960, 172, 'Find the volume of four odd shapes', 80, PU, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    for k in range(4):
        mm = m1 * fd(T(1), .3 + k * .35)
        shape(c, k, 360 + k * 400, 500, 2.2, mm)
        c.text(360 + k * 400, 700, SHAPE_NAMES[k], 46, INK, mm, w='Bold')
    m2 = hl(2)
    c.text(960, 172, 'Same 16 problems, two orders', 84, INK, sw_in(T, 2), w='Bold')
    c.text(150, 330, 'Block group: four of the same in a row', 44, BLK, m2, 'lm', 'Bold')
    strip(c, BLOCKED, 230, 440, 97, .8, m2, BLK, p=fd(T(2), .2, 1.6))
    c.text(150, 590, 'Mixed group: the same problems, shuffled', 44, MIXC, m2 * fd(T(2), 1.8), 'lm', 'Bold')
    strip(c, MIXED, 230, 700, 97, .8, m2 * fd(T(2), 1.8), MIXC, p=fd(T(2), 2.0, 1.6))

def s_practice(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'During practice', 92, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Blocking looks like the winner', 84, BLK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'But a week later: the test', 88, CHOICE, sw_in(T, 2), w='Bold')
    p = fd(T(0), .5, 1.5)
    bar(c, 760, 760, 220, 420, 89, BLK, 1, p, 'In blocks')
    bar(c, 1160, 760, 220, 420, 60, MIXC, 1, p, 'Shuffled')
    c.line([(560, 760), (1360, 760)], DIM, 4)
    c.text(400, 300, 'PRACTICE SCORES', 36, DIM, 1, w='Bold')
    cr = hl(1) * (1 - hl(2) * .6)
    c.text(400, 360, 'winner?', 56, BLK, cr, w='Bold')
    m = hl(2)
    c.rr(1480, 360, 1800, 640, 28, CARD, m, outline=CHOICE, ow=4)
    c.rr(1480, 360, 1800, 430, 28, CHOICE, m)
    c.text(1640, 397, 'ONE WEEK', 36, DARK, m, w='Bold', bg=CHOICE)
    c.text(1640, 530, '+7', 110, CHOICE, m * fd(T(2), .4), w='Bold', bg=CARD)
    c.text(1880, 860, 'Source: Rohrer and Taylor 2007 (average of two practice sessions)', 30, DIM, 1, anchor='rm', w='Regular')

def s_test(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'The test, one week later', 88, CHOICE, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'About three times higher', 92, MIXC, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Their mistake: the wrong formula', 84, BAD, sw_in(T, 2), w='Bold')
    # practice bars shrink to the left, test bars grow
    c.text(400, 300, 'PRACTICE', 36, DIM, .7, w='Bold')
    bar(c, 320, 760, 110, 360, 89, BLK, .45)
    bar(c, 480, 760, 110, 360, 60, MIXC, .45)
    c.line([(230, 760), (570, 760)], DIM, 3, .6)
    c.text(1000, 300, 'TEST', 40, CHOICE, 1, w='Bold')
    p = fd(T(0), .4, 1.6)
    bar(c, 880, 760, 200, 440, 20, BLK, 1, p, 'In blocks')
    bar(c, 1120, 760, 200, 440, 63, MIXC, 1, p, 'Shuffled')
    c.line([(740, 760), (1260, 760)], DIM, 4)
    m1 = hl(1)
    c.circ(1260, 330, 66, MIXC, m1 * fd(T(1), .3, .3)); c.text(1260, 330, '3x', 64, DARK, m1 * fd(T(1), .3, .3), w='Bold', bg=MIXC)
    m = hl(2)
    c.rr(1360, 420, 1870, 790, 28, CARD, m, outline=BAD, ow=4)
    c.text(1615, 475, 'Block group errors:', 40, INK, m, w='Bold', bg=CARD)
    shape(c, 2, 1500, 580, 1.0, m, bg=CARD); c.text(1590, 580, '=', 60, INK, m, w='Bold', bg=CARD)
    c.text(1720, 580, 'cone?', 48, BAD, m, w='Bold', bg=CARD); c.cross(1820, 580, 44, BAD, m)
    c.text(1615, 680, 'picked the wrong formula', 36, BAD, m, w='Bold', bg=CARD)
    c.text(1615, 740, '(example)', 30, DIM, m, w='Regular', bg=CARD)
    c.text(1880, 860, 'Source: Rohrer and Taylor 2007', 30, DIM, 1, anchor='rm', w='Regular')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'In a block, the page picks the method', 80, BLK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Mixed: which kind is this?', 88, CHOICE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A test asks that too', 92, CHOICE, sw_in(T, 2), w='Bold')
    sheet(c, 140, 260, 460, 540, [1] * 7, 1, 'Section 2: Cones')
    c.rr(170, 280, 570, 330, 14, None, .9 * (1 - hl(1) * .5), outline=BLK, ow=4)
    c.text(370, 845, 'the header gives it away', 36, BLK, 1 - hl(1) * .5, w='Bold')
    m = hl(1)
    c.rr(700, 300, 1820, 820, 30, CARD, m, outline=CHOICE, ow=4)
    k_now = int((t * .9) % 4) if m > .01 else 0
    shape(c, MIXED[int(t * .9) % 16], 940, 500, 2.0, m, bg=CARD)
    q = .5 + .5 * math.sin(t * 4)
    c.text(940, 690, '?', 110, CHOICE, m * (.6 + .4 * q), w='Bold', bg=CARD)
    for k in range(4):
        yy = 380 + k * 115
        c.rr(1130, yy - 44, 1780, yy + 44, 20, DARK, m, outline=CHOICE if k == k_now else (60, 70, 120), ow=3, bg=CARD)
        shape(c, k, 1190, yy, .55, m, bg=DARK)
        c.text(1255, yy, SHAPE_NAMES[k] + ' formula', 38, INK, m, 'lm', 'Bold', bg=DARK)

def s_quiz(c, T, t):
    """Pattern interrupt: the frame fills with colour (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(560, 110, 1360, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK QUESTION', 78, CHOICE, 1, w='Bold', bg=DARK)
    c.text(960, 300, 'Learning painters by style: which way felt better?', 54, INK, hl(1), w='Bold', bg=QUIZ)
    for x, lab, l1, l2, col, sty in ((490, 'A', 'One artist', 'at a time', BLK, (0, 0, 0)), (1430, 'B', 'Artists', 'mixed up', MIXC, (0, 1, 0))):
        m = hl(2) if lab == 'A' else fd(T(2), 1.8)
        c.rr(x - 380, 380, x + 380, 820, 34, DARK, m, bg=QUIZ)
        c.text(x - 260, 470, lab, 100, col, m, w='Bold', bg=DARK)
        for j, s in enumerate(sty): painting(c, x - 120 + j * 150, 470, 110, 80, s, m, seed=j + (5 if lab == 'B' else 0), bg=DARK)
        c.text(x, 650, l1, 56, INK, m, w='Bold', bg=DARK)
        c.text(x, 725, l2, 56, INK, m, w='Bold', bg=DARK)
    c.text(960, 860, '6 paintings each by 12 artists', 32, (220, 200, 170), hl(1), w='Medium', bg=QUIZ)
    end = T(2) - 5.0
    if end > 0:
        q = clamp(end / 2.4); n = 3 - int(min(q * 3, 2.9))
        c.circ(960, 600, 84, DARK, 1, bg=QUIZ); ring(c, 960, 600, 70, 1 - q, CHOICE, 1, 10)
        c.text(960, 600, str(n), 76, INK, 1, w='Bold', bg=DARK)

def s_answer(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Most people picked A', 88, BLK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'But B did better on new paintings', 80, MIXC, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Side by side, differences pop out', 82, OK, sw_in(T, 2), w='Bold')
    m0 = 1 - hl(1)
    for k in range(9):
        person(c, 560 + k * 100, 520, 1.2, m0 * fd(T(0), .2 + k * .08), BLK if k < 7 else MIXC)
    c.text(960, 700, 'Most judged one-at-a-time as better', 50, INK, m0, w='Bold')
    c.text(960, 770, '(people shown are illustrative)', 32, DIM, m0, w='Regular')
    m1 = hl(1) * (1 - hl(2))
    p = fd(T(1), .3, 1.4)
    bar(c, 780, 760, 220, 440, 36, BLK, m1, p, 'One at a time')
    bar(c, 1140, 760, 220, 440, 59, MIXC, m1, p, 'Mixed')
    c.line([(580, 760), (1340, 760)], DIM, 4, m1)
    c.text(960, 300, 'NAMING THE ARTIST OF A NEW PAINTING', 34, DIM, m1, w='Bold')
    m2 = hl(2)
    painting(c, 640, 520, 440, 300, 0, m2, seed=11)
    painting(c, 1280, 520, 440, 300, 1, m2, seed=12)
    c.text(640, 740, 'soft dabs', 52, OK, m2 * fd(T(2), .8), w='Bold')
    c.text(1280, 740, 'long strokes', 52, OK, m2 * fd(T(2), 1.2), w='Bold')
    c.text(960, 520, 'vs', 70, INK, m2, w='Bold')
    c.text(1880, 860, 'Source: Kornell and Bjork 2008, via Kang 2023. Paintings drawn for this video', 30, DIM, 1, anchor='rm', w='Regular')

def s_limits(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A review of 59 studies', 88, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'It depends on what you learn', 84, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Mix things you could confuse', 88, OK, sw_in(T, 2), w='Bold')
    m = 1 - hl(2)
    rows = (('Paintings', .67, OK, 'biggest gain', 0), ('Maths', .34, OK, 'smaller gain', 1), ('Word lists', -.39, BAD, 'blocking did better', 1))
    cx = 900
    c.line([(cx, 300), (cx, 760)], DIM, 4, m)
    for k, (lab, g, col, note, ln) in enumerate(rows):
        mm = m * (fd(T(0), .5 + k * .4) if ln == 0 else hl(1) * fd(T(1), (k - 1) * 1.2))
        yy = 360 + k * 170
        c.text(cx - 330, yy, lab, 52, INK, mm, 'rm', 'Bold')
        L = 700 * g * clamp(mm)
        c.rr(min(cx, cx + L), yy - 40, max(cx, cx + L), yy + 40, 14, col, mm)
        c.text(cx + max(L, 0) + 30 if g > 0 else cx + 30, yy, note, 44, col, mm, 'lm', 'Bold')
    c.text(cx, 800, 'bar length: effect size in the review', 32, DIM, m, w='Regular')
    m2 = hl(2)
    c.rr(260, 320, 860, 760, 30, CARD, m2, outline=OK, ow=4)
    c.text(560, 390, 'Helps', 60, OK, m2, w='Bold', bg=CARD)
    c.text(560, 490, 'look-alike problem types', 40, INK, m2, w='Bold', bg=CARD)
    for k in range(4): shape(c, MIXED[k], 410 + k * 100, 620, .9, m2, bg=CARD)
    c.rr(1060, 320, 1660, 760, 30, CARD, m2, outline=BAD, ow=4)
    c.text(1360, 390, "Won't help much", 56, BAD, m2, w='Bold', bg=CARD)
    c.text(1360, 490, 'very different subjects', 40, INK, m2, w='Bold', bg=CARD)
    c.text(1360, 620, 'a language + anatomy', 44, DIM, m2, w='Bold', bg=CARD)
    c.text(1880, 860, 'Sources: Brunmair and Richter 2019 (Psychological Bulletin); Kang 2023', 30, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    """Recap as three shuffled cards dealt from a deck (layout change)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 80, INK, sw_in(T, 0), w='Bold')
    rows = ((1, 'Smooth practice can hide how little sticks', BLK, -5),
            (2, 'Mixing makes you choose the method, like a test', CHOICE, 3),
            (3, 'Mix things that look alike. Expect it to feel harder', MIXC, -2))
    for ln, txt, col, rot in rows:
        m = hl(ln); x = (400, 960, 1520)[ln - 1]; dy = 40 * (1 - m)
        c.rr(x - 260, 280 + dy + rot, x + 260, 720 + dy - rot, 28, CARD, m, outline=col, ow=5)
        c.circ(x, 360 + dy, 42, col, m, bg=CARD); c.text(x, 360 + dy, str(ln), 48, DARK, m, w='Bold', bg=col)
        ls = wrap(c, txt, 44, 440, 'Bold')
        for j, l in enumerate(ls):
            c.text(x, 540 + dy + (j - (len(ls) - 1) / 2) * 56, l, 44, INK, m, w='Bold', bg=CARD)
    c.text(960, 830, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    strip(c, BLOCKED, 1240, 330, 80, .75, 1, BLK, n=8)
    c.cross(1840, 330, 60, BAD)
    strip(c, MIXED, 1240, 600, 80, .75, 1, MIXC, n=8)
    c.check(1840, 600, 70, OK)

SCENES = [
 ('THE HOOK', ["In one study, the students who did worse during practice scored about three times higher on the test.",
               "Same problems. Same lessons. Only the order changed.",
               "So what were they doing differently?"], s_hook),
 ('THE USUAL WAY', ["Think of maths homework at the end of a chapter.",
                    "Ten problems, all the same kind. You learn the method on number one, then repeat it.",
                    "That's called blocked practice. It feels smooth. By the fifth one, you're fast."], s_homework),
 ('THE EXPERIMENT', ["In two thousand seven, Doug Rohrer and Kelli Taylor tested this with eighteen university students.",
                     "They learned to find the volume of four unusual shapes, like a wedge and a half cone.",
                     "One group practised in blocks, four of the same shape in a row. The other group got the same problems, shuffled."], s_experiment),
 ('PRACTICE', ["During practice, the block group did much better. Eighty nine percent correct, against sixty percent for the mixed group.",
               "If you stopped there, blocking looks like the clear winner.",
               "But one week later came the test."], s_practice),
 ('THE TEST', ["On the test, the mixed group scored sixty three percent. The block group scored twenty percent.",
               "About three times higher, for the group that struggled more.",
               "And almost all of the block group's mistakes were the same kind. They picked the wrong formula."], s_test),
 ('THE REASON', ["That's the hidden skill. In a block, you never choose the method. The page already told you.",
                 "When problems are mixed, every one starts with a question. Which kind is this?",
                 "And a test, like real life, asks that question too."], s_why),
 ('QUICK QUESTION', ["Quick question.",
                     "In another study, people learned to recognise painters by their style, from six paintings each by twelve artists.",
                     "Afterwards, which way did most of them think worked better? A, one artist at a time. Or B, the artists mixed up."], s_quiz),
 ('THE ANSWER', ["Most judged A, one artist at a time, as better.",
                 "But mixed study did better at naming the artist of new paintings. Fifty nine percent, against thirty six percent.",
                 "Seeing two styles side by side shows what makes them different.",
                 "Like twins: easier to tell apart when they stand next to each other."], s_answer),
 ('THE LIMITS', ["It isn't magic. A review of fifty nine studies found the biggest gains for things that look alike, like paintings.",
                 "For maths the gain was smaller, and for lists of words, blocking actually did better.",
                 "Mixing very different subjects, like a language and anatomy, won't help much. Mix things you could confuse."], s_limits),
 ('RECAP', ["Three things to keep.",
            "One: practice that feels smooth can hide how little will stick.",
            "Two: mixing makes you choose the method, and that's what a test asks.",
            "Three: mix things that look alike, and expect it to feel harder.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    strip(c, BLOCKED, 470, 420, 140, 1.0, 1, BLK, n=8)
    c.text(400, 320, 'In blocks', 46, BLK, 1, 'lm', 'Bold')
    strip(c, MIXED, 470, 700, 140, 1.0, fd(t, .3), MIXC, n=8)
    c.text(400, 600, 'Shuffled', 46, MIXC, fd(t, .3), 'lm', 'Bold')
    c.text(960, 172, 'Want it to stick? Shuffle it.', 84, MIXC, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Shuffled scored 3x higher on the test', 76, MIXC, sw_in(T, 1), w='Bold')

def short_groups(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Four odd shapes, 16 problems', 84, PU, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'In blocks, or shuffled', 84, INK, sw_in(T, 1), w='Bold')
    for k in range(4): shape(c, k, 360 + k * 400, 400, 1.6, 1 - hl(1) * .7)
    strip(c, BLOCKED, 230, 560, 97, .8, hl(1), BLK, p=fd(T(1), .1, 1.2))
    strip(c, MIXED, 230, 760, 97, .8, hl(1) * fd(T(1), 1.2), MIXC, p=fd(T(1), 1.3, 1.2))

def short_scores(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Practice: blocks win', 88, BLK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Test a week later: shuffled wins', 80, MIXC, sw_in(T, 1), w='Bold')
    p0 = fd(T(0), .3, 1.2)
    c.text(680, 280, 'PRACTICE', 44, DIM, 1, w='Bold')
    bar(c, 560, 780, 180, 400, 89, BLK, 1, p0, 'In blocks'); bar(c, 800, 780, 180, 400, 60, MIXC, 1, p0, 'Shuffled')
    c.line([(430, 780), (930, 780)], DIM, 4)
    p1 = hl(1) * fd(T(1), .5, 1.2)
    c.text(1360, 280, 'TEST', 44, CHOICE, hl(1), w='Bold')
    bar(c, 1240, 780, 180, 400, 20, BLK, hl(1), p1, 'In blocks'); bar(c, 1480, 780, 180, 400, 63, MIXC, hl(1), p1, 'Shuffled')
    c.line([(1110, 780), (1610, 780)], DIM, 4, hl(1))

def short_why(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'In a block, you never choose', 84, BLK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Mixed: which kind is this?', 88, CHOICE, sw_in(T, 1), w='Bold')
    sheet(c, 200, 260, 460, 560, [1] * 7, 1 - hl(1) * .6, 'Section 2: Cones')
    m = hl(1)
    c.rr(800, 300, 1720, 820, 30, CARD, m, outline=CHOICE, ow=4)
    shape(c, MIXED[int(t * .9) % 16], 1040, 520, 2.0, m, bg=CARD)
    c.text(1450, 520, '?', 200, CHOICE, m * (.7 + .3 * math.sin(t * 4)), w='Bold', bg=CARD)

SHORT_SCENES = [
 ('THE HOOK', ["Want what you practise to stick? Shuffle it.",
               "In one study, students who practised shuffled problems scored about three times higher on the test."], short_open),
 ('THE SETUP', ["They learned the volume of four unusual shapes.",
                "One group did four of the same shape in a row. The other got the same problems, shuffled."], short_groups),
 ('THE SCORES', ["In practice, blocks looked better. Eighty nine percent against sixty.",
                 "But a week later, on the test, shuffled scored sixty three. Blocks scored twenty."], short_scores),
 ('THE REASON', ["Why? In a block, you never choose the method. The page tells you.",
                 "Shuffled, every problem asks: which kind is this? And so does the test."], short_why),
 ('THE ANSWER', ["So mix up things you could confuse.",
                 "It feels harder, and it sticks better."], card('Mix what you could confuse.', 'Feels harder. Sticks better.')),
]
SHORT_HITS = [(4, 1, 0.0)]
