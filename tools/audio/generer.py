"""Génération d'une narration Moka avec UNE voix choisie (GitHub Actions uniquement).

Commande : audio/commande.json
  {"mode": "estimer"|"generer", "demande": n, "voix": "el:<voice_id>"|"google:Aoede",
   "modele": "eleven_v4"|"eleven_multilingual_v2", "articles": [...], "formats": [...],
   "scripts": "audio/scripts-v2"}
  - estimer : gratuit, aucun appel de synthèse ; affiche le coût prévisionnel et « solde suffisant : oui/non ».
  - generer : payant ; uniquement après accord explicite. Une même « demande » n'est jamais exécutée deux fois.

Garde-fous ElevenLabs (registre public audio/phase.json, sans solde du compte) :
  - plafond de phase (10 000 crédits), consommation déjà enregistrée comprise ;
  - solde vérifié avant chaque fichier (marge de 500) ; coût réel relevé après chaque fichier ;
  - arrêt si le coût réel est inconnu ou dépasse 1,25 × l'estimation + 20 ;
  - MP3 déjà produit pour le même texte, la même voix et le même modèle : réutilisé, rien n'est payé.
Le solde exact du compte n'est jamais affiché (journaux publics).
"""
import hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from engines import APOS, EngineError, el_models, el_subscription, el_tts, google_tts

root = pathlib.Path(__file__).resolve().parents[2]
CMD = json.loads((root / "audio/commande.json").read_text())
MODE = os.environ.get("MODE") or CMD["mode"]
PHASE_F = root / "audio/phase.json"
NARR_F = root / "site/audio/narrations.json"
CAT = json.loads((root / "site/audio/voix.json").read_text())
MARGE = 500
GOOGLE_MAX_CHARS = 25000

phase = json.loads(PHASE_F.read_text()) if PHASE_F.exists() else {"plafond": 10000, "consomme": 0, "demandes": [], "fichiers": []}
narr = json.loads(NARR_F.read_text()) if NARR_F.exists() else {}

voix = next((v for v in CAT["voix"] if v["id"] == CMD["voix"]), None)
if not voix:
    sys.exit(f"Voix inconnue du catalogue : {CMD['voix']} (relancer le mode voix)")
eng = voix["engine"]
modele = CMD.get("modele", "eleven_v4") if eng == "elevenlabs" else "chirp3-hd"
if eng == "elevenlabs" and voix.get("v4") is False and modele == "eleven_v4":
    print("Voix non optimisée pour Eleven v4 : bascule sur Multilingual v2"); modele = "eleven_multilingual_v2"

# ---------- texte : règles communes + ajustements par moteur ----------
CHIRP_PAUSE = re.compile(r"\[pause(?: short| long)?\]")
TAG = re.compile(r"\[[a-zA-Zéèàù' -]{2,30}\]")

def adapter(t):
    t = APOS(t.strip())
    if eng == "google":
        return TAG.sub(lambda m: m.group(0) if CHIRP_PAUSE.fullmatch(m.group(0)) else "", t)
    t = re.sub(r"\[pause short\]\s*", "", t)            # pauses Chirp → ponctuation pour ElevenLabs
    t = re.sub(r"\s*\[pause(?: long)?\]\s*", "… ", t)
    if modele != "eleven_v4":                              # balises d'expression : Eleven v4 seulement
        t = TAG.sub("", t)
    return re.sub(r"[ \t]+", " ", t).strip()

def source(art, fmt):
    dirs = CMD.get("scripts", "audio/scripts")
    for base in ([dirs] if isinstance(dirs, str) else dirs):     # premier dossier qui a le script
        d = root / base / art
        for name in (f"{fmt}.{eng}.txt", f"{fmt}.txt"):
            if (d / name).exists(): return d / name
    return None

def chunks(text, limit):
    out, cur = [], ""
    for par in text.split("\n\n"):
        if cur and len(cur) + len(par) + 2 > limit: out.append(cur); cur = par
        else: cur = f"{cur}\n\n{par}" if cur else par
    return out + ([cur] if cur else [])

