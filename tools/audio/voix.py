"""Catalogue des narrateurs de Moka (gratuit : aucune génération).

Lit les voix enregistrées dans le compte ElevenLabs (identifiants exacts) et écrit site/audio/voix.json,
avec Google Chirp 3 HD / Aoede en alternative. Les voix par défaut d'ElevenLabs (« premade », anglaises)
sont ignorées. Le tarif d'une voix de la bibliothèque (×1, ×2…) est relevé quand l'API le donne.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from engines import EngineError, el_my_voices, el_find_shared, el_models

root = pathlib.Path(__file__).resolve().parents[2]
OUT = root / "site/audio/voix.json"
PREFERE = "Patrick"          # narrateur initial souhaité

cat = [{"id": "google:Aoede", "engine": "google", "voice": "fr-FR-Chirp3-HD-Aoede", "name": "Aoede",
        "label": "Aoede · Google", "gender": "female", "models": ["chirp3-hd"], "rate": 0}]
models = {}
try:
    models = {m["model_id"]: m for m in el_models()}
except EngineError as e:
    print("modèles :", e)
try:
    voices = el_my_voices()
except EngineError as e:
    sys.exit(f"Lecture des voix impossible : {e}")

for v in voices:
    if v.get("category") == "premade":
        continue
    lab = {k.lower(): str(val).lower() for k, val in (v.get("labels") or {}).items()}
    gender = lab.get("gender") or ("female" if "female" in json.dumps(lab) else "male" if "male" in json.dumps(lab) else None)
    rate = (v.get("sharing") or {}).get("rate")
    if rate is None:
        try:
            short = v["name"].split(" - ")[0].split(" – ")[0].strip()
            sv = el_find_shared(v["voice_id"], short)
            if sv: rate = sv.get("rate")
        except EngineError:
            pass
    hq = v.get("high_quality_base_model_ids") or []
    cat.append({"id": f"el:{v['voice_id']}", "engine": "elevenlabs", "voice_id": v["voice_id"], "name": v["name"],
                "label": f"{v['name'].split(' - ')[0].split(' – ')[0].strip()} · ElevenLabs", "gender": gender,
                "category": v.get("category"), "rate": rate, "optimise_pour": hq,
                "v4": ("eleven_v4" in hq) if hq else None})

default = next((c["id"] for c in cat if c["engine"] == "elevenlabs" and c["name"].lower().startswith(PREFERE.lower())), "google:Aoede")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"defaut": default, "voix": cat,
                           "modeles": {k: (models.get(k, {}).get("model_rates") or {}).get("character_cost_multiplier")
                                       for k in ("eleven_v4", "eleven_multilingual_v2")}}, ensure_ascii=False, indent=1))
print(f"{len(cat) - 1} voix ElevenLabs du compte + Aoede. Narrateur par défaut : {default}")
for c in cat:
    print(f"  {c['id']:32} {c['label']:40} genre={c['gender']} tarif={c['rate']} v4={c.get('v4')}")
