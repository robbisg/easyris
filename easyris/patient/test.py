from mongoengine import *
import unittest
from model import Patient
from datetime import datetime

class TestStringMethods(unittest.TestCase):
    
    def test_upper(self):

        connect('easyris', port=27017)
    
        Patient.drop_collection()
        
        me = Patient(first_name='Piero', 
                     last_name='Chiacchiaretta',
                     birthdate=datetime(year=1979, day=27, month=9), 
                     birthplace='PESCARA', 
                     #cf_code='CHCPRI79P27G482U',
                     gender="M", 
                     address='Via Aldo Moro, 114', 
                     city='San Giovanni Teatino', 
                     #province='Chieti',
                     CAP='66020', 
                     phone_number="3294946261", 
                     email='piero.chiacchiaretta@gmail.com', 
                     nationality='italiana')
    
        me.save()
            
        you = Patient(first_name='Roberto', 
                      last_name='Guidotti',
                      birthdate=datetime(year=1983, day=18, month=5), 
                      birthplace='SAN BENEDETTO DEL TRONTO', 
                      gender="M", 
                      address='Via della Liberazione 55', 
                      city='San Benedetto del Tronto', 
                      #province='L\'Aquila',
                      CAP='63074', 
                      phone_number='2404751719', 
                      email='rob.guidotti@gmail.com', 
                      nationality='italiana')

    
        you.save()
    
        
        #result=db.get_collection('patients').find({'first_name' :me.first_name})
        query = Patient.objects(first_name=me.first_name)
        
        result = query.next()
        test = result['first_name']
        self.assertEqual(me.first_name, str(test))
        
        test = result['id_patient']
        self.assertEqual(me.id_patient, str(test))
        
        test = result['codice_fiscale']
        self.assertEqual('CHCPRI79P27G482U', str(test))
        
        
        

if __name__ == '__main__':
    unittest.main()
