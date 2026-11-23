#!/usr/bin/env python3
"""Draw a newspaper front page summing up the world news of Monday 23 Nov 2026.

Deterministic: fixed layout, no randomness, no time, no network.
Writes entry.png (1024x1024) to the repo root.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

# ---- palette -------------------------------------------------------------
PAPER = (244, 238, 224)      # warm off-white newsprint
INK = (28, 26, 24)           # near-black
RED = (150, 30, 30)          # deep red accent (masthead rule + section labels)
BLUE = (30, 50, 90)          # dark blue (panel headers)
GREY = (90, 88, 84)          # muted grey for ticker dots / secondary text
SMOKE = (210, 205, 195)      # light grey for illustration fills

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, max_w):
    """Wrap text into lines that each fit within max_w."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    margin = 40
    content_w = W - 2 * margin

    # ---- masthead --------------------------------------------------------
    mast_font = font(BOLD, 54)
    date_font = font(BOLD, 24)
    mast = "THE WORLD IN ONE PICTURE"
    mw = d.textlength(mast, font=mast_font)
    d.text(((W - mw) / 2, 26), mast, font=mast_font, fill=INK)

    date = "MONDAY, 23 NOVEMBER 2026"
    dw = d.textlength(date, font=date_font)
    d.text(((W - dw) / 2, 96), date, font=date_font, fill=INK)

    # masthead rule (deep red)
    d.rectangle([margin, 136, W - margin, 142], fill=RED)

    # ---- story panels (2x2) ---------------------------------------------
    gap = 24
    panel_w = (content_w - gap) / 2
    panel_h = 300
    top = 158
    row1_y = top
    row2_y = top + panel_h + gap

    headline_font = font(BOLD, 30)
    body_font = font(REG, 20)
    label_font = font(BOLD, 18)
    ill_h = 96

    stories = [
        {
            "label": "CLIMATE",
            "head": "COP31 CLIMATE TALKS COLLAPSE",
            "body": "No deal in Antalya after the EU rejected a draft that dropped fossil-fuel phase-out language.",
            "draw": "globe",
        },
        {
            "label": "WAR",
            "head": "KYIV DRONE STRIKE",
            "body": "At least 14 people are missing after a Russian drone hit a residential building in the Kyiv region.",
            "draw": "drone",
        },
        {
            "label": "SEA",
            "head": "RUSSIAN SHIP ABLAZE",
            "body": "A Russian cargo ship is still on fire off Finland after an attack in the Gulf of Finland.",
            "draw": "ship",
        },
        {
            "label": "FIRE",
            "head": "INDONESIA FACTORY FIRE",
            "body": "Seven bodies recovered and dozens of workers missing after a fire tore through a confectionery factory.",
            "draw": "factory",
        },
    ]

    positions = [
        (margin, row1_y),
        (margin + panel_w + gap, row1_y),
        (margin, row2_y),
        (margin + panel_w + gap, row2_y),
    ]

    for (px, py), st in zip(positions, stories):
        # panel border
        d.rectangle([px, py, px + panel_w, py + panel_h], outline=INK, width=2)

        # section label (deep red)
        d.text((px + 14, py + 10), st["label"], font=label_font, fill=RED)

        # headline (dark blue), wrapped
        hx = px + 14
        hy = py + 40
        head_lines = wrap_lines(d, st["head"], headline_font, panel_w - 28)
        for ln in head_lines:
            d.text((hx, hy), ln, font=headline_font, fill=BLUE)
            hy += 34

        # body text (plain), wrapped, must end with full stop
        body = st["body"]
        if not body.endswith("."):
            body += "."
        bx = px + 14
        by = hy + 6
        body_lines = wrap_lines(d, body, body_font, panel_w - 28)
        for ln in body_lines:
            d.text((bx, by), ln, font=body_font, fill=INK)
            by += 24

        # illustration area at bottom of panel
        iy = py + panel_h - ill_h - 10
        draw_illustration(d, st["draw"], px + 14, iy, panel_w - 28, ill_h)

    # ---- bottom ticker ---------------------------------------------------
    tick_y = row2_y + panel_h + 16
    d.rectangle([margin, tick_y - 6, W - margin, tick_y - 2], fill=RED)
    tick_head_font = font(BOLD, 18)
    tick_head = "ALSO TODAY"
    d.text((margin, tick_y + 6), tick_head, font=tick_head_font, fill=RED)

    tick_items = [
        "24 civilians killed in fresh violence in South Sudan",
        "magnitude 6.1 earthquake jolted northern Japan",
        "South Korea's education minister resigned over an AI exam-cheating scandal",
        "Liverpool hammered ten-man Manchester United in Pochettino's first match as United manager",
        "FIFA set to confirm the UK as host of the 2035 Women's World Cup",
        "UN nations agreed to keep negotiating rules for lethal AI weapons",
        "India vs New Zealand 1st Test goes to a final day",
    ]

    dot = "  \u2022  "
    # choose ticker font size that fits
    tf = font(REG, 18)
    # build lines
    lines = []
    cur = ""
    for item in tick_items:
        piece = (dot + item) if cur else item
        if d.textlength(cur + piece, font=tf) <= content_w:
            cur += piece
        else:
            if cur:
                lines.append(cur)
            cur = item
    if cur:
        lines.append(cur)

    tx = margin
    ty = tick_y + 34
    line_h = 24
    for ln in lines:
        d.text((tx, ty), ln, font=tf, fill=INK)
        ty += line_h

    # footer credit line
    foot_font = font(REG, 18)
    foot = "THE WORLD IN ONE PICTURE  \u2014  MONDAY, 23 NOVEMBER 2026"
    fw = d.textlength(foot, font=foot_font)
    d.text(((W - fw) / 2, H - 30), foot, font=foot_font, fill=GREY)

    img.save("entry.png")
    print("wrote entry.png", img.size)


