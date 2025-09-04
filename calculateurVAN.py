from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from Etape_1 import MiseFondsInitiale, ConvertisseurInterets
from Etape_2 import CalculateurAnnuitees
from Etape_3 import VAEIACC
from Etape_4_5 import ValeurRevente
from Etape_6 import ValeurImpotGainCapital
from Etape_7_8 import ValeurFermeture
from erreur_verif import input_retry

console = Console()

console.print(Panel("[bold cyan]Calculateur de VAN[/bold cyan]", expand=False))

duree_projet = float(Prompt.ask("[bold yellow]Quelle est la durée du projet en années?[/bold yellow]"))

def changement_taux():
    taux = (float(Prompt.ask("[bold yellow]Quel est le taux d'intérêts du projet en pourcentage?[/bold yellow]"))) / 100

    frequence_taux = Prompt.ask(
        "[bold yellow]Le taux d'intérêts donné est-il en année, en trimestre, en mois, en semaine ou en jour?[/bold yellow]"
    ).strip().lower()
    conv = ConvertisseurInterets(taux, frequence_taux)
    nouveau_taux = conv.convertisseur_taux()
    return nouveau_taux

taux_global = changement_taux()

taux_imposition = (float(Prompt.ask("[bold yellow]Quel est"
                                    " le taux d'imposition de l'entreprise en pourcentage?[/bold yellow]"))) / 100


# étape 1 (calcul des mises de fonds)
def calcul_mise_fonds():
    nombre_mise_fonds = int(Prompt.ask("[bold yellow]Combien y a-t-il de mise de fonds différentes?[/bold yellow]"))
    vaa_total_mise_de_fonds = 0
    for number in range(nombre_mise_fonds):

        console.print(f"\n--- Mise de fonds {number + 1} (étape 1) ---", style="bold green")

        temps = int(Prompt.ask("[bold yellow]Quelle est l'année du projet correspondant à cette mise de fonds? (le projet débute en l'an 0)[/bold yellow]"))
        montant = float(Prompt.ask("[bold yellow]Quel est le montant de cette mise de fonds?[/bold yellow]").replace(" ", ""))
        position_montant = str(Prompt.ask("[bold yellow]Est-ce que ce montant est déboursé au début ou à la fin de la période?[/bold yellow]"))

        calc = MiseFondsInitiale(taux_global, temps, montant, position_montant)
        vaa_mise_de_fonds_singulier = -1 * (calc.calculer_mise())

        console.print(f"\n-- Valeur actualisée de la mise de fonds {number + 1} = {vaa_mise_de_fonds_singulier:.2f} --", style="bold green")

        vaa_total_mise_de_fonds += vaa_mise_de_fonds_singulier

    console.print(f"\n- Valeur actualisée totale des différentes mises de fonds = {vaa_total_mise_de_fonds} -\n", style="bold green")

    return vaa_total_mise_de_fonds

vaa_mise_de_fonds = calcul_mise_fonds()


# étape 2 (calcul des annuités)
def calcul_annuites():
    nombre_annuites = int(Prompt.ask("[bold yellow]Combien y a-t-il de séries d'annuitées différentes?[/bold yellow]"))
    vaa_total_annuites = 0

    for number in range(nombre_annuites):

        console.print(f"\n--- Annuités {number + 1} (étape 2) ---", style="bold green")

        temps_debut = int(Prompt.ask("[bold yellow]Quelle est l'année de début de cette série d'annuitées? (le projet débute en l'an 0)[/bold yellow]"))
        temps_fin = int(Prompt.ask("[bold yellow]Quel est l'année de fin de cette série d'annuitées?[/bold yellow]"))
        montant_annuites = float(Prompt.ask("[bold yellow]Quel est le montant des annuitées?[/bold yellow]").replace(" ", ""))
        taux_croissance = (float(Prompt.ask("[bold yellow]Quel est le taux de croissance/décroissance en pourcentage? (chiffre négatif pour décroissance)[/bold yellow]")) / 100)
        position = str(Prompt.ask("[bold yellow]Est-ce que les annuités sont déboursées au début ou à la fin de la période?[/bold yellow]"))

        calcu = CalculateurAnnuitees(taux_global, temps_debut, temps_fin, montant_annuites, position, taux_croissance)

        vaa_annuites_singulier = calcu.calculateur_VA_croissance()
        vaa_annuites_singulier = vaa_annuites_singulier * (1 - taux_imposition)

        console.print(f"\n-- Valeur actualisée de la série d'annuités {number + 1} = {vaa_annuites_singulier:.2f} --", style="bold green")

        vaa_total_annuites += vaa_annuites_singulier

    console.print(f"\n- Valeur totale des séries d'annuités = {vaa_total_annuites} -\n", style="bold green")

    return vaa_total_annuites

vaa_annuites = calcul_annuites()

# étapes 3, 6, 7 et 8 (calcul des VAEIACC + impôt à payer sur chaque actif si gain en capital + va économie ou perte)
impot_a_payer = 0
nombre_actif = int(Prompt.ask("[bold yellow]Combien d'actifs ont été utilisé pendant le projet?[/bold yellow]"))
valeur_vaeiacc = 0
valeur_etape_7_8 = 0

