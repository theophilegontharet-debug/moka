"""Banc d'essai comparatif Google Chirp 3 HD / ElevenLabs.

    MODE=diagnostic python3 tools/audio/banc.py   # gratuit : modèles, coûts, voix, permissions, solde
    MODE=generer    python3 tools/audio/banc.py   # payant : seulement après accord explicite

Règles :
- plafond total de la campagne : budget_credits (audio/tests/banc.json), registre dans site/audio/banc/manifest.json ;
- avant chaque génération ElevenLabs : solde vérifié (reste ≥ coût estimé + marge) ;
- après chaque génération : coût réel relevé ; s'il est inconnu ou plus élevé que prévu, arrêt ;
- un fichier déjà produit pour le même texte n'est jamais régénéré ;
- les journaux ne montrent ni la clé ni le solde exact (dépôt public).
"""
import os, sys, json, hashlib, html, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from engines import (EngineError, APOS, google_tts, el_models, el_subscription, el_my_voices,
                     el_find_shared, el_add_shared, el_tts)

root = pathlib.Path(__file__).resolve().parents[2]
CFG = json.loads((root / "audio/tests/banc.json").read_text())
OUT = root / "site/audio/banc"; OUT.mkdir(parents=True, exist_ok=True)
MF = OUT / "manifest.json"
manifest = json.loads(MF.read_text()) if MF.exists() else {"credits_depenses": 0, "fichiers": {}}
MODE = os.environ.get("MODE", "diagnostic")
BUDGET, MARGE = CFG["budget_credits"], CFG["marge_credits"]
problems, notes = [], []
say = lambda *a: print(*a, flush=True)

# ---------- plan des rendus ----------
def renditions():
    for p in CFG["passages"]:
        for m in CFG["moteurs"]:
            if m.get("passages") and p["id"] not in m["passages"]: continue   # voix limitée à certains passages
            yield p, m, "commun", p["commun"]
            if m["engine"] == "google" and p.get("chirp"):
                yield p, m, "chirp", p["chirp"]["text"]
            if m["engine"] == "elevenlabs" and p.get("eleven") and m.get("variantes", True) and m["model"] != "eleven_multilingual_v2":
                yield p, m, "eleven", p["eleven"]["text"]
def h(m, text): return hashlib.sha256(json.dumps([m, APOS(text), CFG["reglages_elevenlabs"]], sort_keys=True).encode()).hexdigest()[:10]
def fname(p, m, var, text): return f"{p['id']}-{m['id']}-{var}-{h(m, text)}.mp3"

# ---------- diagnostic (gratuit) ----------
say("== Diagnostic (aucune génération) ==")
el_needed = [m for m in CFG["moteurs"] if m["engine"] == "elevenlabs"]
mult = {}
try:
    models = {x["model_id"]: x for x in el_models()}
    for mid in sorted({m["model"] for m in el_needed}):
        x = models.get(mid)
        if not x:
            problems.append(f"modèle {mid} non accessible avec cette clé"); say(f"✗ {mid} : absent de la liste des modèles"); continue
        langs = {l.get("language_id") for l in x.get("languages", [])}
        rate = (x.get("model_rates") or {}).get("character_cost_multiplier")
        mult[mid] = rate
        say(f"✓ {mid} ({x.get('name')}) : synthèse={x.get('can_do_text_to_speech')} français={'fr' in langs} "
            f"multiplicateur de coût={rate} limite/requête={x.get('max_characters_request_subscribed_user')}")
        if not x.get("can_do_text_to_speech"): problems.append(f"{mid} ne fait pas de synthèse vocale")
        if "fr" not in langs: problems.append(f"{mid} : français non listé")
        if rate is None: problems.append(f"{mid} : coût par caractère non communiqué par l'API (consommation incertaine)")
except EngineError as e:
    problems.append(f"liste des modèles inaccessible ({e})"); say("✗ modèles :", e)

sub = None
try:
    sub = el_subscription(); say(f"✓ lecture du solde autorisée (formule {sub.get('tier')}, statut {sub.get('status')})")
except EngineError as e:
    problems.append("la clé ne permet pas de lire le solde (permission « User : read » absente) : solde invérifiable"); say("✗ solde :", e)