def draw_illustration(d, kind, x, y, w, h):
    """Draw a small symbolic illustration using only PIL shapes."""
    cx = x + w / 2
    cy = y + h / 2
    if kind == "globe":
        r = h * 0.42
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
        d.ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], outline=GREY, width=2)
        d.line([cx, cy - r, cx, cy + r], fill=GREY, width=2)
        # factory chimneys on globe
        for ox in [-0.25, 0.0, 0.25]:
            bx = cx + ox * r
            d.rectangle([bx - 6, cy - r * 0.55, bx + 6, cy - r * 0.2], fill=INK)
            d.rectangle([bx - 3, cy - r * 0.7, bx + 3, cy - r * 0.55], fill=INK)
        for ox, dy in [(-0.25, -0.8), (0.0, -0.9), (0.25, -0.8)]:
            sx = cx + ox * r
            sy = cy + dy * r
            d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=GREY)
        # cracked document labelled DEAL
        dx = cx + r * 0.55
        dy = cy + r * 0.3
        d.rectangle([dx - 20, dy - 26, dx + 20, dy + 26], outline=INK, width=2, fill=PAPER)
        d.line([dx - 20, dy - 26, dx + 20, dy + 26], fill=INK, width=2)
        d.line([dx + 20, dy - 26, dx - 20, dy + 26], fill=INK, width=2)
        df = font(BOLD, 12)
        dw = d.textlength("DEAL", font=df)
        d.text((dx - dw / 2, dy - 7), "DEAL", font=df, fill=RED)
    elif kind == "drone":
        bx = x + w * 0.28
        bw = w * 0.34
        bh = h * 0.62
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=3, fill=SMOKE)
        for r in range(3):
            for c in range(3):
                wx = bx + 8 + c * (bw - 20) / 3
                wy = by + 8 + r * (bh - 20) / 3
                d.rectangle([wx, wy, wx + 8, wy + 8], fill=INK)
        dx = cx
        dy = y + h * 0.18
        d.line([dx - 26, dy, dx + 26, dy], fill=INK, width=3)
        d.line([dx - 26, dy, dx - 34, dy - 10], fill=INK, width=3)
        d.line([dx + 26, dy, dx + 34, dy - 10], fill=INK, width=3)
        d.ellipse([dx - 8, dy - 6, dx + 8, dy + 6], fill=INK)
        for ang in (-0.35, 0.35):
            ex = dx + ang * 60
            ey = dy + 70
            d.line([dx, dy, ex, ey], fill=RED, width=3)
    elif kind == "ship":
        wy = y + h * 0.72
        for i in range(6):
            wx = x + i * (w / 5)
            d.arc([wx, wy - 8, wx + 20, wy + 8], 180, 360, fill=BLUE, width=2)
        hx = cx - w * 0.28
        hy = wy - 6
        d.polygon([(hx, hy), (hx + w * 0.56, hy), (hx + w * 0.44, hy + 22), (hx + w * 0.12, hy + 22)], outline=INK, fill=SMOKE, width=2)
        d.rectangle([cx - 12, hy - 22, cx + 12, hy], outline=INK, fill=SMOKE, width=2)
        d.line([cx, hy - 22, cx, hy - 46], fill=INK, width=3)
        for ox in (-0.18, 0.0, 0.18):
            fx = cx + ox * w
            fy = hy - 4
            d.polygon([(fx - 8, fy), (fx, fy - 18), (fx + 8, fy)], fill=RED)
        for ox, dy in [(-0.18, -0.5), (0.0, -0.62), (0.18, -0.5)]:
            sx = cx + ox * w
            sy = hy + dy * h * 0.5
            d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=GREY)
    elif kind == "factory":
        bx = x + w * 0.2
        bw = w * 0.6
        bh = h * 0.5
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=3, fill=SMOKE)
        d.polygon([(bx, by), (bx + bw, by), (bx + bw - 12, by - 14), (bx + 12, by - 14)], outline=INK, fill=SMOKE, width=2)
        for ox in (0.2, 0.5, 0.8):
            chx = bx + bw * ox
            d.rectangle([chx - 6, by - 26, chx + 6, by], outline=INK, fill=SMOKE, width=2)
            d.ellipse([chx - 8, by - 34, chx + 8, by - 22], fill=GREY)
        for ox in (0.2, 0.5, 0.8):
            fx = bx + bw * ox
            fy = by - 26
            d.polygon([(fx - 7, fy), (fx, fy - 16), (fx + 7, fy)], fill=RED)
        hx = bx + bw * 0.5
        hy = by + bh - 16
        d.arc([hx - 12, hy - 14, hx + 12, hy + 6], 180, 360, fill=RED, width=4)
        d.rectangle([hx - 12, hy - 2, hx + 12, hy + 2], fill=RED)


if __name__ == "__main__":
    main()