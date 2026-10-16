"""Application mock-ups (flat vector) for the Panda Leagues VI manual. All return SVG strings."""
import json, os, math
from vi_lib import C, logo_g, LOGO_W, LOGO_H, text_el, panel_pattern, growth_rings, hex_pts, pent_pts

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, "icons.json")))
F_CN = "'Noto Sans CJK SC','Microsoft YaHei',sans-serif"
F_EN = "'Barlow Condensed','Arial Narrow',sans-serif"
F_B = "'Barlow','Noto Sans CJK SC',sans-serif"


def icon(name, x, y, size, color):
    s = ICONS[name]
    inner = s[s.index(">") + 1: s.rindex("</svg>")]
    k = size / 24
    return (f'<g transform="translate({x},{y}) scale({k})" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</g>')


def t(x, y, s, txt, fill, size, fam=F_CN, weight=700, anchor="start", ls=0, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{txt}</text>')


def svg(w, h, body, cls=""):
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" style="overflow:hidden">{body}</svg>'


def lg(variant, cx, cy, d, badge=False, disc=True):
    return logo_g(variant, cx - d / 2, cy - d / 2, d, badge=badge, disc=disc)


ACC = {"elite": C["gold"], "youth": C["green"]}
NAME = {"elite": ("熊猫精英足球联赛", "PANDA ELITE LEAGUE"), "youth": ("熊猫少儿足球联赛", "PANDA YOUTH LEAGUE")}


# ------------------------------------------------------------------ kit
SHIRT = ("M70,30 L120,10 Q150,30 180,10 L230,30 L290,90 L255,130 L230,112 L230,330 L70,330 L70,112 "
         "L45,130 L10,90 Z")


def shirt(fill, trim, front=True, number="10", name="", logo_variant="master", badge_txt=None, num_col=None):
    b = [f'<path d="{SHIRT}" fill="{fill}" stroke="{trim}" stroke-width="3" stroke-linejoin="round"/>']
    b.append(f'<path d="M120,10 Q150,40 180,10" fill="none" stroke="{trim}" stroke-width="8"/>')
    b.append(f'<path d="M10,90 L45,130" stroke="{trim}" stroke-width="8"/><path d="M290,90 L255,130" stroke="{trim}" stroke-width="8"/>')
    if front:
        b.append(lg(logo_variant, 198, 82, 46, badge=True))
        b.append(f'<g opacity=".14">{growth_rings(150, 230, 46, C["white"], 10, n=3, gap=12)}</g>')
        if badge_txt:
            b.append(t(150, 300, 0, badge_txt, num_col or trim, 20, F_EN, 800, "middle", 2))
    else:
        b.append(t(150, 92, 0, name, num_col or trim, 22, F_EN, 800, "middle", 3))
        b.append(t(150, 245, 0, number, num_col or trim, 140, F_EN, 800, "middle"))
    return "".join(b)


def kit_sheet():
    W, H = 1300, 400
    b = []
    items = [
        ("执裁教练服 正面", shirt(C["gold"], C["navy"], True, logo_variant="elite", badge_txt="COACH REFEREE", num_col=C["navy"])),
        ("执裁教练服 背面", shirt(C["gold"], C["navy"], False, "R", "COACH REF", num_col=C["navy"])),
        ("组委会工作服", shirt(C["blue"], C["white"], True, badge_txt="STAFF")),
        ("志愿者服", shirt(C["green"], C["white"], True, logo_variant="youth", badge_txt="VOLUNTEER")),
    ]
    for i, (lab, s) in enumerate(items):
        x = 15 + i * 322
        b.append(f'<g transform="translate({x},10) scale(1)">{s}</g>')
        b.append(t(x + 150, 382, 0, lab, C["ink"], 22, F_CN, 500, "middle"))
    return svg(W, H, "".join(b))


def bib(color, label, txtc):
    p = "M60,0 L100,0 Q130,40 160,0 L200,0 L200,260 L60,260 Z"
    return (f'<path d="{p}" fill="{color}"/><path d="M60,0 L100,0 Q130,40 160,0 L200,0" fill="none" stroke="{C["white"]}" stroke-width="5"/>'
            + lg("master", 130, 85, 50, badge=True) + t(130, 205, 0, label, txtc, 72, F_EN, 800, "middle"))


def bibs_sheet():
    b = []
    for i, (k, lab) in enumerate([("u6", "U6"), ("u8", "U8"), ("u10", "U10"), ("u11", "U11")]):
        tc = C["navy"] if k == "u6" else C["white"]
        b.append(f'<g transform="translate({i * 230 - 40},10)">{bib(C[k], lab, tc)}</g>')
    return svg(900, 280, "".join(b))


# ------------------------------------------------------------------ medal / cards
def medal(league):
    acc = ACC[league]; cn, en = NAME[league]
    b = [f'<path d="M150,0 L210,0 L180,140 L120,140 Z" fill="{C["blue"]}"/>',
         f'<path d="M250,0 L310,0 L280,140 L220,140 Z" fill="{C["blue"]}"/>',
         f'<path d="M150,0 L310,0 L300,22 L160,22 Z" fill="{acc}"/>',
         f'<circle cx="230" cy="270" r="135" fill="#D9A93A"/>',
         f'<circle cx="230" cy="270" r="120" fill="#F2C75C"/>',
         f'<circle cx="230" cy="270" r="106" fill="none" stroke="#C6922A" stroke-width="3"/>',
         lg("mono-#A9761C", 230, 255, 120, disc=False),
         f'<path id="arc{league}" d="M140,270 A90,90 0 0 0 320,270" fill="none"/>',
         f'<text font-family="{F_EN}" font-weight="800" font-size="17" fill="#8A5D12" letter-spacing="2">'
         f'<textPath href="#arc{league}" startOffset="50%" text-anchor="middle">{en} · 2026 AUTUMN</textPath></text>']
    return "".join(b)


def medals_sheet():
    return svg(920, 420, f'<g transform="translate(0,0)">{medal("elite")}</g><g transform="translate(450,0)">{medal("youth")}</g>'
               + t(230, 412, 0, "精英联赛 完赛奖牌", C["ink"], 20, F_CN, 500, "middle")
               + t(680, 412, 0, "少儿联赛 完赛奖牌", C["ink"], 20, F_CN, 500, "middle"))


def card(color, title_cn, title_en, txtc, iconname):
    return (f'<rect x="0" y="0" width="170" height="240" rx="14" fill="{color}"/>'
            f'<g opacity=".18">{growth_rings(85, 120, 40, txtc, 7, n=3, gap=9)}</g>'
            + lg("master", 85, 54, 46, badge=True)
            + icon(iconname, 61, 98, 48, txtc)
            + t(85, 190, 0, title_cn, txtc, 26, F_CN, 900, "middle")
            + t(85, 216, 0, title_en, txtc, 15, F_EN, 700, "middle", 2))


def cards_sheet():
    return svg(600, 250, f'<g transform="translate(5,5)">{card(C["green"], "绿牌", "FAIR PLAY", C["white"], "TbHeartHandshake")}</g>'
               f'<g transform="translate(215,5)">{card("#FFD200", "黄牌", "COOL-DOWN 8′", C["navy"], "TbSnowflake")}</g>'
               f'<g transform="translate(425,5)">{card("#E2231A", "红牌", "SEND-OFF", C["white"], "TbBan")}</g>')


# ------------------------------------------------------------------ certificate
def certificate(league, kind="finisher"):
    acc = ACC[league]; cn, en = NAME[league]
    W, H = 1123, 794
    head = "完赛证书" if kind == "finisher" else "成长之星"
    head_en = "CERTIFICATE OF COMPLETION" if kind == "finisher" else "GROWTH STAR AWARD"
    body = "完成 2026 秋季赛季全部比赛。你在比赛中勇敢尝试、尊重对手、与队友并肩作战，<br/>你已经成为更好的自己 —— 每个人都是冠军！" if kind == "finisher" else \
        "在 2026 秋季赛季中进步显著、积极尝试、乐于合作，<br/>经所在球队教练推选，特授予“成长之星”称号。"
    b = [f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="none" stroke="{C["blue"]}" stroke-width="3"/>',
         f'<g opacity=".08">{growth_rings(W - 60, H - 40, 140, C["blue"], 26, n=4, gap=30)}</g>',
         f'<g opacity=".10">{growth_rings(70, 70, 70, acc, 20, n=3, gap=22)}</g>',
         lg(league, W / 2, 140, 130),
         t(W / 2, 270, 0, head, C["navy"], 64, F_CN, 900, "middle", 12),
         t(W / 2, 308, 0, head_en, C["blue"], 22, F_EN, 700, "middle", 6),
         f'<line x1="{W/2-170}" y1="420" x2="{W/2+170}" y2="420" stroke="{C["slate"]}" stroke-width="1.5"/>',
         t(W / 2, 410, 0, "球员姓名", "#B8C3D1", 26, F_CN, 400, "middle"),
         f'<foreignObject x="150" y="440" width="{W-300}" height="110"><div xmlns="http://www.w3.org/1999/xhtml" '
         f'style="font-family:{F_CN};font-size:20px;line-height:1.9;color:{C["ink"]};text-align:center">{body}</div></foreignObject>',
         t(260, 690, 0, "成都高新区足球协会", C["ink"], 18, F_CN, 700, "middle"),
         t(260, 716, 0, "CDHT FOOTBALL ASSOCIATION", C["slate"], 13, F_EN, 600, "middle", 2),
         t(W - 260, 690, 0, f"{cn}组委会", C["ink"], 18, F_CN, 700, "middle"),
         t(W - 260, 716, 0, "2026 年 · 成都", C["slate"], 13, F_CN, 400, "middle", 2),
         f'<rect x="{W/2-60}" y="640" width="120" height="44" rx="22" fill="{acc}"/>',
         t(W / 2, 669, 0, "2026 AUTUMN", C["navy"] if league == "elite" else C["white"], 18, F_EN, 800, "middle", 2)]
    return svg(W, H, "".join(b))


# ------------------------------------------------------------------ accreditation
def accreditation(league, role="球员", role_en="PLAYER", group="U10", name="张小熊", team="高新熊猫队"):
    acc = ACC[league]; cn, en = NAME[league]
    W, H = 340, 520
    gc = C["u10"] if group == "U10" else C["u11"] if group == "U11" else C["u8"] if group == "U8" else C["u6"]
    b = [f'<rect x="150" y="0" width="40" height="40" fill="{C["blue"]}"/>',
         f'<rect x="0" y="30" width="{W}" height="{H-30}" rx="18" fill="#fff" stroke="#D5DEE8"/>',
         f'<path d="M0,48 Q0,30 18,30 L322,30 Q340,30 340,48 L340,170 L0,170 Z" fill="{C["navy"]}"/>',
         f'<rect x="150" y="44" width="40" height="10" rx="5" fill="#E6EEF6"/>',
         lg(league, 60, 112, 72, badge=True),
         t(105, 106, 0, cn, "#fff", 21, F_CN, 900),
         t(105, 132, 0, en, acc, 15, F_EN, 800, ls=1.5),
         f'<rect x="110" y="196" width="120" height="150" rx="10" fill="#E6EEF6"/>',
         icon("TbUsers", 140, 236, 60, "#9AAABD"),
         t(W / 2, 384, 0, name, C["ink"], 30, F_CN, 900, "middle"),
         t(W / 2, 412, 0, team, C["slate"], 17, F_CN, 500, "middle"),
         f'<rect x="0" y="440" width="{W}" height="80" fill="{gc}"/>',
         f'<path d="M0,440 L340,440 L340,502 Q340,520 322,520 L18,520 Q0,520 0,502 Z" fill="{gc}"/>',
         t(30, 492, 0, group, C["navy"] if group in ("U6",) else "#fff", 40, F_EN, 800),
         t(W - 30, 478, 0, role, C["navy"] if group in ("U6",) else "#fff", 20, F_CN, 900, "end"),
         t(W - 30, 502, 0, role_en, C["navy"] if group in ("U6",) else "#fff", 14, F_EN, 700, "end", 2)]
    return svg(W, H, "".join(b))


# ------------------------------------------------------------------ venue
def backdrop():
    W, H = 1200, 600
    b = [f'<rect width="{W}" height="{H}" fill="{C["navy"]}"/>']
    for r in range(4):
        for c in range(6):
            x = 100 + c * 200 + (100 if r % 2 else 0); y = 80 + r * 140
            if x > W - 40: continue
            v = "elite" if (r + c) % 2 == 0 else "youth"
            b.append(lg(v, x, y, 70, badge=True))
            b.append(t(x, y + 58, 0, "PANDA LEAGUES", "#fff", 13, F_EN, 800, "middle", 2))
    b.append(f'<rect x="0" y="{H-60}" width="{W}" height="60" fill="{C["blue"]}"/>')
    b.append(t(W / 2, H - 22, 0, "为了每个人更好的成长 · FOR BETTER GROWTH OF EVERYONE", "#fff", 22, F_CN, 700, "middle", 2))
    return svg(W, H, "".join(b))


def perimeter_board(league):
    acc = ACC[league]; cn, en = NAME[league]
    W, H = 1200, 140
    b = [f'<rect width="{W}" height="{H}" fill="{C["blue"]}"/>',
         f'<g opacity=".22">{panel_pattern(W, H, r=26, colors=[C["navy"]], seed=11, density=.3)}</g>',
         lg(league, 80, 70, 104, badge=True),
         t(150, 66, 0, cn, "#fff", 40, F_CN, 900),
         t(150, 104, 0, en + " · 2026 AUTUMN", acc, 26, F_EN, 800, ls=2),
         f'<rect x="{W-460}" y="22" width="430" height="96" rx="48" fill="#fff"/>',
         t(W - 245, 64, 0, "尊重 · 成长 · 快乐", C["navy"], 30, F_CN, 900, "middle", 4),
         t(W - 245, 98, 0, "RESPECT · GROWTH · JOY", C["blue"], 20, F_EN, 800, "middle", 3)]
    return svg(W, H, "".join(b))


def sign(title, en, iconname, color, txtc="#fff", note=""):
    W, H = 300, 420
    b = [f'<path d="M40,410 L80,120 M260,410 L220,120" stroke="#8A97A8" stroke-width="10" stroke-linecap="round"/>',
         f'<rect x="20" y="0" width="260" height="330" rx="16" fill="{color}"/>',
         f'<g opacity=".16">{growth_rings(150, 150, 52, txtc, 10, n=3, gap=12)}</g>',
         icon(iconname, 105, 50, 90, txtc),
         t(150, 210, 0, title, txtc, 40, F_CN, 900, "middle", 4),
         t(150, 244, 0, en, txtc, 20, F_EN, 800, "middle", 3),
         t(150, 282, 0, note, txtc, 15, F_CN, 500, "middle"),
         lg("master", 150, 306, 30, badge=True)]
    return svg(W, H, "".join(b))


def corner_flag(league):
    acc = ACC[league]
    b = [f'<rect x="20" y="10" width="8" height="300" rx="4" fill="#E9EEF3" stroke="#B9C4D0"/>',
         f'<path d="M28,14 L180,40 L28,120 Z" fill="{C["blue"]}"/>',
         f'<path d="M28,90 L120,72 L28,120 Z" fill="{acc}"/>',
         lg(league, 80, 56, 40, badge=True)]
    return svg(200, 320, "".join(b))


# ------------------------------------------------------------------ digital
def wechat_cover(league, title="2026秋季联赛 报名开启", sub="REGISTRATION OPEN"):
    acc = ACC[league]; cn, en = NAME[league]
    W, H = 900, 383
    b = [f'<rect width="{W}" height="{H}" fill="{C["navy"]}"/>',
         f'<g opacity=".9">{growth_rings(760, 190, 120, C["blue"], 34, n=3, gap=26)}</g>',
         f'<g>{growth_rings(760, 190, 120, acc, 6, n=1)}</g>',
         lg(league, 760, 190, 190, badge=True),
         t(60, 110, 0, cn, acc, 30, F_CN, 900, ls=4),
         t(60, 200, 0, title, "#fff", 56, F_CN, 900),
         t(60, 252, 0, sub, "#fff", 34, F_EN, 800, ls=4),
         f'<rect x="60" y="292" width="280" height="50" rx="25" fill="{acc}"/>',
         t(200, 326, 0, "为了每个人更好的成长", C["navy"] if league == "elite" else "#fff", 22, F_CN, 900, "middle")]
    return svg(W, H, "".join(b))


def poster(league, img_href=None):
    acc = ACC[league]; cn, en = NAME[league]
    W, H = 1080, 1920
    fmt = "8人制 · U10 / U11 · 每周六下午" if league == "elite" else "3人制 U6 · 5人制 U8 / U10 · 每周日上午"
    b = [f'<rect width="{W}" height="{H}" fill="{C["blue"]}"/>']
    if img_href:
        b.append(f'<defs><clipPath id="pc{league}"><circle cx="540" cy="900" r="430"/></clipPath></defs>')
        b.append(f'<image href="{img_href}" x="40" y="470" width="1000" height="860" preserveAspectRatio="xMidYMid slice" clip-path="url(#pc{league})"/>')
    b.append(growth_rings(540, 900, 460, acc, 22, n=2, gap=30))
    b.append(f'<g opacity=".25">{panel_pattern(W, 360, r=46, colors=[C["navy"]], seed=5, density=.3)}</g>')
    b.append(lg(league, 540, 230, 240, badge=True))
    b.append(t(540, 1470, 0, cn, "#fff", 92, F_CN, 900, "middle", 6))
    b.append(t(540, 1550, 0, en, acc, 64, F_EN, 800, "middle", 6))
    b.append(t(540, 1640, 0, "2026 秋季赛季 · 报名开启", "#fff", 48, F_CN, 700, "middle", 4))
    b.append(t(540, 1720, 0, fmt, "#fff", 34, F_CN, 500, "middle", 2))
    b.append(f'<rect x="0" y="{H-110}" width="{W}" height="110" fill="{C["navy"]}"/>')
    b.append(t(540, H - 45, 0, "成都高新区足球协会  主办", "#fff", 30, F_CN, 500, "middle", 3))
    return svg(W, H, "".join(b))


def avatar(league):
    acc = ACC[league]
    return svg(400, 400, f'<rect width="400" height="400" fill="{C["blue"]}"/>{growth_rings(200, 200, 150, acc, 14, n=1)}' + lg(league, 200, 200, 250, badge=True))


def result_card(league):
    """Match-day 'growth' card for social media — youth league shows no score."""
    acc = ACC[league]
    W, H = 1080, 1350
    b = [f'<rect width="{W}" height="{H}" fill="{C["paper"]}"/>',
         f'<rect width="{W}" height="380" fill="{C["navy"]}"/>',
         f'<g opacity=".35">{panel_pattern(W, 380, r=40, colors=[C["blue"]], seed=9, density=.35)}</g>',
         lg(league, 140, 190, 170, badge=True),
         t(260, 170, 0, "第 3 比赛日 · MATCHDAY 3", acc, 40, F_CN, 900, ls=2),
         t(260, 240, 0, "今天的我们，比昨天更好", "#fff", 56, F_CN, 900),
         t(260, 300, 0, "TODAY WE GREW", "#fff", 40, F_EN, 800, ls=6)]
    stats = [("TbUsers", "48", "名小球员上场"), ("TbClock", "100%", "全员均等上场"), ("TbHeartHandshake", "12", "张绿牌"), ("TbBallFootball", "36", "次勇敢射门")]
    for i, (ic, n, lab) in enumerate(stats):
        x = 60 + (i % 2) * 500; y = 450 + (i // 2) * 330
        b.append(f'<rect x="{x}" y="{y}" width="460" height="290" rx="28" fill="#fff"/>')
        b.append(f'<circle cx="{x+80}" cy="{y+80}" r="46" fill="{C["mist"]}"/>' + icon(ic, x + 52, y + 52, 56, C["blue"]))
        b.append(t(x + 40, y + 210, 0, n, C["navy"], 110, F_EN, 800))
        b.append(t(x + 40, y + 262, 0, lab, C["slate"], 32, F_CN, 700))
    b.append(t(540, 1270, 0, "#每个人都是冠军  #熊猫联赛", C["blue"], 34, F_CN, 900, "middle", 2))
    return svg(W, H, "".join(b))


# ------------------------------------------------------------------ merchandise
def tote():
    b = [f'<path d="M90,90 Q90,10 150,10 Q210,10 210,90" fill="none" stroke="#C9B99A" stroke-width="14"/>',
         f'<rect x="30" y="80" width="240" height="280" rx="6" fill="#EFE8DA"/>',
         lg("master", 150, 190, 130),
         t(150, 296, 0, "PANDA LEAGUES", C["blue"], 28, F_EN, 800, "middle", 3),
         t(150, 326, 0, "为了每个人更好的成长", C["navy"], 16, F_CN, 700, "middle", 2)]
    return svg(300, 370, "".join(b))


def bottle():
    b = [f'<rect x="80" y="0" width="80" height="40" rx="8" fill="{C["navy"]}"/>',
         f'<rect x="60" y="36" width="120" height="330" rx="40" fill="{C["blue"]}"/>',
         f'<g opacity=".25">' + "".join(f'<polygon points="{hex_pts(120 + (i%2)*30 - 15, 80 + i*40, 14, 30)}" fill="{C["navy"]}"/>' for i in range(7)) + '</g>',
         lg("master", 120, 190, 86, badge=True),
         t(120, 280, 0, "DRINK", "#fff", 22, F_EN, 800, "middle", 3),
         t(120, 304, 0, "多喝水", "#fff", 16, F_CN, 700, "middle", 2)]
    return svg(240, 370, "".join(b))


def cap():
    b = [f'<path d="M30,200 Q30,40 170,40 Q310,40 310,200 Z" fill="{C["navy"]}"/>',
         f'<path d="M20,200 Q170,230 360,200 Q360,236 300,240 Q170,250 20,214 Z" fill="{C["blue"]}"/>',
         f'<circle cx="170" cy="48" r="8" fill="{C["blue"]}"/>',
         lg("master", 170, 130, 96, badge=True)]
    return svg(380, 260, "".join(b))


def wristbands():
    b = []
    for i, (k, lab) in enumerate([("u6", "U6"), ("u8", "U8"), ("u10", "U10"), ("u11", "U11")]):
        y = 10 + i * 62
        tc = C["navy"] if k == "u6" else "#fff"
        b.append(f'<rect x="10" y="{y}" width="420" height="46" rx="23" fill="{C[k]}"/>')
        b.append(lg("master", 40, y + 23, 34, badge=True))
        b.append(t(70, y + 31, 0, f"{lab}  ·  尊重 · 成长 · 快乐", tc, 19, F_CN, 900, ls=1))
    return svg(440, 260, "".join(b))


def growth_card(league):
    """'My growth card' — a small post-match card coach hands to each child."""
    acc = ACC[league]
    W, H = 600, 380
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="#fff" stroke="#D5DEE8"/>',
         f'<path d="M0,20 Q0,0 20,0 L580,0 Q600,0 600,20 L600,90 L0,90 Z" fill="{C["blue"]}"/>',
         lg(league, 52, 45, 64, badge=True),
         t(96, 42, 0, "我的成长卡", "#fff", 28, F_CN, 900),
         t(96, 72, 0, "MY GROWTH CARD", acc, 18, F_EN, 800, ls=3),
         t(560, 56, 0, "第 ___ 轮", "#fff", 20, F_CN, 500, "end")]
    rows = ["今天我勇敢尝试了：", "今天我帮助了队友：", "下次我想做得更好："]
    for i, r in enumerate(rows):
        y = 140 + i * 66
        b.append(t(36, y, 0, r, C["ink"], 20, F_CN, 700))
        b.append(f'<line x1="36" y1="{y+22}" x2="564" y2="{y+22}" stroke="#C9D3DF" stroke-dasharray="4 5"/>')
    for i in range(5):
        b.append(f'<polygon points="{pent_pts(380 + i*40, 350, 14)}" fill="{acc if i < 3 else "#E6EEF6"}"/>')
    b.append(t(36, 356, 0, "教练寄语 / 签名：", C["slate"], 16, F_CN, 500))
    return svg(W, H, "".join(b))


def letterhead():
    W, H = 595, 842
    b = [f'<rect width="{W}" height="{H}" fill="#fff"/>',
         lg("master", 66, 70, 56),
         t(104, 66, 0, "熊猫足球联赛组委会", C["navy"], 17, F_CN, 900),
         t(104, 86, 0, "PANDA LEAGUES ORGANISING COMMITTEE", C["blue"], 10.5, F_EN, 700, ls=1.5),
         f'<line x1="40" y1="112" x2="555" y2="112" stroke="{C["blue"]}" stroke-width="1"/>']
    for i in range(16):
        b.append(f'<rect x="56" y="{150 + i*24}" width="{480 - (i%4)*40}" height="7" rx="3.5" fill="#E6EEF6"/>')
    b.append(f'<g opacity=".08">{growth_rings(W-30, H-30, 90, C["blue"], 18, n=3, gap=20)}</g>')
    b.append(t(40, 800, 0, "成都高新区足球协会 主办  ·  四川新北足球中心  ·  PYLCTU@163.com", C["slate"], 9.5, F_CN, 400))
    return svg(W, H, "".join(b))


def business_card():
    W, H = 540, 300
    front = [f'<rect width="{W}" height="{H}" rx="10" fill="{C["navy"]}"/>',
             f'<g opacity=".6">{growth_rings(W-20, H/2, 110, C["blue"], 22, n=3, gap=18)}</g>',
             lg("master", 420, 150, 150, badge=True),
             t(40, 120, 0, "杨老师", "#fff", 34, F_CN, 900),
             t(40, 152, 0, "赛区组委会 · 赛事运营", C["gold"], 17, F_CN, 500),
             t(40, 220, 0, "M  199 8072 0350", "#fff", 17, F_EN, 600, ls=1),
             t(40, 248, 0, "E  PYLCTU@163.com", "#fff", 17, F_EN, 600, ls=1)]
    return svg(W, H, "".join(front))
