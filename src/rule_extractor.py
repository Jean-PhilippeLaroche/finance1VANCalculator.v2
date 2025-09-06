import spacy
from spacy.matcher import Matcher
import re
from extract_text import *

# loads french model
nlp = spacy.load("fr_core_news_sm")
matcher = Matcher(nlp.vocab)

# -------------------------
# spaCy patterns
# -------------------------

# amounts : ex 80 000, -35 000, 50000€
pattern_montant = [{"LIKE_NUM": True}, {"IS_SPACE": True, "OP":"?"}, {"LIKE_NUM": True, "OP":"?"}]
matcher.add("MONTANT", [pattern_montant])

# percentage : ex 5 %
pattern_pourcent = [{"LIKE_NUM": True}, {"ORTH": "%"}]
matcher.add("POURCENT", [pattern_pourcent])

# years : ex année 2, années 4-12
pattern_annee = [{"LOWER": {"REGEX": "année|années"}}, {"LIKE_NUM": True}]
matcher.add("ANNEE", [pattern_annee])

# beginning of year / end
pattern_debut_fin = [{"LOWER": {"IN": ["début", "fin"]}}]
matcher.add("PERIODE", [pattern_debut_fin])

# keywords for each category (optionnel, aide à classer)
pattern_revenu = [{"LOWER": {"REGEX": "revenu|recette"}}]
matcher.add("REVENU", [pattern_revenu])

pattern_depense = [{"LOWER": {"REGEX": "dépense|charge"}}]
matcher.add("DEPENSE", [pattern_depense])

pattern_investissement = [{"LOWER": {"REGEX": "investissement"}}]
matcher.add("INVESTISSEMENT", [pattern_investissement])

pattern_actif = [{"LOWER": {"REGEX": "actif|bien|équipement|machinerie"}}]
matcher.add("ACTIF", [pattern_actif])

# -------------------------
# main function
# -------------------------

def extraire_projet_data(texte):
    """

    :param texte:
    :return:
    """
    doc = nlp(texte)
    matches = matcher(doc)

    # Stockage temporaire
    montants, annees, pourcents, periodes, categories, actifs = [], [], [], [], [], []

    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]

        if label == "MONTANT":
            montants.append(span.text)
        elif label == "ANNEE":
            annees.append(span.text)
        elif label == "POURCENT":
            pourcents.append(span.text)
        elif label == "PERIODE":
            periodes.append(span.text)
        elif label in ["REVENU", "DEPENSE", "INVESTISSEMENT"]:
            categories.append((label, span.start))
        elif label == "ACTIF":
            actifs.append(span.text)

    # -------------------------
    # Règles intelligentes pour organiser les blocs
    # -------------------------

    # Investissement initial = premier investissement mentionné
    investissement_initial = []
    investissement_en_cours = []
    revenu = []
    depense = []
    taux_imposition = None
    taux_actualisation = None
    taux_amortissement = []
    montant_recuperes_fin = []
    duree_projet = None
    actifs_utilises = []

    # Exemple simple de regroupement
    # Ici on va scanner les montants + années + catégorie pour créer des blocs
    for i, (cat, pos) in enumerate(categories):
        # Chercher le montant le plus proche après la catégorie
        montant_block = next((m for m in montants if doc.text.find(m) > pos), None)
        annee_block = next((a for a in annees if doc.text.find(a) > pos), None)
        periode_block = next((p for p in periodes if doc.text.find(p) > pos), None)
        pourcent_block = next((p for p in pourcents if doc.text.find(p) > pos), None)

        block = {}
        if montant_block:
            block["montant"] = montant_block
        if annee_block:
            block["année"] = annee_block
        if periode_block:
            block["periode"] = periode_block
        if pourcent_block:
            block["croissance"] = pourcent_block

        if cat == "INVESTISSEMENT":
            if not investissement_initial:
                investissement_initial.append(block.get("montant"))
            else:
                investissement_en_cours.append(block)
        elif cat == "REVENU":
            revenu.append(block)
        elif cat == "DEPENSE":
            depense.append(block)

    # Extraire taux et durée par regex simples
    taux_imposition_match = re.search(r"taux d['’]imposition|Tc\s*[:=]?\s*(\d+\.?\d*)\s*%", texte)
    if taux_imposition_match:
        taux_imposition = taux_imposition_match.group(1) + "%"

    taux_actualisation_match = re.search(r"taux d['’]actualisation\s*[:=]?\s*(\d+\.?\d*)\s*%", texte)
    if taux_actualisation_match:
        taux_actualisation = taux_actualisation_match.group(1) + "%"

    taux_amortissement_matches = re.findall(r"amortissement|d:|d :|dépréciation|d=|d =\s*[:=]?\s*(\d+\.?\d*)\s*%", texte)
    if taux_amortissement_matches:
        taux_amortissement = taux_amortissement_matches

    montant_recuperes_fin_matches = re.findall(r"récupéré[s]? à la fin\s*[:=]?\s*(\d+[\s\d]*)", texte)
    if montant_recuperes_fin_matches:
        montant_recuperes_fin = montant_recuperes_fin_matches

    duree_match = re.search(r"durée du projet|Durée du projet\s*[:=]?\s*(\d+)\s*ans?", texte)
    if duree_match:
        duree_projet = duree_match.group(1)

    # Actifs utilisés (montant d’achat, durée, montant vente)
    for actif in actifs:
        achat_match = re.search(fr"{actif}.*?achat\s*[:=]?\s*(\d+[\s\d]*)", texte, re.IGNORECASE)
        vente_match = re.search(fr"{actif}.*?vente\s*[:=]?\s*(\d+[\s\d]*)", texte, re.IGNORECASE)
        duree_match = re.search(fr"{actif}.*?durée\s*[:=]?\s*(\d+)\s*ans?", texte, re.IGNORECASE)
        actifs_utilises.append({
            "nom": actif,
            "montant_achat": achat_match.group(1) if achat_match else None,
            "montant_vente": vente_match.group(1) if vente_match else None,
            "durée": duree_match.group(1) if duree_match else None
        })

    projet_data = {
        "investissement_initial": investissement_initial,
        "investissement_en_cours": investissement_en_cours,
        "revenu": revenu,
        "dépense": depense,
        "taux_imposition": taux_imposition,
        "taux_actualisation": taux_actualisation,
        "taux_amortissement": taux_amortissement,
        "montant_recuperes_fin": montant_recuperes_fin,
        "durée_projet": duree_projet,
        "actifs_utilisés": actifs_utilises
    }

    return projet_data


# -------------------------
# Test rapide
# -------------------------
if __name__ == "__main__":

    samples_dir = Path(__file__).resolve(). parents[1] / "data" / "samples"

    # accessing each pdf, printing its name then converting the pdf object to a str
    for pdf in samples_dir.glob("*.pdf"):
        print(f"\n==== {pdf.name} ====")
        txt = pdf_to_text(str(pdf))
    print(txt)
    data = extraire_projet_data(txt)
    from pprint import pprint
    pprint(data)