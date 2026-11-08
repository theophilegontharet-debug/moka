"""Importe des photos Wikimedia Commons choisies à la main dans Moka.

    python3 tools/images/commons_import.py data/photos-candidats.json

Pour chaque entrée {article, file, kind, caption, alt, crop_y} :
  1. lit la page Commons (auteur, licence, lien de licence, restrictions) ;
  2. refuse tout ce qui n'est pas CC0, domaine public, CC BY ou CC BY-SA ;
  3. télécharge une miniature standard (1 280 px), recadre les formats extrêmes, compresse en JPEG ;
  4. écrit photos/<nom>.jpg et l'entrée de data/photos.json (crédits, licence, obligations, source).
Les articles qui ont déjà une photo ne sont pas modifiés. Lancé par l'action « Photos Commons ».
"""
import json, sys, time, io, re, html, pathlib, urllib.request, urllib.parse
from PIL import Image, ImageOps

root = pathlib.Path(__file__).resolve().parents[2]
UA = "MokaBot/1.0 (https://github.com/theophilegontharet-debug/moka; low volume)"
OK = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? [0-9.]+)", re.I)

def get(url, as_json=True):
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                b = r.read(); return json.loads(b) if as_json else b
        except urllib.error.HTTPError as e:
            ra = e.headers.get("retry-after"); w = int(ra) + 2 if ra and ra.isdigit() else 15 * (i + 1)
            print(f"  attente {w}s ({e.code})", flush=True); time.sleep(w)
    raise RuntimeError("échec " + url)

strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
cands = json.loads(pathlib.Path(sys.argv[1]).read_text())
pfile = root / "data/photos.json"; P = json.loads(pfile.read_text())
report = []
for c in cands:
    aid = c["article"]
    if aid in P: report.append(f"= {aid[:40]} : a déjà une photo, ignoré"); continue
    q = urllib.parse.urlencode({"action": "query", "titles": c["file"], "prop": "imageinfo", "iiprop": "url|size|extmetadata",
                                "iiurlwidth": 1280, "format": "json", "maxlag": 5})
    page = next(iter(get("https://commons.wikimedia.org/w/api.php?" + q)["query"]["pages"].values()))
    if "imageinfo" not in page: report.append(f"✗ {c['file']} : introuvable"); continue
    ii = page["imageinfo"][0]; m = ii.get("extmetadata", {}); g = lambda k: strip(m.get(k, {}).get("value"))
    lic, lic_url, artist = g("LicenseShortName"), g("LicenseUrl"), g("Artist")
    if not OK.match(lic) or g("Restrictions"):
        report.append(f"✗ {c['file']} : licence refusée ({lic}) {g('Restrictions')}"); continue
    raw = get(ii["thumburl"].replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/"), as_json=False)
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB"); W, H = im.size; r = W / H; crop = False
    if r > 2.0: nw = H * 2; x = (W - nw) // 2; im = im.crop((x, 0, x + nw, H)); crop = True
    elif r < 1.3: nh = int(W / 1.5); y = int((H - nh) * c.get("crop_y", 0.5)); im = im.crop((0, y, W, y + nh)); crop = True
    if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    name = c.get("name") or re.sub(r"[^a-z0-9]+", "-", aid.lower())[:40].strip("-")
    (root / "photos").mkdir(exist_ok=True); im.save(root / f"photos/{name}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    if lic in ("CC0",) or lic.startswith("CC0"): L, LU, att = "CC0 1.0 (domaine public)", "https://creativecommons.org/publicdomain/zero/1.0/deed.fr", "Aucune obligation ; crédit indiqué par courtoisie."
    elif lic.lower().startswith(("public domain", "pd")): L, LU, att = "Domaine public", ii["descriptionurl"], "Aucune obligation selon la page Commons ; crédit indiqué par courtoisie."
    else:
        L, LU = lic, lic_url.replace("http://", "https://").rstrip("/") + "/deed.fr"
        att = "Citer l'auteur, la licence et la source, et indiquer les modifications." + (" La version modifiée reste diffusée sous la même licence." if "SA" in lic else "")
    P[aid] = {"src": f"photos/{name}.jpg", "kind": c["kind"], "subject": "sujet" if c["kind"] == "photo" else "contexte",
              "caption": c["caption"], "alt": c["alt"], "title": c["file"][5:].rsplit(".", 1)[0], "credit": c.get("credit") or artist[:60],
              "author": artist, "license": L, "license_url": LU, "attribution": att,
              "modifications": "recadrée et redimensionnée" if crop else "redimensionnée", "source_url": ii["descriptionurl"],
              "source_site": "Wikimedia Commons", "width": im.width, "height": im.height, "added_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    report.append(f"✓ {aid[:40]} ← {c['file'][5:60]} ({L}, {im.width}×{im.height})")
    time.sleep(3)

pfile.write_text(json.dumps(P, ensure_ascii=False, indent=1))
L = ["# Crédits des photographies", "", "Toutes les photos proviennent de Wikimedia Commons. Elles ont été redimensionnées (et parfois recadrées) pour le web ; ces versions modifiées restent sous la licence de l'original, en particulier pour les licences CC BY-SA (partage dans les mêmes conditions).", "",
     "| Fichier | Sujet | Auteur | Licence | Modifications | Source |", "|---|---|---|---|---|---|"]
for _, im in sorted(P.items(), key=lambda x: x[1]["src"]):
    L.append(f"| `{im['src'].split('/')[-1]}` | {im['caption']} | {im['author']} | [{im['license']}]({im['license_url']}) | {im['modifications']} | [Commons]({im['source_url']}) |")
L += ["", "Les illustrations Moka (paysages générés dans l'application) et le logo appartiennent au projet Moka."]
(root / "photos/CREDITS.md").write_text("\n".join(L) + "\n")
print("\n".join(report))
