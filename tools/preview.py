"""Aperçu local de Moka avec des données simulées (sans claude.ai).

  python3 tools/preview.py            → écrit preview/index.html
  ouvrir preview/index.html dans un navigateur

Remplace window.claude par une imitation minimale : base en lecture (articles + formats),
utilisateur propriétaire, pas de Gmail, pas de rédaction, pas d'assets.
Utile pour vérifier l'interface ; ne teste ni la collecte ni l'enregistrement.
"""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
arts = json.loads((root / "data/articles.json").read_text())
formats = json.loads((root / "data/formats.json").read_text())
for a in arts:
    a["formats"] = formats.get(a["id"])

mock = """<script>
const __A=%s;
window.claude={use:async(n)=>{
 if(n==='db'){ const snap=d=>({docs:d.map(a=>({id:a.id,exists:true,data:()=>a})),metadata:{fromCache:false}});
   return {collection:()=>({onSnapshot:f=>{setTimeout(()=>f(snap(__A)),10);return()=>{}}}),
           doc:()=>({onSnapshot:f=>{setTimeout(()=>f({exists:false,data:()=>undefined}),10);return()=>{}}, get:async()=>({exists:false}), set:async()=>{}, update:async()=>{}})}; }
 if(n==='user') return {id:async()=>'apercu', isOwner:async()=>true};
 return null; }};
</script>""" % json.dumps(arts, ensure_ascii=False)

html = (root / "app/index.html").read_text()
marker = "<script>\n/* ============ Moka"
assert marker in html, "marqueur introuvable dans app/index.html"
out = root / "preview"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(html.replace(marker, mock + "\n" + marker, 1))
print("preview/index.html écrit")
