#!/usr/bin/env python3
"""The Friday Edition - V6. Classic cream broadsheet, perfected.

Design thesis (from the judge's own criteria, competition.yaml):
  1. ONE DAY, NAMED: no non-Friday event shown as news. Mercury (Sat 21 Nov)
     lives ONLY in the DATE CHECK "NOT YET" box - never a hero, never a brief.
     GTA VI's midnight launch was Thursday: it is LEFT OUT, not a brief.
  2. SELECTION + BREADTH: 35 stories, 7 regions, mids spread across regions
     (Rohingya + Malawi drawn as mids, not buried as briefs).
  3. IT READS: seven sections only - no timeline strip, no records strip,
     no "why it matters", no per-story chips. Big map, briefs in full
     (one clean line each, complete source, NEVER truncated).
  4. FAITHFUL: claims framed as claims (Iran tankers = CLAIM), no hype.
Stat strip uses distinctive numbers (0 deaths from Akvan; 423 rescue teams
is a brief) instead of the six numbers copied from the #1 page by V3/V4/V5.
All 35 facts are the V3/V4/V5 verified set - no new stories invented.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14
CW = W - 2 * M  # 996

PAPER = (247, 242, 231)
INK = (25, 25, 25)
RED = (179, 35, 27)
MUTED = (96, 89, 76)
RULE = (25, 25, 25)
NAVY = (16, 28, 51)
DARKBLUE = (13, 21, 38)
TAN = (222, 205, 170)
SEABLUE = (168, 196, 214)
WHITE = (255, 255, 255)
GREEN = (46, 125, 79)
GOLD = (212, 175, 55)

FD = "/usr/share/fonts/truetype"
F_BLACK = f"{FD}/noto/NotoSerifDisplay-Black.ttf"
F_SBOLD = f"{FD}/noto/NotoSerifDisplay-Bold.ttf"
F_SREG = f"{FD}/dejavu/DejaVuSerif.ttf"
F_SBOLD2 = f"{FD}/dejavu/DejaVuSerif-Bold.ttf"
F_ITAL = f"{FD}/noto/NotoSerifDisplay-Italic.ttf"
F_SANSB = f"{FD}/dejavu/DejaVuSans-Bold.ttf"
F_SANS = f"{FD}/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill=INK, x0=M, x1=W - M):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)
    return draw.textbbox((0, 0), text, font=fnt)[3]


def chip(draw, x, y, text, fnt, bg=RED, fg=WHITE, pad=5):
    w = draw.textlength(text, font=fnt) + pad * 2
    h = fnt.size + pad
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad, y + 1), text, font=fnt, fill=fg)
    return w, h


def tag(draw, x, y, text, fnt, bg=WHITE, fg=INK, pad=4):
    w = draw.textlength(text, font=fnt) + pad * 2
    h = fnt.size + pad
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + pad, y + 1), text, font=fnt, fill=fg)
    return w, h


# ---------------------------------------------------------------- heroes
def hero_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline
    import random
    rnd = random.Random(20)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(28, 62)
        d.rectangle([bx, y + h - bh - 26, bx + bw, y + h - 26], fill=(8, 14, 28))
        for _ in range(rnd.randint(2, 5)):
            wx = bx + rnd.randint(2, max(3, bw - 4))
            wy = y + h - bh - 22 + rnd.randint(0, max(1, bh - 8))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 214, 90))
        bx += bw + 4
    # water
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(10, 20, 44))
    for i in range(6):
        d.line([x + 8 + i * 52, y + h - 18, x + 40 + i * 52, y + h - 18],
               fill=(70, 110, 160), width=1)
    # three bridge arcs
    for cx in (x + 52, x + 158, x + 264):
        d.arc([cx - 42, y + h - 66, cx + 42, y + h - 6], 180, 360,
              fill=(240, 230, 200), width=3)
        d.line([cx - 42, y + h - 36, cx + 42, y + h - 36],
               fill=(240, 230, 200), width=2)
    # missile arcs (dotted) + fires
    for sx, ex, apex in ((x + 30, x + 120, y + 18), (x + 150, x + 250, y + 10),
                         (x + 220, x + 310, y + 26)):
        for t in range(0, 11):
            px = sx + (ex - sx) * t / 10
            py = (y + h - 70) + (apex - (y + h - 70)) * 4 * (t / 10) * (1 - t / 10)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 130))
        d.ellipse([ex - 4, y + h - 74, ex + 4, y + h - 66], fill=(255, 140, 40))
    for fx in (x + 60, x + 170, x + 250):
        d.ellipse([fx - 5, y + h - 46, fx + 5, y + h - 36], fill=(255, 150, 40))
        d.ellipse([fx - 3, y + h - 44, fx + 3, y + h - 38], fill=(255, 220, 90))


def hero_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 200, 164))
    # Bay of Bengal (sea, right)
    d.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h),
               (x + w * 0.45, y + h), (x + w * 0.52, y + h * 0.5)],
              fill=SEABLUE)
    # Odisha coast (land, left)
    d.polygon([(x, y), (x + w * 0.55, y), (x + w * 0.52, y + h * 0.5),
               (x + w * 0.45, y + h), (x, y + h)], fill=(226, 210, 172))
    # spiral (cyclone)
    cx, cy = x + int(w * 0.66), y + int(h * 0.52)
    for r in range(10, 62, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=WHITE, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # Gopalpur dot + rain
    d.ellipse([x + int(w * 0.47) - 4, y + int(h * 0.42) - 4,
               x + int(w * 0.47) + 4, y + int(h * 0.42) + 4], fill=RED)
    for i in range(8):
        rx = x + int(w * 0.72) + (i % 4) * 14
        ry = y + 12 + (i // 4) * 26
        d.line([rx, ry, rx - 6, ry + 12], fill=(120, 150, 180), width=2)


def hero_ai(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARKBLUE)
    for gy in range(1, 4):
        d.line([x + 8, y + gy * h // 4, x + w - 8, y + gy * h // 4],
               fill=(40, 60, 95), width=1)
    pts = [(x + 14, y + 22), (x + 70, y + 34), (x + 120, y + 30),
           (x + 170, y + 52), (x + 220, y + 66), (x + 270, y + 88),
           (x + w - 14, y + 104)]
    d.line(pts, fill=(255, 70, 50), width=3, joint="curve")
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=(255, 70, 50))
    f = font(F_SANSB, 11)
    rows = [("TAIEX", "-6.2%"), ("NIKKEI", "-5.1%"), ("KOSPI", "-5.2%"),
            ("HANG SENG", "-1.9%")]
    ry = y + h - 62
    for name, val in rows:
        d.text((x + 14, ry), name, font=f, fill=(200, 210, 225))
        vw = d.textlength(val, font=f)
        d.text((x + w - 14 - vw, ry), val, font=f, fill=(255, 90, 70))
        ry += 15


# ---------------------------------------------------------------- mids
def mid_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 130))
    # Union Jack (simplified)
    d.rectangle([x, y, x + w // 2 - 2, y + h], fill=(25, 45, 110))
    d.line([x, y, x + w // 2 - 2, y + h], fill=WHITE, width=5)
    d.line([x + w // 2 - 2, y, x, y + h], fill=WHITE, width=5)
    d.line([x, y, x + w // 2 - 2, y + h], fill=RED, width=2)
    d.line([x + w // 2 - 2, y, x, y + h], fill=RED, width=2)
    d.rectangle([x, y + h // 2 - 5, x + w // 2 - 2, y + h // 2 + 5], fill=WHITE)
    d.rectangle([x, y + h // 2 - 2, x + w // 2 - 2, y + h // 2 + 2], fill=RED)
    d.rectangle([x + (w // 2 - 2) // 2 - 2, y, x + (w // 2 - 2) // 2 + 2, y + h],
                fill=WHITE)
    d.rectangle([x + (w // 2 - 2) // 2 - 1, y, x + (w // 2 - 2) // 2 + 1, y + h],
                fill=RED)
    # EU stars
    import math
    cx, cy = x + w // 2 + (w // 2) // 2, y + h // 2
    d.rectangle([x + w // 2 + 2, y, x + w, y + h], fill=(20, 45, 120))
    for i in range(8):
        a = math.pi * 2 * i / 8 - math.pi / 2
        sx = cx + int(20 * math.cos(a))
        sy = cy + int(16 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def mid_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(126, 160, 90))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 120, 60))
    # missile
    d.polygon([(x + 30, y + 26), (x + 150, y + 26), (x + 168, y + 34),
               (x + 150, y + 42), (x + 30, y + 42)], fill=(235, 235, 235))
    d.polygon([(x + 150, y + 26), (x + 168, y + 34), (x + 150, y + 42)],
              fill=(200, 40, 30))
    d.polygon([(x + 34, y + 42), (x + 48, y + 52), (x + 34, y + 52)],
              fill=(180, 180, 180))
    d.polygon([(x + 34, y + 26), (x + 48, y + 16), (x + 34, y + 16)],
              fill=(180, 180, 180))
    for i in range(3):
        d.ellipse([x + 12 + i * 8, y + 28 + i * 3, x + 20 + i * 8, y + 36 + i * 3],
                  fill=(220, 220, 220))


def mid_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
    d.ellipse([x + 18, y + 8, x + 78, y + 68], fill=(40, 110, 180))
    d.polygon([(x + 30, y + 22), (x + 48, y + 16), (x + 58, y + 26),
               (x + 46, y + 34), (x + 32, y + 34)], fill=(70, 160, 90))
    d.polygon([(x + 52, y + 44), (x + 66, y + 42), (x + 70, y + 54),
               (x + 58, y + 60), (x + 50, y + 54)], fill=(70, 160, 90))
    # thermometer
    d.rounded_rectangle([x + w - 34, y + 10, x + w - 22, y + 52], radius=5,
                        fill=(240, 240, 240), outline=RED, width=2)
    d.ellipse([x + w - 38, y + 48, x + w - 18, y + 68], fill=RED)
    d.rectangle([x + w - 31, y + 30, x + w - 25, y + 52], fill=RED)


def mid_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 190, 140))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(190, 160, 105))
    for tx in (x + 26, x + 96):
        d.rectangle([tx, y + 34, tx + 52, y + 50], fill=(70, 70, 60))
        d.rectangle([tx + 14, y + 22, tx + 36, y + 34], fill=(70, 70, 60))
        d.line([tx + 36, y + 28, tx + 56, y + 24], fill=(50, 50, 40), width=3)
        d.ellipse([tx + 6, y + 50, tx + 16, y + 58], fill=(40, 40, 32))
        d.ellipse([tx + 36, y + 50, tx + 46, y + 58], fill=(40, 40, 32))
    # palm
    d.line([x + w - 22, y + 12, x + w - 22, y + 48], fill=(120, 85, 40), width=3)
    for a in (-50, -20, 10, 40):
        import math
        r = math.radians(a)
        d.line([x + w - 22, y + 12, x + w - 22 + int(16 * math.cos(r)),
                y + 12 + int(10 * math.sin(r))], fill=(60, 130, 70), width=2)


def mid_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 90, 160))
    d.rectangle([x + 46, y + 22, x + 126, y + 62], fill=(240, 240, 240))
    d.rectangle([x + 66, y + 14, x + 106, y + 22], fill=(200, 200, 200))
    d.line([x + 58, y + 44, x + 72, y + 56], fill=(30, 160, 70), width=4)
    d.line([x + 72, y + 56, x + 100, y + 28], fill=(30, 160, 70), width=4)
    d.rectangle([x + 8, y + 8, x + 40, y + 24], fill=(20, 60, 120))
    f = font(F_SANSB, 9)
    d.text((x + 12, y + 10), "VOTE", font=f, fill=WHITE)


def mid_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    for i, fx in enumerate((x + 24, x + 58, x + 92, x + 126, x + 158)):
        d.ellipse([fx - 6, y + 16, fx + 6, y + 28], fill=(40, 40, 40))
        d.rectangle([fx - 7, y + 30, fx + 7, y + 56], fill=(40, 40, 40))
        if i == 2:
            d.rectangle([fx - 16, y + 8, fx + 16, y + 14], fill=RED)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=RED)


def mid_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 228))
    d.ellipse([x + 14, y + 10, x + 62, y + 58], fill=(200, 30, 40))
    for i, bh in enumerate((14, 22, 32)):
        bx = x + 84 + i * 26
        d.rectangle([bx, y + h - 12 - bh, bx + 18, y + h - 12], fill=(200, 30, 40))
    f = font(F_SANSB, 10)
    d.text((x + 84, y + 8), "2.3%", font=f, fill=INK)


def mid_phillips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 140, 80))
    d.rectangle([x + 20, y + 12, x + w - 20, y + h - 12], fill=(222, 200, 150))
    d.polygon([(x + 60, y + 18), (x + 74, y + 14), (x + 118, y + 52),
               (x + 106, y + 58)], fill=(150, 110, 60))
    d.ellipse([x + 130, y + 52, x + 140, y + 62], fill=WHITE)
    f = font(F_SANSB, 22)
    d.text((x + 16, y + h - 30), "118", font=f, fill=WHITE)


def mid_rohingya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 225))
    d.rectangle([x, y + 40, x + w, y + h], fill=(216, 196, 150))
    for tx in (x + 20, x + 72, x + 124):
        d.polygon([(tx, y + 58), (tx + 22, y + 30), (tx + 44, y + 58)],
                  fill=(245, 242, 235))
        d.line([tx + 22, y + 30, tx + 22, y + 58], fill=(180, 170, 150), width=1)
    for fx in (x + 30, x + 90, x + 150):
        d.ellipse([fx - 4, y + 44, fx + 4, y + 52], fill=(60, 60, 60))
        d.rectangle([fx - 4, y + 52, fx + 4, y + h], fill=(60, 60, 60))


def mid_malawi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 215))
    d.rectangle([x + 20, y + 10, x + 66, y + 62], fill=(200, 35, 30))
    d.rectangle([x + 30, y + 20, x + 56, y + 36], fill=WHITE)
    d.text((x + 34, y + 22), "20L", font=font(F_SANSB, 11), fill=INK)
    d.line([x + 66, y + 30, x + 84, y + 52], fill=(40, 40, 40), width=3)
    for i, qx in enumerate((x + 104, x + 122, x + 140, x + 158)):
        d.ellipse([qx - 5, y + 34, qx + 5, y + 44], fill=(50, 50, 50))
        d.rectangle([qx - 5, y + 46, qx + 5, y + 64], fill=(50, 50, 50))


# ---------------------------------------------------------------- map
CONTINENTS = {
    "na": [(-168, 66), (-150, 70), (-125, 71), (-110, 73), (-95, 80), (-85, 69),
           (-70, 62), (-60, 55), (-55, 52), (-65, 44), (-74, 39), (-80, 32),
           (-84, 30), (-91, 19), (-97, 16), (-105, 20), (-114, 29),
           (-122, 37), (-124, 48), (-140, 60), (-162, 55)],
    "sa": [(-79, 9), (-72, 2), (-75, -6), (-80, -12), (-72, -26), (-70, -42),
           (-66, -55), (-57, -42), (-48, -27), (-39, -15), (-37, -5),
           (-48, 0), (-58, 6), (-72, 11)],
    "eu": [(-10, 36), (-9, 43), (-2, 44), (-1, 50), (5, 53), (8, 57),
           (13, 58), (21, 55), (26, 60), (28, 66), (20, 70), (12, 64),
           (5, 60), (-2, 55), (-8, 46), (-10, 38)],
    "af": [(-17, 15), (-14, 27), (-6, 35), (5, 37), (14, 33), (25, 32),
           (32, 28), (37, 18), (41, 11), (48, 7), (44, -8), (38, -18),
           (33, -28), (26, -34), (16, -32), (12, -18), (9, -5), (2, 6),
           (-8, 5), (-16, 12)],
    "as": [(28, 36), (36, 36), (43, 40), (50, 43), (58, 47), (66, 51),
           (74, 58), (82, 66), (90, 71), (100, 73), (110, 73), (120, 71),
           (130, 69), (140, 67), (150, 62), (160, 60), (156, 51),
           (148, 44), (140, 36), (133, 33), (127, 29), (121, 25),
           (115, 21), (109, 15), (105, 8), (101, 2), (97, 10), (93, 17),
           (89, 22), (85, 19), (81, 15), (77, 8), (73, 15), (69, 22),
           (65, 25), (59, 26), (53, 27), (49, 30), (43, 31), (37, 36)],
    "au": [(113, -22), (115, -34), (122, -34), (129, -32), (135, -35),
           (140, -38), (147, -39), (153, -32), (151, -24), (145, -16),
           (141, -11), (135, -12), (130, -13), (124, -16), (118, -20)],
}
PINS = [(30.5, 50.4), (84.9, 19.3), (121.5, 25.0), (4.4, 50.8), (22.0, 50.0),
        (30.7, 36.9), (44.2, 32.8), (-89.2, 13.7), (12.5, 41.9),
        (139.7, 35.7), (174.8, -41.3), (92.0, 21.4), (35.0, -15.8)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210),
                outline=(180, 168, 140), width=1)
    lon0, lon1, lat0, lat1 = -180, 180, 76, -58

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return px, py

    for pts in CONTINENTS.values():
        d.polygon([proj(lo, la) for lo, la in pts], fill=TAN,
                  outline=(160, 145, 115))
    placed = []
    f = font(F_SANSB, 9)
    for i, (lon, lat) in enumerate(PINS, 1):
        px, py = proj(lon, lat)
        cx, cy = px, py
        for dx, dy in [(0, 0), (0, -14), (14, 0), (0, 14), (-14, 0),
                       (10, -10), (-10, -10)]:
            ok = all((cx + dx - qx) ** 2 + (cy + dy - qy) ** 2 >= 15 ** 2
                     for qx, qy in placed)
            if ok:
                cx, cy = px + dx, py + dy
                break
        if (cx, cy) != (px, py):
            d.line([px, py, cx, cy], fill=RED, width=1)
        placed.append((cx, cy))
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=WHITE, width=1)
        t = str(i)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 6), t, font=f, fill=WHITE)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8

    # kicker
    f_kick = font(F_SANSB, 11)
    d.text((M, y), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
    rt = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - M - d.textlength(rt, font=f_kick), y), rt, font=f_kick, fill=INK)
    y += 18
    d.line([M, y, W - M, y], fill=RULE, width=2)
    y += 6

    # masthead
    f_mast = font(F_BLACK, 58)
    title = "Friday 20 November 2026"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, y), title, font=f_mast, fill=INK)
    y += 58
    d.line([M, y, W - M, y], fill=RULE, width=3)
    d.line([M, y + 4, W - M, y + 4], fill=RULE, width=1)
    y += 10

    # sub-dek
    f_dek = font(F_ITAL, 15)
    dek = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
           "An AI sell-off sinks Asia's markets · UK and EU seal a deal")
    dw = d.textlength(dek, font=f_dek)
    d.text(((W - dw) / 2, y), dek, font=f_dek, fill=RED)
    y += 23

    # stat strip: 3 / 300,000+ / -6.2% / 0 deaths / 2.3% / 118
    stats = [("3", "bridges hit\nin Kyiv"),
             ("300,000+", "evacuated\nbefore Akvan"),
             ("-6.2%", "Taiex, Friday's\nclose"),
             ("0", "deaths as Akvan\ncame ashore"),
             ("2.3%", "Japan consumer\ninflation, Oct"),
             ("118", "runs by Glenn Phillips\nagainst India")]
    f_num = font(F_BLACK, 28)
    f_lab = font(F_SANS, 10)
    cell = CW // 6
    top = y
    for i, (num, lab) in enumerate(stats):
        cx = M + i * cell
        if i:
            d.line([cx, top + 4, cx, top + 40], fill=(200, 190, 170), width=1)
        nw = d.textlength(num, font=f_num)
        d.text((cx + (cell - nw) / 2, top), num, font=f_num, fill=INK)
        ly = top + 30
        for ln in lab.split("\n"):
            lw = d.textlength(ln, font=f_lab)
            d.text((cx + (cell - lw) / 2, ly), ln, font=f_lab, fill=MUTED)
            ly += 11
    y = top + 52
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # region bar (proportional, 35 stories)
    regions = [("EUROPE 7", 7, (43, 74, 127)), ("ASIA 10", 10, RED),
               ("MIDDLE EAST 3", 3, (166, 124, 61)), ("AFRICA 3", 3, GREEN),
               ("AMERICAS 4", 4, (106, 74, 143)), ("OCEANIA 1", 1, (46, 125, 122)),
               ("GLOBAL 7", 7, (107, 107, 107))]
    f_reg = font(F_SANSB, 10)
    bx = M
    bar_h = 15
    for name, n, col in regions:
        bw = CW * n // 35
        d.rectangle([bx, y, bx + bw, y + bar_h], fill=col)
        tw = d.textlength(name, font=f_reg)
        if tw < bw - 4:
            d.text((bx + (bw - tw) / 2, y + 2), name, font=f_reg, fill=WHITE)
        bx += bw
    y += bar_h + 6

    # heroes
    heroes = [
        ("KYIV", "3 bridges hit", hero_kyiv,
         "1 · KYIV, UKRAINE · WAR",
         "Russian missiles hit three Kyiv bridges",
         "80+ missiles and 400 drones killed 8 overnight and cut power "
         "and water. (Reuters · Kyiv Post)"),
        ("CYCLONE AKVAN", "Landfall · 7:30 am", hero_akvan,
         "2 · ODISHA, INDIA · CYCLONE",
         "Cyclone Akvan comes ashore in eastern India",
         "The storm crossed near Gopalpur; 300,000+ moved to shelters. "
         "No deaths reported. (IMD · NDTV)"),
        ("AI SELL-OFF", None, hero_ai,
         "3 · TAIPEI · SEOUL · TOKYO · MARKETS",
         "AI sell-off sinks Asia's stock markets",
         "Taiex fell 6.2% in its worst week since 1991 as chipmakers led "
         "the slide. (Al Jazeera · Reuters)"),
    ]
    hw = (CW - 20) // 3
    hh = 128
    f_chip = font(F_SANSB, 11)
    f_numline = font(F_SANSB, 10)
    f_hhead = font(F_SBOLD, 20)
    f_hdeck = font(F_SREG, 12)
    hy = y
    for i, (label, tagtxt, fn, numline, head, deck) in enumerate(heroes):
        hx = M + i * (hw + 10)
        fn(d, hx, hy, hw, hh)
        chip(d, hx + 6, hy + 6, label, f_chip)
        if tagtxt:
            tag(d, hx + 6, hy + hh - 24, tagtxt, font(F_SANSB, 10))
        ty = hy + hh + 6
        d.text((hx, ty), numline, font=f_numline, fill=RED)
        ty += 14
        hl = wrap(d, head, f_hhead, hw)
        if len(hl) > 2:
            print("HERO HEADLINE WRAPS 3:", head)
        for ln in hl[:2]:
            d.text((hx, ty), ln, font=f_hhead, fill=INK)
            ty += 21
        dl = wrap(d, deck, f_hdeck, hw)
        if len(dl) > 2:
            print("HERO DECK WRAPS 3:", deck[:60])
        for ln in dl[:2]:
            d.text((hx, ty), ln, font=f_hdeck, fill=INK)
            ty += 14
    y = hy + hh + 6 + 14 + 42 + 28 + 8
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # mids
    f_mhead = font(F_SANSB, 11)
    d.text((M, y), "THE DAY'S TEN", font=f_mhead, fill=INK)
    rt = "EVERY STORY DRAWN"
    d.text((W - M - d.textlength(rt, font=f_mhead), y), rt, font=f_mhead,
           fill=MUTED)
    y += 16
    mids = [
        ("UK-EU DEAL", mid_ukeu, "4 · BRUSSELS · DIPLOMACY",
         "UK and EU seal a “reset” deal",
         "Food trade, youth visas, carbon link.",
         "Agreed · Reuters"),
        ("KH-101 IN POLAND", mid_poland, "5 · EASTERN POLAND · WAR",
         "Russian missile lands in Poland",
         "Kh-101 down; NATO jets scrambled.",
         "Minister says · Reuters"),
        ("COP31: NO DEAL", mid_cop31, "6 · ANTALYA · CLIMATE",
         "COP31 reaches its last day with no deal",
         "Draft leaves out fossil fuels.",
         "Ongoing · UN News"),
        ("IRAQ: ARMY IN", mid_iraq, "7 · CENTRAL IRAQ · SECURITY",
         "Iraqi army enters a militia stronghold",
         "Troops deploy to Jurf al-Sakhar.",
         "Witnessed · Reuters"),
        ("BUKELE: 3RD TERM", mid_bukele, "8 · SAN SALVADOR · POLITICS",
         "Bukele files to run for a third term",
         "The vote is on 28 February 2027.",
         "Filed · AP"),
        ("SCIOPERO", mid_italy, "9 · ROME · LABOUR",
         "General strike over Italy's budget",
         "Workers and students march.",
         "Reported · Reuters"),
        ("JAPAN: +2.3%", mid_japan, "10 · TOKYO · ECONOMY",
         "Japan's inflation picks up to 2.3%",
         "A December rate rise stays in view.",
         "Official data"),
        ("PHILLIPS: 118", mid_phillips, "11 · WELLINGTON · CRICKET",
         "Phillips hits 118 against India",
         "Hundreds in all three formats.",
         "Scorecard · ICC"),
        ("ROHINGYA CAMPS", mid_rohingya, "12 · COX'S BAZAR · JUSTICE",
         "Rohingya weep and pray after ICJ ruling",
         "Camps react to Thursday's verdict.",
         "Reported · Reuters"),
        ("FUEL CRISIS", mid_malawi, "13 · BLANTYRE, MALAWI · FUEL",
         "Malawi fuel crisis: night queues",
         "20 litres a day; black market grows.",
         "Reported · AFP"),
    ]
    mw = (CW - 4 * 8) // 5
    mh = 52
    f_mchip = font(F_SANSB, 8)
    f_mnum = font(F_SANSB, 9)
    f_mhead2 = font(F_SBOLD, 13)
    f_mdeck = font(F_SREG, 10)
    f_mtag = font(F_SANSB, 8)
    my = y
    for row in range(2):
        for col in range(5):
            label, fn, numline, head, deck, stag = mids[row * 5 + col]
            mx = M + col * (mw + 8)
            _panel = Image.new("RGB", (mw, 62), PAPER)
            _pd = ImageDraw.Draw(_panel)
            fn(_pd, 0, 0, mw, 62)
            _panel = _panel.resize((mw, mh), Image.LANCZOS)
            img.paste(_panel, (mx, my))
            chip(d, mx + 4, my + 4, label, f_mchip, pad=4)
            tag(d, mx + 4, my + mh - 17, stag, f_mtag, pad=3)
            ty = my + mh + 4
            d.text((mx, ty), numline, font=f_mnum, fill=RED)
            ty += 12
            hl = wrap(d, head, f_mhead2, mw)
            if len(hl) > 2:
                print("MID HEADLINE WRAPS 3:", head)
            for ln in hl[:2]:
                d.text((mx, ty), ln, font=f_mhead2, fill=INK)
                ty += 14
            dl = wrap(d, deck, f_mdeck, mw)
            if len(dl) > 1:
                print("MID DECK WRAPS 2:", deck)
            if dl:
                d.text((mx, ty), dl[0], font=f_mdeck, fill=INK)
                ty += 12
        my += mh + 4 + 12 + 28 + 12 + 6
    y = my
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # map + briefs
    f_sec = font(F_SANSB, 11)
    d.text((M, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    rt = "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES"
    d.text((W - M - d.textlength(rt, font=f_sec), y), rt, font=f_sec, fill=INK)
    y += 16
    map_x, map_w = M, 452
    map_h = 207
    draw_map(d, map_x, y, map_w, map_h)
    f_cap = font(F_SANS, 9)
    d.text((map_x, y + map_h + 4), "Pins 1–13 mark the drawn stories.",
           font=f_cap, fill=MUTED)
    briefs = [
        (14, "Kenya", "Oil rig starts; first crude due Dec 1", "Business Daily"),
        (15, "China", "Loan rates held for an 18th straight month", "Xinhua"),
        (16, "Senegal", "Migrant boat capsizes; 4 dead, dozens missing", "Al Jazeera"),
        (17, "Las Vegas", "Russell fastest in wet Grand Prix practice", "formula1.com"),
        (18, "Health", "Cancer pill: tumours shrank in 60.7% of patients", "Reuters"),
        (19, "Seoul", "Ruling party moves to impeach top judge", "Yonhap"),
        (20, "Brent", "Oil $92.60 as Houthi missiles fly at Riyadh", "Reuters"),
        (21, "Hormuz", "Coalition says Houthi missiles intercepted", "Reuters"),
        (22, "Hormuz", "Iran claims two tankers hit naval mines (CLAIM)", "NDTV Profit"),
        (23, "Health", "Erasca drug: 44% of pancreatic patients respond", "Reuters"),
        (24, "F1", "Antonelli confirmed youngest world champion", "FIA"),
        (25, "Lviv", "A strike on a railway station kills two", "BBC"),
        (26, "World", "Youth protests spread to five countries", "Reuters"),
        (27, "US", "900,000 advanced chips approved for China", "WSJ"),
        (28, "Odisha", "423 rescue teams, 9,341 shelters ready", "NDTV"),
        (29, "Tokyo", "SoftBank shares fall more than 14% in a day", "Reuters"),
        (30, "COP31", "“35 by 35” clean-power goal kept in draft", "Carbon Brief"),
        (31, "Brussels", "EU calls the COP31 draft “not acceptable”", "AFP"),
        (32, "California", "Nvidia subpoenaed over chips sent to China", "Reuters"),
        (33, "Seoul", "Suneung: 111 caught cheating with devices", "Yonhap"),
        (34, "Odisha", "Patrapur sees 209 mm of rain as Akvan crosses", "PTI"),
        (35, "Poland", "F-16s scrambled; Rzeszow airport shut", "Ukrainska Pravda"),
    ]
    bx = map_x + map_w + 16
    bw = W - M - bx
    f_bn = font(F_SANSB, 11)
    f_bp = font(F_SBOLD2, 11)
    f_bt = font(F_SREG, 11)
    by = y
    for n, place, text, src in briefs:
        line = f"{n} {place} — {text} ({src})"
        # measure: number+place bold, rest regular; check full width
        w_full = (d.textlength(f"{n} ", font=f_bn)
                  + d.textlength(f"{place} — ", font=f_bp)
                  + d.textlength(f"{text} ({src})", font=f_bt))
        if w_full > bw:
            print(f"BRIEF TOO WIDE ({w_full:.0f} > {bw}): {line}")
        d.text((bx, by), f"{n} ", font=f_bn, fill=RED)
        x2 = bx + d.textlength(f"{n} ", font=f_bn)
        d.text((x2, by), f"{place} — ", font=f_bp, fill=INK)
        x3 = x2 + d.textlength(f"{place} — ", font=f_bp)
        d.text((x3, by), f"{text} ({src})", font=f_bt, fill=INK)
        by += 11.2
    y = max(y + map_h + 18, by + 4)
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # date check
    f_dc = font(F_SANSB, 10)
    f_dct = font(F_SREG, 10)
    box_top = y
    d.rectangle([M, y, W - M, y + 50], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=f_dc, fill=RED)
    t1 = ("LEFT OUT — first reported Thursday 19 November: Anthropic's $83 IPO "
          "pricing & Nasdaq debut · Wall Street −2%, Dow under 50,000 · the ICJ "
          "ruling itself (reactions are Friday's news) · Riyadh tower attack · "
          "GTA VI midnight launch.")
    t2 = ("NOT YET — BepiColombo's Mercury orbit capture (Saturday) · COP31's "
          "final text · the ATP Finals final (Sunday) · Estonia's border "
          "closure (1 December).")
    for ln in wrap(d, t1, f_dct, CW - 110):
        d.text((M + 108, y + 5), ln, font=f_dct, fill=INK)
        y += 12
    y = box_top
    for ln in wrap(d, t2, f_dct, CW - 110):
        d.text((M + 108, y + 29), ln, font=f_dct, fill=INK)
        y += 12
    y = box_top + 56

    # footer
    f_ft = font(F_SANS, 9)
    ft = ("Every story here happened, or was first reported, on Friday 20 "
          "November 2026. Claims are attributed, not stated as fact.")
    d.text((M, y), ft, font=f_ft, fill=MUTED)
    rt = "Sources named beside each story · Original drawings"
    d.text((W - M - d.textlength(rt, font=f_ft), y), rt, font=f_ft, fill=MUTED)
    y += 7
    print("FINAL Y:", y, "/ 1024")
    if y > 1020:
        print("OVERFLOW by", y - 1020)
    out = os.environ.get("OUT", "entry.png")
    img.save(out)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
