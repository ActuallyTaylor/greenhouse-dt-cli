from apiflask import APIBlueprint

from greenhouse_lib.models import PotAsset

pot_bp = APIBlueprint('pot_api', __name__)

@pot_bp.post('/api/pots')
@pot_bp.input(PotAsset)
@pot_bp.output({}, status_code=201)
def create_pot():
    """Create a new pot"""
    pass

@pot_bp.patch('/api/pots')
@pot_bp.input(PotAsset)
@pot_bp.output({}, status_code=201)
def update_pot(potId):
    """Update an existing pot"""
    pass

@pot_bp.get('/api/pots/<potId>')
@pot_bp.output(PotAsset, status_code=200)
def get_pot_by_id(potId):
    """Retrieve a pot by ID"""
    pass

@pot_bp.get('/api/pots')
@pot_bp.output(list[PotAsset], status_code=200)
def get_all_pots():
    """Retrieve all pots"""
    pass

@pot_bp.delete('/api/pots/<potId>')
@pot_bp.output({}, status_code=200)
def delete_pot(potId: int):
    """Delete an existing pot"""
    pass

