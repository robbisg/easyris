from easyris.tests.test import EasyRisAppTest
import unittest
import json

import logging
logger = logging.getLogger('easyris_logger')


class AuthenticationTest(EasyRisAppTest):
    
        
    def test_login_logout(self):
        rv = self.login('mcaulo', 'massimo')
        logger.debug(rv.data)
        message = json.loads(rv.data)
        data = message[0]['data']
        logger.debug(data)
        # TODO: Change assertion with messages implemented
        assert data[0]['username'] == 'mcaulo'
        assert data[0]['roles'][0]['role_name'] == 'medico'

        rv = self.logout()
        response = json.loads(rv.data)
        
        assert response[0]['code'] == 400
        
        
    def test_bad_login(self):
        rv = self.login('mcaulo', 'daniele')
        logger.debug(rv.data)
        message = json.loads(rv.data)
        code = message[0]['code']
        assert code == 402
        
    def test_no_user(self):
        rv = self.login('savastano', 'pietro')
        logger.debug(rv.data)
        message = json.loads(rv.data)
        code = message[0]['code']
        assert code == 401
        

if __name__ == '__main__':
    unittest.run()