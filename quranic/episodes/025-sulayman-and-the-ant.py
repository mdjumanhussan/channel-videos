"""Story 25: Sulayman and the ant. Source: Quran 27:15-19 (Saheeh International).
Cinematic "macro" episode, made on Juman's request (25 Nov 2026) to lift reach and watch time.
No people are drawn: no Sulayman, no soldiers, no jinn, no figure of any kind, and nothing stands for Allah.
The army is shown only as rising dust on the horizon and birds flying in rows (27:17 names birds among the soldiers).
The ants are animals. The speaking ant is never given a face, mouth or human features.
Facts used: Sulayman was given knowledge and taught the language of birds (27:15-16); his soldiers of jinn, men and birds were
gathered, marching in rows (27:17); they came upon the valley of the ants; an ant said "O ants, enter your dwellings that you not be
crushed by Solomon and his soldiers while they perceive not" (27:18); he smiled, amused at her speech, and prayed "My Lord, enable
me to be grateful for Your favor which You have bestowed upon me and upon my parents..." (27:19).
"She did not call the army cruel" only states what the verse does not say; her words "while they perceive not" are quoted exactly.
Not used: the ant's name or size, how far Sulayman heard her, numbers of soldiers, the valley's location, Israiliyyat.
Improvements tried (diagnosis 25 Nov: 3-8 s average watch on 60-70 s Reels):
- Shorter: ~40 s instead of 60-70 s (WORDS 85-130).
- Frame 1 is a striking picture with a short spoken hook, not a wall of title text.
- Cinematic macro look: depth-of-field blur on far and near layers, warm grade, film grain, rim-lit hero ant.
- Captions lower (CAPTION_Y 1470) so the picture owns the middle of the screen.
- Loop: the last scene returns to the hook's picture.
- Human-quality narrator (vidIQ voiceover, Brian) instead of Kokoro bm_george; Kokoro am_michael was the first cut."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  25'
VOICE, SPEED = 'am_michael', 1.1
WORDS = (85, 130)
CAPTION_Y = 1470
THUMB_AT = 0.8
# Narration: vidIQ voiceover, voice "Brian - Deep, Resonant and Comforting" (voiceoverId 9a50709f-86d6-4925-b52c-db35e60f6e23,
# full audio https://assets.vidiq.com/voiceovers/0e949607-e5bd-47e3-bfe6-e215e3d1e6c3/9a50709f-86d6-4925-b52c-db35e60f6e23.mp3).
# The engine renders picture + ambience on these line timings; vidIQ compose then lays the voiceover on top.
EXT_LINES = [(0, 2.586), (2.586, 3.553), (6.139, 6.766), (12.904, 2.429), (15.334, 1.306), (16.64, 6.844), (23.484, 1.646),
             (25.13, 2.273), (27.402, 2.508), (29.91, 3.161), (33.071, 1.228), (34.299, 5.564), (39.863, 3.318), (43.18, 2.429), (45.61, 4.911)]
TITLE = 'The Ant Who Spoke Up'
HITS = [(5, 0, 0.0)]      # 'Sulayman smiled, amused at her speech.'

AMBER = (255, 170, 70); ROSE = (240, 120, 90)

# ---------------------------------------------------------------- the ant (an animal only)
def ant(p, cx, base, s=1.0, flip=False, col=(30, 19, 14), rim=AMBER, raise_front=0.0, ant_up=0.0, a=255):
    """A side-view ant standing on `base`, facing right (flip=True faces left). Body length ~ 560*s.
    raise_front lifts the front legs (0..1); ant_up raises the antennae (0..1). Rim light on the top edge."""
    k = -1 if flip else 1
    def X(dx): return cx + k * dx * s
    def Y(dy): return base + dy * s
    sheen = lc(col, (120, 80, 50), .45); far = lc(col, (0, 0, 0), .35)
    def leg(x0, y0, kx, ky, fx, fy, c, w):
        p.line([(X(x0), Y(y0)), (X(kx), Y(ky)), (X(fx), Y(fy))], c, w * s, a)
        p.line([(X(fx), Y(fy)), (X(fx + 22), Y(fy + 2))], c, w * .7 * s, a)                 # foot (tarsus)
    # far legs (darker, behind the body)
    leg(30, -118, -30, -205, -95, 0, far, 11); leg(70, -118, 95, -215, 120, 0, far, 11)
    leg(110, -122, 175, -225 - 30 * raise_front, 225 + 20 * raise_front, -10 - 60 * raise_front, far, 11)
    def body(c, dx=0, dy=0, aa=a):
        def E(x, y, rx, ry): p.ell(X(x) + dx, Y(y) + dy, rx * s, ry * s, c, aa)
        E(-215, -128, 128, 88)              # gaster (abdomen)
        E(-80, -132, 26, 32); E(-40, -126, 22, 24)    # petiole nodes
        E(25, -140, 72, 40); E(88, -152, 48, 40)      # mesosoma (thorax)
        E(178, -168, 68, 58)                # head
        p.poly([(X(222) + dx, Y(-150) + dy), (X(268) + dx, Y(-128) + dy), (X(252) + dx, Y(-112) + dy), (X(216) + dx, Y(-126) + dy)], c, aa)   # mandible
    body(rim, -3 * s * k, -6 * s, int(a * .9))      # rim light: amber copy, nudged up and back
    body(col)
    # glossy sheen
    p.ell(X(-235), Y(-170), 62 * s, 26 * s, sheen, int(a * .55)); p.ell(X(170), Y(-200), 32 * s, 14 * s, sheen, int(a * .55))
    p.ell(X(30), Y(-165), 34 * s, 10 * s, sheen, int(a * .45))
    p.ell(X(200), Y(-182), 13 * s, 11 * s, (8, 6, 5), a); p.ell(X(204), Y(-187), 4 * s, 3 * s, (255, 236, 200), a)     # eye + glint
    # antennae (elbowed): a short scape up and forward from the front of the head, then the segmented funiculus reaching forward
    for side, off in ((0, 0), (1, -16)):
        c = far if side else col
        ex, ey = 222 + off, -208
        kx, ky = ex + 60, ey - 80 - 30 * ant_up
        tx, ty = kx + 150, ky + 40 - 90 * ant_up
        p.line([(X(ex), Y(ey)), (X(kx), Y(ky))], c, 7 * s, a)
        pts = [(X(lerp(kx, tx, f)), Y(lerp(ky, ty, f) - 22 * math.sin(f * math.pi))) for f in np.linspace(0, 1, 10)]
        p.line(pts, c, 5 * s, a)
        for q in pts[3::2]: p.ell(q[0], q[1], 4 * s, 4 * s, c, a)          # segments
        p.ell(pts[-1][0], pts[-1][1], 8 * s, 6 * s, c, a)                   # club
        if not side: p.line(pts[:6], rim, 1.8 * s, int(a * .7))
    # banding on the gaster
    for dx in (-150, -205, -260):
        p.line([(X(dx + 18 * math.cos(q)), Y(-128 - 82 * math.sin(q))) for q in np.linspace(.35, 2.8, 12)], lc(col, (120, 80, 50), .3), 3 * s, int(a * .7))
    # near legs (on top)
    leg(30, -118, -40, -200, -110, 0, col, 12); leg(70, -118, 85, -210, 140, 0, col, 12)
    leg(110, -122, 190, -230 - 30 * raise_front, 250 + 20 * raise_front, -10 - 70 * raise_front, col, 12)
    for x0, kx, ky in ((30, -40, -200), (70, 85, -210), (110, 190, -230 - 30 * raise_front)):
        p.line([(X(x0 + 3), Y(-122)), (X(kx), Y(ky - 3))], rim, 2.4 * s, int(a * .6))

def tiny_ant(d, x, y, s, flip=False, col=(28, 18, 12, 255), ph=0.0):
    """A small walking ant drawn with ImageDraw (screen pixels), for live crowds. Legs swing with ph."""
    k = -1 if flip else 1
    for i, lx in enumerate((-3, 2, 7)):
        sw = 5 * math.sin(ph + i * 2.1)
        d.line([(x + k * lx * s, y - 4 * s), (x + k * (lx + sw) * s, y + 4 * s)], fill=col, width=max(1, int(1.2 * s)))
    d.ellipse((x + k * -14 * s - 6 * s, y - 9 * s, x + k * -14 * s + 6 * s, y - 1 * s), fill=col)
    d.ellipse((x - 4 * s, y - 7 * s, x + 6 * s, y - 2 * s), fill=col)
    d.ellipse((x + k * 10 * s - 4 * s, y - 9 * s, x + k * 10 * s + 4 * s, y - 2 * s), fill=col)

# ---------------------------------------------------------------- scenery
def bokeh(p, seed, n, y0, y1, cols, rmin=20, rmax=70, a=(40, 110)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y, r = rnd.uniform(-60, 1140), rnd.uniform(y0, y1), rnd.uniform(rmin, rmax)
        c = rnd.choice(cols); p.ell(x, y, r, r, c, int(rnd.uniform(*a))); p.glow(x, y, r * 1.8, c, .25)

def sand_texture(p, y0, y1, seed, col=(255, 220, 170), n=2600, a=(40, 140)):
    rnd = random.Random(seed)
    for _ in range(n):
        y = rnd.uniform(y0, y1); r = rnd.uniform(.8, 2.2) * (.6 + .9 * (y - y0) / max(1, y1 - y0))
        p.ell(rnd.uniform(-80, 1160), y, r, r, col, int(rnd.uniform(*a)))

def ripples(p, y0, y1, seed, col, n=14, a=60):
    rnd = random.Random(seed)
    for i in range(n):
        y = lerp(y0, y1, (i + .5) / n) ; amp = rnd.uniform(6, 16); ph = rnd.uniform(0, 6)
        p.line([(x, y + amp * math.sin(x / rnd.uniform(90, 160) + ph)) for x in range(-80, 1180, 30)], col, 2 + 4 * i / n, a)

def dust_wall(p, y, h, col, seed, a=230):
    """The army's dust: a towering, billowing wall of dust on the horizon (no figures)."""
    def fn(t):
        rnd = random.Random(seed)
        for i in range(26):
            x = rnd.uniform(-120, 1200); r = rnd.uniform(.35, 1) * h * .45
            t.ell(x, y - rnd.uniform(0, h * .7), r * 1.3, r, lc(col, (255, 230, 190), rnd.uniform(0, .35)), a)
        t.rect(-200, y - 40, 1300, y + 260, col, a)
    p.blur_shape(fn, 26)

