import json

class Bibliotheque:
    def __init__(self, identifiant, titre, auteur, annee):
        """
        PRE: - identifiant est une chaîne non vide
             - titre est une chaîne non vide
             - auteur est une chaîne non vide
             - annee est un entier positif
        POST: Un livre est ajouté à la bibliothèque avec les propriétés spécifiées.
        """
        self.verifier_parametres(identifiant, titre, auteur, annee)
        
        self.identifiant = identifiant
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.exemplaire = 1  # par défaut, un exemplaire lors de la création
        self.ajouter_livre()

    def verifier_parametres(self, identifiant, titre, auteur, annee):
        if not identifiant:
            raise ValueError("L'identifiant ne peut pas être une chaîne vide.")
        
        if not titre:
            raise ValueError("Le titre ne peut pas être une chaîne vide.")
        
        if not auteur:
            raise ValueError("L'auteur ne peut pas être une chaîne vide.")
        
        if not isinstance(annee, int):
            raise ValueError("L'année doit être un entier.")
        
        if annee <= 0:
            raise ValueError("L'année doit être un entier positif.")

    def ajouter_livre(self):
        """
        PRE: - exemplaire est un entier positif
        POST: Le livre est ajouté à la bibliothèque avec le nombre d'exemplaires spécifié.
        """
        if not isinstance(self.exemplaire, int) or self.exemplaire <= 0:
            raise ValueError("Le nombre d'exemplaires doit être un entier strictement positif.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        livre_existant = False
        for livre in livres:
            if livre.get('identifiant') == self.identifiant:
                livre['exemplaire'] += self.exemplaire
                livre_existant = True
                break

        if not livre_existant:
            nouveau_livre = {
                "identifiant": self.identifiant,
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
            if matricule is None or livre['identifiant'] == matricule:
                print(f"Matricule: {livre['identifiant']}, Exemplaires: {livre['exemplaire']}")

    def emprunter(self, matricule, nb_exemplaires):
        """
        PRE: - matricule est une chaîne non vide
             - nb_exemplaires est un entier positif
        POST: Le nombre d'exemplaires spécifié est emprunté pour le matricule spécifié.
        """
        if not isinstance(nb_exemplaires, int) or nb_exemplaires <= 0:
            raise ValueError("Le nombre d'exemplaires doit être un entier strictement positif.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise Exception("Aucun livre disponible.")

        for livre in livres:
            if livre['identifiant'] == matricule:
                try:
                    print(f"Avant emprunt : {livre['exemplaire']}")
                    if livre['exemplaire'] - nb_exemplaires < 0:
                        raise ValueError("Pas assez d'exemplaires disponibles.")
                    else:
                        livre['exemplaire'] -= nb_exemplaires
                        print(f"Après emprunt : {livre['exemplaire']}")
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
        if not isinstance(nb_exemplaires, int) or nb_exemplaires <= 0:
            raise ValueError("Le nombre d'exemplaires à rajouter doit être un entier strictement positif.")

        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            raise Exception("Aucun livre disponible.")

        livre_existant = False
        for livre in livres:
            if livre['identifiant'] == matricule:
                livre['exemplaire'] += nb_exemplaires
                livre_existant = True
                break

        if not livre_existant:
            raise ValueError(f"Le matricule '{matricule}' n'existe pas dans la bibliothèque.")

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)