mine = {}
try:
    mine = {v["voice_id"]: v for v in el_my_voices()}; say(f"✓ lecture des voix du compte autorisée ({len(mine)} voix)")
except EngineError as e:
    problems.append(f"lecture des voix impossible ({e})"); say("✗ voix du compte :", e)

voice_rate, to_add = {}, []
for vid, name in sorted({(m["voice_id"], m["voice"]) for m in el_needed}):
    acct = mine.get(vid) or next((v for v in mine.values() if v.get("category") != "premade"
                                  and (v.get("name", "").startswith(name) or v.get("name", "") == f"Moka {name}")), None)
    if acct:
        for m in CFG["moteurs"]:
            if m.get("voice_id") == vid: m["voice_id_compte"] = acct["voice_id"]
        voice_rate[vid] = None; say(f"✓ voix {name} : déjà dans le compte, aucun ajout nécessaire"); continue
    try:
        sv = el_find_shared(vid, name)
    except EngineError as e:
        sv = None; say(f"✗ voix {name} : recherche impossible ({e})")
    if not sv:
        problems.append(f"voix {name} introuvable dans la bibliothèque"); continue
    r = sv.get("rate"); voice_rate[vid] = r if isinstance(r, (int, float)) else 1
    to_add.append((sv["public_owner_id"], vid, name))
    say(f"✓ voix {name} : trouvée dans la bibliothèque (à ajouter au compte, sans crédits) ; tarif={r if r is not None else 'standard'} "
        f"utilisateurs gratuits={sv.get('free_users_allowed')}")

plan, est_total, n_google = [], 0, 0
for p, m, var, text in renditions():
    f = fname(p, m, var, text)
    done = f in manifest["fichiers"] and (OUT / f).exists()
    if m["engine"] == "google":
        n_google += 0 if done else 1; plan.append((p, m, var, text, f, 0, done)); continue
    est = 0 if done else round(len(APOS(text)) * (mult.get(m["model"]) or 1) * (voice_rate.get(m["voice_id"]) or m.get("tarif", 1)))
    est_total += est; plan.append((p, m, var, text, f, est, done))
deja = manifest["credits_depenses"]
say(f"Plan : {sum(1 for x in plan if x[1]['engine']=='elevenlabs' and not x[6])} rendus ElevenLabs à produire, "
    f"{n_google} rendus Google (quota gratuit). Estimation ElevenLabs : {est_total} crédits ; déjà dépensés dans la campagne : {deja} ; plafond : {BUDGET}.")
if deja + est_total > BUDGET: problems.append(f"estimation ({deja + est_total}) au-delà du plafond de campagne ({BUDGET})")
if sub and sub.get("limit") is not None and sub.get("used") is not None:
    ok = (sub["limit"] - sub["used"]) >= est_total + MARGE
    say(f"{'✓' if ok else '✗'} solde suffisant pour la campagne et la marge de {MARGE} crédits : {'oui' if ok else 'non'}")
    if not ok: problems.append("solde insuffisant pour la campagne avec la marge de sécurité")

if to_add:
    say(f"! {len(to_add)} voix à ajouter au compte : il faut la permission « Voix : écriture » sur la clé, "
        "ou un ajout manuel depuis la bibliothèque ElevenLabs (non vérifiable sans action).")
if problems:
    say("== BLOQUÉ =="); [say(" -", x) for x in problems]
else:
    say("== PRÊT : aucune génération n'a été faite ==")
if MODE != "generer":
    sys.exit(0)
if problems:
    sys.exit("Génération refusée : diagnostic non concluant.")

# ---------- génération (payante, après accord) ----------
say("== Génération ==")
for owner, vid, name in to_add:
    try:
        new = el_add_shared(owner, vid, f"Moka {name}")
        for m in CFG["moteurs"]:
            if m.get("voice_id") == vid: m["voice_id_compte"] = new
        say(f"✓ voix {name} ajoutée au compte")
    except EngineError as e:
        sys.exit(f"Arrêt : impossible d'ajouter la voix {name} ({e})")

