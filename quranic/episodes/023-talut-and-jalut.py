"""Story 23: Talut, Jalut and Dawud. Source: Quran 2:246-251 (Saheeh International: Saul, Goliath, David).
No people are drawn: no prophet, no Talut, no Dawud, no Jalut, no soldiers, no figure of any kind, no angels, and nothing stands for Allah.
Only a river, reeds, tents, banners on poles, a crown, coins, camp fires far away, lamps, the sky and light. No fighting is shown.
Facts used and where they are: after Musa, the assembly of the Children of Israel asked a prophet of theirs for a king (2:246); their prophet said Allah has sent Saul (Talut) as a king; they said he has not been given any
measure of wealth; he said "Indeed, Allah has chosen him over you and has increased him abundantly in knowledge and stature" (2:247);
Talut went forth with the soldiers and said "Indeed, Allah will be testing you with a river": whoever drinks is not of him, except one
who takes from it in the hollow of his hand; "But they drank from it, except a [very] few of them"; after crossing, they faced Goliath and his
soldiers; those certain they would meet Allah said "How many a small company has overcome
a large company by permission of Allah. And Allah is with the patient" (2:249); their prayer "Our Lord, pour upon us patience and plant firmly our feet" (2:250, first part); "So they defeated them by
permission of Allah, and David killed Goliath" (2:251).
Not used: the chest carried by the angels (2:248, would need angels), the name of the prophet in 2:246, any number of soldiers, how
Dawud killed Jalut (no sling: that is not in the Quran), Dawud's age, any Israiliyyat. Talut is not called a prophet.
Improvement tried today: the frame-1 statement is paid off live on screen. Frame 1 shows a river with a whole camp of banners on the near
bank; in scene 5, as "they drank from it" is spoken, most banners fade away and only a few stay lit (episode fx `banners_fx`). The
lesson scene returns to the same river with only those few banners, now on the far bank in morning light (rhyming loop). Pre-flight
check from the playbook (2026-11-10): who it is for (anyone who feels outnumbered), loop opened (who passed the test?), frame 1 makes
sense alone (river + army + "failed its test"), reveal saved (the few win, 2:251, near the end).
Also kept: statement hook = headline with nothing else on frame 1 (caption hidden); a dua the viewer can keep (2:250); second loop
("Then they saw the enemy.", 0.5 s pause before it); deep hits on 2:249 and 2:251; speed 1.1; lesson card; specific
send-to end card; CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  23'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'One River, Most of an Army Failed'
HITS = [(5, 1, 0.0), (7, 0, 0.0)]      # 'How many a small company...' and 'So they defeated them...'

# ---------------------------------------------------------------- objects (no people)
def tent(p, cx, base, s, col=(120, 84, 60), light=(255, 196, 110)):
    """A plain tent with lamplight in its open side (from episode 14)."""
    p.glow(cx, base - 120 * s, 360 * s, light, .35)
    p.poly([(cx - 300 * s, base), (cx - 230 * s, base - 200 * s), (cx, base - 250 * s), (cx + 230 * s, base - 200 * s), (cx + 300 * s, base)], col)
    for k in range(-2, 3): p.line([(cx + k * 110 * s, base - 240 * s + abs(k) * 18 * s), (cx + k * 130 * s, base)], lc(col, (0, 0, 0), .25), 3, 200)
    p.poly([(cx + 40 * s, base), (cx + 70 * s, base - 150 * s), (cx + 170 * s, base - 140 * s), (cx + 190 * s, base)], light)

def reeds(p, x0, x1, base, h, col, seed, n=40):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1); hh = h * rnd.uniform(.5, 1.0); lean = rnd.uniform(-.12, .12)
        c = lc(col, (0, 0, 0), rnd.uniform(0, .35))
        p.line([(x, base), (x + lean * hh * .5, base - hh * .5), (x + lean * hh, base - hh)], c, rnd.uniform(4, 8))
        if rnd.random() < .4: p.ell(x + lean * hh, base - hh - 14, 6, 20, lc(c, (90, 60, 30), .4))

def crown(p, cx, cy, s, col=GOLD):
    dark = lc(col, (0, 0, 0), .35)
    p.ell(cx, cy + 120 * s, 260 * s, 60 * s, (90, 30, 40))                                     # cushion
    p.ell(cx, cy + 100 * s, 240 * s, 40 * s, (130, 44, 56))
    p.poly([(cx - 170 * s, cy + 70 * s), (cx - 190 * s, cy - 90 * s), (cx - 90 * s, cy - 10 * s), (cx, cy - 130 * s),
            (cx + 90 * s, cy - 10 * s), (cx + 190 * s, cy - 90 * s), (cx + 170 * s, cy + 70 * s)], col)
    p.rect(cx - 172 * s, cy + 30 * s, cx + 172 * s, cy + 74 * s, dark)
    for dx, c in ((-110, (200, 40, 60)), (0, (60, 160, 220)), (110, (60, 190, 120))): p.ell(cx + dx * s, cy + 52 * s, 14 * s, 14 * s, c)
    for dx, dy in ((-190, -90), (0, -130), (190, -90)): p.ell(cx + dx * s, cy + dy * s, 16 * s, 16 * s, CREAM)

def coins(p, cx, base, seed, n=9, col=(150, 130, 80)):
    rnd = random.Random(seed)
    for _ in range(n):
        x = cx + rnd.uniform(-240, 240); y = base + rnd.uniform(-20, 30)
        p.ell(x, y, 26, 9, lc(col, (0, 0, 0), .4)); p.ell(x, y - 3, 24, 8, col)

def scroll(p, cx, cy, s=1.0):
    """An open scroll with lines of writing (knowledge)."""
    p.glow(cx, cy, 380 * s, (255, 230, 170), .6)
    p.rect(cx - 220 * s, cy - 140 * s, cx + 220 * s, cy + 140 * s, (236, 220, 180))
    for x in (cx - 230 * s, cx + 230 * s): p.ell(x, cy, 26 * s, 160 * s, (196, 170, 120))
    for k in range(6): p.line([(cx - 170 * s, cy - 95 * s + k * 38 * s), (cx + (170 - (k % 3) * 40) * s, cy - 95 * s + k * 38 * s)], (120, 90, 60), 5 * s, 200)

def camp_fires(p, y, x0, x1, seed, n=120, col=(255, 140, 60), a=210):
    """A huge camp seen from far away: only its fires and tent tips on the horizon."""
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1); yy = y + rnd.uniform(-14, 22); r = rnd.uniform(3, 7)
        p.glow(x, yy, r * 6, col, .25); p.ell(x, yy, r, r, col, a)
    for _ in range(n // 2):
        x = rnd.uniform(x0, x1); yy = y + rnd.uniform(-10, 18)
        p.poly([(x - 16, yy), (x, yy - 22), (x + 16, yy)], (24, 16, 20))

def lamps(p, xs, base, col=(255, 206, 120)):
    for x in xs: lantern(p, x, base, .9, col)

# ---------------------------------------------------------------- live drawing (fx), redrawn every frame
BAN = [(70, 1270, 300), (170, 1300, 330), (270, 1260, 280), (360, 1310, 340), (455, 1275, 300), (545, 1300, 320), (640, 1265, 290),
       (735, 1305, 335), (830, 1270, 300), (925, 1300, 320), (1010, 1265, 285), (120, 1350, 360), (310, 1355, 370), (500, 1350, 360),
       (690, 1355, 370), (880, 1350, 360)]
KEEP = (2, 7, 10)
BAN_COLS = [(176, 52, 46), (60, 96, 150), (200, 150, 60), (70, 120, 80)]

def _banner(d, x, base, h, col, a):
    d.line([(x, base), (x, base - h)], fill=(70, 46, 30, a), width=7)
    d.polygon([(x, base - h), (x + 74, base - h + 14), (x + 64, base - h + 108), (x, base - h + 94)], fill=col + (a,))
    d.ellipse((x - 9, base - h - 19, x + 9, base - h - 1), fill=(255, 210, 110, a))

def banners_fx(img, tt, info, line=None, glow_keep=False, only_keep=False, dy=0, sc=1.0, x0=0):
    """Banners of the army on the river bank. If `line` is given, all but KEEP fade out as that line is spoken."""
    q = 0.0
    if line is not None:
        a, b = info['lines'][line]; q = ease((tt - a - .4) / max(.6, (b - a) * .8))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sway = math.sin(tt * 1.3) * 3
    for i, (x, base, h) in enumerate(BAN):
        keep = i in KEEP
        if only_keep and not keep: continue
        al = 255 if keep else int(255 * (1 - q))
        if al <= 2: continue
        X = x0 + x * sc + sway * (i % 3 - 1); B = base * sc + dy; hh = h * sc
        if keep and (glow_keep or q > 0):
            g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((X - 80, B - hh - 80, X + 120, B - hh + 140), fill=(255, 210, 120, int(120 * max(q, glow_keep))))
            lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(30)))
        _banner(d, X, B, hh, BAN_COLS[i % 4], al)
    img.alpha_composite(lay)

def dawn_fx(img, tt, info, line=0, x=540, y=1180):
    """Dawn breaking over the empty plain as the line is spoken."""
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
DUSK = [(0, (20, 24, 60)), (.25, (80, 60, 110)), (.38, (220, 116, 84)), (.46, (255, 180, 110)), (.5, (150, 120, 90)), (1, (30, 30, 24))]
NOON = [(0, (50, 120, 196)), (.3, (130, 190, 230)), (.45, (240, 230, 196)), (.5, (220, 200, 140)), (1, (110, 90, 50))]
MORN = [(0, (70, 140, 200)), (.24, (156, 204, 228)), (.4, (250, 232, 190)), (.47, (255, 242, 210)), (.5, (200, 196, 150)), (1, (60, 70, 40))]
NIGHT = [(0, (6, 8, 26)), (.4, (18, 22, 56)), (.5, (40, 34, 60)), (1, (10, 8, 16))]
PRE_DAWN = [(0, (10, 14, 44)), (.35, (36, 44, 92)), (.46, (120, 90, 120)), (.5, (70, 56, 70)), (1, (16, 14, 18))]

def dusk_sky(p): p.sky(DUSK); sun(p, 760, 840, 46, (255, 196, 120)); clouds(p, 501, 200, 640, (255, 190, 150), 6, 90)
def noon_sky(p): p.sky(NOON); sun(p, 820, 380, 56, (255, 246, 210)); clouds(p, 502, 240, 640, (255, 255, 250), 4, 110)
def morn_sky(p): p.sky(MORN); sun(p, 300, 780, 42); clouds(p, 503, 200, 600, (255, 250, 236), 5, 110)
def night_sky(p): p.sky(NIGHT); stars(p, 380, 504, 1000); moon(p, 820, 300, 50)
def predawn_sky(p): p.sky(PRE_DAWN); stars(p, 200, 505, 800)

def far_hills(col, seed, base=1000, h=140): return lambda p: mountains(p, base, h, col, seed, None, 4)
def river_band(top, c_top, c_bot, seed, shine):
    return lambda p: sea(p, top, c_top, c_bot, seed, shine)
def bank(y, top, bot, seed, reed_col):
    def fn(p):
        p.grad_poly([(-200, y), (1300, y - 20), (1300, 2300), (-200, 2300)], top, bot, y, 1900)
        reeds(p, -40, 1120, y + 10, 140, reed_col, seed, 34)
    return fn
def far_bank(y, col, seed):
    def fn(p):
        p.poly([(-200, y), (1300, y - 10), (1300, y + 60), (-200, y + 70)], col)
        reeds(p, -40, 1120, y + 8, 60, lc(col, (0, 0, 0), .2), seed, 30)
    return fn

def camp_town(p):
    for x, b, s, c in ((120, 1150, .3, (90, 66, 58)), (400, 1140, .28, (96, 72, 60)), (700, 1150, .3, (90, 66, 58)), (980, 1145, .28, (96, 72, 60)),
                       (250, 1220, .42, (110, 80, 64)), (620, 1215, .4, (104, 76, 62)), (900, 1230, .45, (110, 80, 64)),
                       (120, 1340, .6, (120, 86, 66)), (540, 1360, .7, (126, 92, 70)), (960, 1350, .62, (116, 84, 64))): tent(p, x, b, s, c)
def ground(top, bot, y=1200, seed=507):
    return lambda p: p.grad_poly([(-200, y), (1300, y), (1300, 2300), (-200, 2300)], top, bot, y, 1900)
def throne(p): p.glow(540, 1020, 520, (255, 210, 120), .5); crown(p, 540, 1020, 1.15); coins(p, 540, 1300, 508, 10)
def knowledge(p): scroll(p, 540, 760, 1.15); coins(p, 540, 1240, 509, 6, (110, 100, 70))
def enemy_camp(p): camp_fires(p, 1060, -40, 1120, 510, 170)
def enemy_far_dim(p): camp_fires(p, 1060, -40, 1120, 511, 150, (200, 110, 60), 150)
def few_lamps(p): lamps(p, (380, 540, 700), 1260)

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 512, 900); moon(p, 820, 300, 56)
def end_ground(p): dunes(p, 1420, 30, (80, 70, 60), (16, 14, 12), 513)

RIVER_DUSK = river_band(1150, (150, 110, 120), (30, 34, 54), 520, (255, 200, 150))
RIVER_NOON = river_band(1150, (110, 170, 200), (30, 70, 100), 521, (255, 255, 240))
RIVER_MORN = river_band(1150, (150, 196, 220), (50, 96, 120), 522, (255, 245, 220))

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[dusk_sky, far_hills((70, 50, 66), 530), RIVER_DUSK, bank(1250, (70, 60, 40), (20, 18, 12), 531, (60, 70, 36))],
         fx=[(banners_fx, {}), 'dust'], cam='hold', bloom=.55,
         title=dict(text='One river. Most of the army failed its test.', hold=99, plain=True), no_caption=(0,),
         lines=['One river. Most of the army failed its test.']),
    dict(layers=[dusk_sky, far_hills((80, 56, 70), 532), ground((90, 74, 56), (24, 20, 16)), camp_town], fx=['dust'], cam='in', bloom=.55,
         lines=['After Musa, peace be upon him, his people asked for a king.', 'Allah chose Talut. They said: he has no wealth.']),
    dict(layers=[night_sky, ground((50, 40, 50), (14, 10, 14)), throne], fx=['twinkle'], cam='in', bloom=.65,
         verse=dict(key='2:247', ar=(26, 35), en='Indeed, Allah has chosen him over you and has increased him abundantly in knowledge and stature', line=0, ar_size=62, y=560),
         lines=['Indeed, Allah has chosen him over you and has increased him abundantly in knowledge and stature.']),
    dict(layers=[noon_sky, far_hills((140, 150, 120), 533), RIVER_NOON, bank(1250, (180, 150, 90), (90, 70, 40), 534, (90, 110, 50))],
         fx=[(banners_fx, {}), 'dust'], cam='hold', bloom=.5,
         verse=dict(key='2:249', ar=(5, 9), en='Indeed, Allah will be testing you with a river', line=1, ar_size=84, y=560),
         lines=['Talut marched out, and said:', 'Indeed, Allah will be testing you with a river.', 'Only one handful was allowed.']),
    dict(layers=[noon_sky, far_hills((140, 150, 120), 533), RIVER_NOON, bank(1250, (180, 150, 90), (90, 70, 40), 534, (90, 110, 50))],
         fx=[(banners_fx, dict(line=0)), 'dust'], cam='hold', bloom=.55, pause=0.5,
         verse=dict(key='2:249', ar=(24, 29), en='But they drank from it, except a [very] few of them', line=0, ar_size=84, y=560),
         lines=['But they drank from it, except a very few of them.', 'Then they saw the enemy.']),
    dict(layers=[night_sky, far_hills((26, 22, 40), 535, 1040, 90), enemy_camp, ground((40, 34, 40), (10, 8, 10), 1120), few_lamps], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='2:249', ar=(48, 60), en='How many a small company has overcome a large company by permission of Allah. And Allah is with the patient', line=1, ar_size=60, y=520),
         lines=['Those certain of meeting Allah said:',
                'How many a small company has overcome a large company by permission of Allah. And Allah is with the patient.']),
    dict(layers=[predawn_sky, far_hills((30, 30, 50), 536, 1040, 90), enemy_far_dim, ground((44, 40, 50), (12, 10, 14), 1120), few_lamps], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='2:250', ar=(5, 11), en='Our Lord, pour upon us patience and plant firmly our feet', line=1, ar_size=70, y=560),
         lines=['They prayed:', 'Our Lord, pour upon us patience and plant firmly our feet.']),
    dict(layers=[predawn_sky, far_hills((40, 40, 60), 537, 1040, 90), ground((60, 54, 56), (16, 14, 16), 1120), few_lamps], fx=[(dawn_fx, dict(line=0, y=1120)), 'dust'], cam='hold', bloom=.75,
         verse=dict(key='2:251', ar=(0, 6), en='So they defeated them by permission of Allah, and David killed Goliath', line=0, ar_size=70, y=540),
         lines=['So they defeated them by permission of Allah, and David killed Goliath.', 'That was Dawud, peace be upon him.']),
    dict(layers=[morn_sky, far_hills((150, 150, 140), 530), RIVER_MORN, far_bank(1140, (130, 120, 80), 538), bank(1420, (150, 140, 90), (60, 56, 30), 539, (90, 110, 50))],
         fx=[(banners_fx, dict(only_keep=True, glow_keep=True, sc=.55, dy=420, x0=240)), 'dust'], cam='hold', bloom=.7,
         lesson=dict(text='Allah is with the patient. Be among the few.', after=0, y=520, size=80), no_caption=(0,),
         lines=['Allah is with the patient. Be among the few.']),
    dict(layers=[end_sky, end_ground], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone who feels outnumbered'), no_caption=(0,),
         lines=['Share this with someone who feels outnumbered. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa', 'Talut': 'tˈaːluːt', 'Dawud': 'dˈaːwuːd'}

CAPTION = """One river. Most of the army failed its test. 🌊
Would you have passed it? Comment below 👇

