#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a one-page newspaper front page that
sums up Saturday 21 November 2026's world news.

Build-time tool only: it renders entry.png on this machine from the news
reported on 21 November 2026. The entry program (main.py) ships the finished
PNG and copies it to /output/entry.png, so grading runs need no fonts.

Stories (all as reported on 21 Nov 2026, figures as stated by officials):
  1. Russian missiles and a suspected drone land in south-east Poland;
     PM Tusk calls it a deliberate provocation, NATO's Rutte a grave
     violation; Rutte travels to Warsaw on 21 November.
  2. Overnight Russian barrage on Ukraine: 400+ drones, 110 missiles,
     at least 8 killed in Kyiv; embassies hit; France seeks a UN
     Security Council meeting.
  3. Wall Street: S&P 500 and Dow enter correction as AI shares plunge;
     Nasdaq fell 5.28% on Friday, Nvidia about 14%.
  4. First Trump-Xi-Putin trilateral summit in China ends with few
     concrete results.
  5. The World Court (ICJ) rules Myanmar committed genocide against
     the Rohingya.
  6. Saudi-led coalition intercepts Houthi ballistic missiles over
     Riyadh and strikes Hodeidah.
  Also today: Kryvyi Rih strike casualties; Estonia to shut its border
  with Russia; UK and EU sign food, carbon and youth-mobility deals.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

NAVY = (13, 30, 58)
NAVY_LIGHT = (24, 48, 88)
PAPER = (247, 243, 232)
CARD = (255, 255, 255)
INK = (18, 22, 30)
GREY = (88, 94, 106)
RED = (192, 39, 43)
DARKRED = (138, 24, 29)
GOLD = (212, 160, 23)
BLUE = (36, 84, 160)
TEAL = (16, 118, 108)
RULE = (205, 199, 182)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, max_w, minimum=10):
    """Largest font size (down from start) that fits text on one line."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, minimum)


def headline_wrap(draw, xy, text, max_w, size=26, leading=31, color=INK,
                  max_lines=2):
    """Draw a headline wrapped to at most max_lines; shrink if needed."""
    fnt = font(SANS_B, size)
    lines = wrap(draw, text, fnt, max_w)
    while len(lines) > max_lines and size > 14:
        size -= 1
        fnt = font(SANS_B, size)
        lines = wrap(draw, text, fnt, max_w)
    y = xy[1]
    for line in lines[:max_lines]:
        draw.text((xy[0], y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, xy, text, color):
    fnt = font(SANS_B, 17)
    draw.text(xy, text, font=fnt, fill=color)


def headline(draw, xy, text, max_w, start=34, color=INK):
    fnt = fit(draw, text, SANS_B, start, max_w)
    draw.text(xy, text, font=fnt, fill=color)
    return fnt.size


def body(draw, xy, text, max_w, size=21, leading=29, color=INK):
    fnt = font(SANS, size)
    y = xy[1]
    for line in wrap(draw, text, fnt, max_w):
        draw.text((xy[0], y), line, font=fnt, fill=color)
        y += leading
    return y


def panel(draw, box, accent):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=RULE, width=2)
    draw.rectangle([x0, y0, x0 + 7, y1], fill=accent)


# ---------------------------------------------------------------- icons
def icon_missile(draw, box, color=RED):
    """A diagonal missile with a blast star, inside box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # blast star at lower left
    bx, by = x0 + 26, y1 - 30
    pts = []
    for i in range(16):
        r = 30 if i % 2 == 0 else 13
        a = math.pi * i / 8 - math.pi / 2
        pts.append((bx + r * math.cos(a), by + r * math.sin(a)))
    draw.polygon(pts, fill=GOLD)
    # missile body: rotated rounded bar from lower-left to upper-right
    draw.line([(x0 + 34, y1 - 44), (x1 - 22, y0 + 30)], fill=color, width=16)
    draw.polygon([(x1 - 22, y0 + 30), (x1 - 2, y0 + 6),
                  (x1 - 44, y0 + 8)], fill=color)
    draw.polygon([(x0 + 34, y1 - 44), (x0 + 14, y1 - 34),
                  (x0 + 30, y1 - 64)], fill=color)


