from django.test import TestCase
from piemonteStructure.models import Diretor, Gerente

class DiretorModelTestCase(TestCase):
    def setUp(self):
        self.diretor = Diretor(
            nome = 'José Augusto',
            sobrenome = 'Dias',
            matricula = 'JA123456',
            cargo = 'diretor',
            email = 'adm@piemontecred.com.br',
            email_sent = False
        )
    
    def test_check_directors_attributes(self):
        self.assertEqual(self.diretor.nome, 'José Augusto')
        self.assertEqual(self.diretor.sobrenome, 'Dias')
        self.assertEqual(self.diretor.matricula, 'JA123456')
        self.assertEqual(self.diretor.cargo, 'diretor')
        self.assertEqual(self.diretor.email, 'adm@piemontecred.com.br')
        self.assertEqual(self.diretor.email_sent, False)

class GerenteModelTestCase(TestCase):
    def setUp(self):
        self.gerente = Gerente(
            nome = 'Reginaldo',
            sobrenome = 'Rossi',
            matricula = 'RR123456',
            cargo = 'gerente',
            email = 'adm@piemontecred.com.br',
            email_sent = False
        )
    
    def test_check_managers_attributes(self):
        self.assertEqual(self.gerente.nome, 'Reginaldo')
        self.assertEqual(self.gerente.sobrenome, 'Rossi')
        self.assertEqual(self.gerente.matricula, 'RR123456')
        self.assertEqual(self.gerente.cargo, 'gerente')
        self.assertEqual(self.gerente.email, 'adm@piemontecred.com.br')
        self.assertEqual(self.gerente.email_sent, False)
