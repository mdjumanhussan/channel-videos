"""Quranic Story engine: vertical 1080x1920 cinematic Reels.
Painted scene layers + slow parallax camera + glowing particles + word-by-word captions
+ verse cards (exact Arabic + Saheeh International from data/quran.json) + star-wipe transitions.
Narration: Kokoro TTS. No music. See RUNBOOK.md.

usage: python3 quranic/engine.py quranic/episodes/NAME.py audio | still T1 T2 ... | render | check
"""
import math, os, sys, json, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
M = 1.15                                    # layers are painted 15% larger than the screen for camera moves
LW, LH = int(W * M), int(H * M)
OX, OY = (LW - W) // 2, (LH - H) // 2       # screen (0,0) sits at layer (OX,OY)
SS = 2                                      # supersampling when painting layers
SR = 24000
GOLD = (255, 205, 90); CREAM = (255, 244, 220); WHITE = (255, 255, 255); INK = (20, 14, 10)
GF = '/usr/share/fonts/truetype/google-fonts/'
_fc = {}
MODELS = os.environ.get('KOKORO_MODELS', os.path.expanduser('~/.cache/kokoro'))
QURAN = None
EP = None; SC = []; OUT = 'build'

# Pronunciation fixes (en-gb phonemes). Episodes may extend with PRON = {...}.
PRON = {
    'Allah': 'ɐlˈɑː', "Allah's": 'ɐlˈɑːz', 'Iblees': 'ɪblˈiːs', 'Shaytaan': 'ʃeɪtˈɑːn', 'Adam': 'ˈɑːdæm',
    'Musa': 'mˈuːsɑː', 'Nuh': 'nˈuːh', 'Ibrahim': 'ɪbɹɑːhˈiːm', 'Isa': 'ˈiːsɑː', 'Quran': 'kʊɹˈɑːn',
    'Sulayman': 'sʊlɐjmˈɑːn', 'Dawud': 'dɑːwˈuːd', 'Yunus': 'jˈuːnʊs', 'Yusuf': 'jˈuːsʊf',
    'Ismail': 'ɪsmɑːʔˈiːl', 'Ishaq': 'ɪsħˈɑːq', 'Yaqub': 'jɑːʔqˈuːb', 'Harun': 'hɑːɹˈuːn', 'Firawn': 'fɪɹʕˈaʊn',
    'Maryam': 'mˈaɹjæm', 'Zakariya': 'zækɐɹˈiːjɑː', 'Yahya': 'jˈæħjɑː', 'Hud': 'hˈuːd', 'Salih': 'sˈɑːlɪħ',
    'Shuayb': 'ʃʊʕˈeɪb', 'Lut': 'lˈuːt', 'Ayyub': 'ɐjjˈuːb', 'Idris': 'ɪdɹˈiːs', 'Luqman': 'lʊqmˈɑːn',
    'Dhul-Qarnayn': 'ðʊlqɑɹnˈeɪn', 'Khidr': 'xˈɪdɚ', 'Jannah': 'dʒˈænnɑː', 'Kabah': 'kˈɑːbɐ', 'Makkah': 'mˈækkɐ',
    'Bilqis': 'bɪlqˈiːs', 'Qarun': 'qɑːɹˈuːn', 'Talut': 'tɑːlˈuːt', 'Jalut': 'dʒɑːlˈuːt', 'Uzair': 'ʊzˈeɪɹ',
    'Hawwa': 'ħˈæwwɑː', 'Muhammad': 'mʊħˈæmmæd', 'Surah': 'sˈʊɹɐ', 'subhanahu': 'sʊbħˈɑːnɐhuː',
}

# ------------------------------------------------------------------ helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerp(a, b, t): return a + (b - a) * t
def lc(c1, c2, t): return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def F(size, w='Bold'):
    k = (size, w)
    if k not in _fc:
        if w.startswith('Amiri'):
            p = os.path.join(HERE, 'fonts', w + '.ttf')
            _fc[k] = ImageFont.truetype(p, int(size), layout_engine=ImageFont.Layout.RAQM)
        elif w.startswith('Lora'):
            p = GF + ('Lora-Italic-Variable.ttf' if 'Italic' in w else 'Lora-Variable.ttf')
            f = ImageFont.truetype(p, int(size))
            try: f.set_variation_by_name('Bold' if 'Bold' in w else 'Medium')
            except Exception: pass
            _fc[k] = f
        else:
            p = GF + f'Poppins-{w}.ttf'
            _fc[k] = ImageFont.truetype(p if os.path.exists(p) else GF + 'Poppins-Bold.ttf', int(size))
    return _fc[k]

def quran():
    global QURAN
    if QURAN is None: QURAN = json.load(open(os.path.join(HERE, 'data', 'quran.json')))
    return QURAN

