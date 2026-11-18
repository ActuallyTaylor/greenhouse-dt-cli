from apiflask import APIBlueprint

from greenhouse_lib.models import LightSwitchAsset

light_switch_bp = APIBlueprint('light_switch_api', __name__)

@light_switch_bp.post('/api/actuators/light')
@light_switch_bp.output({}, status_code=200)
def turn_light_switch_on():
    """Turn on the lights"""
    pass

@light_switch_bp.get('/api/actuators/light')
@light_switch_bp.output({}, status_code=200)
def turn_light_switch_off():
    """Turn off the lights"""
    pass

@light_switch_bp.get('/api/actuators/light')
@light_switch_bp.output(LightSwitchAsset, status_code=200)
def get_light():
    """Get the active greenhouse light"""
    pass
