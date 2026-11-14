from apiflask import APIBlueprint

section_bp = APIBlueprint('section_api', __name__)

@section_bp.get('/api/sections')
def get_all_plant():
    """Retrieve all sections"""
    pass

@section_bp.post('/api/sections')
def create_plant():
    """Create a new section"""
    pass

@section_bp.get('/api/sections/<sectionId>')
def get_plant_by_id(sectionId):
    """Retrieve a section by ID"""
    pass

@section_bp.patch('/api/sections/<sectionId>')
def update_plant(sectionId):
    """Update an existing section"""
    pass

@section_bp.delete('/api/sections/<sectionId>')
def delete_plant(sectionId):
    """Delete an existing section"""
    pass
