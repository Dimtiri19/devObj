import json

class Bibliothèque:
    def __init__(self, id, titre, auteur, annee):
        self.id = id
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.exemplaire = 1  # par défaut, un exemplaire lors de la création
        self.ajouter_livre()

    def ajouter_livre(self):
        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        livre_existant = False
        for livre in livres:
            if livre.get('id') == self.id:
                livre['exemplaire'] += 1
                livre_existant = True
                break

        if not livre_existant:
            nouveau_livre = {
                "id": self.id,
                "titre": self.titre,
                "auteur": self.auteur,
                "annee": self.annee,
                "exemplaire": 1
            }
            livres.append(nouveau_livre)

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)

    def afficher_stock(self, matricule=None):
        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        for livre in livres:
            if matricule is None or livre['id'] == matricule:
                print(f"Matricule: {livre['id']}, Exemplaires: {livre['exemplaire']}")

    def emprunter(self, matricule, nb_exemplaires):
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

# Exemple d'utilisation
nouveau_livre1 = Bibliothèque("aze", "Harry Potter à l'école des sorciers", "J.K. Rowling", 1997)
nouveau_livre2 = Bibliothèque("123", "Le Seigneur des Anneaux", "J.R.R. Tolkien", 1954)

# Afficher le stock
nouveau_livre1.afficher_stock()

# Emprunter 1 exemplaire du livre avec le matricule "aze"
try:
    nouveau_livre1.emprunter("aze", 1)
    print("Emprunt réussi.")
except Exception as e:
    print(f"Erreur: {e}")

# Afficher le stock après l'emprunt
nouveau_livre1.afficher_stock()
