#!/usr/bin/env python3
"""Draw the news-image-20261125 slot 1 front page (PIL, no network).

Renders "THE WORLD IN ONE DAY — Wednesday 25 November 2026" as a
1024x1024 broadsheet: masthead, three illustrated heroes, stat strip,
12 story cards, pin map + UTC timeline, ALSO strip, footer.
Every story is from AUDIT.md (verified live reporting, honestly dated).
Run: python3 draw_entry.py  ->  entry.png (deterministic, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28
PAPER = (247, 243, 234)
INK = (20, 20, 20)
GREY = (90, 88, 82)
RED = (178, 32, 44)
BLUE = (29, 78, 137)
GOLD = (176, 124, 20)
LINE = (60, 58, 52)
SKY = (214, 228, 240)
SEA = (178, 205, 228)

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def F(path, size):
    return ImageFont.truetype(path, size)


def mast(size):
    return F(f"{FD}/DejaVuSerif-Bold.ttf", size)


def sansb(size):
    return F(f"{FL}/LiberationSans-Bold.ttf", size)


def sans(size):
    return F(f"{FL}/LiberationSans-Regular.ttf", size)


def serif(size):
    return F(f"{FD}/DejaVuSerif.ttf", size)


def mono(size):
    return F(f"{FD}/DejaVuSansMono-Bold.ttf", size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, font, width, max_lines):
    lines = wrap(d, text, font, width)
    while len(lines) > max_lines:
        words = text.split()
        text = " ".join(words[:-1])
        lines = wrap(d, text, font, width)
        if len(words) <= 1:
            break
    return lines


def draw_lines(d, lines, x, y, font, fill=INK, leading=None):
    lh = leading or int(font.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# date: WED = first reported Wed 25 Nov 2026; TUE = Tue 24 Nov; MON = Mon 23 Nov
HEROES = [
    dict(key="cpi", region="OCEANIA", date="WED",
         kicker="ECONOMY  •  CANBERRA",
         head="INFLATION ROARS BACK: AUSTRALIA CPI 4.9%",
         deck="Prices jumped from 4.3% to 4.9% in October, the fastest in "
              "three years. Core inflation hit 3.8%; the RBA's rate-cut hopes faded."),
    dict(key="warship", region="EUROPE", date="WED",
         kicker="WAR IN UKRAINE  •  KYIV",
         head="KYIV SINKS RUSSIAN WARSHIP OFF LIBYA",
         deck="Zelenskiy confirms Ukraine sank a Russian warship off Libya "
              "and owns the weekend drone hit in the Gulf of Finland."),
    dict(key="riyadh", region="MIDDLE EAST", date="TUE",
         kicker="GULF WAR  •  RIYADH",
         head="HOUTHIS HIT RIYADH'S TALLEST TOWER: 11 HURT",
         deck="A strike on the PIF Tower in Riyadh's financial district "
              "wounded eleven. Houthi forces are now 60 km from Aden."),
]

GRID = [
    dict(region="MIDDLE EAST", date="TUE",
         head="Three tankers hit by mines in Hormuz",
         deck="Iran's navy says three tankers caught fire after hitting mines."),
    dict(region="USA", date="TUE",
         head="Huawei convicted in US trial over Iran",
         deck="Guilty of stealing trade secrets; cleared of racketeering."),
    dict(region="USA", date="TUE",
         head="Trump gives Giuliani the Medal of Freedom",
         deck="The ex-New York mayor receives the top civilian honour."),
    dict(region="USA", date="TUE",
         head="CIA and spy chief's office hit by breach",
         deck="A breach touched some unclassified data at the CIA and ODNI."),
    dict(region="EUROPE", date="TUE",
         head="Sarkozy corruption case sent to trial",
         deck="France orders the ex-president and wife Carla Bruni to trial."),
    dict(region="USA", date="TUE",
         head="Fort Hood gunman seeks stay of execution",
         deck="Nidal Hasan, who killed 13 in 2009, seeks a stay of execution."),
    dict(region="EUROPE", date="TUE",
         head="NATO jets to guard Poland's skies",
         deck="Early-warning jets to deploy after missiles landed in Poland."),
    dict(region="EUROPE", date="TUE",
         head="EU readies 22nd Russia sanctions package",
         deck="Brussels presents the package at the 26–27 Nov summit."),
    dict(region="ASIA", date="TUE",
         head="England level the T20 series in Australia",
         deck="England beat Australia by eight wickets, chasing 185."),
    dict(region="MARKETS", date="TUE",
         head="Dell lifts forecasts on AI server boom",
         deck="A record quarter on surging demand for AI servers."),
    dict(region="USA", date="TUE",
         head="Trump pardons turkeys Freedom and Feathers",
         deck="The Thanksgiving eve ceremony spares two birds."),
    dict(region="MIDDLE EAST", date="TUE",
         head="US envoy unsure Israel aid ends this year",
         deck="Envoy 'not certain' the aid ends as Trump promised."),
]

ALSO = [
    "UK age-of-consent review (Tue)",
    "UK nuclear-veterans panel (Tue)",
    "Denmark upholds 'ghetto' evictions (Mon)",
    "Venezuela debt $237.5bn (Tue)",
    "IDF suicides at 16-yr high (Mon)",
    "Iran winter gas shortages (Wed)",
    "720,000 Russians killed (Wed)",
    "Perth CPI jumps to 5.5% (Wed)",
]

PINS = [  # (label, x 0..1, y 0..1) on the map panel
    ("1 Sydney", 0.88, 0.80), ("2 Benghazi", 0.52, 0.44),
    ("3 Gulf of Finland", 0.58, 0.13), ("4 Riyadh", 0.60, 0.47),
    ("5 Hormuz", 0.65, 0.50), ("6 Kyiv", 0.54, 0.24),
    ("7 Paris", 0.44, 0.31), ("8 Washington", 0.15, 0.38),
    ("9 London", 0.43, 0.19), ("10 New Delhi", 0.70, 0.48),
    ("11 Perth", 0.83, 0.76), ("12 Chicago", 0.23, 0.27),
]

TIMELINE = [
    ("00:30", "ABS: Australia CPI 4.9%"),
    ("01:00", "RFE/RL: 720,000 Russians killed"),
    ("MORNING", "Reuters: Zelenskiy owns ship strikes"),
    ("MIDDAY", "Houthi tower strike confirmed"),
    ("AFTERNOON", "Huawei verdict; Giuliani medal"),
    ("EVENING", "EU sanctions package previewed"),
]

STATS = [
    ("30", "stories, 7 regions"),
    ("4", "Wednesday exclusives"),
    ("3", "seas in one war day"),
    ("4.9%", "Australia CPI"),
]

# ---------------------------------------------------------------- art
def art_ship(d, x, y, w, h):
    """Sinking warship at dusk: sea, hull listing, smoke, explosion."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 66))
    d.rectangle([x, y, x + w, y + int(h * 0.45)], fill=(232, 150, 80))
    d.ellipse([x + int(w * 0.72), y + 6, x + int(w * 0.92), y + 26], fill=(240, 200, 90))
    for i in range(5):
        yy = y + int(h * (0.62 + i * 0.07))
        d.line([x + 4, yy, x + w - 4, yy], fill=(120, 170, 210), width=2)
    hx, hy = x + int(w * 0.12), y + int(h * 0.52)
    d.polygon([(hx, hy), (hx + int(w * 0.62), hy - 14), (hx + int(w * 0.72), hy + 6),
               (hx + int(w * 0.70), hy + 26), (hx + 8, hy + 26)], fill=(40, 44, 52))
    d.rectangle([hx + int(w * 0.18), hy - 30, hx + int(w * 0.30), hy - 8], fill=(52, 56, 64))
    d.line([hx + int(w * 0.24), hy - 52, hx + int(w * 0.24), hy - 30], fill=(52, 56, 64), width=3)
    for cx, cy, r, col in [(0.62, 0.30, 16, (90, 90, 90)), (0.68, 0.24, 20, (70, 70, 70)),
                           (0.74, 0.30, 14, (110, 110, 110))]:
        d.ellipse([x + int(w * cx) - r, y + int(h * cy) - r,
                   x + int(w * cx) + r, y + int(h * cy) + r], fill=col)
    ex, ey = x + int(w * 0.55), y + int(h * 0.34)
    for dx, dy in [(0, -16), (11, -11), (16, 0), (11, 11), (0, 16), (-11, 11), (-16, 0), (-11, -11)]:
        d.line([ex, ey, ex + dx, ey + dy], fill=(255, 190, 60), width=4)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 220, 120))


