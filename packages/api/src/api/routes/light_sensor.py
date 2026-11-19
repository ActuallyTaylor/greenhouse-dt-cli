from apiflask import APIBlueprint

light_sensor_bp = APIBlueprint('light_sensor_api', __name__)

@light_sensor_bp.post('/api/sensors/light')
def create_light_sensor():
    """Create a new light sensor"""
    pass

@light_sensor_bp.patch('/api/sensors/light/<sensorId>')
def update_light_sensor(sensorId):
    """Update an existing light sensor"""
    pass

@light_sensor_bp.get('/api/sensors/light/<sensorId>')
def get_light_sensor_by_id(sensorId):
    """Retrieve a light sensor by ID"""
    pass

@light_sensor_bp.get('/api/sensors/light')
def get_all_light_sensors():
    """Retrieve all light sensors"""
    pass

@light_sensor_bp.delete('/api/sensors/light/<sensorId>')
def delete_light_sensor(sensorId):
    """Delete a light sensor"""
    pass

