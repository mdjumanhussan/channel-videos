"""Story 16: Baby Musa (Moses) in the river. Sources: Quran 28:3-13, 20:37-40 (Saheeh International).
No people are drawn: no Musa (as a baby or otherwise), no mother, no sister, no Pharaoh or his wife, no nurses. Only the
river, reeds, a closed wooden chest on the water, a small mud-brick house with a lamp, Pharaoh's riverside halls,
pyramids under a red sky, the night sky and morning light.
Facts used and where they are: Pharaoh oppressed a sector of the people, slaughtering their newborn sons (28:4); Allah
inspired Musa's mother: "Suckle him; but when you fear for him, cast him into the river and do not fear and do not
grieve. Indeed, We will return him to you" (28:7); "Cast him into the chest and cast it into the river, and the river
will throw it onto the bank" (20:39); she said to his sister "Follow him", so she watched him from a distance (28:11);
the family of Pharaoh picked him up (28:8); Pharaoh's wife said "Do not kill him; perhaps he may benefit us" (28:9); the
heart of Musa's mother became empty (28:10); Allah had prevented all wet nurses from him, and his sister offered a
household that would be responsible for him (28:12); "So We restored him to his mother that she might be content and not
grieve and that she would know that the promise of Allah is true" (28:13, 20:40).
Not used: the wife's name (the Quran does not give it), the sister's name, Musa's father, any tafsir detail (the Nile by
name, how long he floated, who opened the chest, the number of nurses, payments to the mother), no "palace" claim in
narration (the Quran says only "the family of Pharaoh picked him up"; the riverside halls are scenery). Narration says
"a people he oppressed" as 28:4 does, without naming them.
Improvement tried today: frame 1 is one concrete human moment from the verses, said in under 10 words, with nothing else
on screen (no Arabic subtitle under the headline, no series label). Source: the page's own breakouts (Ayyub, al-Amin,
Cave of Hira) all open on one plain, specific moment (VIRAL-PLAYBOOK 2026-10-31, 2026-11-02). Also kept: plain headline =
spoken hook with caption hidden, hook answered by a verse card (28:7), second loop ("Where would the river take him?")
with a 0.5 s pause, payoff at the peak with a deep hit (28:13 closes the promise of 28:7), rhyming loop ending (the
lesson plays over the same river and reeds as frame 1, now in morning light and with the chest gone), speed 1.1, lesson
card, a specific send-to end card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  16'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Baby Musa in the River'
HITS = [(5, 0, 0.0), (8, 0, 0.0)]

WOOD = (130, 86, 48)

# ---------------------------------------------------------------- small scenery helpers for this story
def chest(p, cx, cy, s=1.0, wood=WOOD, band=(200, 160, 80)):
    """A closed wooden chest (20:39) floating, seen slightly from above: lid, planks, brass bands. Object only."""
    dark = lc(wood, (0, 0, 0), .45); hi = lc(wood, (255, 230, 190), .3)
    w, h, lid = 190 * s, 80 * s, 46 * s
    p.ell(cx, cy + h * .55, w * 1.25, 26 * s, (0, 0, 0), 70)                            # shadow on the water
    p.poly([(cx - w, cy - h * .2), (cx + w, cy - h * .2), (cx + w * .92, cy + h * .6), (cx - w * .92, cy + h * .6)], wood)
    for k in (1, 2): p.line([(cx - w * .96, cy - h * .2 + k * h * .26), (cx + w * .96, cy - h * .2 + k * h * .26)], dark, 3 * s)
    p.poly([(cx - w * 1.04, cy - h * .2), (cx - w * .9, cy - h * .2 - lid), (cx + w * .9, cy - h * .2 - lid), (cx + w * 1.04, cy - h * .2)], hi)
    p.line([(cx - w * .9, cy - h * .2 - lid), (cx + w * .9, cy - h * .2 - lid)], lc(hi, (255, 255, 255), .3), 3 * s)
    for dx in (-.62, .62):
        x = cx + dx * w; p.poly([(x - 12 * s, cy - h * .2 - lid), (x + 12 * s, cy - h * .2 - lid), (x + 12 * s, cy + h * .6), (x - 12 * s, cy + h * .6)], band)
    p.rect(cx - 16 * s, cy - h * .2 - 6 * s, cx + 16 * s, cy - h * .2 + 22 * s, band)
    for k in range(3):                                                                       # ripples around it
        r = (1.35 + k * .35); p.line([(cx - w * r, cy + h * .62 + k * 10 * s), (cx - w * (r - .3), cy + h * .66 + k * 10 * s)], (255, 255, 255), 2 * s, 90 - k * 25)
        p.line([(cx + w * (r - .3), cy + h * .66 + k * 10 * s), (cx + w * r, cy + h * .62 + k * 10 * s)], (255, 255, 255), 2 * s, 90 - k * 25)

def reeds(p, x0, x1, base, h, col, seed, n=40, tip=None):
    """A bed of tall reeds and papyrus heads along a river bank."""
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1); hh = h * rnd.uniform(.5, 1.0); lean = rnd.uniform(-.12, .12)
        c = lc(col, (0, 0, 0), rnd.uniform(0, .35))
        p.line([(x, base), (x + lean * hh * .5, base - hh * .5), (x + lean * hh, base - hh)], c, rnd.uniform(4, 8))
        if rnd.random() < .45:
            tx, ty = x + lean * hh, base - hh
            for a in range(-60, 61, 20):
                r = math.radians(a - 90); p.line([(tx, ty), (tx + 34 * math.cos(r), ty + 34 * math.sin(r))], tip or c, 2.5)
        elif rnd.random() < .5:
            p.ell(x + lean * hh, base - hh - 14, 6, 20, lc(c, (90, 60, 30), .4))

def river(p, top, c_top, c_bot, seed, shine=(255, 220, 170), bank=None):
    sea(p, top, c_top, c_bot, seed, shine)
    if bank: p.poly([(-200, top - 6), (1300, top - 6), (1300, top + 18), (-200, top + 30)], bank)

def halls(p, cx, base, s, col, lights=None):
    """Grand riverside halls with tall columns and steps down to the water (Pharaoh's household). Building only."""
    dark = lc(col, (0, 0, 0), .35)
    for k in range(5): p.rect(cx - (420 - k * 18) * s, base - k * 16 * s, cx + (420 - k * 18) * s, base - (k - 1) * 16 * s, lc(col, (255, 255, 255), .05 * k))
    top = base - 80 * s - 380 * s
    p.rect(cx - 380 * s, top, cx + 380 * s, base - 80 * s, dark)
    for i in range(9):
        x = cx - 340 * s + i * 85 * s
        p.rect(x - 20 * s, top + 30 * s, x + 20 * s, base - 80 * s, col)
        p.poly([(x - 30 * s, top + 30 * s), (x + 30 * s, top + 30 * s), (x + 20 * s, top + 60 * s), (x - 20 * s, top + 60 * s)], lc(col, (255, 255, 255), .15))
        if lights and i < 8: p.glow(x + 42 * s, base - 200 * s, 60 * s, lights, .35)
    p.rect(cx - 410 * s, top - 30 * s, cx + 410 * s, top + 34 * s, col)
    p.rect(cx - 410 * s, top - 10 * s, cx + 410 * s, top, lc(col, (255, 220, 160), .3))

def house(p, cx, base, s, col=(120, 84, 56), lamp=(255, 190, 100)):
    """A small mud-brick house with a flat roof and one lit window."""
    p.rect(cx - 170 * s, base - 230 * s, cx + 170 * s, base, col)
    p.rect(cx - 185 * s, base - 250 * s, cx + 185 * s, base - 226 * s, lc(col, (0, 0, 0), .25))
    p.rect(cx - 120 * s, base - 140 * s, cx - 50 * s, base, lc(col, (0, 0, 0), .5))
    if lamp:
        p.glow(cx + 70 * s, base - 140 * s, 160 * s, lamp, .55)
        p.rect(cx + 40 * s, base - 175 * s, cx + 100 * s, base - 110 * s, lamp)
    else:
        p.rect(cx + 40 * s, base - 175 * s, cx + 100 * s, base - 110 * s, lc(col, (0, 0, 0), .55))

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def dusk_sky(p):
    p.sky([(0, (40, 26, 60)), (.4, (130, 70, 90)), (.6, (240, 140, 90)), (.68, (255, 196, 130)), (1, (60, 40, 50))])
    sun(p, 760, 1220, 70, (255, 214, 150))
def dusk_far(p):
    reeds(p, -60, 260, 1300, 300, (40, 30, 34), 2, 34); reeds(p, 820, 1140, 1300, 320, (40, 30, 34), 3, 34)
def dusk_water(p):
    river(p, 1290, (220, 140, 110), (40, 30, 50), 4, (255, 210, 160))
    p.glow(760, 1330, 260, (255, 200, 140), .35)
    chest(p, 540, 1430, 1.0)
    reeds(p, -80, 200, 1900, 560, (24, 20, 22), 5, 30); reeds(p, 900, 1160, 1900, 520, (24, 20, 22), 6, 26)

def tyranny_sky(p):
    p.sky([(0, (24, 6, 10)), (.5, (100, 26, 24)), (.72, (190, 70, 40)), (1, (30, 10, 10))])
    cloud_bank(p, 360, (70, 20, 20), (36, 10, 12), 11, 70, 220)
def tyranny_mid(p): pyramids(p, 1360, (70, 30, 26), (40, 16, 16), 12)
def tyranny_near(p):
    p.rect(-100, 1360, 1200, 2300, (26, 10, 10))
    halls(p, 540, 1560, .9, (60, 26, 24), (255, 150, 80))

def night_sky(p):
    p.sky([(0, (8, 10, 30)), (.55, (26, 30, 66)), (.78, (60, 50, 80)), (1, (14, 14, 22))])
    stars(p, 220, 21, 1000); moon(p, 820, 270, 46)
def night_mid(p): river(p, 1420, (40, 44, 80), (10, 10, 20), 22, (180, 190, 255))
def night_near(p):
    p.rect(-100, 1300, 560, 1440, (30, 24, 26))
    house(p, 260, 1320, 1.0, (70, 50, 40))
    palm(p, 470, 1330, 380, (20, 16, 20), .05)
    reeds(p, 560, 1140, 1460, 300, (18, 18, 24), 23, 30)

def dawn_sky(p):
    p.sky([(0, (40, 50, 100)), (.45, (150, 130, 160)), (.62, (255, 190, 140)), (.7, (255, 225, 170)), (1, (80, 70, 70))])
    sun(p, 300, 1230, 60, (255, 230, 180))
def dawn_water(p):
    river(p, 1250, (230, 180, 150), (40, 50, 80), 31, (255, 230, 190))
    p.glow(300, 1290, 240, (255, 220, 170), .35)
    chest(p, 620, 1420, .8)
    reeds(p, -80, 280, 1900, 600, (34, 30, 34), 32, 34); reeds(p, 940, 1160, 1900, 460, (34, 30, 34), 33, 20)

def wide_sky(p):
    p.sky([(0, (60, 110, 170)), (.5, (170, 190, 210)), (.66, (250, 220, 170)), (1, (110, 110, 90))])
    clouds(p, 41, 260, 640, (255, 248, 236), 6, 150)
def wide_far(p):
    p.rect(-100, 1200, 1200, 1240, (110, 120, 70)); palm(p, 120, 1220, 220, (60, 70, 40), -.04); palm(p, 980, 1220, 240, (60, 70, 40), .05)
def wide_water(p):
    river(p, 1230, (120, 160, 190), (30, 50, 70), 42, (255, 255, 255))
    chest(p, 540, 1290, .32)
    reeds(p, -80, 300, 1900, 640, (50, 70, 40), 43, 36, (160, 140, 80)); reeds(p, 780, 1160, 1900, 600, (50, 70, 40), 44, 36, (160, 140, 80))

def bank_sky(p):
    p.sky([(0, (70, 120, 180)), (.5, (190, 200, 215)), (.7, (255, 220, 160)), (1, (120, 100, 70))])
def bank_mid(p):
    halls(p, 540, 1380, 1.05, (200, 170, 130))
    palm(p, 60, 1300, 420, (50, 60, 30), .06); palm(p, 1020, 1300, 400, (50, 60, 30), -.06)
def bank_near(p):
    river(p, 1400, (120, 150, 170), (30, 40, 60), 51, (255, 255, 255))
    chest(p, 540, 1470, .75)
    reeds(p, -80, 230, 1900, 480, (50, 70, 40), 52, 26, (170, 150, 90)); reeds(p, 860, 1160, 1900, 460, (50, 70, 40), 53, 24, (170, 150, 90))

def garden_sky(p):
    p.sky([(0, (20, 18, 40)), (.5, (70, 50, 80)), (.75, (200, 130, 100)), (1, (40, 26, 26))])
    stars(p, 90, 61, 600)
def garden_mid(p): halls(p, 540, 1420, 1.0, (110, 80, 70), (255, 190, 110))
def garden_near(p):
    p.rect(-100, 1420, 1200, 2300, (34, 24, 22))
    for x, h, ln in ((90, 520, .05), (990, 500, -.05)): palm(p, x, 1500, h, (20, 16, 18), ln)
    lantern(p, 300, 1260, .7); lantern(p, 780, 1260, .7)

def empty_sky(p):
    p.sky([(0, (10, 12, 30)), (.6, (34, 36, 70)), (.85, (60, 50, 70)), (1, (16, 14, 20))])
    stars(p, 160, 71, 900)
def empty_mid(p): river(p, 1450, (40, 44, 70), (10, 10, 20), 72, (170, 180, 230))
def empty_near(p):
    p.rect(-100, 1330, 1200, 1470, (30, 24, 26))
    house(p, 540, 1360, 1.2, (66, 48, 40), None)
    reeds(p, -80, 260, 1500, 280, (16, 16, 22), 73, 22); reeds(p, 820, 1160, 1500, 280, (16, 16, 22), 74, 22)

def return_sky(p):
    p.sky([(0, (60, 90, 160)), (.45, (200, 170, 170)), (.62, (255, 210, 150)), (.72, (255, 236, 190)), (1, (110, 90, 70))])
def return_rays(p):
    rays(p, 540, 1200, (255, 230, 180), n=11, spread=110, length=1700, width=6, a=.26, angle=-90, seed=81)
    p.glow(540, 1200, 420, (255, 225, 170), .6)
def return_near(p):
    river(p, 1460, (200, 170, 150), (60, 60, 80), 82, (255, 240, 210))
    p.rect(-100, 1330, 1200, 1470, (120, 90, 60))
    house(p, 540, 1360, 1.2, (170, 120, 80), (255, 210, 130))
    palm(p, 200, 1370, 360, (60, 60, 30), -.05); palm(p, 900, 1370, 330, (60, 60, 30), .05)

# the loop rhyme: the same river and reeds as frame 1, in morning light, and the chest is gone
def morning_sky(p):
    p.sky([(0, (90, 150, 215)), (.4, (190, 210, 230)), (.6, (255, 230, 180)), (.68, (255, 240, 205)), (1, (110, 120, 110))])
    sun(p, 760, 1220, 70, (255, 246, 220))
def morning_far(p):
    reeds(p, -60, 260, 1300, 300, (70, 100, 60), 2, 34, (180, 160, 100)); reeds(p, 820, 1140, 1300, 320, (70, 100, 60), 3, 34, (180, 160, 100))
def morning_water(p):
    river(p, 1290, (190, 210, 220), (50, 80, 100), 4, (255, 255, 255))
    p.glow(760, 1330, 260, (255, 245, 220), .4)
    reeds(p, -80, 200, 1900, 560, (50, 76, 44), 5, 30, (170, 150, 90)); reeds(p, 900, 1160, 1900, 520, (50, 76, 44), 6, 26, (170, 150, 90))

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 121, 900); moon(p, 820, 300, 56)
def end_mid(p): river(p, 1420, (60, 60, 100), (10, 10, 20), 122, (200, 200, 255))
def end_near(p): reeds(p, -80, 1160, 1900, 360, (14, 14, 22), 123, 50)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[dusk_sky, dusk_far, dusk_water], fx=['dust'], cam='in', bloom=.55,
         title=dict(text='A mother cast her baby into the river. Why?', hold=99, plain=True),
         no_caption=(0,),
         lines=['A mother cast her baby into the river. Why?']),
    dict(layers=[tyranny_sky, tyranny_mid, tyranny_near], fx=['embers'], cam='right',
         lines=['Pharaoh was killing the newborn sons of a people he oppressed.']),
    dict(layers=[night_sky, night_mid, night_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='28:7', ar=(6, 19), en='when you fear for him, cast him into the river and do not fear and do not grieve. Indeed, We will return him to you', line=1, ar_size=66, y=600),
         lines=['Allah inspired the mother of Musa, peace be upon him:', 'When you fear for him, cast him into the river, and do not fear and do not grieve. Indeed, We will return him to you.']),
    dict(layers=[dawn_sky, dawn_water], fx=['dust'], cam='left',
         lines=['She cast him into the river in a chest.', 'His sister watched from a distance.']),
    dict(layers=[wide_sky, wide_far, wide_water], fx=['dust'], cam='in', pause=0.5,
         lines=['Where would the river take him?']),
    dict(layers=[bank_sky, bank_mid, bank_near], fx=['dust'], cam='out',
         lines=['Of all people, the family of Pharaoh picked him up.']),
    dict(layers=[garden_sky, garden_mid, garden_near], fx=['twinkle'], cam='in', bloom=.7,
         verse=dict(key='28:9', ar=(7, 12), en='Do not kill him; perhaps he may benefit us', line=1, ar_size=72, y=600),
         lines=["Pharaoh's wife said:", 'Do not kill him; perhaps he may benefit us.']),
    dict(layers=[empty_sky, empty_mid, empty_near], fx=['twinkle'], cam='in',
         lines=["His mother's heart became empty.", 'Allah kept every nurse from him, until his sister offered a family.']),
    dict(layers=[return_sky, return_rays, return_near], fx=['dust'], cam='up', bloom=.75,
         verse=dict(key='28:13', ar=(0, 13), en='So We restored him to his mother that she might be content and not grieve and that she would know that the promise of Allah is true', line=0, ar_size=60, y=620),
         lines=['So Allah returned him to his mother,', 'that she might be content, and know the promise of Allah is true.']),
    dict(layers=[morning_sky, morning_far, morning_water], fx=['dust'], cam='out',
         lesson=dict(text='The promise of Allah is true. Trust Him with what you love most.', after=0, y=520, size=72), no_caption=(0,),
         lines=['The promise of Allah is true. Trust Him with what you love most.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Share this with a mother', line2='who worries about her child'), no_caption=(0,),
         lines=['Share this with a mother who worries about her child. And follow for a new story from the Quran every day.']),
]

PRON = {'Musa': 'mˈuːsa'}

CAPTION = """A mother cast her baby into the river. Why? 🤍

Pharaoh was killing the newborn sons of a people he oppressed. Then Musa, peace be upon him, was born, and Allah inspired his mother: "Suckle him; but when you fear for him, cast him into the river and do not fear and do not grieve. Indeed, We will return him to you and will make him [one] of the messengers." (Quran 28:7)

She put him in a chest on the river, and his sister followed from a distance. Of all people, the family of Pharaoh picked him up. Pharaoh's wife said: "Do not kill him; perhaps he may benefit us." (Quran 28:9)

Allah kept every nurse from him, until his sister offered a family to care for him. "So We restored him to his mother that she might be content and not grieve and that she would know that the promise of Allah is true." (Quran 28:13)

The promise of Allah is true. Trust Him with what you love most.

📖 Sources: Quran 28:3–13, 20:37–40 (Saheeh International)
Share this with a mother who worries about her child. Follow for a new story every day.

#QuranicStories #ProphetMusa #IslamicReminder"""

FIRST_COMMENT = """Which mother would you send this to today? 🤍

References: Quran, Surah Al-Qasas 28:3–13 and Surah Ta-Ha 20:37–40 (Saheeh International translation)."""
