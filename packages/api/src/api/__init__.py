from apiflask import APIFlask

app = APIFlask("greenhouse_dt_api")

# Import and register all blueprints
from api.routes import (
    decision_bp,
    plant_bp,
    pot_bp,
    water_bucket_bp,
    pump_bp,
    light_switch_bp,
    light_sensor_bp,
    moisture_sensor_bp,
    nutrient_sensor_bp,
    temperature_humidity_sensor_bp,
    section_bp,
)

app.register_blueprint(decision_bp)
app.register_blueprint(plant_bp)
app.register_blueprint(pot_bp)
app.register_blueprint(water_bucket_bp)
app.register_blueprint(pump_bp)
app.register_blueprint(light_switch_bp)
app.register_blueprint(light_sensor_bp)
app.register_blueprint(moisture_sensor_bp)
app.register_blueprint(nutrient_sensor_bp)
app.register_blueprint(temperature_humidity_sensor_bp)
app.register_blueprint(section_bp)


def main() -> None:
    app.run()