After Musa (Moses), peace be upon him, his people asked a prophet of theirs: "Send to us a king, and we will fight in the way of Allah." (Quran 2:246) Allah chose Talut (Saul). They said he had no wealth. "Indeed, Allah has chosen him over you and has increased him abundantly in knowledge and stature." (2:247)

Talut said: "Indeed, Allah will be testing you with a river." Only a handful was allowed. "But they drank from it, except a [very] few of them." (2:249)

The few faced Jalut (Goliath) and his army. They said: "How many a small company has overcome a large company by permission of Allah. And Allah is with the patient." (Quran 2:249)

They prayed: "Our Lord, pour upon us patience and plant firmly our feet." (2:250) "So they defeated them by permission of Allah, and David killed Goliath." (2:251)

Allah is with the patient. Be among the few.

📖 Sources: Quran 2:246–251 (Saheeh International)
Share this with someone who feels outnumbered. Follow for a new story every day.

#QuranicStories #ProphetDawud #IslamicReminder"""

FIRST_COMMENT = """Most of the army drank from the river. Only a few held back. Would you have passed the test? 🤍

Their dua: "Our Lord, pour upon us patience and plant firmly our feet and give us victory over the disbelieving people." (2:250)

Reference: Quran, Surah Al-Baqarah 2:246–251 (Saheeh International translation)."""
