"""Animated explainer engine: PIL frames + Kokoro narration + ffmpeg. See CLAUDE.md."""
import math, os, sys, subprocess, json, pickle
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S, FPS = 1920, 1080, 2, 30
BG = (14, 18, 40)
INK = (240, 243, 255)
DIM = (150, 160, 200)
CY = (64, 210, 255)
YE = (255, 200, 70)
PK = (255, 105, 150)
GR = (90, 225, 150)
PU = (150, 120, 255)
CARD = (28, 34, 68)
GF = '/usr/share/fonts/truetype/google-fonts/'
_fc = {}
MODELS = os.environ.get('KOKORO_MODELS', os.path.expanduser('~/.cache/kokoro'))
EP = None; SCENES = []; OUT = 'build'

def F(size, w='SemiBold', sc=None):
    if w == 'SemiBold': w = 'Bold'
    sc = sc or S
    k = (size, w, sc)
    if k not in _fc:
        p = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf' if w == 'Mono' else f'{GF}Poppins-{w}.ttf'
        _fc[k] = ImageFont.truetype(p, int(size * sc))
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return x * x * (3 - 2 * x)
def fd(t, start=0.0, dur=0.45): return ease((t - start) / dur)
def mix(c, a, bg=BG):
    a = clamp(a); return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))

class C:
    """Drawing context in logical 1920x1080 units."""
    def __init__(s, img, k=None): s.img = img; s.d = ImageDraw.Draw(img); s.k = k or S
    def text(s, x, y, t, size=48, col=INK, a=1.0, anchor='mm', w='SemiBold', bg=BG, stroke=0, stroke_fill=(6, 8, 20)):
        if a <= 0.01 or not t: return
        s.d.text((x * s.k, y * s.k), t, font=F(size, w, s.k), fill=mix(col, a, bg), anchor=anchor, stroke_width=int(stroke * s.k), stroke_fill=stroke_fill)
    def tw(s, t, size, w='SemiBold'): return s.d.textlength(t, font=F(size, w, s.k)) / s.k
    def rr(s, x0, y0, x1, y1, r=24, fill=CARD, a=1.0, outline=None, ow=3, bg=BG):
        if a <= 0.01: return
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        s.d.rounded_rectangle((x0 * s.k, y0 * s.k, x1 * s.k, y1 * s.k), r * s.k,
                              fill=mix(fill, a, bg) if fill else None,
                              outline=mix(outline, a, bg) if outline else None, width=int(ow * s.k))
    def circ(s, x, y, r, fill=None, a=1.0, outline=None, ow=3, bg=BG):
        if a <= 0.01 or r <= 0: return
        s.d.ellipse(((x - r) * s.k, (y - r) * s.k, (x + r) * s.k, (y + r) * s.k),
                    fill=mix(fill, a, bg) if fill else None,
                    outline=mix(outline, a, bg) if outline else None, width=int(ow * s.k))
    def line(s, pts, col=INK, w=4, a=1.0, bg=BG):
        if a <= 0.01 or len(pts) < 2: return
        s.d.line([(x * s.k, y * s.k) for x, y in pts], fill=mix(col, a, bg), width=max(1, int(w * s.k)), joint='curve')
    def check(s, x, y, r, col=GR, a=1.0, p=1.0):
        pts = [(x - r * .55, y), (x - r * .12, y + r * .42), (x + r * .6, y - r * .45)]
        if p < 0.5:
            q = p / 0.5; pts = [pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * q, pts[0][1] + (pts[1][1] - pts[0][1]) * q)]
        elif p < 1:
            q = (p - .5) / .5; pts = [pts[0], pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)]
        s.line(pts, col, r * .22, a)
    def cross(s, x, y, r, col=PK, a=1.0):
        s.line([(x - r * .5, y - r * .5), (x + r * .5, y + r * .5)], col, r * .22, a)
        s.line([(x - r * .5, y + r * .5), (x + r * .5, y - r * .5)], col, r * .22, a)
    def arrow(s, x0, y0, x1, y1, col=DIM, w=4, a=1.0, head=16):
        s.line([(x0, y0), (x1, y1)], col, w, a)
        ang = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6):
            s.line([(x1, y1), (x1 + head * math.cos(ang + da), y1 + head * math.sin(ang + da))], col, w, a)

def typed(txt, p): return txt[:int(len(txt) * clamp(p))]

