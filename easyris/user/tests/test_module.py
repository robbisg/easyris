from easyris.tests.test import EasyRisUnitTest
import unittest
import json


class AuthenticationTest(EasyRisUnitTest):
    
        
    def test_login_logout(self):
        rv = self.login('mcaulo', 'massimo')

        data = json.loads(rv.data)
        print data
        # TODO: Change assertion with messages implemented
        assert data[0]['username'] == 'mcaulo'
        assert data[0]['roles'][0]['role_name'] == 'medico'

        rv = self.logout()
        
        assert rv.data == 'Logged out!'

if __name__ == '__main__':
    unittest.run()