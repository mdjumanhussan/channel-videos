"""Surah in 90 Seconds: Surah Al-Ma'un (107). Quran text only from data/quran.json (Saheeh International).
Explanations from Tafsir Ibn Kathir on 107 (text given by Juman from quran.com):
- 107:5: Ibn Abbas: hypocrites who pray in public but not in private. 'Ata' bin Dinar: Allah said heedless OF
  their prayer, not heedless IN their prayer (so a wandering mind is not what is meant).
- 107:7: Ibn Mas'ud: al-ma'un is what people give each other, like an axe, a pot, a bucket.
No hadith quoted (the "prayer of the hypocrite" narration was left out: could not open sunnah.com to confirm wording).
No people drawn. No music."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Surah in 90 Seconds  ·  107'
VOICE, SPEED = 'bm_george', 0.9
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah Al-Ma\'un in 90 Seconds: Woe to Those Who Pray?'
AYAH4 = quran()['verses']['107:4']['ar']

def door(p, cx, base, w, h, frame, inside, light=None):
    p.rect(cx - w / 2 - 18, base - h - 18, cx + w / 2 + 18, base, frame); p.ell(cx, base - h, w / 2 + 18, w / 2 + 18, frame)
    p.rect(cx - w / 2, base - h, cx + w / 2, base, inside); p.ell(cx, base - h, w / 2, w / 2, inside)
    if light: p.glow(cx, base - h * .5, w * 1.3, light, .5)

def pot(p, cx, base, s, col, rim):
    p.ell(cx, base - 70 * s, 95 * s, 75 * s, col); p.rect(cx - 70 * s, base - 150 * s, cx + 70 * s, base - 120 * s, rim)
    p.ell(cx, base - 150 * s, 70 * s, 14 * s, lc(rim, (255, 255, 255), .2))
    p.line([(cx - 95 * s, base - 110 * s), (cx - 125 * s, base - 120 * s)], rim, 10 * s); p.line([(cx + 95 * s, base - 110 * s), (cx + 125 * s, base - 120 * s)], rim, 10 * s)

def bucket(p, cx, base, s, col, rim):
    p.poly([(cx - 70 * s, base - 160 * s), (cx + 70 * s, base - 160 * s), (cx + 52 * s, base), (cx - 52 * s, base)], col)
    p.rect(cx - 72 * s, base - 168 * s, cx + 72 * s, base - 154 * s, rim)
    p.line([(cx - 70 * s, base - 160 * s), (cx - 40 * s, base - 240 * s), (cx + 40 * s, base - 240 * s), (cx + 70 * s, base - 160 * s)], rim, 6 * s)

# ---------------------------------------------------------------- layer painters (1080x1920)
def hook_sky(p):
    p.sky([(0, (6, 6, 20)), (.5, (24, 18, 44)), (.8, (70, 40, 50)), (1, (12, 8, 12))])
    stars(p, 160, 2, 900); moon(p, 820, 300, 50)
def hook_mid(p): mosque(p, 540, 1600, 1.2, (26, 18, 26), windows=(255, 200, 120))
def hook_near(p):
    dunes(p, 1620, 8, (36, 26, 32), (8, 6, 8), 4)
    p.glow(540, 1420, 360, (255, 120, 80), .25)

def intro_sky(p):
    p.sky([(0, (30, 40, 90)), (.45, (120, 110, 160)), (.68, (250, 170, 120)), (.8, (255, 210, 150)), (1, (60, 40, 40))])
    sun(p, 540, 1290, 70, (255, 225, 170)); p.glow(540, 1290, 480, (255, 180, 110), .6)
def intro_mid(p): city(p, 1420, (70, 50, 60), 11, lights=(255, 210, 140), domes=True)
def intro_near(p): dunes(p, 1500, 12, (80, 56, 60), (24, 16, 20), 12)

def deny_sky(p):
    p.sky([(0, (8, 8, 20)), (.5, (30, 24, 44)), (.8, (60, 40, 54)), (1, (10, 8, 12))])
    stars(p, 220, 21, 1100)
def deny_mid(p): mountains(p, 1320, 280, (26, 20, 32), 22, rim=(130, 100, 140))
def deny_near(p): dunes(p, 1500, 14, (40, 30, 42), (10, 8, 12), 23)

def orphan_sky(p):
    p.sky([(0, (14, 12, 26)), (.5, (40, 30, 46)), (1, (12, 10, 14))])
def orphan_mid(p):                                          # a warm doorway, firmly shut out by a dark street
    p.rect(0, 900, 1080, 1920, (34, 26, 30))
    door(p, 540, 1640, 300, 420, (70, 50, 44), (255, 196, 120), light=(255, 180, 100))
    p.rect(390, 1220, 690, 1640, (28, 20, 18))             # the door, closed
    p.ell(660, 1440, 10, 10, (200, 160, 90))
def orphan_near(p):
    p.rect(0, 1640, 1080, 1920, (20, 14, 14))
    lantern(p, 200, 1380, .55, (255, 190, 100))

def food_sky(p):
    p.sky([(0, (20, 14, 20)), (.5, (60, 36, 34)), (.8, (120, 70, 50)), (1, (24, 14, 12))])
    p.glow(540, 1300, 520, (255, 170, 100), .4)
def food_mid(p): mountains(p, 1360, 200, (50, 30, 30), 31, rim=(220, 140, 100))
def food_near(p):
    dunes(p, 1500, 12, (70, 44, 36), (20, 12, 10), 32)
    p.ell(540, 1620, 150, 30, (40, 26, 22)); p.ell(540, 1600, 130, 22, (90, 60, 40))   # an empty bowl

def woe_sky(p):
    p.sky([(0, (10, 4, 8)), (.5, (50, 14, 20)), (.8, (110, 36, 34)), (1, (16, 6, 8))])
    p.glow(540, 1200, 600, (255, 80, 60), .3)
def woe_mid(p): mosque(p, 540, 1620, 1.1, (20, 8, 12), windows=(255, 120, 80))
def woe_near(p): dunes(p, 1640, 8, (30, 12, 14), (8, 4, 4), 42)

def heed_sky(p):
    p.sky([(0, (6, 10, 30)), (.5, (20, 30, 70)), (.8, (60, 60, 100)), (1, (8, 10, 20))])
    stars(p, 140, 51, 900)
def heed_mid(p):                                            # a prayer mat, alone and empty, under a single lamp
    p.rect(0, 1000, 1080, 1920, (24, 20, 34))
    p.poly([(330, 1560), (750, 1560), (820, 1820), (260, 1820)], (90, 30, 36))
    p.poly([(380, 1580), (700, 1580), (750, 1790), (330, 1790)], (120, 44, 46))
    p.poly([(500, 1600), (580, 1600), (560, 1660), (520, 1660)], (210, 170, 90))
def heed_near(p): lantern(p, 540, 1260, .8, (255, 200, 120))

def show_sky(p):
    p.sky([(0, (30, 20, 10)), (.5, (110, 70, 30)), (.8, (220, 150, 70)), (1, (40, 24, 12))])
    rays(p, 540, -100, (255, 230, 170), n=11, spread=50, a=.22, seed=61)
def show_mid(p):                                            # a bright spotlit stage, and nobody but the crowd matters
    p.ell(540, 1600, 380, 80, (255, 220, 150), a=120); p.glow(540, 1560, 380, (255, 230, 170), .55)
def show_near(p):
    for k in range(9):
        x = 60 + k * 120; p.ell(x, 1820, 60, 70, (24, 16, 10)); p.ell(x, 1720, 34, 38, (24, 16, 10))

def maun_sky(p):
    p.sky([(0, (40, 30, 40)), (.5, (120, 80, 70)), (.8, (230, 170, 110)), (1, (70, 46, 34))])
    p.glow(540, 1200, 600, (255, 210, 150), .45)
def maun_mid(p): p.rect(0, 1450, 1080, 1920, (80, 54, 40)); p.rect(0, 1440, 1080, 1460, (120, 84, 60))
def maun_near(p):
    pot(p, 300, 1640, 1.0, (60, 40, 34), (150, 110, 70))
    bucket(p, 760, 1660, 1.0, (90, 70, 50), (170, 140, 100))
    p.line([(520, 1660), (600, 1420)], (110, 80, 50), 16); p.poly([(580, 1400), (660, 1430), (640, 1490), (590, 1460)], (180, 180, 190))  # axe

def lesson_sky(p):
    p.sky([(0, (40, 80, 150)), (.45, (160, 170, 200)), (.7, (255, 205, 150)), (1, (140, 100, 70))])
    sun(p, 540, 1250, 80, (255, 240, 210)); p.glow(540, 1250, 520, (255, 220, 170), .55)
def lesson_mid(p): mosque(p, 540, 1560, .95, (150, 110, 90), windows=(255, 230, 180))
def lesson_near(p):
    dunes(p, 1500, 14, (200, 160, 120), (110, 80, 60), 93)
    for x in (170, 910): palm(p, x, 1600, 300, (100, 72, 54), lean=.07 if x < 540 else -.07)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): mosque(p, 540, 1580, .9, (22, 18, 36), windows=(255, 200, 120))
def end_near(p): dunes(p, 1500, 12, (34, 28, 50), (10, 8, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.6,
         title=dict(text='Woe to those who pray?', arabic=AYAH4, hold=99, plain=True),
         lines=['There is a verse that warns people who pray.', 'Why would Allah warn them? Surah Al-Maun, in ninety seconds.']),
    dict(layers=[intro_sky, intro_mid, intro_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Surah 107', text='Al-Ma\'un = Small kindnesses', after=0, y=600, size=70),
         lines=['Surah one hundred and seven. Seven verses, revealed in Makkah.']),
    dict(layers=[deny_sky, deny_mid, deny_near], fx=['twinkle'], cam='in',
         verse=dict(key='107:1', line=0, ar_size=92),
         lines=['Have you seen the one who denies the Recompense?', 'He does not believe he will be judged. So watch how he acts.']),
    dict(layers=[orphan_sky, orphan_mid, orphan_near], fx=['dust'], cam='hold',
         verse=dict(key='107:2', line=0, ar_size=96),
         lines=['For that is the one who drives away the orphan.']),
    dict(layers=[food_sky, food_mid, food_near], fx=['dust'], cam='up',
         verse=dict(key='107:3', line=0, ar_size=92),
         lines=['And does not encourage the feeding of the poor.', 'He will not feed them. He will not even ask others to.']),
    dict(layers=[woe_sky, woe_mid, woe_near], fx=['dust'], cam='in', pause=0.6,
         verse=dict(key='107:4', line=1, ar_size=110),
         lines=['Then comes the shock.', 'So woe to those who pray.']),
    dict(layers=[heed_sky, heed_mid, heed_near], fx=['twinkle'], cam='in',
         verse=dict(key='107:5', line=0, ar_size=92),
         lines=['Who are heedless of their prayer.',
                'Ibn Abbas said: they pray in public, but not in private.',
                'A scholar noticed: heedless of their prayer, not in it. A wandering mind is not the point.']),
    dict(layers=[show_sky, show_mid, show_near], fx=['dust'], cam='out',
         verse=dict(key='107:6', line=0, ar_size=104),
         lines=['Those who make show of their deeds.', 'They pray for people to see, not for Allah.']),
    dict(layers=[maun_sky, maun_mid, maun_near], fx=['dust'], cam='hold', bloom=.6,
         verse=dict(key='107:7', line=0, ar_size=104),
         lines=['And withhold simple assistance.', 'Ibn Masud said this means an axe, a pot, a bucket. Things neighbours lend each other.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='Pray for Allah. Be kind to people.', after=0, y=580, size=78),
         lines=['Faith is not only on the prayer mat.', 'Pray for Allah. And be kind to people, even with a pot.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Surah in 90 Seconds', line2='Understand, Memorize & Perfect'),
         lines=['Share this with someone who is learning the Quran.', 'And follow Surah in Ninety Seconds for the next surah.']),
]

HITS = [(5, 1, 0.0), (8, 1, 0.0)]
PRON = {'Maun': 'mɑːʕˈuːn', 'Abbas': 'ɐbbˈɑːs', 'Masud': 'mɑsʕˈuːd'}