# ------------------------------------------------------------------ painter (static layers)
class P:
    """Paints one RGBA layer in SCREEN coordinates (0..1080 x 0..1920; may overshoot by the camera margin)."""
    def __init__(s):
        s.img = Image.new('RGBA', (LW * SS, LH * SS), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.img)
    def X(s, x): return (x + OX) * SS
    def Y(s, y): return (y + OY) * SS
    def pts(s, pts): return [(s.X(x), s.Y(y)) for x, y in pts]
    def poly(s, pts, col, a=255): s.d.polygon(s.pts(pts), fill=tuple(col[:3]) + (a,))
    def ell(s, x, y, rx, ry, col, a=255): s.d.ellipse((s.X(x - rx), s.Y(y - ry), s.X(x + rx), s.Y(y + ry)), fill=tuple(col[:3]) + (a,))
    def rect(s, x0, y0, x1, y1, col, a=255): s.d.rectangle((s.X(x0), s.Y(y0), s.X(x1), s.Y(y1)), fill=tuple(col[:3]) + (a,))
    def line(s, pts, col, w, a=255): s.d.line(s.pts(pts), fill=tuple(col[:3]) + (a,), width=max(1, int(w * SS)), joint='curve')
    def sky(s, stops):
        """stops: [(y_frac 0..1 of screen, color), ...] vertical gradient over whole layer."""
        ys = (np.arange(LH * SS) / SS - OY) / H
        arr = np.zeros((LH * SS, 3))
        fr = [p for p, _ in stops]
        for i in range(3): arr[:, i] = np.interp(ys, fr, [c[i] for _, c in stops])
        col = np.repeat(arr[:, None, :], LW * SS, 1)
        rgba = np.concatenate([col, np.full(col.shape[:2] + (1,), 255)], 2).astype(np.uint8)
        s.img = Image.fromarray(rgba, 'RGBA'); s.d = ImageDraw.Draw(s.img)
    def grad_poly(s, pts, top, bot, y0=None, y1=None, a=255):
        ys = [p[1] for p in pts]; y0 = min(ys) if y0 is None else y0; y1 = max(ys) if y1 is None else y1
        mask = Image.new('L', s.img.size, 0); ImageDraw.Draw(mask).polygon(s.pts(pts), fill=a)
        yy = (np.arange(LH * SS) / SS - OY); t = np.clip((yy - y0) / max(1, y1 - y0), 0, 1)[:, None]
        arr = np.stack([np.repeat(top[i] + (bot[i] - top[i]) * t, LW * SS, 1) for i in range(3)] + [np.full((LH * SS, LW * SS), 255)], 2).astype(np.uint8)
        s.img.paste(Image.fromarray(arr, 'RGBA'), (0, 0), mask); s.d = ImageDraw.Draw(s.img)
    def glow(s, x, y, r, col, strength=1.0, power=2.0):
        """Soft radial light (alpha falloff)."""
        R = int(r * SS); cx, cy = int(s.X(x)), int(s.Y(y))
        x0, y0 = max(0, cx - R), max(0, cy - R); x1, y1 = min(s.img.width, cx + R), min(s.img.height, cy + R)
        if x1 <= x0 or y1 <= y0: return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / R
        al = (np.clip(1 - d, 0, 1) ** power) * 255 * strength
        g = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); g[..., :3] = col[:3]; g[..., 3] = np.clip(al, 0, 255)
        s.img.alpha_composite(Image.fromarray(g, 'RGBA'), (x0, y0))
    def blur_shape(s, fn, radius):
        """Draw with fn(P) onto a temp layer, blur it, composite."""
        t = P(); fn(t); im = t.img.reduce(4).filter(ImageFilter.GaussianBlur(radius * SS / 4)).resize(s.img.size, Image.BILINEAR)
        s.img.alpha_composite(im)
    def finish(s): return s.img.resize((LW, LH), Image.LANCZOS)

# ---- reusable scenery (call inside layer painters). Coordinates are screen units.
def wave_ridge(x0, x1, base, amp, seed, n=5, step=12):
    rnd = random.Random(seed); comps = [(rnd.uniform(.002, .009), rnd.uniform(0, 6.28), rnd.uniform(.3, 1)) for _ in range(n)]
    tot = sum(c[2] for c in comps)
    return [(x, base - amp * sum(w * math.sin(x * f + ph) for f, ph, w in comps) / tot) for x in range(int(x0), int(x1) + step, step)]

def dunes(p, base, amp, top, bot, seed, bottom=2300):
    r = wave_ridge(-200, 1300, base, amp, seed, 3, 10)
    p.grad_poly(r + [(1300, bottom), (-200, bottom)], top, bot, base - amp, base + 500)

def mountains(p, base, height, col, seed, rim=None, peaks=5):
    rnd = random.Random(seed); pts = [(-200, base)]; x = -200
    while x < 1300:
        x += rnd.uniform(120, 300); pts.append((x, base - height * rnd.uniform(.35, 1)))
        x += rnd.uniform(100, 250); pts.append((x, base - height * rnd.uniform(.05, .35)))
    pts += [(1300, base), (1300, 2300), (-200, 2300)]
    p.poly(pts, col)
    if rim:
        for i in range(1, len(pts) - 3): p.line([pts[i], pts[i + 1]], rim, 3, 120)

def stars(p, n, seed, y1=1100, col=(255, 250, 235)):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(-80, 1160), rnd.uniform(-140, y1); r = rnd.choice([1, 1, 1.4, 1.8, 2.4])
        p.ell(x, y, r, r, col, int(rnd.uniform(120, 255)))
        if r > 2: p.glow(x, y, 14, col, .35)

def moon(p, x, y, r, crescent=True, col=(255, 240, 200)):
    p.glow(x, y, r * 5, col, .25); p.glow(x, y, r * 2.2, col, .35)
    p.ell(x, y, r, r, col)
    if crescent:
        # cut with sky-coloured disc: use transparency-safe approach by painting with pixel sampled sky
        c = p.img.getpixel((int(p.X(x + r * 1.6)), int(p.Y(y - r * .9))))
        p.ell(x + r * .42, y - r * .22, r * .86, r * .86, c[:3])

def sun(p, x, y, r, col=(255, 220, 150)):
    p.glow(x, y, r * 9, col, .35, 1.6); p.glow(x, y, r * 3, (255, 235, 190), .6); p.ell(x, y, r, r, (255, 248, 225))

def cloud_bank(p, y, top, bot, seed, bump=60, a=255, blur=4):
    """Soft cloud bank: bumpy top edge made of overlapping puffs, vertical gradient fill."""
    rnd = random.Random(seed); pts = []; x = -220
    while x < 1320:
        r = rnd.uniform(bump * .6, bump * 1.6)
        for k in range(9): ang = math.pi + math.pi * k / 8; pts.append((x + r * math.cos(ang) + r, y - rnd.uniform(0, bump * .8) + r * math.sin(ang) * .9))
        x += r * rnd.uniform(1.1, 1.6)
    pts += [(1320, 2300), (-220, 2300)]
    t = P(); t.grad_poly(pts, top, bot, y - bump * 2, y + 500, a)
    im = t.img.filter(ImageFilter.GaussianBlur(blur * SS)) if blur else t.img
    p.img.alpha_composite(im); p.d = ImageDraw.Draw(p.img)

