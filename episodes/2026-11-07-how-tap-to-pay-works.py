"""Episode: The Hidden Coil Inside Your Bank Card (passive contactless card: inductive power at 13.56 MHz, load modulation, short range, one-time cryptogram: Wikipedia NFC and ISO/IEC 14443, ITWissen, Roland and Hoelzl arXiv 1507.06427, EMV ARQC explainers)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'The Hidden Coil Inside Your Bank Card'           # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Your card has no battery. How?'                  # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 0, 0.0), (7, 0, 0.0)]                 # the question, quiz answer, the twist
THUMB = ['NO BATTERY.', 'STILL PAYS.']                         # 4 words (vidIQ: median 5 words on breakout thumbnails)
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.2, (0, 1): 0.3, (0, 2): 0.5, (1, 2): 0.2, (2, 2): 0.3, (3, 2): 0.3, (4, 2): 2.6, (5, 2): 0.3, (6, 2): 0.3, (7, 0): 0.3, (7, 3): 0.3, (8, 1): 0.2}
SHORT_PAUSES = {(0, 0): 0.2, (3, 0): 0.2}
CAPTION_FIXES = {'thirteen and a half million': '13.5 million', 'four centimetres': '4 cm', 'ten centimetres': '10 cm'}

# Colour code kept in every scene (lesson of 2026-11-01):
# hidden coil yellow, the reader's field cyan, power green, the card's reply purple, the one-time code pink.
COIL = YE; FIELD = CY; POW = GR; REPLY = PU; CODE = PK
CBODY = (46, 64, 132); CBODY2 = (64, 86, 168); CHIP = (214, 178, 92); TERM = (34, 38, 62); TERM2 = (58, 64, 100)
DARK = (20, 22, 38); QUIZ = (24, 70, 112); SKIN = (236, 190, 150); HAIR = (60, 44, 40)
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0
# headline swaps: the old line fades out before the new one fades in, so they never overlap
sw_out = lambda T, i: 1 - fd(T(i), 0, .25) if T(i) > -.1 else 1.0
sw_in = lambda T, i: fd(T(i), .25, .35) if T(i) > -.1 else 0.0

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def perim(x0, y0, x1, y1, u):
    """Point at fraction u along a rectangle's outline (clockwise from top-left)."""
    w, h = x1 - x0, y1 - y0; L = 2 * (w + h); d = (u % 1) * L
    if d < w: return x0 + d, y0
    d -= w
    if d < h: return x1, y0 + d
    d -= h
    if d < w: return x1 - d, y1
    return x0, y1 - (d - w)

def bank_card(c, cx, cy, s, a=1.0, coil=0.0, flow=0.0, t=0.0, chip_on=0.0, xray=0.0):
    """A generic bank card (no brand). coil: hidden loops visible; flow: current dots moving round the loops."""
    w, h = 428 * s, 270 * s; x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    body = tuple(int(lerp(CBODY[i], DARK[i], xray * .6)) for i in range(3))
    c.rr(x0, y0, x1, y1, 26 * s, body, a)
    if xray < .5:
        c.rr(x0 + 30 * s, y1 - 70 * s, x0 + 250 * s, y1 - 50 * s, 6 * s, CBODY2, a * (1 - xray * 2), bg=body)
        c.rr(x0 + 30 * s, y1 - 40 * s, x0 + 150 * s, y1 - 24 * s, 6 * s, CBODY2, a * (1 - xray * 2), bg=body)
    if coil > .01:
        for k in range(4):
            ins = (14 + k * 11) * s
            c.rr(x0 + ins, y0 + ins, x1 - ins, y1 - ins, max(4, (20 - k * 3) * s), None, a * coil, outline=COIL, ow=max(2, 4 * s), bg=body)
        cxx = x0 + 96 * s
        c.line([(x0 + 14 * s, cy - 10 * s), (cxx - 34 * s, cy - 10 * s)], COIL, max(2, 4 * s), a * coil, bg=body)
    if flow > .01:
        for k in range(4):
            ins = (14 + k * 11) * s
            for j in range(5):
                px, py = perim(x0 + ins, y0 + ins, x1 - ins, y1 - ins, t * .35 + j / 5 + k * .07)
                c.circ(px, py, 7 * s, POW, a * flow, bg=body)
    chip = tuple(int(lerp(CHIP[i], POW[i], chip_on)) for i in range(3))
    c.rr(x0 + 62 * s, cy - 44 * s, x0 + 132 * s, cy + 10 * s, 10 * s, chip, a, bg=body)
    c.line([(x0 + 62 * s, cy - 17 * s), (x0 + 132 * s, cy - 17 * s)], (150, 120, 60), max(1, 3 * s), a * (1 - chip_on), bg=chip)
    c.line([(x0 + 97 * s, cy - 44 * s), (x0 + 97 * s, cy + 10 * s)], (150, 120, 60), max(1, 3 * s), a * (1 - chip_on), bg=chip)
    if chip_on > .01:
        c.circ(x0 + 97 * s, cy - 17 * s, (48 + 8 * math.sin(t * 6)) * s, None, a * chip_on * .7, outline=POW, ow=max(2, 4 * s), bg=body)

