"""Filter/classify 360 + Huodong POIs and merge with seed orgs.json -> orgs_v2.json + venues_v2.json"""
import json, re, sys

seed = json.load(open("orgs.json"))
poi = json.load(open("poi360.json"))
hd = json.load(open("huodong_list.json"))

AREA_FIX = {"四川天府新区成都直管区": "天府新区", "成都高新区": "高新区", "高新区": "高新区", "成都东部新区": "东部新区"}
DISTRICTS = ["锦江区", "青羊区", "金牛区", "武侯区", "成华区", "高新区", "天府新区", "东部新区", "龙泉驿区", "青白江区", "新都区",
             "温江区", "双流区", "郫都区", "新津区", "简阳市", "都江堰市", "彭州市", "邛崃市", "崇州市", "金堂县", "大邑县", "蒲江县"]

FOOT = re.compile(r"足球|青训|球会|足校|FC|F\.C|[Ff]ootball|[Ss]occer|绿茵")
JUNK = re.compile(r"公交站|地铁|出入口|停车场|[东南西北]门$|-[东南西北]?门|入口|号足球场|号场|厕所|卫生间|售票|专卖|用品|体育用品|商店|超市|彩票|酒吧|餐吧|火锅|烧烤|宿舍|公寓|小区|车站|收费站|加油站|商铺|门市|球鞋|大连|电竞|足球彩|足球宝贝|直播|足疗|足浴")
SCHOOL_PITCH = re.compile(r"(小学|中学|大学|学院|学校|职业技术|技工|幼儿园|实验|附属)[^俱]*(足球场|运动场|操场|球场)$")
TRAIN = re.compile(r"俱乐部|培训|青训|学院|学校|训练营|训练基地|训练中心|少儿|儿童|幼儿|青少年|体适能|教育|球会|FC|学堂|足校|学苑|精英|梯队|基地|Academy|academy")
ASSOC = re.compile(r"足球协会|足协")
VENUE = re.compile(r"足球公园|足球场|运动中心|体育公园|足球中心|球场|运动场|体育中心|足球小镇|足球村|运动公园|体育馆")


def norm_area(a, addr=""):
    a = (a or "").strip()
    for k, v in AREA_FIX.items():
        if k in a or k in (addr or ""): return v
    for d in DISTRICTS:
        if d in a: return d
    for d in DISTRICTS:
        if d in (addr or ""): return d
    return "全市/多区"


def classify(name, typ):
    if ASSOC.search(name): return "协会"
    if SCHOOL_PITCH.search(name): return None
    if TRAIN.search(name) or "足球培训" in (typ or "") or "教育培训" in (typ or ""):
        if re.search(r"体育学院|大学|中学|小学|职业技术学院|技工学校", name) and not re.search(r"俱乐部|青训|培训", name):
            return None
        return "培训机构/俱乐部"
    if VENUE.search(name): return "场馆"
    return "培训机构/俱乐部" if "足球" in name else None


def brand_of(name):
    b = re.sub(r"[（(].*?[)）]", "", name)
    b = re.sub(r"^(四川省?|成都市?|成都)", "", b)
    b = re.sub(r"(有限责任公司|有限公司|股份有限公司)$", "", b)
    b = re.sub(r"[-·—].*$", "", b)
    return b.strip() or name


rows, venues = [], []
seen_names = set()
for p in poi:
    name = (p.get("name") or "").strip()
    if not name or not FOOT.search(name) or JUNK.search(name): continue
    c = classify(name, p.get("type"))
    if not c: continue
    key = re.sub(r"\s", "", name)
    if key in seen_names: continue
    seen_names.add(key)
    tel = (p.get("tel") or "").strip()
    rec = {"name": name, "brand": brand_of(name), "district": norm_area(p.get("area"), p.get("address")),
           "address": (p.get("address") or "").strip(), "phone": tel, "poi_type": p.get("type") or "",
           "lng": p.get("x"), "lat": p.get("y"), "sources": ["360地图 POI（restapi.map.so.com）"], "confidence": "中",
           "status": "运营中（地图收录）"}
    if c == "协会":
        rec["type"] = "协会"; rows.append(rec)
    elif c == "场馆":
        rec["type"] = "场馆运营方"; venues.append(rec)
    else:
        rec["type"] = "培训机构/俱乐部"; rows.append(rec)

# huodong: name · district · area · tag
for h in hd:
    t = re.sub(r'^class="venue-card">\s*', "", h["text"]).strip()
    parts = [x.strip() for x in t.split(" · ")]
    head = parts[0]
    m = re.match(r"(.+?)\s+(\S+(?:区|市|县))$", head)
    if not m: continue
    name, area = m.group(1).strip(), m.group(2)
    if not FOOT.search(name) or JUNK.search(name): continue
    c = classify(name, "")
    if not c: continue
    key = re.sub(r"\s", "", name)
    if key in seen_names: continue
    seen_names.add(key)
    rec = {"name": name, "brand": brand_of(name), "district": norm_area(area + " " + " ".join(parts[1:2])), "address": "", "phone": "",
           "sources": ["https://huodong.com" + h["href"]], "confidence": "低", "status": "运营中（平台收录）", "type": "协会" if c == "协会" else ("场馆运营方" if c == "场馆" else "培训机构/俱乐部")}
    (venues if c == "场馆" else rows).append(rec)

# merge POI rows into seed when same brand core + district
def core(s):
    s = brand_of(s)
    s = re.sub(r"足球|俱乐部|培训|中心|青少年|少儿|青训|体育|学院|学校|训练营|基地|有限|公司|成都|四川|[（）()·\s]", "", s)
    return s

used = set()
for sd in seed:
    cs = core(sd["name"])
    if len(cs) < 2: continue
    for i, r in enumerate(rows):
        if i in used: continue
        cr = core(r["name"])
        if len(cr) >= 2 and (cs in cr or cr in cs) and (r["district"] == sd["district"] or sd["district"] == "全市/多区"):
            used.add(i)
            if not sd.get("address"): sd["address"] = r["address"]
            elif r["address"] and r["address"] not in sd["address"]:
                sd["campuses"] = ((sd.get("campuses") or "") + f"；地图收录：{r['name']}（{r['district']}）{r['address']}").lstrip("；")
            if r.get("phone") and not sd.get("phone"): sd["phone"] = r["phone"]
            sd.setdefault("sources", []); sd["sources"] += [s for s in r["sources"] if s not in sd["sources"]]
seed_types = {"培训机构", "业余俱乐部", "职业俱乐部青训", "海外青训分校", "协会", "场馆运营方", "其他"}
new_rows = [r for i, r in enumerate(rows) if i not in used]
for r in new_rows:
    if r["type"] == "培训机构/俱乐部":
        r["type"] = "业余俱乐部" if re.search(r"俱乐部|FC|球会", r["name"]) and not re.search(r"培训|学院|学校|训练营|教育", r["name"]) else "培训机构"
out = seed + new_rows
json.dump(out, open("orgs_v2.json", "w"), ensure_ascii=False, indent=0)
json.dump(venues, open("venues_v2.json", "w"), ensure_ascii=False, indent=0)
print("seed", len(seed), "poi-train", len(rows), "merged-into-seed", len(used), "new", len(new_rows), "total", len(out), "venues", len(venues))
