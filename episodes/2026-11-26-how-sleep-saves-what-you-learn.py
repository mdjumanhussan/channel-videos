"""Episode: Sleep Is When Learning Sticks (less forgetting after sleep, the hippocampus notepad, replay in deep sleep, spindles, timing)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Sleep Saves What You Learn'               # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.88                            # 155 wpm last run at 0.88 (lesson of 2026-11-25)
SHORT_HOOK = 'Why does sleep help you remember?'             # headline on the vertical Short
HITS = [(0, 2, 0.0), (4, 1, 0.0), (6, 0, 0.0)]               # "the sleeper remembers more", "twenty times faster", "It's B"
THUMB = ['SLEEP', 'SAVES IT']
THUMB_COLS = [CY, YE]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 1): 0.8, (5, 0): 3.4, (3, 2): 0.6}
SHORT_PAUSES = {(0, 0): 0.4}
QZ = 7.2                                                     # length of the quiz line (set from tl.json after audio)
CAPTION_FIXES = {'twenty times': '20 times', 'a hundred minutes': '100 minutes', 'twenty percent': '20%'}

# Colour code kept in every scene:
# the new memory yellow, hippocampus (notepad) cyan, cortex (library) purple, replay green, staying awake pink, sleep blue.
MEM = YE; HIP = CY; CTX = PU; REP = GR; AWK = PK; SLP = (110, 140, 255)
NIGHT = (22, 26, 60); QUIZ = (46, 28, 74); DARK = (20, 22, 38); BRAIN = (70, 62, 120); SKIN = (60, 70, 120)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    """3 to 6 word headline with one key word in colour (most mobile viewers watch muted)."""
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def moon(c, x, y, r, a, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, SLP, a, bg=bg); c.circ(x + r * .45, y - r * .3, r * .85, bg, a, bg=bg)

def zzz(c, x, y, a, t, bg=BG):
    if a <= .01: return
    for k in range(3):
        ph = (t * .5 + k / 3) % 1.0
        c.text(x + 30 * k + 20 * ph, y - 40 * k - 30 * ph, 'z', 40 + 12 * k, SLP, a * (1 - ph * .7), w='Bold', bg=bg)

def sleeper(c, x, y, s, a, t, bg=BG):
    """A figure lying in bed under a blue blanket, with z's."""
    if a <= .01: return
    c.rr(x - 200 * s, y + 20 * s, x + 200 * s, y + 70 * s, 16 * s, (90, 70, 60), a, bg=bg)           # bed frame
    c.rr(x - 190 * s, y - 50 * s, x - 90 * s, y + 20 * s, 30 * s, (220, 222, 240), a, bg=bg)         # pillow
    c.circ(x - 140 * s, y - 50 * s, 42 * s, SKIN, a, bg=(220, 222, 240))                               # head
    c.rr(x - 100 * s, y - 50 * s, x + 200 * s, y + 30 * s, 34 * s, SLP, a, bg=bg)                     # blanket
    zzz(c, x - 110 * s, y - 120 * s, a, t, bg=bg)

def waker(c, x, y, s, a, t, bg=BG):
    """A figure sitting up, lit by a phone, with a coffee cup: awake just as long."""
    if a <= .01: return
    c.circ(x, y - 170 * s, 52 * s, SKIN, a, bg=bg)
    c.rr(x - 90 * s, y - 110 * s, x + 90 * s, y + 70 * s, 46 * s, SKIN, a, bg=bg)
    c.rr(x + 40 * s, y - 80 * s, x + 90 * s, y - 10 * s, 10 * s, AWK, a, bg=SKIN)                      # phone glow
    c.rr(x - 170 * s, y - 10 * s, x - 120 * s, y + 60 * s, 8 * s, (200, 160, 120), a, bg=bg)           # cup
    for k in range(2):
        ph = (t * .6 + k * .5) % 1.0
        c.line([(x - 155 * s + 10 * k, y - 20 * s - 40 * ph), (x - 145 * s + 10 * k, y - 45 * s - 40 * ph)], DIM, 4, a * (1 - ph), bg=bg)

