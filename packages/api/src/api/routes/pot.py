from apiflask import APIBlueprint

from api.api_only_models import ApiPotAsset

pot_bp = APIBlueprint('pot_api', __name__)

@pot_bp.post('/api/pots')
@pot_bp.input(ApiPotAsset)
@pot_bp.output({}, status_code=201)
def create_pot(json_data: ApiPotAsset):
    """Create a new pot"""
    pass

@pot_bp.patch('/api/pots')
@pot_bp.input(ApiPotAsset)
@pot_bp.output({}, status_code=201)
def update_pot(json_data: ApiPotAsset):
    """Update an existing pot"""
    pass

@pot_bp.get('/api/pots/<potId>')
@pot_bp.output(ApiPotAsset, status_code=200)
def get_pot_by_id(potId: int):
    """Retrieve a pot by ID"""
    pass

@pot_bp.get('/api/pots')
@pot_bp.output(list[ApiPotAsset], status_code=200)
def get_all_pots():
    """Retrieve all pots"""
    pass

@pot_bp.delete('/api/pots/<potId>')
@pot_bp.output({}, status_code=200)
def delete_pot(potId: int):
    """Delete an existing pot"""
    pass

