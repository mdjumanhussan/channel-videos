"""Seerah Reel 1 (from Juman's Seerah Class 1 slides): Why was Mecca rich in a desert?
Quran only: 2:126 (Ibrahim's prayer for a secure city and fruits), 106:1-4 (Surah Quraysh).
"Winter caravan to Yemen, summer caravan to Syria" is the common tafsir of 106:2 (e.g. Ibn Kathir) and is said as narration.
No people or prophets drawn: valley, Kaaba, a small town, roads lit by caravan lanterns, palms, sky. No music."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  Seerah 1'
VOICE, SPEED = 'bm_george', 1.05
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Why Was Mecca Rich in a Desert?'
HITS = [(5, 1, 0.0), (6, 0, 0.0)]
TITLE_AR = quran()['verses']['106:1']['ar']

def flat_town(p, base, col, seed, lit=None):
    rnd = random.Random(seed); x = -150
    while x < 1250:
        w = rnd.uniform(70, 150); h = rnd.uniform(40, 140)
        p.rect(x, base - h, x + w, base + 800, col); p.rect(x - 4, base - h - 8, x + w + 4, base - h, lc(col, (0, 0, 0), .2))
        if lit and rnd.random() < .45:
            wx, wy = x + rnd.uniform(12, w - 22), base - h + rnd.uniform(16, max(20, h - 16))
            p.rect(wx, wy, wx + 10, wy + 14, lit, 200); p.glow(wx + 5, wy + 7, 20, lit, .25)
        x += w + rnd.uniform(-10, 14)

def caravan_road(p, x0, y0, x1, y1, w0, w1, col, light, n=9):
    """A road from (x0,y0) near the viewer to (x1,y1) on the horizon, with a line of caravan lanterns along it."""
    p.poly([(x0 - w0 / 2, y0), (x0 + w0 / 2, y0), (x1 + w1 / 2, y1), (x1 - w1 / 2, y1)], col, 190)
    for k in range(n):
        t = (k + .5) / n; x = lerp(x0, x1, t); y = lerp(y0, y1, t); s = lerp(.32, .09, t)
        p.glow(x, y - 30 * s, 70 * s, light, .5); lantern(p, x, y - 40 * s, s, light)

# ---------------------------------------------------------------- painters
def hook_sky(p):
    p.sky([(0, (120, 160, 200)), (.5, (225, 210, 180)), (.75, (240, 200, 140)), (1, (150, 110, 70))])
    sun(p, 780, 330, 70, (255, 250, 230)); p.glow(780, 330, 520, (255, 240, 200), .5)
def hook_mid(p): mountains(p, 1280, 330, (52, 40, 36), 2, rim=(160, 120, 90), peaks=6)
def hook_near(p): dunes(p, 1470, 20, (196, 150, 100), (120, 84, 54), 3)

def dua_sky(p):
    p.sky([(0, (4, 8, 26)), (.5, (16, 24, 60)), (.8, (50, 46, 90)), (1, (10, 10, 18))])
    stars(p, 240, 11, 1100); moon(p, 820, 300, 50)
def dua_mid(p): mountains(p, 1300, 260, (20, 20, 40), 12, rim=(110, 110, 170))
def dua_near(p):
    dunes(p, 1480, 12, (40, 36, 56), (10, 10, 18), 13)
    p.glow(540, 1430, 260, (255, 200, 120), .45); kaaba(p, 520, 1500, .75)
    lantern(p, 760, 1420, .45, (255, 196, 110))

def quraysh_sky(p):
    p.sky([(0, (40, 50, 100)), (.45, (170, 130, 150)), (.68, (255, 170, 110)), (.8, (255, 214, 150)), (1, (70, 44, 34))])
    sun(p, 540, 1290, 70, (255, 230, 180)); p.glow(540, 1290, 520, (255, 170, 100), .6)
def quraysh_mid(p): mountains(p, 1310, 240, (70, 46, 50), 22, rim=(255, 190, 130))
def quraysh_near(p):
    flat_town(p, 1450, (86, 58, 50), 23)
    kaaba(p, 540, 1540, .8)
    dunes(p, 1580, 8, (110, 76, 60), (40, 26, 22), 24)

def roads_sky(p):
    p.sky([(0, (6, 10, 30)), (.5, (20, 30, 70)), (.8, (60, 54, 90)), (1, (12, 10, 18))])
    stars(p, 260, 31, 1000)
    p.glow(150, 1150, 480, (120, 170, 255), .35)        # cool winter side
    p.glow(930, 1150, 480, (255, 170, 90), .35)         # warm summer side
def roads_mid(p): mountains(p, 1220, 180, (24, 24, 44), 32, rim=(120, 120, 170))
def roads_near(p):
    dunes(p, 1360, 10, (44, 40, 60), (12, 12, 20), 33)
    caravan_road(p, 470, 1950, 170, 1230, 420, 16, (90, 90, 120), (190, 215, 255))
    caravan_road(p, 610, 1950, 910, 1230, 420, 16, (110, 92, 96), (255, 200, 120))
    kaaba(p, 540, 1700, .55)

def house_sky(p):
    p.sky([(0, (30, 40, 90)), (.45, (150, 120, 150)), (.7, (255, 190, 120)), (1, (80, 50, 36))])
    rays(p, 540, -100, (255, 236, 190), n=11, spread=55, a=.16, seed=41)
def house_near(p):
    dunes(p, 1660, 8, (120, 86, 66), (44, 30, 24), 42)
    p.glow(540, 1500, 520, (255, 220, 150), .55); kaaba(p, 540, 1720, 1.0)

def fed_sky(p):
    p.sky([(0, (60, 100, 160)), (.45, (190, 190, 200)), (.7, (255, 210, 150)), (1, (130, 96, 70))])
    sun(p, 540, 1240, 80, (255, 240, 210)); p.glow(540, 1240, 520, (255, 220, 170), .55)
def fed_mid(p): flat_town(p, 1380, (130, 96, 80), 52, lit=(255, 220, 150))
def fed_near(p):
    dunes(p, 1500, 10, (190, 150, 110), (110, 80, 56), 53)
    for x, h, ln in ((120, 520, .06), (300, 420, .02), (800, 440, -.03), (970, 540, -.07)): palm(p, x, 1620, h, (50, 40, 30), lean=ln)

def lesson_sky(p):
    p.sky([(0, (20, 40, 90)), (.45, (120, 130, 180)), (.68, (255, 190, 130)), (.8, (255, 225, 170)), (1, (90, 60, 44))])
    sun(p, 540, 1280, 90, (255, 245, 220)); p.glow(540, 1280, 620, (255, 210, 150), .6)
def lesson_mid(p): mountains(p, 1320, 200, (90, 64, 64), 62, rim=(255, 210, 160))
def lesson_near(p): dunes(p, 1480, 12, (160, 116, 84), (70, 48, 36), 63); kaaba(p, 540, 1560, .6)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 71, 900); moon(p, 820, 300, 56)
def end_mid(p): flat_town(p, 1420, (30, 26, 44), 72, lit=(255, 200, 120))
def end_near(p): dunes(p, 1540, 10, (34, 28, 50), (10, 8, 16), 73)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.6,
         title=dict(text='No river. No farms. Rich?', arabic=TITLE_AR, hold=99, plain=True),
         lines=['A valley with no river and no farms became the richest town in Arabia. How?']),
    dict(layers=[dua_sky, dua_mid, dua_near], fx=['twinkle'], cam='in',
         verse=dict(key='2:126', ar=(3, 12), en='My Lord, make this a secure city and provide its people with fruits', line=1, ar_size=78),
         lines=['Long ago, Prophet Ibrahim, peace be upon him, stood in this valley and prayed:',
                'My Lord, make this a secure city and provide its people with fruits.']),
    dict(layers=[quraysh_sky, quraysh_mid, quraysh_near], fx=['dust'], cam='up',
         verse=dict(key='106:1', line=1, ar_size=104),
         lines=['Centuries later, Allah revealed a surah about his descendants, the Quraysh:',
                'For the accustomed security of the Quraysh.']),
    dict(layers=[roads_sky, roads_mid, roads_near], fx=['twinkle'], cam='in',
         verse=dict(key='106:2', line=0, ar_size=96),
         lines=['Their accustomed security in the caravan of winter and summer.',
                'A winter caravan south to Yemen. A summer caravan north to Syria.']),
    dict(layers=[house_sky, house_near], fx=['dust'], cam='in',
         verse=dict(key='106:3', line=1, ar_size=100),
         lines=['Then Allah told them who to thank:', 'Let them worship the Lord of this House.']),
    dict(layers=[fed_sky, fed_mid, fed_near], fx=['dust'], cam='up', pause=0.6,
         verse=dict(key='106:4', line=1, ar_size=84),
         lines=['The One', 'Who has fed them, saving them from hunger, and made them safe, saving them from fear.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='Safe and fed. He answered.', after=0, y=580),
         lines=['Safe, and fed. Exactly what Ibrahim asked for.', 'Allah answers prayers, even across the centuries.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='Seerah · Class 1'),
         lines=['Share this with someone who is still waiting on a dua.', 'And follow for a new story from the Quran every day.']),
]

PRON = {'Quraysh': 'kʊɹˈeɪʃ'}

CAPTION = """A valley with no river and no farms became the richest town in Arabia. How? 🤍

Prophet Ibrahim (peace be upon him) prayed: "My Lord, make this a secure city and provide its people with fruits." (Quran 2:126)

Centuries later, Allah revealed Surah Quraysh: "For the accustomed security of the Quraysh. Their accustomed security [in] the caravan of winter and summer." (Quran 106:1–2)

"Let them worship the Lord of this House, Who has fed them, [saving them] from hunger and made them safe, [saving them] from fear." (Quran 106:3–4)

Safe and fed. Exactly what Ibrahim asked for. Allah answers prayers, even across centuries.

📖 Sources: Quran 2:126, 106:1–4 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#Seerah #SurahQuraysh #IslamicReminder"""

FIRST_COMMENT = """Which dua are you still waiting on? Say "Ameen" for each other below. 🤲

References: Quran, Surah Al-Baqarah 2:126; Surah Quraysh 106:1–4 (Saheeh International translation). Winter caravan to Yemen and summer caravan to Syria: the common tafsir of 106:2 (e.g., Ibn Kathir). Seerah Class 1."""