def word_list(c, x, y, a, words, lit=1.0, fade=None, bg=BG, size=40, w=300):
    """A card of learned words; `fade` is a list of per-word strengths (forgetting)."""
    if a <= .01: return
    n = len(words); h = 70 + n * 62
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 24, CARD, a, outline=MEM, ow=4, bg=bg)
    for k, wd in enumerate(words):
        f = 1.0 if fade is None else fade[k]
        c.text(x, y - h / 2 + 66 + k * 62, wd, size, mix(MEM, .25 + .75 * f * lit, CARD), a, w='Bold', bg=CARD)

def brain(c, x, y, s, a, bg=BG, ctx=0.0, hip=0.0):
    """A simple side-view brain: a rounded outer layer (cortex) with folds, and a small curved hippocampus deep inside."""
    if a <= .01: return
    col = mix(CTX, .35 + .65 * ctx, BRAIN)
    for dx, dy, r in ((-120, -20, 150), (40, -70, 170), (170, 10, 140), (-20, 70, 150), (110, 90, 120)):
        c.circ(x + dx * s, y + dy * s, r * s, col, a, bg=bg)
    for k in range(7):     # folds
        ang0 = -2.6 + k * .55
        pts = [(x + (60 + 160 * math.cos(ang0 + u * .25)) * s * .95 - 40 * s, y + (150 * math.sin(ang0 + u * .25)) * s * .9 - 10 * s) for u in range(5)]
        c.line(pts, mix(BRAIN, .6, col), 6 * s, a, bg=col)
    c.rr(x + 10 * s, y + 150 * s, x + 70 * s, y + 260 * s, 26 * s, BRAIN, a, bg=bg)                 # brainstem
    hc = mix(HIP, .4 + .6 * hip, BRAIN)
    pts = [(x + (-10 + 70 * math.cos(u)) * s, y + (60 + 45 * math.sin(u)) * s) for u in [3.3 + j * .28 for j in range(12)]]
    c.line(pts, hc, 26 * s, a, bg=col)

def notepad(c, x, y, s, a, bg=BG, lines=3, lit=1.0):
    if a <= .01: return
    c.rr(x - 90 * s, y - 120 * s, x + 90 * s, y + 120 * s, 14 * s, (230, 236, 250), a, bg=bg)
    c.rr(x - 90 * s, y - 120 * s, x + 90 * s, y - 80 * s, 14 * s, HIP, a, bg=bg)
    for k in range(lines):
        c.rr(x - 60 * s, y - 50 * s + k * 50 * s, x + 60 * s, y - 34 * s + k * 50 * s, 8 * s, mix(MEM, lit, (230, 236, 250)), a, bg=(230, 236, 250))

def shelf(c, x, y, s, a, bg=BG, n=9, new=0.0):
    """A bookshelf (the cortex library); `new` slides a yellow book into the last slot."""
    if a <= .01: return
    c.rr(x - 230 * s, y - 150 * s, x + 230 * s, y + 150 * s, 16 * s, (60, 48, 90), a, bg=bg)
    cols = (CTX, (120, 100, 200), (170, 140, 255), (100, 80, 170))
    for row in range(2):
        yy = y - 130 * s + row * 140 * s
        c.rr(x - 220 * s, yy + 112 * s, x + 220 * s, yy + 124 * s, 4 * s, (40, 32, 64), a, bg=(60, 48, 90))
        for k in range(n):
            bx = x - 200 * s + k * 44 * s
            if row == 1 and k == n - 1:
                if new > .01:
                    c.rr(bx, yy + 10 * s - 120 * s * (1 - new), bx + 34 * s, yy + 110 * s - 120 * s * (1 - new), 6 * s, MEM, a * new, bg=(60, 48, 90))
                continue
            c.rr(bx, yy + 10 * s + (k % 3) * 8 * s, bx + 34 * s, yy + 110 * s, 6 * s, cols[(k + row) % 4], a, bg=(60, 48, 90))

TRACK = [(330 + 1260 * k / 7, 470 + 90 * math.sin(k * .9)) for k in range(8)]

def track(c, a, lit, bg=BG, col=REP, labels=False):
    """A curvy track with 8 brain cells along it; `lit` (0..8, may be fractional) lights them in order."""
    if a <= .01: return
    c.line(TRACK, (70, 80, 120), 40, a, bg=bg)
    for k, (x, y) in enumerate(TRACK):
        on = clamp(lit - k)
        c.circ(x, y - 110, 34, mix(col, .2 + .8 * on, CARD), a, bg=bg)
        if on > .5: c.circ(x, y - 110, 50, None, a * (1 - (lit - k - .5) % 1 * .6) * .8, outline=col, ow=4, bg=bg)
        if labels: c.text(x, y - 110, str(k + 1), 30, DARK if on > .5 else DIM, a, w='Bold', bg=mix(col, .2 + .8 * on, CARD))

