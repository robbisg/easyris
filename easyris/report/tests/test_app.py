import unittest
import json
from easyris.report.controller import ReportController
from datetime import datetime
from easyris.examination import _get_correct_examinations
from easyris.tests import _get_current_patient_id
from easyris.tests.test import EasyRisUnitTest

import logging
logger = logging.getLogger("easyris_logger")

class ReportApiTest(EasyRisUnitTest):
    
    def setUp(self):
        
        self.controller = ReportController()
        super(ReportApiTest, self).setUp(n_examination=50, 
                                         n_patient=15, 
                                         n_report=10)
    
    #@unittest.skip("A me do search... nun me ne fott nu cazz")
    def test_search_patient(self):
        self.login('mcaulo', 'massimo')
        rv = self.app.get(path='/report/patient/'+self.get_id_patient_report()+'/suspended', 
                           data=json.dumps({}),
                           content_type='application/json')
        
        
        response = json.loads(rv.data)
        
        report = response[0]['data'][0]
        logger.debug(report)
        
        assert report['status_name'] == 'suspended'

        
    #@unittest.skip("reason")
    def test_save_create(self):
        self.login('mcaulo', 'massimo')
        
        examination_list = _get_correct_examinations()
        examination_json = [str(e.id) for e in examination_list]       
        
        rv = self.app.post(path='/report/save', 
                           data=json.dumps({'id_examination': examination_json,
                                            'report_text': "La dottoressa... Dottoressa",
                                            }),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        logger.debug(response)
        assert response[0]['code'] == 500
        
        id_report = str(response[0]['data'][0]['_id']['$oid'])
        logger.debug(id_report)
        
        rv = self.app.post(path='/report/search', 
                           data=json.dumps({'id':id_report}),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        logger.debug(response)
        report_text = response[0]['data'][0]['report_text']
        examination = response[0]['data'][0]['id_examination'][0]
        assert response[0]['code'] == 500
        assert report_text == "La dottoressa... Dottoressa"
        assert examination['status_name'] == 'reported'
        
    
    #@unittest.skip("reason")
    def test_save_update(self):
        self.login('mcaulo', 'massimo')
        
        id_report = self.get_id_report()
        
        rv = self.app.post(path='/report/save', 
                           data=json.dumps({'id': id_report,
                                            'report_text': "La pillola!",
                                            }),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        logger.debug(response)
        logger.debug(report)
        examination = response[0]['data'][0]['id_examination'][0]
        assert report['action_list'][-1]['action'] == "update"
        assert examination['status_name'] == 'closed'
    
    #@unittest.skip("reason")
    def test_close(self):
        self.login('mcaulo', 'massimo')
        
        id_report = self.get_id_report()        
        rv = self.app.post(path='/report/%s/close' % (id_report), 
                           data=json.dumps({}),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        logger.debug(response)
        
        report = response[0]['data'][0]
        
        assert response[0]['code'] == 500
        assert report['action_list'][-1]['action'] == "close"
        assert report['status_name'] == "closed"
        
    
    
    def test_delete(self):
        self.login('mcaulo', 'massimo')
        
        rv = self.app.get(path='/report')
        response = json.loads(rv.data)
        id_report = str(response[0]['data'][0]['_id']['$oid'])
        examination = response[0]['data'][0]['id_examination'][0]
        assert examination['status_name'] != 'completed'
        
        rv = self.app.post(path='/report/%s/delete' % (id_report), 
                           data=json.dumps({}),
                           content_type='application/json')
        response = json.loads(rv.data)
        assert response[0]['code'] == 500
        
        id_examination = examination['_id']['$oid']
        
        rv = self.app.post(path='/report/search', 
                           data=json.dumps({'id':str(id_report)}),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        assert response[0]['code'] == 501
    
    #@unittest.skip("reason")
    def test_open(self):
        self.login('mcaulo', 'massimo')
        
        id_report = self.get_id_report()        
        rv = self.app.post(path='/report/%s/close' % (id_report), 
                           data=json.dumps({}),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "closed"
        
        
        rv = self.app.post(path='/report/%s/open' % (id_report), 
                           data=json.dumps({'password':'massimo'}),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "opened"
        assert report['action_list'][-1]['action'] == "open"
    
    
    #@unittest.skip("reason")
    def test_open_wrong(self):
        self.login('mcaulo', 'massimo')
        
        id_report = self.get_id_report()        
        rv = self.app.post(path='/report/%s/close' % (id_report), 
                           data=json.dumps({}),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "closed"
        self.logout()
        
        self.login('valentina', 'valentina')
        rv = self.app.post(path='/report/%s/open' % (id_report), 
                           data=json.dumps({'password':'massimo'}),
                           content_type='application/json')
        response = json.loads(rv.data)

        assert response[0]['code'] == 501
        
        rv = self.app.post(path='/report/search', 
                           data=json.dumps({'id':id_report}),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        logger.debug(response)        
        assert report['status_name'] != "suspended"
        assert report['action_list'][-1]['action'] != "open"
    
    
    #@unittest.skip('reason')
    def test_single_examination(self):
        
        self.login('mcaulo', 'massimo')
        examination_list = _get_correct_examinations()
        examination_json = [str(e.id) for e in examination_list[:1]]
        
        rv = self.app.post(path='/report/save', 
                           data=json.dumps({'id_examination': examination_json,
                                            'report_text': "La dottoressa... Dottoressa",
                                            }),
                           content_type='application/json')
        
        response = json.loads(rv.data)
        assert response[0]['code'] == 500
    
    
    def test_process(self):
        self.login('mcaulo', 'massimo')
        
        # Creo un esame 
        examination_list = _get_correct_examinations()
        examination_json = [str(e.id) for e in examination_list]
        
        rv = self.app.post(path='/report/save', 
                           data=json.dumps({'id_examination': examination_json,
                                            'report_text': "La dottoressa... Dottoressa",
                                            }),
                           content_type='application/json')
        response = json.loads(rv.data)
        logger.debug(response)
        assert response[0]['code'] == 500
        id_report = str(response[0]['data'][0]['_id']['$oid'])
        
        # Lo modifico
        rv = self.app.post(path='/report/save', 
                           data=json.dumps({
                                            'report_text': "Oltre 15 anni",
                                            'id': id_report,
                                            }),
                           content_type='application/json')
        response = json.loads(rv.data)
        logger.debug(response)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "opened"
        assert report['report_text'] == "Oltre 15 anni"
        
        # Lo metto in pausa
        rv = self.app.post(path='/report/%s/pause' % (id_report), 
                           data=json.dumps({}),
                           content_type='application/json')
        response = json.loads(rv.data)
        logger.debug(response)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "suspended"
        
        
        # Lo riapro
        rv = self.app.post(path='/report/%s/open' % (id_report), 
                           data=json.dumps({'password':'massimo'
                                            }),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "opened"       
        
        # Lo chiudo
        rv = self.app.post(path='/report/%s/close' % (id_report), 
                   data=json.dumps({}),
                   content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "closed"    
        
        
        # Lo riapro dopo chiusura
        rv = self.app.post(path='/report/%s/open' % (id_report), 
                           data=json.dumps({'password':'massimo'}),
                           content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "opened"        
        assert report['action_list'][-1]['action'] == "open"       
        
        
        # Lo richiudo
        rv = self.app.post(path='/report/%s/close' % (id_report), 
                   data=json.dumps({}),
                   content_type='application/json')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        assert response[0]['code'] == 500
        assert report['status_name'] == "closed" 
        assert report['action_list'][-1]['action'] == "close"
        
    
    def get_id_report(self):
        
        rv = self.app.get(path='/report')
        response = json.loads(rv.data)
        id_report = str(response[0]['data'][0]['_id']['$oid'])
        return id_report

    
    def get_id_patient_report(self):
        rv = self.app.get(path='/report')
        response = json.loads(rv.data)
        report = response[0]['data'][0]
        id_patient = str(report['id_examination'][0]['id_patient']['id_patient'])
        return id_patient