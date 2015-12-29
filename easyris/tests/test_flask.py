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

        
        
if __name__ == '__main__':
    unittest.main()