# Moka — édition du 7 novembre 2026, rédigée à partir des newsletters du libellé Moka/Newsletters.
# Chaque chiffre provient d'une source citée. Le "contexte Moka" (connaissances générales) est séparé et signalé.
import json

# Liens Gmail retirés de la version publique du dépôt.
S = {
  "bd_nov5":   {"name": "Africa: The Big Deal", "date": "2026-11-05", "web": "https://thebigdeal.substack.com/p/october26", "web_label": "Lire sur thebigdeal.substack.com"},
  "bd_oct20":  {"name": "Africa: The Big Deal", "date": "2026-10-20", "web": "https://thebigdeal.substack.com/p/q32026c", "web_label": "Lire sur thebigdeal.substack.com"},
  "bd_oct13":  {"name": "Africa: The Big Deal", "date": "2026-10-13", "web": "https://thebigdeal.substack.com/p/q32026b", "web_label": "Lire sur thebigdeal.substack.com"},
  "ido":       {"name": "Ido Sum", "date": "2026-09-29", "web": "https://idosum.substack.com/p/adolescence-a-different-take-on-african", "web_label": "Lire sur idosum.substack.com"},
  "tldrfin_revolut": {"name": "TLDR Fintech", "via": "TechCrunch", "date": "2026-11-05", "web": "https://techcrunch.com/2026/11/04/revoluts-valuation-jumps-53-to-115b-in-new-share-sale-as-it-prepares-to-launch-us-bank/", "web_label": "Article TechCrunch"},
  "tldrfin_sequoia": {"name": "TLDR Fintech", "via": "TechCrunch", "date": "2026-11-05", "web": "https://techcrunch.com/2026/11/04/sequoia-hits-rewind-undoing-20-years-of-expansion/", "web_label": "Article TechCrunch"},
  "tldrfin_pe": {"name": "TLDR Fintech", "via": "a16z", "date": "2026-11-05", "web": "https://a16z.com/is-private-equity-cooked", "web_label": "Essai a16z « Is private equity cooked? »"},
  "tldrfin_credit": {"name": "TLDR Fintech", "date": "2026-11-05", },
  "tldrfin_anthropic": {"name": "TLDR Fintech", "via": "CNBC", "date": "2026-11-05", "web": "https://www.cnbc.com/2026/11/02/anthropic-ant-s-1-quarter-financials.html", "web_label": "Article CNBC"},
  "tldr_anthropic": {"name": "TLDR", "via": "Wall Street Journal", "date": "2026-11-06", "web": "https://www.wsj.com/finance/major-investors-are-skeptical-anthropic-ipo-can-achieve-1-5-trillion-valuation-ca965d8b", "web_label": "Article WSJ (abonnés)"},
  "tldr_election": {"name": "TLDR", "via": "Wall Street Journal", "date": "2026-11-06", "web": "https://www.wsj.com/tech/ai/the-election-day-revolt-that-threatens-americas-ai-boom-03a53b52", "web_label": "Article WSJ (abonnés)"},
  "sifted_nov5": {"name": "Sifted Daily", "date": "2026-11-05", },
  "sifted_nov6": {"name": "Sifted Daily", "date": "2026-11-06", },
}
def src(*keys): return [S[k] for k in keys]

A = []

A.append(dict(
  id="afrique-octobre-2026", category="afrique-vc", kind="actu", score=98,
  title="Octobre en Afrique : moins d'argent, mais le Maroc et la Tanzanie raflent les plus gros tickets",
  dek="34 startups ont levé 183 M$ en octobre. Les deux plus gros tours, 40 M$ chacun, sont allés à des pays qu'on voit rarement en tête.",
  brief="Mois calme pour la tech africaine : 183 M$ levés, nettement sous la moyenne. Mais pour la première fois depuis longtemps, plus de la moitié de l'argent est partie hors du Nigeria, du Kenya, de l'Égypte et de l'Afrique du Sud.",
  event_label="Octobre 2026", event_date="2026-10-31", published_date="2026-11-05",
  figures=[
    {"v":"183 M$","l":"levés en octobre","n":"−24 % vs septembre, −58 % sur un an"},
    {"v":"34","l":"startups financées (100 k$ et plus)","n":"moyenne de 43 par mois sur un an"},
    {"v":"2 × 40 M$","l":"ABA Life (Maroc) et East Africa Foods (Tanzanie)"},
    {"v":"46 %","l":"part des « Big Four »","n":"plus bas depuis novembre 2022"},
  ],
  body=[
    {"p":"Octobre a été un mois creux. Selon The Big Deal, qui recense chaque tour de 100 000 $ ou plus sur le continent, 34 startups ont annoncé 183 M$ au total. C'est 24 % de moins qu'en septembre (241 M$) et 29 % sous la moyenne des douze derniers mois. La comparaison avec octobre 2025 est encore plus dure, −58 %, mais ce mois-là avait été dopé par Spiro (100 M$) et Moniepoint (90 M$)."},
    {"p":"L'intérêt du mois est ailleurs : la géographie. D'habitude, le Nigeria, le Kenya, l'Égypte et l'Afrique du Sud captent l'essentiel des montants. En octobre, ils n'en ont pris que 46 %. Les deux plus gros tours, 40 M$ chacun, sont allés à ABA Life, une entreprise de santé marocaine financée par Admaius Capital Partners, et à East Africa Foods, une agritech tanzanienne dont la Série B réunit notamment InfraCo Africa, Oikocredit et FMO."},
    {"h":"Le reste du mois, surtout de la dette","p":"Derrière ces deux tours en capital, une série d'opérations en dette : une émission obligataire de 17 M$ pour ValU en Égypte, 13 M$ pour Afreenergy Solar au Sénégal, un prêt de 11 M$ de Finnfund à Bisedge et un prêt de 10 M$ de la BERD à Beacon Power Services, ces deux derniers au Nigeria. Au total, l'equity pèse 110 M$ (60 %), la dette 71 M$ (39 %) et les subventions environ 2 M$. La climate tech a capté 55 % des fonds."},
    {"p":"En valeur, le Nigeria reste premier (42 M$ pour 9 startups, surtout de la dette dans l'énergie et la mobilité), mais le Maroc et la Tanzanie suivent de très près avec 40 M$ chacun, devant l'Égypte (19 M$) et le Sénégal (13 M$). Les Big Four comptent quand même 26 des 34 startups financées."},
  ],
  why="Un mois ne fait pas une tendance, et l'auteur de la newsletter le dit lui-même. Mais voir deux marchés hors Big Four à égalité avec le Nigeria vaut d'être suivi, d'autant que The Big Deal annonce une analyse sur les « prochains » marchés à surveiller.",
  explain=[
    {"q":"Qui sont les « Big Four » ?","a":"Le Nigeria, le Kenya, l'Égypte et l'Afrique du Sud. Ce sont les quatre pays qui concentrent historiquement la grande majorité des financements de startups en Afrique."},
    {"q":"East Africa Foods, que sait-on ?","a":"La source dit seulement : agritech tanzanienne, Série B de 40 M$, avec InfraCo Africa, Oikocredit et FMO parmi les investisseurs. Ses produits, ses clients et son modèle économique ne sont pas décrits."},
    {"q":"ABA Life, que sait-on ?","a":"Entreprise de santé basée au Maroc, 40 M$ levés auprès d'Admaius Capital Partners. Son activité précise n'est pas détaillée dans la newsletter."},
  ],
  unknowns=["Valorisations d'ABA Life et d'East Africa Foods : non communiquées.","Usage des fonds des deux tours de 40 M$ : non précisé."],
  verification="rapporte", sources=src("bd_nov5"), related=["afrique-bilan-2026","exits-afrique-octobre"],
  tags=["Maroc","Tanzanie","Nigeria","Égypte","Sénégal"], entities=["ABA Life","East Africa Foods","Admaius Capital Partners","InfraCo Africa","Oikocredit","FMO","ValU","Afreenergy Solar","Bisedge","Finnfund","Beacon Power Services","BERD"],
  cover={"big":"183 M$","small":"octobre"}
))

