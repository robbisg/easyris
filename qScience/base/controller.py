from qScience.base.factory import ControllerMapper
from qScience.base.action import action_factory

import logging
logger = logging.getLogger('easyris_logger')


class QScienceFacade(object):
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

        user = None

        if 'user' in kwargs.keys():
            user = kwargs.pop('user')

        # Get controller and action class
        # TODO: Check if they're mapped
        controller_class = ControllerMapper.get_mapped(resource_name)

        logger.info("Action: %s - Controller: %s - User: %s" %(action_name,
                                                               resource_name,
                                                               str(user)))
        # We instantiate the classes
        controller = controller_class(user=user)
        action = action_factory(action_name)

        # Message from controller
        message = action.execute(controller, **kwargs)
        # Attach user to the message
        message.set_user(user)
        
        return message   
    
    