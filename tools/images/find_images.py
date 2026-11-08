"""Moka — recherche d'images réutilisables pour un article.

STATUT : prototype NON TESTÉ. La session de travail où il a été écrit n'a pas accès
à commons.wikimedia.org ni à api.unsplash.com (connexion refusée par le proxy).

Usage :
  python3 find_images.py data/articles.json <article_id>
  UNSPLASH_ACCESS_KEY=... python3 find_images.py data/articles.json <article_id>

Ordre de priorité : photo du sujet (Commons, par entité) → photo de contexte
(Commons puis Unsplash, par lieu ou secteur) → aucune (l'app garde l'illustration Moka).
Chaque candidat doit ensuite être vérifié visuellement avant publication.
"""
import json, os, re, sys, urllib.parse, urllib.request

UA = "MokaImageFinder/0.1 (application personnelle ; contact via le dépôt)"
OK_LICENSES = re.compile(r"^(cc0|pd|public domain|cc[- ]by(-sa)?[- ]\d)", re.I)
BAD_LICENSES = re.compile(r"(nc|nd|fair use|non-free)", re.I)

def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

def commons(query, limit=8):
    """Fichiers Commons correspondant à la requête, avec licence et auteur."""
    params = {
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6, "gsrlimit": limit, "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": 1600,
    }
    data = get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params))
    out = []
    for page in (data.get("query", {}).get("pages", {}) or {}).values():
        ii = (page.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip_html(md.get("LicenseShortName", {}).get("value"))
        if not lic or BAD_LICENSES.search(lic) or not OK_LICENSES.search(lic):
            continue
        if ii.get("width", 0) < 900:
            continue
        out.append({
            "provider": "wikimedia", "title": page.get("title"), "download": ii.get("thumburl") or ii.get("url"),
            "source_url": ii.get("descriptionurl"), "credit": strip_html(md.get("Artist", {}).get("value")) or "Auteur inconnu",
            "license": lic, "license_url": md.get("LicenseUrl", {}).get("value"),
            "description": strip_html(md.get("ImageDescription", {}).get("value"))[:300], "query": query,
        })
    return out

def unsplash(query, limit=5):
    """Photos Unsplash (contexte uniquement). Exige une clé API et l'attribution du photographe."""
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return []
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode({"query": query, "per_page": limit, "orientation": "landscape"})
    data = get_json(url, {"Authorization": f"Client-ID {key}"})
    return [{
        "provider": "unsplash", "download": p["urls"]["regular"], "download_location": p["links"]["download_location"],
        "source_url": p["links"]["html"] + "?utm_source=moka&utm_medium=referral",
        "credit": f'{p["user"]["name"]} / Unsplash', "credit_url": p["user"]["links"]["html"] + "?utm_source=moka&utm_medium=referral",
        "license": "Licence Unsplash", "license_url": "https://unsplash.com/license",
        "description": p.get("alt_description") or "", "query": query,
    } for p in data.get("results", [])]

def candidates(article):
    """Requêtes : entités d'abord (photo du sujet), puis lieux/secteurs (photo de contexte)."""
    subject = [e for e in article.get("entities", [])[:4]]
    context = [t for t in article.get("tags", [])[:3]]
    found = []
    for q in subject:
        for c in commons(q):
            found.append({**c, "kind": "sujet"})
    for q in context:
        for c in commons(q):
            found.append({**c, "kind": "contexte"})
        for c in unsplash(q):
            found.append({**c, "kind": "contexte"})
    return found

if __name__ == "__main__":
    articles = {a["id"]: a for a in json.load(open(sys.argv[1]))}
    a = articles[sys.argv[2]]
    print(json.dumps(candidates(a), ensure_ascii=False, indent=1))
