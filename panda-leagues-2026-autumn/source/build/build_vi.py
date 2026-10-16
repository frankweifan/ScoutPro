"""Build the Panda Leagues VI manual (HTML -> PDF) and export the asset kit."""
import os, sys, subprocess, base64, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairosvg
from vi_lib import *
from vi_apps import *

B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(B), "out", "01_VI视觉识别系统")
A = os.path.join(OUT, "assets")
for d in ["logo", "lockup", "graphics", "templates", "applications"]:
    os.makedirs(os.path.join(A, d), exist_ok=True)


def save_svg(path, svgtxt, png_w=None, bg=None):
    open(path, "w").write(svgtxt)
    if png_w:
        cairosvg.svg2png(bytestring=svgtxt.encode(), write_to=path[:-4] + ".png", output_width=png_w, background_color=bg)


def b64img(p):
    ext = p.rsplit(".", 1)[1]
    return f"data:image/{'jpeg' if ext == 'jpg' else ext};base64," + base64.b64encode(open(p, "rb").read()).decode()


# ------------------------------------------------------------------ 1. asset export
S = LOGO_H
for v, fn in [("master", "panda-logo_master"), ("elite", "panda-logo_elite"), ("youth", "panda-logo_youth"),
              (f"mono-{C['blue']}", "panda-logo_mono-blue"), ("mono-#000000", "panda-logo_mono-black"),
              ("white", "panda-logo_mono-white")]:
    save_svg(f"{A}/logo/{fn}.svg", svg_doc(LOGO_W, LOGO_H, logo_g(v, 0, 0, S, disc=(v != "white"))), 2000)
for v in ["master", "elite", "youth"]:
    save_svg(f"{A}/logo/panda-logo_{v}_badge.svg", svg_doc(LOGO_W, LOGO_H, logo_g(v, 0, 0, S, badge=True)), 2000)

for lgk in ["umbrella", "elite", "youth"]:
    for mode in ["positive", "reverse"]:
        for season in [False, True]:
            W, H, body = lockup_h(lgk, mode, season)
            bg = None if mode == "positive" else C["navy"]
            sfx = "_2026autumn" if season else ""
            doc = svg_doc(W + 60, H + 60, f'<g transform="translate(30,30)">{body}</g>', bg)
            save_svg(f"{A}/lockup/{lgk}_horizontal_{mode}{sfx}.svg", doc, 2400)
            W, H, body = lockup_v(lgk, mode, season)
            doc = svg_doc(W + 60, H + 60, f'<g transform="translate(30,30)">{body}</g>', bg)
            save_svg(f"{A}/lockup/{lgk}_vertical_{mode}{sfx}.svg", doc, 1600)

# auxiliary graphics
save_svg(f"{A}/graphics/growth-rings_blue.svg", svg_doc(1200, 1200, growth_rings(600, 600, 300, C["blue"], 60, n=3, gap=60)), 1600)
save_svg(f"{A}/graphics/growth-rings_white.svg", svg_doc(1200, 1200, growth_rings(600, 600, 300, C["white"], 60, n=3, gap=60)), 1600)
for nm, cols, base in [("elite", [C["blue"], C["gold"], C["navy"]], C["navy"]), ("youth", [C["blue"], C["green"], C["u6"], C["u10"]], C["blue"]),
                       ("light", [C["mist"], "#D3E1EF"], C["white"])]:
    save_svg(f"{A}/graphics/panel-pattern_{nm}.svg", svg_doc(1600, 900, panel_pattern(1600, 900, r=56, colors=cols, seed=4, density=.28, base=base)), 1600)

apps = {
    "kit_coach-referee_staff_volunteer": kit_sheet(), "bibs_age-groups": bibs_sheet(), "medals": medals_sheet(),
    "cards_green-yellow-red": cards_sheet(), "backdrop": backdrop(), "perimeter-board_elite": perimeter_board("elite"),
    "perimeter-board_youth": perimeter_board("youth"), "wechat-cover_elite": wechat_cover("elite"), "wechat-cover_youth": wechat_cover("youth"),
    "avatar_elite": avatar("elite"), "avatar_youth": avatar("youth"), "tote-bag": tote(), "bottle": bottle(), "cap": cap(),
    "wristbands": wristbands(), "growth-card_elite": growth_card("elite"), "growth-card_youth": growth_card("youth"),
    "accreditation_elite": accreditation("elite"), "accreditation_youth": accreditation("youth", group="U8", name="王小竹", team="新北小熊队"),
    "corner-flag_elite": corner_flag("elite"), "corner-flag_youth": corner_flag("youth"),
    "matchday-card_youth": result_card("youth"), "letterhead": letterhead(), "business-card": business_card(),
}
SIGNS = [("换人区", "SUB ZONE", "TbArrowsExchange", C["blue"], "#fff", "击掌上下 · 滚动换人"),
         ("家长观赛区", "PARENT ZONE", "TbHeart", C["green"], "#fff", "只加油 不指挥"),
         ("冷静区", "COOL-DOWN ZONE", "TbSnowflake", C["u10"], "#fff", "暂时罚离 · 冷静后归队"),
         ("饮水补给", "HYDRATION", "TbDroplet", C["u6"], C["navy"], "每节休息 及时补水"),
         ("医疗点", "FIRST AID", "TbFirstAidKit", C["red"], "#fff", "受伤请立即示意"),
         ("比赛用球", "MATCH BALLS", "TbBallFootball", C["navy"], "#fff", "多球制 · 非比赛人员勿碰")]
for i, s in enumerate(SIGNS):
    apps[f"sign_{i+1}_{s[1].lower().replace(' ', '-')}"] = sign(*s)

photo = b64img(os.path.join(B, "photos", "p7_x49.jpg"))
photo2 = b64img(os.path.join(B, "photos", "p5_x33.jpg"))
apps["poster_youth"] = poster("youth", photo)
apps["poster_elite"] = poster("elite", photo2)

# app svgs use <text>: export through Chromium for exact fonts
APP_HTML = os.path.join(B, "_apps.html")
html = ["<html><head><meta charset='utf-8'><style>body{margin:0}</style></head><body>"]
for k, v in apps.items():
    vb = v.split('viewBox="0 0 ')[1].split('"')[0].split()
    html.append(f"<div data-export='{k}' style='display:inline-block;width:{vb[0]}px;height:{vb[1]}px'>{v.replace('<svg ', f'<svg width={vb[0]} height={vb[1]} ', 1)}</div>")