def bird_rows(p, y, rows, seed, col=(40, 26, 30), s=1.0, a=210):
    """Birds flying in neat rows (27:17: the soldiers marched in rows)."""
    rnd = random.Random(seed)
    for r in range(rows):
        yy = y + r * 46 * s; x0 = rnd.uniform(-60, 40)
        for i in range(14):
            x = x0 + i * 80 * s + r * 26; w = 16 * s
            p.line([(x - w, yy - 6 * s), (x, yy), (x + w, yy - 6 * s)], col, 3.2 * s, a)

def nest_hole(p, x, y, r, rim=(214, 160, 100)):
    p.ell(x, y + r * .15, r * 1.9, r * .75, lc(rim, (255, 235, 200), .25))     # mound
    p.ell(x, y, r * 1.25, r * .5, rim)
    p.ell(x, y + r * .05, r * .7, r * .3, (26, 14, 8))                          # the opening

# ---- layer painters
def warm_sky(p):
    p.sky([(-.1, (92, 60, 98)), (.18, (196, 106, 92)), (.34, (250, 168, 98)), (.46, (255, 214, 150)), (.62, (238, 170, 108)), (1.1, (120, 70, 46))])
    p.glow(700, 820, 520, (255, 236, 180), .9, 1.6); sun(p, 700, 820, 70, (255, 244, 214))

