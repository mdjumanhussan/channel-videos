"""Episode: A Year Isn't 365 Days (why leap years exist, why 1900 wasn't one, and how close the calendar is now)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why Leap Years Exist'                          # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Why does February get a 29th?'                  # headline on the vertical Short
HITS = [(1, 1, 0.0), (5, 0, 0.0), (6, 1, 0.3)]                # 365 and a quarter, "No, it wasn't", the century rule
THUMB = ["A YEAR ISN'T", '365 DAYS']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.3, (1, 1): 0.4, (2, 3): 0.3, (4, 0): 3.4, (5, 0): 0.5, (6, 1): 0.4}
SHORT_PAUSES = {(0, 0): 0.2}
CAPTION_FIXES = {'three hundred and sixty-five and a quarter': '365 and a quarter', 'three hundred and sixty-five': '365',
                 'twenty-four days': '24 days', 'March the twentieth': 'March 20', 'April the thirteenth': 'April 13',
                 'seven hundred and fifty': '750', 'February the twenty-ninth': 'February 29', 'forty-six BC': '46 BC',
                 'nineteen hundred': '1900', 'Nineteen hundred': '1900', 'Two thousand': '2000', 'Twenty-one hundred': '2100', 'fifteen eighty-two': '1582', 'October the fourth': 'October 4',
                 'October the fifteenth': 'October 15', 'seventeen hundred': '1700', 'eighteen hundred': '1800',
                 'two thousand': '2000', 'twenty-one hundred': '2100', 'four hundred': '400', 'one hundred': '100',
                 'three thousand': '3,000', 'twenty twenty-eight': '2028', 'eleven minutes': '11 minutes'}
CAPTION_FIXES = dict(sorted(CAPTION_FIXES.items(), key=lambda kv: -len(kv[0])))   # longest phrase first

# Colour code kept in every scene:
# Earth's real year is cyan, the calendar is yellow, drift and error are pink,
# the leap-day fix is green, the old Julian calendar is purple.
EARTH = CY; CAL = YE; ERR = PK; FIX = GR; OLD = PU
DARK = (20, 22, 38); QUIZ = (66, 42, 18); PAPER = (236, 238, 248); RED = (220, 70, 80)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    """3 to 7 word headline with one key word in colour (most mobile viewers watch muted)."""
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def page(c, x, y, a, top, big, s=1.0, band=RED, numcol=DARK, bg=BG, glow=0.0, gcol=FIX):
    """A tear-off calendar page: coloured band with the month, big number below. (x, y) is the centre."""
    if a <= .01: return
    w, h = 170 * s, 200 * s
    if glow > .01: c.rr(x - w - 14, y - h - 14, x + w + 14, y + h + 14, 34 * s, None, a * glow, outline=gcol, ow=6, bg=bg)
    c.rr(x - w, y - h, x + w, y + h, 26 * s, PAPER, a, bg=bg)
    c.rr(x - w, y - h, x + w, y - h + 100 * s, 26 * s, band, a, bg=PAPER)
    c.rr(x - w, y - h + 60 * s, x + w, y - h + 100 * s, 0, band, a, bg=PAPER)
    for k in (-1, 1): c.circ(x + k * w * .55, y - h, 14 * s, (60, 66, 100), a, bg=band)
    c.text(x, y - h + 52 * s, top, int(44 * s), INK, a, w='Bold', bg=band)
    c.text(x, y + 50 * s, big, int(150 * s), numcol, a, w='Bold', bg=PAPER)

def sun(c, x, y, r, a, t=0.0, bg=BG):
    if a <= .01: return
    for k in range(12):
        ang = 6.283 * k / 12 + t * .3
        c.line([(x + r * 1.25 * math.cos(ang), y + r * 1.25 * math.sin(ang)), (x + r * 1.6 * math.cos(ang), y + r * 1.6 * math.sin(ang))], CAL, 7, a, bg=bg)
    c.circ(x, y, r, CAL, a, bg=bg)

def snow(c, x, y, r, a, t=0.0, col=(200, 225, 255), bg=BG):
    if a <= .01: return
    for k in range(3):
        ang = math.pi * k / 3 + t * .2
        c.line([(x - r * math.cos(ang), y - r * math.sin(ang)), (x + r * math.cos(ang), y + r * math.sin(ang))], col, 8, a, bg=bg)
    c.circ(x, y, r * .18, col, a, bg=bg)

def earth(c, x, y, r, a, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, EARTH, a, bg=bg)
    c.circ(x - r * .3, y - r * .2, r * .35, GR, a * .9, bg=EARTH); c.circ(x + r * .35, y + r * .3, r * .25, GR, a * .9, bg=EARTH)

def pie(c, x, y, r, a, frac, col, bg=BG, start=-90):
    """A filled pie wedge (frac of a full circle)."""
    if a <= .01 or frac <= 0: return
    c.d.pieslice(((x - r) * c.k, (y - r) * c.k, (x + r) * c.k, (y + r) * c.k), start, start + 360 * frac, fill=mix(col, a, bg))

def arc(c, x, y, rx, ry, a0, a1, col, w, a, bg=BG, n=90):
    """An elliptical arc from angle a0 to a1 (radians)."""
    if a <= .01 or a1 <= a0: return
    pts = [(x + rx * math.cos(a0 + (a1 - a0) * k / n), y + ry * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
    c.line(pts, col, w, a, bg=bg)

def tile(c, x, y, txt, a, col, ok, p=1.0, bg=BG):
    """A year tile with a tick or a cross."""
    if a <= .01: return
    c.rr(x - 120, y - 70, x + 120, y + 70, 22, CARD, a, outline=col, ow=5, bg=bg)
    c.text(x, y, txt, 62, INK, a, w='Bold', bg=CARD)
    if p > .01:
        if ok: c.check(x + 100, y - 70, 34, FIX, a, p)
        else: c.cross(x + 100, y - 70, 50, ERR, a * p)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Frame one already carries the claim: a Christmas page and a season sign that keeps flipping (motion from t = 0)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Christmas in ', INK), ('winter', ERR), ('?', INK)], sw_out(T, 1))
    headline(c, [('The ', INK), ('calendar', CAL), (' slips', ERR)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Why February gets a ', INK), ('29th', FIX)], sw_in(T, 2), size=80)
    m = 1 - hl(2)
    page(c, 560, 540, m, 'DECEMBER', '25', 1.2)
    c.text(560, 820, 'Sydney', 40, EARTH, m, w='Bold')
    # the season under the same date keeps sliding: summer sun fades into snow and back
    sw = .5 + .5 * math.sin(t * 1.4 - 1.57)
    c.rr(1060, 330, 1560, 760, 30, CARD, m, outline=mix(CAL, 1 - sw) if sw < .5 else (200, 225, 255), ow=5)
    sun(c, 1310, 500, 70, m * (1 - sw), t, bg=CARD)
    snow(c, 1310, 500, 90, m * sw, t, bg=CARD)
    c.text(1310, 680, 'summer' if sw < .5 else 'winter', 52, CAL if sw < .5 else (200, 225, 255), m, w='Bold', bg=CARD)
    c.arrow(780, 540, 1030, 540, DIM, 5, m)
    m2 = hl(2)
    page(c, 960, 540, m2, 'FEBRUARY', '29', 1.3, glow=.6 + .4 * math.sin(t * 3))

def s_orbit(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('One year = ', INK), ('back to the same season', EARTH)], sw_out(T, 1), size=76)
    headline(c, [('About ', INK), ('365¼ days', EARTH)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Calendar: ', CAL), ('365', CAL), (' . Earth: ', INK), ('365¼', EARTH)], sw_in(T, 2), size=80)
    X, Y, RX, RY = 760, 540, 420, 250
    sun(c, X, Y, 60, 1, t)
    c.line([(X + RX * math.cos(k / 60 * 6.283), Y + RY * math.sin(k / 60 * 6.283)) for k in range(61)], (54, 62, 110), 4, 1)
    p = fd(T(0), .2, 3.0) if T(0) > -.1 else 0.0
    if T(1) > -.1: p = 1.0
    ang = -1.57 + 6.283 * p * (1 if T(2) < 0 else 1.0)
    # the calendar's year (yellow) closes a little before Earth's (cyan) once line 2 starts
    gap = .068 * fd(T(2), .3, 1.0) if T(2) > -.1 else 0.0
    arc(c, X, Y, RX + 30, RY + 30, -1.57, -1.57 + 6.283 * (p - gap), CAL, 10, 1)
    arc(c, X, Y, RX - 30, RY - 30, -1.57, -1.57 + 6.283 * p, EARTH, 10, 1)
    if gap > .001:
        arc(c, X, Y, RX + 30, RY + 30, -1.57 + 6.283 * (1 - gap), 4.71, ERR, 14, 1)
    earth(c, X + RX * math.cos(ang), Y + RY * math.sin(ang), 34, 1)
    c.text(X, Y + 110, 'Sun', 34, CAL, 1, w='Bold')
    m1 = hl(1)
    c.rr(1300, 330, 1800, 520, 26, CARD, m1, outline=EARTH, ow=4)
    c.text(1550, 390, "Earth's year", 36, DIM, m1, w='Bold', bg=CARD)
    c.text(1550, 460, '365.2422 days', 54, EARTH, m1, w='Bold', bg=CARD)
    m2 = hl(2)
    c.rr(1300, 560, 1800, 760, 26, CARD, m2, outline=ERR, ow=4)
    c.text(1550, 620, 'calendar ends', 36, DIM, m2, w='Bold', bg=CARD)
    c.text(1550, 690, 'almost 6 h early', 50, ERR, m2, w='Bold', bg=CARD)
    c.text(1550, 820, '0.2422 day = about 5 h 49 min', 28, DIM, m2, w='Regular')

def s_drift(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Six hours ', ERR), ('adds up', INK)], sw_out(T, 1))
    headline(c, [('4 years: ', INK), ('almost 1 day', ERR)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('100 years: ', INK), ('about 24 days', ERR)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('750 years: ', INK), ('seasons swap', ERR)], sw_in(T, 3))
    # lines 0-1: one quarter-day wedge per year, four of them almost fill a day
    m01 = 1 - hl(2)
    for k in range(4):
        x = 420 + k * 360; u = m01 * (1 if k == 0 else (fd(T(1), .3 + .5 * (k - 1)) if T(1) > -.1 else 0.0))
        c.circ(x, 500, 120, None, m01 * .7, outline=(60, 68, 110), ow=4)
        pie(c, x, 500, 116, u, .2422, ERR, start=-90 + 87.2 * k)
        c.text(x, 690, f'year {k + 1}', 40, INK, u, w='Bold')
    c.text(960, 800, 'each wedge: almost 6 hours the calendar misses', 32, DIM, m01, w='Bold')
    # line 2: the start of spring slides along a date strip
    m2 = hl(2) * (1 - hl(3))
    if m2 > .01:
        X0, X1, Y = 260, 1660, 560
        c.rr(X0, Y - 40, X1, Y + 40, 20, CARD, m2, outline=(60, 68, 110), ow=3)
        for d in range(0, 26):
            x = X0 + 40 + d * (X1 - X0 - 80) / 25
            c.line([(x, Y - 18), (x, Y + 18)], (80, 90, 140), 3, m2, bg=CARD)
        s = fd(T(2), 1.0, 2.4); x = X0 + 40 + s * 24 * (X1 - X0 - 80) / 25
        c.circ(x, Y, 34, GR, m2, bg=CARD)
        c.text(X0 + 40, Y + 90, 'March 20', 40, INK, m2, w='Bold'); c.text(X0 + 40 + 24 * (X1 - X0 - 80) / 25, Y + 90, 'April 13', 40, ERR, m2 * fd(T(2), 2.6), w='Bold')
        c.text(x, Y - 80, 'first day of spring', 34, GR, m2, w='Bold')
        c.text(960, 820, 'Northern Hemisphere, after 100 years with no leap days (US Naval Observatory)', 28, DIM, m2, w='Regular')
    m3 = hl(3)
    page(c, 640, 520, m3, 'DECEMBER', '25', 1.1)
    c.text(640, 790, 'Sydney', 38, EARTH, m3, w='Bold')
    f = fd(T(3), 1.2, 1.6)
    c.rr(1080, 330, 1560, 720, 30, CARD, m3, outline=(200, 225, 255), ow=5)
    sun(c, 1320, 500, 70, m3 * (1 - f), t, bg=CARD); snow(c, 1320, 500, 90, m3 * f, t, bg=CARD)
    c.text(1320, 660, 'winter', 52, (200, 225, 255), m3 * f, w='Bold', bg=CARD)
    c.text(960, 840, 'Half a year of drift: 0.2422 day x 750 years (our arithmetic)', 28, DIM, m3, w='Regular')

def s_leap(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('The fix: a ', INK), ('leap day', FIX)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Every 4th year: ', INK), ('Feb 29', FIX)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('4 quarters = ', ERR), ('1 day', FIX)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Julius Caesar, ', OLD), ('46 BC', INK)], sw_in(T, 3))
    m01 = 1 - hl(2)
    # a February grid: 28 days, and the 29th pops in on line 1
    X0, Y0, CW, CH = 560, 300, 116, 96
    c.rr(X0 - 20, Y0 - 20, X0 + 7 * CW + 4, Y0 + 5 * CH + 20, 24, CARD, m01, outline=CAL, ow=4)
    for d in range(29):
        col, row = d % 7, d // 7; x = X0 + col * CW + CW / 2 - 8; y = Y0 + row * CH + CH / 2
        if d < 28:
            c.text(x, y, str(d + 1), 40, INK, m01 * .9, w='Bold', bg=CARD)
        else:
            u = m01 * (fd(T(1), 1.0) if T(1) > -.1 else 0.0); pop = 1 + .25 * (1 - fd(T(1), 1.0, .6)) if T(1) > -.1 else 1
            c.circ(x, y, 42 * pop, FIX, u, bg=CARD); c.text(x, y, '29', 44, DARK, u, w='Bold', bg=FIX)
    # line 2: four quarter wedges join into one whole day
    m2 = hl(2) * (1 - hl(3))
    j = fd(T(2), .8, 1.6) if T(2) > -.1 else 0.0
    for k in range(4):
        ang = -math.pi / 4 + k * math.pi / 2
        dx, dy = 260 * (1 - j) * math.cos(ang), 200 * (1 - j) * math.sin(ang)
        pie(c, 960 + dx, 520 + dy, 150, m2, .25, ERR if j < .98 else FIX, start=-90 + 90 * k)
    c.text(960, 790, '= one extra day', 48, FIX, m2 * j, w='Bold')
    m3 = hl(3)
    page(c, 760, 530, m3, 'FEBRUARY', '29', 1.1, band=OLD)
    c.text(1300, 470, 'Julian calendar', 52, OLD, m3, w='Bold')
    c.text(1300, 540, 'a leap day', 44, INK, m3, w='Bold')
    c.text(1300, 600, 'every 4th year', 44, FIX, m3, w='Bold')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a warm amber pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Was ', INK), ('1900', CAL), (' a leap year?', INK)], 1, bg=QUIZ)
    c.text(700, 300, '1900 ÷ 4 = 475', 50, INK, fd(t, .4), w='Bold', bg=QUIZ)
    for k, txt in enumerate(('A  Yes', 'B  No')):
        u = fd(t, .8 + .3 * k)
        c.rr(330, 390 + k * 170, 1070, 510 + k * 170, 26, (96, 64, 30), u, outline=(170, 130, 80), ow=3, bg=QUIZ)
        c.text(380, 450 + k * 170, txt, 52, INK, u, 'lm', 'Bold', bg=(96, 64, 30))
    if T(0) > 0:
        e = T(0) - 5.0; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 4.8)
        c.circ(1450, 540, 96, CAL, u, bg=QUIZ); c.text(1450, 540, str(k) if k else '?', 88, DARK, u, w='Bold', bg=CAL)

def s_toomuch(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('No. ', ERR), ('1900 had no Feb 29', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('A quarter is ', INK), ('too much', ERR)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('1582: ', INK), ('10 days skipped', FIX)], sw_in(T, 2))
    m0 = hl(0) * (1 - hl(1))
    page(c, 960, 540, m0, 'FEB 1900', '29', 1.1)
    c.cross(960, 590, 220 * m0 + 1, ERR, m0)
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        X0, Y = 360, 440; L = 1200
        g = fd(T(1), .3, 1.0)
        c.rr(X0, Y - 50, X0 + L * g, Y + 50, 16, EARTH, m1)
        c.text(X0 - 20, Y, 'Earth', 40, EARTH, m1, 'rm', 'Bold')
        c.text(X0 + 30, Y, '0.2422 day', 40, DARK, m1 * g, 'lm', 'Bold', bg=EARTH)
        g2 = fd(T(1), 1.2, 1.0); L2 = L * .25 / .2422
        c.rr(X0, Y + 110, X0 + L2 * g2, Y + 210, 16, CAL, m1)
        c.text(X0 - 20, Y + 160, 'Leap rule', 40, CAL, m1, 'rm', 'Bold')
        c.text(X0 + 30, Y + 160, '0.25 day', 40, DARK, m1 * g2, 'lm', 'Bold', bg=CAL)
        e = fd(T(1), 2.4)
        c.rr(X0 + L, Y + 110, X0 + L2, Y + 210, 6, ERR, m1 * e)
        c.arrow(X0 + L + 18, Y + 330, X0 + L + 18, Y + 220, ERR, 5, m1 * e)
        c.text(X0 + L + 18, Y + 370, 'about 11 minutes a year too long', 40, ERR, m1 * e, 'rm', 'Bold')
    m2 = hl(2)
    page(c, 640, 520, m2, 'OCT 1582', '4', 1.0, numcol=DARK)
    c.text(640, 790, 'Thursday', 40, INK, m2, w='Bold')
    c.arrow(860, 520, 1060, 520, FIX, 7, m2 * fd(T(2), 1.0))
    page(c, 1280, 520, m2 * fd(T(2), 1.4), 'OCT 1582', '15', 1.0, glow=.8, gcol=FIX)
    c.text(1280, 790, 'Friday', 40, INK, m2 * fd(T(2), 1.4), w='Bold')
    c.text(960, 470, 'Gregorian calendar', 28, DIM, m2 * fd(T(2), 1.0), w='Regular')

def s_rule(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('The ', INK), ('century', CAL), (' rule', INK)], sw_out(T, 1))
    headline(c, [('÷100: no. ', ERR), ('Unless ÷400', FIX)], sw_in(T, 1) * sw_out(T, 3))
    headline(c, [('3 leap days ', ERR), ('dropped per 400 years', INK)], sw_in(T, 3), size=74)
    m0 = 1 - hl(2)
    steps = (('Divisible by 4?', 'leap year', FIX), ('Divisible by 100?', 'not a leap year', ERR), ('Divisible by 400?', 'leap year after all', FIX))
    for k, (q, a_, col) in enumerate(steps):
        u = m0 * (1 if k == 0 else (fd(T(1), .3 + 1.2 * (k - 1)) if T(1) > -.1 else 0.0))
        y = 330 + k * 175
        c.rr(360, y - 62, 1000, y + 62, 24, CARD, u, outline=CAL, ow=4)
        c.text(400, y, q, 46, INK, u, 'lm', 'Bold', bg=CARD)
        c.arrow(1020, y, 1180, y, col, 6, u)
        c.text(1210, y, a_, 46, col, u, 'lm', 'Bold')
    m2 = hl(2)
    for k, (yr, ok) in enumerate((('1700', 0), ('1800', 0), ('1900', 0), ('2000', 1), ('2100', 0))):
        x = 260 + k * 350; u = m2 * fd(T(2), .4 + .6 * k)
        tile(c, x, 520, yr, u, FIX if ok else ERR, ok, fd(T(2), .8 + .6 * k))
        c.text(x, 650, 'leap' if ok else 'no leap day', 36, FIX if ok else ERR, u, w='Bold')
    m3 = hl(3)
    c.text(960, 790, 'Leap years: 100 every 400 years becomes 97', 40, INK, m3, w='Bold')

def s_close(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Off by ', INK), ('under half a minute', FIX)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('1 day in ', INK), ('3,000+ years', FIX)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Next leap day: ', INK), ('29 Feb 2028', FIX)], sw_in(T, 2))
    m0 = hl(0) * (1 - hl(1))
    # a stopwatch: the hand sweeps less than half the dial
    X, Y, R = 960, 540, 230
    c.circ(X, Y, R, CARD, m0, outline=FIX, ow=8)
    c.rr(X - 30, Y - R - 50, X + 30, Y - R - 4, 8, FIX, m0)
    for k in range(60):
        ang = -1.57 + 6.283 * k / 60; r0 = R * (.82 if k % 5 == 0 else .9)
        c.line([(X + r0 * math.cos(ang), Y + r0 * math.sin(ang)), (X + R * .96 * math.cos(ang), Y + R * .96 * math.sin(ang))], DIM, 4, m0, bg=CARD)
    sweep = .43 * fd(T(0), .4, 2.2)
    pie(c, X, Y, R * .78, m0 * .5, sweep, FIX, bg=CARD)
    ang = -1.57 + 6.283 * sweep
    c.line([(X, Y), (X + R * .8 * math.cos(ang), Y + R * .8 * math.sin(ang))], INK, 8, m0, bg=CARD); c.circ(X, Y, 14, INK, m0, bg=CARD)
    c.text(X, 840, 'average calendar year 365.2425 vs Earth 365.2422 days', 30, DIM, m0, w='Regular')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        X0, X1, Y1 = 260, 1660, 540
        g = fd(T(1), .3, 2.4)
        c.line([(X0, Y1), (X1, Y1)], (70, 78, 120), 8, m1)
        c.line([(X0, Y1), (X0 + (X1 - X0) * g, Y1)], FIX, 10, m1)
        for k, lab in enumerate(('1582', '+1,000', '+2,000', '+3,000')):
            x = X0 + k * (X1 - X0) / 3.3; c.circ(x, Y1, 14, FIX if g * (X1 - X0) >= x - X0 else (70, 78, 120), m1)
            c.text(x, Y1 + 60, lab, 36, INK, m1, w='Bold')
        page(c, X1 - 40, Y1 - 200, m1 * fd(T(1), 2.4), '+1 DAY', '1', .6, band=ERR)
        c.text(960, 820, 'about 3,300 years (US Naval Observatory)', 30, DIM, m1, w='Regular')
    m2 = hl(2)
    page(c, 960, 520, m2, 'FEB 2028', '29', 1.3, glow=.6 + .4 * math.sin(t * 3))

def s_recap(c, T, t):
    """Recap as three tear-off calendar pages side by side (last recap used stacked rows)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', CAL)], 1)
    items = ((1, '365¼', 'days for Earth', 'to reach the same season', EARTH, (40, 110, 150)),
             (2, '+1', 'every 4 years', 'catches up the quarter', FIX, (40, 140, 90)),
             (3, '÷400', 'century rule', 'trims the overshoot', ERR, (170, 60, 100)))
    for ln, big, l1, l2, col, band in items:
        m = hl(ln); x = 400 + (ln - 1) * 560; dy = 50 * (1 - m)
        c.rr(x - 230, 290 + dy, x + 230, 790 + dy, 30, PAPER, m)
        c.rr(x - 230, 290 + dy, x + 230, 380 + dy, 30, band, m, bg=PAPER); c.rr(x - 230, 340 + dy, x + 230, 380 + dy, 0, band, m, bg=PAPER)
        c.text(x, 335 + dy, str(ln), 48, INK, m, w='Bold', bg=band)
        c.text(x, 510 + dy, big, 104, DARK, m, w='Bold', bg=PAPER)
        c.text(x, 650 + dy, l1, 40, DARK, m, w='Bold', bg=PAPER)
        c.text(x, 710 + dy, l2, 32, (70, 76, 110), m, w='Medium', bg=PAPER)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    page(c, 1520, 560, 1, 'FEBRUARY', '29', 1.35, glow=1)

