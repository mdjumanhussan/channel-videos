"""Story 13: Yusuf, part 3 of 3: the king's dream and the reunion. Sources: Quran 12:43-101 (Saheeh International).
No people are drawn: no Yusuf, no king, no brothers, no father. Only Egypt, a columned hall, the king's dream as symbols
(cows on the horizon, ears of grain), a prison window, grain storehouses, camels of a caravan, a tent at night, the old
well, a plain shirt, and the eleven stars, the sun and the moon (the dream of 12:4, now fulfilled, 12:100).
Facts used and where they are: the king saw seven fat cows eaten by seven lean, and seven green ears and others dry
(12:43); the freed man remembered Yusuf and went to him in prison (12:45-46); Yusuf explained: seven years of planting,
then seven difficult years (12:47-48); Yusuf asked to be put over the storehouses of the land and Allah established him
(12:55-56); his brothers came, he knew them and they did not know him (12:58); their father grieved for Yusuf until his
eyes became white (12:84) and told his sons "despair not of relief from Allah" (12:87); they came back asking for
charity (12:88); he asked "Do you know what you did with Joseph...?" (12:89); they said "Are you indeed Joseph?" and he
said "I am Joseph" (12:90); "No blame will there be upon you today. Allah will forgive you" (12:92); his shirt was cast
over his father's face and he could see again (12:93, 12:96); the family came to Egypt (12:99) and Yusuf said "O my
father, this is the explanation of my vision of before. My Lord has made it reality" (12:100).
Not used: the women who cut their hands (12:50-51), the hidden bowl and the brother kept behind (12:69-82), the
prostration scene itself (12:100, first part), 12:53. The father is not named here, so no second "peace be upon him"
is needed; the Quran names no brother. The king is not named.
Improvement tried today: a payoff-first ending that closes the series. The hook question ("What would he say?") is
answered at the peak (12:92, deep hit), and the last story scene returns to Part 1's opening picture: the eleven stars,
the sun and the moon in one arc, now over Egypt at dawn, while 12:100 says the dream came true (second deep hit). Lesson
and end card are kept short so the payoff sits in the final seconds. Source: Daivid's study of 5,000 creator posts
(content that builds to a satisfying payoff got 110% more organic views; the last three seconds drive shares and
follows), via https://click2view.substack.com/p/the-hook-is-overrated . Also kept: plain headline = spoken hook with
caption hidden, series pill, open question, second loop (12:87), 0.5 s pause before the reveal, speed 1.1, lesson card,
CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  13'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = "Yusuf, Part 3: The King's Dream and the Reunion"
HITS = [(6, 1, 0.0), (8, 1, 0.0)]
# "no blame", taken straight from the text of 12:92
TITLE_AR = ' '.join(quran()['verses']['12:92']['ar'].split()[1:3])

# ---------------------------------------------------------------- small scenery helpers for this story
def camel(p, cx, base, s=1.0, col=(30, 20, 14), flip=False):
    """A camel, side view, standing at (cx, base). An animal only (copied from episode 11)."""
    k = -1 if flip else 1
    def X(dx): return cx + k * dx * s
    def Y(dy): return base + dy * s
    for lx, ph in ((-105, 0), (-70, 1), (80, 0), (110, 1)):
        sh = lc(col, (0, 0, 0), .25) if ph else col
        p.line([(X(lx), Y(-240)), (X(lx + 6), Y(-120))], sh, 20 * s); p.line([(X(lx + 6), Y(-120)), (X(lx), Y(-6))], sh, 14 * s)
        p.ell(X(lx + 6), Y(-120), 11 * s, 12 * s, sh); p.ell(X(lx + 8), Y(-4), 16 * s, 7 * s, sh)
    p.ell(X(-5), Y(-268), 160 * s, 66 * s, col)
    p.poly([(X(-150), Y(-290)), (X(-150), Y(-250)), (X(-110), Y(-200)), (X(-60), Y(-230))], col)
    p.ell(X(-15), Y(-322), 88 * s, 64 * s, col)
    p.line([(X(-160), Y(-290)), (X(-178), Y(-230)), (X(-172), Y(-190))], col, 8 * s)
    p.poly([(X(105), Y(-315)), (X(155), Y(-235)), (X(205), Y(-300)), (X(235), Y(-400)), (X(205), Y(-415)), (X(180), Y(-330)), (X(130), Y(-300))], col)
    p.ell(X(240), Y(-418), 44 * s, 22 * s, col); p.ell(X(278), Y(-408), 18 * s, 14 * s, col)
    p.poly([(X(215), Y(-434)), (X(210), Y(-458)), (X(226), Y(-438))], col)

def cow(p, cx, base, s=1.0, col=(30, 20, 30), thin=False):
    """A simple cow silhouette, side view (the king's dream, 12:43). An animal only. thin=True: bony and narrow."""
    bh = 46 if thin else 78; bw = 120 if thin else 140
    for lx in (-95, -70, 75, 100):
        p.line([(cx + lx * s, base - 120 * s), (cx + lx * s, base)], col, (9 if thin else 15) * s)
    p.ell(cx, base - 150 * s, bw * s, bh * s, col)
    if thin:
        for k in range(-2, 3): p.line([(cx + k * 26 * s, base - 186 * s), (cx + k * 26 * s, base - 120 * s)], lc(col, (255, 255, 255), .12), 3 * s)
    p.poly([(cx + 120 * s, base - 190 * s), (cx + 170 * s, base - 200 * s), (cx + 205 * s, base - 150 * s), (cx + 175 * s, base - 130 * s), (cx + 120 * s, base - 150 * s)], col)
    p.line([(cx + 160 * s, base - 205 * s), (cx + 150 * s, base - 235 * s)], col, 6 * s)
    p.line([(cx + 178 * s, base - 200 * s), (cx + 190 * s, base - 230 * s)], col, 6 * s)
    p.line([(cx - bw * s, base - 160 * s), (cx - bw * s - 25 * s, base - 80 * s)], col, 5 * s)

def grain_ear(p, x, base, h, col, lean=0.0, dry=False):
    """One stalk of grain with its ear of seeds (12:43). dry=True: bent, pale, thin."""
    tx = x + lean * h
    p.line([(x, base), (x + lean * h * .5, base - h * .6), (tx, base - h)], lc(col, (0, 0, 0), .2), 5)
    n = 6 if dry else 9
    for k in range(n):
        yy = base - h + k * 18; r = 9 if dry else 13
        for side in (-1, 1):
            p.ell(tx + side * (r * .9), yy + 4, r * .7, r * 1.25, col)
    if not dry: p.line([(x, base - h * .4), (x + 70 * (1 if lean >= 0 else -1), base - h * .55)], lc(col, (0, 0, 0), .1), 5)

def barred_window(p, cx, cy, w, h, sky_col=(150, 180, 230), bars=4, frame=(30, 26, 30)):
    """A small high window with iron bars (copied from episode 12)."""
    for x0, y0, x1, y1 in ((cx - w / 2 - 24, cy - h / 2 - 24, cx + w / 2 + 24, cy - h / 2), (cx - w / 2 - 24, cy + h / 2, cx + w / 2 + 24, cy + h / 2 + 24),
                           (cx - w / 2 - 24, cy - h / 2, cx - w / 2, cy + h / 2), (cx + w / 2, cy - h / 2, cx + w / 2 + 24, cy + h / 2)):
        p.rect(x0, y0, x1, y1, frame)
    if sky_col: p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, sky_col)
    for k in range(1, bars + 1):
        x = cx - w / 2 + k * w / (bars + 1); p.line([(x, cy - h / 2), (x, cy + h / 2)], (24, 22, 26), 14)
    p.line([(cx - w / 2, cy), (cx + w / 2, cy)], (24, 22, 26), 12)

