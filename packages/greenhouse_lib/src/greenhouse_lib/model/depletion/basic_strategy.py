# Edited by Claude Opus 5.5 (Anthropic) (pi) on 2026-11-23, Fixed step() multipliers zeroing/flipping values and clamped depletion at 0
from greenhouse_lib.model.models import DepletionStrategy
from greenhouse_lib.model.parameters import PlantParameters
from greenhouse_lib.model.utility import percentage_out_of_range, vpd, deviation

BASE_MOISTURE_LOSS = 0.5  # % per step
BASE_NITROGEN_LOSS = 0.2  # ppm per step

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

    def __init__(self, plant: PlantParameters):
        self.plant = plant

    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        self.temperature = temperature
        self.relative_humidity = humidity
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.light = light
        self.ph_level = ph_level


    def step(self):
        light_deviation = deviation(percentage_out_of_range(self.light, self.plant.light.min, self.plant.light.max))
        nitrogen_deviation = deviation(percentage_out_of_range(self.nitrogen, self.plant.nitrogen.min, self.plant.nitrogen.max))
        moisture_deviation = deviation(percentage_out_of_range(self.moisture, self.plant.moisture.min, self.plant.moisture.max))

        vapor_pressure_deficit = vpd(self.temperature, self.relative_humidity)
        vpd_deviation = deviation(percentage_out_of_range(vapor_pressure_deficit, self.plant.vpd.min, self.plant.vpd.max))

        # water_mult = max(0.0, 1 + 1.0 * vpd_deviation + 0.5* light_deviation - 0.3*max(nitrogen_d, 0))
        # self.moisture = max(0.0, self.moisture - BASE_MOISTURE_LOSS * water_mult)

        # Baseline water loss
        water_mult = BASE_MOISTURE_LOSS
        nitrogen_mult = BASE_NITROGEN_LOSS

        ### VPD ###
        # A high VPD will lose water quicker. So multiply by 1 + vpd to increase the multiplier. A lower vpd will reduce the water multiple.
        water_mult *= (1 + vpd_deviation)

        ### Light ###
        # High light means more photosynthesis, so water and nitrogen deplete quicker. Low light, less depletion.
        water_mult *= (1 + light_deviation)
        nitrogen_mult *= (1 + light_deviation)

        ### Moisture ###
        if moisture_deviation > 0:
            # Waterlogged roots, so they uptake less water and nitrogen leaches out of the soil.
            water_mult *= max(0.0, 1 - 0.5 * moisture_deviation)
            # If there is extra water, it will evaporate out
            water_mult += BASE_MOISTURE_LOSS * 2.0 * moisture_deviation

            nitrogen_mult *= (1 + moisture_deviation)
        elif moisture_deviation < 0:
            # Soil is dry, so moisture uptake falls quickly, and less N is lost in the soil
            water_mult *= max(0.0, 1 + 2.0 * moisture_deviation)
            nitrogen_mult *= max(0.0, 1 + moisture_deviation)

        ### Nitrogen ###
        if nitrogen_deviation > 0:
            # High nitrogen stresses the plant and makes water update slower
            water_mult *= max(0.0, 1 - 0.3 * nitrogen_deviation)

        # Low VPD/light deviations can push multipliers negative, so clamp them before subtracting.
        water_mult = max(0.0, water_mult)
        nitrogen_mult = max(0.0, nitrogen_mult)

        self.moisture = max(0.0, self.moisture - water_mult)
        self.nitrogen = max(0.0, self.nitrogen - nitrogen_mult)