def art_tower(d, x, y, w, h):
    """Riyadh financial-district tower at night, smoke from upper floors."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 44))
    for i in range(14):
        d.ellipse([x + (i * 37) % w, y + (i * 53) % int(h * 0.4), x + (i * 37) % w + 2,
                   y + (i * 53) % int(h * 0.4) + 2], fill=(240, 240, 220))
    d.ellipse([x + int(w * 0.82), y + 10, x + int(w * 0.92), y + 10 + int(w * 0.10)],
              fill=(235, 230, 210))
    for bx, bw, bh in [(0.02, 0.16, 0.45), (0.20, 0.13, 0.60), (0.66, 0.14, 0.55), (0.84, 0.14, 0.40)]:
        d.rectangle([x + int(w * bx), y + h - int(h * bh), x + int(w * (bx + bw)), y + h],
                    fill=(38, 48, 70))
    tx = x + int(w * 0.38)
    d.polygon([(tx, y + h), (tx + 6, y + int(h * 0.10)), (tx + int(w * 0.22), y + int(h * 0.10)),
               (tx + int(w * 0.28), y + h)], fill=(96, 120, 160))
    for r in range(9):
        yy = y + int(h * (0.16 + r * 0.085))
        d.line([tx + 12, yy, tx + int(w * 0.24), yy], fill=(255, 214, 130), width=2)
    ix, iy = tx + int(w * 0.15), y + int(h * 0.22)
    d.ellipse([ix - 18, iy - 12, ix + 18, iy + 12], fill=(255, 140, 40))
    d.ellipse([ix - 9, iy - 6, ix + 9, iy + 6], fill=(255, 220, 130))
    for cx, cy, r, col in [(0.52, 0.10, 18, (120, 120, 125)), (0.58, 0.06, 22, (100, 100, 105)),
                           (0.64, 0.11, 15, (135, 135, 140))]:
        d.ellipse([x + int(w * cx) - r, y + int(h * cy) - r,
                   x + int(w * cx) + r, y + int(h * cy) + r], fill=col)


def art_cpi(d, x, y, w, h):
    """Bar chart: Australia CPI 4.3% (Sep) -> 4.9% (Oct)."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 236))
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=2)
    d.text((x + 10, y + 8), "AUSTRALIA CPI, % Y/Y", font=mono(13), fill=GREY)
    base = y + h - 34
    scale = (h - 70) / 5.5
    for v in [2, 4, 5]:
        yy = base - int(v * scale)
        d.line([x + 10, yy, x + w - 10, yy], fill=(210, 206, 196), width=1)
    bw = int(w * 0.24)
    x1 = x + int(w * 0.14)
    d.rectangle([x1, base - int(4.3 * scale), x1 + bw, base], fill=(120, 130, 140))
    d.text((x1, base - int(4.3 * scale) - 22), "4.3%", font=sansb(20), fill=INK)
    d.text((x1, base + 8), "SEP", font=mono(13), fill=GREY)
    x2 = x + int(w * 0.52)
    d.rectangle([x2, base - int(4.9 * scale), x2 + bw, base], fill=RED)
    d.text((x2, base - int(4.9 * scale) - 22), "4.9%", font=sansb(20), fill=RED)
    d.text((x2, base + 8), "OCT", font=mono(13), fill=GREY)
    d.line([x, base, x + w, base], fill=INK, width=2)


