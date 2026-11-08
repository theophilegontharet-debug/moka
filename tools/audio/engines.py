"""Moteurs de synthèse de Moka Audio : Google Chirp 3 HD et ElevenLabs.

Utilisé uniquement côté GitHub Actions. Les clés viennent des secrets (variables d'environnement),
partent en en-tête HTTP, ne sont jamais écrites ni affichées. Aucun appel depuis le navigateur.
"""
import os, json, base64, urllib.request, urllib.parse

APOS = lambda t: t.replace("'", "’")      # règle commune : apostrophes typographiques


class EngineError(RuntimeError):
    pass


def _req(url, body=None, headers=None, method=None, timeout=180):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"),
                                 headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        # le corps d'erreur ne contient pas la clé ; on le tronque quand même
        raise EngineError(f"HTTP {e.code} : {e.read()[:240].decode(errors='replace')}") from None
    except urllib.error.URLError as e:
        raise EngineError(f"réseau : {e.reason}") from None


# ---------------- Google Chirp 3 HD ----------------
def google_tts(text=None, markup=None, voice="fr-FR-Chirp3-HD-Aoede", rate=None, pron=None):
    key = os.environ.get("GOOGLE_TTS_API_KEY") or ""
    if not key: raise EngineError("secret GOOGLE_TTS_API_KEY absent")
    inp = {"markup": APOS(markup)} if markup else {"text": APOS(text)}
    if pron:
        inp["customPronunciations"] = {"pronunciations": [
            {"phrase": APOS(p), "phoneticEncoding": "PHONETIC_ENCODING_IPA", "pronunciation": ipa} for p, ipa in pron]}
    cfg = {"audioEncoding": "MP3"}
    if rate: cfg["speakingRate"] = rate
    raw, _ = _req("https://texttospeech.googleapis.com/v1/text:synthesize",
                  {"input": inp, "voice": {"languageCode": "fr-FR", "name": voice}, "audioConfig": cfg},
                  {"X-Goog-Api-Key": key})
    return base64.b64decode(json.loads(raw)["audioContent"])


# ---------------- ElevenLabs ----------------
EL = "https://api.elevenlabs.io"

def _elk():
    key = os.environ.get("ELEVENLABS_API_KEY") or ""
    if not key: raise EngineError("secret ELEVENLABS_API_KEY absent")
    return {"xi-api-key": key}

def el_models():
    """Modèles accessibles avec la clé (gratuit)."""
    raw, _ = _req(f"{EL}/v1/models", headers=_elk())
    return json.loads(raw)

def el_subscription():
    """Solde de crédits (gratuit). Lève EngineError si la clé n'a pas la permission de lecture du compte."""
    raw, _ = _req(f"{EL}/v1/user/subscription", headers=_elk())
    j = json.loads(raw)
    return {"used": j.get("character_count"), "limit": j.get("character_limit"),
            "reset": j.get("next_character_count_reset_unix"), "tier": j.get("tier"),
            "can_extend": j.get("can_extend_character_limit"), "status": j.get("status")}

def el_my_voices():
    raw, _ = _req(f"{EL}/v1/voices", headers=_elk())
    return json.loads(raw).get("voices", [])

def el_find_shared(voice_id, name):
    """Retrouve une voix de la bibliothèque (gratuit) pour connaître son propriétaire et son tarif éventuel."""
    q = urllib.parse.urlencode({"search": name, "language": "fr", "page_size": 50})
    raw, _ = _req(f"{EL}/v1/shared-voices?{q}", headers=_elk())
    for v in json.loads(raw).get("voices", []):
        if v.get("voice_id") == voice_id:
            return v
    return None

def el_add_shared(public_owner_id, voice_id, new_name):
    """Ajoute une voix de la bibliothèque au compte (ne consomme pas de crédits, occupe un emplacement de voix)."""
    raw, _ = _req(f"{EL}/v1/voices/add/{public_owner_id}/{voice_id}", {"new_name": new_name}, _elk())
    return json.loads(raw)["voice_id"]

def el_tts(text, voice_id, model, settings=None, language_code=None):
    """Synthèse ElevenLabs. Renvoie (mp3, coût annoncé par l'API ou None)."""
    body = {"text": APOS(text), "model_id": model}
    if language_code: body["language_code"] = language_code
    if settings: body["voice_settings"] = settings
    audio, hdr = _req(f"{EL}/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128", body, _elk())
    cost = hdr.get("character-cost") or hdr.get("x-character-count")
    return audio, (int(cost) if cost and str(cost).isdigit() else None)
