from easyris.base.factory import ControllerMapper, ActionMapper

class EasyRisFacade(object):
    """Basic class that manage controller and actions"""
        
    def do(self, action_name, resource_name, **kwargs):
        """Method used to perform an action on the controllers,
        it should be noted that resource and action should be mapped
        
        Parameters
        ----------
        action_name : a string with the action to be performed
        resource_name : a string representing the controller which 
                        manages the action
                        
        Returns
        -------
        message : the controller output of that action
        
        """
        # Get controller and action class
        # TODO: Check if they're mapped
        controller_class = ControllerMapper.get_mapped(resource_name)
        action_class = ActionMapper.get_mapped(action_name)
        
        # We instantiate the classes
        controller = controller_class()
        action = action_class()
        
        user = 'None'

        if 'user' in kwargs.keys():
            user = kwargs.pop('user')

        # Message from controller
        message = action.execute(controller, **kwargs)
        # Attach user to the message
        message.set_user(user)
        print message
        return message
        
# TODO: define a general controller?