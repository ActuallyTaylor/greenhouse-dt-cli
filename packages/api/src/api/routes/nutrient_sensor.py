from apiflask import APIBlueprint

from greenhouse_lib.models import MoistureSensorAsset, NutrientSensorAsset

nutrient_sensor_bp = APIBlueprint('nutrient_sensor_api', __name__)

@nutrient_sensor_bp.post('/api/sensors/nutrient')
@nutrient_sensor_bp.input(NutrientSensorAsset)
@nutrient_sensor_bp.output({}, status_code=201)
def create_nutrient_sensor(json_data: NutrientSensorAsset):
    """Create a new nutrient sensor"""
    pass

@nutrient_sensor_bp.patch('/api/sensors/nutrient')
@nutrient_sensor_bp.input(NutrientSensorAsset)
@nutrient_sensor_bp.output({}, status_code=201)
def update_nutrient_sensor(json_data: NutrientSensorAsset):
    """Update an existing nutrient sensor"""
    pass

@nutrient_sensor_bp.get('/api/sensors/nutrient/<sensorId>')
@nutrient_sensor_bp.output(NutrientSensorAsset, status_code=200)
def get_nutrient_sensor_by_id(sensorId):
    """Retrieve a nutrient sensor by ID"""
    pass

@nutrient_sensor_bp.get('/api/sensors/nutrient')
@nutrient_sensor_bp.output(list[NutrientSensorAsset], status_code=200)
def get_all_nutrient_sensors():
    """Retrieve all nutrient sensors"""
    pass

@nutrient_sensor_bp.delete('/api/sensors/nutrient/<sensorId>')
@nutrient_sensor_bp.output({}, status_code=200)
def delete_nutrient_sensor(sensorId):
    """Delete an existing nutrient sensor"""
    pass
