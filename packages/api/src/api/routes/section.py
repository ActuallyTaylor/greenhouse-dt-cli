from shelve import Shelf

from apiflask import APIBlueprint

from greenhouse_lib.models import ShelfAsset

section_bp = APIBlueprint('section_api', __name__)

@section_bp.post('/api/sections')
@section_bp.input(ShelfAsset)
@section_bp.output({}, status_code=201)
def create_shelf(json_data: ShelfAsset):
    """Create a new section"""
    pass

@section_bp.patch('/api/sections/')
@section_bp.input(ShelfAsset)
@section_bp.output({}, status_code=201)
def update_shelf(json_data: ShelfAsset):
    """Update an existing section"""
    pass

@section_bp.delete('/api/sections/<sectionId>')
@section_bp.output({}, status_code=200)
def delete_shelf(sectionId):
    """Delete an existing section"""
    pass

@section_bp.get('/api/sections')
@section_bp.output(list[ShelfAsset], status_code=200)
def get_all_shelves():
    """Retrieve all sections"""
    pass

@section_bp.get('/api/sections/<sectionId>')
@section_bp.output(ShelfAsset, status_code=200)
def get_shelf_by_id(sectionId):
    """Retrieve a section by ID"""
    pass