A.append(dict(
  id="exits-afrique-octobre", category="afrique-vc", kind="actu", score=95,
  title="MNT-Halan entre en Bourse, OPay freine net : un mois de sorties en Afrique",
  dek="Quatre exits en octobre, dont l'introduction en Bourse de la fintech égyptienne MNT-Halan. La cotation new-yorkaise d'OPay, elle, a été stoppée à la dernière minute.",
  brief="MNT-Halan est cotée au Caire et pèse environ 1,4 Md$. OPay, qui préparait une cotation à New York, a interrompu l'opération au dernier moment. Depuis janvier, 38 sorties ont été recensées.",
  event_label="Octobre 2026", event_date="2026-10-31", published_date="2026-11-05",
  figures=[
    {"v":"≈ 1,4 Md$","l":"capitalisation de MNT-Halan","n":"au moment où The Big Deal écrit, le 5 novembre"},
    {"v":"4","l":"exits en octobre"},
    {"v":"38","l":"exits depuis janvier","n":"42 sur la même période en 2025"},
  ],
  body=[
    {"p":"La grosse sortie du mois, c'est MNT-Halan. La fintech égyptienne s'est introduite sur l'Egyptian Exchange, et sa capitalisation tournait autour de 1,4 Md$ au moment où The Big Deal publiait son bilan. Mi-octobre, la même newsletter décrivait une opération sursouscrite, autrement dit une demande d'actions supérieure à l'offre."},
    {"p":"Trois autres opérations complètent le mois : le rachat de PeacePay par HealthPay en Égypte, la finalisation de l'acquisition de 888Africa par GiG Software au Mozambique, et la vente de LekkeSlaap à des investisseurs sud-africains."},
    {"h":"OPay, l'histoire à suivre","p":"OPay devait être la deuxième grande cotation de la saison, à New York cette fois. Elle a été stoppée à la dernière minute. The Big Deal parle d'une histoire « en développement », sans donner les raisons."},
  ],
  why="Les sorties sont le maillon faible de l'écosystème africain : c'est ce qui permet aux investisseurs de récupérer leur mise et de réinvestir. Une IPO réussie au Caire montre qu'une Bourse locale peut absorber une fintech de cette taille. Le coup d'arrêt d'OPay rappelle que la fenêtre américaine reste fragile.",
  timeline=[
    {"date":"2026-10-13","text":"The Big Deal décrit l'IPO de MNT-Halan sur l'Egyptian Exchange comme en cours et sursouscrite, et annonce l'IPO américaine d'OPay.","source":"Africa: The Big Deal"},
    {"date":"2026-11-05","text":"MNT-Halan est cotée (≈ 1,4 Md$). La cotation d'OPay à New York a été stoppée à la dernière minute.","source":"Africa: The Big Deal"},
  ],
  unknowns=["Raisons de l'arrêt de la cotation d'OPay : non précisées.","Montants des rachats de PeacePay, 888Africa et LekkeSlaap : non communiqués.","Montant levé lors de l'IPO de MNT-Halan : non indiqué dans la newsletter."],
  verification="rapporte", sources=src("bd_nov5","bd_oct13"), related=["ido-sum-le-mur","afrique-bilan-2026"],
  tags=["Égypte","IPO","Exits"], entities=["MNT-Halan","OPay","HealthPay","PeacePay","GiG Software","888Africa","LekkeSlaap","Egyptian Exchange"],
  cover={"big":"IPO","small":"Le Caire"}
))

