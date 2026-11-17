from apiflask import APIBlueprint

from greenhouse_lib.models import TempHumiditySensorAsset

temperature_humidity_sensor_bp = APIBlueprint('temperature_humidity_sensor_api', __name__, url_prefix='/api/sensors/temperature-humidity')

@temperature_humidity_sensor_bp.post('/api/sensors/temperature_humidity')
@temperature_humidity_sensor_bp.input(TempHumiditySensorAsset)
@temperature_humidity_sensor_bp.output({}, status_code=201)
def create_temperature_humidity_sensor(json_data: TempHumiditySensorAsset):
    """Create a new temperature / humidity sensor"""
    pass

@temperature_humidity_sensor_bp.patch('/api/sensors/temperature_humidity')
@temperature_humidity_sensor_bp.input(TempHumiditySensorAsset)
@temperature_humidity_sensor_bp.output({}, status_code=201)
def update_temperature_humidity_sensor(json_data: TempHumiditySensorAsset):
    """Update an existing temperature / humidity sensor"""
    pass

@temperature_humidity_sensor_bp.delete('/api/sensors/temperature_humidity/<sensorId>')
@temperature_humidity_sensor_bp.output({}, status_code=200)
def delete_temperature_humidity_sensor(sensorId):
    """Delete an existing temperature / humidity sensor"""
    pass

@temperature_humidity_sensor_bp.get('/api/sensors/temperature_humidity/<sensorId>')
@temperature_humidity_sensor_bp.output(TempHumiditySensorAsset, status_code=200)
def get_temperature_humidity_sensor_by_id(sensorId):
    """Retrieve a temperature / humidity sensor by ID"""
    pass

@temperature_humidity_sensor_bp.get('/api/sensors/temperature_humidity')
@temperature_humidity_sensor_bp.output(list[TempHumiditySensorAsset], status_code=200)
def get_all_temperature_humidity_sensors():
    """Retrieve all temperature / humidity sensors"""
    pass

