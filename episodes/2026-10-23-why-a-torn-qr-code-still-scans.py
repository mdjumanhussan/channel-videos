"""Episode: You Can Tear a QR Code and It Still Scans. Here's How"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Why Torn QR Codes Still Scan"          # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                  # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why does a torn QR code still scan?"     # headline on the vertical Short
HITS = [(0, 2, 0.0), (4, 3, 0.0), (6, 2, 0.0)]          # title card, the rebuild, quiz answer
THUMB = ['CORNER TORN OFF?', 'IT STILL', 'SCANS']
MUSIC_LEVEL = 0.006                                     # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                          # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.4, (4, 3): 0.8, (6, 2): 0.6}
SHORT_PAUSES = {(0, 2): 0.4, (1, 3): 0.6}
CAPTION_FIXES = {'one, one, three, one, one': '1:1:3:1:1', 'nineteen ninety-four': '1994',
                 'seven percent': '7%', 'thirty percent': '30%', 'fifteen percent': '15%',
                 'about twenty characters': 'about 20 characters'}

PAPER = (236, 239, 250); DOT = (16, 20, 44); TEAL = (40, 200, 190); COFFEE = (150, 96, 60)
TABLE = (92, 64, 48); SPARE = YE; MSG = CY

# ---------------------------------------------------------------- the QR drawing (simplified, not a real code)
N = 25
def _grid():
    rng = np.random.default_rng(1994)
    g = (rng.random((N, N)) < .48).astype(int); fn = np.zeros((N, N), bool)
    def finder(r0, c0):
        for r in range(-1, 8):
            for cc in range(-1, 8):
                r1, c1 = r0 + r, c0 + cc
                if 0 <= r1 < N and 0 <= c1 < N:
                    fn[r1, c1] = True
                    ring = max(abs(r - 3), abs(cc - 3))
                    g[r1, c1] = 1 if ring in (0, 1, 3) else 0
                    if r in (-1, 7) or cc in (-1, 7): g[r1, c1] = 0
    finder(0, 0); finder(0, N - 7); finder(N - 7, 0)
    for k in range(8, N - 8):
        g[6, k] = g[k, 6] = (k + 1) % 2; fn[6, k] = fn[k, 6] = True
    for r in range(5):
        for cc in range(5):
            ring = max(abs(r - 2), abs(cc - 2)); g[N - 9 + r, N - 9 + cc] = 1 if ring in (0, 2) else 0; fn[N - 9 + r, N - 9 + cc] = True
    return g, fn
GRID, FUNC = _grid()

def qr(c, x, y, size, a=1.0, bg=BG, gone=None, fix=None, fixp=0.0, hot=None, hotcol=YE, hota=0.0, finders=0.0, paper=True):
    """QR drawing centred at (x, y). gone(r, k) -> True hides a module (damage); fix(r, k) -> True marks
    modules rebuilt in green as fixp goes 0..1; hot(r, k) highlights modules in hotcol."""
    if a <= 0.01: return
    q = size / (N + 4); x0, y0 = x - size / 2 + 2 * q, y - size / 2 + 2 * q
    if paper: c.rr(x - size / 2, y - size / 2, x + size / 2, y + size / 2, q * .8, PAPER, a, bg=bg)
    pb = PAPER if paper else bg
    for r in range(N):
        for k in range(N):
            if gone and gone(r, k): continue
            col = DOT
            if hot and hota > 0 and hot(r, k): col = mix(hotcol, hota, DOT) if GRID[r, k] else mix(hotcol, hota * .25, PAPER)
            elif finders > 0 and FUNC[r, k] and (r < 8 and k < 8 or r < 8 and k > N - 9 or r > N - 9 and k < 8):
                col = mix(PK, finders, DOT) if GRID[r, k] else None
            if GRID[r, k] or (hot and hota > 0 and hot(r, k)):
                if col is None: continue
                c.d.rectangle(((x0 + k * q) * c.k, (y0 + r * q) * c.k, (x0 + (k + 1) * q) * c.k + 1, (y0 + (r + 1) * q) * c.k + 1), fill=mix(col, a, pb))
    if fix and fixp > 0:
        for r in range(N):
            for k in range(N):
                if fix(r, k) and GRID[r, k] and clamp(fixp * 1.6 - ((r * 7 + k * 3) % 11) / 18) > 0:
                    p = clamp(fixp * 1.6 - ((r * 7 + k * 3) % 11) / 18)
                    c.d.rectangle(((x0 + k * q) * c.k, (y0 + r * q) * c.k, (x0 + (k + 1) * q) * c.k + 1, (y0 + (r + 1) * q) * c.k + 1), fill=mix(GR, a * p, PAPER))
    return x0, y0, q

def tear(c, x, y, size, p, a=1.0, bg=BG, corner='br', depth=.3):
    """Rip a corner off the paper: covers it with a jagged background-coloured patch. Returns the grid test."""
    if p <= 0.01 or a <= .01: return None
    d = size * depth * clamp(p)
    sx, sy = (1 if 'r' in corner else -1), (1 if 'b' in corner else -1)
    cx, cy = x + sx * size / 2, y + sy * size / 2
    pts = [(cx + sx * 10, cy - sy * (d * 1.15)), (cx + sx * 10, cy + sy * 10), (cx - sx * (d * 1.15), cy + sy * 10)]
    jag = []
    for i in range(9):
        u = i / 8; jx = cx - sx * d * 1.15 * u + sx * 0; jy = cy - sy * d * 1.15 * (1 - u)
        off = (9 if i % 2 else -9)
        jag.append((jx - sx * off * .7, jy - sy * off * .7))
    poly = [pts[1], pts[0]] + jag + [pts[2]]
    c.d.polygon([(px * c.k, py * c.k) for px, py in poly], fill=mix(bg, a, bg))
    c.line(jag, (200, 205, 225), 3, a * .8, bg)
    q = size / (N + 4); x0, y0 = x - size / 2 + 2 * q, y - size / 2 + 2 * q
    def gone(r, k):
        mx, my = x0 + (k + .5) * q, y0 + (r + .5) * q
        return sx * (mx - cx) * -1 + sy * (my - cy) * -1 < d * 1.15 - 6
    return gone

def phone(c, x, y, h, a=1.0, t=0.0, ok=0.0, bg=BG, scan=True):
    if a <= 0.01: return
    w = h * .5
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, w * .16, (40, 46, 84), a, outline=INK, ow=5, bg=bg)
    c.rr(x - w * .4, y - h * .4, x + w * .4, y + h * .38, w * .08, (22, 26, 52), a, bg=(40, 46, 84))
    if scan and ok < .5:
        yy = y - h * .3 + h * .6 * (.5 + .5 * math.sin(t * 3))
        c.line([(x - w * .32, yy), (x + w * .32, yy)], CY, 4, a, (22, 26, 52))
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx, cy = x + sx * w * .3, y + sy * h * .28
                c.line([(cx, cy - sy * h * .07), (cx, cy), (cx - sx * w * .14, cy)], INK, 4, a, (22, 26, 52))
    if ok > .01:
        c.circ(x, y - h * .05, w * .26, GR, a * ok, bg=(22, 26, 52))
        c.check(x, y - h * .05, w * .3, BG, a * ok, fd(ok, .2, .8))

def stain(c, x, y, r, p, a=1.0, bg=PAPER):
    if p <= .01: return
    c.circ(x, y, r * clamp(p), mix(COFFEE, .75, bg), a, bg=bg)
    c.circ(x, y, r * clamp(p), None, a, outline=mix(COFFEE, 1, bg), ow=7, bg=bg)

def stain_gone(x, y, size, sx_, sy_, r):
    q = size / (N + 4); x0, y0 = x - size / 2 + 2 * q, y - size / 2 + 2 * q
    return lambda rr_, k: (x0 + (k + .5) * q - sx_) ** 2 + (y0 + (rr_ + .5) * q - sy_) ** 2 < r * r

def byte_box(c, x, y, w, h, txt, col, a=1.0, bg=BG, size=30, tcol=BG):
    if a <= 0.01: return
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 12, col, a, bg=bg)
    if txt: c.text(x, y, txt, size, tcol, a, w='Bold', bg=col)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def cup(c, x, y, s, a=1.0, bg=PAPER):
    if a <= 0.01: return
    c.circ(x + s * .9, y, s * .35, None, a, outline=COFFEE, ow=max(3, s * .14), bg=bg)
    c.rr(x - s * .8, y - s * .7, x + s * .8, y + s * .8, s * .2, COFFEE, a, bg=bg)

def thumb_art(c):
    qr(c, 1500, 470, 560, 1, finders=0)
    g = tear(c, 1500, 470, 560, 1, 1, BG, 'br', .42)
    phone(c, 1270, 700, 300, 1, 0, ok=1)

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(2), 1.2, .5)
    if a > 0:
        # a café table card with a QR sticker; the corner rips, then coffee spills, and the phone still scans it
        c.rr(330, 200, 1010, 860, 30, TABLE, a)
        c.text(670, 255, 'SCAN FOR MENU', 40, PAPER, a, w='Bold', bg=TABLE)
        qx, qy, qs = 670, 560, 470
        sp = fd(T(1), .1, 1.2) if T(1) > -.1 else 0.0
        sg = stain_gone(qx, qy, qs, qx - 110, qy - 60, 95 * sp) if sp > 0 else None
        qr(c, qx, qy, qs, a, bg=TABLE, gone=sg)
        stain(c, qx - 110, qy - 60, 95, sp, a, PAPER)
        tear(c, qx, qy, qs, fd(t, 0, .9), a, TABLE, 'br', .3)
        ok = fd(T(0), 1.6, .5) * (1 - fd(T(1), 0, .3)) + fd(T(1), 1.6, .5)
        phone(c, 1400, 520, 520, a, t, ok=ok)
        c.text(1400, 840, 'menu opened', 40, GR, a * ok, w='Bold')
        c.text(960, 120, 'Torn. Still scans.', 66, INK, a * (1 - hl(1)), w='Bold')
        c.text(960, 120, 'Coffee on it. Still scans.', 66, YE, a * hl(1), w='Bold')
    if T(2) > 1.0:
        m = fd(T(2), 1.4, .7)
        c.text(960, 330 + 30 * (1 - m), 'The Code That', 120, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'Repairs Itself', 120, YE, m, w='Bold')
        c.line([(960 - 320 * m, 590), (960 + 320 * m, 590)], CY, 8, m)
        c.text(960, 680, 'Why a damaged QR code still scans', 46, DIM, fd(T(2), 2.0), w='Medium')

def s_origin(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Made to track car parts, 1994', 60, INK, hl(0), w='Bold')
    # barcode
    k1 = hl(1)
    if k1 > 0:
        bx, by = 560, 480
        c.rr(bx - 300, by - 200, bx + 300, by + 200, 26, PAPER, k1)
        rng = np.random.default_rng(5); x = bx - 250
        while x < bx + 240:
            w = int(rng.integers(1, 4)) * 6
            c.d.rectangle((x * c.k, (by - 150) * c.k, (x + w) * c.k, (by + 110) * c.k), fill=mix(DOT, k1, PAPER)); x += w + int(rng.integers(1, 4)) * 6
        c.text(bx, by + 155, '1 direction', 32, DOT, k1, w='Bold', bg=PAPER)
        c.text(bx, 740, 'about 20 characters', 44, PK, k1 * fd(T(1), .6), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        qr(c, 1360, 480, 400, k2)
        c.arrow(1360 - 230, 290, 1360 + 230, 290, CY, 5, k2, 18)
        c.arrow(1130, 290, 1130, 690, CY, 5, k2, 18)
        c.text(1360, 740, 'up to 7,089 digits', 44, GR, k2 * fd(T(2), .8), w='Bold')
        c.text(1360, 790, '(largest size, level L)', 28, DIM, k2 * fd(T(2), .8), w='Medium')
        c.text(1360, 840, '2 directions', 32, CY, k2, w='Bold')
    if k1 > 0 and k2 > 0: c.arrow(900, 480, 1040, 480, YE, 8, k2, 30)
    if T(1) < 0:
        # line 0: a stack of car-part boxes with barcodes being scanned
        for j in range(4):
            x = 520 + j * 300; y = 560 + 20 * math.sin(t * 1.5 + j)
            c.rr(x - 120, y - 110, x + 120, y + 110, 14, (170, 130, 90), hl(0) * fd(T(0), .2 * j))
            c.rr(x - 70, y - 40, x + 70, y + 40, 6, PAPER, hl(0) * fd(T(0), .2 * j), bg=(170, 130, 90))
            for b in range(9): c.line([(x - 56 + b * 14, y - 30), (x - 56 + b * 14, y + 30)], DOT, 5 if b % 3 else 3, hl(0) * fd(T(0), .2 * j), PAPER)
        c.text(960, 800, 'Denso Wave, Japan', 44, CY, hl(0) * fd(T(0), 1.0), w='Bold')

def s_finders(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'Three big squares', 66, INK, hl(0) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'A pattern that is rare in print', 66, YE, hl(2), w='Bold')
    ang = 0.0
    k = hl(0)
    if T(2) < 0:
        # line 1: the code turns; the phone still finds it
        rot = fd(T(1), .3, 2.5) if T(1) > -.1 else 0.0
        qx, qy, qs = 760, 520, 560
        img = Image.new('RGB', (int(qs * c.k) + 4, int(qs * c.k) + 4), BG); cc = C(img, c.k)
        qr(cc, qs / 2 + 1, qs / 2 + 1, qs, k, finders=.5 + .5 * math.sin(t * 4) if k > .5 else 0)
        img = img.rotate(-90 * ease(rot) - 45 * math.sin(math.pi * rot), resample=Image.BICUBIC, fillcolor=BG)
        c.img.paste(img, (int((qx - qs / 2) * c.k), int((qy - qs / 2) * c.k)))
        c.text(1500, 380, 'Where is it?', 48, PK, k * fd(T(0), 1.0), 'mm', 'Bold')
        c.text(1500, 460, 'Which way up?', 48, PK, hl(1), 'mm', 'Bold')
        c.text(1500, 560, 'any angle works', 40, GR, hl(1) * fd(T(1), 2.0), 'mm', 'Bold')
    else:
        # line 2: slice through one finder and measure 1:1:3:1:1
        q = 70; x0, y0 = 360, 230
        k2 = hl(2)
        c.rr(x0 - q, y0 - q, x0 + 8 * q, y0 + 8 * q, 16, PAPER, k2)
        c.rr(985, 425, 1515, 575, 16, PAPER, k2)
        for r in range(7):
            for kk in range(7):
                ring_ = max(abs(r - 3), abs(kk - 3))
                col = DOT if ring_ in (0, 1, 3) else PAPER
                c.d.rectangle(((x0 + kk * q) * c.k, (y0 + r * q) * c.k, (x0 + (kk + 1) * q) * c.k, (y0 + (r + 1) * q) * c.k), fill=mix(col, k2, PAPER))
        sl = fd(T(2), .4, 1.0)
        c.line([(x0 - 30, y0 + 3.5 * q), (x0 - 30 + (7 * q + 60) * sl, y0 + 3.5 * q)], PK, 6, k2)
        segs = [(1, DOT), (1, PAPER), (3, DOT), (1, PAPER), (1, DOT)]
        xx = 1000; yb = 500
        for j, (n, col) in enumerate(segs):
            kk = k2 * fd(T(2), 1.0 + j * .3)
            c.rr(xx, yb - 60, xx + n * 100 - 8, yb + 60, 8, col, kk, outline=DIM, ow=2, bg=PAPER)
            c.text(xx + (n * 100 - 8) / 2, yb + 110, str(n), 54, YE, kk, w='Bold')
            xx += n * 100
        c.text(1350, 720, 'magazines, flyers, boxes: this ratio is rare', 34, DIM, k2 * fd(T(2), 3.0), w='Medium')

def s_message(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 130, 'The rest is your message', 66, INK, hl(0) * (1 - hl(2)), w='Bold')
    c.text(960, 130, 'Lose squares, lose letters', 66, PK, hl(2), w='Bold')
    qx, qy, qs = 560, 520, 560
    blk = lambda r, k: 13 <= r <= 16 and 17 <= k <= 18
    sp = fd(T(2), .3, 1.0) if T(2) > -.1 else 0.0
    sg = stain_gone(qx, qy, qs, qx + 150, qy + 150, 120 * sp) if sp > 0 else None
    qr(c, qx, qy, qs, hl(0), gone=sg, hot=blk, hota=hl(1), hotcol=MSG)
    stain(c, qx + 150, qy + 150, 120, sp, hl(0), PAPER)
    c.text(1400, 300, '1 square = a 1 or a 0', 46, INK, hl(0) * fd(T(0), 1.6), w='Bold')
    k1 = hl(1)
    if k1 > 0:
        bits = '01100011'
        for j, b in enumerate(bits):
            byte_box(c, 1130 + j * 76, 430, 64, 70, b, MSG if b == '1' else CARD, k1 * fd(T(1), .5 + j * .12), tcol=BG if b == '1' else INK)
        c.text(1400, 530, '8 squares = 1 byte', 44, MSG, k1, w='Bold')
        c.arrow(1400, 580, 1400, 640, DIM, 4, k1 * fd(T(1), 1.6), 14)
        c.text(1400, 700, '= the letter c', 52, YE, k1 * fd(T(1), 1.8), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        c.text(1400, 800, 'c_ff_e sh_p ?', 50, PK, k2 * fd(T(2), 1.2), w='Bold')
    c.text(560, 840, 'simplified drawing', 26, DIM, hl(0), w='Medium')

def s_spare(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 120, 'Not just your message', 66, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 120, 'Spare bytes, made with maths', 66, YE, hl(1) * (1 - hl(3)), w='Bold')
    c.text(960, 120, 'Your phone rebuilds the gaps', 66, GR, hl(3), w='Bold')
    # row of message bytes + spare bytes
    nm, ns = 8, 6; bw = 100; x0 = 960 - (nm + ns) * bw / 2 + bw / 2; y = 280
    lost = {2, 5, 10}
    rb = fd(T(3), 1.0, 1.6) if T(3) > -.1 else 0.0
    for j in range(nm + ns):
        is_sp = j >= nm
        kk = (hl(0) * fd(T(0), j * .08) if not is_sp else hl(1) * fd(T(1), .3 + (j - nm) * .15))
        x = x0 + j * bw
        col = SPARE if is_sp else MSG
        if j in lost and T(2) > -.1 and not is_sp:
            fade = fd(T(2), 2.0, .6) if T(3) < 0 else 1.0
            byte_box(c, x, y, bw - 14, 90, '', mix(col, 1 - .85 * fade * (1 - rb), CARD), kk)
            if rb > 0: byte_box(c, x, y, bw - 14, 90, '', GR, kk * rb)
        elif j in lost and T(2) > -.1 and is_sp:
            byte_box(c, x, y, bw - 14, 90, '', CARD, kk, )
        else:
            byte_box(c, x, y, bw - 14, 90, '', col, kk)
    c.text(x0 + (nm - 1) * bw / 2, y + 80, 'message', 34, MSG, hl(0), w='Bold')
    c.text(x0 + (nm + (ns - 1) / 2) * bw, y + 80, 'spare (Reed-Solomon)', 34, SPARE, hl(1), w='Bold')
    # the smudged note
    k2 = hl(2)
    if k2 > 0:
        c.rr(560, 450, 1360, 760, 24, PAPER, k2, outline=(200, 190, 150), ow=4)
        word = 'coffee shop'; hide = {1, 5, 9}
        w = c.tw(word, 96, 'Bold'); x = 960 - w / 2
        for i, ch in enumerate(word):
            cw = c.tw(ch, 96, 'Bold')
            if i in hide:
                rev = fd(T(2), 2.6 + i * .15, .5)
                c.circ(x + cw / 2, 600, 40, mix(COFFEE, .6, PAPER), k2 * (1 - rev), bg=PAPER)
                c.text(x + cw / 2, 600, ch, 96, GR, k2 * rev, w='Bold', bg=PAPER)
            else:
                c.text(x + cw / 2, 600, ch, 96, DOT, k2, w='Bold', bg=PAPER)
            x += cw
        c.text(960, 820, 'the rest gives the gaps away', 38, INK, k2 * fd(T(2), 2.4) * (1 - hl(3)), w='Bold')
    if T(3) > -.1:
        c.text(960, 820, 'same idea, much stronger maths', 38, GR, hl(3), w='Bold')

def s_levels(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 120, 'How much can be lost?', 66, INK, hl(0) * (1 - hl(2)), w='Bold')
    c.text(960, 120, 'More spares, less room', 66, YE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 120, 'The most common choice: M', 66, CY, hl(3), w='Bold')
    lv = [('L', 7, GR), ('M', 15, CY), ('Q', 25, YE), ('H', 30, PK)]
    base, top = 760, 300; sc_ = (base - top) / 32
    for j, (n, pct, col) in enumerate(lv):
        x = 330 + j * 230
        kk = hl(0) * fd(T(0), .8 + j * .25)
        grow = fd(T(1), .2 + j * .5, .8) if T(1) > -.1 else 0.0
        h = pct * sc_ * grow
        dim = 1 - .55 * hl(3) * (j != 1)
        c.rr(x - 70, base - h, x + 70, base, 14, col, kk * dim * (1 if h > 4 else 0))
        c.text(x, base + 50, n, 50, col, kk * dim, w='Bold')
        if grow > .3: c.text(x, base - h - 40, f'~{pct}%', 40, INK, kk * dim * fd(grow, .3, .5), w='Bold')
    c.line([(240, base), (1110, base)], DIM, 3, hl(0))
    c.text(675, 860, 'share of data bytes that can be rebuilt', 30, DIM, hl(1), w='Medium')
    # the trade-off: same size code, message vs spare share (illustrative)
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, sp, col) in enumerate([('Level L', .2, GR), ('Level H', .6, PK)]):
            y = 380 + j * 230
            c.text(1270, y - 75, lab, 36, col, k2 * fd(T(2), j * .5), 'lm', 'Bold')
            w = 500
            c.rr(1270, y - 40, 1270 + w * (1 - sp), y + 40, 12, MSG, k2 * fd(T(2), j * .5))
            c.rr(1270 + w * (1 - sp) + 6, y - 40, 1270 + w, y + 40, 12, SPARE, k2 * fd(T(2), j * .5))
        c.text(1520, 820, 'message   /   spare   (illustrative)', 30, DIM, k2, w='Medium')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(2)
    c.text(960, 120, 'Quick question', 64, YE, m * (1 - ans), w='Bold')
    c.text(960, 190, 'A small tear on one corner. Which is safest?', 44, INK, m * fd(T(0), .5) * (1 - ans), w='Bold')
    c.text(960, 150, 'D: the corner with no big square', 60, GR, ans, w='Bold')
    qx, qy, qs = 960, 540, 540
    gone = None
    tp = fd(T(2), .6, 1.0) if T(2) > -.1 else 0.0
    q = qs / (N + 4); x0, y0 = qx - qs / 2 + 2 * q, qy - qs / 2 + 2 * q
    qr(c, qx, qy, qs, m, finders=ans)
    tear(c, qx, qy, qs, tp, m, BG, 'br', .26)
    labs = [('A', -1, -1), ('B', 1, -1), ('C', -1, 1), ('D', 1, 1)]
    for j, (lab, sx, sy) in enumerate(labs):
        kk = m * fd(T(0), 1.0 + j * .3)
        col = GR if (ans > 0 and lab == 'D') else (PK if ans > 0 else YE)
        x, y = qx + sx * (qs / 2 + 70), qy + sy * (qs / 2 - 30)
        c.circ(x, y, 44, col, kk); c.text(x, y, lab, 48, BG, kk, w='Bold', bg=col)
    if ans > 0:
        c.text(380, 540, 'lose a big square:', 36, PK, fd(T(2), 2.4), w='Bold')
        c.text(380, 590, 'the phone may not', 36, PK, fd(T(2), 2.4), w='Bold')
        c.text(380, 640, 'find the code', 36, PK, fd(T(2), 2.4), w='Bold')
        phone(c, 1560, 540, 380, fd(T(2), 1.2), t, ok=fd(T(2), 1.8))
    if T(1) > 0 and ans < 1:
        p = clamp(T(1) / 2.0)
        ring(c, 1560, 540, 70, 1 - p, CY, fd(T(1)) * (1 - ans))

def s_logo(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 120, 'Why logos can sit in the middle', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 120, 'The logo counts as damage', 62, YE, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 120, 'Too big, and it fails', 62, PK, hl(2), w='Bold')
    qx, qy, qs = 620, 520, 560
    q = qs / (N + 4); x0, y0 = qx - qs / 2 + 2 * q, qy - qs / 2 + 2 * q
    cov = lambda r, k: 10 <= r <= 14 and 10 <= k <= 14
    hidden = hl(1) * (1 - fd(T(1), 1.8, .6)) if T(1) > -.1 else 0.0
    qr(c, qx, qy, qs, hl(0), gone=cov if T(1) < 0 or T(1) < 1.8 else None, fix=cov, fixp=fd(T(1), 2.0, 1.2) if T(1) > -.1 else 0.0, hot=cov, hotcol=PK, hota=hidden)
    lk = hl(0) * (1 - .75 * fd(T(1), 1.0, .6)) if T(1) > -.1 else hl(0)
    c.rr(qx - 2.6 * q * 2, qy - 2.6 * q * 2, qx + 2.6 * q * 2, qy + 2.6 * q * 2, 20, PAPER, lk, outline=COFFEE, ow=5)
    cup(c, qx - 10, qy + 5, 42, lk)
    c.text(qx, qy + qs / 2 + 50, 'café logo', 34, DIM, hl(0), w='Bold')
    if T(1) > -.1 and hl(2) < 1:
        o = 1 - hl(2)
        c.text(1440, 400, 'phone: "these bytes are missing"', 38, PK, o * hl(1) * (1 - fd(T(1), 2.0)), w='Bold')
        c.text(1440, 400, 'spare bytes fill the gap', 40, GR, o * fd(T(1), 2.2), w='Bold')
        phone(c, 1440, 640, 300, o * hl(1), t, ok=fd(T(1), 2.8))
    if T(2) > -.1:
        k2 = hl(2)
        bx, by, bs = 1440, 470, 340
        qr(c, bx, by, bs, k2, bg=BG)
        c.rr(bx - 115, by - 115, bx + 115, by + 115, 16, PAPER, k2, outline=COFFEE, ow=4)
        cup(c, bx - 6, by, 50, k2)
        c.cross(bx + 230, by - 150, 70, PK, k2 * fd(T(2), 1.4))
        c.text(bx, by + 230, 'not enough spares left', 36, PK, k2 * fd(T(2), 1.4), w='Bold')

RECAPS = [('1', 'Big squares: where and which way up', PK), ('2', 'Spare bytes rebuild up to ~30%', YE), ('3', 'Protect the squares, small logos', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 195, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; x = 400 + i * 560; up = 24 * (1 - fd(T(i + 1)))
        if m <= 0.01: continue
        c.rr(x - 260, 290 + up, x + 260, 790 + up, 30, CARD, m, outline=col, ow=5)
        c.circ(x - 195, 355 + up, 40, col, m, bg=CARD); c.text(x - 195, 355 + up, nn, 48, BG, m, w='Bold', bg=CARD if False else col)
        y = 530 + up
        if i == 0:
            qr(c, x, y, 230, m, bg=CARD, finders=.5 + .5 * math.sin(t * 3))
        elif i == 1:
            qr(c, x, y, 230, m, bg=CARD, gone=lambda r, k: r > 16 and k > 16, fix=lambda r, k: r > 16 and k > 16, fixp=.5 + .5 * math.sin(t * 2))
        else:
            qr(c, x, y, 230, m, bg=CARD)
            c.rr(x - 30, y - 30, x + 30, y + 30, 8, PAPER, m, outline=COFFEE, ow=3, bg=PAPER)
            cup(c, x - 3, y + 2, 14, m)
        ls = wrap(c, lab, 30, 470, 'Bold')
        for j, l in enumerate(ls): c.text(x, 700 + up + j * 40 - (len(ls) - 1) * 20, l, 30, col, m, w='Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Tear a corner off a QR code, and it still scans.",
            "Spill coffee on it. It still scans.",
            "So how can your phone read a code with pieces missing?"], s_hook),
 ('1  ·  WHY IT WAS MADE', ["QR codes were invented in nineteen ninety-four, at a Japanese company called Denso Wave.",
            "Factories tracked parts with barcodes. But a barcode holds only about twenty characters.",
            "So a two-person team, led by Masahiro Hara, stored data in two directions: a grid of black and white squares."], s_origin),
 ('2  ·  THE BIG SQUARES', ["Look at the corners. There are three big squares.",
            "They tell your phone where the code is, and which way up. That's why you can scan it from any angle.",
            "Slice through one, and the stripes go one, one, three, one, one. The team picked that pattern because it's rare in magazines and on boxes, so nothing else gets mistaken for it."], s_finders),
 ('3  ·  THE MESSAGE', ["The rest of the grid holds your message. Each small square is a one or a zero.",
            "Eight squares make a byte. That's enough for one letter of a web address.",
            "A coffee stain wipes out letters. So how does the phone read it?"], s_message),
 ('4  ·  THE SPARE BYTES', ["Here's the trick. A QR code doesn't only store your message.",
            "It adds spare bytes, worked out from the message with clever maths called Reed-Solomon code.",
            "Picture a note saying coffee shop, with three letters smudged. You can still read it. The rest gives the gaps away.",
            "Reed-Solomon is a much stronger, mathematical version of that. Lose some bytes, and your phone rebuilds them from the spares."], s_spare),
 ('5  ·  HOW MUCH', ["How much can be lost? Whoever makes the code picks one of four levels.",
            "The lowest can rebuild about seven percent of the data. The highest, about thirty percent.",
            "More spares survive more damage, but leave less room for the message.",
            "Denso Wave says the most common choice is level M, about fifteen percent."], s_levels),
 ('6  ·  QUICK QUESTION', ["Quick question. A small tear takes off one corner. Which corner is safest to lose?",
            "Three, two, one.",
            "D, the bottom right. It's the only corner without a big square. Lose a big square, and your phone may not find the code at all."], s_quiz),
 ('7  ·  LOGOS', ["That's why some QR codes can have a logo in the middle, like a café's cup.",
            "The logo hides part of the grid. Your phone treats it as damage, and the spare bytes fill the gap.",
            "But keep it small. Cover too much, and there aren't enough spares left to rebuild it."], s_logo),
 ('RECAP', ["So remember three things.",
            "One. The three big squares show your phone where the code is, and which way up.",
            "Two. Spare bytes let your phone rebuild missing parts, up to about thirty percent.",
            "Three. Protect the big squares, and keep logos small.",
            "If this made you think, subscribe to Short Story Long Thinking."], s_recap),
]

# The Short: its own complete mini-story. Applied lesson (learnings.md, 2026-10-23): the average Shorts view
# lasts about 16 s, so the core answer ("it carries spare data") is said inside the first ~8 s, then explained.
SHORT_SCENES = [
 ('THE PUZZLE', ["Tear a corner off a QR code, and it still scans.",
                 "Spill coffee on it. Still scans.",
                 "The reason: it carries spare data."], s_hook),
 ('SPARE BYTES', ["Your message is stored as bytes, in the small squares.",
                  "But the code also adds spare bytes, worked out from the message with clever maths.",
                  "Like a note with letters smudged: the rest gives the gaps away.",
                  "So when some bytes are lost, your phone rebuilds them from the spares."], s_spare),
 ('HOW MUCH', ["How much can be lost?",
               "At the strongest setting, about thirty percent of the data."], s_levels),
 ('THE ANSWER', ["So a torn QR code works because it carries spares to rebuild what's lost.",
                 "Just don't tear off one of the three big squares. Follow for more."],
                card('Spare bytes rebuild the gaps', 'Protect the 3 big squares')),
]
SHORT_HITS = [(3, 0, 0.0)]