def hook_far(p):        # far: the dust of the army towering on the horizon (heavily blurred = depth of field)
    warm_sky(p); dust_wall(p, 930, 640, (150, 92, 76), 11); bird_rows(p, 330, 3, 18, col=(60, 36, 40), s=.9, a=190)
    mountains(p, 980, 160, (150, 92, 80), 12); p.rect(-200, 960, 1300, 1400, (170, 104, 70))
    bokeh(p, 13, 16, 600, 1000, [(255, 220, 160), (255, 190, 120)], 30, 80)

def hook_ground(p):     # mid: a sunlit sand ridge
    r = wave_ridge(-200, 1300, 1180, 50, 14, 3, 10)
    p.grad_poly(r + [(1300, 2300), (-200, 2300)], (236, 176, 110), (120, 66, 36), 1130, 1900)
    ripples(p, 1230, 1800, 15, (255, 214, 160), 12, 70); sand_texture(p, 1180, 2000, 16)
    p.glow(560, 1190, 520, (255, 210, 140), .45, 1.4)

def hook_ant(p):        # near: the hero ant on the ridge, antennae raised, rim-lit by the low sun
    p.glow(520, 1060, 460, (255, 190, 110), .35, 1.8)
    ant(p, 545, 1225, 1.2, ant_up=.7, raise_front=.1)

