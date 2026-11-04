"""Story 18: Musa (Moses) and the magicians of Pharaoh. Sources: Quran 7:103-126, 20:56-73, 26:34-51, 10:79-82 (Saheeh International).
No people are drawn: no Musa, no Harun, no Pharaoh, no magicians, no crowd, no figure of any kind, and nothing stands for Allah.
Only a sand arena, Pharaoh's halls (building only), ropes, staffs, one serpent, palm trees, the sky and light.
Facts used and where they are: Pharaoh called the signs magic (20:57, 7:109 his chiefs too); every learned magician was brought
(7:112, 10:79); they said "Indeed for us is a reward if we are the predominant" (7:113, 26:41); the festival day (20:59); they
threw their ropes and staffs (26:44); these seemed to him to be moving like snakes (20:66); he sensed apprehension (20:67);
"Fear not. Indeed, it is you who are superior" (20:68); "Throw your staff," and at once it devoured what they were falsifying
(7:117); they fell in prostration and believed (20:70); Pharaoh's threat (20:71, 7:124); "Never will we prefer you over what has
come to us of clear proofs" (20:72).
Not used: any number of magicians, any magician's name, gold (the Quran says only "a reward"), the crowd drawn on screen, whether
the threat was carried out (the Quran does not say here, so the narration does not either), the white hand (7:108).
The ropes moving is what they "seemed" to do, and the narration says "seemed". The serpent is an object of the miracle, not a
person; it swallows the ropes as 7:117 is spoken. The ropes are gone from every later scene, because they were devoured.
Improvement tried today: the peak is shown happening, not told over a still painting. Ropes and staffs writhe live, redrawn every
frame, and when 7:117 reaches "devoured" the serpent grows across the sand and the ropes vanish in its path, with the deep hit
on that word. Reason: all 17 Reels so far use painted stills with a slow camera at the peak; a pattern-break guide lists "a sudden
shift from explanation to demonstration" as a retention move (playbook 2026-11-04). New engine hook: an fx entry may be a function.
Also kept: plain headline = spoken hook with nothing else on frame 1 (caption hidden), live motion from frame 1, second loop
("What would happen?") with a 0.5 s pause, rhyming loop ending (same arena as frame 1, ropes gone, evening light), speed 1.1,
lesson card, specific send-to end card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  18'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Musa and the Magicians of Pharaoh'
HITS = [(5, 0, 3.69), (8, 1, 0.0)]      # the word 'devoured' in 7:117; then 20:72

# ---------------------------------------------------------------- live ropes and the serpent (screen coords, redrawn every frame)
ROPE, ROPE_D = (206, 164, 104), (120, 86, 50)
STAFF, STAFF_D = (112, 72, 40), (64, 40, 22)

def _items():
    rnd = random.Random(18); out = []
    for i in range(15):
        row = i / 14
        out.append(dict(staff=i % 3 == 2, x=rnd.uniform(170, 930), y=lerp(0, 430, row) + rnd.uniform(-20, 20), L=rnd.uniform(240, 400) * (.7 + .5 * row),
                        ang=rnd.uniform(-.5, .5), ph=rnd.uniform(0, 6.3), sp=rnd.uniform(2.2, 3.6), s=.7 + .6 * row))
    return out
ITEMS = _items()

def _rope_pts(it, y0, t, amp):
    n = 26; pts = []; ca, sa = math.cos(it['ang']), math.sin(it['ang']) * .55
    for k in range(n + 1):
        f = k / n; d = (f - .5) * it['L']; w = math.sin(f * 3.14) ** .5
        off = (amp * (26 if it['staff'] else 60) * it['s']) * w * math.sin(f * (5 if it['staff'] else 9) + t * it['sp'] + it['ph'])
        pts.append((it['x'] + d * ca - off * sa, y0 + it['y'] + d * sa + off * ca * .7))
    return pts

def live_ropes(img, tt, info, y0=1050, amp=1.0, eat=None):
    """Ropes and staffs that seem to move. eat=(line, f0, f1): from fraction f0 to f1 of that spoken line a serpent grows across the sand
    from the left, and every rope behind its head is gone."""
    hx = None
    if eat:
        a, b = info['lines'][eat[0]]; q = (tt - lerp(a, b, eat[1])) / max(.05, (b - a) * (eat[2] - eat[1]))
        if q > 0: hx = lerp(110, 985, ease(min(q, 1)))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for it in ITEMS:
        if hx is not None and it['x'] < hx: continue
        pts = _rope_pts(it, y0, tt, amp); w = int((22 if it['staff'] else 15) * it['s'])
        col, dk = (STAFF, STAFF_D) if it['staff'] else (ROPE, ROPE_D)
        d.line([(x + 7, y + 14) for x, y in pts], fill=(0, 0, 0, 80), width=w, joint='curve')
        d.line(pts, fill=dk + (255,), width=w + 5, joint='curve'); d.line(pts, fill=col + (255,), width=w, joint='curve')
        if not it['staff']:
            for k in range(1, len(pts) - 1, 2):
                (ax, ay), (bx, by) = pts[k], pts[k + 1]
                d.line([(ax, ay - w * .4), (bx, by + w * .4)], fill=dk + (200,), width=max(2, w // 4))
    if hx is not None:
        cy = y0 + 215; n = 90; x0 = 70; pts = []
        for i in range(n + 1):
            f = i / n; x = lerp(x0, hx, f); pts.append((x, cy + math.sin(f * 10.5 * (hx - x0) / 900 - tt * 5) * 92 * (.35 + .65 * f)))
        L, R = [], []
        for i, (x, y) in enumerate(pts):
            f = i / n; ax, ay = pts[max(0, i - 1)]; bx, by = pts[min(n, i + 1)]; dx, dy = bx - ax, by - ay; m = math.hypot(dx, dy) or 1
            w = 8 + 44 * f ** .55
            L.append((x - dy / m * w, y + dx / m * w)); R.append((x + dy / m * w, y - dx / m * w))
        body = L + R[::-1]
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).polygon(body, fill=(255, 190, 90, 200))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(26)))
        d.polygon([(x + 8, y + 18) for x, y in body], fill=(0, 0, 0, 90)); d.polygon(body, fill=(70, 46, 28, 255))
        for i in range(6, n - 2, 5):
            x, y = pts[i]; r = 4 + 13 * (i / n) ** .6; d.ellipse((x - r, y - r, x + r, y + r), fill=(226, 180, 96, 235))
        hxx, hy = pts[-1]
        d.ellipse((hxx - 42, hy - 46, hxx + 86, hy + 46), fill=(70, 46, 28, 255)); d.ellipse((hxx + 30, hy - 26, hxx + 46, hy - 10), fill=(250, 226, 130, 255))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(.8)))

# ---------------------------------------------------------------- small scenery helpers
def halls(p, cx, base, s, col, lights=None):
    """Grand columned halls of Pharaoh. Building only."""
    dark = lc(col, (0, 0, 0), .35)
    for k in range(5): p.rect(cx - (420 - k * 18) * s, base - k * 16 * s, cx + (420 - k * 18) * s, base - (k - 1) * 16 * s, lc(col, (255, 255, 255), .05 * k))
    top = base - 460 * s
    p.rect(cx - 380 * s, top, cx + 380 * s, base - 80 * s, dark)
    for i in range(9):
        x = cx - 340 * s + i * 85 * s
        p.rect(x - 20 * s, top + 30 * s, x + 20 * s, base - 80 * s, col)
        p.poly([(x - 30 * s, top + 30 * s), (x + 30 * s, top + 30 * s), (x + 20 * s, top + 60 * s), (x - 20 * s, top + 60 * s)], lc(col, (255, 255, 255), .15))
        if lights and i < 8: p.glow(x + 42 * s, base - 200 * s, 60 * s, lights, .35)
    p.rect(cx - 410 * s, top - 30 * s, cx + 410 * s, top + 34 * s, col)

def colonnade(p, wall, col, light):
    """Looking down a long hall toward one lit doorway. Empty: no one is in it."""
    p.rect(-100, -100, 1200, 2300, wall)
    p.glow(540, 880, 560, light, .8)
    p.rect(470, 650, 610, 1100, lc(light, (255, 255, 255), .4)); p.ell(540, 650, 70, 70, lc(light, (255, 255, 255), .4))
    p.poly([(-100, 2300), (470, 1100), (610, 1100), (1200, 2300)], lc(wall, light, .35))
    for k in range(6):
        f = (k / 5) ** 1.7; xo = lerp(130, 520, f); y1 = lerp(1125, 1800, f); h = lerp(620, 2200, f); w = lerp(18, 110, f); c = lc(lc(col, light, .3), col, f)
        for sx in (-1, 1):
            x = 540 + sx * xo; p.rect(x - w, y1 - h, x + w, y1, c)
            p.rect(x - w * 1.35, y1 - w * .7, x + w * 1.35, y1, lc(c, (255, 255, 255), .12))

# ---------------------------------------------------------------- layer painters
def arena(sky_stops, hall, top, bot, light=None):
    def sky_l(p):
        p.sky(sky_stops)
        clouds(p, 181, 240, 640, (255, 250, 240), 5, 90)
    def mid_l(p):
        if light: p.glow(540, 940, 620, light, .6)
        pyramids(p, 1010, lc(hall, (255, 220, 170), .35), lc(hall, (0, 0, 0), .15), 182)
        halls(p, 540, 1040, .86, hall)
    def near_l(p):
        dunes(p, 1040, 16, top, bot, 183)
        rnd = random.Random(184)
        for _ in range(40):
            x, y = rnd.uniform(-100, 1180), rnd.uniform(1090, 1900)
            p.line([(x - 80, y), (x, y + rnd.uniform(-4, 4)), (x + 80, y)], lc(top, (60, 30, 10), .45), 3, 70)
    return [sky_l, mid_l, near_l]

DAY = [(0, (40, 132, 176)), (.3, (112, 190, 204)), (.5, (232, 228, 196)), (.56, (250, 226, 176)), (1, (150, 110, 70))]
AMBER = [(0, (70, 74, 96)), (.3, (172, 130, 92)), (.5, (240, 180, 104)), (.56, (232, 150, 80)), (1, (90, 58, 40))]
DIM = [(0, (28, 44, 74)), (.3, (86, 88, 112)), (.5, (200, 150, 112)), (.56, (190, 120, 84)), (1, (60, 40, 34))]
EVE = [(0, (44, 54, 112)), (.28, (150, 104, 138)), (.46, (252, 170, 110)), (.56, (255, 206, 130)), (1, (130, 84, 56))]

def rays_top(p): rays(p, 540, -200, (255, 244, 210), n=11, spread=60, length=2300, width=8, a=.26, angle=90, seed=185)

def court_sky(p):
    p.sky([(0, (64, 150, 186)), (.45, (170, 212, 206)), (.6, (250, 226, 176)), (1, (120, 90, 60))])
def court_mid(p): pyramids(p, 1330, (214, 164, 104), (150, 106, 66), 12)
def court_near(p):
    p.rect(-100, 1380, 1200, 2300, (196, 150, 96))
    halls(p, 540, 1640, 1.08, (176, 130, 84))

def hall_l(p): colonnade(p, (30, 20, 26), (58, 38, 34), (255, 196, 110))

def empty_sky(p):
    p.sky([(0, (26, 84, 126)), (.36, (44, 118, 150)), (.5, (170, 196, 186)), (.57, (255, 232, 180)), (1, (170, 126, 80))])
def empty_near(p):
    mountains(p, 1050, 170, (196, 160, 124), 71, (255, 236, 200), 5)
    dunes(p, 1050, 14, (240, 200, 140), (170, 124, 80), 183)

def threat_sky(p):
    p.sky([(0, (24, 6, 22)), (.45, (102, 20, 40)), (.68, (204, 62, 44)), (1, (32, 8, 16))])
    cloud_bank(p, 320, (72, 16, 36), (34, 8, 20), 81, 70, 220)
def threat_near(p):
    p.rect(-100, 1380, 1200, 2300, (24, 8, 14))
    halls(p, 540, 1620, 1.0, (66, 22, 30), (255, 120, 60))

def palm_sky(p):
    p.sky([(0, (10, 14, 48)), (.4, (40, 40, 98)), (.62, (150, 86, 118)), (.72, (250, 150, 96)), (1, (30, 18, 22))])
    stars(p, 200, 91, 900)
def palm_near(p):
    dunes(p, 1500, 26, (54, 34, 42), (16, 10, 14), 92)
    for x, b, h, ln in ((230, 1600, 640, -.05), (600, 1560, 520, .04), (880, 1620, 640, .07)): palm(p, x, b, h, (12, 8, 14), ln)

def end_sky(p):
    p.sky([(0, (8, 12, 40)), (.45, (26, 44, 92)), (.7, (72, 100, 136)), (.82, (232, 170, 110)), (1, (26, 18, 22))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): pyramids(p, 1420, (40, 34, 58), (22, 18, 36), 102)
def end_near(p): dunes(p, 1430, 30, (52, 40, 48), (16, 12, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=arena(DAY, (168, 124, 84), (232, 190, 130), (168, 122, 78)), fx=[(live_ropes, dict(y0=1190, amp=.55)), 'dust'], cam='hold', bloom=.45,
         title=dict(text='They came to defeat Musa. Then they fell in prostration. Why?', hold=99, plain=True), no_caption=(0,),
         lines=['They came to defeat Musa. Then they fell in prostration. Why?']),
    dict(layers=[court_sky, court_mid, court_near], fx=['dust'], cam='up',
         lines=['Pharaoh called the signs of Musa, peace be upon him, magic.', 'He brought every learned magician.']),
    dict(layers=[(hall_l, .6)], fx=['dust'], cam='in', bloom=.75,
         verse=dict(key='7:113', ar=(4, 11), en='Indeed for us is a reward if we are the predominant', line=1, ar_size=74, y=470),
         lines=['They asked for one thing:', 'Indeed for us is a reward if we are the predominant.']),
    dict(layers=arena(AMBER, (130, 88, 60), (216, 164, 104), (130, 88, 56)), fx=[(live_ropes, dict(y0=1000, amp=1.0)), 'dust'], cam='hold', pause=0.5,
         lines=['On the festival day, they threw their ropes and staffs.', 'They seemed to move like snakes.', 'Musa felt apprehension. What would happen?']),
    dict(layers=arena(DIM, (84, 60, 56), (168, 122, 86), (84, 58, 44)) + [rays_top], fx=[(live_ropes, dict(y0=1040, amp=1.0))], cam='hold', bloom=.7,
         verse=dict(key='20:68', ar=(1, 6), en='Fear not. Indeed, it is you who are superior', line=1, ar_size=78, y=520),
         lines=['Allah said:', 'Fear not. Indeed, it is you who are superior.']),
    dict(layers=arena(AMBER, (130, 88, 60), (216, 164, 104), (130, 88, 56)), fx=[(live_ropes, dict(y0=1040, amp=1.0, eat=(0, .62, .97)))], cam='hold', bloom=.6,
         verse=dict(key='7:117', ar_size=66, y=500, line=0),
         lines=['And We inspired to Moses, Throw your staff, and at once it devoured what they were falsifying.']),
    dict(layers=[empty_sky, rays_top, empty_near], fx=['dust'], cam='up', bloom=.8,
         verse=dict(key='20:70', ar=(4, 8), en='We have believed in the Lord of Aaron and Moses', line=1, ar_size=78, y=560),
         lines=['So the magicians fell down in prostration. They said:', 'We have believed in the Lord of Aaron and Moses.']),
    dict(layers=[threat_sky, threat_near], fx=['embers'], cam='in', pause=0.5,
         lines=['Pharaoh threatened to cut off their hands and feet, and crucify them.']),
    dict(layers=[palm_sky, palm_near], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='20:72', ar=(1, 8), en='Never will we prefer you over what has come to us of clear proofs', line=1, ar_size=74, y=560),
         lines=['They said:', 'Never will we prefer you over what has come to us of clear proofs.']),
    dict(layers=arena(EVE, (150, 96, 72), (236, 176, 116), (146, 96, 66), (255, 196, 120)), fx=['dust'], cam='out',
         lesson=dict(text='Truth is worth more than any reward.', after=0, y=560, size=84), no_caption=(0,),
         lines=['Truth is worth more than any reward.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with someone', line2='standing firm for the truth'), no_caption=(0,),
         lines=['Share this with someone standing firm for the truth. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """They came to defeat Musa. Then they fell in prostration. Why? 🤍

Pharaoh called the signs of Musa (Moses), peace be upon him, magic, and every learned magician was brought. They said: "Indeed for us is a reward if we are the predominant." (Quran 7:113)

They threw their ropes and staffs, and these seemed to move like snakes (20:66). Allah said: "Fear not. Indeed, it is you who are superior." (Quran 20:68)

"And We inspired to Moses, 'Throw your staff,' and at once it devoured what they were falsifying." (Quran 7:117)

The magicians fell in prostration and believed (20:70). Pharaoh threatened them with terrible punishment (20:71). They answered: "Never will we prefer you over what has come to us of clear proofs." (Quran 20:72)

Truth is worth more than any reward.

📖 Sources: Quran 7:103–126, 20:56–73, 26:34–51 (Saheeh International)
Share this with someone standing firm for the truth. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """Who do you know who stands firm for the truth? Send them this story 🤍

References: Quran, Surah Al-A'raf 7:103–126, Surah Ta-Ha 20:56–73 and Surah Ash-Shu'ara 26:34–51 (Saheeh International translation)."""
