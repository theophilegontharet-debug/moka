import json
m = json.load(open("meta.json"))
A = {  # key: (article_id, version, asset, kind, caption, alt)
 "apple": ("apple-reduit-le-budget-ia-de-ses-employes-20261105", 2, "6347fe776742690e27e06747f1f2b23e", "photo", "Apple Park, le siège d'Apple à Cupertino, en 2018", "Vue aérienne du bâtiment circulaire d'Apple Park"),
 "revolut": ("revolut-115-milliards", 7, "8121fec3499f3f37dab9c3a012532979", "photo", "une carte bancaire Revolut Premium", "Carte Revolut bleu nuit, logo Visa Infinite"),
 "qualcomm": ("qualcomm-fournira-les-equipements-5g-du-reseau-terrestre-de--20261106", 1, "51fd616cdc9402d60a6de3b99f8b2805", "photo", "le siège de Qualcomm à San Diego", "Immeuble de bureaux vitré du siège de Qualcomm"),
 "airbnb": ("airbnb-muscle-un-petit-modele-d-ia-pour-egaler-les-geants-10-20261105", 3, "004dc70326740fecb5dc5e95d06ac8a5", "photo", "le siège d'Airbnb à San Francisco, en 2018", "Atrium intérieur du siège d'Airbnb"),
 "apollo": ("apollo-investit-350-millions-de-dollars-pour-rendre-le-priva-20261106", 1, "dbfe8d3ff787904eb2ff21c340bde5fc", "photo", "le Solow Building, au 9 West 57th Street à New York, où Apollo a son siège, en 2012", "Façade sombre et incurvée du Solow Building à New York"),
 "ashburn": ("les-mesures-locales-contre-les-data-centers-gagnent-presque--20261105", 2, "4cd5a378e93c1e9bfbd04222fefcc9f3", "contexte", "data centers à Ashburn, dans le comté de Loudoun (Virginie), en 2025", "Vue aérienne de grands entrepôts de data centers"),
 "texas": ("texas-un-moratoire-sur-les-data-centers-menace-13-3-gw-de-pr-20261106", 1, "8bcdff8948aaf8ef8e46d350c6c0259c", "contexte", "le Capitole du Texas à Austin, siège du Parlement de l'État", "Capitole du Texas, coupole et façade"),
 "capitol": ("midterms-ia", 2, "479970fc35d0fdf653d13b97968596cc", "photo", "le Capitole des États-Unis, siège du Congrès, à Washington", "Façade ouest du Capitole des États-Unis"),
 "lagos": ("nigeria-en-tete", 2, "8e8e1b2cf5f6b3258ff6377080467379", "contexte", "Lagos, vue depuis la marina, en 2024", "Immeubles de Lagos au bord de l'eau"),
 "solar": ("energie-recule", 2, "645a95dd47519414c67586b0e1f8c857", "contexte", "une mini-centrale solaire dans l'État de Bayelsa, au Nigeria, en 2020", "Panneaux solaires d'un mini-réseau au milieu de la végétation"),
 "kariakoo": ("afrique-octobre-2026", 5, "b283c9cdad7f495d0d5f8da1cc3e1065", "contexte", "étals de fruits et légumes au marché de Kariakoo, à Dar es Salaam, en 2012", "Marché couvert de parasols, étals de fruits"),
 "openai": ("les-gros-cheques-de-l-ia-se-font-plus-rares-openai-n-a-leve--20261105", 3, "d24d3d349a75ddd6833b02f89ccdb442", "photo", "le 1515 Third Street à San Francisco, siège d'OpenAI, en 2025", "Immeuble de bureaux vitré à San Francisco"),
 "googledc": ("les-elections-americaines-menacent-la-course-aux-data-center-20261106", 2, "994deb334921cda602644ef12585b271", "contexte", "un data center de Google à Council Bluffs (Iowa), en 2017", "Vue aérienne d'un data center au coucher du soleil"),
}
def lic(c):
    l = c["lic"]
    if l == "CC0": return "CC0 1.0 (domaine public)", "https://creativecommons.org/publicdomain/zero/1.0/deed.fr", "Aucune obligation ; crédit indiqué par courtoisie."
    if l == "Public domain": return "Domaine public", c["page"], "Aucune obligation selon la page Commons ; crédit indiqué par courtoisie."
    url = c["lic_url"].replace("http://", "https://").rstrip("/") + "/deed.fr"
    sa = " La version modifiée reste diffusée sous la même licence." if "SA" in l else ""
    return l, url, f"Citer l'auteur, la licence et la source, et indiquer les modifications.{sa}"
ops = []
for k, (aid, v, asset, kind, cap, alt) in A.items():
    c = m[k]; L, LU, att = lic(c)
    ops.append({"op": "update", "path": "articles/" + aid, "ifVersion": v, "data": {"image": {
        "asset": asset, "kind": kind, "subject": "sujet" if kind == "photo" else "contexte", "caption": cap, "alt": alt,
        "title": c["title"][5:].rsplit(".", 1)[0], "credit": c["artist"].split(" from ")[0].replace(" (user:dllu)", ""),
        "author": c["artist"], "license": L, "license_url": LU, "attribution": att,
        "modifications": "recadrée et redimensionnée" if c["cropped"] else "redimensionnée",
        "source_url": c["page"], "source_site": "Wikimedia Commons",
        "width": c["out_w"], "height": c["out_h"], "added_at": "2026-11-07T23:30:00Z"}}})
json.dump(ops, open("ops.json", "w"), ensure_ascii=False)
for o in ops: i=o["data"]["image"]; print(o["path"][9:40], "|", i["credit"], "|", i["license"], "|", i["modifications"])
