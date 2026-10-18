"""Story 9: Ibrahim and Ismail build the Kabah. Sources: Quran 14:35-41, 2:125-129, 22:26, 62:2, 2:144 (Saheeh International).
No people are drawn: a dry valley, rock, sky, paths, lanterns, plain stone foundations, light, and the Kabah today.
Nothing beyond the verses: no Hajar/Zamzam story (that is hadith, not today's verses), no Black Stone, no angel,
no invented dialogue. The family left in the valley is "some of my descendants" (14:37), not named.
The answered prayer: 2:129 asks for "a messenger from themselves who will recite to them Your verses";
62:2 says Allah "has sent among the unlettered a Messenger from themselves reciting to them His verses" (the Prophet Muhammad).
Improvement tried today: a lesson card. The one-line takeaway stays on screen in big type while it is spoken
(new engine option sc['lesson']; default unchanged). Reason: a text recap in the last seconds helps sound-off viewers
and rewatches (socialk.it retention guide); it was also in our ideas queue."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  9'
VOICE, SPEED = 'bm_george', 1.1
THUMB_AT = 1.0
TITLE = 'Ibrahim and Ismail Build the Kabah: "Our Lord, Accept From Us"'
HITS = [(4, 1, 0.0), (7, 0, 0.0)]
# "the House", taken straight from the text of 2:127
TITLE_AR = quran()['verses']['2:127']['ar'].split()[5]

STONE = (196, 160, 112); STONE_D = (120, 92, 62)

# ---------------------------------------------------------------- small scenery helpers for this story
def valley_walls(p, col, rim, seed, top=900, floor=1500):
    """Steep bare rock walls on both sides of a narrow valley."""
    rnd = random.Random(seed)
    for side in (-1, 1):
        x_edge = -200 if side < 0 else 1280
        pts = [(x_edge, top - 200)]
        for k in range(7):
            f = k / 6
            x = 540 + side * lerp(620, 250, f) + rnd.uniform(-30, 30)
            pts.append((x, lerp(top, floor, f) + rnd.uniform(-40, 40)))
        pts += [(540 + side * 200, floor + 80), (540 + side * 200, 2300), (x_edge, 2300)]
        p.poly(pts, col)
        for i in range(1, 7): p.line([pts[i], pts[i + 1]], rim, 3, 110)

def path(p, x_far, y_far, x_near, base, w, col):
    """A faint track running from a far pass down to the valley floor."""
    p.poly([(x_far - 3, y_far), (x_far + 3, y_far), (x_near + w / 2, base), (x_near - w / 2, base)], col, 200)

def foundations(p, cx, base, s, courses, col=STONE, dark=STONE_D, loose=True):
    """Plain stone walls, a few courses high (an unfinished square building seen from a corner). No cloth, no decoration."""
    bh = 34 * s
    for c in range(courses):
        y1 = base - c * bh; y0 = y1 - bh + 3 * s
        x = cx - 230 * s + (c % 2) * 22 * s
        while x < cx + 40 * s:                                   # front face
            w = 58 * s; p.rect(x, y0, min(x + w - 4 * s, cx + 40 * s), y1, lc(col, (255, 255, 255), .05 * ((x // 7) % 3)))
            x += w
        x = cx + 40 * s
        while x < cx + 210 * s:                                  # side face (darker)
            w = 50 * s; p.rect(x, y0 - (x - cx - 40 * s) * .12, min(x + w - 4 * s, cx + 210 * s), y1 - (x - cx - 40 * s) * .12, dark)
            x += w
    if loose:
        for dx, dy in ((-330, 30), (-290, 40), (270, 50), (320, 36), (300, 70)):
            p.rect(cx + dx * s, base + dy * s - 30 * s, cx + dx * s + 52 * s, base + dy * s, lc(col, (0, 0, 0), .15))

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (12, 30, 60)), (.4, (40, 70, 110)), (.66, (230, 140, 80)), (.8, (255, 190, 110)), (1, (60, 36, 24))])
    sun(p, 540, 1260, 90, (255, 214, 150)); p.glow(540, 1260, 520, (255, 170, 90), .7)
def hook_mid(p): valley_walls(p, (70, 46, 36), (255, 170, 110), 1, top=820, floor=1420)
def hook_near(p):
    dunes(p, 1500, 20, (110, 74, 50), (40, 26, 18), 2)
    foundations(p, 560, 1540, 1.35, 4, (90, 62, 44), (52, 36, 26))

def valley_sky(p):
    p.sky([(0, (70, 120, 170)), (.4, (180, 200, 210)), (.7, (250, 220, 170)), (1, (200, 150, 100))])
    sun(p, 780, 520, 70, (255, 248, 220)); p.glow(780, 520, 420, (255, 240, 200), .6)
def valley_mid(p): valley_walls(p, (150, 104, 70), (255, 220, 170), 11, top=780, floor=1460)
def valley_near(p): dunes(p, 1520, 16, (214, 172, 120), (150, 110, 70), 12)

def hearts_sky(p):
    p.sky([(0, (14, 18, 46)), (.45, (50, 50, 96)), (.72, (170, 110, 120)), (1, (40, 26, 30))])
    stars(p, 160, 21, 900); moon(p, 240, 330, 50)
def hearts_mid(p):
    mountains(p, 1300, 220, (50, 40, 60), 22, rim=(210, 160, 170))
    for xf, xn in ((140, 380), (540, 540), (940, 700), (300, 460), (800, 620)):
        path(p, xf, 1180, xn, 1560, 70, (120, 96, 100))
def hearts_near(p):
    dunes(p, 1540, 20, (90, 66, 70), (30, 22, 26), 23)
    for x, y, s in ((380, 1360, .45), (700, 1320, .4), (470, 1250, .32), (610, 1230, .3), (540, 1440, .55)):
        lantern(p, x, y, s, (255, 196, 110))

def site_sky(p):
    p.sky([(0, (90, 130, 190)), (.35, (200, 200, 200)), (.7, (230, 170, 110)), (1, (110, 76, 50))])
    rays(p, 540, -200, (255, 250, 225), n=10, spread=50, length=2600, width=8, a=.24, angle=90, seed=31)
    p.glow(540, 160, 520, (255, 248, 220), .55)
def site_mid(p): valley_walls(p, (160, 118, 80), (255, 230, 180), 32, top=800, floor=1440)
def site_near(p):
    dunes(p, 1500, 14, (220, 180, 128), (150, 110, 70), 33)
    foundations(p, 560, 1600, 1.5, 3, (176, 136, 90), (110, 80, 52))

def pray_sky(p):
    p.sky([(0, (40, 40, 90)), (.4, (170, 100, 110)), (.66, (255, 170, 100)), (1, (110, 56, 40))])
    sun(p, 540, 1080, 110, (255, 220, 150))
    rays(p, 540, 1080, (255, 230, 180), n=18, spread=360, length=1700, width=3, a=.16, angle=0, seed=41)
def pray_mid(p): valley_walls(p, (110, 60, 50), (255, 190, 130), 42, top=840, floor=1440)
def pray_near(p):
    dunes(p, 1500, 14, (170, 110, 76), (80, 46, 32), 43)
    foundations(p, 560, 1560, 1.4, 6)

def night_sky(p):
    p.sky([(0, (4, 8, 26)), (.5, (14, 24, 60)), (.8, (40, 44, 90)), (1, (10, 10, 20))])
    stars(p, 240, 51, 1200); moon(p, 820, 300, 60)
    p.glow(820, 300, 360, (200, 210, 255), .4)
def night_mid(p): valley_walls(p, (24, 26, 50), (110, 120, 180), 52, top=860, floor=1440)
def night_near(p):
    dunes(p, 1500, 14, (40, 38, 60), (12, 12, 20), 53)
    foundations(p, 560, 1560, 1.4, 7, (70, 66, 90), (40, 38, 56), loose=False)
    lantern(p, 300, 1500, .6, (255, 190, 100))

def dawn_sky(p):
    p.sky([(0, (30, 60, 120)), (.45, (120, 150, 200)), (.7, (255, 200, 150)), (1, (150, 100, 70))])
    clouds(p, 61, 380, 800, (255, 230, 210), 6, 120)
    sun(p, 540, 1240, 60, (255, 240, 210))
def dawn_mid(p): valley_walls(p, (120, 96, 100), (255, 220, 190), 62, top=820, floor=1440)
def dawn_near(p):
    dunes(p, 1500, 14, (200, 160, 120), (110, 80, 60), 63)
    foundations(p, 560, 1560, 1.4, 8, loose=False)

def answer_sky(p):
    p.sky([(0, (60, 110, 180)), (.4, (170, 200, 230)), (.66, (255, 230, 180)), (1, (200, 160, 110))])
    sun(p, 540, 1180, 130, (255, 246, 210))
    rays(p, 540, 1180, (255, 250, 230), n=22, spread=360, length=1800, width=3, a=.2, angle=0, seed=71)
def answer_mid(p): valley_walls(p, (170, 130, 96), (255, 240, 200), 72, top=820, floor=1440)
def answer_near(p):
    dunes(p, 1500, 14, (226, 192, 140), (160, 120, 80), 73)
    palm(p, 170, 1620, 360, (60, 90, 50), -.05); palm(p, 920, 1600, 320, (60, 90, 50), .05)

def today_sky(p):
    p.sky([(0, (6, 10, 34)), (.45, (24, 34, 80)), (.72, (70, 70, 120)), (1, (20, 18, 30))])
    stars(p, 160, 81, 800); p.glow(540, 1180, 620, (255, 220, 160), .55)
def today_mid(p):
    city(p, 1500, (30, 30, 52), 82, lights=(255, 214, 140))
def today_near(p):
    p.grad_poly([(-200, 1500), (1280, 1500), (1280, 2300), (-200, 2300)], (214, 204, 190), (120, 112, 104), 1500, 2050)   # the open courtyard floor
    p.glow(540, 1560, 460, (255, 236, 190), .35)
    kaaba(p, 540, 1730, 1.05)

def end_sky(p):
    p.sky([(0, (8, 12, 34)), (.45, (34, 40, 84)), (.7, (110, 90, 120)), (.8, (230, 160, 110)), (1, (30, 20, 20))])
    stars(p, 220, 91, 900); moon(p, 820, 300, 56)
def end_mid(p): valley_walls(p, (40, 34, 50), (200, 150, 130), 92, top=900, floor=1460)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.7,
         title=dict(text='They built a house for Allah', arabic=TITLE_AR, hold=99, plain=True),
         lines=['A father and son built a house for Allah. What did they ask for?']),
    dict(layers=[valley_sky, valley_mid, valley_near], fx=['dust', 'sand'], cam='up',
         verse=dict(key='14:37', ar=(0, 12), en='Our Lord, I have settled some of my descendants in an uncultivated valley near Your sacred House', line=1, ar_size=72),
         lines=['Ibrahim, peace be upon him, left family in a dry valley and prayed:',
                'Our Lord, I have settled some of my descendants in an uncultivated valley near Your sacred House.']),
    dict(layers=[hearts_sky, hearts_mid, hearts_near], fx=['twinkle', 'fireflies'], cam='in',
         verse=dict(key='14:37', ar=(15, 21), en='So make hearts among the people incline toward them', line=1, ar_size=92),
         lines=['No crops grew there.', 'So make hearts among the people incline toward them.']),
    dict(layers=[site_sky, site_mid, site_near], fx=['dust'], cam='down', pause=0.5,
         lines=['With his son Ismail, he raised the foundations of the House.']),
    dict(layers=[pray_sky, pray_mid, pray_near], fx=['dust'], cam='in', bloom=.65,
         verse=dict(key='2:127', ar=(7, 14), en='Our Lord, accept [this] from us. Indeed You are the Hearing, the Knowing', line=1, ar_size=84),
         lines=['And they prayed:', 'Our Lord, accept this from us. Indeed You are the Hearing, the Knowing.']),
    dict(layers=[night_sky, night_mid, night_near], fx=['twinkle'], cam='hold', pause=0.5,
         lines=['Not for praise. Only: accept it.', 'Then came one more prayer, answered long after.']),
    dict(layers=[dawn_sky, dawn_mid, dawn_near], fx=['dust'], cam='up',
         verse=dict(key='2:129', ar=(0, 5), en='Our Lord, and send among them a messenger from themselves', line=1, ar_size=92),
         lines=['For their descendants:', 'Our Lord, and send among them a messenger from themselves.']),
    dict(layers=[answer_sky, answer_mid, answer_near], fx=['dust'], cam='out', bloom=.7,
         verse=dict(key='62:2', ar=(0, 7), en='It is He who has sent among the unlettered a Messenger from themselves', line=1, ar_size=84),
         lines=['From that valley came the Prophet Muhammad, peace and blessings be upon him.',
                'It is He who has sent among the unlettered a Messenger from themselves.']),
    dict(layers=[today_sky, today_mid, today_near], fx=['twinkle'], cam='in',
         lesson=dict(text='Do good. Then ask Allah to accept it.', after=1, y=560),
         lines=['Today, Muslims everywhere pray toward that House.', 'Do good, then ask Allah to accept it.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who does good quietly.', 'And follow for a new story from the Quran every day.']),
]

PRON = {}

CAPTION = """A father and son built a house for Allah. What did they ask for? 🤍

Ibrahim (peace be upon him) left some of his family in a dry valley and prayed: "Our Lord, I have settled some of my descendants in an uncultivated valley near Your sacred House." (Quran 14:37)

With his son Ismail he raised the foundations of the House, and they prayed: "Our Lord, accept [this] from us. Indeed You are the Hearing, the Knowing." (Quran 2:127)

They also prayed: "Our Lord, and send among them a messenger from themselves." (Quran 2:129) From that valley came the Prophet Muhammad (peace and blessings be upon him).

Do good, then ask Allah to accept it.

📖 Sources: Quran 14:35–41, 2:125–129, 22:26, 62:2, 2:144 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetIbrahim #IslamicReminder"""

FIRST_COMMENT = """What good deed are you asking Allah to accept today? 🤍

References: Quran, Surah Ibrahim 14:35–41; Surah Al-Baqarah 2:125–129 and 2:144; Surah Al-Hajj 22:26; Surah Al-Jumu'ah 62:2 (Saheeh International translation)."""
