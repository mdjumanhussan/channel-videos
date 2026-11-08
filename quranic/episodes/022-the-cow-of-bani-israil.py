"""Story 22: The cow of Bani Israil. Source: Quran 2:67-73 (Saheeh International).
No people are drawn: no Musa, no crowd, no slain man, no figure of any kind, and nothing stands for Allah.
Only cows (animals), a pasture, a fence, a plough, a rope and post, a town at night, a lantern, the sky and light.
Nothing violent is shown: the slaughter is told only by the verse card over an empty pasture.
Facts used and where they are: Musa told his people "Indeed, Allah commands you to slaughter a cow"; they said "Do you take us in
ridicule?" (2:67); three times they said "Call upon your Lord" and asked: what it is (2:68), what is her color (2:69), what it is,
"all cows look alike to us" (2:70); the answers: "neither old nor virgin, but median between that" (2:68), "a yellow cow, bright in
color - pleasing to the observers" (2:69), "neither trained to plow the earth nor to irrigate the field" (2:71); "So they slaughtered
her, but they could hardly do it" (2:71); "you slew a man and disputed over it, but Allah was to bring out that which you were
concealing" (2:72); "Strike the slain man with part of it. Thus does Allah bring the dead to life" (2:73).
Not used: who the slain man was, who killed him, any words of the slain man, the price paid for the cow, its owner, the orphan story,
any number of days, Israiliyyat. The hook's "three times" is counted from 2:68, 2:69 and 2:70, which each begin "Call upon your Lord".
Improvement tried today: a concrete number on frame 1, taken from the verses, and paid off on screen: three gold rings under the badge
tick 1, 2, 3 as each question is asked (scenes 3-5), so the viewer can see how far the count has come. Playbook 2026-11-01 (numbers in
the first line) and 2026-11-08.
Also kept: statement hook = headline with nothing else on frame 1 (caption hidden); second loop ("Then came what they were hiding.",
0.5 s pause); live light at the peak (dawn breaks over the town on 2:73, deep hit); rhyming loop ending (same pasture and herd as frame 1,
now in morning light); speed 1.1; lesson card; specific send-to end card; CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  22'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'One Cow, Three Questions'
HITS = [(7, 1, 0.0)]      # 'Thus does Allah bring the dead to life'

# ---------------------------------------------------------------- the cow (an animal only)
def cow(p, cx, base, s=1.0, col=(150, 96, 60), flip=False, a=255):
    """A cow, side view, standing on base, facing right (flip=True faces left)."""
    k = -1 if flip else 1
    def X(dx): return cx + k * dx * s
    def Y(dy): return base + dy * s
    dark = lc(col, (0, 0, 0), .3); hoof = lc(col, (0, 0, 0), .7); nose = lc(col, (230, 150, 140), .35)
    for lx, sh in ((-108, dark), (82, dark), (-84, col), (106, col)):          # far legs darker, near legs in body colour
        p.poly([(X(lx - 15), Y(-160)), (X(lx + 15), Y(-160)), (X(lx + 11), Y(-14)), (X(lx - 11), Y(-14))], sh, a)
        p.ell(X(lx), Y(-92), 13 * s, 12 * s, sh, a)                                         # knee
        p.rect(min(X(lx - 13), X(lx + 13)), Y(-16), max(X(lx - 13), X(lx + 13)), Y(0), hoof, a)
    p.line([(X(-146), Y(-240)), (X(-164), Y(-180)), (X(-160), Y(-110))], dark, 8 * s, a)    # tail
    p.ell(X(-160), Y(-102), 9 * s, 15 * s, hoof, a)
    p.rect(min(X(-130), X(104)), Y(-250), max(X(-130), X(104)), Y(-150), col, a)            # body
    p.ell(X(-128), Y(-200), 30 * s, 50 * s, col, a)                                         # rump
    p.ell(X(92), Y(-196), 46 * s, 56 * s, col, a)                                           # chest
    p.ell(X(70), Y(-250), 54 * s, 14 * s, col, a)                                           # withers
    p.ell(X(-14), Y(-150), 116 * s, 22 * s, col, a)                                         # belly
    p.poly([(X(96), Y(-256)), (X(160), Y(-240)), (X(196), Y(-204)), (X(186), Y(-168)), (X(150), Y(-140)), (X(112), Y(-148))], col, a)   # neck and dewlap
    p.poly([(X(176), Y(-236)), (X(210), Y(-234)), (X(244), Y(-166)), (X(238), Y(-140)), (X(206), Y(-138)), (X(176), Y(-196))], col, a)  # head, sloping down
    p.ell(X(226), Y(-146), 22 * s, 17 * s, nose, a)                                         # muzzle
    p.ell(X(178), Y(-226), 22 * s, 8 * s, dark, a)                                          # ear
    p.line([(X(194), Y(-234)), (X(198), Y(-258)), (X(212), Y(-266))], (236, 226, 204), 7 * s, a)   # short horn
    p.ell(X(206), Y(-204), 4 * s, 4 * s, (20, 14, 10), a)                                   # eye

def herd(p, base, seed, n, cols, s=.35, x0=80, x1=1000, jitter=14):
    rnd = random.Random(seed)
    for i in range(n):
        x = lerp(x0, x1, (i + rnd.uniform(.1, .9)) / n)
        cow(p, x, base + rnd.uniform(-jitter, jitter), s * rnd.uniform(.85, 1.15), rnd.choice(cols), flip=rnd.random() < .5)

def fence(p, y, col=(92, 64, 40), x0=-60, x1=1140, step=130, h=120):
    for x in range(x0, x1 + 1, step): p.rect(x - 8, y - h, x + 8, y + 6, col)
    for dy in (.25, .65): p.line([(x0, y - h * (1 - dy)), (x1, y - h * (1 - dy))], col, 10)

def plough(p, cx, base, s=1.0, col=(110, 76, 46)):
    """A wooden plough lying unused on the ground."""
    p.line([(cx - 260 * s, base - 40 * s), (cx + 120 * s, base - 10 * s)], col, 18 * s)          # beam
    p.line([(cx + 120 * s, base - 10 * s), (cx + 170 * s, base - 120 * s)], col, 14 * s)         # handle
    p.poly([(cx + 60 * s, base - 14 * s), (cx + 150 * s, base - 4 * s), (cx + 90 * s, base + 10 * s)], (150, 150, 156))  # share
    p.line([(cx - 260 * s, base - 40 * s), (cx - 320 * s, base - 30 * s)], col, 12 * s)

def channel(p, y, col=(120, 90, 60)):
    """A dry irrigation channel running across the field."""
    pts = [(x, y + math.sin(x / 140) * 18) for x in range(-60, 1160, 40)]
    p.line(pts, lc(col, (0, 0, 0), .35), 30); p.line([(x, yy - 4) for x, yy in pts], col, 18)

def post_and_rope(p, cx, base):
    p.rect(cx - 16, base - 220, cx + 16, base + 8, (86, 58, 36)); p.ell(cx, base - 222, 18, 8, (110, 76, 48))
    pts = [(cx + 14, base - 150)] + [(cx + 14 + k * 26, base - 150 + 140 * math.sin(min(1, k / 6) * math.pi / 2) + (k % 2) * 4) for k in range(1, 9)]
    p.line(pts, (196, 166, 110), 7)

# ---------------------------------------------------------------- live drawing (fx), redrawn every frame
def tally_fx(img, tt, info, n=1, line=0, x=540, y=250, gap=110):
    """Three gold rings under the badge. Rings before n are filled; ring n fills as `line` is spoken; later rings stay empty."""
    a, b = info['lines'][line]; q = ease((tt - a + .1) / .35)
    d = ImageDraw.Draw(img); f = F(46, 'Bold')
    for i in range(3):
        cx = x + (i - 1) * gap; fill = 1.0 if i < n - 1 else (q if i == n - 1 else 0.0)
        r = 40 + (8 * math.sin(math.pi * q) if i == n - 1 else 0)
        d.ellipse((cx - r, y - r, cx + r, y + r), outline=GOLD + (255,), width=6, fill=(12, 8, 6, 140))
        rr = r * fill
        if rr > 10:
            d.ellipse((cx - rr + 6, y - rr + 6, cx + rr - 6, y + rr - 6), fill=GOLD + (int(255 * fill),))
            stroke_text(d, (cx, y + 2), str(i + 1), f, (30, 18, 8, int(255 * fill)), 0, shadow=False)

def dawn_fx(img, tt, info, line=1, x=540, y=1140):
    """Dawn breaking over the town as the line is spoken (2:73): a warm glow rises and soft rays open."""
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
DUSK = [(0, (24, 20, 58)), (.24, (96, 58, 96)), (.38, (226, 120, 76)), (.46, (255, 186, 104)), (.5, (200, 150, 90)), (1, (40, 46, 24))]
MORN = [(0, (70, 140, 200)), (.24, (156, 204, 228)), (.4, (250, 232, 190)), (.47, (255, 242, 210)), (.5, (210, 214, 160)), (1, (60, 76, 36))]
NOON = [(0, (60, 130, 200)), (.3, (140, 196, 232)), (.45, (236, 232, 200)), (.5, (226, 214, 150)), (1, (120, 100, 40))]

def dusk_sky(p): p.sky(DUSK); sun(p, 300, 800, 46, (255, 196, 120)); clouds(p, 401, 200, 640, (255, 196, 150), 6, 90)
def morn_sky(p): p.sky(MORN); sun(p, 300, 740, 40); clouds(p, 402, 200, 600, (255, 250, 236), 5, 110)
def noon_sky(p): p.sky(NOON); sun(p, 820, 420, 52, (255, 244, 200)); clouds(p, 403, 240, 700, (255, 255, 250), 5, 120)
def hills(col, seed, base=1080, h=150): return lambda p: mountains(p, base, h, col, seed, None, 4)
def pasture(top, bot, seed, y=1120):
    def fn(p):
        p.grad_poly([(-200, y), (1300, y), (1300, 2300), (-200, 2300)], top, bot, y, 1800)
        rnd = random.Random(seed)
        for _ in range(140):
            gx, gy = rnd.uniform(-60, 1140), rnd.uniform(y + 20, 1900)
            p.line([(gx, gy), (gx + rnd.uniform(-6, 6), gy - 10 - (gy - y) * .03)], lc(top, (0, 0, 0), .3), 3, 120)
    return fn
HERD_DARK = [(40, 28, 24), (56, 38, 30), (30, 22, 20)]
HERD_MIX = [(150, 96, 60), (110, 70, 44), (196, 160, 120), (70, 48, 34), (230, 220, 200)]
HERD_SAME = [(128, 84, 52)]

def ridge_herd_dusk(p): herd(p, 1230, 404, 6, HERD_DARK, s=.42, x0=120, x1=980)
def ridge_herd_morn(p): herd(p, 1230, 404, 6, [(150, 104, 66), (120, 80, 50), (196, 164, 120)], s=.42, x0=120, x1=980)
def pen(p):
    herd(p, 1240, 405, 5, HERD_MIX, s=.55, x0=60, x1=1020, jitter=20); fence(p, 1330)
def ages(p):
    for x, base, s, c, fl in ((230, 1260, .95, (110, 70, 44), False), (560, 1300, .5, (196, 160, 120), True), (860, 1250, .72, (150, 96, 60), True)):
        cow(p, x, base, s, c, flip=fl)
def yellow(p):
    p.glow(540, 1150, 520, (255, 220, 90), .55)
    cow(p, 520, 1290, 1.25, (240, 192, 46))
def same_row(p):
    channel(p, 1190)
    herd(p, 1150, 406, 5, HERD_SAME, s=.38, x0=100, x1=990, jitter=4)
    plough(p, 560, 1330, 1.1)
def empty_post(p): post_and_rope(p, 400, 1290); lantern(p, 760, 1180, .9)

def night_sky(p): p.sky([(0, (6, 8, 30)), (.4, (16, 22, 60)), (.5, (30, 36, 80)), (1, (8, 10, 24))]); stars(p, 360, 410, 1000); moon(p, 800, 300, 54)
def night_town(p): city(p, 1150, (30, 30, 52), 411, (255, 190, 100), domes=False)
def night_street(p):
    p.grad_poly([(-200, 1150), (1300, 1150), (1300, 2300), (-200, 2300)], (44, 40, 60), (12, 10, 20), 1150, 1800)
    for cx in (180, 900):
        p.rect(cx - 150, 900, cx + 150, 1250, (52, 46, 70)); p.rect(cx - 50, 1080, cx + 50, 1250, (24, 18, 30))   # closed doors
    lantern(p, 540, 1080, 1.0)

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 412, 900); moon(p, 820, 300, 56)
def end_ground(p): dunes(p, 1420, 30, (90, 96, 60), (16, 20, 12), 413)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[dusk_sky, hills((70, 50, 60), 420), pasture((96, 104, 44), (26, 30, 14), 421), ridge_herd_dusk], fx=['dust'], cam='hold', bloom=.55,
         title=dict(text='One command. Three times they came back with questions.', hold=99, plain=True), no_caption=(0,),
         lines=['One command. Three times they came back with questions.']),
    dict(layers=[dusk_sky, hills((80, 56, 66), 422), pasture((104, 110, 50), (30, 32, 16), 423), pen], fx=['dust'], cam='in', bloom=.55,
         verse=dict(key='2:67', ar=(4, 10), en='Indeed, Allah commands you to slaughter a cow', line=1, ar_size=72, y=560),
         lines=['Musa, peace be upon him, said:', 'Indeed, Allah commands you to slaughter a cow.', 'They said: Do you take us in ridicule?']),
    dict(layers=[noon_sky, hills((120, 140, 110), 424), pasture((150, 160, 70), (60, 66, 24), 425), ages], fx=[(tally_fx, dict(n=1, line=0)), 'dust'], cam='in', bloom=.5,
         verse=dict(key='2:68', ar=(11, 20), en='It is a cow which is neither old nor virgin, but median between that', line=1, ar_size=66, y=650),
         lines=['First they asked: what is it?', 'It is a cow which is neither old nor virgin, but median between that.']),
    dict(layers=[noon_sky, hills((150, 150, 110), 426), pasture((196, 176, 80), (90, 76, 26), 427), yellow], fx=[(tally_fx, dict(n=2, line=0)), 'dust'], cam='in', bloom=.65,
         verse=dict(key='2:69', ar=(11, 18), en='It is a yellow cow, bright in color - pleasing to the observers', line=1, ar_size=70, y=610),
         lines=['Then: what is her color?', 'It is a yellow cow, bright in color, pleasing to the observers.']),
    dict(layers=[noon_sky, hills((130, 140, 110), 428), pasture((140, 150, 66), (56, 60, 22), 429), same_row], fx=[(tally_fx, dict(n=3, line=0)), 'dust'], cam='in', bloom=.5,
         verse=dict(key='2:71', ar=(3, 12), en='It is a cow neither trained to plow the earth nor to irrigate the field', line=1, ar_size=66, y=640),
         lines=['A third time they asked.', 'It is a cow neither trained to plow the earth nor to irrigate the field.']),
    dict(layers=[dusk_sky, hills((70, 50, 60), 430), pasture((90, 96, 40), (24, 26, 12), 431), empty_post], fx=['dust'], cam='in', bloom=.55, pause=0.5,
         verse=dict(key='2:71', ar=(20, 24), en='So they slaughtered her, but they could hardly do it', line=0, ar_size=80, y=560),
         lines=['So they slaughtered her, but they could hardly do it.', 'Then came what they were hiding.']),
    dict(layers=[night_sky, night_town, night_street], fx=['twinkle'], cam='in', bloom=.7, pause=0.6,
         verse=dict(key='2:72', ar=(6, 11), en='Allah was to bring out that which you were concealing', line=1, ar_size=76, y=560),
         lines=['A man had been slain, and they disputed over it.', 'Allah was to bring out that which you were concealing.']),
    dict(layers=[night_sky, night_town, night_street], fx=[(dawn_fx, dict(line=1)), 'dust'], cam='hold', bloom=.75,
         verse=dict(key='2:73', ar=(3, 7), en='Thus does Allah bring the dead to life', line=1, ar_size=84, y=540),
         lines=['Then Allah said: Strike the slain man with part of it.', 'Thus does Allah bring the dead to life.']),
    dict(layers=[morn_sky, hills((150, 140, 130), 420), pasture((150, 170, 70), (50, 66, 24), 421), ridge_herd_morn], fx=['dust'], cam='hold', bloom=.7,
         lesson=dict(text='When Allah commands, obey with a willing heart.', after=0, y=520, size=80), no_caption=(0,),
         lines=['When Allah commands, obey with a willing heart.']),
    dict(layers=[end_sky, end_ground], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone putting off what is right'), no_caption=(0,),
         lines=['Share this with someone putting off what is right. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """One command. Three times they came back with questions. 🐄

Musa (Moses), peace be upon him, told his people: "Indeed, Allah commands you to slaughter a cow." They said, "Do you take us in ridicule?" (Quran 2:67)

They asked what it was, then its color, then again what it was. The answer came each time: "It is a yellow cow, bright in color - pleasing to the observers." (2:69) "So they slaughtered her, but they could hardly do it." (2:71)

A man had been slain and they disputed over it, "but Allah was to bring out that which you were concealing." (2:72) "Thus does Allah bring the dead to life." (Quran 2:73)

When Allah commands, obey with a willing heart.

📖 Sources: Quran 2:67–73 (Saheeh International)
Share this with someone putting off what is right. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """Three times they came back with questions. What helps you obey Allah without delay? 🤍

Reference: Quran, Surah Al-Baqarah 2:67–73 (Saheeh International translation)."""
