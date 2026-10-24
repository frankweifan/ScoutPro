"""Clean merged v2 data: drop noise, move venues, merge duplicate campuses, mark youth evidence, apply enrichment."""
import json, re, importlib.util

orgs = json.load(open("orgs_v2.json"))
venues = json.load(open("venues_v2.json"))

DROP = re.compile(r"充电|特斯拉|装备|商贸|传媒|天朗足球|足球水塔|篮球青训|医院|^足球场$|^五人制足球场$|^七人制足球场$|^足球运动场$|^足球场篮球场$")
TO_VENUE = re.compile(r"四川成都足球广场|水韵园综合教育基地足球场|斑竹园足球音乐小镇|晨辉路公园足球基地|诺坎普足球平衡车滑步车公园|毛家湾足球训练基地")
# POI rows that duplicate an existing seed record (name -> seed name containing key, note to append)
DUP = {
    "国家青少年足球训练中心": ("FF体育公园", "地图另列名称：国家青少年足球训练中心（青羊区）"),
    "成都足球俱乐部五牛训练基地-培训基地": ("成都足协温江基地", "原成都五牛训练基地（地图名称）"),
    "成都足球俱乐部": ("成都足协温江基地", None),
    "沸点足球俱乐部(高新校区)": ("沸点足球俱乐部（高新校区）", "地图收录地址在武侯区一侧"),
    "成都高新区猎豹足球俱乐部": ("成都猎豹足球培训", None),
    "城市仁德足球青训基地": ("宇晖仁德", None),
    "成都仁德足球青训基地": ("宇晖仁德", None),
    "卡尔美·成都仁德足球青训基地(城市仁德山庄店)": ("宇晖仁德", None),
    "卡尔美·成都仁德足球青训基地": ("宇晖仁德", None),
    "锦江仁德足球主题公园": ("宇晖仁德", None),
    "皇贝足球": ("皇家贝里斯足球俱乐部（皇贝青训）", None),
    "皇家贝里斯足球俱乐部(桂溪校区)": ("皇家贝里斯足球俱乐部（皇贝青训）", None),
    "玩湃社区足球公园": None,  # keep
}
YOUTH_WORDS = re.compile(r"少儿|儿童|幼儿|青少年|青训|小将|学院|足校|训练营|训练中心|培训|梯队|Academy|小虎")


def find(sub):
    r = [o for o in orgs if sub in o["name"]]
    return r[0] if r else None


keep = []
for o in orgs:
    n = o["name"]
    if DROP.search(n):
        continue
    if TO_VENUE.search(n):
        o["type"] = "场馆运营方"; venues.append(o); continue
    if n in DUP and DUP[n]:
        tgt, note = DUP[n]; s = find(tgt)
        if s and s is not o:
            if o.get("address") and o["address"] not in (s.get("address") or "") and o["address"] not in (s.get("campuses") or ""):
                s["campuses"] = ((s.get("campuses") or "") + f"；地图收录：{n}（{o['district']}）{o['address']}").lstrip("；")
            if o.get("phone") and not s.get("phone"): s["phone"] = o["phone"]
            if note: s["note"] = ((s.get("note") or "") + "；" + note).lstrip("；")
            for u in o.get("sources", []):
                if u not in s.setdefault("sources", []): s["sources"].append(u)
            continue
    keep.append(o)
orgs = keep

# special re-typing
for o in orgs:
    n = o["name"]
    if n.startswith("绿轴兴城足球公园"):
        o["type"] = "职业俱乐部青训"; o["note"] = "成都蓉城足球俱乐部训练基地（地图名称），是否对外开设青少年课程未知"
    if n in ("四川足球俱乐部-训练基地", "四川省明宇足球俱乐部"):
        o["type"] = "其他"; o["status"] = "现状未知"; o["note"] = "历史职业俱乐部相关名称，是否仍有青训业务未知"
    if n == "玩湃社区足球公园":
        o["type"] = "场馆运营方"
    if n == "众禾足球俱乐部" and o["district"] == "双流区":
        o["name"] = "众禾足球俱乐部（双流）"
    if n == "鲁家滩运动公园(温江足球协会训练基地)":
        o["type"] = "协会"