def save(f, audio, credits, p, m, var):
    (OUT / f).write_bytes(audio)
    manifest["fichiers"][f] = {"passage": p["id"], "moteur": m["id"], "variante": var, "credits": credits}
    MF.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))

for p, m, var, text, f, est, done in plan:
    if done: continue
    if m["engine"] == "google":
        try: save(f, google_tts(text=text, voice=m["voice"]), 0, p, m, var); say("✓", f)
        except EngineError as e: say("✗ Google", f, e)
        continue
    if manifest["credits_depenses"] + est > BUDGET:
        sys.exit(f"Arrêt : le plafond de campagne serait dépassé ({manifest['credits_depenses']} + {est} > {BUDGET}).")
    before = el_subscription()
    if before["limit"] - before["used"] < est + MARGE:
        sys.exit("Arrêt : solde trop bas pour continuer avec la marge de sécurité.")
    try:
        audio, cost = el_tts(text, m.get("voice_id_compte") or m["voice_id"], m["model"], CFG["reglages_elevenlabs"])
    except EngineError as e:
        sys.exit(f"Arrêt : erreur ElevenLabs sur {f} ({e}). Aucune autre génération lancée.")
    after = el_subscription(); delta = after["used"] - before["used"]
    real = cost if cost is not None else (delta if delta > 0 else None)
    if real is None:
        save(f, audio, est, p, m, var); manifest["credits_depenses"] += est; MF.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
        sys.exit(f"Arrêt : coût réel inconnu pour {f} (consommation incertaine).")
    save(f, audio, real, p, m, var); manifest["credits_depenses"] += real; MF.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    say(f"✓ {f} : {real} crédits (estimés {est})")
    if real > est * 1.25 + 20:
        sys.exit(f"Arrêt : coût réel supérieur à l'estimation ({real} > {est}).")
    time.sleep(1)

# ---------- page d'écoute ----------
labels = {m["id"]: m["label"] for m in CFG["moteurs"]}
secs = []
for p in CFG["passages"]:
    rows = []
    for var, title, text in [("commun", "Texte commun à tous les moteurs", p["commun"])] + \
            ([("chirp", p["chirp"]["label"], p["chirp"]["text"])] if p.get("chirp") else []) + \
            ([("eleven", p["eleven"]["label"], p["eleven"]["text"])] if p.get("eleven") else []):
        lines = []
        for m in CFG["moteurs"]:
            f = fname(p, m, var, text)
            if f in manifest["fichiers"] and (OUT / f).exists():
                lines.append(f'<div class="r"><b>{html.escape(labels[m["id"]])}</b><audio controls preload="none" src="{f}"></audio></div>')
        if lines:
            rows.append(f'<div class="var"><h3>{html.escape(title)}</h3><p>{html.escape(APOS(text))}</p>{"".join(lines)}</div>')
    secs.append(f'<section><h2>{html.escape(p["theme"])}</h2>{"".join(rows)}</section>')
(OUT / "index.html").write_text(f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Moka · banc d'essai audio</title>
<style>body{{font-family:-apple-system,system-ui,sans-serif;background:#FDF9F4;color:#33241B;max-width:680px;margin:0 auto;padding:24px 18px 60px;line-height:1.45}}
h1{{color:#4A2C1F;font-size:26px}} h2{{color:#4A2C1F;font-size:19px;margin:0 0 8px}} h3{{font-size:14px;color:#8B5A3C;margin:14px 0 4px}}
section{{background:#fff;border:1px solid #EADBCB;border-radius:16px;padding:16px;margin:16px 0}} p{{margin:0 0 8px;color:#7A6455;font-size:14px}}
.r{{padding:6px 0;border-top:1px solid #F1E5D8}} .r b{{font-size:13px}} audio{{width:100%;margin-top:4px}}</style></head>
<body><p><a href="../../" style="color:#8B5A3C">← Retour à Moka</a></p><h1>Banc d'essai audio</h1>
<p>Mêmes textes, plusieurs moteurs. Les variantes adaptées à un moteur sont signalées.</p>{"".join(secs)}</body></html>""")
say(f"Terminé. Crédits ElevenLabs dépensés dans la campagne : {manifest['credits_depenses']} / {BUDGET}.")