def icon_burst(draw, box, color=DARKRED):
    """Explosion burst over building silhouettes."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    pts = []
    for i in range(24):
        r = 38 if i % 2 == 0 else 17
        a = math.pi * i / 12 - math.pi / 2
        pts.append((cx + r * math.cos(a), y0 + 42 + r * math.sin(a)))
    draw.polygon(pts, fill=GOLD, outline=color)
    base = y1 - 6
    draw.rectangle([x0 + 8, base - 26, x0 + 44, base], fill=NAVY)
    draw.rectangle([x0 + 52, base - 40, x0 + 88, base], fill=NAVY)
    draw.rectangle([x1 - 88, base - 32, x1 - 52, base], fill=NAVY)
    draw.rectangle([x1 - 44, base - 22, x1 - 8, base], fill=NAVY)
    draw.rectangle([x0 + 8, base, x1 - 8, base + 4], fill=NAVY)


def icon_chart(draw, box, color=RED):
    """Falling market line on a faint grid, with a down arrow."""
    x0, y0, x1, y1 = box
    for gy in range(y0 + 12, y1 - 8, 22):
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(225, 225, 225), width=1)
    pts = [(x0 + 10, y0 + 16), (x0 + 42, y0 + 34), (x0 + 66, y0 + 28),
           (x0 + 92, y0 + 62), (x0 + 118, y0 + 74), (x0 + 142, y0 + 96)]
    draw.line(pts, fill=color, width=6, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 16), (ex - 12, ey - 2), (ex + 12, ey - 2)],
                 fill=color)
    draw.text((x0 + 8, y0 + 2), "-5.28%", font=font(SANS_B, 22), fill=color)


def icon_summit(draw, box):
    """Three circles for the three leaders' countries."""
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    draw.line([(x0 + 30, cy), (x1 - 30, cy)], fill=GREY, width=2)
    specs = [(x0 + 32, BLUE, "US"), (x1 - 32, GOLD, "RU"),
             ((x0 + x1) // 2, RED, "CN")]
    for cx, col, lab in specs:
        draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27],
                     fill=col, outline=(255, 255, 255), width=3)
        w = draw.textlength(lab, font=font(SANS_B, 18))
        draw.text((cx - w / 2, cy - 10), lab, font=font(SANS_B, 18),
                  fill=(255, 255, 255))


def icon_scales(draw, box, color=NAVY):
    """Scales of justice."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    top = y0 + 14
    draw.line([(cx, top), (cx, y1 - 22)], fill=color, width=5)
    draw.line([(x0 + 16, top + 12), (x1 - 16, top + 12)], fill=color, width=5)
    draw.ellipse([cx - 7, top - 8, cx + 7, top + 6], fill=color)
    for sx in (x0 + 16, x1 - 16):
        draw.line([(sx, top + 12), (sx, top + 44)], fill=color, width=3)
        draw.arc([sx - 26, top + 36, sx + 26, top + 76], 0, 180,
                 fill=color, width=4)
        draw.line([(sx - 26, top + 56), (sx + 26, top + 56)], fill=color,
                  width=4)
    draw.line([(cx - 26, y1 - 22), (cx + 26, y1 - 22)], fill=color, width=5)


def icon_shield(draw, box, color=TEAL):
    """Shield with a check mark (interception)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    pts = [(cx - 52, y0 + 10), (cx + 52, y0 + 10), (cx + 52, cy + 6),
           (cx, y1 - 8), (cx - 52, cy + 6)]
    draw.polygon(pts, fill=color)
    draw.line([(cx - 26, cy - 2), (cx - 6, cy + 18), (cx + 30, cy - 24)],
              fill=(255, 255, 255), width=8, joint="curve")