def stone_wall(p, y0, y1, col=(70, 62, 66), seed=1, rows=11):
    """A rough wall of stone blocks filling the band y0..y1 (copied from episode 12)."""
    rnd = random.Random(seed); h = (y1 - y0) / rows
    p.rect(-100, y0, 1200, y1, lc(col, (0, 0, 0), .45))
    for r in range(rows):
        x = -100 - rnd.uniform(0, 120); y = y0 + r * h
        while x < 1200:
            w = rnd.uniform(130, 230); c = lc(col, (0, 0, 0) if rnd.random() < .5 else (255, 255, 255), rnd.uniform(0, .14))
            p.rect(x + 4, y + 4, x + w - 4, y + h - 4, c)
            x += w

def storehouse(p, cx, base, s, col=(200, 160, 110)):
    """A domed mud-brick grain store with a small dark opening (12:55). A building only."""
    shade = lc(col, (0, 0, 0), .3)
    p.rect(cx - 110 * s, base - 170 * s, cx + 110 * s, base, col)
    p.ell(cx, base - 170 * s, 110 * s, 120 * s, col)
    p.ell(cx + 40 * s, base - 200 * s, 40 * s, 70 * s, lc(col, (255, 255, 255), .15))
    p.rect(cx + 70 * s, base - 170 * s, cx + 110 * s, base, shade, 120)
    p.rect(cx - 26 * s, base - 90 * s, cx + 26 * s, base, (50, 34, 22)); p.ell(cx, base - 90 * s, 26 * s, 20 * s, (50, 34, 22))

