from apiflask import APIBlueprint

from greenhouse_lib.models import MoistureSensorAsset

moisture_sensor_bp = APIBlueprint('moisture_sensor_api', __name__)

@moisture_sensor_bp.post('/api/sensors/moisture')
@moisture_sensor_bp.input(MoistureSensorAsset)
@moisture_sensor_bp.output({}, status_code=201)
def create_moisture_sensor(json_data: MoistureSensorAsset):
    """Create a new moisture sensor"""
    pass

@moisture_sensor_bp.patch('/api/sensors/moisture/')
@moisture_sensor_bp.input(MoistureSensorAsset)
@moisture_sensor_bp.output({}, status_code=201)
def update_moisture_sensor(json_data: MoistureSensorAsset):
    """Update an existing moisture sensor"""
    pass

@moisture_sensor_bp.get('/api/sensors/moisture/<sensorId>')
@moisture_sensor_bp.output(MoistureSensorAsset, status_code=200)
def get_moisture_sensor_by_id(sensorId: int):
    """Retrieve a moisture sensor by ID"""
    pass

@moisture_sensor_bp.get('/api/sensors/moisture')
@moisture_sensor_bp.output(list[MoistureSensorAsset], status_code=200)
def get_all_moisture_sensors():
    """Retrieve all moisture sensors"""
    pass

@moisture_sensor_bp.delete('/api/sensors/moisture/<sensorId>')
@moisture_sensor_bp.output({}, status_code=200)
def delete_moisture_sensor(sensorId: int):
    """Delete an existing moisture sensor"""
    pass
