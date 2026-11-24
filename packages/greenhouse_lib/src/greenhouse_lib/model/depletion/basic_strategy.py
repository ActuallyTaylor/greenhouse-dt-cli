from greenhouse_lib.model.models import DepletionStrategy
from greenhouse_lib.model.parameters import PlantParameters
from greenhouse_lib.model.utility import percentage_out_of_range


class BasicDepletionStrategy(DepletionStrategy):
    plant: PlantParameters

    # Current temperature, °C
    temperature: float | int = 0
    # Relative humidity, %
    relative_humidity: float | int = 0
    # Current level of nitrogen in the soil, parts per million (ppm)
    nitrogen: float | int = 0
    # Relative moisture % of the soil
    moisture: float | int = 0
    # Current light level in Photosynthetic Photon Flux Density (PPFD), µmol/m²/s.
    light: float | int = 0
    # Current ph level of the soil (0-14)
    ph_level: float | int = 0

    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        self.temperature = temperature
        self.relative_humidity = humidity
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.light = light
        self.ph_level = ph_level


    def step(self):
        light_out_of_range = percentage_out_of_range(self.light, self.plant.light.min, self.plant.light.max)
        nitrogen_out_of_range = percentage_out_of_range(self.nitrogen, self.plant.nitrogen.min, self.plant.nitrogen.max)
        moisture_out_of_range = percentage_out_of_range(self.moisture, self.plant.moisture.min, self.plant.moisture.max)