def joindre(parts):
    """Assemble les MP3 de plusieurs requêtes en un seul fichier propre (en-têtes d'origine retirés)."""
    if len(parts) == 1 or not shutil.which("ffmpeg"): return b"".join(parts)
    with tempfile.TemporaryDirectory() as d:
        names = []
        for i, b in enumerate(parts):
            n = f"{d}/p{i}.mp3"; open(n, "wb").write(b); names.append(n)
        open(f"{d}/l.txt", "w").write("".join(f"file '{n}'\n" for n in names))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{d}/l.txt", "-c", "copy", f"{d}/o.mp3"], check=True)
        return open(f"{d}/o.mp3", "rb").read()

mult = (CAT.get("modeles") or {}).get(modele) if eng == "elevenlabs" else 0
if eng == "elevenlabs" and mult is None:
    try: mult = next(((m.get("model_rates") or {}).get("character_cost_multiplier") for m in el_models() if m["model_id"] == modele), None)
    except EngineError as e: print("modèles :", e)
tarif = voix.get("rate") if eng == "elevenlabs" else 0

# coût réellement observé par caractère (registre) ; pire cas = multiplicateur × tarif annoncés
obs = [f["credits"] / f["chars"] for f in phase["fichiers"] if f.get("chars") and f.get("voix") == voix["id"] and f.get("modele") == modele]
pire = (mult or 0) * (tarif or 0)
ratio = min(pire, max(obs) * 1.02) if (obs and pire) else pire

def decoupe(text, reste):
    """Requêtes successives : jusqu'à CHUNK caractères, mais chacune doit tenir dans le reste du plafond
    même au tarif annoncé (pire cas). Renvoie la liste des requêtes, ou None si le fichier ne tient pas
    en supposant le coût observé."""
    pars, out = text.split("\n\n"), []
    while pars:
        cur = ""
        while pars and len(cur) + len(pars[0]) + 2 <= CHUNK and (len(cur) + len(pars[0]) + 2) * pire <= reste:
            cur = f"{cur}\n\n{pars.pop(0)}" if cur else pars.pop(0)
        if not cur: return None
        out.append(cur); reste -= len(cur) * ratio
    return out
CHUNK = 2500

plan = []
for fmt in CMD["formats"]:            # ordre : formats d'abord (Approfondir, Comprendre, Express)
    for art in CMD["articles"]:
        p = source(art, fmt)
        if not p: print(f"  {art}/{fmt} : pas de script, ignoré"); continue
        text = adapter(p.read_text())
        h = hashlib.sha256(f"{voix['id']}|{modele}\n{text}".encode()).hexdigest()[:10]
        prev = narr.get(art, {}).get(voix["id"], {}).get(fmt)
        reuse = bool(prev and prev.get("hash") == h and (root / "site/audio" / art / prev["file"]).exists())
        est = 0 if (reuse or eng == "google") else (round(len(text) * ratio) if ratio else None)
        plan.append({"art": art, "fmt": fmt, "src": str(p.relative_to(root)), "text": text, "hash": h, "reuse": reuse, "est": est})

total = sum(x["est"] or 0 for x in plan)
print(f"Voix {voix['label']} ({voix['id']}) · modèle {modele} · multiplicateur {mult} · tarif voix ×{tarif}")
for x in plan:
    print(f"  {x['art']}/{x['fmt']:11} {len(x['text']):5} caractères  "
          + ("déjà généré, réutilisé" if x["reuse"] else f"≈ {x['est']} crédits" if eng == "elevenlabs" else "Google (gratuit dans le quota)")
          + f"  [{x['src']}]")
reste_phase = phase["plafond"] - phase["consomme"]
print(f"Total prévisionnel : {total} crédits · phase : {phase['consomme']} consommés sur {phase['plafond']} (reste {reste_phase})")

if eng == "elevenlabs" and any(x["est"] is None for x in plan):
    sys.exit("Coût prévisionnel inconnu (tarif ou multiplicateur absent) : arrêt.")
if total > reste_phase:
    print("Le total dépasse le reste du plafond : génération dans l'ordre, tant que le budget le permet.")
if eng == "google" and sum(len(x["text"]) for x in plan if not x["reuse"]) > GOOGLE_MAX_CHARS:
    sys.exit("Plus de 25 000 caractères Google : arrêt.")

