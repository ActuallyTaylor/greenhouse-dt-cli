from shelve import Shelf

from apiflask import APIBlueprint

from api.api_only_models import ApiShelfAsset
from greenhouse_lib.models import ShelfAsset

shelf_bp = APIBlueprint('shelf_api', __name__)

@shelf_bp.post('/api/shelf')
@shelf_bp.input(ApiShelfAsset)
@shelf_bp.output({}, status_code=201)
def create_shelf(json_data: ApiShelfAsset):
    """Create a new shelf"""
    pass

@shelf_bp.patch('/api/shelf/')
@shelf_bp.input(ApiShelfAsset)
@shelf_bp.output({}, status_code=201)
def update_shelf(json_data: ApiShelfAsset):
    """Update an existing shelf"""
    pass

@shelf_bp.delete('/api/shelf/<shelfId>')
@shelf_bp.output({}, status_code=200)
def delete_shelf(shelfId):
    """Delete an existing shelf"""
    pass

@shelf_bp.get('/api/shelf')
@shelf_bp.output(list[ApiShelfAsset], status_code=200)
def get_all_shelves():
    """Retrieve all shelfs"""
    pass

@shelf_bp.get('/api/shelf/<shelfId>')
@shelf_bp.output(ApiShelfAsset, status_code=200)
def get_shelf_by_id(shelfId):
    """Retrieve a shelf by ID"""
    pass