def wrap(c, txt, size, maxw, w='Medium'):
    out, cur = [], ''
    for word in txt.split():
        t = (cur + ' ' + word).strip()
        if c.tw(t, size, w) > maxw and cur: out.append(cur); cur = word
        else: cur = t
    if cur: out.append(cur)
    return out

GAP, SCENE_GAP, SR = 0.38, 0.9, 24000

def build_audio():
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(MODELS + '/kokoro.onnx', MODELS + '/voices.bin')
    chunks, tl, cur = [np.zeros(int(.6 * SR), np.float32)], [], .6
    for si, (_, lines, _) in enumerate(SCENES):
        starts = []; s0 = cur
        for li, ln in enumerate(lines):
            a, sr = k.create(ln, voice=getattr(EP, 'VOICE', 'am_michael'), speed=getattr(EP, 'SPEED', 0.96), lang='en-us'); a = a.astype(np.float32)
            g = SCENE_GAP if li == len(lines) - 1 else GAP
            starts.append((cur, cur + len(a) / SR)); chunks += [a, np.zeros(int(g * SR), np.float32)]
            cur += len(a) / SR + g
        tl.append({'start': s0 if si else 0.0, 'end': cur, 'lines': starts}); print(si, round(cur, 1), flush=True)
    chunks.append(np.zeros(int(1.2 * SR), np.float32)); tl[-1]['end'] = cur + 1.2
    au = np.concatenate(chunks); au = au / max(1e-6, np.abs(au).max()) * .9
    sf.write(OUT + '/voice_dry.wav', au, SR); json.dump(tl, open(OUT + '/tl.json', 'w'))
    mix_audio()

def mix_audio():
    """Narration + soft ambient pad + scene whooshes + low hits. Writes voice.wav (the track the render uses)."""
    import soundfile as sf
    v, sr = sf.read(OUT + '/voice_dry.wav', dtype='float32'); tl = json.load(open(OUT + '/tl.json')); n = len(v)
    rng = np.random.default_rng(3); pad = np.zeros(n, np.float32); sfx = np.zeros(n, np.float32)
    chords = [[110.0, 164.81, 220.0, 261.63, 329.63], [87.31, 130.81, 220.0, 261.63, 349.23],
              [130.81, 196.0, 261.63, 329.63, 392.0], [98.0, 146.83, 246.94, 293.66, 392.0]]
    seg, xf = 8.0, 3.0
    for k in range(int(n / SR / seg) + 2):
        t0 = k * seg - xf / 2; i0, i1 = max(0, int(t0 * SR)), min(n, int((t0 + seg + xf) * SR))
        if i1 <= i0: continue
        t = np.arange(i0, i1) / SR
        env = np.clip((t - t0) / xf, 0, 1) * np.clip((t0 + seg + xf - t) / xf, 0, 1); env = env * env * (3 - 2 * env)
        for j, f in enumerate(chords[k % 4]):
            amp = 1 / (1 + j * .3); ph = rng.uniform(0, 6.28)
            w = np.sin(2 * np.pi * f * t + ph) + .5 * np.sin(2 * np.pi * f * 1.003 * t) + .12 * np.sin(4 * np.pi * f * t)
            pad[i0:i1] += (amp * env * w * (1 + .15 * np.sin(2 * np.pi * .11 * t + j))).astype(np.float32)
    tt = np.arange(n) / SR
    pad *= np.clip(tt / 2.0, 0, 1) * np.clip((n / SR - tt) / 3.0, 0, 1)
    pad *= getattr(EP, 'MUSIC_LEVEL', 0.014) / max(1e-9, float(np.sqrt(np.mean(pad ** 2))))
    def add(sig, at):
        i = int(at * SR)
        if i < 0: sig = sig[-i:]; i = 0
        m = min(len(sig), n - i)
        if m > 0: sfx[i:i + m] += sig[:m]
    for sc in tl[1:]:                                   # soft whoosh on every scene change
        m = int(.8 * SR); u = np.arange(m) / m
        w = np.convolve(rng.standard_normal(m + 40), np.ones(28) / 28, 'same')[:m]
        add((w / np.abs(w).max() * np.sin(np.pi * u) ** 3 * .05).astype(np.float32), sc['start'] - .45)
    for (si, li, off) in getattr(EP, 'HITS', []):       # deep cinematic hit on key reveals
        m = int(1.6 * SR); u = np.arange(m) / SR
        h = (np.sin(2 * np.pi * 55 * u) + .6 * np.sin(2 * np.pi * 82.4 * u)) * np.exp(-u * 3.2) * np.clip(u / .012, 0, 1)
        add((h * .16).astype(np.float32), tl[si]['lines'][li][0] + off)
    out = v + pad + sfx; pk = float(np.abs(out).max())
    if pk > .97: out *= .97 / pk
    sf.write(OUT + '/voice.wav', out, SR)
    r = lambda x: 20 * np.log10(max(1e-9, float(np.sqrt(np.mean(x ** 2)))))
    print(f'audio mix: voice {r(v):.1f} dB, music {r(pad):.1f} dB, sfx peak {float(np.abs(sfx).max()):.3f}, final peak {float(np.abs(out).max()):.2f}')

