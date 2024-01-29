from django.test import TestCase
from piemonteStructure.models import Diretor, Gerente, Supervisor, Agente

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
            ativo = True,
            email = 'adm@piemontecred.com.br',
            email_sent = False
        )
    
    def test_check_managers_attributes(self):
        self.assertEqual(self.gerente.nome, 'Reginaldo')
        self.assertEqual(self.gerente.sobrenome, 'Rossi')
        self.assertEqual(self.gerente.matricula, 'RR123456')
        self.assertEqual(self.gerente.cargo, 'gerente')
        self.assertEqual(self.gerente.ativo, True)
        self.assertEqual(self.gerente.email, 'adm@piemontecred.com.br')
        self.assertEqual(self.gerente.email_sent, False)

class SupervisorModelTestCase(TestCase):
    def setUp(self):
        self.gerente = Gerente(
            
            id = 1,
            nome = 'Reginaldo',
            sobrenome = 'Rossi',
            matricula = 'RR123456',
            cargo = 'gerente',
            email = 'adm@piemontecred.com.br',
            email_sent = False
        )

        self.supervisor = Supervisor(
            nome = 'Roberto Carlos',
            sobrenome = 'Braga', 
            matricula = 'RB123456', 
            cargo = 'supervisor',
            ativo = True,
            gerente = self.gerente,
            email = 'adm@piemontecred.com.br',
            email_sent = False)
        
    
    def test_check_supervisor_attributes(self):
        self.assertEqual(self.supervisor.nome, 'Roberto Carlos')
        self.assertEqual(self.supervisor.sobrenome, 'Braga')
        self.assertEqual(self.supervisor.matricula, 'RB123456')
        self.assertEqual(self.supervisor.cargo, 'supervisor')
        self.assertEqual(self.supervisor.ativo, True)
        self.assertEqual(self.supervisor.gerente, self.gerente)
        self.assertEqual(self.supervisor.email, 'adm@piemontecred.com.br')
        self.assertEqual(self.supervisor.email_sent, False)

class AgenteModelTesteCase(TestCase):
    def setUp(self):
        self.gerente = Gerente(
                nome = 'Reginaldo',
                sobrenome = 'Rossi',
                matricula = 'RR123456',
                cargo = 'gerente',
                ativo = True,
                email = 'adm@piemontecred.com.br',
                email_sent = False
            )
        

        self.supervisor = Supervisor(
            nome = 'Roberto Carlos',
            sobrenome = 'Braga', 
            matricula = 'RB123456', 
            cargo = 'supervisor',
            ativo = True,
            gerente = self.gerente,
            email = 'adm@piemontecred.com.br',
            email_sent = False)
        
        self.agente = Agente(
            nome = 'Odair José',
            sobrenome = 'De Araújo',
            matricula='OA123456',
            cargo = 'agente',
            gerente = self.gerente,
            supervisor = self.supervisor, 
            email = 'adm@piemontecred.com.br',
            email_sent = False
        )
    
    def test_check_agent_attributes(self):
        self.assertEqual(self.agente.nome, 'Odair José')
        self.assertEqual(self.agente.sobrenome, 'De Araújo')
        self.assertEqual(self.agente.matricula, 'OA123456')
        self.assertEqual(self.agente.cargo, 'agente')
        self.assertEqual(self.agente.gerente, self.gerente)
        self.assertEqual(self.agente.supervisor, self.supervisor)
        self.assertEqual(self.agente.email, 'adm@piemontecred.com.br')
        self.assertEqual(self.agente.email_sent, False)