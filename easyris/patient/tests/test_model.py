from mongoengine import *
import unittest

from ..model import Patient
from ..controller import PatientController
from ...utils import patient_db, user_db

from datetime import datetime

 
#@unittest.skip("showing class skipping")        
class TestPatientController(unittest.TestCase):

    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        patient_db.run(database, port=port, n_loaded=5)
        user_db.run(database, port)
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
        
    
    def test_add(self):

        controller = PatientController()
        controller.create(first_name='Roberto', 
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
        
        
        query = Patient.objects(first_name="Roberto",
                                last_name="Guidotti")
        
        self.assertNotEqual(query.count(), 0)
        self.assertEqual(controller._currentPatient.first_name, "Roberto")
        
        patient_app = query.first()
        
        self.assertEqual(patient_app.codice_fiscale, "GDTRRT83E18H769W")
        self.assertEqual(patient_app.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient_app.status, "Attivo")
        self.assertEqual(patient_app.age, 32)
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = str(Patient.objects().count()).zfill(4)
        true_ = str(yy)+str(mm)+fill_
        
        #self.assertEqual(true_, patient_app.id_patient)
        
    #@unittest.skip("Issues on id") 
    def test_get(self):

        controller = PatientController()
        list_ = controller.read(first_name='Tecla')
        controller.get_patient(list_[0].id_patient)
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "MDGTCL50C50H769Q")
        self.assertEqual(patient.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient.status, "Attivo")

        
    #@unittest.skip("Issues on id")
    def test_update(self):

        controller = PatientController()
        list_ = controller.read(first_name='Tecla')
        controller.get_patient(list_[0].id_patient)
        
        
        controller.update(first_name='Andrea',
                          birthdate="1983-04-07T13:08:00.0Z",
                          birthplace="AGRIGENTO")
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "MDGNDR83D47A089X")
        self.assertEqual(patient.birthplace, "AGRIGENTO")
        self.assertEqual(patient.province, "AP")

        
    #@unittest.skip("Issues on id")   
    def test_delete(self):

        controller = PatientController()
        list_ = controller.read(first_name='Tecla')
        controller.get_patient(list_[0].id_patient)
        
        controller.delete(status='Revocato',
                          note="Problemi con il medico curante!")
        
        
        patient = controller._currentPatient
        
        self.assertNotEqual(patient.status, "Attivo")
        self.assertEqual(patient.status, "Revocato")


        
    
class TestPatientCases(unittest.TestCase):
    
    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        patient_db.run(database, port=port, n_loaded=5)
        user_db.run(database, port)
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')
        

    def test_add_same_patient(self):
        
        controller = PatientController()
        res1 = controller.create(first_name='Roberto', 
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
        
        res2 = controller.create(first_name='Roberto', 
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
        
        self.assertEqual(res1, 'OK')
        self.assertEqual(res2, "ERR")
        
        return
    
    def test_bad_research(self):
        
        return
    
    def test_update_same_patient(self):
        
        controller = PatientController()
        
        res1 = controller.create(first_name='Andrea', 
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
        
        res2 = controller.create(first_name='Roberto', 
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
        
        self.assertEqual(res1, 'OK')
        self.assertEqual(res2, 'OK')
        patients = controller.read(first_name='Andrea',
                          last_name='Guidotti')
        
        id_ = patients[0].id_patient
        controller.get_patient(id_)
        
        res3 = controller.update(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate="1983-05-18T13:08:00.0Z")
        
        self.assertEqual(res3, 'ERR')
                
        return
        
if __name__ == '__main__':
    unittest.run()