def clouds(p, seed, y0, y1, col=(255, 210, 170), n=7, a=150):
    rnd = random.Random(seed)
    def fn(t):
        for _ in range(n):
            x, y = rnd.uniform(-100, 1180), rnd.uniform(y0, y1); w = rnd.uniform(160, 380)
            for k in range(9): t.ell(x + rnd.uniform(-w * .7, w * .7), y + rnd.uniform(-14, 14), w * rnd.uniform(.12, .3), w * rnd.uniform(.04, .09), col, int(a * rnd.uniform(.5, 1)))
    p.blur_shape(fn, 9)

def mosque(p, cx, base, s, col, windows=None):
    """Mosque silhouette: central dome, two minarets. windows=(r,g,b) lights them."""
    p.rect(cx - 170 * s, base - 150 * s, cx + 170 * s, base + 600, col)
    p.ell(cx, base - 150 * s, 120 * s, 125 * s, col); p.rect(cx - 120 * s, base - 160 * s, cx + 120 * s, base - 140 * s, col)
    p.poly([(cx - 8 * s, base - 270 * s), (cx, base - 320 * s), (cx + 8 * s, base - 270 * s)], col)
    for dx in (-250, 250):
        x = cx + dx * s; p.rect(x - 22 * s, base - 420 * s, x + 22 * s, base + 600, col)
        p.rect(x - 32 * s, base - 300 * s, x + 32 * s, base - 285 * s, col)
        p.ell(x, base - 420 * s, 24 * s, 34 * s, col); p.poly([(x - 5 * s, base - 450 * s), (x, base - 490 * s), (x + 5 * s, base - 450 * s)], col)
    for dx in (-300, 300):
        x = cx + dx * s; p.rect(x - 70 * s, base - 60 * s, x + 70 * s, base + 600, col); p.ell(x, base - 60 * s, 55 * s, 50 * s, col)
    if windows:
        for i in range(-2, 3):
            x = cx + i * 55 * s; p.ell(x, base - 60 * s, 14 * s, 14 * s, windows); p.rect(x - 14 * s, base - 60 * s, x + 14 * s, base - 10 * s, windows)
            p.glow(x, base - 40 * s, 50 * s, windows, .35)

def city(p, base, col, seed, lights=None, domes=True):
    rnd = random.Random(seed); x = -150
    while x < 1250:
        w = rnd.uniform(60, 150); h = rnd.uniform(60, 260); p.rect(x, base - h, x + w, base + 800, col)
        if domes and rnd.random() < .35: p.ell(x + w / 2, base - h, w * .38, w * .4, col)
        if lights and rnd.random() < .7:
            for _ in range(rnd.randint(1, 3)):
                wx, wy = x + rnd.uniform(10, w - 18), base - h + rnd.uniform(25, h - 10)
                p.rect(wx, wy, wx + 8, wy + 14, lights, 230); p.glow(wx + 4, wy + 7, 22, lights, .3)
        x += w + rnd.uniform(-10, 20)

def palm(p, x, base, h, col, lean=0.0):
    tx = x + lean * h; p.line([(x, base), (x + lean * h * .5 + 8, base - h * .5), (tx, base - h)], col, 14)
    for ang in (-160, -130, -100, -70, -40, -15, 15, 200, 230):
        a = math.radians(ang); pts = []
        for k in range(8):
            r = k * h * .055; pts.append((tx + r * math.cos(a), base - h + r * math.sin(a) + (k ** 2) * 1.6))
        p.line(pts, col, 9)

def tree(p, x, base, h, trunk, leaves, seed, glow=None):
    rnd = random.Random(seed)
    p.poly([(x - 16, base), (x - 7, base - h * .55), (x + 7, base - h * .55), (x + 16, base)], trunk)
    for k in range(3): p.line([(x, base - h * (.4 + k * .07)), (x + rnd.choice([-1, 1]) * h * .25, base - h * (.6 + k * .07))], trunk, 7)
    if glow: p.glow(x, base - h * .7, h * .9, glow, .45)
    for _ in range(26):
        ax, ay = x + rnd.uniform(-h * .38, h * .38), base - h * rnd.uniform(.55, 1.0); r = rnd.uniform(.12, .2) * h
        p.ell(ax, ay, r, r * .85, lc(leaves, (255, 255, 255), rnd.uniform(0, .12)))

def kaaba(p, cx, base, s):
    blk = (16, 14, 14); side = (34, 30, 28); gold = (214, 170, 80)
    p.poly([(cx - 150 * s, base), (cx + 70 * s, base + 30 * s), (cx + 70 * s, base - 250 * s), (cx - 150 * s, base - 270 * s)], blk)
    p.poly([(cx + 70 * s, base + 30 * s), (cx + 200 * s, base - 10 * s), (cx + 200 * s, base - 270 * s), (cx + 70 * s, base - 250 * s)], side)
    p.poly([(cx - 150 * s, base - 270 * s), (cx + 70 * s, base - 250 * s), (cx + 200 * s, base - 270 * s), (cx - 20 * s, base - 290 * s)], (28, 24, 24))
    p.poly([(cx - 150 * s, base - 205 * s), (cx + 70 * s, base - 186 * s), (cx + 70 * s, base - 168 * s), (cx - 150 * s, base - 187 * s)], gold)
    p.poly([(cx + 70 * s, base - 186 * s), (cx + 200 * s, base - 206 * s), (cx + 200 * s, base - 188 * s), (cx + 70 * s, base - 168 * s)], lc(gold, (0, 0, 0), .25))
    p.rect(cx - 40 * s, base - 140 * s, cx + 10 * s, base - 30 * s, gold)

def ark(p, cx, y, s, col=(92, 58, 34), dark=(54, 34, 20)):
    p.poly([(cx - 300 * s, y - 40 * s), (cx + 300 * s, y - 40 * s), (cx + 230 * s, y + 70 * s), (cx - 230 * s, y + 70 * s)], col)
    for k in range(4): p.line([(cx - 280 * s + k * 10 * s, y - 10 * s + k * 20 * s), (cx + 280 * s - k * 12 * s, y - 10 * s + k * 20 * s)], dark, 3)
    p.rect(cx - 150 * s, y - 130 * s, cx + 150 * s, y - 40 * s, lc(col, (0, 0, 0), .15))
    p.poly([(cx - 175 * s, y - 130 * s), (cx, y - 200 * s), (cx + 175 * s, y - 130 * s)], dark)
    for i in range(-2, 3): p.rect(cx + i * 50 * s - 10 * s, y - 105 * s, cx + i * 50 * s + 10 * s, y - 80 * s, (255, 200, 110))

