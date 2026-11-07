"""Story 21: Qarun and his treasure. Source: Quran 28:76-83 (Saheeh International).
No people are drawn: no Musa, no Qarun, no crowd, no "people of knowledge", no figure of any kind, and nothing stands for Allah.
Only a palace, keys, chests, coins, a vault, a road with banners, a town, a lamp, the ground, the sky and light.
Facts used and where they are: Qarun was from the people of Moses but tyrannized them; he was given treasures whose keys would burden
a band of strong men; his people told him "Do not exult" (28:76); "do good as Allah has done good to you" (28:77); he said "I was only
given it because of knowledge I have" (28:78); he came out before his people in his adornment, and those who desired the worldly life
said "Oh, would that we had like what was given to Qarun" (28:79); those given knowledge said "The reward of Allah is better for he who
believes and does righteousness" (28:80); "And We caused the earth to swallow him and his home", and no company aided him (28:81);
those who had wished for his position said "If not that Allah had conferred favor on us, He would have caused it to swallow us" (28:82).
Not used: any number of keys or of men carrying them, what the keys were made of, Qarun's clothes, mounts or procession details, any
family tie to Musa beyond "from the people of Moses", the zakat story, any plot against Musa, Israiliyyat. The keys, chests and banners
on screen are drawn simply; no claim is made about how they looked.
Improvement tried today: proof of the hook inside the first 7 seconds. Frame 1 states only the striking fact ("His keys alone were too
heavy for strong men."), and the very next line is the verse card that says it (28:76), arriving at about 6 s instead of later.
Source: OpusClip's Reels hook guide (Nov 2025, author's advice): "the first three seconds belong to the hook and nothing else", then show
proof "within the first five to seven seconds after the hook", and the payoff must match the promise. Playbook 2026-11-07.
Also kept: statement hook = headline with nothing else on frame 1 (caption hidden); live motion at the peak (the palace sinks on
"swallow", deep hit); second loop ("Then it happened.", 0.5 s pause); rhyming loop ending (same ground as frame 1, morning, palace gone);
speed 1.1; lesson card; specific send-to end card; CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  21'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Qarun: The Man Whose Keys Were Too Heavy'
HITS = [(6, 0, 1.6), (7, 1, 0.0)]      # 'swallow'; then 'If not that Allah had conferred favor on us'

# ---------------------------------------------------------------- the palace (a cached sprite, so it can sink live)
_pal = {}
def palace_sprite(s=1.0, wall=(196, 150, 104), dark=(96, 64, 44), gold=(255, 200, 96), win=(255, 206, 120)):
    k = (s, wall, dark, gold, win)
    if k in _pal: return _pal[k]
    Q = 2; Wd, Hd = 1000, 640; im = Image.new('RGBA', (Wd * Q, Hd * Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def R(x0, y0, x1, y1, c): d.rectangle((x0 * Q, y0 * Q, x1 * Q, y1 * Q), fill=c)
    # two wings, a tall centre block, stepped flat roofs, a colonnade, gold bands. Flat roofs on purpose (not a mosque).
    for x0, x1, top in ((40, 320, 300), (680, 960, 300)):
        R(x0, top, x1, 640, wall); R(x0 - 14, top - 22, x1 + 14, top, dark); R(x0 + 20, top - 50, x1 - 20, top - 22, wall)
        R(x0 + 6, top + 20, x1 - 6, top + 34, gold)
        for wx in range(x0 + 34, x1 - 40, 62):
            R(wx, top + 80, wx + 28, top + 150, win); R(wx, top + 200, wx + 28, top + 270, win)
    R(300, 160, 700, 640, lc(wall, (255, 255, 255), .08)); R(284, 136, 716, 160, dark); R(320, 96, 680, 136, wall); R(350, 66, 650, 96, dark)
    R(306, 186, 694, 204, gold); R(306, 60, 694, 70, gold)
    for cx in range(330, 690, 60):                                   # colonnade
        R(cx, 300, cx + 24, 640, lc(wall, (255, 255, 255), .2)); R(cx - 6, 292, cx + 30, 304, gold)
    R(300, 300, 700, 312, dark)
    R(440, 420, 560, 640, (40, 24, 18)); d.ellipse((440 * Q, 360 * Q, 560 * Q, 480 * Q), fill=(40, 24, 18))
    d.rectangle((470 * Q, 520 * Q, 530 * Q, 640 * Q), fill=win)
    im = im.resize((int(Wd * s), int(Hd * s)), Image.LANCZOS)
    _pal[k] = im
    return im

CRACK = [(-430, 0), (-300, 10), (-180, -4), (-60, 14), (60, -6), (190, 12), (310, -2), (440, 8)]
def palace_fx(img, tt, info, x=540, base=1180, s=.9, sink=None, glow=.6, **kw):
    """The palace on the ground. sink=(line, f0, f1): it sinks into the earth as the line is spoken (28:81), dust rises,
    a crack opens and closes over it. Nobody is drawn."""
    q = 0.0
    if sink:
        a, b = info['lines'][sink[0]]; q = ease((tt - lerp(a, b, sink[1])) / max(.05, (b - a) * (sink[2] - sink[1])))
    spr = palace_sprite(s, **kw)
    shake = math.sin(tt * 47) * 6 * (q * (1 - q) * 4) if sink else 0
    depth = int(spr.height * q * 1.02)
    if depth < spr.height:
        part = spr.crop((0, 0, spr.width, spr.height - depth))
        if glow > 0 and q < .05:
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((x - 520 * s, base - 520 * s, x + 520 * s, base + 60 * s), fill=(255, 190, 90, int(70 * glow)))
            img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(70)))
        img.alpha_composite(part, (int(x - spr.width / 2 + shake), int(base - spr.height + depth)))
    if sink and 0 < q:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        open_ = math.sin(math.pi * min(1, q * 1.05)) if q < 1 else 0
        gap = 38 * open_ * s
        top = [(x + u * s, base + v * s - gap) for u, v in CRACK]; bot = [(x + u * s, base + v * s + gap * .4) for u, v in CRACK[::-1]]
        if gap > 1: d.polygon(top + bot, fill=(14, 8, 8, 255))
        d.line([(x + u * s, base + v * s) for u, v in CRACK], fill=(40, 24, 18, int(255 * min(1, q * 3))), width=6)
        img.alpha_composite(lay)
        # dust rising off the ground while it sinks
        rnd = random.Random(21); dl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dl)
        dens = math.sin(math.pi * q) if q < 1 else 0
        for i in range(60):
            u = rnd.uniform(-1, 1); sp = rnd.uniform(.4, 1)
            px = x + u * 480 * s + math.sin(tt * sp * 2 + i) * 20; py = base - rnd.uniform(0, 260) * sp * (.4 + q)
            r = rnd.uniform(30, 80)
            dd.ellipse((px - r, py - r * .7, px + r, py + r * .7), fill=(176, 140, 104, int(90 * dens)))
        img.alpha_composite(dl.filter(ImageFilter.GaussianBlur(18)))

# ---------------------------------------------------------------- objects
def key(p, x, y, s, col, ang=0.0, a=255):
    """A large old key: ring bow, long shaft, two teeth. ang in degrees."""
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def T(u, v): return (x + (u * c - v * sn) * s, y + (u * sn + v * c) * s)
    dark = lc(col, (0, 0, 0), .45)
    p.line([T(40, 0), T(260, 0)], dark, 22 * s, a); p.line([T(40, 0), T(260, 0)], col, 16 * s, a)
    for u in (210, 245): p.poly([T(u, 0), T(u + 22, 0), T(u + 22, 46), T(u, 46)], col, a)
    for r, cc in ((52, dark), (46, col), (24, dark)):
        cx, cy = T(0, 0); p.ell(cx, cy, r * s, r * s, cc, a)

def key_heap(p, cx, cy, n, seed, cols=((214, 168, 84), (180, 132, 70), (236, 196, 110), (150, 110, 70)), spread=(380, 90), s=.9):
    rnd = random.Random(seed)
    for i in range(n):
        f = i / max(1, n - 1)
        key(p, cx + rnd.uniform(-1, 1) * spread[0] * (1 - .5 * f), cy + rnd.uniform(-.2, 1) * spread[1] - f * spread[1] * .8,
            s * rnd.uniform(.75, 1.1), rnd.choice(cols), rnd.uniform(-180, 180))
    p.glow(cx, cy - 20, 420, (255, 196, 100), .35)

def chest(p, cx, base, s, wood=(118, 72, 40), band=(220, 176, 84), open_=False):
    w, h = 170 * s, 110 * s
    p.rect(cx - w, base - h, cx + w, base, wood); p.rect(cx - w - 8 * s, base - h - 50 * s, cx + w + 8 * s, base - h, lc(wood, (255, 220, 160), .15))
    for dx in (-.55, .55): p.rect(cx + dx * w - 12 * s, base - h - 50 * s, cx + dx * w + 12 * s, base, band)
    p.rect(cx - 18 * s, base - h - 20 * s, cx + 18 * s, base - h + 26 * s, band)
    if open_:
        p.glow(cx, base - h - 40 * s, 240 * s, (255, 200, 90), .6)
        for k in range(14): p.ell(cx + (k - 7) * 22 * s, base - h - 52 * s - (k % 3) * 12 * s, 20 * s, 9 * s, (250, 210, 100))

def coins(p, cx, cy, n, seed, r=16, spread=260):
    rnd = random.Random(seed)
    for _ in range(n):
        x = cx + rnd.gauss(0, spread * .45); y = cy + rnd.uniform(-20, 40)
        p.ell(x, y, r, r * .45, (150, 104, 40)); p.ell(x, y - 2, r * .9, r * .38, (246, 204, 96))
    p.glow(cx, cy, spread * 1.3, (255, 200, 90), .3)

def banner(p, x, base, h, col, pole=(70, 46, 30), flip=1):
    p.line([(x, base), (x, base - h)], pole, 8)
    p.poly([(x, base - h), (x + 80 * flip, base - h + 16), (x + 70 * flip, base - h + 120), (x, base - h + 104)], col)
    p.ell(x, base - h - 10, 10, 10, (255, 210, 110))

def vault_arches(p, col, edge, light):
    p.rect(-200, -200, 1300, 2300, lc(col, (0, 0, 0), .4))
    for cx in (110, 540, 970):
        p.rect(cx - 170, 360, cx + 170, 1500, col); p.ell(cx, 360, 170, 150, col)
        p.rect(cx - 150, 420, cx + 150, 1500, lc(col, (0, 0, 0), .55)); p.ell(cx, 420, 150, 130, lc(col, (0, 0, 0), .55))
        p.line([(cx - 170, 1500), (cx - 170, 360)], edge, 4, 140); p.line([(cx + 170, 1500), (cx + 170, 360)], edge, 4, 140)
    p.glow(540, 820, 520, light, .4)
    p.grad_poly([(-200, 1240), (1300, 1240), (1300, 2300), (-200, 2300)], lc(col, (255, 220, 160), .1), lc(col, (0, 0, 0), .7), 1240, 1900)

# ---------------------------------------------------------------- layer painters
DUSK = [(0, (18, 12, 46)), (.22, (78, 40, 84)), (.38, (210, 98, 70)), (.46, (255, 168, 92)), (.5, (220, 130, 80)), (1, (40, 22, 18))]
MORN = [(0, (64, 132, 196)), (.24, (150, 196, 224)), (.4, (250, 226, 186)), (.47, (255, 238, 204)), (.5, (230, 210, 180)), (1, (70, 56, 40))]

def dusk_sky(p): p.sky(DUSK); sun(p, 820, 760, 44, (255, 190, 120)); clouds(p, 301, 180, 640, (255, 190, 150), 6, 90)
def morn_sky(p): p.sky(MORN); sun(p, 820, 700, 40); clouds(p, 302, 180, 600, (255, 250, 236), 5, 110)
def far_city(col, lights):
    def fn(p): mountains(p, 1080, 140, lc(col, (0, 0, 0), .2), 303, None, 4); city(p, 1150, col, 304, lights, domes=False)
    return fn
def ground(top, bot, seed):
    def fn(p):
        p.grad_poly([(-200, 1170), (1300, 1170), (1300, 2300), (-200, 2300)], top, bot, 1170, 1800)
        rnd = random.Random(seed)
        for _ in range(40):
            x, y = rnd.uniform(-60, 1120), rnd.uniform(1200, 1880); p.line([(x - 50, y), (x + 50, y)], (0, 0, 0), 3, 35)
    return fn
def heap_front(p): key_heap(p, 540, 1330, 30, 305, spread=(430, 110), s=1.0)
def scar(p):
    p.line([(540 + u * .9, 1180 + v * .9) for u, v in CRACK], (60, 40, 28), 6, 200)
    for k in range(5): p.ell(200 + k * 170, 1186 + (k % 2) * 10, 60, 8, (90, 66, 46), 120)

def vault_warm(p): vault_arches(p, (92, 60, 44), (220, 170, 100), (255, 190, 100))
def vault_cool(p): vault_arches(p, (52, 44, 64), (170, 150, 200), (255, 200, 120))
def vault_chests(p):
    for cx, s, op in ((200, .8, False), (540, 1.0, True), (880, .8, False)): chest(p, cx, 1250 - (1 - s) * 60, s, open_=op)
    coins(p, 540, 1270, 40, 306)
    key_heap(p, 540, 1380, 22, 319, spread=(420, 70), s=.8)
def vault_lamp(p):
    lantern(p, 540, 980, 1.2)
    coins(p, 540, 1240, 60, 307, 18, 380)
    chest(p, 210, 1240, .7); chest(p, 870, 1240, .7)

def road_sky(p): p.sky([(0, (40, 30, 90)), (.24, (140, 90, 130)), (.4, (255, 176, 110)), (.47, (255, 214, 150)), (1, (90, 60, 40))]); clouds(p, 308, 160, 620, (255, 220, 180), 6, 100)
def road_near(p):
    p.grad_poly([(-200, 1100), (1300, 1100), (1300, 2300), (-200, 2300)], (170, 126, 86), (60, 38, 26), 1100, 1800)
    L, R = [], []
    for k in range(41):
        f = k / 40; y = lerp(1110, 2300, f ** 1.3); w = lerp(30, 520, f ** 1.4); L.append((540 - w, y)); R.append((540 + w, y))
    p.poly(L + R[::-1], (214, 176, 120), 200)
    for i, f in enumerate((.05, .16, .32, .55)):
        y = lerp(1110, 2300, f ** 1.3); w = lerp(30, 520, f ** 1.4) + 40 + 30 * f; h = lerp(120, 520, f)
        cols = [(196, 40, 50), (232, 180, 60)]
        banner(p, 540 - w, y, h, cols[i % 2], flip=-1); banner(p, 540 + w, y, h, cols[(i + 1) % 2])
    for k in range(70):
        rnd = random.Random(309 + k); f = rnd.uniform(0, .6); y = lerp(1110, 2300, f ** 1.3); w = lerp(30, 520, f ** 1.4)
        p.ell(540 + rnd.uniform(-w, w), y, 5 + f * 10, 3 + f * 5, (255, 220, 120), 200)

def night_sky(p): p.sky([(0, (6, 8, 30)), (.4, (16, 22, 60)), (.5, (30, 36, 80)), (1, (8, 10, 24))]); stars(p, 380, 310, 1000); moon(p, 780, 300, 58)
def night_wall(p):
    p.rect(-200, 1000, 1300, 2300, (54, 46, 60))
    for r in range(8):
        for c in range(-1, 12):
            x = c * 110 + (55 if r % 2 else 0); y = 1000 + r * 60; p.rect(x + 3, y + 3, x + 107, y + 57, (70, 60, 76))
    lantern(p, 540, 940, 1.0)

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 311, 900); moon(p, 820, 300, 56)
def end_ground(p): dunes(p, 1420, 30, (120, 90, 80), (20, 16, 20), 312)

DUSKPAL = dict(wall=(180, 120, 88), dark=(84, 48, 40), gold=(255, 196, 96), win=(255, 210, 130))
NIGHTPAL = dict(wall=(98, 82, 104), dark=(44, 34, 52), gold=(220, 180, 110), win=(255, 200, 120))
NOONPAL = dict(wall=(214, 176, 130), dark=(120, 84, 60), gold=(255, 214, 110), win=(70, 44, 30))

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[dusk_sky, far_city((70, 36, 40), (255, 190, 110)), ground((150, 96, 66), (40, 22, 18), 313), heap_front],
         fx=[(palace_fx, dict(base=1180, s=.86, **DUSKPAL)), 'dust'], cam='hold', bloom=.55,
         title=dict(text='His keys alone were too heavy for strong men.', hold=99, plain=True), no_caption=(0,),
         lines=['His keys alone were too heavy for strong men.']),
    dict(layers=[vault_warm, vault_chests], fx=['dust'], cam='in', bloom=.65,
         verse=dict(key='28:76', ar=(8, 18), en='And We gave him of treasures whose keys would burden a band of strong men', line=1, ar_size=66, y=560),
         lines=['Qarun was from the people of Musa, peace be upon him.', 'And We gave him of treasures whose keys would burden a band of strong men.']),
    dict(layers=[dusk_sky, far_city((60, 30, 40), (255, 200, 120)), ground((130, 84, 60), (34, 20, 16), 314)],
         fx=[(palace_fx, dict(base=1200, s=.7, glow=.4, **DUSKPAL)), 'twinkle'], cam='hold', bloom=.5,
         verse=dict(key='28:77', ar=(11, 16), en='And do good as Allah has done good to you', line=1, ar_size=72, y=560),
         lines=['But he tyrannized them. His people warned him:', 'And do good as Allah has done good to you.']),
    dict(layers=[vault_cool, vault_lamp], fx=['dust'], cam='in', bloom=.7,
         verse=dict(key='28:78', ar=(1, 6), en='I was only given it because of knowledge I have', line=1, ar_size=74, y=560),
         lines=['He said:', 'I was only given it because of knowledge I have.']),
    dict(layers=[road_sky, (lambda p: city(p, 1110, (120, 80, 70), 315, None, domes=False), .4), road_near], fx=['dust'], cam='in', bloom=.6,
         verse=dict(key='28:79', ar=(10, 16), en='Oh, would that we had like what was given to Qarun', line=2, ar_size=70, y=520),
         lines=['He came out before his people in his adornment.', 'Some said:', 'Oh, would that we had like what was given to Qarun.']),
    dict(layers=[night_sky, night_wall], fx=['twinkle'], cam='in', bloom=.7, pause=0.5,
         verse=dict(key='28:80', ar=(5, 12), en='The reward of Allah is better for he who believes and does righteousness', line=1, ar_size=68, y=540),
         lines=['Those given knowledge said:', 'The reward of Allah is better for he who believes and does righteousness.', 'Then it happened.']),
    dict(layers=[dusk_sky, far_city((60, 30, 40), None), ground((140, 90, 62), (36, 20, 16), 316)],
         fx=[(palace_fx, dict(base=1180, s=.86, glow=0, sink=(0, .42, .98), **DUSKPAL))], cam='hold', bloom=.45, pause=0.9,
         verse=dict(key='28:81', ar=(0, 4), en='And We caused the earth to swallow him and his home', line=0, ar_size=80, y=470),
         lines=['And We caused the earth to swallow him and his home.']),
    dict(layers=[morn_sky, far_city((150, 120, 104), None), ground((190, 150, 108), (70, 50, 36), 317), scar], fx=['dust'], cam='in', bloom=.6,
         verse=dict(key='28:82', ar=(15, 22), en='If not that Allah had conferred favor on us, He would have caused it to swallow us', line=1, ar_size=66, y=560),
         lines=['Those who had wished for his place said:', 'If not that Allah had conferred favor on us, He would have caused it to swallow us.']),
    dict(layers=[morn_sky, far_city((150, 120, 104), None), ground((196, 156, 112), (76, 54, 38), 318), scar], fx=['dust'], cam='hold', bloom=.7,
         lesson=dict(text='His wealth could not save him. Do good with what Allah gave you.', after=0, y=520, size=76), no_caption=(0,),
         lines=['His wealth could not save him. Do good with what Allah gave you.']),
    dict(layers=[end_sky, end_ground], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone who has been given much'), no_caption=(0,),
         lines=['Share this with someone who has been given much. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """His keys alone were too heavy for strong men. 🔑

Qarun was from the people of Musa (Moses), peace be upon him, but he tyrannized them. "And We gave him of treasures whose keys would burden a band of strong men." (Quran 28:76)

His people warned him: do not exult, "And do good as Allah has done good to you." (28:77) He answered: "I was only given it because of knowledge I have." (28:78)

He came out in his adornment, and some wished they had what he had (28:79). Those given knowledge said Allah's reward is better (28:80).

"And We caused the earth to swallow him and his home." (Quran 28:81)

His wealth could not save him. Do good with what Allah gave you.

📖 Sources: Quran 28:76–83 (Saheeh International)
Share this with someone who has been given much. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """What blessing has Allah given you that you can use to do good today? 🤍

Reference: Quran, Surah Al-Qasas 28:76–83 (Saheeh International translation)."""