def hook_fg(p):         # nearest: out-of-focus pebbles and grains in front of the lens
    for x, y, r, c in ((90, 1790, 150, (90, 52, 30)), (980, 1830, 190, (110, 66, 40)), (820, 1700, 60, (150, 96, 60))):
        p.ell(x, y, r * 1.4, r, c, 235)
    bokeh(p, 17, 8, 1500, 1900, [(255, 210, 150)], 18, 40, (60, 120))

def march_sky(p):
    p.sky([(-.1, (70, 52, 92)), (.2, (170, 96, 98)), (.4, (246, 160, 96)), (.55, (255, 206, 140)), (1.1, (150, 92, 56))])
    p.glow(260, 1010, 600, (255, 230, 170), .8, 1.6); sun(p, 260, 1010, 60, (255, 242, 210))
    bird_rows(p, 380, 4, 21, s=1.0); bird_rows(p, 640, 3, 22, s=.7, a=170)

def march_land(p):
    mountains(p, 1080, 300, (120, 72, 74), 23, rim=(255, 190, 130))
    def haze(t):
        rnd = random.Random(27)
        for i in range(40):
            x = rnd.uniform(-150, 1230); r = rnd.uniform(40, 110)
            t.ell(x, 1075 - rnd.uniform(0, 90), r * 1.6, r, lc((226, 158, 110), (255, 226, 180), rnd.uniform(0, .4)), 200)
    p.blur_shape(haze, 18)
    dunes(p, 1100, 40, (214, 140, 86), (120, 70, 42), 24)
    dunes(p, 1260, 60, (190, 120, 74), (90, 50, 30), 25); sand_texture(p, 1250, 2000, 26, n=1200, a=(30, 90))

def valley_far(p):
    p.sky([(-.1, (90, 60, 90)), (.25, (220, 130, 96)), (.45, (255, 200, 140)), (1.1, (150, 90, 52))])
    dust_wall(p, 820, 420, (210, 136, 92), 31, 200); p.rect(-200, 820, 1300, 1300, (180, 112, 70))

def valley_floor(p):
    r = wave_ridge(-200, 1300, 980, 30, 32, 3, 10)
    p.grad_poly(r + [(1300, 2300), (-200, 2300)], (226, 166, 104), (110, 60, 34), 960, 1900)
    ripples(p, 1020, 1800, 33, (255, 212, 160), 10, 55); sand_texture(p, 980, 2000, 34, n=2000)
    for x, y, r in ((250, 1120, 34), (760, 1060, 26), (560, 1300, 52), (900, 1420, 40), (170, 1500, 46)):
        nest_hole(p, x, y, r)

def warn_far(p):        # the warning: low angle, dust closer and darker
    p.sky([(-.1, (60, 40, 70)), (.3, (180, 96, 86)), (.5, (240, 160, 100)), (1.1, (120, 70, 46))])
    dust_wall(p, 1000, 760, (176, 110, 84), 41, 240); p.rect(-200, 1000, 1300, 1400, (150, 90, 62))
    bokeh(p, 42, 14, 500, 1050, [(255, 200, 140), (255, 170, 110)], 30, 90, (30, 80))

def warn_ground(p):
    r = wave_ridge(-200, 1300, 1230, 40, 43, 3, 10)
    p.grad_poly(r + [(1300, 2300), (-200, 2300)], (220, 156, 96), (96, 52, 30), 1200, 1900)
    sand_texture(p, 1230, 2000, 44, n=1800); nest_hole(p, 820, 1330, 70)
    p.ell(430, 1250, 190, 60, (120, 80, 56)); p.ell(430, 1232, 170, 46, (156, 108, 76))   # a small stone she stands on

def warn_ant(p):
    p.glow(420, 1050, 360, (255, 186, 110), .4, 1.8)
    ant(p, 380, 1222, .9, ant_up=1.0, raise_front=1.0)

def close_far(p):       # extreme close-up of the hero ant
    p.sky([(-.1, (70, 46, 70)), (.4, (210, 120, 86)), (.6, (246, 170, 104)), (1.1, (120, 70, 46))])
    bokeh(p, 51, 22, 200, 1300, [(255, 210, 150), (255, 170, 110), (250, 140, 110)], 40, 120, (40, 110))

def close_ant(p):
    p.glow(560, 980, 520, (255, 190, 120), .35, 1.8)
    ant(p, 260, 1330, 1.7, ant_up=.6, raise_front=.3)
    r = wave_ridge(-200, 1300, 1330, 10, 52, 3, 10); p.grad_poly(r + [(1300, 2300), (-200, 2300)], (200, 140, 86), (80, 44, 26), 1320, 1900)
    sand_texture(p, 1330, 2000, 53, n=1500, a=(60, 160))

