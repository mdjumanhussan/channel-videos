"""Story 17: Musa (Moses) and the fire by the mountain. Sources: Quran 20:9-36, 28:29-35 (Saheeh International); 27:7-12 read too.
No people are drawn: no Musa, no family, no Pharaoh, no figure of any kind, and nothing stands for Allah. Only a valley, a
mountain, a far fire, a tent, a worn track in the sand, a tree, a pair of sandals on the ground, a snake, Pharaoh's halls
(building only), the sky and morning light.
Facts used and where they are: Musa was travelling with his family and saw a fire from the direction of the mount (28:29, 20:10);
he hoped to bring burning wood to warm them (28:29, 27:7); when he came to it he was called from the tree: "O Moses, indeed
I am Allah, Lord of the worlds" (28:30); remove your sandals, you are in the sacred valley of Tuwa (20:12); throw down your
staff (28:31, 20:19); it writhed as if it was a snake and he turned in flight (28:31, 27:10); "O Moses, approach and fear not"
(28:31); "Go to Pharaoh. Indeed, he has transgressed" (20:24); "I fear they will kill me" (28:33); his prayer (20:25-28); he
asked for his brother Harun (20:29-32, 28:34); "You have been granted your request, O Moses" (20:36).
Not used: "burning bush" or a tree that burns and is not consumed (the Quran says only that he was called from the tree; the
tree here is not on fire), the name Sinai, night as a stated fact (the sky is scenery; the narration does not say it), that he
had lost his way, his wife's name, how many years had passed, the white hand (20:22, left out for length and it could not be
drawn anyway), the nine signs. The fire is scenery only and never shown as Allah. "Moses" is kept in spoken quotes because
the rule is exact Saheeh International wording; the narration says Musa.
Improvement tried today: the payoff is a dua the viewer can keep. The peak is Musa's own prayer, card by card in the Arabic
(20:25, 20:26), the answer (20:36) gets the deep hit, and the lesson hands the viewer the same words. Reason: the page's best
hold in this series is Ayyub (16 s), the first with a lesson built from the prophet's own prayer, and The Sunnah Guy's advice
is to end on a payoff because "People share content that represents their identity." Sky goes from dark to sunrise across the
prayer and the answer. Also kept: plain headline = spoken hook with nothing else on frame 1 (caption hidden), live fire from
frame 1, second loop ("What would he say?") with a 0.5 s pause, rhyming loop ending (same valley and track as frame 1 in
morning light, fire gone), speed 1.1, lesson card, specific send-to end card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  17'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Musa and the Fire by the Mountain'
HITS = [(2, 1, 0.0), (8, 1, 0.0)]

# ---------------------------------------------------------------- small scenery helpers for this story
FAR_FIRE = dict(cx=640, base=1178, w=70, h=120, n=6)

def path(p, x0, y0, x1, y1, col, a=70, bend=120):
    """A faint worn track winding across the sand toward the mountain: wide near the viewer, a thread far away. No walker is drawn."""
    L, R = [], []
    for i in range(41):
        f = i / 40; e = f ** .62; x = lerp(x0, x1, e) + math.sin(f * 3.1) * bend; y = lerp(y0, y1, e); w = lerp(70, 3, f ** .5)
        L.append((x - w, y)); R.append((x + w, y))
    p.poly(L + R[::-1], col, a)

def tent(p, cx, base, s, col, flap):
    p.poly([(cx - 150 * s, base), (cx, base - 150 * s), (cx + 150 * s, base)], col)
    p.poly([(cx - 34 * s, base), (cx, base - 150 * s), (cx + 34 * s, base)], flap)
    p.line([(cx - 260 * s, base + 6 * s), (cx, base - 158 * s), (cx + 260 * s, base + 6 * s)], col, 3 * s, 170)

def sandals(p, cx, cy, s=1.0, leather=(134, 88, 50), strap=(84, 52, 30)):
    """A pair of simple leather sandals resting on the ground, seen from above at a slant. Objects only."""
    for sx, tilt in ((-1, -.1), (1, .09)):
        x = cx + sx * 118 * s
        def R(dx, dy): return (x + dx * s + tilt * dy * s, cy + dy * s * .62)
        out = [R(-54, 170), R(-74, 60), R(-68, -60), R(-40, -140), R(0, -168), R(44, -146), R(68, -60), R(66, 60), R(52, 170), R(0, 190)]
        p.poly([(a + 10 * s, b + 14 * s) for a, b in out], (0, 0, 0), 90)                 # shadow on the sand
        p.poly(out, leather)
        p.poly([R(-42, 145), R(-58, 55), R(-50, -55), R(-28, -120), R(0, -142), R(32, -124), R(50, -55), R(50, 55), R(40, 145), R(0, 162)], lc(leather, (255, 220, 170), .22))
        p.line([R(-70, 10), R(-34, -30), R(36, -30), R(66, 10)], strap, 22 * s)
        p.line([R(-60, 92), R(0, 70), R(60, 92)], strap, 16 * s)
        p.line([R(0, -30), R(0, -130)], strap, 12 * s)

def snake(p, x0, x1, y, s, col, belly):
    """One long snake moving over the sand: a smooth tapering body, the head at the thick end, turned to the left."""
    pts = [(lerp(x0, x1, i / 120), y + math.sin(i / 120 * 10.5) * (120 - 60 * i / 120) * s) for i in range(121)]
    L, R = [], []
    for i, (x, yy) in enumerate(pts):
        f = i / 120; ax, ay = pts[max(0, i - 1)]; bx, by = pts[min(120, i + 1)]
        dx, dy = bx - ax, by - ay; n = math.hypot(dx, dy) or 1; w = (34 * (1 - f) ** .6 + 3) * s
        L.append((x - dy / n * w, yy + dx / n * w)); R.append((x + dy / n * w, yy - dx / n * w))
    body = L + R[::-1]
    p.poly([(a + 8 * s, b + 16 * s) for a, b in body], (0, 0, 0), 70)                      # shadow on the sand
    p.poly(body, col)
    for i in range(6, 112, 9):
        x, yy = pts[i]; p.ell(x, yy, (12 * (1 - i / 120) + 4) * s, (12 * (1 - i / 120) + 4) * s, belly, 210)
    hx, hy = pts[0]
    p.ell(hx - 26 * s, hy, 56 * s, 34 * s, col); p.ell(hx - 50 * s, hy - 12 * s, 6 * s, 6 * s, (240, 220, 120))

def halls(p, cx, base, s, col, lights=None):
    """Grand columned halls (Pharaoh's rule). Building only."""
    dark = lc(col, (0, 0, 0), .35)
    for k in range(5): p.rect(cx - (420 - k * 18) * s, base - k * 16 * s, cx + (420 - k * 18) * s, base - (k - 1) * 16 * s, lc(col, (255, 255, 255), .05 * k))
    top = base - 460 * s
    p.rect(cx - 380 * s, top, cx + 380 * s, base - 80 * s, dark)
    for i in range(9):
        x = cx - 340 * s + i * 85 * s
        p.rect(x - 20 * s, top + 30 * s, x + 20 * s, base - 80 * s, col)
        p.poly([(x - 30 * s, top + 30 * s), (x + 30 * s, top + 30 * s), (x + 20 * s, top + 60 * s), (x - 20 * s, top + 60 * s)], lc(col, (255, 255, 255), .15))
        if lights and i < 8: p.glow(x + 42 * s, base - 200 * s, 60 * s, lights, .35)
    p.rect(cx - 410 * s, top - 30 * s, cx + 410 * s, top + 34 * s, col)

def rocks(p, seed, n, y0, y1, col):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(-60, 1140), rnd.uniform(y0, y1); w = rnd.uniform(40, 130) * (.6 + .6 * (y - y0) / max(1, y1 - y0)); h = w * rnd.uniform(.4, .65)
        p.poly([(x - w, y), (x - w * .6, y - h), (x + w * .2, y - h * 1.15), (x + w * .8, y - h * .5), (x + w, y)], lc(col, (0, 0, 0), rnd.uniform(0, .3)))

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (10, 8, 32)), (.35, (40, 26, 66)), (.54, (120, 62, 84)), (.63, (214, 120, 84)), (1, (40, 26, 30))])
    stars(p, 170, 3, 760)
