"""Episode: Same Price. Smaller Packet. (shrinkflation: BLS unit-price example, Gourville & Koehler 2004, GAO 2025, ONS, Evangelidis 2024, the unit price fix)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'Same Price. Smaller Packet.'                    # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                              # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = 'Same price. Why a smaller packet?'               # headline on the vertical Short
HITS = [(0, 3, 0.0), (3, 0, 0.0), (5, 0, 0.0), (7, 3, 0.0)]    # title card, quiz answer, the twist, the fix
THUMB = ['SAME PRICE.', 'LESS INSIDE.']
MUSIC_LEVEL = 0.006                                            # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                                 # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 0): 0.2, (0, 1): 0.4, (1, 3): 0.2, (2, 3): 1.2, (3, 0): 0.3, (4, 3): 0.3, (5, 0): 0.3, (5, 2): 0.2, (6, 2): 0.3, (7, 3): 0.3}
SHORT_PAUSES = {(0, 0): 0.2, (3, 1): 0.2}
CAPTION_FIXES = {'five ninety-nine': '$5.99', 'two ninety-nine': '$2.99', 'three thirty-three': '$3.33',
                 'six point seven percent': '6.7%', 'Sixty-four': '64', 'sixty-four': '64', 'sixty ounces': '60 ounces',
                 'ten to twenty percent': '10 to 20%', 'zero point zero six': '0.06', 'thirty-four and a half percent': '34.5%',
                 'forty-four percent': '44%', 'thirty-one percent': '31%', 'two hundred and six': '206', 'seventy-nine': '79',
                 'hundred grams': '100 grams'}

# Colour code kept in every scene (lesson of 2026-11-01):
# the price you see yellow, the size blue, the hidden rise pink, the fix green.
PRICE = YE; SIZE = CY; HIDDEN = PK; FIX = GR
PAPER = (232, 218, 172); DARK = (20, 22, 38)

hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def lerp(p, q, u): return p + (q - p) * u

def poly(c, pts, fill, a=1.0, bg=BG):
    if a <= .01 or len(pts) < 3: return
    c.d.polygon([(x * c.k, y * c.k) for x, y in pts], fill=mix(fill, a, bg))

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def tub(c, cx, by, h, a, w=300, col=SIZE, bg=BG, word='ICE CREAM'):
    """A tub of ice cream standing on y = by, h tall."""
    if a <= .01: return
    top = by - h
    poly(c, [(cx - w / 2, top), (cx + w / 2, top), (cx + w * .4, by), (cx - w * .4, by)], col, a, bg)
    c.rr(cx - w * .55, top - 36, cx + w * .55, top + 8, 12, mix(col, .72, DARK), a, bg=bg)
    ym = top + h * .5
    c.rr(cx - w * .36, ym - 46, cx + w * .36, ym + 46, 12, DARK, a, bg=col)
    c.text(cx, ym, word, int(w * .118), INK, a, w='Bold', bg=DARK)

def tag(c, x, y, txt, a, size=64, col=PRICE, bg=BG):
    """Swing tag with the price on it."""
    if a <= .01: return
    tw = c.tw(txt, size, 'Bold')
    c.rr(x - tw / 2 - 58, y - size * .82, x + tw / 2 + 36, y + size * .82, 18, DARK, a, outline=col, ow=7, bg=bg)
    c.circ(x - tw / 2 - 30, y, 10, col, a, bg=DARK)
    c.text(x + 10, y, txt, size, col, a, w='Bold', bg=DARK)

def ghost(c, cx, by, h, a, w=300, col=HIDDEN):
    """Dashed outline of the old height."""
    if a <= .01: return
    top = by - h; n = 12
    for i in range(n):
        if i % 2 == 0:
            c.line([(cx - w / 2 + w * i / n, top), (cx - w / 2 + w * (i + 1) / n, top)], col, 6, a)

def jar(c, x, by, h, a, w=120, col=SIZE, bg=CARD):
    c.rr(x - w / 2, by - h, x + w / 2, by, 14, col, a, bg=bg)
    c.rr(x - w * .58, by - h - 20, x + w * .58, by - h + 6, 8, mix(col, .7, DARK), a, bg=bg)

# ---- scenes ----
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    u = 1 - hl(3)
    c.text(960, 170, "The price tag didn't change", 72, PRICE, u * (1 - hl(1)), w='Bold')
    c.text(960, 170, 'You still paid more', 76, HIDDEN, u * hl(1), w='Bold')
    H = 440; h2 = lerp(H, 356, fd(t, .1, 2.0)); by = 800
    c.text(520, 280, 'LAST TIME', 40, DIM, u, w='Bold'); c.text(1400, 280, 'TODAY', 40, DIM, u, w='Bold')
    tub(c, 520, by, H, u); tub(c, 1400, by, h2, u)
    ghost(c, 1400, by, H, u * fd(t, .6))
    tag(c, 830, 430, '$5.99', u); tag(c, 1710, 430, '$5.99', u)
    c.text(830, 560, '64 oz', 56, SIZE, u, w='Bold'); c.text(1710, 560, '60 oz', 56, SIZE, u * fd(t, 1.2), w='Bold')
    c.text(1880, 860, 'Drawing exaggerated', 30, DIM, u, anchor='rm', w='Regular')
    a = hl(3)
    c.text(960, 370, 'Same price.', 138, PRICE, a, w='Bold'); c.text(960, 560, 'Smaller packet.', 138, SIZE, a, w='Bold')
    c.rr(760, 680, 1160, 692, 6, HIDDEN, a)

def s_sum(c, T, t):
    hl = lambda i: hl_(T, i)
    H = 400; by = 790
    h = lerp(H, 330, fd(T(1), .3, 1.2) if T(1) > 0 else 0)
    c.text(960, 170, 'The sum on the back of the packet', 62, INK, 1 - hl(3), w='Bold')
    c.text(960, 170, 'Shrinkflation', 92, HIDDEN, hl(3), w='Bold')
    tub(c, 380, by, h, 1, w=300); ghost(c, 380, by, H, hl(1))
    tag(c, 380, 300 if hl(1) == 0 else 300, '$5.99', 1, 56)
    x = 780
    a0 = fd(T(0), .4); a1 = hl(1)
    c.rr(x - 30, 290, 1830, 430, 22, CARD, a0, outline=(60, 70, 120), ow=3)
    c.text(x + 10, 360, '$5.99 / 64 oz', 58, SIZE, a0, anchor='lm', w='Bold', bg=CARD); c.text(1800, 360, '9.4¢ an ounce', 58, PRICE, hl(2), anchor='rm', w='Bold', bg=CARD)
    c.rr(x - 30, 460, 1830, 600, 22, CARD, a1, outline=(60, 70, 120), ow=3)
    c.text(x + 10, 530, '$5.99 / 60 oz', 58, SIZE, a1, anchor='lm', w='Bold', bg=CARD); c.text(1800, 530, '10.0¢ an ounce', 58, PRICE, hl(2), anchor='rm', w='Bold', bg=CARD)
    c.text(1300, 700, '6.7% more per ounce', 80, HIDDEN, hl(2), w='Bold')
    c.text(1880, 860, 'Example: US Bureau of Labor Statistics', 30, DIM, 1, anchor='rm', w='Regular')

def s_test(c, T, t):
    """Pattern interrupt: the whole frame turns into a bright paper tag (lesson of 2026-11-05)."""
    hl = lambda i: hl_(T, i)
    c.d.rectangle((0, 0, 1920 * c.k, 890 * c.k), fill=PAPER)
    c.d.rectangle((0, 890 * c.k, 1920 * c.k, 900 * c.k), fill=DARK)
    c.rr(560, 130, 1360, 260, 30, DARK, 1, bg=PAPER)
    c.text(960, 195, 'QUICK TEST', 96, PRICE, 1, w='Bold', bg=DARK)
    for x, lab, top, sub, m in ((510, 'A', '$2.99  to  $3.33', 'same size tin', hl(1)), (1410, 'B', '$2.99  stays', 'tin loses 1.5 oz', hl(2))):
        c.rr(x - 410, 310, x + 410, 800, 34, DARK, m, bg=PAPER)
        c.text(x, 400, lab, 92, PRICE if lab == 'A' else SIZE, m, w='Bold', bg=DARK)
        c.text(x, 545, top, 62, PRICE, m, w='Bold', bg=DARK)
        c.text(x, 650, sub, 52, SIZE, m, w='Bold', bg=DARK)
    if T(3) > 0:
        n = 3 - int(clamp(T(3) - 3.0, 0, 2.9)); p = clamp((T(3) - 3.0) / 3.0)
        c.circ(960, 555, 96, DARK, 1, bg=PAPER); ring(c, 960, 555, 82, 1 - p, PRICE, 1, 10)
        c.text(960, 555, str(n), 86, INK, 1, w='Bold', bg=DARK)

def s_evidence(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'Most people catch A', 80, PRICE, 1, w='Bold')
    m = hl(1)
    for y, lab, col, v in ((350, 'Price change', PRICE, .92), (480, 'Quiet size cut', SIZE, .07)):
        c.text(180, y, lab, 50, col, fd(T(0), .3), anchor='lm', w='Bold')
        c.rr(620, y - 34, 1700, y + 34, 20, (34, 40, 78), fd(T(0), .3))
        if m > .01: c.rr(620, y - 34, 620 + max(40, 1080 * v * m), y + 34, 20, col, 1)
    c.text(1700, 545, 'Illustrative bars: how much sales reacted', 30, DIM, 1, anchor='rm', w='Regular')
    c.text(960, 640, '10 to 20% smaller over 3 years', 64, SIZE, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 730, 'Little to no complaint', 58, INK, hl(2) * (1 - hl(3)), w='Bold')
    c.text(960, 665, '2 to 5 times', 118, PRICE, hl(3), w='Bold')
    c.text(960, 775, 'more responsive to the price rise', 54, INK, hl(3), w='Bold')
    c.text(1880, 860, 'Gourville and Koehler 2004; US GAO 2025', 30, DIM, 1, anchor='rm', w='Regular')

def s_why(c, T, t):
    hl = lambda i: hl_(T, i)
    m0 = fd(T(0), .1); m1 = hl(1)
    c.text(960, 170, 'Two numbers. One is much easier', 70, INK, 1 - hl(3), w='Bold')
    c.text(960, 170, 'Change the number you see, or the one you do not?', 58, HIDDEN, hl(3), w='Bold')
    c.rr(120, 270, 900, 820, 30, CARD, m0, outline=PRICE, ow=5)
    c.text(510, 340, 'PRICE', 56, PRICE, m0, w='Bold', bg=CARD)
    tag(c, 510, 510, '$2.99', m0, 110, bg=CARD)
    c.text(510, 720, 'One number, right there', 46, INK, m0, w='Bold', bg=CARD)
    c.rr(1020, 270, 1800, 820, 30, CARD, m1, outline=SIZE, ow=5)
    c.text(1410, 340, 'SIZE', 56, SIZE, m1, w='Bold', bg=CARD)
    c.text(1410, 460, 'Last weight?', 66, SIZE, hl(1), w='Bold', bg=CARD)
    c.text(1410, 570, '? oz  vs  13 oz', 66, DIM, fd(T(1), 1.0), w='Bold', bg=CARD)
    c.text(1410, 680, '$2.99 / 13 = ?', 62, INK, hl(2), w='Bold', bg=CARD)
    c.text(1410, 760, 'Sums in the aisle', 46, HIDDEN, hl(2), w='Bold', bg=CARD)

def s_twist(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - hl(3)
    c.text(960, 170, "The official inflation figure isn't fooled", 66, FIX, a * (1 - hl(2)), w='Bold')
    c.text(960, 170, "And it's rarer than it feels", 76, PRICE, hl(2), w='Bold')
    b = hl(1) * (1 - hl(2))
    tub(c, 420, 780, lerp(400, 330, fd(T(1), .3)), 1 - hl(2), w=300)
    c.rr(800, 320, 1820, 720, 28, CARD, b, outline=FIX, ow=4)
    c.text(1310, 410, 'US and UK statisticians', 52, INK, b, w='Bold', bg=CARD)
    c.text(1310, 520, 'track price per unit', 64, FIX, b, w='Bold', bg=CARD)
    c.text(1310, 630, 'Smaller tub = price rise', 54, HIDDEN, b, w='Bold', bg=CARD)
    if T(2) > -.1:
        m = hl(2) * (1 - hl(4))
        W_ = 1500; x0 = 210
        c.text(x0, 340, 'US prices, 2019 to 2024', 48, INK, m, anchor='lm', w='Bold')
        if T(3) > 0: c.rr(x0, 390, x0 + max(8, W_ * fd(T(3), .2, 1.6)), 480, 12, PRICE, m)
        c.text(x0, 530, '+34.5%', 62, PRICE, m * fd(T(3), 1.0), anchor='lm', w='Bold')
        c.text(x0, 640, 'Added by smaller packs', 48, INK, m, anchor='lm', w='Bold')
        c.rr(x0, 690, x0 + 3, 780, 1, HIDDEN, m * fd(T(3), 6.0))
        c.text(x0 + 40, 735, '0.06 of a point', 62, HIDDEN, m * fd(T(3), 6.0), anchor='lm', w='Bold')
        c.text(1880, 860, 'Bars to scale. Source: US GAO 2025', 30, DIM, m, anchor='rm', w='Regular')
    if T(4) > -.1:
        m = hl(4)
        c.text(520, 290, '206 shrank', 66, HIDDEN, m, w='Bold'); c.text(1420, 290, '79 grew', 66, SIZE, m, w='Bold')
        for k in range(int(206 * clamp(T(4) / 2.0))):
            c.circ(200 + k % 24 * 28, 370 + k // 24 * 28, 10, HIDDEN, m)
        for k in range(int(79 * clamp(T(4) / 2.0))):
            c.circ(1100 + k % 24 * 28, 370 + k // 24 * 28, 10, SIZE, m)
        c.text(1880, 860, 'UK ONS price data, 2015 to 2017', 30, DIM, m, anchor='rm', w='Regular')

def s_back(c, T, t):
    hl = lambda i: hl_(T, i)
    u = 1 - hl(3)
    c.text(960, 170, 'People who notice call it unfair', 68, HIDDEN, u, w='Bold')
    for j, (lab, v, col) in enumerate((('Smaller pack', 44, HIDDEN), ('Equal price rise', 31, PRICE))):
        y = 360 + j * 170; m = fd(T(1), .1) if j == 0 else fd(T(1), 2.2)
        c.text(160, y, lab, 50, INK, m * u, anchor='lm', w='Bold')
        c.rr(640, y - 44, 640 + 1040 * v / 50 * ease(clamp((T(1) - (0 if j == 0 else 2.2)) / .9)), y + 44, 18, col, m * u)
        c.text(640 + 1040 * v / 50 + 30, y, f'{v}%', 60, col, m * u, anchor='lm', w='Bold')
    c.text(960, 690, 'It feels sneaky', 86, HIDDEN, hl(2) * u, w='Bold')
    c.text(1880, 860, 'Called it unfair, chocolate test. Evangelidis, Marketing Science, 2024', 30, DIM, u, anchor='rm', w='Regular')
    a = hl(3)
    c.text(960, 170, 'See-through packaging', 76, SIZE, a, w='Bold')
    c.rr(760, 290, 1160, 790, 30, None, a, outline=SIZE, ow=8)
    for k in range(int(4 * a) * 3):
        c.circ(860 + k % 3 * 100, 720 - k // 3 * 100, 42, PRICE, a)
    c.text(1480, 480, 'Unfair gap', 56, INK, a, w='Bold'); c.text(1480, 570, 'almost gone', 56, FIX, a, w='Bold')
    c.text(1480, 680, '37% vs 35%', 58, PRICE, a, w='Bold')

def s_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'The small line on the shelf tag', 70, FIX, 1 - hl(3), w='Bold')
    c.text(960, 170, 'Read the small number, not the big one', 66, FIX, hl(3), w='Bold')
    for x, big, size_, unit, best in ((510, '$4.00', '250 g', '$1.60 per 100 g', True), (1410, '$3.50', '200 g', '$1.75 per 100 g', False)):
        m = hl(1) if best else fd(T(1), 1.2)
        c.rr(x - 400, 290, x + 400, 790, 26, CARD, m, outline=(60, 70, 120), ow=3)
        c.text(x, 400, big, 120, PRICE, m * (1 - .55 * hl(2)), w='Bold', bg=CARD)
        c.text(x, 530, size_, 60, SIZE, m, w='Bold', bg=CARD)
        hi = hl(2)
        if hi > 0 and best: c.rr(x - 345, 590, x + 345, 690, 16, mix(FIX, .28, CARD), hi, outline=FIX, ow=5, bg=CARD)
        c.text(x, 640, unit, 52, FIX if best else INK, m, w='Bold', bg=mix(FIX, .28, CARD) if (best and hi > .5) else CARD)
        if hi > 0 and best: c.text(x, 745, 'Cheaper', 50, FIX, hi, w='Bold', bg=CARD)
    c.text(1880, 860, 'Illustrative prices', 30, DIM, 1, anchor='rm', w='Regular')

def s_recap(c, T, t):
    """Recap printed as a till receipt (layout change)."""
    hl = lambda i: hl_(T, i)
    p = fd(t, 0, 1.2)
    x0, x1 = 370, 1550; top = 130; bot = lerp(top + 90, 850, p)
    c.rr(x0, top, x1, bot, 8, CARD, 1, outline=(110, 120, 170), ow=3)
    k = 0
    while x0 + k * 30 < x1:                         # torn edge
        c.line([(x0 + k * 30, bot), (x0 + k * 30 + 15, bot + 16), (x0 + k * 30 + 30, bot)], (110, 120, 170), 4, 1); k += 1
    c.text(960, 195, 'THREE THINGS TO KEEP', 54, PRICE, p, w='Bold', bg=CARD)
    c.line([(420, 245), (1500, 245)], DIM, 3, p, CARD)
    rows = ((1, 'Same price, smaller pack:', 'a price rise', HIDDEN), (2, 'We react far less', 'to size than to price', SIZE), (3, 'Check the unit price,', 'not the tag', FIX))
    for j, (ln, a_, b_, col) in enumerate(rows):
        y = 320 + j * 150; m = hl(ln)
        c.text(430, y, f'{j + 1}', 62, DIM, m, anchor='lm', w='Bold', bg=CARD)
        c.text(510, y - 30, a_, 48, INK, m, anchor='lm', w='Bold', bg=CARD)
        c.text(510, y + 34, b_, 48, col, m, anchor='lm', w='Bold', bg=CARD)
    m = hl(4)
    c.line([(420, 748), (1500, 748)], DIM, 3, m, CARD)
    c.text(960, 800, 'Short Story Long Thinking', 48, CY, m, w='Bold', bg=CARD)

def thumb_art(c):
    tub(c, 1500, 900, 560, 1, w=500); ghost(c, 1500, 900, 760, 1, w=500)
    c.text(1500, 245, 'GONE', 64, HIDDEN, 1, w='Bold')
    tag(c, 1500, 780, '$5.99', 1, 96, bg=SIZE)

SCENES = [
 ('THE HOOK', ["The price tag didn't change.",
               "You still paid more.",
               "One sum shows it, one test explains it, and one small label beats it.",
               "Same price. Smaller packet."], s_hook),
 ('THE SUM', ["Take a tub of ice cream. Sixty-four ounces, five ninety-nine.",
              "Next time, the tub holds sixty ounces. Still five ninety-nine.",
              "Divide the price by the ounces. Each ounce now costs six point seven percent more.",
              "So that's a price rise. It just isn't on the tag. It's called shrinkflation."], s_sum),
 ('QUICK TEST', ["Quick test. Your coffee can change in one of two ways.",
                 "A: the price jumps from two ninety-nine to three thirty-three.",
                 "B: the price stays, and the tin loses an ounce and a half.",
                 "Each ounce costs about the same extra either way. Which would you spot?"], s_test),
 ('THE RESULT', ["Most people catch A.",
                 "In 2004, Harvard's John Gourville and a colleague tracked snack buyers. They reacted strongly to price changes. To quiet size cuts, they barely reacted.",
                 "One maker cut packs by ten to twenty percent over three years, with little to no complaint.",
                 "A 2025 US government review found shoppers about two to five times more responsive to a price rise."], s_evidence),
 ('WHY WE MISS IT', ["Why the gap? Price is one number, right there on the tag.",
                     "To catch a smaller pack, you need to remember the old weight.",
                     "Then do division in the aisle. Most of us won't.",
                     "So when costs rise, a company can change the number you see, or the one you don't."], s_why),
 ('THE TWIST', ["Here's the twist. The official inflation figure isn't fooled.",
                "Statisticians in the US and UK track price per unit, so that smaller tub counts as a price rise.",
                "And it's rarer than it feels.",
                "US prices rose thirty-four and a half percent from 2019 to 2024. Smaller packs added just zero point zero six of a point.",
                "In UK price data, two hundred and six products shrank, and seventy-nine grew."], s_twist),
 ('THE BACKFIRE', ["The trick has a cost, too. When people do notice, it feels worse.",
                   "In one 2024 study, forty-four percent called a smaller chocolate pack unfair. For an equal price rise, thirty-one percent did.",
                   "Why? It feels sneaky.",
                   "With see-through packaging, nothing is hidden, and that gap nearly vanished."], s_back),
 ('THE FIX', ["So here's the label that beats it.",
              "Many shelf tags carry a small line: the unit price. Price per hundred grams, or per ounce.",
              "Two packets, two sizes, two prices. The unit price shows which is really cheaper.",
              "Ignore the big number. Read the small one."], s_fix),
 ('RECAP', ["Three things to keep.",
            "One: a smaller pack at the same price is a price rise.",
            "Two: we react far less to size than to price.",
            "Three: check the unit price, not the tag.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---- the Short: its own complete mini-story with the answer up front ----
def short_open(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'Same price. Why a smaller packet?', 66, PRICE, 1 - hl(1), w='Bold')
    c.text(960, 170, 'Shoppers notice price far more than size', 62, HIDDEN, hl(1), w='Bold')
    H = 440; h2 = lerp(H, 356, fd(t, .1, 2.0)); by = 800
    tub(c, 520, by, H, 1); tub(c, 1400, by, h2, 1); ghost(c, 1400, by, H, fd(t, .6))
    tag(c, 830, 430, '$5.99', 1); tag(c, 1710, 430, '$5.99', 1)
    c.text(830, 560, '64 oz', 56, SIZE, 1, w='Bold'); c.text(1710, 560, '60 oz', 56, SIZE, fd(t, 1.2), w='Bold')

def short_sum(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'It is still a price rise', 76, HIDDEN, 1, w='Bold')
    x = 200
    c.rr(x, 290, 1720, 430, 22, CARD, fd(T(0), .1), outline=(60, 70, 120), ow=3)
    c.text(x + 40, 360, '$5.99 / 64 oz', 62, SIZE, fd(T(0), .1), anchor='lm', w='Bold', bg=CARD); c.text(1690, 360, '9.4¢ an ounce', 62, PRICE, fd(T(1), .1), anchor='rm', w='Bold', bg=CARD)
    c.rr(x, 460, 1720, 600, 22, CARD, fd(T(0), 1.0), outline=(60, 70, 120), ow=3)
    c.text(x + 40, 530, '$5.99 / 60 oz', 62, SIZE, fd(T(0), 1.0), anchor='lm', w='Bold', bg=CARD); c.text(1690, 530, '10.0¢ an ounce', 62, PRICE, fd(T(1), .1), anchor='rm', w='Bold', bg=CARD)
    c.text(960, 720, '6.7% more per ounce', 92, HIDDEN, fd(T(1), .8), w='Bold')

def short_proof(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'The evidence', 80, PRICE, 1, w='Bold')
    c.text(960, 430, '2 to 5 times', 150, PRICE, fd(T(0), .3), w='Bold')
    c.text(960, 570, 'more responsive to a price rise', 66, INK, fd(T(0), .8), w='Bold')
    c.text(960, 700, 'than to the same size cut', 66, SIZE, fd(T(0), 1.4), w='Bold')
    c.text(1880, 860, 'US GAO review, 2025', 30, DIM, 1, anchor='rm', w='Regular')

def short_fix(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 170, 'The small line on the shelf tag', 70, FIX, 1, w='Bold')
    for x, big, size_, unit, best in ((510, '$4.00', '250 g', '$1.60 per 100 g', True), (1410, '$3.50', '200 g', '$1.75 per 100 g', False)):
        c.rr(x - 400, 290, x + 400, 790, 26, CARD, 1, outline=(60, 70, 120), ow=3)
        c.text(x, 400, big, 120, PRICE, 1, w='Bold', bg=CARD)
        c.text(x, 530, size_, 60, SIZE, 1, w='Bold', bg=CARD)
        c.text(x, 640, unit, 52, FIX if best else INK, 1, w='Bold', bg=CARD)
        if best: c.text(x, 745, 'Cheaper', 50, FIX, hl(1), w='Bold', bg=CARD)
    c.text(1880, 860, 'Illustrative prices', 30, DIM, 1, anchor='rm', w='Regular')

SHORT_SCENES = [
 ('THE HOOK', ["Why does a packet get smaller, but not cheaper?",
               "Because shoppers notice price far more than size."], short_open),
 ('THE SUM', ["A tub of ice cream goes from sixty-four ounces to sixty. Still five ninety-nine.",
              "That's six point seven percent more for each ounce. A price rise, with no new tag."], short_sum),
 ('THE EVIDENCE', ["Studies find shoppers are about two to five times more responsive to a price rise than to the same size cut."], short_proof),
 ('THE NAME', ["So when costs rise, shrinking the pack is the change fewer people see.",
               "That's shrinkflation."], card('Costs rise. The pack shrinks.', 'Fewer people see it.')),
 ('THE FIX', ["To beat it, check the unit price: the small line on the shelf tag, like price per hundred grams.",
              "Read the small number, not the big one."], short_fix),
]
SHORT_HITS = [(3, 1, 0.0)]
