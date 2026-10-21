"""Surah in 90 Seconds: Surah Al-Masad (111). Quran text only from data/quran.json (Saheeh International).
Reason for revelation: Sahih al-Bukhari 4971 (Ibn Abbas: the Prophet called Quraysh from As-Safa, asked if they would
believe him about horsemen/an enemy coming, they said they had never known him to lie, he warned of a severe punishment,
Abu Lahab rejected him, and the surah was revealed). Confirmed on sunnah.com/bukhari:4971 on 2026-10-21.
Abu Lahab was the Prophet's uncle (Ibn Kathir, Tafsir of 111). He is the only opponent of the Prophet named in the Quran.
He lived for years after the surah (early Makkan revelation; he died after Badr) and never believed.
"Lahab" = flame (111:1 and 111:3 share the word). His wife is not named (the Quran does not name her).
Left out on purpose: the Asma' narration (Ibn Abi Hatim) and the "thorns in the path" view, to stay with what is firm.
No people, prophets or angels drawn: hill, valley, fire, firewood, palm rope, coins only. No music."""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Surah in 90 Seconds  ·  111'
VOICE, SPEED = 'bm_george', 1.0
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah Al-Masad in 90 Seconds: The Uncle Named in the Quran'
HITS = [(3, 1, 0.0), (8, 2, 0.0)]
AYAH1 = quran()['verses']['111:1']['ar']
PRON = {'Lahab': 'lˈæhæb', 'Masad': 'mˈæsæd', 'Safa': 'sˈɑːfɑː', 'Makkah': 'mˈækkɐ'}

