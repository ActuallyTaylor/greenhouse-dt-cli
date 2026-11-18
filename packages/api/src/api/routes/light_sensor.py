from apiflask import APIBlueprint
from pydantic import BaseModel, Field

from greenhouse_lib.models import LightSensorAsset

light_sensor_bp = APIBlueprint('light_sensor_api', __name__)

@light_sensor_bp.post('/api/sensors/light')
@light_sensor_bp.input(LightSensorAsset)
@light_sensor_bp.output({}, status_code=201)
def create_light_sensor(json_data: LightSensorAsset):
    """Create a new light sensor"""
    return {}

@light_sensor_bp.patch('/api/sensors/light')
@light_sensor_bp.input(LightSensorAsset)
@light_sensor_bp.output({}, status_code=201)
def update_light_sensor(json_data: LightSensorAsset):
    """Update an existing light sensor"""
    pass

@light_sensor_bp.delete('/api/sensors/light/<sensorId>')
@light_sensor_bp.output({}, status_code=200)
def delete_light_sensor(sensorId: int):
    """Delete a light sensor"""
    pass

@light_sensor_bp.get('/api/sensors/light/<sensorId>')
@light_sensor_bp.output(LightSensorAsset, status_code=200)
def get_light_sensor_by_id(json_data: LightSensorAsset):
    """Retrieve a light sensor by ID"""
    pass

@light_sensor_bp.get('/api/sensors/light')
@light_sensor_bp.output(list[LightSensorAsset], status_code=200)
def get_all_light_sensors(json_data: list[LightSensorAsset]):
    """Retrieve all light sensors"""
    pass
