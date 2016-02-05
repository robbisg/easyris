
class Action(object):
    def __init__(self, name):
        self.name = name
        
    def execute(self, controller, **kwargs):
        method = getattr(controller, self.name)
        if not method:
            raise Exception('Method %s not implemented' % self.name)
        
        response = method(**kwargs)
        return response
    

class Create(object):
    
    def __init__(self, name='create'):
        super(Create, self).__init__(name)
        

class Read(object):
    
    def __init__(self, name='read'):
        super(Read, self).__init__(name)
        

class Update(object):
    
    def __init__(self, name='update'):
        super(Update, self).__init__(name)
        

class Delete(object):
    
    def __init__(self, name='delete'):
        super(Delete, self).__init__(name)
        
        
        
    
