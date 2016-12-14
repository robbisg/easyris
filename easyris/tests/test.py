import os
from easyris import create_app
import unittest
import json
from mongoengine import connect
from datetime import datetime



class EasyRisUnitTest(unittest.TestCase):
    
    
    def setUp(self, n_loaded=5, **kwargs):
        # TODO: Check overriding in other classes
        from easyris.base.database import parse_db_config, \
                                            restore_db,\
                                            easyris_connect
        db_filename = "config/database_test.cfg"
        db_config = parse_db_config(db_filename)
        conn = easyris_connect(**db_config)
        self.client = conn      
          
        restore_db(db_filename)
        
        
    def tearDown(self):
        print 'Removing test database.'
        self.client.drop_database('easyris_test')
        pass


class EasyRisAppTest(unittest.TestCase):
    
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
        from easyris.base.database import restore_db
        db_filename = "config/database_test.cfg"
        easyr = create_app(database_cfg=db_filename)
        
        restore_db(db_filename)
        
        self.easyris = easyr
        self.app = easyr.test_client(use_cookies=True)
        
        
    def tearDown(self):
        self.logout()
        print 'Remove test database.'
        self.easyris.config['DB_CLIENT'].drop_database('easyris_test')
        



class EasyRisTest(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app().test_client()
        print self.app
        
    def test_home(self):
        rv = self.app.get('/')
        assert 'Flask is up!' == rv.data

        
if __name__ == '__main__':
    unittest.run()