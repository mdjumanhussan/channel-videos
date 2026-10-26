"""Story 14: Prophet Ayyub (Job): patience in hardship. Sources: Quran 21:83-84, 38:41-44 (Saheeh International); 6:84 and
4:163 name him among the prophets Allah guided and sent revelation to.
No people are drawn: no Ayyub, no family. Only a storm over a bare tree, dry cracked ground, a lantern at night, a spring
rising from rock, green returning, a camp of lit tents (his family given back, as a symbol), and the night sky.
Facts used and where they are: he is among the prophets Allah guided (6:84); he called to his Lord, "Indeed, adversity
has touched me, and you are the Most Merciful of the merciful" (21:83), and "Satan has touched me with hardship and
torment" (38:41); he was told "Strike [the ground] with your foot; this is a [spring for] a cool bath and drink" (38:42);
Allah responded and removed what afflicted him of adversity (21:84); Allah gave him his family and a like [number] with
them as mercy and a reminder (21:84, 38:43); "Indeed, We found him patient, an excellent servant. Indeed, he was one
repeatedly turning back [to Allah]" (38:44).
Not used: the bunch of grass and the oath (38:44, first part: who and why come from tafsir, not the verse); any length of
time, any named illness, any loss of wealth or children in detail, any role of his wife: none of these are in the verses.
Improvement tried today: a specific "send it to" ending. Sends (shares in private messages) are reported as the strongest
signal for reaching people who do not follow a page, weighted about 3-5x a like (eclincher, citing Adam Mosseri). So the
end card names one real person to send it to, on screen and spoken: "Share this with someone going through a hard time",
right after the lesson card, and the lesson itself is the part of 21:83 worth sending. No engine change (end card
line1/line2). Also kept: plain headline = spoken hook with caption hidden, open question answered at the peak (21:83,
deep hit), a second loop ("What would he do?") with a 0.5 s pause before the answer, speed 1.1, lesson card,
CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  14'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Prophet Ayyub: Patience in Hardship'
HITS = [(4, 1, 0.0), (8, 1, 0.0)]
# "adversity has touched me", taken straight from the text of 21:83
TITLE_AR = ' '.join(quran()['verses']['21:83']['ar'].split()[5:7])

# ---------------------------------------------------------------- small scenery helpers for this story
def bare_tree(p, x, base, h, col=(30, 22, 20), seed=1):
    """A leafless, wind-bent tree: trunk and forking branches only."""
    rnd = random.Random(seed)
    def branch(x0, y0, ang, ln, w, depth):
        x1 = x0 + ln * math.cos(math.radians(ang)); y1 = y0 - ln * math.sin(math.radians(ang))
        p.line([(x0, y0), (x1, y1)], col, w)
        if depth > 0:
            for da in (rnd.uniform(18, 34), -rnd.uniform(18, 34)):
                branch(x1, y1, ang + da + 6, ln * rnd.uniform(.6, .75), max(2, w * .62), depth - 1)
    p.poly([(x - 22, base), (x - 9, base - h * .45), (x + 9, base - h * .45), (x + 22, base)], col)
    branch(x, base - h * .42, 96, h * .34, 16, 4)

def cracked_ground(p, top, col=(120, 84, 56), seed=2):
    """Dry, cracked earth from y=top down."""
    rnd = random.Random(seed)
    p.grad_poly([(-200, top), (1300, top), (1300, 2300), (-200, 2300)], lc(col, (255, 255, 255), .1), lc(col, (0, 0, 0), .5), top, top + 700)
    dark = lc(col, (0, 0, 0), .55)
    for _ in range(26):
        x, y = rnd.uniform(-100, 1180), rnd.uniform(top + 20, 2000); pts = [(x, y)]
        for k in range(rnd.randint(3, 6)):
            x += rnd.uniform(-90, 90); y += rnd.uniform(-20, 40) * (1 + (y - top) / 600); pts.append((x, y))
        p.line(pts, dark, 2 + (y - top) / 260)

def flowers(p, top, seed=3, cols=((255, 220, 120), (255, 255, 240), (250, 170, 190))):
    """Small wildflowers and grass tufts scattered on the ground below y=top."""
    rnd = random.Random(seed)
    for _ in range(90):
        x, y = rnd.uniform(-60, 1140), rnd.uniform(top, 1900); s = .6 + (y - top) / 900
        g = (70, 140, 60)
        for dx in (-6, 0, 6): p.line([(x, y), (x + dx * 1.8 * s, y - 26 * s)], g, 3 * s)
        if rnd.random() < .55:
            c = rnd.choice(cols); p.ell(x + 2, y - 30 * s, 7 * s, 7 * s, c); p.ell(x + 2, y - 30 * s, 2.6 * s, 2.6 * s, (240, 170, 50))

def spring(p, cx, base, s=1.0, water=(150, 215, 240)):
    """Rocks around a pool with clear water rising from the ground (38:42). Water and stone only."""
    rock = (96, 84, 76)
    p.ell(cx, base + 10 * s, 330 * s, 70 * s, lc(water, (0, 0, 0), .35))
    p.ell(cx, base, 300 * s, 58 * s, water); p.ell(cx - 40 * s, base - 10 * s, 160 * s, 22 * s, lc(water, (255, 255, 255), .45))
    for dx, r in ((-330, 70), (-250, 52), (300, 76), (360, 48), (-120, 34), (170, 40)):
        yy = base + (20 if abs(dx) > 200 else 52) * s
        p.ell(cx + dx * s, yy, r * s, r * .62 * s, rock); p.ell(cx + dx * s - r * .25 * s, yy - r * .22 * s, r * .45 * s, r * .22 * s, lc(rock, (255, 255, 255), .2))
    def jet(t):
        for k in range(7):
            ww = (60 - k * 7) * s; hh = (300 - k * 24) * s
            t.poly([(cx - ww, base), (cx - ww * .3, base - hh * .7), (cx, base - hh), (cx + ww * .3, base - hh * .7), (cx + ww, base)], lc(water, (255, 255, 255), .1 + k * .1), 120)
    p.blur_shape(jet, 5)
    p.glow(cx, base - 140 * s, 320 * s, (220, 245, 255), .55)
    for k in range(-3, 4): p.ell(cx + k * 34 * s, base - (210 + abs(k) * -20) * s + abs(k) * 40 * s, 9 * s, 13 * s, (235, 250, 255), 220)

def tent(p, cx, base, s, col=(120, 84, 60), light=(255, 196, 110)):
    """A plain desert tent with lamplight in its open side (copied from episode 11)."""
    p.glow(cx, base - 120 * s, 360 * s, light, .45)
    p.poly([(cx - 300 * s, base), (cx - 230 * s, base - 200 * s), (cx, base - 250 * s), (cx + 230 * s, base - 200 * s), (cx + 300 * s, base)], col)
    for k in range(-2, 3): p.line([(cx + k * 110 * s, base - 240 * s + abs(k) * 18 * s), (cx + k * 130 * s, base)], lc(col, (0, 0, 0), .25), 3, 200)
    p.poly([(cx + 40 * s, base), (cx + 70 * s, base - 150 * s), (cx + 170 * s, base - 140 * s), (cx + 190 * s, base)], light)
    p.glow(cx + 115 * s, base - 70 * s, 120 * s, light, .6)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def storm_sky(p):
    p.sky([(0, (16, 18, 30)), (.45, (44, 46, 66)), (.7, (90, 80, 90)), (1, (24, 20, 22))])
    cloud_bank(p, 260, (40, 42, 60), (20, 20, 32), 11, 90, 235)
    cloud_bank(p, 520, (60, 60, 80), (34, 32, 46), 12, 70, 200)
def storm_near(p):
    mountains(p, 1360, 260, (30, 28, 36), 13)
    cracked_ground(p, 1380, (86, 64, 50), 14)
    bare_tree(p, 560, 1500, 720, (18, 14, 14), 15)

def blessed_sky(p):
    p.sky([(0, (90, 150, 210)), (.5, (190, 210, 230)), (.75, (255, 226, 170)), (1, (150, 170, 90))])
    sun(p, 820, 760, 70, (255, 236, 180))
    clouds(p, 21, 300, 600, (255, 250, 240), 6, 170)
def blessed_mid(p):
    mountains(p, 1260, 220, (120, 150, 150), 22)
    dunes(p, 1330, 30, (120, 170, 80), (80, 130, 60), 23)
def blessed_near(p):
    for x, h, sd in ((150, 520, 24), (920, 480, 25)): tree(p, x, 1520, h, (70, 50, 34), (70, 140, 60), sd)
    palm(p, 330, 1500, 360, (60, 70, 36), -.05); palm(p, 760, 1490, 330, (60, 70, 36), .06)
    flowers(p, 1480, 26)

def dry_sky(p):
    p.sky([(0, (40, 26, 30)), (.5, (120, 70, 50)), (.75, (200, 120, 70)), (1, (60, 36, 26))])
    cloud_bank(p, 360, (70, 44, 46), (40, 26, 30), 31, 80, 210)
    p.glow(540, 1150, 520, (255, 150, 80), .45)
def dry_near(p):
    cracked_ground(p, 1300, (150, 100, 66), 32)
    bare_tree(p, 260, 1520, 560, (40, 26, 20), 33); bare_tree(p, 860, 1460, 420, (40, 26, 20), 34)

def lamp_sky(p):
    p.sky([(0, (4, 6, 20)), (.6, (14, 16, 40)), (1, (6, 6, 14))])
    stars(p, 260, 41, 1250)
def lamp_mid(p): dunes(p, 1380, 16, (26, 24, 40), (8, 8, 16), 42)
def lamp_near(p):
    lantern(p, 540, 1420, 1.4, (255, 190, 90))
    p.glow(540, 1520, 380, (255, 170, 80), .35)

def prayer_sky(p):
    p.sky([(0, (6, 8, 30)), (.5, (24, 26, 70)), (.8, (60, 50, 96)), (1, (12, 10, 22))])
    stars(p, 220, 51, 1200); moon(p, 800, 300, 48)
def prayer_mid(p): mountains(p, 1380, 300, (18, 18, 34), 52, (90, 100, 160))
def prayer_near(p):
    p.rect(-100, 1460, 1200, 2300, (10, 10, 18))
    lantern(p, 540, 1380, .9)

def turn_sky(p):
    p.sky([(0, (14, 16, 44)), (.45, (70, 60, 110)), (.7, (230, 150, 110)), (.8, (255, 200, 140)), (1, (60, 40, 40))])
    stars(p, 120, 61, 700)
def turn_rays(p):
    rays(p, 540, 1330, (255, 220, 160), n=11, spread=110, length=1700, width=6, a=.28, angle=-90, seed=62)
    p.glow(540, 1330, 420, (255, 210, 150), .7)
def turn_near(p):
    mountains(p, 1400, 200, (34, 26, 40), 63)
    p.rect(-100, 1460, 1200, 2300, (26, 20, 30))
    bare_tree(p, 200, 1520, 420, (20, 14, 18), 64)

def spring_sky(p):
    p.sky([(0, (14, 30, 60)), (.4, (40, 70, 110)), (.62, (150, 150, 160)), (.75, (250, 210, 160)), (1, (120, 100, 80))])
    mountains(p, 1300, 280, (90, 90, 110), 71, (170, 170, 190))
def spring_near(p):
    p.grad_poly([(-200, 1300), (1300, 1300), (1300, 2300), (-200, 2300)], (170, 140, 100), (90, 70, 50), 1300, 1900)
    spring(p, 540, 1520, 1.05)

def green_sky(p):
    p.sky([(0, (80, 140, 210)), (.5, (200, 220, 235)), (.72, (255, 230, 170)), (1, (140, 170, 90))])
    sun(p, 540, 1150, 90, (255, 240, 190))
def green_rays(p): rays(p, 540, 1150, (255, 240, 200), n=13, spread=360, length=1300, width=4, a=.18, angle=0, seed=81)
def green_near(p):
    dunes(p, 1340, 28, (110, 170, 80), (70, 130, 60), 82)
    tree(p, 830, 1480, 460, (70, 50, 34), (80, 150, 70), 83); tree(p, 230, 1500, 380, (70, 50, 34), (90, 160, 70), 84)
    flowers(p, 1440, 85)

def camp_sky(p):
    p.sky([(0, (20, 20, 60)), (.45, (80, 60, 110)), (.72, (230, 140, 100)), (1, (60, 36, 30))])
    stars(p, 90, 91, 600)
def camp_mid(p):
    dunes(p, 1300, 16, (120, 80, 70), (70, 44, 40), 92)
    for x, s in ((150, .45), (380, .5), (700, .5), (930, .45)): tent(p, x, 1330, s, (96, 64, 50), (255, 200, 120))
def camp_near(p):
    dunes(p, 1460, 10, (90, 60, 50), (40, 26, 22), 93)
    for x, s in ((260, .8), (820, .8)): tent(p, x, 1560, s, (110, 74, 56), (255, 200, 120))
    palm(p, 540, 1520, 340, (40, 30, 26))

def praise_sky(p):
    p.sky([(0, (4, 6, 26)), (.5, (20, 26, 70)), (.8, (50, 50, 110)), (1, (8, 8, 18))])
    stars(p, 320, 101, 1300, (230, 235, 255))
def praise_rays(p):
    rays(p, 540, -200, (220, 230, 255), n=9, spread=40, length=2000, width=4, a=.25, angle=90, seed=102)
def praise_near(p):
    mountains(p, 1420, 320, (14, 14, 30), 103, (120, 130, 200))
    p.rect(-100, 1480, 1200, 2300, (8, 8, 16))

def lesson_sky(p):
    p.sky([(0, (70, 120, 190)), (.5, (200, 210, 230)), (.75, (255, 220, 170)), (1, (130, 150, 90))])
    sun(p, 540, 1220, 70, (255, 236, 190))
def lesson_near(p):
    dunes(p, 1360, 22, (120, 170, 90), (80, 130, 60), 111)
    spring(p, 540, 1560, .8)
    flowers(p, 1520, 112)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 121, 900); moon(p, 820, 300, 56)
def end_mid(p): mountains(p, 1360, 240, (40, 34, 56), 122)
def end_near(p): lantern(p, 150, 900, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[storm_sky, storm_near], fx=['rain'], cam='in', bloom=.55,
         title=dict(text='Hardship touched him. What did he say to Allah?', arabic=TITLE_AR, hold=99, plain=True),
         no_caption=(0,),
         lines=['Hardship touched him. What did he say to Allah?']),
    dict(layers=[blessed_sky, blessed_mid, blessed_near], fx=['dust'], cam='right',
         lines=['Ayyub, peace be upon him, was one of the prophets Allah guided.', 'His story in the Quran is short. Its lesson is huge.']),
    dict(layers=[dry_sky, dry_near], fx=['sand'], cam='in',
         lines=['Then hardship touched him, and torment.', 'Many people would turn away. What would he do?']),
    dict(layers=[lamp_sky, lamp_mid, lamp_near], fx=['twinkle'], cam='in', pause=0.5,
         lines=['He did not turn away from his Lord. He turned to Him.']),
    dict(layers=[prayer_sky, prayer_mid, prayer_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='21:83', ar=(4, 10), en='Indeed, adversity has touched me, and you are the Most Merciful of the merciful', line=1, ar_size=84, y=620),
         lines=['He called to his Lord:', 'Indeed, adversity has touched me, and you are the Most Merciful of the merciful.', "He named his hardship. Then he named Allah's mercy."]),
    dict(layers=[spring_sky, spring_near], fx=['dust'], cam='in', bloom=.7,
         verse=dict(key='38:42', en='Strike [the ground] with your foot; this is a [spring for] a cool bath and drink', ar_size=80, y=600, line=1),
         lines=['Then he was told:', 'Strike the ground with your foot. This is a spring for a cool bath and drink.']),
    dict(layers=[green_sky, green_rays, green_near], fx=['petals'], cam='out',
         lines=['So Allah answered him, and removed his hardship.']),
    dict(layers=[camp_sky, camp_mid, camp_near], fx=['twinkle'], cam='right',
         lines=['Allah gave him his family, and as many again with them, as a mercy.']),
    dict(layers=[praise_sky, praise_rays, praise_near], fx=['twinkle'], cam='up', bloom=.75,
         verse=dict(key='38:44', ar=(7, 12), en='Indeed, We found him patient, an excellent servant', line=1, ar_size=84, y=620),
         lines=['And Allah says about him:', 'Indeed, We found him patient, an excellent servant.']),
    dict(layers=[lesson_sky, lesson_near], fx=['dust'], cam='out',
         lesson=dict(text='In hardship, turn to Allah. He is the Most Merciful.', after=0, y=560), no_caption=(0,),
         lines=['In hardship, turn to Allah. He is the Most Merciful.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with someone', line2='going through a hard time'), no_caption=(0,),
         lines=['Share this with someone going through a hard time. And follow for a new story from the Quran every day.']),
]

PRON = {'Ayyub': 'ajjˈuːb'}

CAPTION = """Hardship touched him. What did he say to Allah? 🤍

Ayyub (Job), peace be upon him, was one of the prophets Allah guided. Hardship touched him, but he did not turn away. He called to his Lord: "Indeed, adversity has touched me, and you are the Most Merciful of the merciful." (Quran 21:83)

He was told: "Strike [the ground] with your foot; this is a [spring for] a cool bath and drink." (Quran 38:42)

Allah answered him, removed his hardship, and gave him his family and as many again with them, as a mercy (21:84, 38:43). Allah says: "Indeed, We found him patient, an excellent servant." (Quran 38:44)

In hardship, turn to Allah. He is the Most Merciful.

📖 Sources: Quran 21:83–84, 38:41–44 (Saheeh International)
Share this with someone going through a hard time. Follow for a new story every day.

#QuranicStories #ProphetAyyub #IslamicReminder"""

FIRST_COMMENT = """Who would you send Ayyub's prayer to today? 🤍

References: Quran, Surah Al-Anbiya 21:83–84 and Surah Sad 38:41–44 (Saheeh International translation)."""