def sack(p, cx, base, s, col=(186, 150, 100)):
    """A tied grain sack."""
    p.ell(cx, base - 60 * s, 62 * s, 64 * s, col); p.poly([(cx - 22 * s, base - 120 * s), (cx + 22 * s, base - 120 * s), (cx + 10 * s, base - 140 * s), (cx - 10 * s, base - 140 * s)], col)
    p.line([(cx - 24 * s, base - 118 * s), (cx + 24 * s, base - 118 * s)], (90, 60, 34), 6 * s)
    p.ell(cx - 20 * s, base - 80 * s, 18 * s, 26 * s, lc(col, (255, 255, 255), .15))

def column_hall(p, col=(180, 140, 100), light=(255, 196, 120)):
    """A great hall of tall columns with warm lamps, an open doorway to the desert at the end. Architecture only."""
    p.sky([(0, (30, 18, 14)), (.5, (66, 40, 26)), (1, (20, 12, 8))])
    p.rect(360, 900, 720, 1500, (255, 190, 120)); p.glow(540, 1250, 520, (255, 170, 90), .7)
    dunes(p, 1400, 10, (230, 150, 90), (200, 120, 70), 5)
    p.rect(-100, 1500, 1200, 2300, (60, 38, 24))
    for k, (x, w) in enumerate(((60, 90), (250, 70), (830, 70), (1020, 90))):
        p.rect(x - w / 2, 560, x + w / 2, 1520 + k % 2 * 10, lc(col, (0, 0, 0), .2 + .1 * (k in (0, 3))))
        p.rect(x - w / 2 - 20, 520, x + w / 2 + 20, 570, lc(col, (255, 255, 255), .08))
        for j in range(5): p.line([(x - w / 2 + 12, 640 + j * 170), (x + w / 2 - 12, 640 + j * 170)], lc(col, (0, 0, 0), .45), 3)
    p.rect(-100, 380, 1200, 520, (44, 28, 20))
    for x in (160, 920): lantern(p, x, 760, .7, light)

def plain_shirt(p, cx, cy, s, col=(232, 222, 196)):
    """A plain long shirt held up in light, no tear, no stain (12:93). Object only."""
    body = [(cx - 120 * s, cy - 170 * s), (cx - 40 * s, cy - 190 * s), (cx, cy - 165 * s), (cx + 40 * s, cy - 190 * s), (cx + 120 * s, cy - 170 * s),
            (cx + 260 * s, cy - 90 * s), (cx + 220 * s, cy - 30 * s), (cx + 130 * s, cy - 80 * s), (cx + 140 * s, cy + 220 * s), (cx - 140 * s, cy + 220 * s),
            (cx - 130 * s, cy - 80 * s), (cx - 220 * s, cy - 30 * s), (cx - 260 * s, cy - 90 * s)]
    p.glow(cx, cy, 520 * s, (255, 240, 200), .55)
    p.poly(body, col)
    p.line([(cx - 40 * s, cy - 190 * s), (cx, cy - 165 * s), (cx + 40 * s, cy - 190 * s)], lc(col, (0, 0, 0), .25), 4 * s)
    for dx in (-60, 0, 60): p.line([(cx + dx * s, cy - 100 * s), (cx + dx * 1.2 * s, cy + 210 * s)], lc(col, (0, 0, 0), .1), 3 * s)

