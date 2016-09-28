from easyris.tests.test import EasyRisUnitTest
import unittest
import json


class AuthenticationTest(EasyRisUnitTest):
    
        
    def test_login_logout(self):
        rv = self.login('mcaulo', 'massimo')
        print rv.data
        message = json.loads(rv.data)
        data = message[0]['data']
        print data
        # TODO: Change assertion with messages implemented
        assert data[0]['username'] == 'mcaulo'
        assert data[0]['roles'][0]['role_name'] == 'medico'

        rv = self.logout()
        
        assert rv.data == 'Logged out!'
        
    def test_bad_login(self):
        rv = self.login('mcaulo', 'daniele')
        print rv.data
        message = json.loads(rv.data)
        code = message[0]['code']
        assert code == 402
        
    def test_no_user(self):
        rv = self.login('savastano', 'pietro')
        print rv.data
        message = json.loads(rv.data)
        code = message[0]['code']
        assert code == 401
        

if __name__ == '__main__':
    unittest.run()