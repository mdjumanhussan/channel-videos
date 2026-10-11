"""Story 2: The two sons of Adam. Source: Quran 5:27-31 (Saheeh International).
The Quran does not name the brothers, so this episode does not either. No figures are drawn."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  2'
VOICE, SPEED = 'bm_george', 1.0
THUMB_AT = 1.6
TITLE = 'The Two Sons of Adam and the Crow'
HITS = [(4, 0, 0.0), (5, 0, 0.0)]
# "Adam's two sons", taken straight from the text of 5:27
TITLE_AR = ' '.join(quran()['verses']['5:27']['ar'].split()[3:5])

# ---------------------------------------------------------------- small scenery helpers for this story
def cairn(p, cx, base, s, col, lit=None):
    """A small pile of stones (a place of offering). No figures."""
    rnd = random.Random(int(cx))
    rows = [(5, 0), (4, -46), (3, -90), (2, -130), (1, -164)]
    for n, dy in rows:
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * 62 * s + rnd.uniform(-6, 6) * s; y = base + dy * s
            c = lc(col, (0, 0, 0), rnd.uniform(0, .25))
            p.ell(x, y, 36 * s, 26 * s, c)
            if lit: p.ell(x - 6 * s, y - 9 * s, 22 * s, 9 * s, lc(c, lit, .55))

def bare_tree(p, x, base, h, col, seed):
    """Leafless tree silhouette."""
    rnd = random.Random(seed)
    def branch(x0, y0, ang, ln, w, depth):
        x1, y1 = x0 + ln * math.cos(ang), y0 - ln * math.sin(ang)
        p.line([(x0, y0), (x1, y1)], col, max(2, w))
        if depth:
            for _ in range(2 if depth > 1 else 3):
                branch(x1, y1, ang + rnd.uniform(-.75, .75), ln * rnd.uniform(.58, .76), w * .62, depth - 1)
    p.poly([(x - 22, base + 20), (x - 10, base - h * .3), (x + 10, base - h * .3), (x + 22, base + 20)], col)
    branch(x, base - h * .28, math.pi / 2 + rnd.uniform(-.1, .1), h * .3, 16, 4)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def open_sky(p):
    p.sky([(0, (10, 14, 34)), (.4, (34, 44, 84)), (.62, (150, 110, 110)), (.72, (236, 176, 120)), (1, (36, 24, 26))])
    stars(p, 220, 12, 900); clouds(p, 5, 900, 1250, (250, 180, 150), 6, 110)
    p.glow(540, 1380, 620, (255, 190, 120), .35)
def open_mid(p): mountains(p, 1420, 300, (52, 44, 66), 14, rim=(240, 180, 130))
def open_near(p):
    dunes(p, 1640, 70, (44, 34, 40), (12, 8, 10), 15)
    bare_tree(p, 170, 1660, 420, (14, 10, 12), 3)

def offer_sky(p):
    p.sky([(0, (40, 70, 120)), (.4, (120, 150, 190)), (.62, (250, 214, 160)), (1, (90, 70, 50))])
    clouds(p, 21, 300, 800, (255, 245, 230), 6, 150)
    rays(p, 300, -260, (255, 240, 190), n=6, spread=14, width=3, a=.55, angle=90, seed=3)
    p.glow(300, 1240, 360, (255, 226, 160), .6)
def offer_far(p): mountains(p, 1330, 220, (120, 120, 140), 23)
def offer_mid(p):
    dunes(p, 1370, 60, (176, 150, 100), (90, 70, 46), 24)
    p.glow(300, 1300, 240, (255, 236, 180), .55)
    cairn(p, 300, 1370, 1.0, (150, 128, 96), lit=(255, 236, 180))
    cairn(p, 790, 1400, 1.0, (64, 60, 62))
def offer_near(p): dunes(p, 1680, 60, (70, 54, 38), (22, 16, 12), 25)

def storm_sky(p):
    p.sky([(0, (16, 6, 10)), (.45, (62, 14, 18)), (.7, (130, 36, 24)), (1, (18, 8, 8))])
    clouds(p, 31, 150, 900, (40, 14, 18), 12, 230); clouds(p, 32, 700, 1150, (170, 60, 40), 6, 120)
    p.glow(540, 1320, 700, (255, 80, 40), .28)
def storm_mid(p): mountains(p, 1400, 420, (26, 10, 12), 33, rim=(190, 70, 40))
def storm_near(p): dunes(p, 1660, 50, (18, 8, 8), (4, 2, 2), 34)

def calm_sky(p):
    p.sky([(0, (4, 10, 30)), (.5, (16, 36, 76)), (.74, (60, 90, 130)), (1, (10, 16, 28))])
    stars(p, 420, 41, 1250); moon(p, 780, 1040, 70, crescent=False)
def calm_mid(p):
    mountains(p, 1330, 200, (22, 34, 60), 42)
    sea(p, 1330, (40, 70, 110), (8, 16, 30), 43, lines=(220, 235, 255))
    p.glow(780, 1420, 300, (220, 235, 255), .18)
def calm_near(p): dunes(p, 1720, 50, (10, 16, 28), (2, 4, 8), 44)

def dark_sky(p):
    p.sky([(0, (4, 4, 8)), (.55, (16, 10, 16)), (.74, (84, 22, 20)), (.8, (150, 44, 26)), (1, (8, 4, 4))])
    clouds(p, 51, 250, 1000, (26, 12, 16), 10, 220)
    p.glow(540, 1500, 520, (200, 50, 30), .3)
def dark_mid(p): mountains(p, 1500, 260, (12, 6, 8), 52)
def dark_near(p):
    dunes(p, 1650, 50, (10, 5, 6), (2, 1, 1), 53)
    bare_tree(p, 800, 1670, 520, (4, 2, 3), 8)

def crow_sky(p):
    p.sky([(0, (70, 84, 110)), (.45, (150, 150, 160)), (.66, (232, 196, 160)), (1, (90, 70, 56))])
    clouds(p, 61, 250, 900, (230, 226, 226), 7, 140)
    p.glow(540, 1220, 520, (255, 226, 180), .4)
def crow_far(p): mountains(p, 1250, 180, (120, 112, 122), 62)
def crow_ground(p):
    dunes(p, 1500, 30, (164, 124, 84), (70, 48, 32), 63)
    p.ell(730, 1512, 120, 26, (60, 40, 28))                      # scratched hollow in the earth
    for dx, r in ((-150, 34), (-110, 22), (140, 30), (95, 18)): p.ell(730 + dx, 1500, r * 1.5, r * .7, (120, 86, 56))
    crow(p, 540, 1508, 1.35)
def crow_near(p): dunes(p, 1740, 40, (60, 42, 30), (18, 12, 8), 64)

def regret_sky(p):
    p.sky([(0, (30, 34, 52)), (.5, (84, 84, 104)), (.7, (176, 150, 140)), (1, (40, 34, 36))])
    clouds(p, 71, 200, 1000, (60, 60, 76), 10, 200)
def regret_mid(p):
    mountains(p, 1420, 220, (44, 42, 56), 72)
    dunes(p, 1520, 40, (70, 60, 60), (24, 20, 22), 73)
def regret_near(p):
    bare_tree(p, 250, 1700, 560, (10, 8, 10), 21)
    crow(p, 760, 1560, 1.0, peck=False, flip=True)
    dunes(p, 1730, 40, (20, 16, 18), (6, 4, 6), 74)

def lesson_sky(p):
    p.sky([(0, (70, 110, 190)), (.4, (240, 190, 170)), (.62, (255, 226, 170)), (1, (120, 76, 52))])
    sun(p, 540, 1150, 110); rays(p, 540, 1150, (255, 240, 200), n=14, spread=360, length=1600, width=3, a=.22, angle=0, seed=5)
    clouds(p, 81, 450, 950, (255, 206, 190), 7, 150)
def lesson_mid(p): dunes(p, 1340, 80, (226, 166, 112), (140, 90, 60), 82)
def lesson_near(p):
    dunes(p, 1640, 80, (110, 66, 46), (34, 20, 14), 83); palm(p, 170, 1640, 420, (36, 22, 16), .1)

def end_sky(p):
    p.sky([(0, (6, 14, 36)), (.45, (26, 50, 96)), (.66, (120, 130, 150)), (.74, (236, 190, 140)), (1, (20, 18, 24))])
    stars(p, 220, 91, 900); moon(p, 230, 300, 56)
def end_mid(p):
    city(p, 1430, (22, 28, 46), 5, lights=(255, 200, 120))
    mosque(p, 540, 1330, 1.0, (12, 18, 34), windows=(255, 206, 130))
def end_near(p):
    dunes(p, 1700, 40, (8, 12, 22), (2, 4, 8), 92); lantern(p, 930, 1180, .9)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[open_sky, open_mid, open_near], fx=['twinkle', 'dust'], cam='in',
         title=dict(kicker='Story 2  ·  from the Quran', text='Why did Allah send a crow?', arabic=TITLE_AR, hold=99),
         lines=['Why did Allah send a crow?', 'This is the story of the two sons of Adam, peace be upon him.']),
    dict(layers=[offer_sky, offer_far, offer_mid, offer_near], fx=['dust'], cam='up',
         lines=['They both offered a sacrifice.', 'It was accepted from one, but not from the other.']),
    dict(layers=[storm_sky, storm_mid, storm_near], fx=['embers'], cam='in', bloom=.7,
         verse=dict(key='5:27', ar=(17, 18), en='I will surely kill you', line=1, ar_size=96),
         lines=['The one who was refused said:', 'I will surely kill you.']),
    dict(layers=[calm_sky, calm_mid, calm_near], fx=['twinkle'], cam='out', pause=0.5,
         verse=dict(key='5:28', en='If you should raise your hand against me to kill me - I shall not raise my hand against you to kill you. Indeed, I fear Allah, Lord of the worlds', line=1, ar_size=62, y=620),
         lines=['His brother said:', 'If you should raise your hand against me to kill me, I shall not raise my hand against you to kill you. Indeed, I fear Allah, Lord of the worlds.']),
    dict(layers=[dark_sky, dark_mid, dark_near], fx=['embers'], cam='in', bloom=.6,
         verse=dict(key='5:30', en='And his soul permitted to him the murder of his brother, so he killed him and became among the losers', line=0, ar_size=66),
         lines=['And his soul permitted to him the murder of his brother, so he killed him, and became among the losers.']),
    dict(layers=[crow_sky, crow_far, crow_ground, crow_near], fx=['dust'], cam='in',
         verse=dict(key='5:31', ar=(0, 11), en='Then Allah sent a crow searching in the ground to show him how to hide the disgrace of his brother', line=0, ar_size=62, y=600),
         lines=['Then Allah sent a crow, searching in the ground, to show him how to hide the disgrace of his brother.']),
    dict(layers=[regret_sky, regret_mid, regret_near], fx=['dust'], cam='left',
         verse=dict(key='5:31', ar=(12, 22), en='O woe to me! Have I failed to be like this crow and hide the body of my brother?', line=1, ar_size=62, y=600),
         lines=['He said:', 'O woe to me! Have I failed to be like this crow, and hide the body of my brother?', 'And he became of the regretful.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='up',
         lines=['One brother feared Allah.', 'Be like him.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'dust'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who needs it. And follow for a new story from the Quran every day.']),
]

CAPTION = """Why did Allah send a crow to a man? 🤍

The two sons of Adam (peace be upon him) each offered a sacrifice. It was accepted from one, but not from the other.

The one who was refused said, "I will surely kill you."

His brother answered: "Indeed, Allah only accepts from the righteous [who fear Him]." (Quran 5:27)

He killed him, and became among the losers. Then Allah sent a crow, searching in the ground, to show him how to hide his brother's body. And he became of the regretful.

One brother feared Allah. Be like him.

📖 Sources: Quran 5:27–31, Saheeh International
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetAdam #IslamicReminder"""

FIRST_COMMENT = """Which words from this story stay with you? 🤍

References: Quran, Surah Al-Ma'idah 5:27–31 (Saheeh International translation). The Quran does not name the two brothers, so we did not either."""
