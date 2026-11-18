from apiflask import APIBlueprint

from greenhouse_lib.models import PlantAsset

plant_bp = APIBlueprint('plant_api', __name__)
@plant_bp.post('/api/plants')
@plant_bp.input(PlantAsset)
@plant_bp.output({}, status_code=201)
def create_plant():
    """Create a new plant"""
    pass

@plant_bp.patch('/api/plants')
@plant_bp.input(PlantAsset)
@plant_bp.output({}, status_code=201)
def update_plant(json_data: PlantAsset):
    """Update an existing plant"""
    pass

@plant_bp.delete('/api/plants/<plantId>')
@plant_bp.output({}, status_code=200)
def delete_plant(plantId: int):
    """Delete an existing plant"""
    pass

@plant_bp.get('/api/plants/<plantId>')
@plant_bp.output(PlantAsset, status_code=200)
def get_plant_by_id(plantId: int):
    """Retrieve a plant by ID"""
    pass

@plant_bp.get('/api/plants')
@plant_bp.output(list[PlantAsset], status_code=200)
def get_all_plants():
    """Retrieve all plants"""
    pass
