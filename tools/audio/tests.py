"""Essais comparatifs de formulations, voix Aoede (Google Chirp 3 HD).

Lit audio/tests/passages.json (groupes de variantes d'une même phrase), génère un MP3 par variante
dans site/audio/tests/ et une page d'écoute. Plafond strict : MAX_TOTAL_CHARS (3 000 par défaut).
La clé GOOGLE_TTS_API_KEY vient des secrets GitHub et part en en-tête uniquement.
"""
import os, json, base64, html, pathlib, sys, urllib.request

root = pathlib.Path(__file__).resolve().parents[2]
groups = json.loads((root / "audio/tests/passages.json").read_text())
OUT = root / "site/audio/tests"; OUT.mkdir(parents=True, exist_ok=True)
VOICE = os.environ.get("VOICE", "fr-FR-Chirp3-HD-Aoede")
MAX_TOTAL = int(os.environ.get("MAX_TOTAL_CHARS", "3000"))
total = sum(len(t) for g in groups for _, t in g["items"])
print(f"{total} caractères à générer (plafond {MAX_TOTAL})")
if total > MAX_TOTAL: sys.exit("Plafond dépassé : rien n'a été envoyé.")
KEY = os.environ.get("GOOGLE_TTS_API_KEY") or sys.exit("Secret GOOGLE_TTS_API_KEY absent.")

def synth(text):
    req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", method="POST",
        data=json.dumps({"input": {"text": text}, "voice": {"languageCode": "fr-FR", "name": VOICE},
                         "audioConfig": {"audioEncoding": "MP3"}}).encode(),
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return base64.b64decode(json.loads(r.read())["audioContent"])
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Google HTTP {e.code} : {e.read()[:300].decode(errors='replace')}") from None

for f in OUT.glob("*.mp3"): f.unlink()
secs = []
for gi, g in enumerate(groups, 1):
    rows = []
    for vi, (label, text) in enumerate(g["items"], 1):
        name = f"t{gi}-{vi}.mp3"; (OUT / name).write_bytes(synth(text)); print("✓", name)
        rows.append(f"""<div class="v"><b>{chr(64+vi)}. {html.escape(label)}</b><p>{html.escape(text)}</p>
<audio controls preload="none" src="{name}"></audio></div>""")
    secs.append(f"<section><h2>{html.escape(g['groupe'])}</h2>{''.join(rows)}</section>")
(OUT / "index.html").write_text(f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Moka · essais de diction</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;background:#FDF9F4;color:#33241B;max-width:640px;margin:0 auto;padding:24px 18px 60px;line-height:1.45}}
h1{{color:#4A2C1F;font-size:26px}} h2{{color:#4A2C1F;font-size:18px;margin:0 0 10px}} section{{background:#fff;border:1px solid #EADBCB;border-radius:16px;padding:16px;margin:16px 0}}
.v{{padding:10px 0;border-top:1px solid #F1E5D8}} .v:first-of-type{{border-top:0}} .v p{{margin:4px 0 6px;color:#7A6455;font-size:14px}} audio{{width:100%}}</style></head>
<body><p><a href="../../" style="color:#8B5A3C">← Retour à Moka</a></p><h1>Essais de diction · Aoede</h1>
<p>Pour chaque passage : A est la version actuelle, les suivantes sont les variantes corrigées.</p>{''.join(secs)}</body></html>""")
print("Page : site/audio/tests/index.html")
