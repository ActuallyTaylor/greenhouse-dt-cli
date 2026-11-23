
import numpy as np
from greenhouse_lib.model.models import GrowthStrategy, DecisionOutput, PumpControlOutput
from greenhouse_lib.model.parameters import PlantParameters


# MARK: Static Methods
def vdp(temperature: float, relative_humidity: float) -> float:
    """
    Computes the Vapor-pressure deficit for a greenhouse
    Based on: https://en.wikipedia.org/wiki/Vapour-pressure_deficit#Computing_VPD_for_plants_in_a_greenhouse
    :param relative_humidity:
    :param temperature:
    :return:
    """
    A = -1.0440397e4
    B = -11.29465
    C = -2.7022355e-2
    D = 1.289036e-5
    E = -2.4780681e-9
    F = 6.545973

    rankine_temperature = temperature + 459.67
    exponent = (A / rankine_temperature) + B + (C * rankine_temperature) + ((D * rankine_temperature) ** 2) + ((E * rankine_temperature) ** 3) + (F * np.log(rankine_temperature))
    saturation_vapor_pressure = np.e ** exponent

    vapor_pressure_deficit = saturation_vapor_pressure * (1 - (relative_humidity / 100))

    return vapor_pressure_deficit


# MARK: Growth Strategy
class BasicGrowthStrategy(GrowthStrategy):
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

    def decide(self) -> DecisionOutput:
        nutrient_pump_decision = PumpControlOutput.NONE
        water_pump_decision = PumpControlOutput.NONE
        light_decision = False

        if self.light < self.plant.light.min:
            light_decision = True
        elif self.light > self.plant.light.max:
            light_decision = False

        # Calculate how much far out of the vapor pressure deficit range we are.
        vapor_pressure_deficit = vdp(self.temperature, self.relative_humidity)


        # vpd_penalty = out_of_range_penalty(self.plant.vdp.min, self.plant.vdp.max, vapor_pressure_deficit)
        #
        # # Calculates how far out of the preferred nitrogen range we are.
        # nitrogen_out_of_range_penalty = out_of_range_penalty(self.plant.nitrogen.min, self.plant.nitrogen.max, self.nitrogen)
        #
        # # Calculates how far out of the preferred moisture range we are.
        # moisture_out_of_range_penalty = out_of_range_penalty(self.plant.moisture.min, self.plant.moisture.max, self.moisture)


        if self.nitrogen < self.plant.nitrogen.min:
             nutrient_pump_decision = PumpControlOutput.NONE
        elif self.nitrogen < self.plant.nitrogen.max:
            nutrient_pump_decision = PumpControlOutput.NONE


        return DecisionOutput(water_pump_decision, nutrient_pump_decision, light_decision)

    # Nitrogen Stress, pH Stress
    # Moisture?
    # Light sensor in PPFD, for Daily Light Integral