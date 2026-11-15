from apiflask import APIBlueprint

pump_bp = APIBlueprint('pump_api', __name__)

@pump_bp.get('/api/pumps')
def get_all_plant():
    """Retrieve all pumps"""
    pass

@pump_bp.post('/api/pumps')
def create_plant():
    """Create a new pump"""
    pass

@pump_bp.get('/api/pumps/<pumpId>')
def get_plant_by_id(pumpId):
    """Retrieve a pump by ID"""
    pass

@pump_bp.patch('/api/pumps/<pumpId>')
def update_plant(pumpId):
    """Update an existing pump"""
    pass

@pump_bp.delete('/api/pumps/<pumpId>')
def delete_plant(pumpId):
    """Delete an existing pump"""
    pass
