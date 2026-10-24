"""Harvest football-related POIs in Chengdu from 360 Maps public search API (polite: ~1 req/s)."""
import json, time, urllib.parse, urllib.request, sys, os

OUT = sys.argv[1]
AREAS = ["锦江区", "青羊区", "金牛区", "武侯区", "成华区", "高新区", "天府新区", "东部新区", "龙泉驿区", "青白江区", "新都区", "温江区",
         "双流区", "郫都区", "新津区", "简阳市", "都江堰市", "彭州市", "邛崃市", "崇州市", "金堂县", "大邑县", "蒲江县"]
KWS = ["足球", "足球培训", "足球俱乐部", "少儿足球", "青少年足球", "足球青训", "足球训练", "足球学校", "足球学院", "足球训练营", "足球公园", "足球协会", "球会", "体育培训 足球"]
CITY_KWS = KWS + ["儿童足球", "幼儿足球", "足球体适能", "FC足球", "足球中心", "青训"]

seen = {}
if os.path.exists(OUT):
    for p in json.load(open(OUT)): seen[p["pguid"]] = p


def q(keyword):
    url = ("https://restapi.map.so.com/newapi?" + urllib.parse.urlencode(
        {"keyword": keyword, "cityname": "成都", "number": 50, "batch": 1, "sid": 1000}))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:
            time.sleep(3)
    return {}


queries = [f"{a} {k}" for a in AREAS for k in KWS] + CITY_KWS
n0 = len(seen)
for i, kw in enumerate(queries):
    d = q(kw)
    for p in d.get("poi") or []:
        if p.get("city") != "成都市": continue
        g = p.get("pguid") or p.get("primaryid")
        if not g: continue
        if g not in seen:
            seen[g] = {k: p.get(k) for k in ["pguid", "name", "area", "address", "tel", "type", "cat_new_name", "category", "x", "y", "adcode", "b_area_name"]}
            seen[g]["queries"] = []
        seen[g]["queries"].append(kw)
    if i % 25 == 0:
        print(i, kw, len(seen), flush=True)
        json.dump(list(seen.values()), open(OUT, "w"), ensure_ascii=False)
    time.sleep(1.0)
json.dump(list(seen.values()), open(OUT, "w"), ensure_ascii=False)
print("done", len(seen), "new", len(seen) - n0)