def reader(c, cx, cy, s, a=1.0, field=0.0, t=0.0, beep=0.0):
    """A generic card terminal with a coil under the pad; field = pulsing magnetic loops above it."""
    c.rr(cx - 170 * s, cy - 60 * s, cx + 170 * s, cy + 300 * s, 34 * s, TERM, a)
    c.rr(cx - 130 * s, cy - 30 * s, cx + 130 * s, cy + 80 * s, 16 * s, (30, 70, 90) if beep < .5 else (30, 110, 70), a, bg=TERM)
    if beep > .01:
        c.check(cx, cy + 25 * s, 50 * s, POW, a * beep)
    for r_ in range(3):
        for q in range(3):
            c.rr(cx - 110 * s + q * 80 * s, cy + 120 * s + r_ * 56 * s, cx - 50 * s + q * 80 * s, cy + 160 * s + r_ * 56 * s, 10 * s, TERM2, a, bg=TERM)
    if field > .01:
        for k in range(4):
            ph = (t * .9 + k / 4) % 1
            rx = (120 + ph * 260) * s; ry = (40 + ph * 120) * s
            c.d.ellipse(((cx - rx) * c.k, (cy - 90 * s - ry) * c.k, (cx + rx) * c.k, (cy - 90 * s + ry) * c.k),
                        outline=mix(FIELD, a * field * (1 - ph) * .9), width=max(1, int(5 * s * c.k)))

def face(c, x, y, s, a=1.0, mood=0.0, look=0.0):
    """An original simple cartoon shopper. mood 0 = calm smile, 1 = surprised."""
    c.rr(x - 150 * s, y + 150 * s, x + 150 * s, y + 420 * s, 90 * s, (90, 110, 190), a)
    c.circ(x, y, 150 * s, SKIN, a)
    poly(c, [(x - 150 * s, y - 10 * s), (x - 130 * s, y - 100 * s), (x - 40 * s, y - 160 * s), (x + 80 * s, y - 150 * s), (x + 150 * s, y - 50 * s), (x + 150 * s, y - 20 * s), (x + 60 * s, y - 90 * s), (x - 60 * s, y - 80 * s)], HAIR, a)
    ex = 52 * s; ey = y - 5 * s; er = (16 + 10 * mood) * s; dx = look * 8 * s
    for sx in (-1, 1):
        c.circ(x + sx * ex, ey, er + 8 * s, (250, 250, 255), a, bg=SKIN)
        c.circ(x + sx * ex + dx, ey + 2 * s, er * .7, DARK, a, bg=SKIN)
        by = ey - (44 + 22 * mood) * s
        c.line([(x + sx * ex - 26 * s, by + 6 * s * (1 - mood)), (x + sx * ex + 26 * s, by)] if sx > 0 else
               [(x + sx * ex - 26 * s, by), (x + sx * ex + 26 * s, by + 6 * s * (1 - mood))], HAIR, 9 * s, a, bg=SKIN)
    my = y + 70 * s
    if mood < .5:
        c.line([(x - 45 * s + k * 9 * s, my + 18 * s * math.sin(math.pi * k / 10)) for k in range(11)], (150, 70, 70), 9 * s, a, bg=SKIN)
    else:
        c.circ(x, my + 10 * s, (14 + 16 * mood) * s, (120, 50, 60), a, bg=SKIN)

