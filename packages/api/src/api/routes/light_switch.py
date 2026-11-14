from apiflask import APIBlueprint

light_switch_bp = APIBlueprint('light_switch_api', __name__)

@light_switch_bp.post('/api/actuators/light')
def turn_light_switch_on():
    """Turn on the lights"""
    pass

@light_switch_bp.get('/api/actuators/light')
def turn_light_switch_off():
    """Turn off the lights"""
    pass

@light_switch_bp.get('/api/actuators/light')
def get_light_status():
    """Get the status of the lights"""
    pass