A.append(dict(
  id="afrique-bilan-2026", category="afrique-vc", kind="actu", score=90,
  title="2,4 milliards levés depuis janvier : la tech africaine recule, mais l'equity tient bon",
  dek="Sur dix mois, les startups africaines ont levé 12 % de moins qu'en 2025. Toute la baisse vient de la dette. Le capital, lui, progresse.",
  brief="Il manque trop d'argent pour égaler 2025 au total. En revanche, 2026 pourrait devenir la meilleure année pour l'equity depuis 2022. Le vrai signal d'alerte : de moins en moins de startups et d'investisseurs.",
  event_label="Janvier–octobre 2026", event_date="2026-10-31", published_date="2026-11-05",
  figures=[
    {"v":"2,4 Md$","l":"levés de janvier à octobre","n":"−12 % vs 2025 (2,7 Md$)"},
    {"v":"1,6 Md$","l":"en equity","n":"+5 % sur un an"},
    {"v":"740 M$","l":"en dette","n":"−33 % (1,1 Md$ en 2025)"},
    {"v":"343","l":"startups financées","n":"438 en 2025, plus bas depuis 2021"},
  ],
  chart={"title":"Janvier–octobre, 2025 vs 2026","a_label":"2025","b_label":"2026","rows":[
    {"label":"Total levé (Md$)","a":2.7,"b":2.4},
    {"label":"Dette (Md$)","a":1.1,"b":0.74},
    {"label":"Startups financées","a":438,"b":343},
    {"label":"Investisseurs actifs","a":442,"b":370}
  ],"note":"Chaque ligne a sa propre échelle. Investisseurs : « 442+ » et « 370+ » dans la source."},
  body=[
    {"p":"Les chiffres cumulés de The Big Deal donnent une image nuancée. 2,4 Md$ levés en dix mois, c'est 12 % de moins qu'à la même période l'an dernier, et l'écart s'est creusé en octobre parce qu'octobre 2025 avait été exceptionnel."},
    {"p":"Mais il faut séparer deux types d'argent. L'equity, c'est-à-dire des investisseurs qui entrent au capital, progresse de 5 % à 1,6 Md$. La dette, qui doit être remboursée et finance souvent des actifs concrets comme des flottes de véhicules ou des installations d'énergie, chute d'un tiers à 740 M$. Le recul global vient donc entièrement de la dette."},
    {"h":"Ce qui inquiète vraiment","p":"Le nombre de startups financées tombe à 343, contre 438 un an plus tôt (−22 %). C'est le plus bas niveau depuis que The Big Deal suit les tours de 100 k$ et plus, en 2021. Les investisseurs actifs nommés passent de 442+ à 370+ (−16 %)."},
    {"h":"Et d'ici décembre ?","p":"Pour égaler le total de 2025 (3,2 Md$), il faudrait 814 M$ en novembre et décembre, contre 496 M$ sur ces deux mois l'an dernier. Peu probable. Côté equity en revanche, 338 M$ suffiraient pour dépasser 2025 (1,9 Md$), soit moins de deux mois au rythme moyen de l'année."},
  ],
  why="Un marché où l'equity tient mais où le nombre de startups financées s'effondre, c'est un marché qui se concentre : plus d'argent sur moins de dossiers. Pour un investisseur, cela veut dire moins de concurrence sur les premiers tickets, mais aussi un pipeline futur plus mince.",
  unknowns=["Répartition 2025 de l'equity au mois près : non fournie."],
  verification="rapporte", sources=src("bd_nov5"), related=["base-qui-samincit","afrique-octobre-2026"],
  tags=["Afrique","Bilan","Equity","Dette"], entities=[],
  cover={"big":"2,4 Md$","small":"depuis janvier"}
))

A.append(dict(
  id="ido-sum-le-mur", category="afrique-vc", kind="analyse", score=88,
  title="Le « mur » du VC africain : des startups financées comme si les grandes sorties existaient déjà",
  dek="Ido Sum a cartographié levées et exits depuis 2019. Résultat : beaucoup d'entreprises ont levé plus que ce que presque aucune sortie africaine n'a jamais rapporté.",
  brief="162 startups africaines ont levé au moins 20 M$ en equity depuis 2019, et 21 d'entre elles plus de 120 M$. En face, seules six sorties connues ont dépassé 120 M$. L'auteur parle d'un écosystème « adolescent ».",
  event_label="Analyse", event_date="2026-09-29", published_date="2026-09-29",
  figures=[
    {"v":"162","l":"startups ayant levé ≥ 20 M$ en equity","n":"de 2019 à juillet 2026"},
    {"v":"21","l":"ont levé plus de 120 M$"},
    {"v":"59","l":"exits avec un prix connu","n":"sur près de 250 recensées en huit ans"},
    {"v":"20 M$","l":"prix médian des sorties de startups africaines dont le prix est connu","n":"6 seulement au-dessus de 120 M$"},
  ],
  body=[
    {"p":"Ido Sum préparait un cours pour des investisseurs institutionnels à Oxford. En posant côte à côte trois images, ce qui a été levé, ce qui est sorti et ce qui entre dans l'entonnoir, il a vu apparaître ce qu'il appelle un mur."},
    {"p":"D'un côté, 162 startups africaines ont levé au moins 20 M$ en equity entre 2019 et juillet 2026, dont 21 plus de 120 M$. De l'autre, près de 250 sorties en huit ans, dont seulement 59 avec un prix public. Parmi elles, la médiane est de 20 M$, le 90ᵉ centile de 135 M$, et six seulement ont dépassé 120 M$. Trois entreprises, chacune au-delà de 500 M$ levés sur la période, ont levé davantage qu'aucune sortie n'a jamais rapporté. Et à l'entrée de l'entonnoir, les premiers tours ont chuté d'environ 70 % depuis le pic de 2022."},
    {"h":"Prix « vers l'avant » contre prix « vers l'arrière »","p":"Sa thèse : l'Afrique aurait adopté la structure de capital d'un écosystème mûr avant d'en avoir les débouchés. Les tours de VC fixent un prix sur la promesse de croissance future. Les acheteurs locaux, eux, paient sur ce qui existe aujourd'hui : résultats, fonds propres, licences. Les sorties africaines récentes le confirment, avec SmsPortal cédée à 4,6 fois l'EBITDA, Pay@ à environ 9,6 fois l'EBITDA, ou Tamweely à 1,7 fois ce que ses propriétaires avaient payé deux ans plus tôt. Seule exception notable : Optasia, valorisée environ neuf fois son chiffre d'affaires lors de sa cotation à Johannesburg, mais l'entreprise arrivait déjà rentable."},
    {"p":"Ailleurs, l'écart s'est résolu de trois façons : un acheteur étranger qui paie pour ses propres raisons stratégiques (Walmart avec Flipkart), une Bourse qui valorise le futur puis en rend une partie, ou une entreprise qui ne dépasse jamais la valeur locale. L'auteur ajoute un point important : une partie de l'equity levée en Afrique a financé des portefeuilles de prêts, des flottes ou des stocks, que d'autres écosystèmes finançaient au même âge avec de la dette locale."},
  ],
  why="C'est la meilleure grille de lecture du moment pour comprendre les autres actualités de la semaine : l'IPO de MNT-Halan, la prudence des investisseurs, la baisse des premiers tours. La question n'est pas de savoir si l'écosystème est cassé, mais quels acheteurs ou quelles Bourses paieront demain les valorisations d'hier.",
  explain=[
    {"q":"Que veut dire « le dernier mark » ?","a":"C'est la dernière valorisation fixée lors d'un tour de financement. Une sortie « clear le mark » quand le prix payé est supérieur à cette valorisation."},
    {"q":"EBITDA ?","a":"Le résultat avant intérêts, impôts et amortissements. Un rachat à « 4,6 fois l'EBITDA » signifie un prix égal à 4,6 années de ce résultat."},
  ],
  unknowns=["Avis personnel de l'auteur, qui précise distinguer chiffres confirmés, rapportés et estimés dans ses notes.","Moka n'a lu que la première moitié de l'essai."],
  verification="analyse", sources=src("ido"), related=["exits-afrique-octobre","base-qui-samincit"],
  tags=["Analyse","Exits","Valorisations"], entities=["Ido Sum","SmsPortal","Pay@","Tamweely","Optasia","Baobab","Bank Zero","Flipkart","Walmart"],
  cover={"big":"20 M$","small":"sortie médiane"}
))

