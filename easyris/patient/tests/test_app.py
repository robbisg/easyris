import os
import easyris.app as easyris
import unittest
import tempfile
import json

#@unittest.skip("showing class skipping")
class EasyRisTest(unittest.TestCase):
    
    def setUp(self):
        self.app = easyris.app.test_client()
        
        
    def test_search(self):
        
        rv = self.app.post(path='/patient/search', 
                           data=json.dumps({'first_name':'Fiorella'}),
                           content_type='application/json')
        print rv.data
        response = json.loads(rv.data)
        patient = response[0]
        print response
        assert 'Fiorella' == patient['first_name']
        assert 'Zabbo' == patient['last_name']
    
    def test_add(self):
        
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
        
        print rv
        
        assert rv.data == "OK"
        
if __name__ == '__main__':
    unittest.main()