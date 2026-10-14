"""Story 5: Prophet Salih and the she-camel. Sources: Quran 7:73-79, 11:61-68, 26:141-159, 54:23-31, 91:11-15, 17:59 (Saheeh International).
No people are drawn: cliffs, carved rock homes, palms, springs, sky, and the she-camel (an animal) only.
Improvement tried today: no title card. Frame 1 is the story picture with the hook headline already fully on screen
(no star ornament, no kicker, no animate-in; engine title option plain=True), and speech starts at 0.25 s.
Reason: average watch fell to 3 s on episode 4; guidance says a title card / slow intro loses people in the first 2 seconds."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  5'
VOICE, SPEED = 'bm_george', 1.0
THUMB_AT = 1.2
TITLE = 'Prophet Salih and the She-Camel of Allah'
HITS = [(6, 0, 0.0), (8, 0, 0.0)]
# "This is the she-camel of Allah", taken straight from the text of 7:73
TITLE_AR = ' '.join(quran()['verses']['7:73']['ar'].split()[18:21])

# ---------------------------------------------------------------- small scenery helpers for this story
def cliff(p, x0, x1, top, base, col, seed, rim=None, streaks=True):
    """A tall sandstone cliff / rock outcrop with a ragged top."""
    rnd = random.Random(seed); pts = [(x0, base)]; x = x0
    pts.append((x0 + rnd.uniform(10, 40), top + rnd.uniform(40, 90)))
    while x < x1 - 60:
        x += rnd.uniform(40, 90); pts.append((x, top + rnd.uniform(-20, 50)))
    pts += [(x1 - rnd.uniform(10, 40), top + rnd.uniform(40, 90)), (x1, base)]
    p.poly(pts, col)
    for k in range(5 if streaks else 0):                         # vertical weathering streaks
        xx = rnd.uniform(x0 + 40, x1 - 40); p.line([(xx, top + 80), (xx + rnd.uniform(-10, 10), base)], lc(col, (0, 0, 0), .15), 6, 120)
    if rim:
        for i in range(1, len(pts) - 2): p.line([pts[i], pts[i + 1]], rim, 3, 140)

def rock_home(p, cx, base, w, h, col, door=None):
    """A home carved into the rock face (7:74, 26:149): recessed facade, doorway, stepped crown. Stone only."""
    dk = lc(col, (0, 0, 0), .3); lt = lc(col, (255, 230, 190), .18)
    p.rect(cx - w / 2, base - h, cx + w / 2, base, lt)                      # smoothed facade
    p.rect(cx - w / 2, base - h, cx - w / 2 + 6, base, dk); p.rect(cx + w / 2 - 6, base - h, cx + w / 2, base, dk)
    bw = w * .14
    for k in range(3):                                                      # stepped crown
        for sx in (-1, 1):
            xc = cx + sx * (w / 2 - bw / 2 - k * bw); p.rect(xc - bw / 2, base - h - 24 * (k + 1), xc + bw / 2, base - h, lt)
    p.rect(cx - w * .5, base - h - 8, cx + w * .5, base - h, dk)           # cornice
    dw, dh = w * .32, h * .5
    p.rect(cx - dw / 2 - 10, base - dh - 18, cx + dw / 2 + 10, base - dh - 6, dk)
    p.rect(cx - dw / 2, base - dh, cx + dw / 2, base, door or lc(col, (0, 0, 0), .65))
    if door: p.glow(cx, base - dh / 2, dw * 1.4, door, .45)

def cliff_homes(p, cx, base, n, gap, col, seed, door=None, top=None, streaks=True):
    rnd = random.Random(seed); top = top if top is not None else base - 560
    cliff(p, cx - n * gap / 2 - 120, cx + n * gap / 2 + 120, top, base + 400, col, seed, rim=lc(col, (255, 220, 170), .5), streaks=streaks)
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * gap; b = base - rnd.uniform(0, 140); s = rnd.uniform(.8, 1.1)
        rock_home(p, x, b, 130 * s, 210 * s, col, door)

def camel(p, cx, base, s=1.0, col=(30, 20, 14), flip=False, drink=False):
    """The she-camel, side view, standing at (cx, base). An animal only."""
    k = -1 if flip else 1
    def X(dx): return cx + k * dx * s
    def Y(dy): return base + dy * s
    for lx, ph in ((-105, 0), (-70, 1), (80, 0), (110, 1)):                 # legs with knees
        sh = lc(col, (0, 0, 0), .25) if ph else col
        p.line([(X(lx), Y(-240)), (X(lx + 6), Y(-120))], sh, 20 * s); p.line([(X(lx + 6), Y(-120)), (X(lx), Y(-6))], sh, 14 * s)
        p.ell(X(lx + 6), Y(-120), 11 * s, 12 * s, sh)
        p.ell(X(lx + 8), Y(-4), 16 * s, 7 * s, sh)
    p.ell(X(-5), Y(-268), 160 * s, 66 * s, col)                             # body
    p.poly([(X(-150), Y(-290)), (X(-150), Y(-250)), (X(-110), Y(-200)), (X(-60), Y(-230))], col)      # rump
    p.ell(X(-15), Y(-322), 88 * s, 64 * s, col)                             # hump
    p.line([(X(-160), Y(-290)), (X(-178), Y(-230)), (X(-172), Y(-190))], col, 8 * s)                 # tail
    if drink:
        p.poly([(X(110), Y(-310)), (X(160), Y(-240)), (X(250), Y(-110)), (X(235), Y(-80)), (X(130), Y(-210)), (X(95), Y(-250))], col)
        p.ell(X(262), Y(-80), 40 * s, 21 * s, col); p.ell(X(296), Y(-66), 18 * s, 14 * s, col)
    else:
        p.poly([(X(105), Y(-315)), (X(155), Y(-235)), (X(205), Y(-300)), (X(235), Y(-400)), (X(205), Y(-415)), (X(180), Y(-330)), (X(130), Y(-300))], col)
        p.ell(X(240), Y(-418), 44 * s, 22 * s, col); p.ell(X(278), Y(-408), 18 * s, 14 * s, col)   # head and muzzle
        p.poly([(X(215), Y(-434)), (X(210), Y(-458)), (X(226), Y(-438))], col)                       # ear
        p.ell(X(245), Y(-424), 4 * s, 4 * s, lc(col, (255, 230, 200), .5))

def spring_pool(p, cx, y, w, col=(110, 190, 200), a=255):
    p.ell(cx, y, w, w * .16, lc(col, (0, 0, 0), .35), a); p.ell(cx, y - 4, w * .92, w * .13, col, a)
    for k in range(3): p.line([(cx - w * .5 + k * 40, y - 4), (cx - w * .3 + k * 40, y - 4)], (230, 250, 255), 2, 160)

def bolt(p, x, y0, y1, seed, col=(240, 236, 255)):
    rnd = random.Random(seed); pts = [(x, y0)]; y = y0
    while y < y1:
        y += rnd.uniform(50, 110); x += rnd.uniform(-70, 70); pts.append((x, y))
    p.glow(pts[len(pts) // 2][0], pts[len(pts) // 2][1], 420, (200, 190, 255), .5)
    p.line(pts, (190, 180, 255), 16, 120); p.line(pts, col, 6)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (40, 14, 30)), (.4, (150, 50, 50)), (.64, (250, 160, 80)), (1, (70, 30, 20))])
    p.glow(640, 1180, 520, (255, 190, 110), .75); sun(p, 640, 1230, 90, (255, 210, 140))
def hook_far(p): cliff_homes(p, 160, 1330, 2, 230, (110, 50, 40), 3, door=(255, 170, 90), top=880)
def hook_mid(p): dunes(p, 1500, 50, (120, 56, 36), (60, 24, 18), 4)
def hook_near(p):
    camel(p, 640, 1560, .95, (36, 14, 14))
    dunes(p, 1600, 30, (70, 30, 22), (20, 8, 8), 5)

def thamud_sky(p):
    p.sky([(0, (60, 120, 180)), (.45, (170, 205, 225)), (.66, (255, 232, 190)), (1, (150, 120, 70))])
    clouds(p, 11, 260, 620, (255, 250, 240), 5, 140); sun(p, 870, 520, 70)
def thamud_far(p): cliff_homes(p, 540, 1320, 5, 190, (196, 120, 80), 12, top=780)
def thamud_near(p):
    dunes(p, 1440, 30, (120, 160, 80), (60, 100, 50), 13)
    spring_pool(p, 540, 1500, 260)
    for x, h, ln in ((90, 420, -.05), (260, 340, .04), (830, 360, -.03), (1000, 440, .06)): palm(p, x, 1560, h, (50, 80, 40), ln)

def salih_sky(p):
    p.sky([(0, (20, 30, 70)), (.42, (110, 110, 160)), (.66, (255, 200, 150)), (1, (90, 60, 60))])
    stars(p, 50, 21, 500); p.glow(540, 1280, 520, (255, 220, 170), .8)
    rays(p, 540, 1300, (255, 236, 200), n=12, spread=150, length=1700, width=4, a=.2, angle=-90, seed=22)
def salih_mid(p): cliff_homes(p, 540, 1420, 4, 230, (120, 90, 100), 23, top=1000)
def salih_near(p): dunes(p, 1580, 50, (90, 66, 70), (30, 20, 24), 24)

def said_sky(p):
    p.sky([(0, (30, 10, 16)), (.45, (120, 36, 36)), (.68, (220, 100, 60)), (1, (40, 14, 12))])
    clouds(p, 31, 380, 900, (190, 80, 60), 6, 120)
def said_mid(p): cliff_homes(p, 540, 1460, 4, 240, (80, 34, 30), 32, door=(255, 180, 100), top=980)
def said_near(p): dunes(p, 1620, 50, (50, 20, 18), (14, 6, 6), 33)

def sign_sky(p):
    p.sky([(0, (70, 140, 200)), (.45, (190, 220, 235)), (.66, (255, 236, 196)), (1, (190, 150, 90))])
    sun(p, 540, 760, 90); rays(p, 540, 760, (255, 246, 210), n=14, spread=360, length=1600, width=3, a=.2, angle=0, seed=41)
def sign_mid(p):
    mountains(p, 1380, 220, (200, 150, 110), 42)
    p.glow(540, 1350, 460, (255, 236, 180), .5)
def sign_near(p):
    dunes(p, 1500, 30, (226, 186, 120), (170, 120, 70), 43)
    spring_pool(p, 300, 1600, 230)
    camel(p, 640, 1560, .9, (120, 70, 40))
    palm(p, 1000, 1600, 400, (90, 80, 40), .05)

def warn_sky(p):
    p.sky([(0, (16, 22, 50)), (.45, (70, 80, 130)), (.68, (200, 140, 130)), (1, (40, 30, 40))])
    clouds(p, 51, 300, 860, (110, 100, 140), 8, 170)
def warn_mid(p): cliff_homes(p, 860, 1400, 2, 220, (70, 60, 80), 52, top=1000)
def warn_near(p):
    dunes(p, 1540, 40, (90, 76, 90), (30, 24, 34), 53)
    spring_pool(p, 380, 1560, 220, (90, 140, 170))
    camel(p, 420, 1520, .55, (24, 18, 26), drink=True)

def dared_sky(p):
    p.sky([(0, (8, 6, 18)), (.45, (36, 20, 44)), (.68, (110, 50, 50)), (1, (16, 8, 14))])
    moon(p, 760, 420, 46, col=(230, 200, 170))
def dared_mid(p): cliff_homes(p, 540, 1420, 4, 230, (40, 26, 40), 62, top=1000, streaks=False)
def dared_near(p):
    dunes(p, 1560, 40, (50, 30, 44), (10, 6, 10), 63)
    spring_pool(p, 540, 1600, 260, (50, 70, 100))

def days_sky(p):
    p.sky([(0, (6, 8, 24)), (.45, (24, 30, 60)), (.68, (70, 60, 80)), (1, (12, 10, 18))])
    stars(p, 160, 71, 1000); moon(p, 300, 420, 50)
def days_mid(p): cliff_homes(p, 540, 1440, 5, 190, (40, 40, 60), 72, door=(255, 190, 110), top=1000)
def days_near(p): dunes(p, 1600, 50, (30, 30, 44), (8, 8, 14), 73)

def blast_sky(p):
    p.sky([(0, (8, 6, 16)), (.45, (40, 30, 60)), (.68, (90, 70, 110)), (1, (14, 10, 20))])
    clouds(p, 81, 100, 700, (70, 60, 100), 10, 220)
    bolt(p, 420, 300, 1000, 82); bolt(p, 760, 420, 900, 83)
def blast_mid(p): cliff_homes(p, 540, 1460, 4, 230, (50, 44, 66), 84, top=1040)
def blast_near(p): dunes(p, 1620, 50, (36, 30, 46), (8, 6, 12), 85)

def saved_sky(p):
    p.sky([(0, (60, 130, 200)), (.45, (180, 215, 230)), (.66, (255, 230, 190)), (1, (140, 150, 90))])
    sun(p, 540, 1000, 90)
    rays(p, 540, 1000, (255, 244, 210), n=14, spread=360, length=1600, width=3, a=.22, angle=0, seed=91)
def saved_mid(p): mountains(p, 1360, 200, (150, 150, 120), 92)
def saved_near(p):
    dunes(p, 1500, 40, (170, 190, 110), (100, 120, 60), 93)
    palm(p, 200, 1560, 420, (50, 80, 40), -.05); palm(p, 880, 1540, 360, (50, 80, 40), .05)
    spring_pool(p, 540, 1600, 260, (120, 200, 210))

def end_sky(p):
    p.sky([(0, (8, 6, 30)), (.45, (40, 26, 70)), (.68, (140, 80, 90)), (.76, (230, 150, 100)), (1, (30, 14, 14))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p):
    dunes(p, 1380, 50, (60, 36, 50), (24, 14, 20), 102)
    mosque(p, 540, 1380, .9, (14, 10, 18), windows=(255, 206, 130))
def end_near(p): lantern(p, 170, 1160, .9)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_far, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.6,
         title=dict(text='They asked for a sign', arabic=TITLE_AR, hold=99, plain=True),
         lines=['They asked for a sign. Allah sent a she-camel. What did they do to her?']),
    dict(layers=[thamud_sky, thamud_far, thamud_near], fx=['dust'], cam='right',
         lines=['Thamud carved their homes out of the mountains.']),
    dict(layers=[salih_sky, salih_mid, salih_near], fx=['twinkle', 'dust'], cam='up',
         verse=dict(key='7:73', ar=(5, 8), en='O my people, worship Allah', line=1, ar_size=90),
         lines=['Allah sent them their brother Salih, peace be upon him.', 'O my people, worship Allah.']),
    dict(layers=[said_sky, said_mid, said_near], fx=['embers'], cam='left',
         verse=dict(key='26:154', en='You are but a man like ourselves, so bring a sign, if you should be of the truthful', line=1, ar_size=78),
         lines=['They said:', 'You are but a man like ourselves, so bring a sign, if you should be of the truthful.']),
    dict(layers=[sign_sky, sign_mid, sign_near], fx=['dust'], cam='in', bloom=.6,
         lines=['So Allah sent a she-camel, as a sign.', 'The water was shared: a day for her, a day for them.']),
    dict(layers=[warn_sky, warn_mid, warn_near], fx=['dust'], cam='down', pause=0.5,
         verse=dict(key='26:156', ar=(0, 3), en='And do not touch her with harm', line=1, ar_size=96),
         lines=['He warned them:', 'And do not touch her with harm.']),
    dict(layers=[dared_sky, dared_mid, dared_near], fx=['embers'], cam='in', bloom=.5,
         verse=dict(key='54:29', en='But they called their companion, and he dared and hamstrung [her]', line=0, ar_size=96),
         lines=['But they called their companion, and he dared and hamstrung her.']),
    dict(layers=[days_sky, days_mid, days_near], fx=['twinkle'], cam='out',
         verse=dict(key='11:65', ar=(2, 7), en='Enjoy yourselves in your homes for three days', line=1, ar_size=84),
         lines=['Salih said:', 'Enjoy yourselves in your homes for three days.']),
    dict(layers=[blast_sky, blast_mid, blast_near], fx=[('sand', dict(n=60, alpha=.6))], cam='in', bloom=.7,
         lines=['Then one blast from the sky seized them.', 'As if they had never prospered there.']),
    dict(layers=[saved_sky, saved_mid, saved_near], fx=['dust'], cam='up',
         verse=dict(key='11:66', ar=(3, 10), en='We saved Salih and those who believed with him, by mercy from Us', line=0, ar_size=78),
         lines=['We saved Salih and those who believed with him, by mercy from Us.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle', 'dust'], cam='in',
         end=dict(after=1, line1='Follow Quranic Story', line2='A new story every day'),
         lines=['They asked for a sign, then harmed it. Do not turn away from the truth.',
                'Share this with someone who needs it. And follow for a new story from the Quran every day.']),
]

PRON = {'Thamud': 'θɐmˈuːd'}

CAPTION = """They asked for a sign. Allah sent a she-camel. What did they do to her? 🤍

Allah sent the people of Thamud their brother Salih (peace be upon him). They told him: "You are but a man like ourselves, so bring a sign, if you should be of the truthful." (Quran 26:154)

Allah gave them the she-camel as a clear sign. The water was shared between them, each on its day. Salih warned them: "And do not touch her with harm, lest you be seized by the punishment of a terrible day." (Quran 26:156)

But they hamstrung her. After three days, the punishment came, and Allah saved Salih and those who believed with him, by His mercy.

They asked for a sign, then harmed it. Do not turn away from the truth.

📖 Sources: Quran 7:73–79, 11:61–68, 26:141–159, 54:23–31, 91:11–15 (Saheeh International)
Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetSalih #IslamicReminder"""

FIRST_COMMENT = """Which part of this story stays with you? 🤍

References: Quran, Surah Al-A'raf 7:73–79; Surah Hud 11:61–68; Surah Ash-Shu'ara 26:141–159; Surah Al-Qamar 54:23–31; Surah Ash-Shams 91:11–15; Surah Al-Isra 17:59 (Saheeh International translation). The Quran does not name the man who hamstrung the she-camel, so we did not either."""
