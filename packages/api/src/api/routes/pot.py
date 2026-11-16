from apiflask import APIBlueprint

pot_bp = APIBlueprint('pot_api', __name__)

@pot_bp.get('/api/pots')
def get_all_plant():
    """Retrieve all pots"""
    pass

@pot_bp.post('/api/pots')
def create_plant():
    """Create a new pot"""
    pass

@pot_bp.get('/api/pots/<potId>')
def get_plant_by_id(potId):
    """Retrieve a pot by ID"""
    pass

@pot_bp.patch('/api/pots/<potId>')
def update_plant(potId):
    """Update an existing pot"""
    pass

@pot_bp.delete('/api/pots/<potId>')
def delete_plant(potId):
    """Delete an existing pot"""
    pass