html.append("</body></html>")
open(APP_HTML, "w").write("".join(html))

certs = {f"certificate_{lg_}_{k}": certificate(lg_, k) for lg_ in ["elite", "youth"] for k in ["finisher", "growthstar"]}
for k, v in certs.items():
    open(os.path.join(B, f"_{k}.html"), "w").write(
        f"<html><head><meta charset='utf-8'><style>@page{{size:297mm 210mm;margin:0}}body{{margin:0}}svg{{width:297mm;height:210mm;display:block}}</style></head><body>{v}</body></html>")

# ------------------------------------------------------------------ 2. manual
LOGO_SVG = lambda v, d, badge=False: f'<svg viewBox="0 0 {LOGO_W} {LOGO_H}" style="width:{d}mm;height:{d}mm">{logo_g(v, 0, 0, LOGO_H, badge=badge, disc=(v != "white"))}</svg>'


def lock_svg(lgk, mode="positive", season=False, h=None, w=None, vertical=False):
    W, H, body = (lockup_v if vertical else lockup_h)(lgk, mode, season)
    st = f"height:{h}mm" if h else f"width:{w}mm"
    return f'<svg viewBox="0 0 {W} {H}" style="{st}">{body}</svg>'


def page(title_cn, title_en, sec, n, content, dark=False, cls=""):
    return f'''<section class="page {'dark' if dark else ''} {cls}">
<header><span class="sec">{sec}</span><span class="pt">{title_cn}<em>{title_en}</em></span></header>
<div class="content">{content}</div>
<footer><span>熊猫足球联赛 视觉识别系统 · PANDA LEAGUES VISUAL IDENTITY 2026</span><span class="pn">{n:02d}</span></footer></section>'''


css = f"""
@page {{ size: 297mm 210mm; margin: 0 }}
* {{ box-sizing: border-box }}
body {{ margin:0; font-family:'Noto Sans CJK SC',sans-serif; color:{C['ink']}; -webkit-print-color-adjust:exact }}
.page {{ width:297mm; height:210mm; position:relative; overflow:hidden; page-break-after:always; background:#fff; padding:16mm 18mm 14mm }}
.page.dark {{ background:{C['navy']}; color:#fff }}
header {{ display:flex; align-items:baseline; gap:6mm; margin-bottom:7mm }}
header .sec {{ font-family:'Barlow Condensed'; font-weight:800; font-size:11pt; color:#fff; background:{C['blue']}; padding:1mm 3mm; border-radius:1mm; letter-spacing:.08em }}
header .pt {{ font-size:20pt; font-weight:900; letter-spacing:.04em }}
header .pt em {{ font-style:normal; font-family:'Barlow Condensed'; font-weight:700; font-size:13pt; color:{C['slate']}; margin-left:4mm; letter-spacing:.12em }}
.dark header .pt em {{ color:#9FB6D1 }}
footer {{ position:absolute; left:18mm; right:18mm; bottom:8mm; display:flex; justify-content:space-between; font-size:7.5pt; color:{C['slate']}; font-family:'Barlow','Noto Sans CJK SC' }}
.dark footer {{ color:#8EA3BD }}
footer .pn {{ font-family:'Barlow Condensed'; font-weight:800; font-size:11pt; color:{C['blue']} }}
.dark footer .pn {{ color:{C['gold']} }}
.content {{ height:160mm; position:relative }}
p, li {{ font-size:9.5pt; line-height:1.75; margin:0 0 2.5mm }}
h3 {{ font-size:12pt; margin:0 0 2.5mm; font-weight:900 }}
h3 em {{ font-family:'Barlow Condensed'; font-style:normal; font-weight:700; color:{C['slate']}; margin-left:2mm; letter-spacing:.08em; font-size:10pt }}
.cols {{ display:grid; gap:8mm }}
.c2 {{ grid-template-columns:1fr 1fr }} .c3 {{ grid-template-columns:1fr 1fr 1fr }} .c4 {{ grid-template-columns:repeat(4,1fr) }}
.c13 {{ grid-template-columns:1fr 2fr }} .c31 {{ grid-template-columns:2fr 1fr }}
.panel {{ background:{C['paper']}; border-radius:3mm; padding:6mm; display:flex; align-items:center; justify-content:center; flex-direction:column }}
.panel.navy {{ background:{C['navy']} }} .panel.blue {{ background:{C['blue']} }}
.cap {{ font-size:8pt; color:{C['slate']}; margin-top:2.5mm; text-align:center }}
.dark .cap {{ color:#9FB6D1 }}
.swatch {{ border-radius:3mm; overflow:hidden; border:1px solid #E1E7EE }}
.swatch .chip {{ height:30mm; padding:3mm; display:flex; align-items:flex-end; font-family:'Barlow Condensed'; font-weight:800; font-size:13pt; letter-spacing:.06em }}
.swatch .meta {{ padding:2.5mm 3mm; font-size:7.5pt; line-height:1.6; color:{C['ink']}; font-family:'Barlow','Noto Sans CJK SC' }}
.swatch .meta b {{ font-family:'Noto Sans CJK SC'; font-size:9pt }}
.tag {{ display:inline-block; font-family:'Barlow Condensed'; font-weight:800; letter-spacing:.08em; font-size:9pt; padding:.6mm 2.4mm; border-radius:5mm; background:{C['mist']}; color:{C['blue']} }}
.no {{ position:relative }}
.no:after {{ content:'✕'; position:absolute; right:2mm; top:1mm; color:{C['red']}; font-weight:900; font-size:14pt }}
.app {{ display:flex; flex-direction:column; align-items:center; justify-content:center }}
.app svg {{ max-width:100%; max-height:100% }}
.big {{ font-family:'Barlow Condensed'; font-weight:800 }}
table.spec {{ border-collapse:collapse; width:100%; font-size:8.5pt }}
table.spec td, table.spec th {{ border-bottom:1px solid #E1E7EE; padding:2mm 2mm; text-align:left; vertical-align:top }}
table.spec th {{ color:{C['slate']}; font-weight:500; width:28% }}
"""

pages = []
n = 0


def add(*a, **k):
    global n
    n += 1
    pages.append(page(*a[:3], n, *a[3:], **k))


