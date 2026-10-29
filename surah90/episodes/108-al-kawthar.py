"""Surah in 90 Seconds: Surah Al-Kawthar (108). Quran text only from data/quran.json (Saheeh International).
Revelation scene + meaning of al-Kawthar: Sahih Muslim 400 (Anas: the Prophet dozed, raised his head smiling, said
"A surah has just been revealed to me", recited it; al-Kawthar is a river his Lord promised him, a pond his ummah will
come to on the Day of Resurrection, its vessels as many as the stars). Ibn Abbas: al-Kawthar is the good Allah gave
him; the river is part of it (Sahih al-Bukhari 4966). Both confirmed on 2026-10-29 (sunnah.com/bukhari:4966;
quran.com/al-kawthar/1/hadith for Muslim 400).
108:3 background (Ibn Kathir, from As-Suddi and others): when the Prophet's sons died, enemies said he was "cut off".
Several names are given for the one who said it; the video names none. Shortest surah of the Quran: 3 verses.
No people, prophets or angels drawn. No music."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Surah in 90 Seconds  ·  108'
VOICE, SPEED = 'bm_george', 0.95
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah Al-Kawthar in 90 Seconds: They Called Him "Cut Off"'
AYAH1 = quran()['verses']['108:1']['ar']

def river(p, y0, col_a, col_b, glow_col, seed, pearls=True):
    """A winding river from the horizon (y0) to the bottom, with soft light on the water and pearl domes on its banks."""
    pts_l, pts_r = [], []
    for k in range(41):
        u = k / 40; y = y0 + (1920 - y0) * u ** 1.3
        cx = 540 + 150 * math.sin(u * 5.2 + seed) * u; w = 12 + 380 * u ** 1.6
        pts_l.append((cx - w, y)); pts_r.append((cx + w, y))
    p.grad_poly(pts_l + pts_r[::-1], col_a, col_b, y0, 1920)
    p.glow(540, y0 + 20, 220, glow_col, .55)
    for k in range(6, 40, 3):
        u = k / 40; y = y0 + (1920 - y0) * u ** 1.3; cx = 540 + 150 * math.sin(u * 5.2 + seed) * u; w = (12 + 380 * u ** 1.6) * .5
        p.line([(cx - w, y), (cx + w * .6, y)], (255, 255, 255), 1 + 3 * u, a=int(40 + 60 * u))
    if pearls:
        for side in (-1, 1):
            for k in (14, 24, 34):
                u = k / 40; y = y0 + (1920 - y0) * u ** 1.3; cx = 540 + 150 * math.sin(u * 5.2 + seed) * u
                x = cx + side * (12 + 380 * u ** 1.6 + 40 + 60 * u); r = 10 + 46 * u
                p.glow(x, y - r * .5, r * 2.2, (230, 235, 255), .35)
                p.ell(x, y - r * .4, r, r * .9, (200, 210, 235)); p.ell(x - r * .3, y - r * .7, r * .3, r * .22, (255, 255, 255))

# ---------------------------------------------------------------- layer painters (1080x1920)
def hook_sky(p):
    p.sky([(0, (4, 6, 22)), (.5, (16, 18, 50)), (.8, (50, 36, 70)), (1, (10, 8, 16))])
    stars(p, 200, 2, 1000); moon(p, 800, 300, 52); p.glow(800, 300, 320, (200, 210, 255), .35)
def hook_mid(p): mountains(p, 1320, 300, (24, 18, 34), 3, rim=(150, 120, 170))
def hook_near(p):
    dunes(p, 1500, 14, (36, 28, 44), (8, 6, 12), 4)
    tree(p, 260, 1560, 300, (18, 12, 14), (26, 20, 26), 5)

def intro_sky(p):
    p.sky([(0, (30, 40, 90)), (.45, (120, 110, 160)), (.68, (250, 170, 120)), (.8, (255, 210, 150)), (1, (60, 40, 40))])
    sun(p, 540, 1290, 70, (255, 225, 170)); p.glow(540, 1290, 480, (255, 180, 110), .6)
def intro_mid(p): mountains(p, 1300, 200, (90, 64, 80), 11, rim=(255, 200, 150))
def intro_near(p): dunes(p, 1480, 12, (80, 56, 60), (24, 16, 20), 12)

def smile_sky(p):
    p.sky([(0, (10, 8, 24)), (.5, (36, 24, 50)), (1, (14, 10, 16))])
    p.glow(540, 1000, 700, (255, 200, 120), .45); rays(p, 540, -120, (255, 230, 180), n=9, spread=40, a=.16, seed=21)
def smile_mid(p): mosque(p, 540, 1600, 1.15, (34, 24, 30), windows=(255, 210, 130))
def smile_near(p):
    for x, y in ((170, 1420), (910, 1420)): lantern(p, x, y, .7, (255, 200, 110))

def v1_sky(p):
    p.sky([(0, (4, 10, 30)), (.45, (20, 40, 86)), (.62, (110, 120, 170)), (1, (10, 18, 40))])
    stars(p, 300, 31, 1200); p.glow(540, 1250, 480, (255, 236, 200), .45)
def v1_mid(p): mountains(p, 1260, 140, (20, 30, 60), 32, rim=(180, 190, 230))
def v1_near(p): river(p, 1250, (215, 225, 245), (50, 80, 140), (255, 245, 220), 1.0)

def river_sky(p):
    p.sky([(0, (2, 4, 18)), (.5, (12, 20, 60)), (.75, (60, 70, 120)), (1, (6, 10, 26))])
    stars(p, 600, 41, 1150); stars(p, 160, 42, 1150, col=(255, 230, 170))
def river_mid(p): mountains(p, 1270, 120, (14, 20, 46), 43, rim=(150, 160, 210))
def river_near(p): river(p, 1260, (225, 230, 248), (60, 90, 150), (255, 240, 210), 2.3)

def v2_sky(p):
    p.sky([(0, (8, 10, 34)), (.45, (40, 50, 110)), (.7, (170, 130, 160)), (.82, (255, 190, 140)), (1, (40, 26, 30))])
    stars(p, 120, 51, 700); p.glow(540, 1350, 600, (255, 190, 130), .55)
def v2_mid(p): mosque(p, 540, 1580, 1.0, (30, 22, 36), windows=(255, 205, 130))
def v2_near(p): dunes(p, 1520, 10, (50, 36, 46), (14, 10, 14), 53)

def v3_sky(p):
    p.sky([(0, (16, 10, 14)), (.5, (54, 30, 30)), (.8, (110, 60, 50)), (1, (20, 12, 12))])
    p.glow(540, 1200, 500, (200, 110, 80), .3)
def v3_mid(p): mountains(p, 1320, 240, (40, 24, 26), 61, rim=(170, 100, 80), peaks=4)
def v3_near(p):
    dunes(p, 1480, 18, (60, 36, 32), (16, 10, 10), 62)
    x, b = 540, 1600                                         # a bare, broken trunk: nothing grows from it
    p.poly([(x - 30, b), (x - 18, b - 300), (x + 4, b - 330), (x + 22, b - 290), (x + 30, b)], (24, 14, 12))
    p.line([(x - 10, b - 220), (x - 120, b - 320)], (24, 14, 12), 12); p.line([(x + 10, b - 170), (x + 100, b - 240)], (24, 14, 12), 10)

def adhan_sky(p):
    p.sky([(0, (30, 60, 130)), (.45, (130, 150, 200)), (.7, (255, 200, 150)), (1, (120, 80, 70))])
    rays(p, 540, 1240, (255, 236, 190), n=15, spread=170, a=.16, seed=71, angle=-90)
    sun(p, 540, 1240, 70, (255, 240, 210)); p.glow(540, 1240, 560, (255, 220, 160), .6)
def adhan_mid(p): city(p, 1440, (60, 44, 60), 72, lights=(255, 210, 140), domes=True)
def adhan_near(p): mosque(p, 540, 1640, 1.05, (40, 28, 40), windows=(255, 210, 130))

def mem_sky(p):
    p.sky([(0, (14, 10, 22)), (.5, (40, 26, 36)), (1, (12, 8, 12))])
    p.glow(540, 900, 700, (255, 180, 100), .35)
def mem_mid(p):
    for x in (180, 540, 900):
        p.rect(x - 130, 1000, x + 130, 2000, (70, 46, 36)); p.ell(x, 1000, 130, 150, (70, 46, 36))
        p.rect(x - 100, 1010, x + 100, 2000, (36, 22, 18)); p.ell(x, 1010, 100, 120, (36, 22, 18))
def mem_near(p):
    for x, y in ((180, 1430), (540, 1400), (900, 1430)): lantern(p, x, y, .6, (255, 196, 110))

def lesson_sky(p):
    p.sky([(0, (40, 80, 150)), (.45, (160, 170, 200)), (.7, (255, 205, 150)), (1, (140, 100, 70))])
    sun(p, 540, 1250, 80, (255, 240, 210)); p.glow(540, 1250, 520, (255, 220, 170), .55)
def lesson_mid(p): mountains(p, 1300, 160, (150, 120, 110), 92, rim=(255, 230, 190))
def lesson_near(p):
    dunes(p, 1470, 14, (200, 160, 120), (110, 80, 60), 93)
    for x in (170, 910): palm(p, x, 1580, 300, (90, 64, 50), lean=.07 if x < 540 else -.07)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): mosque(p, 540, 1580, .9, (22, 18, 36), windows=(255, 200, 120))
def end_near(p): dunes(p, 1500, 12, (34, 28, 50), (10, 8, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle'], cam='in', bloom=.6,
         title=dict(text='They called him "cut off"', arabic=AYAH1, hold=99, plain=True),
         lines=['His enemies said his name would be forgotten.', 'Allah answered with the shortest surah in the Quran.']),
    dict(layers=[intro_sky, intro_mid, intro_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Surah 108', text='Al-Kawthar = Abundance', after=0, y=600, size=76),
         lines=['Surah Al-Kawthar, in ninety seconds.', 'Just three verses. Al-Kawthar comes from a word that means abundance.']),
    dict(layers=[smile_sky, smile_mid, smile_near], fx=['dust'], cam='in',
         lines=['One day, the Prophet, peace be upon him, raised his head, smiling.',
                'He said, a surah has just been revealed to me.']),
    dict(layers=[v1_sky, v1_mid, v1_near], fx=['twinkle'], cam='in', bloom=.65,
         verse=dict(key='108:1', line=1, ar_size=104),
         lines=['Then he recited:', 'Indeed, We have granted you al-Kawthar.']),
    dict(layers=[river_sky, river_mid, river_near], fx=['twinkle'], cam='out',
         lesson=dict(kicker='What is Al-Kawthar?', text='A river in Paradise', after=0, y=560, size=80),
         lines=['He said it is a river his Lord promised him.',
                'His people will come to it on the Day of Resurrection. Its cups are as many as the stars.',
                'Ibn Abbas said it is all the good Allah gave him. The river is part of it.']),
    dict(layers=[v2_sky, v2_mid, v2_near], fx=['dust'], cam='up',
         verse=dict(key='108:2', line=1, ar_size=104),
         lines=['Verse two.', 'So pray to your Lord and sacrifice to Him alone.', 'A huge gift. So thank Him with worship.']),
    dict(layers=[v3_sky, v3_mid, v3_near], fx=['dust'], cam='in', pause=0.5,
         verse=dict(key='108:3', line=1, ar_size=104),
         lines=['Verse three.', 'Indeed, your enemy is the one cut off.']),
    dict(layers=[adhan_sky, adhan_mid, adhan_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(kicker='Who was cut off?', text='His name is in every call to prayer', after=1, y=560, size=66),
         lines=['When his sons died, they mocked him. Cut off. No one to carry his name.',
                'Today, his name is called in the call to prayer, every day, all over the world.']),
    dict(layers=[mem_sky, mem_mid, mem_near], fx=['dust'], cam='hold',
         lesson=dict(kicker='Memorize', text='Each verse 3 times. Then join them.', after=0, y=560, size=72),
         lines=['Three verses. You can memorize them in five minutes.', 'Read each verse three times. Then join them.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='People may mock. Allah gives.', after=0, y=580),
         lines=['People may mock you. Allah gives more than they can take.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Surah in 90 Seconds', line2='Understand, Memorize & Perfect'),
         lines=['Share this with someone who is learning the Quran.', 'And follow Surah in Ninety Seconds for the next surah.']),
]

HITS = [(3, 1, 0.0), (6, 1, 0.0)]
PRON = {'Kawthar': 'kˈaʊθɑː', 'Abbas': 'ɐbbˈɑːs'}