A.append(dict(
  id="logistique-depasse-fintech", category="afrique-vc", kind="actu", score=80,
  title="La logistique dépasse la fintech en Afrique, grâce à deux entreprises",
  dek="Pour la première fois, le transport et la logistique lèvent plus que la fintech sur neuf mois. Spiro et Moove représentent les trois quarts de ce montant.",
  brief="780 M$ pour la logistique et le transport contre 760 M$ pour la fintech de janvier à septembre. Un record, mais très concentré : sans Spiro et Moove, le secteur serait au niveau des années précédentes.",
  event_label="T1–T3 2026", event_date="2026-09-30", published_date="2026-10-20",
  figures=[
    {"v":"780 M$","l":"logistique & transport","n":"36 % du total, 7 % un an plus tôt"},
    {"v":"760 M$","l":"fintech","n":"35 % du total"},
    {"v":"345 M$","l":"levés par Spiro"},
    {"v":"250 M$","l":"levés par Moove"},
  ],
  body=[
    {"p":"Depuis sept ans, la fintech était numéro un incontesté. Elle l'est encore en nombre de startups financées (80), mais plus en montants. De janvier à septembre, la logistique et le transport ont levé 780 M$, soit 36 % du total, contre 760 M$ pour la fintech. Le précédent record du secteur sur neuf mois était de 17 %, en 2019."},
    {"p":"The Big Deal le dit franchement : c'est en grande partie l'histoire de deux entreprises. Spiro (345 M$) et Moove (250 M$) pèsent les trois quarts des fonds du secteur. Sans elles, la logistique aurait levé environ 185 M$, à peu près comme les autres années."},
  ],
  moka_context="Contexte général, non tiré de la newsletter : Spiro développe des motos électriques et un réseau d'échange de batteries dans plusieurs pays africains. Moove finance des véhicules pour des chauffeurs de VTC, remboursés sur leurs revenus. Dans les deux cas, une bonne partie des montants finance des actifs physiques.",
  why="Quand deux entreprises font un record sectoriel, il faut lire le record comme un signal sur ces deux entreprises plus que sur le secteur. Ça rejoint l'analyse d'Ido Sum : une partie de l'argent levé en Afrique finance des flottes et des actifs, ce que d'autres marchés financent par de la dette.",
  unknowns=["Répartition equity/dette des tours de Spiro et Moove : non détaillée ici."],
  verification="rapporte", sources=src("bd_oct20"), related=["energie-recule","ido-sum-le-mur"],
  tags=["Mobilité","Fintech","Secteurs"], entities=["Spiro","Moove"],
  cover={"big":"36 %","small":"logistique"}
))

A.append(dict(
  id="nigeria-en-tete", category="afrique-vc", kind="actu", score=78,
  title="Le Nigeria repasse en tête, le Kenya et l'Afrique du Sud décrochent",
  dek="635 M$ levés par des startups nigérianes en neuf mois, 2,6 fois plus qu'en 2025. Le Kenya tombe à son plus bas niveau depuis 2020.",
  brief="Le Nigeria retrouve sa première place, portée par de gros tours mais aussi par le nombre : 77 startups financées. L'Égypte est stable. Le Kenya et l'Afrique du Sud reculent fortement.",
  event_label="T1–T3 2026", event_date="2026-09-30", published_date="2026-10-20",
  figures=[
    {"v":"635 M$","l":"Nigeria","n":"×2,6 vs 2025, plus haut depuis 2022"},
    {"v":"445 M$","l":"Égypte","n":"+10 %"},
    {"v":"201 M$","l":"Kenya","n":"−73 %"},
    {"v":"182 M$","l":"Afrique du Sud","n":"−58 %"},
  ],
  chart={"title":"Montants levés, T1–T3 2026","a_label":None,"b_label":"2026 (M$)","rows":[
    {"label":"Nigeria","b":635},{"label":"Égypte","b":445},{"label":"Kenya","b":201},{"label":"Afrique du Sud","b":182},{"label":"Tanzanie","b":53},{"label":"Côte d'Ivoire","b":48}
  ],"note":"Hors startups classées « panafricaines » comme Spiro."},
  body=[
    {"p":"Moove (250 M$), Flutterwave (100 M$), Jumia (50 M$) et Yellow Card (40 M$) ont fait une bonne partie du travail, mais pas tout : 77 startups nigérianes ont levé au moins 100 k$, plus que dans n'importe quel autre pays. Hors entreprises panafricaines, le Nigeria capte 37 % des fonds, sa part la plus haute depuis 2021."},
    {"p":"Pour le Kenya, une précision : Spiro, très présente dans le pays, est désormais classée panafricaine par The Big Deal. Même en tenant compte de ce changement, le pays est nettement en dessous de l'an dernier. Kenya (45) et Afrique du Sud (34) enregistrent leur plus faible nombre de startups financées depuis 2021."},
    {"h":"Hors Big Four","p":"Les autres pays ont levé 260 M$ (−29 %), répartis sur 106 startups dans 19 pays. La Tanzanie mène (53 M$, surtout la facilité de dette de 50 M$ de NALA), devant la Côte d'Ivoire (48 M$, presque entièrement GoCab), la Zambie (32 M$), le Maroc (30 M$) et le Ghana (21 M$). Le Sénégal, premier marché hors Big Four l'an dernier avec 153 M$, n'a levé que 5 M$ cette année."},
  ],
  why="Le retour du Nigeria n'est pas qu'une affaire de méga-tours : c'est le seul des Big Four où le nombre de startups financées augmente. Le recul kényan, lui, mérite d'être suivi de près.",
  unknowns=[],
  verification="rapporte", sources=src("bd_oct20"), related=["afrique-octobre-2026","logistique-depasse-fintech"],
  tags=["Nigeria","Kenya","Égypte","Afrique du Sud","Côte d'Ivoire"], entities=["Moove","Flutterwave","Jumia","Yellow Card","NALA","GoCab"],
  cover={"big":"635 M$","small":"Nigeria"}
))