# ---------------------------------------------------------------- panels
def masthead(d, y0=0):
    d.rectangle([0, y0, W, y0 + 8], fill=RED)
    d.text((M, y0 + 16), "THE WORLD IN ONE DAY", font=mast(56), fill=INK)
    d.text((W - M - d.textlength("No. 329", font=mast(16)), y0 + 22),
           "No. 329", font=mast(16), fill=GREY)
    d.text((M, y0 + 82), "WEDNESDAY  25  NOVEMBER  2026",
           font=sansb(24), fill=RED)
    d.text((M + d.textlength("WEDNESDAY  25  NOVEMBER  2026  ", font=sansb(24)), y0 + 86),
           "•  30 STORIES  •  7 REGIONS  •  ALL DATED",
           font=sans(20), fill=GREY)
    d.line([M, y0 + 116, W - M, y0 + 116], fill=INK, width=3)
    d.line([M, y0 + 121, W - M, y0 + 121], fill=INK, width=1)
    return y0 + 130


def hero(d, x, y, w, h, s, art_h=96):
    if s["key"] == "cpi":
        art_cpi(d, x, y, w, art_h)
    elif s["key"] == "warship":
        art_ship(d, x, y, w, art_h)
    else:
        art_tower(d, x, y, w, art_h)
    yy = y + art_h + 8
    d.text((x, yy), s["kicker"], font=mono(12), fill=RED)
    yy += 18
    d.text((x, yy), s["date"] + "  •  " + s["region"], font=mono(12), fill=GREY)
    yy += 18
    yy = draw_lines(d, fit_lines(d, s["head"], sansb(22), w, 3), x, yy, sansb(22))
    yy += 2
    draw_lines(d, fit_lines(d, s["deck"], serif(13), w, 3), x, yy, serif(13))
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)


