"""Episode: Your Battery Is Sealed. So Where Does Its Charge Go?"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Where Does Your Battery's Charge Go?"   # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.97
SHORT_HOOK = "Where does your battery's charge go?"     # headline on the vertical Short
HITS = [(0, 2, 0.0), (3, 2, 0.0), (5, 3, 0.0)]           # title card, "main cause of capacity fade", quiz answer
THUMB = ['SEALED SHUT.', 'SO WHERE DOES', 'THE CHARGE GO?']
MUSIC_LEVEL = 0.006                                      # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                           # no dead air before the first word (lesson of 2026-10-19)
CAPTION_FIXES = {
    ' percent': '%', 'one thousand': '1,000', '25 degrees': '25°C', '40 degrees': '40°C', '35 degrees': '35°C',
}
# Applied lesson (learnings.md, 2026-10-20): open with the paradox before the lesson (outlier pattern of
# big science channels: a familiar system people rely on but few understand, framed as a puzzle).
# Hook and title: the battery is sealed and nothing leaks out, yet it holds less every year.

CATH = (150, 120, 255); GRAPH = (96, 104, 140); ELEC = (26, 44, 88); CRUST = (240, 150, 60)
ION = CY; TRAP = PK; SHELL = (60, 66, 110); SCREEN = (34, 52, 96)

# ---------------------------------------------------------------- helpers

def pill(c, x, y, txt, col, a=1.0, size=34, bg=BG, padx=26, h=62, fg=None):
    if a <= 0.01: return
    w = c.tw(txt, size, 'Bold') + 2 * padx
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h / 2, col, a, bg=bg)
    c.text(x, y, txt, size, fg or BG, a, w='Bold', bg=col)

def lvl_col(v):
    return GR if v > .5 else (YE if v > .25 else PK)

def phone(c, x, y, s, a=1.0, level=1.0, bg=BG, label=True):
    """Phone centred at (x, y), s = half-height, with a battery gauge on screen."""
    if a <= 0.01: return
    c.rr(x - s * .5, y - s, x + s * .5, y + s, s * .12, SHELL, a, bg=bg)
    c.rr(x - s * .42, y - s * .86, x + s * .42, y + s * .86, s * .08, SCREEN, a, bg=SHELL)
    bw, bh = s * .5, s * .24
    c.rr(x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2, s * .04, None, a, outline=INK, ow=max(2, s * .03), bg=SCREEN)
    c.rr(x + bw / 2 + 2, y - bh * .22, x + bw / 2 + s * .05, y + bh * .22, 2, INK, a, bg=SCREEN)
    v = clamp(level)
    if v > .01:
        c.rr(x - bw / 2 + s * .03, y - bh / 2 + s * .03, x - bw / 2 + s * .03 + (bw - s * .06) * v, y + bh / 2 - s * .03, s * .02, lvl_col(v), a, bg=SCREEN)
    if label:
        c.text(x, y + s * .35, f'{int(round(v * 100))}%', max(18, s * .2), INK, a, w='Bold', bg=SCREEN)

ION_Y = [((i * 37) % 11) / 10 for i in range(14)]
def cell(c, x0, y0, x1, y1, a=1.0, p=0.0, crust=0.0, trapped=0, t=0.0, labels=True, bg=BG, n=12):
    """Battery cross-section. p: 0 = ions at the left (cathode), 1 = parked in the graphite (right).
    crust: thickness of the SEI layer on the graphite (0..1). trapped: ions stuck inside the crust."""
    if a <= 0.01: return
    w = x1 - x0; cw = w * .22
    c.rr(x0, y0, x1, y1, 28, (20, 26, 56), a, outline=(70, 80, 130), ow=4, bg=bg)
    c.rr(x0 + 16, y0 + 16, x0 + cw, y1 - 16, 18, mix(CATH, .55), a, bg=(20, 26, 56))
    c.rr(x0 + cw + 10, y0 + 16, x1 - cw - 10, y1 - 16, 14, ELEC, a, bg=(20, 26, 56))
    gx = x1 - cw
    c.rr(gx, y0 + 16, x1 - 16, y1 - 16, 18, GRAPH, a, bg=(20, 26, 56))
    for j in range(7):                                          # graphite layers
        yy = y0 + 40 + j * (y1 - y0 - 80) / 6
        c.line([(gx + 14, yy), (x1 - 30, yy)], (140, 148, 185), 4, a, GRAPH)
    if crust > .01:
        cwid = 8 + 34 * crust
        c.rr(gx - cwid, y0 + 16, gx + 4, y1 - 16, 8, CRUST, a, bg=ELEC)
    if labels:
        c.text(x0 + 16 + (cw - 16) / 2, y1 + 34, 'metal oxide', 30, CATH, a, w='Bold')
        c.text((x0 + x1) / 2, y1 + 34, 'liquid', 30, (120, 150, 210), a, w='Bold')
        c.text(gx + (cw - 16) / 2, y1 + 34, 'graphite', 30, (170, 178, 210), a, w='Bold')
    # mobile ions
    left, right = x0 + cw * .55, gx + cw * .45
    for i in range(trapped, n):
        q = ease(clamp(p * 1.6 - (i / n) * .6))
        yy = y0 + 50 + ION_Y[i % len(ION_Y)] * (y1 - y0 - 100)
        xx = left + (right - left) * q + 5 * math.sin(t * 2 + i)
        c.circ(xx, yy, 16, ION, a, bg=ELEC)
        c.text(xx, yy, '+', 22, BG, a, w='Bold', bg=ION)
    # trapped ions in the crust
    cwid = 8 + 34 * crust
    for i in range(trapped):
        yy = y0 + 50 + ION_Y[i % len(ION_Y)] * (y1 - y0 - 100)
        c.circ(gx - cwid / 2 + 2, yy, 15, TRAP, a, bg=CRUST)

def thermo(c, x, y, h, v, col, a=1.0, bg=BG):
    if a <= 0.01: return
    c.rr(x - 18, y - h, x + 18, y + 10, 18, (50, 56, 96), a, bg=bg)
    c.circ(x, y + 22, 34, col, a, bg=bg)
    c.rr(x - 9, y - h * v, x + 9, y + 10, 9, col, a, bg=(50, 56, 96))

def sun(c, x, y, r, a=1.0, t=0.0, bg=BG):
    if a <= 0.01: return
    for k in range(10):
        u = k * math.pi / 5 + t * .4
        c.line([(x + r * 1.25 * math.cos(u), y + r * 1.25 * math.sin(u)), (x + r * 1.6 * math.cos(u), y + r * 1.6 * math.sin(u))], YE, r * .14, a, bg)
    c.circ(x, y, r, YE, a, bg=bg)

def car(c, x, y, s, a=1.0, bg=BG, col=(200, 80, 90)):
    if a <= 0.01: return
    c.rr(x - s, y - s * .25, x + s, y + s * .3, s * .18, col, a, bg=bg)
    c.rr(x - s * .55, y - s * .62, x + s * .45, y - s * .2, s * .16, col, a, bg=bg)
    c.rr(x - s * .45, y - s * .54, x + s * .35, y - s * .26, s * .1, (120, 170, 220), a, bg=col)
    for dx in (-.55, .55):
        c.circ(x + s * dx, y + s * .3, s * .2, (40, 44, 70), a, bg=bg)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def thumb_art(c):
    cell(c, 1180, 250, 1840, 680, 1, p=.55, crust=1, trapped=5, labels=False)
    c.text(1510, 760, 'lithium stuck here', 46, PK, 1, w='Bold')
    c.arrow(1560, 720, 1640, 690, PK, 7, 1, 24)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), .2, .5)
    if a > 0:
        # moving from frame one: the phone's full charge keeps shrinking, year after year
        yrs = min(3, int(t / 1.6))
        lv = 1.0 - .08 * yrs - .08 * fd(t % 1.6, 1.0, .5) * (yrs < 3)
        phone(c, 960, 520, 300, a, level=lv)
        c.text(960, 140, 'Sealed shut. Nothing leaks out.', 66, INK, a, w='Bold')
        lock_a = a
        c.rr(1240, 330, 1340, 420, 16, YE, lock_a); c.circ(1290, 330, 34, None, lock_a, outline=YE, ow=12)
        c.text(1290, 378, 'sealed', 22, BG, lock_a, w='Bold', bg=YE)
        k1 = hl(1)
        if k1 > 0:
            c.text(560, 470, 'full charge,', 40, DIM, k1, 'rm', 'Medium')
            c.text(560, 520, f'year {yrs + 1}', 54, YE, k1, 'rm', 'Bold')
            pill(c, 960, 860 - 20, 'holds less every year', PK, k1, 38, h=70)
    if T(2) > 0:
        m = fd(T(2), .35, .7)
        c.text(960, 330 + 30 * (1 - m), 'Where Does Your', 120, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), "Battery's Charge Go?", 120, YE, m, w='Bold')
        c.line([(960 - 360 * m, 590), (960 + 360 * m, 590)], CY, 8, m)
        c.text(960, 680, 'The answer is hiding inside.', 46, DIM, fd(T(2), 1.2), w='Medium')

def s_inside(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'Inside the battery', 66, INK, hl(0), w='Bold')
    k = hl(0)
    if T(3) > -.1:
        p = .5 - .5 * math.cos(T(3) * 1.6)
    elif T(2) > -.1:
        p = 1 - fd(T(2), .3, 3.0)
    else:
        p = fd(T(1), .5, 3.0)
    cell(c, 360, 220, 1560, 660, k, p=p, t=t)
    if hl(1) > 0 and T(2) < 0:
        c.text(960, 790, 'charging: lithium ions drive into the graphite', 40, CY, hl(1), w='Bold')
        c.arrow(800, 735, 1120, 735, CY, 6, hl(1), 22)
    if hl(2) > 0:
        c.text(960, 790, 'using the phone: they drive back, and power flows', 40, GR, hl(2) * (1 - hl(3)), w='Bold')
        c.arrow(1120, 735, 800, 735, GR, 6, hl(2) * (1 - hl(3)), 22)
    if hl(3) > 0:
        pill(c, 960, 800, 'more ions making the trip = more battery', YE, hl(3), 38, h=72)

def s_crust(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'The catch: a thin crust', 66, INK, hl(0), w='Bold')
    cr = fd(T(0), .8, 1.5) * (.55 + .45 * fd(T(2), 1.0, 3.0))
    tr = int(4 * fd(T(2), .8, 3.0))
    cell(c, 360, 220, 1560, 660, hl(0), p=.15, crust=cr, trapped=tr, t=t)
    # call-out pointing at the crust
    gx = 1560 - 1200 * .22
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        c.arrow(gx - 30, 760, gx - 20, 680, CRUST, 6, k1, 22)
        c.text(960, 780, 'solid electrolyte interphase (SEI)', 42, CRUST, k1, w='Bold')
        c.text(960, 840, 'a filter: ions pass, the liquid is kept off', 34, DIM, k1, w='Medium')
    k2 = hl(2)
    if k2 > 0:
        c.text(960, 780, 'building it uses up lithium', 44, PK, k2, w='Bold')
        c.text(960, 840, 'and it keeps growing, slowly, in use and at rest', 34, DIM, k2 * fd(T(2), 1.2), w='Medium')

def s_trapped(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), -.2, .4)
    k = hl(0)
    if a > 0:
        c.text(960, 140, 'Stuck in the crust', 66, INK, k * a, w='Bold')
        # the ions that still move keep shuttling; the trapped ones never leave
        p = .5 + .5 * math.sin(t * 1.3)
        cell(c, 360, 220, 1560, 660, k * a, p=p, crust=1, trapped=5, t=t, labels=False)
        k1 = hl(1) * a
        c.text(960, 760, 'still inside the battery', 42, INK, k1, w='Bold')
        c.text(960, 820, "but they can't carry charge any more", 42, PK, k1 * fd(T(1), .6), w='Bold')
    if T(2) > -.1:
        m = fd(T(2))
        c.rr(330, 240, 1590, 700, 30, CARD, m, outline=CY, ow=5)
        c.text(450, 330, '“', 150, CY, m, w='Bold', bg=CARD)
        c.text(960, 400, 'Losing mobile lithium ions is', 56, INK, m, w='Bold', bg=CARD)
        c.text(960, 490, 'the main cause of capacity fade.', 56, YE, m, w='Bold', bg=CARD)
        c.text(960, 610, 'Electrochemical Society, on research at Argonne National Laboratory', 30, DIM, m, w='Medium', bg=CARD)

def s_cycles(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), -.2, .4)
    c.text(960, 140, 'Counting wear: charge cycles', 64, INK, hl(0), w='Bold')
    if a > 0:
        k1 = hl(1) * a
        if k1 > 0:
            # 75% today + 25% tomorrow = one cycle
            for j, (lab, v, d) in enumerate((('today', .75, 0), ('tomorrow', .25, 2.2))):
                kk = k1 * fd(T(1), d)
                x = 560 + j * 520
                phone(c, x, 470, 200, kk, level=1 - v * fd(T(1), d + .3, 1.2), label=False)
                c.text(x, 720, f'use {int(v * 100)}%', 46, YE, kk, w='Bold')
                c.text(x, 780, lab, 34, DIM, kk, w='Medium')
            c.text(820, 470, '+', 90, INK, k1 * fd(T(1), 2.2), w='Bold')
            kk = k1 * fd(T(1), 3.6)
            c.text(1340, 470, '=', 90, INK, kk, w='Bold')
            ring(c, 1560, 470, 110, fd(T(1), 3.8, 1.2), GR, kk, 16)
            c.text(1560, 450, '1', 80, GR, kk, w='Bold'); c.text(1560, 520, 'cycle', 32, GR, kk, w='Bold')
    if T(2) > -.1:
        m = fd(T(2))
        c.text(960, 250, 'Apple: about 80% of capacity left after...', 42, DIM, m, w='Medium')
        for j, (lab, n, d) in enumerate((('older iPhones', 500, 0), ('iPhone 15 models', 1000, 1.8))):
            kk = m * fd(T(2), d)
            y = 400 + j * 200
            c.text(560, y, lab, 40, INK, kk, 'rm', 'Bold')
            c.rr(600, y - 34, 600 + 900 * (n / 1000) * fd(T(2), d + .2, 1.0), y + 34, 16, (CY, GR)[j], kk)
            c.text(620 + 900 * (n / 1000) * fd(T(2), d + .2, 1.0), y + 72, f'{n:,} full cycles', 36, (CY, GR)[j], kk, 'mm' if j else 'mm', 'Bold')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    c.text(960, 140, 'Quick question', 70, YE, m * (1 - ans), w='Bold')
    c.text(960, 220, 'Which battery wears out faster?', 52, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 180, 'Hot and full: the worst combination', 64, PK, ans, w='Bold')
    k1 = hl(1)
    for j, x in enumerate((560, 1360)):
        kk = k1 * fd(T(1), j * 2.2)
        if kk <= 0: continue
        bad = j == 0
        dim = 1 - (.45 * ans if not bad else 0)
        c.rr(x - 330, 290, x + 330, 780, 30, CARD, kk * dim, outline=(PK if ans > 0 else YE) if bad else CY, ow=5)
        c.text(x - 260, 350, 'AB'[j], 46, YE if bad else CY, kk * dim, w='Bold', bg=CARD)
        if bad:
            sun(c, x + 180, 400, 46, kk, t, CARD)
            car(c, x - 40, 560, 170, kk, CARD)
            phone(c, x + 230, 600, 80, kk, level=1.0, bg=CARD, label=False)
            thermo(c, x - 250, 600, 150, .9, PK, kk, CARD)
            c.text(x, 720, '100% in a hot car', 40, INK, kk * dim, w='Bold', bg=CARD)
        else:
            c.rr(x - 200, 420, x + 60, 640, 14, (40, 70, 110), kk * dim, bg=CARD)          # a window, cool room
            c.line([(x - 70, 420), (x - 70, 640)], CARD, 8, kk * dim, (40, 70, 110))
            c.line([(x - 200, 530), (x + 60, 530)], CARD, 8, kk * dim, (40, 70, 110))
            phone(c, x + 180, 540, 110, kk * dim, level=.4, bg=CARD, label=False)
            thermo(c, x - 260, 600, 150, .35, CY, kk * dim, CARD)
            c.text(x, 720, '40% in a cool room', 40, INK, kk * dim, w='Bold', bg=CARD)
        if ans > 0 and bad:
            pill(c, x + 200, 350, 'WEARS FASTER', PK, ans, 28, bg=CARD, h=54)
    if T(2) > 0 and ans < 1:
        p = clamp(T(2) / 2.0)
        ring(c, 960, 535, 60, 1 - p, CY, fd(T(2)) * (1 - ans))
        c.text(960, 535, 'or', 40, DIM, fd(T(2)) * (1 - ans), w='Bold')
    if ans > 0:
        c.text(960, 840, 'heat + full charge speed up the crust-building reactions', 36, YE, fd(T(3), 1.5), w='Bold')

def s_numbers(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'After one year in storage', 64, INK, hl(0), w='Bold')
    c.text(960, 210, 'capacity left, typical lithium-ion (estimates)', 34, DIM, hl(0) * fd(T(0), .5), w='Medium')
    rows = [('25°C, 40% charge', .96, GR, 1), ('40°C, fully charged', .65, PK, 2)]
    for j, (lab, v, col, li) in enumerate(rows):
        kk = hl(0) * fd(T(0), 1.0 + j * .5)
        if kk <= 0: continue
        y = 380 + j * 220
        thermo(c, 330, y + 10, 110, (.4, .85)[j], (CY, PK)[j], kk)
        c.text(420, y - 60, lab, 42, INK, kk, 'lm', 'Bold')
        c.rr(420, y - 20, 1500, y + 50, 18, (40, 46, 84), kk)
        if T(li) > 0: c.rr(420, y - 20, 420 + max(40, 1080 * v * fd(T(li), .3, 1.2)), y + 50, 18, col, kk)
        c.text(1530, y + 15, f'{int(v * 100)}%' if T(li) > 0 else '?', 60, col if T(li) > 0 else DIM, kk * (fd(T(li), 1.2) if T(li) > 0 else 1), 'lm', 'Bold')
    c.text(960, 840, 'Source: Battery University, BU-808', 28, DIM, hl(1), w='Medium')

def s_tips(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 140, 'What actually helps', 66, INK, hl(0), w='Bold')
    tips = [(1, 'Keep it out of the heat', 'avoid using or charging above 35°C', PK),
            (2, "Don't sit at 100% for hours", "use your phone's optimised charging", YE),
            (3, 'Small top-ups are fine', 'partial charges are gentler', GR)]
    for j, (li, title, sub, col) in enumerate(tips):
        k = hl(li); up = 24 * (1 - k)
        if k <= 0: continue
        x = 400 + j * 560
        c.rr(x - 260, 260 + up, x + 260, 800 + up, 30, CARD, k, outline=col, ow=5)
        y = 460 + up
        if j == 0:
            sun(c, x - 40, y, 60, k, t, CARD)
            phone(c, x + 90, y + 30, 90, k, level=.8, bg=CARD, label=False)
            c.cross(x + 150, y - 70, 70, PK, k)
        elif j == 1:
            phone(c, x - 60, y, 120, k, level=1.0, bg=CARD, label=False)
            c.circ(x + 120, y, 62, None, k, outline=YE, ow=8, bg=CARD)
            u = t * 1.2
            c.line([(x + 120, y), (x + 120 + 44 * math.sin(u), y - 44 * math.cos(u))], YE, 7, k, CARD)
            c.line([(x + 120, y), (x + 120, y - 30)], YE, 7, k, CARD)
            c.circ(x + 120, y, 8, YE, k, bg=CARD)
        else:
            for q, lv in enumerate((.5, .6, .7)):
                phone(c, x - 120 + q * 120, y, 80, k * (.5 + .5 * (q == int(t * 1.2) % 3)), level=lv, bg=CARD, label=False)
        c.text(x, 660 + up, title, 34, col, k, w='Bold', bg=CARD)
        c.text(x, 720 + up, sub, 26, INK, k, w='Medium', bg=CARD)

REC = [('1', 'Ions shuttle in and out', CY), ('2', 'The crust traps some lithium', CRUST), ('3', 'Heat + 100% speed it up', PK)]
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
            q = .5 + .5 * math.sin(t * 2)
            for j in range(4):
                xx = x - 140 + 280 * ease(clamp(q * 1.4 - j * .12))
                c.circ(xx, y - 70 + j * 45, 15, ION, m, bg=CARD)
            c.rr(x - 200, y - 110, x - 170, y + 90, 8, CATH, m, bg=CARD); c.rr(x + 170, y - 110, x + 200, y + 90, 8, GRAPH, m, bg=CARD)
        elif i == 1:
            c.rr(x - 60, y - 110, x + 60, y + 90, 12, GRAPH, m, bg=CARD)
            c.rr(x - 90, y - 110, x - 55, y + 90, 8, CRUST, m, bg=CARD)
            for j in range(4): c.circ(x - 72, y - 80 + j * 50, 13, TRAP, m, bg=CRUST)
        else:
            sun(c, x - 70, y - 20, 50, m, t, CARD)
            phone(c, x + 100, y, 90, m, level=1.0, bg=CARD, label=False)
        c.text(x, 740 + up, lab, 32, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Your phone battery is sealed shut. Nothing leaks out.",
            "Yet every year, a full charge lasts a little less.",
            "So where does that charge go? The answer is hiding inside."], s_hook),
 ('1  ·  INSIDE', ["Inside are two layers, with a liquid between them.",
            "When you charge, tiny lithium ions travel across and park in the graphite, like cars pulling into a garage.",
            "When you use your phone, they drive back across, and that flow powers your screen.",
            "The more ions that can make the trip, the more battery you have."], s_inside),
 ('2  ·  THE CRUST', ["Here's the catch. The liquid reacts with the graphite and forms a thin crust.",
            "Scientists call it the solid electrolyte interphase. It works like a filter. Ions pass, and the liquid is kept off.",
            "But building that crust uses up lithium. And it keeps growing, slowly, while you charge and even while the phone just sits."], s_crust),
 ('3  ·  TRAPPED', ["Every ion locked in the crust is a car that can never leave the garage.",
            "It's still inside the battery. It just can't carry charge any more.",
            "Battery researchers say losing these moving lithium ions is the main cause of capacity fade."], s_trapped),
 ('4  ·  CYCLES', ["Phone makers count this wear in charge cycles.",
            "One cycle means using 100 percent in total. Use 75 percent today and 25 percent tomorrow, and that's one cycle.",
            "Apple says older iPhones keep about 80 percent of their capacity after 500 full cycles. iPhone 15 models, after one thousand."], s_cycles),
 ('5  ·  QUICK QUESTION', ["Quick question. Which battery wears out faster?",
            "A phone left at 100 percent in a hot car? Or one sitting at 40 percent in a cool room?",
            "Three, two, one.",
            "The hot, full one. Heat and a full charge both speed up the reactions that build the crust."], s_quiz),
 ('6  ·  THE NUMBERS', ["Battery University estimates how much capacity a typical lithium-ion battery keeps after a year in storage.",
            "At 25 degrees and 40 percent charge, about 96 percent.",
            "At 40 degrees and fully charged, only about 65 percent."], s_numbers),
 ('7  ·  WHAT HELPS', ["So what can you do?",
            "Keep your phone out of the heat. Apple advises against using or charging it above 35 degrees.",
            "Don't leave it sitting at 100 percent for hours. Many phones have a setting that cuts the time spent fully charged. Turn it on.",
            "And small top-ups are fine. Partial charges are gentler than full ones."], s_tips),
 ('RECAP', ["So remember three things.",
            "One. Charging and using your phone moves lithium ions back and forth.",
            "Two. A thin crust slowly traps some of them, and trapped ions can't carry charge.",
            "Three. Heat and long hours at 100 percent speed that up.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story (hook -> core idea -> payoff), 40-58 s.
SHORT_SCENES = [
 ('THE PUZZLE', ["Your phone battery is sealed. Nothing leaks out.",
                 "Yet every year it holds less.",
                 "So where does the charge go?"], s_hook),
 ('INSIDE', ["Inside, lithium ions carry the charge.",
             "Charging parks them in graphite, like cars in a garage.",
             "Using the phone sends them back.",
             "More ions making the trip means more battery."], s_inside),
 ('THE CRUST', ["But a thin crust grows on the graphite.",
                "It's a useful filter, yet building it uses up lithium.",
                "And it keeps growing, slowly, over time."], s_crust),
 ('THE ANSWER', ["So nothing leaks out. The lithium gets trapped in the crust, where it can't carry charge.",
                 "Heat and long hours at 100 percent make it worse. Follow for more."],
                card('The lithium gets trapped', 'Keep it cool, not always 100%')),
]
SHORT_HITS = [(3, 0, 0.0)]
