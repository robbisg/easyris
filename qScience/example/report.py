from qScience.model.user import User, Permission, Role
from qScience.model.patient import Patient
from qScience.model.examination import Examination, Priority, Typology
from qScience.model.report import Report, ReportAction
from mongoengine import connect
import itertools
import collections
import random
import numpy as np
import datetime
from qScience.model.report_status import SuspendedReportStatus
from qScience.model.examination_status import ClosedExaminationStatus
from qScience.database.base import parse_db_config, easyris_connect

def run(database_config, n_loaded=50):
    
    db_config = parse_db_config(database_config)

    _ = easyris_connect(**db_config)
    
    Report.drop_collection()
    
    user = User.objects(username='mcaulo').first()
    
    examination_list = Examination.objects(status_name='completed',
                                           data_inserimento=datetime.datetime(year=2016,
                                                                              month=02,
                                                                              day=02))
    
    # Trovo i pazienti con piu esami
    id_patient_list = [e.id_patient.id_patient for e in examination_list]
    counter = collections.Counter(id_patient_list)
    
    if len(counter) < n_loaded:
        n_loaded = len(counter) / 2
    
    print n_loaded
    
    for i in range(n_loaded):
        
        id_patient = counter.keys()[i]
        patient = Patient.objects(id_patient=id_patient).first()
        patient_examination = Examination.objects(id_patient=patient.id,
                                                  status_name='completed',
                                                  data_inserimento=datetime.datetime(year=2016,
                                                                            month=02,
                                                                            day=02))

        dates_ = np.unique([e.data_inserimento for e in patient_examination])
        
        for d_ in dates_:
            data_ = datetime.datetime(d_.year, d_.month, d_.day)
            same_date_examination = Examination.objects(id_patient=patient.id,
                                                        data_inserimento=data_,
                                                        status_name='completed')
        

        report_log = ReportAction(
                                     user=user,
                                     action='create'
                                     )
               

        report = Report(
                        id_examination = [e for e in same_date_examination],
                        report_text = "Il paziente bla bla bla",
                        action_list = [report_log],
                        id_patient = id_patient,
                        status=SuspendedReportStatus(),
                        status_name='suspended'
                        )

        report.save()
        
        for e in same_date_examination:
            e.modify(status=ClosedExaminationStatus(),
                     status_name='closed')
            e.save()
        