def globe(draw, box):
    """Simple wireframe globe for the masthead."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    rx, ry = (x1 - x0) // 2, (y1 - y0) // 2
    draw.ellipse(box, outline=GOLD, width=3)
    draw.ellipse([cx - 6, y0, cx + 6, y1], outline=GOLD, width=2)
    draw.line([(x0, cy), (x1, cy)], fill=GOLD, width=2)
    draw.arc([cx - rx, cy - ry // 2, cx + rx, cy + ry // 2], 200, 340,
             fill=GOLD, width=2)
    draw.arc([cx - rx, cy - ry // 2, cx + rx, cy + ry // 2], 20, 160,
             fill=GOLD, width=2)


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 132], fill=NAVY)
    draw.rectangle([0, 132, W, 138], fill=GOLD)
    globe(draw, (W - 112, 18, W - 28, 102))
    draw.text((MARGIN, 18), "THE WORLD IN ONE PICTURE",
              font=font(SANS_B, 24), fill=GOLD)
    draw.text((MARGIN, 50), "SATURDAY 21 NOVEMBER 2026",
              font=font(SERIF_B, 44), fill=(255, 255, 255))
    draw.text((MARGIN, 106),
              "The day's world news, summed up in a single image",
              font=font(SANS, 21), fill=(200, 210, 225))

    # Lead story
    lead = (MARGIN, 152, W - MARGIN, 424)
    panel(draw, lead, RED)
    lx = lead[0] + 26
    kicker(draw, (lx, 172), "LEAD STORY  —  EUROPE / NATO", RED)
    headline(draw, (lx, 196), "RUSSIAN MISSILES LAND", 640, start=46)
    headline(draw, (lx, 244), "IN POLAND", 640, start=46)
    body(draw, (lx, 302),
         "Two Russian missiles and a suspected drone came down in "
         "south-east Poland during an overnight barrage on Ukraine. "
         "PM Donald Tusk calls it a deliberate provocation; NATO chief "
         "Mark Rutte calls it a grave violation and travels to Warsaw "
         "today.",
         640, size=20, leading=27)
    icon_missile(draw, (W - MARGIN - 236, 176, W - MARGIN - 24, 400))

    # Two rows of two panels
    pw = (W - 2 * MARGIN - 20) // 2
    rows = [
        (436, [
            ("UKRAINE", "KYIV HIT IN HUGE OVERNIGHT BARRAGE",
             "Russia fired 400+ drones and 110 missiles; at least 8 "
             "killed in Kyiv. France seeks a UN Security Council "
             "meeting.",
             NAVY, icon_burst),
            ("MARKETS", "WALL STREET SLUMPS INTO CORRECTION",
             "The S&P 500 and Dow enter correction as AI shares plunge: "
             "the Nasdaq fell 5.28% on Friday, Nvidia about 14%.",
             DARKRED, icon_chart),
        ]),
        (684, [
            ("DIPLOMACY  —  CHINA", "TRUMP–XI–PUTIN SUMMIT ENDS THIN",
             "The first trilateral summit of the three leaders ends "
             "with few concrete results; Ukraine peace talks stay "
             "stalled.",
             BLUE, icon_summit),
            ("JUSTICE  —  THE HAGUE", "COURT: MYANMAR COMMITTED GENOCIDE",
             "The World Court rules Myanmar's forces committed "
             "state-sponsored genocide against the Rohingya people.",
             TEAL, icon_scales),
        ]),
    ]
    for y0, pair in rows:
        for i, (kick, head, text, accent, icon) in enumerate(pair):
            x0 = MARGIN + i * (pw + 20)
            box = (x0, y0, x0 + pw, y0 + 228)
            panel(draw, box, accent)
            tx = x0 + 24
            kicker(draw, (tx, y0 + 16), kick, accent)
            hy = headline_wrap(draw, (tx, y0 + 40), head, pw - 196,
                               size=26, leading=31)
            body(draw, (tx, hy + 8), text, pw - 196, size=18, leading=24)
            icon(draw, (x0 + pw - 152, y0 + 16, x0 + pw - 16, y0 + 106))

    # Also-today strip (full width)
    strip = (MARGIN, 924, W - MARGIN, 982)
    draw.rounded_rectangle(strip, radius=8, fill=CARD, outline=RULE, width=2)
    draw.rectangle([strip[0], strip[1], strip[0] + 7, strip[3]], fill=RED)
    draw.text((MARGIN + 22, 936), "ALSO TODAY:",
              font=font(SANS_B, 18), fill=RED)
    body(draw, (MARGIN + 168, 936),
         "Riyadh intercepts Houthi missiles  •  Kryvyi Rih: 2 dead, "
         "42 hurt  •  Estonia to shut its Russia border  •  UK and EU "
         "sign food, carbon and youth-mobility deals",
         W - MARGIN - 24 - (MARGIN + 168), size=17, leading=23)

    # Footer
    draw.text((MARGIN, 994),
              "Compiled from news reported on Saturday 21 November 2026. "
              "Figures as stated by officials and wire reports.",
              font=font(SANS, 15), fill=GREY)

    return img


if __name__ == "__main__":
    out = render()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