# cover
n += 1
pages.append(f'''<section class="page dark" style="padding:0">
<svg style="position:absolute;right:-40mm;top:-30mm;width:230mm;height:230mm;opacity:.9" viewBox="0 0 1200 1200">{growth_rings(600, 600, 300, C['blue'], 70, n=3, gap=70)}</svg>
<div style="position:absolute;right:28mm;top:42mm">{LOGO_SVG('master', 112, badge=True)}</div>
<div style="position:absolute;left:20mm;top:22mm"><span class="tag" style="background:{C['gold']};color:{C['navy']}">VISUAL IDENTITY MANUAL</span></div>
<div style="position:absolute;left:20mm;top:78mm;width:150mm">
<div style="font-size:15pt;font-weight:700;color:#9FB6D1;letter-spacing:.2em">熊猫精英足球联赛 · 熊猫少儿足球联赛</div>
<div style="font-size:44pt;font-weight:900;line-height:1.15;margin-top:4mm">熊猫足球联赛<br/>视觉识别系统</div>
<div class="big" style="font-size:24pt;color:{C['gold']};letter-spacing:.12em;margin-top:4mm">PANDA LEAGUES · VI MANUAL</div></div>
<div style="position:absolute;left:20mm;bottom:16mm;font-size:9pt;color:#9FB6D1;line-height:1.7">成都高新区足球协会<br/><span class="big" style="letter-spacing:.12em">CDHT FOOTBALL ASSOCIATION · V1.0 · 2026.10</span></div>
</section>''')

# contents
toc = [("A", "品牌核心", "Brand Core", ["品牌理念", "品牌架构"]),
       ("B", "基础要素", "Basic Elements", ["标志释义", "标志制图与安全空间", "标志色彩变体", "联赛组合标志", "标志错误使用", "标准色彩", "年龄组识别色", "标准字体", "辅助图形：成长环", "辅助图形：熊猫球面纹", "图标系统", "摄影风格"]),
       ("C", "应用系统", "Applications", ["办公事务", "证件与手环", "服装与背心", "奖牌与牌卡", "证书", "赛场导视", "赛场品牌环境", "数字媒体", "球员成长卡与赛日图", "纪念品"])]
tc = '<div class="cols c3">'
pn = 3
for code, cn, en, items in toc:
    tc += f'<div><div class="big" style="font-size:44pt;color:{C["blue"]};line-height:1">{code}</div><h3>{cn}<em>{en.upper()}</em></h3><ol style="padding-left:5mm;margin:0">'
    for it in items:
        tc += f'<li style="font-size:10pt;line-height:2">{it}<span style="float:right;font-family:Barlow Condensed;font-weight:700;color:{C["slate"]}">{pn:02d}</span></li>'
        pn += 1
    tc += "</ol></div>"
tc += "</div>"
add("目录", "CONTENTS", "INDEX", tc)

# A1 brand idea
vals = [("TbSeedling", "成长", "GROWTH", "以球员成长为中心。比赛是训练的延伸，每一次触球、每一次尝试都是成长。"),
        ("TbHeartHandshake", "尊重", "RESPECT", "尊重对手、队友、执裁者与家长；用握手与致谢开始和结束每一场比赛。"),
        ("TbMoodHappy", "快乐", "JOY", "让孩子爱上足球——足够的上场时间、自由的决策空间、积极的场边声音。"),
        ("TbScale", "公平", "FAIR PLAY", "按实力分组、保持竞争、均等上场；用绿牌表彰诚实与善意。")]
c = f'''<div class="cols c13" style="height:100%"><div style="display:flex;flex-direction:column;justify-content:center">
<div style="font-size:30pt;font-weight:900;line-height:1.3;color:{C['navy']}">为了每个人<br/>更好的成长</div>
<div class="big" style="font-size:18pt;color:{C['blue']};letter-spacing:.08em;margin:3mm 0 6mm">FOR BETTER GROWTH OF EVERYONE</div>
<p>熊猫足球联赛始于 2017 年，由成都高新区足球协会主办。我们相信：比赛是足球运动的核心，而每一个孩子都应拥有在比赛中成长的机会。视觉系统的一切表达，都服务于这一信念。</p></div>
<div class="cols c2" style="gap:5mm">'''
for ic, cn, en, txt in vals:
    c += f'<div class="panel" style="align-items:flex-start;justify-content:flex-start"><svg viewBox="0 0 24 24" style="width:12mm;height:12mm">{icon(ic,0,0,24,C["blue"])}</svg><h3 style="margin-top:3mm">{cn}<em>{en}</em></h3><p style="margin:0">{txt}</p></div>'
c += "</div></div>"
add("品牌理念", "BRAND IDEA", "A1", c)