def sea(p, top, c_top, c_bot, seed, lines=(255, 255, 255)):
    p.grad_poly([(-200, top), (1300, top), (1300, 2300), (-200, 2300)], c_top, c_bot, top, top + 900)
    rnd = random.Random(seed)
    for k in range(40):
        y = top + (k / 40) ** 1.6 * 900; x = rnd.uniform(-100, 1100); w = 40 + k * 6
        p.line([(x, y), (x + w, y)], lines, 1 + k * .06, int(40 + k * 2))

def fire(p, cx, base, w, h, seed):
    rnd = random.Random(seed)
    p.glow(cx, base - h * .4, w * 1.6, (255, 130, 40), .7)
    def fn(t): _flames(t, cx, base, w, h, random.Random(seed))
    p.blur_shape(fn, 10); _flames(p, cx, base, w, h, random.Random(seed))
    p.glow(cx, base - h * .2, w * .5, (255, 240, 200), .6)

def _flames(p, cx, base, w, h, rnd):
    for col, sc in (((200, 50, 20), 1), ((255, 120, 30), .75), ((255, 200, 80), .5), ((255, 245, 200), .25)):
        for _ in range(7):
            x = cx + rnd.uniform(-w * .5, w * .5) * sc; hh = h * sc * rnd.uniform(.6, 1); ww = w * .18 * sc
            p.poly([(x - ww, base), (x - ww * .4, base - hh * .5), (x + rnd.uniform(-ww, ww) * .4, base - hh), (x + ww * .4, base - hh * .5), (x + ww, base)], col)

def lantern(p, x, y, s=1.0, col=(255, 190, 90)):
    frame = (60, 40, 20)
    p.line([(x, y - 150 * s), (x, y - 60 * s)], frame, 3)
    p.glow(x, y, 160 * s, col, .55)
    p.poly([(x - 30 * s, y - 60 * s), (x + 30 * s, y - 60 * s), (x + 40 * s, y + 40 * s), (x - 40 * s, y + 40 * s)], col)
    p.poly([(x - 40 * s, y - 60 * s), (x, y - 95 * s), (x + 40 * s, y - 60 * s)], frame)
    p.rect(x - 44 * s, y + 40 * s, x + 44 * s, y + 55 * s, frame)
    p.line([(x, y - 60 * s), (x, y + 40 * s)], frame, 3); p.glow(x, y - 5, 45 * s, (255, 250, 220), .8)

def rays(p, x, y, col, n=9, spread=70, length=2600, width=5, a=.22, angle=90, seed=1):
    rnd = random.Random(seed)
    def fn(t):
        for i in range(n):
            ang = math.radians(angle - spread / 2 + spread * (i + rnd.uniform(-.3, .3)) / max(1, n - 1))
            w = math.radians(width * rnd.uniform(.5, 1.4))
            t.poly([(x, y), (x + length * math.cos(ang - w), y + length * math.sin(ang - w)), (x + length * math.cos(ang + w), y + length * math.sin(ang + w))], col, int(255 * a))
    p.blur_shape(fn, 18)

def cave_frame(p, col=(18, 14, 12), cx=540, top=520, w=520):
    pts = [(-200, -200), (1300, -200), (1300, 2300), (-200, 2300), (-200, -200)]
    hole = [(cx + w * math.cos(a) * (1 + .08 * math.sin(a * 5)), top + 700 + 700 * math.sin(a) * (1 + .05 * math.cos(a * 7))) for a in np.linspace(math.pi, 2 * math.pi, 40)]
    hole = [(cx - w, 1700)] + hole + [(cx + w, 1700)]
    m = Image.new('L', p.img.size, 255); ImageDraw.Draw(m).polygon(p.pts(hole), fill=0)
    solid = Image.new('RGBA', p.img.size, tuple(col) + (255,)); p.img.paste(solid, (0, 0), m); p.d = ImageDraw.Draw(p.img)

def whale(p, cx, cy, s, col=(20, 40, 60)):
    p.ell(cx, cy, 330 * s, 120 * s, col)
    p.poly([(cx + 280 * s, cy - 20 * s), (cx + 470 * s, cy - 120 * s), (cx + 430 * s, cy), (cx + 470 * s, cy + 110 * s), (cx + 280 * s, cy + 30 * s)], col)
    p.poly([(cx - 40 * s, cy + 80 * s), (cx + 40 * s, cy + 190 * s), (cx + 70 * s, cy + 90 * s)], col)
    p.ell(cx - 230 * s, cy - 30 * s, 9 * s, 9 * s, lc(col, (255, 255, 255), .5))

def well(p, cx, base, s, col=(120, 100, 80)):
    p.ell(cx, base, 150 * s, 40 * s, lc(col, (0, 0, 0), .4)); p.rect(cx - 150 * s, base - 120 * s, cx + 150 * s, base, col)
    p.ell(cx, base - 120 * s, 150 * s, 40 * s, lc(col, (255, 255, 255), .15)); p.ell(cx, base - 120 * s, 120 * s, 28 * s, (10, 8, 8))
    for k in range(4): p.line([(cx - 150 * s, base - 30 * k * s), (cx + 150 * s, base - 30 * k * s)], lc(col, (0, 0, 0), .3), 2)

def pyramids(p, base, col, shade, seed=1):
    for cx, w in ((250, 300), (640, 420), (980, 220)):
        p.poly([(cx - w, base), (cx, base - w * .9), (cx + w, base)], col)
        p.poly([(cx, base - w * .9), (cx + w, base), (cx + w * .25, base)], shade)

