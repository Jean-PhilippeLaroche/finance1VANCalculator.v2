class ValeurFermeture:

    def __init__(self, cout_capital_initial, taux_acc, duree_vie_actif, r, taux_imposition, taux_global, duree_projet):

        self.taux_global = taux_global
        self.duree_projet = duree_projet
        self.cout_capital_initial = cout_capital_initial
        self.taux_acc = taux_acc
        self.duree_vie_actif = duree_vie_actif
        self.r = r
        self.taux_imposition = taux_imposition

    def va_economie_ou_perte(self):
        fnacc = (self.cout_capital_initial * (1 - (1.5 * self.taux_acc))
                     * ((1 - self.taux_acc) ** (self.duree_vie_actif - 1)))
        r = self.r
        taux_imposition = self.taux_imposition
        taux_global = self.taux_global
        duree = self.duree_projet

        va = ((fnacc - r) * taux_imposition) / ((1 + taux_global) ** (duree + 1))
        return va