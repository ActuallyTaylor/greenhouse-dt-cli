from apiflask import APIBlueprint

from api.api_only_models import ApiPumpAsset

pump_bp = APIBlueprint('pump_api', __name__)

@pump_bp.post('/api/pumps')
@pump_bp.input(ApiPumpAsset)
@pump_bp.output({}, status_code=201)
def create_pump(json_data: ApiPumpAsset):
    """Create a new pump"""
    pass

@pump_bp.patch('/api/pumps')
@pump_bp.input(ApiPumpAsset)
@pump_bp.output({}, status_code=201)
def update_pump(json_data: ApiPumpAsset):
    """Update an existing pump"""
    pass

@pump_bp.delete('/api/pumps/<pumpId>')
@pump_bp.output({}, status_code=200)
def delete_pump(pumpId: int):
    """Delete an existing pump"""
    pass

@pump_bp.get('/api/pumps/<pumpId>')
@pump_bp.output(ApiPumpAsset, status_code=200)
def get_pump_by_id(pumpId: int):
    """Retrieve a pump by ID"""
    pass

@pump_bp.get('/api/pumps')
@pump_bp.output(list[ApiPumpAsset], status_code=200)
def get_all_pumps():
    """Retrieve all pumps"""
    pass