def tent(p, cx, base, s, col=(120, 84, 60), light=(255, 196, 110)):
    """A plain desert tent with lamplight in its open side (copied from episode 11)."""
    p.glow(cx, base - 120 * s, 360 * s, light, .45)
    p.poly([(cx - 300 * s, base), (cx - 230 * s, base - 200 * s), (cx, base - 250 * s), (cx + 230 * s, base - 200 * s), (cx + 300 * s, base)], col)
    for k in range(-2, 3): p.line([(cx + k * 110 * s, base - 240 * s + abs(k) * 18 * s), (cx + k * 130 * s, base)], lc(col, (0, 0, 0), .25), 3, 200)
    p.poly([(cx + 40 * s, base), (cx + 70 * s, base - 150 * s), (cx + 170 * s, base - 140 * s), (cx + 190 * s, base)], light)
    p.glow(cx + 115 * s, base - 70 * s, 120 * s, light, .6)

def dream_arc(p, cx, cy, r, star_col=(255, 250, 235)):
    """Eleven bright stars, the sun and the moon in one arc: the dream of 12:4, as in Part 1. Symbols only."""
    for i in range(11):
        a = math.radians(200 + i * 14); x = cx - r * math.cos(a); y = cy + r * math.sin(a)
        p.glow(x, y, 70, (255, 240, 200), .9); p.ell(x, y, 9, 9, star_col)
    sun(p, cx - 140, cy - 60, 62, (255, 214, 140)); p.glow(cx - 140, cy - 60, 300, (255, 170, 80), .6)
    moon(p, cx + 150, cy - 60, 50, crescent=False, col=(214, 226, 255)); p.glow(cx + 150, cy - 60, 260, (200, 215, 255), .5)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hall_bg(p): column_hall(p)
def hall_near(p):
    for x, s in ((470, .9), (600, 1.0), (540, .7)): sack(p, x, 1500, s)

def kdream_sky(p):
    p.sky([(0, (24, 10, 44)), (.5, (70, 36, 96)), (.78, (170, 90, 120)), (1, (30, 16, 30))])
    stars(p, 140, 21, 1000, (230, 210, 255))
def kdream_mid(p):
    dunes(p, 1320, 12, (60, 30, 60), (30, 14, 30), 22)
    for i in range(7): cow(p, 50 + i * 148, 1340, .4, (156, 104, 112))                      # seven fat (back row)
    dunes(p, 1450, 10, (44, 22, 46), (24, 10, 26), 24)
    for i in range(7): cow(p, 80 + i * 148, 1480, .4, (120, 98, 108), thin=True)           # seven lean (front row)
def kdream_near(p):
    p.rect(-100, 1560, 1200, 2300, (20, 10, 22))
    for i in range(7): grain_ear(p, 120 + i * 50, 1800, 260 + (i % 2) * 30, (120, 190, 80), -.05 + i * .01)
    for i in range(7): grain_ear(p, 640 + i * 50, 1800, 200 + (i % 2) * 20, (190, 170, 120), .2 + i * .02, dry=True)

def prison_sky(p):
    p.sky([(0, (14, 14, 20)), (1, (6, 6, 10))])
    stone_wall(p, -200, 2300, (70, 62, 66), 31, 26)
    p.rect(360, 620, 720, 900, (255, 200, 120))
    for i in range(6): grain_ear(p, 380 + i * 62, 900, 150, (230, 180, 70), .02 * i)
    barred_window(p, 540, 760, 360, 280, None)
    p.glow(540, 760, 520, (255, 210, 140), .55)
def prison_light(p):
    def b(q):
        q.poly([(380, 900), (700, 900), (900, 1700), (180, 1700)], (255, 220, 160), 50); q.ell(540, 1700, 380, 90, (255, 220, 160), 80)
    p.blur_shape(b, 18)