def battery(c, x, y, s, a, col=INK):
    c.rr(x - 60 * s, y - 34 * s, x + 50 * s, y + 34 * s, 10 * s, None, a, outline=col, ow=6 * s)
    c.rr(x + 50 * s, y - 14 * s, x + 64 * s, y + 14 * s, 4 * s, col, a)

# ---- scenes ----
def s_hook(c, T, t):
    """A face in the first frame (lesson of 2026-11-07, vidIQ thumbnail study)."""
    hl = lambda i: hl_(T, i)
    q = hl(2)
    fa = 1 - q * .92
    face(c, 400, 420, 1.05, fa, mood=hl(1), look=1 - hl(1) * .5)
    tap = .5 + .5 * math.sin(min(t, 2.2) * 2.6 - 1.6) if t < 2.4 else 1.0
    reader(c, 1420, 520, 1.0, fa, field=1.0, t=t, beep=fd(t, 1.4, .3))
    bank_card(c, 1420, 300 + 80 * tap, .9, fa, t=t)
    c.text(960, 172, 'Tap. Beep. Paid.', 92, INK, sw_out(T, 1) * fa, w='Bold')
    m = sw_in(T, 1) * (1 - q)
    c.text(960, 172, 'That card has no battery', 92, CODE, m, w='Bold')
    if m > .01:
        battery(c, 1700, 250, 1.1, m, CODE); c.cross(1700, 250, 90, CODE, m)
    c.text(960, 430, 'So where does', 120, INK, q, w='Bold')
    c.text(960, 580, 'the power come from?', 120, POW, q, w='Bold')
    c.text(960, 740, 'A hidden coil of wire', 66, COIL, hl(3), w='Bold')