def rat(c, x, y, s, a, bg=BG):
    if a <= .01: return
    col = (190, 190, 205)
    c.circ(x, y, 34 * s, col, a, bg=bg); c.circ(x + 38 * s, y - 6 * s, 22 * s, col, a, bg=bg)
    c.circ(x + 34 * s, y - 30 * s, 12 * s, (240, 170, 190), a, bg=bg); c.circ(x + 56 * s, y - 10 * s, 5 * s, DARK, a, bg=col)
    c.line([(x - 34 * s, y + 6 * s), (x - 80 * s, y + 20 * s), (x - 100 * s, y + 4 * s)], (240, 170, 190), 5 * s, a, bg=bg)

def waves(c, x0, x1, y, a, t, spindles=0.0, bg=BG, amp=70):
    """Slow brain waves (blue) with quick spindle bursts (green) riding on the up-swings."""
    if a <= .01: return
    pts = []
    for k in range(241):
        u = k / 240; x = x0 + (x1 - x0) * u; ph = u * 4 * 6.283 - t * 1.2
        v = math.sin(ph) * amp
        burst = max(0, math.sin(ph)) ** 6 * spindles
        v += burst * 26 * math.sin(u * 260)
        pts.append((x, y - v))
    c.line(pts, SLP, 7, a, bg=bg)
    if spindles > .01:
        for k in range(241):
            u = k / 240; ph = u * 4 * 6.283 - t * 1.2
            if math.sin(ph) > .8 and k % 2 == 0:
                x = x0 + (x1 - x0) * u; v = math.sin(ph) * amp + max(0, math.sin(ph)) ** 6 * spindles * 26 * math.sin(u * 260)
                c.circ(x, y - v, 5, REP, a * spindles, bg=bg)

def clock(c, x, y, r, a, frac, col=INK, bg=BG):
    if a <= .01: return
    c.circ(x, y, r, CARD, a, outline=col, ow=6, bg=bg)
    for k in range(12):
        ang = 6.283 * k / 12; c.circ(x + r * .8 * math.cos(ang), y + r * .8 * math.sin(ang), 4, DIM, a, bg=CARD)
    ang = -1.571 + 6.283 * frac
    c.line([(x, y), (x + r * .7 * math.cos(ang), y + r * .7 * math.sin(ang))], col, 7, a, bg=CARD)
    c.line([(x, y), (x, y - r * .45)], DIM, 7, a, bg=CARD); c.circ(x, y, 8, col, a, bg=CARD)

WORDS = ['river', 'candle', 'tiger', 'window']

