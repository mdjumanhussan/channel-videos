"""Story 19: The parting of the sea. Sources: Quran 26:52-68, 20:77-79, 10:90-91, 2:50, 44:23-24 (Saheeh International).
No people are drawn: no Musa, no Pharaoh, no soldiers, no crowd, no figure of any kind, and nothing stands for Allah.
Only the sea, the shore, dunes, a far dust cloud, a city seen from far off, the sky and light.
Facts used and where they are: "Travel by night with My servants; indeed, you will be pursued" (26:52); Pharaoh sent gatherers to
the cities (26:53); "Indeed, those are but a small band" (26:54); pursued at sunrise (26:60); "Indeed, we are to be overtaken"
(26:61); "No! Indeed, with me is my Lord; He will guide me" (26:62); strike the sea, it parted, each portion like a great towering
mountain (26:63); a dry path through the sea (20:77); "And We saved Moses and those with him, all together" (26:65); Pharaoh
pursued with his soldiers and the sea covered them (20:78); when drowning overtook him he said "I believe" (10:90); "Now? And you
had disobeyed [Him] before and were of the corrupters" (10:91).
Not used: any number of paths or tribes (the Quran gives no number here; one path is drawn as in 20:77), any number of people or
soldiers, chariots, any place name for the sea, any wording of the Children of Israel beyond 26:61, the staff drawn on screen.
The "army" is only ever a dust cloud far away. It is never shown as figures.
Improvement tried today: the hook is a statement dropped into the middle of the moment, not a question. Frame 1 says only "The army
behind them. The sea ahead." (7 words). Reason: page data 5 Nov. Reels whose hook ended in "Why?" hold 2 s (Magicians) and 7 s (Baby
Musa); statement hooks hold 13 s (Fire) and 16 s (Ayyub). The Creator Stack heatmap write-up found question openers "get skipped"
(author's own 200 Reels, not a study). Live motion from 18 is kept where the story needs it: the sea parts on the word "parted".
Also kept: plain headline = spoken hook with nothing else on frame 1 (caption hidden), second loop ("What would Musa say?") with a
0.5 s pause, rhyming loop ending (same shore, dust gone, calm morning), speed 1.1, lesson card, specific send-to end card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  19'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'The Army Behind, the Sea Ahead'
HITS = [(5, 0, 4.0), (8, 1, 0.0)]      # the word 'parted' in 26:63; then 'Now?' in 10:91

# ---------------------------------------------------------------- live dust cloud (far away, never figures)
def _puffs():
    rnd = random.Random(19); out = []
    for i in range(46):
        f = i / 45
        out.append(dict(u=rnd.uniform(-1, 1), v=f, r=rnd.uniform(.5, 1.1), ph=rnd.uniform(0, 6.3), sp=rnd.uniform(.5, 1.1)))
    return out
PUFFS = _puffs()

def dust_cloud(img, tt, info, x=800, base=980, w=420, h=300, col=(112, 70, 56), lit=(244, 170, 116), a=225, grow=None):
    """A wall of dust far off on the land, billowing. grow=(start_scale, end_scale) over the scene."""
    s = 1.0
    if grow:
        s = lerp(grow[0], grow[1], clamp((tt - info['start']) / max(.1, info['end'] - info['start'])))
    x0 = int(max(0, x - w * s - 240)); y0 = int(max(0, base - h * s - 240)); x1 = int(min(W, x + w * s + 240)); y1 = int(min(H, base + 300))
    lay = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for p in PUFFS:
        drift = math.sin(tt * p['sp'] + p['ph'])
        px = x + p['u'] * w * s * (1 - .45 * p['v']) + drift * 16 - x0
        py = base - p['v'] * h * s + math.cos(tt * p['sp'] * .8 + p['ph']) * 10 - y0
        r = p['r'] * lerp(92, 56, p['v']) * (.8 + .35 * s) * (1 + .08 * drift)
        c = lc(col, lit, clamp(.15 + .75 * p['v']))
        d.ellipse((px - r * 1.35, py - r, px + r * 1.35, py + r), fill=c + (a,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(16)), (x0, y0))

# ---------------------------------------------------------------- the sea that parts (redrawn every frame, cam='hold')
VP = (540, 900)         # where the path meets the horizon

def _lin(a, b, f): return (lerp(a[0], b[0], f), lerp(a[1], b[1], f))

def sea_walls(img, tt, info, part=None, close=None, base=1.0, wall=(14, 74, 104), deep=(6, 34, 62), crest=(226, 246, 244), sand=(214, 180, 126), sand_d=(150, 112, 74)):
    """Two towering walls of water, in perspective, with a dry sandy path between. q = 0 closed, 1 fully open.
    part=(line, f0, f1) opens across that fraction of the spoken line. close=(line, f0, f1) shuts it again."""
    q = base
    if part:
        a, b = info['lines'][part[0]]; q = ease((tt - lerp(a, b, part[1])) / max(.05, (b - a) * (part[2] - part[1])))
    if close:
        a, b = info['lines'][close[0]]; q = 1 - ease((tt - lerp(a, b, close[1])) / max(.05, (b - a) * (close[2] - close[1])))
    if q <= .002: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    bw = 440 * q                                 # half width of the path at the bottom of the frame
    top = lerp(2000, 170, q ** .8)               # crest height of the wall at the near edge of the frame
    nearb = 2000
    # sand path
    d.polygon([VP, (540 + bw * 1.1, nearb), (540 - bw * 1.1, nearb)], fill=sand + (255,))
    rnd = random.Random(1963)                    # dry, wind-marked sand: short scattered marks, nothing that reads as planks
    for k in range(90):
        f = rnd.random() ** 1.6; y = lerp(VP[1], nearb, f); hw = bw * 1.05 * f; x = 540 + rnd.uniform(-1, 1) * hw; L = rnd.uniform(.05, .16) * (bw * 2) * (.15 + f)
        d.line([(x - L, y), (x - L * .3, y + rnd.uniform(1, 7) * f), (x + L * .4, y - rnd.uniform(1, 6) * f), (x + L, y + rnd.uniform(-3, 3) * f)], fill=lc(sand, sand_d, rnd.uniform(.25, .6)) + (255,), width=max(1, int(1 + 3.5 * f)))
    for sx in (-1, 1):
        far = VP
        foot = (540 + sx * bw, nearb)                                     # where wall meets sand, near the viewer
        hi = (540 + sx * (bw + 760), lerp(top, -560, q ** 1.4))                       # crest, leaning outward beyond the frame edge
        # crest line from far to near, with moving waves
        crestpts = []
        n = 34
        for i in range(n + 1):
            f = (i / n) ** 1.7; x, y = _lin(far, hi, f)
            y += math.sin(f * 15 + tt * 2.4 + sx) * 34 * f * q + math.sin(f * 37 - tt * 3.2) * 12 * f * q
            crestpts.append((x, y))
        body = crestpts + [(540 + sx * 1300, top + 200), (540 + sx * 1300, nearb), foot]
        d.polygon(body, fill=deep + (255,))
        # bands of colour across the face of the wall, lighter toward the crest
        for k in range(1, 9):
            g = k / 9
            band = []
            for i in range(n + 1):
                f = (i / n) ** 1.7; bx, by = _lin(far, foot, f); cx, cy = crestpts[i]
                band.append((lerp(bx, cx, g), lerp(by, cy, g) + math.sin(f * 21 + g * 9 + tt * 1.7) * 11 * f))
            band2 = band + [(c[0], c[1]) for c in crestpts[::-1]]
            d.polygon(band2, fill=lc(deep, wall, g * g * .9) + (255,))
        # white streaks running down the face
        for k in range(26):
            f = ((k + .5) / 26) ** 1.5; bx, by = _lin(far, foot, f); i = int(f ** (1 / 1.7) * n); cx, cy = crestpts[i]
            ph = (tt * .45 + k * .37) % 1
            g0, g1 = ph, min(1, ph + .16)
            d.line([(lerp(bx, cx, g0), lerp(by, cy, g0)), (lerp(bx, cx, g1), lerp(by, cy, g1))], fill=lc(wall, crest, .28) + (255,), width=max(1, int(1 + 5 * f)))
        # foam along the crest
        d.line(crestpts, fill=crest + (255,), width=max(2, int(14 * q)), joint='curve')
        # foam along the foot, where the wall stands on dry sand
        fp = [(lerp(far[0], foot[0], (i / 20) ** 1.7), lerp(far[1], foot[1], (i / 20) ** 1.7)) for i in range(21)]
        d.line(fp, fill=lc(sand, crest, .7) + (255,), width=max(2, int(8 * q)), joint='curve')
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(.8)))

# ---------------------------------------------------------------- layer painters
def shore_sky(stops, sun_at=None):
    def f(p):
        p.sky(stops)
        if sun_at: sun(p, sun_at[0], sun_at[1], sun_at[2], sun_at[3])
        clouds(p, 191, 200, 700, (255, 226, 190), 5, 80)
    return f

def shore_water(top, bot, glint=(255, 214, 160)):
    def f(p):
        sea(p, 900, top, bot, 192, glint)
    return f

def shore_land(sand_top, sand_bot):
    """The land: a beach coming in from the right and along the bottom of the frame."""
    def f(p):
        A, B, C, D = (1300, 912), (820, 916), (560, 1180), (-200, 1600)      # one smooth curve of beach
        edge = [tuple((1 - u) ** 3 * A[i] + 3 * (1 - u) ** 2 * u * B[i] + 3 * (1 - u) * u * u * C[i] + u ** 3 * D[i] for i in (0, 1)) for u in [k / 40 for k in range(41)]]
        p.grad_poly(edge + [(-200, 2300), (1300, 2300)], sand_top, sand_bot, 905, 1800)
        p.line(edge, (255, 244, 226), 9, 210)
        rnd = random.Random(193)
        for _ in range(32):
            x, y = rnd.uniform(380, 1180), rnd.uniform(1150, 1900)
            if y < 1000 + (1200 - x) * .55: continue
            p.line([(x - 70, y), (x, y + rnd.uniform(-4, 4)), (x + 70, y)], lc(sand_top, (60, 30, 10), .4), 3, 60)
    return f

DAWN = [(0, (24, 26, 74)), (.2, (92, 62, 112)), (.38, (232, 116, 88)), (.47, (255, 186, 110)), (.6, (255, 200, 130)), (1, (120, 80, 60))]
MORN = [(0, (70, 140, 200)), (.26, (150, 196, 220)), (.42, (250, 224, 180)), (.47, (255, 236, 196)), (1, (200, 170, 130))]

def night_sky(p):
    p.sky([(0, (6, 10, 34)), (.4, (16, 26, 66)), (.58, (40, 52, 104)), (.66, (84, 80, 128)), (1, (10, 12, 26))])
    stars(p, 380, 195, 1050); moon(p, 780, 300, 62)
def night_mid(p):
    mountains(p, 1120, 190, (22, 26, 52), 196, (60, 66, 110), 5)
def night_near(p):
    dunes(p, 1130, 30, (52, 56, 96), (14, 14, 32), 197)
    L, Rr = [], []
    for k in range(41):
        f = k / 40; y = lerp(1140, 2300, f ** 1.3); c = 545 + math.sin(f * 7.5) * lerp(30, 130, f); w = lerp(10, 300, f ** 1.5)
        L.append((c - w, y)); Rr.append((c + w, y))
    p.poly(L + Rr[::-1], (112, 112, 150), 80)
    for x, b, h, ln in ((130, 1520, 520, -.05), (980, 1560, 560, .06)): palm(p, x, b, h, (8, 8, 20), ln)

def city_sky(p):
    p.sky([(0, (18, 6, 26)), (.42, (70, 18, 46)), (.6, (170, 56, 50)), (.68, (232, 110, 62)), (1, (24, 8, 14))])
    clouds(p, 198, 140, 620, (150, 60, 70), 6, 70)
def city_mid(p):
    pyramids(p, 1130, (96, 40, 44), (56, 20, 30), 199)
def city_near(p):
    city(p, 1330, (34, 12, 22), 200, (255, 170, 80), domes=False)
    dunes(p, 1320, 22, (40, 16, 24), (12, 6, 10), 201)
    p.glow(540, 1300, 500, (255, 110, 50), .35)

def rise_sky(p):
    p.sky([(0, (30, 28, 72)), (.24, (112, 64, 108)), (.4, (246, 120, 80)), (.47, (255, 204, 130)), (.5, (255, 230, 170)), (1, (60, 50, 70))])
    p.glow(540, 880, 760, (255, 200, 120), .75)
    sun(p, 540, 905, 110, (255, 232, 170))
def rise_water(p): sea(p, 900, (214, 128, 86), (20, 40, 66), 202, (255, 220, 160))

def part_sky(p):
    p.sky([(0, (34, 50, 104)), (.24, (120, 110, 150)), (.42, (250, 170, 110)), (.47, (255, 226, 170)), (1, (60, 60, 80))])
    p.glow(540, 890, 520, (255, 226, 170), .7)
def part_water(p): sea(p, 900, (40, 104, 130), (8, 40, 70), 203, (255, 230, 190))

def path_sky(p):
    p.sky([(0, (60, 124, 190)), (.26, (150, 200, 226)), (.42, (255, 236, 200)), (.47, (255, 244, 214)), (1, (80, 120, 140))])
    p.glow(540, 880, 460, (255, 244, 210), .9)
def path_water(p): sea(p, 900, (70, 150, 170), (14, 70, 100), 204, (255, 255, 240))

def dark_sky(p):
    p.sky([(0, (10, 12, 30)), (.26, (30, 34, 66)), (.44, (96, 72, 92)), (.47, (150, 96, 90)), (1, (10, 18, 34))])
    clouds(p, 205, 120, 700, (70, 70, 110), 7, 90)
def dark_water(p):
    sea(p, 900, (28, 54, 84), (6, 20, 40), 206, (190, 210, 220))
    for k in range(9):
        f = (k / 8) ** 1.5; y = lerp(960, 1860, f)
        pts = [(x, y + math.sin(x * .012 + k * 2) * lerp(6, 46, f)) for x in range(-150, 1250, 60)]
        p.line(pts, (150, 186, 200), 3 + 12 * f, 130)

def after_sky(p):
    p.sky([(0, (22, 30, 70)), (.26, (66, 66, 110)), (.44, (196, 104, 90)), (.47, (232, 130, 90)), (1, (20, 22, 44))])
    sun(p, 760, 880, 62, (240, 150, 100))
def after_water(p): sea(p, 900, (120, 76, 88), (10, 22, 44), 207, (240, 170, 130))

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 208, 900); moon(p, 820, 300, 56)
def end_water(p): sea(p, 1410, (150, 110, 96), (12, 20, 40), 209, (250, 200, 150))

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[shore_sky(DAWN), shore_water((150, 96, 96), (12, 34, 60)), shore_land((206, 150, 104), (92, 62, 54))],
         fx=[(dust_cloud, dict(x=850, base=985, w=320, h=250)), 'dust'], cam='hold', bloom=.5,
         title=dict(text='The army behind them. The sea ahead.', hold=99, plain=True), no_caption=(0,),
         lines=['The army behind them. The sea ahead.']),
    dict(layers=[night_sky, night_mid, night_near], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='26:52', ar=(4, 8), en='Travel by night with My servants; indeed, you will be pursued', line=1, ar_size=72, y=560),
         lines=['Allah inspired Musa, peace be upon him:', 'Travel by night with My servants; indeed, you will be pursued.']),
    dict(layers=[city_sky, city_mid, city_near], fx=['embers'], cam='up',
         verse=dict(key='26:54', en='Indeed, those are but a small band', line=2, ar_size=82, y=560),
         lines=['Pharaoh sent gatherers through the cities.', 'He said:', 'Indeed, those are but a small band.']),
    dict(layers=[shore_sky(DAWN), shore_water((170, 104, 92), (12, 34, 60)), shore_land((214, 152, 102), (92, 62, 54))],
         fx=[(dust_cloud, dict(x=830, base=1010, w=420, h=390, grow=(1.0, 1.35))), 'dust'], cam='hold', bloom=.55, pause=0.5,
         verse=dict(key='26:61', ar=(6, 8), en='Indeed, we are to be overtaken', line=2, ar_size=84, y=470),
         lines=['At sunrise, the army reached them.', 'The companions of Musa said:', 'Indeed, we are to be overtaken.', 'What would Musa say?']),
    dict(layers=[rise_sky, rise_water], fx=['twinkle'], cam='in', bloom=.8,
         verse=dict(key='26:62', ar=(1, 6), en='No! Indeed, with me is my Lord; He will guide me', line=1, ar_size=78, y=470),
         lines=['He said:', 'No! Indeed, with me is my Lord; He will guide me.']),
    dict(layers=[part_sky, part_water], fx=[(sea_walls, dict(part=(0, .55, .86)))], cam='hold', bloom=.6,
         verse=dict(key='26:63', ar_size=56, y=480, line=0),
         lines=['Then We inspired to Moses, Strike with your staff the sea, and it parted, and each portion was like a great towering mountain.']),
    dict(layers=[path_sky, path_water], fx=[(sea_walls, dict(base=1.0, wall=(26, 112, 140), deep=(10, 56, 88))), 'dust'], cam='hold', bloom=.75,
         verse=dict(key='26:65', ar_size=78, y=430, line=1),
         lines=['A dry path through the sea.', 'And We saved Moses and those with him, all together.']),
    dict(layers=[dark_sky, dark_water], fx=[(sea_walls, dict(close=(1, 0, .7), wall=(16, 52, 80), deep=(6, 24, 46), crest=(190, 214, 224), sand=(120, 104, 90), sand_d=(70, 60, 56)))], cam='hold', bloom=.4, pause=0.5,
         lines=['Pharaoh pursued them with his soldiers.', 'Then the sea covered them.']),
    dict(layers=[after_sky, after_water], fx=['dust'], cam='in', bloom=.6,
         verse=dict(key='10:91', ar_size=72, y=520, line=1),
         lines=['As he drowned, Pharaoh said: I believe.', 'Now? And you had disobeyed Him before and were of the corrupters.']),
    dict(layers=[shore_sky(MORN), shore_water((170, 206, 206), (24, 90, 120), (255, 255, 240)), shore_land((244, 220, 170), (170, 130, 90))], fx=['dust'], cam='out', bloom=.7,
         lesson=dict(text='When every way is closed, Allah can open a path.', after=0, y=560, size=80), no_caption=(0,),
         lines=['When every way is closed, Allah can open a path.']),
    dict(layers=[end_sky, end_water], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone who feels stuck'), no_caption=(0,),
         lines=['Share this with someone who feels stuck. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """The army behind them. The sea ahead. 🌊

Allah inspired Musa (Moses), peace be upon him: "Travel by night with My servants; indeed, you will be pursued." (Quran 26:52)

Pharaoh's army reached them at sunrise. The companions of Musa said: "Indeed, we are to be overtaken." (Quran 26:61)

Musa answered: "No! Indeed, with me is my Lord; He will guide me." (Quran 26:62)

The sea parted, "and each portion was like a great towering mountain." (Quran 26:63) Allah saved Musa and those with him (26:65), and the sea covered Pharaoh and his soldiers (20:78). As he drowned, Pharaoh said he believed. The answer: "Now? And you had disobeyed [Him] before and were of the corrupters." (Quran 10:91)

When every way is closed, Allah can open a path.

📖 Sources: Quran 26:52–68, 20:77–79, 10:90–91 (Saheeh International)
Share this with someone who feels stuck. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """What would you have said on that shore? Send this to someone who feels stuck 🤍

References: Quran, Surah Ash-Shu'ara 26:52–68, Surah Ta-Ha 20:77–79 and Surah Yunus 10:90–91 (Saheeh International translation)."""
