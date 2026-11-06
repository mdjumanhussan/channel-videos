"""Story 20: Musa and the wise servant. Source: Quran 18:60-82 (Saheeh International).
No people are drawn: no Musa, no servant, no boy, no parents, no king, no orphans, no figure of any kind, and nothing stands for Allah.
Only ships, the sea, a rock where two seas meet, an empty road, a town, a wall, a small house, a chest, the sky and light.
Facts used and where they are: Musa travels to the junction of the two seas (18:60); a servant Allah gave mercy and taught knowledge
(18:65); Musa asks to follow and learn (18:66); "Indeed, with me you will never be able to have patience" (18:67); the servant tears the
ship and Musa objects (18:71); they meet a boy, the servant kills him, and Musa objects (18:74); a town refuses them hospitality, the
servant restores a wall about to collapse, and Musa says he could have taken a payment (18:77); the ship belonged to poor people and a
king seized every good ship by force (18:79); the boy's parents were believers and it was feared he would overburden them by
transgression and disbelief (18:80); their Lord was to give them one better in purity and nearer to mercy (18:81); the wall belonged to
two orphans with a treasure beneath it, a mercy from your Lord (18:82); "And I did it not of my own accord" (18:82).
Not used: the name Khidr (the Quran does not give it; 18:71 etc. carry it only as a translator's bracket, so no card quotes those
words), the fish, any detail of how the boy died, the boy's age, the name of the town, any name of the king, the replacement child's
sex, Israiliyyat. Told as ONE Reel, not two: the boy's death must never sit a day without its explanation and "not of my own accord".
Improvement tried today: an explicit comment question high in the caption ("Which of the three would you have questioned first?
Comment below"), mirrored in the first comment. Reason: the page's "one word" Reel asked "Do you know what that word was? Comment
below" and reached 4,517 views; Dar al-Arqam asked too and stayed at 264, so this is a test, not a rule (playbook 2026-11-06).
Also kept: statement hook = headline, nothing else on frame 1 (caption hidden); live motion on the words that matter (the hull tears,
the wall rebuilds stone by stone, the ground opens on "treasure", deep hit); second loop ("Then came the answers.", 0.5 s pause);
rhyming loop ending (same ship, morning); speed 1.1; lesson card; specific send-to end card; CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  20'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Musa and the Servant Who Tore Open the Ship'
HITS = [(7, 0, 1.0), (8, 1, 0.0)]      # 'treasure'; then 'not of my own accord'

# ---------------------------------------------------------------- the ship (a cached sprite, redrawn over the sea every frame)
_ships = {}
def ship_sprite(s=1.0, hull=(112, 66, 38), dark=(58, 32, 20), sail=(226, 204, 170), flag=None):
    k = (s, hull, dark, sail, flag)
    if k in _ships: return _ships[k]
    Q = 2; im = Image.new('RGBA', (1000 * Q, 820 * Q), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def sc(pts): return [(x * Q, y * Q) for x, y in pts]
    # mast, yard, furled sail, rigging. Nobody on deck.
    d.polygon(sc([(492, 130), (508, 130), (514, 560), (486, 560)]), fill=dark)
    d.line(sc([(190, 250), (810, 170)]), fill=dark, width=12 * Q)
    furl = [(200, 252), (500, 208), (800, 172), (800, 200), (640, 232), (500, 262), (360, 268), (210, 282)]
    d.polygon(sc(furl), fill=sail)
    for x in range(250, 790, 70): d.line(sc([(x, 252 - (x - 200) * .13), (x + 8, 282 - (x - 200) * .13)]), fill=lc(sail, (0, 0, 0), .3), width=3 * Q)
    for a, b in (((500, 136), (120, 470)), ((500, 136), (880, 450))): d.line(sc([a, b]), fill=dark, width=3 * Q)
    if flag:
        d.polygon(sc([(500, 130), (500, 70), (610, 100)]), fill=flag)
    # hull: a long curved trader, high stem and stern
    top = [(60 + 880 * (i / 30), 520 + 74 * ((i / 30 - .5) * 2) ** 2 * -1.0) for i in range(31)]
    keel = [(880 - 660 * (i / 30), 690 + 22 * math.sin(math.pi * i / 30)) for i in range(31)]
    d.polygon(sc(top + keel), fill=hull)
    for k2 in range(1, 5):
        f = k2 / 5; pts = [(lerp(top[i][0], keel[30 - i][0], f), lerp(top[i][1], keel[30 - i][1], f)) for i in range(31)]
        d.line(sc(pts), fill=dark, width=3 * Q)
    d.line(sc(top), fill=lc(hull, (255, 226, 180), .4), width=9 * Q)
    d.polygon(sc([(60, 446), (36, 400), (92, 462)]), fill=dark); d.polygon(sc([(940, 446), (966, 396), (908, 462)]), fill=dark)
    im = im.resize((int(1000 * s), int(820 * s)), Image.LANCZOS)
    _ships[k] = im
    return im

GASH = [(-92, -10), (-58, -24), (-40, -6), (-8, -30), (20, -8), (52, -26), (88, -6), (70, 12), (36, 2), (10, 20), (-20, 4), (-52, 14)]
def ship_fx(img, tt, info, x=540, y=1060, s=.9, tear=None, q=1.0, foam=(236, 240, 232), sway=1.0, **kw):
    """The ship rides the swell. A jagged tear in the hull opens over tear=(line, f0, f1). No sailors, nobody on deck."""
    if tear:
        a, b = info['lines'][tear[0]]; q = ease((tt - lerp(a, b, tear[1])) / max(.05, (b - a) * (tear[2] - tear[1])))
    spr = ship_sprite(s, **kw)
    bob = math.sin(tt * 1.3) * 10 * sway; roll = math.sin(tt * .9 + .6) * 1.6 * sway
    im = spr
    if q > .01:
        im = spr.copy(); d = ImageDraw.Draw(im)
        cx, cy = 300 * s, 610 * s; k = (.15 + .85 * q) * 1.5 * s
        d.polygon([(cx + u * k, cy + v * k * q) for u, v in GASH], fill=(10, 8, 12, 255))
        for u, v in GASH[1:7:2]:
            d.line([(cx + u * k, cy + v * k * q), (cx + u * k * 1.1, cy + (v - 16) * k * q)], fill=(216, 176, 120, 255), width=max(2, int(5 * s)))
    r = im.rotate(roll, Image.BICUBIC, expand=False, center=(im.width / 2, im.height * .8))
    img.alpha_composite(r, (int(x - r.width / 2), int(y - r.height * .84 + bob)))
    # water in front of the hull
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k2 in range(4):
        yy = y + 8 + k2 * 26
        pts = [(xx, yy + math.sin(xx * .012 + tt * (1.5 + k2 * .2) + k2) * (6 + 3 * k2)) for xx in range(-20, W + 40, 30)]
        d.line(pts, fill=foam + (150 - k2 * 26,), width=3 + k2)
    img.alpha_composite(lay)

# ---------------------------------------------------------------- the wall
def _stones():
    rnd = random.Random(20); out = []; rows, cols = 8, 9
    for r in range(rows):
        for c in range(cols + (r % 2)):
            x = 110 + (c - (.5 if r % 2 else 0)) * 96; y = 880 - (r + 1) * 46
            out.append(dict(x=max(110, x), x1=min(970, x + 92), y=y, r=r, tone=rnd.uniform(0, 1), th=rnd.uniform(0, 1), lost=(r >= 3 and rnd.random() < (r - 1) / 7)))
    return out
STONES = _stones()

def wall_fx(img, tt, info, repair=None, base=1.0, reveal=None, stone=(182, 148, 110), dark=(84, 62, 48), earth=(66, 44, 32), earth_d=(30, 20, 18)):
    """Stones of a wall, leaning and gapped at q=0, whole at q=1. repair=(line,f0,f1): stones lift back as it is spoken.
    reveal=(line,f0,f1): the ground below opens like a cut-away and shows the closed chest that was under the wall (18:82)."""
    q = base
    if repair:
        a, b = info['lines'][repair[0]]; q = ease((tt - lerp(a, b, repair[1])) / max(.05, (b - a) * (repair[2] - repair[1])))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for s in STONES:
        lean = (1 - q) * s['r'] * 13                                  # upper courses lean out before the repair
        c = lc(dark, stone, .45 + .55 * s['tone'])
        if s['lost']:
            g = clamp((q - s['th'] * .7) / .3)                        # a missing stone drops into place
            if g <= 0: continue
            off = -(1 - ease(g)) * 170
            d.rectangle((s['x'] + lean, s['y'] + off, s['x1'] + lean - 4, s['y'] + 42 + off), fill=c + (int(255 * ease(g)),), outline=dark + (255,))
        else:
            d.rectangle((s['x'] + lean, s['y'], s['x1'] + lean - 4, s['y'] + 42), fill=c + (255,), outline=dark + (255,))
    img.alpha_composite(lay)
    if reveal:
        a, b = info['lines'][reveal[0]]; g = ease((tt - lerp(a, b, reveal[1])) / max(.05, (b - a) * (reveal[2] - reveal[1])))
        if g > 0:
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            A = int(255 * g)
            d.polygon([(110, 884), (970, 884), (880, 1060), (200, 1060)], fill=earth_d + (A,))
            d.line([(110, 884), (200, 1060), (880, 1060), (970, 884)], fill=earth + (A,), width=8)
            cx, cy = 540, 985
            d.rectangle((cx - 120, cy - 34, cx + 120, cy + 56), fill=(112, 70, 38, A), outline=(52, 30, 18, A))
            d.rectangle((cx - 132, cy - 68, cx + 132, cy - 30), fill=(146, 96, 54, A), outline=(52, 30, 18, A))
            for dx in (-74, 74): d.rectangle((cx + dx - 12, cy - 68, cx + dx + 12, cy + 56), fill=(214, 170, 84, A))
            d.rectangle((cx - 18, cy - 40, cx + 18, cy - 6), fill=(236, 196, 104, A))
            glow = lay.filter(ImageFilter.GaussianBlur(20)); img.alpha_composite(glow); img.alpha_composite(lay)

# ---------------------------------------------------------------- layer painters
def sea_scene(stops, top, c1, c2, seed, glint=(255, 214, 160), sunat=None):
    def sk(p):
        p.sky(stops)
        if sunat: sun(p, sunat[0], sunat[1], sunat[2], sunat[3])
        clouds(p, seed, 180, 720, (255, 226, 200), 5, 70)
    def wa(p): sea(p, top, c1, c2, seed + 1, glint)
    return [sk, wa]

DUSK = [(0, (14, 22, 60)), (.26, (70, 54, 104)), (.42, (226, 112, 84)), (.48, (255, 182, 110)), (.56, (120, 80, 80)), (1, (10, 20, 34))]
NOON = [(0, (36, 104, 176)), (.3, (116, 180, 220)), (.46, (232, 234, 214)), (.52, (200, 220, 214)), (1, (30, 90, 120))]
MORN = [(0, (70, 140, 200)), (.28, (160, 204, 224)), (.44, (252, 226, 184)), (.5, (255, 238, 200)), (1, (40, 110, 130))]

def two_seas_sky(p):
    p.sky([(0, (30, 44, 104)), (.24, (120, 110, 160)), (.42, (250, 180, 130)), (.5, (255, 226, 176)), (1, (60, 70, 90))])
    clouds(p, 211, 200, 700, (255, 220, 190), 6, 80)
def two_seas_water(p):
    p.grad_poly([(-200, 900), (1300, 900), (1300, 2300), (-200, 2300)], (70, 128, 150), (12, 58, 92), 900, 1800)
    p.blur_shape(lambda t: t.poly([(540, 900), (1300, 900), (1300, 2300), (540, 2300)], (24, 118, 112), 120), 40)   # the second sea, a different green
    for k in range(40):
        f = (k / 40) ** 1.6; y = 900 + f * 900
        for sx in (-1, 1):
            x = 540 + sx * (100 + (k * 37 % 500)); p.line([(x, y), (x + 40 + k * 4, y)], (255, 244, 220), 1 + k * .06, 60 + k)
def two_seas_rock(p):
    rock = [(300, 1400), (360, 1310), (450, 1262), (560, 1250), (650, 1280), (740, 1340), (790, 1400), (840, 1460), (240, 1460)]
    p.poly(rock, (70, 58, 56))
    p.poly([(360, 1310), (450, 1262), (560, 1250), (520, 1340), (420, 1390)], (128, 106, 96))
    p.ell(540, 1466, 330, 22, (240, 244, 230), 110)

def road_sky(p):
    p.sky([(0, (10, 8, 26)), (.3, (40, 20, 52)), (.46, (120, 50, 70)), (.52, (170, 80, 76)), (1, (16, 10, 20))])
    clouds(p, 212, 180, 760, (80, 40, 70), 6, 90)
def road_mid(p): mountains(p, 1050, 150, (28, 16, 34), 213, (90, 50, 80), 5)
def road_near(p):
    dunes(p, 1040, 28, (60, 34, 50), (14, 8, 16), 214)
    L, R = [], []
    for k in range(41):
        f = k / 40; y = lerp(1030, 2300, f ** 1.3); c = 560 + math.sin(f * 6) * lerp(20, 120, f); w = lerp(8, 300, f ** 1.5)
        L.append((c - w, y)); R.append((c + w, y))
    p.poly(L + R[::-1], (118, 84, 90), 150)
    tree(p, 860, 1090, 300, (20, 12, 18), (24, 14, 22), 215)

def town_sky(p):
    p.sky([(0, (18, 16, 58)), (.26, (84, 50, 96)), (.4, (214, 100, 74)), (.46, (246, 150, 88)), (1, (30, 16, 18))])
    clouds(p, 216, 160, 560, (250, 170, 130), 5, 70)
def town_mid(p):
    city(p, 880, (44, 22, 34), 217, (255, 180, 90), domes=False)
def town_near(p):
    p.grad_poly([(-200, 876), (1300, 876), (1300, 2300), (-200, 2300)], (112, 76, 56), (30, 18, 16), 876, 1700)
    rnd = random.Random(218)
    for _ in range(30):
        x, y = rnd.uniform(-60, 1120), rnd.uniform(1080, 1880)
        p.line([(x - 60, y), (x + 60, y)], (0, 0, 0), 3, 40)

def harbour_sky(p):
    p.sky([(0, (24, 8, 22)), (.3, (92, 22, 38)), (.44, (214, 72, 50)), (.48, (252, 130, 66)), (1, (20, 10, 16))])
    clouds(p, 219, 200, 760, (120, 40, 50), 6, 90)
def harbour_water(p): sea(p, 900, (150, 62, 50), (14, 14, 26), 220, (255, 170, 110))

def house_sky(p):
    p.sky([(0, (14, 16, 56)), (.3, (50, 56, 116)), (.46, (150, 120, 150)), (.52, (252, 190, 140)), (1, (28, 22, 34))])
    stars(p, 160, 221, 640); moon(p, 820, 300, 56)
def house_mid(p): mountains(p, 1000, 120, (46, 44, 80), 222, (130, 120, 150), 4)
def house_near(p):
    dunes(p, 990, 22, (92, 74, 84), (26, 20, 28), 223)
    w, y0, cx = 170, 780, 540
    p.poly([(cx - w, y0), (cx + w, y0), (cx + w, y0 + 220), (cx - w, y0 + 220)], (196, 164, 130))
    p.rect(cx - w - 14, y0 - 22, cx + w + 14, y0 + 6, (140, 112, 92))
    p.rect(cx - 34, y0 + 90, cx + 34, y0 + 220, (72, 48, 36))
    for dx in (-104, 104):
        p.glow(cx + dx, y0 + 80, 170, (255, 200, 110), .55)
        p.rect(cx + dx - 28, y0 + 56, cx + dx + 28, y0 + 118, (255, 214, 130))

def wall_sky(p):
    p.sky([(0, (40, 92, 164)), (.26, (130, 180, 214)), (.4, (250, 226, 180)), (.46, (255, 236, 196)), (1, (60, 40, 30))])
    clouds(p, 224, 150, 520, (255, 246, 226), 5, 90)
def wall_mid(p): city(p, 880, (140, 112, 96), 225, None, domes=False)

def night_sky(p):
    p.sky([(0, (4, 8, 30)), (.4, (12, 22, 60)), (.46, (24, 40, 84)), (1, (6, 12, 30))])
    stars(p, 420, 226, 900); moon(p, 780, 280, 60)
def night_water(p): sea(p, 900, (30, 54, 100), (4, 12, 30), 227, (190, 210, 240))

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 228, 900); moon(p, 820, 300, 56)
def end_water(p): sea(p, 1410, (150, 110, 96), (12, 20, 40), 229, (250, 200, 150))

SHIPDUSK = dict(hull=(70, 42, 34), dark=(26, 16, 18), sail=(180, 130, 120))
FLEET = dict(hull=(50, 18, 22), dark=(16, 6, 10), sail=(100, 40, 44), flag=(20, 6, 10))

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=sea_scene(DUSK, 900, (150, 96, 96), (10, 26, 50), 240), fx=[(ship_fx, dict(y=1290, s=.82, q=1.0, **SHIPDUSK))], cam='hold', bloom=.5,
         title=dict(text='He tore open a ship of poor people.', hold=99, plain=True), no_caption=(0,),
         lines=['He tore open a ship of poor people.']),
    dict(layers=[two_seas_sky, two_seas_water, two_seas_rock], fx=['twinkle'], cam='in', bloom=.65,
         verse=dict(key='18:67', ar=(1, 6), en='Indeed, with me you will never be able to have patience', line=2, ar_size=72, y=500),
         lines=['Musa, peace be upon him, asked to follow a servant Allah had taught.', 'He answered:', 'Indeed, with me you will never be able to have patience.']),
    dict(layers=sea_scene(NOON, 900, (110, 186, 196), (14, 84, 120), 242, (255, 255, 240)), fx=[(ship_fx, dict(y=1290, s=.82, tear=(0, .62, .9), foam=(255, 255, 250)))], cam='hold', bloom=.6,
         verse=dict(key='18:71', ar=(8, 11), en='Have you torn it open to drown its people?', line=2, ar_size=74, y=450),
         lines=['They boarded a ship, and he tore it open.', 'Musa said:', 'Have you torn it open to drown its people?']),
    dict(layers=[road_sky, road_mid, road_near], fx=['dust'], cam='in', bloom=.4,
         verse=dict(key='18:74', ar=(7, 12), en='Have you killed a pure soul for other than [having killed] a soul?', line=2, ar_size=74, y=520),
         lines=['They met a boy, and he killed him.', 'Musa said:', 'Have you killed a pure soul for other than having killed a soul?']),
    dict(layers=[town_sky, town_mid, town_near], fx=[(wall_fx, dict(repair=(0, .45, 1.0)))], cam='hold', bloom=.5, pause=0.5,
         lines=['A town refused them food. He rebuilt its falling wall.', 'Musa said he could have taken payment.', 'Then came the answers.']),
    dict(layers=[harbour_sky, harbour_water],
         fx=[(ship_fx, dict(x=210, y=930, s=.4, q=0, sway=.4, **FLEET)), (ship_fx, dict(x=560, y=925, s=.46, q=0, sway=.4, **FLEET)), (ship_fx, dict(x=900, y=930, s=.4, q=0, sway=.4, **FLEET)), (ship_fx, dict(x=540, y=1330, s=.6, q=1.0, foam=(255, 200, 170), **SHIPDUSK))],
         cam='hold', bloom=.45,
         lines=['A king was seizing every good ship by force.', 'The damage saved it.']),
    dict(layers=[house_sky, house_mid, house_near], fx=['twinkle'], cam='in', bloom=.75,
         lines=["The boy's parents were believers.", 'It was feared he would burden them with disbelief.', 'Their Lord was to give them one better.']),
    dict(layers=[wall_sky, wall_mid, town_near], fx=[(wall_fx, dict(base=1.0, reveal=(0, .32, .62)))], cam='hold', bloom=.6,
         lines=['Under the wall lay a treasure for two orphans.', 'A mercy from your Lord.']),
    dict(layers=[night_sky, night_water], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='18:82', ar=(24, 28), en='And I did it not of my own accord', line=1, ar_size=68, y=600),
         lines=['He said:', 'And I did it not of my own accord.']),
    dict(layers=sea_scene(MORN, 900, (170, 214, 214), (24, 100, 130), 244, (255, 255, 240)), fx=[(ship_fx, dict(y=1290, s=.82, q=1.0, foam=(255, 255, 250)))], cam='hold', bloom=.7,
         lesson=dict(text='We see the moment. Allah knows what comes after.', after=0, y=520, size=80), no_caption=(0,),
         lines=['We see the moment. Allah knows what comes after.']),
    dict(layers=[end_sky, end_water], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with', line2='someone asking why'), no_caption=(0,),
         lines=['Share this with someone asking why. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """He tore open a ship of poor people. 🌊
Which of the three would you have questioned first? Comment below 👇

Musa (Moses), peace be upon him, asked to follow a servant Allah had taught. He was told: "Indeed, with me you will never be able to have patience." (Quran 18:67)

The servant tore open a ship (18:71). He killed a boy (18:74). He rebuilt a falling wall in a town that refused them food (18:77). Each time, Musa spoke up.

Then came the answers. A king was seizing every good ship by force (18:79). The boy's parents were believers, and it was feared he would overburden them by transgression and disbelief (18:80–81). Under the wall lay a treasure for two orphans (18:82).

"And I did it not of my own accord." (Quran 18:82)

We see the moment. Allah knows what comes after.

📖 Sources: Quran 18:60–82 (Saheeh International)
Share this with someone asking why. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """Which of the three would you have questioned first: the ship, the boy or the wall? Tell us below 🤍

Reference: Quran, Surah Al-Kahf 18:60–82 (Saheeh International translation)."""
