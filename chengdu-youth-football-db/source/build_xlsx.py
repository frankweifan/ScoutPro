"""Build 大成都青少年足球培训机构数据库 Excel from merged JSON (orgs.json)."""
import json, sys, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.comments import Comment

SRC, OUT = sys.argv[1], sys.argv[2]
orgs = json.load(open(SRC))
VEN = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
VERSION = sys.argv[4] if len(sys.argv) > 4 else "v0.2"

DISTRICTS = ["锦江区", "青羊区", "金牛区", "武侯区", "成华区", "高新区", "天府新区", "东部新区", "龙泉驿区", "青白江区", "新都区",
             "温江区", "双流区", "郫都区", "新津区", "简阳市", "都江堰市", "彭州市", "邛崃市", "崇州市", "金堂县", "大邑县", "蒲江县", "全市/多区"]
FONT = "Microsoft YaHei"
BLUE, NAVY, MIST, YEL = "04518E", "0B2545", "E6EEF6", "FFF4CC"
thin = Side(style="thin", color="C9D5E3")
BORDER = Border(top=thin, bottom=thin, left=thin, right=thin)
F = lambda **k: Font(name=FONT, size=k.pop("size", 10), **k)

COLS = [  # header, key, width
    ("序号", None, 6), ("区（市县）", "district", 11), ("机构名称", "name", 30), ("品牌/所属", "brand", 16), ("机构类型", "type", 13), ("青训业务", "youth", 14), ("运营状态", "status", 11), ("公司/法人名称", "legal_name", 18),
    ("训练地址", "address", 34), ("联系电话", "phone", 16), ("其他联系方式", "wechat_or_other_contact", 18),
    ("成立年份", "founded_year", 9), ("运营年限（年）", None, 9), ("运营年限说明", "years_operating_note", 16),
    ("教练员数量", "coaches", 9), ("学员数量", "students", 9), ("校区/场地数", "campuses", 14), ("规模等级", None, 9), ("规模说明", "scale_note", 26),
    ("招生年龄", "age_range", 12), ("大众点评评分", "dianping", 9), ("美团评分", "meituan", 9), ("其他平台评分", "rating_other", 14),
    ("收费信息", "price_note", 18), ("荣誉/资质", "honors_note", 28), ("信息来源", "sources", 40), ("可信度", "confidence", 7), ("待核实/备注", "note", 26)]
FILL_KEYS = {"phone", "founded_year", "coaches", "students", "dianping", "meituan"}  # yellow when empty → to be collected


def norm_district(d):
    d = (d or "").strip()
    for k in DISTRICTS:
        if k[:2] in d:
            return k
    if "天府" in d: return "天府新区"
    return "全市/多区"


def prep(o):
    r = dict(o)
    r["district"] = norm_district(o.get("district"))
    rp = (o.get("rating_platform") or "")
    r["dianping"] = o.get("rating") if "点评" in rp else None
    r["meituan"] = o.get("rating") if "美团" in rp else None
    r["rating_other"] = f'{o["rating"]}（{rp}）' if o.get("rating") is not None and r["dianping"] is None and r["meituan"] is None else None
    r["sources"] = "\n".join(o.get("sources") or [])
    if isinstance(r.get("campuses"), (int, float)): r["campuses"] = str(r["campuses"])
    return r


YO = {"已证实（有来源）": 0, "协会（组织/承办青少年赛事）": 1, "名称显示青少年业务（待核实）": 2}
rows = sorted([prep(o) for o in orgs], key=lambda r: (DISTRICTS.index(r["district"]), YO.get(r.get("youth"), 3), r.get("type") or "", r.get("name") or ""))

