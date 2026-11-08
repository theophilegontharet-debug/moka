import json, sys, time, urllib.request, urllib.parse, re, html
UA = "MokaReader/0.1 (private personal news reader; low volume)"
API = "https://commons.wikimedia.org/w/api.php"
OK = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [0-9.]+|CC BY [0-9.]+)", re.I)
def get(params, tries=3):
    q = API + "?" + urllib.parse.urlencode({**params, "format": "json", "maxlag": 5})
    for i in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(q, headers={"User-Agent": UA}), timeout=30)
            return json.load(r)
        except Exception as e:
            ra = getattr(e, "headers", None) and e.headers.get("retry-after")
            w = int(ra) + 3 if ra and ra.isdigit() else 30
            print(f"  … attente {w}s ({e})", flush=True); time.sleep(w)
    return {}
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
def search(query, n=8):
    d = get({"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
             "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1600})
    out = []
    for p in sorted((d.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        g = lambda k: strip(m.get(k, {}).get("value"))
        out.append(dict(title=p["title"], w=ii.get("width"), h=ii.get("height"), thumb=ii.get("thumburl"),
            page=ii.get("descriptionurl"), lic=g("LicenseShortName"), lic_url=g("LicenseUrl"), artist=g("Artist")[:120],
            credit=g("Credit")[:120], attr_req=g("AttributionRequired"), restrictions=g("Restrictions"),
            desc=g("ImageDescription")[:200], date=g("DateTimeOriginal")[:40], ok=bool(OK.match(g("LicenseShortName")))))
    return out
if __name__ == "__main__":
    qs = json.load(open(sys.argv[1])); res = {}
    for key, q in qs.items():
        res[key] = search(q); json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1); time.sleep(12)
        print(f"== {key} [{q}]", flush=True)
        for c in res[key]:
            print(f"  {'✓' if c['ok'] else '✗'} {c['w']}x{c['h']} {c['lic']} | {c['title'][5:90]} | {c['desc'][:90]}", flush=True)
    json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
