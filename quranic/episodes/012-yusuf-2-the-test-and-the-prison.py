"""Story 12: Yusuf, part 2 of 3: the test and the prison. Sources: Quran 12:21-42 (Saheeh International).
No people are drawn: no Yusuf, no woman, no husband, no witness, no prisoners. Only Egypt, a house, closed doors,
a torn shirt, a prison wall and window, grapes, bread and birds (the two dreams of 12:36, as objects), the moon.
Facts used and where they are: a man from Egypt bought him and Yusuf grew up in his house (12:21-22); the woman in whose
house he was sought to seduce him and closed the doors (12:23, told modestly here as "tried to tempt him"); he said
"[I seek] the refuge of Allah" (12:23); they raced to the door and his shirt was torn from the back (12:25); a witness
from her family: "But if his shirt is torn from the back, then she has lied, and he is of the truthful" (12:27);
she threatened prison if he would not obey (12:32); his prayer "My Lord, prison is more to my liking than that to which
they invite me" (12:33); Allah averted their plan (12:34); he was imprisoned (12:35); two young men told him their
dreams (12:36); he called them to Allah alone (12:37-40) and gave the meaning (12:41); to the one he knew would go free
he said "Mention me before your master." But Satan made him forget, and Joseph remained in prison several years (12:42).
Not used: 12:24 (its meaning needs tafsir), the banquet and the cut hands (12:30-31), the fate of the second prisoner.
No one is named except Yusuf (the Quran names no one else here; "al-'Azeez" is a title and is not used).
Improvement tried today: hook text that does not compete with itself. Frame 1 shows only the big headline, and it
matches the spoken hook word for word ("Sin or prison? He chose prison."), so the karaoke caption is hidden on that
line (no_caption=(0,)). Emplifi's study of Facebook Reels: in speech-led Reels extra on-screen text lowered 10-second
retention by 6%; speech in the first 3 seconds raised it by about 25%. Also kept: series pill ("Yusuf · Part 2 of 3"),
open question answered in scene 7, 0.5 s pause before the key prayer, speed 1.1, lesson card, CAPTION_Y 1110."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  12'
VOICE, SPEED = 'bm_george', 1.1
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Yusuf, Part 2: The Test and the Prison'
HITS = [(5, 1, 0.0), (8, 0, 0.0)]
# "the prison", taken straight from the text of 12:33
TITLE_AR = quran()['verses']['12:33']['ar'].split()[2]

# ---------------------------------------------------------------- small scenery helpers for this story
def stone_wall(p, y0, y1, col=(70, 62, 66), seed=1, rows=11):
    """A rough wall of stone blocks filling the band y0..y1."""
    rnd = random.Random(seed); h = (y1 - y0) / rows
    p.rect(-100, y0, 1200, y1, lc(col, (0, 0, 0), .45))
    for r in range(rows):
        x = -100 - rnd.uniform(0, 120); y = y0 + r * h
        while x < 1200:
            w = rnd.uniform(130, 230); c = lc(col, (0, 0, 0) if rnd.random() < .5 else (255, 255, 255), rnd.uniform(0, .14))
            p.rect(x + 4, y + 4, x + w - 4, y + h - 4, c)
            p.line([(x + 8, y + 7), (x + w - 10, y + 7)], lc(c, (255, 255, 255), .12), 2)
            x += w

def barred_window(p, cx, cy, w, h, sky_col=(150, 180, 230), bars=4, frame=(30, 26, 30)):
    """A small high window with iron bars. The sky shows through it."""
    for x0, y0, x1, y1 in ((cx - w / 2 - 24, cy - h / 2 - 24, cx + w / 2 + 24, cy - h / 2), (cx - w / 2 - 24, cy + h / 2, cx + w / 2 + 24, cy + h / 2 + 24),
                           (cx - w / 2 - 24, cy - h / 2, cx - w / 2, cy + h / 2), (cx + w / 2, cy - h / 2, cx + w / 2 + 24, cy + h / 2)):
        p.rect(x0, y0, x1, y1, frame)                        # frame drawn as four sides so a moon painted first stays visible
    if sky_col: p.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, sky_col)
    for k in range(1, bars + 1):
        x = cx - w / 2 + k * w / (bars + 1); p.line([(x, cy - h / 2), (x, cy + h / 2)], (24, 22, 26), 14)
    p.line([(cx - w / 2, cy), (cx + w / 2, cy)], (24, 22, 26), 12)

def light_beam(p, x0, y0, x1, y1, spread, col=(210, 225, 255), a=60):
    """A soft shaft of light from a window (x0,y0, width spread) down to a patch on the floor at (x1,y1)."""
    def b(q):
        q.poly([(x0 - spread / 2, y0), (x0 + spread / 2, y0), (x1 + spread * .9, y1), (x1 - spread * .9, y1)], col, a)
        q.ell(x1, y1, spread * 1.1, spread * .28, col, a + 40)
    p.blur_shape(b, 18)

def egypt_house(p, cx, base, s, col=(196, 160, 120), light=(255, 196, 110)):
    """A large flat-roofed Egyptian house with columns and lit windows. A building only."""
    w, h = 420 * s, 360 * s; shade = lc(col, (0, 0, 0), .35)
    p.rect(cx - w, base - h, cx + w, base, col)
    p.rect(cx - w - 20 * s, base - h - 30 * s, cx + w + 20 * s, base - h, lc(col, (255, 255, 255), .1))
    for k in range(-3, 4):                                   # columns along the front
        x = cx + k * 120 * s
        p.rect(x - 18 * s, base - h + 40 * s, x + 18 * s, base, lc(col, (255, 255, 255), .18))
        p.rect(x - 28 * s, base - h + 20 * s, x + 28 * s, base - h + 44 * s, shade)
    for k in (-2.5, -1.5, 1.5, 2.5):                          # lit windows between the columns
        x = cx + k * 120 * s; p.rect(x - 22 * s, base - h + 90 * s, x + 22 * s, base - h + 170 * s, light)
        p.glow(x, base - h + 130 * s, 70 * s, light, .5)
    p.rect(cx - 50 * s, base - 200 * s, cx + 50 * s, base, (60, 40, 26))   # tall closed door in the middle
    p.rect(cx - 70 * s, base, cx + 70 * s, base + 20 * s, shade)

def doors(p, cx, base, s, col=(92, 58, 34), shut=1.0):
    """A pair of tall carved wooden doors, closed, with a heavy bolt. Inside a lamplit room."""
    w, h = 300 * s, 760 * s; dark = lc(col, (0, 0, 0), .45)
    p.rect(cx - w - 40 * s, base - h - 60 * s, cx + w + 40 * s, base, (52, 34, 24))           # door frame
    p.ell(cx, base - h - 60 * s, w + 40 * s, 120 * s, (52, 34, 24))                            # arched top
    p.rect(cx - w, base - h, cx + w, base, col); p.ell(cx, base - h, w, 90 * s, col)
    p.line([(cx, base - h - 90 * s), (cx, base)], dark, 8 * s)
    for side in (-1, 1):                                     # carved panels
        for k in range(3):
            x0 = cx + side * 40 * s; x1 = cx + side * (w - 40 * s); y0 = base - h + 60 * s + k * 230 * s
            p.rect(min(x0, x1), y0, max(x0, x1), y0 + 180 * s, lc(col, (0, 0, 0), .2))
            p.rect(min(x0, x1) + 14 * s, y0 + 14 * s, max(x0, x1) - 14 * s, y0 + 166 * s, lc(col, (255, 255, 255), .08))
    p.rect(cx - 150 * s, base - h * .5 - 22 * s, cx + 150 * s, base - h * .5 + 22 * s, (40, 30, 26))   # bolt bar
    for x in (cx - 120 * s, cx + 120 * s): p.ell(x, base - h * .5, 16 * s, 16 * s, (170, 130, 60))

def torn_shirt(p, cx, cy, s, col=(214, 200, 172)):
    """A plain long shirt laid flat, back side up, with a long tear down the back (12:25-28). Object only."""
    p.ell(cx, cy + 230 * s, 380 * s, 74 * s, (60, 52, 56))
    body = [(cx - 120 * s, cy - 170 * s), (cx - 40 * s, cy - 182 * s), (cx + 40 * s, cy - 182 * s), (cx + 120 * s, cy - 170 * s),
            (cx + 260 * s, cy - 90 * s), (cx + 220 * s, cy - 30 * s), (cx + 130 * s, cy - 80 * s), (cx + 140 * s, cy + 210 * s), (cx - 140 * s, cy + 210 * s),
            (cx - 130 * s, cy - 80 * s), (cx - 220 * s, cy - 30 * s), (cx - 260 * s, cy - 90 * s)]
    p.poly(body, col)
    p.line([(cx - 40 * s, cy - 182 * s), (cx + 40 * s, cy - 182 * s)], lc(col, (0, 0, 0), .3), 4 * s)
    # the tear: a ragged dark gap running down the back, edges lifted
    left = [(cx - 6 * s + 10 * s * math.sin(k * 1.7), cy - 150 * s + k * 34 * s) for k in range(11)]
    right = [(x + (14 + 8 * math.sin(k * 2.3)) * s * min(1, k / 3), y) for k, (x, y) in enumerate(left)]
    p.poly(left + right[::-1], (40, 30, 30))
    p.line(left, lc(col, (255, 255, 255), .25), 3 * s); p.line(right, lc(col, (0, 0, 0), .2), 3 * s)

def grapes(p, cx, cy, s, col=(120, 40, 90)):
    """A bunch of grapes with a leaf (the first young man's dream: pressing wine, 12:36)."""
    p.line([(cx, cy - 150 * s), (cx + 10 * s, cy - 90 * s)], (70, 50, 30), 8 * s)
    p.poly([(cx + 10 * s, cy - 130 * s), (cx + 110 * s, cy - 170 * s), (cx + 90 * s, cy - 90 * s)], (70, 120, 50))
    rows = [(0, 5), (1, 4), (2, 4), (3, 3), (4, 2), (5, 1)]
    for r, n in rows:
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * 46 * s; y = cy - 80 * s + r * 40 * s
            p.ell(x, y, 25 * s, 25 * s, col); p.ell(x - 8 * s, y - 8 * s, 7 * s, 7 * s, lc(col, (255, 255, 255), .45))

def bread_tray(p, cx, cy, s):
    """Round loaves of bread on a flat tray (the second young man's dream, 12:36). Object only."""
    p.ell(cx, cy + 40 * s, 200 * s, 36 * s, (110, 80, 50)); p.ell(cx, cy + 30 * s, 190 * s, 30 * s, (150, 110, 70))
    for dx, dy, r in ((-90, 0, 70), (70, -5, 75), (-10, -40, 72)):
        p.ell(cx + dx * s, cy + dy * s, r * s, r * .55 * s, (200, 140, 70))
        p.ell(cx + dx * s - 10 * s, cy + dy * s - 12 * s, r * .55 * s, r * .22 * s, (232, 182, 110))

def bird(p, x, y, s, col=(30, 26, 30), up=True):
    """A small bird in flight, a simple 'm' shape."""
    k = -1 if up else 1
    p.line([(x - 40 * s, y + k * 18 * s), (x - 18 * s, y - k * 4 * s), (x, y + 6 * s), (x + 18 * s, y - k * 4 * s), (x + 40 * s, y + k * 18 * s)], col, 6 * s)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_wall(p):
    p.sky([(0, (10, 10, 18)), (1, (4, 4, 8))])
    stone_wall(p, -200, 2300, (64, 58, 66), 1, 26)
    p.rect(390, 965, 690, 1195, (120, 150, 210))
    moon(p, 610, 1030, 34, col=(240, 236, 220))                # crescent painted before the bars so the bars sit in front
    barred_window(p, 540, 1080, 300, 230, None)
    p.glow(540, 1080, 420, (170, 200, 255), .45)
def hook_light(p):
    light_beam(p, 540, 1120, 600, 1620, 260)

def egypt_sky(p):
    p.sky([(0, (60, 40, 90)), (.42, (190, 110, 100)), (.66, (255, 170, 100)), (.8, (255, 214, 150)), (1, (90, 60, 40))])
    sun(p, 260, 1060, 70, (255, 226, 170)); p.glow(260, 1060, 420, (255, 160, 90), .5)
def egypt_mid(p):
    pyramids(p, 1220, (170, 100, 70), (120, 66, 46))
    for x in (90, 1000): palm(p, x, 1500, 420, (50, 40, 30), .08 if x > 500 else -.08)
def egypt_near(p):
    p.rect(-100, 1500, 1200, 2300, (110, 80, 54))
    egypt_house(p, 540, 1650, .95)

def room_bg(p):
    p.sky([(0, (40, 24, 18)), (.5, (70, 42, 28)), (1, (24, 14, 10))])
    p.glow(140, 1000, 420, (255, 170, 80), .35); p.glow(940, 1000, 420, (255, 170, 80), .35)
def room_near(p):
    doors(p, 540, 1560, 1.0)
    lantern(p, 140, 980, .7); lantern(p, 940, 980, .7)
    p.rect(-100, 1560, 1200, 2300, (40, 26, 18))

def shirt_bg(p):
    p.sky([(0, (24, 18, 30)), (.6, (50, 36, 48)), (1, (16, 12, 18))])
    p.glow(540, 1150, 700, (255, 200, 140), .3)
def shirt_near(p):
    torn_shirt(p, 540, 1520, 1.2)
    lantern(p, 920, 1240, .55)


def threat_sky(p):
    p.sky([(0, (20, 6, 12)), (.45, (90, 20, 26)), (.72, (170, 60, 40)), (1, (30, 10, 10))])
    cloud_bank(p, 900, (50, 14, 20), (90, 24, 26), 61, 70, 230)
def threat_mid(p):
    city(p, 1320, (40, 14, 16), 62, lights=(255, 150, 80), domes=False)
def threat_near(p):
    p.rect(-100, 1400, 1200, 2300, (20, 8, 8))
    barred_window(p, 540, 1560, 230, 170, (150, 50, 40), frame=(16, 8, 8))

def prayer_sky(p):
    p.sky([(0, (6, 8, 28)), (.5, (20, 26, 70)), (.85, (40, 44, 96)), (1, (10, 10, 22))])
    stars(p, 240, 71, 1300, (210, 220, 255))
def prayer_near(p):
    stone_wall(p, 1180, 2300, (56, 52, 66), 72, 10)
    barred_window(p, 540, 1320, 260, 200, (30, 40, 90))
    p.glow(540, 1320, 300, (150, 170, 255), .35)

def cell_bg(p):
    p.sky([(0, (14, 14, 20)), (1, (6, 6, 10))])
    stone_wall(p, -200, 1500, (66, 60, 64), 81, 15)
    barred_window(p, 300, 760, 220, 170, (190, 210, 240))
    p.rect(-100, 1500, 1200, 2300, (40, 34, 30))
def cell_near(p):
    light_beam(p, 300, 800, 620, 1560, 200, (255, 236, 200), 55)
    for x, y in ((180, 1600), (860, 1620), (500, 1700)):              # straw on the floor
        for k in range(9): p.line([(x - 60 + k * 14, y), (x - 40 + k * 15, y - 12 - (k % 3) * 6)], (170, 140, 80), 3)

def dreams_bg(p):
    p.sky([(0, (16, 12, 40)), (.5, (40, 30, 80)), (1, (10, 8, 20))])
    stars(p, 150, 91, 1600, (220, 210, 255))
    p.glow(300, 1420, 380, (200, 120, 200), .3); p.glow(790, 1480, 380, (255, 200, 120), .3)
def dreams_near(p):
    grapes(p, 300, 1420, 1.4)
    bread_tray(p, 790, 1520, 1.1)
    for x, y, s in ((700, 1300, 1.0), (860, 1250, .8), (960, 1340, .9)): bird(p, x, y, s, (230, 220, 240))

def years_bg(p):
    p.sky([(0, (8, 8, 16)), (1, (4, 4, 8))])
    stone_wall(p, -200, 2300, (52, 48, 56), 101, 26)
    p.rect(280, 1230, 800, 1630, (14, 20, 50))
    stars(p, 40, 102, 1620); moon(p, 640, 1330, 40, col=(240, 236, 220))
    barred_window(p, 540, 1430, 520, 400, None, bars=5)
def years_moons(p):
    light_beam(p, 540, 1480, 560, 1880, 340, (180, 200, 255), 40)

def lesson_sky(p):
    p.sky([(0, (40, 60, 120)), (.45, (150, 160, 200)), (.72, (255, 210, 160)), (1, (140, 96, 70))])
def lesson_near(p):
    stone_wall(p, 1050, 2300, (90, 80, 84), 111, 12)
    barred_window(p, 540, 1260, 300, 240, (255, 226, 170))
    p.glow(540, 1260, 520, (255, 220, 160), .55)
    light_beam(p, 540, 1300, 540, 1760, 300, (255, 230, 180), 60)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 121, 900); moon(p, 820, 300, 56)
