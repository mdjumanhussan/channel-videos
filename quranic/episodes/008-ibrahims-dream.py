"""Story 8: Ibrahim's dream and the great sacrifice. Sources: Quran 37:99-111 (Saheeh International).
No people are drawn: night sky, moon, stars, desert roads, hills, a young palm, light and sunrise only.
Nothing beyond the verses: the son is NOT named (37:99-111 do not name him), no ram (the Quran says only
"a great sacrifice"), no knife, no place names, no Iblees/stoning story, no dialogue that is not in the Quran.
Improvement tried today: two stacked open loops. Frame 1 asks "What did his son say?" (answered in scene 5),
and the moment it is answered a second question opens ("What would happen now?", answered in scenes 7-8).
Reason: Reel 6 (idols), which used a mid-story re-hook and speed 1.1, became the best Reel by far
(1236 views, 10 s average) while Reel 7 (action opening, no re-hook) got 221 views, 5 s."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  8'
VOICE, SPEED = 'bm_george', 1.1
THUMB_AT = 1.0
TITLE = "Ibrahim's Dream: \"Do As You Are Commanded\""
HITS = [(4, 1, 0.0), (6, 1, 0.0)]
# "O my son", taken straight from the text of 37:102
TITLE_AR = quran()['verses']['37:102']['ar'].split()[5]

# ---------------------------------------------------------------- small scenery helpers for this story
def road(p, x_far, y_far, base, w_near, col, edge):
    """A desert road narrowing to the horizon."""
    p.poly([(x_far - 6, y_far), (x_far + 6, y_far), (540 + w_near / 2, base), (540 - w_near / 2, base)], col)
    p.line([(x_far - 6, y_far), (540 - w_near / 2, base)], edge, 4, 160); p.line([(x_far + 6, y_far), (540 + w_near / 2, base)], edge, 4, 160)

def sprout_palm(p, x, base, h, col):
    """A young palm: short trunk, a few fresh fronds."""
    p.line([(x, base), (x + 4, base - h * .5), (x, base - h)], lc(col, (60, 40, 20), .5), 12)
    for ang in (-150, -115, -80, -50, -20, 200):
        a = math.radians(ang); pts = []
        for k in range(7):
            r = k * h * .07; pts.append((x + r * math.cos(a), base - h + r * math.sin(a) + (k ** 2) * 2.2))
        p.line(pts, col, 10)

def birds(p, pts, col, s=1.0):
    """Distant birds as small 'v' strokes."""
    for x, y in pts:
        p.line([(x - 22 * s, y - 8 * s), (x, y + 4 * s), (x + 22 * s, y - 8 * s)], col, 4, 200)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (4, 6, 22)), (.45, (18, 22, 60)), (.75, (60, 50, 100)), (1, (14, 12, 26))])
    stars(p, 200, 1, 1000); moon(p, 540, 920, 95); p.glow(540, 920, 460, (190, 200, 255), .55)
def hook_mid(p): mountains(p, 1430, 200, (26, 26, 52), 2, rim=(150, 150, 210))
def hook_near(p): dunes(p, 1560, 40, (30, 28, 50), (10, 10, 18), 3)

def pray_sky(p):
    p.sky([(0, (40, 40, 90)), (.45, (150, 110, 150)), (.7, (255, 180, 130)), (1, (110, 70, 60))])
    sun(p, 540, 1240, 80, (255, 220, 170)); p.glow(540, 1240, 420, (255, 190, 140), .6)
def pray_mid(p): mountains(p, 1300, 160, (110, 80, 100), 11, rim=(255, 200, 160))
def pray_near(p):
    dunes(p, 1290, 30, (190, 130, 100), (90, 56, 46), 12)
    road(p, 540, 1290, 2000, 760, (150, 104, 80), (230, 180, 140))

def boy_sky(p):
    p.sky([(0, (70, 110, 170)), (.45, (170, 190, 220)), (.7, (255, 220, 170)), (1, (170, 140, 100))])
    sun(p, 800, 900, 70, (255, 240, 200)); clouds(p, 21, 300, 800, (255, 240, 225), 6, 130)
def boy_mid(p):
    mountains(p, 1380, 150, (150, 140, 150), 22, rim=(255, 230, 200))
    birds(p, [(300, 620), (380, 580), (450, 640)], (60, 50, 60))
def boy_near(p):
    dunes(p, 1500, 30, (200, 170, 110), (130, 100, 60), 23)
    palm(p, 250, 1560, 460, (50, 80, 40), -.05)
    sprout_palm(p, 760, 1560, 230, (80, 140, 60))

def dream_sky(p):
    p.sky([(0, (2, 4, 14)), (.5, (10, 16, 44)), (.8, (30, 30, 70)), (1, (8, 8, 18))])
    stars(p, 260, 31, 1300); moon(p, 880, 210, 48)
    clouds(p, 32, 900, 1200, (60, 60, 110), 5, 90)
def dream_mid(p): mountains(p, 1460, 180, (18, 18, 40), 33, rim=(90, 90, 150))
def dream_near(p):
    dunes(p, 1560, 30, (22, 20, 40), (6, 6, 12), 34); lantern(p, 540, 1490, 1.0, (255, 200, 120))

def answer_sky(p):
    p.sky([(0, (60, 40, 90)), (.4, (200, 120, 110)), (.66, (255, 200, 120)), (1, (140, 80, 50))])
    sun(p, 540, 1320, 120, (255, 230, 160))
    rays(p, 540, 1320, (255, 236, 190), n=18, spread=360, length=1700, width=3, a=.18, angle=0, seed=41)
def answer_mid(p): mountains(p, 1400, 180, (120, 70, 70), 42, rim=(255, 210, 150))
def answer_near(p): dunes(p, 1520, 36, (170, 110, 70), (80, 46, 30), 43)

def submit_sky(p):
    p.sky([(0, (20, 22, 40)), (.5, (70, 66, 90)), (.8, (160, 120, 110)), (1, (50, 40, 40))])
    clouds(p, 51, 500, 1100, (110, 100, 120), 7, 150)
def submit_mid(p): mountains(p, 1420, 260, (50, 46, 64), 52, rim=(200, 160, 150))
def submit_near(p): dunes(p, 1560, 50, (70, 58, 64), (24, 20, 24), 53)

def call_sky(p):
    p.sky([(0, (240, 236, 220)), (.3, (190, 200, 230)), (.7, (110, 120, 170)), (1, (50, 50, 70))])
    rays(p, 540, -200, (255, 252, 235), n=12, spread=60, length=2600, width=8, a=.30, angle=90, seed=61)
    p.glow(540, 200, 700, (255, 250, 230), .9)
def call_mid(p): mountains(p, 1420, 260, (70, 72, 100), 52, rim=(255, 245, 220))
def call_near(p): dunes(p, 1560, 50, (90, 86, 100), (30, 28, 36), 53)

def ransom_sky(p):
    p.sky([(0, (40, 90, 170)), (.45, (110, 150, 200)), (.7, (230, 160, 110)), (1, (120, 110, 80))])
    sun(p, 540, 1390, 80, (255, 235, 200))
    rays(p, 540, 1390, (255, 248, 225), n=16, spread=360, length=1600, width=3, a=.1, angle=0, seed=71)
def ransom_mid(p):
    mountains(p, 1340, 200, (90, 120, 110), 72, rim=(255, 240, 200))
    birds(p, [(260, 1000), (330, 960), (760, 940), (830, 980)], (40, 40, 60))
def ransom_near(p):
    dunes(p, 1480, 30, (110, 150, 80), (50, 80, 40), 73)
    palm(p, 140, 1600, 420, (40, 80, 40), -.04); palm(p, 950, 1580, 380, (40, 80, 40), .05)

def lesson_sky(p):
    p.sky([(0, (30, 50, 110)), (.4, (100, 110, 170)), (.66, (200, 120, 100)), (1, (110, 70, 50))])
    sun(p, 820, 700, 70, (255, 220, 150))
def lesson_mid(p): mountains(p, 1360, 230, (90, 70, 90), 82, rim=(255, 210, 160))
def lesson_near(p):
    dunes(p, 1500, 40, (200, 160, 110), (120, 80, 50), 83)
    palm(p, 260, 1600, 400, (50, 70, 36), -.04); sprout_palm(p, 820, 1600, 260, (70, 110, 50))

def end_sky(p):
    p.sky([(0, (6, 8, 30)), (.45, (30, 36, 80)), (.7, (100, 90, 130)), (.78, (220, 160, 120)), (1, (24, 16, 20))])
    stars(p, 220, 91, 900); moon(p, 820, 300, 56)
def end_mid(p): dunes(p, 1380, 50, (44, 44, 66), (16, 16, 26), 92)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle', 'dust'], cam='in', bloom=.7,
         title=dict(text="A father's hardest test", arabic=TITLE_AR, hold=99, plain=True),
         lines=['A father dreamed he must sacrifice his son. What did his son say?']),
    dict(layers=[pray_sky, pray_mid, pray_near], fx=['dust'], cam='up',
         verse=dict(key='37:100', en='My Lord, grant me [a child] from among the righteous', line=1, ar_size=96),
         lines=['Ibrahim, peace be upon him, prayed:', 'My Lord, grant me a child from among the righteous.']),
    dict(layers=[boy_sky, boy_mid, boy_near], fx=['dust'], cam='right',
         verse=dict(key='37:101', en='So We gave him good tidings of a forbearing boy', line=0, ar_size=100),
         lines=['So We gave him good tidings of a forbearing boy.', 'The boy grew, old enough to work beside his father.']),
    dict(layers=[dream_sky, dream_mid, dream_near], fx=['twinkle'], cam='in', pause=0.5,
         verse=dict(key='37:102', ar=(5, 15), en='O my son, indeed I have seen in a dream that I [must] sacrifice you, so see what you think', line=1, ar_size=74),
         lines=['Then Ibrahim told his son:', 'O my son, indeed I have seen in a dream that I must sacrifice you, so see what you think.']),
    dict(layers=[answer_sky, answer_mid, answer_near], fx=['dust'], cam='up', bloom=.65,
         verse=dict(key='37:102', ar=(16, 26), en='O my father, do as you are commanded. You will find me, if Allah wills, of the steadfast', line=1, ar_size=74),
         lines=['And his son said:', 'O my father, do as you are commanded. You will find me, if Allah wills, of the steadfast.']),
    dict(layers=[submit_sky, submit_mid, submit_near], fx=['dust'], cam='hold', pause=0.5,
         lines=['They both submitted to Allah.', 'He laid his son down on his forehead.', 'What would happen now?']),
    dict(layers=[call_sky, call_mid, call_near], fx=['dust'], cam='in', bloom=.75,
         verse=dict(key='37:105', ar=(0, 3), en='You have fulfilled the vision', line=1, ar_size=100),
         lines=['Allah called to him: O Abraham!', 'You have fulfilled the vision.']),
    dict(layers=[ransom_sky, ransom_mid, ransom_near], fx=['dust'], cam='out', bloom=.65,
         verse=dict(key='37:107', en='And We ransomed him with a great sacrifice', line=1, ar_size=100),
         lines=['Indeed, this was the clear trial.', 'And We ransomed him with a great sacrifice.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='up',
         lines=['When a command of Allah feels hard, submit and trust Him.', 'He rewards the doers of good.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Share this with someone who is being tested right now.', 'And follow for a new story from the Quran every day.']),
]

PRON = {}

CAPTION = """A father dreamed he must sacrifice his son. What did his son say? 🤍

Ibrahim (peace be upon him) prayed: "My Lord, grant me [a child] from among the righteous." So Allah gave him good tidings of a forbearing boy. (Quran 37:100–101)

When the boy was old enough to work beside him, Ibrahim said: "O my son, indeed I have seen in a dream that I [must] sacrifice you, so see what you think."

His son said: "O my father, do as you are commanded. You will find me, if Allah wills, of the steadfast." (Quran 37:102)

They both submitted. Then Allah called: "You have fulfilled the vision." "And We ransomed him with a great sacrifice." (Quran 37:105, 37:107)

When a command of Allah feels hard, submit and trust Him. He rewards the doers of good.

📖 Sources: Quran 37:99–111 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetIbrahim #IslamicReminder"""

FIRST_COMMENT = """Which line of this story touched your heart most? 🤍

References: Quran, Surah As-Saffat 37:99–111 (Saheeh International translation). These verses do not name the son, so we did not either."""
