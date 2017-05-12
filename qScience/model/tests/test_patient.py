import unittest

from qScience.model.patient import Patient
from qScience.controller.patient import PatientController

from datetime import datetime
from qScience.tests.test import EasyRisUnitTest

 
#@unittest.skip("showing class skipping")        
class TestPatientController(EasyRisUnitTest):
    
    def setUp(self, n_loaded=5, **kwargs):
        EasyRisUnitTest.setUp(self, n_loaded=n_loaded, **kwargs)
        self.controller = PatientController()
    
    """
    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        database_setup.run(database, port, n_loaded=5)
        self.controller = PatientController()
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
    """   
    
    def test_add(self):

        
        self.controller.create(first_name='Roberto', 
                              last_name='Guidotti',
                              birthdate="1983-05-18T13:08:00.0Z", 
                              birthplace='SAN BENEDETTO DEL TRONTO', 
                              gender="M", 
                              address='Via della Liberazione 55', 
                              city='SAN BENEDETTO DEL TRONTO', 
                              cap='63074', 
                              phone_number='3404751719', 
                              email='rob.guidotti@gmail.com', 
                              nationality='italiana')
        
        
        message = self.controller.read(first_name="Roberto",
                                      last_name="Guidotti")
        
        
        
        self.assertEqual(message.header.code, 100)
        self.assertEqual(self.controller._currentPatient.first_name, "Roberto")
        
        patient_app = message.data[0]
        
        self.assertEqual(patient_app.codice_fiscale, "GDTRRT83E18H769W")
        self.assertEqual(patient_app.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient_app.status, "Attivo")
        #self.assertEqual(patient_app.age, 32)
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = str(Patient.objects().count()).zfill(4)
        true_ = str(yy)+str(mm)+fill_
        
        #self.assertEqual(true_, patient_app.id_patient)
        
    #@unittest.skip("Issues on id") 
    def test_get(self):

        message = self.controller.read(first_name='Tecla')
        
        self.controller._get_patient(message.data[0].id_patient)
        
        patient = self.controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "MDGTCL50C50H769Q")
        self.assertEqual(patient.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient.status, "Attivo")

        
    #@unittest.skip("Issues on id")
    def test_update(self):

        message = self.controller.read(first_name='Tecla')
        self.controller._get_patient(message.data[0].id_patient)
        
        
        self.controller.update(first_name='Andrea',
                              birthdate="1983-04-07T13:08:00.0Z",
                              birthplace="AGRIGENTO")
        
        patient = self.controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "MDGNDR83D47A089X")
        self.assertEqual(patient.birthplace, "AGRIGENTO")
        self.assertEqual(patient.province, "AP")

        
    #@unittest.skip("Issues on id")   
    def test_delete(self):
        
        message = self.controller.read(first_name='Tecla')
        self.controller._get_patient(message.data[0].id_patient)
        
        self.controller.delete(status='Revocato',
                               note="Problemi con il medico curante!")
        
        
        patient = self.controller._currentPatient
        
        self.assertNotEqual(patient.status, "Attivo")
        self.assertEqual(patient.status, "Revocato")


        
    
class TestPatientCases(EasyRisUnitTest):
    
    def setUp(self, n_loaded=5, **kwargs):
        EasyRisUnitTest.setUp(self, n_loaded=n_loaded, **kwargs)
        self.controller = PatientController()
    """
    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        patient_db.run(database, port=port, n_loaded=5)
        user_db.run(database, port)
        self.controller = PatientController()
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
    """   

    def test_add_same_patient(self):
        
        
        message_ok = self.controller.create(first_name='Roberto', 
                                              last_name='Guidotti',
                                              birthdate="1983-05-18T13:08:00.0Z", 
                                              birthplace='SAN BENEDETTO DEL TRONTO', 
                                              gender="M", 
                                              address='Via della Liberazione 55', 
                                              city='SAN BENEDETTO DEL TRONTO', 
                                              cap='63074', 
                                              phone_number='3404751719', 
                                              email='rob.guidotti@gmail.com', 
                                              nationality='italiana')
        
        message_bad = self.controller.create(first_name='Roberto', 
                                              last_name='Guidotti',
                                              birthdate="1983-05-18T13:08:00.0Z", 
                                              birthplace='SAN BENEDETTO DEL TRONTO', 
                                              gender="M", 
                                              address='Via della Liberazione 55', 
                                              city='SAN BENEDETTO DEL TRONTO', 
                                              cap='63074', 
                                              phone_number='3404751719', 
                                              email='rob.guidotti@gmail.com', 
                                              nationality='italiana')
        
        self.assertEqual(message_bad.header.code, 102)
        self.assertEqual(message_ok.header.code, 100)
        
        return
    
    def test_bad_research(self):
        
        return
    
    def test_update_same_patient(self):
        
        
        
        message1 = self.controller.create(first_name='Andrea', 
                                          last_name='Guidotti',
                                          birthdate="1947-12-17T13:08:00.0Z", 
                                          birthplace='SAN BENEDETTO DEL TRONTO', 
                                          gender="M", 
                                          address='Via della Liberazione 55', 
                                          city='SAN BENEDETTO DEL TRONTO', 
                                          cap='63074',
                                          phone_number='3404751719', 
                                          email='rob.guidotti@gmail.com', 
                                          nationality='italiana')
        
        message2 = self.controller.create(first_name='Roberto', 
                                          last_name='Guidotti',
                                          birthdate="1983-05-18T13:08:00.0Z", 
                                          birthplace='SAN BENEDETTO DEL TRONTO', 
                                          gender="M", 
                                          address='Via della Liberazione 55', 
                                          city='SAN BENEDETTO DEL TRONTO', 
                                          cap='63074', 
                                          phone_number='3404751719', 
                                          email='rob.guidotti@gmail.com', 
                                          nationality='italiana')
        
        self.assertEqual(message1.header.code, 100)
        self.assertEqual(message2.header.code, 100)
        message = self.controller.read(first_name='Andrea',
                                       last_name='Guidotti')
        
        id_ = message.data[0].id_patient
        _ = self.controller._get_patient(id_)
        
        message3 = self.controller.update(first_name='Roberto', 
                                          last_name='Guidotti',
                                          birthdate="1983-05-18T13:08:00.0Z")
        
        self.assertEqual(message3.header.code, 102)
                
        return
        
if __name__ == '__main__':
    unittest.run()