def end_mid(p): pyramids(p, 1330, (60, 46, 64), (40, 30, 46))
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_wall, hook_light], fx=['dust'], cam='in', bloom=.65,
         title=dict(text='Sin or prison? He chose prison', arabic=TITLE_AR, part='Yusuf · Part 2 of 3', hold=99, plain=True),
         no_caption=(0,),
         lines=['Sin, or prison? He chose prison. Why?']),
    dict(layers=[egypt_sky, egypt_mid, egypt_near], fx=['dust'], cam='in',
         lines=["In Egypt, Yusuf, peace be upon him, grew up in his master's house.",
                "The man's wife tried to tempt him. She closed the doors."]),
    dict(layers=[room_bg, room_near], fx=['embers'], cam='hold',
         verse=dict(key='12:23', ar=(13, 15), en='[I seek] the refuge of Allah', line=1, ar_size=96, y=600),
         lines=['He said:', 'I seek the refuge of Allah.']),
    dict(layers=[shirt_bg, shirt_near], fx=['dust'], cam='in',
         verse=dict(key='12:27', en='But if his shirt is torn from the back, then she has lied, and he is of the truthful', line=2, ar_size=70, y=560),
         lines=['He ran for the door. His shirt was torn from the back.', 'A witness from her family said:',
                'But if his shirt is torn from the back, then she has lied, and he is of the truthful.']),
    dict(layers=[threat_sky, threat_mid, threat_near], fx=['embers'], cam='in', pause=0.5,
         lines=['Still, she threatened him with prison.']),
    dict(layers=[prayer_sky, prayer_near], fx=['twinkle'], cam='up', bloom=.7,
         verse=dict(key='12:33', ar=(1, 8), en='My Lord, prison is more to my liking than that to which they invite me', line=1, ar_size=74, y=620),
         lines=['He prayed:', 'My Lord, prison is more to my liking than that to which they invite me.']),
    dict(layers=[cell_bg, cell_near], fx=['dust'], cam='in',
         lines=["So he was put in prison. There, he explained two men's dreams, and called them to Allah alone."]),
    dict(layers=[dreams_bg, dreams_near], fx=['twinkle'], cam='in',
         lines=['He told the one who would go free: Mention me before your master.']),
    dict(layers=[years_bg, years_moons], fx=['dust'], cam='hold', pause=0.4,
         lines=['But Satan made him forget. And Yusuf stayed in prison for several years.']),
    dict(layers=[lesson_sky, lesson_near], fx=['dust'], cam='out',
         lesson=dict(text='Choose Allah, even when it costs you.', after=0, y=560), no_caption=(0,),
         lines=['Choose Allah, even when it costs you.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Part 3 tomorrow', line2='Follow Quranic Story'),
         lines=['Who would remember him? Part 3 tomorrow, in sha Allah.',
                'Share this with someone being tested. And follow for a new story from the Quran every day.']),
]

