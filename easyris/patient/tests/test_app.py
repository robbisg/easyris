import unittest
import json
from mongoengine import connect
from easyris.utils import patient_db, user_db
from easyris.tests.test import EasyRisUnitTest
import easyris.app as easyris

#@unittest.skip("showing class skipping")
class EasyRisTest(EasyRisUnitTest):
    
            
    def test_search(self):
        
        self.login('mcaulo', 'massimo')
        rv = self.app.post(path='/patient/search', 
                           data=json.dumps({'first_name':'Fiorella'}),
                           content_type='application/json')

        response = json.loads(rv.data)

        patient = response[0]['data'][0]
        
        assert response[0]['user'] == 'mcaulo'
        assert 'Fiorella' == patient['first_name']
        assert 'Zabbo' == patient['last_name']
    
    def test_add(self):
        
        self.login('gaetano', 'gaetano')
        rv = self.app.post(path='/patient/insert', 
                           data=json.dumps({'first_name':'Roberto',
                                            'last_name':'Guidotti',
                                            'gender':'M',
                                            'birthplace':'SAN BENEDETTO DEL TRONTO',
                                            'city':'SAN BENEDETTO DEL TRONTO',
                                            'address':'Via della Liberazione 55',
                                            'phone_number':'3404752345',
                                            'nationality':'italiana',
                                            'cap':'64050',
                                            'birthdate':'1983-05-18T00:00:00.0Z'}),
                           content_type='application/json')
        response = json.loads(rv.data)
        print response
        assert response[0]['user'] == 'gaetano'
        assert response[0]['code'] == 100
        
if __name__ == '__main__':
    unittest.run()