"""Episode: Why Leaves Turn Yellow, Orange and Red."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Leaves Change Color'           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {'colour': 'color'}
SHORT_HOOK = 'Why do leaves change color?'        # headline on the vertical Short
HITS = [(0, 1, 0.0), (3, 2, 0.0), (4, 3, 0.0)]    # 'you could not see it', 'hidden all summer', the quiz answer
THUMB = ['THE YELLOW', 'WAS ALWAYS', 'THERE']

LEAF = (70, 190, 95); LEAF2 = (40, 120, 60); GOLDL = (255, 205, 50); ORANGE = (255, 140, 40)
RED = (225, 45, 55); BROWN = (150, 95, 55); NIGHT = (34, 40, 92); SUGAR = (255, 245, 220)

# ---------------------------------------------------------------- helpers

def poly(c, pts, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def leaf_pts(x, y, s, ang=0.0):
    """Pointed leaf outline; (x, y) is the base of the blade, the tip points along ang (radians, 0 = up)."""
    pts = []
    for i in range(41):
        u = i / 40; wv = s * .36 * math.sin(math.pi * u) ** .8 * (1 + .25 * math.sin(math.pi * u * 2) * (u < .5))
        pts.append((wv, -s * u))
    pts = pts + [(-px, py) for px, py in pts[::-1]]
    ca, sa = math.cos(ang), math.sin(ang)
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]

def leaf(c, x, y, s, col, a=1.0, ang=0.0, bg=BG, vein=None, stem=True):
    if a <= 0.01: return
    ca, sa = math.cos(ang), math.sin(ang)
    P = lambda px, py: (x + px * ca - py * sa, y + px * sa + py * ca)
    if stem: c.line([P(0, 0), P(0, s * .2)], vein or mix(col, .6, (20, 20, 20)), max(3, s * .035), a, bg)
    poly(c, leaf_pts(x, y, s, ang), col, a, bg)
    vc = vein or mix(col, .62, (20, 20, 20))
    c.line([P(0, 0), P(0, -s * .93)], vc, max(2, s * .025), a, col)
    for k in range(1, 4):
        v = -s * (.16 + .17 * k); wv = s * .26 * math.sin(math.pi * (.16 + .17 * k)) ** .8
        for sg in (-1, 1):
            c.line([P(0, v + s * .02), P(sg * wv * .85, v - s * .12)], vc, max(2, s * .018), a, col)

def tree(c, x, base, s, cols, a=1.0, bg=BG, sway=0.0):
    if a <= 0.01: return
    c.rr(x - s * .07, base - s * .55, x + s * .07, base, 6, BROWN, a, bg=bg)
    c.line([(x, base - s * .42), (x - s * .22, base - s * .66)], BROWN, s * .045, a, bg)
    c.line([(x, base - s * .45), (x + s * .2, base - s * .7)], BROWN, s * .045, a, bg)
    blobs = [(-.24, -.78, .2), (.24, -.8, .2), (0, -.98, .24), (-.1, -.72, .19), (.12, -.66, .18), (-.3, -.96, .16), (.3, -.98, .16), (0, -1.16, .17)]
    for i, (dx, dy, r) in enumerate(blobs):
        c.circ(x + dx * s + sway * math.sin(i), base + dy * s, r * s, cols[i % len(cols)], a, bg=bg)

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def sun(c, x, y, r, a=1.0, t=0.0, bg=BG):
    if a <= 0.01: return
    for k in range(10):
        q = t * .4 + k * math.pi / 5
        c.line([(x + r * 1.3 * math.cos(q), y + r * 1.3 * math.sin(q)), (x + r * 1.7 * math.cos(q), y + r * 1.7 * math.sin(q))], YE, max(4, r * .12), a, bg)
    c.circ(x, y, r, YE, a, bg=bg)

def moon(c, x, y, r, a=1.0, bg=BG):
    if a <= 0.01: return
    c.circ(x, y, r, (225, 232, 255), a, bg=bg)
    c.circ(x + r * .45, y - r * .2, r * .9, bg, a, bg=bg)

def sugar(c, x, y, r, a=1.0, bg=BG):
    if a <= 0.01: return
    c.rr(x - r, y - r, x + r, y + r, r * .3, SUGAR, a, bg=bg)

def thumb_art(c):
    # one big leaf, green at the tip fading to yellow
    leaf(c, 1530, 900, 760, GOLDL, 1, -.35, vein=(170, 120, 20))
    poly(c, leaf_pts(1530, 900, 760, -.35)[28:54], LEAF, .9)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(4), 0, .5)
    if a > 0:
        # one big leaf: green on top of yellow. When line 1 starts the green wipes away.
        g = 1 - ease(clamp(T(1, .2) / 1.8)) if T(1) > -.2 else 1.0
        x, y = 1300, 760
        col = mix(LEAF, g, GOLDL)
        leaf(c, x, y, 580, col, a * fd(t, 0, .3), -.12)
        c.text(560, 300, 'The yellow in', 76, INK, a * fd(t, 0, .2), w='Bold')
        c.text(560, 395, 'autumn leaves', 76, INK, a * fd(t, 0, .2), w='Bold')
        c.text(560, 490, 'was there', 76, INK, a * fd(t, 0, .2), w='Bold')
        c.text(560, 585, 'all summer', 76, YE, a * fd(t, 0, .2), w='Bold')
        if T(1) > 0:
            pill(c, 560, 710, 'Hidden under the green', CY, a * fd(T(1), .3), 36)
        if T(2) > 0:
            k = a * fd(T(2))
            for i, (lab, cc) in enumerate([('Yellow', GOLDL), ('Orange', ORANGE), ('Red', RED)]):
                leaf(c, 300 + i * 260, 860, 120, cc, k * fd(T(2), .3 + i * .35), -.5 + .5 * i)
        if T(3) > 0:
            k = a * fd(T(3))
            leaf(c, 1000, 860, 120, BROWN, k, .55)
    if T(4) > 0:
        m = fd(T(4), .2, .7)
        c.text(960, 380 + 30 * (1 - m), 'Why Leaves', 140, INK, m, w='Bold')
        c.text(960, 545 + 30 * (1 - m), 'Change Color', 140, YE, m, w='Bold')
        c.line([(960 - 280 * m, 655), (960 + 280 * m, 655)], ORANGE, 8, m)
        c.text(960, 735, 'what really happens inside a leaf', 46, DIM, fd(T(4), .9), w='Medium')
        for i, cc in enumerate([LEAF, GOLDL, ORANGE, RED]):
            leaf(c, 330 + i * 420, 850, 70, cc, fd(T(4), 1.2 + i * .2), -.8 + .5 * i)

def s_green(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if a0 > 0:
        # the leaf as a food factory: sunlight in, sugar out
        leaf(c, 900, 740, 500, LEAF, a0, 0)
        sun(c, 330, 280, 80, a0 * fd(T(1), 0), t)
        for k in range(3):
            p = ((t * .5 + k / 3) % 1)
            c.circ(440 + 360 * p, 330 + 170 * p, 10, YE, a0 * fd(T(1), .2) * (1 - p))
        c.arrow(440, 330, 760, 480, YE, 6, a0 * fd(T(1), .2), 20)
        c.text(330, 440, 'Sunlight', 40, YE, a0 * fd(T(1), .2), w='Bold')
        c.arrow(1110, 520, 1400, 520, INK, 6, a0 * fd(T(1), 1.4), 20)
        for i in range(3): sugar(c, 1480 + i * 70, 520, 24, a0 * fd(T(1), 1.6 + i * .2))
        c.text(1550, 600, 'Sugar', 40, SUGAR, a0 * fd(T(1), 1.8), w='Bold')
        c.text(1550, 650, '(food for the tree)', 30, DIM, a0 * fd(T(1), 1.8), w='Medium')
        c.text(960, 190, 'A leaf is a tiny food factory', 60, INK, a0, w='Bold')
        pill(c, 1550, 300, 'Photosynthesis', GR, a0 * fd(T(1), 2.4), 34)
    if T(2) < -.1: return
    m = fd(T(2))
    c.text(960, 190, 'The green is chlorophyll', 66, INK, m, w='Bold')
    # zoomed view: green pigment particles that break in the light and are replaced
    c.circ(620, 520, 260, CARD, m, outline=LEAF, ow=6)
    c.text(620, 820, 'Inside the leaf (simplified)', 30, DIM, m, w='Medium')
    for i in range(40):
        ang = i * 2.399; r = 225 * math.sqrt((i + .5) / 40)
        x, y = 620 + r * math.cos(ang), 520 + r * math.sin(ang)
        life = (t * .45 + i * .137) % 1.0
        on = 1 - fd(life, .78, .2) if T(3) > 0 else 1.0
        grow = fd(life, 0, .15) if T(3) > 0 else 1.0
        c.circ(x, y, 14 * grow, LEAF, m * on, bg=CARD)
    if T(3) > 0:
        k = fd(T(3))
        sun(c, 1050, 330, 50, k, t)
        c.text(1420, 420, 'Sunlight breaks it down', 46, PK, k, w='Bold')
        c.text(1420, 500, 'The leaf makes more', 46, GR, k * fd(T(3), 1.6), w='Bold')
        # road crew repainting a line
        kk = fd(T(4)) if T(4) > -.1 else 0.0
        c.rr(1060, 640, 1780, 780, 20, (60, 64, 80), kk)
        p = (t * .25) % 1
        for j in range(6):
            x0 = 1090 + j * 115
            fade = 1 - .7 * clamp(((x0 - 1090) / 660 - p) % 1 * 1.0)
            c.rr(x0, 700, x0 + 80, 720, 4, YE, kk * fade, bg=(60, 64, 80))
        c.text(1420, 830, 'Like a line that gets repainted every day', 32, DIM, kk, w='Medium')

def s_trigger(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 420, 'What tells a tree', 100, INK, a0, w='Bold')
        c.text(960, 560, 'that autumn is coming?', 100, YE, a0, w='Bold')
    if T(1) < -.1: return
    m = fd(T(1))
    c.text(960, 190, 'Mostly: longer nights', 70, INK, m, w='Bold')
    # 24-hour bars: the night share grows from summer to autumn
    rows = [('Summer', .38), ('Late summer', .46), ('Autumn', .54)]
    x0, x1 = 480, 1640
    for i, (lab, nf) in enumerate(rows):
        k = m * fd(T(1), .5 + i * .6); y = 340 + i * 150
        if k <= 0.01: continue
        c.text(x0 - 30, y, lab, 38, INK, k, 'rm', 'Bold')
        xd = x0 + (x1 - x0) * (1 - nf)
        c.rr(x0, y - 45, xd, y + 45, 18, YE, k)
        c.rr(xd - 20, y - 45, x1, y + 45, 18, NIGHT, k, outline=(80, 90, 170), ow=3)
        c.rr(xd - 20, y - 45, xd + 10, y + 45, 0, YE, k)
        sun(c, x0 + 60, y, 18, k, t); moon(c, x1 - 60, y, 24, k, NIGHT)
    c.text(1060, 800, 'Night length shown is illustrative', 28, DIM, m * fd(T(1), 1.6), w='Regular')
    if T(2) > 0:
        k = fd(T(2))
        pill(c, 1060, 730, 'Cool weather plays a part too', CY, k, 34)
    if T(3) > 0:
        k = fd(T(3)); o = fd(T(3), 0, .4)
        c.rr(0, 140, 1920, 900, 0, BG, o * .97)
        c.text(960, 330, 'Weather changes a lot from year to year', 46, INK, k, w='Bold')
        c.text(960, 400, 'Night length does not', 52, YE, k * fd(T(3), 1.4), w='Bold')
        # a simple wall calendar
        kk = k * fd(T(3), 1.8)
        c.rr(760, 470, 1160, 820, 22, INK, kk)
        c.rr(760, 470, 1160, 550, 22, RED, kk, bg=INK); c.rr(760, 520, 1160, 550, 0, RED, kk, bg=INK)
        c.text(960, 510, 'CALENDAR', 34, INK, kk, w='Bold', bg=RED)
        for j in range(15):
            xx = 805 + (j % 5) * 77; yy = 600 + (j // 5) * 70
            c.rr(xx - 24, yy - 22, xx + 24, yy + 22, 6, (200, 205, 225) if j != 12 else ORANGE, kk, bg=INK)
    if T(4) > 0:
        k = fd(T(4)); o = fd(T(4), 0, .4)
        c.rr(0, 140, 1920, 900, 0, BG, o)
        leaf(c, 1100, 760, 440, mix(LEAF, 1 - .6 * ease(clamp(T(4, .4) / 3)), GOLDL), k, 0)
        c.text(500, 450, 'New chlorophyll:', 46, INK, k, w='Bold')
        c.text(500, 530, 'stopped', 64, PK, k * fd(T(4), .8), w='Bold')
        c.cross(500, 650, 50, PK, k * fd(T(4), 1.0))

def s_yellow(c, T, t):
    a0 = 1 - fd(T(3), -.4, .4)
    if a0 > 0:
        g = 1 - ease(clamp(T(0, .3) / 2.4))
        leaf(c, 640, 830, 600, mix(LEAF, g, GOLDL), a0 * fd(t, 0, .3), -.1)
        c.text(1330, 260, 'As the green fades...', 54, INK, a0 * fd(T(0)), w='Bold')
        if T(1) > 0:
            k = a0 * fd(T(1))
            c.text(1330, 380, 'Carotenoids', 96, YE, k, w='Bold')
            c.text(1330, 470, 'yellow and orange pigments', 40, DIM, k, w='Medium')
            for i, cc in enumerate([GOLDL, (255, 175, 45), ORANGE]):
                c.circ(1210 + i * 120, 560, 34, cc, k * fd(T(1), .5 + i * .2))
        if T(2) > 0:
            pill(c, 1330, 680, 'In the leaf all summer', YE, a0 * fd(T(2)), 40, h=72)
            c.text(1330, 770, 'hidden under the green', 40, INK, a0 * fd(T(2), .8), w='Bold')
    if T(3) > -.1:
        # paint layers: green paint scraped off a yellow wall
        m = fd(T(3)) * (1 - fd(T(4), -.4, .4))
        if m > 0:
            c.text(960, 190, 'Like paint over paint', 64, INK, m, w='Bold')
            c.rr(360, 290, 1560, 800, 20, GOLDL, m)
            p = ease(clamp(T(3, 1.0) / 2.6))
            xs = 360 + 1200 * p
            if xs < 1560: c.rr(xs, 290, 1560, 800, 20 if p < .02 else 0, LEAF, m, bg=GOLDL)
            # scraper
            c.rr(xs - 16, 260, xs + 16, 830, 8, (190, 198, 230), m * (p < .99))
            c.text(700, 545, 'yellow underneath', 52, (120, 80, 0), m * fd(T(3), 2.2), w='Bold', bg=GOLDL)
    if T(4) > -.1:
        m = fd(T(4))
        c.text(960, 200, 'Same family of pigments', 60, INK, m, w='Bold')
        # a carrot
        poly(c, [(560, 380), (700, 380), (630, 780)], ORANGE, m)
        for k in range(4):
            c.line([(585 + k * 28, 440 + k * 70), (640 + k * 12, 445 + k * 70)], (200, 100, 30), 5, m, ORANGE)
        for dx in (-40, 0, 40):
            c.line([(630, 380), (630 + dx, 260)], LEAF, 14, m)
        c.text(1250, 440, 'carrot', 80, ORANGE, m * fd(T(4), .8), w='Bold')
        c.arrow(1250, 500, 1250, 580, DIM, 6, m * fd(T(4), 1.4), 18)
        c.text(1250, 650, 'carotene', 80, YE, m * fd(T(4), 1.6), w='Bold')
        c.text(1250, 740, 'named after the carrot (Latin: carota)', 32, DIM, m * fd(T(4), 2.2), w='Medium')

def s_quiz(c, T, t):
    m = fd(T(0))
    c.text(960, 190, 'Quick question', 70, YE, m, w='Bold')
    c.circ(330, 520, 150, CARD, m, outline=YE, ow=6)
    c.text(330, 520, '?', 200, YE, m * (1 + .0 * math.sin(t)), w='Bold', bg=CARD)
    if T(1) > -.1:
        k = fd(T(1))
        leaf(c, 900, 720, 360, RED, k, 0)
        c.text(1420, 330, 'Red leaves:', 52, INK, k, w='Bold')
        c.text(1420, 400, 'was the red hiding', 44, INK, k * fd(T(1), .4), w='Medium')
        c.text(1420, 455, 'all summer too?', 44, INK, k * fd(T(1), .4), w='Medium')
        ans = fd(T(3)) if T(3) > -.1 else 0.0
        for i, (lab, col) in enumerate([('A  Hidden all summer', DIM), ('B  Made new in autumn', GR)]):
            y = 590 + i * 110; kk = k * fd(T(1), 1.0 + i * .3)
            hi = col if (i == 1 and ans > 0) else (60, 70, 120)
            c.rr(1160, y - 42, 1700, y + 42, 42, CARD, kk * (1 - .5 * ans * (i == 0)), outline=hi, ow=5)
            c.text(1430, y, lab, 34, INK if not (i == 0 and ans > 0) else DIM, kk, w='Bold', bg=CARD)
        if ans > 0:
            c.check(1740, 700, 30, GR, ans); c.cross(1740, 590, 24, PK, ans)
    if T(2) > 0 and T(3) < 0:
        # countdown ring while the viewer guesses
        p = clamp(T(2) / 2.2)
        pts = [(330 + 175 * math.sin(2 * math.pi * u / 60), 520 - 175 * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * (1 - p)) + 1)]
        c.line(pts, CY, 10, fd(T(2)))
    if T(3) > 0:
        c.text(960, 860, 'For most trees, most red is made new each autumn', 38, GR, fd(T(3), .4), w='Bold')

def s_red(c, T, t):
    a0 = 1 - fd(T(4), -.4, .4)
    m = fd(T(0)) * a0
    if m > 0:
        c.text(960, 190, 'Anthocyanins: the red and purple', 62, INK, m, w='Bold')
        # big leaf with its stalk; a seal grows at the base
        X, Y, S0 = 640, 720, 470
        red = ease(clamp(T(3, .2) / 2.4)) if T(3) > -.2 else 0.0
        col = mix(RED, red, mix(LEAF, .35, GOLDL))
        leaf(c, X, Y, S0, col, m, 0, stem=False)
        c.rr(X - 9, Y, X + 9, Y + 150, 5, BROWN, m)
        if T(1) > -.1:
            k = fd(T(1)) * a0; sw = ease(clamp(T(1, .3) / 1.6))
            c.rr(X - 34 * sw, Y + 50, X + 34 * sw, Y + 72, 6, PK, k)
            c.arrow(X + 230, Y + 61, X + 50, Y + 61, PK, 5, k, 16)
            c.text(X + 250, Y + 61, 'sealing layer', 36, PK, k, 'lm', 'Bold')
        if T(2) > -.1:
            k = fd(T(2)) * a0
            for i in range(9):
                ang = i * 2.1; rr = 40 + (i * 23) % 120
                bx = X + rr * .9 * math.cos(ang) * .8; by = Y - 160 - rr * .9 * math.sin(ang) * .9 - 30
                dy = 6 * math.sin(t * 2 + i)
                sugar(c, bx, by + dy, 12, k * fd(T(2), .2 + i * .12), col)
            c.text(1340, 330, 'Sugar gets trapped', 50, SUGAR, k, w='Bold')
            c.text(1340, 395, 'in the leaf', 50, SUGAR, k, w='Bold')
        if T(3) > -.1:
            k = fd(T(3)) * a0
            sun(c, 1150, 520, 34, k, t)
            c.text(1210, 520, '+', 60, INK, k, w='Bold')
            sugar(c, 1270, 520, 22, k)
            c.text(1325, 520, '=', 60, INK, k, w='Bold')
            c.circ(1400, 520, 30, RED, k); c.circ(1470, 520, 30, (160, 40, 110), k)
            c.text(1340, 620, 'red and purple pigment', 40, RED, k * fd(T(3), .8), w='Bold')
    if T(4) > -.1:
        m = fd(T(4)) * (1 - fd(T(5), -.4, .4))
        if m > 0:
            c.text(960, 190, 'Saving for spring', 66, INK, m, w='Bold')
            leaf(c, 560, 740, 420, RED, m, .15)
            # little packets move from leaf to the trunk
            c.rr(1380, 260, 1480, 800, 14, BROWN, m)
            for i in range(5):
                p = (t * .35 + i / 5) % 1
                x = 700 + (1360 - 700) * p; y = 560 - 80 * math.sin(math.pi * p)
                sugar(c, x, y, 16, m * (1 - fd(p, .85, .15)))
            c.text(1060, 650, 'Sugars and other useful material', 36, INK, m * fd(T(4), .6), w='Bold')
            c.text(1060, 700, 'move back into the tree', 36, INK, m * fd(T(4), .6), w='Bold')
    if T(5) > -.1:
        m = fd(T(5))
        c.text(960, 190, 'Why red? One leading idea', 62, INK, m, w='Bold')
        leaf(c, 800, 760, 440, RED, m, 0)
        # a shield over the leaf
        k = m * fd(T(5), .8)
        poly(c, [(1180, 330), (1420, 330), (1420, 520), (1300, 640), (1180, 520)], CY, k * .9)
        c.text(1300, 450, 'shield', 44, BG, k, w='Bold', bg=CY)
        c.text(1300, 720, 'Red may protect the leaf', 40, INK, k, w='Bold')
        c.text(1300, 770, 'while nutrients move out', 40, INK, k, w='Bold')
        pill(c, 1300, 850, 'Still being studied', YE, m * fd(T(5), 2.0), 30, h=54)

def s_brown(c, T, t):
    m = fd(T(0)) * (1 - fd(T(2), -.4, .4))
    if m > 0:
        c.text(960, 190, 'And the brown?', 76, INK, m, w='Bold')
        leaf(c, 560, 780, 480, BROWN, m, -.1, vein=(100, 60, 30))
        c.text(1300, 380, 'Tannins', 100, (205, 150, 95), m * fd(T(0), .6), w='Bold')
        c.text(1300, 470, 'in oaks and beeches', 44, DIM, m * fd(T(0), 1.0), w='Medium')
        if T(1) > 0:
            k = m * fd(T(1))
            for i, (lab, cc) in enumerate([('green', LEAF), ('yellow', GOLDL), ('red', RED)]):
                x = 1080 + i * 220; out = fd(T(1), .6 + i * .5)
                c.circ(x, 620, 46, cc, k * (1 - out))
                c.cross(x, 620, 30, PK, k * out)
            c.circ(1300, 760, 52, BROWN, k * fd(T(1), 2.2))
            c.text(1300, 850, 'brown is what is left', 36, INK, k * fd(T(1), 2.2), w='Bold')
    if T(2) < -.1: return
    k = fd(T(2))
    c.text(960, 190, 'Then the leaf lets go', 70, INK, k, w='Bold')
    tree(c, 440, 860, 430, [ORANGE, RED, GOLDL], k, sway=4 * math.sin(t))
    for i in range(9):
        p = ((t * .18 + i / 9) % 1)
        x = 650 + 900 * p + 60 * math.sin(t * 2 + i); y = 300 + 520 * p
        leaf(c, x, y, 60, [ORANGE, RED, GOLDL, BROWN][i % 4], k * fd(T(2), .5) * (1 - fd(p, .9, .1)), t * 1.5 + i)
    if T(3) > 0:
        kk = fd(T(3))
        for i in range(5):
            x = 1300 + i * 90 + 40 * math.sin(t * 3 + i)
            c.line([(x, 360), (x - 60, 460)], CY, 5, kk * .8)
        c.text(1480, 560, 'Wind or rain', 52, CY, kk, w='Bold')
        c.text(1480, 630, 'carries it down', 52, CY, kk, w='Bold')

def s_weather(c, T, t):
    a0 = fd(T(0)) * (1 - fd(T(1), -.4, .4))
    if a0 > 0:
        c.text(960, 300, 'No two autumns', 110, INK, a0, w='Bold')
        c.text(960, 440, 'look the same', 110, ORANGE, a0, w='Bold')
        for i, cols in enumerate([[ORANGE, RED, GOLDL], [GOLDL, (230, 180, 60), LEAF], [RED, (170, 40, 90), ORANGE]]):
            tree(c, 520 + i * 440, 860, 230, cols, a0 * fd(T(0), .5 + i * .3))
    if T(1) < -.1: return
    cards = [(1, 'Sunny days', 'cool nights, not freezing', 'Brightest reds', GR), (2, 'Warm autumn', '', 'Duller color', PK),
             (2, 'Severe summer drought', '', 'Color can start later', PK)]
    m0 = fd(T(1))
    c.text(960, 190, 'What the weather does', 66, INK, m0, w='Bold')
    for i, (li, lab, sub, res, col) in enumerate(cards):
        off = 0.0 if i < 2 else 2.2
        k = fd(T(li), off) if T(li) > -.1 else 0.0; x = 380 + i * 580
        if k <= 0.01: continue
        c.rr(x - 260, 270, x + 260, 760, 28, CARD, k, outline=col, ow=5)
        y = 420
        if i == 0:
            sun(c, x - 70, y, 50, k, t, CARD); moon(c, x + 110, y - 10, 40, k, CARD)
        elif i == 1:
            sun(c, x, y, 64, k, t, CARD)
        else:
            c.rr(x - 160, y + 10, x + 160, y + 70, 10, (150, 110, 70), k, bg=CARD)
            for j in range(5): c.line([(x - 130 + j * 65, y + 10), (x - 110 + j * 65, y + 70)], (90, 60, 40), 5, k, (150, 110, 70))
            sun(c, x, y - 70, 40, k, t, CARD)
        c.text(x, 560, lab, 40 if i < 2 else 34, INK, k, w='Bold', bg=CARD)
        if sub: c.text(x, 610, sub, 28, DIM, k, w='Medium', bg=CARD)
        c.text(x, 690, res, 38, col, k * fd(T(li), off + .8), w='Bold', bg=CARD)
    if T(3) > 0:
        k = fd(T(3))
        c.rr(260, 790, 1660, 870, 40, CARD, k, outline=GOLDL, ow=4)
        c.text(960, 830, 'Yellows stay fairly steady: those pigments were there all along', 32, GOLDL, k, w='Bold', bg=CARD)

REC = [('1', 'Longer nights stop new green', LEAF), ('2', 'Yellow was hiding all along', GOLDL), ('3', 'Most red is made new', RED)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 255, 290 + up, x + 255, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 190, 355 + up, 40, col, m, bg=CARD); c.text(x - 190, 355 + up, nn, 48, BG, m, w='Bold', bg=col)
        y = 540 + up
        if i == 0:
            moon(c, x - 90, y - 60, 50, m, CARD)
            leaf(c, x + 70, y + 80, 190, LEAF, m, .2, CARD, stem=False)
            c.cross(x + 80, y, 34, PK, m)
        elif i == 1:
            g = .5 + .5 * math.sin(t * 1.4)
            leaf(c, x, y + 90, 220, mix(LEAF, g, GOLDL), m, 0, CARD, stem=False)
        else:
            leaf(c, x - 20, y + 90, 210, RED, m, -.15, CARD, stem=False)
            c.text(x + 120, y - 70, 'NEW', 34, YE, m, w='Bold', bg=CARD)
        c.text(x, 725 + up, lab, 30, INK, m, w='Bold', bg=CARD)
    if T(4) > 0:
        o2 = 1 - fd(T(5), -.3, .5)
        c.text(960, 400, 'The yellow was always there.', 88, GOLDL, fd(T(4)) * o2, w='Bold')
        c.text(960, 560, 'The red is brand new.', 88, RED, fd(T(4), 1.4) * o2, w='Bold')
    if T(5) > 0:
        m = fd(T(5), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(5), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(5), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Here is a surprising fact. The yellow in autumn leaves was there all summer.",
            "You just could not see it.",
            "So why do leaves turn yellow, orange and red?", "And why do some just go brown?",
            "Here is what is really happening inside a leaf."], s_hook),
 ('1  ·  THE GREEN', ["Start with summer. A leaf is a tiny food factory.",
            "It uses sunlight to make sugar, the tree's food. This is called photosynthesis.",
            "The green colour comes from a pigment called chlorophyll.",
            "Sunlight breaks chlorophyll down all the time, so the leaf keeps making more.",
            "It is like a road line that gets repainted every day."], s_green),
 ('2  ·  THE SIGNAL', ["So what tells a tree that autumn is coming?",
            "Mostly, the nights get longer.",
            "Cool weather plays a part too.",
            "But weather changes a lot from year to year. Night length does not. It works like a calendar.",
            "As the nights grow long, the tree slows, then stops, making new chlorophyll."], s_trigger),
 ('3  ·  THE YELLOW', ["As the green fades, other colours show through.",
            "Yellow and orange pigments, called carotenoids.",
            "They were in the leaf all summer, hidden under the green.",
            "It is like a wall painted green over yellow. Scrape off the green, and the yellow appears.",
            "The same family of pigments makes carrots orange. Carotene is even named after the carrot."], s_yellow),
 ('4  ·  QUICK QUESTION', ["Quick question. Take a second and guess.",
            "Red leaves. Was the red hiding all summer too, like the yellow?",
            "Three, two, one.",
            "For most trees, no. Most of the red is made new, in autumn."], s_quiz),
 ('5  ·  THE RED', ["The red and purple come from pigments called anthocyanins.",
            "In autumn, a sealing layer starts to grow where the leaf joins the twig.",
            "It traps sugar inside the leaf.",
            "With bright sunlight and that extra sugar, the leaf makes red and purple pigment.",
            "Meanwhile, the tree pulls sugars and other useful material back out of the leaf, to use in spring.",
            "Why make red at all? One leading idea is that it helps protect the leaf while that happens. Scientists are still studying it."], s_red),
 ('6  ·  THE BROWN', ["And brown? In oaks and beeches, much of the brown comes from tannins.",
            "They show once the green, yellow and red are gone.",
            "Then the sealing layer finishes its job. The leaf lets go.",
            "Wind or rain carries it down."], s_brown),
 ('7  ·  THE WEATHER', ["That is why no two autumns look the same.",
            "Sunny days and cool nights, but not freezing, give the brightest reds.",
            "A warm autumn dulls the colour. A severe summer drought can delay it by a few weeks.",
            "Yellows stay fairly steady from year to year, because those pigments were there all along."], s_weather),
 ('RECAP', ["So remember three things.",
            "One. Longer nights tell the tree to stop making new green chlorophyll.",
            "Two. Yellow and orange were hiding there all summer.",
            "Three. Most red is made new in autumn, from trapped sugar and sunlight.",
            "The yellow was always there. The red is brand new.",
            "If this helped, subscribe for more."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-60 s.
SHORT_SCENES = [
 ('WHY LEAVES CHANGE', ["Here is a surprising fact. The yellow in autumn leaves was there all summer.", "You just could not see it."], s_hook),
 ('THE SIGNAL', ["So what changes in autumn?", "The nights get longer.", "Cool air helps too.", "Long nights work like a calendar.",
                 "So the tree stops making green chlorophyll."], s_trigger),
 ('THE YELLOW', ["As the green fades, other colours show through.", "Yellow and orange pigments, called carotenoids.",
                 "They were hiding under the green all summer."], s_yellow),
 ('THE RED', ["Red is different. It comes from pigments called anthocyanins.", "In autumn, a seal grows where the leaf meets the twig.",
              "It traps sugar inside the leaf.", "Sugar plus bright sun makes brand new red pigment."], s_red),
 ('THE ANSWER', ["So the yellow was always there.", "The red is brand new.", "Follow for more."], card('Yellow: always there', 'Red: brand new')),
]
SHORT_HITS = [(4, 1, 0.0)]
