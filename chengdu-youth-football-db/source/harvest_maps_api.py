"""Collect Chengdu youth-football POIs via the OFFICIAL Amap (高德) Web Service API v5 and Baidu Maps Place API v2.
Keys come from env: AMAP_KEY, BAIDU_AK (either one is enough). Respects daily quotas; ~3 req/s.
Output: maps_api.json (list of POIs with source, rating, review count, tel, address, district, type, coords)."""
import os, json, time, urllib.parse, urllib.request, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "maps_api.json"
AMAP_KEY, BAIDU_AK = os.environ.get("AMAP_KEY"), os.environ.get("BAIDU_AK")
ADCODES = {"锦江区": "510104", "青羊区": "510105", "金牛区": "510106", "武侯区": "510107", "成华区": "510108", "龙泉驿区": "510112",
           "青白江区": "510113", "新都区": "510114", "温江区": "510115", "双流区": "510116", "郫都区": "510117", "新津区": "510118",
           "简阳市": "510185", "都江堰市": "510181", "彭州市": "510182", "邛崃市": "510183", "崇州市": "510184", "金堂县": "510121",
           "大邑县": "510129", "蒲江县": "510131"}  # 高新区/天府新区/东部新区 are functional zones; covered by the district queries above
KWS = ["足球培训", "少儿足球", "青少年足球", "足球俱乐部", "足球青训", "足球训练营", "足球学校", "足球学院", "儿童足球", "足球协会", "足球公园"]
res = {}
if os.path.exists(OUT):
    for p in json.load(open(OUT)): res[p["src"] + p["id"]] = p


def get(url):
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "panda-league-research"}), timeout=20))
        except Exception:
            time.sleep(2)
    return {}


def amap(dist, code, kw):
    for page in range(1, 9):  # 25 x 8 = 200 per query max
        q = urllib.parse.urlencode({"key": AMAP_KEY, "keywords": kw, "region": code, "city_limit": "true", "page_size": 25,
                                    "page_num": page, "show_fields": "business"})
        d = get("https://restapi.amap.com/v5/place/text?" + q); time.sleep(0.35)
        pois = d.get("pois") or []
        if d.get("status") != "1": print("amap error", d.get("info")); return False
        for p in pois:
            b = p.get("business") or {}
            res["amap" + p["id"]] = {"src": "amap", "id": p["id"], "name": p.get("name"), "district": p.get("adname") or dist,
                                     "address": p.get("address"), "tel": b.get("tel"), "rating": b.get("rating"), "cost": b.get("cost"),
                                     "type": p.get("type"), "location": p.get("location"), "query": kw}
        if len(pois) < 25: break
    return True


def baidu(dist, kw):
    for page in range(0, 10):  # 20 x 10
        q = urllib.parse.urlencode({"ak": BAIDU_AK, "query": kw, "region": f"成都市{dist}", "city_limit": "true", "scope": 2,
                                    "page_size": 20, "page_num": page, "output": "json"})
        d = get("https://api.map.baidu.com/place/v2/search?" + q); time.sleep(0.35)
        if d.get("status") != 0: print("baidu error", d.get("message")); return False
        rs = d.get("results") or []
        for p in rs:
            di = p.get("detail_info") or {}
            res["baidu" + p["uid"]] = {"src": "baidu", "id": p["uid"], "name": p.get("name"), "district": p.get("area") or dist,
                                       "address": p.get("address"), "tel": p.get("telephone"), "rating": di.get("overall_rating"),
                                       "reviews": di.get("comment_num"), "cost": di.get("price"), "type": di.get("tag"),
                                       "location": p.get("location"), "query": kw}
        if len(rs) < 20: break
    return True


for dist, code in ADCODES.items():
    for kw in KWS:
        if AMAP_KEY and not amap(dist, code, kw): AMAP_KEY = None
        if BAIDU_AK and not baidu(dist, kw): BAIDU_AK = None
    json.dump(list(res.values()), open(OUT, "w"), ensure_ascii=False)
    print(dist, len(res), flush=True)
print("done", len(res))
