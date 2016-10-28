import os
import easyris.app as easyris
import unittest
import json
from mongoengine import connect
from easyris.utils import database_setup
from datetime import datetime


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
    
    
    def setUp(self, n_loaded=5, **kwargs):
        
        database = 'test_easyris'
        port = 27017
        
        self.client = connect(database, port=port)
        easyris.app.config['PACS_URL'] = "http://localhost:6000//api/v1/orders"
        self.app = easyris.app.test_client(use_cookies=True)
        database_setup.run(database, port, n_loaded=n_loaded, **kwargs)
        
        
    def tearDown(self):
        self.logout()
        self.client.drop_database('test_easyris')
        pass
        


class EasyRisTest(unittest.TestCase):
    
    def setUp(self):
        self.app = easyris.app.test_client()
        
    def test_home(self):
        rv = self.app.get('/')
        assert 'Flask is up!' == rv.data

        
if __name__ == '__main__':
    unittest.run()