def store_sky(p):
    p.sky([(0, (120, 70, 50)), (.5, (220, 140, 80)), (.8, (250, 196, 120)), (1, (150, 96, 60))])
    sun(p, 820, 820, 70, (255, 230, 170))
def store_mid(p):
    dunes(p, 1260, 18, (200, 140, 90), (160, 104, 64), 41)
    for x, s in ((210, .55), (380, .5)): camel(p, x, 1270, s, (70, 40, 26))
def store_near(p):
    p.rect(-100, 1460, 1200, 2300, (150, 104, 64))
    for x, s in ((330, 1.0), (620, 1.15), (900, .95)): storehouse(p, x, 1520, s)
    for x in (470, 760): sack(p, x, 1540, .8)

def tent_sky(p):
    p.sky([(0, (4, 6, 22)), (.55, (16, 20, 54)), (.85, (34, 34, 70)), (1, (10, 10, 20))])
    stars(p, 220, 51, 1250, (210, 220, 255)); moon(p, 820, 340, 44)
def tent_mid(p): dunes(p, 1340, 14, (28, 26, 46), (10, 10, 20), 52)
def tent_near(p): tent(p, 540, 1500, .95, (64, 50, 48), (230, 170, 100))

def well_sky(p):
    p.sky([(0, (6, 8, 20)), (.6, (22, 24, 50)), (1, (8, 8, 16))])
    stars(p, 160, 61, 1100)
def well_mid(p): dunes(p, 1360, 20, (40, 34, 50), (16, 14, 22), 62)
def well_near(p):
    dunes(p, 1500, 10, (30, 24, 30), (12, 10, 14), 63)
    well(p, 540, 1480, 1.25, (90, 76, 70))
    wood = (50, 34, 22)
    p.line([(540 - 168, 1480 - 140), (540 - 150, 1480 - 410)], wood, 20); p.line([(540 + 168, 1480 - 140), (540 + 150, 1480 - 410)], wood, 20)
    p.line([(540 - 185, 1480 - 410), (540 + 185, 1480 - 410)], wood, 22)

def dawn_bg(p):
    column_hall(p, (200, 160, 120), (255, 220, 160))
def dawn_rays(p):
    rays(p, 540, 1150, (255, 230, 170), n=11, spread=80, length=1800, width=7, a=.3, angle=-90)
    p.glow(540, 1150, 380, (255, 240, 200), .7)

def shirt_sky(p):
    p.sky([(0, (40, 60, 110)), (.45, (150, 150, 190)), (.72, (255, 206, 150)), (1, (130, 90, 64))])
    sun(p, 540, 1420, 80, (255, 236, 190))
def shirt_mid(p): dunes(p, 1360, 16, (200, 150, 110), (150, 106, 76), 81)
def shirt_near(p): plain_shirt(p, 540, 1450, 1.0)

def fulfil_sky(p):
    p.sky([(0, (10, 14, 46)), (.45, (50, 50, 110)), (.72, (220, 140, 110)), (.86, (255, 196, 130)), (1, (90, 56, 40))])
    stars(p, 120, 91, 900, (220, 220, 255))
def fulfil_mid(p): dream_arc(p, 540, 1080, 420)
def fulfil_near(p):
    pyramids(p, 1430, (150, 90, 70), (100, 56, 44))
    for x in (90, 1000): palm(p, x, 1560, 380, (40, 26, 20), .08 if x > 500 else -.08)
    p.rect(-100, 1550, 1200, 2300, (80, 50, 34))

def lesson_sky(p):
    p.sky([(0, (60, 90, 150)), (.45, (170, 180, 210)), (.72, (255, 214, 160)), (1, (150, 104, 70))])
    sun(p, 540, 1260, 70, (255, 236, 190))
def lesson_mid(p):
    dunes(p, 1340, 20, (210, 170, 120), (170, 130, 90), 101)
    for x, h in ((200, 420), (330, 340), (800, 400), (930, 330)): palm(p, x, 1460, h, (70, 80, 40), .06 if x > 500 else -.06)