A.append(dict(
  id="base-qui-samincit", category="afrique-vc", kind="actu", score=74,
  title="Lever son premier ticket en Afrique n'a jamais été aussi difficile",
  dek="Moins de startups financées, moins d'investisseurs, des chèques plus gros : 83 % de l'argent passe par des tours de 10 M$ et plus.",
  brief="311 startups ont levé au moins 100 k$ en neuf mois, un plus bas historique. Les petits tours reculent le plus. Spiro et Moove pèsent à eux seuls 28 % de tout l'argent levé sur le continent.",
  event_label="T1–T3 2026", event_date="2026-09-30", published_date="2026-10-13",
  figures=[
    {"v":"311","l":"startups financées","n":"381 en 2025, −18 %"},
    {"v":"171","l":"tours entre 100 k$ et 1 M$","n":"220 en 2025"},
    {"v":"83 %","l":"des fonds via des tours ≥ 10 M$","n":"78 % en 2025, 69 % en 2024"},
    {"v":"334+","l":"investisseurs actifs nommés","n":"408+ en 2025"},
  ],
  body=[
    {"p":"The Big Deal le répète depuis le début de l'année : la base s'amincit. De janvier à septembre, 311 startups ont levé au moins 100 k$ sur le continent, contre 381 un an plus tôt. C'est moins qu'en 2023, au cœur de l'« hiver » du financement."},
    {"p":"La baisse se concentre en bas de l'entonnoir. Les tours de 100 k$ à 1 M$ passent de 220 à 171. Ceux de plus de 1 M$ baissent moins (140 contre 161). En clair : obtenir un premier chèque devient plus dur, alors que ceux qui atteignent les gros tours s'en sortent."},
    {"h":"Moins de mains signent les chèques","p":"Seuls 271+ investisseurs ont participé à au moins un tour en equity, contre 366+ (−26 %). Les plus actifs restent DEG (25+ opérations) et Launch Africa (21+), suivis de Co-Creation Hub et Mastercard (12+ chacun) puis Digital Africa (11+)."},
    {"p":"Bonne nouvelle quand même : 34 sorties sur neuf mois, environ deux fois plus qu'en 2023 ou 2024."},
  ],
  why="Les tours d'amorçage d'aujourd'hui sont les Séries A et B de demain. Une base qui rétrécit maintenant, c'est moins de grosses opérations dans trois ou quatre ans.",
  unknowns=[],
  verification="rapporte", sources=src("bd_oct13"), related=["afrique-bilan-2026","femmes-fondatrices"],
  tags=["Amorçage","Investisseurs"], entities=["DEG","Launch Africa","Co-Creation Hub","Mastercard","Digital Africa"],
  cover={"big":"311","small":"startups"}
))

A.append(dict(
  id="energie-recule", category="energie-industrie", kind="actu", score=72,
  title="L'énergie, grande perdante de l'année pour les startups africaines",
  dek="Après un record en 2025, les startups de l'énergie n'ont levé que 187 M$ en neuf mois, −74 %. En cause, surtout, la dette.",
  brief="L'énergie passe de 32 % à 9 % des fonds levés. La santé s'effondre aussi. La climate tech au sens large reste pourtant un tiers du marché, et 55 % des fonds en octobre.",
  event_label="T1–T3 2026", event_date="2026-09-30", published_date="2026-10-20",
  figures=[
    {"v":"187 M$","l":"énergie, T1–T3 2026","n":"−74 % (721 M$ en 2025)"},
    {"v":"9 %","l":"part de l'énergie","n":"plus bas depuis 2021"},
    {"v":"21 M$","l":"santé, pour 35 startups","n":"−88 %"},
    {"v":"35 %","l":"part de la climate tech","n":"39 % en 2025"},
  ],
  body=[
    {"p":"2025 avait été une année record pour l'énergie : 721 M$ levés sur neuf mois, 32 % du total. En 2026, le secteur ne pèse plus que 187 M$ et 9 % des fonds. The Big Deal désigne la dette comme principal responsable : le secteur dépend beaucoup de ce type de financement, et il s'est contracté cette année."},
    {"p":"Octobre montre que la dette n'a pas disparu pour autant : 13 M$ pour Afreenergy Solar au Sénégal, un prêt de 10 M$ de la BERD à Beacon Power Services au Nigeria. Et la climate tech, qui recoupe plusieurs secteurs, a capté 55 % des fonds du mois."},
    {"p":"Autre secteur en chute libre : la santé, avec 21 M$ pour 35 startups, son plus bas niveau depuis 2019."},
  ],
  why="Les projets d'énergie en Afrique dépendent énormément de la dette, souvent apportée par des institutions de développement. Quand ce robinet ralentit, le secteur plonge, même si la demande est là. À suivre : les publications de la BEI et Green Rising, désormais dans vos sources.",
  unknowns=["Raisons précises du recul de la dette énergie : non détaillées (taux, appétit des bailleurs, etc.)."],
  verification="rapporte", sources=src("bd_oct20","bd_nov5"), related=["logistique-depasse-fintech","afrique-octobre-2026"],
  tags=["Énergie","Climate tech","Santé","Dette"], entities=["Afreenergy Solar","Beacon Power Services","BERD"],
  cover={"big":"−74 %","small":"énergie"}
))

A.append(dict(
  id="femmes-fondatrices", category="afrique-vc", kind="brief", score=60,
  title="Femmes fondatrices : un chiffre en hausse qui cache une baisse",
  dek="La part des fonds levés par des startups dirigées par une femme double, mais une seule entreprise explique presque tout.",
  brief="5,4 % des fonds pour des startups dirigées par une femme, contre 2,7 % en 2025. Sans Odyssey Energy Solutions (74 M$), on serait autour de 2 %. Et le nombre de ces startups financées baisse de 28 %.",
  event_label="T1–T3 2026", event_date="2026-09-30", published_date="2026-10-20",
  figures=[
    {"v":"5,4 %","l":"des fonds pour une CEO femme","n":"≈ 2 % sans Odyssey"},
    {"v":"46","l":"startups à CEO femme financées","n":"64 en 2025"},
    {"v":"240 k$","l":"tour médian, ≥ 1 cofondatrice","n":"750 k$ avec ≥ 1 cofondateur homme"},
  ],
  body=[
    {"p":"Les startups qui comptent au moins une cofondatrice représentent 28 % des entreprises financées, mais seulement 8,9 % des montants. Les équipes exclusivement féminines ont levé 16 M$ au total, moins de 1 % des fonds."},
    {"p":"The Big Deal fait le lien avec la raréfaction des petits tickets : quand l'argent se concentre sur de gros tours, les startups qui lèvent des montants plus modestes, souvent menées par des femmes, sont les premières à en pâtir."},
  ],
  why="C'est l'autre face de la « base qui s'amincit » : la concentration du marché ne pénalise pas tout le monde de la même façon.",
  unknowns=[], verification="rapporte", sources=src("bd_oct20"), related=["base-qui-samincit"],
  tags=["Diversité"], entities=["Odyssey Energy Solutions"],
  cover={"big":"8,9 %","small":"des fonds"}
))