# youth evidence
for o in orgs:
    from_map = any("360地图" in s or "huodong.com" in s for s in o.get("sources", [])) and len(o.get("sources", [])) <= 1
    if not from_map:
        weak = re.search(r"未证实|未见|未找到|未确认有|是否.*未知|规划", (o.get("note") or "") + (o.get("scale_note") or "") + (o.get("honors_note") or "") + (o.get("status") or ""))
        if o["type"] == "协会": o.setdefault("youth", "协会（组织/承办青少年赛事）")
        elif weak: o.setdefault("youth", "待核实（来源未证实青训业务）")
        else: o.setdefault("youth", "已证实（有来源）")
    elif YOUTH_WORDS.search(o["name"]):
        o["youth"] = "名称显示青少年业务（待核实）"
    else:
        o["youth"] = "待核实（可能为成人业余球队/场地）"

# venues cleanup + dedupe
vk, vout = set(), []
for v in venues:
    n = v["name"]
    if DROP.search(n) or re.search(r"-\d号|-A区|号智能球场|快乐练习场|vvip|暂停营业", n):
        continue
    k = re.sub(r"[（(].*?[)）]|\s", "", n)
    if k in vk: continue
    vk.add(k); vout.append(v)
venues = vout

# enrichment round 1
spec = importlib.util.spec_from_file_location("e1", "enrich1.py"); e1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(e1)
ENR = list(e1.E)
try:
    spec2 = importlib.util.spec_from_file_location("e2", "enrich2.py"); e2 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(e2)
    ENR += list(e2.E)
except FileNotFoundError:
    pass


def app(o, d):
    for k, v in d.items():
        if k in ("students", "coaches", "founded_year", "phone", "address", "campuses", "status", "rating", "rating_platform"):
            if k == "address" and o.get("address"):
                o["campuses"] = ((o.get("campuses") or "") + "；" + v).lstrip("；") if v not in (o.get("address") or "") else o.get("campuses")
            else:
                o[k] = v
        elif k == "phone_add": o["phone"] = (o.get("phone") + "；" if o.get("phone") else "") + v
        elif k == "scale_add": o["scale_note"] = ((o.get("scale_note") or "") + "；" + v).lstrip("；")
        elif k == "honors_add": o["honors_note"] = ((o.get("honors_note") or "") + v).lstrip("；")
        elif k == "years_add": o["years_operating_note"] = ((o.get("years_operating_note") or "") + "；" + v).lstrip("；")
        elif k == "note_add": o["note"] = ((o.get("note") or "") + "；" + v).lstrip("；")
        elif k == "contact_add": o["wechat_or_other_contact"] = ((o.get("wechat_or_other_contact") or "") + "；" + v).lstrip("；")
        elif k == "legal": o["legal_name"] = v
        elif k == "age": o["age_range"] = v
        elif k in ("students_note", "coaches_note"): o["scale_note"] = ((o.get("scale_note") or "") + "；" + v).lstrip("；")
        elif k in ("rating_note", "dianping"): o["note"] = ((o.get("note") or "") + "；" + v).lstrip("；")
        elif k == "youth": o["youth"] = v
        elif k == "src":
            for u in v:
                if u not in o.setdefault("sources", []): o["sources"].append(u)


hits = 0
for key, d in ENR:
    m = [o for o in orgs + venues if key in o["name"]]
    for o in m: app(o, d)
    hits += bool(m)
json.dump(orgs, open("orgs_v2c.json", "w"), ensure_ascii=False, indent=0)
json.dump(venues, open("venues_v2c.json", "w"), ensure_ascii=False, indent=0)
print("orgs", len(orgs), "venues", len(venues), "enrich hits", hits, "/", len(ENR))
