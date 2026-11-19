from apiflask import APIBlueprint

water_bucket_bp = APIBlueprint('water_bucket_api', __name__, url_prefix='/api/waterbuckets')

@water_bucket_bp.post('/api/buckets')
def create_nutrient_sensor():
    """Create a new water bucket"""
    pass

@water_bucket_bp.get('/api/buckets')
def get_all_nutrient_buckets():
    """Retrieve all water bucket"""
    pass

@water_bucket_bp.get('/api/buckets/<waterBucketId>')
def get_nutrient_sensor_by_id(waterBucketId):
    """Retrieve a water bucket by ID"""
    pass

@water_bucket_bp.patch('/api/buckets/<waterBucketId>')
def update_nutrient_sensor(waterBucketId):
    """Update an existing water bucket"""
    pass

@water_bucket_bp.delete('/api/buckets/<waterBucketId>')
def delete_nutrient_sensor(waterBucketId):
    """Delete an existing water bucket"""
    pass
