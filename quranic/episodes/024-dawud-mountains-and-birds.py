"""Story 24: Prophet Dawud: mountains and birds praise with him. Source: Quran 34:10-11, 38:17-26 (Saheeh International: David).
No people are drawn: no prophet, no Dawud, no adversaries, no figure of any kind, no angels, and nothing stands for Allah.
Only mountains, birds, sky, light, iron rings and a forge, an anvil, a stone wall with a lit window, a lamp, sheep and a far city.
Facts used and where they are: Allah gave David bounty; "O mountains, repeat [Our] praises with him, and the birds [as well]"; "And We made
pliable for him iron" (34:10); make full coats of mail and calculate [precisely] the links (34:11); the mountains were subjected to praise with
him in the [late] afternoon and [after] sunrise (38:18); "And the birds were assembled, all with him repeating [praises]" (38:19); Allah
strengthened his kingdom and gave him wisdom (38:20); the adversaries climbed over the wall of his prayer chamber (38:21) and asked him to judge
between them with truth (38:22); "Indeed this, my brother, has ninety-nine ewes, and I have one ewe" (38:23); David's answer "He has certainly
wronged you in demanding your ewe [in addition] to his ewes"; David became certain that he had been tried, asked forgiveness of his Lord, fell
down bowing and turned in repentance (38:24); "So We forgave him that; and indeed, for him is nearness to Us and a good place of return" (38:25);
"judge between the people in truth and do not follow [your own] desire" (38:26, used for the lesson).
Not used: who the two adversaries were, what exactly the test was, any story about a wife or a soldier (Israiliyyat), the Zabur, Dawud's
voice, any number of years. The adversaries are not shown and are only called "two adversaries", as in the Quran.
Improvement tried today: a live flock (episode fx `birds_fx`, redrawn every frame). Frame 1 opens on motion: birds circling above the
mountains at sunrise. In scene 3, as "And the birds were assembled" is spoken, scattered birds fly in from the whole sky and gather into
one circling flock, so the verse happens on screen. The lesson scene returns to the same mountains with the same flock (rhyming loop).
Also kept: statement hook = headline with nothing else on frame 1 (caption hidden); a self-test question at the turn ("How would you
judge?", like Talut's "Would you have passed it?"); 0.5 s pause before 38:25; deep hits on 38:23 and 38:25; speed 1.1; lesson card;
specific send-to end card; CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  24'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Mountains and Birds Joined His Praise'
HITS = [(5, 1, 0.0), (8, 0, 0.0)]      # 'ninety-nine ewes ... one ewe' and 'So We forgave him that'

# ---------------------------------------------------------------- objects (no people)
def ring(p, x, y, r, col, w=4, a=255):
    p.line([(x + r * math.cos(k * math.pi / 9), y + r * .8 * math.sin(k * math.pi / 9)) for k in range(19)], col, w, a)

def mail_sheet(p, cx, cy, cols=9, rows=7, r=30, col=(150, 140, 130), hot=(255, 150, 70)):
    """A sheet of interlocking iron rings hanging from a bar, the lower rows still glowing from the forge."""
    p.glow(cx, cy + rows * r * .7, 460, hot, .45)
    x0 = cx - (cols - 1) * r * .75; y0 = cy
    p.line([(x0 - 70, y0 - 40), (x0 + (cols - 1) * r * 1.5 + 70, y0 - 40)], (70, 56, 46), 16)
    for j in range(rows):
        for i in range(cols):
            x = x0 + i * r * 1.5 + (r * .75 if j % 2 else 0); y = y0 + j * r * 1.15
            c = lc(col, hot, clamp((j - rows * .45) / (rows * .55)))
            ring(p, x, y, r * .62, lc(c, (0, 0, 0), .35), 9); ring(p, x, y, r * .62, c, 5)

def anvil(p, cx, base, s=1.0, col=(46, 40, 40)):
    p.poly([(cx - 220 * s, base - 170 * s), (cx + 170 * s, base - 170 * s), (cx + 260 * s, base - 200 * s), (cx + 140 * s, base - 120 * s),
            (cx + 70 * s, base - 120 * s), (cx + 110 * s, base), (cx - 140 * s, base), (cx - 90 * s, base - 120 * s), (cx - 220 * s, base - 120 * s)], col)
    p.line([(cx - 210 * s, base - 168 * s), (cx + 200 * s, base - 168 * s)], (255, 150, 80), 4, 170)

def forge(p, cx, base):
    p.glow(cx, base - 120, 420, (255, 120, 40), .7)
    p.rect(cx - 170, base - 260, cx + 170, base, (60, 44, 40))
    p.poly([(cx - 110, base - 60), (cx - 110, base - 170), (cx, base - 220), (cx + 110, base - 170), (cx + 110, base - 60)], (255, 130, 50))
    p.ell(cx, base - 110, 70, 40, (255, 220, 150))

def sheep(p, x, base, s=1.0, wool=(232, 226, 210), face=(52, 44, 44), flip=False):
    k = -1 if flip else 1
    for lx in (-26, -8, 12, 28): p.line([(x + k * lx * s, base - 30 * s), (x + k * lx * s, base)], face, 6 * s)
    for dx, dy, rx, ry in ((-20, -52, 30, 26), (0, -60, 32, 28), (20, -52, 30, 26), (0, -42, 44, 24)):
        p.ell(x + k * dx * s, base + dy * s, rx * s, ry * s, wool)
    p.ell(x + k * 50 * s, base - 62 * s, 16 * s, 20 * s, face); p.ell(x + k * 38 * s, base - 76 * s, 9 * s, 5 * s, face)

def flock_99(p, x0, x1, y0, y1, seed, s=.36):
    rnd = random.Random(seed); pts = []
    rows = 9
    for j in range(rows):
        y = y0 + (y1 - y0) * j / (rows - 1); n = 11
        for i in range(n):
            if len(pts) == 99: break
            pts.append((x0 + (x1 - x0) * (i + .5 * (j % 2)) / n + rnd.uniform(-10, 10), y + rnd.uniform(-8, 8)))
    for x, y in sorted(pts, key=lambda q: q[1]):
        sc = s * (.75 + .5 * (y - y0) / max(1, y1 - y0))
        sheep(p, x, y, sc, lc((226, 220, 204), (120, 120, 130), .35), flip=rnd.random() < .5)

def chamber_wall(p, lamp=True, glow=(255, 200, 110)):
    """A tall stone wall with an arched, lamp-lit window (the prayer chamber, seen from outside)."""
    p.rect(160, 520, 920, 1500, (70, 62, 66))
    for j in range(16):
        y = 520 + j * 62; off = 0 if j % 2 else 60
        p.line([(160, y), (920, y)], (50, 44, 48), 3)
        for x in range(160 + off, 920, 120): p.line([(x, y), (x, y + 62)], (50, 44, 48), 3)
    p.glow(540, 860, 420, glow, .6)
    p.rect(420, 760, 660, 1060, glow); p.ell(540, 760, 120, 110, glow)
    p.rect(450, 780, 630, 1060, lc(glow, (255, 250, 230), .5)); p.ell(540, 780, 90, 85, lc(glow, (255, 250, 230), .5))
    if lamp: lantern(p, 540, 940, .8, (255, 200, 100))
    p.rect(130, 500, 950, 530, (90, 80, 84))

# ---------------------------------------------------------------- live drawing (fx), redrawn every frame
def _bird(d, x, y, s, ph, col):
    f = math.sin(ph) * 14 * s
    d.line([(x - 30 * s, y - 6 * s + f), (x - 12 * s, y - 2 * s), (x, y + 4 * s), (x + 12 * s, y - 2 * s), (x + 30 * s, y - 6 * s + f)],
           fill=col, width=max(3, int(6 * s)), joint='curve')

def birds_fx(img, tt, info, line=None, n=34, cx=540, cy=640, R=330, col=(30, 22, 34, 235), seed=24, scale=1.0):
    """A flock circling over the peaks. If `line` is given, scattered birds fly in from the whole sky and gather into the circle as that line is spoken."""
    q = 1.0
    if line is not None:
        a, b = info['lines'][line]; q = ease((tt - a + .2) / max(.8, (b - a) * .85))
    rnd = random.Random(seed)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(n):
        th0 = rnd.uniform(0, 2 * math.pi); rr = R * rnd.uniform(.35, 1.0); w = rnd.uniform(.32, .5) * (1 if i % 5 else -1)
        sx, sy = rnd.uniform(-150, W + 150), rnd.uniform(250, 1050); vx = rnd.uniform(-40, 40)
        s = rnd.uniform(.6, 1.1) * scale; fl = rnd.uniform(7, 10); ph0 = rnd.uniform(0, 6)
        th = th0 + w * tt
        ox, oy = cx + rr * math.cos(th) * scale, cy + rr * .42 * math.sin(th) * scale + math.sin(tt * .7 + i) * 10
        x = lerp(sx + vx * tt, ox, q); y = lerp(sy, oy, q)
        _bird(d, x, y, s * (.85 + .15 * math.sin(th)), tt * fl + ph0, col)
    img.alpha_composite(lay)

def dawn_fx(img, tt, info, line=0, x=540, y=1180):
    """Dawn breaking as the line is spoken (from episode 23)."""
    a, b = info['lines'][line]; q = ease((tt - a) / max(.3, (b - a) * .9))
    if q <= 0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = 260 + 620 * q
    d.ellipse((x - r, y - r * .7, x + r, y + r * .7), fill=(255, 176, 96, int(170 * q)))
    for k in range(11):
        ang = math.radians(-90 + (k - 5) * 15 + math.sin(tt * .6 + k) * 1.5); L = 1500 * q
        d.polygon([(x, y), (x + math.cos(ang - .03) * L, y + math.sin(ang - .03) * L), (x + math.cos(ang + .03) * L, y + math.sin(ang + .03) * L)],
                  fill=(255, 226, 170, int(110 * q)))
    lay = lay.filter(ImageFilter.GaussianBlur(40)); al = lay.getchannel('A'); ImageDraw.Draw(al).rectangle((0, y + 20, W, H), fill=0)
    lay.putalpha(al.filter(ImageFilter.GaussianBlur(30))); img.alpha_composite(lay)

# ---------------------------------------------------------------- layer painters
SUNRISE = [(0, (40, 50, 110)), (.22, (120, 96, 150)), (.36, (240, 150, 120)), (.44, (255, 206, 140)), (.5, (180, 140, 110)), (1, (40, 32, 30))]
MORNING = [(0, (80, 146, 206)), (.25, (166, 206, 230)), (.4, (252, 236, 200)), (.47, (255, 244, 214)), (.5, (200, 190, 150)), (1, (60, 64, 44))]
AFTERNOON = [(0, (60, 90, 160)), (.25, (200, 160, 140)), (.4, (255, 190, 110)), (.47, (255, 214, 150)), (.5, (170, 120, 80)), (1, (40, 28, 20))]
NIGHT = [(0, (6, 8, 26)), (.4, (20, 24, 60)), (.5, (40, 36, 64)), (1, (10, 8, 16))]
PRE_DAWN = [(0, (10, 14, 44)), (.35, (40, 46, 96)), (.46, (130, 96, 120)), (.5, (70, 56, 70)), (1, (16, 14, 18))]
FORGE = [(0, (14, 10, 10)), (.5, (40, 24, 18)), (1, (12, 8, 8))]

def sunrise_sky(p): p.sky(SUNRISE); sun(p, 540, 940, 70, (255, 214, 150)); p.glow(540, 940, 600, (255, 180, 120), .5)
def morning_sky(p): p.sky(MORNING); sun(p, 800, 420, 54, (255, 248, 220)); clouds(p, 541, 220, 620, (255, 252, 240), 5, 120)
def afternoon_sky(p): p.sky(AFTERNOON); sun(p, 260, 820, 60, (255, 210, 140)); clouds(p, 542, 240, 700, (255, 200, 150), 6, 110)
def night_sky(p): p.sky(NIGHT); stars(p, 380, 543, 1000); moon(p, 800, 320, 52)
def predawn_sky(p): p.sky(PRE_DAWN); stars(p, 200, 544, 800)
def forge_room(p): p.sky(FORGE)

def peaks(col, seed, base=1150, h=420, rim=None, n=4): return lambda p: mountains(p, base, h, col, seed, rim, n)
def ground(top, bot, y=1250, seed=545):
    return lambda p: p.grad_poly([(-200, y), (1300, y - 30), (1300, 2300), (-200, 2300)], top, bot, y, 1900)
def ledge_lamp(p): lantern(p, 540, 1210, 1.0, (255, 200, 110))
def iron(p): mail_sheet(p, 540, 720, 9, 8, 32); anvil(p, 540, 1400, 1.25); forge(p, 900, 1560)
def far_city(p): city(p, 1440, (24, 22, 34), 546, (255, 200, 110))
def wall(p): chamber_wall(p)
def wall_dawn(p): chamber_wall(p, True, (255, 214, 140))
def field_night(p): p.grad_poly([(-200, 1080), (1300, 1040), (1300, 2300), (-200, 2300)], (40, 50, 44), (10, 14, 12), 1080, 1900)
def ewes(p):
    flock_99(p, 40, 640, 1110, 1380, 547)
    p.glow(890, 1300, 200, (255, 220, 150), .55); sheep(p, 890, 1340, .85, (246, 240, 226), flip=True)
def one_ewe(p):
    flock_99(p, 40, 560, 1110, 1380, 547)
    p.glow(890, 1300, 280, (255, 220, 150), .9); sheep(p, 890, 1340, .95, (250, 246, 232), flip=True)

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 548, 900); moon(p, 820, 300, 56)
def end_peaks(p): mountains(p, 1420, 260, (30, 28, 40), 549, None, 5)

FLOCK = (birds_fx, dict(cy=300, R=300, n=28, col=(255, 236, 214, 235)))
# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[sunrise_sky, peaks((90, 70, 100), 550, 1180, 460), peaks((50, 40, 56), 551, 1350, 300, None, 5), ground((44, 36, 40), (14, 10, 12), 1400)],
         fx=[FLOCK, 'dust'], cam='hold', bloom=.6,
         title=dict(text='Mountains and birds joined his praise of Allah.', hold=99, plain=True), no_caption=(0,),
         lines=['Mountains and birds joined his praise of Allah.']),
    dict(layers=[morning_sky, peaks((120, 130, 150), 552, 1180, 480, (255, 240, 210)), peaks((70, 80, 90), 553, 1360, 280, None, 5), ground((80, 84, 60), (24, 24, 16), 1420)],
         fx=[(birds_fx, dict(n=16, cy=880, R=280, scale=.8)), 'dust'], cam='hold', bloom=.6,
         verse=dict(key='34:10', ar=(5, 9), en='O mountains, repeat [Our] praises with him, and the birds [as well]', line=1, ar_size=78, y=560),
         lines=['This is Dawud, peace be upon him. Allah said:', 'O mountains, repeat Our praises with him, and the birds as well.']),
    dict(layers=[afternoon_sky, peaks((140, 96, 90), 554, 1180, 440, (255, 200, 140)), peaks((80, 56, 52), 555, 1360, 280, None, 5), ground((90, 64, 46), (26, 18, 12), 1420)],
         fx=[(birds_fx, dict(line=1, n=40)), 'dust'], cam='hold', bloom=.6,
         verse=dict(key='38:19', en='And the birds were assembled, all with him repeating [praises]', line=1, ar_size=84, y=1000),
         lines=['After sunrise and at the end of the day, the mountains praised with him.', 'And the birds were assembled, all with him repeating praises.']),
    dict(layers=[forge_room, iron], fx=['embers'], cam='in', bloom=.7,
         verse=dict(key='34:10', ar=(9, 12), en='And We made pliable for him iron', line=0, ar_size=84, y=420),
         lines=['And We made pliable for him iron.', 'He made coats of mail, measuring every link.']),
    dict(layers=[night_sky, far_city, wall], fx=['twinkle'], cam='in', bloom=.65,
         lines=['Allah strengthened his kingdom.', 'Then two adversaries climbed the wall of his prayer chamber.']),
    dict(layers=[night_sky, field_night, ewes], fx=['twinkle'], cam='in', bloom=.6,
         verse=dict(key='38:23', ar=(0, 10), en='Indeed this, my brother, has ninety-nine ewes, and I have one ewe', line=1, ar_size=72, y=560),
         lines=['One said:', 'Indeed this, my brother, has ninety-nine ewes, and I have one ewe.', 'How would you judge?']),
    dict(layers=[night_sky, field_night, one_ewe], fx=['twinkle'], cam='in', bloom=.65,
         verse=dict(key='38:24', ar=(1, 7), en='He has certainly wronged you in demanding your ewe [in addition] to his ewes', line=1, ar_size=72, y=560),
         lines=['Dawud said:', 'He has certainly wronged you in demanding your ewe in addition to his ewes.']),
    dict(layers=[predawn_sky, wall], fx=['twinkle'], cam='in', bloom=.7, pause=0.5,
         lines=['Then Dawud knew Allah had tested him.', 'He asked forgiveness, bowed down, and turned back to Allah.']),
    dict(layers=[predawn_sky, wall_dawn], fx=[(dawn_fx, dict(line=0, y=1500)), 'dust'], cam='hold', bloom=.8,
         verse=dict(key='38:25', en='So We forgave him that; and indeed, for him is nearness to Us and a good place of return', line=0, ar_size=70, y=600),
         lines=['So We forgave him that; and indeed, for him is nearness to Us and a good place of return.']),
    dict(layers=[sunrise_sky, peaks((90, 70, 100), 550, 1180, 460), peaks((50, 40, 56), 551, 1350, 300, None, 5), ground((44, 36, 40), (14, 10, 12), 1400)],
         fx=[(birds_fx, dict(cy=1000, R=300)), 'dust'], cam='hold', bloom=.6,
         lesson=dict(text='Judge with truth, not with your own desire.', after=0, y=520, size=80), no_caption=(0,),
         lines=['Judge with truth, not with your own desire.']),
    dict(layers=[end_sky, end_peaks], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone facing a hard decision'), no_caption=(0,),
         lines=['Share this with someone facing a hard decision. And follow for a new story from the Quran every day.']),
]

PRON = {'Dawud': 'dˈaːwuːd'}

CAPTION = """Mountains and birds joined his praise of Allah. ⛰️🕊️
Ninety-nine ewes and one. How would you have judged? Comment below 👇

Allah said: "O mountains, repeat [Our] praises with him, and the birds [as well]." And He made iron soft for Dawud (David), peace be upon him. (Quran 34:10) "And the birds were assembled, all with him repeating [praises]." (38:19)

Two adversaries climbed the wall of his prayer chamber. One said: "Indeed this, my brother, has ninety-nine ewes, and I have one ewe." (38:23) Dawud said: "He has certainly wronged you in demanding your ewe [in addition] to his ewes." Then he knew he had been tested, asked forgiveness of his Lord and bowed down. (38:24)

"So We forgave him that; and indeed, for him is nearness to Us and a good place of return." (Quran 38:25)

Judge with truth, not with your own desire. (38:26)

📖 Sources: Quran 34:10–11, 38:17–26 (Saheeh International)
Share this with someone facing a hard decision. Follow for a new story every day.

#QuranicStories #ProphetDawud #IslamicReminder"""

FIRST_COMMENT = """Ninety-nine ewes and one. How would you have judged? 🤍

"O David, indeed We have made you a successor upon the earth, so judge between the people in truth and do not follow [your own] desire, as it will lead you astray from the way of Allah." (38:26)

Reference: Quran, Surah Saba 34:10–11 and Surah Sad 38:17–26 (Saheeh International translation)."""
