"""Pitch diagrams for regulations / decks (SVG with text -> PNG via Chromium)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vi_lib import C, logo_g
from vi_apps import icon, F_CN, F_EN

B = os.path.dirname(os.path.abspath(__file__))
GRASS, GRASS2, LINE = "#2E8B57", "#33975F", "#FFFFFF"


def t(x, y, s, fill, size, w=700, anchor="middle", fam=F_CN):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{w}" font-family="{fam}" text-anchor="{anchor}">{s}</text>'


def zone(x, y, w, h, color, label, sub="", ic=None, txt="#fff"):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{color}"/>'
    cx = x + w / 2
    if ic:
        o += icon(ic, cx - 13, y + 6, 26, txt)
        o += t(cx, y + 48, label, txt, 15) + (t(cx, y + 66, sub, txt, 11, 500) if sub else "")
    else:
        o += t(cx, y + h / 2 + 2, label, txt, 15) + (t(cx, y + h / 2 + 20, sub, txt, 11, 500) if sub else "")
    return o


def stripes(x, y, L, W, s, n=10):
    o = f'<rect x="{x}" y="{y}" width="{L*s}" height="{W*s}" fill="{GRASS}"/>'
    for i in range(n):
        if i % 2: o += f'<rect x="{x + i*L*s/n}" y="{y}" width="{L*s/n}" height="{W*s}" fill="{GRASS2}"/>'
    return o


def pitch_8v8():
    L, W, s = 68, 50, 10
    x0, y0 = 60, 110
    o = [f'<rect width="800" height="760" fill="#fff"/>', stripes(x0, y0, L, W, s)]
    ln = f'stroke="{LINE}" stroke-width="2.5" fill="none"'
    o.append(f'<rect x="{x0}" y="{y0}" width="{L*s}" height="{W*s}" {ln}/>')
    o.append(f'<line x1="{x0+L*s/2}" y1="{y0}" x2="{x0+L*s/2}" y2="{y0+W*s}" {ln}/>')
    o.append(f'<circle cx="{x0+L*s/2}" cy="{y0+W*s/2}" r="{7*s}" {ln}/>')
    pa_w, pa_d, ga_w, ga_d, g = 29, 12, 13, 4, 5
    for side in (0, 1):
        gx = x0 if side == 0 else x0 + L * s
        sg = 1 if side == 0 else -1
        o.append(f'<rect x="{gx if side==0 else gx-pa_d*s}" y="{y0+(W-pa_w)/2*s}" width="{pa_d*s}" height="{pa_w*s}" {ln}/>')
        o.append(f'<rect x="{gx if side==0 else gx-ga_d*s}" y="{y0+(W-ga_w)/2*s}" width="{ga_d*s}" height="{ga_w*s}" {ln}/>')
        o.append(f'<circle cx="{gx+sg*8*s}" cy="{y0+W*s/2}" r="3" fill="{LINE}"/>')
        o.append(f'<rect x="{gx-12 if side==0 else gx}" y="{y0+(W-g)/2*s}" width="12" height="{g*s}" fill="#fff" stroke="#333"/>')
        ox = gx + sg * 22.7 * s
        o.append(f'<line x1="{ox}" y1="{y0}" x2="{ox}" y2="{y0+W*s}" stroke="{C["gold"]}" stroke-width="3" stroke-dasharray="10 7"/>')
        o.append(t(ox, y0 - 8, "越位线", C["gold"], 13))
    for zx in (x0, x0 + L * s - 22.7 * s):
        o.append(f'<rect x="{zx}" y="{y0}" width="{22.7*s}" height="{W*s}" fill="{C["gold"]}" opacity=".16"/>')
    o.append(t(x0 + 22.7 * s / 2 + 40, y0 + 60, "越位区", "#fff", 18, 900))
    o.append(t(x0 + L * s - 22.7 * s / 2 - 40, y0 + 60, "越位区", "#fff", 18, 900))
    o.append(t(x0 + L * s / 2, y0 + W * s / 2 - 80, "中线 = 球门球退守线", "#fff", 14, 700))
    # dims
    o.append(f'<line x1="{x0}" y1="{y0-30}" x2="{x0+L*s}" y2="{y0-30}" stroke="{C["slate"]}"/>')
    o.append(f'<rect x="{x0+L*s/2-40}" y="{y0-44}" width="80" height="24" fill="#fff"/>')
    o.append(t(x0 + L * s / 2, y0 - 25, "约 68 m", C["ink"], 16, 800, fam=F_EN))
    o.append(f'<text x="{x0-22}" y="{y0+W*s/2}" fill="{C["ink"]}" font-size="16" font-weight="800" font-family="{F_EN}" text-anchor="middle" transform="rotate(-90 {x0-22} {y0+W*s/2})">约 50 m</text>')
    # zones along bottom (bench side) and top (parents)
    yb = y0 + W * s + 16
    o.append(zone(x0 + 20, yb, 140, 72, C["blue"], "主队技术区", "替补席", "TbUsers"))
    o.append(zone(x0 + 170, yb, 100, 72, C["u10"], "冷静区", "暂时罚离", "TbSnowflake"))
    o.append(zone(x0 + L * s / 2 - 60, yb, 120, 72, C["green"], "换人区", "击掌上下", "TbArrowsExchange"))
    o.append(zone(x0 + L * s - 270, yb, 100, 72, C["navy"], "比赛监督", "", "TbUserCheck"))
    o.append(zone(x0 + L * s - 160, yb, 140, 72, C["blue"], "客队技术区", "替补席", "TbUsers"))
    o.append(zone(x0, 14, L * s, 50, C["mist"], "家长观赛区（距边线 ≥ 2 m）· 只加油，不指挥", "", None, C["navy"]))
    for bx in (x0 + 2, x0 + L * s - 40):
        for k in range(3):
            o.append(f'<circle cx="{bx + k*14}" cy="{y0+W*s+8}" r="5.5" fill="#fff" stroke="#333"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 760" style="overflow:hidden">{"".join(o)}</svg>'


def pitch_small(L, W, label, sub, gk=True, goal=3, pa=6):
    s = 300 / max(L, 1) * (1 if L > 30 else 1)
    s = 14 if L <= 20 else 9
    x0, y0 = 30, 50
    o = [stripes(x0, y0, L, W, s, n=6)]
    ln = f'stroke="{LINE}" stroke-width="2" fill="none"'
    o.append(f'<rect x="{x0}" y="{y0}" width="{L*s}" height="{W*s}" {ln}/>')
    o.append(f'<line x1="{x0+L*s/2}" y1="{y0}" x2="{x0+L*s/2}" y2="{y0+W*s}" stroke="{C["gold"]}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    o.append(f'<circle cx="{x0+L*s/2}" cy="{y0+W*s/2}" r="{3*s}" {ln}/>')
    for side in (0, 1):
        gx = x0 if side == 0 else x0 + L * s
        if gk:
            r = pa * s; cy = y0 + W * s / 2; sg = 1 if side == 0 else -1
            o.append(f'<path d="M{gx},{cy-r-goal*s/2} A{r},{r} 0 0 {1 if side==0 else 0} {gx+sg*r},{cy-goal*s/2} L{gx+sg*r},{cy+goal*s/2} A{r},{r} 0 0 {1 if side==0 else 0} {gx},{cy+r+goal*s/2}" {ln}/>')
        gw = goal * s
        o.append(f'<rect x="{gx-8 if side==0 else gx}" y="{y0+W*s/2-gw/2}" width="8" height="{gw}" fill="#fff" stroke="#333"/>')
    Wt = x0 * 2 + L * s
    o.append(t(Wt / 2, 24, label, C["navy"], 20, 900))
    o.append(t(Wt / 2, y0 + W * s + 26, sub, C["slate"], 14, 600))
    o.append(t(x0 + L * s / 2, y0 + W * s - 8, "退守线", C["gold"], 12, 700))
    return Wt, y0 + W * s + 40, "".join(o)


def youth_pitches():
    parts = []; x = 0; H = 0
    for L, W, lab, sub, gk, goal in [(20, 15, "U6 · 3v3", "约 20 × 15 m · 迷你球门 · 无守门员", False, 1.2),
                                      (34, 22, "U8 · 5v5", "约 30–37 × 20–25 m · 3 × 2 m 球门", True, 3),
                                      (38, 22, "U10 · 5v5", "约 36–40 × 20–25 m · 3 × 2 m 球门", True, 3)]:
        w, h, body = pitch_small(L, W, lab, sub, gk, goal)
        parts.append(f'<g transform="translate({x},0)">{body}</g>'); x += w + 10; H = max(H, h)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x} {H}" style="overflow:hidden"><rect width="{x}" height="{H}" fill="#fff"/>{"".join(parts)}</svg>'


if __name__ == "__main__":
    items = {"pitch_8v8": pitch_8v8(), "pitch_youth": youth_pitches()}
    html = ["<html><head><meta charset='utf-8'><style>body{margin:0}</style></head><body>"]
    for k, v in items.items():
        vb = v.split('viewBox="0 0 ')[1].split('"')[0].split()
        html.append(f"<div data-export='{k}' data-scale='1.5' style='display:inline-block;width:{vb[0]}px;height:{vb[1]}px'>{v.replace('<svg ', f'<svg width={vb[0]} height={vb[1]} ', 1)}</div>")
    open(os.path.join(B, "_diagrams.html"), "w").write("".join(html) + "</body></html>")


def export_single():
    items = {}
    for key, args in {"pitch_u6": (20, 15, "U6 · 3v3", "约 20 × 15 m · 迷你球门 · 无守门员", False, 1.2),
                      "pitch_u8": (34, 22, "U8 · 5v5", "约 30–37 × 20–25 m · 3 × 2 m 球门", True, 3),
                      "pitch_u10": (38, 22, "U10 · 5v5", "约 36–40 × 20–25 m · 3 × 2 m 球门", True, 3)}.items():
        w, h, body = pitch_small(*args)
        items[key] = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" style="overflow:hidden"><rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
    return items
