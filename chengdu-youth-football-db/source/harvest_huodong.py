"""Harvest Chengdu football venues from huodong.com listing pages (name, district, sub-area, link). Polite pacing."""
import re, json, time, sys, html, urllib.request, urllib.parse

OUT = sys.argv[1]
items = {}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for _ in range(3):
        try:
            return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(3)
    return ""


def parse(t):
    # each card: <a href="/venue/detail/xxx"> ... name ... district · area · tag
    out = []
    for m in re.finditer(r'href="(/venue/detail/[a-zA-Z0-9]+)"(.*?)</a>', t, re.S):
        txt = re.sub(r"<[^>]+>", " ", m.group(2)); txt = re.sub(r"\s+", " ", html.unescape(txt)).strip()
        if txt: out.append((m.group(1), txt))
    return out


sources = [f"https://huodong.com/venue/chengdu/football?page={p}" for p in range(1, 15)]
for kw in ["足球", "足球培训", "青训", "少儿足球"]:
    sources += [f"https://huodong.com/venue/chengdu?keyword={urllib.parse.quote(kw)}&page={p}" for p in range(1, 12)]
last = None
for u in sources:
    t = get(u)
    cards = parse(t)
    sig = tuple(c[0] for c in cards)
    if not cards or sig == last:
        continue
    last = sig
    for href, txt in cards:
        items.setdefault(href, txt)
    print(u, len(cards), len(items), flush=True)
    time.sleep(1.2)
json.dump([{"href": k, "text": v} for k, v in items.items()], open(OUT, "w"), ensure_ascii=False, indent=0)
print("done", len(items))
