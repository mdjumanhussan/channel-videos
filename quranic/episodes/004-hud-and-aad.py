"""Story 4: Prophet Hud and the people of 'Aad. Sources: Quran 46:21-26, 7:65-72, 11:50-60, 41:15-16, 69:6-8, 89:6-8, 26:123-140 (Saheeh International).
No figures are drawn: desert, pillars, fortresses, clouds, wind and sand only.
Improvement tried today: a "wrong answer" hook. Frame 1 sets up what the people expected (a rain cloud, 46:24) and says at once
that they were wrong, without saying what it really was. The reversal is paid off in scene 7, after a pause."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  4'
VOICE, SPEED = 'bm_george', 1.0
THUMB_AT = 1.6
TITLE = "Prophet Hud and the People of 'Aad: The Cloud That Was Not Rain"
HITS = [(6, 0, 0.0)]
# "This is a cloud bringing us rain", taken straight from the text of 46:24
TITLE_AR = ' '.join(quran()['verses']['46:24']['ar'].split()[6:9])

# ---------------------------------------------------------------- small scenery helpers for this story
def pillars(p, cx, base, n, gap, h, col, cap, seed, w=46, lintel=True):
    """A row of tall stone columns ("Iram, who had lofty pillars"). Stone only."""
    rnd = random.Random(seed); xs = [cx + (i - (n - 1) / 2) * gap for i in range(n)]
    for x in xs:
        p.rect(x - w / 2, base - h, x + w / 2, base, col)
        p.rect(x - w / 2, base - h, x - w / 2 + w * .28, base, lc(col, (255, 230, 180), .25))
        for k in (.35, .65): p.line([(x - w / 2 + w * k, base - h + 20), (x - w / 2 + w * k, base - 20)], lc(col, (0, 0, 0), .25), 2)
        p.rect(x - w * .75, base - h - 26, x + w * .75, base - h, cap)
        p.rect(x - w * .7, base - 22, x + w * .7, base, cap)
    if lintel: p.rect(xs[0] - w, base - h - 60, xs[-1] + w, base - h - 24, cap)

def ruins(p, cx, base, n, gap, col, cap, seed, w=44):
    """Broken columns and fallen drums: what was left."""
    rnd = random.Random(seed)
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * gap; h = rnd.uniform(.15, .65) * 520
        p.rect(x - w / 2, base - h, x + w / 2, base, col)
        p.poly([(x - w / 2, base - h), (x + w / 2, base - h - rnd.uniform(-30, 30)), (x + w / 2, base - h + 10), (x - w / 2, base - h + 10)], col)
        p.rect(x - w * .7, base - 20, x + w * .7, base, cap)
    for k in range(3):                                          # fallen drums on the sand
        x = cx + rnd.uniform(-380, 380); r = w * .5
        p.poly([(x - 70, base - r * 2 + 6), (x + 70, base - r * 2 - 4), (x + 74, base + 2), (x - 66, base + 10)], lc(col, cap, .3))

def fortress(p, cx, base, s, col, win=None):
    """A palace-fortress on a hilltop (26:128-129). Building only."""
    p.poly([(cx - 260 * s, base + 40 * s), (cx - 120 * s, base - 20 * s), (cx + 130 * s, base - 30 * s), (cx + 280 * s, base + 40 * s)], lc(col, (0, 0, 0), .2))
    p.rect(cx - 150 * s, base - 200 * s, cx + 150 * s, base, col)
    for tx in (-170, 170): p.rect(cx + tx * s - 40 * s, base - 300 * s, cx + tx * s + 40 * s, base, col)
    p.rect(cx - 45 * s, base - 380 * s, cx + 45 * s, base - 200 * s, col)
    for x0, x1, top in ((-150, 150, -200), (-210, -130, -300), (130, 210, -300), (-45, 45, -380)):
        k = x0
        while k < x1: p.rect(cx + k * s, base + (top - 22) * s, cx + (k + 14) * s, base + top * s, col); k += 26
    if win:
        for wx, wy in ((-80, -120), (0, -140), (80, -120), (-170, -230), (170, -230), (0, -300)):
            p.rect(cx + wx * s - 8 * s, base + wy * s - 14 * s, cx + wx * s + 8 * s, base + wy * s + 14 * s, win, 230)
            p.glow(cx + wx * s, base + wy * s, 30 * s, win, .35)

def storm_wall(p, y, top, bot, seed, rim=(200, 170, 130), bump=110):
    """A huge cloud bank rolling in from above, its lower edge at about y. Soft billows with lit undersides."""
    rnd = random.Random(seed)
    t = P(); t.grad_poly([(-250, -400), (1330, -400), (1330, y - bump * .6), (-250, y - bump * .6)], top, bot, -200, y)
    x = -260; puffs = []
    while x < 1340:
        r = rnd.uniform(bump * .8, bump * 1.5); puffs.append((x, y + rnd.uniform(-bump * .4, bump * .1), r)); x += r * rnd.uniform(.9, 1.3)
    for x, yy, r in puffs: t.ell(x, yy + r * .18, r * 1.05, r * .62, lc(bot, rim, .45))      # lit underside
    for x, yy, r in puffs: t.ell(x, yy, r, r * .6, bot)
    for x, yy, r in puffs: t.ell(x + rnd.uniform(-r * .3, r * .3), yy - r * .55, r * .9, r * .6, lc(top, bot, .55))
    p.img.alpha_composite(t.img.filter(ImageFilter.GaussianBlur(7 * SS))); p.d = ImageDraw.Draw(p.img)

def spring_pool(p, cx, y, w, col=(110, 190, 200)):
    p.ell(cx, y, w, w * .16, lc(col, (0, 0, 0), .35)); p.ell(cx, y - 4, w * .92, w * .13, col)
    for k in range(3): p.line([(cx - w * .5 + k * 40, y - 4), (cx - w * .3 + k * 40, y - 4)], (230, 250, 255), 2, 160)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (40, 34, 40)), (.4, (120, 90, 70)), (.66, (230, 170, 100)), (1, (90, 56, 30))])
    p.glow(820, 1150, 420, (255, 200, 120), .6)
def hook_cloud(p): storm_wall(p, 900, (26, 22, 26), (92, 74, 66), 11)
def hook_mid(p): mountains(p, 1400, 230, (110, 70, 44), 12, rim=(255, 190, 120))
def hook_near(p):
    dunes(p, 1580, 60, (196, 140, 80), (90, 56, 30), 13)
    palm(p, 170, 1640, 360, (50, 30, 18), .06); palm(p, 930, 1620, 300, (50, 30, 18), .04)

def iram_sky(p):
    p.sky([(0, (40, 90, 150)), (.45, (150, 180, 200)), (.66, (255, 214, 150)), (1, (150, 100, 60))])
    sun(p, 860, 760, 80); clouds(p, 21, 300, 700, (255, 240, 220), 5, 120)
def iram_far(p): mountains(p, 1420, 160, (170, 130, 110), 22)
def iram_mid(p):
    dunes(p, 1500, 30, (220, 170, 110), (160, 110, 60), 23)
    p.glow(540, 1150, 420, (255, 220, 160), .35)
    pillars(p, 540, 1500, 7, 140, 620, (200, 160, 110), (226, 190, 140), 24)
def iram_near(p): dunes(p, 1700, 50, (170, 116, 64), (60, 38, 20), 25)

def hud_sky(p):
    p.sky([(0, (30, 26, 70)), (.45, (120, 90, 140)), (.68, (255, 190, 150)), (1, (80, 50, 50))])
    stars(p, 70, 31, 600); p.glow(540, 1260, 460, (255, 210, 160), .8); sun(p, 540, 1300, 70)
def hud_mid(p): dunes(p, 1360, 80, (160, 110, 110), (90, 60, 66), 32)
def hud_near(p):
    dunes(p, 1560, 60, (110, 70, 66), (36, 22, 24), 33)
    palm(p, 140, 1600, 420, (30, 18, 20), .05); palm(p, 950, 1580, 340, (30, 18, 20), -.06)

def rain_sky(p):
    p.sky([(0, (70, 110, 140)), (.45, (160, 196, 200)), (.68, (240, 236, 200)), (1, (90, 120, 80))])
    clouds(p, 41, 300, 650, (240, 246, 250), 7, 170)
    rnd = random.Random(46)                                    # soft rain falling far away
    for _ in range(70):
        x, y = rnd.uniform(180, 900), rnd.uniform(620, 1000); p.line([(x, y), (x - 8, y + 40)], (230, 240, 250), 2, 90)
def rain_mid(p): mountains(p, 1360, 180, (110, 140, 120), 42)
def rain_near(p):
    dunes(p, 1480, 40, (120, 160, 90), (60, 96, 50), 43)
    tree(p, 230, 1500, 360, (70, 50, 30), (70, 130, 70), 44); tree(p, 870, 1480, 300, (70, 50, 30), (90, 150, 80), 45)
    palm(p, 560, 1490, 330, (50, 70, 40), .03)
    spring_pool(p, 560, 1560, 300)

def mock_sky(p):
    p.sky([(0, (30, 10, 20)), (.45, (110, 40, 40)), (.68, (230, 110, 60)), (1, (40, 16, 16))])
    clouds(p, 51, 400, 900, (200, 90, 70), 6, 120); p.glow(540, 1200, 420, (255, 140, 80), .5)
def mock_mid(p):
    mountains(p, 1420, 300, (70, 30, 30), 52, peaks=4)
    for cx, base, s_, col in ((300, 1180, .7, (50, 20, 24)), (790, 1250, .9, (40, 16, 20))):
        p.poly([(cx - 420, 1650), (cx - 170, base + 8), (cx + 170, base + 8), (cx + 420, 1650)], col)   # the hill under it
        fortress(p, cx, base, s_, col, (255, 190, 110))
def mock_near(p): dunes(p, 1600, 50, (50, 22, 22), (14, 6, 8), 53)

def valley_sky(p):
    p.sky([(0, (30, 30, 36)), (.4, (120, 100, 90)), (.66, (236, 180, 110)), (1, (100, 66, 36))])
def valley_cloud(p): storm_wall(p, 1020, (20, 18, 22), (80, 66, 60), 61)
def valley_mid(p):
    mountains(p, 1360, 300, (120, 80, 50), 62, rim=(255, 196, 130))
    for x in (380, 700): p.glow(x, 1300, 70, (255, 200, 120), .5)  # the valley towns
    city(p, 1380, (70, 46, 30), 63, lights=(255, 196, 110), domes=False)
def valley_near(p): dunes(p, 1600, 60, (190, 130, 70), (80, 50, 26), 64)

def wind_sky(p):
    p.sky([(0, (20, 12, 10)), (.4, (90, 50, 30)), (.66, (170, 100, 50)), (1, (50, 26, 14))])
def wind_cloud(p): storm_wall(p, 1080, (16, 10, 8), (110, 66, 36), 71, rim=(230, 150, 80), bump=140)
def wind_mid(p):
    mountains(p, 1420, 240, (70, 40, 22), 72)
    p.glow(540, 1200, 500, (220, 130, 60), .4)
def wind_near(p):
    dunes(p, 1600, 70, (120, 70, 36), (40, 22, 10), 73)
    for x, h in ((150, 380), (420, 330), (900, 360)): palm(p, x, 1640, h, (30, 16, 10), .32)

def nights_sky(p):
    p.sky([(0, (8, 8, 14)), (.45, (40, 30, 30)), (.68, (90, 60, 40)), (1, (20, 12, 10))])
    moon(p, 820, 340, 50, col=(220, 190, 150)); clouds(p, 81, 200, 900, (90, 60, 40), 10, 200)
def nights_mid(p):
    dunes(p, 1520, 50, (90, 62, 44), (40, 26, 20), 82)
    p.glow(540, 1380, 420, (200, 150, 100), .35)
    ruins(p, 540, 1530, 7, 140, (150, 116, 84), (176, 136, 98), 83)
def nights_near(p): dunes(p, 1700, 70, (60, 40, 26), (14, 8, 6), 84)

def saved_sky(p):
    p.sky([(0, (80, 150, 210)), (.45, (190, 220, 230)), (.66, (255, 236, 190)), (1, (140, 150, 90))])
    sun(p, 540, 980, 90)
    rays(p, 540, 980, (255, 244, 210), n=14, spread=360, length=1600, width=3, a=.22, angle=0, seed=91)
def saved_mid(p): mountains(p, 1340, 180, (150, 160, 130), 92)
def saved_near(p):
    dunes(p, 1500, 40, (200, 190, 120), (120, 120, 60), 93)
    palm(p, 200, 1540, 400, (60, 70, 40), -.04); palm(p, 880, 1520, 340, (60, 70, 40), .05)
    spring_pool(p, 540, 1600, 260, (120, 200, 210))

def end_sky(p):
    p.sky([(0, (6, 10, 30)), (.45, (30, 30, 70)), (.68, (120, 80, 80)), (.76, (230, 160, 100)), (1, (30, 16, 12))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p):
    dunes(p, 1380, 50, (60, 40, 50), (24, 16, 20), 102)
    mosque(p, 540, 1380, .9, (14, 10, 18), windows=(255, 206, 130))
def end_near(p): lantern(p, 170, 1160, .9)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_cloud, hook_mid, hook_near], fx=['sand', 'dust'], cam='in', bloom=.6,
         title=dict(kicker='Story 4  ·  from the Quran', text='They thought it was rain', arabic=TITLE_AR, hold=99),
         lines=['They saw a cloud coming and said: rain! They were wrong.']),
    dict(layers=[iram_sky, iram_far, iram_mid, iram_near], fx=['dust'], cam='up',
         verse=dict(key='41:15', ar=(8, 12), en='Who is greater than us in strength?', line=1, ar_size=90),
         lines=["The people of 'Aad were strong, and proud.", 'They said: Who is greater than us in strength?']),
    dict(layers=[hud_sky, hud_mid, hud_near], fx=['twinkle', 'dust'], cam='right',
         verse=dict(key='7:65', ar=(5, 13), en='O my people, worship Allah; you have no deity other than Him', line=1, ar_size=78),
         lines=['Allah sent them Hud, peace be upon him.', 'O my people, worship Allah; you have no deity other than Him.']),
    dict(layers=[rain_sky, rain_mid, rain_near], fx=['dust'], cam='in',
         lines=["He told them: ask your Lord's forgiveness, and He will send you rain."]),
    dict(layers=[mock_sky, mock_mid, mock_near], fx=['embers'], cam='left',
         verse=dict(key='46:22', ar=(5, 12), en='Then bring us what you promise us, if you should be of the truthful', line=1, ar_size=78),
         lines=['They mocked him:', 'Then bring us what you promise us, if you should be of the truthful.']),
    dict(layers=[valley_sky, valley_cloud, valley_mid, valley_near], fx=['dust'], cam='down', pause=0.5,
         verse=dict(key='46:24', ar=(6, 9), en='This is a cloud bringing us rain!', line=1, ar_size=90),
         lines=['Then a cloud came toward their valleys. They said:', 'This is a cloud bringing us rain!']),
    dict(layers=[wind_sky, wind_cloud, wind_mid, wind_near], fx=[('sand', dict(n=220)), 'dust'], cam='in', bloom=.5,
         verse=dict(key='46:24', ar=(9, 18), en='Rather, it is that for which you were impatient: a wind, within it a painful punishment', line=1, ar_size=72),
         lines=['It was not rain.', 'Rather, it is that for which you were impatient: a wind, within it a painful punishment.']),
    dict(layers=[nights_sky, nights_mid, nights_near], fx=['sand'], cam='out',
         lines=['A screaming wind blew for seven nights and eight days.', 'Only their dwellings were left to be seen.']),
    dict(layers=[saved_sky, saved_mid, saved_near], fx=['dust'], cam='up',
         verse=dict(key='11:58', ar=(3, 10), en='We saved Hud and those who believed with him, by mercy from Us', line=0, ar_size=78),
         lines=['We saved Hud and those who believed with him, by mercy from Us.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'dust'], cam='in',
         end=dict(after=1, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['Strength could not save them. Turning back to Allah can.', 'Share this with someone you love. And follow for a new story from the Quran every day.']),
]

PRON = {"'Aad": 'ˈɑːd', 'Hud': 'hˈuːd'}

CAPTION = """They saw a cloud coming and said: rain! They were wrong. 🤍

The people of 'Aad were strong and proud. They said: "Who is greater than us in strength?" (Quran 41:15)

Allah sent them their brother Hud (peace be upon him). He called them to worship Allah alone and to ask His forgiveness. They mocked him and said: "Then bring us what you promise us." (Quran 46:22)

Then they saw a cloud coming toward their valleys and said, "This is a cloud bringing us rain!" (Quran 46:24)

"Rather, it is that for which you were impatient: a wind, within it a painful punishment." (Quran 46:24) Allah saved Hud and the believers by His mercy.

Strength could not save them. Turning back to Allah can.

📖 Sources: Quran 46:21–26, 7:65–72, 11:50–60, 41:15–16, 69:6–8 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetHud #IslamicReminder"""

FIRST_COMMENT = """What did this story teach you? 🤍

References: Quran, Surah Al-Ahqaf 46:21–26; Surah Al-A'raf 7:65–72; Surah Hud 11:50–60; Surah Fussilat 41:15–16; Surah Al-Haqqah 69:6–8; Surah Al-Fajr 89:6–8 (Saheeh International translation)."""
