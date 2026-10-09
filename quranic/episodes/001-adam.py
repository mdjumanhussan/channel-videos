"""Story 1: Prophet Adam (AS). Sources: Quran 2:30-37, 7:11-23, 15:28-29, 20:121-122 (Saheeh International)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  1'
VOICE, SPEED = 'bm_george', 0.97
THUMB_AT = 1.6
TITLE = 'Prophet Adam: The First Human and the First Repentance'

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def cosmos_sky(p):
    p.sky([(0, (6, 8, 30)), (.45, (28, 18, 70)), (.7, (120, 50, 80)), (.8, (230, 130, 90)), (1, (40, 20, 30))])
    for i in range(9): p.glow(200 + i * 90, 300 + i * 70, 260, (150, 120, 255), .10)
    stars(p, 420, 11, 1300)
    p.glow(540, 1450, 700, (255, 170, 110), .35)
def cosmos_far(p): dunes(p, 1480, 70, (70, 30, 50), (30, 14, 26), 3)
def cosmos_near(p): dunes(p, 1640, 90, (36, 16, 26), (12, 6, 10), 8)

def dawn_sky(p):
    p.sky([(0, (14, 20, 60)), (.35, (60, 60, 130)), (.55, (240, 140, 110)), (.62, (255, 200, 140)), (1, (60, 30, 30))])
    sun(p, 540, 1180, 70); clouds(p, 4, 650, 1000, (255, 170, 150), 6, 120)
def dawn_mid(p): mountains(p, 1230, 330, (70, 45, 70), 5, rim=(255, 190, 140))
def dawn_near(p): dunes(p, 1520, 80, (120, 70, 60), (40, 20, 22), 12)

def clay_sky(p):
    p.sky([(0, (24, 14, 10)), (.4, (80, 44, 26)), (.7, (170, 96, 50)), (1, (40, 22, 14))])
    rays(p, 540, -250, (255, 230, 170), n=7, spread=18, width=3, a=.5)
    p.glow(540, 1250, 520, (255, 210, 140), .55)
def clay_ground(p):
    dunes(p, 1330, 60, (150, 86, 52), (70, 38, 24), 21)
    p.glow(540, 1330, 260, (255, 235, 190), .7)
def clay_near(p):
    dunes(p, 1700, 50, (60, 32, 20), (20, 10, 6), 22)
    rnd = random.Random(6)
    for _ in range(14):
        x = rnd.choice([rnd.uniform(-60, 330), rnd.uniform(750, 1140)]); y = rnd.uniform(1640, 1900); r = rnd.uniform(18, 60)
        p.ell(x, y, r, r * .6, (44, 24, 16)); p.ell(x - r * .2, y - r * .25, r * .55, r * .25, (90, 52, 32))

def names_sky(p):
    p.sky([(0, (4, 6, 22)), (.6, (16, 24, 60)), (.85, (40, 40, 90)), (1, (10, 10, 24))])
    stars(p, 500, 31, 1500)
    rnd = random.Random(5)
    for g in range(6):
        cx, cy = rnd.uniform(150, 930), rnd.uniform(150, 1100); pts = [(cx + rnd.uniform(-170, 170), cy + rnd.uniform(-130, 130)) for _ in range(5)]
        p.line(pts, (255, 215, 130), 2, 130)
        for x, y in pts: p.glow(x, y, 28, (255, 230, 170), .8); p.ell(x, y, 4, 4, (255, 250, 230))
def names_near(p): mountains(p, 1600, 300, (10, 10, 22), 9)

def heaven_sky(p):
    p.sky([(0, (255, 236, 190)), (.4, (255, 210, 140)), (.75, (240, 160, 110)), (1, (130, 80, 70))])
    rays(p, 540, -200, (255, 255, 240), n=13, spread=80, width=4, a=.35, seed=4)
def heaven_clouds1(p):
    clouds(p, 8, 500, 900, (255, 250, 235), 8, 170)
    cloud_bank(p, 1150, (255, 248, 235), (240, 190, 160), 5, 70, 235)
def heaven_clouds2(p): cloud_bank(p, 1500, (255, 236, 215), (220, 150, 120), 9, 90, 255)

def fire_sky(p):
    p.sky([(0, (14, 4, 4)), (.5, (60, 12, 8)), (.8, (120, 30, 12)), (1, (20, 6, 4))])
    p.glow(540, 1200, 800, (255, 90, 30), .35)
def fire_mid(p):
    mountains(p, 1350, 380, (28, 8, 6), 15)
    fire(p, 540, 1460, 300, 520, 3)
def fire_near(p): dunes(p, 1640, 50, (20, 6, 4), (6, 2, 2), 30)

def garden_sky(p):
    p.sky([(0, (120, 200, 230)), (.4, (190, 225, 230)), (.62, (255, 215, 200)), (1, (80, 120, 80))])
    sun(p, 820, 520, 55, (255, 240, 200)); clouds(p, 14, 300, 700, (255, 255, 255), 6, 170)
def garden_mid(p):
    mountains(p, 1160, 200, (120, 170, 150), 4)
    for i, x in enumerate((-40, 200, 880, 1100)): tree(p, x, 1260, 360, (70, 50, 40), (60, 150, 90), 40 + i)
    p.grad_poly([(-200, 1240), (1300, 1240), (1300, 2300), (-200, 2300)], (90, 170, 90), (30, 80, 40))
def garden_near(p):
    p.grad_poly([(380, 1240), (700, 1240), (1100, 2300), (-60, 2300)], (170, 220, 240), (60, 140, 190))
    tree(p, 540, 1240, 460, (90, 60, 40), (120, 190, 110), 77, glow=(255, 240, 160))
    rnd = random.Random(2)
    for _ in range(80):
        x, y = rnd.uniform(-60, 1140), rnd.uniform(1300, 2050)
        if 300 < x < 800 and y < 1700: continue
        p.ell(x, y, 9, 9, rnd.choice([(255, 180, 200), (255, 240, 150), (250, 250, 255), (200, 150, 255)]))

def dusk_sky(p):
    p.sky([(0, (30, 20, 60)), (.4, (80, 40, 90)), (.62, (190, 90, 90)), (1, (20, 14, 26))])
    stars(p, 120, 41, 700)
def dusk_mid(p):
    mountains(p, 1160, 200, (50, 34, 60), 4)
    for i, x in enumerate((-40, 200, 880, 1100)): tree(p, x, 1260, 360, (24, 16, 22), (34, 30, 50), 40 + i)
    p.grad_poly([(-200, 1240), (1300, 1240), (1300, 2300), (-200, 2300)], (40, 34, 50), (12, 10, 16))
def dusk_near(p):
    tree(p, 540, 1240, 460, (30, 18, 18), (70, 30, 40), 77, glow=(255, 90, 70))

def night_sky(p):
    p.sky([(0, (4, 8, 24)), (.5, (18, 28, 64)), (.72, (50, 50, 96)), (1, (14, 12, 24))])
    stars(p, 380, 51, 1250); moon(p, 760, 420, 85)
def night_mid(p): dunes(p, 1420, 90, (60, 50, 80), (24, 20, 36), 61)
def night_near(p):
    dunes(p, 1640, 70, (30, 24, 40), (10, 8, 14), 62)
    lantern(p, 250, 1520, 1.25)

def sunrise_sky(p):
    p.sky([(0, (90, 120, 200)), (.35, (250, 190, 170)), (.6, (255, 220, 160)), (1, (120, 70, 50))])
    sun(p, 540, 1080, 120); rays(p, 540, 1080, (255, 240, 200), n=16, spread=360, length=1600, width=3, a=.25, angle=0, seed=9)
    clouds(p, 16, 500, 900, (255, 200, 190), 7, 150)
def sunrise_mid(p): dunes(p, 1300, 80, (230, 160, 110), (150, 90, 60), 71)
def sunrise_near(p):
    dunes(p, 1620, 90, (120, 70, 50), (40, 22, 16), 72); palm(p, 900, 1600, 420, (40, 24, 18), -.12); palm(p, 1010, 1640, 330, (40, 24, 18), .1)

def end_sky(p):
    p.sky([(0, (8, 10, 34)), (.45, (40, 34, 90)), (.66, (210, 110, 100)), (.74, (255, 170, 110)), (1, (30, 16, 20))])
    stars(p, 200, 81, 900); moon(p, 820, 300, 60)
def end_mid(p):
    city(p, 1430, (40, 24, 40), 3, lights=(255, 190, 110))
    mosque(p, 540, 1330, 1.0, (24, 14, 26), windows=(255, 200, 120))
def end_near(p):
    dunes(p, 1700, 40, (16, 10, 18), (6, 4, 8), 82); lantern(p, 150, 1150, 1.0); lantern(p, 930, 1240, .85)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[cosmos_sky, cosmos_far, cosmos_near], fx=['twinkle', 'dust'], cam='in',
         title=dict(kicker='Story 1  ·  from the Quran', text='The First Human', arabic='آدم عليه السلام', hold=4.2),
         lines=['Before a single human ever walked the Earth,', 'Allah told the angels something amazing.'], no_caption=(0, 1)),
    dict(layers=[dawn_sky, dawn_mid, dawn_near], fx=['dust'], cam='up',
         verse=dict(key='2:30', ar=(4, 9), en='Indeed, I will make upon the earth a successive authority', line=1),
         lines=['He said:', 'Indeed, I will make upon the earth a successive authority.']),
    dict(layers=[clay_sky, clay_ground, clay_near], fx=['dust'], cam='in',
         lines=['So Allah created Adam from clay.', 'He shaped him, then breathed into him the soul He created.']),
    dict(layers=[names_sky, names_near], fx=['twinkle'], cam='left',
         verse=dict(key='2:32', ar=(1, 8), en='Exalted are You; we have no knowledge except what You have taught us', line=2),
         lines=['Then Allah taught Adam the names. All of them.', 'Even the angels said:', 'Exalted are You. We have no knowledge except what You have taught us.']),
    dict(layers=[heaven_sky, heaven_clouds1, heaven_clouds2], fx=['dust'], cam='out',
         lines=['Then Allah commanded the angels to bow down to Adam.', 'They all bowed. Except one. Iblees.', 'He refused, and he was arrogant.']),
    dict(layers=[fire_sky, fire_mid, fire_near], fx=['embers'], cam='in', bloom=.7,
         verse=dict(key='7:12', ar=(8, 17), en='I am better than him. You created me from fire and created him from clay', line=1),
         lines=['His excuse?', 'I am better than him. You created me from fire, and created him from clay.', 'His pride ruined him.']),
    dict(layers=[garden_sky, garden_mid, garden_near], fx=['petals', 'dust'], cam='up',
         verse=dict(key='2:35', ar=(11, 15), en='But do not approach this tree', line=2),
         lines=['Adam and his wife lived in Paradise. They could eat freely, wherever they wished.', 'Only one thing was forbidden.', 'Do not approach this tree.']),
    dict(layers=[dusk_sky, dusk_mid, dusk_near], fx=['twinkle'], cam='in',
         lines=['But Shaytaan whispered to them.', 'He deceived them. And they ate from the tree.']),
    dict(layers=[night_sky, night_mid, night_near], fx=['twinkle', 'dust'], cam='in', pause=1.0,
         verse=dict(key='7:23', ar=(1, 99), en='Our Lord, we have wronged ourselves, and if You do not forgive us and have mercy upon us, we will surely be among the losers', line=1, ar_size=64, y=600),
         lines=['Adam did not run from his mistake. He ran back to Allah.', 'Our Lord, we have wronged ourselves. And if You do not forgive us and have mercy upon us, we will surely be among the losers.']),
    dict(layers=[sunrise_sky, sunrise_mid, sunrise_near], fx=['dust'], cam='out',
         verse=dict(key='2:37', ar=(5, 11), en='He accepted his repentance. Indeed, it is He who is the Accepting of repentance, the Merciful', line=1),
         lines=['And Allah forgave him.', 'He accepted his repentance. Indeed, it is He who is the Accepting of repentance, the Merciful.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'dust'], cam='in',
         end=dict(after=1, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['We all make mistakes. What matters is that we turn back to Allah.', 'Share this with someone who needs hope today. And follow, for a new story from the Quran every day.']),
]

CAPTION = """The very first human. The very first mistake. And the very first "I'm sorry" to Allah. 🤍

Before a single human walked the Earth, Allah told the angels: "Indeed, I will make upon the earth a successive authority." (Quran 2:30)

Adam (peace be upon him) was created from clay and taught the names of all things. Iblees refused to bow out of pride. Adam slipped, but he turned straight back to Allah with this dua:

"Our Lord, we have wronged ourselves, and if You do not forgive us and have mercy upon us, we will surely be among the losers." (Quran 7:23)

And Allah accepted his repentance. (Quran 2:37)

Mistakes don't define us. Turning back does.

📖 Sources: Quran 2:30–37, 7:11–23, 15:28–29, 20:121–122 (Saheeh International)
Share this with someone who needs hope today. Follow for a new story every day.

#QuranicStories #ProphetAdam #IslamicReminder"""
