import unittest
import json
from mongoengine import connect
from easyris.utils import patient_db, user_db
from easyris.tests.test import EasyRisUnitTest
import easyris.app as easyris

#@unittest.skip("showing class skipping")
class ExaminationAPITest(EasyRisUnitTest):
    
    
    def test_search(self):
        
        self.login('daniele', 'daniele')
        rv = self.app.post(path='/examination/search', 
                           data=json.dumps({'medico_richiedente':'Mauro Caffarini'}),
                           content_type='application/json')

        response = json.loads(rv.data)

        examination = response[0]['data'][0]
        #print examination
        
        assert response[0]['user'] == 'daniele'
        assert examination['codice_esenzione'] == '67577568'
        
    
    #@unittest.skip("showing class skipping")
    def test_status(self):
        
        self.login('daniele', 'daniele')
        rv = self.app.post(path='/examination/search', 
                           data=json.dumps({'medico_richiedente':'Mauro Caffarini'}),
                           content_type='application/json')
        response = json.loads(rv.data)
        examination = response[0]['data'][0]
        id_examination = str(examination['_id']['$oid'])
        
        
        def post_status(name, id_examination):
            rv = self.app.post(path='/examination/%s/%s' % (id_examination, name),
                           content_type='application/json')
            response = json.loads(rv.data)
            examination = response[0]['data'][0]
            print examination
            return examination
        
        ####### Now testing status api ########
 
        examination = post_status('start', id_examination)
        print '--------- '+examination['status_name']
        assert examination['status_name'] == 'scheduled'
        
        examination = post_status('go', id_examination)
        print '--------- '+examination['status_name']
        assert examination['status_name'] == 'running'
        
        examination = post_status('stop', id_examination)
        assert examination['status_name'] == 'rescheduled'
        
        examination = post_status('go', id_examination)
        examination = post_status('pause', id_examination)
        assert examination['status_name'] == 'incomplete'
        
        examination = post_status('stop', id_examination)
        assert examination['status_name'] == 'incomplete'
        
        examination = post_status('start', id_examination)
        examination = post_status('go', id_examination)
        examination = post_status('finish', id_examination)
        assert examination['status_name'] == 'completed'
        
        self.logout()
        self.login('mcaulo', 'massimo')
        examination = post_status('eject', id_examination)
        assert examination['status_name'] == 'reported'


if __name__ == '__main__':
    unittest.run()