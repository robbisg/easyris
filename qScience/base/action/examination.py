from qScience.base.action import Action


class Start(Action):
    
    def __init__(self, name='start'):
        super(Start, self).__init__(name)
        
        
class Go(Action):
    
    def __init__(self, name='go'):
        super(Go, self).__init__(name)
        
        
class Stop(Action):
    
    def __init__(self, name='stop'):
        super(Stop, self).__init__(name)
        
        
class Pause(Action):
    
    def __init__(self, name='pause'):
        super(Pause, self).__init__(name)
        
        
class Finish(Action):
    
    def __init__(self, name='finish'):
        super(Finish, self).__init__(name)
        
        
class Eject(Action):
    
    def __init__(self, name='eject'):
        super(Eject, self).__init__(name)