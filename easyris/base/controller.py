from easyris.base.factory import ControllerMapper, ActionMapper

class EasyRisFacade(object):
    
        
    def do(self, action_name, resource_name, **kwargs):
        # action_name is a string
        # resource_name is a string
                
        controller_class = ControllerMapper.get_mapped(resource_name)
        action_class = ActionMapper.get_mapped(action_name)

        controller = controller_class()
        action = action_class()

        return action.execute(controller, **kwargs)
        
# TODO: define a general controller?