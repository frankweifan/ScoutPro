"""Panda Leagues VI toolkit: brand tokens, vector logo, text-to-outline lockups."""
import os, re, functools
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont, TTCollection

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(HERE)

# ---------------------------------------------------------------- tokens
C = {
    "blue": "#04518E",      # Panda Blue (measured from original logo)
    "navy": "#0B2545",      # Night Navy
    "ink": "#13202F",
    "slate": "#5A6B80",
    "mist": "#E6EEF6",
    "paper": "#F5F8FB",
    "white": "#FFFFFF",
    "gold": "#F2B21B",      # Elite Gold
    "green": "#2FB45A",     # Bamboo Green
    "red": "#E2231A",       # CDHT FA red
    # age group colour code
    "u6": "#FFC72C", "u8": "#2FB45A", "u10": "#1E9BD7", "u11": "#F26A2E",
}

FONTS = {
    "cjk_bold": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 2),
    "cjk_black": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", 2),
    "cjk_medium": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc", 2),
    "cjk_regular": ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 2),
    "cond_xb": (os.path.expanduser("~/.fonts/barlow-condensed-800-normal.ttf"), 0),
    "cond_b": (os.path.expanduser("~/.fonts/barlow-condensed-700-normal.ttf"), 0),
    "cond_sb": (os.path.expanduser("~/.fonts/barlow-condensed-600-normal.ttf"), 0),
    "barlow_sb": (os.path.expanduser("~/.fonts/barlow-600-normal.ttf"), 0),
}


@functools.lru_cache(None)
def _font(key):
    path, idx = FONTS[key]
    blob = hb.Blob.from_file_path(path)
    face = hb.Face(blob, idx)
    font = hb.Font(face)
    tt = TTCollection(path).fonts[idx] if path.endswith(".ttc") else TTFont(path)
    return font, tt, face.upem


def text_path(text, key, size, x=0, y=0, tracking=0.0, anchor="start"):
    """Return (svg path d, width) for text set in font `key` at `size` px with baseline y."""
    font, tt, upem = _font(key)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    s = size / upem
    trk = tracking * size
    total = sum(p.x_advance for p in buf.glyph_positions) * s + trk * (len(buf.glyph_infos) - 1)
    if anchor == "middle": x -= total / 2
    elif anchor == "end": x -= total
    pen = SVGPathPen(gs)
    cx = x
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        tp = TransformPen(pen, (s, 0, 0, -s, cx + pos.x_offset * s, y - pos.y_offset * s))
        gs[name].draw(tp)
        cx += pos.x_advance * s + trk
    return pen.getCommands(), total


def text_el(text, key, size, x=0, y=0, fill="#000", tracking=0.0, anchor="start"):
    d, w = text_path(text, key, size, x, y, tracking, anchor)
    return f'<path fill="{fill}" d="{d}"/>', w

# ---------------------------------------------------------------- logo
_raw = open(os.path.join(SCR, "vi", "logo_raw.svg")).read()
_paths = [d.replace("\n", " ") for d in re.findall(r'<path d="([^"]+)"', _raw, re.S)]
# 0 ring, 1 crown, 2 ear+band, 3 eye R, 4 eye L, 5 nose+mouth, 6 jaw/ball
LOGO_W, LOGO_H = 2748, 2744
CX, CY, R_OUT, R_IN = 1374, 1372, 1334, 1218
_T = 'transform="translate(0,2744) scale(0.1,-0.1)"'


def logo_g(variant="master", x=0, y=0, size=100, disc=True, badge=False):
    """Logo group placed with top-left (x,y), height `size` px.
    variants: master | elite | youth | mono-<hex> | white | knockout"""
    sc = size / LOGO_H
    blue = C["blue"]; crown = blue; ring = blue; art = blue; disc_fill = C["white"]
    if variant == "elite": crown = C["gold"]
    elif variant == "youth": crown = C["green"]
    elif variant.startswith("mono-"):
        blue = crown = ring = art = variant[5:]
    elif variant == "white":          # one-colour white on dark, no disc
        crown = ring = art = C["white"]; disc = False
    elif variant == "knockout":       # white ring + white disc, blue art (for dark bg)
        ring = C["white"]
    parts = [f'<g transform="translate({x:.2f},{y:.2f}) scale({sc:.6f})">']
    if badge:   # keep total footprint = size: shrink artwork inside sticker
        k = 1374 / (R_OUT + 110)
        parts.append(f'<g transform="translate({CX*(1-k):.1f},{CY*(1-k):.1f}) scale({k:.4f})">')
    if badge:   # white sticker disc behind the whole mark, for dark / busy backgrounds
        parts.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT + 110}" fill="{disc_fill}"/>')
    elif disc:
        parts.append(f'<circle cx="{CX}" cy="{CY}" r="{R_IN + 40}" fill="{disc_fill}"/>')
    parts.append(f'<g {_T}>')
    fills = [ring, crown, art, art, art, art, art]
    for d, f in zip(_paths, fills):
        parts.append(f'<path fill="{f}" d="{d}"/>')
    parts.append("</g></g>")
    if badge: parts.append("</g>")
    return "".join(parts)


