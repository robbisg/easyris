from mongoengine import *
import unittest

from ..model import Patient
from ..controller import PatientController

from datetime import datetime

class TestPatient(unittest.TestCase):
    
    connect('easyris', port=27017)
    
    def test_model(self):
        print "Testing model"
        Patient.drop_collection()
        
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
        """   
        you = Patient(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate=datetime(year=1983, day=18, month=5), 
                      birthplace='SAN BENEDETTO DEL TRONTO', 
                      gender="M", 
                      address='Via della Liberazione 55', 
                      city='San Benedetto del Tronto', 
                      #province='L\'Aquila',
                      cap='63074', 
                      phone_number='2404751719', 
                      email='rob.guidotti@gmail.com', 
                      nationality='italiana')

    
        you.save()
        """
        
        #result=db.get_collection('patients').find({'first_name' :me.first_name})
        query = Patient.objects(first_name=me.first_name)
        
        result = query.next()
        test = result['first_name']
        self.assertEqual(me.first_name, str(test))
        
        test = result['id_patient']
        self.assertEqual(me.id_patient, str(test))
        
        test = result['codice_fiscale']
        self.assertEqual('CHCPRI79P27G482U', str(test))
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = '0001'
        true_ = str(yy)+str(mm)+fill_
        test = result['id_patient']
        
        self.assertEqual(true_, test)
        self.assertEqual(me.province, "CH")
    
        
class TestPatientController(unittest.TestCase):
    
    
    def test_add(self):
        print "Testing add function"
        controller = PatientController()
        controller.add(first_name='Roberto', 
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
        
        
        query = Patient.objects(first_name="Roberto")
        
        self.assertNotEqual(query.count(), 0)
        self.assertEqual(controller._currentPatient.first_name, "Roberto")
        
        patient = query.first()
        
        self.assertEqual(patient.codice_fiscale, "GDTRRT83E18H769W")
        self.assertEqual(patient.city, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient.status, "Attivo")
        self.assertEqual(patient.age, 32)
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = '0002'
        true_ = str(yy)+str(mm)+fill_
        
        self.assertEqual(true_, patient.id_patient)
        
        
    def test_get(self):
        print "Testing get function"
        controller = PatientController()
        controller.get_patient("2015120002")
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.codice_fiscale, "GDTRRT83E18H769W")
        self.assertEqual(patient.birthplace, "SAN BENEDETTO DEL TRONTO")
        self.assertEqual(patient.status, "Revocato")
        self.assertEqual(patient.age, 32)
        
        yy = datetime.now().year
        mm = datetime.now().month
        fill_ = '0002'
        true_ = str(yy)+str(mm)+fill_
        
        self.assertEqual(true_, patient.id_patient)
       
    def test_update(self):
        print "Testing update function"
        controller = PatientController()
        controller.get_patient("2015120002")
        
        controller.update(first_name='Andrea',
                          birthdate="1983-04-07T13:08:00",
                          birthplace="AGRIGENTO")
        
        patient = controller._currentPatient
        
        self.assertEqual(patient.id_patient, "2015120002")
        self.assertEqual(patient.codice_fiscale, "GDTNDR83D07A089P")
        self.assertEqual(patient.birthplace, "AGRIGENTO")
        self.assertEqual(patient.province, "AP")
        self.assertEqual(patient.status, "Revocato")
        self.assertEqual(patient.age, 32)
        
        
    def test_delete(self):
        print "Testing delete function"
        controller = PatientController()
        controller.get_patient("2015120002")
        
        controller.delete(status='Revocato',
                          note="Problemi con il medico curante!")
        
        
        patient = controller._currentPatient
        
        self.assertNotEqual(patient.status, "Attivo")
        self.assertEqual(patient.status, "Revocato")
        
        
        
if __name__ == '__main__':
    unittest.main()