def story_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 4], fill=RED if s["date"] == "WED" else (BLUE if s["date"] == "TUE" else GOLD))
    yy = y + 10
    d.text((x + 8, yy), s["region"], font=mono(11), fill=RED)
    dw = d.textlength(s["date"], font=mono(11))
    d.text((x + w - 8 - dw, yy), s["date"], font=mono(11), fill=GREY)
    yy += 17
    yy = draw_lines(d, fit_lines(d, s["head"], sansb(14), w - 16, 2), x + 8, yy, sansb(14))
    draw_lines(d, fit_lines(d, s["deck"], serif(11), w - 16, 2), x + 8, yy + 2, serif(11))


def map_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=LINE, width=1)
    d.text((x + 10, y + 8), "WHERE THE DAY HAPPENED", font=mono(13), fill=INK)
    conts = [
        [(0.03, 0.30), (0.10, 0.22), (0.22, 0.24), (0.26, 0.38), (0.16, 0.48), (0.06, 0.44)],
        [(0.30, 0.22), (0.42, 0.18), (0.48, 0.30), (0.44, 0.44), (0.34, 0.42), (0.30, 0.32)],
        [(0.50, 0.26), (0.60, 0.20), (0.72, 0.24), (0.78, 0.36), (0.70, 0.48), (0.58, 0.44), (0.50, 0.36)],
        [(0.74, 0.24), (0.86, 0.22), (0.92, 0.34), (0.86, 0.46), (0.78, 0.42)],
        [(0.80, 0.62), (0.90, 0.60), (0.95, 0.72), (0.88, 0.82), (0.80, 0.74)],
    ]
    for poly in conts:
        d.polygon([(x + px * w, y + 26 + py * (h - 40)) for px, py in poly], fill=(190, 200, 180))
    for i, (lab, px, py) in enumerate(PINS, 1):
        cx, cy = x + px * w, y + 26 + py * (h - 40)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255), width=2)
        d.text((cx - 3, cy - 6), str(i), font=mono(10), fill=(255, 255, 255))
    d.text((x + 10, y + h - 32),
           "1 Sydney  2 Benghazi  3 Gulf of Finland  4 Riyadh  5 Hormuz  6 Kyiv",
           font=mono(10), fill=GREY)
    d.text((x + 10, y + h - 18),
           "7 Paris  8 Washington  9 London  10 New Delhi  11 Perth  12 Chicago",
           font=mono(10), fill=GREY)


