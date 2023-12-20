import unittest
import json
from bibilo import Bibliotheque 

class TestBibliotheque(unittest.TestCase):
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

        livres = [livre for livre in livres if livre['id'] != 'test123']

        with open('livres.json', 'w') as f:
            json.dump(livres, f, indent=2)

    def test_ajouter_livre(self):
        # Vérifier que le livre de test est ajouté correctement
        self.livre_test.ajouter_livre()

        with open('livres.json', 'r') as f:
            livres = json.load(f)

        livre_test_result = next((livre for livre in livres if livre['id'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 1)

    def test_afficher_stock(self):
        # Vérifier l'affichage du stock pour le livre de test
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.livre_test.afficher_stock('test123')
            self.assertEqual(mock_stdout.getvalue().strip(), "Matricule: test123, Exemplaires: 1")

    def test_emprunter(self):
        # Vérifier l'emprunt d'un exemplaire du livre de test
        self.livre_test.emprunter('test123', 1)

        with open('livres.json', 'r') as f:
            livres = json.load(f)

        livre_test_result = next((livre for livre in livres if livre['id'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 0)

    def test_restockage(self):
        # Vérifier le restockage de 3 exemplaires du livre de test
        self.livre_test.restockage('test123', 3)

        with open('livres.json', 'r') as f:
            livres = json.load(f)

        livre_test_result = next((livre for livre in livres if livre['id'] == 'test123'), None)
        self.assertIsNotNone(livre_test_result)
        self.assertEqual(livre_test_result['exemplaire'], 4)

if __name__ == '__main__':
    unittest.main()