def hook_mid(p):
    mountains(p, 1230, 520, (34, 24, 42), 5, (120, 70, 80), 4)
    p.glow(640, 1150, 330, (255, 140, 60), .55)
def hook_near(p):
    dunes(p, 1250, 44, (120, 76, 60), (46, 30, 34), 7)
    path(p, 390, 1930, 630, 1262, (22, 12, 14), 80)
    rocks(p, 8, 7, 1660, 1900, (34, 22, 26))

def travel_sky(p):
    p.sky([(0, (18, 16, 48)), (.42, (58, 44, 92)), (.6, (170, 96, 110)), (.68, (244, 160, 110)), (1, (50, 34, 40))])
    stars(p, 120, 13, 700)
def travel_mid(p):
    mountains(p, 1270, 640, (46, 34, 56), 15, (150, 90, 90), 3)
    p.glow(800, 950, 170, (255, 150, 70), .55)
    fire(p, 800, 985, 26, 54, 16)
def travel_near(p):
    dunes(p, 1290, 50, (156, 104, 76), (60, 40, 42), 17)
    tent(p, 260, 1470, 1.25, (58, 38, 34), (26, 16, 16))
    path(p, 420, 1700, 800, 1300, (60, 36, 30), 80, 60)

def tree_sky(p):
    p.sky([(0, (6, 8, 26)), (.5, (20, 24, 58)), (.72, (56, 44, 74)), (1, (22, 16, 22))])
    stars(p, 260, 21, 1050)
