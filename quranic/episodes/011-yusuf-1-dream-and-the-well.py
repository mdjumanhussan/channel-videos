"""Story 11: Yusuf, part 1 of 3: the dream and the well. Sources: Quran 12:4-22 (Saheeh International).
No people are drawn: no Yusuf, no Yaqub, no brothers, no travellers. Only sky, stars, sun and moon, a tent, the desert,
the well (outside and seen from inside), a shirt, a bucket on a rope, distant camels, Egypt at dusk.
Facts used and where they are: Yusuf told his father of eleven stars, the sun and the moon prostrating to him (12:4);
his father said not to tell his brothers (12:5); the brothers said Yusuf and his brother were more beloved to their father
(12:8); one of them said do not kill him but throw him into the bottom of the well (12:10); they asked to take him so he
may "eat well and play" (12:12); they put him into the bottom of the well and Allah inspired him: "You will surely inform
them [someday] about this affair of theirs while they do not perceive [your identity]" (12:15); they came at night
weeping and said a wolf ate him (12:16-17); false blood on his shirt; his father: "patience is most fitting" (12:18);
travellers let down a bucket: "Good news! Here is a boy." (12:19); sold for a few dirhams (12:20); bought by "the one from
Egypt" (12:21). The meaning of the dream is NOT explained here: the Quran gives it in 12:100 (part 3).
No brother is named (the Quran names none). The wolf is not drawn (there was no wolf). The test in Egypt (12:23) is
only hinted at as "a new test" for part 2.
Improvement tried today: an explicit series label. A gold "Part 1 of 3" pill on frame 1 (new engine title option `part`,
default unchanged) and an end card that says "Part 2 tomorrow", following advice to mark progress ("Part 1 of 3") and end
part 1 on one specific question (influencers-time.com). Our own data: the linked Ibrahim Reels 6-8 all broke out on day 2.
Also kept: open question on frame 1 (answered in scene 5), a second loop (the father), 0.5 s pause before the reveal,
speed 1.1, the lesson card, captions at CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  11'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Yusuf, Part 1: The Dream and the Well'
HITS = [(4, 1, 0.0), (6, 0, 0.0)]
# "Yusuf", taken straight from the text of 12:4
TITLE_AR = quran()['verses']['12:4']['ar'].split()[2]

# ---------------------------------------------------------------- small scenery helpers for this story
def camel(p, cx, base, s=1.0, col=(30, 20, 14), flip=False):
    """A camel, side view, standing at (cx, base). An animal only (copied from episode 5)."""
    k = -1 if flip else 1
    def X(dx): return cx + k * dx * s
    def Y(dy): return base + dy * s
    for lx, ph in ((-105, 0), (-70, 1), (80, 0), (110, 1)):
        sh = lc(col, (0, 0, 0), .25) if ph else col
        p.line([(X(lx), Y(-240)), (X(lx + 6), Y(-120))], sh, 20 * s); p.line([(X(lx + 6), Y(-120)), (X(lx), Y(-6))], sh, 14 * s)
        p.ell(X(lx + 6), Y(-120), 11 * s, 12 * s, sh); p.ell(X(lx + 8), Y(-4), 16 * s, 7 * s, sh)
    p.ell(X(-5), Y(-268), 160 * s, 66 * s, col)
    p.poly([(X(-150), Y(-290)), (X(-150), Y(-250)), (X(-110), Y(-200)), (X(-60), Y(-230))], col)
    p.ell(X(-15), Y(-322), 88 * s, 64 * s, col)
    p.line([(X(-160), Y(-290)), (X(-178), Y(-230)), (X(-172), Y(-190))], col, 8 * s)
    p.poly([(X(105), Y(-315)), (X(155), Y(-235)), (X(205), Y(-300)), (X(235), Y(-400)), (X(205), Y(-415)), (X(180), Y(-330)), (X(130), Y(-300))], col)
    p.ell(X(240), Y(-418), 44 * s, 22 * s, col); p.ell(X(278), Y(-408), 18 * s, 14 * s, col)
    p.poly([(X(215), Y(-434)), (X(210), Y(-458)), (X(226), Y(-438))], col)

def stone_well(p, cx, base, s, col=(130, 104, 80), rope=True):
    """A round stone well with a wooden frame and a rope going down into the dark."""
    well(p, cx, base, s, col)
    wood = (70, 46, 28)
    p.line([(cx - 135 * s, base - 110 * s), (cx - 120 * s, base - 330 * s)], wood, 16 * s)
    p.line([(cx + 135 * s, base - 110 * s), (cx + 120 * s, base - 330 * s)], wood, 16 * s)
    p.line([(cx - 150 * s, base - 330 * s), (cx + 150 * s, base - 330 * s)], wood, 18 * s)
    if rope: p.line([(cx + 10 * s, base - 330 * s), (cx + 10 * s, base - 125 * s)], (190, 160, 110), 4 * s)

def bucket(p, cx, y, s, col=(110, 74, 44)):
    """A wooden bucket hanging on a rope from above."""
    p.line([(cx, -100), (cx, y - 60 * s)], (200, 170, 120), 5 * s)
    p.line([(cx - 55 * s, y - 20 * s), (cx, y - 60 * s), (cx + 55 * s, y - 20 * s)], (60, 40, 24), 5 * s)
    p.poly([(cx - 60 * s, y - 20 * s), (cx + 60 * s, y - 20 * s), (cx + 48 * s, y + 70 * s), (cx - 48 * s, y + 70 * s)], col)
    for dy in (0, 45): p.line([(cx - 58 * s, y - 10 * s + dy * s), (cx + 58 * s, y - 10 * s + dy * s)], (60, 40, 24), 4 * s)

def tent(p, cx, base, s, col=(120, 84, 60), light=(255, 196, 110)):
    """A plain desert tent of woven cloth with warm lamplight in its open side."""
    p.glow(cx, base - 120 * s, 360 * s, light, .45)
    p.poly([(cx - 300 * s, base), (cx - 230 * s, base - 200 * s), (cx, base - 250 * s), (cx + 230 * s, base - 200 * s), (cx + 300 * s, base)], col)
    for k in range(-2, 3): p.line([(cx + k * 110 * s, base - 240 * s + abs(k) * 18 * s), (cx + k * 130 * s, base)], lc(col, (0, 0, 0), .25), 3, 200)
    p.poly([(cx + 40 * s, base), (cx + 70 * s, base - 150 * s), (cx + 170 * s, base - 140 * s), (cx + 190 * s, base)], light)
    p.glow(cx + 115 * s, base - 70 * s, 120 * s, light, .6)

def shirt(p, cx, cy, s, col=(214, 200, 172), stain=(128, 22, 24)):
    """A plain long shirt laid flat on a stone, with a dark stain (the false blood of 12:18). Object only."""
    p.ell(cx, cy + 210 * s, 360 * s, 70 * s, (70, 60, 64))                                  # flat stone
    body = [(cx - 120 * s, cy - 170 * s), (cx - 40 * s, cy - 190 * s), (cx, cy - 165 * s), (cx + 40 * s, cy - 190 * s), (cx + 120 * s, cy - 170 * s),
            (cx + 260 * s, cy - 90 * s), (cx + 220 * s, cy - 30 * s), (cx + 130 * s, cy - 80 * s), (cx + 140 * s, cy + 200 * s), (cx - 140 * s, cy + 200 * s),
            (cx - 130 * s, cy - 80 * s), (cx - 220 * s, cy - 30 * s), (cx - 260 * s, cy - 90 * s)]
    p.poly(body, col)
    p.line([(cx - 40 * s, cy - 190 * s), (cx, cy - 165 * s), (cx + 40 * s, cy - 190 * s)], lc(col, (0, 0, 0), .3), 4 * s)
    for dx in (-60, 0, 60): p.line([(cx + dx * s, cy - 100 * s), (cx + dx * 1.2 * s, cy + 190 * s)], lc(col, (0, 0, 0), .12), 3 * s)
    p.ell(cx + 30 * s, cy + 40 * s, 52 * s, 36 * s, stain, 200); p.ell(cx - 20 * s, cy + 80 * s, 28 * s, 20 * s, stain, 180)
    p.ell(cx + 70 * s, cy + 5 * s, 18 * s, 13 * s, stain, 170)

def well_inside(p, top_y=420, r=170):
    """Looking up from the bottom of a well: dark stone rings closing in on a small circle of sky."""
    p.sky([(0, (18, 16, 22)), (1, (6, 6, 10))])
    for k in range(9, 0, -1):                       # stone rings, smaller and lighter toward the opening
        rr = r + k * 120; c = lc((14, 12, 16), (70, 60, 58), 1 - k / 10)
        p.ell(540, top_y + k * 70, rr, rr * .9, c)
        p.ell(540, top_y + k * 70, rr - 14, (rr - 14) * .9, lc(c, (0, 0, 0), .25))
    p.ell(540, top_y, r, r * .9, (150, 190, 235)); p.ell(540, top_y, r * .8, r * .72, (205, 225, 250))
    p.glow(540, top_y, r * 3, (200, 225, 255), .8)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (10, 14, 40)), (.45, (50, 50, 96)), (.72, (220, 130, 90)), (.84, (255, 190, 120)), (1, (60, 34, 30))])
    stars(p, 120, 1, 700); moon(p, 820, 260, 50)
def hook_mid(p): dunes(p, 1300, 26, (120, 70, 56), (60, 34, 30), 2)
def hook_near(p):
    dunes(p, 1500, 14, (70, 40, 34), (24, 14, 12), 3)
    stone_well(p, 540, 1460, 1.25, (120, 90, 70))

def dream_sky(p):
    p.sky([(0, (4, 6, 26)), (.5, (16, 22, 64)), (.85, (40, 40, 96)), (1, (10, 10, 24))])
    stars(p, 260, 11, 1300, (200, 210, 255))
def dream_mid(p):
    # eleven bright stars, the sun and the moon in one arc (the dream of 12:4); symbols only
    for i in range(11):
        a = math.radians(200 + i * 14); x = 540 - 420 * math.cos(a); y = 1320 + 420 * math.sin(a)
        p.glow(x, y, 70, (255, 240, 200), .9); p.ell(x, y, 9, 9, (255, 250, 235))
    sun(p, 400, 1260, 62, (255, 214, 140)); p.glow(400, 1260, 300, (255, 170, 80), .6)
    moon(p, 690, 1260, 54); p.glow(690, 1260, 260, (200, 215, 255), .5)
def dream_near(p): dunes(p, 1480, 10, (26, 26, 52), (8, 8, 18), 13)

def plan_sky(p):
    p.sky([(0, (30, 16, 30)), (.5, (110, 50, 50)), (.78, (220, 110, 60)), (1, (50, 22, 18))])
    cloud_bank(p, 760, (60, 30, 40), (100, 50, 50), 21, 70, 230)
def plan_mid(p):
    mountains(p, 1250, 160, (64, 30, 30), 22, rim=(200, 110, 70))
    tent(p, 760, 1330, .55, (90, 60, 46))
def plan_near(p): dunes(p, 1480, 18, (80, 40, 30), (24, 10, 8), 23)

def day_sky(p):
    p.sky([(0, (60, 110, 170)), (.5, (150, 180, 200)), (.78, (240, 210, 160)), (1, (150, 110, 70))])
    sun(p, 860, 300, 70, (255, 246, 220)); p.glow(860, 300, 400, (255, 230, 180), .5)
def day_mid(p):
    dunes(p, 1280, 30, (214, 170, 118), (170, 120, 80), 31)
    palm(p, 200, 1300, 340, (70, 60, 40), -.1)
def day_near(p):
    dunes(p, 1480, 16, (196, 146, 96), (120, 80, 50), 32)
    stone_well(p, 560, 1440, 1.5, (150, 120, 92))

def inside(p): well_inside(p, 330, 150)

def home_sky(p):
    p.sky([(0, (4, 6, 20)), (.5, (12, 16, 42)), (.85, (30, 30, 60)), (1, (8, 8, 16))])
    stars(p, 200, 51, 900)
def home_mid(p): dunes(p, 1340, 14, (30, 28, 48), (10, 10, 20), 52)
def home_near(p):
    shirt(p, 540, 860, 1.25)
    lantern(p, 900, 760, .6, (255, 190, 100))

def patience_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (24, 34, 78)), (.75, (70, 70, 120)), (1, (14, 12, 26))])
    stars(p, 220, 61, 1100); moon(p, 540, 1050, 70, crescent=False, col=(240, 236, 220)); p.glow(540, 1050, 420, (200, 210, 255), .5)
def patience_mid(p): dunes(p, 1360, 14, (40, 40, 70), (14, 14, 26), 62)
def patience_near(p): tent(p, 540, 1500, .9, (70, 54, 50))

def caravan_sky(p):
    p.sky([(0, (70, 120, 180)), (.5, (170, 190, 205)), (.8, (250, 214, 160)), (1, (170, 120, 80))])
def caravan_mid(p):
    dunes(p, 1300, 26, (220, 176, 124), (180, 130, 88), 71)
    for x in (130, 300, 470): camel(p, x, 1330, .42, (110, 76, 50))
def caravan_near(p):
    dunes(p, 1500, 14, (200, 150, 100), (130, 86, 54), 72)
    bucket(p, 760, 930, 1.3)

def egypt_sky(p):
    p.sky([(0, (40, 30, 70)), (.4, (160, 90, 100)), (.66, (255, 160, 90)), (.8, (255, 210, 140)), (1, (70, 40, 30))])
    sun(p, 640, 1180, 90, (255, 220, 160)); p.glow(640, 1180, 520, (255, 150, 80), .6)
def egypt_mid(p): pyramids(p, 1290, (150, 86, 60), (100, 54, 40))
def egypt_near(p):
    p.rect(-100, 1300, 1200, 1400, (80, 110, 140)); p.line([(100, 1330), (400, 1330)], (255, 200, 140), 3, 160); p.line([(600, 1360), (900, 1360)], (255, 200, 140), 3, 140)
    dunes(p, 1440, 12, (110, 70, 46), (40, 24, 16), 82)
    palm(p, 900, 1460, 360, (40, 30, 22), .1)

def lesson_sky(p):
    p.sky([(0, (40, 70, 130)), (.45, (150, 170, 200)), (.72, (250, 210, 160)), (1, (140, 100, 70))])
    rays(p, 540, 1100, (255, 236, 190), n=9, spread=80, angle=-90, a=.18)
    sun(p, 540, 1150, 70, (255, 244, 214))
def lesson_mid(p): dunes(p, 1320, 24, (220, 180, 130), (170, 130, 90), 91)
def lesson_near(p):
    dunes(p, 1500, 12, (190, 146, 100), (110, 76, 50), 92)
    stone_well(p, 540, 1460, 1.15, (160, 130, 100), rope=False)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): pyramids(p, 1330, (60, 46, 64), (40, 30, 46))
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['twinkle'], cam='in', bloom=.65,
         title=dict(text='Thrown into a well', arabic=TITLE_AR, part='Part 1 of 3', hold=99, plain=True),
         lines=['His brothers threw him into a well. What did Allah tell him there?']),
    dict(layers=[dream_sky, dream_mid, dream_near], fx=['twinkle'], cam='up',
         verse=dict(key='12:4', ar=(4, 15), en='O my father, indeed I have seen [in a dream] eleven stars and the sun and the moon; I saw them prostrating to me', line=1, ar_size=70),
         lines=['Young Yusuf, peace be upon him, told his father a dream:',
                'O my father, indeed I have seen eleven stars and the sun and the moon; I saw them prostrating to me.']),
    dict(layers=[plan_sky, plan_mid, plan_near], fx=['sand'], cam='in',
         lines=['But his brothers felt their father loved Yusuf more.']),
    dict(layers=[day_sky, day_mid, day_near], fx=['dust'], cam='in', pause=0.5,
         lines=['They took him out to play, and put him down into a dark well.']),
    dict(layers=[inside], fx=['dust'], cam='hold', bloom=.75,
         verse=dict(key='12:15', ar=(11, 17), en='You will surely inform them [someday] about this affair of theirs while they do not perceive [your identity]', line=1, ar_size=74, y=700),
         lines=['Down there, Allah inspired him:',
                'You will surely inform them someday about this affair of theirs, while they do not perceive.']),
    dict(layers=[home_sky, home_mid, home_near], fx=['twinkle'], cam='in', pause=0.5,
         lines=['At night they came home weeping, with false blood on his shirt.', 'And his father?']),
    dict(layers=[patience_sky, patience_mid, patience_near], fx=['twinkle'], cam='up',
         verse=dict(key='12:18', ar=(6, 13), en='Rather, your souls have enticed you to something, so patience is most fitting', line=0, ar_size=78),
         lines=['Rather, your souls have enticed you to something, so patience is most fitting.']),
    dict(layers=[caravan_sky, caravan_mid, caravan_near], fx=['dust'], cam='down',
         lines=['Travelers let down a bucket. Up came a boy.']),
    dict(layers=[egypt_sky, egypt_mid, egypt_near], fx=['embers'], cam='in',
         lines=['They sold him for a few coins. A man from Egypt bought him.']),
    dict(layers=[lesson_sky, lesson_mid, lesson_near], fx=['dust'], cam='out',
         lesson=dict(text='The well was not the end of his story.', after=0, y=560), no_caption=(0,),
         lines=['The well was not the end of his story.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Part 2 tomorrow', line2='Follow Quranic Story'),
         lines=['In Egypt, a new test was waiting. Part 2 tomorrow, in sha Allah.',
                'Share this with someone in a hard time. And follow for a new story from the Quran every day.']),
]

PRON = {'Yusuf': 'jˈuːsʊf', 'Yaqub': 'jɑːkˈuːb', 'in sha Allah': 'ˌɪn ʃɑː ˈælə'}

CAPTION = """His own brothers threw him into a well. What did Allah tell him down there? 🤍 (Part 1 of 3)

Young Yusuf (peace be upon him) told his father: "O my father, indeed I have seen [in a dream] eleven stars and the sun and the moon; I saw them prostrating to me." (Quran 12:4)

His brothers felt their father loved him more (12:8). They put him into the bottom of a well. Then Allah inspired him: "You will surely inform them [someday] about this affair of theirs while they do not perceive [your identity]." (Quran 12:15)

They came home weeping, with false blood on his shirt. His father said: "Rather, your souls have enticed you to something, so patience is most fitting." (Quran 12:18)

Travelers found him. He was sold for a few dirhams, and a man from Egypt bought him (12:19–21).

The well was not the end of his story.

📖 Sources: Quran 12:4–22 (Saheeh International)
Part 2 tomorrow, in sha Allah. Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetYusuf #IslamicReminder"""

FIRST_COMMENT = """When did a hard time in your life turn out to be the start of something good? 🤍

References: Quran, Surah Yusuf 12:4–22 (Saheeh International translation). Part 2 tomorrow, in sha Allah."""