SCENES = [
 ('THE SLIP', ["Without leap days, Christmas in Sydney would one day land in the middle of winter.",
               "Not because the weather changes. Because the calendar slips.",
               "Here's why February gets an extra day, and why even that isn't quite right."], s_hook),
 ('THE REAL YEAR', ["A year is the time Earth takes to go round the Sun and come back to the same season.",
                    "That isn't three hundred and sixty-five days. It's about three hundred and sixty-five and a quarter.",
                    "So a three hundred and sixty-five day calendar finishes almost six hours before Earth does."], s_orbit),
 ('THE DRIFT', ["Six hours a year doesn't sound like much. But it adds up.",
                "After four years, the calendar is almost a whole day behind.",
                "After a century, about twenty-four days. The first day of spring in the north would slide from March the twentieth to April the thirteenth.",
                "Keep going for about seven hundred and fifty years, and the seasons swap places. Christmas in Sydney, in winter."], s_drift),
 ('THE FIX', ["So we add a leap day.",
              "Every fourth year, the calendar gets one extra day, February the twenty-ninth.",
              "Four missing quarters make one whole day, so the calendar catches up with Earth.",
              "Julius Caesar's calendar used this rule from forty-six BC."], s_leap),
 ('QUICK QUESTION', ["Quick question. Was nineteen hundred a leap year? It divides by four. Have a guess."], s_quiz),
 ('THE ANSWER', ["No, it wasn't.",
                 "Adding a quarter of a day every year is slightly too much. The rule ran about eleven minutes long each year.",
                 "Over centuries, those minutes became days. So in fifteen eighty-two, the new Gregorian calendar skipped ten days.",
                 "Thursday, October the fourth, was followed by Friday, October the fifteenth."], s_toomuch),
 ('THE CENTURY RULE', ["It also added a rule for century years.",
                       "A year that divides by one hundred is not a leap year, unless it also divides by four hundred.",
                       "So seventeen hundred, eighteen hundred and nineteen hundred had no leap day. Two thousand did. Twenty-one hundred won't.",
                       "That drops three leap days every four hundred years."], s_rule),
 ('HOW CLOSE', ["Now the average calendar year is within about half a minute of Earth's year.",
                "It takes more than three thousand years for that to add up to a single day.",
                "And the next leap day? February the twenty-ninth, twenty twenty-eight."], s_close),
 ('RECAP', ["Three things to keep.",
            "One: Earth takes about three hundred and sixty-five and a quarter days to come back to the same season.",
            "Two: a leap day every four years catches up the missing quarter.",
            "Three: skipping most century years trims the small overshoot.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_claim(c, T, t):
    """Bold-claim hook with the claim on screen from frame one (lesson of 2026-11-22, Virlo)."""
    headline(c, [("A year isn't ", INK), ('365 days', ERR)], sw_out(T, 1), size=92)
    headline(c, [("It's about ", INK), ('365¼', EARTH)], sw_in(T, 1), size=92)
    X, Y, RX, RY = 960, 560, 520, 240
    sun(c, X, Y, 60, 1, t)
    c.line([(X + RX * math.cos(k / 60 * 6.283), Y + RY * math.sin(k / 60 * 6.283)) for k in range(61)], (54, 62, 110), 4, 1)
    p = (t * .22) % 1.0; ang = -1.57 + 6.283 * p
    arc(c, X, Y, RX - 30, RY - 30, -1.57, ang, EARTH, 10, 1)
    earth(c, X + RX * math.cos(ang), Y + RY * math.sin(ang), 34, 1)

def short_drift(c, T, t):
    headline(c, [('Almost ', INK), ('6 hours', ERR), (' short a year', INK)], sw_out(T, 1), size=80)
    headline(c, [('4 years: ', INK), ('almost 1 day', ERR)], sw_in(T, 1), size=84)
    for k in range(4):
        x = 420 + k * 360; u = 1 if k == 0 else (fd(T(1), .2 + .5 * (k - 1)) if T(1) > -.1 else 0.0)
        c.circ(x, 520, 120, None, .7, outline=(60, 68, 110), ow=4)
        pie(c, x, 520, 116, u, .2422, ERR, start=-90 + 87.2 * k)
        c.text(x, 710, f'year {k + 1}', 40, INK, u, w='Bold')

def short_leap(c, T, t):
    headline(c, [('So: ', INK), ('February 29', FIX)], 1, size=88)
    page(c, 960, 540, 1, 'FEBRUARY', '29', 1.3, glow=.6 + .4 * math.sin(t * 3))

def short_rule(c, T, t):
    headline(c, [('Most ', INK), ('century years', CAL), (' skip it', ERR)], sw_out(T, 1), size=80)
    headline(c, [('Unless ', INK), ('÷400', FIX)], sw_in(T, 1), size=88)
    for k, (yr, ok) in enumerate((('1900', 0), ('2000', 1), ('2100', 0))):
        x = 560 + k * 400; u = fd(T(1), .3 + .6 * k) if T(1) > -.1 else 0.0
        tile(c, x, 520, yr, fd(t, .3 + .3 * k), (FIX if ok else ERR) if u > .5 else CAL, ok, u)
        c.text(x, 650, 'leap' if ok else 'no leap day', 36, FIX if ok else ERR, u, w='Bold')

SHORT_SCENES = [
 ('THE CLAIM', ["A year isn't three hundred and sixty-five days.",
                "Earth takes about three hundred and sixty-five and a quarter to come back to the same season."], short_claim),
 ('THE DRIFT', ["So each year, the calendar ends almost six hours early.",
                "After four years, that's almost a whole day."], short_drift),
 ('THE FIX', ["So every fourth year, we add one day. February the twenty-ninth."], short_leap),
 ('THE CATCH', ["But a quarter day is a little too much. So most century years skip it.",
                "Nineteen hundred had no leap day. Two thousand did, because it divides by four hundred."], short_rule),
 ('THE ANSWER', ["That's why February gets a twenty-ninth.",
                 "It keeps the calendar in step with the seasons."], card('Feb 29 adds the missing quarter.', 'Seasons stay put.')),
]
SHORT_HITS = [(4, 0, 0.0)]