# ------------------------------------------------------------------ animated effects
_sprites = {}
def sprite(r, col):
    k = (r, col)
    if k not in _sprites:
        n = int(r * 2 + 1); yy, xx = np.mgrid[0:n, 0:n]; d = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
        a = np.clip(1 - d, 0, 1) ** 2.2
        core = np.clip(1 - d * 4, 0, 1)
        g = np.zeros((n, n, 4), np.uint8)
        for i in range(3): g[..., i] = np.clip(col[i] + (255 - col[i]) * core, 0, 255)
        g[..., 3] = np.clip(a * 255, 0, 255); _sprites[k] = Image.fromarray(g, 'RGBA')
    return _sprites[k]

def fx_particles(img, kind, t, seed=3, n=None, alpha=1.0):
    rnd = random.Random(seed)
    if kind == 'dust':        # golden motes drifting up
        n = n or 45
        for i in range(n):
            x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(15, 50), rnd.choice([6, 8, 10, 14])
            y = (y0 - t * sp) % (H + 40) - 20; x = x0 + 18 * math.sin(t * .6 + i)
            tw = .55 + .45 * math.sin(t * 2.2 + i * 1.7)
            sp_ = sprite(r, GOLD); s2 = sp_.copy(); s2.putalpha(s2.getchannel('A').point(lambda v, k=tw * alpha: int(v * k)))
            img.alpha_composite(s2, (int(x - r), int(y - r)))
    elif kind == 'embers':
        n = n or 40
        for i in range(n):
            x0, sp, r = rnd.uniform(100, W - 100), rnd.uniform(80, 220), rnd.choice([5, 7, 9])
            y = H - ((t * sp + rnd.uniform(0, H)) % (H * .8)); x = x0 + 40 * math.sin(t * 1.3 + i)
            img.alpha_composite(sprite(r, (255, 140, 50)), (int(x - r), int(y - r)))
    elif kind == 'twinkle':   # bright twinkling stars in the sky
        n = n or 22
        for i in range(n):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * .5), rnd.choice([10, 14, 18])
            k = max(0, math.sin(t * rnd.uniform(1, 2.5) + i * 2.1)) ** 3
            if k > .05:
                s2 = sprite(r, (255, 250, 230)).copy(); s2.putalpha(s2.getchannel('A').point(lambda v, k=k: int(v * k)))
                img.alpha_composite(s2, (int(x - r), int(y - r)))
    elif kind == 'fireflies':
        n = n or 26
        for i in range(n):
            x = rnd.uniform(0, W) + 60 * math.sin(t * rnd.uniform(.3, .8) + i); y = rnd.uniform(H * .45, H * .95) + 40 * math.cos(t * .5 + i)
            k = .4 + .6 * max(0, math.sin(t * 2 + i))
            s2 = sprite(9, (200, 255, 140)).copy(); s2.putalpha(s2.getchannel('A').point(lambda v, k=k: int(v * k)))
            img.alpha_composite(s2, (int(x - 9), int(y - 9)))
    elif kind == 'rain':
        d = ImageDraw.Draw(img)
        for i in range(n or 140):
            x0, sp = rnd.uniform(-200, W), rnd.uniform(1400, 2200); y = (rnd.uniform(0, H) + t * sp) % (H + 100) - 50; x = x0 + (y / H) * 160
            d.line([(x, y), (x + 12, y + 60)], fill=(200, 215, 235, 110), width=2)
    elif kind == 'bubbles':
        d = ImageDraw.Draw(img)
        for i in range(n or 30):
            x0, sp, r = rnd.uniform(0, W), rnd.uniform(40, 120), rnd.uniform(4, 14); y = H - ((t * sp + rnd.uniform(0, H)) % H); x = x0 + 12 * math.sin(t * 2 + i)
            d.ellipse((x - r, y - r, x + r, y + r), outline=(200, 235, 255, 150), width=2)
    elif kind == 'petals':
        d = ImageDraw.Draw(img)
        for i in range(n or 22):
            x0, sp = rnd.uniform(-100, W), rnd.uniform(60, 140); y = (rnd.uniform(0, H) + t * sp) % (H + 60) - 30; x = x0 + 80 * math.sin(t * .8 + i) + t * 20
            a = t * 2 + i; r = 9
            d.polygon([(x + r * math.cos(a), y + r * math.sin(a)), (x + r * .4 * math.cos(a + 1.6), y + r * .4 * math.sin(a + 1.6)), (x - r * math.cos(a), y - r * math.sin(a)), (x - r * .4 * math.cos(a + 1.6), y - r * .4 * math.sin(a + 1.6))], fill=(255, 190, 200, 200))

# ------------------------------------------------------------------ text: captions, verse cards, titles
def stroke_text(d, xy, txt, font, fill, stroke=6, anchor='mm', shadow=True, **kw):
    if shadow: d.text((xy[0] + 4, xy[1] + 6), txt, font=font, fill=(0, 0, 0, 120), anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, 120), **kw)
    d.text(xy, txt, font=font, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(10, 6, 4, 255), **kw)

def wrap(d, txt, font, maxw):
    out, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) > maxw and cur: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out

def chunk_words(words, maxc=16):
    """Group words into caption chunks of up to ~2 short lines (the karaoke 'page')."""
    out, cur = [], []
    for w in words:
        if cur and (len(' '.join(cur + [w])) > maxc * 2 or cur[-1][-1:] in '.?!' and len(' '.join(cur)) > 6): out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return out

