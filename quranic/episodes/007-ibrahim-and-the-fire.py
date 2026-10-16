"""Story 7: Ibrahim and the fire that turned cool. Sources: Quran 21:66-70, 29:24, 37:97-98 (Saheeh International).
No people are drawn: night sky, a stone enclosure, stacked wood, fire, broken stone idols (plain pillars), lanterns, light only.
Nothing beyond the verses: no catapult, no garden in the fire, no names, no length of time, no dialogue that is not in the Quran.
Improvement tried today: open on action and a 2-second hook. The fire is LIVE from frame 1 (new engine fx 'flames':
flickering tongues redrawn every frame, with a still camera), and the first spoken sentence is 6 words (about 1.5 s).
Reason: average watch is stuck at 3-7 s; the first frame has always been a still painting with a slow zoom."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  7'
VOICE, SPEED = 'bm_george', 1.1
THUMB_AT = 1.0
TITLE = 'Ibrahim and the Fire: "Be Coolness and Safety"'
HITS = [(5, 1, 0.0)]
# "Burn him", taken straight from the text of 21:68
TITLE_AR = quran()['verses']['21:68']['ar'].split()[1]

# ---------------------------------------------------------------- small scenery helpers for this story
def stone_wall(p, x0, x1, base, h, col, seed):
    """A rough wall of cut stone blocks (the structure of 37:97)."""
    rnd = random.Random(seed); dk = lc(col, (0, 0, 0), .45); lt = lc(col, (255, 220, 180), .2)
    p.rect(x0, base - h, x1, base, col)
    rows = int(h // 70)
    for r in range(rows):
        y = base - (r + 1) * 70; off = 0 if r % 2 else 60; x = x0 - off
        p.line([(x0, y), (x1, y)], dk, 5, 200)
        while x < x1:
            bw = rnd.uniform(90, 150)
            if x > x0: p.line([(x, y), (x, y + 70)], dk, 5, 200)
            if min(x1, x + bw - 8) > max(x0, x + 8): p.rect(max(x0, x + 8), y + 6, min(x1, x + bw - 8), y + 14, lt, 90)
            x += bw
    p.rect(x0, base - h - 14, x1, base - h, lt)

def logs(p, cx, base, w, rows, col, seed):
    """Stacked firewood: round log ends in a pile."""
    rnd = random.Random(seed); dk = lc(col, (0, 0, 0), .5); rg = lc(col, (255, 210, 150), .35)
    for r in range(rows):
        n = rows - r + 3; y = base - 40 - r * 66
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * 74 + rnd.uniform(-6, 6)
            p.ell(x, y, 36, 33, dk); p.ell(x, y, 30, 27, col); p.ell(x, y, 16, 14, rg, 160); p.ell(x, y, 5, 5, dk)

def idol(p, cx, base, w, h, col):
    """A plain stone pillar idol, no face or limbs."""
    dk = lc(col, (0, 0, 0), .35); lt = lc(col, (255, 230, 190), .2)
    p.rect(cx - w * .7, base - h * .1, cx + w * .7, base, dk)
    p.poly([(cx - w / 2, base - h * .1), (cx - w * .4, base - h * .82), (cx + w * .4, base - h * .82), (cx + w / 2, base - h * .1)], col)
    p.rect(cx - w * .5, base - h * .88, cx + w * .5, base - h * .82, lt)
    p.poly([(cx - w * .4, base - h * .88), (cx, base - h), (cx + w * .4, base - h * .88)], col)

def rubble(p, cx, base, spread, col, seed, n=14):
    rnd = random.Random(seed); dk = lc(col, (0, 0, 0), .4); lt = lc(col, (255, 230, 190), .2)
    for i in range(n):
        x = cx + rnd.uniform(-spread, spread); y = base + rnd.uniform(-30, 40); s = rnd.uniform(18, 50)
        pts = [(x + s * math.cos(a) * rnd.uniform(.6, 1.2), y + s * .6 * math.sin(a) * rnd.uniform(.6, 1.2)) for a in [k * 2 * math.pi / 5 + rnd.uniform(0, .5) for k in range(5)]]
        p.ell(x, y + s * .5, s * 1.1, s * .25, (0, 0, 0), 90)
        p.poly(pts, dk if i % 3 == 0 else col); p.line(pts[:2], lt, 3, 180)

def coals(p, cx, base, w, col, seed):
    rnd = random.Random(seed)
    p.ell(cx, base, w * .6, 40, (20, 14, 12))
    for i in range(30):
        x = cx + rnd.uniform(-w * .5, w * .5); y = base + rnd.uniform(-20, 20)
        p.ell(x, y, rnd.uniform(10, 22), rnd.uniform(7, 12), col, int(rnd.uniform(120, 230)))

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (10, 4, 6)), (.5, (60, 14, 10)), (.8, (150, 50, 20)), (1, (40, 10, 6))])
    p.glow(540, 1300, 760, (255, 110, 30), .9)
def hook_mid(p):
    stone_wall(p, -100, 150, 1640, 760, (70, 40, 30), 1); stone_wall(p, 930, 1180, 1640, 760, (70, 40, 30), 2)
    p.glow(540, 1450, 520, (255, 170, 60), .8)
def hook_near(p):
    p.rect(-200, 1600, 1280, 2300, (24, 12, 8)); logs(p, 540, 1660, 0, 1, (90, 50, 26), 3)

def idols_sky(p):
    p.sky([(0, (8, 8, 26)), (.5, (30, 22, 50)), (.8, (90, 40, 50)), (1, (20, 10, 14))])
    stars(p, 90, 11, 800); moon(p, 820, 380, 46)
def idols_mid(p):
    city(p, 1380, (34, 22, 30), 12, lights=(255, 180, 100), domes=False)
    for x, h in ((300, 380), (780, 380)): idol(p, x, 1460, 80, h, (60, 44, 46))
def idols_near(p):
    dunes(p, 1520, 30, (60, 40, 40), (16, 10, 12), 13)
    rubble(p, 540, 1580, 440, (110, 84, 76), 14, n=20)

def burn_sky(p):
    p.sky([(0, (24, 6, 6)), (.5, (110, 24, 16)), (.75, (220, 90, 30)), (1, (40, 10, 8))])
    p.glow(540, 1250, 650, (255, 120, 40), .6)
def burn_mid(p):
    city(p, 1400, (30, 10, 10), 21, lights=(255, 150, 60), domes=False)
def burn_near(p):
    dunes(p, 1560, 40, (50, 16, 12), (12, 4, 4), 22)
    for x, y in ((140, 1320), (360, 1400), (720, 1400), (940, 1320)): lantern(p, x, y, .8, (255, 130, 50))

def build_sky(p):
    p.sky([(0, (40, 30, 60)), (.45, (140, 80, 90)), (.7, (240, 150, 90)), (1, (90, 50, 40))])
    sun(p, 820, 1150, 70, (255, 190, 120)); p.glow(820, 1150, 380, (255, 170, 100), .5)
def build_mid(p):
    stone_wall(p, 120, 960, 1500, 520, (110, 70, 50), 31)
    p.rect(330, 1080, 750, 1500, (40, 22, 16))                       # dark opening inside the walls
def build_near(p):
    p.rect(-200, 1500, 1280, 2300, (70, 44, 30))
    logs(p, 200, 1620, 0, 4, (120, 72, 40), 33); logs(p, 880, 1620, 0, 3, (120, 72, 40), 34)

def thrown_sky(p):
    p.sky([(0, (6, 2, 4)), (.5, (70, 10, 8)), (.85, (190, 60, 20)), (1, (50, 12, 6))])
    p.glow(540, 1200, 900, (255, 90, 20), 1.0)
def thrown_mid(p):
    stone_wall(p, -100, 110, 1660, 980, (50, 26, 20), 41); stone_wall(p, 970, 1180, 1660, 980, (50, 26, 20), 42)
def thrown_near(p): p.rect(-200, 1620, 1280, 2300, (18, 8, 6))

def cool_sky(p):
    p.sky([(0, (6, 16, 40)), (.5, (30, 70, 120)), (.8, (120, 190, 230)), (1, (20, 40, 70))])
    stars(p, 70, 51, 700)
    p.glow(540, 1250, 800, (170, 220, 255), .9)
def cool_mid(p):
    stone_wall(p, -100, 110, 1660, 980, (40, 54, 80), 52); stone_wall(p, 970, 1180, 1660, 980, (40, 54, 80), 53)
def cool_near(p): p.rect(-200, 1620, 1280, 2300, (10, 18, 30))

def saved_sky(p):
    p.sky([(0, (40, 70, 130)), (.45, (150, 180, 220)), (.7, (255, 225, 190)), (1, (130, 110, 100))])
    sun(p, 540, 1080, 90, (255, 240, 200))
    rays(p, 540, 1080, (255, 248, 225), n=16, spread=360, length=1600, width=3, a=.22, angle=0, seed=61)
def saved_mid(p):
    stone_wall(p, 140, 940, 1500, 300, (130, 120, 120), 62)
    p.rect(380, 1260, 700, 1500, (230, 225, 220)); p.glow(540, 1380, 300, (255, 255, 240), .7)
def saved_near(p):
    p.rect(-200, 1500, 1280, 2300, (110, 100, 96)); coals(p, 540, 1560, 340, (200, 200, 210), 63)

def losers_sky(p):
    p.sky([(0, (14, 12, 18)), (.6, (50, 44, 54)), (1, (24, 20, 26))])
    clouds(p, 71, 300, 900, (80, 74, 88), 6, 120)
def losers_mid(p):
    city(p, 1420, (26, 22, 30), 72, domes=False)
    idol(p, 540, 1480, 90, 360, (50, 46, 52))
def losers_near(p):
    dunes(p, 1540, 30, (40, 36, 40), (12, 10, 12), 73)
    rubble(p, 540, 1600, 470, (70, 64, 70), 74, n=18)

def lesson_sky(p):
    p.sky([(0, (30, 50, 110)), (.4, (120, 140, 200)), (.66, (255, 200, 140)), (1, (120, 80, 50))])
    sun(p, 540, 1420, 110, (255, 220, 150))
    rays(p, 540, 1420, (255, 236, 190), n=18, spread=360, length=1700, width=3, a=.15, angle=0, seed=81)
def lesson_mid(p): mountains(p, 1360, 230, (90, 70, 90), 82, rim=(255, 210, 160))
def lesson_near(p):
    dunes(p, 1500, 40, (200, 160, 110), (120, 80, 50), 83)
    palm(p, 150, 1620, 420, (50, 70, 36), -.04); palm(p, 950, 1600, 380, (50, 70, 36), .05)

def end_sky(p):
    p.sky([(0, (6, 8, 30)), (.45, (30, 36, 80)), (.7, (100, 90, 130)), (.78, (220, 160, 120)), (1, (24, 16, 20))])
    stars(p, 220, 91, 900); moon(p, 820, 300, 56)
def end_mid(p): dunes(p, 1380, 50, (44, 44, 66), (16, 16, 26), 92)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
FIRE = dict(cx=540, base=1640, w=760, h=820)
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=[('flames', FIRE), 'embers'], cam='hold', bloom=.7,
         title=dict(text='A fire built to burn him', arabic=TITLE_AR, hold=99, plain=True),
         lines=['A fire built to burn him. Then Allah spoke to it.']),
    dict(layers=[idols_sky, idols_mid, idols_near], fx=['twinkle'], cam='right',
         lines=['Ibrahim, peace be upon him, had broken their idols.', 'He asked why they worship what cannot help or harm.']),
    dict(layers=[burn_sky, burn_mid, burn_near], fx=['embers'], cam='in',
         verse=dict(key='21:68', en='Burn him and support your gods - if you are to act', line=1, ar_size=90),
         lines=['Their only answer was this. They said:', 'Burn him and support your gods, if you are to act.']),
    dict(layers=[build_sky, build_mid, build_near], fx=['dust'], cam='up',
         verse=dict(key='37:97', en='Construct for him a furnace and throw him into the burning fire', line=1, ar_size=90),
         lines=['And they said:', 'Construct for him a furnace and throw him into the burning fire.']),
    dict(layers=[thrown_sky, thrown_mid, thrown_near], fx=[('flames', dict(FIRE, w=900, h=1000)), 'embers'], cam='hold', bloom=.75, pause=0.5,
         lines=['They threw him into the fire.', 'What would happen to him now?']),
    dict(layers=[cool_sky, cool_mid, cool_near], fx=[('flames', dict(FIRE, w=900, h=1000, cool=True)), 'twinkle'], cam='hold', bloom=.75,
         verse=dict(key='21:69', ar=(1, 7), en='O fire, be coolness and safety upon Abraham', line=1, ar_size=84),
         lines=['Allah said:', 'O fire, be coolness and safety upon Abraham.']),
    dict(layers=[saved_sky, saved_mid, saved_near], fx=['dust'], cam='in', bloom=.65,
         verse=dict(key='29:24', ar=(10, 14), en='but Allah saved him from the fire', line=0, ar_size=96),
         lines=['But Allah saved him from the fire.']),
    dict(layers=[losers_sky, losers_mid, losers_near], fx=['dust'], cam='out',
         verse=dict(key='21:70', en='And they intended for him harm, but We made them the greatest losers', line=1, ar_size=84),
         lines=['Allah says:', 'And they intended for him harm, but We made them the greatest losers.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='up',
         lines=['Nothing can harm you unless Allah allows it.', 'So stand for the truth, and trust Him.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who needs hope today.', 'And follow for a new story from the Quran every day.']),
]

PRON = {}

CAPTION = """They built a fire to burn him. Then Allah spoke to the fire. 🤍

Ibrahim (peace be upon him) broke his people's idols and called them to Allah alone. Their only answer was: "Kill him or burn him." (Quran 29:24)

They said: "Construct for him a furnace and throw him into the burning fire." (Quran 37:97)

Allah said, "O fire, be coolness and safety upon Abraham." (Quran 21:69) And Allah saved him from the fire.

"And they intended for him harm, but We made them the greatest losers." (Quran 21:70)

Nothing can harm you unless Allah allows it. Stand for the truth and trust Him.

📖 Sources: Quran 21:66–70, 29:24, 37:97–98 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetIbrahim #IslamicReminder"""

FIRST_COMMENT = """When have you felt Allah's help at the hardest moment? 🤍

References: Quran, Surah Al-Anbya 21:66–70; Surah Al-'Ankabut 29:24; Surah As-Saffat 37:97–98 (Saheeh International translation)."""