def tree_mid(p):
    mountains(p, 1320, 500, (20, 18, 36), 23, (60, 50, 80), 3)
def tree_near(p):
    dunes(p, 1340, 34, (76, 56, 50), (24, 18, 22), 24)
    p.glow(540, 1230, 460, (255, 180, 90), .5)
    tree(p, 540, 1480, 470, (34, 22, 20), (30, 62, 44), 25)
    rocks(p, 26, 8, 1600, 1880, (20, 14, 16))

def sandal_sky(p):
    p.sky([(0, (26, 18, 40)), (.4, (86, 54, 70)), (.6, (150, 96, 82)), (1, (70, 46, 42))])
def sandal_near(p):
    mountains(p, 800, 260, (70, 48, 62), 31, (190, 120, 100), 5)
    dunes(p, 790, 30, (176, 124, 88), (86, 56, 46), 33)
    rnd = random.Random(32)
    for _ in range(46):
        x, y = rnd.uniform(-100, 1180), rnd.uniform(1050, 1900)
        p.line([(x - 90, y), (x, y + rnd.uniform(-5, 5)), (x + 90, y)], (120, 80, 60), 3, 90)
    p.glow(540, 1400, 520, (255, 196, 120), .4)
    sandals(p, 540, 1490, 1.0)

def snake_sky(p):
    p.sky([(0, (10, 16, 36)), (.5, (30, 40, 70)), (.7, (90, 70, 90)), (1, (30, 22, 26))])
    stars(p, 90, 41, 500)
def snake_mid(p): mountains(p, 1180, 330, (22, 24, 40), 42, (70, 66, 90), 4)
def snake_near(p):
    dunes(p, 1200, 30, (120, 92, 76), (50, 36, 36), 43)
    snake(p, 130, 940, 1500, 1.3, (58, 40, 28), (210, 170, 100))
    rocks(p, 44, 6, 1720, 1900, (30, 22, 24))

def rule_sky(p):
    p.sky([(0, (22, 6, 26)), (.5, (92, 20, 46)), (.72, (196, 66, 52)), (1, (32, 8, 18))])
    cloud_bank(p, 340, (70, 18, 40), (34, 8, 22), 51, 70, 220)
