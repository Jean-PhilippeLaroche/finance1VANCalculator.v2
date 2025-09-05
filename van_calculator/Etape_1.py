class MiseFondsInitiale:

    def __init__(self, taux_global, temps, montant, position):
        self.taux_global = taux_global
        self.temps = temps
        self.montant = montant
        self.position = position

    def calculer_mise(self):
        if self.position == "fin":
            mise = self.montant * ((1 + self.taux_global) ** (-1 * self.temps))
            return mise

        elif self.position == "début":
            mise = (self.montant * ((1 + self.taux_global) ** (-1 * self.temps))) * (1 + self.taux_global)
            return mise

        else:
            raise ValueError("La fréquence n'est pas valide")

class ConvertisseurInterets:

    def __init__(self, taux, frequence):
        self.taux = taux
        self.frequence = frequence

    def convertisseur_taux(self):
        if self.frequence == "année":
            return self.taux
        elif self.frequence == "trimestre":
            return (1 + self.taux) ** 4 - 1
        elif self.frequence == "mois":
            return (1 + self.taux) ** 12 - 1
        elif self.frequence == "semaine":
            return (1 + self.taux) ** 52 - 1
        elif self.frequence == "jour":
            return (1 + self.taux) ** 365 - 1
        else:
            raise ValueError("Le taux n'est pas valide")