A.append(dict(
  id="revolut-115-milliards", category="tech", kind="actu", score=86,
  title="Revolut vaut désormais 115 milliards de dollars",
  dek="+53 % en un an, à l'occasion d'une vente secondaire d'actions. Prochaine étape : une banque nationale aux États-Unis, au premier semestre 2027.",
  brief="La néobanque britannique confirme une valorisation de 115 Md$. Elle revendique plus de 80 millions de clients particuliers et une activité entreprises qui pèse à elle seule 1,28 Md$ de chiffre d'affaires annualisé. Pas d'IPO avant 2028.",
  event_label="4 novembre 2026", event_date="2026-11-04", published_date="2026-11-05",
  figures=[
    {"v":"115 Md$","l":"valorisation","n":"+53 % sur un an"},
    {"v":"80 M+","l":"clients particuliers"},
    {"v":"1,28 Md$","l":"CA annualisé de Revolut Business","n":"≈ 48,6 Md$ de transactions par mois"},
    {"v":"7","l":"licences bancaires","n":"dont 5 obtenues en 2026"},
  ],
  body=[
    {"p":"Revolut a bouclé une vente secondaire d'actions qui la valorise 115 Md$, 53 % de plus qu'il y a un an. Sifted confirme le chiffre, qui circulait déjà."},
    {"p":"Le moteur de croissance le moins visible, c'est Revolut Business : environ 1,28 Md$ de chiffre d'affaires annualisé et quelque 48,6 Md$ de transactions traitées chaque mois. La banque prépare aussi le lancement d'une banque nationale aux États-Unis au premier semestre 2027, sous réserve de l'accord final, et vient d'obtenir une licence en Nouvelle-Zélande. Elle détient désormais sept licences bancaires et opère comme banque agréée dans 34 territoires."},
    {"p":"Une introduction en Bourse n'est pas envisagée avant 2028. Signe de l'effet « école Revolut » : deux de ses premiers salariés viennent de sortir de l'ombre avec Haido, une app de gestion de patrimoine pilotée par l'IA."},
  ],
  moka_context="Une vente secondaire, c'est quand des actionnaires existants (salariés, premiers investisseurs) vendent leurs actions à de nouveaux acheteurs. L'entreprise ne lève pas d'argent frais : l'opération donne de la liquidité et fixe un prix de marché.",
  why="La valorisation impressionne, mais le vrai test sera la banque américaine : c'est un marché où plusieurs néobanques européennes ont déjà buté.",
  unknowns=["Identité des acheteurs de la vente secondaire : non précisée dans les newsletters."],
  verification="rapporte", sources=src("tldrfin_revolut","sifted_nov5","sifted_nov6"), related=["sequoia-recentre"],
  tags=["Fintech","Europe","Valorisation"], entities=["Revolut","Haido"],
  cover={"big":"115 Md$","small":"Revolut"}
))

A.append(dict(
  id="sequoia-recentre", category="capital", kind="actu", score=84,
  title="Sequoia ferme Londres et défait vingt ans d'expansion",
  dek="L'un des fonds les plus emblématiques de la Silicon Valley ferme son bureau européen, arrête ses programmes d'amorçage et revient à un modèle concentré.",
  brief="Fin du bureau de Londres après six ans, fin de l'accélérateur Arc et du programme Scouts, fusion des équipes early stage et growth. Sequoia dit avoir levé environ 10 Md$ et veut faire moins de paris, avec une équipe plus petite, depuis la baie de San Francisco.",
  event_label="4 novembre 2026", event_date="2026-11-04", published_date="2026-11-05",
  figures=[
    {"v":"≈ 10 Md$","l":"de nouveaux capitaux levés"},
    {"v":"6 ans","l":"de présence à Londres","n":"plusieurs postes supprimés"},
  ],
  body=[
    {"p":"Sequoia simplifie tout. Le fonds ferme son bureau londonien ouvert il y a six ans, et plusieurs membres de l'équipe européenne vont perdre leur poste, selon Sifted. Il met fin à son accélérateur Arc et à son programme Scouts, fusionne investissement early stage et growth, aplatit son partenariat et supprime même sa réunion d'associés du lundi."},
    {"p":"L'objectif affiché : revenir à un modèle plus concentré, avec moins de paris, une équipe plus réduite et un accompagnement plus profond des fondateurs, depuis la baie de San Francisco."},
  ],
  why="C'est un signal pour l'Europe : l'un des fonds les plus influents du monde juge qu'il n'a pas besoin d'équipe locale pour y investir. Pour les fondateurs européens, et a fortiori africains, accéder à Sequoia passera par la Californie.",
  unknowns=["Nombre exact de postes supprimés : non communiqué.","Avenir des participations européennes existantes : non précisé."],
  verification="rapporte", sources=src("tldrfin_sequoia","sifted_nov5"), related=["europe-levees-semaine","pe-sous-pression"],
  tags=["VC","Europe"], entities=["Sequoia Capital"],
  cover={"big":"Londres","small":"fermé"}
))

A.append(dict(
  id="anthropic-ipo", category="tech", kind="actu", score=82,
  title="IPO d'Anthropic : les investisseurs veulent un prix plus bas",
  dek="L'introduction en Bourse, attendue la semaine précédant Thanksgiving, visait 1 500 milliards de dollars. Les gros investisseurs parlent plutôt de 1 000.",
  brief="Selon le Wall Street Journal, la levée attendue passerait d'au plus 100 Md$ à environ 80 Md$. En parallèle, Anthropic a publié environ 17 Md$ de chiffre d'affaires au troisième trimestre.",
  event_label="Semaine du 2 novembre", event_date="2026-11-06", published_date="2026-11-06",
  figures=[
    {"v":"1 500 Md$","l":"valorisation visée","n":"≈ 1 000 Md$ jugée plus réaliste"},
    {"v":"≈ 80 Md$","l":"levée désormais attendue","n":"jusqu'à 100 Md$ initialement"},
    {"v":"≈ 17 Md$","l":"chiffre d'affaires du T3"},
    {"v":"33,24 Md$","l":"CA sur neuf mois","n":"≈ +1 200 % sur un an"},
  ],
  body=[
    {"p":"Les grands investisseurs qui comptent participer à l'IPO d'Anthropic estiment, selon le WSJ, que la valorisation de 1 500 Md$ devra baisser. La levée, attendue jusqu'à 100 Md$, serait plutôt de l'ordre de 80 Md$, pour une valorisation plus proche de 1 000 Md$. Anthropic évite pour l'instant de s'engager sur un calendrier ou des modalités précises."},
    {"p":"Le contexte a changé en quelques jours : les midterms américaines ont porté au pouvoir plusieurs élus sceptiques sur l'IA, ce qui pourrait ralentir la construction de data centers, et les investisseurs ont pris leurs distances avec les paris sur l'IA cette semaine."},
    {"h":"Les chiffres publiés","p":"D'après CNBC, Anthropic a réalisé environ 17 Md$ de chiffre d'affaires au troisième trimestre, soit 33,24 Md$ sur neuf mois, en hausse d'environ 1 200 % sur un an. La croissance d'un trimestre à l'autre ralentit toutefois à 47 %. Les engagements de calcul de l'entreprise approchent 900 Md$."},
  ],
  why="À ces montants, l'opération serait hors norme. Le prix final dira combien les marchés publics sont prêts à payer pour la croissance de l'IA, une question qui pèse sur toute la chaîne, des fonds aux data centers.",
  disclosure="Transparence : Moka est construit avec Claude, un modèle d'Anthropic. Cet article s'en tient aux faits rapportés par les sources citées.",
  unknowns=["Estimations des investisseurs rapportées par le WSJ : rien n'est confirmé par Anthropic.","Date exacte de l'IPO : non fixée publiquement."],
  verification="non-confirme", sources=src("tldr_anthropic","tldrfin_anthropic"), related=["midterms-ia"],
  tags=["IA","IPO","États-Unis"], entities=["Anthropic"],
  cover={"big":"1 000 Md$ ?","small":"IPO"}
))

