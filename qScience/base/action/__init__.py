
class Action(object):
    
    def __init__(self, name):
        self.name = name
        
    def execute(self, controller, **kwargs):
        """Basic method for the Action class. Overriding this method is
        discouraged
        
        Parameters
        ----------
        controller : a class with the implementation of the action
        **kwargs : dictionary with the parameters to be passed to the 
                    controller
        Returns
        -------
        response : the response given by the controller
        """
        
        # We found if the controller has that specific method
        method = getattr(controller, self.name)
        
        if not method:
            raise Exception('Method %s not implemented' % self.name)
        
        # We run the method with parameters from dictionary
        response = method(**kwargs)
        
        return response
    

def action_factory(name):
    return Action(name)
        

