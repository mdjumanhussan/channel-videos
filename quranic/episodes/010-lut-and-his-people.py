"""Story 10: Prophet Lut and his people. Sources: Quran 29:28-35, 7:80-84, 11:77-83, 15:57-77, 26:160-175, 27:54-58,
51:31-37, 54:33-39, 66:10 (Saheeh International).
No people are drawn: a city skyline, one lit house, a doorway with a lantern, a road at night, falling stones, ruins, sky.
No angels are drawn or shown in any form. Restraint: the people's sin is named only in the Quran's own general words
(29:28 "such immorality as no one has preceded you with"); nothing more explicit, nothing about anyone today.
Facts used and where they are: Lut warned his people (29:28, 26:161-166); their answer was "Evict them from your city!
Indeed, they are men who keep themselves pure" (7:82); only one house of believers in the city (51:36); the angels came
to Lut as guests (11:77, 15:68); his people came hastening to him (11:78); "they will never reach you ... except your
wife" (11:81); his wife remained behind (7:83, 15:60); stones of hard clay at sunrise (15:73-74); the wives of Nuh and Lut
were under righteous servants, "so those prophets did not avail them from Allah at all" (66:10). The daughters (11:78) are
left out: the verses need explanation that does not fit a 60-second Reel. No place name (the Quran gives none).
Improvement tried today: captions inside the Reels safe zone. Facebook/Instagram cover roughly the bottom 35% of a
1080x1920 Reel with the caption text, name and buttons (socialync.io safe-zone tool, Meta's Reels margins). Our karaoke
captions sat at y 1190, so a 2-line caption reached about y 1280, under the overlay. New engine option CAPTION_Y
(default unchanged); this episode sets 1110 so every caption ends above y ~1240. Also kept: open question on frame 1,
a second open loop when it is half answered, 0.5 s pause before the reveal, speed 1.1."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  10'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Prophet Lut and His People: "Except Your Wife"'
HITS = [(6, 0, 0.0), (7, 1, 0.0)]
# "Lut", taken straight from the text of 66:10 (without its pause mark)
TITLE_AR = quran()['verses']['66:10']['ar'].split()[8].rstrip('ۖۗۘۙۚۛۜ')

# ---------------------------------------------------------------- small scenery helpers for this story
def flat_city(p, base, col, seed, lit=None, ruin=0.0):
    """Ancient flat-roofed houses (no domes, no towers). lit=(r,g,b) lights a few small windows.
    ruin>0 breaks the roof lines and tilts the blocks (the overturned city)."""
    rnd = random.Random(seed); x = -150
    while x < 1250:
        w = rnd.uniform(70, 160); h = rnd.uniform(50, 190)
        if ruin:
            tilt = rnd.uniform(-1, 1) * 40 * ruin; h *= rnd.uniform(.35, .8)
            p.poly([(x, base + 800), (x, base - h + tilt), (x + w * .4, base - h - rnd.uniform(0, 30) * ruin), (x + w * .55, base - h * .7),
                    (x + w, base - h - tilt), (x + w, base + 800)], col)
        else:
            p.rect(x, base - h, x + w, base + 800, col)
            p.rect(x - 4, base - h - 8, x + w + 4, base - h, lc(col, (0, 0, 0), .2))      # roof lip
        if lit and not ruin and rnd.random() < .45:
            wx, wy = x + rnd.uniform(12, w - 22), base - h + rnd.uniform(20, max(24, h - 20))
            p.rect(wx, wy, wx + 10, wy + 14, lit, 200); p.glow(wx + 5, wy + 7, 20, lit, .25)
        x += w + rnd.uniform(-12, 14)

def lit_house(p, cx, base, s, wall=(70, 52, 44), light=(255, 196, 110)):
    """One plain house glowing warm among dark houses: flat roof, a door and two windows full of light."""
    p.glow(cx, base - 110 * s, 380 * s, light, .55)
    p.rect(cx - 150 * s, base - 200 * s, cx + 150 * s, base + 600, wall)
    p.rect(cx - 160 * s, base - 214 * s, cx + 160 * s, base - 200 * s, lc(wall, (0, 0, 0), .3))
    # asymmetric on purpose (door to one side, one long window), so the front never reads as a face
    p.rect(cx - 10 * s, base - 165 * s, cx + 120 * s, base - 125 * s, light); p.glow(cx + 55 * s, base - 145 * s, 90 * s, light, .5)
    p.rect(cx - 115 * s, base - 125 * s, cx - 55 * s, base, light); p.glow(cx - 85 * s, base - 60 * s, 90 * s, light, .6)

def doorway(p, cx, base, s, wall=(58, 42, 36), light=(255, 200, 120)):
    """Close view of a plain arched doorway, door open, warm light spilling out onto the ground."""
    p.rect(-200, base - 900 * s, 1300, base + 600, wall)
    for k in range(9):                                            # mud-brick courses
        y = base - 900 * s + k * 100 * s; p.line([(-200, y), (1300, y)], lc(wall, (0, 0, 0), .25), 3, 160)
    p.poly([(cx - 220 * s, base + 600), (cx - 150 * s, base), (cx + 150 * s, base), (cx + 220 * s, base + 600)], light, 70)  # spill of light
    p.rect(cx - 150 * s, base - 420 * s, cx + 150 * s, base, lc(wall, (0, 0, 0), .45))
    p.ell(cx, base - 420 * s, 150 * s, 110 * s, lc(wall, (0, 0, 0), .45))
    p.rect(cx - 120 * s, base - 400 * s, cx + 120 * s, base, light); p.ell(cx, base - 400 * s, 120 * s, 90 * s, light)
    p.glow(cx, base - 250 * s, 330 * s, light, .6)
    p.poly([(cx - 120 * s, base - 400 * s), (cx - 60 * s, base - 380 * s), (cx - 60 * s, base + 10 * s), (cx - 120 * s, base)], (70, 46, 30))  # the open door leaf

def road(p, x_far, y_far, base, w, col, a=200):
    """A pale road from the near ground to a far gap in the hills."""
    p.poly([(x_far - 4, y_far), (x_far + 4, y_far), (540 + w / 2, base), (540 - w / 2, base)], col, a)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (6, 10, 30)), (.45, (20, 26, 62)), (.7, (60, 50, 90)), (1, (14, 12, 22))])
    stars(p, 200, 1, 1000); moon(p, 820, 300, 58); p.glow(820, 300, 360, (200, 210, 255), .4)
def hook_mid(p):
    mountains(p, 1180, 170, (26, 24, 46), 2, rim=(120, 120, 170))
    flat_city(p, 1260, (16, 14, 26), 3)
def hook_near(p):
    dunes(p, 1440, 14, (44, 40, 62), (12, 12, 20), 4)
    road(p, 540, 1260, 2000, 520, (90, 88, 120), 170)
    lantern(p, 540, 1520, .55, (255, 196, 110))

def warn_sky(p):
    p.sky([(0, (40, 30, 70)), (.45, (150, 80, 90)), (.7, (240, 140, 80)), (.82, (255, 190, 110)), (1, (60, 30, 30))])
    sun(p, 540, 1270, 80, (255, 210, 140)); p.glow(540, 1270, 520, (255, 150, 80), .6)
def warn_mid(p): flat_city(p, 1320, (60, 36, 40), 11, lit=(255, 200, 120))
def warn_near(p): dunes(p, 1480, 16, (90, 52, 46), (30, 18, 18), 12)

def answer_sky(p):
    p.sky([(0, (20, 8, 10)), (.45, (90, 30, 26)), (.72, (200, 80, 40)), (1, (40, 14, 10))])
    clouds(p, 21, 300, 900, (160, 70, 50), 7, 140)
def answer_mid(p): flat_city(p, 1330, (34, 16, 18), 22)
def answer_near(p): dunes(p, 1480, 18, (70, 30, 24), (20, 8, 8), 23)

def house_sky(p):
    p.sky([(0, (4, 6, 22)), (.5, (14, 18, 48)), (.8, (34, 32, 70)), (1, (8, 8, 16))])
    stars(p, 220, 31, 1000)
def house_mid(p): flat_city(p, 1330, (14, 14, 26), 32)
def house_near(p):
    dunes(p, 1520, 10, (30, 28, 44), (8, 8, 14), 33)
    lit_house(p, 540, 1560, 1.3)

def door_sky(p): p.sky([(0, (8, 8, 20)), (1, (20, 16, 26))])
def door_near(p):
    doorway(p, 540, 1520, 1.25)
    lantern(p, 880, 820, .75, (255, 190, 100))

def night_sky(p):
    p.sky([(0, (4, 8, 26)), (.5, (12, 22, 58)), (.8, (36, 40, 86)), (1, (10, 10, 20))])
    stars(p, 260, 41, 1200); moon(p, 260, 320, 52)
def night_mid(p):
    mountains(p, 1200, 220, (22, 26, 52), 42, rim=(110, 120, 180))
def night_near(p):
    dunes(p, 1420, 14, (38, 38, 60), (10, 10, 18), 43)
    road(p, 560, 1210, 2000, 600, (96, 98, 136), 190)
    for x, y, s in ((560, 1290, .22), (566, 1340, .26)):
        lantern(p, x, y, s, (255, 196, 110))

def ruin_sky(p):
    p.sky([(0, (40, 10, 10)), (.4, (150, 50, 30)), (.66, (255, 140, 60)), (.8, (255, 200, 120)), (1, (50, 16, 10))])
    sun(p, 540, 1240, 100, (255, 220, 160)); p.glow(540, 1240, 600, (255, 120, 50), .7)
def ruin_mid(p): flat_city(p, 1330, (40, 16, 14), 52, ruin=1.0)
def ruin_near(p): dunes(p, 1470, 22, (80, 30, 20), (20, 6, 4), 53)

def lesson_sky(p):
    p.sky([(0, (40, 70, 130)), (.45, (150, 160, 190)), (.7, (250, 200, 150)), (1, (130, 90, 70))])
    sun(p, 540, 1260, 70, (255, 240, 210)); p.glow(540, 1260, 460, (255, 220, 170), .5)
def lesson_mid(p): flat_city(p, 1330, (110, 84, 76), 62, ruin=.8)
def lesson_near(p): dunes(p, 1470, 14, (190, 150, 120), (100, 70, 56), 63)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.82, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 71, 900); moon(p, 820, 300, 56)
def end_mid(p): flat_city(p, 1350, (30, 26, 44), 72, ruin=.8)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle'], cam='in', bloom=.65,
         title=dict(text='Who stayed behind?', arabic=TITLE_AR, hold=99, plain=True),
         lines=['One family escaped a city by night. One of them stayed behind. Who?']),
    dict(layers=[warn_sky, warn_mid, warn_near], fx=['dust'], cam='up',
         verse=dict(key='29:28', ar=(4, 14), en='Indeed, you commit such immorality as no one has preceded you with from among the worlds', line=1, ar_size=78),
         lines=['Prophet Lut, peace be upon him, warned his people:',
                'Indeed, you commit such immorality as no one has preceded you with from among the worlds.']),
    dict(layers=[answer_sky, answer_mid, answer_near], fx=['sand'], cam='in',
         verse=dict(key='7:82', ar=(7, 13), en='Evict them from your city! Indeed, they are men who keep themselves pure', line=1, ar_size=84),
         lines=['Their answer?', 'Evict them from your city! Indeed, they are men who keep themselves pure.']),
    dict(layers=[house_sky, house_mid, house_near], fx=['twinkle'], cam='in', pause=0.5,
         lines=['The whole city had only one house of believers.', 'Even there, not everyone believed.']),
    dict(layers=[door_sky, door_near], fx=['dust'], cam='hold',
         lines=['Angels came to Lut as guests. His people rushed to him.']),
    dict(layers=[night_sky, night_mid, night_near], fx=['twinkle'], cam='up', pause=0.5,
         verse=dict(key='11:81', ar=(5, 19), en='they will never reach you. So set out with your family during a portion of the night and let not any among you look back - except your wife', line=1, ar_size=66),
         lines=['The angels told him:',
                'They will never reach you. So set out with your family during a portion of the night, and let not any among you look back, except your wife.']),
    dict(layers=[ruin_sky, ruin_mid, ruin_near], fx=['stones', 'embers'], cam='in', bloom=.7,
         lines=['His own wife stayed behind with the wrongdoers.', 'At sunrise, stones of hard clay rained down.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out',
         lesson=dict(text='Being near good people is not enough.', after=1, y=560),
         lines=["She lived in a prophet's house. It did not save her.", 'Being near good people is not enough. Your own heart must believe.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who stands for the truth.', 'And follow for a new story from the Quran every day.']),
]

PRON = {}

CAPTION = """One family escaped a city by night. One of them stayed behind. Who? 🤍

Prophet Lut (peace be upon him) warned his people: "Indeed, you commit such immorality as no one has preceded you with from among the worlds." (Quran 29:28)

They answered: "Evict them from your city! Indeed, they are men who keep themselves pure." (Quran 7:82)

In the whole city there was only one house of believers (Quran 51:36). The angels told Lut: "So set out with your family during a portion of the night and let not any among you look back - except your wife." (Quran 11:81)

She lived in a prophet's house, yet it did not save her (Quran 66:10). Being near good people is not enough. Your own heart must believe.

📖 Sources: Quran 29:28–35, 7:80–84, 11:77–83, 15:57–77, 51:31–37, 66:10 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetLut #IslamicReminder"""

FIRST_COMMENT = """Which line of this story stayed with you? 🤍

References: Quran, Surah Al-'Ankabut 29:28–35; Surah Al-A'raf 7:80–84; Surah Hud 11:77–83; Surah Al-Hijr 15:57–77; Surah Adh-Dhariyat 51:31–37; Surah At-Tahrim 66:10 (Saheeh International translation)."""