def rule_mid(p): pyramids(p, 1330, (86, 30, 40), (44, 14, 26), 52)
def rule_near(p):
    p.rect(-100, 1360, 1200, 2300, (26, 8, 16))
    halls(p, 540, 1600, .92, (64, 24, 34), (255, 130, 70))

def pray_sky(p):
    p.sky([(0, (8, 12, 40)), (.5, (24, 34, 86)), (.74, (72, 62, 116)), (.84, (150, 96, 120)), (1, (26, 20, 30))])
    stars(p, 240, 61, 1050); moon(p, 820, 250, 46)
def pray_mid(p): mountains(p, 1400, 560, (18, 20, 44), 62, (80, 70, 120), 4)
def pray_near(p):
    dunes(p, 1420, 30, (70, 54, 64), (22, 16, 24), 63)
    tree(p, 860, 1540, 330, (24, 16, 18), (24, 40, 40), 64)
    rocks(p, 65, 7, 1640, 1880, (18, 14, 20))

def first_sky(p):
    p.sky([(0, (34, 42, 104)), (.45, (120, 96, 150)), (.68, (240, 150, 130)), (.78, (255, 200, 140)), (1, (70, 48, 50))])
    stars(p, 70, 71, 420)
def first_mid(p):
    p.glow(540, 1440, 420, (255, 210, 150), .5)
    mountains(p, 1440, 520, (46, 38, 70), 62, (240, 150, 120), 4)
def first_near(p):
    dunes(p, 1460, 30, (120, 84, 80), (40, 28, 34), 63)
    tree(p, 860, 1570, 330, (40, 26, 26), (44, 66, 54), 64)

def answer_sky(p):
    p.sky([(0, (36, 60, 130)), (.38, (96, 90, 140)), (.56, (232, 170, 130)), (.68, (255, 236, 190)), (1, (130, 96, 70))])
def answer_rays(p):
    rays(p, 540, 1320, (255, 232, 180), n=13, spread=120, length=1800, width=7, a=.3, angle=-90, seed=81)
    p.glow(540, 1320, 480, (255, 236, 190), .75); sun(p, 540, 1330, 86, (255, 246, 216))
def answer_near(p):
    mountains(p, 1460, 300, (92, 66, 66), 82, (255, 210, 150), 4)
    dunes(p, 1470, 30, (196, 146, 100), (100, 70, 56), 83)

# the loop rhyme: the same valley and the same track as frame 1, in morning light, and the fire is gone
def morn_sky(p):
    p.sky([(0, (86, 146, 214)), (.4, (186, 208, 228)), (.58, (252, 224, 186)), (.66, (255, 236, 200)), (1, (150, 120, 92))])
    clouds(p, 91, 300, 700, (255, 250, 240), 5, 120)
def morn_mid(p): mountains(p, 1230, 520, (136, 110, 116), 5, (255, 220, 180), 4)
def morn_near(p):
    dunes(p, 1250, 44, (232, 188, 136), (164, 118, 84), 7)
    path(p, 390, 1930, 630, 1262, (150, 104, 72), 90)
    rocks(p, 8, 7, 1660, 1900, (130, 96, 74))

def end_sky(p):
    p.sky([(0, (6, 8, 30)), (.45, (26, 30, 80)), (.7, (96, 70, 120)), (.82, (232, 150, 100)), (1, (26, 18, 22))])
    stars(p, 220, 101, 900); moon(p, 820, 300, 56)
