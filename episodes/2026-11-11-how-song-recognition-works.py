"""Episode: How Your Phone Names a Song From a Noisy Room (audio fingerprinting as described in Avery Wang's 2003 ISMIR paper for Shazam)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Your Phone Names a Song'                # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92
SHORT_HOOK = 'How does it name a song?'                    # headline on the vertical Short
HITS = [(0, 1, 0.0), (5, 2, 0.0), (6, 2, 0.0)]             # star map reveal, the pair is rare, the tallest pile wins
THUMB = ['NOISY ROOM.', 'SONG FOUND.']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.4, (0, 1): 0.3, (1, 2): 0.3, (2, 2): 0.4, (3, 2): 0.3, (4, 0): 3.2, (5, 2): 0.4, (6, 2): 0.4, (7, 2): 0.3, (8, 3): 0.2}
SHORT_PAUSES = {(0, 1): 0.2, (3, 1): 0.2}
CAPTION_FIXES = {'two thousand three': '2003', 'one or two in a hundred': '1 or 2 in 100', 'forty seconds': '40 seconds',
                 'fifteen second': '15-second'}

# Colour code kept in every scene (lesson of 2026-11-01):
# sound / the picture is blue, the kept loud points (stars) are yellow, pairs and codes are purple, the match is green, noise is pink.
SND = CY; STAR = YE; PAIR = PU; MATCH = GR; NOISE = PK
DARK = (20, 22, 38); PAPER = (236, 232, 220); QUIZ = (52, 30, 74)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

# ---- one made-up "song" used in every scene: a spectrogram grid and its peaks (illustrative) ----
NC, NR = 48, 20                       # columns (time) x rows (pitch)
GX0, GX1, GY0, GY1 = 260, 1660, 300, 800
_r = np.random.default_rng(5)
SPEC = _r.uniform(0, .22, (NC, NR))
for k in range(9):                    # a few wandering melody lines and chords
    r0 = _r.uniform(2, 17); dr = _r.uniform(-.25, .25); c0 = int(_r.uniform(0, NC - 10)); L = int(_r.uniform(10, 30))
    for cc in range(c0, min(NC, c0 + L)):
        rr_ = int(r0 + dr * (cc - c0) + 1.5 * math.sin(cc * .7 + k)) % NR
        SPEC[cc, rr_] += _r.uniform(.45, .8)
        if rr_ + 1 < NR: SPEC[cc, rr_ + 1] += .2
SPEC = np.clip(SPEC, 0, 1)
PW, PH = 4, 5                          # patch size for "keep the loudest point"
PEAKS = []
for pc in range(NC // PW):
    for pr in range(NR // PH):
        blk = SPEC[pc * PW:(pc + 1) * PW, pr * PH:(pr + 1) * PH]
        i, j = np.unravel_index(int(np.argmax(blk)), blk.shape)
        PEAKS.append((pc * PW + i, pr * PH + j))
PEAKS.sort()
cw = (GX1 - GX0) / NC; ch_ = (GY1 - GY0) / NR
def cxy(col, row): return GX0 + (col + .5) * cw, GY1 - (row + .5) * ch_

def spectro(c, a, upto=NC, dim=1.0, bg=BG):
    """The picture of sound: time left to right, pitch bottom to top, brightness = loudness."""
    if a <= .01: return
    for col in range(min(NC, int(upto))):
        for row in range(NR):
            v = SPEC[col, row]
            x, y = GX0 + col * cw, GY1 - (row + 1) * ch_
            c.d.rectangle((x * c.k, y * c.k, (x + cw - 2) * c.k, (y + ch_ - 2) * c.k), fill=mix(mix(SND, .12 + .88 * v * dim, bg), a, bg))

def axes(c, a):
    if a <= .01: return
    c.arrow(GX0, GY1 + 30, GX1, GY1 + 30, DIM, 4, a, 16)
    c.text(GX1 + 24, GY1 + 30, 'time', 32, DIM, a, 'lm', 'Bold')
    c.arrow(GX0 - 30, GY1, GX0 - 30, GY0, DIM, 4, a, 16)
    c.text(GX0 - 50, GY0 + 10, 'high', 30, DIM, a, 'rm', 'Bold'); c.text(GX0 - 50, GY1 - 10, 'low', 30, DIM, a, 'rm', 'Bold')

def star(c, x, y, r, a, col=STAR, bg=BG):
    if a <= .01: return
    pts = []
    for k in range(10):
        rr_ = r if k % 2 == 0 else r * .45; th = -math.pi / 2 + k * math.pi / 5
        pts.append(((x + rr_ * math.cos(th)) * c.k, (y + rr_ * math.sin(th)) * c.k))
    c.d.polygon(pts, fill=mix(col, a, bg))

def stars(c, a, r=11, upto=NC, t=0.0, shift=None):
    for k, (col, row) in enumerate(PEAKS):
        if col >= upto: continue
        x, y = cxy(col, row)
        if shift: x, y = x + shift[k][0], y + shift[k][1]
        tw = .85 + .15 * math.sin(t * 2.5 + k)
        star(c, x, y, r * tw, a)

def phone(c, x, y, s, a, bg=BG):
    if a <= .01: return
    c.rr(x - 130 * s, y - 240 * s, x + 130 * s, y + 240 * s, 34 * s, (40, 44, 70), a, outline=(110, 120, 170), ow=4, bg=bg)
    c.rr(x - 112 * s, y - 210 * s, x + 112 * s, y + 200 * s, 18 * s, DARK, a, bg=(40, 44, 70))

def cup(c, x, y, s, a):
    if a <= .01: return
    c.rr(x - 40 * s, y - 40 * s, x + 30 * s, y + 40 * s, 10 * s, NOISE, a)
    c.d.arc(((x + 14 * s) * c.k, (y - 22 * s) * c.k, (x + 56 * s) * c.k, (y + 20 * s) * c.k), -90, 90, fill=mix(NOISE, a), width=int(8 * s * c.k))
    for dx in (-18, 4):
        c.line([(x + dx * s, y - 54 * s), (x + (dx + 8) * s, y - 74 * s), (x + dx * s, y - 94 * s)], NOISE, 4, a * .7)

def bubble(c, x, y, s, a, txt='blah'):
    if a <= .01: return
    c.rr(x - 80 * s, y - 40 * s, x + 80 * s, y + 40 * s, 30 * s, NOISE, a)
    c.d.polygon([((x - 30 * s) * c.k, (y + 38 * s) * c.k), ((x - 4 * s) * c.k, (y + 38 * s) * c.k), ((x - 40 * s) * c.k, (y + 66 * s) * c.k)], fill=mix(NOISE, a))
    c.text(x, y, txt, int(34 * s), DARK, a, w='Bold', bg=NOISE)

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def note(c, x, y, s, a, col=SND):
    c.circ(x, y, 18 * s, col, a); c.line([(x + 16 * s, y), (x + 16 * s, y - 70 * s)], col, 6 * s, a)
    c.line([(x + 16 * s, y - 70 * s), (x + 44 * s, y - 52 * s)], col, 6 * s, a)

# ---- scenes ----
def s_hook(c, T, t):
    """Show the wow, then explain the how (lesson of 2026-11-11, TheWrap on Mark Rober)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A noisy café. A few seconds. Song found.', 80, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'It turns the music into a map of stars', 80, STAR, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'How that map works, in four steps', 80, MATCH, sw_in(T, 2), w='Bold')
    m = 1 - hl(1)
    phone(c, 960, 540, 1.0, m)
    for k in range(4):                                 # sound rings travelling into the phone from the first frame
        u = (t * .6 + k / 4) % 1
        c.circ(960, 540, 140 + 180 * (1 - u), None, m * u * .8, outline=SND, ow=5)
    for k, x in enumerate((1260, 1360, 1460)): note(c, x, 420 + 30 * math.sin(t * 2 + k), 1.0, m * fd(t, .1 * k))
    cup(c, 470, 640, 1.2, m); bubble(c, 520, 400, 1.0, m, 'blah'); bubble(c, 1440, 700, .9, m * fd(t, .3), 'clink')
    found = m * fd(T(0), 2.6)
    c.circ(960, 470, 64, MATCH, found, bg=DARK); c.check(960, 470, 50, DARK, found, 1)
    c.text(960, 590, 'Song found', 40, MATCH, found, w='Bold', bg=DARK)
    m1 = hl(1) * (1 - hl(2))
    spectro(c, m1, dim=.35); stars(c, m1, 12, t=t)
    m2 = hl(2)
    for k, (lab, col) in enumerate((('PICTURE', SND), ('STARS', STAR), ('PAIRS', PAIR), ('MATCH', MATCH))):
        mm = m2 * fd(T(2), .2 + k * .35); x = 330 + k * 420
        c.circ(x, 480, 90, col, mm); c.text(x, 480, str(k + 1), 90, DARK, mm, w='Bold', bg=col)
        c.text(x, 640, lab, 52, col, mm, w='Bold')
        if k < 3: c.arrow(x + 110, 480, x + 300, 480, DIM, 5, mm, 18)

