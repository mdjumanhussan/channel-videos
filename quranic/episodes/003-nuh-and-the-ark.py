"""Story 3: Prophet Nuh and the Ark. Sources: Quran 29:14, 11:25-48, 71:5-7, 54:11-14, 23:27 (Saheeh International).
The Quran does not name Nuh's son, so this episode does not either. No figures are drawn: sea, sky, ship, mountains only.
Improvement tried today: a cold open. Scene 1 is the most dramatic picture of the story (the Ark in the storm) with a single
spoken hook line and no "This is the story of..." intro. The question is answered in scene 7."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  3'
VOICE, SPEED = 'bm_george', 1.0
THUMB_AT = 1.6
TITLE = 'Prophet Nuh and the Ark: "O My Son, Come Aboard"'
HITS = [(6, 1, 0.0), (7, 1, 0.0)]
# "O my son, come aboard with us", taken straight from the text of 11:42
TITLE_AR = ' '.join(quran()['verses']['11:42']['ar'].split()[12:15])

# ---------------------------------------------------------------- small scenery helpers for this story
def big_waves(p, base, height, top, bot, seed, crest=(230, 240, 245), n=4):
    """Tall rolling waves ("waves like mountains") with foam crests. Water only."""
    rnd = random.Random(seed)
    for k in range(n):
        y0 = base + k * height * .28; amp = height * (1 - k * .18)
        x0 = rnd.uniform(-300, 0); w = rnd.uniform(380, 520)
        pts = []
        x = x0 - w
        while x < 1400:
            ph = rnd.uniform(.8, 1.2)
            for j in range(13):
                u = j / 12; px = x + u * w
                py = y0 - amp * ph * (math.sin(u * math.pi) ** 1.6) * (1 - .25 * u)
                pts.append((px, py))
            x += w
        c1 = lc(top, bot, k * .15); c2 = lc(bot, (0, 0, 0), .3)
        p.grad_poly([(x0 - w, 2300)] + pts + [(1400, 2300)], c1, c2, y0 - amp, y0 + 600)
        for i in range(1, len(pts) - 1, 13):
            cx, cy = pts[i + 5] if i + 5 < len(pts) else pts[i]
            p.line(pts[i + 2:i + 9], crest, 6 - k, 200 - k * 30)
            p.ell(cx + 10, cy + 4, 26 - k * 3, 9, crest, 150)

def ark_frame(p, cx, y, s, col=(150, 104, 60), dark=(70, 44, 24)):
    """An unfinished ship on dry land: keel, ribs and a few planks. Object only."""
    p.poly([(cx - 320 * s, y - 20 * s), (cx + 320 * s, y - 20 * s), (cx + 250 * s, y + 40 * s), (cx - 250 * s, y + 40 * s)], dark)
    for i in range(-6, 7):
        x = cx + i * 48 * s; h = 170 * s * (1 - (abs(i) / 7) ** 2 * .35)
        p.line([(x, y - 20 * s), (x - 8 * s * (1 if i > 0 else -1), y - 20 * s - h)], col, 9 * s)
    for k in range(3):
        yy = y - 30 * s - k * 26 * s; ww = 300 * s - k * 6 * s
        p.line([(cx - ww, yy), (cx + ww, yy)], lc(col, (255, 230, 180), .2), 14 * s)
    for k in range(4):                                         # stacked planks beside it
        p.rect(cx + 360 * s, y + 20 * s - k * 18 * s, cx + 560 * s, y + 34 * s - k * 18 * s, lc(col, dark, k * .15))

def springs(p, xs, base, col=(170, 210, 230)):
    """Water bursting up from the ground."""
    for x in xs:
        for j in range(5):
            h = 120 + j * 30; dx = (j - 2) * 14
            p.line([(x, base), (x + dx * .5, base - h * .6), (x + dx, base - h)], col, 6, 190)
        p.ell(x, base, 60, 14, col, 200)

def peak(p, cx, base, w, h, col, snow=None):
    """A single tall mountain."""
    p.poly([(cx - w, base), (cx - w * .35, base - h * .7), (cx - w * .1, base - h * .95), (cx, base - h), (cx + w * .2, base - h * .85), (cx + w * .5, base - h * .5), (cx + w, base)], col)
    p.poly([(cx, base - h), (cx + w * .2, base - h * .85), (cx + w * .5, base - h * .5), (cx + w, base), (cx + w * .2, base)], lc(col, (0, 0, 0), .25))
    if snow: p.poly([(cx - w * .1, base - h * .95), (cx, base - h), (cx + w * .2, base - h * .85), (cx + w * .08, base - h * .8)], snow)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def storm_sky(p):
    p.sky([(0, (6, 10, 18)), (.45, (22, 36, 52)), (.7, (50, 74, 90)), (1, (8, 14, 22))])
    clouds(p, 11, 100, 900, (30, 40, 56), 12, 230); clouds(p, 12, 500, 1100, (90, 110, 130), 6, 110)
    p.glow(820, 420, 360, (200, 220, 255), .45)                # lightning glow in the clouds
def storm_back(p): big_waves(p, 1420, 300, (40, 74, 92), (10, 24, 34), 13, n=2)
def storm_ark(p):
    p.glow(540, 1440, 300, (255, 200, 120), .25)
    ark(p, 540, 1480, .95)
def storm_front(p): big_waves(p, 1600, 240, (24, 52, 70), (4, 12, 20), 14, n=3)

def call_sky(p):
    # night on the left, day on the right: "night and day"
    p.sky([(0, (14, 22, 52)), (.5, (70, 80, 120)), (.7, (230, 170, 120)), (1, (60, 40, 30))])
    p.glow(0, 500, 700, (10, 14, 40), .9); stars(p, 120, 21, 700); moon(p, 230, 360, 60)
    p.glow(900, 1150, 420, (255, 210, 140), .7); sun(p, 900, 1180, 80)
def call_mid(p): mountains(p, 1360, 240, (96, 70, 80), 22, rim=(255, 200, 150))
def call_near(p):
    dunes(p, 1560, 60, (150, 104, 74), (60, 40, 30), 23)
    palm(p, 860, 1600, 380, (40, 26, 20), -.08)

def city_sky(p):
    p.sky([(0, (24, 18, 30)), (.5, (80, 56, 66)), (.72, (196, 120, 90)), (1, (40, 24, 22))])
    clouds(p, 31, 500, 1100, (120, 70, 70), 7, 120)
def city_mid(p):
    city(p, 1420, (34, 24, 30), 32)
    for x, y in ((300, 1330), (612, 1300), (840, 1350)):          # only a few lights: "except a few"
        p.glow(x, y, 70, (255, 200, 110), .8); p.rect(x - 9, y - 12, x + 9, y + 12, (255, 214, 140))
def city_near(p): dunes(p, 1640, 50, (30, 20, 22), (8, 6, 6), 33)

def build_sky(p):
    p.sky([(0, (70, 130, 190)), (.45, (170, 200, 220)), (.66, (255, 226, 170)), (1, (150, 110, 70))])
    sun(p, 820, 520, 90); clouds(p, 41, 300, 800, (255, 250, 240), 6, 140)
def build_far(p): mountains(p, 1400, 200, (170, 150, 140), 42)
def build_mid(p):
    dunes(p, 1480, 40, (226, 186, 130), (150, 110, 70), 43)
    ark_frame(p, 470, 1470, 1.0)
def build_near(p): dunes(p, 1700, 50, (140, 100, 64), (50, 34, 22), 44)

def flood_sky(p):
    p.sky([(0, (8, 10, 16)), (.5, (26, 32, 44)), (.75, (56, 66, 80)), (1, (14, 18, 24))])
    clouds(p, 51, 0, 700, (16, 18, 26), 14, 240)
    rays(p, 540, -200, (180, 200, 230), n=10, spread=40, width=2, a=.35, angle=90, seed=52)
def flood_mid(p): mountains(p, 1380, 200, (30, 34, 44), 53)
def flood_ground(p):
    dunes(p, 1450, 30, (60, 54, 50), (24, 22, 22), 54)
    sea(p, 1560, (60, 90, 110), (14, 24, 32), 55, lines=(200, 220, 235))
    springs(p, (200, 540, 880), 1560)

def waves_sky(p):
    p.sky([(0, (10, 16, 26)), (.5, (30, 50, 70)), (.72, (70, 100, 116)), (1, (10, 18, 26))])
    clouds(p, 61, 100, 800, (24, 34, 48), 12, 220)
def waves_back(p): big_waves(p, 1330, 420, (46, 86, 104), (12, 30, 40), 62, n=2)
def waves_ark(p): ark(p, 330, 1420, .6)
def waves_front(p): big_waves(p, 1620, 320, (26, 58, 76), (4, 14, 22), 63, n=3)

def apart_sky(p):
    p.sky([(0, (16, 18, 30)), (.5, (54, 60, 82)), (.72, (120, 120, 130)), (1, (20, 22, 30))])
    clouds(p, 71, 150, 800, (40, 44, 60), 10, 200)
def apart_mid(p):
    peak(p, 780, 1520, 330, 540, (52, 50, 62))
    p.glow(780, 1000, 160, (220, 230, 255), .25)
def apart_ark(p): ark(p, 240, 1450, .45)
def apart_sea(p): sea(p, 1460, (54, 84, 100), (10, 20, 28), 72, lines=(210, 225, 240))

def drown_sky(p):
    p.sky([(0, (4, 6, 12)), (.55, (16, 22, 34)), (.75, (36, 46, 60)), (1, (6, 8, 14))])
    clouds(p, 81, 100, 1000, (14, 18, 28), 14, 240)
def drown_mid(p): peak(p, 780, 1400, 260, 260, (34, 34, 44))
def drown_front(p): big_waves(p, 1380, 420, (22, 46, 62), (2, 8, 14), 83, n=3)

def calm_sky(p):
    p.sky([(0, (80, 120, 180)), (.45, (200, 190, 200)), (.66, (255, 214, 170)), (1, (110, 90, 80))])
    rays(p, 640, 420, (255, 240, 200), n=10, spread=60, width=4, a=.35, angle=90, seed=91)
    clouds(p, 92, 200, 700, (255, 236, 220), 6, 140)
def calm_mid(p):
    peak(p, 600, 1480, 440, 520, (110, 100, 110), snow=(240, 236, 240))
    ark(p, 600, 965, .5)
def calm_sea(p): sea(p, 1480, (150, 170, 180), (60, 70, 80), 93, lines=(255, 245, 230))

def lesson_sky(p):
    p.sky([(0, (90, 150, 210)), (.45, (200, 220, 230)), (.66, (255, 230, 180)), (1, (120, 110, 70))])
    sun(p, 540, 1100, 100)
    rays(p, 540, 1100, (255, 240, 200), n=14, spread=360, length=1600, width=3, a=.2, angle=0, seed=101)
def lesson_mid(p): mountains(p, 1300, 200, (100, 130, 110), 102)
def lesson_near(p):
    dunes(p, 1480, 50, (110, 150, 90), (50, 80, 40), 103)
    tree(p, 220, 1520, 380, (60, 40, 26), (70, 120, 60), 104)
    sea(p, 1640, (120, 170, 190), (30, 60, 70), 105)

def end_sky(p):
    p.sky([(0, (4, 12, 26)), (.45, (16, 40, 70)), (.66, (60, 100, 120)), (.74, (200, 180, 150)), (1, (10, 18, 24))])
    stars(p, 240, 111, 900); moon(p, 820, 300, 56)
def end_mid(p):
    mosque(p, 540, 1340, 1.0, (8, 20, 34), windows=(255, 206, 130))
    sea(p, 1360, (20, 44, 60), (4, 10, 18), 112, lines=(200, 220, 240))
def end_near(p): lantern(p, 160, 1160, .9)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[storm_sky, storm_back, storm_ark, storm_front], fx=['rain', 'twinkle'], cam='in', bloom=.6,
         title=dict(kicker='Story 3  ·  from the Quran', text='What did his son say?', arabic=TITLE_AR, hold=99),
         lines=['A prophet called his son onto the Ark. What did his son say?']),
    dict(layers=[call_sky, call_mid, call_near], fx=['twinkle', 'dust'], cam='right',
         verse=dict(key='29:14', ar=(5, 12), en='he remained among them a thousand years minus fifty years', line=1, ar_size=80),
         lines=['Nuh, peace be upon him, called his people.', 'He remained among them a thousand years minus fifty years.']),
    dict(layers=[city_sky, city_mid, city_near], fx=['dust'], cam='in',
         lines=['Only a few believed.']),
    dict(layers=[build_sky, build_far, build_mid, build_near], fx=['dust'], cam='up',
         lines=['Allah told him to build a ship.', 'The chiefs mocked him.']),
    dict(layers=[flood_sky, flood_mid, flood_ground], fx=['rain'], cam='in', bloom=.5,
         verse=dict(key='54:11', en='Then We opened the gates of the heaven with rain pouring down', line=0, ar_size=84),
         lines=['Then We opened the gates of the heaven with rain pouring down.']),
    dict(layers=[waves_sky, waves_back, waves_ark, waves_front], fx=['rain'], cam='left', pause=0.5,
         verse=dict(key='11:42', ar=(12, 19), en='O my son, come aboard with us and be not with the disbelievers', line=1, ar_size=80),
         lines=['Nuh called to his son:', 'O my son, come aboard with us, and be not with the disbelievers.']),
    dict(layers=[apart_sky, apart_mid, apart_ark, apart_sea], fx=['rain'], cam='in',
         verse=dict(key='11:43', ar=(1, 7), en='I will take refuge on a mountain to protect me from the water', line=1, ar_size=84),
         lines=['His son said:', 'I will take refuge on a mountain to protect me from the water.']),
    dict(layers=[drown_sky, drown_mid, drown_front], fx=['rain'], cam='out', bloom=.4,
         verse=dict(key='11:43', ar=(8, 17), en='There is no protector today from the decree of Allah, except for whom He gives mercy', line=1, ar_size=76),
         lines=['Nuh said:', 'There is no protector today from the decree of Allah, except for whom He gives mercy.', 'And the waves came between them, and he was among the drowned.']),
    dict(layers=[calm_sky, calm_mid, calm_sea], fx=['dust'], cam='up',
         verse=dict(key='11:44', ar=(1, 6), en='O earth, swallow your water, and O sky, withhold [your rain]', line=1, ar_size=84, y=560),
         lines=['Then it was said:', 'O earth, swallow your water, and O sky, withhold your rain.', 'And the ship came to rest on Judiyy.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='in',
         lines=['No mountain can save you.', "Only Allah's mercy can."]),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'dust'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone you love. And follow for a new story from the Quran every day.']),
]

PRON = {'Judiyy': 'dʒuːdˈiː'}

CAPTION = """A prophet called his own son onto the Ark. What did his son say? 🤍

Nuh (peace be upon him) called his people to Allah for "a thousand years minus fifty years." (Quran 29:14) Only a few believed.

Allah inspired him to build a ship. The waves rose like mountains, and Nuh called to his son, who stood apart:

"O my son, come aboard with us and be not with the disbelievers." (Quran 11:42)

His son said he would take refuge on a mountain. Nuh answered: "There is no protector today from the decree of Allah, except for whom He gives mercy." (Quran 11:43)

No mountain can protect you. Only Allah's mercy can.

📖 Sources: Quran 29:14, 11:25–48, 71:5–7, 54:11–14, 23:27 (Saheeh International)
Share this with someone you love. Follow for a new story every day.

#QuranicStories #ProphetNuh #IslamicReminder"""

FIRST_COMMENT = """Which line from this story moved you most? 🤍

References: Quran, Surah Al-'Ankabut 29:14; Surah Hud 11:25–48; Surah Nuh 71:5–7; Surah Al-Qamar 54:11–14; Surah Al-Mu'minun 23:27 (Saheeh International translation). The Quran does not name Nuh's son, so we did not either."""
