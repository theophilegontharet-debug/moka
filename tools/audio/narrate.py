"""Génère les narrations MP3 de Moka (Google Chirp 3 HD, voix Aoede) à partir des scripts oraux.

    ARTICLES="exits-afrique-octobre,revolut-115-milliards" python3 tools/audio/narrate.py

Entrées : audio/scripts/<article>/<format>.txt (texte réécrit pour l'oral, relu, sans fait nouveau).
Sorties : site/audio/<article>/<format>-<empreinte>.mp3 et site/audio/index.json.

- Un fichier n'est généré que si son script a changé (empreinte du texte + voix) : jamais à l'écoute.
- Plafonds : MAX_FILE_CHARS par fichier, MAX_TOTAL_CHARS par exécution, vérifiés AVANT tout appel.
- La clé GOOGLE_TTS_API_KEY vient des secrets GitHub, part en en-tête, n'est jamais écrite.
- Google limite une requête à 5 000 octets : le texte est découpé par paragraphes, puis les MP3 sont
  mis bout à bout (même encodage, lecture continue).
"""
import os, json, hashlib, base64, pathlib, re, sys, urllib.request

root = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = root / "audio/scripts"; OUT = root / "site/audio"; IDX = OUT / "index.json"
VOICE = os.environ.get("VOICE", "fr-FR-Chirp3-HD-Aoede")
MAX_FILE = int(os.environ.get("MAX_FILE_CHARS", "12000"))
MAX_TOTAL = int(os.environ.get("MAX_TOTAL_CHARS", "25000"))
FORMATS = [f for f in os.environ.get("FORMATS", "express,comprendre,approfondir").split(",") if f]
ARTICLES = [a.strip() for a in os.environ.get("ARTICLES", "").split(",") if a.strip()]
DRY = os.environ.get("DRY_RUN") == "1"
if not ARTICLES: sys.exit("Indiquez les articles (ARTICLES=id1,id2).")

index = json.loads(IDX.read_text()) if IDX.exists() else {}
todo = []
for a in ARTICLES:
    for f in FORMATS:
        p = SCRIPTS / a / f"{f}.txt"
        if not p.exists(): continue                      # format inexistant : rien à générer
        text = p.read_text().strip()
        h = hashlib.sha256((VOICE + "\n" + text).encode()).hexdigest()[:10]
        cur = index.get(a, {}).get(f)
        if cur and cur.get("hash") == h and (OUT / a / cur["file"]).exists():
            print(f"= {a}/{f} : déjà généré, réutilisé"); continue
        if len(text) > MAX_FILE: sys.exit(f"{a}/{f} : {len(text)} caractères > plafond par fichier {MAX_FILE}")
        todo.append((a, f, text, h))
total = sum(len(t) for _, _, t, _ in todo)
print(f"À générer : {len(todo)} fichier(s), {total} caractères (plafond {MAX_TOTAL})")
if total > MAX_TOTAL: sys.exit("Plafond par exécution dépassé : rien n'a été envoyé à Google.")
if DRY or not todo: sys.exit(0)

KEY = os.environ.get("GOOGLE_TTS_API_KEY") or sys.exit("Secret GOOGLE_TTS_API_KEY absent.")
def chunks(text, limit=4500):
    out, cur = [], ""
    for par in [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]:
        cand = (cur + "\n\n" + par).strip()
        if len(cand.encode()) <= limit: cur = cand; continue
        if cur: out.append(cur)
        while len(par.encode()) > limit:                 # paragraphe trop long : coupe à une phrase
            k = par.rfind(". ", 0, limit // 2); k = k + 1 if k > 0 else limit // 2
            out.append(par[:k].strip()); par = par[k:].strip()
        cur = par
    if cur: out.append(cur)
    return out
def synth(text):
    req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", method="POST",
        data=json.dumps({"input": {"text": text}, "voice": {"languageCode": "fr-FR", "name": VOICE},
                         "audioConfig": {"audioEncoding": "MP3"}}).encode(),
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=180) as r: return base64.b64decode(json.loads(r.read())["audioContent"])
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Google HTTP {e.code} : {e.read()[:300].decode(errors='replace')}") from None

sent = 0
for a, f, text, h in todo:
    audio = b"".join(synth(c) for c in chunks(text)); sent += len(text)
    d = OUT / a; d.mkdir(parents=True, exist_ok=True)
    old = index.get(a, {}).get(f, {}).get("file")
    name = f"{f}-{h}.mp3"; (d / name).write_bytes(audio)
    if old and old != name and (d / old).exists(): (d / old).unlink()   # remplace l'ancienne version
    index.setdefault(a, {})[f] = {"file": name, "hash": h, "voice": VOICE.split("-")[-1], "chars": len(text),
                                  "bytes": len(audio), "seconds": round(len(audio) * 8 / 32000)}
    IDX.write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True))
    print(f"✓ {a}/{name} ({len(audio)//1024} Ko, ~{round(len(audio)*8/32000)} s)")
print(f"Terminé : {sent} caractères envoyés à Google.")