# ---------------------------------------------------------------- small helpers for this surah
def firewood(p, cx, base, s, col=(92, 60, 36), dark=(48, 30, 18), seed=5):
    """A bound bundle of firewood lying on the ground (object only)."""
    rnd = random.Random(seed)
    for k in range(9):
        y = base - 40 * s - (k % 3) * 34 * s - (k // 3) * 18 * s; dx = rnd.uniform(-20, 20) * s
        x0, x1 = cx - 230 * s + dx, cx + 230 * s + dx
        p.line([(x0, y + rnd.uniform(-10, 10) * s), (x1, y + rnd.uniform(-10, 10) * s)], dark, 34 * s)
        p.line([(x0, y - 6 * s), (x1, y - 6 * s)], col, 22 * s)
        p.ell(x1, y, 17 * s, 17 * s, (150, 110, 70)); p.ell(x1, y, 8 * s, 8 * s, (110, 76, 44))
    for x in (cx - 110 * s, cx + 110 * s):                       # two cords of palm fibre around the bundle
        p.line([(x - 8 * s, base - 150 * s), (x + 8 * s, base - 10 * s)], (170, 130, 80), 12 * s)
    for k in range(6):                                           # thorny twigs sticking out
        x = cx + rnd.uniform(-200, 200) * s; y = base - 130 * s
        p.line([(x, y), (x + rnd.uniform(-50, 50) * s, y - 70 * s)], dark, 5 * s)

def rope_coil(p, cx, cy, s, col=(176, 132, 82), shade=(110, 78, 44)):
    """A coil of twisted palm-fibre rope (masad)."""
    for r in range(5, 0, -1):
        rx, ry = 70 * s * r, 26 * s * r
        pts = [(cx + rx * math.cos(a / 40 * 2 * math.pi), cy + ry * math.sin(a / 40 * 2 * math.pi)) for a in range(41)]
        p.line(pts, shade, 30 * s); p.line(pts, col, 20 * s)
        for a in range(0, 40, 2):                                # the twist: short diagonal strokes along the strand
            t = a / 40 * 2 * math.pi; x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
            p.line([(x - 7 * s, y - 7 * s), (x + 7 * s, y + 7 * s)], shade, 4 * s)
    p.line([(cx + 350 * s, cy), (cx + 470 * s, cy - 90 * s), (cx + 520 * s, cy - 60 * s)], shade, 30 * s)
    p.line([(cx + 350 * s, cy), (cx + 470 * s, cy - 90 * s), (cx + 520 * s, cy - 60 * s)], col, 20 * s)

def coins(p, cx, base, s, seed=9):
    """A heap of gold coins with a soft shine."""
    rnd = random.Random(seed)
    p.glow(cx, base - 80 * s, 360 * s, (255, 200, 90), .45)
    for k in range(70):
        r = (1 - (k / 70)) ** .7
        x = cx + rnd.uniform(-1, 1) * 260 * s * r; y = base - (k / 70) * 170 * s + rnd.uniform(-8, 8) * s
        p.ell(x, y, 34 * s, 13 * s, (150, 100, 30)); p.ell(x, y - 4 * s, 32 * s, 11 * s, (240, 190, 80)); p.ell(x - 6 * s, y - 6 * s, 10 * s, 3 * s, (255, 240, 180))

# ---------------------------------------------------------------- layer painters (1080x1920)
def hook_sky(p):
    p.sky([(0, (10, 4, 6)), (.45, (60, 18, 16)), (.7, (170, 70, 30)), (.82, (240, 140, 60)), (1, (30, 10, 8))])
    p.glow(540, 1300, 600, (255, 120, 40), .5)
def hook_mid(p): mountains(p, 1300, 260, (40, 16, 14), 2, rim=(255, 140, 70))
def hook_near(p): dunes(p, 1480, 16, (60, 26, 18), (14, 6, 6), 3)

def intro_sky(p):
    p.sky([(0, (20, 30, 50)), (.45, (90, 100, 110)), (.7, (210, 170, 110)), (1, (70, 50, 30))])
    sun(p, 820, 900, 60, (255, 230, 170)); p.glow(820, 900, 420, (255, 200, 120), .5)
def intro_mid(p):
    for x in (120, 330, 760, 960): palm(p, x, 1640, 260 + (x % 3) * 30, (40, 30, 24), lean=.1 if x < 540 else -.08)
def intro_near(p): dunes(p, 1500, 12, (120, 90, 60), (40, 28, 18), 12)

def safa_sky(p):
    p.sky([(0, (14, 20, 50)), (.4, (70, 80, 130)), (.66, (240, 170, 120)), (.78, (255, 210, 150)), (1, (60, 40, 40))])
    sun(p, 300, 1230, 52, (255, 235, 190)); p.glow(300, 1230, 460, (255, 190, 120), .55)
def safa_mid(p):
    rnd = random.Random(21)
    for cx, w, h, col in ((200, 700, 260, (78, 58, 64)), (900, 800, 300, (70, 52, 60)), (560, 520, 380, (92, 66, 66))):   # low rounded rocky hills
        pts = [(cx + w / 2 * math.cos(math.pi * k / 30), 1420 - h * math.sin(math.pi * k / 30) ** .8 + rnd.uniform(-8, 8)) for k in range(31)]
        p.poly(pts + [(cx - w / 2, 1500), (cx + w / 2, 1500)], col)
    p.glow(560, 1050, 160, (255, 210, 160), .35)                 # first light on the top of the small hill
def safa_near(p):
    rnd = random.Random(22); p.rect(-100, 1470, 1200, 2300, (34, 24, 30))
    for k in range(16):                                          # low, flat-roofed old houses of the valley
        x = -40 + k * 75 + rnd.uniform(-10, 10); w = rnd.uniform(60, 90); h = rnd.uniform(50, 110)
        p.rect(x, 1500 - h, x + w, 1520, (40 + k % 3 * 6, 28, 32))
        if rnd.random() < .6: p.rect(x + w * .35, 1500 - h * .6, x + w * .55, 1500 - h * .35, (255, 200, 120))
    dunes(p, 1560, 8, (40, 28, 32), (12, 8, 10), 23)

def ruin_sky(p):
    p.sky([(0, (6, 4, 6)), (.5, (40, 14, 12)), (.78, (120, 40, 20)), (1, (16, 6, 6))])
    stars(p, 60, 31, 700, col=(255, 200, 170))
def ruin_mid(p): mountains(p, 1320, 220, (30, 12, 12), 32, rim=(200, 80, 40))
def ruin_near(p): dunes(p, 1500, 20, (40, 16, 12), (10, 4, 4), 33)

def wealth_sky(p):
    p.sky([(0, (10, 8, 20)), (.5, (40, 28, 40)), (1, (14, 10, 12))])
def wealth_mid(p): coins(p, 540, 1520, 1.2)
def wealth_near(p): dunes(p, 1560, 8, (34, 24, 24), (10, 8, 8), 42)

def fire_sky(p):
    p.sky([(0, (8, 2, 2)), (.5, (60, 12, 6)), (.8, (160, 50, 16)), (1, (30, 8, 4))])
    p.glow(540, 1400, 700, (255, 100, 30), .6)
def fire_near(p): dunes(p, 1560, 10, (30, 8, 4), (8, 2, 2), 52)

def wood_sky(p):
    p.sky([(0, (16, 12, 26)), (.5, (60, 40, 50)), (.8, (150, 90, 60)), (1, (30, 20, 16))])
    moon(p, 820, 330, 50, col=(255, 220, 180))
def wood_mid(p): firewood(p, 540, 1500, 1.15)
def wood_near(p): dunes(p, 1560, 8, (60, 40, 30), (20, 12, 10), 62)

def rope_sky(p):
    p.sky([(0, (24, 30, 40)), (.5, (90, 80, 70)), (.8, (190, 140, 90)), (1, (50, 36, 24))])
    p.glow(540, 1350, 520, (255, 190, 110), .4)
def rope_mid(p):
    for x in (110, 970): palm(p, x, 1600, 520, (36, 28, 22), lean=.06 if x < 540 else -.06)
    rope_coil(p, 470, 1420, .95)
def rope_near(p): dunes(p, 1600, 8, (100, 74, 50), (36, 26, 18), 72)

def sign_sky(p):
    p.sky([(0, (4, 6, 18)), (.5, (16, 22, 50)), (.8, (40, 40, 70)), (1, (8, 8, 16))])
    stars(p, 300, 81, 1200); moon(p, 540, 1040, 60, crescent=False, col=(240, 236, 220)); p.glow(540, 1040, 380, (200, 210, 255), .35)
def sign_near(p): dunes(p, 1480, 18, (24, 22, 40), (6, 6, 12), 82)

def lesson_sky(p):
    p.sky([(0, (40, 80, 150)), (.45, (150, 170, 200)), (.7, (255, 210, 160)), (1, (140, 100, 70))])
    sun(p, 540, 1250, 80, (255, 245, 215)); p.glow(540, 1250, 520, (255, 225, 170), .55)
def lesson_mid(p): mosque(p, 540, 1580, 1.0, (120, 90, 80), windows=(255, 220, 150))
def lesson_near(p): dunes(p, 1500, 12, (200, 160, 120), (110, 80, 60), 93)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): mosque(p, 540, 1580, .9, (22, 18, 36), windows=(255, 200, 120))
def end_near(p): dunes(p, 1500, 12, (34, 28, 50), (10, 8, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['embers'], cam='in', bloom=.65,
         title=dict(text='Named in the Quran', arabic=AYAH1, hold=99, plain=True),
         lines=['Only one of the Prophet\'s enemies is named in the Quran.', 'He was his own uncle. Surah Al-Masad, in ninety seconds.']),
    dict(layers=[intro_sky, intro_mid, intro_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Surah 111', text='Al-Masad = Palm Fibre', after=0, y=600, size=76),
         lines=['Surah one hundred and eleven. Five verses, revealed in Makkah.', 'Al-Masad means palm fibre, the rope in its last verse.']),
    dict(layers=[safa_sky, safa_mid, safa_near], fx=['dust'], cam='right',
         lesson=dict(kicker='Sahih al-Bukhari 4971', text='The warning from Safa', after=0, y=560, size=72),
         lines=['The Prophet Muhammad, peace and blessings be upon him, climbed the hill of Safa and called his people.',
                'If I said horsemen were coming to attack, would you believe me? They said, you never lie.',
                'He warned them of a severe punishment. His uncle, Abu Lahab, rejected him in front of everyone.'], pause=0.5),
    dict(layers=[ruin_sky, ruin_mid, ruin_near], fx=['embers'], cam='in',
         verse=dict(key='111:1', ar_size=90),
         lines=['Then Allah revealed:', 'May the hands of Abu Lahab be ruined, and ruined is he.']),
    dict(layers=[wealth_sky, wealth_mid, wealth_near], fx=['twinkle'], cam='out',
         verse=dict(key='111:2', ar_size=90),
         lines=['Verse two.', 'His wealth will not avail him, or that which he gained.', 'His money and status could not save him.']),
    dict(layers=[fire_sky, fire_near], fx=[('flames', dict(cx=540, base=1620, w=640, h=360)), 'embers'], cam='hold', bloom=.7,
         verse=dict(key='111:3', ar_size=96),
         lines=['Verse three.', 'He will burn in a Fire of blazing flame.', 'Lahab means flame. His nickname became his end.']),
    dict(layers=[wood_sky, wood_mid, wood_near], fx=['dust'], cam='left',
         verse=dict(key='111:4', ar_size=96),
         lines=['Verse four.', 'And his wife as well, the carrier of firewood.', 'She stood with her husband against the truth.']),
    dict(layers=[rope_sky, rope_mid, rope_near], fx=['dust'], cam='in',
         verse=dict(key='111:5', ar_size=96),
         lines=['Verse five.', 'Around her neck is a rope of twisted fibre.', 'That fibre is masad, the name of this surah.']),
    dict(layers=[sign_sky, sign_near], fx=['twinkle'], cam='out', pause=0.5,
         lesson=dict(kicker='A sign', text='Years passed. He never believed.', after=1, y=580, size=74),
         lines=['Abu Lahab lived for years after this surah.', 'To prove it wrong, he only had to believe.', 'He never did.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='Wealth and family cannot save you. Faith can.', after=0, y=580, size=72),
         lines=['Wealth and family cannot save anyone.', 'Only faith and good deeds can.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Surah in 90 Seconds', line2='Understand, Memorize & Perfect'),
         lines=['Share this with someone who is learning the Quran.', 'And follow Surah in Ninety Seconds for the next surah.']),
]