# ---------- scenes ----------
def s_hook(c, T, t):
    """Two figures from frame one: one asleep, one awake; then test cards, the sleeper's words still bright."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Same ', INK), ('list', MEM), (', same hours', INK)], sw_out(T, 1))
    headline(c, [('One ', INK), ('sleeps', SLP), ('. One ', INK), ('stays up', AWK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('The ', INK), ('sleeper', SLP), (' remembers more', INK)], sw_in(T, 2))
    sleeper(c, 520, 560, 1.0, 1, t)
    waker(c, 1400, 600, 1.1, 1, t)
    moon(c, 300, 330, 46, 1)
    m0 = 1 - hl(1)
    if m0 > .01:
        word_list(c, 960, 560, m0, WORDS, size=36, w=260)
    m2 = hl(2)
    if m2 > .01:
        word_list(c, 520, 790, m2, ['river  candle', 'tiger  window'], size=32, w=420)
        word_list(c, 1400, 790, m2, ['river  ......', '.....  window'], fade=[.5, .5], size=32, w=420)
        c.check(780, 790, 50, REP, m2, fd(T(2), .4, .5) if T(2) > -.1 else 0)

def s_1924(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Spotted in ', INK), ('1924', MEM)], sw_out(T, 1))
    headline(c, [('Nonsense ', MEM), ('syllables', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('After sleep: ', SLP), ('less forgotten', INK)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:
        c.rr(560, 300, 1360, 760, 30, (225, 205, 160), m0)
        c.text(960, 420, '1924', 150, (110, 80, 50), m0, w='Bold', bg=(225, 205, 160))
        c.text(960, 580, 'a memory experiment', 50, (110, 80, 50), m0, w='Bold', bg=(225, 205, 160))
        c.text(960, 660, 'Jenkins and Dallenbach, USA', 36, (140, 110, 80), m0, w='Medium', bg=(225, 205, 160))
    m1 = hl(1)
    if m1 > .01:
        for k, syl in enumerate(('ZAK', 'BIF', 'MUV', 'TOJ', 'KEP', 'DAX')):
            x = 460 + (k % 3) * 500; y = 380 + (k // 3) * 170
            c.rr(x - 140, y - 60, x + 140, y + 60, 22, CARD, m1 * (1 - hl(2)), outline=MEM, ow=3)
            c.text(x, y, syl, 64, MEM, m1 * (1 - hl(2)), w='Bold', bg=CARD)
        c.text(960, 760, 'made-up words, so nothing is already known', 36, DIM, m1 * (1 - hl(2)), w='Medium')
    m2 = hl(2)
    if m2 > .01:
        for k, (lab, col, keep) in enumerate((('after sleep', SLP, 1.0), ('after being awake', AWK, .45))):
            x = 560 + k * 800
            c.text(x, 330, lab, 48, col, m2, w='Bold')
            for j, syl in enumerate(('ZAK', 'BIF', 'MUV', 'TOJ')):
                on = 1.0 if (k == 0 or j in (0, 3)) else .2
                c.rr(x - 200, 400 + j * 100, x + 200, 480 + j * 100, 18, CARD, m2, outline=mix(col, on, CARD), ow=3)
                c.text(x, 440 + j * 100, syl if on > .5 else '? ? ?', 46, mix(MEM if on > .5 else DIM, 1, CARD), m2, w='Bold', bg=CARD)
        c.text(960, 860, 'illustrative: the study found less forgetting after sleep', 28, DIM, m2, w='Regular')

def s_quiet(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Asleep, ', SLP), ('nothing crowds in', INK)], sw_out(T, 1))
    headline(c, [('No new ', INK), ('noise', AWK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('But sleep also ', INK), ('works', REP)], sw_in(T, 2))
    # a whiteboard with today's word; awake: scribbles pile on; asleep: it stays clean
    for k, (lab, col) in enumerate((('awake', AWK), ('asleep', SLP))):
        x = 560 + k * 800; bgc = (235, 238, 248)
        c.rr(x - 300, 300, x + 300, 700, 20, bgc, 1, outline=col, ow=6)
        c.text(x, 760, lab, 44, col, 1, w='Bold')
        c.text(x, 430, 'tiger', 80, (200, 150, 30), 1, w='Bold', bg=bgc)
        if k == 0:
            rng = random.Random(3); n = int(clamp(t / 6) * 14) + 2
            for j in range(n):
                wd = ('msg', 'ad', 'news', 'song', 'chat', 'ping', 'game')[j % 7]
                c.text(x + rng.uniform(-230, 230), 400 + rng.uniform(-60, 260), wd, rng.randint(34, 54), mix(AWK, .5 + .5 * hl(1), bgc), 1, w='Bold', bg=bgc)
        else:
            moon(c, x + 230, 360, 34, 1, bg=bgc)
    m2 = hl(2)
    if m2 > .01:
        c.rr(660, 800, 1260, 870, 30, CARD, m2, outline=REP, ow=4)
        c.text(960, 835, 'part of the story, not all of it', 34, REP, m2, w='Bold', bg=CARD)

def s_notepad(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('New memories: the ', INK), ('hippocampus', HIP)], sw_out(T, 1), size=78)
    headline(c, [('A quick ', INK), ('notepad', HIP)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('The ', INK), ('cortex', CTX), (': a library', INK)], sw_in(T, 2))
    brain(c, 560, 540, 1.0, 1, hip=.5 + .5 * math.sin(t * 3) if hl(2) < .5 else .4, ctx=hl(2))
    c.text(560, 820, 'deep inside: hippocampus', 36, HIP, 1 - hl(2), w='Bold')
    c.text(560, 820, 'outer layer: cortex', 36, CTX, hl(2), w='Bold')
    m1 = hl(1)
    if m1 > .01:
        notepad(c, 1250, 480, 1.3, m1, lit=1)
        c.text(1250, 720, 'quick to write, small', 36, HIP, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        shelf(c, 1640, 480, .8, m2)
        c.text(1640, 720, 'big, long-term', 36, CTX, m2, w='Bold')

def s_replay(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Rats ', INK), ('learn a route', MEM)], sw_out(T, 1))
    headline(c, [('Asleep: ', SLP), ('the same cells fire', REP)], sw_in(T, 1) * sw_out(T, 2), size=80)
    headline(c, [('Same order. ', INK), ('20x faster', REP)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:   # awake: the rat runs, each cell lights as it passes
        u = (t * .18) % 1.0; lit = u * 8.2
        k = min(6, int(u * 7)); q = u * 7 - k
        x = TRACK[k][0] + (TRACK[k + 1][0] - TRACK[k][0]) * q; y = TRACK[k][1] + (TRACK[k + 1][1] - TRACK[k][1]) * q
        track(c, m0, lit, col=MEM, labels=True); rat(c, x, y - 10, 1.0, m0)
        c.text(960, 700, 'awake, running the track', 38, MEM, m0, w='Bold')
    m1 = hl(1)
    if m1 > .01:
        speed = 1.0 if hl(2) < .5 else 6.0
        lit = (t * speed * .8) % 9.5
        c.rr(0, 260, 1920, 760, 0, NIGHT, m1)
        track(c, m1, lit, bg=NIGHT, col=REP, labels=True)
        moon(c, 1760, 330, 40, m1, bg=NIGHT)
        c.text(960, 700, 'asleep: the cells fire again, 1 to 8', 38, REP, m1 * (1 - hl(2)), w='Bold', bg=NIGHT)
        c.text(960, 700, 'like a fast-forward replay of the day', 38, REP, hl(2), w='Bold', bg=NIGHT)
        c.text(960, 800, 'cells drawn simplified', 26, DIM, m1, w='Regular')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('When does the ', INK), ('replay', REP), (' mostly happen?', INK)], 1, bg=QUIZ, size=70)
    for k, txt in enumerate(('A  REM sleep', 'B  Deep sleep')):
        u = fd(t, .8 + .3 * k)
        c.rr(300, 360 + k * 200, 1100, 500 + k * 200, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(350, 430 + k * 200, txt, 56, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    moon(c, 1460, 470, 110 * fd(t, .5) + 1, fd(t, .5), bg=QUIZ)
    zzz(c, 1560, 380, fd(t, .5), t, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - QZ; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), QZ - .3)
        c.circ(1460, 730, 80, MEM, u, bg=QUIZ); c.text(1460, 730, str(k) if k else '?', 76, DARK, u, w='Bold', bg=MEM)

def s_deep(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('B: ', INK), ('deep sleep', SLP)], sw_out(T, 1))
    headline(c, [('Slow waves + ', SLP), ('spindles', REP)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Notepad ', HIP), ('to ', INK), ('library', CTX)], sw_in(T, 2))
    m01 = 1 - hl(2)
    if m01 > .01:
        waves(c, 200, 1720, 480, m01, t, spindles=hl(1), amp=90 + 30 * (1 - hl(1)))
        c.text(960, 680, 'slow brain waves', 40, SLP, m01 * (1 - hl(1)), w='Bold')
        if hl(1) > .01:
            c.text(700, 680, 'slow waves', 38, SLP, m01 * hl(1), w='Bold')
            c.text(1220, 680, 'spindles: quick bursts, under 2 s', 38, REP, m01 * hl(1), w='Bold')
    m2 = hl(2)
    if m2 > .01:
        notepad(c, 420, 480, 1.2, m2, lit=1 - .5 * fd(T(2), 1, 2))
        shelf(c, 1460, 480, .9, m2, new=fd(T(2), 1.2, 2.0) if T(2) > -.1 else 0)
        for k in range(5):     # yellow notes travel along a green arc
            u = ((t * .35) + k / 5) % 1.0; x = 560 + 650 * u; y = 470 - 170 * math.sin(3.1416 * u)
            c.rr(x - 22, y - 16, x + 22, y + 16, 6, MEM, m2)
        c.line([(560 + 650 * u, 470 - 170 * math.sin(3.1416 * u)) for u in [j / 30 for j in range(31)]], REP, 4, m2 * .5)
        c.rr(560, 770, 1360, 850, 30, CARD, m2, outline=DIM, ow=3)
        c.text(960, 810, 'a leading theory, still being tested', 34, INK, m2, w='Bold', bg=CARD)

def s_nap(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Sleep makes ', INK), ('room', REP), (' too', INK)], sw_out(T, 1))
    headline(c, [('Nappers learned ', SLP), ('20% better', REP)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('More ', INK), ('spindles', REP), (', better', INK)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:
        notepad(c, 960, 500, 1.6, m0, lit=1 - fd(T(0), .8, 1.2) if T(0) > -.1 else 1)
        c.text(960, 760, 'a fresh page for tomorrow', 40, HIP, m0, w='Bold')
    m1 = hl(1)
    if m1 > .01:
        base = 300
        for k, (lab, col, h, sub) in enumerate((('stayed awake', AWK, base, '100'), ('100-minute nap', SLP, base * 1.2, '120'))):
            x = 640 + k * 420; grow = fd(T(1), .3 + .3 * k, .8) if T(1) > -.1 else 0
            hh = h * grow
            c.rr(x - 110, 760 - hh, x + 110, 760, 18, col, m1)
            c.text(x, 800, lab, 34, col, m1, w='Bold')
            c.text(x, 730 - hh, sub, 40, INK, m1 * grow, w='Bold')
        c.text(1500, 420, 'new names and faces', 38, MEM, m1, w='Bold')
        c.text(1500, 480, 'learned after the nap', 32, DIM, m1, w='Medium')
        c.text(1500, 560, 'relative scores:', 30, DIM, m1, w='Regular')
        c.text(1500, 600, 'nappers about 20% higher', 30, DIM, m1, w='Regular')
        c.text(1500, 680, 'UC Berkeley study', 30, DIM, m1, w='Medium')
    m2 = hl(2)
    if m2 > .01 and m1 > .01:
        h = base * 1.2
        c.rr(1060 - 122, 760 - h - 12, 1060 + 122, 772, 24, None, m2, outline=REP, ow=6)
        c.text(1500, 760, 'more spindles in the nap', 32, REP, m2, w='Bold')

def s_timing(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Timing ', MEM), ('matters', INK)], sw_out(T, 1))
    headline(c, [('Sleep ', SLP), ('within a few hours', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('All-nighter: ', AWK), ('no replay', INK)], sw_in(T, 2))
    # a day timeline: study block (yellow) then the night (blue)
    x0, x1, y = 220, 1700, 470
    c.rr(x0, y - 40, x1, y + 40, 20, CARD, 1)
    for k, lab in enumerate(('6 pm', '9 pm', 'midnight', '3 am', '6 am')):
        xx = x0 + (x1 - x0) * k / 4; c.text(xx, y + 90, lab, 32, DIM, 1, w='Medium')
    c.rr(x0 + 10, y - 30, x0 + 380, y + 30, 16, MEM, 1, bg=CARD); c.text(x0 + 195, y - 80, 'study', 40, MEM, 1, w='Bold')
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        c.rr(x0 + 560, y - 30, x1 - 10, y + 30, 16, SLP, m1, bg=CARD); c.text((x0 + 560 + x1) / 2, y - 80, 'sleep', 40, SLP, m1, w='Bold')
        u = (t * .3) % 1.0
        c.line([(x0 + 380 + 180 * u, y), (x0 + 380 + 180 * u + 30, y)], REP, 8, m1, bg=CARD)
        c.text(960, 700, 'memory gains were biggest when sleep came soon after', 36, REP, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        c.rr(x0 + 400, y - 30, x1 - 10, y + 30, 16, AWK, m2, bg=CARD); c.text((x0 + 400 + x1) / 2, y - 80, 'awake all night', 40, AWK, m2, w='Bold')
        c.cross(960, 690, 90, AWK, m2)
        c.text(960, 800, 'the night that would have saved it', 34, DIM, m2, w='Medium')

def s_answer(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Sleep ', SLP), ('saves', REP), (' the day', INK)], sw_out(T, 1))
    headline(c, [('Study, then ', MEM), ('sleep on it', SLP)], sw_in(T, 1))
    sleeper(c, 560, 560, 1.1, 1, t)
    moon(c, 330, 330, 46, 1)
    brain(c, 1380, 470, .9, 1, hip=.5 + .5 * math.sin(t * 4), ctx=.6 + .4 * math.sin(t * 2))
    for k in range(4):
        u = ((t * .4) + k / 4) % 1.0; x = 1380 - 30 + 200 * u; y = 520 - 140 * u
        c.rr(x - 16, y - 12, x + 16, y + 12, 5, MEM, 1)
    m1 = hl(1)
    if m1 > .01:
        c.rr(1060, 780, 1700, 860, 26, CARD, m1, outline=REP, ow=4)
        c.text(1380, 820, 'give the replay something fresh', 34, INK, m1, w='Bold', bg=CARD)

def s_recap(c, T, t):
    """Recap as a night strip: three moons, each lighting up with one point."""
    hl = lambda i: hl_(T, i)
    c.rr(0, 250, 1920, 840, 0, NIGHT, 1)
    headline(c, [('Three things ', INK), ('to keep', MEM)], 1)
    items = ((1, 'sleep after learning', 'less is forgotten', SLP), (2, 'deep sleep replays', 'the day, faster', REP), (3, 'notepad to library', 'hippocampus to cortex', CTX))
    for ln, l1, l2, col in items:
        m = hl(ln); y = 340 + (ln - 1) * 170; dx = 60 * (1 - m)
        moon(c, 420 + dx, y + 20, 50, .3 + .7 * m, bg=NIGHT)
        c.text(520 + dx, y, str(ln) + '.  ' + l1, 54, col, .25 + .75 * m, 'lm', 'Bold', bg=NIGHT)
        c.text(600 + dx, y + 58, l2, 36, DIM, m, 'lm', 'Medium', bg=NIGHT)
    c.text(960, 880, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """A brain under a moon, with yellow notes flying into it."""
    brain(c, 1500, 560, 1.25, 1, hip=1.0, ctx=.8)
    moon(c, 1760, 250, 80, 1)
    for k in range(4):
        x = 1220 + 70 * k; y = 300 + 40 * k
        c.rr(x - 30, y - 22, x + 30, y + 22, 8, YE, 1)

SCENES = [
 ('TWO NIGHTS', ["Two people learn the same list of words.",
                 "Then one sleeps. The other stays awake for just as long.",
                 "When they're tested, the sleeper remembers more."], s_hook),
 ('1924', ["Scientists spotted this a century ago.",
           "In 1924, two American psychologists had people learn made-up words, then tested them after sleep and after being awake.",
           "After sleep, less had been forgotten."], s_1924),
 ('A QUIET NIGHT', ["One early idea: when you're asleep, nothing new crowds in.",
                    "No messages, no news, no noise to bump the fresh memory, like a whiteboard nobody else writes on.",
                    "That's part of it. But sleep also does active work."], s_quiet),
 ('THE NOTEPAD', ["During the day, new memories lean on the hippocampus, a small curved part deep in your brain.",
                  "Think of it as a notepad: quick to write on, but small.",
                  "The long-term library is the cortex, the brain's wrinkly outer layer."], s_notepad),
 ('THE REPLAY', ["Now the surprise. Scientists recorded brain cells in rats that ran along a track.",
                 "During sleep afterwards, the same cells fired again, in the same order.",
                 "And as much as twenty times faster. Like a fast-forward replay of the day."], s_replay),
 ('QUICK QUESTION', ["Quick question. Does that replay mostly happen in REM sleep, or in deep sleep? Have a guess."], s_quiz),
 ('DEEP SLEEP', ["It's B. Deep sleep.",
                 "Slow brain waves roll across the cortex, and quick bursts called sleep spindles ride on top.",
                 "Scientists think these rhythms time the replay, so the memory is copied from the notepad into the library. That's a leading theory, still being tested."], s_deep),
 ('ROOM FOR MORE', ["Sleep seems to clear space for tomorrow, too.",
                    "In one study at UC Berkeley, people who napped for a hundred minutes learned new names and faces about twenty percent better than people who stayed awake.",
                    "And the more sleep spindles they had made, the better they did."], s_nap),
 ('TIMING', ["Timing matters.",
             "One study found memory got the biggest boost when sleep came within a few hours of learning.",
             "And an all-nighter skips the night that would have saved it."], s_timing),
 ('THE ANSWER', ["So sleep isn't time off from learning. It's when your brain saves the day.",
                 "Study, then sleep on it, and give the replay something fresh to work with."], s_answer),
 ('RECAP', ["Three things to keep.",
            "One: after sleep, people forget less than after the same time awake.",
            "Two: in deep sleep, the brain replays what you learned, faster.",
            "Three: the replay is thought to move memories from the hippocampus notepad into the cortex library.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story; the full answer lands inside the first 15 seconds ----------
def short_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Sleep ', SLP), ('saves', REP), (' what you learn', INK)], 1, size=80)
    sleeper(c, 560, 560, 1.1, 1, t)
    moon(c, 330, 330, 46, 1)
    brain(c, 1380, 470, .9, 1, hip=.5 + .5 * math.sin(t * 4), ctx=.4 + .6 * hl(1))
    m = hl(1)
    for k in range(4):
        u = ((t * .4) + k / 4) % 1.0; x = 1350 + 200 * u; y = 520 - 140 * u
        c.rr(x - 16, y - 12, x + 16, y + 12, 5, MEM, m)
    c.text(1380, 800, 'replays the day, files it away', 36, REP, m, w='Bold')

def short_replay(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Same cells, ', REP), ('same order', INK)], sw_out(T, 1), size=84)
    headline(c, [('Up to ', INK), ('20x faster', REP)], sw_in(T, 1), size=88)
    c.rr(0, 260, 1920, 760, 0, NIGHT, 1)
    speed = 1.0 if hl(1) < .5 else 6.0
    track(c, 1, (t * speed * .8) % 9.5, bg=NIGHT, col=REP, labels=True)
    moon(c, 1760, 330, 40, 1, bg=NIGHT)
    c.text(960, 700, 'rat brain cells during sleep (simplified)', 36, REP, 1, w='Bold', bg=NIGHT)

def short_deep(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('In ', INK), ('deep sleep', SLP)], sw_out(T, 1), size=88)
    headline(c, [('Notepad ', HIP), ('to ', INK), ('library', CTX)], sw_in(T, 1), size=88)
    m0 = 1 - hl(1)
    if m0 > .01: waves(c, 200, 1720, 480, m0, t, spindles=1)
    m1 = hl(1)
    if m1 > .01:
        notepad(c, 420, 480, 1.2, m1)
        shelf(c, 1460, 480, .9, m1, new=fd(T(1), 1.5, 2.0) if T(1) > -.1 else 0)
        for k in range(5):
            u = ((t * .35) + k / 5) % 1.0; x = 560 + 650 * u; y = 470 - 170 * math.sin(3.1416 * u)
            c.rr(x - 22, y - 16, x + 22, y + 16, 6, MEM, m1)
        c.text(420, 720, 'hippocampus', 38, HIP, m1, w='Bold'); c.text(1460, 720, 'cortex', 38, CTX, m1, w='Bold')
        c.text(960, 830, 'a leading theory', 30, DIM, m1, w='Medium')

def short_two(c, T, t):
    """The hook picture with the result already showing (the Short has one line here)."""
    s_hook(c, lambda i: T(0) + (1.0 if i == 2 else 3.0) if i <= 2 else -99, t)

SHORT_SCENES = [
 ('THE ANSWER FIRST', ["Why does sleep help you remember what you learned?",
                       "Because while you sleep, your brain replays the day and files it away."], short_hook),
 ('TWO NIGHTS', ["People who sleep after learning remember more than people who stay awake just as long."], short_two),
 ('THE REPLAY', ["In rats that learned a route, the same brain cells fired again during sleep, in the same order.",
                 "And up to twenty times faster, like a fast-forward replay of the day."], short_replay),
 ('DEEP SLEEP', ["It happens mostly in deep sleep, timed by slow brain waves.",
                 "Scientists think it copies new memories from the hippocampus, a quick notepad, into the cortex, the long-term library."], short_deep),
 ('SO', ["So sleep isn't time off from learning.",
         "It's when learning gets saved. So study, then sleep on it."], card('Sleep replays your day.', "That's when it gets saved.")),
]
SHORT_HITS = [(4, 1, 0.0)]
