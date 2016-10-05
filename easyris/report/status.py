from mongoengine.document import EmbeddedDocument

class ReportStatus(EmbeddedDocument):
    
    meta = {'allow_inheritance': True}
    
    def __init__(self, name='basic', *args, **values):
        self.name = name
        EmbeddedDocument.__init__(self, *args, **values)
        
    
    def _modify(self, report, status):
        
        if not report.modify(status=status, 
                             status_name=status.name):
            # TODO: Log error
            print 'Error'
        
        # Try to save
        try:
            report.save()
        except ValueError, err:
            # TODO: Log error
            print 'Value Error!'
    
    
    def _not_enabled(self):
        return
    
    def open(self, report):
        self._not_enabled()
        return
    
    def close(self, report):
        self._not_enabled()
        return
    
    def pause(self, report):
        self._not_enabled()
        return
    
    
class OpenedReportStatus(ReportStatus):
    
    def __init__(self, name='opened', *args, **values):
        ReportStatus.__init__(self, name=name, *args, **values)
    
    
    def pause(self, report):
        status = SuspendedReportStatus()
        self._modify(report, status)
        return 
    
    
    def close(self, report):
        status = ClosedReportStatus()
        self._modify(report, status)
        return        




class SuspendedReportStatus(ReportStatus):
    
    def __init__(self, name='suspended', *args, **values):
        ReportStatus.__init__(self, name=name, *args, **values)
    
    def open(self, report):
        status = OpenedReportStatus()
        self._modify(report, status)
        return
        
    def close(self, report):
        status = ClosedReportStatus()
        self._modify(report, status)
        return
    
    

class ClosedReportStatus(ReportStatus):
    
    def __init__(self, name='closed', *args, **values):
        ReportStatus.__init__(self, name=name, *args, **values)
    
    
    def open(self, report):
        status = OpenedReportStatus()
        self._modify(report, status)
        return