"""Episode: 3 Seconds From Flash to Thunder = About 1 km (what thunder is, light vs sound, the divide-by-three rule, why it rumbles, how far it carries, the safety rule)"""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = 'How Thunder Works'                            # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.88                            # about 155 wpm at 0.88 (lesson of 2026-11-25)
SHORT_HOOK = 'How far away is that lightning?'               # headline on the vertical Short
HITS = [(0, 2, 0.0), (5, 0, 0.0)]                            # "three seconds means about one kilometre", "It's three kilometres"
THUMB = ['3 SECONDS', '= 1 KM']
THUMB_COLS = [CY, YE]
MUSIC_LEVEL = 0.006
LEAD_IN = 0.15
PAUSES = {(0, 0): 0.3, (4, 0): 3.4, (2, 1): 0.7}
SHORT_PAUSES = {}
QZ = 8.6                                                     # length of the quiz line (set from tl.json after audio)
CAPTION_FIXES = {'thirty thousand degrees Celsius': '30,000 °C', 'thirty thousand degrees': '30,000 degrees',
                 'three hundred thousand kilometres': '300,000 km', 'fifteen kilometres': '15 km',
                 'twenty-five': '25', 'five kilometres': '5 km', 'thirty minutes': '30 minutes'}

# Colour code kept in every scene:
# light / the flash yellow, sound cyan, heat and pressure pink, you (the listener) green, safety green, distance purple.
LIGHT = YE; SOUND = CY; HEAT = PK; YOU = GR; DIST = PU
QUIZ = (46, 28, 74); DARK = (20, 22, 38); GROUND = (24, 30, 52); CLOUD = (70, 74, 110); CLOUD2 = (92, 96, 136)
WHITE = (255, 250, 225)
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
def zig(x0, y0, x1, y1, n, amp, seed):
    """Deterministic jagged path for a bolt."""
    rng = random.Random(seed); pts = [(x0, y0)]
    for k in range(1, n):
        u = k / n; pts.append((x0 + (x1 - x0) * u + rng.uniform(-amp, amp), y0 + (y1 - y0) * u + rng.uniform(-amp * .3, amp * .3)))
    pts.append((x1, y1)); return pts

def bolt(c, pts, a, w=10, bg=BG):
    """A lightning bolt: soft wide glow, bright yellow core, white-hot centre."""
    if a <= .01: return
    c.line(pts, mix(LIGHT, .35), w * 4, a, bg=bg)
    c.line(pts, LIGHT, w, a, bg=bg)
    c.line(pts, WHITE, max(2, w * .4), a, bg=bg)

def cloud(c, x, y, s, a, bg=BG):
    if a <= .01: return
    for dx, dy, r in ((-150, 20, 80), (-60, -30, 110), (60, -10, 100), (160, 25, 75), (0, 40, 90)):
        c.circ(x + dx * s, y + dy * s, r * s, CLOUD, a, bg=bg)
    for dx, dy, r in ((-60, -45, 70), (60, -25, 60)):
        c.circ(x + dx * s, y + dy * s, r * s, CLOUD2, a, bg=CLOUD)

def person(c, x, y, s, a, col=YOU, bg=BG):
    if a <= .01: return
    c.circ(x, y - 58 * s, 24 * s, col, a, bg=bg)
    c.rr(x - 30 * s, y - 28 * s, x + 30 * s, y + 50 * s, 18 * s, col, a, bg=bg)

def bubble(c, x, y, txt, a, col=INK, size=64):
    if a <= .01: return
    w = max(110, c.tw(txt, size, 'Bold') + 60)
    c.rr(x - w / 2, y - 55, x + w / 2, y + 55, 30, CARD, a, outline=col, ow=4)
    c.text(x, y, txt, size, col, a, w='Bold', bg=CARD)

def rings(c, x, y, a, t, rmax=520, speed=170, n=4, col=SOUND, ow=5):
    """Sound spreading out as rings."""
    if a <= .01: return
    for k in range(n):
        r = (t * speed + k * rmax / n) % rmax
        c.circ(x, y, r, None, a * (1 - r / rmax), outline=col, ow=ow)

def ground(c, y=770, h=100):
    c.rr(0, y, 1920, y + h, 0, GROUND, 1)