def draw_caption(img, line, t0, t1, tt):
    """Word-by-word karaoke caption. Words appear as spoken; current word pops in gold."""
    words = caption_text(line).split()
    if not words: return
    wts = [len(w) + 2 for w in words]; tot = sum(wts); dur = max(.1, t1 - t0)
    starts = []; acc = 0
    for wt in wts: starts.append(t0 + dur * acc / tot); acc += wt
    cur = max((i for i, s in enumerate(starts) if tt >= s - .05), default=0)
    chunks = chunk_words(words); idx = 0
    for ch in chunks:
        if idx <= cur < idx + len(ch): break
        idx += len(ch)
    d = ImageDraw.Draw(img); f = F(74, 'ExtraBold') if os.path.exists(GF + 'Poppins-ExtraBold.ttf') else F(74, 'Bold')
    lines = wrap(d, ' '.join(ch).upper(), f, 900)
    y0 = 1360 - (len(lines) - 1) * 46; k = idx
    for li, ln in enumerate(lines):
        ws = ln.split(); sp = d.textlength(' ', font=f); widths = [d.textlength(w, font=f) for w in ws]
        x = W / 2 - (sum(widths) + sp * (len(ws) - 1)) / 2
        for w, wd in zip(ws, widths):
            if k <= cur:
                pop = ease((tt - starts[k]) / .12) if k == cur else 1
                col = GOLD if k == cur else WHITE
                stroke_text(d, (x + wd / 2, y0 + li * 92 + (1 - pop) * 10), w, f, col + (255,), 7)
            else:
                stroke_text(d, (x + wd / 2, y0 + li * 92), w, f, (255, 255, 255, 70), 0, shadow=False)
            x += wd + sp; k += 1

def caption_text(s):
    for a, b in getattr(EP, 'CAPTION_FIXES', {}).items(): s = s.replace(a, b)
    return s

def verse_parts(key, ar=None, en=None):
    v = quran()['verses'][key]; words = v['ar'].split()
    a = ' '.join(words[ar[0]:ar[1]]) if ar else v['ar']
    if en:
        assert en.rstrip('.') in v['en'] + '.', f'English for {key} is not an exact excerpt of Saheeh International: {en!r}'
    e = en or v['en']
    if not e.endswith(('.', '?', '!')): e += '.'
    s, n = key.split(':'); name = quran()['surah_names'][s]
    return a, e, f'Surah {name} {key}'

def draw_verse(img, vs, tt):
    """Verse card: exact Arabic (gold) + Saheeh International (cream) + reference."""
    a, e, ref = verse_parts(vs['key'], vs.get('ar'), vs.get('en'))
    p = ease((tt - vs['_t0']) / .6)
    if p <= 0: return
    d0 = ImageDraw.Draw(img); fa = F(vs.get('ar_size', 70), 'Amiri-Bold'); fe = F(44, 'Lora-Italic-Bold'); fr = F(30, 'SemiBold')
    alines = wrap(d0, a, fa, 860); elines = wrap(d0, '“' + e + '”', fe, 860)
    hh = len(alines) * vs.get('ar_size', 70) * 1.75 + 40 + len(elines) * 60 + 80
    cy = vs.get('y', 640); y0 = cy - hh / 2
    panel = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((60, y0 - 50, W - 60, y0 + hh + 30), 40, fill=(12, 8, 6, int(150 * p)), outline=GOLD + (int(170 * p),), width=3)
    for i, ln in enumerate(alines):
        stroke_text(pd, (W / 2, y0 + 30 + i * vs.get('ar_size', 70) * 1.75), ln, fa, GOLD + (int(255 * p),), 3, direction='rtl', language='ar')
    ye = y0 + len(alines) * vs.get('ar_size', 70) * 1.75 + 30
    for i, ln in enumerate(elines):
        stroke_text(pd, (W / 2, ye + i * 60), ln, fe, CREAM + (int(255 * p),), 3)
    stroke_text(pd, (W / 2, ye + len(elines) * 60 + 30), ref.upper(), fr, (255, 210, 120, int(230 * p)), 3)
    img.alpha_composite(panel)

def draw_title(img, sc, tt):
    ti = sc['title']; p = ease(tt / .5)
    orn = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(orn); cy = 560
    for r, rot0, wdt in ((330, 0, 5), (250, 22.5, 3)):
        for rot in (0, 45):
            a0 = rot0 + rot + tt * 8
            pts = [(W / 2 + r * p * math.cos(math.radians(a0 + 90 * k)), cy + r * p * math.sin(math.radians(a0 + 90 * k))) for k in range(4)]
            od.line(pts + [pts[0]], fill=GOLD + (int(110 * p),), width=wdt)
    img.alpha_composite(orn.filter(ImageFilter.GaussianBlur(6))); img.alpha_composite(orn)
    d = ImageDraw.Draw(img)
    if ti.get('kicker'): stroke_text(d, (W / 2, 330), ti['kicker'].upper(), F(40, 'SemiBold'), GOLD + (int(255 * p),), 4)
    f = F(118, 'ExtraBold') if os.path.exists(GF + 'Poppins-ExtraBold.ttf') else F(118, 'Bold')
    ls = wrap(d, ti['text'].upper(), f, 960)
    for i, l in enumerate(ls):
        stroke_text(d, (W / 2, 450 + i * 130 + (1 - p) * 40), l, f, (WHITE if i % 2 == 0 else GOLD) + (int(255 * p),), 9)
    if ti.get('arabic'):
        stroke_text(d, (W / 2, 470 + len(ls) * 130), ti['arabic'], F(90, 'Amiri-Bold'), GOLD + (int(255 * ease((tt - .4) / .6)),), 4, direction='rtl', language='ar')

def draw_chrome(img, tt, total):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 90, 40 + 18, 90 + 18), 4, fill=GOLD)
    stroke_text(d, (72, 99), getattr(EP, 'BADGE', 'QURANIC STORY').upper(), F(30, 'SemiBold'), CREAM + (230,), 3, anchor='lm', shadow=False)
    d.rectangle((0, H - 8, W, H), fill=(0, 0, 0, 120)); d.rectangle((0, H - 8, W * tt / total, H), fill=GOLD + (255,))

def draw_end(img, sc, tt):
    e = sc['end']; d = ImageDraw.Draw(img); p = ease((tt - sc['_lines'][e.get('after', 0)][0]) / .5)
    if p <= 0: return
    f = F(64, 'Bold')
    stroke_text(d, (W / 2, 560), e.get('line1', 'Follow Quranic Story').upper(), f, GOLD + (int(255 * p),), 7)
    stroke_text(d, (W / 2, 650), e.get('line2', 'A new story every day').upper(), F(46, 'SemiBold'), WHITE + (int(255 * p),), 5)
    bx = ease((tt - sc['_lines'][e.get('after', 0)][0] - .4) / .5)
    if bx > 0:
        d.rounded_rectangle((W / 2 - 230, 730, W / 2 + 230, 830), 50, fill=(24, 119, 242, int(255 * bx)))
        stroke_text(d, (W / 2, 780), 'FOLLOW', F(52, 'Bold'), (255, 255, 255, int(255 * bx)), 0, shadow=False)

