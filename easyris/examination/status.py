from mongoengine.document import EmbeddedDocument


class ExaminationStatus(EmbeddedDocument):
    
    meta = {'allow_inheritance': True}
    
    def __init__(self, name='basic', *args, **values):
        self.name = name
        EmbeddedDocument.__init__(self, *args, **values)
        
    
    def _modify(self, examination, status):
        
        if not examination.modify(status=status, status_name=status.name):
            #message = Message(PatientErrorHeader(message='Error in modifying'))
            print 'Error'
        
        # Try to save
        try:
            examination.save()
        except ValueError, err:
            print 'Value Error!'
    
    
    def _not_enabled(self):
        return
    
    def start(self, examination):
        self._not_enabled()
        return
    
    def go(self, examination):
        self._not_enabled()
        return
    
    def stop(self, examination):
        self._not_enabled()
        return
    
    def pause(self, examination):
        self._not_enabled()
        return
    
    def finish(self, examination):
        self._not_enabled()
        return 
    
    def eject(self, examination):
        self._not_enabled()
        return
    
    def close(self, examination):
        self._not_enabled()
        return
    

class NewExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='new', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
    
    def start(self, examination):
        status = ScheduledExaminationStatus()
        self._modify(examination, status)
        return 
    

class ScheduledExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='scheduled', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
    
    
    def go(self, examination):
        status = RunningExaminationStatus()
        self._modify(examination, status)
        return
    
    
class RunningExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='running', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
    
    
    def finish(self, examination):
        status = CompletedExaminationStatus()
        self._modify(examination, status)
        return 
    
    def stop(self, examination):
        status = ReScheduledExaminationStatus()
        self._modify(examination, status)
        return
    
    def pause(self, examination):
        status = IncompletedExaminationStatus()
        self._modify(examination, status)
        return 
    
    
class ReScheduledExaminationStatus(ScheduledExaminationStatus):
    
    def __init__(self, name='rescheduled', *args, **values):
        ScheduledExaminationStatus.__init__(self, name=name, *args, **values)
    

class CompletedExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='completed', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
    
    def eject(self, examination):
        status = ReportedExaminationStatus()
        self._modify(examination, status)
        return
        
        
class IncompletedExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='incomplete', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
    
    def start(self, examination):
        status = ReScheduledExaminationStatus()
        self._modify(examination, status)
        return
    
    
class ReportedExaminationStatus(ExaminationStatus):
    
    def __init__(self, name='reported', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values)
        
    def eject(self, examination):
        status = CompletedExaminationStatus()
        self._modify(examination, status)
        return
    
    def close(self, examination):
        status = ClosedExaminationStatus()
        self._modify(examination, status)
        return

class ClosedExaminationStatus(ExaminationStatus):
    def __init__(self, name='closed', *args, **values):
        ExaminationStatus.__init__(self, name=name, *args, **values) 