def end_mid(p): mountains(p, 1400, 380, (20, 18, 38), 102, (130, 90, 110), 5)
def end_near(p): dunes(p, 1430, 40, (56, 40, 46), (16, 12, 16), 103)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=[('flames', FAR_FIRE), 'embers'], cam='hold', bloom=.6,
         title=dict(text='He walked toward a fire. Allah called his name.', hold=99, plain=True),
         no_caption=(0,),
         lines=['He walked toward a fire. Allah called his name.']),
    dict(layers=[travel_sky, travel_mid, travel_near], fx=['dust'], cam='right',
         lines=['Musa, peace be upon him, was travelling with his family.', 'He saw a fire toward the mountain. He went to bring some back, to warm them.']),
    dict(layers=[tree_sky, tree_mid, tree_near], fx=['twinkle'], cam='in', bloom=.75,
         verse=dict(key='28:30', ar=(13, 19), en='O Moses, indeed I am Allah, Lord of the worlds', line=1, ar_size=74, y=600),
         lines=['When he came to it, he was called from the tree:', 'O Moses, indeed I am Allah, Lord of the worlds.']),
    dict(layers=[sandal_sky, sandal_near], fx=['dust'], cam='out',
         lines=['He was told to remove his sandals, in the sacred valley of Tuwa.']),
    dict(layers=[snake_sky, snake_mid, snake_near], fx=['dust'], cam='in',
         verse=dict(key='28:31', ar=(12, 16), en='O Moses, approach and fear not', line=2, ar_size=74, y=600),
         lines=['He was told to throw down his staff.', 'It moved like a snake, and he turned and fled.', 'O Moses, approach and fear not.']),
    dict(layers=[rule_sky, rule_mid, rule_near], fx=['embers'], cam='up', pause=0.5,
         verse=dict(key='20:24', en='Go to Pharaoh. Indeed, he has transgressed', line=1, ar_size=78, y=560),
         lines=['Then came the command:', 'Go to Pharaoh. Indeed, he has transgressed.', 'He feared they would kill him. What would he say?']),
    dict(layers=[pray_sky, pray_mid, pray_near], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='20:25', ar=(1, 5), en='My Lord, expand for me my breast [with assurance]', line=1, ar_size=78, y=600),
         lines=['He prayed:', 'My Lord, expand for me my breast,']),
    dict(layers=[first_sky, first_mid, first_near], fx=['dust'], cam='in', bloom=.7,
         verse=dict(key='20:26', en='And ease for me my task', line=0, ar_size=84, y=600),
         lines=['And ease for me my task.', 'He asked for his brother Harun to help.']),
    dict(layers=[answer_sky, answer_rays, answer_near], fx=['dust'], cam='up', bloom=.8,
         verse=dict(key='20:36', ar=(1, 5), en='You have been granted your request, O Moses', line=1, ar_size=78, y=600),
         lines=['Allah answered:', 'You have been granted your request, O Moses.']),
    dict(layers=[morn_sky, morn_mid, morn_near], fx=['dust'], cam='out',
         lesson=dict(text='Facing something hard? Ask as he asked: Ease for me my task.', after=0, y=520, size=70), no_caption=(0,),
         lines=['Facing something hard? Ask as he asked: Ease for me my task.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with someone', line2='facing a hard task'), no_caption=(0,),
         lines=['Share this with someone facing a hard task. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa', 'Harun': 'hˈɑːɹuːn', 'Tuwa': 'tˈuːwa'}

CAPTION = """He walked toward a fire. Allah called his name. 🤍

Musa (Moses), peace be upon him, was travelling with his family when he saw a fire toward the mountain. When he came to it, he was called from the tree: "O Moses, indeed I am Allah, Lord of the worlds." (Quran 28:30)

His staff moved like a snake, and he turned and fled. Then he was told: "O Moses, approach and fear not." (Quran 28:31)

Then came the command: "Go to Pharaoh. Indeed, he has transgressed." (Quran 20:24)

He feared they would kill him (28:33). So he prayed: "My Lord, expand for me my breast [with assurance]. And ease for me my task." (Quran 20:25–26)

Allah answered: "You have been granted your request, O Moses." (Quran 20:36)

Facing something hard? Ask as he asked: "Ease for me my task."

📖 Sources: Quran 20:9–36, 28:29–35 (Saheeh International)
Share this with someone facing a hard task. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """What hard task are you asking Allah to ease for you today? 🤍

References: Quran, Surah Ta-Ha 20:9–36 and Surah Al-Qasas 28:29–35 (Saheeh International translation)."""
