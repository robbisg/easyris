import unittest
import json
from mongoengine import connect
from easyris.utils import patient_db, user_db
from easyris.tests import _get_current_patient_id
from easyris.tests.test import EasyRisUnitTest
import easyris.app as easyris

#@unittest.skip("showing class skipping")
class ExaminationAPITest(EasyRisUnitTest):
    
    #@unittest.skip("skipping")
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
        
    @unittest.skip("Not yet implemented")
    def test_data(self):
        self.login('daniele', 'daniele')
        rv = self.app.post(path='/examination/search', 
                           data=json.dumps({'data_inserimento':'16/0'}),
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
        
    #@unittest.skip("No reasons")
    def test_create(self):
        
        self.login('gaetano', 'gaetano')
        rv = self.app.post(path='/examination/insert', 
                           data=json.dumps({"exams":[{"priority":"ALTA",
                                                      "modality":"MR",
                                                      "sala":"RM1.5T",
                                                      "distretto":"TORACE",
                                                      "nome":"RM TORACE SENZA MDC",
                                                      "selected":True},
                                                     {"priority":"ROUTINE",
                                                      "modality":"MR",
                                                      "sala":"RM1.5T",
                                                      "distretto":"ADDOME",
                                                      "nome":"RM SCROTO SENZA MDC",
                                                      "selected":True},
                                                     {"priority":"BASSA",
                                                      "modality":"MR",
                                                      "sala":"RM1.5T",
                                                      "distretto":"ESTREMITA/ARTICOLAZIONI",
                                                      "nome":"RM GOMITO E AVAMBRACCIO SENZA MDC",
                                                      "selected":True}],
                                            "id_patient":_get_current_patient_id(),
                                            "data_inserimento":"2016-08-11T17:25:38.117Z",
                                            "medico_richiedente":"frisco frasco",
                                            #"accession_number":"40404040"
                                            }),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        print response
        assert response[0]['message'] == 'Examination created correctly'
        
        
        rv = self.app.post(path='/examination/search', 
                           data=json.dumps({'id_patient':_get_current_patient_id(),
                                            "medico_richiedente":"frisco frasco"}),
                           content_type='application/json')
        response = json.loads(rv.data)
        
        print response[0]['data']
        
        examination = response[0]['data']
        
        assert len(examination) == 3
        assert examination[0]['id_typology']['distretto_corporeo'] == "TORACE"
        assert examination[1]['id_typology']['distretto_corporeo'] == "ADDOME"
        assert examination[2]['id_typology']['distretto_corporeo'] == "ESTREMITA/ARTICOLAZIONI"        
        
        


if __name__ == '__main__':
    unittest.run()