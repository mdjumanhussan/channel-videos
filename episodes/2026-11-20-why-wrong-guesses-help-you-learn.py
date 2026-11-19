"""Episode: Why a Wrong Guess Helps You Learn (the pretesting effect: guess first, then see the answer)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Guess first, then learn'                      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Can a wrong guess help you learn?'             # headline on the vertical Short
HITS = [(0, 1, 0.0), (4, 0, 0.0), (5, 2, 0.0)]               # 'mammal' reveal, the quiz answer, the essay result
THUMB = ['GUESS WRONG,', 'REMEMBER', 'MORE']
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 2.6, (1, 3): 0.3, (2, 2): 0.3, (3, 0): 3.2, (4, 2): 0.3, (5, 2): 0.3, (6, 2): 0.3, (7, 2): 0.3, (8, 3): 0.3}
SHORT_PAUSES = {(0, 0): 1.6, (2, 1): 0.3}
CAPTION_FIXES = {'two thousand nine': '2009', 'two thousand twenty-three': '2023', 'thirteen seconds': '13 seconds',
                 'eight seconds': '8 seconds', 'five seconds': '5 seconds', 'five percent': '5%', 'ten percent': '10%',
                 'two minutes': '2 minutes', 'eight minutes': '8 minutes', 'ten minutes': '10 minutes'}

# Durations of the guess-prompt lines (seconds), set after the audio build so countdowns start when the voice stops.
HOOK_L0 = 3.2      # long video, scene 0 line 0
QUIZ_L0 = 7.0      # long video, scene 3 line 0
SHOOK_L0 = 3.2     # Short, scene 0 line 0

# Colour code kept in every scene: a guess is yellow, the right answer green, plain study cyan, wrong pink.
GUESS = YE; ANS = GR; STUDY = CY; WRONG = PK
DARK = (20, 22, 38); QUIZ = (54, 40, 70); PAPER = (236, 232, 220); INKP = (16, 18, 36)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0
st = lambda T, i, off=0.0, d=.45: fd(T(i), off, d) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def word_box(c, x, y, txt, col, a, w=360, h=130, size=60, bg=BG, fill=CARD, txt_col=None):
    if a <= .01: return
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 28, fill, a, outline=col, ow=5, bg=bg)
    c.text(x, y, txt, size, txt_col or col, a, w='Bold', bg=fill)

def pair(c, x, y, left, right, a, reveal=0.0, rcol=ANS, w=360, h=130, size=60, bg=BG, lcol=INK, gap=90):
    """Two word cards joined by a dash; the right card shows '?' until reveal goes 0 -> 1 (a flip)."""
    if a <= .01: return
    word_box(c, x - w / 2 - gap / 2, y, left, lcol, a, w, h, size, bg)
    c.line([(x - gap / 2 + 14, y), (x + gap / 2 - 14, y)], DIM, 6, a, bg=bg)
    rx = x + w / 2 + gap / 2
    if reveal < .5:
        sq = 1 - reveal * 2
        if sq > .02:
            c.rr(rx - w / 2 * sq, y - h / 2, rx + w / 2 * sq, y + h / 2, 28, CARD, a, outline=GUESS, ow=5, bg=bg)
            if sq > .4: c.text(rx, y, '?', size + 10, GUESS, a, w='Bold', bg=CARD)
    else:
        sq = (reveal - .5) * 2
        c.rr(rx - w / 2 * sq, y - h / 2, rx + w / 2 * sq, y + h / 2, 28, CARD, a, outline=rcol, ow=5, bg=bg)
        if sq > .6: c.text(rx, y, right, size, rcol, a, w='Bold', bg=CARD)

def timer_bar(c, x, y, w, secs, total, col, a, p=1.0, label=None, bg=BG, h=46):
    """A segment of a time bar: secs out of total, drawn from x; p animates the fill."""
    if a <= .01: return x
    ww = w * secs / total
    c.rr(x, y - h / 2, x + max(h, ww * clamp(p)), y + h / 2, h / 2, col, a, bg=bg)
    if label and p > .6: c.text(x + ww / 2, y, label, 30, DARK, a * fd(p, .6, .4), w='Bold', bg=col)
    return x + ww

def countdown(c, x, y, e, a, col=GUESS, bg=BG, r=60):
    """3-2-1 ring that starts at e = 0 (seconds after the prompt finished)."""
    if a <= .01: return
    k = 3 - int(max(0, e) / .8) if e > 0 else 3
    c.circ(x, y, r, col, a, bg=bg)
    if e > 0:
        sweep = clamp(e / 2.4)
        pts = [(x + math.sin(sweep * 2 * math.pi * j / 40) * (r + 16), y - math.cos(sweep * 2 * math.pi * j / 40) * (r + 16)) for j in range(41)]
        c.line(pts, INK, 6, a, bg=bg)
    c.text(x, y, str(k) if k > 0 else '?', 60, DARK, a, w='Bold', bg=col)

def chip(c, x, y, txt, col, a, bg=BG, size=40, crossed=0.0, fill=CARD):
    if a <= .01: return
    w = c.tw(txt, size, 'Bold') + 60
    c.rr(x - w / 2, y - 40, x + w / 2, y + 40, 40, fill, a, outline=col, ow=4, bg=bg)
    c.text(x, y, txt, size, col, a, w='Bold', bg=fill)
    if crossed > .01: c.line([(x - w / 2 + 10, y + 26), (x - w / 2 + 10 + (w - 20) * crossed, y - 26)], WRONG, 7, a, bg=bg)

def eye(c, x, y, r, a, bg=PAPER):
    if a <= .01: return
    pts = [(x + r * math.cos(u / 20 * math.pi), y - r * .55 * math.sin(u / 20 * math.pi)) for u in range(21)]
    pts += [(x + r * math.cos(u / 20 * math.pi), y + r * .55 * math.sin(u / 20 * math.pi)) for u in range(20, -1, -1)]
    c.d.polygon([(px * c.k, py * c.k) for px, py in pts], fill=mix((250, 250, 250), a, bg), outline=mix(INKP, a, bg))
    c.circ(x, y, r * .42, STUDY, a, bg=bg); c.circ(x, y, r * .2, DARK, a, bg=STUDY)

def page(c, x0, y0, x1, y1, a, lines=6, bg=BG):
    if a <= .01: return
    c.rr(x0, y0, x1, y1, 18, PAPER, a, bg=bg)
    for k in range(lines):
        yy = y0 + 150 + k * 44
        if yy > y1 - 30: break
        c.line([(x0 + 40, yy), (x1 - 40 - (90 if k % 3 == 2 else 0), yy)], (180, 178, 170), 8, a, bg=PAPER)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: the viewer guesses within the first seconds; the card is on screen from the first frame."""
    headline(c, [('Guess the word', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('It was ', INK), ('mammal', ANS)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('A ', INK), ('wrong guess', WRONG), (' helps you remember', INK)], sw_in(T, 2), size=72)
    rev = st(T, 1, 0, .5)
    pair(c, 960, 420, 'WHALE', 'MAMMAL', 1, reveal=rev, w=420, h=150, size=70, gap=110)
    if rev < .99:
        countdown(c, 960, 640, T(0) - HOOK_L0, (1 - rev) * fd(T(0), HOOK_L0 - .6))
    m2 = st(T, 2)
    if m2 > .01:
        for k, g in enumerate(('fish', 'ocean', 'big')):
            a = st(T, 2, .3 + .6 * k)
            chip(c, 560 + k * 400, 640, g, GUESS, a, crossed=st(T, 2, .6 + .6 * k, .4))
        c.text(960, 740, 'your guess', 34, GUESS, st(T, 2, .4), w='Bold')
        for k in range(3):
            c.arrow(560 + k * 400, 590, 960 + (k - 1) * 120, 510, ANS, 5, st(T, 2, 2.6 + .3 * k))
        c.text(960, 820, 'then the answer sticks better', 38, ANS, st(T, 2, 3.4), w='Bold')

def s_setup(c, T, t):
    headline(c, [('Word pairs that ', INK), ('loosely', GUESS), (' go together', INK)], sw_out(T, 1), size=72)
    headline(c, [('Group 1: ', STUDY), ('just study', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Group 2: ', GUESS), ('guess first', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Same time: ', INK), ('13 seconds', STUDY)], sw_in(T, 3))
    a0 = st(T, 0)
    m1 = st(T, 1)
    if m1 < .99:
        pair(c, 960, 460, 'STAR', 'NIGHT', a0 * (1 - m1), reveal=1, rcol=INK, w=380, h=140, size=64)
        c.text(960, 620, 'also: factory - plant, whale - mammal', 34, DIM, a0 * (1 - m1) * st(T, 0, 1.4), w='Bold')
    if m1 > .01:
        X0, BW = 900, 820
        # row 1: study the whole pair for 13 s
        c.text(150, 430, 'STUDY', 44, STUDY, m1, 'lm', 'Bold')
        pair(c, 560, 430, 'STAR', 'NIGHT', m1, reveal=1, rcol=INK, w=200, h=90, size=38, gap=40)
        timer_bar(c, X0, 430, BW, 13, 13, STUDY, m1, p=st(T, 1, .3, 2.0), label='13 s study')
        # row 2: guess for 8 s, then see the answer for 5 s
        m2 = st(T, 2)
        if m2 > .01:
            c.text(150, 650, 'GUESS', 44, GUESS, m2, 'lm', 'Bold')
            rv = st(T, 2, 5.0, .5)
            pair(c, 560, 650, 'STAR', 'NIGHT', m2, reveal=rv, w=200, h=90, size=38, gap=40)
            x = timer_bar(c, X0, 650, BW, 8, 13, GUESS, m2, p=st(T, 2, .3, 2.0), label='8 s guess')
            timer_bar(c, x + 6, 650, BW - 6, 5, 13, ANS, st(T, 2, 5.0), p=st(T, 2, 5.0, 1.2), label='5 s answer')
        m3 = st(T, 3)
        if m3 > .01:
            c.line([(X0 + BW + 30, 430), (X0 + BW + 30, 650)], INK, 5, m3)
            c.text(X0 + BW / 2, 790, 'Kornell, Hays and Bjork, 2009', 30, DIM, m3, w='Regular')

def s_wrong(c, T, t):
    headline(c, [('Guessers were ', INK), ('almost always wrong', WRONG)], sw_out(T, 1) * sw_out(T, 2), size=76)
    headline(c, [('Right guesses ', ANS), ("didn't count", INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Mostly ', INK), ('wrong', WRONG), (', then shown the answer', INK)], sw_in(T, 2), size=70)
    # 20 guess tiles: about 1 in 20 (5%) right
    for k in range(20):
        r, q = divmod(k, 10)
        x = 330 + q * 140; y = 380 + r * 170
        a = st(T, 0, .1 + .08 * k, .3)
        right = k == 13
        col = ANS if right else WRONG
        out = st(T, 1, .4) if right else 0
        c.rr(x - 55, y - 60, x + 55, y + 60, 18, CARD, a * (1 - .7 * out), outline=col, ow=4)
        if right: c.check(x, y, 50, ANS, a * (1 - .7 * out))
        else: c.cross(x, y, 56, WRONG, a)
        if right and out > .01: c.line([(x - 70, y + 70), (x + 70, y - 70)], DIM, 6, out)
    c.text(960, 760, 'right only about 5% of the time', 40, ANS, st(T, 0, 2.2), w='Bold')
    c.text(960, 830, 'Illustrative grid: 1 in 20', 26, DIM, st(T, 0, 2.2), w='Regular')

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a plum pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Who remembered ', INK), ('more', ANS), (' later?', INK)], 1, bg=QUIZ, size=80)
    for k, (lab, sub, col) in enumerate((('Just studied', '13 s with the pair', STUDY), ('Guessed wrong first', '8 s guess + 5 s answer', GUESS))):
        x = 560 + k * 800; a = st(T, 0, .3 + .5 * k)
        c.rr(x - 330, 300, x + 330, 680, 30, CARD, a, outline=col, ow=5, bg=QUIZ)
        c.text(x, 380, lab, 52, col, a, w='Bold', bg=CARD)
        c.text(x, 450, sub, 32, DIM, a, w='Bold', bg=CARD)
        if k == 0: pair(c, x, 570, 'STAR', 'NIGHT', a, reveal=1, rcol=INK, w=220, h=90, size=38, gap=40, bg=CARD)
        else:
            pair(c, x, 570, 'STAR', 'NIGHT', a, reveal=(math.sin(t * 1.6) > 0) * 1.0, w=220, h=90, size=38, gap=40, bg=CARD)
    countdown(c, 960, 790, T(0) - QUIZ_L0, fd(T(0), QUIZ_L0 - .6), bg=QUIZ)

def s_result(c, T, t):
    headline(c, [('The ', INK), ('guessers', GUESS), (': about 10% more', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Right away, and ', INK), ('a day and a half later', ANS)], sw_in(T, 1) * sw_out(T, 2), size=70)
    headline(c, [('A wrong guess ', WRONG), ('beat extra study', INK)], sw_in(T, 2))
    base = 760
    groups = (('right away', 0), ('about 38 hours later', 1))
    for g, (lab, gi) in enumerate(groups):
        ga = st(T, 0, .2) if gi == 0 else st(T, 1, .2)
        x = 600 + g * 720
        for j, (nm, col, v) in enumerate((('study', STUDY, .50), ('guess first', GUESS, .55))):
            if gi == 1: v -= .12
            hh = 420 * v * st(T, 0 if gi == 0 else 1, .4 + .3 * j, .9)
            bx = x - 160 + j * 180
            c.rr(bx, base - max(hh, 8), bx + 140, base, 16, col, ga)
            c.text(bx + 70, base + 34, nm, 30, col, ga, w='Bold')
        c.text(x, base + 90, lab, 36, INK, ga, w='Bold')
        if gi == 0:
            c.text(x + 90, base - 420 * .55 - 40, '+10%', 40, GUESS, st(T, 0, 1.4), w='Bold')
    c.text(1720, 300, 'Illustrative heights', 26, DIM, st(T, 0, .5), 'rm', 'Regular')

def s_essay(c, T, t):
    headline(c, [('Not just ', INK), ('word games', GUESS)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Questions first', GUESS), (', then read', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Better', ANS), (', even on ones they got ', INK), ('wrong', WRONG)], sw_in(T, 2), size=70)
    a0 = st(T, 0)
    m1 = st(T, 1)
    # left: the essay about vision
    page(c, 140, 300, 560, 820, a0, lines=10)
    c.text(350, 350, 'How we see', 40, INKP, a0, w='Bold', bg=PAPER)
    eye(c, 350, 440, 80, a0 * st(T, 0, .6))
    c.text(350, 860, 'an essay about vision', 30, DIM, st(T, 0, 1.0), w='Bold')
    if m1 > .01:
        X0, BW = 720, 1000
        c.text(X0, 400, 'GROUP A', 36, GUESS, m1, 'lm', 'Bold')
        x = timer_bar(c, X0, 460, BW, 2, 10, GUESS, m1, p=st(T, 1, .4, .8), label='2 min')
        timer_bar(c, x + 6, 460, BW - 6, 8, 10, STUDY, m1, p=st(T, 1, 1.2, 1.4), label='8 min reading')
        c.text(X0, 560, 'GROUP B', 36, STUDY, st(T, 1, 2.0), 'lm', 'Bold')
        timer_bar(c, X0, 620, BW, 10, 10, STUDY, st(T, 1, 2.0), p=st(T, 1, 2.2, 1.6), label='10 min reading')
        c.text(X0 + 10, 500, 'questions', 26, GUESS, st(T, 1, 1.0), 'lt', 'Bold')
    m2 = st(T, 2)
    if m2 > .01:
        c.rr(720, 700, 1720, 820, 26, CARD, m2, outline=ANS, ow=4)
        c.check(790, 760, 50, ANS, m2, p=st(T, 2, .3, .6))
        c.text(850, 760, 'Group A scored higher on the final test', 38, ANS, m2, 'lm', 'Bold', bg=CARD)
        c.text(1220, 860, 'Richland, Kornell and Kao, 2009', 26, DIM, st(T, 2, 1.0), w='Regular')

def s_why(c, T, t):
    headline(c, [('Why would a ', INK), ('wrong guess', WRONG), (' help?', INK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Searching ', GUESS), ('wakes up related memories', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3), size=70)
    headline(c, [('The answer has ', INK), ('somewhere to attach', ANS)], sw_in(T, 2) * sw_out(T, 3), size=74)
    headline(c, [('Still debated. ', DIM), ('Often found.', INK)], sw_in(T, 3))
    cx, cy = 960, 545
    a0 = st(T, 0)
    word_box(c, cx, cy, 'STAR', INK, a0, w=260, h=110, size=54)
    nodes = (('sky', -430, -170), ('moon', 430, -170), ('bright', -460, 170), ('shine', 0, -250), ('NIGHT', 440, 190))
    for k, (w, dx, dy) in enumerate(nodes):
        is_ans = w == 'NIGHT'
        if is_ans:
            a = st(T, 2, .2)
            col = ANS
        else:
            a = st(T, 1, 1.2 + .5 * k)
            col = GUESS
        if a <= .01: continue
        pulse = .7 + .3 * math.sin(t * 3 + k)
        c.line([(cx + dx * .25, cy + dy * .25), (cx + dx * .82, cy + dy * .82)], col, 6, a * (pulse if not is_ans else 1))
        if is_ans:
            for r in (3, 2, 1): c.circ(cx + dx, cy + dy, 90 + 14 * r, ANS, a * .07 * (1 + .3 * math.sin(t * 4)))
        chip(c, cx + dx, cy + dy, w, col, a, size=44 if is_ans else 40)
    if T(3) > -.1:
        c.text(960, 840, 'Pan and Carpenter, 2023 review: often helps; how much varies', 28, DIM, st(T, 3, .4), w='Regular')

def s_rules(c, T, t):
    headline(c, [('It needs ', INK), ('two things', GUESS)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('1. See the answer ', INK), ('soon after', ANS)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('2. The guess needs a ', INK), ('link', GUESS)], sw_in(T, 2))
    for k in range(2):
        x = 520 + k * 880; a = st(T, 0, .3 + .4 * k)
        on = st(T, 1 + k)
        col = ANS if k == 0 else GUESS
        c.rr(x - 400, 290, x + 400, 800, 30, CARD, a, outline=mix(col, .3 + .7 * on, CARD), ow=5)
        c.circ(x - 330, 350, 34, col, a * (.4 + .6 * on), bg=CARD)
        c.text(x - 330, 350, str(k + 1), 40, DARK, a, w='Bold', bg=col)
        if k == 0:
            chip(c, x - 160, 470, 'guess', GUESS, a, bg=CARD, fill=BG)
            c.arrow(x - 40, 470, x + 70, 470, INK, 5, a * on)
            chip(c, x + 190, 470, 'answer', ANS, a * on, bg=CARD, fill=BG)
            # a small clock: the answer comes seconds later, not never
            c.circ(x, 640, 70, BG, a, outline=ANS, ow=5, bg=CARD)
            ang = clamp(st(T, 1, .4, 1.6)) * 2 * math.pi * .15
            c.line([(x, 640), (x + math.sin(ang) * 50, 640 - math.cos(ang) * 50)], ANS, 6, a, bg=BG)
            c.text(x, 750, 'seconds later works', 32, ANS, a * on, w='Bold', bg=CARD)
        else:
            pair(c, x, 450, 'STAR', 'NIGHT', a, reveal=1, w=230, h=90, size=40, gap=50, bg=CARD)
            c.check(x + 330, 450, 40, ANS, a * on)
            pair(c, x, 620, 'DOOR', 'SHOE', a * on, reveal=1, rcol=DIM, lcol=DIM, w=230, h=90, size=40, gap=50, bg=CARD)
            c.cross(x + 330, 620, 50, WRONG, a * st(T, 2, 2.0))
            c.text(x, 740, 'random pairs: benefit can vanish', 32, WRONG, a * st(T, 2, 2.4), w='Bold', bg=CARD)

def s_try(c, T, t):
    headline(c, [('How to ', INK), ('use it', GUESS)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Turn headings into ', INK), ('questions', GUESS)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Write your ', INK), ('best guess', GUESS)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('Then read and ', INK), ('check', ANS)], sw_in(T, 3))
    a0 = st(T, 0)
    page(c, 300, 280, 1000, 840, a0, lines=10)
    q = st(T, 1, .5, .4)
    c.text(650, 340, 'Photosynthesis', 50, INKP, a0 * (1 - q), w='Bold', bg=PAPER)
    if q > .01:
        c.text(650, 340, typed('What is photosynthesis?', st(T, 1, .5, 1.4)), 44, (140, 70, 0), q, w='Bold', bg=PAPER)
    # sticky note with the guess
    m2 = st(T, 2, .2)
    if m2 > .01:
        y = 470 + 30 * (1 - m2)
        c.rr(1080, y, 1640, y + 280, 14, (255, 222, 120), m2)
        c.text(1110, y + 40, 'My guess:', 34, INKP, m2, 'lm', 'Bold', bg=(255, 222, 120))
        c.text(1110, y + 110, typed('plants make food', st(T, 2, 1.0, 1.4)), 38, INKP, m2, 'lm', 'Bold', bg=(255, 222, 120))
        c.text(1110, y + 170, typed('from sunlight?', st(T, 2, 2.0, 1.0)), 38, INKP, m2, 'lm', 'Bold', bg=(255, 222, 120))
    m3 = st(T, 3)
    if m3 > .01:
        for k in range(4):
            yy = 470 + k * 88
            c.rr(340, yy - 18, 340 + 600 * st(T, 3, .2 + .4 * k, .6), yy + 18, 10, ANS, m3 * .55, bg=PAPER)
        c.check(1360, 820, 56, ANS, m3, p=st(T, 3, 1.2, .6))
        c.text(1440, 820, 'checked', 40, ANS, st(T, 3, 1.6), 'lm', 'Bold')

def s_recap(c, T, t):
    """Recap as three flashcards with the question on the left and the answer on the right."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', GUESS)], 1)
    items = ((1, 'Guess, then see the answer', 'beats just studying', GUESS),
             (2, 'Check the answer', 'soon after you guess', ANS),
             (3, 'Headings into questions', 'guess before you read', STUDY))
    for ln, a_txt, b_txt, col in items:
        m = hl(ln); y = 330 + (ln - 1) * 170; dx = 60 * (1 - m)
        c.rr(260 + dx, y - 65, 1660 + dx, y + 65, 30, CARD, m, outline=col, ow=4)
        c.circ(340 + dx, y, 42, col, m, bg=CARD); c.text(340 + dx, y, str(ln), 46, DARK, m, w='Bold', bg=col)
        c.text(410 + dx, y, a_txt, 44, col, m, 'lm', 'Bold', bg=CARD)
        c.text(1620 + dx, y, b_txt, 38, INK, m, 'rm', 'Bold', bg=CARD)
    c.text(960, 840, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    word_box(c, 1500, 330, 'WHALE', INK, 1, w=520, h=170, size=84)
    c.rr(1240, 520, 1760, 690, 28, CARD, 1, outline=WRONG, ow=7)
    c.text(1500, 605, 'fish?', 84, WRONG, 1, w='Bold', bg=CARD); c.cross(1700, 540, 80, WRONG, 1)
    c.rr(1240, 760, 1760, 930, 28, CARD, 1, outline=ANS, ow=7)
    c.text(1500, 845, 'MAMMAL', 84, ANS, 1, w='Bold', bg=CARD)

SCENES = [
 ('GUESS FIRST', ["Guess the word I'm thinking of. It goes with whale.",
                  "Got one? The word was mammal.",
                  "If you guessed wrong, good news. That wrong guess just helped you remember it."], s_hook),
 ('THE EXPERIMENT', ["In two thousand nine, psychologists gave people pairs of words that go loosely together, like star and night.",
                     "One group just studied each pair, for thirteen seconds.",
                     "The other group saw only the first word, and had eight seconds to guess the second. Then they saw the answer for five seconds.",
                     "Same total time for both groups."], s_setup),
 ('THE CATCH', ["The guessers were almost always wrong. They got it right only about five percent of the time.",
                "And those lucky right guesses were left out of the results.",
                "So the guessers spent most of their time being wrong, before seeing the answer."], s_wrong),
 ('QUICK QUESTION', ["Quick question. Who remembered more pairs: the ones who just studied, or the ones who guessed wrong first?"], s_quiz),
 ('THE RESULT', ["The guessers. They recalled about ten percent more.",
                 "It held right away, and again about a day and a half later.",
                 "A wrong guess, then the answer, beat extra study time."], s_result),
 ('REAL READING', ["Is it just a word game? No. In another study, people read an essay about how we see.",
                   "One group answered questions for two minutes first, then read for eight minutes. The other group read for the full ten.",
                   "The question group did better on the final test, even on the questions they had answered wrong."], s_essay),
 ('WHY IT WORKS', ["So why would a wrong guess help?",
                   "One idea: when you search for the answer, you wake up related memories. Sky. Moon. Bright.",
                   "So when the right answer arrives, it has somewhere to attach.",
                   "Scientists still debate exactly why. But a two thousand twenty-three review found the effect often shows up."], s_why),
 ('TWO RULES', ["But it needs two things.",
                "One: see the right answer soon after you guess.",
                "Two: the guess needs a link to the answer. With random pairs, like door and shoe, the benefit can vanish."], s_rules),
 ('TRY IT', ["Here's how to use it.",
             "Before you read a chapter, turn each heading into a question.",
             "Photosynthesis becomes: what is photosynthesis? Write down your best guess.",
             "Then read, and check. Your wrong guesses help the right answers stick."], s_try),
 ('RECAP', ["Three things to keep.",
            "One: a guess, followed by the answer, beats just studying.",
            "Two: check the right answer soon after you guess.",
            "Three: turn headings into questions, and guess before you read.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('Guess the word', INK)], sw_out(T, 1), size=96)
    headline(c, [('It was ', INK), ('mammal', ANS)], sw_in(T, 1), size=96)
    rev = st(T, 1, 0, .5)
    pair(c, 960, 440, 'WHALE', 'MAMMAL', 1, reveal=rev, w=420, h=150, size=70, gap=110)
    if rev < .99:
        countdown(c, 960, 680, T(0) - SHOOK_L0, (1 - rev) * fd(T(0), SHOOK_L0 - .6))
    m = st(T, 1, 1.2)
    if m > .01:
        c.text(960, 680, 'Guessed wrong? That helps.', 54, GUESS, m, w='Bold')

SHORT_SCENES = [
 ('THE QUESTION', ["Guess the word I'm thinking of. It goes with whale.",
                   "It was mammal. And if you guessed wrong, that wrong guess helps you remember it."], short_hook),
 ('THE EXPERIMENT', ["In a two thousand nine study, people learned word pairs, like star and night.",
                     "One group just studied each pair, for thirteen seconds.",
                     "The other group had eight seconds to guess the second word, then saw the answer for five seconds.",
                     "Same total time."], s_setup),
 ('THE RESULT', ["The guessers were almost always wrong. Yet they recalled about ten percent more.",
                 "Even about a day and a half later."], s_result),
 ('THE ANSWER', ["So before you study, guess the answers first.",
                 "Then check them soon after. The wrong guesses help the right answers stick."],
  card('Guess first, then check.', 'Wrong guesses help you remember.', size=72)),
]
SHORT_HITS = [(2, 0, 0.0)]