A.append(dict(
  id="midterms-ia", category="monde", kind="actu", score=76,
  title="Midterms : les démocrates reprennent le Congrès, l'industrie de l'IA s'inquiète",
  dek="Victoire démocrate à la Chambre et au Sénat. Les électeurs ont aussi envoyé un message hostile aux grands projets de data centers.",
  brief="Les démocrates gagnent les deux chambres, dont un siège de sénateur au Texas, une première depuis 1988. Les VC européens sont partagés sur l'impact. Côté IA, l'opposition locale aux data centers devient un vrai risque politique.",
  event_label="3 novembre 2026", event_date="2026-11-03", published_date="2026-11-05",
  figures=[
    {"v":"2 / 2","l":"chambres du Congrès gagnées par les démocrates"},
    {"v":"1988","l":"dernière fois que le Texas avait élu un sénateur démocrate"},
  ],
  body=[
    {"p":"Mardi soir, les démocrates ont repris le contrôle de la Chambre des représentants et du Sénat. Pour l'Europe, l'impact divise les investisseurs interrogés par Sifted. Michael Jackson, de Multiple Capital, doute que cela change grand-chose : selon lui, le Congrès s'attaquera surtout à l'administration, et le président peut continuer à gouverner par décret."},
    {"p":"Jack Wang, associé chez Project A, s'attend en revanche à des effets dans la défense. Le Texas, qui a basculé, soutenait fortement l'industrie de défense, et plusieurs startups du secteur y ont des usines, dont Saronic, Warhound et le britannique Isembard. Pierre-Eric Leibovici, de Daphni, espère surtout un retour à la stabilité."},
    {"h":"L'IA dans le viseur","p":"D'après le WSJ, relayé par TLDR, les résultats montrent une forte opposition des électeurs à la construction massive de capacités de calcul. Un ralentissement des chantiers serait un problème pour des entreprises tech qui manquent déjà de puissance de calcul, avec des effets possibles sur l'économie américaine."},
  ],
  why="Pour un investisseur, deux effets concrets à surveiller : le soutien local aux startups de défense, et le rythme de construction des data centers, qui conditionne une bonne partie des valorisations de l'IA.",
  unknowns=["Mesures concrètes que prendra le nouveau Congrès : inconnues à ce stade."],
  verification="rapporte", sources=src("sifted_nov5","tldr_election"), related=["anthropic-ipo","pe-sous-pression"],
  tags=["États-Unis","Politique","IA","Défense"], entities=["Multiple Capital","Project A","Daphni","Saronic","Warhound","Isembard"],
  cover={"big":"Congrès","small":"bascule"}
))

A.append(dict(
  id="pe-sous-pression", category="capital", kind="actu", score=70,
  title="Private equity et crédit privé : le mur de refinancement approche",
  dek="Les sorties tech du PE ont fondu de 77 % en un an, et des centaines de milliards de prêts risqués arrivent à échéance en 2028 et 2029.",
  brief="Un essai d'a16z chiffre la pression sur le PE tech. En parallèle, le financement des infrastructures d'IA fait gonfler le crédit privé, avec un risque de refinancement concentré entre 2027 et 2029.",
  event_label="Début novembre 2026", event_date="2026-11-05", published_date="2026-11-05",
  figures=[
    {"v":"−77 %","l":"valeur des sorties tech adossées au PE","n":"sur un an"},
    {"v":"140 Md$","l":"prêts risqués à échéance en 2028"},
    {"v":"160 Md$","l":"en 2029","n":"dont environ un tiers dans le logiciel"},
    {"v":"≈ 1 000 Md$","l":"dépenses attendues en 2027","n":"hyperscalers et CoreWeave"},
  ],
  body=[
    {"p":"Dans un essai intitulé « Is private equity cooked? », a16z note que la valeur des sorties tech adossées au private equity a chuté de 77 % en un an. Environ 140 Md$ de prêts risqués liés au PE arrivent à échéance en 2028, puis 160 Md$ en 2029, dont un tiers environ dans le logiciel."},
    {"p":"Au même moment, l'IA transforme le crédit privé. Il ne finance plus seulement des entreprises, mais aussi du foncier, de l'énergie, des semi-conducteurs et de la capacité de calcul. Les hyperscalers et CoreWeave devraient dépenser près de 1 000 Md$ en 2027, via leur trésorerie, de la dette, des coentreprises et des véhicules dédiés."},
    {"h":"Où est le risque","p":"Un mur de refinancement entre 2027 et 2029, surtout pour les emprunteurs les plus fragiles qui paient leurs intérêts en nature (PIK), et des financements de plus en plus circulaires entre fabricants de puces, développeurs d'IA et fournisseurs d'infrastructure, qui pourraient produire des pertes corrélées en cas de retournement."},
  ],
  moka_context="PIK (« payment in kind ») : au lieu de payer ses intérêts en cash, l'emprunteur les ajoute au montant de sa dette. Pratique à court terme, mais la dette grossit.",
  why="Ces échéances concernent aussi les fonds de PE actifs en Afrique et au Moyen-Orient : quand les grands acteurs doivent refinancer, l'argent disponible ailleurs se raréfie.",
  unknowns=["Moka n'a pas encore pu lire les numéros PitchBook de la semaine (« Megafunds falter », « The IPO backlog is a myth »), qui arrivent sans version texte."],
  verification="rapporte", sources=src("tldrfin_pe","tldrfin_credit"), related=["midterms-ia","sequoia-recentre"],
  tags=["Private equity","Crédit privé","IA"], entities=["a16z","CoreWeave"],
  cover={"big":"−77 %","small":"sorties PE"}
))

