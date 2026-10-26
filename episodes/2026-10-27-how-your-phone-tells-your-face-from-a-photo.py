"""Episode: How Your Phone Tells Your Face From a Photo (2D face unlock vs 3D depth sensing)"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pipeline'))
from engine import *

SHORT_TITLE = "Looks vs Measures"                         # shown top-right on every frame
VOICE, SPEED = 'am_michael', 0.92                         # about 158 wpm while speaking (lesson of 2026-10-22)
SHORT_HOOK = "Why can a photo fool some phones?"          # headline on the vertical Short
HITS = [(0, 4, 0.0), (5, 3, 0.0), (6, 2, 0.0)]            # title card, quiz answer, one-in-a-million
THUMB = ['YOUR FACE', 'OR A PHOTO?', '30,000 DOTS']
MUSIC_LEVEL = 0.006                                        # music about 20 dB under the voice (lesson of 2026-10-14)
LEAD_IN = 0.15                                             # no dead air before the first word (lesson of 2026-10-19)
PAUSES = {(0, 1): 0.4, (0, 3): 0.5, (5, 3): 0.6, (6, 2): 0.5}
SHORT_PAUSES = {(0, 1): 0.3}
CAPTION_FIXES = {'nineteen of forty-eight': '19 of 48', 'thirty thousand': '30,000', 'one in a million': '1 in a million',
                 'one in fifty thousand': '1 in 50,000', 'under thirteen': 'under 13', 'six digits': '6 digits',
                 'twenty twenty-three': '2023'}

IR = (255, 80, 120); SKIN = (225, 180, 150); PAPER = (236, 232, 220); NEAR = (255, 220, 90); FAR = (50, 70, 170)
PHONE = (34, 40, 74)

# ---------------------------------------------------------------- drawing helpers
hl_ = lambda T, i: fd(T(i)) if T(i) > -.1 else 0.0

def ell(c, x, y, rx, ry, fill=None, a=1.0, outline=None, ow=3, bg=BG):
    if a <= .01: return
    c.d.ellipse(((x - rx) * c.k, (y - ry) * c.k, (x + rx) * c.k, (y + ry) * c.k),
                fill=mix(fill, a, bg) if fill else None, outline=mix(outline, a, bg) if outline else None, width=int(ow * c.k))

def face(c, x, y, s, a=1.0, skin=SKIN, bg=BG, line=(60, 40, 40), eyes_open=1.0, beard=0.0):
    """Simple front-view face; s = half-height of the head."""
    if a <= .01: return
    ell(c, x, y, s * .78, s, skin, a, bg=bg)
    if beard > 0:
        bc = mix((95, 62, 40), .9 * beard, skin)
        ell(c, x, y + s * .5, s * .7, s * .48, bc, a, bg=skin)
        ell(c, x, y + s * .12, s * .74, s * .4, skin, a, bg=skin)
        ell(c, x, y + s * .5, s * .26, s * .12, skin, a * (1 - .6 * beard), bg=bc)
    for sx in (-1, 1):
        ex = x + sx * s * .32; ey = y - s * .18
        if eyes_open > .5:
            ell(c, ex, ey, s * .14, s * .08 * eyes_open, (250, 250, 250), a, bg=skin)
            c.circ(ex, ey, s * .06, (60, 90, 140), a, bg=(250, 250, 250))
        else:
            c.line([(ex - s * .13, ey), (ex + s * .13, ey)], line, max(2, s * .03), a, skin)
        c.line([(ex - s * .16, ey - s * .17), (ex + s * .14, ey - s * .2)], line, max(2, s * .035), a, skin)
    c.line([(x, y - s * .1), (x - s * .08, y + s * .2), (x + s * .04, y + s * .22)], line, max(2, s * .03), a, skin)
    c.line([(x - s * .22, y + s * .48), (x, y + s * .54), (x + s * .22, y + s * .48)], line, max(2, s * .035), a, skin)

def phone(c, x, y, h, a=1.0, screen=(18, 22, 44), bg=BG):
    """Upright phone centred at (x, y), height h. Returns the screen box."""
    if a <= .01: return (0, 0, 0, 0)
    w = h * .5
    c.rr(x - w / 2, y - h / 2, x + w / 2, y + h / 2, h * .08, PHONE, a, outline=(90, 100, 150), ow=3, bg=bg)
    c.rr(x - w / 2 + h * .03, y - h / 2 + h * .03, x + w / 2 - h * .03, y + h / 2 - h * .03, h * .06, screen, a, bg=PHONE)
    c.rr(x - w * .2, y - h / 2 + h * .045, x + w * .2, y - h / 2 + h * .085, h * .02, (8, 10, 20), a, bg=screen)
    return (x - w / 2 + h * .03, y - h / 2 + h * .03, x + w / 2 - h * .03, y + h / 2 - h * .03)

def lock(c, x, y, s, open_=0.0, col=INK, a=1.0, bg=BG):
    if a <= .01: return
    lift = s * .3 * clamp(open_)
    arc = [(x + s * .3 * math.cos(math.pi + math.pi * u / 16), y - s * .35 - lift + s * .3 * math.sin(math.pi + math.pi * u / 16)) for u in range(17)]
    c.line([(x - s * .3, y - s * .05 - lift)] + arc + [(x + s * .3, y - s * .05)], col, s * .1, a, bg)
    c.rr(x - s * .45, y - s * .08, x + s * .45, y + s * .5, s * .1, col, a, bg=bg)

def depthf(u, v):
    """Illustrative depth of a face at normalised (u, v): 0 = flat background, ~1 = nose tip."""
    r2 = u * u + v * v
    if r2 >= 1: return 0.0
    dome = math.sqrt(1 - r2) * .55
    nose = .45 * math.exp(-(u / .13) ** 2 - ((v - .02) / .22) ** 2)
    eyes = -.22 * math.exp(-((abs(u) - .4) / .15) ** 2 - ((v + .18) / .1) ** 2)
    return max(0.0, dome + nose + eyes)

def depth_col(d):
    d = clamp(d)
    return tuple(int(FAR[i] + (NEAR[i] - FAR[i]) * d) for i in range(3))

def dots(c, x, y, rx, ry, p, a=1.0, dfun=None, step=26, shift=34, col=IR, bg=BG, r=4.5):
    """Grid of IR dots over a box; each dot slides sideways by its depth (p = 0..1 of the shift)."""
    if a <= .01: return
    nx, ny = int(2 * rx / step), int(2 * ry / step)
    for i in range(nx + 1):
        for j in range(ny + 1):
            px = x - rx + i * step; py = y - ry + j * step
            d = dfun((px - x) / (rx * .82), (py - y) / ry) if dfun else 0.0
            c.circ(px + d * shift * p, py, r, col, a * (.55 + .45 * d), bg=bg)

def depth_map(c, x, y, rx, ry, a=1.0, cell=12, p=1.0, bg=BG):
    """Heat-map style picture of depthf: blue = far, yellow = near. p wipes it in from the top."""
    if a <= .01: return
    ymax = y - ry + 2 * ry * clamp(p)
    yy = y - ry
    while yy < min(ymax, y + ry):
        xx = x - rx
        while xx < x + rx:
            d = depthf((xx + cell / 2 - x) / (rx * .82), (yy + cell / 2 - y) / ry)
            if d > 0:
                c.d.rectangle((xx * c.k, yy * c.k, (xx + cell) * c.k + 1, (yy + cell) * c.k + 1), fill=mix(depth_col(d), a, bg))
            xx += cell
        yy += cell

def ring(c, x, y, r, p, col, a=1.0, w=10):
    pts = [(x + r * math.sin(2 * math.pi * u / 60), y - r * math.cos(2 * math.pi * u / 60)) for u in range(int(60 * clamp(p)) + 1)]
    c.line(pts, col, w, a)

def photo(c, x, y, s, a=1.0, bg=BG, tilt=0.0):
    """A printed photo of the face: white border, flat picture."""
    if a <= .01: return
    c.rr(x - s * .95, y - s * 1.2, x + s * .95, y + s * 1.2, 8, PAPER, a, bg=bg)
    c.rr(x - s * .82, y - s * 1.07, x + s * .82, y + s * 1.07, 4, (120, 150, 190), a, bg=PAPER)
    face(c, x, y + s * .05, s * .85, a, bg=(120, 150, 190))

def thumb_art(c):
    face(c, 1500, 560, 330, 1.0)
    dots(c, 1500, 560, 300, 360, 1.0, 1.0, depthf, step=34, shift=40, bg=SKIN, r=6)
    c.text(1500, 960, '?', 150, YE, 1, w='Bold', stroke=8)

# ---------------------------------------------------------------- scenes
def s_hook(c, T, t):
    hl = lambda i: hl_(T, i)
    a = 1 - fd(T(4), 0.0, .5)
    if a > 0:
        n1 = max(hl(1), hl(2), hl(3)); n2 = max(hl(2), hl(3))
        c.text(960, 150, 'A printed photo can unlock some phones', 64, INK, a * (1 - n1), w='Bold')
        c.text(960, 150, 'In a 2023 test: 19 of 48 phones', 66, PK, a * hl(1) * (1 - n2), w='Bold')
        c.text(960, 150, 'Others can\'t be fooled that way', 66, GR, a * hl(2) * (1 - hl(3)), w='Bold')
        c.text(960, 150, 'One looks at your face. One measures it.', 62, YE, a * hl(3), w='Bold')
        k0 = a * (1 - n1)
        if k0 > 0:
            # motion from frame one: a photo slides toward the phone and the lock pops open
            px = 1240 - 300 * clamp(t / 1.2)
            sb = phone(c, 760, 500, 520, k0)
            ok = fd(t, 1.3, .4)
            lock(c, 760, 470, 110, ok, GR if ok > .5 else INK, k0, bg=(18, 22, 44))
            photo(c, px, 500, 130, k0, tilt=0)
            c.text(760, 790, 'unlocked', 40, GR, k0 * ok, w='Bold')
        k1 = a * hl(1) * (1 - n2)
        if k1 > 0:
            for i in range(48):
                col_, row = i % 12, i // 12
                x = 440 + col_ * 95; y = 330 + row * 120
                fooled = i < 19
                kk = k1 * fd(T(1), .02 * i, .3)
                c.rr(x - 28, y - 48, x + 28, y + 48, 10, PHONE, kk, outline=(PK if fooled else (80, 90, 140)), ow=3)
                if fooled: c.circ(x, y, 12, PK, kk * fd(T(1), 1.2 + .03 * i), bg=PHONE)
            c.text(960, 820, 'phones fooled by a printed photo (Which?, 2023)', 32, DIM, k1 * fd(T(1), .8), w='Medium')
        k2 = a * max(hl(2) * (1 - hl(3)), 0)
        if k2 > 0:
            phone(c, 760, 500, 520, k2)
            lock(c, 760, 470, 110, 0, INK, k2, bg=(18, 22, 44))
            photo(c, 1100, 500, 130, k2)
            c.cross(1100, 500, 160, PK, k2 * fd(T(2), .6))
            c.text(760, 790, 'still locked', 40, INK, k2 * fd(T(2), .8), w='Bold')
        k3 = a * hl(3)
        if k3 > 0:
            for j, (lab, x) in enumerate((('LOOKS', 560), ('MEASURES', 1360))):
                kk = k3 * fd(T(3), j * 1.3)
                face(c, x, 480, 170, kk)
                if j == 0:
                    c.rr(x - 210, 260, x + 210, 700, 20, None, kk, outline=CY, ow=5)
                else:
                    dots(c, x, 480, 150, 190, clamp((T(3) - 1.6) / 1.2), kk, depthf, step=30, shift=30, bg=SKIN)
                c.text(x, 780, lab, 56, CY if j == 0 else YE, kk, w='Bold')
    if T(4) > 0:
        m = fd(T(4), .2, .7)
        c.text(960, 340 + 30 * (1 - m), 'How Your Phone Tells', 112, INK, m, w='Bold')
        c.text(960, 480 + 30 * (1 - m), 'Your Face From a Photo', 112, YE, m, w='Bold')
        c.line([(960 - 320 * m, 590), (960 + 320 * m, 590)], CY, 8, m)

LMK = ((-61, -34), (61, -34), (-8, 38), (0, 100))
def s_flat(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Simple face unlock: compare two flat pictures', 58, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Like spotting a friend in a photo', 62, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'But a photo has all of that too', 64, PK, hl(2), w='Bold')
    k = hl(0)
    if k <= 0: return
    # left: live camera view, right: saved picture
    for j, (lab, x) in enumerate((('camera sees', 600), ('saved picture', 1320))):
        kk = k * fd(T(0), j * .8)
        c.rr(x - 230, 270, x + 230, 740, 24, CARD, kk, outline=(70, 80, 130), ow=3)
        if j == 0 and hl(2) > 0:
            photo(c, x, 500, 150, kk * hl(2), bg=CARD)
            face(c, x, 500, 190, kk * (1 - hl(2)), bg=CARD)
        else:
            face(c, x, 500, 190, kk, bg=CARD)
        c.text(x, 780, lab, 34, DIM, kk, w='Bold')
    # landmarks: eyes, nose, mouth
    lm = max(hl(1), hl(2))
    if lm > 0:
        for x in (600, 1320):
            ph_ = x == 600 and hl(2) > .5
            sc_, yc = (127 / 190, 507) if ph_ else (1.0, 500)
            for (dx, dy) in LMK:
                c.circ(x + dx * sc_, yc + dy * sc_, 13 * (.8 if ph_ else 1), CY, lm, bg=SKIN)
        for (dx, dy) in LMK:
            ph_ = hl(2) > .5; sc_, yc = (127 / 190, 507) if ph_ else (1.0, 500)
            c.line([(600 + dx * sc_ + 20, yc + dy * sc_), (1320 + dx - 20, 500 + dy)], CY, 3, lm * .55 * fd(T(1), .8))
        c.text(960, 300, 'eyes, nose, mouth', 34, CY, hl(1) * (1 - hl(2)), w='Bold')
    if hl(2) > 0:
        p = .7 + .3 * math.sin(t * 5)
        c.rr(820, 440, 1100, 560, 30, PK, hl(2) * fd(T(2), 1.0) * p)
        c.text(960, 500, 'MATCH?', 52, INK, hl(2) * fd(T(2), 1.0), w='Bold', bg=PK)

def s_light(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, '3D face unlock adds hidden parts', 64, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'A flood of infrared light', 66, IR, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'Invisible light, like a TV remote', 64, YE, hl(2), w='Bold')
    k = hl(0)
    if k <= 0: return
    dark = hl(1) * .8
    c.rr(90, 230, 1830, 800, 30, mix((6, 6, 14), dark, CARD), k)
    bgc = mix((6, 6, 14), dark, CARD)
    # phone top bar seen from the front, enlarged
    k0 = k * (1 - hl(2))
    if k0 > 0:
        c.rr(300, 300, 900, 420, 40, PHONE, k0, outline=(90, 100, 150), ow=3, bg=bgc)
        parts = [('infrared light', 380, IR), ('camera', 520, CY), ('dot projector', 700, YE)]
        for j, (lab, x, col) in enumerate(parts):
            kk = k0 * fd(T(0), .6 + j * .5)
            c.circ(x, 360, 24, (10, 12, 24), kk, outline=col, ow=4, bg=PHONE)
            c.text(x, 470 + (j % 2) * 50, lab, 30, col, kk, w='Bold', bg=bgc)
        c.text(600, 640, "e.g. the iPhone's Face ID", 36, DIM, k0 * fd(T(0), 2.0), w='Medium', bg=bgc)
        face(c, 1450, 520, 210, k0 * (1 - .75 * dark), bg=bgc)
        if hl(1) > 0:
            for q in range(5):
                ph = (t * .9 + q / 5) % 1.0
                x = 420 + ph * 820
                c.line([(x, 360 - 40 - ph * 80), (x, 360 + 40 + ph * 80)], IR, 6, k0 * hl(1) * (1 - ph) * .8, bgc)
            ell(c, 1450, 520, 170, 220, None, k0 * hl(1) * .9, outline=IR, ow=6, bg=bgc)
            c.text(1450, 780, 'works in the dark', 38, IR, k0 * fd(T(1), 1.2), w='Bold', bg=bgc)
    k2 = hl(2)
    if k2 > 0:
        # TV remote: a beam you can't see, a camera can
        c.rr(420, 420, 560, 760, 30, (50, 54, 80), k2, bg=bgc)
        for j in range(6):
            c.circ(460 + (j % 2) * 60, 560 + (j // 2) * 60, 16, (90, 96, 130), k2, bg=(50, 54, 80))
        c.circ(490, 450, 14, IR, k2 * (.5 + .5 * math.sin(t * 8)), bg=(50, 54, 80))
        for q in range(4):
            ph = (t * .8 + q / 4) % 1.0
            ell(c, 490 + ph * 600, 450 - ph * 60, 20 + 60 * ph, 30 + 80 * ph, None, k2 * (1 - ph) * .7, outline=IR, ow=4, bg=bgc)
        c.text(1350, 430, 'your eyes: nothing', 44, DIM, k2 * fd(T(2), .8), w='Bold', bg=bgc)
        c.text(1350, 520, 'a camera: bright light', 44, IR, k2 * fd(T(2), 1.6), w='Bold', bg=bgc)

def s_dots(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Then: more than 30,000 invisible dots', 62, YE, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'On a flat wall: neat rows', 64, INK, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'On a crumpled sheet: the dots shift', 64, IR, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        face(c, 1250, 510, 250, k0)
        p = clamp(T(0) / 2.0)
        c.rr(280, 450, 420, 570, 20, PHONE, k0, outline=(90, 100, 150))
        c.circ(390, 510, 16, (10, 12, 24), k0, outline=YE, ow=4, bg=PHONE)
        for q in range(9):
            ty = 270 + q * 60
            c.line([(400, 510), (400 + (1020 - 400) * p, 510 + (ty - 510) * p)], IR, 2, k0 * .5)
        dots(c, 1250, 510, 220, 270, 0.0, k0 * fd(T(0), 1.4), None, step=28, bg=SKIN)
        c.text(960, 800, 'drawn larger and fewer than the real dots', 28, DIM, k0, w='Medium')
    k1 = max(hl(1) * (1 - hl(2)), hl(2))
    if k1 > 0:
        # flat wall on the left, crumpled bedsheet on the right
        c.rr(150, 260, 900, 760, 20, (60, 64, 90), k1)
        dots(c, 525, 510, 340, 220, 0.0, k1, None, step=40, bg=(60, 64, 90), r=6)
        c.text(525, 795, 'flat wall', 36, INK, k1, w='Bold')
        ks = hl(2)
        if ks > 0:
            SH = (200, 205, 225)
            c.rr(1020, 260, 1770, 760, 20, SH, ks)
            for j in range(6):
                y = 300 + j * 80
                c.line([(1040 + x, y + 28 * math.sin(x / 60 + j)) for x in range(0, 711, 10)], (170, 175, 200), 5, ks, SH)
            bump = lambda u, v: .5 + .5 * math.sin(u * 5 + 1) * math.cos(v * 4)
            dots(c, 1395, 510, 340, 220, clamp(T(2) / 1.5), ks, bump, step=40, shift=40, bg=SH, r=6)
            c.text(1395, 795, 'crumpled bedsheet', 36, IR, ks, w='Bold')

def s_depth(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'A camera reads how far each dot moved', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Near or far: a depth map', 64, NEAR, hl(1), w='Bold')
    k = hl(0)
    if k <= 0: return
    # left: face with shifting dots
    face(c, 600, 510, 260, k)
    dots(c, 600, 510, 230, 280, .5 + .5 * math.sin(clamp(T(0) / 2.5) * math.pi / 2), k, depthf, step=28, shift=38, bg=SKIN)
    c.text(600, 835, 'infrared camera view', 30, DIM, k, w='Bold')
    k1 = hl(1)
    if k1 > 0:
        c.arrow(900, 510, 1040, 510, CY, 6, k1, 22)
        depth_map(c, 1340, 510, 220, 280, k1, 12, clamp(T(1) / 1.8))
        c.text(1650, 330, 'nose: near', 34, NEAR, k1 * fd(T(1), 1.6), 'lm', 'Bold')
        c.text(1650, 420, 'eyes: deeper', 34, (120, 140, 230), k1 * fd(T(1), 2.4), 'lm', 'Bold')
        for j in range(8):
            c.rr(1600 + j * 24, 700, 1622 + j * 24, 730, 4, depth_col(j / 7), k1)
        c.text(1600, 760, 'far', 26, DIM, k1, 'lm', 'Medium'); c.text(1790, 760, 'near', 26, DIM, k1, 'rm', 'Medium')
        c.text(1340, 820, 'simplified', 26, DIM, k1, w='Medium')

def s_quiz(c, T, t):
    hl = lambda i: hl_(T, i)
    m = hl(0); ans = hl(3)
    short = T(1) < -50 and T(2) < -50
    c.text(960, 140, 'Quick question', 64, YE, m * (1 - ans) * (0 if short else 1), w='Bold')
    c.text(960, 215, 'A sharp, life-size photo. What does the depth map show?', 42, INK, m * fd(T(0), .5) * (1 - ans) * (0 if short else 1), w='Bold')
    c.text(960, 140, 'A photo is flat' if short else 'B: a flat sheet', 64, GR, ans, w='Bold')
    k0 = m * (1 - hl(1)) * (1 - ans)
    if k0 > 0:
        photo(c, 960, 520, 190, k0)
        c.text(1300, 360, '?', 140, YE, k0 * (.7 + .3 * math.sin(t * 4)), w='Bold')
    kc = hl(1) * (1 - ans)
    if kc > 0:
        for j, (lab, l1, x) in enumerate((('A', 'a face shape', 560), ('B', 'a flat sheet', 1360))):
            kk = kc * (.3 + .7 * fd(T(1), j * 1.4))
            c.rr(x - 320, 300, x + 320, 700, 34, CARD, kk, outline=CY, ow=3)
            c.circ(x - 250, 360, 42, CY, kk, bg=CARD); c.text(x - 250, 360, lab, 48, BG, kk, w='Bold', bg=CY)
            if j == 0: depth_map(c, x + 30, 500, 110, 140, kk, 10, bg=CARD)
            else: c.rr(x - 60, 380, x + 120, 620, 6, FAR, kk, bg=CARD)
            c.text(x, 660, l1, 40, INK, kk, w='Bold', bg=CARD)
    if T(2) > 0 and ans < 1:
        ring(c, 960, 500, 70, 1 - clamp(T(2) / 2.0), YE, fd(T(2)) * (1 - ans))
    if ans > 0:
        photo(c, 560, 510, 170, ans)
        dots(c, 560, 510, 150, 200, 1.0, ans * fd(T(3), .4), None, step=28, bg=(120, 150, 190))
        c.text(560, 790, 'every dot: same depth', 34, IR, ans * fd(T(3), .8), w='Bold')
        c.arrow(800, 510, 960, 510, CY, 6, ans * fd(T(3), 1.2), 22)
        c.rr(1060, 300, 1400, 720, 8, FAR, ans * fd(T(3), 1.4))
        c.text(1230, 510, 'no nose', 40, INK, ans * fd(T(3), 1.8), w='Bold', bg=FAR)
        c.text(1230, 570, 'no eye sockets', 40, INK, ans * fd(T(3), 2.2), w='Bold', bg=FAR)
        c.rr(1460, 380, 1840, 640, 24, CARD, ans * fd(T(3), 3.0), outline=GR, ow=3)
        c.text(1650, 450, 'Apple: Face ID', 32, GR, ans * fd(T(3), 3.0), w='Bold', bg=CARD)
        c.text(1650, 510, 'always needs depth.', 32, INK, ans * fd(T(3), 3.0), w='Bold', bg=CARD)
        c.text(1650, 570, 'Photos have none.', 32, INK, ans * fd(T(3), 3.0), w='Bold', bg=CARD)

CODE = ['0.81', '0.12', '0.57', '0.33', '0.94', '0.46', '0.08', '0.71', '0.25', '0.63', '0.39', '0.88']
def s_match(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Your face becomes a code of numbers', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'It must fit the saved code, like a key', 62, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'A stranger: less than 1 in a million', 62, YE, hl(2), w='Bold')
    k = hl(0) * (1 - hl(2))
    if k > 0:
        depth_map(c, 330, 500, 150, 190, k, 10)
        c.arrow(520, 500, 640, 500, CY, 6, k * fd(T(0), .6), 22)
        for i, n in enumerate(CODE):
            x = 720 + (i % 4) * 120; y = 380 + (i // 4) * 100
            c.text(x, y, n, 44, NEAR, k * fd(T(0), 1.0 + .08 * i), w='Bold')
        c.text(900, 700, 'illustrative numbers', 28, DIM, k * fd(T(0), 1.5), w='Medium')
        kk = hl(1)
        if kk > 0:
            for i, n in enumerate(CODE):
                x = 1340 + (i % 4) * 120; y = 380 + (i // 4) * 100
                c.text(x, y, n, 44, GR, kk * fd(T(1), .05 * i), w='Bold')
            c.text(1520, 300, 'saved at setup', 32, DIM, kk, w='Bold')
            ok = fd(T(1), 2.2)
            c.check(1520, 700, 60, GR, kk * ok, ok)
            c.text(1205, 480, '=', 80, CY, kk * fd(T(1), 1.4), w='Bold')
    k2 = hl(2)
    if k2 > 0:
        for j, (lab, num, frac, col) in enumerate((('Face ID', 'under 1 in 1,000,000', 1 / 1000000, YE), ('Touch ID (fingerprint)', '1 in 50,000', 1 / 50000, CY))):
            y = 350 + j * 230
            c.rr(250, y - 80, 1670, y + 80, 30, CARD, k2 * fd(T(2), j * 1.2), outline=col, ow=3)
            c.text(300, y - 22, lab, 40, col, k2 * fd(T(2), j * 1.2), 'lm', 'Bold', bg=CARD)
            c.text(300, y + 32, 'chance a random person unlocks it', 30, DIM, k2 * fd(T(2), j * 1.2), 'lm', 'Medium', bg=CARD)
            c.text(1620, y, num, 64, col, k2 * fd(T(2), .5 + j * 1.2), 'rm', 'Bold', bg=CARD)
        c.text(960, 800, "Apple's figures", 28, DIM, k2, w='Medium')

def s_limits(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'Higher odds for twins and lookalikes', 62, PK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'It checks your attention', 66, CY, hl(1) * (1 - hl(2)), w='Bold')
    c.text(960, 150, 'It updates as your face changes', 64, GR, hl(2), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        for j, x in enumerate((640, 1280)):
            face(c, x, 480, 210, k0 * fd(T(0), j * .5))
        c.text(960, 480, '=?', 90, PK, k0 * fd(T(0), 1.0), w='Bold')
        c.text(960, 780, 'twins, lookalike siblings, children under 13', 36, INK, k0 * fd(T(0), 1.4), w='Bold')
    k1 = hl(1) * (1 - hl(2))
    if k1 > 0:
        for j, (x, eo, ok) in enumerate(((640, 0.0, False), (1280, 1.0, True))):
            kk = k1 * fd(T(1), j * .8)
            face(c, x, 470, 200, kk, eyes_open=eo)
            if ok: c.check(x + 220, 300, 60, GR, kk, fd(T(1), 1.2))
            else: c.cross(x + 220, 300, 80, PK, kk)
            c.text(x, 760, 'eyes open, looking' if ok else 'eyes closed', 38, GR if ok else PK, kk, w='Bold')
        c.text(960, 820, 'the default setting', 28, DIM, k1, w='Medium')
    k2 = hl(2)
    if k2 > 0:
        for j, (x, b) in enumerate(((500, 0.0), (960, .5), (1420, 1.0))):
            kk = k2 * fd(T(2), j * .6)
            face(c, x, 480, 180, kk, beard=b)
        c.arrow(640, 480, 780, 480, GR, 5, k2 * fd(T(2), .4), 18)
        c.arrow(1100, 480, 1240, 480, GR, 5, k2 * fd(T(2), 1.0), 18)
        c.text(960, 760, 'growing a beard, wearing makeup', 38, INK, k2 * fd(T(2), 1.4), w='Bold')

def s_private(c, T, t):
    hl = lambda i: hl_(T, i)
    c.text(960, 150, 'The face code never leaves your phone', 62, INK, hl(0) * (1 - hl(1)), w='Bold')
    c.text(960, 150, 'Camera-only face unlock? Use a stronger lock', 56, YE, hl(1), w='Bold')
    k0 = hl(0) * (1 - hl(1))
    if k0 > 0:
        sb = phone(c, 620, 500, 520, k0)
        c.rr(540, 440, 700, 560, 16, (40, 46, 90), k0, outline=CY, ow=4, bg=(18, 22, 44))
        c.text(620, 480, 'secure', 26, CY, k0, w='Bold', bg=(40, 46, 90))
        c.text(620, 520, 'chip', 26, CY, k0, w='Bold', bg=(40, 46, 90))
        lock(c, 620, 640, 70, 0, CY, k0, bg=(18, 22, 44))
        for j in range(3):
            ell(c, 1330 + (j - 1) * 110, 420 - (j % 2) * 40, 120, 80, (70, 80, 120), k0 * fd(T(0), .6))
        c.text(1330, 430, 'Apple', 40, INK, k0 * fd(T(0), .6), w='Bold', bg=(70, 80, 120))
        c.arrow(800, 470, 1150, 440, DIM, 5, k0 * fd(T(0), .6) * .6, 20)
        c.cross(980, 455, 90, PK, k0 * fd(T(0), 1.4))
        c.text(1330, 580, 'not sent to Apple', 40, PK, k0 * fd(T(0), 1.6), w='Bold')
        c.text(1330, 650, "Apple's support page", 28, DIM, k0, w='Medium')
    k1 = hl(1)
    if k1 > 0:
        for j, (lab, x) in enumerate((('fingerprint', 620), ('PIN: 6+ digits', 1300))):
            kk = k1 * fd(T(1), .6 + j * .8)
            c.rr(x - 260, 280, x + 260, 720, 30, CARD, kk, outline=GR, ow=3)
            if j == 0:
                for q in range(6):
                    ell(c, x, 470, 40 + q * 22, 55 + q * 26, None, kk, outline=GR, ow=6, bg=CARD)
            else:
                for q in range(6):
                    c.circ(x - 175 + q * 70, 470, 22, GR, kk, bg=CARD)
            c.text(x, 670, lab, 40, INK, kk, w='Bold', bg=CARD)
        c.text(960, 800, "advice from the consumer group Which?", 28, DIM, k1, w='Medium')

RECAPS = [('1', 'Simple face unlock compares flat pictures', PK),
          ('2', '3D face unlock measures your face with dots', IR),
          ('3', 'A photo is flat: no depth to match', GR)]
def s_recap(c, T, t):
    out = 1 - fd(T(4), -.3, .5)
    c.text(960, 160, 'Remember three things', 70, INK, fd(T(0)) * out, w='Bold')
    for i, (nn, lab, col) in enumerate(RECAPS):
        m = fd(T(i + 1)) * out; y = 320 + i * 170; dx = 40 * (1 - fd(T(i + 1)))
        if m <= .01: continue
        c.rr(300 + dx, y - 70, 1620 + dx, y + 70, 34, CARD, m, outline=col, ow=4)
        c.circ(390 + dx, y, 42, col, m, bg=CARD); c.text(390 + dx, y, nn, 48, BG, m, w='Bold', bg=col)
        c.text(470 + dx, y, lab, 46, INK, m, 'lm', 'Bold', bg=CARD)
    if T(4) > 0:
        m = fd(T(4), .2); p = 1 + .03 * math.sin(t * 5)
        c.rr(960 - 290 * p, 430 - 75 * p, 960 + 290 * p, 430 + 75 * p, 75, (235, 50, 60), m)
        c.text(960, 430, 'SUBSCRIBE', 72, INK, m, w='Bold', bg=(235, 50, 60))
        c.text(960, 610, 'A new explainer every day', 44, DIM, fd(T(4), .7), w='Medium')
        c.text(960, 690, 'Short Story Long Thinking', 40, CY, fd(T(4), 1.0), w='Medium')

SCENES = [
 ('INTRO', ["Hold a printed photo of your face up to some phones, and they unlock.",
            "In a twenty twenty-three test, a printed photo fooled nineteen of forty-eight phones.",
            "Other phones can't be fooled that way at all.",
            "The difference? One looks at your face. The other measures it.",
            "Here's how."], s_hook),
 ('1  ·  FLAT PICTURES', ["The simplest face unlock compares two flat pictures: what the camera sees now, and one saved at setup.",
            "It's like spotting a friend in a photo. Eyes, nose and mouth, in the right places.",
            "But a printed photo has those too. So a flat photo can pass as you."], s_flat),
 ('2  ·  INVISIBLE LIGHT', ["3D face unlock adds parts you never notice. Take the iPhone's Face ID.",
            "First, it floods your face with infrared light. So it works even in the dark.",
            "Infrared is invisible to you, like the light from a TV remote."], s_light),
 ('3  ·  30,000 DOTS', ["Next, a tiny projector throws more than thirty thousand invisible dots onto your face.",
            "Picture a grid of dots shone onto a flat wall. They land in neat rows.",
            "Shine them onto a crumpled bedsheet, and over every bump, the dots shift."], s_dots),
 ('4  ·  DEPTH MAP', ["An infrared camera photographs the dots. From how far each one shifted, the phone works out how close each part of your face is.",
            "Your nose sticks out. Your eyes sit deeper. That's a depth map: the 3D shape of your face."], s_depth),
 ('5  ·  QUICK QUESTION', ["Quick question. Hold up a sharp, life-size photo. What does the depth map show?",
            "A: a face shape. Or B: a flat sheet.",
            "Three, two, one.",
            "B. Every dot lands at the same depth. No nose, no eye sockets. Apple says Face ID always needs depth."], s_quiz),
 ('6  ·  THE MATCH', ["Then a chip turns the depth map and an infrared picture into a code of numbers.",
            "It compares that code with the one saved at setup. Like a key in a lock, it has to fit closely.",
            "Apple puts the chance a random stranger unlocks it at less than one in a million. Its fingerprint sensor: one in fifty thousand."], s_match),
 ('7  ·  LIMITS', ["It isn't perfect. Apple says the odds are higher for twins, lookalike siblings, and children under thirteen.",
            "It also checks attention. By default, your eyes must be open and looking.",
            "And it updates as your face changes, like a growing beard or makeup."], s_limits),
 ('8  ·  YOUR PHONE', ["Apple says the face code never leaves your phone. It's locked in a secure chip.",
            "If your phone's face unlock uses only the camera, Which? suggests a fingerprint, or a PIN of at least six digits."], s_private),
 ('RECAP', ["So remember three things.",
            "One. Simple face unlock compares flat pictures, so a photo can fool it.",
            "Two. 3D face unlock shines invisible dots to measure your face's shape.",
            "Three. A photo is flat. It has no depth to match.",
            "If you learned something, subscribe to Short Story Long Thinking."], s_recap),
]

def remap(fn, mp):
    """Reuse a long-video scene with a different line order: mp maps the scene's line index -> narration line index."""
    def g(c, T, t):
        def T2(i, off=0.0):
            if i not in mp: return -99
            j, o = mp[i] if isinstance(mp[i], tuple) else (mp[i], 0.0)
            return T(j, off + o)
        fn(c, T2, t)
    return g

