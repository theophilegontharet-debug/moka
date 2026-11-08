"""Construit la version web indépendante de Moka dans site/ (déployée sur Vercel).

    python3 tools/build_site.py

Entrées :
  app/index.html                          l'application (la même que sur Claude Artifacts)
  data/articles.json + data/formats.json  les 16 articles d'origine et leurs formats
  data/patch-originaux-2026-11-07.json    suivis et sources ajoutés par les relèves
  data/auto-2026-11-07.json               les 16 articles de la relève du 7 novembre
  data/photos.json + photos/*.jpg         les photos et leurs crédits
  app/brand/symbol.svg                    le symbole (icônes générées à part : tools/make_icons.py)

Sortie : site/ (statique : index.html, data/articles.json, photos/, icons/, manifest, service worker).
Aucun lien Gmail ni adresse email n'est copié dans site/.
"""
import json, pathlib, re, shutil, hashlib

root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
D = root / "data"

# ---------- Articles ----------
arts = json.loads((D / "articles.json").read_text())
formats = json.loads((D / "formats.json").read_text())
patch = json.loads((D / "patch-originaux-2026-11-07.json").read_text())
for a in arts:
    a["formats"] = formats.get(a["id"])
    if a["id"] in patch["timeline"]:
        a["timeline"] = patch["timeline"][a["id"]]
    a["sources"] = a["sources"] + patch["add_sources"].get(a["id"], [])
arts += json.loads((D / "auto-2026-11-07.json").read_text())

photos = json.loads((D / "photos.json").read_text())
by_id = {a["id"]: a for a in arts}
for aid, im in photos.items():
    by_id[aid]["image"] = {k: v for k, v in im.items() if k != "asset"}

def clean_sources(srcs):
    out, seen = [], set()
    for s in srcs:
        s = {k: v for k, v in s.items() if k != "gmail"}
        key = (s.get("name"), s.get("date"), s.get("web"))
        # une source sans lien public est fusionnée avec la même source qui en a un
        if not s.get("web") and any(o.get("name") == s.get("name") and o.get("date") == s.get("date") for o in out):
            continue
        if key in seen: continue
        seen.add(key); out.append(s)
    return out
for a in arts:
    a["sources"] = clean_sources(a.get("sources", []))
    a.setdefault("image", None)

blob = json.dumps(arts, ensure_ascii=False, separators=(",", ":"))
assert "mail.google.com" not in blob and "@gmail" not in blob, "lien Gmail ou email dans les données"
assert len(arts) == 32, len(arts)
assert sum(1 for a in arts if a.get("image")) == len(photos)

# ---------- Fichiers ----------
if site.exists(): shutil.rmtree(site)
(site / "data").mkdir(parents=True)
(site / "data/articles.json").write_text(blob)
shutil.copytree(root / "photos", site / "photos")
shutil.copytree(root / "icons", site / "icons")
version = hashlib.sha1((blob + (root / "app/index.html").read_text()).encode()).hexdigest()[:10]

adapter = """<script>
/* Moka autonome : remplace window.claude (Claude Artifacts) par une lecture de fichiers statiques. */
window.MOKA_STANDALONE = true;
window.claude = { use: async (name) => {
  if (name !== "db") return null;            // pas d'utilisateur, de Gmail, de rédaction ni d'upload
  const load = fetch("data/articles.json?v=__V__").then(r => { if (!r.ok) throw {code: "http_" + r.status}; return r.json(); });
  const none = { exists: false, data: () => undefined };
  return {
    collection: () => ({ onSnapshot: (ok, ko) => { load.then(list => ok({ docs: list.map(a => ({ id: a.id, exists: true, data: () => a })), metadata: { fromCache: false } })).catch(e => ko && ko(e)); return () => {}; } }),
    doc: () => ({ onSnapshot: (ok) => { setTimeout(() => ok(none), 0); return () => {}; }, get: async () => none, set: async () => {}, update: async () => {} })
  };
}};
if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
</script>""".replace("__V__", version)

head = """<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon.svg" type="image/svg+xml">
<link rel="icon" href="icons/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Moka">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#FDF9F4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#1A120D" media="(prefers-color-scheme: dark)">
<meta name="description" content="Moka, votre brief quotidien : startups africaines, capital, énergie et tech.">
<link rel="preload" href="data/articles.json?v=__V__" as="fetch" crossorigin>""".replace("__V__", version)

html = (root / "app/index.html").read_text()
html = html.replace('<meta name="theme-color" content="#FDF9F4">\n', "", 1)
html = html.replace("<title>Moka</title>", "<title>Moka</title>\n" + head, 1)
marker = "<script>\n/* ============ Moka"
assert marker in html
html = html.replace(marker, adapter + "\n" + marker, 1)
(site / "index.html").write_text(html)

(site / "manifest.webmanifest").write_text(json.dumps({
    "name": "Moka", "short_name": "Moka", "lang": "fr",
    "description": "Votre brief quotidien : startups africaines, capital, énergie et tech.",
    "start_url": "./", "scope": "./", "display": "standalone",
    "background_color": "#FDF9F4", "theme_color": "#FDF9F4",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
}, ensure_ascii=False, indent=1))

# Service worker : page et données d'abord depuis le réseau (pour voir les mises à jour),
# photos et icônes depuis le cache (rapides, elles ne changent pas).
(site / "sw.js").write_text("""const C = "moka-__V__";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(["./", "data/articles.json?v=__V__"]))); });
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  if (/\\/(photos|icons)\\//.test(u.pathname)) {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); return res; })));
  } else {
    e.respondWith(fetch(e.request).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(e.request, cp)); return res; }).catch(() => caches.match(e.request)));
  }
});
""".replace("__V__", version))

(site / "vercel.json").write_text(json.dumps({
    "headers": [
        {"source": "/photos/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        {"source": "/icons/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
        {"source": "/sw.js", "headers": [{"key": "Cache-Control", "value": "no-cache"}]},
        {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]}]
}, indent=1))

print(f"site/ prêt : {len(arts)} articles, {len(photos)} photos, version {version}")