def sun(c, x, y, r, a, bg=BG):
    if a <= .01: return
    for k in range(10):
        ang = k * 6.283 / 10
        c.line([(x + r * 1.2 * math.cos(ang), y + r * 1.2 * math.sin(ang)), (x + r * 1.55 * math.cos(ang), y + r * 1.55 * math.sin(ang))], (255, 170, 60), 6, a, bg=bg)
    c.circ(x, y, r, (255, 170, 60), a, bg=bg)

def wave(c, x0, x1, y, amp, a, col=SOUND, cyc=8, ph=0.0, env=None, w=5):
    """A sound wave drawn as a line; env(u) shapes its loudness along the line."""
    if a <= .01: return
    pts = []
    for k in range(121):
        u = k / 120; e = env(u) if env else 1.0
        pts.append((x0 + (x1 - x0) * u, y - amp * e * math.sin(u * cyc * 6.283 + ph)))
    c.line(pts, col, w, a)

def flash_env(T, i, at=0.0):
    """Bolt brightness: a quick flash, then it stays drawn but dimmer."""
    if T(i) < at - .05: return 0.0
    e = T(i) - at
    return clamp(.55 + .45 * math.exp(-e * 3)) * fd(e, 0, .08)

BOLT_HOOK = zig(380, 420, 420, 770, 7, 45, 3)
BOLT_BIG = zig(960, 250, 960, 800, 10, 55, 11)
BOLT_LONG = zig(330, 290, 1250, 360, 12, 30, 17)
BRANCH = [zig(560, 300, 640, 470, 4, 20, 23), zig(900, 330, 980, 520, 4, 20, 29), zig(1120, 350, 1160, 500, 3, 18, 31)]