# The Short: its own complete mini-story. Loop ending (lesson of 2026-10-27): the last line stops on
# "And that's why", which runs straight back into the first line when the Short replays.
SHORT_SCENES = [
 ('THE PUZZLE', ["A photo of your face can fool some phones.",
                 "Others can't be fooled that way. One kind looks at your face. The other measures it."],
                remap(s_hook, {0: 0, 2: (1, 0.0), 3: (1, 2.4)})),
 ('LOOKS', ["Simple face unlock compares flat camera pictures. A printed photo has eyes, a nose and a mouth too.",
            "In a twenty twenty-three test, photos fooled nineteen of forty-eight phones."],
           remap(s_flat, {0: (0, -0.2), 1: (0, 0.0), 2: (0, 2.2)})),
 ('MEASURES', ["3D face unlock shines more than thirty thousand invisible dots onto your face.",
               "A camera sees how they shift over your nose and eyes, and builds a 3D shape."],
              remap(s_depth, {0: 0, 1: 1})),
 ('THE ANSWER', ["A photo is flat. Every dot lands at the same depth, so there's no face shape to match.",
                 "Camera-only phones can't see that. And that's why"],
                card('A photo is flat.', 'No depth, no match.')),
]
SHORT_HITS = [(3, 0, 0.0)]
