import os
import easyris.app as easyris
import unittest
import tempfile
import json

class EasyRisTest(unittest.TestCase):
    
    def setUp(self):
        self.app = easyris.app.test_client()
        
    def test_home(self):
        rv = self.app.get('/')
        assert 'Hello EasyRIS!' == rv.data
        
    def test_search(self):
        rv = self.app.post(path='/patient/search', 
                           data=json.dumps({'first_name':'Tecla'}),
                           content_type='application/json')

        response = json.loads(rv.data)
        patient = response[0]
        
        assert 'Tecla' == patient['first_name']
        
if __name__ == '__main__':
    unittest.main()