def timeline_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LINE, width=1)
    d.text((x + 10, y + 8), "THE DAY IN UTC", font=mono(13), fill=INK)
    n = len(TIMELINE)
    step = w / n
    yy = y + 52
    d.line([x + 14, yy, x + w - 14, yy], fill=INK, width=2)
    for i, (t, lab) in enumerate(TIMELINE):
        cx = x + step * (i + 0.5)
        d.ellipse([cx - 6, yy - 6, cx + 6, yy + 6], fill=RED, outline=(255, 255, 255), width=2)
        d.text((cx - d.textlength(t, font=mono(11)) / 2, yy - 24), t, font=mono(11), fill=RED)
        lines = fit_lines(d, lab, sans(11), step - 10, 3)
        ly = yy + 12
        for ln in lines:
            d.text((cx - d.textlength(ln, font=sans(11)) / 2, ly), ln, font=sans(11), fill=INK)
            ly += 14


def stat_strip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    cw = w / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = x + cw * i
        d.text((cx + 12, y + 5), num, font=sansb(22), fill=(255, 214, 130))
        d.text((cx + 12, y + 31), lab, font=sans(12), fill=(220, 220, 220))


def also_strip(d, x, y, w, h, items):
    d.text((x, y), "ALSO TODAY", font=mono(13), fill=RED)
    yy = y + 20
    colw = w // 4
    for i, it in enumerate(items):
        cx = x + (i % 4) * colw
        cy = yy + (i // 4) * 18
        d.text((cx, cy), "•  " + it, font=sans(11), fill=INK)


def footer(d, y):
    d.line([M, y, W - M, y], fill=INK, width=1)
    d.text((M, y + 8),
           "All stories first reported 25 November 2026 unless dated TUE (24 Nov) or MON (23 Nov).",
           font=sans(12), fill=GREY)
    d.text((M, y + 26),
           "Sources: Reuters, RFE/RL, Australian Bureau of Statistics, Al Jazeera, Euronews, Haaretz, Forbes.",
           font=sans(12), fill=GREY)
    d.text((W - M - d.textlength("THE WORLD IN ONE DAY  •  25 NOV 2026", font=mono(11)), y + 8),
           "THE WORLD IN ONE DAY  •  25 NOV 2026", font=mono(11), fill=GREY)


# ---------------------------------------------------------------- front page
def draw_frontpage():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    hw, gap = 305, 14
    for i, s in enumerate(HEROES):
        hero(d, M + i * (hw + gap), y, hw, 272, s, art_h=96)
    y += 284
    stat_strip(d, M, y, W - 2 * M, 48)
    y += 58
    gw, gh, ggap = 228, 98, 12
    for i, s in enumerate(GRID):
        r, c = divmod(i, 4)
        story_card(d, M + c * (gw + ggap), y + r * (gh + 8), gw, gh, s)
    y += 3 * gh + 2 * 8 + 12
    map_panel(d, M, y, 470, 116)
    timeline_panel(d, M + 482, y, W - 2 * M - 482, 116)
    y += 128
    also_strip(d, M, y, W - 2 * M, 60, ALSO)
    footer(d, H - 44)
    return img


if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    img = draw_frontpage()
    img.save(os.path.join(out, "entry.png"), optimize=True)
    print("wrote", os.path.join(out, "entry.png"))
