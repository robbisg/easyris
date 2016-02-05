from mongoengine import *
import unittest

from ..model import Patient
from ..controller import PatientController
from ...utils import patient_db

from datetime import datetime

@unittest.skip("showing class skipping")
class TestPatient(unittest.TestCase):
    
    def setUp(self):
        connect('easyris', port=27017)
        Patient.drop_collection()
        patient_db.main()
        
        
    def test_model(self):
        print "Testing model"
                
        me = Patient(first_name='Piero', 
                     last_name='Chiacchiaretta',
                     birthdate=datetime(year=1979, day=27, month=9), 
                     birthplace='PESCARA', 
                     #cf_code='CHCPRI79P27G482U',
                     gender="M", 
                     address='Via Aldo Moro, 114', 
                     city='SAN GIOVANNI TEATINO', 
                     #province='Chieti',
                     cap='66020', 
                     phone_number="3294946261", 
                     email='piero.chiacchiaretta@gmail.com', 
                     nationality='italiana')
    
        me.save()
        
        #result=db.get_collection('patients').find({'first_name' :me.first_name})
        query = Patient.objects(first_name=me.first_name,
                                last_name=me.last_name)
        
        result = query.next()
        test = result['first_name']
        self.assertEqual(me.first_name, str(test))
        
        test = result['codice_fiscale']
        self.assertEqual('CHCPRI79P27G482U', str(test))
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = str(Patient.objects().count()).zfill(4)
        true_ = str(yy)+str(mm)+fill_
        test = result['id_patient']
        
        #self.assertEqual(true_, test)
        self.assertEqual(me.province, "CH")
    
@unittest.skip("showing class skipping")        
class TestPatientController(unittest.TestCase):

    def setUp(self):
        
        connect('easyris', port=27017)
        Patient.drop_collection()
        patient_db.main() 
    
    def test_add(self):

        controller = PatientController()
        controller.create(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate="1983-05-18T13:08:00", 
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
        
    @unittest.skip("Issues on id") 
    def test_get(self):

        controller = PatientController()
        controller.get_patient("2015120001")
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "MDGTCL50C50H769Q")
        self.assertEqual(patient.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient.status, "Attivo")
        self.assertEqual(patient.age, 65)
        
    @unittest.skip("Issues on id")
    def test_update(self):

        controller = PatientController()
        controller.get_patient("2015120001")
        
        controller.update(first_name='Andrea',
                          birthdate="1983-04-07T13:08:00",
                          birthplace="AGRIGENTO")
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.id_patient, "2015120001")
        self.assertEqual(patient.codice_fiscale, "MDGNDR83D47A089X")
        self.assertEqual(patient.birthplace, "AGRIGENTO")
        self.assertEqual(patient.province, "AP")
        self.assertEqual(patient.age, 32)
        
    @unittest.skip("Issues on id")   
    def test_delete(self):

        controller = PatientController()
        controller.get_patient("2015120001")
        
        controller.delete(status='Revocato',
                          note="Problemi con il medico curante!")
        
        
        patient = controller._currentPatient
        
        self.assertNotEqual(patient.status, "Attivo")
        self.assertEqual(patient.status, "Revocato")


class TestPatientCases(unittest.TestCase):
    
    def setUp(self):
        connect('easyris', port=27017)
        Patient.drop_collection()
        patient_db.main() 
        
    def test_add_same_patient(self):
        
        controller = PatientController()
        res1 = controller.create(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate="1983-05-18T13:08:00", 
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
                      birthdate="1983-05-18T13:08:00", 
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
                      birthdate="1947-12-17T13:08:00", 
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
                      birthdate="1983-05-18T13:08:00", 
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
        patients = controller.search(first_name='Andrea',
                          last_name='Guidotti')
        
        id = patients[0].id_patient
        controller.get_patient(id)
        
        res3 = controller.update(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate="1983-05-18T13:08:00")
        
        self.assertEqual(res3, 'ERR')
                
        return
        
if __name__ == '__main__':
    unittest.main()
