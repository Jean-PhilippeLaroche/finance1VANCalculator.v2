class ValeurRevente:

    def __init__(self, taux_global, duree_projet, valeur_recuperation, frequence):
        self.taux_global = taux_global
        self.duree_projet = duree_projet
        self.frequence = frequence
        self.valeur_recuperation = valeur_recuperation

    def va_revente(self):

        if self.frequence == "fin":
            va = self.valeur_recuperation / ((1 + self.taux_global) ** self.duree_projet)
            return va

        elif self.frequence == "début":
            va = (self.valeur_recuperation / ((1 + self.taux_global) ** self.duree_projet)) * (1 + self.taux_global)
            return va
        else:
            return ValueError("La fréquence n'est pas valide")