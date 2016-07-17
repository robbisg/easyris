

class ExaminationStatusMixin(object):
    
    def __init__(self, examination, name='basic'):
        self.name = name
        self.examination = examination
        print ' ****** '+self.name
        
    
    def modify(self):
        if not self.examination.modify(status_name=self.examination.status.name):
            #message = Message(PatientErrorHeader(message='Error in modifying'))
            print 'Error'
        
        # Try to save
        try:
            self.examination.save()
        except ValueError, err:
            print 'Value Error!'
    
    
    def _not_enabled(self):
        self.examination.status = self
        return
    
    def start(self):
        self._not_enabled()
        return
    
    def go(self):
        self._not_enabled()
        return
    
    def stop(self):
        self._not_enabled()
        return
    
    def pause(self):
        self._not_enabled()
        return
    
    def finish(self):
        self._not_enabled()
        return 
    
    def eject(self):
        self._not_enabled()
        return
    

class NewExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='new'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)
    
    def start(self):
        self.examination.status = ScheduledExaminationStatus(self.examination)
        self.modify()
        return 
    

class ScheduledExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='scheduled'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)
    
    
    def go(self):
        self.examination.status = RunningExaminationStatus(self.examination)
        self.modify()
        return
    
    
class RunningExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='running'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)
    
    
    def finish(self):
        self.examination.status = CompletedExaminationStatus(self.examination)
        self.modify()
        return 
    
    def stop(self):
        self.examination.status = ReScheduledExaminationStatus(self.examination)
        self.modify()
        return
    
    def pause(self):
        self.examination.status = IncompletedExaminationStatus(self.examination)
        self.modify()
        return 
    
    
class ReScheduledExaminationStatus(ScheduledExaminationStatus):
    
    def __init__(self, examination, name='rescheduled'):
        return ScheduledExaminationStatus.__init__(self, examination, name=name)
    

class CompletedExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='completed'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)
    
    def eject(self):
        self.examination.status = ReportedExaminationStatus(self.examination)
        self.modify()
        return
        
        
class IncompletedExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='incomplete'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)
    
    def start(self):
        self.examination.status = ReScheduledExaminationStatus(self.examination)
        self.modify()
        return
    
    
class ReportedExaminationStatus(ExaminationStatusMixin):
    
    def __init__(self, examination, name='reported'):
        return ExaminationStatusMixin.__init__(self, examination, name=name)