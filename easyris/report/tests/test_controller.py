from mongoengine import *
from easyris.user.model import User
from easyris.examination.model import Examination
from easyris.report.model import Report
from easyris.tests.test import EasyRisUnitTest
from easyris.report.controller import ReportController
from collections import Counter
from easyris.examination import _get_correct_examinations, _get_random_examinations
import unittest

class TestReportController(EasyRisUnitTest):
    
    def setUp(self):
        
        self.controller = ReportController()
        super(TestReportController, self).setUp(n_loaded=50)
            

    #@unittest.skip("Just passed")
    def test_create(self):
        user = User.objects(username='mcaulo').first()
        self.controller.user = user
        query = dict()
        
        examination_list = _get_correct_examinations()
        print [str(e.data_inserimento) for e in examination_list]
        
        query['action'] = 'create'
        query['user'] = 'mcaulo'
        query['report_text'] = "Do cazz e sciut l Acquafan"
        query['id_examination'] = [str(e.id) for e in examination_list]
        
        message = self.controller.create(**query)
        print "Message: "
        print message.data
        self.assertEqual(message.header.code, 500)
        
    #@unittest.skip("I do")  
    def test_bad_examinations(self):
        user = User.objects(username='mcaulo').first()
        self.controller.user = user
        query = dict()
        
        examination_list = _get_random_examinations()
        
        query['action'] = 'open'
        query['user'] = 'mcaulo'
        query['report_text'] = "Do cazz e sciut l Acquafan"
        query['id_examination'] = [str(e.id) for e in examination_list]
        
        message = self.controller.create(**query)
        print message.header.message
        self.assertEqual(message.header.code, 501)
        
    
    def test_update(self):
        user = User.objects(username='mcaulo').first()
        self.controller.user = user
        query = dict()
        
        examination_list = _get_correct_examinations()
        
        query['action'] = 'create'
        query['report_text'] = "Do cazz e sciut l Acquafan"
        query['id_examination'] = [str(e.id) for e in examination_list]
        
        message = self.controller.create(**query)
        self.assertEqual(message.header.code, 500)
        
        query = dict()
        query['id'] = str(message.data.first().id)
        query['action'] = 'update'
        query['report_text'] = "Gesu"
        
        message = self.controller.update(**query)
        print message.header.message
        self.assertEqual(message.header.code, 500)
        self.assertEqual(len(self.controller._currentReport.action_list), 2)
        self.assertEqual(self.controller._currentReport.report_text, query['report_text'])
        
        
    def test_close(self):
        user = User.objects(username='mcaulo').first()
        self.controller.user = user
        query = dict()
        report = Report.objects().first()
        query['id'] = str(report.id)
        query['user'] = 'mcaulo'
        message = self.controller.close(**query)
        
        report = Report.objects(id=report.id).first()
        
        assert report.status_name == 'closed'
        assert message.header.code == 500
        assert len(report.action_list) == 2
        assert report.action_list[-1].action == 'close'
        
    def test_open(self):
        user = User.objects(username='mcaulo').first()
        self.controller.user = user.username
        query = dict()
        report = Report.objects().first()
        query['id'] = str(report.id)
        query['user'] = 'mcaulo'
        
        
        _ = self.controller.close(**query)
        query['password'] = 'massimo'
        
        message = self.controller.open(**query)
        
        report = Report.objects(id=report.id).first()
        
        assert report.status_name == 'opened'
        assert message.header.code == 500
        assert len(report.action_list) == 3
        assert report.action_list[-1].action == 'open'
        
        
        
        
        
        