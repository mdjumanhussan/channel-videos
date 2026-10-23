"""Special: Surah An-Nasr (110), the whole surah, about 90 s. Made on request by Juman (23 Oct 2026); not a row of series.md.
Sources: Quran 110:1-3 (Saheeh International, from data/quran.json).
Hadith, both confirmed on sunnah.com on 2026-10-23:
- Sahih al-Bukhari 4970 (Ibn Abbas): Umar asked the elders of Badr about 110:1. Some said: "We are ordered to praise Allah
  and ask for His forgiveness", others were silent. Ibn Abbas said: "That is the sign of the death of Allah's Messenger (ﷺ)
  which Allah informed him of", and the text glosses al-fath as "the conquest (of Mecca)". Umar said: "I do not know
  anything about it other than what you have said."
- Sahih al-Bukhari 4968 (Aisha): he used to say very often in bowing and prostration "Subhanaka Allahumma Rabbana wa
  bihamdika; Allahumma ighfirli", according to the order of the Quran.
Not used (not Bukhari/Muslim, or not needed): Ahmad's "my death has been announced to me", the Nasa'i/Muslim "last surah",
Jabir's "they will leave it in crowds", the "one quarter of the Quran" report.
No people are drawn: no Prophet, no companions, no crowds. Only Makkah's valley and the Kabah, mountains, many small
travellers' lamps streaming down the paths (the "multitudes" as lights), a lone lamp at sunset, a mosque at night, the sky.
No music. Speed 0.86 and longer pauses after each verse card (slower, calmer than the story Reels) so the surah lands at about 90 s as asked."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from engine import *

BADGE = 'Quranic Story  ·  Surah 110'
VOICE, SPEED = 'bm_george', 0.86
CAPTION_Y = 1110
THUMB_AT = 1.0
TITLE = 'Surah An-Nasr: The Victory That Was a Farewell'
HITS = [(7, 1, 0.0), (8, 0, 0.0)]
TITLE_AR = quran()['verses']['110:1']['ar'].split()[2]          # نَصۡرُ  (victory/help), from 110:1

# ---------------------------------------------------------------- small scenery helpers for this surah
def valley(p, base, col_far, col_near, seed):
    """Two ranges of dark rocky hills closing in on a valley floor (Makkah's setting)."""
    mountains(p, base - 120, 520, col_far, seed, peaks=6)
    mountains(p, base + 60, 380, col_near, seed + 1, peaks=5)

def lamp_paths(p, seed, n_paths=6, per=26, col=(255, 196, 110), meet=(540, 1480)):
    """Many small travellers' lamps streaming down winding paths into one valley: the 'multitudes' of 110:2 shown as lights only."""
    rnd = random.Random(seed)
    for k in range(n_paths):
        sx = -80 + k * 1240 / (n_paths - 1) + rnd.uniform(-40, 40); sy = rnd.uniform(860, 1060)
        wob = rnd.uniform(40, 90); ph = rnd.uniform(0, 6.28)
        for i in range(per):
            u = i / (per - 1); x = lerp(sx, meet[0], u) + wob * math.sin(u * 7 + ph) * (1 - u); y = lerp(sy, meet[1], u ** .9)
            r = lerp(3.2, 6.5, u) * rnd.uniform(.8, 1.2)
            p.glow(x, y, r * 6, col, .35); p.ell(x, y, r, r, (255, 236, 190))
    p.glow(meet[0], meet[1], 260, col, .55)

def oil_lamp(p, cx, base, s=1.0, flame=(255, 200, 100)):
    """A small clay oil lamp on a ledge, its flame burning low. Object only."""
    clay = (120, 74, 46); dark = lc(clay, (0, 0, 0), .4)
    p.ell(cx, base, 150 * s, 26 * s, (40, 26, 20))
    p.poly([(cx - 130 * s, base - 10 * s), (cx + 60 * s, base - 10 * s), (cx + 150 * s, base - 50 * s), (cx + 170 * s, base - 70 * s),
            (cx + 110 * s, base - 64 * s), (cx + 40 * s, base - 70 * s), (cx - 110 * s, base - 70 * s)], clay)
    p.ell(cx - 30 * s, base - 70 * s, 85 * s, 22 * s, lc(clay, (255, 255, 255), .12)); p.ell(cx - 30 * s, base - 72 * s, 26 * s, 9 * s, dark)
    p.line([(cx - 130 * s, base - 40 * s), (cx - 175 * s, base - 70 * s), (cx - 150 * s, base - 105 * s)], clay, 14 * s)   # handle
    fx, fy = cx + 168 * s, base - 76 * s
    p.glow(fx, fy - 30 * s, 260 * s, flame, .6)
    p.poly([(fx - 14 * s, fy), (fx - 6 * s, fy - 40 * s), (fx, fy - 70 * s), (fx + 8 * s, fy - 38 * s), (fx + 14 * s, fy)], flame)
    p.poly([(fx - 6 * s, fy), (fx, fy - 34 * s), (fx + 6 * s, fy)], (255, 248, 220))

def book_stand(p, cx, base, s=1.0, col=(92, 60, 36)):
    """An open book resting on a folding wooden stand (a rahl), seen from the front. Object only."""
    for side in (-1, 1):                                         # crossed legs of the stand
        p.line([(cx + side * 170 * s, base), (cx - side * 60 * s, base - 170 * s)], col, 16 * s)
    p.poly([(cx - 220 * s, base - 150 * s), (cx, base - 190 * s), (cx + 220 * s, base - 150 * s), (cx + 220 * s, base - 130 * s), (cx, base - 170 * s), (cx - 220 * s, base - 130 * s)], lc(col, (0, 0, 0), .2))
    for side in (-1, 1):                                         # the two open pages, rising from the spine
        p.poly([(cx, base - 186 * s), (cx + side * 205 * s, base - 150 * s), (cx + side * 195 * s, base - 250 * s), (cx, base - 280 * s)], (232, 220, 190))
        for k in range(5):
            y = base - 245 * s + k * 18 * s
            p.line([(cx + side * 30 * s, y - 6 * s * (1 - k / 5)), (cx + side * 170 * s, y + 20 * s)], (150, 130, 100), 3 * s)
    p.line([(cx, base - 280 * s), (cx, base - 186 * s)], (120, 96, 70), 4 * s)
    p.glow(cx, base - 230 * s, 260 * s, (255, 220, 160), .25)

# ---------------------------------------------------------------- layer painters (screen coords, 1080x1920)
def hook_sky(p):
    p.sky([(0, (8, 10, 30)), (.4, (30, 34, 80)), (.66, (150, 90, 90)), (.8, (250, 170, 100)), (1, (40, 22, 18))])
    stars(p, 160, 11, 800)
    sun(p, 540, 1290, 80, (255, 214, 150))
def hook_mid(p): valley(p, 1360, (60, 40, 50), (34, 22, 28), 12)
def hook_near(p):
    p.rect(-100, 1500, 1200, 2300, (22, 14, 16))
    kaaba(p, 540, 1580, .9)

def intro_sky(p):
    p.sky([(0, (6, 8, 26)), (.55, (20, 28, 66)), (.85, (60, 50, 90)), (1, (14, 12, 22))])
    stars(p, 260, 21, 1250, (220, 225, 255)); moon(p, 790, 420, 52)
def intro_mid(p): valley(p, 1400, (30, 30, 56), (18, 16, 32), 22)
def intro_near(p):
    p.rect(-100, 1560, 1200, 2300, (12, 10, 18))
    book_stand(p, 540, 1700, 1.25)
    lantern(p, 830, 1500, .7)

def v1_sky(p):
    p.sky([(0, (40, 30, 80)), (.4, (190, 110, 110)), (.62, (255, 190, 120)), (.75, (255, 226, 170)), (1, (80, 50, 36))])
    sun(p, 540, 1180, 95, (255, 230, 180)); rays(p, 540, 1180, (255, 220, 160), n=11, spread=120, a=.16, angle=-90, seed=31)
def v1_mid(p): valley(p, 1380, (120, 70, 60), (70, 40, 34), 32)
def v1_near(p):
    p.rect(-100, 1520, 1200, 2300, (52, 30, 24))
    kaaba(p, 540, 1610, .8)

def conquest_sky(p):
    p.sky([(0, (70, 110, 170)), (.5, (200, 190, 190)), (.75, (255, 214, 160)), (1, (120, 80, 60))])
    clouds(p, 41, 300, 800, (255, 236, 210), 6, 120)
def conquest_mid(p):
    valley(p, 1300, (150, 104, 84), (110, 72, 56), 42)
    city(p, 1480, (90, 60, 46), 43, lights=None, domes=False)
def conquest_near(p):
    p.rect(-100, 1560, 1200, 2300, (70, 46, 34))
    kaaba(p, 540, 1640, .7)

def v2_sky(p):
    p.sky([(0, (6, 8, 24)), (.5, (24, 26, 64)), (.8, (70, 50, 70)), (1, (16, 10, 14))])
    stars(p, 220, 51, 900)
def v2_mid(p): valley(p, 1180, (34, 28, 48), (24, 18, 30), 52)
def v2_near(p):
    p.rect(-100, 1440, 1200, 2300, (20, 14, 18))
    lamp_paths(p, 53, meet=(540, 1500))
    kaaba(p, 540, 1560, .45)

def v3_sky(p):
    p.sky([(0, (4, 6, 22)), (.5, (16, 22, 60)), (.82, (40, 40, 86)), (1, (10, 10, 20))])
    stars(p, 300, 61, 1300, (215, 225, 255))
def v3_near(p):
    mosque(p, 540, 1520, 1.1, (14, 14, 26), windows=(255, 200, 120))
    p.rect(-100, 1560, 1200, 2300, (10, 10, 18))

def why_sky(p):
    p.sky([(0, (10, 10, 24)), (.6, (30, 26, 50)), (1, (8, 6, 12))])
    stars(p, 90, 71, 1000)
def why_near(p):
    p.rect(-100, 1500, 1200, 2300, (26, 20, 24))
    oil_lamp(p, 470, 1520, 1.3)

def elders_sky(p):
    p.sky([(0, (24, 18, 30)), (.5, (60, 40, 50)), (1, (18, 12, 14))])
    p.glow(540, 1150, 700, (255, 190, 120), .25)
def elders_near(p):
    for x in (150, 930): lantern(p, x, 900, .65)
    p.rect(-100, 1560, 1200, 2300, (34, 22, 20))
    book_stand(p, 540, 1690, 1.1)

def farewell_sky(p):
    p.sky([(0, (30, 26, 70)), (.42, (120, 70, 100)), (.64, (240, 130, 80)), (.74, (255, 190, 120)), (1, (40, 20, 18))])
    sun(p, 540, 1330, 70, (255, 200, 140))
def farewell_mid(p): valley(p, 1420, (70, 34, 40), (40, 20, 24), 82)
def farewell_near(p):
    p.rect(-100, 1600, 1200, 2300, (24, 12, 12))
    oil_lamp(p, 330, 1640, .9)

def aisha_sky(p):
    p.sky([(0, (4, 6, 20)), (.5, (14, 20, 54)), (.85, (34, 34, 74)), (1, (8, 8, 16))])
    stars(p, 260, 91, 1200, (225, 230, 255)); moon(p, 270, 470, 46)
def aisha_near(p):
    mosque(p, 540, 1560, .85, (12, 12, 22), windows=(255, 210, 140))
    p.rect(-100, 1600, 1200, 2300, (8, 8, 14))

def lesson_sky(p):
    p.sky([(0, (50, 80, 150)), (.45, (170, 170, 200)), (.7, (255, 214, 160)), (1, (140, 96, 70))])
    sun(p, 540, 1380, 70, (255, 236, 190))
def lesson_near(p): valley(p, 1500, (120, 84, 80), (80, 54, 50), 102)

def end_sky(p):
    p.sky([(0, (6, 10, 32)), (.45, (26, 34, 78)), (.72, (90, 80, 120)), (.84, (220, 150, 110)), (1, (26, 18, 20))])
    stars(p, 220, 111, 900); moon(p, 820, 300, 56)
def end_mid(p): valley(p, 1400, (50, 40, 64), (30, 24, 40), 112)
def end_near(p): lantern(p, 150, 860, .8)

# ---------------------------------------------------------------- scenes
SCENES = [
    dict(layers=[hook_sky, hook_mid, hook_near], fx=['dust'], cam='in', bloom=.65, pause=0.8,
         title=dict(text='A surah of victory. Or a farewell?', arabic=TITLE_AR, hold=99, plain=True),
         no_caption=(0,),
         lines=['A surah of victory. Or a farewell?']),
    dict(layers=[intro_sky, intro_mid, intro_near], fx=['twinkle'], cam='in', pause=0.7,
         lines=['Surah An-Nasr. Three verses, near the end of the Quran.']),
    dict(layers=[v1_sky, v1_mid, v1_near], fx=['dust'], cam='in', bloom=.7,
         verse=dict(key='110:1', line=1, ar_size=84, y=640), pause=0.9,
         lines=['Allah says:', 'When the victory of Allah has come, and the conquest,']),
    dict(layers=[conquest_sky, conquest_mid, conquest_near], fx=['dust'], cam='right', pause=0.7,
         lines=['Ibn Abbas explained this conquest was the conquest of Makkah.']),
    dict(layers=[v2_sky, v2_mid, v2_near], fx=['fireflies'], cam='in', pause=0.9,
         verse=dict(key='110:2', line=0, ar_size=78, y=660),
         lines=['And you see the people entering into the religion of Allah in multitudes,']),
    dict(layers=[v3_sky, v3_near], fx=['twinkle'], cam='up', bloom=.7, pause=1.0,
         verse=dict(key='110:3', line=0, ar_size=70, y=700),
         lines=['Then exalt Him with praise of your Lord, and ask forgiveness of Him. Indeed, He is ever Accepting of repentance.']),
    dict(layers=[why_sky, why_near], fx=['dust'], cam='hold', pause=0.6,
         lines=['Victory, then forgiveness? Why?']),
    dict(layers=[elders_sky, elders_near], fx=['embers'], cam='in', pause=0.7,
         lines=['Umar asked the elders what this surah meant. Some said: we are ordered to praise Allah and ask His forgiveness.',
                'Then young Ibn Abbas said: That is the sign of the death of Allah\'s Messenger, which Allah informed him of.']),
    dict(layers=[farewell_sky, farewell_mid, farewell_near], fx=['dust'], cam='out', pause=0.5,
         lines=['Umar said: I do not know anything about it other than what you have said.']),
    dict(layers=[aisha_sky, aisha_near], fx=['twinkle'], cam='in', pause=0.9,
         lines=['Aisha said the Prophet Muhammad, peace and blessings be upon him, would often glorify and praise Allah in his bowing and prostration, and ask His forgiveness, as the Quran commanded.']),
    dict(layers=[lesson_sky, lesson_near], fx=['dust'], cam='out', pause=1.0,
         lesson=dict(text='After every success: praise Allah, and ask His forgiveness.', after=0, y=660, size=76), no_caption=(0,),
         lines=['After every success: praise Allah, and ask His forgiveness.']),
    dict(layers=[end_sky, end_mid, end_near], fx=['twinkle'], cam='in',
         end=dict(after=0, line1='Follow Quranic Story', line2='From the Quran, every day'),
         lines=['Share this with someone celebrating a blessing. And follow for more from the Quran.']),
]

PRON = {'An-Nasr': 'ɐn nˈɑːsɚ', 'Ibn Abbas': 'ˌɪbn ʕɐbbˈɑːs', 'Umar': 'ˈʊmɐɹ', 'Aisha': 'ʕˈaɪʃɐ'}

CAPTION = """A surah of victory. Or a farewell? 🤍

Surah An-Nasr is only three verses:
"When the victory of Allah has come and the conquest, and you see the people entering into the religion of Allah in multitudes, then exalt [Him] with praise of your Lord and ask forgiveness of Him. Indeed, He is ever Accepting of repentance." (Quran 110:1–3)

Umar asked the elders what it meant. Ibn Abbas said: "That is the sign of the death of Allah's Messenger (ﷺ) which Allah informed him of." Umar said: "I do not know anything about it other than what you have said." (Sahih al-Bukhari 4970)

Aisha said the Prophet Muhammad (peace and blessings be upon him) would often glorify and praise Allah in his bowing and prostration and ask His forgiveness, as the Quran commanded. (Sahih al-Bukhari 4968)

After every success: praise Allah, and ask His forgiveness.

📖 Sources: Quran 110:1–3 (Saheeh International); Sahih al-Bukhari 4970, 4968
Share this with someone who needs it. Follow for more from the Quran.

#QuranicStories #SurahAnNasr #IslamicReminder"""

FIRST_COMMENT = """When Allah gives you a success, what do you say first? 🤍

References: Quran, Surah An-Nasr 110:1–3 (Saheeh International translation); Sahih al-Bukhari 4970 and 4968 (sunnah.com/bukhari:4970, sunnah.com/bukhari:4968)."""
