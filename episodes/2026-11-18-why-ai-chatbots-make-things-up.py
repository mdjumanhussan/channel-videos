"""Episode: Why AI Chatbots Make Things Up (the birthday test, patterns vs one-off facts, the exam that rewards guessing, the scoring fix)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Why chatbots guess'                           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.93
SHORT_HOOK = 'Why do AI chatbots make things up?'            # headline on the vertical Short
HITS = [(0, 1, 0.0), (6, 1, 0.0), (7, 2, 0.0)]               # 'it will guess', the twist (tests score IDK as zero), the fix
THUMB = ["AI WON'T SAY", "'I DON'T KNOW'"]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
# A short silence before each big reveal (lesson of 2026-11-18, TubeLab), and the quiz countdown.
PAUSES = {(0, 1): 0.3, (1, 1): 0.3, (3, 3): 0.3, (4, 2): 0.3, (5, 0): 3.2, (6, 1): 0.9, (7, 1): 0.3, (8, 1): 0.3}
SHORT_PAUSES = {(0, 0): 0.2, (2, 1): 0.6}
CAPTION_FIXES = {'seventy-five percent': '75%', 'one in five': '1 in 5', 'one time in four': '1 time in 4',
                 'the third of July': '3 July', 'twenty twenty-five': '2025', 'three points': '3 points',
                 'sixty percent': '60%'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the chatbot and its answers are cyan, wrong is pink, right is green, "I don't know" is yellow,
# patterns in the training text are purple, scores and points are white on dark cards.
BOT = CY; WRONG = PK; RIGHT = GR; IDK = YE; PAT = PU
DARK = (20, 22, 38); QUIZ = (24, 52, 60); PAPER = (236, 232, 218); INKP = (40, 44, 70)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def headline(c, parts, a, size=84, y=172, bg=BG):
    if a <= .01: return
    tot = sum(c.tw(p, size, 'Bold') for p, _ in parts); x = 960 - tot / 2
    for p, col in parts:
        c.text(x, y, p, size, col, a, 'lm', 'Bold', bg=bg); x += c.tw(p, size, 'Bold')

# ---------- drawing helpers ----------
def poly(c, pts, col, a, bg=BG):
    if a > .01: c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(col, a, bg))

def bot(c, x, y, r, a, t=0.0, mood=0, bg=BG):
    """A simple drawn chatbot: rounded head, antenna, two eyes. mood 1 = smug (half-closed eyes)."""
    if a <= .01: return
    c.line([(x, y - r * .9), (x, y - r * 1.25)], BOT, max(3, int(r * .07)), a, bg=bg)
    c.circ(x, y - r * 1.3, r * .1 * (1 + .15 * math.sin(t * 4)), YE, a, bg=bg)
    c.rr(x - r, y - r * .9, x + r, y + r * .8, r * .38, (40, 70, 110), a, outline=BOT, ow=max(3, int(r * .06)), bg=bg)
    c.rr(x - r * .75, y - r * .6, x + r * .75, y + r * .35, r * .25, DARK, a, bg=(40, 70, 110))
    blink = 1 if (t % 3.2) > .12 else .15
    for s in (-1, 1):
        ex = x + s * r * .33
        h = r * .16 * blink * (.45 if mood else 1)
        c.rr(ex - r * .14, y - r * .15 - h, ex + r * .14, y - r * .15 + h, r * .1, BOT, a, bg=DARK)
    c.line([(x - r * .25, y + r * .12), (x, y + r * .2), (x + r * .25, y + r * .12)], BOT, max(3, int(r * .06)), a, bg=DARK)

def bubble(c, x0, y0, x1, y1, txt, col, a, side=-1, size=46, fill=CARD, bg=BG, tcol=None):
    """Chat bubble with a small tail on the left (side=-1) or right (side=1)."""
    if a <= .01: return
    c.rr(x0, y0, x1, y1, 30, fill, a, outline=col, ow=4, bg=bg)
    tx = x0 + 40 if side < 0 else x1 - 40
    poly(c, [(tx - 18, y1 - 2), (tx + 18, y1 - 2), (tx - 30 * -side, y1 + 34)], col, a, bg)
    c.text((x0 + x1) / 2, (y0 + y1) / 2, txt, size, tcol or col, a, w='Bold', bg=fill)

def calendar(c, x, y, a, top, mid, col, w=260, bg=BG, sub=''):
    """A tear-off calendar page."""
    if a <= .01: return
    c.rr(x - w / 2, y - w * .55, x + w / 2, y + w * .6, 22, PAPER, a, bg=bg)
    c.rr(x - w / 2, y - w * .55, x + w / 2, y - w * .22, 22, col, a, bg=bg)
    c.d.rectangle(((x - w / 2) * c.k, (y - w * .32) * c.k, (x + w / 2) * c.k, (y - w * .22) * c.k), fill=mix(col, a, bg))
    for s in (-1, 1): c.circ(x + s * w * .25, y - w * .55, w * .045, DARK, a, bg=col)
    c.text(x, y - w * .39, top, int(w * .13), DARK, a, w='Bold', bg=col)
    c.text(x, y + w * .17, mid, int(w * .3), INKP, a, w='Bold', bg=PAPER)
    if sub: c.text(x, y + w * .45, sub, int(w * .09), (110, 114, 140), a, w='Bold', bg=PAPER)

def tag(c, x, y, txt, col, a, sub=None, bg=BG, w=300, size=42):
    if a <= .01: return
    c.rr(x - w / 2, y - 50, x + w / 2, y + 50, 22, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x, y - (12 if sub else 0), txt, size, col, a, w='Bold', bg=CARD)
    if sub: c.text(x, y + 28, sub, 26, DIM, a, w='Bold', bg=CARD)

def exam(c, x, y, a, picks=(), t=0.0, w=420, bg=BG, rows=4):
    """An exam sheet with multiple-choice rows (A to D). picks: list of (row, col, colour)."""
    if a <= .01: return
    h = 120 + rows * 90
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 18, PAPER, a, bg=bg)
    c.rr(x - w / 2 + 30, y - h / 2 + 28, x - w / 2 + 200, y - h / 2 + 50, 8, (190, 186, 172), a, bg=PAPER)
    for r in range(rows):
        yy = y - h / 2 + 120 + r * 90
        c.text(x - w / 2 + 44, yy, f'{r + 1}.', 34, INKP, a, w='Bold', bg=PAPER)
        for k in range(4):
            xx = x - w / 2 + 120 + k * 76
            fill = None
            for pr, pc, col in picks:
                if pr == r and pc == k: fill = col
            c.circ(xx, yy, 24, fill, a, outline=INKP, ow=3, bg=PAPER)
            c.text(xx, yy, 'ABCD'[k], 24, DARK if fill else INKP, a, w='Bold', bg=fill or PAPER)

def score_row(c, x, y, lab, pts, col, a, w=620, bg=BG):
    if a <= .01: return
    c.rr(x - w / 2, y - 46, x + w / 2, y + 46, 20, CARD, a, outline=col, ow=4, bg=bg)
    c.text(x - w / 2 + 34, y, lab, 40, col, a, 'lm', 'Bold', bg=CARD)
    c.text(x + w / 2 - 34, y, pts, 46, INK, a, 'rm', 'Bold', bg=CARD)

def person(c, x, y, s, col, a, bg=BG):
    if a <= .01: return
    c.circ(x, y - s * .55, s * .28, col, a, bg=bg)
    c.rr(x - s * .38, y - s * .2, x + s * .38, y + s * .55, s * .3, col, a, bg=bg)

def meter(c, x0, x1, y, p, a, thr=None, bg=BG):
    """Confidence bar from 0% to 100%, filled to p; optional threshold line."""
    if a <= .01: return
    c.rr(x0, y - 26, x1, y + 26, 26, CARD, a, outline=(70, 80, 130), ow=3, bg=bg)
    fill = RIGHT if (thr is None or p > thr) else IDK
    if p > .02: c.rr(x0 + 6, y - 20, x0 + 6 + (x1 - x0 - 12) * clamp(p), y + 20, 20, fill, a, bg=CARD)
    for v, lab in ((0, '0%'), (1, '100%')):
        c.text(x0 + (x1 - x0) * v, y + 64, lab, 30, DIM, a, w='Bold', bg=bg)
    if thr is not None:
        xx = x0 + (x1 - x0) * thr
        c.line([(xx, y - 52), (xx, y + 52)], INK, 5, a, bg=bg)
        c.text(xx, y - 80, f'{int(thr * 100)}%', 36, INK, a, w='Bold', bg=bg)

# ---------- scenes ----------
def s_hook(c, T, t):
    """Hook: prove the title in the first seconds: a question it can't know, a confident made-up answer."""
    hl = lambda i: hl_(T, i)
    headline(c, [('No ', INK), ('"I don\'t know"', IDK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('It ', INK), ('guesses', WRONG), ('. Confidently.', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('The reason: ', INK), ('a school test', IDK)], sw_in(T, 2))
    m2 = hl(2)
    bot(c, 420, 560, 170, 1, t=t, mood=hl(1))
    bubble(c, 980, 300, 1700, 420, 'When is my birthday?', INK, 1 - m2, side=1, size=48)
    p = fd(T(0), 1.4, .6) if T(0) > -.1 else 0
    bubble(c, 700, 520, 1240, 640, typed('3 July.', p * 1.2), BOT, fd(T(0), 1.2) * (1 - m2 * .6), side=-1, size=60)
    if hl(1) > .01:
        c.circ(1320, 580, 50, WRONG, hl(1) * (1 - m2)); c.cross(1320, 580, 54, DARK, hl(1) * (1 - m2))
        c.text(1420, 580, 'made up', 40, WRONG, hl(1) * (1 - m2), 'lm', w='Bold')
    if m2 > .01:
        exam(c, 1500, 560, m2, picks=((0, 2, IDK), (1, 0, IDK)), w=380, rows=3)

def s_birthday(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('One question, ', INK), ('three tries', BOT)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Three dates. ', INK), ('All wrong.', WRONG)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('The real one: ', INK), ('autumn', RIGHT)], sw_in(T, 2))
    m1 = hl(1); m2 = hl(2)
    if m2 < .99:
        c.rr(360, 270, 1560, 360, 24, CARD, fd(T(0), 0, .5) * (1 - m2), outline=(70, 80, 130), ow=3)
        c.text(960, 315, 'Birthday? Answer DD-MM, only if you know.', 40, INK, fd(T(0), 0, .5) * (1 - m2), w='Bold', bg=CARD)
    for k, (d, m) in enumerate((('3', 'JULY'), ('15', 'JUNE'), ('1', 'JAN'))):
        x = 560 + k * 400; a = fd(T(0), 1.0 + .8 * k, .4) if T(0) > -.1 else 0
        a *= 1 - m2 * .55
        calendar(c, x, 570 + 30 * (1 - a), a, m, d, BOT, sub=f'try {k + 1}')
        if m1 > .01:
            c.circ(x + 110, 440, 40, WRONG, m1 * fd(T(1), .3 * k, .3) * (1 - m2 * .55)); c.cross(x + 110, 440, 44, DARK, m1 * fd(T(1), .3 * k, .3) * (1 - m2 * .55))
    if m2 > .01:
        tag(c, 960, 828, 'never: "I don\'t know"', IDK, m2, w=620)
    c.text(960, 870, 'Kalai et al., "Why Language Models Hallucinate", 2025', 26, DIM, fd(T(0), 2.5) * (1 - m2), w='Regular')

def s_name(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A ', INK), ('hallucination', WRONG)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Specific', BOT), (', not vague', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('So ', INK), ('why', IDK), ('?', INK)], sw_in(T, 2))
    m0 = 1 - hl(1); m1 = hl(1) * (1 - hl(2)); m2 = hl(2)
    if m0 > .01:
        for k, (lab, col, x) in enumerate((('sounds right', RIGHT, 640), ('is false', WRONG, 1280))):
            a = m0 * fd(T(0), .8 + .7 * k)
            c.rr(x - 260, 360, x + 260, 700, 30, CARD, a, outline=col, ow=5)
            if k == 0: c.check(x, 500, 80, RIGHT, a)
            else: c.cross(x, 500, 90, WRONG, a)
            c.text(x, 630, lab, 48, col, a, w='Bold', bg=CARD)
        c.text(960, 530, '+', 90, INK, m0 * fd(T(0), 1.5), w='Bold')
    if m1 > .01:
        bot(c, 360, 560, 130, m1, t=t, mood=1)
        bubble(c, 620, 340, 1180, 460, '3 July.', BOT, m1, size=60)
        tag(c, 1460, 400, 'specific', BOT, m1, w=320)
        bubble(c, 620, 600, 1180, 720, 'Sometime in autumn?', DIM, m1 * .9, size=44)
        tag(c, 1460, 660, 'vague', DIM, m1, w=320)
    if m2 > .01:
        bot(c, 960, 560, 190, m2, t=t)
        c.text(1230, 360, '?', 160, IDK, m2 * (.7 + .3 * math.sin(t * 3) ** 2), w='Bold')
        tag(c, 960, 820, 'it read more text than any person could', DIM, m2, w=860, size=36)

STREAM = ['the cat sat on the mat', 'we went to the shop', 'the train was late again', 'put the kettle on', 'the sky over the hill',
          'open the door please', 'the end of the day', 'all over the world']
def s_patterns(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('It learns ', INK), ('patterns', PAT)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Spelling', PAT), (': seen millions of times', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('A birthday: ', INK), ('seen once', WRONG)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('1 in 5', WRONG), (' seen once = ', INK), ('1 in 5', WRONG), (' wrong', INK)], sw_in(T, 3), size=72)
    m1 = hl(1); m2 = hl(2); m3 = hl(3)
    ma = 1 - m2
    if ma > .01:
        c.rr(300, 260, 1620, 800, 26, CARD, ma * .95)
        for k, s in enumerate(STREAM):
            yy = 310 + k * 62; off = (t * 40 + k * 90) % 300
            x = 340 - off
            for w_ in (s + ' · ' + s).split():
                ww = c.tw(w_ + ' ', 38, 'Bold')
                if 320 < x < 1560:
                    col = PAT if (w_ == 'the' and m1 > .01) else DIM
                    c.text(x, yy, w_, 38, col, ma * fd(T(0), .3), 'lm', 'Bold', bg=CARD)
                x += ww
        if m1 > .01:
            tag(c, 960, 840, '"the": a pattern it can trust', PAT, m1 * ma, w=640, size=38)
    if m2 > .01 and m3 < .99:
        a = m2 * (1 - m3)
        c.rr(300, 280, 1000, 780, 26, CARD, a * .95)
        for k in range(6):
            c.rr(340, 320 + k * 70, 960, 352 + k * 70, 10, (50, 58, 96), a, bg=CARD)
        c.rr(340, 320 + 3 * 70, 960, 352 + 3 * 70, 10, WRONG, a, bg=CARD)
        c.text(650, 336 + 3 * 70, 'a birthday, mentioned once', 26, DARK, a, w='Bold', bg=WRONG)
        c.text(650, 740, 'no pattern to learn', 34, WRONG, a, w='Bold', bg=CARD)
        # a phone number heard once at a party, fading
        c.rr(1150, 300, 1550, 760, 40, (40, 46, 80), a, outline=(80, 90, 140), ow=4)
        num = '0412 ··· ···'
        c.text(1350, 420, num, 44, INK, a * (1 - .7 * fd(T(2), 2.5, 2.0)), w='Bold', bg=(40, 46, 80))
        c.text(1350, 520, 'heard once', 34, DIM, a, w='Bold', bg=(40, 46, 80))
        c.text(1350, 570, 'at a party', 34, DIM, a, w='Bold', bg=(40, 46, 80))
        c.text(1350, 680, '?', 90, IDK, a * fd(T(2), 3.0), w='Bold', bg=(40, 46, 80))
    if m3 > .01:
        for g, (lab, col) in enumerate((('birthdays seen only once', WRONG), ('expected wrong answers (at least)', WRONG))):
            x0 = 300 + g * 700
            c.rr(x0, 300, x0 + 620, 760, 26, CARD, m3 * .95)
            for k in range(5):
                on = k == 2 and fd(T(3), .5 + .8 * g) > .5
                person(c, x0 + 90 + k * 110, 520, 120, col if on else (70, 80, 130), m3, bg=CARD)
            c.text(x0 + 310, 690, lab, 32, col, m3, w='Bold', bg=CARD)
        c.arrow(925, 520, 995, 520, INK, 6, m3)
        c.text(960, 850, 'After the first training stage (Kalai et al., 2025)', 28, DIM, m3, w='Regular')

def s_exam(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Why ', INK), ('guess', WRONG), (' instead?', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('Think of an ', INK), ('exam', IDK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('How it is ', INK), ('scored', IDK)], sw_in(T, 2))
    m0 = 1 - hl(1); m1 = hl(1); m2 = hl(2)
    if m0 > .01:
        bot(c, 960, 560, 170, m0, t=t)
        tag(c, 560, 420, 'errors', WRONG, m0, w=260); c.check(560 + 170, 420, 40, RIGHT, m0)
        tag(c, 1360, 420, 'guessing?', IDK, m0, w=300); c.text(1360 + 190, 420, '?', 70, IDK, m0, w='Bold')
    if m1 > .01:
        ex = 560 + 0 * m2
        exam(c, ex, 540, m1, picks=((0, 1, RIGHT), (1, 3, RIGHT)) if m2 > .01 else (), w=440)
        # a pencil
        px = ex + 180 + 30 * math.sin(t * 2)
        poly(c, [(px, 640), (px + 26, 640), (px + 80, 420), (px + 54, 420)], IDK, m1 * (1 - m2))
    if m2 > .01:
        score_row(c, 1300, 380, 'Right answer', '+1', RIGHT, m2 * fd(T(2), .3))
        score_row(c, 1300, 520, 'Blank / "I don\'t know"', '0', IDK, m2 * fd(T(2), 1.0))
        score_row(c, 1300, 660, 'Wrong answer', '0', WRONG, m2 * fd(T(2), 1.8))

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a teal pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [("You don't know. ", INK), ('Blank', IDK), (' or ', INK), ('guess', WRONG), ('?', INK)], 1, bg=QUIZ, size=76)
    for k, (lab, col) in enumerate((('Leave it blank', IDK), ('Guess', WRONG))):
        x = 560 + k * 800
        c.rr(x - 320, 300, x + 320, 690, 30, CARD, 1, outline=col, ow=5, bg=QUIZ)
        if k == 0:
            c.circ(x, 470, 70, None, 1, outline=INK, ow=5, bg=CARD)
        else:
            for j in range(4):
                c.circ(x - 165 + j * 110, 470, 42, WRONG if j == int(t * 2) % 4 else None, 1, outline=INK, ow=4, bg=CARD)
        c.text(x, 620, lab, 46, col, 1, w='Bold', bg=CARD)
    if T(0) > 0:
        e = T(0) - 5.0; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), 4.8)
        c.circ(960, 790, 60, IDK, u, bg=QUIZ); c.text(960, 790, str(k) if k else '?', 60, DARK, u, w='Bold', bg=IDK)

def s_reveal(c, T, t):
    """The big reveal, placed about two thirds of the way in (lesson of 2026-11-18, OutlierKit)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Guess', WRONG), (': right 1 time in 4', INK)], sw_out(T, 1) * sw_out(T, 2))
    headline(c, [('AI tests ', INK), ('score the same', IDK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Guessing ', WRONG), ('wins', INK)], sw_in(T, 2))
    m0 = 1 - hl(1); m1 = hl(1) * (1 - hl(2)); m2 = hl(2)
    if m0 > .01:
        for k in range(4):
            x = 420 + k * 170; on = k == 2
            c.circ(x, 420, 66, RIGHT if on and fd(T(0), 1.2) > .5 else None, m0, outline=INK, ow=5)
            c.text(x, 420, 'ABCD'[k], 50, DARK if on and fd(T(0), 1.2) > .5 else INK, m0, w='Bold', bg=RIGHT if on and fd(T(0), 1.2) > .5 else BG)
        c.text(675, 540, '1 chance in 4', 40, RIGHT, m0 * fd(T(0), 1.4), w='Bold')
        for k, (lab, v, col) in enumerate((('guess', .25, WRONG), ('blank', 0.0, IDK))):
            x = 1240 + k * 300; hh = 900 * v * fd(T(0), 2.0, .8)
            c.rr(x - 90, 760 - max(hh, 6), x + 90, 760, 14, col, m0)
            c.text(x, 760 - max(hh, 6) - 36, f'{v:.2f}', 40, col, m0 * fd(T(0), 2.4), w='Bold')
            c.text(x, 800, lab, 34, col, m0, w='Bold')
        c.text(1390, 860, 'average points per question', 28, DIM, m0, w='Regular')
    if m1 > .01:
        for k in range(3):
            x = 480 + k * 480
            c.rr(x - 200, 290, x + 200, 760, 26, CARD, m1 * fd(T(1), .2 * k), outline=(70, 80, 130), ow=3)
            c.text(x, 340, f'AI test {"ABC"[k]}', 36, INK, m1 * fd(T(1), .2 * k), w='Bold', bg=CARD)
            for j, (lab, pts, col) in enumerate((('right', '+1', RIGHT), ("I don't know", '0', IDK), ('wrong', '0', WRONG))):
                yy = 450 + j * 100
                c.text(x - 160, yy, lab, 32, col, m1 * fd(T(1), .2 * k), 'lm', 'Bold', bg=CARD)
                c.text(x + 160, yy, pts, 40, INK, m1 * fd(T(1), .2 * k), 'rm', 'Bold', bg=CARD)
        c.text(960, 840, 'Simplified. Most popular AI tests give no credit for "I don\'t know" (Kalai et al., 2025)', 28, DIM, m1, w='Regular')
    if m2 > .01:
        for k, (lab, col, sc, mood) in enumerate((('always answers', WRONG, 'higher score', 1), ('says "I don\'t know"', IDK, 'lower score', 0))):
            x = 620 + k * 680; lift = -40 * (1 - k) * fd(T(2), .8, .6)
            bot(c, x, 520 + lift, 120, m2, t=t + k, mood=mood)
            c.text(x, 700, lab, 38, col, m2, w='Bold')
            c.rr(x - 150, 760, x + 150, 830, 20, CARD, m2, outline=col, ow=3)
            c.text(x, 795, sc, 34, INK, m2, w='Bold', bg=CARD)
        c.text(960, 300, 'Illustrative', 28, DIM, m2, w='Regular')

def s_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('Change the ', INK), ('scoring', IDK)], sw_out(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Wrong ', WRONG), ('costs points', INK)], sw_in(T, 1) * sw_out(T, 2) * sw_out(T, 3))
    headline(c, [('Answer only if ', INK), ('> 75%', RIGHT), (' sure', INK)], sw_in(T, 2) * sw_out(T, 3))
    headline(c, [('"I don\'t know"', IDK), (' is now smart', INK)], sw_in(T, 3))
    m1 = hl(1); m2 = hl(2); m3 = hl(3)
    ma = 1 - m2
    if ma > .01:
        score_row(c, 960, 340, 'Right answer', '+1', RIGHT, ma)
        score_row(c, 960, 480, 'Blank / "I don\'t know"', '0', IDK, ma)
        wv = '0' if m1 < .5 else '−3'
        score_row(c, 960, 620, 'Wrong answer', wv, WRONG, ma)
        if m1 > .01:
            c.rr(1290, 580, 1370, 660, 20, WRONG, m1 * ma * (.6 + .4 * math.sin(t * 5) ** 2)); c.text(1330, 620, '!', 50, DARK, m1 * ma, w='Bold', bg=WRONG)
    if m2 > .01:
        p = .6 + .3 * math.sin(T(2) * .9) if m3 < .01 else .6
        meter(c, 360, 1560, 500, p, m2, thr=.75)
        sure = int(round(p * 100))
        ok = p > .75
        c.text(960, 380 if m3 < .5 else 380, (f'{sure}% sure: answer' if ok else f'{sure}% sure: say "I don\'t know"'), 44, RIGHT if ok else IDK, m2 * (1 - m3), w='Bold')
        c.text(960, 860, 'Example threshold from Kalai et al., 2025: a mistake costs 3 points', 28, DIM, m2, w='Regular')
    if m3 > .01:
        c.rr(460, 640, 1460, 800, 26, CARD, m3, outline=IDK, ow=4)
        c.text(960, 690, 'At 60% sure, answering averages:', 36, INK, m3, w='Bold', bg=CARD)
        c.text(960, 750, '0.6 × (+1) + 0.4 × (−3) = −0.6', 42, WRONG, m3, w='Bold', bg=CARD)

def s_you(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('A ', INK), ('confident', BOT), (' friend', INK)], sw_out(T, 1))
    headline(c, [('Check ', INK), ('rare facts', RIGHT)], sw_in(T, 1))
    m1 = hl(1)
    bot(c, 520, 560, 170, 1, t=t, mood=1)
    bubble(c, 800, 300, 1300, 410, 'Ideas!', BOT, 1 - m1 * .5, size=52)
    bubble(c, 1340, 300, 1760, 410, 'Drafts!', BOT, (1 - m1 * .5) * fd(T(0), .8), size=52)
    if m1 > .01:
        for k, lab in enumerate(('names', 'dates', 'numbers', 'quotes')):
            y = 510 + k * 88; a = m1 * fd(T(1), .3 + .4 * k)
            c.rr(900, y - 36, 1460, y + 36, 18, CARD, a, outline=RIGHT, ow=3)
            c.text(940, y, lab, 40, INK, a, 'lm', 'Bold', bg=CARD)
            c.circ(1410, y, 22, None, a, outline=RIGHT, ow=4, bg=CARD); c.check(1410, y, 22, RIGHT, a, p=fd(T(1), .6 + .4 * k, .4))
        # magnifier
        c.circ(1620, 560, 80, None, m1, outline=INK, ow=10); c.line([(1676, 616), (1740, 690)], INK, 16, m1)

def s_recap(c, T, t):
    """Recap as three stacked rows with an icon on the left (the last two recaps used side-by-side cards)."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', IDK)], 1)
    items = ((1, 'A fact seen once has no pattern to learn', PAT), (2, 'Most AI tests score "I don\'t know" as zero', IDK),
             (3, 'Make mistakes cost more, and guessing stops paying', RIGHT))
    for ln, txt, col in items:
        m = hl(ln); y = 370 + (ln - 1) * 170; dx = 60 * (1 - m)
        c.rr(260 + dx, y - 66, 1660 + dx, y + 66, 30, CARD, m, outline=col, ow=4)
        c.circ(340 + dx, y, 44, col, m, bg=CARD); c.text(340 + dx, y, str(ln), 50, DARK, m, w='Bold', bg=col)
        c.text(420 + dx, y, txt, 41, INK, m, 'lm', 'Bold', bg=CARD)
    c.text(960, 856, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    bot(c, 1560, 640, 210, 1, t=1.0, mood=1)
    bubble(c, 1210, 180, 1820, 330, '3 July!', BOT, 1, size=84)
    c.circ(1790, 200, 50, WRONG, 1); c.cross(1790, 200, 54, DARK, 1)

SCENES = [
 ('THE QUESTION', ["Ask an AI chatbot something it can't know, and it often won't say \"I don't know\".",
                   "It will guess. Confidently.",
                   "In twenty twenty-five, researchers at OpenAI and Georgia Tech explained why. The answer is a school test."], s_hook),
 ('THE BIRTHDAY', ["They asked a popular chatbot for the birthday of one of the researchers. Answer only if you know, it was told.",
                   "Three tries. Three different dates. All wrong.",
                   "The real birthday is in autumn. And not once did it say \"I don't know\"."], s_birthday),
 ('A HALLUCINATION', ["This is called a hallucination. An answer that sounds right, but is false.",
                      "And notice, it isn't vague. It says the third of July, not sometime in autumn.",
                      "So why would a machine that has read so much do this?"], s_name),
 ('HOW IT LEARNS', ["First, how it learns. It finds patterns in huge amounts of text.",
                    "Spelling is a pattern. It sees words like \"the\" millions of times, so spelling mistakes are rare.",
                    "But a person's birthday might appear just once. There's no pattern to learn. Like a phone number you heard once at a party.",
                    "The paper puts a number on it. If one in five birthdays appears only once in the training text, expect at least one in five wrong."], s_patterns),
 ('THE EXAM', ["But that only explains the errors. Not why it guesses instead of admitting it.",
               "For that, think of a multiple-choice exam.",
               "A right answer gets one point. A blank gets zero. And a wrong answer also gets zero."], s_exam),
 ('QUICK QUESTION', ["Quick question. You don't know the answer. Should you leave it blank, or guess?"], s_quiz),
 ('THE TWIST', ["Guess. With four choices, a guess is right one time in four. A blank is never right.",
                "Now here's the twist. Most of the popular tests used to score AI chatbots work the same way. \"I don't know\" earns zero.",
                "So a chatbot that always answers beats one that admits it doesn't know. Tuned to ace these tests, chatbots learn to guess."], s_reveal),
 ('THE FIX', ["The researchers' fix is simple. Change the scoring.",
              "Make a wrong answer cost points, while \"I don't know\" costs nothing.",
              "For example, tell it to answer only if it's more than seventy-five percent sure, because a mistake costs three points.",
              "At sixty percent sure, answering now loses points on average. So \"I don't know\" becomes the smart move."], s_fix),
 ('FOR YOU', ["Until then, treat a chatbot like a confident friend. Great for ideas and drafts.",
              "But check the names, dates, numbers and quotes it gives you, especially rare ones."], s_you),
 ('RECAP', ["Three things to keep.",
            "One: chatbots learn patterns, and a fact seen only once has no pattern.",
            "Two: most AI tests score \"I don't know\" as zero, so guessing wins.",
            "Three: make mistakes cost more than honesty, and guessing stops paying.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story with the answer ----------
def short_hook(c, T, t):
    headline(c, [('It ', INK), ('guesses', WRONG)], 1, size=96)
    bot(c, 420, 560, 170, 1, t=t, mood=1)
    bubble(c, 980, 300, 1700, 420, 'When is my birthday?', INK, 1, side=1, size=48)
    p = fd(t, .5, .6)
    bubble(c, 700, 520, 1240, 640, typed('3 July.', p * 1.2), BOT, fd(t, .3), side=-1, size=60)
    c.circ(1320, 580, 50, WRONG, fd(t, 1.6)); c.cross(1320, 580, 54, DARK, fd(t, 1.6))
    c.text(1420, 580, 'made up', 40, WRONG, fd(t, 1.6), 'lm', w='Bold')

SHORT_SCENES = [
 ('THE GUESS', ["Why do AI chatbots make things up, instead of saying \"I don't know\"?",
                "Researchers asked one for a birthday it couldn't know. Three tries. Three different dates. All of them wrong."], short_hook),
 ('THE EXAM', ["The reason is a school test.",
               "On a multiple-choice exam, you get one point for a right answer. A blank gets zero.",
               "And a wrong answer also gets zero."], s_exam),
 ('THE TWIST', ["So guessing always wins. A guess is sometimes right. A blank never is.",
                "Most of the tests used to score chatbots work the same way. \"I don't know\" earns zero.",
                "So chatbots learn to guess."], s_reveal),
 ('THE ANSWER', ["They're trained to ace tests that reward guessing.", "So make wrong answers cost points, and honesty starts to win."],
  card('Tests reward guessing.', 'So chatbots guess.')),
]
SHORT_HITS = [(2, 2, 0.0)]