if eng == "elevenlabs":
    try:
        s = el_subscription(); dispo = (s["limit"] or 0) - (s["used"] or 0)
        print(f"Solde suffisant pour cette demande (marge {MARGE} comprise) : {'oui' if dispo >= total + MARGE else 'non'}")
    except EngineError as e:
        sys.exit(f"Lecture du solde impossible : {e}")
    if dispo < MARGE + min([x["est"] for x in plan if x["est"]] or [0]): sys.exit("Solde insuffisant : arrêt.")

if MODE != "generer":
    print("Mode estimer : aucune synthèse lancée."); sys.exit(0)

dem = CMD.get("demande")
if dem in phase["demandes"]:
    sys.exit(f"La demande {dem} a déjà été exécutée : rien n'est relancé.")
phase["demandes"].append(dem)

def save():
    PHASE_F.write_text(json.dumps(phase, ensure_ascii=False, indent=1))
    NARR_F.write_text(json.dumps(narr, ensure_ascii=False, indent=1, sort_keys=True))

restants = []
SET = {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True, "speed": 1.0}
SET.update(CMD.get("reglages") or {})
try:
    for x in plan:
        if x["reuse"]: continue
        parts, cost = [], 0
        if eng == "elevenlabs":
            reste = phase["plafond"] - phase["consomme"]; cs = decoupe(x["text"], reste)
            if cs is None:
                print(f"  — {x['art']}/{x['fmt']} : ne tient pas dans le reste du plafond ({reste}), non généré"); restants.append(x); continue
            for c in cs:
                if phase["plafond"] - phase["consomme"] < len(c) * pire: raise EngineError("plafond de phase atteint (pire cas)")
                b = el_subscription()
                if (b["limit"] or 0) - (b["used"] or 0) < len(c) * pire + MARGE: raise EngineError("solde insuffisant")
                mp3, annonce = el_tts(c, voix["voice_id"], modele, SET, "fr")
                a = el_subscription(); delta = (a["used"] or 0) - (b["used"] or 0)
                reel = annonce if annonce is not None else (delta if delta > 0 else None)
                if reel is None:
                    phase["consomme"] += round(len(c) * mult * tarif); save()
                    raise EngineError("coût réel inconnu : arrêt (estimation comptée par prudence)")
                phase["consomme"] += reel; cost += reel; parts.append(mp3); save()
                if reel > len(c) * ratio * 1.1 + 5: raise EngineError(f"coût réel anormal ({reel})")
        else:
            for c in chunks(x["text"], 4000):
                parts.append(google_tts(markup=c, voice=voix["voice"]) if "[pause" in c else google_tts(text=c, voice=voix["voice"]))
        mp3 = joindre(parts); name = f"{x['fmt']}-{x['hash']}.mp3"
        (root / "site/audio" / x["art"]).mkdir(parents=True, exist_ok=True)
        (root / "site/audio" / x["art"] / name).write_bytes(mp3)
        kbps = 128000 if eng == "elevenlabs" else 32000
        narr.setdefault(x["art"], {}).setdefault(voix["id"], {})[x["fmt"]] = {
            "file": name, "hash": x["hash"], "voice": voix["name"].split(" - ")[0].split(" – ")[0].strip(),
            "engine": eng, "model": modele, "chars": len(x["text"]), "bytes": len(mp3),
            "seconds": round(len(mp3) * 8 / kbps), "credits": cost}
        phase["fichiers"].append({"demande": dem, "voix": voix["id"], "modele": modele, "fichier": f"{x['art']}/{name}", "chars": len(x["text"]), "credits": cost})
        save()
        print(f"  ✓ {x['art']}/{name} · {cost} crédits")
except EngineError as e:
    save(); print(f"Arrêt : {e}")
    for x in plan:
        if not x["reuse"] and not (root / "site/audio" / x["art"] / f"{x['fmt']}-{x['hash']}.mp3").exists(): print(f"  reste à faire : {x['art']}/{x['fmt']}")
    sys.exit(1)
save()
print(f"Terminé. Phase : {phase['consomme']} crédits consommés sur {phase['plafond']}.")
for x in restants: print(f"  reste à faire : {x['art']}/{x['fmt']}")