def s_coil(c, T, t):
    hl = lambda i: hl_(T, i)
    x = hl(0)
    bank_card(c, 680, 500, 2.0, 1, coil=x, xray=x)
    c.text(960, 172, 'Inside the plastic', 80, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A flat coil, around the edge', 80, COIL, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'Wired to the chip: the antenna', 80, COIL, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1270, 300, 1840, 640, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1555, 390, 'One study:', 56, INK, m, w='Bold', bg=CARD)
    c.text(1555, 490, 'every bank card', 60, COIL, m, w='Bold', bg=CARD)
    c.text(1555, 570, 'had 4 loops', 60, COIL, m, w='Bold', bg=CARD)
    c.text(1880, 860, 'Drawing simplified. Source: Roland and Hoelzl, 2015', 30, DIM, 1, anchor='rm', w='Regular')

def s_field(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 560, 540, 1.0, 1, field=hl(1), t=t * (1 + hl(1) * .4))
    c.text(960, 172, 'The reader has a coil too', 80, FIELD, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Current flips back and forth', 80, FIELD, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'A magnetic field, flipping just as fast', 72, FIELD, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1060, 290, 1840, 650, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1450, 390, 'About', 56, INK, m, w='Bold', bg=CARD)
    c.text(1450, 480, '13.5 million', 92, FIELD, m, w='Bold', bg=CARD)
    c.text(1450, 575, 'times a second', 56, INK, m, w='Bold', bg=CARD)
    if m > .01:
        pts = [(1120 + k * 7, 740 + 50 * math.sin(k * .5 - t * 8)) for k in range(100)]
        c.line(pts, FIELD, 6, m)
    c.text(1450, 840, '13.56 MHz', 40, DIM, m, w='Medium')

def s_power(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 560, 600, .9, 1, field=1, t=t)
    come = fd(T(0), 0, 1.4)
    flow = hl(0) * fd(T(0), 1.0)
    bank_card(c, 560, lerp(310, 410, come), .9, 1, coil=1, flow=flow, t=t, chip_on=hl(2), xray=.6)
    c.text(960, 172, 'The field pushes current round the card', 70, POW, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Two coils, no wire between them', 76, INK, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'The chip wakes up', 84, POW, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1080, 290, 1840, 660, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.rr(1300, 520, 1620, 600, 20, (70, 76, 110), m, bg=CARD)
    c.rr(1380, 400, 1540, 560, 16, (40, 44, 70), m, bg=CARD)
    for j in range(3): c.d.ellipse(((1400 + j * 18) * c.k, (535 + j * 6) * c.k, (1520 - j * 18) * c.k, (585 - j * 6) * c.k), outline=mix(COIL, m), width=int(4 * c.k))
    c.text(1460, 345, 'Same idea:', 50, INK, m, w='Bold', bg=CARD)
    c.text(1460, 625, 'wireless phone charger', 46, POW, m, w='Bold', bg=CARD)
    c.text(1460, 760, 'No battery needed', 70, POW, hl(2) * fd(T(2), 1.0), w='Bold')

def s_quiz(c, T, t):
    """Pattern interrupt: the frame fills with colour (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=QUIZ)
    c.rr(560, 110, 1360, 230, 30, DARK, 1, bg=QUIZ)
    c.text(960, 170, 'QUICK QUESTION', 78, COIL, 1, w='Bold', bg=DARK)
    c.text(960, 310, 'The chip is awake. How does it answer?', 62, INK, hl(1), w='Bold', bg=QUIZ)
    for x, lab, l1, l2, col in ((510, 'A', 'It sends out', 'its own signal', CODE), (1410, 'B', 'It changes how much', 'it takes from the field', REPLY)):
        m = hl(2) if lab == 'A' else fd(T(2), 1.6)
        c.rr(x - 420, 400, x + 420, 800, 34, DARK, m, bg=QUIZ)
        c.text(x, 500, lab, 110, col, m, w='Bold', bg=DARK)
        c.text(x, 640, l1, 56, INK, m, w='Bold', bg=DARK)
        c.text(x, 715, l2, 56, INK, m, w='Bold', bg=DARK)
    end = T(2) - 4.4
    if end > 0:
        q = clamp(end / 2.4); n = 3 - int(min(q * 3, 2.9))
        c.circ(960, 600, 96, DARK, 1, bg=QUIZ); ring(c, 960, 600, 82, 1 - q, COIL, 1, 10)
        c.text(960, 600, str(n), 86, INK, 1, w='Bold', bg=DARK)

def s_reply(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 470, 600, .9, 1, field=1, t=t)
    on = (int(t * 2.2) % 3) != 1
    sw = hl(1)
    bank_card(c, 470, 410, .9, 1, coil=1, flow=1, t=t, chip_on=1, xray=.6)
    c.text(960, 172, "B. It doesn't send its own signal", 76, REPLY, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'It switches a tiny load on and off', 76, REPLY, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'The reader feels it, like a tug on a rope', 70, REPLY, sw_in(T, 2), w='Bold')
    m = sw
    c.rr(960, 280, 1840, 660, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1400, 350, 'Power the card takes', 46, INK, m, w='Bold', bg=CARD)
    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    sh = int(t * 2.2) % len(bits)
    pts = []
    for k in range(len(bits)):
        b = bits[(k + sh) % len(bits)]; y = 470 if b else 560
        pts += [(1010 + k * 80, y), (1090 + k * 80, y)]
    c.line(pts, REPLY, 8, m, bg=CARD)
    for k in range(len(bits)):
        b = bits[(k + sh) % len(bits)]
        c.text(1050 + k * 80, 620, str(b), 40, INK if b else DIM, m * hl(2), w='Bold', bg=CARD)
    c.text(1400, 760, 'More, less, more: ones and zeros', 56, REPLY, hl(2) * fd(T(2), 1.2), w='Bold')

def s_range(c, T, t):
    hl = lambda i: hl_(T, i)
    gap = lerp(40, 360, .5 + .5 * math.sin(t * .9)) if hl(1) < .5 else 40 + 320 * hl(2)
    near = 1 - clamp((gap - 100) / 150)
    reader(c, 480, 640, .8, 1, field=1, t=t)
    bank_card(c, 480, 510 - gap * .55, .8, 1, coil=1, flow=near, t=t, chip_on=near, xray=.6)
    c.text(960, 172, 'That is why you have to get close', 76, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'It works over a few centimetres', 76, FIELD, sw_in(T, 1) * sw_out(T, 2), w='Bold')
    c.text(960, 172, 'From across the room: nothing', 76, CODE, sw_in(T, 2), w='Bold')
    m = hl(1)
    c.rr(1050, 300, 1840, 640, 28, CARD, m, outline=(60, 70, 120), ow=3)
    c.text(1445, 390, 'Phones and tags (NFC):', 48, INK, m, w='Bold', bg=CARD)
    c.text(1445, 460, 'about 4 cm or less', 56, FIELD, m, w='Bold', bg=CARD)
    c.text(1445, 545, 'Card standard:', 48, INK, m, w='Bold', bg=CARD)
    c.text(1445, 610, 'up to 10 cm', 56, FIELD, m, w='Bold', bg=CARD)
    c.text(1880, 860, 'Sources: Wikipedia NFC; ITWissen (ISO/IEC 14443)', 30, DIM, 1, anchor='rm', w='Regular')

def s_code(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'What does the card actually say?', 76, INK, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'A one-time code for every payment', 76, CODE, sw_in(T, 1), w='Bold')
    c.text(960, 270, 'Not just your card number', 64, CODE, hl(0) * fd(T(0), 2.4) * (1 - hl(1)), w='Bold')
    m = hl(1)
    items = (('Amount', '$4.50'), ('Random number', 'from the shop'), ('Counter', 'tap no. 218'))
    for k, (a_, b_) in enumerate(items):
        y = 330 + k * 150; mm = m * fd(T(1), .5 + k * .6)
        c.rr(120, y - 55, 640, y + 55, 22, CARD, mm, outline=(60, 70, 120), ow=3)
        c.text(380, y - 18, a_, 44, INK, mm, w='Bold', bg=CARD); c.text(380, y + 26, b_, 36, DIM, mm, w='Medium', bg=CARD)
        c.arrow(650, y, 820, 450, DIM, 5, mm)
    k_ = hl(2)
    bank_card(c, 1000, 450, .75, 1, coil=.5, chip_on=k_, t=t, xray=.4)
    c.text(1000, 610, 'Secret key stays in the chip', 40, COIL, k_, w='Bold')
    c.arrow(1190, 450, 1330, 450, CODE, 6, k_)
    digs = '7F3A 91C0 2E5B 64D8'
    c.rr(1340, 390, 1860, 510, 24, DARK, k_, outline=CODE, ow=4)
    c.text(1600, 450, typed(digs, fd(T(2), .8, 1.6)), 40, CODE, k_, w='Mono', bg=DARK)
    c.text(1600, 570, 'Your bank checks it', 48, INK, hl(3), w='Bold')
    c.text(960, 790, "Copy one tap, and you still can't make the next code", 56, CODE, hl(4), w='Bold')
    c.text(1880, 860, 'Simplified. Example values are illustrative', 30, DIM, 1, anchor='rm', w='Regular')

def s_more(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'The same trick, everywhere', 80, FIELD, 1, w='Bold')
    xs = (330, 760, 1190, 1620)
    labs = (('Bus and train cards', 0), ('Passports with a chip', 1), ('Bank cards', 2), ('Phones that pay', 3))
    for k, (lab, kind) in enumerate(labs):
        m = fd(T(0), .3 + k * .5) if k < 3 else hl(1)
        x = xs[k]; y = 480
        c.rr(x - 190, 260, x + 190, 700, 30, CARD, m, outline=(60, 70, 120), ow=3)
        if kind == 0:
            c.rr(x - 120, y - 80, x + 120, y + 70, 18, (40, 120, 110), m, bg=CARD)
            for j in range(3): c.rr(x - 95 + j * 18, y - 60 + j * 18, x + 95 - j * 18, y + 50 - j * 18, 10, None, m, outline=COIL, ow=3, bg=(40, 120, 110))
        elif kind == 1:
            c.rr(x - 95, y - 120, x + 95, y + 120, 14, (110, 40, 60), m, bg=CARD)
            c.circ(x, y - 20, 50, None, m, outline=CHIP, ow=5, bg=(110, 40, 60)); c.rr(x - 30, y + 60, x + 30, y + 90, 6, CHIP, m, bg=(110, 40, 60))
        elif kind == 2:
            bank_card(c, x, y, .55, m, coil=1, xray=.6, t=t)
        else:
            c.rr(x - 80, y - 140, x + 80, y + 140, 26, (60, 66, 100), m, bg=CARD)
            c.rr(x - 66, y - 120, x + 66, y + 110, 14, DARK, m, bg=(60, 66, 100))
            for j in range(3): c.rr(x - 50 + j * 12, y - 70 + j * 12, x + 50 - j * 12, y + 40 - j * 12, 8, None, m, outline=FIELD, ow=3, bg=DARK)
        c.text(x, 650, lab, 34, INK, m, w='Bold', bg=CARD)
    c.text(960, 790, 'A phone uses its own NFC chip and battery', 58, FIELD, hl(1) * fd(T(1), 1.0), w='Bold')

def s_recap(c, T, t):
    """Recap as three cards laid on the reader's pad (layout change)."""
    hl = lambda i: hl_(T, i)
    c.text(960, 172, 'Three things to keep', 80, INK, sw_in(T, 0), w='Bold')
    rows = ((1, "The reader's coil makes a fast-flipping field", FIELD),
            (2, "The card's coil turns it into power, and answers by changing its load", POW),
            (3, 'Each tap sends a one-time code, not just your number', CODE))
    for ln, txt, col in rows:
        m = hl(ln); y = 250 + (ln - 1) * 160
        c.rr(170 + 40 * (1 - m), y, 1750, y + 128, 26, CARD, m, outline=col, ow=4)
        c.circ(250, y + 64, 40, col, m, bg=CARD); c.text(250, y + 64, str(ln), 46, DARK, m, w='Bold', bg=col)
        ls = wrap(c, txt, 44, 1340, 'Bold')
        for j, l in enumerate(ls):
            c.text(320, y + 64 + (j - (len(ls) - 1) / 2) * 52, l, 44, INK, m, anchor='lm', w='Bold', bg=CARD)
    c.text(960, 790, 'Short Story Long Thinking', 58, CY, hl(4), w='Bold')

def thumb_art(c):
    face(c, 1680, 380, .95, 1, mood=1, look=-1)
    reader(c, 1350, 640, .8, 1, field=1, t=.3, beep=1)
    bank_card(c, 1350, 430, .85, 1, coil=1, flow=1, t=.2, chip_on=1, xray=.6)

SCENES = [
 ('THE HOOK', ["You tap your card. Beep. Paid.",
               "But that card has no battery inside.",
               "So where does the power come from?",
               "The answer is a hidden coil of wire."], s_hook),
 ('THE COIL', ["Inside the plastic, there's a flat coil of wire.",
               "It runs in loops around the edge of the card. In one study, every bank card checked had four loops.",
               "The coil connects to the chip. It's the card's antenna."], s_coil),
 ('THE FIELD', ["The card reader has a coil too.",
                "It pushes electric current back and forth through it, about thirteen and a half million times a second.",
                "That makes a magnetic field above the reader, flipping just as fast."], s_field),
 ('THE POWER', ["Bring your card close, and that flipping field pushes current around the card's coil.",
                "It's the same idea as a wireless phone charger. Two coils, no wire between them.",
                "That small current wakes up the chip. No battery needed."], s_power),
 ('QUICK QUESTION', ["Quick question.",
                     "The chip is awake. How does it answer the reader?",
                     "A, it sends out its own radio signal. Or B, it changes how much power it takes from the field."], s_quiz),
 ('THE REPLY', ["B. The card doesn't send its own signal.",
                "It switches a tiny load on and off, so it takes a little more power, then a little less.",
                "The reader feels those changes, like a tug on a rope. More, less, more. Ones and zeros."], s_reply),
 ('THE RANGE', ["That's also why you have to get close.",
                "The field is only strong enough over a few centimetres. Phones and tags work at about four centimetres or less. Cards, up to about ten centimetres.",
                "Wave your card from across the room, and nothing happens."], s_range),
 ('THE TWIST', ["Here's the twist. What does the card actually say? Not just your card number.",
                "For every payment, the chip makes a one-time code. It mixes the amount, a random number from the shop's terminal, and a counter.",
                "It uses a secret key that never leaves the chip.",
                "Your bank checks the code.",
                "So copying what a card said on one tap doesn't let someone make the next code."], s_code),
 ('EVERYWHERE', ["The same idea runs bus and train cards, passports with a chip, and bank cards.",
                 "A phone can pay the same way, but it uses its own NFC chip and its own battery."], s_more),
 ('RECAP', ["Three things to keep.",
            "One: the reader's coil makes a fast-flipping magnetic field.",
            "Two: the card's coil turns that field into power, and answers by changing its load.",
            "Three: each tap sends a one-time code, not just your number.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    face(c, 420, 430, 1.0, 1, mood=fd(T(0), 1.2), look=.5)
    reader(c, 1420, 580, .95, 1, field=1, t=t, beep=fd(t, 1.0, .3))
    bank_card(c, 1420, 385, .85, 1, t=t)
    c.text(960, 172, 'No battery inside', 88, CODE, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'The power comes from the reader', 80, POW, sw_in(T, 1), w='Bold')

def short_field(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 560, 540, 1.0, 1, field=1, t=t * 1.4)
    c.text(960, 172, 'A magnetic field, flipping fast', 80, FIELD, 1, w='Bold')
    c.rr(1060, 290, 1840, 650, 28, CARD, 1, outline=(60, 70, 120), ow=3)
    c.text(1450, 390, 'About', 56, INK, 1, w='Bold', bg=CARD)
    c.text(1450, 480, '13.5 million', 92, FIELD, 1, w='Bold', bg=CARD)
    c.text(1450, 575, 'times a second', 56, INK, 1, w='Bold', bg=CARD)

def short_power(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 560, 600, .9, 1, field=1, t=t)
    bank_card(c, 560, lerp(310, 410, fd(T(0), 0, 1.4)), .9, 1, coil=1, flow=hl(1), t=t, chip_on=hl(1) * fd(T(1), 1.0), xray=.6)
    c.text(960, 172, 'A hidden coil around the edge', 80, COIL, sw_out(T, 1), w='Bold')
    c.text(960, 172, 'Current flows. The chip wakes up', 80, POW, sw_in(T, 1), w='Bold')

def short_reply(c, T, t):
    hl = lambda i: hl_(T, i)
    reader(c, 470, 600, .9, 1, field=1, t=t)
    bank_card(c, 470, 410, .9, 1, coil=1, flow=1, t=t, chip_on=1, xray=.6)
    c.text(960, 172, 'It answers by switching a load', 80, REPLY, 1, w='Bold')
    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]; sh = int(t * 2.2) % len(bits); pts = []
    c.rr(960, 280, 1840, 660, 28, CARD, 1, outline=(60, 70, 120), ow=3)
    for k in range(len(bits)):
        y = 430 if bits[(k + sh) % len(bits)] else 540
        pts += [(1010 + k * 80, y), (1090 + k * 80, y)]
    c.line(pts, REPLY, 8, 1, bg=CARD)
    c.text(1400, 610, 'More, less: ones and zeros', 46, INK, hl(0) * fd(T(0), 1.0), w='Bold', bg=CARD)

SHORT_SCENES = [
 ('THE HOOK', ["Your bank card has no battery. So how does tapping it pay?",
               "The power comes from the card reader."], short_open),
 ('THE FIELD', ["The reader's coil makes a magnetic field that flips about thirteen and a half million times a second."], short_field),
 ('THE COIL', ["Your card hides a flat coil of wire around its edge.",
               "Near the reader, that field pushes current through the coil, like a wireless phone charger, and the chip wakes up."], short_power),
 ('THE REPLY', ["The chip answers by switching a tiny load on and off. The reader feels those changes as ones and zeros."], short_reply),
 ('THE ANSWER', ["So the reader powers your card.",
                 "And your card answers without a battery of its own. It just needs to get close."], card('The reader powers the card.', 'No battery needed.')),
]
SHORT_HITS = [(4, 1, 0.0)]
