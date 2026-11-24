"""make.fun news page v2, Monday 23 November 2026: "The Monday Ledger" redesign (1024x1024).

31 stories, 6 regions. Legibility-first redesign of v1 (43 stories, R2 64.08%):
fewer stories, bigger everything, NO text below 10px anywhere, 3 huge leads with
red banner headlines, 10 small panels (2 rows x 5), one world map + Europe /
Middle East insets with ALL 31 stories pinned (numbered), 2-column ALSO list,
DATE CHECK box, UTC strip, region bar, 6-number data strip. Cream broadsheet,
navy masthead, red accents. Pure PIL, no network, no randomness.
Usage: python3 draw_v2.py [output_path]   (default: entry_v2.png next to this file)
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FLOOR = 10  # no text smaller than 10px anywhere on the page
FL = "/usr/share/fonts/truetype/liberation/"
F = {
    "sb": FL + "LiberationSans-Bold.ttf",
    "s": FL + "LiberationSans-Regular.ttf",
    "si": FL + "LiberationSans-Italic.ttf",
    "xb": FL + "LiberationSerif-Bold.ttf",
    "x": FL + "LiberationSerif-Regular.ttf",
    "xi": FL + "LiberationSerif-Italic.ttf",
}
_fc = {}


def font(k, s):
    key = (k, s)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(F[k], s)
    return _fc[key]


PAPER = (247, 242, 231)
PANEL = (252, 249, 241)
INK = (22, 22, 26)
GREY = (84, 84, 90)
RULE = (30, 30, 34)
NAVY = (15, 36, 64)
RED = (176, 30, 36)
SEA = (178, 203, 222)
LAND = (208, 188, 148)

CAT = {  # category colours (kicker chips, map pins, region chips)
    "WAR": (176, 30, 36),
    "POL": (30, 78, 160),
    "SCI": (28, 126, 82),
    "ECO": (196, 118, 10),
    "SOC": (118, 60, 150),
    "SPT": (0, 128, 140),
}
CERT = {  # certainty tags
    "REPORTED": (28, 126, 82),
    "CLAIM": (176, 30, 36),
    "FORECAST": (196, 118, 10),
}

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
WARN = []


def tw(t, f):
    return d.textlength(t, font=f)


def wrap(t, f, w):
    out, cur = [], ""
    for word in t.split():
        trial = (cur + " " + word).strip()
        if tw(trial, f) <= w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(x, y, w, t, fk, fs, fill, lh=None, maxlines=None, tag=""):
    assert fs >= FLOOR, f"{tag}: font {fs} below floor {FLOOR}"
    f = font(fk, fs)
    lh = lh or int(fs * 1.2)
    lines = wrap(t, f, w)
    if maxlines and len(lines) > maxlines:
        WARN.append(f"{tag}: {len(lines)}>{maxlines} lines: {t[:40]}")
        lines = lines[:maxlines]
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def fit_text(x, y, w, t, fk, fs, fill, anchor="la", minsize=FLOOR, tag=""):
    assert minsize >= FLOOR, f"{tag}: minsize {minsize} below floor"
    s0 = fs
    while tw(t, font(fk, fs)) > w and fs > minsize:
        fs -= 1
    if tag and fs < s0:
        WARN.append(f"{tag}: shrank {s0}->{fs}: {t[:40]}")
    if tw(t, font(fk, fs)) > w:
        WARN.append(f"{tag}: STILL OVERFLOWS at floor {fs}: {t[:40]}")
    d.text((x, y), t, font=font(fk, fs), fill=fill, anchor=anchor)


def rule(x1, y1, x2, y2, w=1, c=RULE):
    d.line([x1, y1, x2, y2], fill=c, width=w)


def kicker(x, y, w, h, text, col=RED):
    """Red kicker chip with white bold text, full width of the panel art."""
    d.rectangle([x, y, x + w, y + h], fill=col)
    fit_text(x + w / 2, y + h / 2, w - 6, text, "sb", max(h - 4, FLOOR), (255, 255, 255),
             anchor="mm", minsize=FLOOR, tag="kicker")


def cert_tag(x, y, tag):
    """Certainty tag (REPORTED green / CLAIM red / FORECAST amber), right-aligned."""
    col = CERT[tag]
    f = font("sb", FLOOR)
    w = int(tw(tag, f)) + 10
    d.rounded_rectangle([x - w, y, x, y + 13], 2, fill=col)
    d.text((x - w + 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return x - w


def art_label(x, y, text, anchor="lb"):
    """Place label inside art: 10px bold white, the floor size."""
    d.text((x, y), text, font=font("sb", FLOOR), fill=(255, 255, 255), anchor=anchor)


# ------------------------------------------------------------------ art helpers
def sky(x, y, w, h, c1, c2):
    for i in range(h):
        t = i / max(1, h - 1)
        col = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([x, y + i, x + w - 1, y + i], fill=col)


def burst(cx, cy, r, c1=(255, 200, 60), c2=(255, 255, 220)):
    for i in range(10):
        a = i * math.pi / 5
        d.line([cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r], fill=c1, width=2)
    d.ellipse([cx - r * .5, cy - r * .5, cx + r * .5, cy + r * .5], fill=c1)
    d.ellipse([cx - r * .28, cy - r * .28, cx + r * .28, cy + r * .28], fill=c2)


def skyline(x, y, w, h, base, lit=(255, 214, 110), seed=3):
    bw = 12
    cx = x + 2
    k = seed
    while cx < x + w - 6:
        k = (k * 37 + 11) % 97
        bh = 14 + (k % 30) * h // 50
        d.rectangle([cx, y + h - bh, cx + bw, y + h], fill=base)
        for wy in range(y + h - bh + 4, y + h - 3, 6):
            for wx in (cx + 2, cx + 7):
                if (wx + wy + k) % 3:
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill=lit)
        cx += bw + 2


# ------------------------------------------------------------------ art (13 originals, one per panel, never reused)
def art_bahrain(x, y, w, h):
    """Lead 1: Bahrain at night — Gulf, island, industrial fire, missile streak.
    Bigger and brighter than v1: pale moon, lit skyline, clear island."""
    sky(x, y, w, h, (20, 32, 72), (72, 62, 96))
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(240, 232, 200))
    d.ellipse([x + w - 46, y + 12, x + w - 28, y + 30], fill=(214, 204, 168))
    skyline(x, y + h - 46, w, 30, (40, 44, 66))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(52, 100, 150))
    d.polygon([(x + 12, y + h - 16), (x + w - 12, y + h - 16), (x + w - 24, y + h - 28), (x + 22, y + h - 28)], fill=(206, 190, 150))
    d.rectangle([x + 30, y + h - 36, x + 58, y + h - 28], fill=(90, 92, 100))
    d.rectangle([x + 62, y + h - 32, x + 84, y + h - 28], fill=(78, 80, 90))
    burst(x + 70, y + h - 26, 11)
    d.ellipse([x + 62, y + h - 46, x + 80, y + h - 28], fill=(96, 96, 104))
    d.line([x + w - 6, y + 4, x + 74, y + h - 46], fill=(255, 200, 90), width=2)
    d.rectangle([x + w - 46, y + h - 42, x + w - 8, y + h - 28], fill=(60, 70, 96))
    d.text((x + w - 27, y + h - 35), "US 5th", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="mm")
    art_label(x + 2, y + h - 4, "SITRA · MANAMA")


def art_cop(x, y, w, h):
    """Lead 2: climate talks collapse — long table, delegates, globe, clock past closing."""
    sky(x, y, w, h, (176, 222, 214), (230, 240, 226))
    d.ellipse([x + 10, y + 8, x + 52, y + 50], fill=(52, 118, 190))
    d.polygon([(x + 20, y + 18), (x + 36, y + 14), (x + 44, y + 26), (x + 32, y + 38), (x + 18, y + 32)], fill=(70, 150, 90))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h], fill=(120, 150, 130))
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 14], fill=(96, 74, 52))
    for bx in range(x + 26, x + w - 24, 30):
        d.ellipse([bx, y + h - 46, bx + 14, y + h - 32], fill=(60, 44, 30))
        d.rectangle([bx + 2, y + h - 32, bx + 12, y + h - 26], fill=(40, 32, 24))
    cx, cy = x + w - 32, y + 26
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(255, 255, 255), outline=INK, width=2)
    d.line([cx, cy, cx, cy - 14], fill=INK, width=2)
    d.line([cx, cy, cx + 12, cy + 5], fill=(200, 40, 30), width=2)
    d.text((x + w // 2 - 24, y + 8), "NO DEAL", font=font("sb", 11), fill=(176, 30, 36), anchor="ma")
    art_label(x + 2, y + h - 4, "ANTALYA")


def art_house(x, y, w, h):
    """Lead 3: US Capitol dome + seat bars (Democrats 258, the largest since 1992)."""
    sky(x, y, w, h, (30, 78, 160), (120, 170, 220))
    cx = x + w // 2
    d.polygon([(cx - 40, y + h - 20), (cx - 40, y + 30), (cx + 40, y + 30), (cx + 40, y + h - 20)], fill=(240, 240, 235))
    d.ellipse([cx - 20, y + 8, cx + 20, y + 34], fill=(240, 240, 235))
    d.rectangle([cx - 1, y + 2, cx + 1, y + 10], fill=(240, 240, 235))
    d.polygon([(cx + 1, y + 2), (cx + 10, y + 5), (cx + 1, y + 8)], fill=(176, 30, 36))
    for bx in range(cx - 36, cx + 36, 10):
        d.rectangle([bx, y + 34, bx + 6, y + h - 20], fill=(200, 200, 195))
    d.rectangle([x, y + h - 20, x + w, y + h - 16], fill=(200, 200, 195))
    bw = (w - 16) / 2
    d.rectangle([x + 8, y + h - 14, x + 8 + bw, y + h - 5], fill=(30, 78, 160))
    d.rectangle([x + 8 + bw + 2, y + h - 11, x + w - 8, y + h - 5], fill=(176, 30, 36))
    d.text((x + 10, y + h - 10), "258", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="lb")
    d.text((x + 2, y + 2), "WASHINGTON", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="la")


def art_ship_finland(x, y, w, h):
    """Panel 4: container ship burning in the Gulf of Finland."""
    sky(x, y, w, h, (190, 218, 238), (240, 232, 214))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(52, 100, 150))
    d.polygon([(x + 14, y + h - 12), (x + w - 18, y + h - 12), (x + w - 28, y + h - 22), (x + 24, y + h - 22)], fill=INK)
    for cx0, col in ((x + 34, (176, 30, 36)), (x + 52, (30, 78, 160)), (x + 70, (196, 118, 10))):
        d.rectangle([cx0, y + h - 28, cx0 + 14, y + h - 22], fill=col)
    burst(x + 88, y + h - 20, 7)
    d.ellipse([x + 80, y + h - 26, x + 96, y + h - 18], fill=(120, 120, 128))
    dx, dy = x + w - 30, y + 8
    d.ellipse([dx, dy, dx + 18, dy + 7], fill=(30, 34, 42))
    d.line([dx - 5, dy + 2, dx + 23, dy + 2], fill=(30, 34, 42), width=2)
    art_label(x + 2, y + h - 4, "GULF OF FINLAND")


def art_kyiv_block(x, y, w, h):
    """Panel 6: apartment block hit by a drone — cracked facade, smoke, drone."""
    sky(x, y, w, h, (70, 80, 96), (140, 150, 160))
    d.rectangle([x + 18, y + 4, x + w - 18, y + h], fill=(150, 140, 125))
    for wy in range(y + 8, y + h - 4, 10):
        for wx in range(x + 24, x + w - 24, 12):
            d.rectangle([wx, wy, wx + 6, wy + 6], fill=(60, 60, 66))
    d.polygon([(x + w // 2 - 8, y + 4), (x + w // 2 + 10, y + 18), (x + w // 2 + 4, y + h - 10), (x + w // 2 - 14, y + h - 6)], fill=(40, 40, 46))
    d.ellipse([x + w // 2 - 4, y + 2, x + w // 2 + 14, y + 18], fill=(120, 120, 128))
    burst(x + w // 2 + 2, y + 12, 8)
    dx, dy = x + w - 26, y + 6
    d.ellipse([dx, dy, dx + 16, dy + 6], fill=(30, 34, 42))
    d.line([dx - 4, dy + 2, dx + 20, dy + 2], fill=(30, 34, 42), width=2)
    art_label(x + 2, y + h - 4, "KYIV REGION")


def art_factory_fire(x, y, w, h):
    """Panel 7: candy factory ablaze in Cikande — sawtooth roof, flames, smoke."""
    sky(x, y, w, h, (214, 198, 168), (240, 232, 214))
    d.polygon([(x + 6, y + h - 8), (x + 6, y + 14), (x + 30, y + 6), (x + 54, y + 14), (x + 78, y + 6), (x + w - 6, y + 14), (x + w - 6, y + h - 8)], fill=(96, 74, 52))
    d.rectangle([x + 6, y + h - 8, x + w - 6, y + h], fill=(120, 100, 80))
    for fx in (x + 22, x + w // 2, x + w - 30):
        d.polygon([(fx - 8, y + h - 8), (fx, y + h - 26), (fx + 8, y + h - 8)], fill=(255, 120, 30))
        d.polygon([(fx - 4, y + h - 8), (fx, y + h - 20), (fx + 4, y + h - 8)], fill=(255, 200, 60))
    d.ellipse([x + w // 2 - 10, y + 2, x + w // 2 + 10, y + 18], fill=(120, 120, 128))
    art_label(x + 2, y + h - 4, "CIKANDE")


def art_airport(x, y, w, h):
    """Panel 8: airport terminal with control tower and a plane tail."""
    sky(x, y, w, h, (190, 218, 238), (240, 232, 214))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(96, 100, 110))
    d.rectangle([x + 6, y + h - 22, x + w - 40, y + h - 10], fill=(200, 200, 195))
    for wx in range(x + 12, x + w - 46, 14):
        d.rectangle([wx, y + h - 19, wx + 8, y + h - 13], fill=(30, 78, 160))
    d.rectangle([x + w - 30, y + 4, x + w - 22, y + h - 10], fill=(60, 60, 66))
    d.ellipse([x + w - 32, y + 2, x + w - 20, y + 12], fill=(120, 170, 220), outline=INK)
    d.polygon([(x + w - 52, y + h - 10), (x + w - 44, y + h - 24), (x + w - 38, y + h - 10)], fill=(176, 30, 36))
    art_label(x + 2, y + h - 4, "OLYMPIA")


def art_seoul_exam(x, y, w, h):
    """Panel 9: exam hall — desks, papers, a laptop flashing a warning."""
    sky(x, y, w, h, (214, 226, 236), (240, 244, 248))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 130, 100))
    for dx0 in (x + 10, x + w // 2 - 12, x + w - 34):
        d.rectangle([dx0, y + h - 20, dx0 + 24, y + h - 10], fill=(96, 74, 52))
        d.rectangle([dx0 + 4, y + h - 26, dx0 + 20, y + h - 20], fill=(255, 255, 255))
    lx, ly = x + w // 2 - 10, y + 6
    d.rectangle([lx, ly, lx + 20, ly + 12], fill=(30, 34, 42))
    d.polygon([(lx + 10, ly + 2), (lx + 16, ly + 10), (lx + 4, ly + 10)], fill=(255, 205, 60))
    d.text((lx + 10, ly + 6), "!", font=font("sb", FLOOR), fill=(30, 34, 42), anchor="mm")
    art_label(x + 2, y + h - 4, "SEOUL")


def art_delhi(x, y, w, h):
    """Panel 11: India Gate arch with the Indian and Nepali flags."""
    sky(x, y, w, h, (240, 200, 140), (250, 230, 190))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(150, 120, 80))
    ax, ay = x + w // 2 - 18, y + 6
    d.rectangle([ax, ay, ax + 36, y + h - 10], fill=(190, 120, 60))
    d.polygon([(ax - 4, ay), (ax + 18, y), (ax + 40, ay)], fill=(160, 90, 40))
    d.rectangle([ax + 13, y + 12, ax + 23, y + h - 10], fill=(240, 200, 140))
    for fx, col in ((x + 8, (255, 153, 51)), (x + w - 20, (220, 20, 60))):
        d.line([fx + 4, y + 4, fx + 4, y + h - 10], fill=INK, width=1)
        d.rectangle([fx + 4, y + 4, fx + 16, y + 12], fill=col)
    art_label(x + 2, y + h - 4, "NEW DELHI")


def art_cricket(x, y, w, h):
    """Panel 12: cricket — bat, ball, stumps and the 720/9 scoreboard."""
    sky(x, y, w, h, (28, 126, 82), (120, 200, 140))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(60, 140, 80))
    d.rectangle([x + w - 56, y + 4, x + w - 6, y + 18], fill=(20, 24, 36))
    d.text((x + w - 31, y + 11), "720/9", font=font("sb", FLOOR), fill=(255, 220, 60), anchor="mm")
    bx, by = x + 20, y + 8
    d.rectangle([bx, by, bx + 6, by + 14], fill=(200, 160, 100))
    d.rectangle([bx + 2, by + 14, bx + 4, y + h], fill=(120, 90, 60))
    d.ellipse([x + w // 2 - 4, y + h - 18, x + w // 2 + 4, y + h - 10], fill=(176, 30, 36))
    for sx in (x + w // 2 - 12, x + w // 2, x + w // 2 + 12):
        d.line([sx, y + h - 22, sx, y + h - 10], fill=(255, 255, 255), width=2)
    art_label(x + 2, y + h - 4, "WELLINGTON")


def art_f1(x, y, w, h):
    """Panel 13: Las Vegas GP — track curve, race car, checkered flag."""
    sky(x, y, w, h, (14, 22, 52), (52, 40, 70))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 40, 46))
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(255, 255, 255), width=1)
    for i in range(0, w, 16):
        d.rectangle([x + i, y + h - 16, x + i + 8, y + h - 14], fill=(176, 30, 36) if (i // 16) % 2 else (255, 255, 255))
    cx, cy = x + w // 2 - 16, y + 4
    d.rectangle([cx, cy, cx + 32, cy + 8], fill=(200, 30, 40))
    d.rectangle([cx + 8, cy - 4, cx + 20, cy], fill=(200, 30, 40))
    for wx in (cx + 4, cx + 24):
        d.ellipse([wx, cy + 6, wx + 6, cy + 12], fill=(20, 20, 22))
    fx = x + w - 16
    for r in range(2):
        for c in range(2):
            d.rectangle([fx + c * 5, y + 4 + r * 5, fx + c * 5 + 5, y + 9 + r * 5],
                        fill=(20, 20, 22) if (r + c) % 2 else (255, 255, 255))
    d.line([fx + 2, y + 14, fx + 2, y + 24], fill=INK, width=1)
    art_label(x + 2, y + h - 4, "LAS VEGAS")


def art_lisbon(x, y, w, h):
    """Panel 14: Lisbon march — crowd heads and placards on a street."""
    sky(x, y, w, h, (240, 200, 140), (250, 230, 190))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 110, 100))
    for hx in range(x + 8, x + w - 8, 16):
        d.ellipse([hx, y + h - 26, hx + 10, y + h - 16], fill=(60, 44, 30))
        d.rectangle([hx + 1, y + h - 16, hx + 9, y + h - 10], fill=(30, 78, 160))
    for px in (x + 24, x + w // 2, x + w - 34):
        d.rectangle([px - 10, y + 4, px + 10, y + 14], fill=(255, 255, 255), outline=INK)
        d.line([px, y + 14, px, y + 22], fill=INK, width=2)
    d.text((x + w // 2, y + 9), "!", font=font("sb", FLOOR), fill=(176, 30, 36), anchor="mm")
    art_label(x + 2, y + h - 4, "LISBON")


def art_juba(x, y, w, h):
    """Panel 15: South Sudan savanna — acacia, hut, smoke on the horizon."""
    sky(x, y, w, h, (240, 200, 140), (250, 230, 190))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(190, 160, 100))
    d.line([x + 14, y + 8, x + 14, y + h - 12], fill=(80, 60, 40), width=2)
    d.ellipse([x + 2, y + 2, x + 26, y + 10], fill=(60, 120, 60))
    d.polygon([(x + w - 44, y + h - 12), (x + w - 30, y + h - 28), (x + w - 16, y + h - 12)], fill=(150, 110, 60))
    d.rectangle([x + w - 38, y + h - 20, x + w - 22, y + h - 12], fill=(120, 90, 60))
    d.ellipse([x + w // 2 - 8, y + 4, x + w // 2 + 8, y + 16], fill=(120, 120, 128))
    art_label(x + 2, y + h - 4, "JUBA")


ART = {"bahrain": art_bahrain, "cop": art_cop, "house": art_house,
       "ship_finland": art_ship_finland, "kyiv": art_kyiv_block,
       "factory": art_factory_fire, "airport": art_airport, "seoul": art_seoul_exam,
       "delhi": art_delhi, "cricket": art_cricket, "f1": art_f1,
       "lisbon": art_lisbon, "juba": art_juba}

# ------------------------------------------------------------------ content (31 stories, 6 regions)
# Region counts must match the masthead: EUROPE 8, MIDDLE EAST 5, AMERICAS 6,
# ASIA-PACIFIC 7, AFRICA 4, OCEANIA 1. Story 5 (Libya port) counts as AFRICA;
# story 12 (India 720/9 in NZ) counts as ASIA-PACIFIC (India subject);
# story 43 (NZ retail sales) counts as OCEANIA.
REGION_OF = {
    1: "MIDDLE EAST", 2: "EUROPE", 3: "AMERICAS", 4: "EUROPE", 5: "AFRICA",
    6: "EUROPE", 7: "ASIA-PACIFIC", 8: "AMERICAS", 9: "ASIA-PACIFIC", 10: "AMERICAS",
    11: "ASIA-PACIFIC", 12: "ASIA-PACIFIC", 13: "AMERICAS",
    14: "EUROPE", 15: "AFRICA",
    16: "MIDDLE EAST", 17: "MIDDLE EAST", 18: "MIDDLE EAST", 20: "MIDDLE EAST",
    23: "EUROPE", 24: "EUROPE", 25: "EUROPE", 26: "EUROPE",
    28: "AMERICAS", 31: "AMERICAS",
    33: "ASIA-PACIFIC", 36: "ASIA-PACIFIC", 38: "ASIA-PACIFIC",
    41: "AFRICA", 42: "AFRICA", 43: "OCEANIA",
}
REGCOL = {"EUROPE": (30, 78, 160), "MIDDLE EAST": (176, 30, 36),
          "AMERICAS": (118, 60, 150), "ASIA-PACIFIC": (0, 128, 140),
          "AFRICA": (28, 126, 82), "OCEANIA": (232, 128, 20)}
REGIONS = ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA-PACIFIC", "AFRICA", "OCEANIA"]
STORY_IDS = sorted(REGION_OF)

DATA = [
    ("258", "House seats for Democrats,\nlargest majority since 1992"),
    ("0", "mentions of 'fossil fuels'\nin the COP31 draft"),
    ("2", "US radars Iran claims\nto have hit (CLAIM)"),
    ("720/9", "India's record Test total\nin New Zealand"),
    ("36", "workers still missing after\nthe Cikande factory fire"),
    ("24", "civilians dead in\nthe South Sudan attack"),
]

UTC_BEATS = [
    ("OVERNIGHT", "Kyiv region hit by Russian drone; 14 feared trapped"),
    ("MORNING", "Search resumes at Cikande factory fire; 36 still missing"),
    ("MIDDAY", "Nepal PM holds talks with Modi in New Delhi"),
    ("AFTERNOON", "India declare 720/9, a record in New Zealand"),
    ("EVENING", "Climate talks collapse with no deal in Antalya"),
]

LEADS = [
    dict(n=1, cat="WAR", art="bahrain", kicker="CLAIM VS DENIAL", cert="CLAIM",
         place="MANAMA, BAHRAIN · IRAN",
         hl="Iran claims two US radars hit; Bahrain denies it",
         body="The IRGC says it destroyed two Patriot radars at a US base in Bahrain. "
              "Bahrain: the target was a civilian site — a fire, no injuries. "
              "(Khaleej Times, Al Jazeera)"),
    dict(n=2, cat="SCI", art="cop", kicker="NO FOSSIL FUELS", cert="REPORTED",
         place="ANTALYA, TÜRKİYE · CLIMATE",
         hl="Climate talks collapse with no deal",
         body="UN climate talks break down without an overarching agreement. Türkiye's final draft never mentions "
              "the words 'fossil fuels' that cause global warming. (Reuters, BBC, The Guardian)"),
    dict(n=3, cat="POL", art="house", kicker="258 SEATS", cert="REPORTED",
         place="WASHINGTON, US · POLITICS",
         hl="Democrats clinch 258 House seats, largest since 1992",
         body="Their 258th seat came Sunday as Chuck Hubbard beat Rep. Virginia Foxx in North Carolina — "
              "44 seats gained, the biggest majority in over three decades. (AP, Reuters)"),
]

SMALLS = [
    dict(n=4, cat="WAR", art="ship_finland", kicker="SHIP ABLAZE",
         place="GULF OF FINLAND · SEA",
         hl="Russian cargo ship still burning",
         body="Hit by drones; Finland leads salvage. (Reuters)"),
    dict(n=6, cat="WAR", art="kyiv", kicker="14 MISSING",
         place="KYIV REGION · WAR",
         hl="14 missing after drone hits block",
         body="Drone hit a building; 14 feared trapped, two injured. (Wires)"),
    dict(n=7, cat="SOC", art="factory", kicker="3 DEAD, 36 MISSING",
         place="CIKANDE, INDONESIA · FIRE",
         hl="Candy-factory fire: 3 dead, 36 missing",
         body="Search resumes Monday; 24 bags found. (Reuters)"),
    dict(n=8, cat="POL", art="airport", kicker="ICE 'OUT OF CONTROL'",
         place="OLYMPIA, US · IMMIGRATION",
         hl="Governor: ICE 'out of control'",
         body="Washington governor speaks after airport arrests. (Wires)"),
    dict(n=9, cat="POL", art="seoul", kicker="AI CHEATING",
         place="SEOUL · POLITICS",
         hl="Education minister quits over AI cheating",
         body="Resigns amid an AI cheating scandal. (Wires)"),
    dict(n=11, cat="POL", art="delhi", kicker="STATE VISIT",
         place="NEW DELHI · DIPLOMACY",
         hl="Nepal PM holds talks with Modi",
         body="Balendra Shah, on a state visit, holds bilateral talks. (Wires)"),
    dict(n=12, cat="SPT", art="cricket", kicker="720/9 DECLARED",
         place="WELLINGTON · CRICKET",
         hl="India declare 720/9, a record in NZ",
         body="Rahul 136, Gill 98, hosts 119/2, trailing by 235. (ESPNcricinfo)"),
    dict(n=13, cat="SPT", art="f1", kicker="VERSTAPPEN WINS",
         place="LAS VEGAS · FORMULA 1",
         hl="Verstappen wins chaotic Vegas GP",
         body="From pole in 1:37.9/24; Norris +0.635, Piastri +1.159. (FIA)"),
    dict(n=14, cat="SOC", art="lisbon", kicker="LIVING COSTS",
         place="LISBON · PROTEST",
         hl="Thousands march as living costs bite",
         body="Thousands march in Lisbon as living costs fuel anger. (Wires)"),
    dict(n=15, cat="WAR", art="juba", kicker="24 DEAD",
         place="JUBA · CONFLICT",
         hl="SPLA-IO attack leaves 24 civilians dead",
         body="SPLA-IO attack; 24 dead, incl. 3 children. (Wires)"),
]

# ALSO list: (n, headline, source). Region comes from REGION_OF.
ALSO = [
    (5, "Russian vessels hit in Libya port", "Wires"),
    (10, "FBI probes apparent hack of crime database", "Al Jazeera"),
    (16, "Houthi missile downed in W. Saudi", "Coalition"),
    (17, "Two tankers hit in Strait of Hormuz", "UKMTO"),
    (18, "Iran: Strait watched; uranium stays in Iran", "Araghchi"),
    (20, "Eisenkot: settler attacks are 'Jewish terrorism'", "Wires"),
    (23, "Woman killed, nine hurt in strikes on Dnipropetrovsk", "Wires"),
    (24, "Poland: Russia twice tried to kill US-Ukrainian rapper", "Wires"),
    (25, "EU chief: smaller budget, €100bn for Ukraine", "Wires"),
    (26, "US intel chief: Putin 'not America's friend in Ukraine'", "Wires"),
    (28, "Delta delays in Atlanta after automation fault", "Wires"),
    (31, "US seeks answers from Nvidia on chip sales to China", "Bessent"),
    (33, "Amit Shah launches Rs 4,000-crore push", "Wires"),
    (36, "Pilgrim bus crash in Kota kills nine", "Wires"),
    (38, "Hyderabad students protest alleged casteist remarks", "Wires"),
    (41, "WHO: fighting near Congo Ebola outbreak hampers aid", "WHO"),
    (42, "Sudan RSF accused of killing civilians", "Wires"),
    (43, "NZ Q3 retail sales due today, consensus +0.5%", "FORECAST"),
]

# (lon, lat) for every one of the 31 stories — all pinned on the map.
PINS = {1: (50.6, 26.2), 2: (30.7, 36.9), 3: (-77.0, 38.9), 4: (25.0, 59.8),
        5: (13.2, 32.9), 6: (30.5, 50.45), 7: (106.4, -6.2), 8: (-122.9, 47.0),
        9: (127.0, 37.5), 10: (-77.0, 38.9), 11: (77.2, 28.6), 12: (174.8, -41.3),
        13: (-115.1, 36.2), 14: (-9.1, 38.7), 15: (31.6, 4.85),
        16: (42.0, 21.5), 17: (56.5, 26.5), 18: (51.4, 35.7), 20: (35.2, 31.9),
        23: (35.0, 48.45), 24: (19.4, 52.2), 25: (4.35, 50.85),
        26: (-77.0, 38.9), 28: (-84.4, 33.75), 31: (-77.0, 38.9),
        33: (94.7, 28.2), 36: (75.9, 25.2), 38: (78.5, 17.4),
        41: (29.0, -1.5), 42: (32.5, 15.6), 43: (174.8, -41.3)}
N_STORIES = 31
assert sorted(REGION_OF) == STORY_IDS
assert set(PINS) == set(STORY_IDS), set(PINS) ^ set(STORY_IDS)
assert len(LEADS) + len(SMALLS) + len(ALSO) == N_STORIES
assert [s["n"] for s in LEADS] + [s["n"] for s in SMALLS] + [a[0] for a in ALSO] == STORY_IDS or \
    sorted([s["n"] for s in LEADS] + [s["n"] for s in SMALLS] + [a[0] for a in ALSO]) == STORY_IDS
_counts = {}
for _n in STORY_IDS:
    _counts[REGION_OF[_n]] = _counts.get(REGION_OF[_n], 0) + 1
assert _counts == {"EUROPE": 8, "MIDDLE EAST": 5, "AMERICAS": 6,
                   "ASIA-PACIFIC": 7, "AFRICA": 4, "OCEANIA": 1}, _counts

# ------------------------------------------------------------------ map (own simplified continents)
LANDS = [
    [(-165, 65), (-140, 70), (-95, 72), (-75, 68), (-60, 50), (-70, 42), (-80, 30), (-85, 25), (-97, 26), (-105, 22), (-115, 30), (-125, 42), (-125, 50), (-140, 60)],
    [(-78, 8), (-62, 10), (-40, -5), (-38, -20), (-50, -32), (-65, -50), (-72, -45), (-72, -20), (-80, -5)],
    [(-55, 60), (-25, 70), (-25, 80), (-55, 80), (-65, 75)],
    [(-10, 36), (-8, 44), (0, 50), (8, 56), (18, 68), (28, 70), (38, 64), (38, 48), (28, 40), (20, 36), (10, 38), (0, 38)],
    [(-17, 15), (-15, 28), (-5, 35), (10, 37), (30, 31), (42, 12), (50, 10), (40, -15), (32, -28), (18, -34), (12, -18), (8, 4), (-8, 5)],
    [(30, 42), (45, 48), (65, 60), (75, 72), (110, 76), (150, 70), (178, 66), (162, 58), (140, 50), (132, 35), (122, 30), (120, 22), (108, 10), (100, 5), (92, 18), (80, 8), (70, 22), (58, 26), (50, 14), (42, 12), (35, 30)],
    [(114, -22), (130, -12), (142, -11), (150, -25), (146, -38), (130, -32), (115, -33)],
    [(95, 5), (105, -5), (120, -9), (110, -7), (98, 2)],
    [(130, 33), (140, 40), (144, 44), (138, 35)],
    [(-5, 50), (1, 51), (2, 53), (-2, 56), (-3, 58), (-6, 57), (-5, 54)],
    [(5, 58), (5, 62), (14, 67), (25, 70), (30, 69), (28, 60), (18, 59), (12, 56)],
]
SEAS = [
    [(-5, 36), (0, 37), (10, 37), (16, 38), (22, 36), (28, 36), (36, 36), (36, 33), (32, 31), (25, 31), (10, 33), (0, 35)],
    [(32, 29), (34, 28), (39, 20), (43, 12), (42, 12), (37, 18), (33, 27)],
    [(48, 30), (50, 28), (52, 26), (56, 26), (56, 24), (51, 24), (50, 26)],
]
EU_BOX = (-12, 36, 34, 62)   # lon0, lon1, lat0, lat1
ME_BOX = (34, 62, 12, 40)


def in_box(ll, box):
    lon, lat = ll
    return box[0] <= lon <= box[1] and box[2] <= lat <= box[3]


def where(n):
    ll = PINS[n]
    if in_box(ll, EU_BOX):
        return "EU"
    if in_box(ll, ME_BOX):
        return "ME"
    return "WORLD"


def spread(items, w, h, md=13, rad=6, ymin=None):
    """items: [(n, x, y)] -> {n: (px, py)}; deterministic repulsion, pins never overlap."""
    pos = [[x, y] for _, x, y in items]
    orig = [[x, y] for _, x, y in items]
    for _ in range(400):
        moved = False
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                dx, dy = pos[j][0] - pos[i][0], pos[j][1] - pos[i][1]
                dist = math.hypot(dx, dy)
                if dist < md:
                    if dist < 0.01:
                        dx, dy, dist = math.cos(i * 2.4 + j), math.sin(i * 2.4 + j), 1.0
                    push = (md - dist) / 2 + 0.05
                    ux, uy = dx / dist, dy / dist
                    pos[i][0] -= ux * push
                    pos[i][1] -= uy * push
                    pos[j][0] += ux * push
                    pos[j][1] += uy * push
                    moved = True
        for k, p in enumerate(pos):
            p[0] += (orig[k][0] - p[0]) * 0.01
            p[1] += (orig[k][1] - p[1]) * 0.01
            p[0] = min(max(p[0], rad + 1), w - rad - 1)
            p[1] = min(max(p[1], (ymin if ymin is not None else rad + 1)), h - rad - 1)
        if not moved:
            break
    return {n: tuple(p) for (n, _, _), p in zip(items, pos)}


def map_pins(dd, items, w, h, md=13, ymin=None):
    placed = spread(items, w, h, md=md, ymin=ymin)
    for n, x, y in items:
        px, py = placed[n]
        if math.hypot(px - x, py - y) > 3:
            dd.line([x, y, px, py], fill=(60, 60, 66), width=1)
        dd.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(40, 40, 46))
    for n, x, y in items:
        px, py = placed[n]
        c = REGCOL[REGION_OF[n]]
        dd.ellipse([px - 8, py - 8, px + 8, py + 8], fill=c, outline=(255, 255, 255))
        dd.text((px, py), str(n), font=font("sb", FLOOR), fill=(255, 255, 255), anchor="mm")
    return placed


def inset(x, y, w, h, title, box, ids):
    lon0, lon1, lat0, lat1 = box
    sub = Image.new("RGB", (w, h), SEA)
    dd = ImageDraw.Draw(sub)

    def P(lon, lat):
        return ((lon - lon0) / (lon1 - lon0) * w, (lat1 - lat) / (lat1 - lat0) * h)

    for poly in LANDS:
        dd.polygon([P(*p) for p in poly], fill=LAND, outline=(150, 132, 96))
    for poly in SEAS:
        dd.polygon([P(*p) for p in poly], fill=SEA)
    items = [(n,) + P(*PINS[n]) for n in sorted(ids)]
    map_pins(dd, items, w, h, md=17, ymin=21)
    dd.rectangle([0, 0, int(tw(title, font("sb", FLOOR))) + 9, 14], fill=INK)
    dd.text((4, 1), title, font=font("sb", FLOOR), fill=(255, 255, 255))
    img.paste(sub, (x, y))
    d.rectangle([x, y, x + w, y + h], outline=INK)


def draw_map(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK)
    d.rectangle([x, y, x + w, y + 14], fill=INK)
    d.text((x + 5, y + 7), "WHERE IT HAPPENED · every story pinned · pin colour = region · leader line = true spot", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="lm")
    mh = h - 16 - 17
    mw = int(mh * 360 / 140)
    mx, my = x + 2, y + 16

    def P(lon, lat):
        return (mx + (lon + 180) / 360.0 * mw, my + (82 - lat) / 140.0 * mh)

    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA)
    for poly in LANDS:
        d.polygon([P(*p) for p in poly], fill=LAND, outline=(150, 132, 96))
    for poly in SEAS:
        d.polygon([P(*p) for p in poly], fill=SEA)
    for box in (EU_BOX, ME_BOX):
        a, b = P(box[0], box[3]), P(box[1], box[2])
        d.rectangle([a[0], a[1], b[0], b[1]], outline=INK, width=1)
    ids = [n for n in sorted(PINS) if where(n) == "WORLD"]
    items = [(n,) + (P(*PINS[n])[0] - mx, P(*PINS[n])[1] - my) for n in ids]
    placed = spread(items, mw, mh, md=17)
    for n, px0, py0 in items:
        px, py = placed[n]
        if math.hypot(px - px0, py - py0) > 3:
            d.line([mx + px0, my + py0, mx + px, my + py], fill=(60, 60, 66), width=1)
        d.ellipse([mx + px0 - 1.5, my + py0 - 1.5, mx + px0 + 1.5, my + py0 + 1.5], fill=(40, 40, 46))
    for n, px0, py0 in items:
        px, py = placed[n]
        c = REGCOL[REGION_OF[n]]
        d.ellipse([mx + px - 8, my + py - 8, mx + px + 8, my + py + 8], fill=c, outline=(255, 255, 255))
        d.text((mx + px, my + py), str(n), font=font("sb", FLOOR), fill=(255, 255, 255), anchor="mm")
    ix = mx + mw + 4
    iw = (x + w - 2 - ix - 3) // 2
    inset(ix, my, iw, mh, "EUROPE", EU_BOX, [n for n in PINS if where(n) == "EU"])
    inset(ix + iw + 3, my, iw, mh, "MIDDLE EAST", ME_BOX, [n for n in PINS if where(n) == "ME"])
    ly = my + mh + 4
    cx = x + 4
    for name in REGIONS:
        d.ellipse([cx, ly + 2, cx + 9, ly + 11], fill=REGCOL[name])
        d.text((cx + 12, ly), name.lower(), font=font("s", FLOOR), fill=INK)
        cx += 12 + int(tw(name.lower(), font("s", FLOOR))) + 8
    if cx > x + w - 4:
        WARN.append("map legend overflow %d" % cx)

# ------------------------------------------------------------------ sections
def draw_header():
    d.rectangle([0, 0, W, 22], fill=NAVY)
    fit_text(10, 11, 400, "THE WORLD IN ONE DAY", "sb", 13, (255, 255, 255), anchor="lm", minsize=FLOOR, tag="mast")
    fit_text(1014, 11, 700, "31 STORIES · 6 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026", "sb", 11, (255, 255, 255), anchor="rm", minsize=FLOOR, tag="mast")
    fit_text(512, 26, 1004, "Monday 23 November 2026", "xb", 46, INK, anchor="ma")
    rule(10, 80, 1014, 80, 1)
    fit_text(512, 82, 1004,
             "Iran claims two US radars hit  ·  Climate talks collapse with no deal  ·  Democrats clinch 258 House seats",
             "xi", 15, RED, anchor="ma", minsize=12)
    rule(10, 102, 1014, 102, 2)


def draw_data_strip(y, h):
    cw = 1004 / 6
    for i, (big, small) in enumerate(DATA):
        x = 10 + i * cw
        d.rectangle([x + 2, y + 2, x + 5, y + h - 2], fill=RED)
        fit_text(x + 10, y + 2, cw - 14, big, "xb", 26, RED)
        for j, ln in enumerate(small.split("\n")):
            fit_text(x + 10, y + 30 + j * 11, cw - 14, ln, "s", FLOOR, GREY, minsize=FLOOR, tag="data")
    rule(10, y + h, 1014, y + h, 1)


def draw_region_bar(y, h):
    counts = {}
    for n in STORY_IDS:
        counts[REGION_OF[n]] = counts.get(REGION_OF[n], 0) + 1
    assert sum(counts.values()) == N_STORIES
    cw = 1004 / len(REGIONS)
    for i, name in enumerate(REGIONS):
        n = counts.get(name, 0)
        x = 10 + i * cw
        d.rectangle([x + 1, y, x + cw - 1, y + h], fill=REGCOL[name])
        lab = "%s %d" % (name, n)
        fit_text(x + cw / 2, y + h / 2, cw - 8, lab, "sb", 11, (255, 255, 255), anchor="mm", minsize=FLOOR, tag="region")
    return counts


def draw_utc_strip(y, h):
    d.rectangle([10, y, 1014, y + h], fill=(236, 230, 214), outline=INK)
    d.rectangle([10, y, 132, y + h], fill=NAVY)
    d.text((71, y + h / 2), "THE DAY IN UTC", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="mm")
    cw = (1014 - 132 - 10) / 5
    for i, (part, beat) in enumerate(UTC_BEATS):
        x = 132 + i * cw
        d.text((x + 6, y + 3), part, font=font("sb", FLOOR), fill=RED)
        para(x + 6, y + 15, cw - 12, beat, "s", FLOOR, INK, lh=11, maxlines=2, tag="utc")
        if i < 4:
            d.line([x + cw - 1, y + 3, x + cw - 1, y + h - 3], fill=(200, 194, 178))


PANEL_SLACK = []


def draw_lead_panel(x, y, w, h, s):
    kicker(x, y, w, 14, s["kicker"])
    d.rectangle([x, y + 14, x + w, y + h], fill=PANEL, outline=INK)
    ART[s["art"]](x + 1, y + 15, w - 1, 96)
    cy = y + 15 + 96 + 4
    d.text((x + 4, cy), "%d %s" % (s["n"], s["place"]), font=font("sb", FLOOR), fill=RED)
    cert_tag(x + w - 4, cy, s["cert"])
    ty = para(x + 4, cy + 14, w - 8, s["hl"], "xb", 15, INK, lh=16, maxlines=2, tag="hl" + str(s["n"]))
    end = para(x + 4, ty + 2, w - 8, s["body"], "s", 11, (40, 40, 46), lh=12, maxlines=3, tag="body" + str(s["n"]))
    if end > y + h:
        WARN.append("lead %d body overflows box by %d" % (s["n"], end - (y + h)))
    PANEL_SLACK.append((s["n"], y + h - end))


def draw_small_panel(x, y, w, h, s):
    kicker(x, y, w, 12, s["kicker"])
    d.rectangle([x, y + 12, x + w, y + h], fill=PANEL, outline=INK)
    ART[s["art"]](x + 1, y + 13, w - 1, 52)
    cy = y + 13 + 52 + 2
    d.text((x + 3, cy), "%d %s" % (s["n"], s["place"]), font=font("sb", FLOOR), fill=RED)
    ty = para(x + 3, cy + 11, w - 6, s["hl"], "sb", 12, INK, lh=13, maxlines=2, tag="hl" + str(s["n"]))
    end = para(x + 3, ty + 1, w - 6, s["body"], "s", 11, (40, 40, 46), lh=12, maxlines=2, tag="body" + str(s["n"]))
    if end > y + h:
        WARN.append("small %d body overflows box by %d" % (s["n"], end - (y + h)))
    PANEL_SLACK.append((s["n"], y + h - end))


def draw_also(y, h):
    n_b = len(ALSO)
    per = -(-n_b // 2)
    d.rectangle([10, y, 1014, y + 15], fill=INK)
    d.text((16, y + 7), "ALSO ON MONDAY 23 NOVEMBER — %d MORE STORIES · ONE LINE EACH" % n_b, font=font("sb", FLOOR), fill=(255, 255, 255), anchor="lm")
    cw = 1004 / 2
    rh = (h - 19) / per
    for i, (n, hl, src) in enumerate(ALSO):
        col, row = divmod(i, per)
        x = 10 + col * cw + 4
        yy = y + 19 + row * rh
        reg = REGION_OF[n]
        d.rectangle([x, yy + 1, x + 18, yy + 13], fill=REGCOL[reg])
        d.text((x + 9, yy + 7), str(n), font=font("sb", FLOOR), fill=(255, 255, 255), anchor="mm")
        tx = x + 22
        line = "%s: %s (%s)" % (reg, hl, src)
        fit_text(tx, yy, cw - 30, line, "s", 11, INK, minsize=FLOOR, tag="also%d" % n)
        if row < per - 1:
            d.line([tx, yy + rh - 1, x + cw - 14, yy + rh - 1], fill=(214, 208, 192))


def draw_datecheck(y, h):
    d.rectangle([10, y, 1014, y + h], fill=(255, 250, 240), outline=RED, width=2)
    d.rectangle([10, y, 1014, y + 15], fill=RED)
    d.text((16, y + 7), "DATE CHECK · LEFT OUT AS OTHER DAYS' NEWS", font=font("sb", FLOOR), fill=(255, 255, 255), anchor="lm")
    para(16, y + 19, 992,
         "Left out as other days' news: 'El Chapo Isidro' captured (Fri 20 Nov) · Hong Kong elects its Election "
         "Committee (Sun 22 Nov) · 186 drones over Ukraine in the night (Sat 22 Nov) · Liverpool beat Man Utd "
         "(Sun 22 Nov) · COP31 talks run into overtime (Sat 22 Nov).",
         "s", FLOOR, INK, lh=11, maxlines=2, tag="date")
    d.text((16, y + h - 11), "Nothing here is dated to any day but Monday 23 November 2026, except the items named above as excluded.",
           font=font("si", FLOOR), fill=GREY)


def draw_footer(y):
    fit_text(10, y, 1004,
             "Sources: Reuters, BBC, AP, Al Jazeera, Guardian, Xinhua, DetikNews · REPORTED = wires · "
             "CLAIM = one side's account · FORECAST = yet to happen · Pictures + map: original, drawn in code.",
             "s", FLOOR, GREY, minsize=FLOOR, tag="foot")


def main(out_path):
    draw_header()
    y = 106
    draw_data_strip(y, 54)
    y += 54 + 4
    counts = draw_region_bar(y, 24)
    y += 24 + 4
    draw_utc_strip(y, 36)
    y += 36 + 4
    g = 8
    pw = (1004 - 2 * g) // 3
    for i, s_ in enumerate(LEADS):
        draw_lead_panel(10 + i * (pw + g), y, pw, 200, s_)
    y += 200 + 4
    g2 = 6
    pw2 = (1004 - 4 * g2) // 5
    for r in range(2):
        for c in range(5):
            draw_small_panel(10 + c * (pw2 + g2), y + r * (132 + 4), pw2, 132, SMALLS[r * 5 + c])
    y += 2 * 132 + 4 + 4
    draw_map(10, y, 1004, 128)
    y += 128 + 4
    draw_also(y, 124)
    y += 124 + 4
    draw_datecheck(y, 44)
    y += 44 + 2
    draw_footer(y)
    print("layout: final y=%d (canvas 1024, bottom margin %d)" % (y + 10, 1024 - (y + 10)))
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    img.save(out_path, optimize=True)
    print("regions:", counts)
    print("panel slack:", PANEL_SLACK)
    for w_ in WARN:
        print("WARN", w_)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_v2.png"))
