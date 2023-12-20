import unittest
from unittest.mock import patch
import io
import json
from bibilo import Bibliotheque

class TestBibliotheque(unittest.TestCase):
    def test_creation_instance_erreur(self):
        # Teste la création d'une instance avec des paramètres incorrects
        with self.assertRaises(ValueError):
            Bibliotheque("", "Titre Test", "Auteur Test", 2022)  # ID vide

        with self.assertRaises(ValueError):
            Bibliotheque("test123", "", "Auteur Test", 2022)  # Titre vide

        with self.assertRaises(ValueError):
            Bibliotheque("test123", "Titre Test", "", 2022)  # Auteur vide

        with self.assertRaises(ValueError):
            Bibliotheque("test123", "Titre Test", "Auteur Test", -2022)  # Année négative

        with self.assertRaises(ValueError):
            Bibliotheque("test123", "Titre Test", "Auteur Test", "2022")  # Année non entière

    def test_ajouter_livre_erreur(self):
        # Teste la méthode ajouter_livre avec des paramètres incorrects
        livre_test = Bibliotheque("test123", "Titre Test", "Auteur Test", 2022)

        with self.assertRaises(ValueError):
            livre_test.exemplaire = 0
            livre_test.ajouter_livre()  # exemplaire <= 0

        with self.assertRaises(ValueError):
            livre_test.exemplaire = -1
            livre_test.ajouter_livre()  # exemplaire < 0

        with self.assertRaises(ValueError):
            livre_test.exemplaire = "1"
            livre_test.ajouter_livre()  # exemplaire non entier

    def test_emprunter_erreur(self):
        # Teste la méthode emprunter avec des paramètres incorrects
        livre_test = Bibliotheque("test123", "Titre Test", "Auteur Test", 2022)

        with self.assertRaises(ValueError):
            livre_test.emprunter('test123', 0)  # nb_exemplaires <= 0

        with self.assertRaises(ValueError):
            livre_test.emprunter('test123', -1)  # nb_exemplaires < 0

        with self.assertRaises(ValueError):
            livre_test.emprunter('test123', '1')  # nb_exemplaires non entier

    def test_restockage_erreur(self):
        # Teste la méthode restockage avec des paramètres incorrects
        livre_test = Bibliotheque("test123", "Titre Test", "Auteur Test", 2022)

        with self.assertRaises(ValueError):
            livre_test.restockage('test123', 0)  # nb_exemplaires <= 0

        with self.assertRaises(ValueError):
            livre_test.restockage('test123', -1)  # nb_exemplaires < 0

        with self.assertRaises(ValueError):
            livre_test.restockage('test123', '1')  # nb_exemplaires non entier

    def setUp(self):
        # Créer un livre pour les tests
        self.livre_test = Bibliotheque("test123", "Titre Test", "Auteur Test", 2022)

    def tearDown(self):
        # Supprimer le livre de test après chaque test
        try:
            with open('livres.json', 'r') as f:
                livres = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            livres = []

        livres = [livre for livre in livres if livre['identifiant'] != 'test123']

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)

    def test_ajouter_livre(self):
        # Vérifier que le livre de test est ajouté correctement
        self.livre_test.ajouter_livre()

        with open('livres.json', 'r') as f:
            livres = json.load(f)

        livre_test_result = next((livre for livre in livres if livre['identifiant'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 2)  # ajuster en fonction du comportement attendu

    def test_afficher_stock(self):
        # Vérifier l'affichage du stock pour le livre de test
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.livre_test.afficher_stock('test123')
            self.assertEqual(mock_stdout.getvalue().strip(), "Matricule: test123, Exemplaires: 1")

    def test_emprunter(self):
        # Vérifier l'emprunt d'un exemplaire du livre de test
        self.livre_test.emprunter('test123', 1)

        with open('livres.json', 'r') as f:
            livres = json.load(f)
        
        livre_test_result = next((livre for livre in livres if livre['identifiant'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 0)  # ajuster en fonction du comportement attendu

    def test_restockage(self):
        # Vérifier le restockage de 3 exemplaires du livre de test
        self.livre_test.restockage('test123', 3)

        with open('livres.json', 'r') as f:
            livres = json.load(f)

        livre_test_result = next((livre for livre in livres if livre['identifiant'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 4)  # ajuster en fonction du comportement attendu

if __name__ == '__main__':
    unittest.main()