wb = Workbook()
# ---------------------------------------------------------------- 说明
ws = wb.active; ws.title = "说明"
ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 100
ws["A1"] = "大成都青少年足球培训机构数据库"; ws["A1"].font = F(size=16, bold=True, color=NAVY)
ws["A2"] = f"版本 {VERSION} · 编制：2026-10 · 青训相关机构 {len(rows)} 条 · 足球场馆 {len(VEN)} 处"; ws["A2"].font = F(color="5A6B80")
info = [
    ("统计年份", 2026),
    ("大型 · 学员≥", 500), ("大型 · 或教练≥", 20), ("中型 · 学员≥", 100), ("中型 · 或教练≥", 6),
    (None, None),
    ("收录范围", "成都市 12 区 5 市 3 县及高新区、天府新区、东部新区内，开展青少年足球培训的机构：商业培训机构、业余/职业俱乐部青训、海外品牌青训分校、开展青训的协会、提供青少年课程的场馆运营方。连锁品牌按校区分列。"),
    ("数据来源", "① 360地图公开地点检索（按 23 个区县 × 14 个关键词逐一检索，约 340 次查询），取得机构名称、区县、地址、电话；② 活动网（huodong.com）成都足球场馆列表，仅取名称、区县、地址，不采用其页面上的通用性价格/教练描述；③ 公开网页检索（新闻、百科、机构官网、教育宝等）补充成立年份、教练、学员、荣誉、风险信息。每条均附来源。"),
    ("重要限制", "大众点评、美团、抖音、小红书需要登录或有人机验证，企查查/天眼查有反爬验证，成都市体育局网站拒绝访问——本库未绕过这些限制，因此平台评分、评价数、参保人数基本缺失；地图收录的机构中，部分可能是成人业余球队或单纯场地，已在“青训业务”列标注“待核实”。标黄单元格为待采集字段。"),
    ("青训业务", "已证实（有来源）= 来源明确提到青少年培训/梯队；名称显示青少年业务 = 名称含少儿/青训/学院等，待核实；待核实 = 仅地图收录、名称未体现青少年业务，可能为成人业余球队；协会 = 区县足协等。"),
    ("零编造原则", "所有数值均来自所附来源；来源未写明的一律留空，未做任何估算。"),
    ("运营年限", "公式 = 统计年份 − 成立年份（成立年份为空时留空）。"),
    ("规模等级", "公式：学员数或教练员数达到上方阈值即判为大型/中型，否则小型；两项都为空时留空。阈值可在本页 B5–B8 修改。"),
    ("可信度", "高 = 官方或权威媒体来源且信息一致；中 = 单一媒体/机构自述；低 = 信息零散或可能已变更，需电话核实。"),
    ("运营状态", "运营中 = 近年来源显示在运营；现状未知 = 仅有较早资料；规划（未见运营）；已停业（保留作风险提示）；待核实 = 来源未说明。"),
    ("数据时效", "部分数值来自较早年份的报道（已在“规模说明/备注”中注明年份），使用前请核实。"),
    (None, None),
    ("建议补采路径", "① 成都市及各区体育局官网《校外体育培训机构白名单》，最权威、最全的名录来源；② 大众点评/美团搜索“青少年足球”“儿童足球”，按区筛选，记录评分、评价数、地址、电话；③ 抖音/小红书搜索机构名，记录粉丝数与口碑；④ 企查查/天眼查查询成立日期、注册资本、参保人数（参保人数可近似反映教练员规模）；⑤ 电话或实地核实学员数。"),
    ("表格结构", "「汇总」按区、按类型统计；「全部机构」为总表（可筛选）；「足球场馆」为可能承接青训课程/赛事的场地（参考）；其后每个区（市县）一张分表。"),
]
for i, (k, v) in enumerate(info, start=4):
    if k is None: continue
    ws.cell(i, 1, k).font = F(bold=True, color=NAVY)
    c = ws.cell(i, 2, v); c.font = F(color="0000FF" if isinstance(v, (int, float)) else "13202F"); c.alignment = Alignment(wrap_text=True, vertical="top")
    if isinstance(v, (int, float)): c.fill = PatternFill("solid", fgColor=YEL); c.alignment = Alignment(horizontal="left")
    ws.row_dimensions[i].height = 18 if isinstance(v, (int, float)) else max(18, 16 * (len(str(v)) // 55 + 1))
ws["C4"] = "← 可修改的参数（蓝字黄底）"; ws["C4"].font = F(color="5A6B80", size=9)
leg = len(info) + 6
ws.cell(leg, 1, "图例").font = F(bold=True, color=NAVY)
ws.cell(leg, 2, "黄底空白 = 待采集字段").fill = PatternFill("solid", fgColor=YEL)
ws.cell(leg, 2).font = F()

# ---------------------------------------------------------------- master writer
def write_table(ws, rows, tname):
    hdr_fill = PatternFill("solid", fgColor=BLUE)
    for j, (h, k, w) in enumerate(COLS, start=1):
        c = ws.cell(1, j, h); c.font = F(bold=True, color="FFFFFF"); c.fill = hdr_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BORDER
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[1].height = 32
    L = {k: get_column_letter(j) for j, (h, k, w) in enumerate(COLS, start=1) if k}
    for i, r in enumerate(rows, start=2):
        for j, (h, k, w) in enumerate(COLS, start=1):
            if h == "序号": v = i - 1
            elif h == "运营年限（年）": v = f'=IF({L["founded_year"]}{i}="","",说明!$B$4-{L["founded_year"]}{i})'
            elif h == "规模等级":
                s, t = f'{L["students"]}{i}', f'{L["coaches"]}{i}'
                v = (f'=IF(AND({s}="",{t}=""),"",IF(OR(N({s})>=说明!$B$5,N({t})>=说明!$B$6),"大型",'
                     f'IF(OR(N({s})>=说明!$B$7,N({t})>=说明!$B$8),"中型","小型")))')
            else: v = r.get(k)
            c = ws.cell(i, j, v)
            c.font = F(size=9.5); c.border = BORDER
            c.alignment = Alignment(vertical="top", wrap_text=h in ("机构名称", "训练地址", "规模说明", "荣誉/资质", "信息来源", "待核实/备注", "收费信息", "运营年限说明", "校区/场地数", "其他联系方式"))
            if k in FILL_KEYS and (v is None or v == ""): c.fill = PatternFill("solid", fgColor=YEL)
            if h == "信息来源": c.font = F(size=8, color="1E6FB8")
        ws.row_dimensions[i].height = 48
    if rows:
        ref = f"A1:{get_column_letter(len(COLS))}{len(rows) + 1}"
        tb = Table(displayName=tname, ref=ref); tb.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True)
        ws.add_table(tb)
    ws.freeze_panes = "D2"


# ---------------------------------------------------------------- 汇总 (placeholder first so order is 说明, 汇总, 全部机构, districts)
wsS = wb.create_sheet("汇总")
wsM = wb.create_sheet("全部机构")
write_table(wsM, rows, "全部机构表")
n = len(rows) + 1
TYPES = ["培训机构", "业余俱乐部", "职业俱乐部青训", "海外青训分校", "协会", "场馆运营方", "其他"]
hdr = ["区（市县）", "合计"] + TYPES + ["有电话", "有成立年份", "有评分", "青训已证实"]
for j, h in enumerate(hdr, start=1):
    c = wsS.cell(1, j, h); c.font = F(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=BLUE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = BORDER
    wsS.column_dimensions[get_column_letter(j)].width = 12 if j > 1 else 14
wsS.row_dimensions[1].height = 32
col = {h: get_column_letter(j) for j, (h, k, w) in enumerate(COLS, start=1)}
rng = lambda h: f"全部机构!${col[h]}$2:${col[h]}${max(n, 2)}"
for i, d in enumerate(DISTRICTS, start=2):
    wsS.cell(i, 1, d)
    wsS.cell(i, 2, f'=COUNTIFS({rng("区（市县）")},$A{i})')
    for j, t in enumerate(TYPES, start=3):
        wsS.cell(i, j, f'=COUNTIFS({rng("区（市县）")},$A{i},{rng("机构类型")},"{t}")')
    b = len(TYPES) + 3
    wsS.cell(i, b, f'=COUNTIFS({rng("区（市县）")},$A{i},{rng("联系电话")},"<>")')
    wsS.cell(i, b + 1, f'=COUNTIFS({rng("区（市县）")},$A{i},{rng("成立年份")},"<>")')
    wsS.cell(i, b + 2, f'=COUNTIFS({rng("区（市县）")},$A{i},{rng("大众点评评分")},"<>")+COUNTIFS({rng("区（市县）")},$A{i},{rng("美团评分")},"<>")+COUNTIFS({rng("区（市县）")},$A{i},{rng("其他平台评分")},"<>")')
    wsS.cell(i, b + 3, f'=COUNTIFS({rng("区（市县）")},$A{i},{rng("青训业务")},"已证实（有来源）")')
tot = len(DISTRICTS) + 2
wsS.cell(tot, 1, "合计")
for j in range(2, len(hdr) + 1):
    L_ = get_column_letter(j); wsS.cell(tot, j, f"=SUM({L_}2:{L_}{tot - 1})")
for r_ in wsS.iter_rows(min_row=2, max_row=tot):
    for c in r_:
        c.font = F(bold=c.row == tot); c.border = BORDER; c.alignment = Alignment(horizontal="center" if c.column > 1 else "left")
        if c.row == tot: c.fill = PatternFill("solid", fgColor=MIST)
wsS.freeze_panes = "B2"
wsS.cell(tot + 2, 1, "注：类型以来源描述归类；“有电话/有成立年份/有评分”用于显示各区信息完整度。").font = F(size=9, color="5A6B80")

# ---------------------------------------------------------------- venues
wv = wb.create_sheet("足球场馆")
VC = [("序号", None, 6), ("区（市县）", "district", 11), ("场馆名称", "name", 34), ("地址", "address", 44), ("电话", "phone", 16), ("来源", "sources", 40), ("备注", "note", 30)]
for j, (h, k, w) in enumerate(VC, start=1):
    c = wv.cell(1, j, h); c.font = F(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=BLUE); c.border = BORDER
    c.alignment = Alignment(horizontal="center", vertical="center"); wv.column_dimensions[get_column_letter(j)].width = w
vrows = sorted([prep(v) for v in VEN], key=lambda r: (DISTRICTS.index(r["district"]), r["name"]))
for i, r in enumerate(vrows, start=2):
    for j, (h, k, w) in enumerate(VC, start=1):
        c = wv.cell(i, j, i - 1 if k is None else r.get(k)); c.font = F(size=9.5); c.border = BORDER
        c.alignment = Alignment(vertical="top", wrap_text=k in ("name", "address", "sources", "note"))
if vrows:
    tb = Table(displayName="场馆表", ref=f"A1:{get_column_letter(len(VC))}{len(vrows) + 1}"); tb.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True); wv.add_table(tb)
wv.freeze_panes = "C2"

# ---------------------------------------------------------------- per district
for k, d in enumerate(DISTRICTS):
    sub = [r for r in rows if r["district"] == d]
    w = wb.create_sheet(d.replace("/", "-"))
    write_table(w, sub, f"T{k:02d}")
    if not sub:
        w.cell(2, 3, "本次公开检索未找到该区域可核实的机构，待通过体育局白名单 / 大众点评补采。").font = F(color="5A6B80")

wb.save(OUT)
print("rows", len(rows))