# ------------------------------------------------------------------ scenes, camera, transitions
def build_layers(sc):
    layers = []
    for spec in sc['layers']:
        fn, depth = (spec, None) if callable(spec) else spec
        p = P(); fn(p); layers.append((p.finish(), depth if depth is not None else len(layers) / max(1, len(sc['layers']) - 1)))
    return layers

def cam_view(sc, depth, u):
    """Affine for a layer at parallax depth (0 far .. 1 near), u = scene progress 0..1."""
    cam = sc.get('cam', 'in'); u = ease(u) * .85 + u * .15
    z = {'in': lerp(1.0, 1.10, u), 'out': lerp(1.10, 1.0, u)}.get(cam, 1.05)
    px = {'left': lerp(40, -40, u), 'right': lerp(-40, 40, u)}.get(cam, 0); py = {'up': lerp(70, -70, u), 'down': lerp(-70, 70, u)}.get(cam, 0)
    zl = 1 + (z - 1) * (.45 + .55 * depth); f = .35 + .65 * depth
    cx, cy = LW / 2 + px * f, LH / 2 + py * f
    return (1 / zl, 0, cx - W / 2 / zl, 0, 1 / zl, cy - H / 2 / zl)

_layer_cache = {}
def scene_frame(si, tt, tl):
    sc = SC[si]; info = tl[si]
    if si not in _layer_cache: _layer_cache.clear() if len(_layer_cache) > 2 else None; _layer_cache[si] = build_layers(sc)
    u = clamp((tt - info['start']) / max(.1, info['end'] - info['start'] + .7))
    img = None
    for lay, depth in _layer_cache[si]:
        v = lay.transform((W, H), Image.AFFINE, cam_view(sc, depth, u), Image.BILINEAR)
        img = v if img is None else Image.alpha_composite(img, v)
    if img.mode != 'RGBA': img = img.convert('RGBA')
    ts = tt - info['start']
    for fx in sc.get('fx', []):
        kind, kw = (fx, {}) if isinstance(fx, str) else fx
        fx_particles(img, kind, tt, seed=si * 7 + 3, **kw)
    img = bloom(img, sc.get('bloom', .55))
    img.alpha_composite(VIG)
    sc['_lines'] = info['lines']
    if sc.get('title') and ts < sc['title'].get('hold', 99): draw_title(img, sc, ts)
    if sc.get('verse'):
        vs = sc['verse']; vs['_t0'] = info['lines'][vs.get('line', 0)][0] - .2
        draw_verse(img, vs, tt)
    if sc.get('end'): draw_end(img, sc, tt)
    # caption of the line being spoken (skipped for lines read from a verse card, which already shows the words)
    li = max((i for i, (a, b) in enumerate(info['lines']) if tt >= a - .1), default=None)
    if li is not None and tt < info['lines'][li][1] + .35 and li not in sc.get('no_caption', ()) and not (sc.get('verse') and li == sc['verse'].get('line', 0)):
        a, b = info['lines'][li]; draw_caption(img, sc['lines'][li], a, b, tt)
    return img

def bloom(img, k):
    """Cinematic glow: blur the bright parts and screen them back on."""
    if k <= 0: return img
    sm = np.asarray(img.convert('RGB').resize((W // 4, H // 4), Image.BILINEAR)).astype(np.float32)
    lum = sm.mean(2, keepdims=True); br = sm * np.clip((lum - 140) / 115, 0, 1)
    b = Image.fromarray(br.astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
    b = b.point(lambda v: int(v * k))
    from PIL import ImageChops
    out = ImageChops.screen(img.convert('RGB'), b).convert('RGBA'); return out

def make_vignette():
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W * .75)) ** 2 + ((yy - H * .48) / (H * .62)) ** 2)
    a = np.clip((d - .55) / .6, 0, 1) ** 1.5 * 170
    bottom = np.clip((yy - H * .62) / (H * .38), 0, 1) ** 1.4 * 120
    g = np.zeros((H, W, 4), np.uint8); g[..., 3] = np.clip(a + bottom, 0, 230)
    return Image.fromarray(g, 'RGBA')
VIG = None

def star_mask(r):
    """Eight-point star (two overlapping squares) of radius r, centred on screen."""
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    for rot in (0, 45):
        pts = [(W / 2 + r * math.cos(math.radians(rot + 45 + 90 * k)), H / 2 + r * math.sin(math.radians(rot + 45 + 90 * k))) for k in range(4)]
        d.polygon(pts, fill=255)
    return m

TRANS = .6
def frame(tl, tt):
    si = next((i for i, s in enumerate(tl) if tt < s['end']), len(tl) - 1)
    img = scene_frame(si, tt, tl)
    nxt = si + 1
    if nxt < len(tl) and tt > tl[si]['end'] - TRANS:
        q = ease((tt - (tl[si]['end'] - TRANS)) / TRANS)
        img2 = scene_frame(nxt, tt, tl)
        r = q * 1500; m = star_mask(r)
        img = Image.composite(img2, img, m)
        if q < .98:
            ol = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ol)
            for rot in (0, 45):
                pts = [(W / 2 + r * math.cos(math.radians(rot + 45 + 90 * k)), H / 2 + r * math.sin(math.radians(rot + 45 + 90 * k))) for k in range(4)]
                od.line(pts + [pts[0]], fill=GOLD + (230,), width=10)
            img.alpha_composite(ol.filter(ImageFilter.GaussianBlur(3))); img.alpha_composite(ol)
    draw_chrome(img, tt, tl[-1]['end'])
    if tt < .35: img = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), img, ease(tt / .35))
    return img.convert('RGB')