for i in range(nombre_actif):

    console.print(f"\n--- Actif {i + 1} (étape 3) ---", style="bold green")

    cout_capital_initial = float(Prompt.ask("[bold yellow]Quel est le coût en capital initial de l'actif?[/bold yellow]").replace(" ", ""))
    taux_acc = (float(Prompt.ask("[bold yellow]Quel est le taux d'ACC pour cette catégorie d'actif en pourcentage?[/bold yellow]"))) / 100
    valeur_vente = float(Prompt.ask("[bold yellow]Quelle est la valeur de revente de l'actif?[/bold yellow]").replace(" ", ""))
    r = min(cout_capital_initial, valeur_vente)
    taux_actualisation = (float(Prompt.ask("[bold yellow]Quel est le taux d'actualisation en pourcentage?[/bold yellow]"))) / 100
    duree_vie_actif = (float(Prompt.ask("[bold yellow]Quelle est la durée de vie de l'actif en années?[/bold yellow]")))
    fermeture = Prompt.ask("[bold yellow]Est-ce qu'il y a une fermeture de catégorie? (Oui/Non)[/bold yellow]").strip().lower()

    vaeiacc = VAEIACC(cout_capital_initial, taux_acc, duree_vie_actif,
                      fermeture, taux_imposition, taux_actualisation,valeur_vente)

    vaeiacc_singulier = vaeiacc.calculateur_vaeiacc()

    console.print(f"\n-- VAEIACC de l'actif {i + 1} = {vaeiacc_singulier:.2f} --", style="bold green")

    valeur_vaeiacc += vaeiacc_singulier

    # addition impot à payer si gain en capital
    if valeur_vente > cout_capital_initial:
        impot = ValeurImpotGainCapital(valeur_vente,
                                                 cout_capital_initial, taux_imposition, taux_global, duree_projet)
        impot_singulier = -1 *  (impot.va_impot_gain_capital())
        impot_a_payer += impot_singulier

    # calcul économie ou perte sur fermeture
    if fermeture == "oui":
        ferm = ValeurFermeture(cout_capital_initial, taux_acc, duree_vie_actif,
                               r, taux_imposition, taux_global, duree_projet)
        ferm_singulier = ferm.va_economie_ou_perte()
        valeur_etape_7_8 += ferm_singulier


console.print(f"\n- Valeur totale du VAEIACC = {valeur_vaeiacc} -\n", style="bold green")

# étapes 4 et 5
nombre_valeur_recup = int(Prompt.ask("[bold yellow]Combien y a-t-il de valeur de récupération différente à la fin du projet? (ex. début de l'année n + 1 ou fin de l'année de fin du projet)[/bold yellow]"))
valeur_recup = 0

for i in range(nombre_valeur_recup):

    console.print(f"\n--- Valeur de récupération {i + 1} (étapes 4 et 5) ---", style="bold green")

    valeur_recuperation = float(Prompt.ask("[bold yellow]Quelle est le montant de cette valeur de récupération à la fin du projet?[/bold yellow]").replace(" ", ""))
    #non valide???? frequence_recup = str(Prompt.ask("[bold yellow]Est-ce que cette valeur de récupération est à la fin de l'année de fin du projet ou au début de l'année n + 1?[/bold yellow]"))

    recup = ValeurRevente(taux_global, duree_projet, valeur_recuperation)

    recup_singulier = recup.va_revente()

    console.print(f"\n-- Valeur actualisée du bloc de valeur de récupération {i + 1} = {recup_singulier:.2f} --", style="bold green")

    valeur_recup += recup_singulier

console.print(f"\n- Valeur actualisée totale de récupération = {valeur_recup} -\n", style="bold green")

# étape 6

gain_capital = Prompt.ask("[bold yellow]Y a-t-il un gain en capital sur des actifs autres que ceux à l'étape 3? (le terrain ne compte pas)[/bold yellow]").strip().lower()

if gain_capital == "oui":
    nombre_gain_capital = int(Prompt.ask("[bold yellow]Combien y a-t-il de gain en capital différent? (rappel: le terrain ne compte pas)[/bold yellow]"))
    for i in range(nombre_gain_capital):

        console.print(f"\n--- Gain en capital {i + 1} (étape 6) ---", style="bold green")

        cout_achat = float(Prompt.ask("[bold yellow]Quel est le coût d'achat de l'actif de ce gain en capital?[/bold yellow]").replace(" ", ""))
        cout_revente = float(Prompt.ask("[bold yellow]Quel est le prix de vente de l'actif de ce gain en capital[/bold yellow]").replace(" ", ""))

        gain = ValeurImpotGainCapital(cout_revente, cout_achat, taux_imposition, taux_global, duree_projet)

        gain_singulier = gain.va_impot_gain_capital()

        console.print(f"\n-- Valeur actualisée de l'impôt à payer sur le gain en capital {i + 1} = {gain_singulier:.2f} --", style="bold green")

        impot_a_payer += gain_singulier

console.print(f"\n- Valeur actualisée totale de l'impôt sur le gain en capital = {impot_a_payer} -\n", style="bold green")

# calcul final de la VAN

montant_final = (vaa_mise_de_fonds + vaa_annuites + valeur_vaeiacc +
                 valeur_recup + impot_a_payer + valeur_etape_7_8)

table = Table(title="Valeur Actualisée par Étape", show_lines=True)
table.add_column("Étape", justify="center", style="bold yellow")
table.add_column("Valeur", justify="right", style="bold green")

table.add_row("Étape 1", f"{vaa_mise_de_fonds:.2f}")
table.add_row("Étape 2", f"{vaa_annuites:.2f}")
table.add_row("Étape 3", f"{valeur_vaeiacc:.2f}")
table.add_row("Étape 4-5", f"{valeur_recup:.2f}")
table.add_row("Étape 6", f"{impot_a_payer:.2f}")
table.add_row("Étape 7-8", f"{valeur_etape_7_8 if valeur_etape_7_8 is not None else 'N/A':.2f}")
table.add_row("Valeur Totale", f"{montant_final:.2f}")

console.print(table)

input("\nAppuyez sur Entrée pour quitter...")