# A2 architecture
c = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:6mm">
<div class="panel" style="width:150mm;padding:5mm">{lock_svg('umbrella', h=24)}<div class="cap">主品牌 Master Brand：熊猫足球联赛 —— 两项联赛共享的品牌资产</div></div>
<svg viewBox="0 0 600 40" style="width:150mm;height:10mm"><path d="M300,0 V20 M150,20 H450 M150,20 V40 M450,20 V40" stroke="{C['slate']}" stroke-width="2" fill="none"/></svg>
<div class="cols c2" style="width:100%">
<div class="panel">{lock_svg('elite', h=22)}<div class="cap" style="text-align:left;line-height:1.7;margin-top:4mm"><b style="color:{C['ink']}">熊猫精英足球联赛 · 识别色 Elite Gold</b><br/>每周六下午 · 8人制 · U10 / U11<br/>标志皇冠以“精英金”表达：在成长中追求卓越。</div></div>
<div class="panel">{lock_svg('youth', h=22)}<div class="cap" style="text-align:left;line-height:1.7;margin-top:4mm"><b style="color:{C['ink']}">熊猫少儿足球联赛 · 识别色 Bamboo Green</b><br/>每周日上午 · 3人制 U6 / 5人制 U8、U10<br/>标志皇冠以“竹叶绿”表达：像竹子一样，节节生长。</div></div>
</div></div>'''
add("品牌架构", "BRAND ARCHITECTURE", "A2", c)

# B1 logo meaning
c = f'''<div class="cols c2" style="height:100%;align-items:center"><div class="panel" style="height:150mm">{LOGO_SVG('master', 110)}</div>
<div><h3>标志释义<em>THE MARK</em></h3>
<p><b>熊猫 · 成都</b>　熊猫是成都的城市名片，也是联赛的名字。熊猫面部由足球的五边形、六边形球皮切面构成——熊猫就是足球，足球就是熊猫。</p>
<p><b>皇冠 · 每个人都是冠军</b>　皇冠戴在每一个孩子头上，而不是只属于赢得比赛的人。它传达联赛最核心的主张：每一名通过比赛获得成长的球员，都是冠军。</p>
<p><b>开放的圆环 · 成长环</b>　外环在左上与右下两处“开口”，像一条不断向前延展的跑道，也像年轮——成长没有终点，联赛向所有孩子敞开。</p>
<p><b>熊猫蓝</b>　取自原标志的深海蓝，冷静、可信赖、专业，是整个系统的主导色。</p>
<p style="color:{C['slate']};font-size:8.5pt">本手册中的标志由原有标志位图精确矢量化重建（SVG），造型与比例保持不变，仅新增两项联赛的皇冠识别色变体。</p></div></div>'''
add("标志释义", "LOGO MEANING", "B1", c)

# B2 construction
grid = "".join(f'<line x1="{i*274.8}" y1="0" x2="{i*274.8}" y2="2744" stroke="{C["u10"]}" stroke-width="5" opacity=".35"/><line x1="0" y1="{i*274.4}" x2="2748" y2="{i*274.4}" stroke="{C["u10"]}" stroke-width="5" opacity=".35"/>' for i in range(11))
cons = (f'<svg viewBox="-700 -700 4148 4144" style="height:140mm"><rect x="-700" y="-700" width="4148" height="4144" fill="{C["paper"]}"/>'
        f'<rect x="-550" y="-550" width="3848" height="3844" fill="none" stroke="{C["red"]}" stroke-width="8" stroke-dasharray="40 30"/>'
        f'{grid}{logo_g("master",0,0,2744)}'
        f'<circle cx="{CX}" cy="{CY}" r="{R_OUT}" fill="none" stroke="{C["red"]}" stroke-width="6"/>'
        f'<circle cx="{CX}" cy="{CY}" r="{R_IN}" fill="none" stroke="{C["red"]}" stroke-width="6" stroke-dasharray="20 20"/>'
        f'<text x="-520" y="-580" font-size="120" fill="{C["red"]}" font-family="Barlow Condensed" font-weight="800">CLEAR SPACE = X</text>'
        f'<path d="M-550,1372 H0" stroke="{C["red"]}" stroke-width="8"/><text x="-470" y="1330" font-size="150" fill="{C["red"]}" font-family="Barlow Condensed" font-weight="800">X</text></svg>')
c = f'''<div class="cols c2" style="height:100%;align-items:center"><div class="panel">{cons}</div>
<div><h3>制图规范<em>CONSTRUCTION</em></h3><p>标志置于 10 × 10 单元网格内，外环与内环为同心圆，圆心与网格中心重合。外环直径 = 10 单元；内环直径约 8.9 单元。</p>
<h3 style="margin-top:6mm">安全空间<em>CLEAR SPACE</em></h3><p>以标志直径的 1/5 为 X。标志四周至少保留 X 的空白，任何文字、图形、版边不得进入该区域。</p>
<h3 style="margin-top:6mm">最小尺寸<em>MINIMUM SIZE</em></h3>
<table class="spec"><tr><th>印刷</th><td>标志直径 ≥ 12 mm；组合标志高度 ≥ 10 mm</td></tr><tr><th>屏幕</th><td>标志直径 ≥ 48 px；组合标志高度 ≥ 40 px</td></tr><tr><th>刺绣 / 丝印</th><td>标志直径 ≥ 30 mm（细节需保持清晰）</td></tr></table></div></div>'''
add("标志制图与安全空间", "CONSTRUCTION & CLEAR SPACE", "B2", c)

# B3 colour variants
vv = [("master", "标准彩色", "白底首选", "panel"), ("master", "反白徽章", "深色 / 图片背景", "panel navy", True),
      (f"mono-{C['blue']}", "单色蓝", "单色印刷", "panel"), ("mono-#000000", "单色黑", "传真 / 黑白印刷", "panel"),
      ("white", "单色白", "烫印、刺绣、深色单色", "panel blue"), ("elite", "精英联赛变体", "皇冠 · 精英金", "panel"),
      ("youth", "少儿联赛变体", "皇冠 · 竹叶绿", "panel"), ("elite", "精英徽章", "深色背景", "panel navy", True)]
c = '<div class="cols c4" style="gap:5mm">'
for item in vv:
    v, cn, use, cls = item[:4]; badge = len(item) > 4
    c += f'<div><div class="{cls}" style="height:58mm">{LOGO_SVG(v, 40, badge)}</div><div class="cap"><b style="color:{C["ink"]}">{cn}</b> · {use}</div></div>'
c += "</div>"
add("标志色彩变体", "LOGO COLOUR VARIANTS", "B3", c)

# B4 lockups
c = f'''<div class="cols c2" style="gap:6mm">
<div class="panel" style="height:44mm">{lock_svg('elite', h=24)}</div><div class="panel navy" style="height:44mm">{lock_svg('elite','reverse', h=24)}</div>
<div class="panel" style="height:44mm">{lock_svg('youth', h=24)}</div><div class="panel navy" style="height:44mm">{lock_svg('youth','reverse', h=24)}</div></div>
<div class="cols c4" style="margin-top:6mm;gap:6mm;align-items:center">
<div class="panel" style="height:52mm">{lock_svg('elite', vertical=True, season=True, h=42)}</div>
<div class="panel" style="height:52mm">{lock_svg('youth', vertical=True, season=True, h=42)}</div>
<div style="grid-column:span 2"><h3>组合规范<em>LOCKUPS</em></h3><p>中文名使用思源黑体 Heavy，英文名使用 Barlow Condensed ExtraBold，二者左对齐；标志与文字间以细分隔线区隔。赛季版本在第三行增加“2026 AUTUMN · CHENGDU”。横式用于横幅、页眉、背景板；竖式用于海报、证书、奖牌等居中构图。</p></div></div>'''
add("联赛组合标志", "LEAGUE LOCKUPS", "B4", c)

# B5 misuse
def mis(trans, note, extra=""):
    return f'<div><div class="panel no" style="height:46mm;{extra}"><div style="transform:{trans}">{LOGO_SVG(misv.pop(0) if misv else "master", 30)}</div></div><div class="cap">{note}</div></div>'
misv = ["master", "mono-#E2231A", "master", "master", "master", "master", "master", "master"]
c = '<div class="cols c4" style="gap:5mm">'
c += mis("scaleX(1.45)", "不得拉伸或压扁")
c += mis("none", "不得更改标准色")
c += mis("rotate(-25deg)", "不得旋转")
c += mis("none", "不得置于杂乱背景上（请使用反白徽章）", "background:repeating-linear-gradient(45deg,#F2B21B 0 6mm,#2FB45A 6mm 12mm)")
c += mis("none", "不得添加投影、描边等特效", "filter:drop-shadow(2mm 2mm 1.5mm rgba(0,0,0,.6))")
c += mis("none", "不得置于低对比度背景", f"background:{C['blue']}")
c += mis("scale(.55)", "不得小于最小尺寸 / 不得侵占安全空间", "")
c += f'<div><div class="panel no" style="height:46mm"><div style="font-family:serif;font-size:18pt;font-weight:700;color:{C["blue"]};text-align:center">熊猫精英联赛<br/><i>Panda Elite</i></div></div><div class="cap">不得改用其他字体重设名称</div></div>'
c += "</div>"
add("标志错误使用", "INCORRECT USAGE", "B5", c)

# B6 colours
PAL = [("熊猫蓝", "PANDA BLUE", C["blue"], "C100 M65 Y10 K10", "4 81 142", "PANTONE 7686 C", "#fff", "主导色 · 60%"),
       ("夜空藏青", "NIGHT NAVY", C["navy"], "C100 M85 Y40 K40", "11 37 69", "PANTONE 289 C", "#fff", "深色背景 · 正文"),
       ("精英金", "ELITE GOLD", C["gold"], "C0 M32 Y92 K0", "242 178 27", "PANTONE 1235 C", C["navy"], "精英联赛识别色"),
       ("竹叶绿", "BAMBOO GREEN", C["green"], "C75 M0 Y85 K0", "47 180 90", "PANTONE 354 C", "#fff", "少儿联赛识别色"),
       ("高新红", "CDHT RED", C["red"], "C0 M95 Y95 K0", "226 35 26", "PANTONE 485 C", "#fff", "主办方 · 警示"),
       ("岩灰", "SLATE", C["slate"], "C65 M45 Y30 K15", "90 107 128", "PANTONE 7545 C", "#fff", "辅助文字"),
       ("雾蓝", "MIST", C["mist"], "C10 M4 Y2 K0", "230 238 246", "PANTONE 656 C", C["navy"], "底色 · 分区"),
       ("纯白", "WHITE", "#FFFFFF", "C0 M0 Y0 K0", "255 255 255", "—", C["navy"], "留白 · 反白")]
c = '<div class="cols c4" style="gap:5mm">'
for cn, en, hx, cmyk, rgb, pms, tc_, use in PAL:
    c += (f'<div class="swatch"><div class="chip" style="background:{hx};color:{tc_}">{en}</div><div class="meta"><b>{cn}</b> · {use}<br/>'
          f'HEX {hx.upper()}<br/>RGB {rgb}<br/>CMYK {cmyk}<br/>{pms}</div></div>')
c += f'</div><p style="font-size:7.5pt;color:{C["slate"]};margin-top:4mm">色彩比例建议：熊猫蓝 / 藏青 60%，白与雾蓝 30%，联赛识别色 ≤10%。CMYK 与 PANTONE 为印刷参考值，正式印制前须以实物色卡打样校准。</p>'
add("标准色彩", "COLOUR PALETTE", "B6", c)

# B7 age colours
AG = [("U6", C["u6"], "C0 M22 Y88 K0 · PANTONE 123 C", "少儿联赛 · 3人制", C["navy"]),
      ("U8", C["u8"], "C75 M0 Y85 K0 · PANTONE 354 C", "少儿联赛 · 5人制", "#fff"),
      ("U10", C["u10"], "C78 M25 Y0 K0 · PANTONE 299 C", "少儿 5人制 / 精英 8人制", "#fff"),
      ("U11", C["u11"], "C0 M70 Y88 K0 · PANTONE 165 C", "精英联赛 · 8人制", "#fff")]
c = '<div class="cols c4" style="gap:5mm">'
for lab, hx, spec, use, tc_ in AG:
    c += f'<div class="swatch"><div class="chip" style="background:{hx};color:{tc_};height:44mm;font-size:36pt">{lab}</div><div class="meta"><b>{use}</b><br/>HEX {hx}<br/>{spec}</div></div>'
c += f'''</div><div class="cols c2" style="margin-top:6mm;align-items:center"><div><h3>年龄组识别色<em>AGE-GROUP CODING</em></h3>
<p>四个年龄组各有一个识别色，贯穿手环、证件色条、训练背心、场地分区牌、赛程表与线上图文。家长和孩子一眼就能找到自己的场地与时间。U10 色在两个联赛中通用。</p></div>
<div class="panel" style="height:44mm">{wristbands().replace('style="overflow:hidden"','style="overflow:hidden;height:38mm"',1)}</div></div>'''
add("年龄组识别色", "AGE-GROUP COLOURS", "B7", c)

# B8 typography
c = f'''<div class="cols c3" style="gap:6mm">
<div class="panel" style="align-items:flex-start;justify-content:flex-start"><span class="tag">中文 · CHINESE</span>
<div style="font-size:40pt;font-weight:900;margin:4mm 0 0;line-height:1.1">思源黑体</div><div class="big" style="color:{C['slate']};font-size:12pt;letter-spacing:.06em">SOURCE HAN SANS SC / NOTO SANS SC</div>
<p style="margin-top:4mm">Heavy 标题 · Bold 小标题 · Regular 正文。开源免费商用（SIL OFL）。Office 文档中以 <b>微软雅黑</b> 替代。</p></div>
<div class="panel" style="align-items:flex-start;justify-content:flex-start"><span class="tag">英文标题 · DISPLAY</span>
<div class="big" style="font-size:44pt;margin:3mm 0 0;line-height:1.05;letter-spacing:.02em">BARLOW<br/>CONDENSED</div>
<p style="margin-top:4mm">ExtraBold / Bold，用于英文名称、数字、比分、年龄组标签。窄体、有力，如球衣号码。Office 中以 Arial Narrow 替代。</p></div>
<div class="panel" style="align-items:flex-start;justify-content:flex-start"><span class="tag">英文正文 · TEXT</span>
<div style="font-family:Barlow;font-weight:700;font-size:40pt;margin:4mm 0 0;line-height:1.1">Barlow</div>
<p style="margin-top:4mm;font-family:Barlow,'Noto Sans CJK SC'">Regular / SemiBold，用于英文正文与说明。Office 中以 Arial 替代。The quick brown panda kicks the ball.</p></div></div>
<div style="margin-top:7mm;display:grid;grid-template-columns:30mm 1fr;row-gap:2mm;align-items:baseline">
<span class="tag">H1 28–44pt</span><span style="font-size:24pt;font-weight:900">每个人都是冠军</span>
<span class="tag">H2 18–24pt</span><span style="font-size:16pt;font-weight:700">均等上场，位置轮换</span>
<span class="tag">BODY 10–14pt</span><span style="font-size:10pt">所有到场球员上场时间不少于全场比赛时间的一半，包括守门员位置的轮换。</span>
<span class="tag">NUMBER</span><span class="big" style="font-size:24pt;color:{C['blue']}">8V8 · 4×20′ · U10 / U11</span></div>'''
add("标准字体", "TYPOGRAPHY", "B8", c)

# B9 growth rings
c = f'''<div class="cols c31" style="height:100%"><div class="cols c2" style="gap:5mm">
<div class="panel navy" style="height:72mm;overflow:hidden;position:relative"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{growth_rings(330, 260, 90, C['blue'], 26, n=3, gap=22)}{growth_rings(330,260,90,C['gold'],5,n=1)}</svg></div>
<div class="panel" style="height:72mm;overflow:hidden"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{growth_rings(60, 40, 70, C['mist'], 22, n=4, gap=18)}{growth_rings(60,40,70,C['green'],5,n=1)}</svg></div>
<div class="panel blue" style="height:72mm;overflow:hidden"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{growth_rings(200, 150, 50, '#ffffff', 12, n=4, gap=16, opacity=.35)}{logo_g('master',160,110,80,badge=True)}</svg></div>
<div class="panel" style="height:72mm;overflow:hidden"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{growth_rings(200, 150, 40, C['u6'], 9, n=1)}{growth_rings(200, 150, 62, C['u8'], 9, n=1)}{growth_rings(200, 150, 84, C['u10'], 9, n=1)}{growth_rings(200, 150, 106, C['u11'], 9, n=1)}</svg></div></div>
<div><h3>成长环<em>GROWTH RINGS</em></h3><p>提取自标志的“开放圆环”。多层同心、带开口的圆弧，像年轮，也像跑道——寓意一年年、一场场的成长。</p>
<p>· 常以大尺度出血裁切于版面一角，营造动感；<br/>· 可用熊猫蓝叠加一条联赛识别色细环作点缀；<br/>· 可按年龄组识别色由内向外排列，表达“从 U6 到 U11 的成长路径”；<br/>· 开口方向保持左上，不得闭合成完整圆。</p></div></div>'''
add("辅助图形：成长环", "AUXILIARY GRAPHIC · GROWTH RINGS", "B9", c)

# B10 panels
c = f'''<div class="cols c31" style="height:100%"><div class="cols c2" style="gap:5mm">
<div class="swatch" style="height:72mm"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{panel_pattern(400,300,r=26,colors=[C['blue'],C['gold'],'#1A3A66'],seed=4,density=.3,base=C['navy'])}</svg></div>
<div class="swatch" style="height:72mm"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{panel_pattern(400,300,r=26,colors=[C['green'],C['u6'],C['u10'],'#0F63A8'],seed=8,density=.3,base=C['blue'])}</svg></div>
<div class="swatch" style="height:72mm"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{panel_pattern(400,300,r=26,colors=[C['mist'],'#D3E1EF'],seed=2,density=.45,base='#fff')}</svg></div>
<div class="swatch" style="height:72mm"><svg viewBox="0 0 400 300" style="width:100%;height:100%">{panel_pattern(400,300,r=30,colors=[C['blue']],seed=6,density=.12,base='#fff',stroke='#E1E7EE')}</svg></div></div>
<div><h3>熊猫球面纹<em>PANDA PANELS</em></h3><p>熊猫脸上的眼圈与下颌，本身就是足球的五边形与六边形球皮。将其拆解为蜂巢网格，随机点亮部分五边形 / 六边形，构成可无限延展的底纹。</p>
<p>· 精英联赛：藏青底 + 熊猫蓝 / 精英金；<br/>· 少儿联赛：熊猫蓝底 + 竹叶绿 / 年龄组色，更活泼；<br/>· 浅色版用于文档底纹与证书，不干扰阅读；<br/>· 点亮密度控制在 10%–35%。</p></div></div>'''
add("辅助图形：熊猫球面纹", "AUXILIARY GRAPHIC · PANDA PANELS", "B10", c)

# B11 icons
ICS = [("TbBallFootball", "比赛"), ("TbClock", "时间"), ("TbArrowsExchange", "滚动换人"), ("TbUsersGroup", "全员上场"), ("TbRotate", "位置轮换"),
       ("TbUserPlus", "保持竞争"), ("TbHeartHandshake", "绿牌·公平"), ("TbSnowflake", "冷静区"), ("TbHeart", "家长区"), ("TbMessageCircle", "提问式指导"),
       ("TbMedal", "完赛奖牌"), ("TbStar", "成长之星"), ("TbShieldCheck", "保险"), ("TbFirstAidKit", "医疗"), ("TbDroplet", "补水"),
       ("TbCalendarEvent", "赛程"), ("TbMapPin", "场地"), ("TbSoccerField", "场地规格"), ("TbVideo", "影像"), ("TbChecklist", "报名")]
c = '<div class="cols" style="grid-template-columns:repeat(10,1fr);gap:4mm">'
for ic, lab in ICS:
    c += f'<div style="text-align:center"><div style="width:20mm;height:20mm;border-radius:50%;background:{C["mist"]};display:flex;align-items:center;justify-content:center;margin:0 auto"><svg viewBox="0 0 24 24" style="width:10mm;height:10mm">{icon(ic,0,0,24,C["blue"])}</svg></div><div class="cap" style="color:{C["ink"]}">{lab}</div></div>'
c += f'''</div><div class="cols c2" style="margin-top:8mm"><div><h3>图标系统<em>ICONOGRAPHY</em></h3><p>采用开源 Tabler Icons 线性图标（MIT 许可），2px 线宽、圆角端点，与标志的几何切面风格协调。图标通常置于雾蓝或熊猫蓝圆形底上，用于规则说明、导视牌与数字图文。</p></div>
<div style="display:flex;gap:5mm;align-items:center">{''.join(f'<div style="width:22mm;height:22mm;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 24 24" style="width:11mm;height:11mm">{icon("TbBallFootball",0,0,24,fg)}</svg></div>' for bg,fg in [(C['mist'],C['blue']),(C['blue'],'#fff'),(C['navy'],C['gold']),(C['green'],'#fff')])}</div></div>'''
add("图标系统", "ICONOGRAPHY", "B11", c)

# B12 photography
ph = ["p7_x48", "p5_x34", "p4_x29", "p6_x39", "p8_x54", "p9_x60"]
c = '<div class="cols c3" style="gap:4mm">' + "".join(f'<div style="height:52mm;border-radius:3mm;background:url({b64img(os.path.join(B,"photos",p+".jpg"))}) center/cover"></div>' for p in ph) + "</div>"
c += f'''<div class="cols c3" style="margin-top:6mm"><div><h3>以孩子为主角<em>KIDS FIRST</em></h3><p>镜头放低到孩子的视线高度；捕捉尝试、协作、庆祝和鼓励，而非只拍进球者。</p></div>
<div><h3>真实与自然<em>REAL MOMENTS</em></h3><p>使用自然光与真实场景，避免过度修图和摆拍；色调偏冷、干净，与熊猫蓝协调。</p></div>
<div><h3>尊重与保护<em>SAFEGUARDING</em></h3><p>仅使用已签署肖像权授权的球员影像；不发布可识别孩子身份的个人信息；不以比分或失误为主题。</p></div></div>'''
add("摄影风格", "PHOTOGRAPHY", "B12", c)


def appimg(k, h):
    v = apps[k]
    return v.replace('style="overflow:hidden"', f'style="overflow:hidden;height:{h}mm;max-width:100%"', 1)


# C1 stationery
c = f'''<div class="cols c3" style="gap:6mm;height:150mm;align-items:center">
<div class="app"><div style="box-shadow:0 2mm 6mm rgba(0,0,0,.15)">{appimg('letterhead', 120)}</div><div class="cap">A4 信纸 / 文件页眉（Word 规程与规则精要沿用此页眉）</div></div>
<div class="app" style="gap:6mm"><div style="box-shadow:0 2mm 6mm rgba(0,0,0,.15);border-radius:2mm">{appimg('business-card', 48)}</div><div class="cap">名片 90×54mm</div>
<div style="box-shadow:0 2mm 6mm rgba(0,0,0,.15);border-radius:2mm">{appimg('growth-card_youth', 52)}</div><div class="cap">信息卡 / 成长卡</div></div>
<div><h3>办公事务<em>STATIONERY</em></h3><p>· 页眉：标志 + 组委会中英文名，熊猫蓝细线分隔；<br/>· 页脚：主办单位、场地、联系方式；<br/>· 右下角可使用 8% 透明度的成长环作水印；<br/>· 正式文件正文：Office 中文字体使用宋体 / 微软雅黑，英文 Arial。</p></div></div>'''
add("办公事务", "STATIONERY", "C1", c)

# C2 accreditation & wristbands
c = f'''<div class="cols c4" style="gap:6mm;height:150mm;align-items:center">
<div class="app">{appimg('accreditation_elite', 105)}<div class="cap">精英联赛 球员证</div></div>
<div class="app">{appimg('accreditation_youth', 105)}<div class="cap">少儿联赛 球员证</div></div>
<div class="app">{appimg('wristbands', 60)}<div class="cap">年龄组硅胶手环</div></div>
<div><h3>证件与手环<em>ACCREDITATION</em></h3><p>证件 86×130mm，顶部藏青区放联赛组合标志，底部色条为年龄组识别色，右侧标注身份（球员 / 教练 / 执裁教练 / 工作人员 / 志愿者）。实名登记后制发，赛场凭证入场。</p></div></div>'''
add("证件与手环", "ACCREDITATION & WRISTBANDS", "C2", c)

# C3 kit
c = f'''<div class="app" style="height:78mm">{appimg('kit_coach-referee_staff_volunteer', 76)}</div>
<div class="cols c13" style="margin-top:6mm;align-items:center"><div class="app">{appimg('bibs_age-groups', 46)}<div class="cap">年龄组对抗背心（区分对阵双方 / 增援球员）</div></div>
<div><h3>服装<em>APPAREL</em></h3><p><b>执裁教练服</b>：两个联赛均由教练员轮流执裁，执裁时穿着精英金色执裁服，背后印“COACH REF”，让孩子与家长清楚识别“此刻他是裁判”。<b>组委会工作服</b> 熊猫蓝；<b>志愿者服</b> 竹叶绿。参赛队比赛服由各队自备，统一在左胸佩戴联赛袖标 / 胸章（标志直径 ≥ 60mm）。守门员背心与对抗背心按年龄组色制作。</p></div></div>'''
add("服装与背心", "APPAREL & BIBS", "C3", c)

# C4 medals & cards
c = f'''<div class="cols c2" style="height:150mm;align-items:center"><div class="app">{appimg('medals', 80)}</div>
<div><div class="app">{appimg('cards_green-yellow-red', 58)}</div>
<h3 style="margin-top:6mm">奖牌与牌卡<em>MEDALS & CARDS</em></h3><p>完赛奖牌发给每一名参赛小球员，绶带为熊猫蓝 + 联赛识别色。<b>绿牌</b>用于表彰诚实、扶起对手、主动致歉等公平竞赛行为；<b>黄牌</b>在本联赛中意味着“冷静一下”——前往冷静区暂时罚离，球队可立即补人；红牌仅用于严重违规。</p></div></div>'''
add("奖牌与牌卡", "MEDALS & CARDS", "C4", c)

# C5 certificates
c = f'''<div class="cols c2" style="gap:6mm">
<div class="app"><div style="box-shadow:0 2mm 6mm rgba(0,0,0,.15)">{certs['certificate_elite_finisher'].replace('style="overflow:hidden"','style="overflow:hidden;width:118mm"',1)}</div><div class="cap">精英联赛 · 完赛证书（A4 横版）</div></div>
<div class="app"><div style="box-shadow:0 2mm 6mm rgba(0,0,0,.15)">{certs['certificate_youth_growthstar'].replace('style="overflow:hidden"','style="overflow:hidden;width:118mm"',1)}</div><div class="cap">少儿联赛 · 成长之星证书（A4 横版）</div></div></div>
<p style="margin-top:6mm">证书模板（完赛证书 / 成长之星 × 两个联赛）已作为可打印 PDF 提供于 assets/templates，球员姓名处留空供手写或套打。</p>'''
add("证书", "CERTIFICATES", "C5", c)

# C6 signage
c = '<div class="cols" style="grid-template-columns:repeat(6,1fr);gap:4mm;align-items:end">'
for i, s in enumerate(SIGNS):
    c += f'<div class="app">{appimg(f"sign_{i+1}_{s[1].lower().replace(" ", "-")}", 74)}</div>'
c += f'''</div><div class="cols c31" style="margin-top:7mm;align-items:center"><div><h3>赛场导视<em>WAYFINDING</em></h3><p>A 字立牌 60×80cm（双面）。规则精要中的“换人区击掌上下”“家长停留在家长区”“冷静区”“多球制”等，都需要在场地上有清晰、友好的标识。每块场地边设置年龄组色场地号牌。</p></div>
<div class="app" style="flex-direction:row;gap:6mm">{appimg('corner-flag_elite', 38)}{appimg('corner-flag_youth', 38)}</div></div>'''
add("赛场导视", "WAYFINDING & SIGNAGE", "C6", c)

# C7 venue branding
c = f'''<div class="cols c2" style="gap:6mm"><div class="app">{appimg('backdrop', 82)}<div class="cap">签到 / 采访背景板（3×2m）</div></div>
<div><div class="app">{appimg('perimeter-board_elite', 15)}</div><div class="app" style="margin-top:4mm">{appimg('perimeter-board_youth', 15)}</div><div class="cap">场边围挡 / 横幅（6×0.7m）</div>
<h3 style="margin-top:6mm">赛场品牌环境<em>VENUE</em></h3><p>背景板交替排列两项联赛的徽章；围挡以熊猫蓝 + 球面纹为底，右侧放核心价值“尊重 · 成长 · 快乐”。赞助商标识应放在独立的赞助区，不与联赛标志直接拼接。</p></div></div>'''
add("赛场品牌环境", "VENUE BRANDING", "C7", c)

# C8 digital
c = f'''<div class="cols" style="grid-template-columns:1.2fr 1fr .9fr;gap:6mm;align-items:center">
<div><div class="app">{appimg('wechat-cover_elite', 46)}</div><div class="app" style="margin-top:4mm">{appimg('wechat-cover_youth', 46)}</div><div class="cap">公众号头图 900×383</div>
<div class="app" style="flex-direction:row;gap:5mm;margin-top:4mm">{appimg('avatar_elite', 24)}{appimg('avatar_youth', 24)}</div><div class="cap">社媒头像 400×400</div></div>
<div class="app" style="flex-direction:row;gap:4mm">{appimg('poster_elite', 118)}{appimg('poster_youth', 118)}</div>
<div><h3>数字媒体<em>DIGITAL</em></h3><p>竖版海报 1080×1920 适配朋友圈 / 视频号 / 小红书；圆形裁切照片 + 成长环是主视觉的固定构图。所有发布遵守肖像授权与儿童保护原则。</p></div></div>'''
add("数字媒体", "DIGITAL MEDIA", "C8", c)

# C9 growth card & matchday
c = f'''<div class="cols c3" style="gap:6mm;align-items:center;height:150mm">
<div class="app">{appimg('matchday-card_youth', 120)}<div class="cap">赛日图文：只讲成长，不发比分</div></div>
<div class="app" style="gap:5mm">{appimg('growth-card_elite', 50)}{appimg('growth-card_youth', 50)}<div class="cap">我的成长卡（A6）</div></div>
<div><h3>以成长代替比分<em>GROWTH, NOT SCORES</em></h3><p>少儿联赛不公布比分、不设积分榜（参照英格兰足总 U11 以下、荷兰足协 6v6、澳大利亚 MiniRoos 等做法）。赛日对外传播使用“成长数据”：上场人数、均等上场率、绿牌、勇敢射门次数。</p><p>“我的成长卡”由教练赛后发给孩子：今天勇敢尝试了什么、帮助了谁、下次想做得更好的是什么。</p></div></div>'''
add("球员成长卡与赛日图", "GROWTH CARD & MATCHDAY", "C9", c)

# C10 merch
c = f'''<div class="cols c4" style="gap:6mm;height:110mm;align-items:end">
<div class="app">{appimg('tote-bag', 90)}<div class="cap">帆布袋</div></div><div class="app">{appimg('bottle', 90)}<div class="cap">运动水壶</div></div>
<div class="app">{appimg('cap', 60)}<div class="cap">棒球帽</div></div><div class="app">{appimg('wristbands', 50)}<div class="cap">手环</div></div></div>
<p style="margin-top:8mm">纪念品优先选择环保材质；标志位置固定在视觉中心或左胸；不在纪念品上印制比分、名次等结果信息，鼓励孩子以“参与和成长”为荣。</p>'''
add("纪念品", "MERCHANDISE", "C10", c)

# back cover
n += 1
pages.append(f'''<section class="page dark" style="padding:0;display:flex;align-items:center;justify-content:center;flex-direction:column">
<svg style="position:absolute;left:-60mm;bottom:-60mm;width:200mm;height:200mm" viewBox="0 0 1200 1200">{growth_rings(600, 600, 300, C['blue'], 70, n=3, gap=70)}</svg>
<div style="position:relative;z-index:1;text-align:center">{LOGO_SVG('master', 60, badge=True)}
<div style="font-size:22pt;font-weight:900;margin-top:8mm;letter-spacing:.1em">为了每个人更好的成长</div>
<div class="big" style="font-size:16pt;color:{C['gold']};letter-spacing:.16em;margin-top:2mm">FOR BETTER GROWTH OF EVERYONE</div>
<div style="font-size:9pt;color:#9FB6D1;margin-top:14mm">成都高新区足球协会 · 熊猫足球联赛组委会 · PYLCTU@163.com</div></div></section>''')

open(os.path.join(B, "_vi.html"), "w").write(f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>")
print("pages", len(pages))