# ---------- scenes ----------
def s_hook(c, T, t):
    """Frame one: storm, bolt and a listener already counting; then the distance appears."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Count after the ', INK), ('flash', LIGHT)], sw_out(T, 1))
    headline(c, [('One. Two. Three. ', INK), ('Boom', SOUND)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('3 seconds', SOUND), (' = about ', INK), ('1 km', DIST)], sw_in(T, 2))
    cloud(c, 400, 390, 1.2, 1)
    ground(c)
    bolt(c, BOLT_HOOK, max(.55, flash_env(T, 0)), 10)
    person(c, 1500, 720, 1.3, 1)
    # the count: 1, 2, 3 during line 1, then BOOM
    n = 0
    if T(1) > 0: n = min(3, 1 + int(T(1) / .45))
    lab = str(n) if n else '...'
    if T(1) > 1.3: lab = 'BOOM'
    bubble(c, 1500, 470, lab, 1, SOUND if lab == 'BOOM' else INK)
    if T(1) > 1.2: rings(c, 1500, 640, sw_out(T, 2) * .8, t, 260, 220, 3)
    m2 = hl(2)
    if m2 > .01:
        c.line([(420, 820), (1500, 820)], DIST, 6, m2)
        for x in (420, 1500): c.line([(x, 800), (x, 840)], DIST, 6, m2)
        c.text(960, 800, 'about 1 km', 44, DIST, m2, w='Bold', bg=GROUND)

def s_heat(c, T, t):
    """The bolt and a thermometer that shoots up to about 30,000 °C, five Suns, a few millionths of a second."""
    hl = lambda i: hl_(T, i)
    headline(c, [('What is ', INK), ('thunder', SOUND), ('?', INK)], sw_out(T, 1))
    headline(c, [('Air at about ', INK), ('30,000 °C', HEAT)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('In a few ', INK), ('millionths', HEAT), (' of a second', INK)], sw_in(T, 2), size=78)
    cloud(c, 560, 380, 1.0, 1)
    pts = zig(560, 410, 580, 830, 8, 40, 5)
    bolt(c, pts, .6 + .4 * hl(1), 9 + 8 * hl(1))
    # heat glow around the bolt
    if hl(1) > .01:
        for k in range(4): c.line(pts, mix(HEAT, .25), 40 + k * 18, hl(1) * .25)
        bolt(c, pts, 1, 12)
    # thermometer
    x0, y0, y1 = 1120, 300, 760
    c.rr(x0 - 30, y0, x0 + 30, y1, 30, CARD, 1, outline=DIM, ow=4)
    c.circ(x0, y1 + 20, 50, HEAT, 1)
    lvl = fd(T(1), 0, 1.0) if T(1) > -.1 else .05
    c.rr(x0 - 16, y1 - (y1 - y0 - 20) * max(.05, lvl), x0 + 16, y1 + 10, 16, HEAT, 1, bg=CARD)
    c.text(x0 + 70, y0 + 30, '30,000 °C', 58, HEAT, hl(1), 'lm', 'Bold')
    m = fd(T(1), 1.6) if T(1) > -.1 else 0
    if m > .01:
        c.text(x0 + 70, 470, 'about 5x the', 40, INK, m, 'lm', 'Medium')
        c.text(x0 + 70, 520, "Sun's surface", 40, INK, m, 'lm', 'Medium')
        for k in range(5): sun(c, x0 + 110 + k * 95, 610, 26, m)
    m2 = hl(2)
    if m2 > .01:
        c.rr(1150, 690, 1800, 790, 30, CARD, m2, outline=HEAT, ow=4)
        c.text(1475, 740, 'a few millionths of a second', 36, INK, m2, w='Bold', bg=CARD)

def s_boom(c, T, t):
    """Squeezed air in the bolt's path, then a ring blast that turns into ordinary sound waves."""
    hl = lambda i: hl_(T, i)
    headline(c, [('No time to ', INK), ('move', HEAT)], sw_out(T, 1))
    headline(c, [('Then it ', INK), ('bursts', HEAT), (' outward', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('That blast is ', INK), ('thunder', SOUND)], sw_in(T, 2))
    x = 960
    m0 = 1 - hl(1)
    # air particles crowded into the channel (pink), with tiny arrows pressing in
    for k in range(9):
        y = 300 + k * 60
        for side in (-1, 1):
            dx = side * (40 + 260 * hl(1) * (1 + .3 * math.sin(k)))
            c.circ(x + dx, y, 14, HEAT if m0 > .5 else SOUND, 1 - hl(2))
    if m0 > .01:
        c.rr(x - 26, 270, x + 26, 820, 26, mix(HEAT, .4), m0)
        c.text(x + 300, 420, 'squeezed', 52, HEAT, m0, 'lm', 'Bold')
        c.text(x + 300, 480, 'to huge pressure', 40, INK, m0, 'lm', 'Medium')
    bolt(c, zig(x, 250, x, 840, 10, 30, 41), .9 * m0 + .2, 8)
    m1 = hl(1) * (1 - hl(2))
    if m1 > .01:
        rings(c, x, 540, m1, t, 700, 420, 5, HEAT, 8)
        c.text(x - 520, 500, 'like a balloon', 44, INK, m1, w='Bold')
        c.text(x - 520, 555, 'popping', 44, INK, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        wave(c, 1060, 1800, 540, 60, m2, SOUND, 6, -t * 6)
        wave(c, 120, 860, 540, 60, m2, SOUND, 6, t * 6)
        c.text(1430, 650, 'ordinary sound', 40, SOUND, m2, w='Bold')
        c.rr(x - 240, 700, x + 240, 780, 30, CARD, m2, outline=HEAT, ow=4)
        c.text(x, 740, 'shock wave: first ~10 m', 34, HEAT, m2, w='Bold', bg=CARD)

def s_race(c, T, t):
    """A race from the storm to you: the light dot arrives at once, the sound dot crawls. Then fireworks."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Same start, ', INK), ('different speeds', DIST)], sw_out(T, 1))
    headline(c, [('Light', LIGHT), (': almost instant', INK)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Sound', SOUND), (': a third of a km a second', INK)], sw_in(T, 2), size=70)
    m01 = 1 - hl(2)
    if m01 > .01:
        cloud(c, 260, 330, .8, m01)
        bolt(c, zig(260, 360, 280, 640, 6, 25, 7), m01 * .8, 7)
        person(c, 1680, 640, 1.0, m01)
        for lane, (col, lab, sp) in enumerate(((LIGHT, 'light: about 300,000 km every second', 40.0), (SOUND, 'sound: about 0.34 km every second', .18))):
            y = 470 + lane * 150
            c.line([(330, y), (1600, y)], DARK, 26, m01)
            start = T(1) if lane == 0 else T(0)
            u = clamp(max(0, start) * sp) if start > -.1 else 0
            if lane == 1: u = clamp(max(0, T(0)) * .025)
            c.line([(330, y), (330 + 1270 * u, y)], col, 26, m01 * (hl(1) if lane == 0 else 1))
            c.circ(330 + 1270 * u, y, 26, col, m01 * (hl(1) if lane == 0 else 1))
            c.text(330, y - 50, lab, 34, col, m01 * (hl(1) if lane == 0 else hl(0)), 'lm', 'Bold')
        c.text(960, 780, 'not to scale: light is close to a million times faster', 30, DIM, hl(1) * m01, w='Regular')
    m2 = hl(2)
    if m2 > .01:   # fireworks far away: see it, then hear it
        bx, by = 520, 420
        for k in range(14):
            ang = k * 6.283 / 14; r = 150 * fd(T(2), .4, .6)
            c.line([(bx + r * .3 * math.cos(ang), by + r * .3 * math.sin(ang)), (bx + r * math.cos(ang), by + r * math.sin(ang))], (LIGHT, HEAT, SOUND)[k % 3], 8, m2)
        person(c, 1450, 700, 1.0, m2)
        c.text(520, 680, '1. you see it', 46, LIGHT, m2, w='Bold')
        u = fd(T(2), 2.2)
        c.text(1450, 470, '2. then hear it', 46, SOUND, m2 * u, w='Bold')
        rings(c, 520, 420, m2 * u, t, 230, 160, 3)

def s_quiz(c, T, t):
    """Mid-video question with a countdown, on a violet pattern-interrupt background."""
    c.rr(0, 120, 1920, 900, 0, QUIZ, 1)
    headline(c, [('Flash, then ', INK), ('9 seconds', SOUND), (': how far?', INK)], 1, bg=QUIZ, size=72)
    for k, txt in enumerate(('A   About 3 km', 'B   About 9 km')):
        u = fd(t, .8 + .3 * k)
        c.rr(260, 360 + k * 200, 1100, 500 + k * 200, 26, (78, 52, 118), u, outline=(150, 120, 200), ow=3, bg=QUIZ)
        c.text(310, 430 + k * 200, txt, 58, INK, u, 'lm', 'Bold', bg=(78, 52, 118))
    cloud(c, 1480, 380, .7, fd(t, .5), bg=QUIZ)
    bolt(c, zig(1480, 410, 1500, 600, 5, 20, 13), fd(t, .5), 6, bg=QUIZ)
    if T(0) > 0:
        e = T(0) - QZ; k = max(0, 3 - int(max(0, e) / 1.0)) if e > 0 else 3
        u = fd(T(0), QZ - .3)
        c.circ(1500, 740, 80, LIGHT, u, bg=QUIZ); c.text(1500, 740, str(k) if k else '?', 76, DARK, u, w='Bold', bg=LIGHT)

def s_rule(c, T, t):
    """The rule as one big equation, then a ruler with the worked examples."""
    hl = lambda i: hl_(T, i)
    headline(c, [("It's ", INK), ('A: about 3 km', YOU)], sw_out(T, 1))
    headline(c, [('Seconds ', SOUND), ('÷ 3', INK), (' = km', DIST)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('In miles: ', INK), ('÷ 5', LIGHT)], sw_in(T, 2))
    m0 = 1 - hl(1)
    if m0 > .01:
        c.rr(560, 320, 1360, 620, 40, CARD, m0, outline=YOU, ow=5)
        c.text(960, 420, '9 seconds', 70, SOUND, m0, w='Bold', bg=CARD)
        c.text(960, 530, '= about 3 km', 80, YOU, m0, w='Bold', bg=CARD)
    m1 = hl(1)
    if m1 > .01:
        c.text(960, 380, 'about 3 seconds per kilometre', 54, INK, m1, w='Bold')
        # ruler: 0 to 5 km, a flash at each 3-second mark
        x0, x1, y = 260, 1660, 600
        c.line([(x0, y), (x1, y)], DIST, 8, m1)
        for k in range(6):
            x = x0 + (x1 - x0) * k / 5; u = fd(T(1), .3 + .25 * k)
            c.line([(x, y - 26), (x, y + 26)], DIST, 6, m1)
            c.text(x, y + 70, f'{k} km', 38, DIST, m1 * u, w='Bold')
            if k: c.text(x, y - 70, f'{3 * k} s', 38, SOUND, m1 * u, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        c.rr(360, 740, 1560, 850, 30, CARD, m2, outline=LIGHT, ow=4)
        c.text(960, 795, '3 s = 1 km      15 s = 5 km      5 s = 1 mile', 44, INK, m2, w='Bold', bg=CARD)

def s_rumble(c, T, t):
    """A long branched bolt; lines of different length from its parts to the listener; a crack vs a rumble."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Crack', LIGHT), (' or ', INK), ('rumble', SOUND), ('?', INK)], sw_out(T, 1))
    headline(c, [('Some parts are ', INK), ('closer', YOU)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Near first, ', YOU), ('far later', DIST)], sw_in(T, 2))
    bolt(c, BOLT_LONG, .9, 8)
    for b in BRANCH: bolt(c, b, .7, 5)
    px, py = 1600, 640
    person(c, px, py, 1.0, 1)
    m1 = hl(1)
    if m1 > .01:
        for k, (x, y) in enumerate((BOLT_LONG[-1], BOLT_LONG[6], BOLT_LONG[1])):
            col = (YOU, SOUND, DIST)[k]
            c.line([(x, y), (px - 20, py - 60)], col, 4, m1 * fd(T(1), .3 * k))
            c.circ(x, y, 14, col, m1 * fd(T(1), .3 * k))
        c.text(1300, 470, 'near', 36, YOU, m1, w='Bold')
    m2 = hl(2)
    if m2 > .01:
        # crack: a short sharp spike; rumble: a long smeared wave
        c.text(380, 690, 'close: a sharp crack', 36, LIGHT, m2, w='Bold')
        wave(c, 160, 600, 770, 70, m2, LIGHT, 3, 0, env=lambda u: math.exp(-((u - .2) / .06) ** 2))
        c.text(1100, 690, 'far: a long rumble', 36, SOUND, m2, w='Bold')
        wave(c, 760, 1440, 770, 40, m2, SOUND, 14, t * 3, env=lambda u: .5 + .5 * math.sin(u * 3.14) * (.7 + .3 * math.sin(u * 19)))

def s_far(c, T, t):
    """Distance rings around a storm: usually heard to about 15 km, up to about 25 km on a still night."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Heard up to about ', INK), ('15 km', SOUND)], sw_out(T, 1))
    headline(c, [('Hear it? ', INK), ("You're in reach", HEAT)], sw_in(T, 1))
    cx, cy = 600, 580
    m0 = hl(0)
    c.circ(cx, cy, 280, None, m0 * .9, outline=DIST, ow=4)
    c.circ(cx, cy, 170, mix(SOUND, .18), 1, outline=SOUND, ow=5)
    c.text(cx, cy - 195, '~15 km: usually', 34, SOUND, 1, w='Bold')
    c.text(cx, cy - 305, '~25 km: on a still night', 34, DIST, m0, w='Bold')
    cloud(c, cx, cy - 10, .55, 1, bg=mix(SOUND, .18))
    bolt(c, zig(cx, cy + 10, cx + 10, cy + 120, 4, 14, 19), .9, 5, bg=mix(SOUND, .18))
    person(c, cx + 140, cy + 110, .6, 1, bg=mix(SOUND, .18))
    m1 = hl(1)
    if m1 > .01:
        c.rr(1100, 400, 1800, 680, 30, CARD, m1, outline=HEAT, ow=4)
        c.text(1450, 470, 'weather services:', 38, DIM, m1, w='Medium', bg=CARD)
        c.text(1450, 550, 'if you can hear thunder,', 42, INK, m1, w='Bold', bg=CARD)
        c.text(1450, 610, 'you can be struck', 42, HEAT, m1, w='Bold', bg=CARD)

def s_safe(c, T, t):
    """A house: the listener walks in, a 30-minute clock runs after the last rumble."""
    hl = lambda i: hl_(T, i)
    headline(c, [('The rule to ', INK), ('really', YOU), (' keep', INK)], sw_out(T, 1))
    headline(c, [('Thunder roars? ', SOUND), ('Go indoors', YOU)], sw_in(T, 1) * sw_out(T, 2))
    headline(c, [('Wait ', INK), ('30 minutes', YOU), (' after it ends', INK)], sw_in(T, 2), size=78)
    hx, hy = 760, 560
    c.rr(hx - 200, hy - 120, hx + 200, hy + 210, 10, (70, 80, 130), 1)
    for k in range(4):
        w = 240 - 50 * k
        c.rr(hx - w, hy - 140 - 45 * k, hx + w, hy - 100 - 45 * k, 8, (120, 90, 170), 1)
    c.rr(hx - 50, hy + 50, hx + 50, hy + 210, 8, DARK, 1, bg=(70, 80, 130))
    c.rr(hx + 90, hy - 60, hx + 170, hy + 10, 6, LIGHT, 1, bg=(70, 80, 130))
    u = fd(T(1), .2, 1.5) if T(1) > -.1 else 0
    px = 1400 - 640 * u
    person(c, px, hy + 160, 1.0, 1 - fd(T(1), 1.4, .4) if T(1) > -.1 else 1)
    cloud(c, 1600, 420, .7, 1)
    rings(c, 1600, 440, .6 * (1 - hl(2)), t, 300, 160, 3)
    m2 = hl(2)
    if m2 > .01:
        cx, cy = 1500, 680
        c.circ(cx, cy, 120, CARD, m2, outline=YOU, ow=6)
        p = fd(T(2), .3, 2.5)
        for k in range(int(30 * p) + 1):
            ang = -1.571 + k / 60 * 6.283
            c.line([(cx + 95 * math.cos(ang), cy + 95 * math.sin(ang)), (cx + 110 * math.cos(ang), cy + 110 * math.sin(ang))], YOU, 6, m2, bg=CARD)
        c.text(cx, cy, '30 min', 48, YOU, m2, w='Bold', bg=CARD)

def s_recap(c, T, t):
    """Recap as three stops along a ruler from the flash to you."""
    hl = lambda i: hl_(T, i)
    headline(c, [('Three things ', INK), ('to keep', LIGHT)], 1)
    items = ((1, 'super-heated air bursts outward', 'that blast is thunder', HEAT),
             (2, 'light is instant, sound is slow', 'about 3 seconds per kilometre', SOUND),
             (3, 'if you can hear thunder', 'go indoors', YOU))
    for ln, l1, l2, col in items:
        m = hl(ln); y = 330 + (ln - 1) * 170; dx = 60 * (1 - m)
        bolt(c, zig(390 + dx, y - 40, 400 + dx, y + 50, 3, 12, ln), .3 + .7 * m, 6)
        c.text(490 + dx, y, str(ln) + '.  ' + l1, 54, col, .25 + .75 * m, 'lm', 'Bold')
        c.text(570 + dx, y + 58, l2, 36, DIM, m, 'lm', 'Medium')
    c.text(960, 860, 'Short Story Long Thinking', 52, CY, hl(4), w='Bold')

def thumb_art(c):
    """Cloud and one big bolt in the right third, kept out of the bottom-right corner (YouTube's duration badge)."""
    cloud(c, 1500, 230, 1.15, 1)
    bolt(c, zig(1480, 270, 1440, 720, 8, 60, 3), 1, 18)
    for k in range(3):
        c.circ(1440, 700, 70 + k * 70, None, 1 - k * .28, outline=CY, ow=8)

SCENES = [
 ('THE COUNT', ["Next time you see lightning, start counting.",
                "One. Two. Three. Boom.",
                "Three seconds means the strike was about one kilometre away. Here's why that works."], s_hook),
 ('THE HEAT', ["First, what actually is thunder?",
               "A lightning bolt heats the air around it to about thirty thousand degrees Celsius. That's about five times hotter than the surface of the Sun.",
               "And it does it in a few millionths of a second."], s_heat),
 ('THE BOOM', ["The air has no time to move out of the way, so it's left squeezed to a huge pressure.",
               "Then it bursts outward, like a balloon popping, all along the bolt.",
               "For about the first ten metres it's a shock wave. Then it settles into ordinary sound. That's thunder."], s_boom),
 ('THE RACE', ["The flash and the bang start at the same moment. But they travel at very different speeds.",
               "Light covers about three hundred thousand kilometres every second. It reaches you almost instantly.",
               "Sound covers only about a third of a kilometre each second. It's like fireworks far away. You see the burst, then you hear the bang."], s_race),
 ('QUICK QUESTION', ["Quick question. You see a flash and count nine seconds before the thunder. Is it about three kilometres away, or nine?"], s_quiz),
 ('THE RULE', ["It's about three kilometres.",
               "Sound takes about three seconds to travel one kilometre. So count the seconds, and divide by three.",
               "In miles, divide by five instead. Three seconds is one kilometre. Fifteen seconds is five kilometres."], s_rule),
 ('THE RUMBLE', ["So why does thunder sometimes crack, and sometimes rumble?",
                 "A bolt is long and branched. Every part of it makes sound, but some parts are closer to you than others.",
                 "Sound from the near part arrives first, and from the far parts later, so it smears into a rumble. A sharp crack means it was close."], s_rumble),
 ('HOW FAR', ["You can usually hear thunder up to about fifteen kilometres away. On a still night, sometimes up to twenty-five.",
              "And weather services warn that if you can hear thunder, you're close enough to be struck by lightning."], s_far),
 ('STAY SAFE', ["So counting is fun. But the rule to really keep is simpler.",
                "When thunder roars, go indoors.",
                "Then wait thirty minutes after the last rumble before you head back out."], s_safe),
 ('RECAP', ["Three things to keep.",
            "One: lightning heats the air so fast that it bursts outward. That blast is thunder.",
            "Two: light reaches you almost instantly, but sound takes about three seconds per kilometre.",
            "Three: if you can hear thunder, go indoors.",
            "Subscribe to Short Story Long Thinking for more."], s_recap),
]

# ---------- the Short: its own complete mini-story (question, answer in the first seconds, why, rule) ----------
def short_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    headline(c, [('How far is ', INK), ('that lightning', LIGHT), ('?', INK)], sw_out(T, 1), size=80)
    headline(c, [('Seconds ', SOUND), ('÷ 3', INK), (' = km', DIST)], sw_in(T, 1), size=88)
    cloud(c, 400, 390, 1.2, 1)
    ground(c)
    bolt(c, BOLT_HOOK, max(.6, flash_env(T, 0)), 10)
    person(c, 1500, 720, 1.3, 1)
    n = min(3, 1 + int(max(0, T(1)) / .9)) if T(1) > 0 else 0
    bubble(c, 1500, 470, str(n) if n else '...', 1)

def short_heat(c, T, t):
    s_heat(c, lambda i: (T(0) if i == 1 else (T(0) - 4.0 if i == 2 else T(0) + 3)) if i <= 2 else -99, t)

def short_boom(c, T, t):
    s_boom(c, lambda i: T(0) + 3 if i <= 1 else (T(0) - 1.6 if i == 2 else -99), t)

def short_race(c, T, t):
    s_race(c, lambda i: T(0) + 4 if i == 0 else (T(0) if i == 1 else (T(1) if i == 2 else -99)), t)

def short_rule(c, T, t):
    s_rule(c, lambda i: T(0) + 3 if i <= 1 else -99, t)

SHORT_SCENES = [
 ('THE COUNT', ["How far away is that lightning?",
                "Count the seconds until the thunder, then divide by three. That's roughly the distance in kilometres."], short_hook),
 ('THE HEAT', ["Here's why. Lightning heats the air to about thirty thousand degrees Celsius in a few millionths of a second."], short_heat),
 ('THE BOOM', ["That air bursts outward, and the blast becomes the sound we call thunder."], short_boom),
 ('THE RACE', ["The flash reaches you almost instantly.",
               "But sound is slow. It covers only about a third of a kilometre each second."], short_race),
 ('THE RULE', ["So every three seconds of counting is about one kilometre. Nine seconds means about three kilometres."], short_rule),
 ('SO', ["So: count the seconds, and divide by three.",
         "And if you can hear thunder at all, go indoors."], card('Count. Divide by 3.', 'Hear thunder? Go indoors.')),
]
SHORT_HITS = [(5, 1, 0.0)]
