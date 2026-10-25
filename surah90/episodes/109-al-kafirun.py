"""Surah in 90 Seconds: Surah Al-Kafirun (109). Quran text only from data/quran.json (Saheeh International).
Background (Ibn Kathir, Tafsir of 109, given by Juman from quran.com): "It has been said" that Quraysh invited the Prophet
to worship their idols for a year and they would worship his God for a year; so the surah was revealed. Narrated as
"Ibn Kathir mentions", not as a firm report. Verses 2-5: Ibn Kathir explains the disavowal covers both WHAT is worshipped
(Allah alone, no partner) and HOW (as Allah legislated). 109:6 = a complete disavowal of shirk (Ibn Kathir).
Sunnah: Sahih Muslim 726 (Abu Hurayrah: the Prophet recited 109 and 112 in the two rak'ahs of dawn, i.e. the sunnah before
Fajr). Confirmed on sunnah.com/muslim:726 on 2026-10-25. "Quarter of the Quran" report left out (weaker chain).
No people, prophets or idols drawn. No music."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Surah in 90 Seconds  ·  109'
VOICE, SPEED = 'bm_george', 0.95
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah Al-Kafirun in 90 Seconds: The Deal the Prophet Refused'
AYAH1 = quran()['verses']['109:1']['ar']

# ---------------------------------------------------------------- layer painters (1080x1920)
def hook_sky(p):
    p.sky([(0, (4, 6, 22)), (.45, (18, 22, 60)), (.72, (70, 50, 90)), (.84, (190, 110, 80)), (1, (18, 12, 20))])
    stars(p, 240, 2, 1000); moon(p, 260, 280, 50); p.glow(260, 280, 320, (200, 210, 255), .4)
def hook_mid(p): city(p, 1380, (26, 20, 34), 3, lights=(255, 190, 110), domes=False)
def hook_near(p):
    kaaba(p, 560, 1600, 1.05); p.glow(560, 1450, 520, (255, 200, 120), .25)
    dunes(p, 1640, 8, (40, 30, 40), (10, 8, 12), 4)

def offer_sky(p):
    p.sky([(0, (30, 16, 20)), (.5, (110, 50, 40)), (.75, (230, 130, 70)), (1, (40, 20, 18))])
    sun(p, 540, 1300, 90, (255, 190, 120)); p.glow(540, 1300, 520, (255, 140, 80), .6)
def offer_mid(p): mountains(p, 1320, 260, (60, 30, 30), 11, rim=(255, 170, 110))
def offer_near(p):
    dunes(p, 1490, 14, (90, 50, 40), (26, 14, 12), 12)
    for x in (160, 920): palm(p, x, 1600, 320, (20, 12, 12), lean=.07 if x < 540 else -.07)

def say_sky(p):
    p.sky([(0, (6, 10, 30)), (.5, (24, 34, 80)), (.78, (70, 80, 130)), (1, (8, 12, 28))])
    stars(p, 160, 21, 900); rays(p, 540, -120, (255, 236, 190), n=9, spread=40, a=.2, seed=22)
def say_near(p): sea(p, 1320, (30, 46, 86), (6, 10, 24), 23, lines=(255, 230, 180))

def no1_sky(p):
    p.sky([(0, (10, 8, 24)), (.5, (40, 26, 60)), (.8, (120, 70, 90)), (1, (12, 8, 16))])
    stars(p, 120, 31, 800); p.glow(540, 1150, 500, (255, 200, 140), .35)
def no1_mid(p): mountains(p, 1300, 360, (40, 26, 46), 32, rim=(220, 150, 140), peaks=3)
def no1_near(p): dunes(p, 1480, 16, (60, 40, 60), (14, 10, 16), 33)

def no2_sky(p):
    p.sky([(0, (4, 12, 30)), (.5, (16, 44, 80)), (.78, (60, 110, 140)), (1, (6, 14, 26))])
    stars(p, 200, 41, 1000); moon(p, 780, 360, 60)
def no2_near(p): sea(p, 1260, (20, 50, 84), (4, 12, 24), 42, lines=(220, 235, 255))

def ever_sky(p):
    p.sky([(0, (2, 2, 12)), (.5, (12, 10, 40)), (.8, (40, 24, 70)), (1, (6, 4, 16))])
    stars(p, 520, 51, 1700); stars(p, 120, 52, 1700, col=(200, 210, 255))
    p.glow(380, 760, 520, (140, 110, 220), .35); p.glow(700, 980, 420, (90, 140, 230), .3)
def ever_near(p): dunes(p, 1560, 10, (22, 18, 40), (6, 4, 12), 53)

def ever2_sky(p):
    p.sky([(0, (6, 4, 20)), (.5, (30, 18, 54)), (.8, (90, 50, 90)), (1, (10, 6, 16))])
    stars(p, 360, 61, 1300); p.glow(540, 900, 600, (200, 140, 255), .3)
def ever2_mid(p): mountains(p, 1360, 220, (30, 20, 44), 62, rim=(190, 150, 230))
def ever2_near(p): dunes(p, 1520, 12, (36, 24, 50), (8, 6, 14), 63)

def line_sky(p):
    p.sky([(0, (20, 30, 70)), (.4, (90, 110, 170)), (.7, (240, 190, 140)), (1, (60, 50, 60))])
    rays(p, 540, -100, (255, 236, 190), n=13, spread=70, a=.2, seed=71)
    p.glow(540, 1200, 600, (255, 220, 160), .45)
def line_mid(p):                                           # one straight path of light running to the horizon
    p.poly([(500, 1250), (580, 1250), (900, 1920), (180, 1920)], (255, 220, 160), a=90)
    p.glow(540, 1250, 120, (255, 240, 200), .9)
def line_near(p):
    dunes(p, 1480, 12, (110, 90, 100), (34, 26, 32), 73)
    p.poly([(520, 1480), (560, 1480), (760, 1920), (320, 1920)], (255, 225, 170), a=120)

def fajr_sky(p):
    p.sky([(0, (8, 10, 34)), (.45, (40, 50, 110)), (.7, (170, 130, 160)), (.82, (255, 190, 140)), (1, (40, 26, 30))])
    stars(p, 120, 81, 700); p.glow(540, 1350, 600, (255, 190, 130), .55)
def fajr_mid(p): mosque(p, 540, 1580, 1.1, (30, 22, 36), windows=(255, 205, 130))
def fajr_near(p): dunes(p, 1520, 10, (50, 36, 46), (14, 10, 14), 83)

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
def lesson_near(p): dunes(p, 1470, 14, (200, 160, 120), (110, 80, 60), 93)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): mosque(p, 540, 1580, .9, (22, 18, 36), windows=(255, 200, 120))
def end_near(p): dunes(p, 1500, 12, (34, 28, 50), (10, 8, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle'], cam='in', bloom=.65,
         title=dict(text='They offered him a deal', arabic=AYAH1, hold=99, plain=True),
         lines=['What if someone offered you a deal on your faith?', 'Surah Al-Kafirun, in ninety seconds.']),
    dict(layers=[offer_sky, offer_mid, offer_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Surah 109', text='One year our gods. One year yours?', after=1, y=600, size=70),
         lines=['Surah one hundred and nine. Six verses, revealed in Makkah.',
                'Ibn Kathir mentions an offer from the leaders of Quraysh.',
                'Worship our idols for one year, and we will worship your Lord for one year.']),
    dict(layers=[say_sky, say_near], fx=['twinkle'], cam='in',
         verse=dict(key='109:1', line=1, ar_size=100),
         lines=['Allah sent the answer.', 'Say, O disbelievers.']),
    dict(layers=[no1_sky, no1_mid, no1_near], fx=['dust'], cam='up',
         verse=dict(key='109:2', line=1, ar_size=100),
         lines=['Verse two.', 'I do not worship what you worship.']),
    dict(layers=[no2_sky, no2_near], fx=['twinkle'], cam='in',
         verse=dict(key='109:3', line=1, ar_size=96),
         lines=['Verse three.', 'Nor are you worshippers of what I worship.', 'They did not worship Allah alone.']),
    dict(layers=[ever_sky, ever_near], fx=['twinkle'], cam='out',
         verse=dict(key='109:4', line=1, ar_size=96),
         lines=['Then it repeats, for the future.', 'Nor will I be a worshipper of what you worship.']),
    dict(layers=[ever2_sky, ever2_mid, ever2_near], fx=['twinkle'], cam='in',
         verse=dict(key='109:5', line=0, ar_size=96),
         lines=['Nor will you be worshippers of what I worship.', 'Not this year. Not next year. Not ever.']),
    dict(layers=[line_sky, line_mid, line_near], fx=['dust'], cam='in', pause=0.5, bloom=.6,
         verse=dict(key='109:6', line=1, ar_size=104),
         lines=['Verse six.', 'For you is your religion, and for me is my religion.', 'A clear line. No mixing in worship.']),
    dict(layers=[fajr_sky, fajr_mid, fajr_near], fx=['dust'], cam='up',
         lesson=dict(kicker='Sunnah', text='Before Fajr: 109 + 112', after=0, y=580, size=78),
         lines=['The Prophet, peace be upon him, recited this surah in the two units of prayer before Fajr,',
                'together with Surah Al-Ikhlas.']),
    dict(layers=[mem_sky, mem_mid, mem_near], fx=['dust'], cam='hold',
         lesson=dict(kicker='Memorize', text='Each verse 3 times. Then join them.', after=1, y=560, size=72),
         lines=['Memorize it today. Watch the pattern: I do not, nor do you, then again.',
                'Read each verse three times. Then join them.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out', bloom=.6,
         lesson=dict(text='Your faith is not for trade.', after=0, y=580),
         lines=['Your faith is not for trade.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Surah in 90 Seconds', line2='Understand, Memorize & Perfect'),
         lines=['Share this with someone who is learning the Quran.', 'And follow Surah in Ninety Seconds for the next surah.']),
]

HITS = [(2, 1, 0.0), (7, 1, 0.0)]
PRON = {'Kafirun': 'kˈɑːfɪɹuːn', 'Quraysh': 'kʊɹˈeɪʃ', 'Fajr': 'fˈædʒɹ', 'Ikhlas': 'ɪxlˈɑːs'}