def lesson_near(p):
    p.ell(540, 1520, 380, 70, (90, 150, 180)); p.ell(540, 1510, 330, 50, (150, 200, 220))   # an oasis pool
    p.rect(-100, 1560, 1200, 2300, (150, 110, 70))

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 121, 900); moon(p, 820, 300, 56)
def end_mid(p): pyramids(p, 1330, (60, 46, 64), (40, 30, 46))
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hall_bg, hall_near], fx=['dust'], cam='in', bloom=.65,
         title=dict(text='His brothers stood before him. What would he say?', arabic=TITLE_AR, part='Yusuf · Part 3 of 3', hold=99, plain=True),
         no_caption=(0,),
         lines=['His brothers stood before him. What would he say?']),
    dict(layers=[kdream_sky, kdream_mid, kdream_near], fx=['twinkle'], cam='in',
         lines=['The king of Egypt dreamed:', 'seven fat cows, eaten by seven lean.']),
    dict(layers=[prison_sky, prison_light], fx=['dust'], cam='in',
         lines=['From prison, Yusuf, peace be upon him, explained:', 'seven good years, then seven hard years.']),
    dict(layers=[store_sky, store_mid, store_near], fx=['sand'], cam='right',
         lines=["Soon he was put over the land's storehouses.", 'His brothers came for food. He knew them. They did not know him.']),
    dict(layers=[tent_sky, tent_mid, tent_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='12:87', ar=(6, 11), en='despair not of relief from Allah', line=2, ar_size=90, y=620),
         lines=['Their father grieved for Yusuf until his eyes turned white.', 'He told his sons:', 'despair not of relief from Allah.']),
    dict(layers=[well_sky, well_mid, well_near], fx=['dust'], cam='in', pause=0.5,
         lines=['Then he asked them: Do you know what you did with Yusuf?', 'They said: Are you indeed Yusuf?']),
    dict(layers=[dawn_bg, dawn_rays], fx=['dust'], cam='in', bloom=.75,
         verse=dict(key='12:92', ar=(1, 8), en='No blame will there be upon you today. Allah will forgive you', line=1, ar_size=84, y=620),
         lines=['He said: I am Yusuf.', 'No blame will there be upon you today. Allah will forgive you.']),
    dict(layers=[shirt_sky, shirt_mid, shirt_near], fx=['dust'], cam='in',
         lines=["His shirt was cast over his father's face. His sight returned."]),
    dict(layers=[fulfil_sky, fulfil_mid, fulfil_near], fx=['twinkle'], cam='out', bloom=.75,
         verse=dict(key='12:100', ar=(8, 18), en='O my father, this is the explanation of my vision of before. My Lord has made it reality', line=1, ar_size=70, y=560),
         lines=['His family came to Egypt. Yusuf said:', 'O my father, this is the explanation of my vision of before. My Lord has made it reality.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out',
         lesson=dict(text='Forgive. And never despair of Allah.', after=0, y=560), no_caption=(0,),
         lines=['Forgive. And never despair of Allah.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who needs hope. And follow for a new story from the Quran every day.']),
]

PRON = {'Yusuf': 'jˈuːsʊf', "Yusuf's": 'jˈuːsʊfs'}

CAPTION = """His brothers stood before him. What would he say? 🤍 (Yusuf, Part 3 of 3)

The king of Egypt dreamed of seven fat cows eaten by seven lean ones. From prison, Yusuf (peace be upon him) explained it: seven good years, then seven hard years. He was put over the storehouses of the land.

His brothers came for food. He knew them, but they did not know him. Their father grieved until his eyes turned white, yet he said: "despair not of relief from Allah." (Quran 12:87)

When Yusuf told them who he was, he said: "No blame will there be upon you today. Allah will forgive you." (Quran 12:92)

His shirt was cast over his father's face, and his sight returned. Then Yusuf said: "O my father, this is the explanation of my vision of before. My Lord has made it reality." (Quran 12:100)

Forgive, and never despair of Allah.

📖 Sources: Quran 12:43–101 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetYusuf #IslamicReminder"""

FIRST_COMMENT = """What touched you most in Yusuf's story: the well, the prison, or "No blame upon you today"? 🤍

References: Quran, Surah Yusuf 12:43–101 (Saheeh International translation). The full story: Parts 1, 2 and 3 on our page."""