def background():
    y = np.linspace(0, 1, H * S)[:, None]; x = np.linspace(0, 1, W * S)[None, :]
    g = 1 - .35 * ((x - .5) ** 2 + (y - .45) ** 2) * 2
    arr = np.stack([np.clip(BG[i] * g + (8 if i == 2 else 0) * (1 - y), 0, 255) for i in range(3)], -1).astype(np.uint8)
    return Image.fromarray(arr)

_FX = {}
def fx_init():
    """Precomputed light layers: drifting colour haze, bokeh dots, vignette, film grain, bloom curve."""
    from PIL import ImageFilter
    rng = np.random.default_rng(7); AW, AH = W + 480, H + 270
    sm = Image.new('RGB', (AW // 8, AH // 8)); d = ImageDraw.Draw(sm)
    for col, k in ((PU, 6), (CY, 5), (PK, 3)):
        for _ in range(k):
            x, y, r = rng.uniform(0, AW / 8), rng.uniform(0, AH / 8), rng.uniform(24, 58)
            d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * rng.uniform(.10, .21)) for v in col))
    _FX['haze'] = sm.filter(ImageFilter.GaussianBlur(26)).resize((AW, AH), Image.BICUBIC)
    bk = Image.new('RGB', (AW // 2, AH // 2)); d = ImageDraw.Draw(bk)
    for _ in range(90):
        x, y, r = rng.uniform(0, AW / 2), rng.uniform(0, AH / 2), rng.uniform(1.5, 7)
        g = int(rng.uniform(22, 60)); d.ellipse((x - r, y - r, x + r, y + r), fill=(int(g * .7), int(g * .9), g))
    _FX['bokeh'] = bk.filter(ImageFilter.GaussianBlur(2.2)).resize((AW, AH), Image.BICUBIC)
    yy, xx = np.mgrid[0:H, 0:W]; rr = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = Image.fromarray(np.clip(255 * (1 - .42 * np.clip(rr - .35, 0, 2) ** 1.6), 90, 255).astype(np.uint8))
    _FX['vig'] = Image.merge('RGB', [v, v, v])
    _FX['grain'] = [Image.merge('RGB', [Image.fromarray(np.clip(128 + rng.normal(0, 4.5, (H, W)), 0, 255).astype(np.uint8))] * 3) for _ in range(5)]
    _FX['lut'] = [int(min(255, max(0, (i - 105) * 1.5))) for i in range(256)] * 3
    _FX['blur'] = ImageFilter.GaussianBlur(7)

def post(out, tt, strength=1.0):
    from PIL import ImageChops
    if not _FX: fx_init()
    glow = out.resize((W // 4, H // 4), Image.BILINEAR).point(_FX['lut']).filter(_FX['blur']).resize((W, H), Image.BILINEAR)
    out = ImageChops.screen(out, glow)
    for key, sp, ph in (('haze', .05, 0.0), ('bokeh', .085, 1.7)):
        ox = int(240 + 235 * math.sin(tt * sp + ph)); oy = int(135 + 130 * math.cos(tt * sp * .74 + ph))
        out = ImageChops.screen(out, _FX[key].crop((ox, oy, ox + W, oy + H)))
    return ImageChops.multiply(out, _FX['vig'])

def draw_caption(c, text, a, b, tt, y=968, size=46):
    """Karaoke-style caption: the word being spoken lights up."""
    words = text.split(); lines, cur = [], []
    for w in words:
        if cur and c.tw(' '.join(cur + [w]), size, 'Bold') > 1450: lines.append(cur); cur = [w]
        else: cur.append(w)
    if cur: lines.append(cur)
    total = sum(len(w) + 1 for w in words); pos = clamp((tt - a) / max(.2, b - a)) * total; done = 0; sp = c.tw(' ', size, 'Bold')
    for j, ln in enumerate(lines):
        wd = [c.tw(w, size, 'Bold') for w in ln]; x = W / 2 - (sum(wd) + sp * (len(ln) - 1)) / 2; yy = y + (j - (len(lines) - 1) / 2) * 62
        for w, ww in zip(ln, wd):
            st = done + len(w) + 1
            col = YE if done <= pos < st else (INK if pos >= st else (165, 174, 212))
            c.text(x, yy, w, size, col, 1, 'lm', 'Bold', stroke=4)
            x += ww + sp; done = st

def frame(tl, bg, tt):
    si = next((i for i, s in enumerate(tl) if tt < s['end']), len(tl) - 1)
    sc = tl[si]; ch, lines, fn = SCENES[si]
    img = bg.copy(); c = C(img)
    def T(i, off=0.0):
        return tt - sc['lines'][i][0] - off if i < len(sc['lines']) else -99
    fn(c, T, tt - sc['start'])
    out = img.reduce(S)
    # camera: slow push-in through the scene, plus a settle-in on every cut
    t_in, t_out = tt - sc['start'], sc['end'] - tt
    z = 1.0 + .045 * clamp(t_in / max(1, sc['end'] - sc['start'])) + .12 * (1 - ease(t_in / .55)) ** 2
    if z > 1.0005:
        out = out.transform((W, H), Image.AFFINE, (1 / z, 0, W / 2 * (1 - 1 / z), 0, 1 / z, H / 2 * (1 - 1 / z)), Image.BICUBIC)
    out = post(out, tt)
    edge = min(t_in, t_out)
    if edge < .35: out = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), out, ease(edge / .35))
    # crisp overlay: chapter label, title, karaoke captions, progress bar
    c = C(out, 1)
    c.d.rectangle((70, 64, 77, 108), fill=CY); c.text(100, 86, ch, 30, (190, 198, 230), 1, 'lm', 'Medium', stroke=2)
    c.text(1850, 86, EP.SHORT_TITLE, 26, (150, 160, 200), 1, 'rm', 'Regular', stroke=2)
    li = max((i for i, (a, b) in enumerate(sc['lines']) if tt >= a - .08), default=None)
    if li is not None and tt < sc['lines'][li][1] + .25:
        a, b = sc['lines'][li]; draw_caption(c, caption(lines[li]), a, b, tt)
    tot = tl[-1]['end']
    c.d.rectangle((0, 1072, 1920, 1080), fill=(24, 28, 58)); c.d.rectangle((0, 1072, int(1920 * tt / tot), 1080), fill=CY)
    from PIL import ImageChops
    return out   # film grain is left off: per-frame noise multiplies the file size ~50x

def make_thumb():
    """Bold 1280x720 thumbnail from EP.THUMB lines (+ optional EP.thumb_art(c) drawing on the right third)."""
    lines = getattr(EP, 'THUMB', None)
    if not lines: return False
    img = background(); c = C(img)
    art = getattr(EP, 'thumb_art', None)
    if art: art(c)
    size = 190
    while max(c.tw(l, size, 'Bold') for l in lines) > (1040 if art else 1700): size -= 6
    y0 = 540 - (len(lines) - 1) * size * .58
    for i, l in enumerate(lines):
        c.text(90, y0 + i * size * 1.16, l, size, YE if i == len(lines) - 1 else INK, 1, 'lm', 'Bold', stroke=6)
    yb = y0 + (len(lines) - 1) * size * 1.16 + size * .62; c.rr(90, yb, 410, yb + 14, 6, CY)
    post(img.reduce(S), 4.0).resize((1280, 720), Image.LANCZOS).save(OUT + '/thumb.jpg', quality=92)
    return True

def render(part, nparts):
    tl = json.load(open(OUT + '/tl.json')); bg = background()
    n = int(tl[-1]['end'] * FPS); a = n * part // nparts; b = n * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', OUT + f'/part{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(frame(tl, bg, f / FPS).tobytes())
        if (f - a) % 300 == 0: print(part, f - a, b - a, flush=True)
    p.stdin.close(); p.wait()

def build_short(max_len=55.0):
    """Vertical 1080x1920 Short: the opening scenes (hook) of the finished video inside a branded frame."""
    global W, H
    tl = json.load(open(OUT + '/tl.json'))
    ends = [sc['end'] for sc in tl if sc['end'] <= max_len]
    end = ends[-1] if ends else min(max_len, tl[0]['end'])
    w0, h0 = W, H; W, H = 1080, 1920
    img = background(); c = C(img)
    head = getattr(EP, 'SHORT_HOOK', EP.SHORT_TITLE)
    ls = wrap(c, head, 92, 940, 'Bold'); y0 = 400 - (len(ls) - 1) * 56
    for i, l in enumerate(ls): c.text(540, y0 + i * 112, l, 92, INK if i % 2 == 0 else CY, w='Bold')
    c.line([(400, 590), (680, 590)], YE, 8)
    c.rr(22, 661, 1058, 1259, 24, CARD, outline=(44, 52, 100), ow=4)
    c.text(540, 1420, 'Full video on the channel', 56, INK, w='Bold')
    c.rr(300, 1520, 780, 1640, 60, (235, 50, 60)); c.text(540, 1580, 'SUBSCRIBE', 54, INK, w='Bold', bg=(235, 50, 60))
    c.text(540, 1720, getattr(EP, 'CHANNEL', 'Md Juman Hussan JP'), 40, CY, w='Medium')
    img.reduce(S).save(OUT + '/short_bg.png'); W, H = w0, h0
    fo = max(0.0, end - 0.4)
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', str(FPS), '-i', OUT + '/short_bg.png', '-t', f'{end:.2f}', '-i', OUT + '/video.mp4',
        '-filter_complex', f'[1:v]scale=1000:-2[v];[0:v][v]overlay=40:(1920-562)/2:shortest=1,fade=t=out:st={fo:.2f}:d=0.4[o];[1:a]afade=t=out:st={fo:.2f}:d=0.4[a]',
        '-map', '[o]', '-map', '[a]', '-t', f'{end:.2f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
        '-movflags', '+faststart', OUT + '/short.mp4'])
    print('DONE', OUT + '/short.mp4', f'{end:.1f}s')

