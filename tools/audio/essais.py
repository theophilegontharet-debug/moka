"""Génère des essais de voix (même passage, plusieurs voix) dans site/audio/essais/.

Exécuté par GitHub Actions (.github/workflows/audio-essais.yml). Les clés sont lues dans les
variables d'environnement, fournies par les « secrets » du dépôt : elles ne sont jamais écrites
dans un fichier ni affichées. Seuls les services dont la clé est présente sont utilisés.

  ELEVENLABS_API_KEY   ElevenLabs (voix françaises de la bibliothèque, modèle multilingue)
  OPENAI_API_KEY       OpenAI gpt-4o-mini-tts (voix guidée par une consigne de ton)
  GOOGLE_TTS_API_KEY   Google Cloud Text-to-Speech, voix Chirp 3 HD françaises

Garde-fou : chaque essai est limité à MAX_CHARS caractères (2 000 par défaut).
"""
import json, os, pathlib, sys, base64, urllib.request, urllib.parse, html

root = pathlib.Path(__file__).resolve().parents[2]
TEXT = (root / "audio/essais/octobre-afrique.txt").read_text().strip()
OUT = root / "site/audio/essais"; OUT.mkdir(parents=True, exist_ok=True)
MAX_CHARS = int(os.environ.get("MAX_CHARS", "2000"))          # par essai
MAX_TOTAL = int(os.environ.get("MAX_TOTAL_CHARS", "6000"))    # pour toute l'exécution
PROVIDERS = {p.strip() for p in os.environ.get("PROVIDERS", "elevenlabs").split(",") if p.strip()} - {"google"}  # Google Chirp retiré de Moka
assert len(TEXT) <= MAX_CHARS, f"texte trop long ({len(TEXT)} > {MAX_CHARS})"
spent = 0
def budget():
    global spent
    if spent + len(TEXT) > MAX_TOTAL:
        raise RuntimeError(f"plafond atteint ({spent} + {len(TEXT)} > {MAX_TOTAL} caractères)")
    spent += len(TEXT)

def call(url, body=None, headers=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"),
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} : {e.read()[:300].decode(errors='replace')}") from None

made = []
def save(slug, label, provider, audio, note):
    (OUT / f"{slug}.mp3").write_bytes(audio)
    made.append({"file": f"{slug}.mp3", "label": label, "provider": provider, "note": note, "chars": len(TEXT)})
    print(f"✓ {slug}.mp3 ({len(audio)//1024} Ko)")