def svg_doc(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{b}{body}</svg>')


LEAGUES = {
    "umbrella": {"cn": "熊猫足球联赛", "en": "PANDA LEAGUES", "variant": "master", "acc": C["blue"]},
    "elite": {"cn": "熊猫精英足球联赛", "en": "PANDA ELITE LEAGUE", "variant": "elite", "acc": C["gold"]},
    "youth": {"cn": "熊猫少儿足球联赛", "en": "PANDA YOUTH LEAGUE", "variant": "youth", "acc": C["green"]},
}


def lockup_h(league, color_mode="positive", season=True):
    # season=False -> permanent league lockup
    """Horizontal lockup. color_mode: positive (on white) | reverse (on navy/blue)."""
    L = LEAGUES[league]
    txt = C["navy"] if color_mode == "positive" else C["white"]
    sub = C["blue"] if color_mode == "positive" else C["white"]
    variant = L["variant"]
    rev = color_mode != "positive"
    seas = (L["acc"] if rev else C["slate"]) if league != "umbrella" else (C["white"] if rev else C["slate"])
    H = 240
    body = [logo_g(variant, 0, 0, H, disc=True, badge=rev)]
    x0 = H + 44
    body.append(f'<rect x="{H + 22}" y="22" width="3" height="{H - 44}" fill="{sub}" opacity=".35"/>')
    yc, ye = (104, 170) if season else (122, 196)
    e, w1 = text_el(L["cn"], "cjk_black", 74, x0, yc, txt, tracking=0.04)
    body.append(e)
    e, w2 = text_el(L["en"], "cond_xb", 66, x0, ye, sub, tracking=0.06)
    body.append(e)
    w = max(w1, w2)
    if season:
        e, w3 = text_el("2026 AUTUMN · CHENGDU", "cond_sb", 34, x0, 222, seas, tracking=0.18)
        body.append(e); w = max(w, w3)
    W = int(x0 + w + 8)
    return W, H, "".join(body)


def lockup_v(league, color_mode="positive", season=True):
    L = LEAGUES[league]
    txt = C["navy"] if color_mode == "positive" else C["white"]
    sub = C["blue"] if color_mode == "positive" else C["white"]
    variant = L["variant"]
    rev = color_mode != "positive"
    seas = (L["acc"] if rev else C["slate"]) if league != "umbrella" else (C["white"] if rev else C["slate"])
    W = 640; S = 360
    body = [logo_g(variant, (W - S * LOGO_W / LOGO_H) / 2, 0, S, badge=rev)]
    e, _ = text_el(L["cn"], "cjk_black", 64, W / 2, S + 96, txt, tracking=0.06, anchor="middle"); body.append(e)
    e, _ = text_el(L["en"], "cond_xb", 54, W / 2, S + 158, sub, tracking=0.08, anchor="middle"); body.append(e)
    if season:
        e, _ = text_el("2026 AUTUMN · CHENGDU", "cond_sb", 30, W / 2, S + 206, seas, tracking=0.2, anchor="middle"); body.append(e)
    return W, S + (226 if season else 176), "".join(body)


# ---------------------------------------------------------------- auxiliary graphics
import math

def hex_pts(cx, cy, r, rot=0):
    return " ".join(f"{cx + r * math.cos(math.radians(60 * i + rot)):.1f},{cy + r * math.sin(math.radians(60 * i + rot)):.1f}" for i in range(6))


def pent_pts(cx, cy, r, rot=-90):
    return " ".join(f"{cx + r * math.cos(math.radians(72 * i + rot)):.1f},{cy + r * math.sin(math.radians(72 * i + rot)):.1f}" for i in range(5))


def panel_pattern(w, h, r=60, colors=None, seed=7, density=0.22, base=None, stroke=None):
    """'Panda Panel' pattern: hex grid with sparse filled pentagons/hexagons derived from logo's ball panels."""
    import random
    rnd = random.Random(seed)
    colors = colors or [C["blue"]]
    out = []
    if base: out.append(f'<rect width="{w}" height="{h}" fill="{base}"/>')
    dx = r * math.sqrt(3); dy = r * 1.5
    row = 0; y = 0
    while y < h + r:
        x = (dx / 2 if row % 2 else 0)
        while x < w + r:
            if stroke:
                out.append(f'<polygon points="{hex_pts(x, y, r * 0.96, 30)}" fill="none" stroke="{stroke}" stroke-width="{r*0.05:.1f}"/>')
            if rnd.random() < density:
                col = rnd.choice(colors)
                if rnd.random() < 0.45:
                    out.append(f'<polygon points="{pent_pts(x, y, r * 0.62, rnd.choice([-90, -54, -18]))}" fill="{col}"/>')
                else:
                    out.append(f'<polygon points="{hex_pts(x, y, r * 0.84, 30)}" fill="{col}"/>')
            x += dx
        y += dy; row += 1
    return "".join(out)


def growth_rings(cx, cy, r, color, width, n=3, gap=None, opacity=1.0):
    """'Growth Ring' motif: open concentric arcs echoing the logo's open ring (gap at top-left, opening clockwise)."""
    gap = gap or width * 1.6
    out = []
    for i in range(n):
        rr = r + i * (width + gap)
        a0 = math.radians(-120 + i * 18); a1 = math.radians(200 + i * 18)
        x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
        x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
        large = 1 if (a1 - a0) % (2 * math.pi) > math.pi else 0
        out.append(f'<path d="M{x0:.1f},{y0:.1f} A{rr:.1f},{rr:.1f} 0 {large} 1 {x1:.1f},{y1:.1f}" fill="none" '
                   f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity="{opacity}"/>')
    return "".join(out)
