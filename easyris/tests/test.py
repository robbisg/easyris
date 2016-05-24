import os
import easyris.app as easyris
import unittest
import json
from mongoengine import connect
from easyris.utils import patient_db, user_db


class EasyRisUnitTest(unittest.TestCase):
    
    def login(self, username, password):
        return self.app.post('/login', 
                            data=json.dumps(
                                            dict(
                                                 username=username,
                                                 password=password
                                                 )
                                            ), 
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    
    def setUp(self):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        self.app = easyris.app.test_client(use_cookies=True)
        patient_db.run(database, port=port, n_loaded=5)
        user_db.run(database, port)
        
        
    def tearDown(self):
        self.client.drop_database('test_easyris')



class EasyRisTest(unittest.TestCase):
    
    def setUp(self):
        self.app = easyris.app.test_client()
        
    def test_home(self):
        rv = self.app.get('/')
        assert 'Flask is up!' == rv.data

        
if __name__ == '__main__':
    unittest.run()