# ---------- ElevenLabs ----------
k = os.environ.get("ELEVENLABS_API_KEY")
if k and "elevenlabs" in PROVIDERS:
    H = {"xi-api-key": k}
    try:
        wanted = [v.strip() for v in os.environ.get("ELEVENLABS_VOICE_IDS", "").split(",") if v.strip()]
        voices = []  # (voice_id, nom)
        if wanted:
            voices = [(v, v[:6]) for v in wanted[:2]]
        else:
            # Voix françaises natives les plus utilisées de la bibliothèque, ajoutées au compte
            q = urllib.parse.urlencode({"language": "fr", "page_size": 30, "sort": "cloned_by_count"})
            lib = json.loads(call(f"https://api.elevenlabs.io/v1/shared-voices?{q}", headers=H)[0])["voices"]
            pref = [v for v in lib if any(u in (v.get("use_case") or "") for u in ("narrative", "conversational", "informative", "social"))] or lib
            picked, genders = [], set()
            for v in pref:
                g = v.get("gender")
                if g not in genders: picked.append(v); genders.add(g)
                if len(picked) == 2: break
            mine = json.loads(call("https://api.elevenlabs.io/v1/voices", headers=H)[0]).get("voices", [])
            for v in picked:
                name = f"Moka {v['name']}"[:40]
                found = next((m for m in mine if m["name"] == name), None)
                if not found:
                    r = json.loads(call(f"https://api.elevenlabs.io/v1/voices/add/{v['public_owner_id']}/{v['voice_id']}", {"new_name": name}, H)[0])
                    vid = r["voice_id"]
                else:
                    vid = found["voice_id"]
                voices.append((vid, v["name"]))
        for vid, name in voices:
            budget()
            audio, _ = call(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                            {"text": TEXT, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
                             "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}, H)
            slug = "elevenlabs-" + "".join(c for c in name.lower() if c.isalnum())[:20]
            save(slug, f"ElevenLabs · {name}", "ElevenLabs", audio, "Voix française de la bibliothèque ElevenLabs, modèle multilingue v2.")
    except Exception as e:
        print("ElevenLabs : échec :", e)

# ---------- OpenAI ----------
k = os.environ.get("OPENAI_API_KEY")
if k and "openai" in PROVIDERS:
    try:
        budget()
        audio, _ = call("https://api.openai.com/v1/audio/speech", {
            "model": "gpt-4o-mini-tts", "voice": os.environ.get("OPENAI_VOICE", "coral"), "input": TEXT, "response_format": "mp3",
            "instructions": "Parle en français de France, comme un ami qui raconte l'actualité dans un podcast : ton chaleureux, "
                            "détendu et pédagogique, débit posé, petites pauses naturelles, sans emphase journalistique."},
            {"Authorization": f"Bearer {k}"})
        save("openai-coral", "OpenAI · Coral", "OpenAI", audio, "gpt-4o-mini-tts avec une consigne de ton « ami qui raconte ».")
    except Exception as e:
        print("OpenAI : échec :", e)

# ---------- Google ----------
k = os.environ.get("GOOGLE_TTS_API_KEY")
if k and "google" in PROVIDERS:
    G = "https://texttospeech.googleapis.com/v1"
    KH = {"X-Goog-Api-Key": k}
    try:
        vs = json.loads(call(f"{G}/voices?languageCode=fr-FR", headers=KH)[0]).get("voices", [])
        chirp = [v for v in vs if "Chirp3-HD" in v["name"] and "fr-FR" in v.get("languageCodes", [])]
        print("Voix fr-FR Chirp 3 HD disponibles :", ", ".join(f"{v['name'].split('-')[-1]} ({v.get('ssmlGender','?')[0]})" for v in chirp))
        wanted = [w.strip() for w in os.environ.get("GOOGLE_VOICES", "").split(",") if w.strip()]
        pref = ["Aoede", "Leda", "Kore", "Despina", "Charon", "Achird", "Orus", "Puck"]
        rank = lambda v: pref.index(v["name"].split("-")[-1]) if v["name"].split("-")[-1] in pref else 99
        if wanted:
            picked = [v for v in chirp if v["name"].split("-")[-1] in wanted]
        else:
            fem = sorted([v for v in chirp if v.get("ssmlGender") == "FEMALE"], key=rank)[:2]
            mal = sorted([v for v in chirp if v.get("ssmlGender") == "MALE"], key=rank)[:2]
            picked = fem + mal
        if not picked: raise RuntimeError("aucune voix Chirp 3 HD française trouvée")
    except Exception as e:
        print("Google : liste des voix impossible :", e); picked = []
    for v in picked:
        label = v["name"].split("-")[-1]; genre = {"FEMALE": "voix féminine", "MALE": "voix masculine"}.get(v.get("ssmlGender"), "voix")
        try:
            budget()
            raw, _ = call(f"{G}/text:synthesize",
                          {"input": {"text": TEXT}, "voice": {"languageCode": "fr-FR", "name": v["name"]},
                           "audioConfig": {"audioEncoding": "MP3"}}, KH)
            save("google-" + label.lower(), f"Google Chirp 3 HD · {label}", "Google Cloud", base64.b64decode(json.loads(raw)["audioContent"]),
                 f"{genre.capitalize()} française ({v['name']}).")
        except Exception as e:
            print(f"Google {label} : échec :", e)

if not made:
    sys.exit("Aucun essai produit : ajoutez au moins une clé dans les secrets du dépôt.")

# ---------- Page d'écoute ----------
old = []
mf = OUT / "essais.json"
if mf.exists():
    old = [e for e in json.loads(mf.read_text()) if e["file"] not in {m["file"] for m in made} and (OUT / e["file"]).exists()]
allm = old + made
mf.write_text(json.dumps(allm, ensure_ascii=False, indent=1))
items = "".join(f"""<section><h2>{html.escape(m['label'])}</h2><p>{html.escape(m['note'])}</p>
<audio controls preload="none" src="{m['file']}"></audio></section>""" for m in allm)
(OUT / "index.html").write_text(f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Moka · essais de voix</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;background:#FDF9F4;color:#33241B;max-width:640px;margin:0 auto;padding:24px 18px 60px;line-height:1.5}}
h1{{color:#4A2C1F;font-size:26px}} h2{{color:#4A2C1F;font-size:18px;margin:0 0 4px}} section{{background:#fff;border:1px solid #EADBCB;border-radius:16px;padding:16px;margin:14px 0}}
audio{{width:100%;margin-top:8px}} p{{margin:0;color:#7A6455;font-size:14px}} blockquote{{white-space:pre-line;font-size:14px;color:#7A6455;border-left:3px solid #D7A77A;margin:20px 0;padding-left:12px}}</style></head>
<body><p><a href="../../" style="color:#8B5A3C">← Retour à Moka</a></p><h1>Essais de voix</h1><p>Même passage, plusieurs voix de synthèse. Écoutez au casque si possible.</p>{items}
<h2 style="margin-top:28px">Le texte lu</h2><blockquote>{html.escape(TEXT)}</blockquote></body></html>""")
print(f"{len(made)} essai(s) écrit(s) dans site/audio/essais/ — {spent} caractères envoyés au total")
