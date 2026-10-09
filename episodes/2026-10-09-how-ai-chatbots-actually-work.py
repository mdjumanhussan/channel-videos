"""Episode: How AI Chatbots Actually Work. Use this file as the template for new episodes."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How AI Chatbots Work'      # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.96
CAPTION_FIXES = {'A.I.': 'AI'}             # narration spelling -> caption spelling
THUMB_AT = 17                              # second of the video used as thumbnail

# ---------------------------------------------------------------- scenes
# each scene: (chapter label, [narration lines], draw(c, T, t)) ; T(i) = seconds since line i began

def s_hook(c, T, t):
    a = 1 - fd(T(5), 0, .5)
    if a > 0:
        c.rr(460, 170, 1460, 800, 36, CARD, a)
        c.rr(460, 170, 1460, 250, 36, (38, 46, 90), a)
        c.circ(510, 210, 12, PK, a); c.circ(548, 210, 12, YE, a); c.circ(586, 210, 12, GR, a)
        c.text(960, 210, 'Chat', 30, DIM, a)
        q = 'Why is the sky blue?'
        qs = typed(q, T(0) / 1.1)
        if qs:
            w = c.tw(qs, 40, 'Medium') + 70
            c.rr(1410 - w, 300, 1410, 390, 30, CY, a)
            c.text(1410 - w + 35, 345, qs, 40, BG, a, 'lm', 'Medium', bg=mix(CY, a))
        if T(1) > 0:
            r = 'Sunlight scatters off the air, and blue light scatters far more than red.'
            ls = wrap(c, r, 38, 720)
            n = int(len(r) * clamp(T(1) / 2.8));
            if T(1) < .5:
                for i in range(3):
                    c.circ(540 + i * 34, 475 + 8 * math.sin(t * 9 + i), 9, DIM, a)
            else:
                c.rr(510, 430, 1310, 430 + 60 * len(ls) + 50, 30, (44, 52, 100), a)
                k = int(len(r) * clamp((T(1) - .5) / 2.6))
                for i, l in enumerate(ls):
                    c.text(545, 485 + i * 60, l[:max(0, k)], 38, INK, a, 'lm', 'Medium', bg=mix((44, 52, 100), a))
                    k -= len(l) + 1
        if T(2) > 0:
            m = fd(T(2)) * a
            for i in range(14):
                ang = i * 2.4 + t * .6; rad = 430 + 60 * math.sin(i * 1.7 + t)
                x = 960 + rad * math.cos(ang) * 1.15; y = 480 + rad * math.sin(ang) * .62
                r0 = 7 + 5 * math.sin(t * 4 + i)
                c.line([(x - r0 * 2, y), (x + r0 * 2, y)], YE, 3, m); c.line([(x, y - r0 * 2), (x, y + r0 * 2)], YE, 3, m)
            c.text(960, 700, 'Magic?', 84, YE, m, w='Bold', bg=mix(CARD, a))
            if T(3) > 0:
                p = ease(T(3) / .35)
                c.line([(790, 704), (790 + 340 * p, 704)], PK, 10, a)
    if T(4) > 0 and T(5) < 0:
        c.text(960, 870 - 0, '', 1)
    if T(5) > 0:
        m = fd(T(5), .2, .7)
        c.text(960, 400 + 30 * (1 - m), 'How AI Chatbots', 130, INK, m, w='Bold')
        c.text(960, 560 + 30 * (1 - m), 'Actually Work', 130, CY, m, w='Bold')
        c.line([(960 - 260 * m, 670), (960 + 260 * m, 670)], YE, 8, m)
        c.text(960, 740, 'Explained in 3 minutes', 44, DIM, fd(T(5), .8), w='Medium')

def s_trick(c, T, t):
    a0 = fd(T(1)) * (1 - fd(T(3), -.4, .4))
    c.text(960, 400, 'It guesses', 110, INK, a0, w='Bold')
    c.text(960, 550, 'the next word.', 110, CY, a0, w='Bold')
    c.text(960, 690, "That's all.", 60, YE, fd(T(2)) * (1 - fd(T(3), -.4, .4)), w='Medium')
    if T(3) > -.1:
        m = fd(T(3)); up = ease(T(5) / .6) * 190
        y = 480 - up
        base = 'The sky is '
        wb = c.tw(base, 110, 'Bold'); x0 = 960 - (wb + 300) / 2
        c.text(x0, y, base, 110, INK, m, 'lm', 'Bold')
        bx = x0 + wb + 10
        got = T(4) > 0.25
        c.rr(bx, y - 78, bx + 300, y + 78, 22, None, m, outline=CY if got else DIM, ow=5)
        if got: c.text(bx + 150, y, 'blue', 110, CY, fd(T(4), .25, .3), w='Bold')
        elif int(t * 2.5) % 2 == 0: c.rr(bx + 30, y - 50, bx + 36, y + 50, 2, DIM, m)
        if T(5) > 0.3:
            bars = [('blue', .72, CY), ('clear', .09, PU), ('falling', .05, PU), ('grey', .04, PU), ('the', .02, PU)]
            for i, (wd, p, col) in enumerate(bars):
                bm = fd(T(5), .5 + i * .22, .5); yy = 480 + i * 74
                c.text(640, yy, wd, 44, INK, bm, 'rm', 'Medium')
                c.rr(670, yy - 22, 1330, yy + 22, 22, CARD, bm)
                c.rr(670, yy - 22, 670 + max(44, 660 * p / .72 * bm), yy + 22, 22, col, bm)
                c.text(1360, yy, f'{int(p * 100 * bm)}%', 40, DIM, bm, 'lm', 'Medium')
            c.text(960, 858, 'Illustrative scores, not real model output', 26, DIM, fd(T(5), 1.6) * .8, w='Regular')

TOK = [('Chat', CY), ('bots', PU), (' are', GR), (' un', YE), ('believ', PK), ('able', CY)]
IDS = ['1723', '9048', '389', '653', '31794', '540']
def s_tokens(c, T, t):
    sp = ease(T(0, .9) / .8)
    ws = [c.tw(x, 84, 'Bold') + 44 for x, _ in TOK]
    gap = 26 * sp; tot = sum(ws) + gap * 5; x = 960 - tot / 2
    c.text(960, 250, 'Tokens', 60, DIM, fd(T(0, .9)), w='Medium')
    for i, ((tx, col), w) in enumerate(zip(TOK, ws)):
        yy = 440
        c.rr(x, yy - 80, x + w, yy + 80, 22, mix(col, .22, CARD), fd(T(0)) , outline=col if sp > .05 else None, ow=4 * sp)
        c.text(x + w / 2, yy, tx.strip(), 84, INK, fd(T(0)), w='Bold', bg=mix(mix(col, .22, CARD), 1))
        part = i in (0, 1, 3, 4, 5)
        if T(1) > 0 and part:
            pm = fd(T(1), .2 + i * .08)
            c.line([(x + 14, yy + 104), (x + w - 14, yy + 104)], col, 5, pm)
        if T(2) > 0:
            nm = fd(T(2), .2 + i * .15)
            c.arrow(x + w / 2, yy + 125, x + w / 2, yy + 200, DIM, 4, nm, 12)
            c.rr(x + w / 2 - 80, yy + 215, x + w / 2 + 80, yy + 295, 16, CARD, nm, outline=col, ow=3)
            c.text(x + w / 2, yy + 255, IDS[i], 40, col, nm, w='Mono', bg=CARD)
        x += w + gap
    c.text(960, 590, 'word pieces', 36, DIM, fd(T(1), .5) * (1 - fd(T(2), 0, .3)), w='Regular')
    c.text(960, 800, 'Example split. Real tokenizers vary.', 26, DIM, fd(T(2), 1.2) * .8, w='Regular')

def s_train(c, T, t):
    c.text(960, 480, 'How does it learn?', 100, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) > -.1:
        m = fd(T(1))
        for i, (lab, col) in enumerate([('Books', CY), ('Articles', PU), ('Websites', GR)]):
            im = fd(T(1), .5 + i * .75) * m; y = 290 + i * 180
            c.rr(150, y - 65, 640, y + 65, 22, CARD, im, outline=col, ow=3)
            c.rr(180, y - 38, 240, y + 38, 8, col, im)
            for k in range(3): c.line([(190, y - 18 + k * 18), (230, y - 18 + k * 18)], CARD, 4, im)
            c.text(275, y, lab, 50, INK, im, 'lm', bg=CARD)
            for k in range(3):
                px = 660 + ((t * 90 + k * 60 + i * 20) % 180)
                c.circ(px, y, 6, col, im * (1 - (px - 660) / 180))
    if T(2) > 0:
        m = fd(T(2))
        c.rr(880, 220, 1780, 800, 30, CARD, m)
        c.text(1330, 280, 'The guessing game', 40, DIM, m, w='Medium', bg=CARD)
        base = 'The cat sat on the '
        c.text(950, 400, base, 56, INK, m, 'lm', bg=CARD)
        bx = 950 + c.tw(base, 56)
        rnd2 = T(4) > 2.4
        guess, ok = ('mat', True) if rnd2 else ('moon', False)
        showg = T(3) > 1.0
        c.rr(bx, 356, bx + 210, 444, 14, (20, 24, 52), m, outline=(GR if ok else PK) if (showg and (T(3) > 2.0)) else DIM, ow=4)
        if showg: c.text(bx + 105, 400, guess, 52, INK, fd(T(3), 1.0, .25) if not rnd2 else fd(T(4), 2.4, .25), bg=(20, 24, 52))
        else: c.text(bx + 105, 400, '?', 52, DIM, m, bg=(20, 24, 52))
        if T(3) > 2.0:
            if rnd2: c.check(bx + 270, 400, 40, GR, 1, clamp((T(4) - 2.7) / .4))
            else:
                c.cross(bx + 270, 400, 40, PK, fd(T(3), 2.0, .2))
                c.text(950, 500, 'Answer:  mat', 44, GR, fd(T(3), 2.3, .3), 'lm', 'Medium', bg=CARD)
        if T(4) > 0:
            am = fd(T(4))
            c.text(950, 610, 'Adjust', 40, YE, am, 'lm', 'Medium', bg=CARD)
            for k in range(8):
                x = 1130 + k * 76
                h = 30 + 22 * math.sin(k * 1.3) + 14 * ease(T(4) / 2.2) * math.sin(k * 2.1 + 1)
                c.rr(x, 660, x + 12, 560, 6, (20, 24, 52), am)
                c.circ(x + 6, 610 - h, 14, YE, am)
        n = int(1e9 * clamp(T(2) / 7) ** 2)
        c.text(1330, 735, f'Rounds played: {n:,}+' if T(2) > .4 else '', 34, DIM, m, w='Mono', bg=CARD)

def s_dials(c, T, t):
    m = fd(T(0)); L = [3, 5, 5, 2]; xs = [330, 560, 790, 1020]
    pos = [[(xs[i], 500 + (j - (n - 1) / 2) * 112) for j in range(n)] for i, n in enumerate(L)]
    sh = ease(T(1) / .6); sc = 1 - .0 * sh
    for i in range(3):
        for a_ in pos[i]:
            for b_ in pos[i + 1]:
                ph = (t * 1.2 + a_[1] * .01 + b_[1] * .013 + i) % 1
                c.line([a_, b_], PU, 2, m * .35)
                c.circ(a_[0] + (b_[0] - a_[0]) * ph, a_[1] + (b_[1] - a_[1]) * ph, 4, CY, m * .7 * math.sin(ph * math.pi))
    for i, col in enumerate([CY, PU, PU, GR]):
        for p in pos[i]:
            c.circ(p[0], p[1], 30, CARD, m, outline=col, ow=5)
    c.text(675, 860 - 30, 'Neural network', 34, DIM, m, w='Medium')
    if T(1) > 0:
        dm = fd(T(1))
        turn = ease(T(3) / 2.4) if T(3) > 0 else 0
        for r in range(3):
            for k in range(4):
                x = 1270 + k * 140; y = 300 + r * 150; idx = r * 4 + k
                c.circ(x, y, 50, CARD, dm, outline=DIM, ow=4)
                a0 = idx * 1.9 + .3 * math.sin(t * 2 + idx) * (1 - turn)
                a1 = -math.pi / 2 + (idx % 3 - 1) * .5
                ang = a0 + (a1 - a0) * turn
                col = mix(YE, 1 - turn, GR)
                c.line([(x, y), (x + 38 * math.cos(ang), y + 38 * math.sin(ang))], col, 7, dm)
                c.circ(x, y, 8, col, dm)
                if T(2) > 0:
                    v = (math.cos(ang) * .5 + .5)
                    c.text(x, y + 72, f'{v:.2f}', 24, DIM, fd(T(2), idx * .04), w='Mono')
        c.text(1480, 200, 'Billions of dials', 40, INK, dm, w='Medium')
        if T(3) > 0:
            gm = fd(T(3))
            c.text(1270 - 50, 780, 'Guess quality', 32, DIM, gm, 'lm', 'Medium')
            c.rr(1220, 810, 1740, 840, 15, CARD, gm)
            c.rr(1220, 810, 1220 + max(30, 520 * (.12 + .82 * turn)), 840, 15, mix(YE, 1 - turn, GR), gm)
    c.text(960, 860 + 30, '', 1)

SENT = ['I', 'sat', 'on', 'the', 'bank', 'of', 'the', 'river']
ATT = [.15, .35, .2, .05, 0, .12, .05, 1.0]
def s_attn(c, T, t):
    c.text(960, 480, 'Words depend on each other', 84, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) < -.1: return
    ws = [c.tw(w, 76, 'Bold') for w in SENT]; gap = 44; tot = sum(ws) + gap * 7; x = 960 - tot / 2; cx = []
    y = 560
    for w in ws: cx.append(x + w / 2); x += w + gap
    for i, wd in enumerate(SENT):
        m = fd(T(1), 1.0 + i * .22, .3)
        col = INK
        if i == 4 and T(2) > 0: col = YE
        if i == 7 and T(5) > 0: col = GR
        if i == 4 and T(2) > 0:
            c.rr(cx[i] - ws[i] / 2 - 18, y - 58, cx[i] + ws[i] / 2 + 18, y + 58, 16, None, fd(T(2)), outline=YE, ow=4)
        c.text(cx[i], y, wd, 76, col, m, w='Bold')
    if T(2) > 0:
        res = T(5) > 1.2
        m1 = fd(T(2), .3) * (1 - (fd(T(5), 1.2) * .75 if res else 0)); m2 = fd(T(2), 1.3)
        c.rr(470, 730, 900, 830, 22, CARD, m1, outline=DIM, ow=3); c.text(685, 780, 'money bank?', 42, INK, m1, w='Medium', bg=CARD)
        c.rr(1020, 730, 1450, 830, 22, CARD, m2, outline=GR if res else DIM, ow=5 if res else 3)
        c.text(1235 - (24 if res else 0), 780, 'river bank' + ('' if res else '?'), 42, GR if res else INK, m2, w='Medium', bg=CARD)
        if res: c.check(1400, 780, 26, GR, 1, clamp((T(5) - 1.4) / .4))
    if T(3) > 0:
        c.text(960, 175, 'Attention', 64, CY, fd(T(3)), w='Bold')
        for i in range(8):
            if i == 4: continue
            g = ease((T(4) - .1 - abs(i - 4) * .12) / .6) if T(4) > 0 else 0
            base = .25 * fd(T(3), .3)
            wgt = ATT[i]; boost = ease(T(5) / .6) if (i == 7 and T(5) > 0) else 0
            a = base + g * (.15 + .6 * wgt) + boost * .2
            wd = 2 + g * (2 + 12 * wgt) + boost * 4
            hgt = 80 + abs(cx[i] - cx[4]) * .3
            pts = []
            for k in range(41):
                u = k / 40; px = cx[4] + (cx[i] - cx[4]) * u; py = y - 62 - hgt * 4 * u * (1 - u)
                pts.append((px, py))
            c.line(pts, GR if (i == 7 and T(5) > 0) else CY, wd, clamp(a))

LOOP = [('Read the text so far', CY), ('Score every next word', PU), ('Pick one word', YE)]
OUT = 'The sky is blue because air scatters blue light the most .'.split()
def s_loop(c, T, t):
    c.text(960, 480, 'Now it writes.', 110, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1))
    k = max(0.0, T(1)); n = 3 + int(k / 1.15); n = min(n, len(OUT)); step = (k % 1.15) / 1.15
    done = n >= len(OUT) and k / 1.15 > len(OUT) - 2.5
    act = -1 if done else int(step * 3)
    pos = [(400, 330), (960, 330), (1520, 330)]
    for i, ((lab, col), (x, y)) in enumerate(zip(LOOP, pos)):
        on = i == act
        c.rr(x - 235, y - 70, x + 235, y + 70, 26, mix(col, .28, CARD) if on else CARD, m, outline=col, ow=6 if on else 3)
        c.text(x, y, lab, 38, INK, m, w='Medium', bg=mix(col, .28, CARD) if on else CARD)
        if i < 2: c.arrow(x + 250, y, pos[i + 1][0] - 250, y, DIM, 5, m)
    pts = [(1520, 410), (1520, 480), (400, 480), (400, 415)]
    c.line(pts[:3], DIM, 5, m); c.arrow(400, 480, 400, 412, DIM, 5, m)
    c.text(960, 515, 'repeat', 30, DIM, m, w='Medium')
    c.rr(240, 610, 1680, 800, 28, CARD, m)
    line = ' '.join(OUT[:n]).replace(' .', '.')
    prev = ' '.join(OUT[:n - 1]).replace(' .', '.')
    c.text(290, 705, line, 50, INK, m, 'lm', 'Medium', bg=CARD)
    if n > 3 and not done and step < .35:
        x0 = 290 + c.tw(prev + (' ' if OUT[n - 1] != '.' else ''), 50, 'Medium')
        c.text(x0, 705, OUT[n - 1], 50, YE, m, 'lm', 'Medium', bg=CARD)
    if not done and int(t * 3) % 2 == 0:
        xe = 290 + c.tw(line, 50, 'Medium') + 10
        c.rr(xe, 678, xe + 5, 732, 2, CY, m)

def s_limits(c, T, t):
    c.text(960, 480, 'Why it makes mistakes', 96, INK, fd(T(0)) * (1 - fd(T(1), -.4, .4)), w='Bold')
    if T(1) < -.1: return
    m = fd(T(1)); out = 1 - fd(T(5), -.2, .5)
    # no fact book
    bm = m * (1 - fd(T(2), -.3, .4))
    c.rr(760, 300, 1160, 660, 18, CARD, bm, outline=DIM, ow=4)
    c.line([(960, 300), (960, 660)], DIM, 4, bm)
    for k in range(5):
        c.line([(800, 360 + k * 55), (920, 360 + k * 55)], DIM, 5, bm * .6); c.line([(1000, 360 + k * 55), (1120, 360 + k * 55)], DIM, 5, bm * .6)
    c.text(960, 730, 'No built-in book of facts', 46, INK, bm, w='Medium')
    c.cross(960, 480, 190, PK, bm * fd(T(1), .8))
    c.text(960, 800, '(unless it has a search tool)', 32, DIM, bm * fd(T(1), 3.2), w='Regular')
    if T(2) > -.1:
        vm = fd(T(2)) * out
        c.circ(790, 480, 250, None, vm, outline=CY, ow=6)
        c.circ(1130, 480, 250, None, fd(T(3)) * out, outline=GR, ow=6)
        c.text(650, 190, 'Sounds likely', 44, CY, vm, w='Medium')
        c.text(1270, 190, 'Is true', 44, GR, fd(T(3)) * out, w='Medium')
        c.text(960, 480, 'Usually', 40, INK, fd(T(3), .2) * out, w='Medium')
        hm = fd(T(3), 1.9) * out
        pulse = 1 + .08 * math.sin(t * 5) if T(4) > 0 else 1
        c.circ(680, 480, 16 * pulse, PK, hm)
        c.text(680, 392, 'confidently', 28, PK, hm, w='Medium'); c.text(680, 428, 'wrong', 28, PK, hm, w='Medium')
        c.rr(250, 760, 830, 850, 22, CARD, fd(T(4)) * out, outline=PK, ow=4)
        c.text(540, 805, 'Hallucination', 48, PK, fd(T(4)) * out, w='Bold', bg=CARD)
        c.line([(600, 760), (670, 505)], PK, 3, fd(T(4), .3) * out * .8)
    if T(5) > 0:
        fm = fd(T(5), .2)
        c.circ(960, 400, 110, None, fm, outline=GR, ow=10)
        c.check(960, 405, 120, GR, fm, clamp((T(5) - .4) / .5))
        c.text(960, 610, 'Always check the important facts', 64, INK, fm, w='Bold')

REC = [('1', 'Text becomes tokens', CY), ('2', 'Predict the next token', PU), ('3', 'Repeat, one at a time', YE)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 210, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(REC):
        m = fd(T(i + 1)) * out; y = 380 + i * 160 + 20 * (1 - fd(T(i + 1)))
        c.rr(400, y - 62, 1520, y + 62, 28, CARD, m, outline=col, ow=4)
        c.circ(480, y, 42, col, m)
        c.text(480, y, nn, 50, BG, m, w='Bold', bg=col)
        c.text(560, y, lab, 54, INK, m, 'lm', bg=CARD)
    if T(4) > 0:
        o2 = 1 - fd(T(5), -.3, .5)
        c.text(960, 420, 'Not magic.', 130, INK, fd(T(4)) * o2, w='Bold')
        c.text(960, 600, 'Just maths, at enormous scale.', 76, CY, fd(T(4), 1.0) * o2, w='SemiBold')
    if T(5) > 0:
        m = fd(T(5), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'More explainers coming soon', 44, DIM, fd(T(5), .7), w='Medium')
        c.text(960, 690, 'Md Juman Hussan JP', 36, CY, fd(T(5), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["You type a question.", "A second later, a chatbot writes back, just like a person.", "It feels like magic.", "It is not magic.",
            "It is one simple trick, repeated very, very fast.", "Let's see how A.I. chatbots actually work."], s_hook),
 ('1  ·  THE TRICK', ["Here is the trick.", "The chatbot guesses the next word.", "That is all.", "Try it yourself. The sky is...",
            "You probably said blue.", "So did the chatbot. It gives every possible word a score, and blue scores highest."], s_trick),
 ('2  ·  TOKENS', ["First, it chops your sentence into small pieces called tokens.", "A token can be a whole word, or just part of a word.",
            "Each token becomes a number, because computers only work with numbers."], s_tokens),
 ('3  ·  TRAINING', ["So how does it learn to guess well?", "It reads. A huge amount of text. Books, articles, and websites.",
            "During training, it plays one game, billions of times.", "Hide the next word. Guess it. Check the answer.",
            "When the guess is wrong, it adjusts itself a tiny bit. Then it tries again."], s_train),
 ('4  ·  THE NETWORK', ["Those tiny adjustments happen inside a neural network.", "Picture billions of little dials.", "Each dial is just a number.",
            "Training turns the dials until the guesses get good.", "Nobody writes the rules by hand. The patterns are learned."], s_dials),
 ('5  ·  ATTENTION', ["But words depend on each other.", "Take this sentence. I sat on the bank of the river.", "Is that a money bank, or a river bank?",
            "The model uses something called attention.", "It looks at the other words to decide.", "River tells it: this is the land kind of bank."], s_attn),
 ('6  ·  WRITING', ["Now it writes.", "It picks one word, and adds it to the sentence.", "Then it guesses again. And again.",
            "One piece at a time, until the answer is done.", "That is why the reply appears word by word."], s_loop),
 ('7  ·  LIMITS', ["This also explains its mistakes.", "The chatbot does not look things up in a book of facts, unless it is given a search tool.",
            "It writes what sounds likely.", "Usually that is right. Sometimes it is confidently wrong.", "People call this a hallucination.",
            "So always check the important facts."], s_limits),
 ('RECAP', ["So remember three things.", "One. Text becomes tokens.", "Two. The model predicts the next token, using patterns it learned.",
            "Three. It repeats, one token at a time.", "Not magic. Just maths, at enormous scale.", "If this helped, subscribe for more."], s_recap),
]
