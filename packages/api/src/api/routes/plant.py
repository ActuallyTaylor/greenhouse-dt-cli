from apiflask import APIBlueprint

plant_bp = APIBlueprint('plant_api', __name__)

@plant_bp.get('/api/plants')
def get_all_plant():
    """Retrieve all plants"""
    pass

@plant_bp.post('/api/plants')
def create_plant():
    """Create a new plant"""
    pass

@plant_bp.get('/api/plants/<plantId>')
def get_plant_by_id(plantId):
    """Retrieve a plant by ID"""
    pass

@plant_bp.patch('/api/plants/<plantId>')
def update_plant(plantId):
    """Update an existing plant"""
    pass

@plant_bp.delete('/api/plants/<plantId>')
def delete_plant(plantId):
    """Delete an existing plant"""
    pass
