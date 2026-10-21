"""Surah in 90 Seconds: Surah Al-Ikhlas (112). Quran text only (data/quran.json, Saheeh International).
Explanations stay close to the verses' own words and the common, uncontested meaning:
One = no partner (112:1), As-Samad = the Eternal Refuge whom all need (112:2), no children and no parents (112:3),
nothing equivalent to Him (112:4); "the First and the Last" (57:3) for "no beginning and no end".
No hadith used (could not be verified on sunnah.com in this session). No people, angels or prophets drawn.
No music: voice + soft ambience only. The Arabic is shown on screen; there is no recitation audio."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Surah in 90 Seconds  ·  112'
VOICE, SPEED = 'bm_george', 0.92
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah Al-Ikhlas in 90 Seconds: Who Is Allah?'
HITS = [(2, 1, 0.0), (7, 1, 0.0)]
AYAH1 = quran()['verses']['112:1']['ar']

# ---------------------------------------------------------------- layer painters (1080x1920)
def hook_sky(p):
    p.sky([(0, (4, 8, 28)), (.45, (16, 26, 66)), (.72, (70, 60, 110)), (.84, (210, 140, 100)), (1, (20, 14, 24))])
    stars(p, 260, 1, 1050); moon(p, 820, 260, 54); p.glow(820, 260, 340, (200, 210, 255), .4)
def hook_mid(p): mountains(p, 1260, 180, (28, 24, 48), 2, rim=(140, 120, 170))
def hook_near(p): dunes(p, 1460, 16, (46, 36, 60), (12, 10, 18), 3)

def intro_sky(p):
    p.sky([(0, (30, 40, 90)), (.45, (120, 110, 160)), (.68, (250, 170, 120)), (.8, (255, 210, 150)), (1, (60, 40, 40))])
    sun(p, 540, 1290, 70, (255, 225, 170)); p.glow(540, 1290, 480, (255, 180, 110), .6)
def intro_mid(p): mosque(p, 540, 1560, 1.15, (40, 28, 40), windows=(255, 200, 120))
def intro_near(p): dunes(p, 1480, 12, (80, 56, 60), (24, 16, 20), 12)

def one_sky(p):
    p.sky([(0, (6, 12, 34)), (.5, (20, 36, 80)), (.78, (60, 90, 140)), (1, (8, 14, 30))])
    stars(p, 140, 21, 900)
    p.glow(540, 1260, 620, (255, 230, 170), .55); sun(p, 540, 1260, 46, (255, 245, 215))   # one single light
def one_near(p): sea(p, 1300, (30, 50, 90), (6, 12, 26), 22, lines=(255, 230, 180))

def refuge_sky(p):
    p.sky([(0, (20, 30, 70)), (.4, (90, 110, 170)), (.7, (230, 190, 150)), (1, (70, 60, 70))])
    rays(p, 540, -100, (255, 236, 190), n=11, spread=60, a=.18, seed=31)
    clouds(p, 32, 250, 700, (255, 225, 190), 6, 120)
def refuge_mid(p): mountains(p, 1240, 300, (60, 56, 86), 33, rim=(255, 210, 160))
def refuge_near(p):
    dunes(p, 1470, 14, (100, 84, 96), (30, 24, 30), 34)
    for x in (180, 920): palm(p, x, 1560, 300, (24, 20, 26), lean=.08 if x < 540 else -.08)

def endless_sky(p):
    p.sky([(0, (2, 2, 12)), (.5, (12, 10, 40)), (.8, (40, 24, 70)), (1, (6, 4, 16))])
    stars(p, 520, 41, 1700); stars(p, 120, 42, 1700, col=(200, 210, 255))
    p.glow(380, 760, 520, (140, 110, 220), .35); p.glow(700, 980, 420, (90, 140, 230), .3)
def endless_near(p): dunes(p, 1560, 10, (22, 18, 40), (6, 4, 12), 43)

def nothing_sky(p):
    p.sky([(0, (4, 10, 30)), (.5, (20, 40, 80)), (.74, (80, 110, 150)), (1, (8, 16, 34))])
    stars(p, 200, 51, 1000); moon(p, 540, 980, 70, crescent=False, col=(255, 248, 225)); p.glow(540, 980, 420, (220, 230, 255), .4)
def nothing_near(p): sea(p, 1280, (24, 46, 84), (4, 10, 24), 52, lines=(220, 230, 255))

def mem_sky(p):
    p.sky([(0, (14, 10, 22)), (.5, (40, 26, 36)), (1, (12, 8, 12))])
    p.glow(540, 900, 700, (255, 180, 100), .35)
def mem_mid(p):
    for x in (180, 540, 900):                                   # three warm arches, like a quiet mosque corridor
        p.rect(x - 130, 1000, x + 130, 2000, (70, 46, 36)); p.ell(x, 1000, 130, 150, (70, 46, 36))
        p.rect(x - 100, 1010, x + 100, 2000, (36, 22, 18)); p.ell(x, 1010, 100, 120, (36, 22, 18))
def mem_near(p):
    for x, y in ((180, 1430), (540, 1400), (900, 1430)): lantern(p, x, y, .6, (255, 196, 110))

def lesson_sky(p):
    p.sky([(0, (40, 80, 150)), (.45, (160, 170, 200)), (.7, (255, 205, 150)), (1, (140, 100, 70))])
    sun(p, 540, 1250, 80, (255, 240, 210)); p.glow(540, 1250, 520, (255, 220, 170), .55)
def lesson_mid(p): mountains(p, 1300, 160, (150, 120, 110), 62, rim=(255, 230, 190))
def lesson_near(p): dunes(p, 1470, 14, (200, 160, 120), (110, 80, 60), 63)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 71, 900); moon(p, 820, 300, 56)
def end_mid(p): mosque(p, 540, 1580, .9, (22, 18, 36), windows=(255, 200, 120))
def end_near(p): dunes(p, 1500, 12, (34, 28, 50), (10, 8, 16), 73)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle'], cam='in', bloom=.65,
         title=dict(text='Who is Allah?', arabic=AYAH1, hold=99, plain=True),
         lines=['Who is Allah? Four short verses answer that question.', 'Surah Al-Ikhlas, in ninety seconds.']),
    dict(layers=[intro_sky, intro_mid, intro_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Surah 112', text='Al-Ikhlas = Sincerity', after=0, y=600, size=76),
         lines=['This is Surah one hundred and twelve.', 'Al-Ikhlas means sincerity. It makes our faith in Allah pure.', 'It is short, but it tells us exactly who Allah is.']),
    dict(layers=[one_sky, one_near], fx=['twinkle'], cam='in',
         verse=dict(key='112:1', line=1, ar_size=96),
         lines=['Verse one.', 'Say, He is Allah, who is One.', 'One. No partner. No second. No one shares His power.']),
    dict(layers=[refuge_sky, refuge_mid, refuge_near], fx=['dust'], cam='up',
         verse=dict(key='112:2', line=1, ar_size=104),
         lines=['Verse two.', 'Allah, the Eternal Refuge.', 'As-Samad. Everyone and everything needs Him. He needs no one.']),
    dict(layers=[endless_sky, endless_near], fx=['twinkle'], cam='out',
         verse=dict(key='112:3', line=1, ar_size=100),
         lines=['Verse three.', 'He neither begets nor is born.', 'He has no children and no parents. He is the First and the Last.']),
    dict(layers=[nothing_sky, nothing_near], fx=['twinkle'], cam='in', pause=0.5,
         verse=dict(key='112:4', line=1, ar_size=92),
         lines=['Verse four.', 'Nor is there to Him any equivalent.', 'Nothing and no one is like Him.']),
    dict(layers=[mem_sky, mem_mid, mem_near], fx=['dust'], cam='hold',
         lesson=dict(kicker='Memorize', text='Each verse 3 times. Then join them.', after=1, y=560, size=72),
         lines=['Now, memorize it. Just four verses. You can learn them today.', 'Read each verse three times. Then join them together.', 'Recite it in your next prayer, and think about what it means.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='Turn to Allah alone.', after=1, y=580),
         lines=['Four verses. One message.', 'Only Allah deserves our worship. Turn to Him alone, with a sincere heart.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Surah in 90 Seconds', line2='Understand, Memorize & Perfect'),
         lines=['Share this with someone who is learning the Quran.', 'And follow Surah in Ninety Seconds for the next surah.']),
]

PRON = {}