def gold_sky(p):        # the smile: the valley floods with soft gold light
    p.sky([(-.1, (110, 64, 92)), (.25, (236, 140, 100)), (.42, (255, 192, 120)), (.55, (255, 220, 160)), (1.1, (160, 96, 50))])
    p.glow(540, 880, 620, (255, 236, 190), .85, 1.6); sun(p, 540, 880, 80, (255, 248, 224))
    bird_rows(p, 300, 3, 61, col=(90, 60, 50), s=.8, a=150)

def gold_land(p):
    mountains(p, 1040, 220, (196, 130, 100), 62, rim=(255, 230, 180))
    dunes(p, 1080, 36, (232, 168, 100), (140, 84, 44), 63); sand_texture(p, 1080, 2000, 64, n=1400, a=(30, 90))
    for x, y, r in ((260, 1260, 40), (700, 1200, 32), (520, 1460, 58)): nest_hole(p, x, y, r, (230, 180, 120))

def dusk_sky(p):        # the dua: a calm dusk, first stars
    p.sky([(-.1, (26, 22, 56)), (.3, (80, 52, 96)), (.5, (200, 110, 96)), (.6, (246, 170, 110)), (1.1, (90, 52, 40))])
    stars(p, 90, 71, 700); moon(p, 820, 360, 46)

def dusk_land(p):
    mountains(p, 1120, 260, (66, 42, 60), 72, rim=(240, 150, 110))
    dunes(p, 1180, 50, (130, 80, 62), (50, 30, 26), 73); p.glow(540, 1180, 600, (255, 170, 110), .25, 1.4)

# ---- live effects (drawn every frame)
def crowd_fx(img, tt, info, n=46, into=None, start=0.0, speed=1.0, seed=7):
    """Small ants walking across the valley floor; when `into` is set they head for those nest holes and vanish into them."""
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); rnd = random.Random(seed)
    t = max(0.0, tt - info['start'] - start)
    for i in range(n):
        y = rnd.uniform(1000, 1760); x0 = rnd.uniform(-80, 1160); s = .9 + 1.6 * (y - 1000) / 760
        if into:
            hx, hy = into[i % len(into)]; dist = math.hypot(hx - x0, hy - y); v = rnd.uniform(80, 150) * speed
            f = clamp(t * v / max(1, dist))
            if f >= 1: continue
            x, yy = lerp(x0, hx, f), lerp(y, hy, f); flip = hx < x0
        else:
            v = rnd.uniform(30, 60); flip = rnd.random() < .5; x = x0 + (-v if flip else v) * t; yy = y
        tiny_ant(d, x * 2, yy * 2, s * 2, flip, ph=tt * 18 + i)
    img.alpha_composite(lay.resize((W, H), Image.LANCZOS))

def tremor_fx(img, tt, info, n=70, seed=9):
    """Sand grains hopping as the ground trembles."""
    d = ImageDraw.Draw(img); rnd = random.Random(seed)
    for i in range(n):
        x, y0, r = rnd.uniform(0, W), rnd.uniform(1250, 1850), rnd.uniform(1.5, 3.5)
        h = abs(math.sin(tt * rnd.uniform(9, 14) + i)) * rnd.uniform(4, 14)
        d.ellipse((x - r, y0 - h - r, x + r, y0 - h + r), fill=(255, 222, 170, 200))

