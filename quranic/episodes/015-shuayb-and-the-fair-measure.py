"""Story 15: Prophet Shuayb (Shu'ayb) and the fair measure. Sources: Quran 7:85-93, 11:84-95 (Saheeh International).
No people are drawn: no Shuayb, no townspeople, no believers. Only a balance scale in a market, the town of Madyan among
palms and hills, coins, a lantern, a city gate under a red sky, cracked ground and broken walls, the night sky.
Facts used and where they are: Allah sent Shu'ayb to Madyan, their brother (7:85, 11:84); "worship Allah; you have no
deity other than Him" (7:85, 11:84); "do not decrease from the measure and the scale. Indeed, I see you in prosperity"
(11:84); "give full measure and weight in justice and do not deprive the people of their due" (11:85); they said "O
Shu'ayb, does your prayer command you that we should leave what our fathers worship or not do with our wealth what we
please?" (11:87); he said "I only intend reform as much as I am able. And my success is not but through Allah" (11:88);
the arrogant eminent ones said they would evict him and those who believed with him from their city (7:88); the
earthquake seized them (7:91); Allah saved Shu'ayb and those who believed with him, by mercy (11:94).
Not used: the "people of the thicket" (26:176-191, 15:78) - scholars differ on whether they are the same people; the
shriek (11:94) is not said, only the earthquake from 7:91, so the two accounts are not merged in narration; no claim that
the old man of Madyan in 28:23-28 is Shuayb (the Quran does not name him); no tafsir details (how they cheated, numbers).
"They cheated on the scale" / "gave short measure" is narration of what the commands in 7:85 and 11:84-85 forbid.
Improvement tried today: a rhyming loop ending. Attention drifts by about 20 s, and a reel whose ending "rhymes" with its
opening invites a rewatch (influencers-time, loop-optimised reels). Frame 1 shows a tilted scale in the market at dusk;
the lesson card plays over the same market and the same scale, now level, in morning light. No engine change.
Also kept: plain headline = spoken hook with caption hidden, open question answered by the verse card (11:85), second
loop ("They had an answer ready. What did they say?") with a 0.5 s pause before 11:87, speed 1.1, lesson card, a
specific "send it to" end card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  15'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Prophet Shuayb and the Fair Measure'
HITS = [(2, 1, 0.0), (7, 0, 0.0)]
# "the measure and the scale", taken straight from the text of 11:85
TITLE_AR = ' '.join(quran()['verses']['11:85']['ar'].split()[2:4])

BRASS = (214, 172, 92)

# ---------------------------------------------------------------- small scenery helpers for this story
def balance_scale(p, cx, top, s=1.0, tilt=0.0, metal=BRASS, goods=((200, 150, 70), (150, 100, 50))):
    """A merchant's balance: plinth, post, beam (tilted by `tilt` degrees, + = left pan down), chains and two pans
    with a small heap of grain in each. Objects only."""
    dark = lc(metal, (0, 0, 0), .45); hi = lc(metal, (255, 255, 255), .35)
    base = top + 560 * s
    p.poly([(cx - 150 * s, base), (cx - 110 * s, base - 50 * s), (cx + 110 * s, base - 50 * s), (cx + 150 * s, base)], dark)
    p.rect(cx - 14 * s, top, cx + 14 * s, base - 48 * s, metal); p.rect(cx - 5 * s, top, cx + 2 * s, base - 48 * s, hi)
    p.ell(cx, top - 12 * s, 26 * s, 26 * s, metal); p.ell(cx - 8 * s, top - 20 * s, 9 * s, 9 * s, hi)
    a = math.radians(tilt); L = 320 * s
    ends = [(cx - L * math.cos(a), top + L * math.sin(a)), (cx + L * math.cos(a), top - L * math.sin(a))]
    p.line(ends, metal, 16 * s); p.line([(ends[0][0], ends[0][1] - 4 * s), (ends[1][0], ends[1][1] - 4 * s)], hi, 4 * s)
    for (ex, ey), g in zip(ends, goods):
        p.ell(ex, ey, 14 * s, 14 * s, metal)
        py = ey + 230 * s
        for dx in (-95, 0, 95): p.line([(ex, ey), (ex + dx * s, py)], dark, 3 * s)
        p.ell(ex, py - 8 * s, 70 * s, 34 * s, g); p.ell(ex - 14 * s, py - 18 * s, 26 * s, 10 * s, lc(g, (255, 255, 255), .3))
        p.poly([(ex - 120 * s, py), (ex + 120 * s, py), (ex + 80 * s, py + 46 * s), (ex - 80 * s, py + 46 * s)], metal)
        p.rect(ex - 120 * s, py - 6 * s, ex + 120 * s, py + 6 * s, hi)

def stall(p, x, base, w, col=(70, 46, 34), cloth=(170, 70, 50), seed=1):
    """A plain market stall: two poles, a striped awning and a counter with jars."""
    rnd = random.Random(seed); h = w * .9
    for dx in (0, w): p.rect(x + dx - 6, base - h, x + dx + 6, base, col)
    for k in range(6):
        c = cloth if k % 2 == 0 else lc(cloth, (255, 240, 220), .55)
        x0 = x - 20 + k * (w + 40) / 6; x1 = x0 + (w + 40) / 6
        p.poly([(x0, base - h - 30), (x1, base - h - 30), (x1, base - h + 30), (x0, base - h + 46)], c)
    p.rect(x - 10, base - h * .38, x + w + 10, base, lc(col, (0, 0, 0), .2))
    for k in range(rnd.randint(3, 5)):
        jx = x + 30 + k * (w - 60) / 4; jc = rnd.choice([(170, 110, 70), (200, 160, 90), (120, 90, 70)])
        p.ell(jx, base - h * .38 - 28, 22, 30, jc); p.rect(jx - 9, base - h * .38 - 66, jx + 9, base - h * .38 - 52, jc)

def coins(p, cx, base, s=1.0, seed=5, gold=(240, 196, 90)):
    """A heap of gold coins (wealth, 11:87)."""
    rnd = random.Random(seed)
    p.glow(cx, base - 60 * s, 380 * s, (255, 200, 110), .45)
    for k in range(140):
        r = rnd.uniform(0, 1) ** .7; ang = rnd.uniform(0, math.pi)
        x = cx + math.cos(ang) * r * 300 * s; y = base - math.sin(ang) * (1 - r) * 170 * s - rnd.uniform(0, 20) * s
        c = lc(gold, (120, 80, 20), rnd.uniform(0, .5))
        p.ell(x, y, 30 * s, 11 * s, lc(c, (0, 0, 0), .35)); p.ell(x, y - 4 * s, 30 * s, 11 * s, c)
        p.ell(x - 8 * s, y - 7 * s, 10 * s, 3 * s, lc(c, (255, 255, 255), .5))

def gate(p, cx, base, s=1.0, col=(40, 24, 24)):
    """A city wall with a closed arched gate."""
    p.rect(-100, base - 300 * s, 1200, base + 600, col)
    for x in range(-80, 1200, 90): p.rect(x, base - 340 * s, x + 50, base - 290 * s, col)
    p.rect(cx - 170 * s, base - 470 * s, cx + 170 * s, base + 600, lc(col, (0, 0, 0), -.15))
    p.ell(cx, base - 220 * s, 110 * s, 120 * s, lc(col, (0, 0, 0), .55)); p.rect(cx - 110 * s, base - 220 * s, cx + 110 * s, base + 600, lc(col, (0, 0, 0), .55))
    for k in (-60, 0, 60): p.line([(cx + k * s, base - 300 * s), (cx + k * s, base)], lc(col, (255, 255, 255), .08), 5 * s)

def ruins(p, base, col=(110, 80, 60), seed=7):
    """Broken, leaning walls and rubble: a town left empty (7:91-92)."""
    rnd = random.Random(seed); x = -120; dark = lc(col, (0, 0, 0), .45)
    while x < 1200:
        w = rnd.uniform(90, 170); h = rnd.uniform(80, 260); lean = rnd.uniform(-30, 30)
        pts = [(x, base), (x + lean, base - h)]
        for k in range(1, 5): pts.append((x + lean + w * k / 5, base - h + rnd.uniform(-40, 60)))
        pts += [(x + w + lean * .5, base - h * rnd.uniform(.3, .8)), (x + w, base)]
        p.poly(pts, col); p.poly([(x + w * .7, base), (x + w * .7 + lean * .8, base - h * .6), (x + w + lean * .5, base - h * .5), (x + w, base)], dark)
        x += w + rnd.uniform(30, 90)
    for _ in range(40):
        rx, ry = rnd.uniform(-60, 1140), base + rnd.uniform(-10, 60); r = rnd.uniform(10, 34)
        p.ell(rx, ry, r, r * .6, rnd.choice([col, dark, lc(col, (255, 255, 255), .15)]))

def cracks(p, top, col, seed, n=22):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(-60, 1140), rnd.uniform(top + 30, 1950); pts = [(x, y)]
        for k in range(rnd.randint(3, 6)):
            x += rnd.uniform(-80, 80); y += rnd.uniform(-10, 50); pts.append((x, y))
        p.line(pts, col, 3 + (y - top) / 200)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def dusk_sky(p):
    p.sky([(0, (36, 22, 50)), (.4, (120, 60, 70)), (.62, (230, 130, 70)), (.75, (255, 190, 110)), (1, (70, 40, 30))])
    sun(p, 220, 1180, 80, (255, 210, 130))
def dusk_mid(p):
    city(p, 1250, (70, 40, 44), 11, (255, 200, 120))
    stall(p, -40, 1520, 260, (60, 36, 30), (150, 60, 46), 12); stall(p, 860, 1540, 260, (60, 36, 30), (60, 90, 120), 13)
def dusk_near(p):
    p.grad_poly([(-200, 1540), (1300, 1540), (1300, 2300), (-200, 2300)], (110, 70, 50), (40, 26, 20), 1540, 1900)
    balance_scale(p, 540, 1170, .72, tilt=14)

def plenty_sky(p):
    p.sky([(0, (70, 130, 200)), (.5, (180, 205, 230)), (.72, (255, 225, 170)), (1, (150, 150, 90))])
    clouds(p, 21, 260, 620, (255, 250, 240), 6, 160)
def plenty_mid(p):
    mountains(p, 1210, 260, (150, 120, 120), 22, (210, 180, 170))
    city(p, 1380, (130, 96, 80), 23, None)
def plenty_near(p):
    dunes(p, 1400, 20, (110, 160, 80), (70, 120, 50), 24)
    for x, h, ln in ((120, 520, -.06), (300, 420, .05), (800, 460, -.04), (980, 540, .07)): palm(p, x, 1560, h, (50, 64, 30), ln)

def night_market_sky(p):
    p.sky([(0, (8, 10, 30)), (.55, (26, 26, 60)), (.8, (70, 46, 60)), (1, (20, 14, 16))])
    stars(p, 200, 31, 1000); moon(p, 820, 260, 44)
def night_market_mid(p):
    city(p, 1300, (30, 24, 40), 32, (255, 190, 100))
    for x, c, sd in ((-60, (140, 60, 50), 33), (330, (50, 90, 110), 34), (720, (150, 110, 50), 35)): stall(p, x, 1560, 300, (44, 30, 28), c, sd)
def night_market_near(p):
    lantern(p, 160, 1080, .9); lantern(p, 920, 1080, .9)
    p.grad_poly([(-200, 1560), (1300, 1560), (1300, 2300), (-200, 2300)], (70, 50, 46), (20, 14, 14), 1560, 1900)
    balance_scale(p, 540, 1240, .55, tilt=0)

def tense_sky(p):
    p.sky([(0, (14, 10, 22)), (.5, (50, 30, 46)), (.8, (110, 50, 46)), (1, (20, 12, 12))])
    cloud_bank(p, 300, (50, 34, 46), (24, 16, 24), 41, 80, 220)
def tense_mid(p): city(p, 1340, (20, 14, 20), 42, (255, 170, 90))
def tense_near(p):
    p.rect(-100, 1500, 1200, 2300, (14, 10, 12))
    lantern(p, 540, 1380, 1.1, (255, 170, 80))

def wealth_sky(p):
    p.sky([(0, (20, 12, 10)), (.6, (50, 30, 20)), (1, (14, 8, 6))])
    p.glow(540, 1400, 700, (200, 120, 50), .35)
def wealth_near(p):
    p.rect(-100, 1500, 1200, 2300, (30, 18, 12))
    coins(p, 540, 1540, 1.15, 51)
    lantern(p, 120, 1250, .8); lantern(p, 960, 1250, .8)

def dawn_sky(p):
    p.sky([(0, (24, 30, 70)), (.45, (90, 90, 140)), (.68, (240, 170, 130)), (.78, (255, 220, 160)), (1, (90, 70, 60))])
    stars(p, 80, 61, 500)
def dawn_rays(p):
    rays(p, 540, 1320, (255, 225, 170), n=11, spread=110, length=1700, width=6, a=.26, angle=-90, seed=62)
    p.glow(540, 1320, 440, (255, 215, 160), .7)
def dawn_near(p):
    mountains(p, 1400, 220, (50, 40, 60), 63)
    p.rect(-100, 1460, 1200, 2300, (34, 26, 34))
    palm(p, 170, 1520, 380, (24, 18, 22), .05); palm(p, 900, 1520, 330, (24, 18, 22), -.05)

def threat_sky(p):
    p.sky([(0, (30, 8, 10)), (.5, (110, 30, 24)), (.75, (200, 80, 40)), (1, (40, 12, 10))])
    cloud_bank(p, 380, (80, 24, 20), (40, 12, 12), 71, 70, 220)
def threat_near(p):
    gate(p, 540, 1520, 1.1, (96, 48, 40))
    p.rect(-100, 1520, 1200, 2300, (24, 10, 10))

def quake_sky(p):
    p.sky([(0, (24, 20, 26)), (.5, (80, 64, 60)), (.75, (150, 110, 80)), (1, (40, 30, 24))])
    cloud_bank(p, 320, (70, 60, 64), (40, 34, 38), 81, 80, 220)
def quake_mid(p): ruins(p, 1330, (100, 80, 66), 82)
def quake_near(p):
    p.grad_poly([(-200, 1360), (1300, 1360), (1300, 2300), (-200, 2300)], (120, 92, 66), (44, 32, 24), 1360, 1900)
    cracks(p, 1380, (30, 20, 16), 83)
    ruins(p, 1560, (80, 60, 48), 84)

# the loop rhyme: same market and same scale as frame 1, now level, in morning light
def morning_sky(p):
    p.sky([(0, (90, 150, 215)), (.5, (200, 215, 235)), (.72, (255, 232, 180)), (1, (150, 130, 90))])
    sun(p, 220, 1180, 80, (255, 240, 200))
def morning_mid(p):
    city(p, 1250, (190, 150, 120), 11, None)
    stall(p, -40, 1520, 260, (90, 60, 44), (190, 80, 56), 12); stall(p, 860, 1540, 260, (90, 60, 44), (70, 110, 150), 13)
def morning_near(p):
    p.grad_poly([(-200, 1540), (1300, 1540), (1300, 2300), (-200, 2300)], (190, 150, 110), (110, 80, 60), 1540, 1900)
    p.glow(540, 1100, 420, (255, 240, 200), .45)
    balance_scale(p, 540, 1170, .72, tilt=0)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 121, 900); moon(p, 820, 300, 56)
def end_mid(p): city(p, 1380, (30, 26, 50), 122, (255, 200, 120))
def end_near(p): lantern(p, 150, 900, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[dusk_sky, dusk_mid, dusk_near], fx=['dust'], cam='in', bloom=.55,
         title=dict(text='They cheated on the scale. What did their prophet say?', arabic=TITLE_AR, hold=99, plain=True),
         no_caption=(0,),
         lines=['They cheated on the scale. What did their prophet say?']),
    dict(layers=[plenty_sky, plenty_mid, plenty_near], fx=['dust'], cam='right',
         lines=['Shuayb, peace be upon him, was sent to Madyan, his own people.', 'They lived in plenty. But they gave people short measure.']),
    dict(layers=[night_market_sky, night_market_mid, night_market_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='11:85', ar=(0, 9), en='O my people, give full measure and weight in justice and do not deprive the people of their due', line=1, ar_size=70, y=600),
         lines=['He called them to worship Allah alone. Then he said:', 'O my people, give full measure and weight in justice, and do not deprive the people of their due.']),
    dict(layers=[tense_sky, tense_mid, tense_near], fx=['sand'], cam='in', pause=0.5,
         lines=['They had an answer ready. What did they say?']),
    dict(layers=[wealth_sky, wealth_near], fx=['embers'], cam='in', bloom=.75,
         verse=dict(key='11:87', ar=(1, 16), en="O Shu'ayb, does your prayer command you that we should leave what our fathers worship or not do with our wealth what we please?", line=1, ar_size=58, y=620),
         lines=['They said:', 'O Shuayb, does your prayer command you that we should leave what our fathers worship, or not do with our wealth what we please?']),
    dict(layers=[dawn_sky, dawn_rays, dawn_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='11:88', ar=(21, 31), en='I only intend reform as much as I am able. And my success is not but through Allah', line=1, ar_size=70, y=620),
         lines=['He answered:', 'I only intend reform as much as I am able. And my success is not but through Allah.']),
    dict(layers=[threat_sky, threat_near], fx=['sand'], cam='in',
         lines=['Their arrogant leaders threatened to drive him and the believers out of their city.']),
    dict(layers=[quake_sky, quake_mid, quake_near], fx=['dust'], cam='out',
         lines=['Then the earthquake seized them.', 'And Allah saved Shuayb and those who believed with him.']),
    dict(layers=[morning_sky, morning_mid, morning_near], fx=['dust'], cam='out',
         lesson=dict(text='Give people their full due. Success is only through Allah.', after=0, y=520, size=76), no_caption=(0,),
         lines=['Give people their full due. Your success is only through Allah.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with someone', line2='who runs a business'), no_caption=(0,),
         lines=['Share this with someone who runs a business. And follow for a new story from the Quran every day.']),
]

PRON = {'Shuayb': 'ʃuˈajb', 'Madyan': 'mˈadjan'}

CAPTION = """They cheated on the scale. What did their prophet say? ⚖️

Shu'ayb, peace be upon him, was sent to his people, Madyan. They lived in plenty, but they gave short measure. He called them to worship Allah alone, and said: "O my people, give full measure and weight in justice and do not deprive the people of their due." (Quran 11:85)

They answered: "O Shu'ayb, does your prayer command you that we should leave what our fathers worship or not do with our wealth what we please?" (Quran 11:87)

He said: "I only intend reform as much as I am able. And my success is not but through Allah." (Quran 11:88)

Their leaders threatened to drive him out (7:88). Then the earthquake seized them (7:91), and Allah saved Shu'ayb and those who believed with him (11:94).

Give people their full due. Success is only through Allah.

📖 Sources: Quran 7:85–93, 11:84–95 (Saheeh International)
Share this with someone who runs a business. Follow for a new story every day.

#QuranicStories #ProphetShuayb #IslamicReminder"""

FIRST_COMMENT = """Who do you know who is honest in every deal? Tell them with this story 🤍

References: Quran, Surah Al-A'raf 7:85–93 and Surah Hud 11:84–95 (Saheeh International translation)."""