# ------------------------------------------------------------------ audio
def to_phonemes(k, text, lang):
    import re
    pron = dict(PRON); pron.update(getattr(EP, 'PRON', {}))
    keys = sorted(pron, key=len, reverse=True)
    pat = re.compile(r"(?<![\w'])(" + '|'.join(re.escape(x) for x in keys) + r")(?![\w'])")
    out = []; pos = 0
    for m in pat.finditer(text):
        seg = text[pos:m.start()]
        if seg.strip(): out.append(k.tokenizer.phonemize(seg, lang))
        out.append(pron[m.group(1)])
        tail = text[m.end():m.end() + 1]
        if tail in ',.;:!?': out[-1] += tail; pos = m.end() + 1
        else: pos = m.end()
    seg = text[pos:]
    if seg.strip(): out.append(k.tokenizer.phonemize(seg, lang))
    return ' '.join(o.strip() for o in out if o.strip())

def build_audio():
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(MODELS + '/kokoro.onnx', MODELS + '/voices.bin')
    voice = getattr(EP, 'VOICE', 'bm_george'); speed = getattr(EP, 'SPEED', .9); lang = 'en-gb' if voice[:1] == 'b' else 'en-us'
    gap, sgap = .35, .75
    chunks, tl, cur = [np.zeros(int(.5 * SR), np.float32)], [], .5
    for si, sc in enumerate(SC):
        starts = []; s0 = cur
        for li, ln in enumerate(sc['lines']):
            ph = to_phonemes(k, ln, lang)
            a, sr = k.create(ph, voice=voice, speed=sc.get('speed', speed), lang=lang, is_phonemes=True); a = a.astype(np.float32)
            g = (sc.get('pause', sgap) if li == len(sc['lines']) - 1 else gap)
            starts.append((cur, cur + len(a) / SR)); chunks += [a, np.zeros(int(g * SR), np.float32)]; cur += len(a) / SR + g
        tl.append({'start': s0 if si else 0.0, 'end': cur, 'lines': starts}); print(si, round(cur, 1), flush=True)
    chunks.append(np.zeros(int(1.0 * SR), np.float32)); tl[-1]['end'] = cur + 1.0
    voice_a = np.concatenate(chunks); voice_a = voice_a / max(1e-6, np.abs(voice_a).max()) * .9
    # ambience: soft warm air (filtered noise) + a gentle whoosh at each star transition. No music.
    n = len(voice_a); rng = np.random.default_rng(7); noise = rng.standard_normal(n).astype(np.float32)
    from scipy.signal import butter, lfilter
    b, a = butter(2, 380 / (SR / 2)); amb = lfilter(b, a, noise); amb = amb / np.abs(amb).max() * .035
    amb *= (1 + .3 * np.sin(np.arange(n) / SR * .4))
    bw, aw = butter(2, [300 / (SR / 2), 2500 / (SR / 2)], 'band'); wh = lfilter(bw, aw, rng.standard_normal(int(.9 * SR)).astype(np.float32))
    env = np.sin(np.linspace(0, math.pi, len(wh))) ** 2; wh = wh / np.abs(wh).max() * .10 * env
    mix = voice_a + amb
    for s in tl[:-1]:
        i0 = int((s['end'] - TRANS) * SR); i1 = min(n, i0 + len(wh)); mix[i0:i1] += wh[:i1 - i0]
    sf.write(OUT + '/voice.wav', mix.astype(np.float32), SR); json.dump(tl, open(OUT + '/tl.json', 'w'))
    words = sum(len(l.split()) for sc in SC for l in sc['lines'])
    print(f'AUDIO {tl[-1]["end"]:.1f}s, {words} words')

# ------------------------------------------------------------------ render
def render(part, nparts):
    global VIG
    VIG = make_vignette(); tl = json.load(open(OUT + '/tl.json'))
    n = int(tl[-1]['end'] * FPS); a = n * part // nparts; b = n * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', OUT + f'/part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(tl, f / FPS).tobytes())
        if (f - a) % 300 == 0: print(part, f - a, b - a, flush=True)
    p.stdin.close(); assert p.wait() == 0

def check():
    """Static checks before rendering: verses exact, lengths sane."""
    for sc in SC:
        if sc.get('verse'): a, e, r = verse_parts(sc['verse']['key'], sc['verse'].get('ar'), sc['verse'].get('en')); print('VERSE', r, '|', e)
    words = sum(len(l.split()) for sc in SC for l in sc['lines'])
    print('scenes', len(SC), 'words', words); assert 150 <= words <= 260, 'script should be 150-260 words (~75-95 s)'

def load(path):
    global EP, SC, OUT
    import importlib.util
    spec = importlib.util.spec_from_file_location('episode', path); EP = importlib.util.module_from_spec(spec); spec.loader.exec_module(EP)
    SC = EP.SCENES
    OUT = os.path.normpath(os.path.join(HERE, '..', 'build', 'quranic', os.path.splitext(os.path.basename(path))[0])); os.makedirs(OUT, exist_ok=True)

if __name__ == '__main__':
    ep, cmd = sys.argv[1], sys.argv[2]
    load(ep)
    if cmd == 'check': check()
    if cmd == 'audio': check(); build_audio()
    if cmd == 'still':
        VIG = make_vignette(); tl = json.load(open(OUT + '/tl.json'))
        for s in sys.argv[3:]: frame(tl, float(s)).save(OUT + f'/still_{float(s):05.1f}.jpg', quality=85)
        print('stills in', OUT)
    if cmd == 'part': render(int(sys.argv[3]), int(sys.argv[4]))
    if cmd == 'render':
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), ep, 'part', str(i), '2']) for i in range(2)]
        assert all(p.wait() == 0 for p in ps), 'render failed'
        open(OUT + '/list.txt', 'w').write('file part0.mp4\nfile part1.mp4\n')
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-i', OUT + '/list.txt', '-i', OUT + '/voice.wav', '-c:v', 'copy',
                               '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-af', 'loudnorm=I=-14:TP=-1.5', '-shortest', '-movflags', '+faststart', OUT + '/video.mp4'])
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(getattr(EP, 'THUMB_AT', 1.5)), '-i', OUT + '/video.mp4', '-frames:v', '1', OUT + '/thumb.jpg'])
        print('DONE', OUT + '/video.mp4')