def s_picture(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Step 1: turn sound into a picture', 84, SND, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Time runs left to right. High notes at the top', 70, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Brighter means louder', 92, SND, sw_in(T, 2), w='Bold')
    sweep = NC * fd(T(0), .3, 4.0) if T(0) > 0 else 0
    spectro(c, 1, upto=sweep)
    if sweep < NC: c.line([(GX0 + sweep * cw, GY0 - 10), (GX0 + sweep * cw, GY1 + 10)], INK, 4, .8)
    axes(c, hl(1))
    m2 = hl(2)
    col, row = max(((cc, rr_) for cc in range(NC) for rr_ in range(NR)), key=lambda p: SPEC[p])
    x, y = cxy(col, row)
    c.circ(x, y, 40 + 6 * math.sin(t * 4), None, m2, outline=STAR, ow=6)
    c.text(x, y - 70, 'loud', 40, STAR, m2, w='Bold')
    c.text(1880, 858, 'Illustrative picture. This kind of picture is called a spectrogram', 28, DIM, 1, anchor='rm', w='Regular')

def s_stars(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Step 2: keep only the loudest points', 84, STAR, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'One brightest spot per patch. Drop the rest', 74, STAR, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'What is left: a constellation map', 84, STAR, sw_in(T, 2), w='Bold')
    fade = 1 - .85 * hl(1) * fd(T(1), 1.2, 1.5)
    spectro(c, 1, dim=fade)
    m1 = hl(1)
    for pc in range(1, NC // PW):
        x = GX0 + pc * PW * cw; c.line([(x, GY0), (x, GY1)], DIM, 2, m1 * .5 * (1 - hl(2)))
    for pr in range(1, NR // PH):
        y = GY1 - pr * PH * ch_; c.line([(GX0, y), (GX1, y)], DIM, 2, m1 * .5 * (1 - hl(2)))
    n = len(PEAKS) * fd(T(1), .3, 2.2) if T(1) > 0 else 0
    for k, (col, row) in enumerate(PEAKS[:int(n)]):
        x, y = cxy(col, row); star(c, x, y, 13 * (.85 + .15 * math.sin(t * 2.5 + k)), 1)
    m2 = hl(2)
    for k, (pc, pr) in enumerate(PEAKS):                # faint "constellation" lines to the nearest star on the right
        cand = [q for q in PEAKS if 1 <= q[0] - pc <= 5 and abs(q[1] - pr) <= 4]
        if cand:
            q = min(cand, key=lambda q: (q[0] - pc) ** 2 + (q[1] - pr) ** 2)
            (x0, y0), (x1, y1) = cxy(pc, pr), cxy(*q); c.line([(x0, y0), (x1, y1)], STAR, 2, m2 * .4)
    c.text(1880, 858, "Name from Avery Wang's 2003 paper describing Shazam's method", 28, DIM, 1, anchor='rm', w='Regular')

def s_noise(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, "Why chatter doesn't stop it", 88, NOISE, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Noise must beat the music at that exact spot', 72, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A few surviving clues can be enough', 82, MATCH, sw_in(T, 2), w='Bold')
    m = 1 - hl(1)
    rr = random.Random(int(t * 6))
    spectro(c, m, dim=.25)
    for k in range(70):
        col = rr.randrange(NC); row = rr.randrange(NR); x, y = cxy(col, row)
        c.circ(x, y, 10, NOISE, m * .55 * fd(T(0), .5))
    stars(c, m, 13, t=t)
    m1 = hl(1) * (1 - hl(2))
    c.rr(560, 320, 1360, 800, 30, CARD, m1, outline=(70, 80, 140), ow=3)
    base = 720
    h1 = 300 * fd(T(1), .3); h2 = 120 * fd(T(1), .8)
    c.rr(700, base - h1, 860, base, 12, STAR, m1, bg=CARD); c.text(780, base + 40, 'the song', 36, STAR, m1, w='Bold', bg=CARD)
    c.rr(1060, base - h2, 1220, base, 12, NOISE, m1, bg=CARD); c.text(1140, base + 40, 'the noise', 36, NOISE, m1, w='Bold', bg=CARD)
    c.text(960, 370, 'loudness at one note, one moment', 36, DIM, m1, w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative bars', 28, DIM, m1, anchor='rm', w='Regular')
    m2 = hl(2)
    for k in range(100):
        x = 560 + (k % 20) * 42; y = 360 + (k // 20) * 70
        ok = k in (37, 71)
        c.circ(x, y, 15, MATCH if ok else (60, 66, 100), m2 * fd(T(2), .2 + k * .006))
    c.text(960, 760, 'about 1 or 2 clues in 100 survived a very noisy clip', 46, MATCH, m2 * fd(T(2), 1.6), w='Bold')
    c.text(1880, 858, 'Source: Wang 2003, tests with recorded pub noise. Dots illustrative', 28, DIM, m2, anchor='rm', w='Regular')

def s_quiz(c, T, t):
    """Pattern interrupt plus mid-video question (lessons of 2026-10-13 and 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(520, 110, 1400, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK QUESTION', 78, STAR, 1, w='Bold', bg=DARK)
    m = 1 - hl(1)
    star(c, 960, 470, 90 * (.9 + .1 * math.sin(t * 3)), m, bg=QUIZ)
    c.text(960, 640, 'One loud note at one moment.', 56, INK, m * fd(T(0), .5), w='Bold', bg=QUIZ)
    c.text(960, 720, "Why isn't one star enough?", 60, STAR, m * fd(T(0), 1.6), w='Bold', bg=QUIZ)
    end = T(0) - 4.0
    if end > 0 and m > .5:
        q = clamp(end / 3.0); n = 3 - int(min(q * 3, 2.9))
        c.circ(1580, 470, 84, DARK, m, bg=QUIZ); ring(c, 1580, 470, 70, 1 - q, STAR, m, 10)
        c.text(1580, 470, str(n), 76, INK, m, w='Bold', bg=DARK)
    m1 = hl(1)
    for k in range(60):
        x = 300 + (k % 15) * 94; y = 340 + (k // 15) * 110
        on = fd(T(1), .3 + k * .03)
        c.rr(x - 36, y - 40, x + 36, y + 40, 10, (70, 50, 110), m1, bg=QUIZ)
        star(c, x, y, 20, m1 * on, bg=(70, 50, 110))
    c.text(960, 800, 'the same note turns up in song after song', 50, INK, m1 * fd(T(1), 2.0), w='Bold', bg=QUIZ)

ANCH = min(range(len(PEAKS)), key=lambda k: (PEAKS[k][0] - 12) ** 2 + 4 * (PEAKS[k][1] - 10) ** 2)   # a star near the middle
def zone_pts():
    ac, ar = PEAKS[ANCH]
    return [k for k, (cc, rr_) in enumerate(PEAKS) if 2 <= cc - ac <= 12 and abs(rr_ - ar) <= 6][:5]

def s_pairs(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Step 3: join the stars in pairs', 86, PAIR, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Note one + note two + the gap = a code', 78, PAIR, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A pair is far rarer than one note', 84, MATCH, sw_in(T, 2), w='Bold')
    m = 1 - hl(2)
    spectro(c, m, dim=.2); stars(c, m * .6, 10, t=t)
    ax, ay = cxy(*PEAKS[ANCH]); zp = zone_pts()
    zx0 = ax + 2 * cw; zx1 = ax + 12.5 * cw
    c.rr(zx0 - 10, ay - 6.6 * ch_, zx1, ay + 6.6 * ch_, 16, None, m * fd(T(0), .8), outline=PAIR, ow=5)
    c.text((zx0 + zx1) / 2, ay - 6.6 * ch_ - 30, 'its target zone', 34, PAIR, m * fd(T(0), .8), w='Bold')
    for j, k in enumerate(zp):
        x, y = cxy(*PEAKS[k]); u = fd(T(0), 1.4 + j * .3)
        c.line([(ax, ay), (ax + (x - ax) * u, ay + (y - ay) * u)], PAIR, 5, m * u)
        star(c, x, y, 15, m * u)
    star(c, ax, ay, 22, m); c.text(ax, ay + 50, 'anchor', 32, STAR, m, w='Bold')
    m1 = hl(1) * m
    c.rr(1180, 640, 1860, 790, 24, CARD, m1, outline=PAIR, ow=4)
    for j, (lab, val) in enumerate((('note 1', 'A'), ('note 2', 'E'), ('gap', '0.4 s'))):
        mm = m1 * fd(T(1), .3 + j * .6); x = 1290 + j * 230
        c.text(x, 690, lab, 30, DIM, mm, w='Bold', bg=CARD); c.text(x, 745, val, 52, PAIR, mm, w='Bold', bg=CARD)
    c.text(1520, 830, '(example code)', 28, DIM, m1, w='Regular')
    m2 = hl(2)
    c.rr(240, 320, 900, 790, 30, CARD, m2, outline=NOISE, ow=4)
    star(c, 570, 450, 60, m2, bg=CARD)
    c.text(570, 590, 'one note', 50, INK, m2, w='Bold', bg=CARD)
    c.text(570, 680, 'matches everywhere', 44, NOISE, m2, w='Bold', bg=CARD)
    c.rr(1020, 320, 1680, 790, 30, CARD, m2 * fd(T(2), .8), outline=MATCH, ow=4)
    mm = m2 * fd(T(2), .8)
    star(c, 1200, 470, 44, mm, bg=CARD); star(c, 1500, 420, 44, mm, bg=CARD); c.line([(1240, 462), (1460, 428)], PAIR, 6, mm, bg=CARD)
    c.text(1350, 590, 'a pair + its gap', 50, INK, mm, w='Bold', bg=CARD)
    c.text(1350, 680, '~a million times rarer', 44, MATCH, m2 * fd(T(2), 2.2), w='Bold', bg=CARD)
    c.text(1880, 858, "Source: Wang 2003 ('about a million times greater' specificity)", 28, DIM, m2, anchor='rm', w='Regular')

def s_match(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Step 4: look up the codes', 86, MATCH, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'In the right song, every code sits 40 s later', 72, MATCH, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Count the codes that agree. Tallest pile wins', 72, MATCH, sw_in(T, 2), w='Bold')
    m = 1 - hl(1)
    # your clip on the left, a wall of songs on the right, codes flying across
    c.rr(180, 380, 560, 700, 26, CARD, m, outline=SND, ow=4)
    c.text(370, 430, 'your clip', 40, SND, m, w='Bold', bg=CARD)
    for j in range(4):
        c.rr(230, 480 + j * 52, 510, 518 + j * 52, 10, (60, 50, 100), m, bg=CARD)
        c.text(370, 499 + j * 52, ('A·E·0.4', 'C·G·0.2', 'D·A·0.7', 'F·B·0.3')[j], 28, PAIR, m, w='Bold', bg=(60, 50, 100))
    for k in range(24):
        x = 860 + (k % 6) * 150; y = 360 + (k // 6) * 110
        c.rr(x - 60, y - 40, x + 60, y + 40, 12, CARD, m * fd(T(0), .2 + k * .03), outline=(70, 80, 140), ow=2)
        note(c, x - 6, y + 14, .55, m * fd(T(0), .2 + k * .03), DIM)
    for j in range(4):
        u = ((t * .5 + j * .25) % 1); x = 560 + u * 250
        c.arrow(x - 30, 470 + j * 60, x + 20, 470 + j * 60, PAIR, 6, m * fd(T(0), 1.0) * math.sin(math.pi * u), 16)
    c.text(1240, 790, 'millions of songs, stored as codes', 38, DIM, m * fd(T(0), 1.5), w='Bold')
    m1 = hl(1) * (1 - hl(2))
    # scatter: time in your clip vs time in the song
    px0, px1, py0, py1 = 420, 1500, 290, 760
    c.line([(px0, py1), (px1, py1)], DIM, 4, m1); c.line([(px0, py1), (px0, py0)], DIM, 4, m1)
    c.text((px0 + px1) / 2, py1 + 44, 'time in your clip (0 to 10 s)', 32, DIM, m1, w='Bold')
    c.text(px0 - 20, py0 - 10, 'time in the song', 32, DIM, m1, 'rm', 'Bold')
    rr = random.Random(3)
    for k in range(40):
        c.circ(px0 + rr.uniform(20, px1 - px0 - 20), py1 - rr.uniform(20, py1 - py0 - 20), 8, DIM, m1 * fd(T(1), .3 + k * .02))
    for k in range(14):
        u = k / 13; x = px0 + 60 + u * (px1 - px0 - 160); y = py1 - 200 - u * 260
        c.circ(x, y, 12, MATCH, m1 * fd(T(1), 2.0 + k * .12))
    c.text(px1 + 20, py1 - 470, 'all 40 s later', 40, MATCH, m1 * fd(T(1), 3.8), 'lm', 'Bold')
    m2 = hl(2)
    base = 750
    hs = [40, 70, 30, 60, 50, 40, 380, 50, 30, 60, 40, 70]
    for k, h in enumerate(hs):
        x = 400 + k * 100; win = k == 6; hh = h * fd(T(2), .2 + (1.0 if win else 0), 1.2 if win else .5)
        c.rr(x - 36, base - hh, x + 36, base, 10, MATCH if win else (90, 96, 140), m2)
    c.line([(340, base), (1580, base)], DIM, 4, m2)
    c.text(1000, base + 44, 'the gap between song time and clip time', 32, DIM, m2, w='Bold')
    c.text(1000, base - 420, '40 s', 52, MATCH, m2 * fd(T(2), 2.2), w='Bold')
    c.text(1880, 858, 'Method from Wang 2003. Clip and pile heights illustrative', 28, DIM, 1, anchor='rm', w='Regular')

SHIFT = [(random.Random(k).uniform(-60, 60), random.Random(k + 99).uniform(-50, 50)) for k in range(len(PEAKS))]
def s_limits(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'It has limits', 92, INK, sw_out(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A live version has different stars', 84, NOISE, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'It matches recordings, not tunes', 84, MATCH, sw_in(T, 2), w='Bold')
    c.rr(220, 300, 1700, 400, 24, CARD, hl(0), outline=(70, 80, 140), ow=3)
    c.text(960, 350, '"not expected to generalize to live recordings"', 42, INK, hl(0), w='Bold', bg=CARD)
    for k, (x, lab, sh) in enumerate(((560, 'the record', None), (1360, 'live on stage', SHIFT))):
        mm = hl(0) * fd(T(0), 1.5) if k == 0 else hl(1) * fd(T(1), .3)
        c.rr(x - 330, 440, x + 330, 800, 26, CARD, mm, outline=(70, 80, 140), ow=3)
        c.text(x, 760, lab, 40, STAR if k == 0 else NOISE, mm, w='Bold', bg=CARD)
        for j, (col, row) in enumerate(PEAKS[:28]):
            px = x - 300 + col * 600 / 28 * .99; py = 720 - row * 13
            if sh: px += sh[j][0] * .4; py += sh[j][1] * .4
            if px < x + 320: star(c, px, py, 9, mm, bg=CARD)
    m2 = hl(2)
    c.cross(1360, 600, 120, NOISE, m2); c.check(560, 600, 120, MATCH, m2, fd(T(2), .2, .6))
    c.text(1880, 858, 'Quote: Wang 2003. Star maps illustrative', 28, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    """Recap as one left-to-right pipeline (layout change from the hanging tags of 2026-11-10)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 80, INK, sw_in(T, 0), w='Bold')
    rows = ((1, 'It keeps only the loudest points', STAR), (2, 'It joins them in pairs with a time gap', PAIR), (3, 'The right song lines up at one gap', MATCH))
    for ln, txt, col in rows:
        m = hl(ln); y = 300 + (ln - 1) * 170; dx = 60 * (1 - m)
        c.rr(240 + dx, y, 1680 + dx, y + 130, 30, CARD, m, outline=col, ow=5)
        c.circ(320 + dx, y + 65, 46, col, m, bg=CARD); c.text(320 + dx, y + 65, str(ln), 52, DARK, m, w='Bold', bg=col)
        c.text(400 + dx, y + 65, txt, 52, INK, m, 'lm', 'Bold', bg=CARD)
        if ln == 1: star(c, 1600 + dx, y + 65, 34 * (.9 + .1 * math.sin(t * 3)), m, bg=CARD)
        if ln == 2: star(c, 1550 + dx, y + 80, 22, m, bg=CARD); star(c, 1630 + dx, y + 45, 22, m, bg=CARD); c.line([(1565 + dx, y + 76), (1615 + dx, y + 50)], PAIR, 5, m, bg=CARD)
        if ln == 3: c.rr(1590 + dx, y + 20, 1630 + dx, y + 110, 8, MATCH, m, bg=CARD)
    c.text(960, 840, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    phone(c, 1500, 540, 1.25, 1)
    for k, (col, row) in enumerate(PEAKS[::3]):
        x = 1390 + (col / NC) * 220; y = 760 - row * 20
        star(c, x, y, 13, 1, bg=DARK)
    c.circ(1500, 330, 60, MATCH, 1, bg=DARK); c.check(1500, 330, 46, DARK, 1, 1)

SCENES = [
 ('THE HOOK', ["Your phone can name a song in a noisy café from just a few seconds of sound.",
               "It doesn't listen the way you do. It turns the music into a map of stars.",
               "Here's how that map works, in four steps."], s_hook),
 ('THE PICTURE', ["Step one: turn the sound into a picture.",
                  "Time runs from left to right. Low notes sit at the bottom, high notes at the top.",
                  "The brighter a spot, the louder that note is at that moment."], s_picture),
 ('THE STARS', ["Step two: keep only the loudest points.",
                "In each small patch of the picture, the app keeps the brightest spot and throws the rest away.",
                "What's left looks like a night sky. Shazam's Avery Wang called it a constellation map."], s_stars),
 ('THE NOISE', ["This is why chatter and clinking cups don't stop it.",
                "To hide one of those stars, a noise has to be louder than the music at that exact note and moment.",
                "In the original tests, a very noisy clip could keep just one or two in a hundred of these clues, and that can still be enough."], s_noise),
 ('QUICK QUESTION', ["Quick question. One star is one loud note at one moment. Why isn't that enough to find the song?",
                     "Because the same note turns up in song after song."], s_quiz),
 ('THE PAIRS', ["Step three: join the stars in pairs. Each star is linked to a few stars just after it.",
                "Every pair becomes a short code: the first note, the second note, and the time gap between them.",
                "A single note matches almost everything. A pair with its gap is about a million times more specific."], s_pairs),
 ('THE MATCH', ["Step four: your clip's codes are looked up in a database of codes from millions of songs.",
                "Lots of songs share a few codes by chance. But in the right song, the codes all line up. If your clip started forty seconds in, every code sits forty seconds later.",
                "So the app counts the codes that agree on one gap. The tallest pile wins."], s_match),
 ('THE LIMITS', ["It has limits. The original paper says the method is not expected to work on live recordings.",
                 "A live version has slightly different loud points, so the stars don't line up.",
                 "It matches a recording, not a tune."], s_limits),
 ('RECAP', ["Three things to keep.",
            "One: it keeps only the loudest points of the sound.",
            "Two: it joins them in pairs, with the time gap between them.",
            "Three: the right song is the one where the most codes line up at one gap.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'How does your phone name a song?', 82, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'It looks for the song\'s stars', 88, STAR, sw_in(T, 1), w='Bold')
    m = 1 - hl(1)
    phone(c, 960, 540, 1.0, m)
    for k in range(4):
        u = (t * .6 + k / 4) % 1
        c.circ(960, 540, 140 + 180 * (1 - u), None, m * u * .8, outline=SND, ow=5)
    cup(c, 470, 640, 1.2, m); bubble(c, 1440, 420, 1.0, m, 'blah')
    spectro(c, hl(1), dim=.35); stars(c, hl(1), 12, t=t)

def short_core(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'A picture of notes, then only the loudest', 74, STAR, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Noise must beat the music at that spot', 78, NOISE, sw_in(T, 1), w='Bold')
    spectro(c, 1, dim=1 - .8 * hl(0) * fd(T(0), 2.0, 1.2))
    n = len(PEAKS) * fd(T(0), 2.2, 1.6) if T(0) > 0 else 0
    for k, (col, row) in enumerate(PEAKS[:int(n)]):
        x, y = cxy(col, row); star(c, x, y, 13, 1)
    rr = random.Random(int(t * 6))
    for k in range(50):
        x, y = cxy(rr.randrange(NC), rr.randrange(NR)); c.circ(x, y, 9, NOISE, hl(1) * .5)

def short_pairs(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Two notes + the gap = a rare code', 82, PAIR, 1, w='Bold')
    spectro(c, 1, dim=.2); stars(c, .6, 10, t=t)
    ax, ay = cxy(*PEAKS[ANCH])
    for j, k in enumerate(zone_pts()):
        x, y = cxy(*PEAKS[k]); u = fd(T(0), .6 + j * .3)
        c.line([(ax, ay), (ax + (x - ax) * u, ay + (y - ay) * u)], PAIR, 5, u); star(c, x, y, 15, u)
    star(c, ax, ay, 22, 1)
    m1 = hl(1)
    c.rr(1180, 640, 1860, 790, 24, CARD, m1, outline=PAIR, ow=4)
    for j, (lab, val) in enumerate((('note 1', 'A'), ('note 2', 'E'), ('gap', '0.4 s'))):
        x = 1290 + j * 230; c.text(x, 690, lab, 30, DIM, m1, w='Bold', bg=CARD); c.text(x, 745, val, 52, PAIR, m1, w='Bold', bg=CARD)
    c.text(1880, 858, 'Illustrative', 28, DIM, 1, anchor='rm', w='Regular')

def short_match(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'In the right song, the codes line up', 80, MATCH, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'The tallest pile wins', 92, MATCH, sw_in(T, 1), w='Bold')
    base = 760
    hs = [40, 70, 30, 60, 50, 40, 380, 50, 30, 60, 40, 70]
    for k, h in enumerate(hs):
        x = 400 + k * 100; win = k == 6; hh = h * fd(T(0), .3 + (1.0 if win else 0), 1.2 if win else .5)
        c.rr(x - 36, base - hh, x + 36, base, 10, MATCH if win else (90, 96, 140), 1)
    c.line([(340, base), (1580, base)], DIM, 4, 1)
    c.text(1000, base + 44, 'codes that agree on one time gap', 34, DIM, 1, w='Bold')
    c.text(1880, 858, 'Illustrative', 28, DIM, 1, anchor='rm', w='Regular')

SHORT_SCENES = [
 ('THE HOOK', ["How does your phone name a song in a noisy room?",
               "It doesn't hear the song like you do. It looks for its stars."], short_open),
 ('THE STARS', ["It turns the sound into a picture of notes over time, then keeps only the loudest points.",
                "To hide one, a noise has to be louder than the music at that exact spot."], short_core),
 ('THE PAIRS', ["Then it joins those points in pairs.",
                "Two notes and the time gap between them make a code rare enough to search for."], short_pairs),
 ('THE MATCH', ["It looks the codes up. In the right song, they all line up at the same time gap.",
                "The song with the most codes in line wins."], short_match),
 ('THE ANSWER', ["So it matches loud points, in pairs, lined up in time.",
                 "Not the tune. The stars."], card('Loud points, in pairs,', 'lined up in time.')),
]
SHORT_HITS = [(4, 0, 0.0)]
