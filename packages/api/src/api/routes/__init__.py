from api.routes.decision import decision_bp
from api.routes.plant import plant_bp
from api.routes.pot import pot_bp
from api.routes.water_bucket import water_bucket_bp
from api.routes.pump import pump_bp
from api.routes.light_switch import light_switch_bp
from api.routes.light_sensor import light_sensor_bp
from api.routes.moisture_sensor import moisture_sensor_bp
from api.routes.nutrient_sensor import nutrient_sensor_bp
from api.routes.temperature_humidity_sensor import temperature_humidity_sensor_bp
from api.routes.section import section_bp

__all__ = [
    "decision_bp",
    "plant_bp",
    "pot_bp",
    "water_bucket_bp",
    "pump_bp",
    "light_switch_bp",
    "light_sensor_bp",
    "moisture_sensor_bp",
    "nutrient_sensor_bp",
    "temperature_humidity_sensor_bp",
    "section_bp",
]
