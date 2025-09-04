class CalculateurAnnuitees:

    def __init__(self, taux_global, temps_debut,
                 temps_fin, montant_annuites, frequence, taux_croissance):
        self.taux_global = taux_global
        self.temps_debut = temps_debut
        self.temps_fin = temps_fin
        self.montant_annuites = montant_annuites
        self.frequence = frequence
        self.taux_croissance = taux_croissance

    def calculateur_VA_simple(self):

        if self.taux_global == 0:
            raise ValueError("Le taux d'intérêts ne peut pas être 0")

        duree = self.temps_fin - self.temps_debut

        if duree <= 0:
            raise ValueError("Si le montant n'apparait qu'une fois,"
                             " l'inclure dans la mise de fonds initiale ou valeur de revente")


        valeur_actualisee = (
                self.montant_annuites * (1 - (1 + self.taux_global) ** -duree) / self.taux_global
        )

        # Décaler dans le temps (si la série commence après t=0)
        valeur_actualisee /= (1 + self.taux_global) ** self.temps_debut

        if self.frequence == "début":
            valeur_actualisee = valeur_actualisee * (1 + self.taux_global)

        return valeur_actualisee

    def calculateur_VA_croissance(self):

        if self.taux_global == 0:
            raise ValueError("Le taux d'intérêts ne peut pas être 0")


        duree = self.temps_fin - self.temps_debut
        if duree <= 0:
            raise ValueError("Si le montant n'apparait qu'une fois, l'inclure dans la mise de fonds initiale")

        if self.taux_croissance == 0:
            # si croissance nulle → même résultat que VA simple
            return self.calculateur_VA_simple()

        # Formule VA d’une rente croissante
        valeur_actualisee = (
                (self.montant_annuites / (self.taux_global - self.taux_croissance))
                * (1 - ((1 + self.taux_croissance) / (1 + self.taux_global)) ** duree)
        )

        # Décalage dans le temps
        valeur_actualisee /= (1 + self.taux_global) ** self.temps_debut

        return valeur_actualisee