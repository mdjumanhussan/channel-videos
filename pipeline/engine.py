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

def F(size, w='SemiBold'):
    if w == 'SemiBold': w = 'Bold'
    k = (size, w)
    if k not in _fc:
        p = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf' if w == 'Mono' else f'{GF}Poppins-{w}.ttf'
        _fc[k] = ImageFont.truetype(p, int(size * S))
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return x * x * (3 - 2 * x)
def fd(t, start=0.0, dur=0.45): return ease((t - start) / dur)
def mix(c, a, bg=BG):
    a = clamp(a); return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))

class C:
    """Drawing context in logical 1920x1080 units."""
    def __init__(s, img): s.img = img; s.d = ImageDraw.Draw(img)
    def text(s, x, y, t, size=48, col=INK, a=1.0, anchor='mm', w='SemiBold', bg=BG):
        if a <= 0.01 or not t: return
        s.d.text((x * S, y * S), t, font=F(size, w), fill=mix(col, a, bg), anchor=anchor)
    def tw(s, t, size, w='SemiBold'): return s.d.textlength(t, font=F(size, w)) / S
    def rr(s, x0, y0, x1, y1, r=24, fill=CARD, a=1.0, outline=None, ow=3, bg=BG):
        if a <= 0.01: return
        x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); r = min(r, (x1 - x0) / 2, (y1 - y0) / 2)
        s.d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), r * S,
                              fill=mix(fill, a, bg) if fill else None,
                              outline=mix(outline, a, bg) if outline else None, width=int(ow * S))
    def circ(s, x, y, r, fill=None, a=1.0, outline=None, ow=3, bg=BG):
        if a <= 0.01 or r <= 0: return
        s.d.ellipse(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S),
                    fill=mix(fill, a, bg) if fill else None,
                    outline=mix(outline, a, bg) if outline else None, width=int(ow * S))
    def line(s, pts, col=INK, w=4, a=1.0, bg=BG):
        if a <= 0.01 or len(pts) < 2: return
        s.d.line([(x * S, y * S) for x, y in pts], fill=mix(col, a, bg), width=max(1, int(w * S)), joint='curve')
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
    sf.write(OUT + '/voice.wav', au, SR); json.dump(tl, open(OUT + '/tl.json', 'w'))

def background():
    y = np.linspace(0, 1, H * S)[:, None]; x = np.linspace(0, 1, W * S)[None, :]
    g = 1 - .35 * ((x - .5) ** 2 + (y - .45) ** 2) * 2
    arr = np.stack([np.clip(BG[i] * g + (8 if i == 2 else 0) * (1 - y), 0, 255) for i in range(3)], -1).astype(np.uint8)
    return Image.fromarray(arr)

def frame(tl, bg, tt):
    si = next((i for i, s in enumerate(tl) if tt < s['end']), len(tl) - 1)
    sc = tl[si]; ch, lines, fn = SCENES[si]
    img = bg.copy(); c = C(img)
    def T(i, off=0.0):
        return tt - sc['lines'][i][0] - off if i < len(sc['lines']) else -99
    fn(c, T, tt - sc['start'])
    # chrome
    c.rr(70, 62, 78, 110, 4, CY); c.text(100, 86, ch, 30, DIM, 1, 'lm', 'Medium')
    c.text(1850, 86, EP.SHORT_TITLE, 26, DIM, .7, 'rm', 'Regular')
    li = max((i for i, (a, b) in enumerate(sc['lines']) if tt >= a - .12), default=None)
    if li is not None and tt < sc['lines'][li][1] + .3:
        a, b = sc['lines'][li]; ca = fd(tt, a - .12, .2)
        ls = wrap(c, caption(lines[li]), 40, 1500)
        for j, l in enumerate(ls):
            c.text(960, 965 + (j - (len(ls) - 1) / 2) * 54, l, 40, INK, ca * .95, w='Medium')
    tot = tl[-1]['end']
    c.rr(0, 1070, 1920, 1080, 0, (30, 36, 72)); c.rr(0, 1070, 1920 * tt / tot, 1080, 0, CY)
    # scene crossfade
    edge = min(tt - sc['start'], sc['end'] - tt)
    out = img.reduce(S)
    if edge < .3 and not (si == 0 and tt < 1):
        out = Image.blend(Image.new('RGB', (W, H), BG), out, .25 + .75 * ease(edge / .3))
    return out

def render(part, nparts):
    tl = json.load(open(OUT + '/tl.json')); bg = background()
    n = int(tl[-1]['end'] * FPS); a = n * part // nparts; b = n * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', OUT + f'/part{part}.mp4'], stdin=subprocess.PIPE)
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
    if cmd == 'short': build_short()
    if cmd == 'part': render(int(sys.argv[3]), int(sys.argv[4]))
    if cmd in ('render', 'all'):
        ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), ep, 'part', str(i), '2']) for i in range(2)]
        assert all(p.wait() == 0 for p in ps), 'render failed'
        open(OUT + '/list.txt', 'w').write("file part0.mp4\nfile part1.mp4\n")
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-i', OUT + '/list.txt', '-i', OUT + '/voice.wav', '-c:v', 'copy',
                               '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-af', 'loudnorm=I=-16:TP=-1.5', '-shortest', '-movflags', '+faststart', OUT + '/video.mp4'])
        subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(getattr(EP, 'THUMB_AT', 3)), '-i', OUT + '/video.mp4', '-frames:v', '1', OUT + '/thumb.png'])
        print('DONE', OUT + '/video.mp4')