PRON = {'Yusuf': 'jˈuːsʊf', 'in sha Allah': 'ˌɪn ʃɑː ˈælə'}

CAPTION = """Sin, or prison? He chose prison. Why? 🤍 (Yusuf, Part 2 of 3)

In Egypt, Yusuf (peace be upon him) grew up in the house of the man who bought him. The man's wife tried to tempt him and closed the doors. He said: "[I seek] the refuge of Allah." (Quran 12:23)

He ran for the door, and his shirt was torn from the back. A witness from her family said: "But if his shirt is torn from the back, then she has lied, and he is of the truthful." (Quran 12:27)

Still she threatened him with prison. He prayed: "My Lord, prison is more to my liking than that to which they invite me." (Quran 12:33)

In prison he explained two men's dreams and called them to Allah alone. He asked the one who would go free to mention him to his master. But Satan made him forget, and Yusuf stayed in prison several years (12:42).

Choose Allah, even when it costs you.

📖 Sources: Quran 12:21–42 (Saheeh International)
Part 3 tomorrow, in sha Allah. Share this with someone who needs it. Follow for a new story every day.

#QuranicStories #ProphetYusuf #IslamicReminder"""

FIRST_COMMENT = """Which moment of Yusuf's story stays with you most: the well, the closed doors, or the prison? 🤍

References: Quran, Surah Yusuf 12:21–42 (Saheeh International translation). Part 3 tomorrow, in sha Allah."""
