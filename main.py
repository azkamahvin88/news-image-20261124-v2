#!/usr/bin/env python3
"""
THE WORLD IN ONE DAY — news-image-20261124 v2
"Sum up 24 November's world news in one image" (make.fun)

Programmatic newspaper front page, drawn entirely in code with PIL.
35 stories, all first reported Tuesday 24 November 2026.
7 regions: Europe 7, Asia 6, Middle East 10, Americas 5, Africa 2,
Oceania 2, Global 3.

Canvas 1600 x 2100. Output: $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png).
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2100
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

# ---------------------------------------------------------------- palette
PAPER   = (247, 243, 232)
INK     = (24, 24, 28)
NAVY    = (18, 38, 74)
NAVY_LT = (38, 68, 118)
RED     = (178, 34, 34)
GOLD    = (196, 148, 44)
TEAL    = (14, 116, 110)
SKY     = (168, 205, 230)
SKY_DK  = (96, 150, 196)
SEA     = (36, 110, 160)
SAND    = (232, 214, 170)
GREY    = (110, 110, 108)
RULE    = (60, 60, 60)
CARD    = (255, 255, 255)
CREAM   = (253, 248, 236)

SERIF      = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B    = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS       = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B     = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_OB    = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- text utils
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; return y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centre(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


def badge(draw, x, y, num, d=34):
    """Numbered red disc used on featured stories and map pins."""
    draw.ellipse([x, y, x + d, y + d], fill=RED, outline=(255, 255, 255), width=2)
    f = font(SANS_B, 17)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (d - tw) / 2, y + 7), t, font=f, fill=(255, 255, 255))


def burst(draw, cx, cy, r, colour):
    """Starburst / explosion shape."""
    pts = []
    import math
    for i in range(16):
        ang = math.pi * 2 * i / 16
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour, outline=(120, 60, 0))


def waves(draw, x, y, w, colour, amp=5, step=18):
    """Row of wave arcs across a sea band."""
    import math
    for xx in range(x, x + w, step):
        draw.arc([xx, y, xx + step, y + amp * 2], 180, 360, fill=colour, width=2)


# ---------------------------------------------------------------- illustrations
# Every featured story gets its own flat-vector scene, drawn in code and
# captioned with a place label inside the frame.  `box` = (x, y, w, h).

def ill_riyadh(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 165))                       # dusk sky
    d.ellipse([x + w - 70, y + 12, x + w - 26, y + 56], fill=(255, 236, 170))
    for i, (tx, tw, th) in enumerate([(0.05, 0.13, 0.62), (0.22, 0.11, 0.45),
                                      (0.38, 0.14, 0.72), (0.58, 0.10, 0.50),
                                      (0.72, 0.15, 0.66)]):
        bx = x + int(w * tx); bw = int(w * tw); bt = y + h - int(h * th)
        d.rectangle([bx, bt, bx + bw, y + h], fill=(52, 68, 96))
        for wy in range(bt + 12, y + h - 8, 22):
            for wx in range(bx + 6, bx + bw - 6, 14):
                d.rectangle([wx, wy, wx + 6, wy + 9], fill=(255, 214, 120))
    burst(d, x + int(w * 0.45), y + int(h * 0.30), 34, (255, 140, 40))
    burst(d, x + int(w * 0.45), y + int(h * 0.30), 18, (255, 220, 90))
    for sx in (x + int(w * 0.30), x + int(w * 0.45), x + int(w * 0.60)):
        d.line([sx, y + int(h * 0.34), sx + 14, y + int(h * 0.55)],
               fill=(120, 120, 120), width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 42, 64))
    d.text((x + 10, y + h - 24), "RIYADH — FINANCIAL DISTRICT TOWER",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_hormuz(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 24, y + 16, x + 64, y + 56], fill=(255, 240, 180))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=SEA)
    waves(d, x, y + int(h * 0.58), w, (255, 255, 255))
    waves(d, x, y + int(h * 0.72), w, (180, 220, 240))
    # tanker
    hx, hy = x + int(w * 0.22), y + int(h * 0.42)
    d.polygon([(hx, hy), (hx + int(w * 0.55), hy), (hx + int(w * 0.50), hy + 34),
               (hx + 8, hy + 34)], fill=(150, 40, 32))
    d.rectangle([hx + 40, hy - 26, hx + 90, hy], fill=(240, 240, 235))
    d.rectangle([hx + 110, hy - 18, hx + 150, hy], fill=(240, 240, 235))
    d.rectangle([hx + 175, hy - 34, hx + 190, hy], fill=(60, 60, 60))
    d.text((hx + 46, hy + 8), "ADNOC L&S", font=font(SANS_B, 13), fill=(255, 255, 255))
    # spiked mine + blast
    mx, my = x + int(w * 0.80), y + int(h * 0.60)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]:
        d.line([mx, my, mx + dx * 16, my + dy * 16], fill=(20, 20, 20), width=3)
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(20, 20, 20))
    burst(d, mx, my - 34, 22, (255, 200, 60))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 50, 80))
    d.text((x + 10, y + h - 24), "STRAIT OF HORMUZ — MINE STRIKE",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_beijing(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(120, 150, 110))
    # government hall, red pillars
    bx, by = x + int(w * 0.18), y + int(h * 0.22)
    bw, bh = int(w * 0.64), int(h * 0.42)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(178, 34, 34))
    d.polygon([(bx - 14, by), (bx + bw + 14, by), (bx + bw // 2, by - 26)],
              fill=(120, 20, 20))
    for i in range(5):
        px = bx + 14 + i * (bw - 28) // 4
        d.rectangle([px, by + 10, px + 12, by + bh], fill=(255, 220, 120))
    d.rectangle([bx + bw // 2 - 16, by + bh - 34, bx + bw // 2 + 16, by + bh],
                fill=(40, 20, 20))
    # magnifier of inquiry
    cx, cy = x + int(w * 0.82), y + int(h * 0.30)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=NAVY, width=7)
    d.line([cx + 18, cy + 18, cx + 44, cy + 44], fill=NAVY, width=7)
    d.text((x + 10, y + h - 24), "BEIJING — POLITBURO PROBE",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=NAVY)


def ill_moscow_talks(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for cx in (x + 60, x + int(w * 0.55), x + int(w * 0.85)):
        d.ellipse([cx, y + 26, cx + 70, y + 52], fill=(255, 255, 255))
        d.ellipse([cx + 30, y + 14, cx + 96, y + 40], fill=(255, 255, 255))
    # jet flying right
    jx, jy = x + int(w * 0.30), y + int(h * 0.42)
    d.polygon([(jx, jy), (jx + 130, jy - 8), (jx + 150, jy + 2),
               (jx + 130, jy + 12), (jx, jy + 10)], fill=(240, 240, 240),
              outline=NAVY)
    d.polygon([(jx + 90, jy - 8), (jx + 110, jy - 34), (jx + 122, jy - 8)],
              fill=(200, 40, 40))
    d.polygon([(jx + 30, jy + 10), (jx + 44, jy + 30), (jx + 60, jy + 10)],
              fill=(200, 40, 40))
    for i in range(4):
        d.line([jx - 16 - i * 22, jy + 4, jx - 30 - i * 22, jy + 4],
               fill=(255, 255, 255), width=3)
    # onion domes bottom right
    dx = x + int(w * 0.66)
    d.rectangle([dx, y + h - 52, dx + 120, y + h], fill=(210, 190, 150))
    for ox, col in [(dx + 18, (0, 120, 90)), (dx + 60, (180, 40, 40)),
                    (dx + 102, (0, 90, 160))]:
        d.ellipse([ox - 16, y + h - 84, ox + 16, y + h - 52], fill=col)
        d.polygon([(ox, y + h - 96), (ox, y + h - 84)], fill=GOLD)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + h - 24), "KYIV → MOSCOW — JOINT FLIGHT OFFER",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_coalition(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(236, 228, 205))
    # parliament building
    bx, by = x + int(w * 0.14), y + int(h * 0.30)
    d.rectangle([bx, by, bx + int(w * 0.72), y + h - 40], fill=(240, 236, 224),
                outline=(150, 140, 110), width=3)
    d.polygon([(bx - 10, by), (bx + int(w * 0.72) + 10, by),
               (bx + int(w * 0.36), by - 30)], fill=(180, 170, 140))
    for i in range(6):
        px = bx + 16 + i * 34
        d.rectangle([px, by + 14, px + 12, y + h - 40], fill=(200, 190, 160))
    # handshake, centre
    hx, hy = x + int(w * 0.38), y + int(h * 0.52)
    d.ellipse([hx, hy, hx + 46, hy + 26], fill=(232, 180, 140))
    d.ellipse([hx + 44, hy, hx + 90, hy + 26], fill=(200, 150, 110))
    d.line([hx + 8, hy + 26, hx + 82, hy + 26], fill=(120, 70, 40), width=3)
    d.text((x + 10, y + h - 24), "JERUSALEM — FIRST COALITION DEAL",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 70, 40))


def ill_chess(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 198))
    sq = max(16, (h - 44) // 8)
    ox, oy = x + (w - sq * 8) // 2, y + 12
    for r in range(8):
        for c in range(8):
            col = (250, 246, 235) if (r + c) % 2 == 0 else (60, 70, 90)
            d.rectangle([ox + c * sq, oy + r * sq,
                         ox + (c + 1) * sq, oy + (r + 1) * sq], fill=col)
    # pieces: white king, black queen, pawns
    def piece(cx, cy, col, kind):
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=col,
                  outline=(0, 0, 0), width=2)
        f = font(SANS_B, 15)
        t = kind
        d.text((cx - d.textlength(t, font=f) / 2, cy - 8), t, font=f,
               fill=(255, 255, 255) if col == (20, 20, 20) else (20, 20, 20))
    piece(ox + 4 * sq + 17, oy + 7 * sq + 17, (255, 255, 255), "K")
    piece(ox + 3 * sq + 17, oy + 0 * sq + 17, (20, 20, 20), "Q")
    piece(ox + 4 * sq + 17, oy + 6 * sq + 17, (255, 255, 255), "P")
    piece(ox + 3 * sq + 17, oy + 1 * sq + 17, (20, 20, 20), "P")
    d.text((x + 10, y + h - 24), "GENEVA — GAME 1, DRAW IN 38 MOVES",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(40, 50, 70))


def ill_dhaka(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(250, 220, 170))
    # factory + chimney
    d.rectangle([x + 20, y + int(h * 0.45), x + int(w * 0.62), y + h - 26],
                fill=(170, 90, 60))
    d.rectangle([x + int(w * 0.62), y + int(h * 0.22), x + int(w * 0.70),
                 y + h - 26], fill=(140, 70, 50))
    for i in range(3):
        d.ellipse([x + int(w * 0.63) + i * 4, y + int(h * 0.22) - 18 - i * 14,
                   x + int(w * 0.63) + 26 + i * 4, y + int(h * 0.22) + 2 - i * 14],
                  fill=(220, 220, 220))
    for i in range(4):
        wx = x + 34 + i * 52
        d.rectangle([wx, y + int(h * 0.55), wx + 30, y + int(h * 0.55) + 24],
                    fill=(255, 220, 120))
    # workers, arms raised
    for i, wx in enumerate([x + int(w * 0.74), x + int(w * 0.84)]):
        d.ellipse([wx, y + int(h * 0.55), wx + 22, y + int(h * 0.55) + 22],
                  fill=(232, 180, 140))
        d.rectangle([wx + 2, y + int(h * 0.55) + 22, wx + 20, y + h - 26],
                    fill=(30 + i * 60, 90, 130))
        d.line([wx + 4, y + int(h * 0.55) + 30, wx - 8, y + int(h * 0.45)],
               fill=(232, 180, 140), width=4)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 40, 30))
    d.text((x + 10, y + h - 24), "DHAKA — GARMENT WORKERS CLASH",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_migrants(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(250, 200, 140))                       # sunset sky
    d.ellipse([x + int(w * 0.68), y + 14, x + int(w * 0.68) + 52,
               y + 66], fill=(255, 120, 60))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(20, 70, 110))
    waves(d, x, y + int(h * 0.60), w, (255, 255, 255))
    waves(d, x, y + int(h * 0.76), w, (140, 200, 230))
    # small boat, tilted
    bx, by = x + int(w * 0.30), y + int(h * 0.42)
    d.polygon([(bx, by), (bx + 120, by - 6), (bx + 104, by + 22),
               (bx + 14, by + 26)], fill=(120, 70, 30))
    for i in range(5):
        px = bx + 18 + i * 20
        d.ellipse([px, by - 22, px + 12, by - 10], fill=(232, 180, 140))
    d.line([bx + 60, by - 6, bx + 60, by - 52], fill=(60, 40, 20), width=4)
    d.polygon([(bx + 60, by - 52), (bx + 60, by - 12), (bx + 96, by - 12)],
              fill=(255, 255, 255))
    d.text((x + 10, y + h - 24), "ATLANTIC — CONTACT LOST, ~175 MISSING",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(10, 40, 70))


def ill_abrego(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + 30, y + 18, x + 110, y + 46], fill=(255, 255, 255))
    # passport + plane taking off
    d.rectangle([x + int(w * 0.12), y + int(h * 0.38), x + int(w * 0.42),
                 y + int(h * 0.82)], fill=(18, 38, 74))
    d.ellipse([x + int(w * 0.20), y + int(h * 0.46), x + int(w * 0.34),
               y + int(h * 0.60)], outline=GOLD, width=3)
    d.text((x + int(w * 0.17), y + int(h * 0.64)), "PASSPORT",
           font=font(SANS_B, 14), fill=GOLD)
    jx, jy = x + int(w * 0.55), y + int(h * 0.30)
    d.polygon([(jx, jy), (jx + 110, jy - 26), (jx + 126, jy - 16),
               (jx + 110, jy - 4), (jx, jy + 6)], fill=(240, 240, 240),
              outline=NAVY)
    d.polygon([(jx + 70, jy - 26), (jx + 84, jy - 48), (jx + 94, jy - 26)],
              fill=(200, 40, 40))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + h - 24), "USA — VOLUNTARY DEPARTURE",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_drones(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))                          # night sky
    for sx, sy in [(30, 24), (120, 50), (200, 20), (280, 60), (360, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 70, y + 16, x + w - 30, y + 56], fill=(240, 240, 220))
    # drone swarm + intercepts
    for i, (dx, dy) in enumerate([(0.12, 0.35), (0.30, 0.28), (0.48, 0.40),
                                  (0.64, 0.30), (0.80, 0.42)]):
        cx, cy = x + int(w * dx), y + int(h * dy)
        d.rectangle([cx - 16, cy - 4, cx + 16, cy + 4], fill=(180, 180, 180))
        d.ellipse([cx - 22, cy - 10, cx - 10, cy + 2], outline=(255, 255, 255), width=2)
        d.ellipse([cx + 10, cy - 10, cx + 22, cy + 2], outline=(255, 255, 255), width=2)
        if i % 2 == 0:
            burst(d, cx + 26, cy - 22, 14, (255, 180, 60))
    d.text((x + 10, y + h - 24), "MOSCOW — 699 DRONES DOWNED",
           font=font(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(10, 16, 32))


def ill_gaza(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(232, 200, 150))
    for i, (tx, tw, th) in enumerate([(0.06, 0.16, 0.55), (0.26, 0.13, 0.42),
                                      (0.44, 0.18, 0.60), (0.66, 0.14, 0.48)]):
        bx = x + int(w * tx); bw = int(w * tw); bt = y + h - int(h * th)
        d.rectangle([bx, bt, bx + bw, y + h], fill=(150, 130, 105))
        for wy in range(bt + 10, y + h - 8, 20):
            d.rectangle([bx + 6, wy, bx + 16, wy + 10], fill=(60, 50, 40))
    # smoke columns
    for sx in (x + int(w * 0.30), x + int(w * 0.55), x + int(w * 0.80)):
        for j in range(3):
            d.ellipse([sx - 14 + j * 6, y + 20 + j * 22, sx + 18 + j * 6,
                       y + 52 + j * 22], fill=(120, 115, 110))
    burst(d, x + int(w * 0.52), y + int(h * 0.45), 20, (255, 150, 50))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 55, 40))
    d.text((x + 10, y + h - 24), "GAZA — 6 KILLED IN STRIKES",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_solomon(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + int(h * 0.60), x + w, y + h], fill=SEA)
    waves(d, x, y + int(h * 0.64), w, (255, 255, 255))
    # island with palms
    ix = x + int(w * 0.30)
    d.polygon([(ix, y + int(h * 0.62)), (ix + 60, y + int(h * 0.40)),
               (ix + 150, y + int(h * 0.40)), (ix + 210, y + int(h * 0.62))],
              fill=(90, 160, 90))
    for px, py in [(ix + 70, y + int(h * 0.40)), (ix + 150, y + int(h * 0.40))]:
        d.line([px, py, px + 6, py - 44], fill=(120, 80, 40), width=5)
        for ang in (-50, -20, 10, 40):
            import math
            ex = px + 6 + 30 * math.cos(math.radians(ang - 90))
            ey = py - 44 + 30 * math.sin(math.radians(ang - 90))
            d.line([px + 6, py - 44, ex, ey], fill=(30, 120, 50), width=4)
    # torn pact paper
    d.polygon([(x + int(w * 0.68), y + int(h * 0.30)),
               (x + int(w * 0.92), y + int(h * 0.28)),
               (x + int(w * 0.90), y + int(h * 0.55)),
               (x + int(w * 0.70), y + int(h * 0.58))], fill=(255, 255, 255),
              outline=(150, 150, 150))
    d.line([x + int(w * 0.72), y + int(h * 0.38), x + int(w * 0.88), y + int(h * 0.38)],
           fill=INK, width=2)
    d.line([x + int(w * 0.72), y + int(h * 0.45), x + int(w * 0.88), y + int(h * 0.45)],
           fill=INK, width=2)
    d.line([x + int(w * 0.76), y + int(h * 0.30), x + int(w * 0.84), y + int(h * 0.58)],
           fill=RED, width=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(0, 90, 110))
    d.text((x + 10, y + h - 24), "HONIARA — SECURITY PACT TO END",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_cyber(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 72))
    # cargo ships on a dark sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(14, 60, 100))
    for i, sx in enumerate([0.08, 0.42, 0.72]):
        hx = x + int(w * sx)
        d.rectangle([hx, y + int(h * 0.50), hx + 90, y + int(h * 0.62)],
                    fill=(200, 80, 50) if i != 1 else (60, 140, 180))
        for j in range(3):
            d.rectangle([hx + 8 + j * 28, y + int(h * 0.40), hx + 30 + j * 28,
                         y + int(h * 0.50)], fill=(240, 200, 80))
    # laptop + shield overlay
    lx, ly = x + int(w * 0.30), y + int(h * 0.12)
    d.rectangle([lx, ly, lx + 110, ly + 66], fill=(220, 230, 240),
                outline=(255, 255, 255), width=2)
    d.polygon([(lx - 12, ly + 66), (lx + 122, ly + 66), (lx + 132, ly + 78),
               (lx - 22, ly + 78)], fill=(180, 190, 200))
    d.text((lx + 18, ly + 22), "</> 50", font=font(SANS_B, 20), fill=RED)
    d.ellipse([x + int(w * 0.78), y + int(h * 0.10), x + int(w * 0.78) + 52,
               y + int(h * 0.10) + 52], fill=(255, 200, 60))
    d.text((x + int(w * 0.78) + 18, y + int(h * 0.10) + 14), "!",
           font=font(SANS_B, 24), fill=INK)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(10, 24, 44))
    d.text((x + 10, y + h - 24), "GLOBAL — 50 SHIPS CYBER-PROBED",
           font=font(SANS_B, 13), fill=(255, 255, 255))


ILLUSTRATIONS = {1: ill_riyadh, 2: ill_hormuz, 3: ill_beijing, 4: ill_moscow_talks,
                 5: ill_coalition, 6: ill_chess, 7: ill_dhaka, 8: ill_migrants,
                 9: ill_abrego, 10: ill_drones, 11: ill_gaza, 12: ill_solomon,
                 13: ill_cyber}


def thumb(img, num, box):
    """Render one illustration at 2x into a temp image, then downscale it
    into the small thumbnail box (keeps scenes proportional at small size)."""
    x, y, w, h = box
    tmp = Image.new("RGB", (w * 2, h * 2), PAPER)
    td = ImageDraw.Draw(tmp)
    ILLUSTRATIONS[num](td, (0, 0, w * 2, h * 2))
    img.paste(tmp.resize((w, h), Image.LANCZOS), (x, y))

# ---------------------------------------------------------------- data
# (num, region, source, headline, deck)
FEATURED = [
    (1, "MIDDLE EAST", "REUTERS",
     "Houthi strike hits Riyadh finance-district tower",
     "11 injured; Saudi-led coalition calls it a terrorist attack."),
    (2, "MIDDLE EAST", "REUTERS",
     "ADNOC ship hit by mine in Strait of Hormuz",
     "One crew member missing, 11 hurt; Iran says it is the fourth tanker mined."),
    (3, "ASIA", "REUTERS",
     "China probes Politburo member Chen Jining",
     "Fourth top leader investigated since 2025, Xinhua confirms."),
    (4, "EUROPE", "REUTERS",
     "Lukashenko invites Zelenskyy to fly together to Moscow",
     "Offer of joint flight for talks with Putin."),
    (5, "MIDDLE EAST", "REUTERS",
     "Eisenkot seals first coalition deal with Lieberman",
     "Netanyahu–Eisenkot talks enter a third round."),
    (6, "EUROPE", "FIDE",
     "Gukesh vs Sindarov, Game 1 drawn in 38 moves",
     "World title match opens in Geneva."),
    (7, "ASIA", "REUTERS",
     "Bangladesh garment workers clash with police",
     "Factories shut as protests spread."),
    (8, "AFRICA", "REUTERS",
     "~175 migrants missing after boat contact lost",
     "Vessel left Senegal; search under way."),
    (9, "AMERICAS", "REUTERS",
     "Kilmar Abrego Garcia leaves US voluntarily",
     "Long-running deportation case ends in departure."),
    (10, "EUROPE", "REUTERS",
     "Russia claims 699 Ukrainian drones downed overnight",
     "355 were heading for Moscow, officials say."),
    (11, "MIDDLE EAST", "ANADOLU",
     "Gaza: 6 killed in Israeli strikes",
     "Hamas internal security chief among the dead."),
    (12, "OCEANIA", "SMH / RNZ",
     "Solomon Islands to end security pact with China",
     "Pacific pivot as Honiara reviews the deal."),
    (13, "GLOBAL", "WSJ VIA REUTERS",
     "US probes cyberattacks on 50 merchant ships",
     "Iran suspected in the fleet-wide intrusions."),
]

ALSO_ON = [
    (14, "Yemen army: Houthis will not take Aden", "REUTERS"),
    (15, "UK sanctions Houthis + 4 officials", "ANADOLU"),
    (16, "Serbia school shooting, 2 hurt, teen held", "ANADOLU"),
    (17, "RSF defectors join Sudan army in Khartoum", "ANADOLU"),
    (18, "Bangladesh rejects Hasina return demand", "ANADOLU"),
    (19, "Israeli post blocks Syrian farmers, Quneitra", "ANADOLU"),
    (20, "Australia's Wong warns on US–China rivalry", "ANADOLU"),
    (21, "Gill asks ICC to review saliva ban", "MYKHEL"),
    (22, "Babar Azam shines on ILT20 debut", "MYKHEL"),
    (23, "Russian strike on Zaporizhzhia kills 2", "REUTERS"),
    (24, "Russian drone briefly enters Polish airspace", "REUTERS"),
    (25, "US court lets army blast toxic explosives in Iowa", "REUTERS"),
    (26, "Iran: no US talks until terms met", "REUTERS"),
    (27, "NATO pledges defence from space threats", "REUTERS"),
    (28, "'El Chapo Isidro' tried in Mexico despite US plea", "REUTERS"),
    (29, "Lahore most polluted major city, AQI 538", "—"),
    (30, "Netanyahu–Eisenkot, third coalition round", "—"),
    (31, "Trump hosts gala as $TRUMP coin falls 99%", "—"),
    (32, "Iraq auctions two Saddam-era Boeing 747s", "RAHNUMA"),
    (33, "US Democrats: 2028 hopefuls must reject dark money", "REUTERS"),
    (34, "US weighs military training for Syrian forces", "REUTERS"),
    (35, "Nikkei +3.9% Tuesday; Nvidia −5% premarket", "REUTERS"),
]

STATS = [("699", "drones downed\nin one night"),
         ("175", "migrants missing\nafter boat lost"),
         ("538", "AQI in Lahore,\nworld's worst"),
         ("11", "injured in\nRiyadh strike"),
         ("50", "ships probed\nin cyberattacks"),
         ("+3.9%", "Nikkei gain\non Tuesday")]

DATE_CHECK = ("DATE CHECK — deliberately left out: COP31 collapsed (22 Nov) · "
              "Huang returns, Nvidia +31.5% (23 Nov) · Ukraine sinks Russian warship off Libya "
              "(22–23 Nov) · NATO AWACS to Poland (23 Nov) · CrowdStrike buys Zscaler $44bn "
              "(23 Nov) · Indonesia factory fire, 24 dead (21 Nov).")

# map pins: (x, dy) where dy is offset below the top edge of the map band
PINS = {1: (915, 75), 2: (945, 100), 3: (1170, 45), 4: (828, 18),
        5: (858, 92), 6: (795, 35), 7: (1105, 80), 8: (640, 105),
        9: (330, 45), 10: (878, 16), 11: (900, 125), 12: (1395, 165),
        13: (520, 145)}

# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 40                      # side margin
    CW = W - 2 * MX              # content width

    # ---- nameplate ------------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=NAVY)
    f_kick = font(SANS_B, 17)
    centre(d, W // 2, 22, "TUESDAY 24 NOVEMBER 2026  ·  WORLD NEWS IN ONE IMAGE",
           f_kick, fill=NAVY)
    f_title = font(SERIF_B, 76)
    centre(d, W // 2, 52, "THE WORLD IN ONE DAY", f_title, fill=INK)
    f_sub = font(SANS, 19)
    centre(d, W // 2, 140,
           "35 STORIES  ·  7 REGIONS  ·  EVERY STORY FIRST REPORTED ON TUESDAY 24 NOVEMBER 2026",
           f_sub, fill=(70, 70, 70))
    d.line([MX, 172, W - MX, 172], fill=RULE, width=2)
    d.line([MX, 177, W - MX, 177], fill=RULE, width=1)

    # ---- stat strip ------------------------------------------------------
    y = 190
    f_sec = font(SANS_B, 16)
    d.text((MX, y), "THE DAY IN NUMBERS", font=f_sec, fill=RED)
    d.line([MX + 210, y + 10, W - MX, y + 10], fill=(200, 190, 160), width=1)
    y += 26
    box_w = (CW - 5 * 12) // 6
    f_num = font(SERIF_B, 34)
    f_lab = font(SANS, 14)
    for i, (num, lab) in enumerate(STATS):
        bx = MX + i * (box_w + 12)
        d.rectangle([bx, y, bx + box_w, y + 68], fill=CARD,
                    outline=(200, 190, 160), width=1)
        centre(d, bx + box_w // 2, y + 2, num, f_num, fill=NAVY)
        for j, ln in enumerate(lab.split("\n")):
            centre(d, bx + box_w // 2, y + 38 + j * 14, ln, f_lab,
                   fill=(80, 80, 80))
    y += 68 + 14

    # ---- 3 lead stories --------------------------------------------------
    d.text((MX, y), "TOP STORIES", font=f_sec, fill=RED)
    d.line([MX + 130, y + 10, W - MX, y + 10], fill=(200, 190, 160), width=1)
    y += 26
    lead_y = y
    lead_w = (CW - 2 * 16) // 3
    lead_h = 452
    f_head = font(SERIF_B, 25)
    f_deck = font(SANS, 16)
    f_tag = font(SANS_B, 12)
    for idx, (num, region, src, head, deck) in enumerate(FEATURED[:3]):
        lx = MX + idx * (lead_w + 16)
        d.rectangle([lx, lead_y, lx + lead_w, lead_y + lead_h], fill=CARD,
                    outline=(190, 180, 155), width=1)
        ILLUSTRATIONS[num](d, (lx + 1, lead_y + 1, lead_w - 2, 218))
        badge(d, lx + 12, lead_y + 226, num)
        d.text((lx + 56, lead_y + 232), region, font=f_tag, fill=RED)
        d.text((lx + 56, lead_y + 250), "SOURCE: " + src, font=f_tag,
               fill=(110, 110, 110))
        ty = draw_wrapped(d, lx + 14, lead_y + 272, head, f_head, lead_w - 28,
                          leading=30)
        draw_wrapped(d, lx + 14, ty + 4, deck, f_deck, lead_w - 28, leading=21,
                     fill=(70, 70, 70))
    y = lead_y + lead_h + 16

    # ---- 10 small featured stories ---------------------------------------
    d.text((MX, y), "MORE OF THE DAY — 10 FEATURED STORIES", font=f_sec, fill=RED)
    d.line([MX + 360, y + 10, W - MX, y + 10], fill=(200, 190, 160), width=1)
    y += 26
    small_y = y
    row_h = 112
    col_w = (CW - 16) // 2
    f_shead = font(SERIF_B, 19)
    f_sdeck = font(SANS, 14)
    for i, (num, region, src, head, deck) in enumerate(FEATURED[3:]):
        col = i % 2
        row = i // 2
        sx = MX + col * (col_w + 16)
        sy = small_y + row * row_h
        d.rectangle([sx, sy, sx + col_w, sy + row_h - 8], fill=CARD,
                    outline=(200, 190, 160), width=1)
        thumb(img, num, (sx + 1, sy + 1, 168, row_h - 10))
        badge(d, sx + 176, sy + 8, num, d=28)
        d.text((sx + 212, sy + 12), region + "  ·  " + src, font=f_tag,
               fill=RED)
        ty = draw_wrapped(d, sx + 212, sy + 32, head, f_shead, col_w - 226,
                          leading=22)
        draw_wrapped(d, sx + 212, ty + 2, deck, f_sdeck, col_w - 226,
                     leading=18, fill=(70, 70, 70))
    y = small_y + 5 * row_h + 8

    # ---- world map ---------------------------------------------------------
    d.text((MX, y), "WHERE IT HAPPENED — 13 FEATURED STORIES PINNED", font=f_sec,
           fill=RED)
    d.line([MX + 470, y + 10, W - MX, y + 10], fill=(200, 190, 160), width=1)
    y += 26
    map_y = y
    map_h = 226
    d.rectangle([MX, map_y, W - MX, map_y + map_h], fill=(214, 232, 242),
                outline=(170, 190, 205), width=1)
    # stylised continents (flat, labelled)
    cont = (120, 160, 105)
    d.polygon([(250, map_y + 55), (330, map_y + 40), (430, map_y + 55),
               (450, map_y + 110), (380, map_y + 150), (290, map_y + 140),
               (240, map_y + 100)], fill=cont)                       # N America
    d.polygon([(380, map_y + 165), (440, map_y + 160), (470, map_y + 200),
               (430, map_y + 225), (390, map_y + 200)], fill=cont)   # S America
    d.polygon([(700, map_y + 45), (790, map_y + 35), (850, map_y + 60),
               (840, map_y + 105), (760, map_y + 120), (700, map_y + 90)],
              fill=cont)                                              # Europe
    d.polygon([(760, map_y + 130), (850, map_y + 125), (900, map_y + 160),
               (870, map_y + 200), (800, map_y + 195), (760, map_y + 165)],
              fill=cont)                                              # Africa
    d.polygon([(880, map_y + 55), (1080, map_y + 40), (1230, map_y + 70),
               (1200, map_y + 130), (1050, map_y + 150), (900, map_y + 120)],
              fill=cont)                                              # Asia
    d.polygon([(1300, map_y + 170), (1420, map_y + 165), (1450, map_y + 200),
               (1360, map_y + 215), (1290, map_y + 195)], fill=cont) # Oceania
    f_map = font(SANS_B, 13)
    for txt, tx, ty in [("N. AMERICA", 255, map_y + 82), ("S. AMERICA", 372, map_y + 180),
                        ("EUROPE", 735, map_y + 66), ("AFRICA", 775, map_y + 152),
                        ("ASIA", 1010, map_y + 86), ("OCEANIA", 1315, map_y + 182),
                        ("ATLANTIC", 500, map_y + 110), ("PACIFIC", 1240, map_y + 130)]:
        d.text((tx, ty), txt, font=f_map, fill=(90, 110, 90))
    for num, (px, dy) in PINS.items():
        badge(d, px - 14, map_y + dy - 14, num, d=28)
    y = map_y + map_h + 14

    # ---- also-on list ------------------------------------------------------
    d.text((MX, y), "ALSO ON — 22 MORE STORIES  (Nos. 14–35)", font=f_sec, fill=RED)
    d.line([MX + 380, y + 10, W - MX, y + 10], fill=(200, 190, 160), width=1)
    y += 26
    list_y = y
    f_list = font(SANS, 16)
    f_lnum = font(SANS_B, 16)
    f_lsrc = font(SANS, 12)
    for i, (num, head, src) in enumerate(ALSO_ON):
        col = i % 2
        row = i // 2
        lx = MX + col * (col_w + 16)
        ly = list_y + row * 26
        d.text((lx, ly), f"{num}.", font=f_lnum, fill=NAVY)
        d.text((lx + 36, ly), head, font=f_list, fill=INK)
        tw = d.textlength(head, font=f_list)
        d.text((lx + 36 + tw + 8, ly + 2), src, font=f_lsrc, fill=(130, 130, 130))
    y = list_y + 11 * 26 + 10

    # ---- date check --------------------------------------------------------
    d.rectangle([MX, y, W - MX, y + 56], fill=(255, 244, 220),
                outline=RED, width=2)
    f_dc = font(SANS, 14)
    d.text((MX + 12, y + 6), "DATE CHECK — WHY THESE STORIES ARE NOT HERE:",
           font=font(SANS_B, 13), fill=RED)
    draw_wrapped(d, MX + 12, y + 24, DATE_CHECK.split("— ", 1)[1], f_dc,
                 CW - 24, leading=17)
    y += 56 + 12

    # ---- footer ------------------------------------------------------------
    d.line([MX, y, W - MX, y], fill=RULE, width=2)
    y += 8
    centre(d, W // 2, y,
           "All 35 stories first reported Tuesday 24 November 2026  ·  Sources: Reuters, Anadolu, FIDE, SMH/RNZ, WSJ, myKhel, Rahnuma",
           font(SANS, 14), fill=(70, 70, 70))
    centre(d, W // 2, y + 20,
           "THE WORLD IN ONE DAY — make.fun bounty news-image-20261124  ·  $100 prize, top 50  ·  Entries close 26 Nov 2026, 07:00 WIB",
           font(SANS_B, 13), fill=NAVY)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, "PNG")
    print(f"saved {OUT_PATH}  {W}x{H}")


if __name__ == "__main__":
    main()
