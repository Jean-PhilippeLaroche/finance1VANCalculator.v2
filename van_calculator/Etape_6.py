class ValeurImpotGainCapital:
    def __init__(self, valeur_vente, cout_capital_initial,
                 taux_imposition, taux_global, duree_projet):
        self.valeur_vente = valeur_vente
        self.cout_capital_initial = cout_capital_initial
        self.taux_imposition = taux_imposition
        self.taux_global = taux_global
        self.duree_projet = duree_projet


    def va_impot_gain_capital(self):
        va = (
            -1 * (((self.valeur_vente - self.cout_capital_initial)
                   * 0.6667 * self.taux_imposition)
                  / ((1 + self.taux_global) ** (self.duree_projet + 1)))
        )
        return va