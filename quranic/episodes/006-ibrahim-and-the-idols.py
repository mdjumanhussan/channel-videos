"""Story 6: Young Ibrahim and the idols. Sources: Quran 21:51-67, 6:74, 37:83-96, 26:69-77, 19:41-48 (Saheeh International).
No people are drawn: a city, a temple hall, stone columns, abstract stone idols (plain pillars, no faces or bodies),
broken fragments, lamps, sky and light only. The Quran does not mention an axe, so none is drawn or said.
Improvement tried today: faster pacing. Voice speed 1.1 (was 1.0) so the script runs about 2.6-2.8 words a second
(guidance: 2.5-3 words/s), and the first picture changes by about second 4.
Reason: average watch has been stuck at 3-7 s for five Reels, whatever the hook; the pace of the first seconds is untested."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  6'
VOICE, SPEED = 'bm_george', 1.1
THUMB_AT = 1.2
TITLE = 'Young Ibrahim and the Idols: "So Ask Them"'
HITS = [(7, 1, 0.0)]
# "Rather, this - the largest of them - did it", taken straight from the text of 21:63
TITLE_AR = ' '.join(quran()['verses']['21:63']['ar'].split()[1:5])

# ---------------------------------------------------------------- small scenery helpers for this story
def idol(p, cx, base, w, h, col, seed=0, rim=None):
    """An abstract stone idol: plinth, banded pillar, stepped pointed crown. Deliberately no face, head or limbs."""
    dk = lc(col, (0, 0, 0), .35); lt = lc(col, (255, 230, 190), .22)
    p.rect(cx - w * .75, base - h * .1, cx + w * .75, base, dk)                       # plinth
    p.rect(cx - w * .62, base - h * .14, cx + w * .62, base - h * .1, lt)
    p.poly([(cx - w / 2, base - h * .14), (cx - w * .42, base - h * .8), (cx + w * .42, base - h * .8), (cx + w / 2, base - h * .14)], col)
    p.poly([(cx + w * .1, base - h * .14), (cx + w * .08, base - h * .8), (cx + w * .42, base - h * .8), (cx + w / 2, base - h * .14)], dk, 120)
    for k in range(3):                                                                # carved bands
        y = base - h * (.3 + .17 * k); p.rect(cx - w * .48 + k * 2, y - 8, cx + w * .48 - k * 2, y + 8, lt, 200)
    p.rect(cx - w * .5, base - h * .86, cx + w * .5, base - h * .8, lt)               # capital
    p.poly([(cx - w * .4, base - h * .86), (cx, base - h), (cx + w * .4, base - h * .86)], col)   # pointed crown
    if rim: p.line([(cx - w * .42, base - h * .8), (cx - w / 2, base - h * .14)], rim, 4, 150)

def fragments(p, cx, base, spread, col, seed, n=14):
    """Broken stone pieces scattered on the floor (21:58)."""
    rnd = random.Random(seed); dk = lc(col, (0, 0, 0), .4); lt = lc(col, (255, 230, 190), .2)
    for i in range(n):
        x = cx + rnd.uniform(-spread, spread); y = base + rnd.uniform(-30, 40); s = rnd.uniform(18, 46)
        pts = [(x + s * math.cos(a) * rnd.uniform(.6, 1.2), y + s * .6 * math.sin(a) * rnd.uniform(.6, 1.2)) for a in [k * 2 * math.pi / 5 + rnd.uniform(0, .5) for k in range(5)]]
        p.ell(x, y + s * .5, s * 1.1, s * .25, (0, 0, 0), 90)
        p.poly(pts, dk if i % 3 == 0 else col); p.line(pts[:2], lt, 3, 180)
    for i in range(4):                                                                 # a few fallen pillar drums
        x = cx + rnd.uniform(-spread, spread); y = base + rnd.uniform(-10, 30)
        p.rect(x - 50, y - 26, x + 50, y + 22, col); p.ell(x + 50, y - 2, 14, 24, lc(col, (255, 230, 190), .25))

def hall(p, col, light=None, cols=(110, 340, 740, 970)):
    """Inside of a temple hall: back wall, columns, lintel."""
    dk = lc(col, (0, 0, 0), .4); lt = lc(col, (255, 230, 190), .18)
    p.rect(-200, 300, 1280, 1500, col)
    if light: p.glow(540, 760, 520, light, .7)
    p.rect(-200, 300, 1280, 400, dk); p.rect(-200, 400, 1280, 420, lt)
    for x in cols:
        p.rect(x - 70, 420, x + 70, 1500, lc(col, (0, 0, 0), .15)); p.rect(x - 70, 420, x - 50, 1500, lt, 160)
        p.rect(x - 90, 420, x + 90, 470, lt); p.rect(x - 90, 1440, x + 90, 1500, dk)

def floor(p, y, col):
    p.rect(-200, y, 1280, 2300, col)
    for k in range(6): p.line([(-200, y + 40 + k * 80), (1280, y + 40 + k * 80)], lc(col, (0, 0, 0), .2), 3, 120)

def doorway(p, cx, base, w, h, col, glow_col):
    p.glow(cx, base - h / 2, w * 1.6, glow_col, .8)
    p.rect(cx - w / 2, base - h, cx + w / 2, base, glow_col)
    p.ell(cx, base - h, w / 2, w / 2 * .7, glow_col)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_bg(p):
    p.sky([(0, (20, 12, 10)), (1, (40, 22, 14))])
    hall(p, (70, 42, 30), light=(255, 170, 90))
def hook_mid(p):
    floor(p, 1500, (54, 32, 22))
    idol(p, 540, 1520, 230, 760, (150, 100, 60), rim=(255, 200, 130))
def hook_near(p): fragments(p, 540, 1600, 460, (120, 80, 50), 7, n=18)

def city_sky(p):
    p.sky([(0, (30, 20, 60)), (.45, (150, 70, 90)), (.66, (250, 170, 100)), (1, (80, 40, 30))])
    sun(p, 780, 1180, 80, (255, 200, 130)); p.glow(780, 1180, 420, (255, 180, 110), .6)
def city_mid(p):
    city(p, 1400, (60, 30, 36), 13, lights=(255, 190, 110), domes=False)
    for x, h in ((360, 300), (540, 420), (720, 300)): idol(p, x, 1420, 70, h, (40, 20, 24))
def city_near(p): dunes(p, 1560, 40, (90, 50, 40), (30, 16, 14), 14)

def ask_bg(p):
    p.sky([(0, (14, 16, 30)), (1, (30, 30, 50))])
    hall(p, (50, 46, 70), light=(220, 200, 255), cols=(60, 1020))
def ask_mid(p):
    floor(p, 1480, (36, 32, 50))
    for x, h, s in ((230, 520, 120), (420, 640, 140), (660, 640, 140), (850, 520, 120)): idol(p, x, 1500, s, h, (90, 80, 110), rim=(200, 190, 255))
def ask_near(p): lantern(p, 160, 1260, .8)

def fathers_sky(p):
    p.sky([(0, (40, 20, 10)), (.45, (120, 60, 30)), (.7, (220, 140, 70)), (1, (60, 30, 20))])
    p.glow(540, 1200, 600, (255, 170, 90), .5)
def fathers_mid(p):
    mountains(p, 1300, 260, (110, 60, 40), 31)
    for i, x in enumerate(range(120, 1000, 150)): idol(p, x, 1430 + (i % 2) * 30, 60, 240 + (i % 3) * 40, (70, 36, 24))
def fathers_near(p): dunes(p, 1540, 40, (80, 40, 26), (24, 12, 8), 33)

def away_sky(p):
    p.sky([(0, (90, 150, 210)), (.45, (190, 220, 235)), (.66, (255, 236, 200)), (1, (170, 140, 100))])
    sun(p, 300, 560, 80); clouds(p, 41, 300, 700, (255, 250, 240), 5, 140)
def away_mid(p):
    city(p, 1380, (170, 130, 100), 42, domes=False)
    p.glow(540, 1300, 400, (255, 240, 200), .4)
def away_near(p):
    dunes(p, 1520, 30, (210, 180, 130), (150, 120, 80), 43)
    palm(p, 140, 1600, 420, (60, 80, 40), -.04); palm(p, 950, 1580, 380, (60, 80, 40), .05)

def broken_bg(p):
    p.sky([(0, (16, 10, 8)), (1, (34, 20, 14))])
    hall(p, (64, 40, 30), light=(255, 210, 140))
    rays(p, 540, 300, (255, 230, 170), n=7, spread=40, length=1500, width=8, a=.2, angle=90, seed=51)
def broken_mid(p):
    floor(p, 1500, (50, 30, 22))
    idol(p, 540, 1520, 200, 700, (140, 96, 60), rim=(255, 210, 140))
def broken_near(p): fragments(p, 540, 1590, 470, (130, 88, 56), 52, n=20)

def back_sky(p):
    p.sky([(0, (10, 8, 24)), (.45, (40, 24, 50)), (.7, (120, 50, 50)), (1, (20, 10, 14))])
    stars(p, 90, 61, 700); moon(p, 820, 360, 44)
def back_mid(p):
    p.rect(160, 900, 920, 1500, (40, 26, 30)); p.rect(130, 860, 950, 910, (60, 40, 40))
    doorway(p, 540, 1500, 260, 380, (90, 40, 30), (255, 150, 80))
    for x in (230, 850): lantern(p, x, 1120, .9)
def back_near(p): dunes(p, 1580, 40, (50, 30, 34), (14, 8, 10), 63)

def answer_bg(p):
    p.sky([(0, (14, 10, 8)), (1, (30, 20, 12))])
    hall(p, (60, 40, 28), light=(255, 220, 150), cols=(80, 1000))
def answer_mid(p):
    floor(p, 1500, (46, 30, 20))
    idol(p, 540, 1520, 240, 820, (150, 104, 66), rim=(255, 220, 150))
    p.glow(540, 1100, 360, (255, 220, 150), .35)
def answer_near(p): fragments(p, 540, 1600, 470, (110, 74, 48), 72, n=14)

def speak_sky(p):
    p.sky([(0, (10, 14, 30)), (.5, (30, 40, 70)), (1, (16, 18, 30))])
    stars(p, 120, 81, 1000)
def speak_mid(p):
    floor(p, 1480, (30, 30, 44))
    for x, h in ((300, 560), (780, 560)): idol(p, x, 1500, 120, h, (70, 70, 96))
    idol(p, 540, 1500, 170, 700, (90, 90, 120), rim=(190, 200, 255))
def speak_near(p): fragments(p, 540, 1590, 460, (70, 70, 90), 82, n=10)

def benefit_sky(p):
    p.sky([(0, (30, 60, 120)), (.45, (110, 150, 200)), (.66, (255, 220, 170)), (1, (120, 90, 60))])
    sun(p, 540, 980, 100, (255, 230, 170))
    rays(p, 540, 980, (255, 244, 210), n=16, spread=360, length=1600, width=3, a=.24, angle=0, seed=91)
def benefit_mid(p):
    mountains(p, 1360, 220, (120, 110, 120), 92)
    idol(p, 300, 1440, 70, 260, (60, 50, 50))
def benefit_near(p):
    dunes(p, 1500, 40, (200, 170, 120), (140, 100, 60), 93)
    fragments(p, 300, 1540, 120, (110, 90, 70), 94, n=6)

def end_sky(p):
    p.sky([(0, (8, 6, 30)), (.45, (36, 30, 80)), (.68, (130, 80, 110)), (.76, (230, 150, 100)), (1, (30, 14, 14))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p):
    dunes(p, 1380, 50, (50, 40, 60), (20, 14, 24), 102)
    fire(p, 540, 1400, 160, 220, 103)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_bg, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.6,
         title=dict(text='Why spare the biggest idol?', arabic=TITLE_AR, hold=99, plain=True),
         lines=['He broke every idol but the biggest. Why spare that one?']),
    dict(layers=[city_sky, city_mid, city_near], fx=['dust'], cam='right',
         lines=['Ibrahim, peace be upon him, saw his people devoted to statues.']),
    dict(layers=[ask_bg, ask_mid, ask_near], fx=['twinkle'], cam='up',
         verse=dict(key='21:52', ar=(4, 11), en='What are these statues to which you are devoted', line=1, ar_size=84),
         lines=['He asked his father and people:', 'What are these statues to which you are devoted?']),
    dict(layers=[fathers_sky, fathers_mid, fathers_near], fx=['embers'], cam='left',
         verse=dict(key='21:53', en='We found our fathers worshippers of them', line=1, ar_size=96),
         lines=['They said:', 'We found our fathers worshippers of them.']),
    dict(layers=[away_sky, away_mid, away_near], fx=['dust'], cam='right',
         lines=['When the people left, he went to their idols.']),
    dict(layers=[broken_bg, broken_mid, broken_near], fx=['dust'], cam='in', bloom=.6,
         verse=dict(key='21:58', ar=(0, 5), en='So he made them into fragments, except a large one among them', line=0, ar_size=90),
         lines=['So he made them into fragments, except a large one among them.']),
    dict(layers=[back_sky, back_mid, back_near], fx=['embers'], cam='down', pause=0.5,
         lines=['The people came back. Who has done this to our gods?', 'They asked Ibrahim if he did it.']),
    dict(layers=[answer_bg, answer_mid, answer_near], fx=['dust'], cam='in', bloom=.7,
         verse=dict(key='21:63', ar=(0, 9), en='Rather, this - the largest of them - did it, so ask them, if they should [be able to] speak', line=1, ar_size=72),
         lines=['He said:', 'Rather, this, the largest of them, did it. So ask them, if they should be able to speak.']),
    dict(layers=[speak_sky, speak_mid, speak_near], fx=['twinkle'], cam='out',
         verse=dict(key='21:65', ar=(4, 9), en='You have already known that these do not speak', line=1, ar_size=90),
         lines=['They said:', 'You have already known that these do not speak.']),
    dict(layers=[benefit_sky, benefit_mid, benefit_near], fx=['dust'], cam='up',
         verse=dict(key='21:66', ar=(1, 11), en='Then do you worship instead of Allah that which does not benefit you at all or harm you', line=1, ar_size=72),
         lines=['He said:', 'Then do you worship instead of Allah that which does not benefit you at all or harm you?']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'embers'], cam='in',
         end=dict(after=1, line1='Follow Quranic Story', line2='Tomorrow: what they did next'),
         lines=['Only Allah can help or harm you. What did they do to him next? See tomorrow.',
                'Share this with someone who needs it. And follow for a new story from the Quran every day.']),
]

PRON = {}

CAPTION = """He broke every idol except the biggest one. Why leave that one standing? 🤍

Young Ibrahim (peace be upon him) asked his father and his people: "What are these statues to which you are devoted?" They said: "We found our fathers worshippers of them." (Quran 21:52–53)

When they went away, he broke the idols into pieces, except the largest one. When they asked him who did it, he said: "Rather, this - the largest of them - did it, so ask them, if they should [be able to] speak." (Quran 21:63)

They knew the idols could not speak. He asked them: "Then do you worship instead of Allah that which does not benefit you at all or harm you?" (Quran 21:66)

Only Allah can help you or harm you. What they did to him next is tomorrow's story.

📖 Sources: Quran 21:51–67, 6:74, 37:83–96, 26:69–77 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetIbrahim #IslamicReminder"""

FIRST_COMMENT = """What would you have said to the people that day? 🤍

References: Quran, Surah Al-Anbya 21:51–67; Surah Al-An'am 6:74; Surah As-Saffat 37:83–96; Surah Ash-Shu'ara 26:69–77 (Saheeh International translation). Next: Ibrahim and the fire (Quran 21:68–70), in sha Allah."""
