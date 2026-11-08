"""Essais comparatifs (voix Aoede, Google Chirp 3 HD).

    TESTS=audio/tests/passages-v2.json OUT_DIR=tests-2 python3 tools/audio/tests.py

Chaque groupe contient des variantes :
  ["libellé", "texte"]                                        (forme simple)
  {"label", "text" | "markup", "rate", "pron": [[mot, IPA]]}  (pauses [pause short], vitesse, prononciation)
  {"label", "existing": "../chemin.mp3"}                      (fichier déjà publié, pour comparer)
Apostrophes droites converties en apostrophes typographiques avant l'envoi (règle de docs/AUDIO-SCRIPTS.md).
Plafond strict : MAX_TOTAL_CHARS. Clé lue dans GOOGLE_TTS_API_KEY (secret GitHub), envoyée en en-tête.
"""
import os, json, base64, html, pathlib, sys, urllib.request

root = pathlib.Path(__file__).resolve().parents[2]
groups = json.loads((root / os.environ.get("TESTS", "audio/tests/passages.json")).read_text())
OUT = root / "site/audio" / os.environ.get("OUT_DIR", "tests"); OUT.mkdir(parents=True, exist_ok=True)
VOICE = os.environ.get("VOICE", "fr-FR-Chirp3-HD-Aoede")
MAX_TOTAL = int(os.environ.get("MAX_TOTAL_CHARS", "3000"))
TITLE = os.environ.get("TITLE", "Essais de diction · Aoede")
norm = lambda t: t.replace("'", "’")

def item(v):
    if isinstance(v, list): return {"label": v[0], "text": v[1]}
    return v
total = sum(len(item(v).get("text") or item(v).get("markup") or "") for g in groups for v in g["items"])
print(f"{total} caractères à générer (plafond {MAX_TOTAL})")
if total > MAX_TOTAL: sys.exit("Plafond dépassé : rien n'a été envoyé.")
KEY = os.environ.get("GOOGLE_TTS_API_KEY") or sys.exit("Secret GOOGLE_TTS_API_KEY absent.")

def synth(v):
    inp = {"markup": norm(v["markup"])} if v.get("markup") else {"text": norm(v["text"])}
    if v.get("pron"):
        inp["customPronunciations"] = {"pronunciations": [
            {"phrase": norm(p), "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": ipa} for p, ipa in v["pron"]]}
    cfg = {"audioEncoding": "MP3"}
    if v.get("rate"): cfg["speakingRate"] = v["rate"]
    req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", method="POST",
        data=json.dumps({"input": inp, "voice": {"languageCode": "fr-FR", "name": VOICE}, "audioConfig": cfg}).encode(),
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=180) as r: return base64.b64decode(json.loads(r.read())["audioContent"])
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Google HTTP {e.code} : {e.read()[:300].decode(errors='replace')}") from None

for f in OUT.glob("*.mp3"): f.unlink()
secs = []
for gi, g in enumerate(groups, 1):
    rows = []
    for vi, v in enumerate(g["items"], 1):
        v = item(v); shown = (v.get("text") or v.get("markup") or "")
        opts = " · ".join(x for x in [f"vitesse {v['rate']}" if v.get("rate") else "", "prononciation imposée" if v.get("pron") else "",
                                      "balises de pause" if v.get("markup") else ""] if x)
        if v.get("existing"):
            src = v["existing"]; err = ""
        else:
            src = f"t{gi}-{vi}.mp3"
            try: (OUT / src).write_bytes(synth(v)); err = ""; print("✓", src)
            except Exception as e: err = str(e); print("✗", src, err)
        player = f'<audio controls preload="none" src="{src}"></audio>' if not err else f'<p class="err">Échec : {html.escape(err[:160])}</p>'
        body = f"<p>{html.escape(norm(shown))}</p>" if shown and len(shown) < 700 else ""
        rows.append(f"""<div class="v"><b>{chr(64+vi)}. {html.escape(v['label'])}</b>{f'<small>{html.escape(opts)}</small>' if opts else ''}{body}{player}</div>""")
    note = f"<p class='note'>{html.escape(g['note'])}</p>" if g.get("note") else ""
    secs.append(f"<section><h2>{html.escape(g['groupe'])}</h2>{note}{''.join(rows)}</section>")
(OUT / "index.html").write_text(f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Moka · {html.escape(TITLE)}</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;background:#FDF9F4;color:#33241B;max-width:640px;margin:0 auto;padding:24px 18px 60px;line-height:1.45}}
h1{{color:#4A2C1F;font-size:26px}} h2{{color:#4A2C1F;font-size:18px;margin:0 0 10px}} section{{background:#fff;border:1px solid #EADBCB;border-radius:16px;padding:16px;margin:16px 0}}
.v{{padding:10px 0;border-top:1px solid #F1E5D8}} .v:first-of-type{{border-top:0}} .v p{{margin:4px 0 6px;color:#7A6455;font-size:14px}} .v small{{display:block;color:#8B5A3C;font-size:12px}}
.note{{color:#7A6455;font-size:14px;margin:0 0 6px}} .err{{color:#A03A2A}} audio{{width:100%}}</style></head>
<body><p><a href="../../" style="color:#8B5A3C">← Retour à Moka</a></p><h1>{html.escape(TITLE)}</h1>{''.join(secs)}</body></html>""")
print(f"Page : site/audio/{OUT.name}/index.html")