def caption(s):
    for a, b in getattr(EP, 'CAPTION_FIXES', {}).items(): s = s.replace(a, b)
    return s

def load(path):
    global EP, SCENES, OUT
    import importlib.util
    spec = importlib.util.spec_from_file_location('episode', path); EP = importlib.util.module_from_spec(spec); spec.loader.exec_module(EP)
    SCENES = EP.SCENES; OUT = os.path.join(os.path.dirname(os.path.abspath(path)), '..', 'build', os.path.splitext(os.path.basename(path))[0])
    OUT = os.path.normpath(OUT); os.makedirs(OUT, exist_ok=True)

if __name__ == '__main__':
    # usage: python3 pipeline/engine.py episodes/NAME.py audio | still T1 T2 ... | render | short | all
    ep, cmd = sys.argv[1], sys.argv[2]
    load(ep)
    if cmd in ('audio', 'all'): build_audio()
    if cmd == 'still':
        tl = json.load(open(OUT + '/tl.json')); bg = background()
        for s in sys.argv[3:]: frame(tl, bg, float(s)).save(OUT + f'/still_{float(s):06.1f}.png')
    if cmd == 'mix': mix_audio()
    if cmd == 'thumb': make_thumb()
    if cmd == 'short': build_short()
    if cmd == 'part': render(int(sys.argv[3]), int(sys.argv[4]))
    if cmd in ('render', 'all'):
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), ep, 'part', str(i), '2']) for i in range(2)]
        assert all(p.wait() == 0 for p in ps), 'render failed'
        open(OUT + '/list.txt', 'w').write("file part0.mp4\nfile part1.mp4\n")
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-i', OUT + '/list.txt', '-i', OUT + '/voice.wav', '-c:v', 'copy',
                               '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-af', 'loudnorm=I=-16:TP=-1.5', '-shortest', '-movflags', '+faststart', OUT + '/video.mp4'])
        if not make_thumb():
            subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(getattr(EP, 'THUMB_AT', 3)), '-i', OUT + '/video.mp4', '-frames:v', '1', OUT + '/thumb.jpg'])
        print('DONE', OUT + '/video.mp4')
