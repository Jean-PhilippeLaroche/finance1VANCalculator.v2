class VAEIACC:

    def __init__(self, cout_capital_initial, taux_acc, duree_vie_actif,
                 fermeture, taux_imposition, taux_actualisation, valeur_vente):
        self.cout_capital_initial = cout_capital_initial
        self.taux_acc = taux_acc
        self.duree_vie_actif = duree_vie_actif
        self.fermeture = fermeture
        self.taux_imposition = taux_imposition
        self.taux_actualisation = taux_actualisation
        self.valeur_vente = valeur_vente
        self.r = min(self.cout_capital_initial, self.valeur_vente)

    def calculateur_vaeiacc(self):
        if self.fermeture == "oui":

            fnacc = (self.cout_capital_initial * (1 - (1.5 * self.taux_acc))
                     * ((1 - self.taux_acc) ** (self.duree_vie_actif - 1)))

            vaeiacc = (
                    (self.cout_capital_initial * self.taux_acc * self.taux_imposition)
                    / (self.taux_actualisation + self.taux_acc)
                    * ((1 + (1.5 * self.taux_actualisation))
                       / (1 + self.taux_actualisation))
                    - ((fnacc * self.taux_acc * self.taux_imposition)
                       / (self.taux_actualisation + self.taux_acc))
                    * (1 / ((1 + self.taux_actualisation) ** self.duree_vie_actif)
                       ))
            return vaeiacc

        else:

            vaeiacc = (
                    (self.cout_capital_initial * self.taux_acc * self.taux_imposition)
                    / (self.taux_actualisation + self.taux_acc)
                    * ((1 + (1.5 * self.taux_actualisation))
                    / (1 + self.taux_actualisation))
                    - ((self.r * self.taux_acc * self.taux_imposition)
                    / (self.taux_actualisation + self.taux_acc))
                    * (1 / ((1 + self.taux_actualisation) ** self.duree_vie_actif)
                        ))
            return vaeiacc