A.append(dict(
  id="europe-levees-semaine", category="capital", kind="brief", score=62,
  title="Les levées européennes de la semaine, de la stratosphère à la carte d'entreprise",
  dek="EOS-X Space lève 110 M€, Pliant 80 M$, Vaeridion complète sa Série A avec 94,5 M€ de subventions européennes.",
  brief="Une sélection des tours repérés par Sifted les 5 et 6 novembre, avec ce que fait chaque entreprise et qui investit.",
  event_label="5–6 novembre 2026", event_date="2026-11-06", published_date="2026-11-06",
  figures=[
    {"v":"110 M€","l":"EOS-X Space (Madrid)"},
    {"v":"80 M$","l":"Pliant (Berlin), Série C"},
    {"v":"30 M€ + 94,5 M€","l":"Vaeridion (Munich)","n":"extension de Série A + subventions UE"},
  ],
  items=[
    {"name":"EOS-X Space","where":"Madrid","amount":"110 M€","what":"Capsules sous ballon à hélium pour le tourisme en haute atmosphère, et constellations de satellites civils et militaires.","who":"Tour mené par Global Emerging Markets."},
    {"name":"Pliant","where":"Berlin","amount":"80 M$ · Série C","what":"Cartes de crédit d'entreprise et logiciel de gestion des dépenses.","who":"Seaya et Speedinvest, avec Illuminate Financial, Motive Partners, Molten Ventures."},
    {"name":"Vaeridion","where":"Munich","amount":"30 M€ · extension de Série A","what":"Avions électriques. A aussi obtenu 94,5 M€ de subventions de la Commission européenne.","who":"Shift Invest et Invest-NL, avec World Fund, Project A, Vsquared Ventures."},
    {"name":"FluoRok","where":"Oxford","amount":"30 M$ · Série A","what":"Produits fluorés pour médicaments, agrochimie et sels d'électrolyte de batteries.","who":"Orano Venture Fund et Supernova Invest, entre autres."},
    {"name":"bit.bio","where":"Cambridge","amount":"25 M$ · Série D","what":"Programme des cellules souches humaines en types cellulaires précis pour la recherche et les thérapies.","who":"Notamment M&G Investments et Jonathan Milner."},
    {"name":"Supa","where":"Londres","amount":"21 M£ · seed","what":"Outils numériques pour la gestion d'immeubles résidentiels.","who":"2150 et OpenOcean."},
    {"name":"Biograil","where":"Roskilde","amount":"20 M€","what":"Dispositifs d'administration orale de médicaments pour remplacer des injections.","who":"Dont Eli Lilly et High-Tech Gründerfonds."},
    {"name":"Green Voltis","where":"Stockholm","amount":"13,5 M€ · Série A","what":"IA pour piloter et vendre l'énergie de batteries de stockage.","who":"Locphine Capital."},
    {"name":"Kabilio","where":"Barcelone","amount":"10 M€","what":"Comptabilité automatisée par IA pour cabinets et PME.","who":"Picus Capital et Visionaries Club."},
  ],
  body=[{"p":"Sifted publie chaque jour une sélection de tours européens. Voici ceux des 5 et 6 novembre, regroupés."}],
  why="Deux thèmes ressortent : la souveraineté industrielle (spatial, aviation électrique, chimie) et l'IA appliquée à des métiers très concrets comme la comptabilité ou le stockage d'énergie.",
  unknowns=["Valorisations : non communiquées pour aucun de ces tours."],
  verification="rapporte", sources=src("sifted_nov6","sifted_nov5"), related=["hardware-sans-chine","sequoia-recentre"],
  tags=["Europe","Levées"], entities=["EOS-X Space","Pliant","Vaeridion","FluoRok","bit.bio","Supa","Biograil","Green Voltis","Kabilio"],
  cover={"big":"9 tours","small":"Europe"}
))

A.append(dict(
  id="hardware-sans-chine", category="energie-industrie", kind="actu", score=58,
  title="Les startups hardware européennes essaient de se passer de la Chine",
  dek="Turbine au kérosène pour éviter les batteries chinoises, fabrication internalisée : jusqu'où peut aller l'indépendance, et à quel prix ?",
  brief="Sous la pression des investisseurs et des États, notamment dans la défense, des startups européennes cherchent à sortir la Chine de leur chaîne d'approvisionnement. C'est long, cher, et fabriquer en Europe ne garantit pas l'absence de composants chinois.",
  event_label="6 novembre 2026", event_date="2026-11-06", published_date="2026-11-06",
  figures=[],
  body=[
    {"p":"Moteurs, batteries, bras robotisés : depuis des années, la Chine fabrique plus vite et moins cher que tout le monde. Avec les tensions géopolitiques, cette dépendance devient un problème pour les startups européennes, surtout celles qui travaillent pour la défense et d'autres secteurs stratégiques."},
    {"p":"Sifted raconte des choix radicaux : une startup française de drones a développé une turbine au kérosène pour ne plus dépendre des batteries et moteurs chinois. D'autres internalisent leur fabrication ou cherchent de nouveaux fournisseurs."},
    {"p":"La difficulté : fabriquer en Europe ne veut pas dire être libre de matériaux chinois, et démêler des décennies de chaînes mondialisées n'est ni simple ni bon marché."},
  ],
  why="La souveraineté industrielle devient un critère d'investissement. Pour les fondateurs hardware, elle a un coût qui pèse sur les marges et sur le temps de développement.",
  unknowns=["Nom de la startup française de drones : non cité dans la newsletter."],
  verification="rapporte", sources=src("sifted_nov6"), related=["europe-levees-semaine"],
  tags=["Industrie","Défense","Chaînes d'approvisionnement"], entities=[],
  cover={"big":"Made in EU","small":"sans Chine ?"}
))

for a in A:
    a.setdefault("origin","claude-session")
    a["collected_at"]="2026-11-07"
    a.setdefault("explain",[]); a.setdefault("timeline",[]); a.setdefault("moka_context",None)
    a.setdefault("chart",None); a.setdefault("items",[]); a.setdefault("disclosure",None)

json.dump(A, open("data/articles.json","w"), ensure_ascii=False, indent=1)
print(len(A), "articles", sum(len(json.dumps(a,ensure_ascii=False)) for a in A), "bytes")
