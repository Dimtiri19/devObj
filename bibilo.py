import json

class Bibliothèque:
    def __init__(self, id, titre, auteur, annee):
        """
        PRE: - id est une chaîne non vide
             - titre est une chaîne non vide
             - auteur est une chaîne non vide
             - annee est un entier positif
        POST: Un livre est ajouté à la bibliothèque avec les propriétés spécifiées.
        """
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.exemplaire = 1  # par défaut, un exemplaire lors de la création
        self.ajouter_livre()

    def ajouter_livre(self):
        """
        PRE: - exemplaire est un entier positif
        POST: Le livre est ajouté à la bibliothèque avec le nombre d'exemplaires spécifié.
        """
        if self.exemplaire <= 0:
            raise ValueError("Le nombre d'exemplaires doit être strictement supérieur à 0.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        livre_existant = False
        for livre in livres:
            if livre.get('id') == self.id:
                livre['exemplaire'] += self.exemplaire
                livre_existant = True
                break

        if not livre_existant:
            nouveau_livre = {
                "id": self.id,
                "titre": self.titre,
                "auteur": self.auteur,
                "annee": self.annee,
                "exemplaire": self.exemplaire
            }
            livres.append(nouveau_livre)

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)

    def afficher_stock(self, matricule=None):
        """
        PRE: Aucune
        POST: Les informations sur le stock sont affichées pour le matricule spécifié ou pour tous les livres.
        """
        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        for livre in livres:
            if matricule is None or livre['id'] == matricule:
                print(f"Matricule: {livre['id']}, Exemplaires: {livre['exemplaire']}")

    def emprunter(self, matricule, nb_exemplaires):
        """
        PRE: - matricule est une chaîne non vide
             - nb_exemplaires est un entier positif
        POST: Le nombre d'exemplaires spécifié est emprunté pour le matricule spécifié.
        """
        if nb_exemplaires <= 0:
            raise ValueError("Le nombre d'exemplaires doit être strictement supérieur à 0.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise Exception("Aucun livre disponible.")

        for livre in livres:
            if livre['id'] == matricule:
                try:
                    if livre['exemplaire'] - nb_exemplaires < 0:
                        raise ValueError("Pas assez d'exemplaires disponibles.")
                    else:
                        livre['exemplaire'] -= nb_exemplaires
                        break
                except ValueError as e:
                    raise e

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)

    def restockage(self, matricule, nb_exemplaires):
        """
        PRE: - matricule est une chaîne non vide
             - nb_exemplaires est un entier positif
        POST: Le nombre d'exemplaires spécifié est ajouté au stock pour le matricule spécifié.
        """
        if nb_exemplaires <= 0:
            raise ValueError("Le nombre d'exemplaires à rajouter doit être strictement supérieur à 0.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise Exception("Aucun livre disponible.")

        livre_existant = False
        for livre in livres:
            if livre['id'] == matricule:
                livre['exemplaire'] += nb_exemplaires
                livre_existant = True
                break

        if not livre_existant:
            raise ValueError(f"Le matricule '{matricule}' n'existe pas dans la bibliothèque.")

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)