# ---- colour grade + film grain (POST hook)
_GRAIN = None
def POST(img, tt):
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(5); _GRAIN = [rng.normal(0, 7, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
    a = np.asarray(img.convert('RGB')).astype(np.float32) / 255.0
    lum = a.mean(2, keepdims=True)
    a = a + (lum - .5) * .10                                         # gentle contrast
    shadow = np.clip(.45 - lum, 0, .45) / .45; high = np.clip(lum - .55, 0, .45) / .45
    a = a + shadow * np.array([-.012, .006, .03]) + high * np.array([.03, .012, -.02])   # teal shadows, warm highlights
    g = _GRAIN[int(tt * 24) % 6]; g = np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None] / 255.0
    a = np.clip(a + g, 0, 1)
    return Image.fromarray((a * 255).astype(np.uint8)).convert('RGBA')

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[(hook_far, 0, 10), (hook_ground, .45, 2), (hook_ant, .7), (hook_fg, 1, 16)], fx=['dust', (tremor_fx, {})], cam='in', bloom=.75,
         title=dict(text='An army was coming.', plain=True, hold=2.6), no_caption=(0,),
         lines=['An army was marching toward the ants.', 'One ant spoke. Her words are in the Quran.']),
    dict(layers=[(march_sky, 0, 3), (march_land, .5, 1)], fx=['dust'], cam='right', bloom=.65,
         lines=['Sulayman, peace be upon him, marched with his soldiers of jinn, men and birds, in rows.']),
    dict(layers=[(valley_far, 0, 12), (valley_floor, .6)], fx=[(crowd_fx, dict(n=50)), (tremor_fx, {})], cam='in', bloom=.6,
         lines=['They came upon the valley of the ants.']),
    dict(layers=[(warn_far, 0, 12), (warn_ground, .5, 1), (warn_ant, .75)], fx=[(crowd_fx, dict(n=40, into=[(820, 1330)], speed=1.4, seed=11)), (tremor_fx, {}), 'dust'],
         cam='in', bloom=.7, pause=.5,
         verse=dict(key='27:18', ar=(8, 19), en='O ants, enter your dwellings that you not be crushed by Solomon and his soldiers while they perceive not', line=1, ar_size=66, y=470),
         lines=['An ant said:', 'O ants, enter your dwellings, that you not be crushed by Solomon and his soldiers while they perceive not.']),
    dict(layers=[(close_far, 0, 14), (close_ant, .8)], fx=['dust'], cam='in', bloom=.7,
         lines=['She warned her people.', 'She did not call the army cruel.', 'She said: they perceive not.']),
    dict(layers=[(gold_sky, 0, 2), (gold_land, .5, 1)], fx=['dust', (crowd_fx, dict(n=14, seed=21))], cam='out', bloom=.85,
         verse=dict(key='27:19', ar=(0, 4), en='So [Solomon] smiled, amused at her speech', line=0, ar_size=92, y=520),
         lines=['Sulayman smiled, amused at her speech.']),
    dict(layers=[(dusk_sky, 0, 1), (dusk_land, .6)], fx=['twinkle', 'dust'], cam='up', bloom=.7, pause=.5,
         verse=dict(key='27:19', ar=(5, 13), en='My Lord, enable me to be grateful for Your favor which You have bestowed upon me', line=1, ar_size=72, y=560),
         lines=['And he prayed:', 'My Lord, enable me to be grateful for Your favor which You have bestowed upon me.']),
    dict(layers=[(gold_sky, 0, 4), (gold_land, .5, 2)], fx=['dust'], cam='in', bloom=.8,
         lesson=dict(text='Answer every blessing with gratitude.', after=1, y=560, size=80), no_caption=(1,),
         lines=['A whole army. One small ant.', 'And his answer was gratitude.']),
    dict(layers=[(hook_far, 0, 10), (hook_ground, .45, 2), (hook_ant, .7), (hook_fg, 1, 16)], fx=['dust'], cam='out', bloom=.75,
         end=dict(after=0, line1='Share this with', line2='someone you are grateful for'), no_caption=(0,),
         lines=['Share this with someone you are grateful for. Follow for a new story every day.']),
]

PRON = {'Sulayman': 'sʊlɐjmˈɑːn', 'Quran': 'kʊɹˈɑːn', 'Allah': 'ɐlˈɑː'}

CAPTION = """An army was marching toward the ants. One ant spoke, and her words are in the Quran. 🐜

Sulayman (Solomon), peace be upon him, was marching with his soldiers of jinn, men and birds, in rows (Quran 27:17).

"Until, when they came upon the valley of the ants, an ant said, 'O ants, enter your dwellings that you not be crushed by Solomon and his soldiers while they perceive not.'" (Quran 27:18)

She warned her people, and she did not call the army cruel.

"So [Solomon] smiled, amused at her speech, and said, 'My Lord, enable me to be grateful for Your favor which You have bestowed upon me and upon my parents...'" (Quran 27:19)

Answer every blessing with gratitude.

📖 Sources: Quran 27:15–19 (Saheeh International)
Share this with someone you are grateful for. Follow for a new story every day.

#QuranicStories #ProphetSulayman #IslamicReminder"""

FIRST_COMMENT = """A king with a whole army, and he answered one small ant with gratitude. What blessing will you thank Allah for today? 🤍

Reference: Quran, Surah An-Naml 27:15–19 (Saheeh International translation)."""
