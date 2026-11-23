from collections import Counter

import numpy as np
from greenhouse_lib.model.models import GrowthStrategy, DecisionOutput, PumpControlOutput
from greenhouse_lib.model.parameters import PlantParameters


# MARK: Static Methods
def percentage_out_of_range(value: float | int, minimum: float | int, maximum: float | int):
    # Avoid divide by zero errors.
    if minimum == maximum:
        return 0.0

    # Swap minimum and maximum in case they are flipped.
    if minimum > maximum:
        minimum, maximum = maximum, minimum

    return ((value - minimum) / (maximum - minimum)) * 100

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

    def make_light_decision(self) -> bool:
        light_out_of_range = percentage_out_of_range(self.light, self.plant.light.min, self.plant.light.max)

        if light_out_of_range > 75:
            # We are in the top 75% of the range
            return False
        else:
            # If we are below 75% of the range, or we are negative in the range, turn the light on.
            return True

    def make_nitrogen_decision(self) -> PumpControlOutput:
        nitrogen_out_of_range = percentage_out_of_range(self.nitrogen, self.plant.nitrogen.min, self.plant.nitrogen.max)

        # Calculates how far out of the preferred nitrogen range we are.
        if nitrogen_out_of_range >= 100:
            return PumpControlOutput.NONE
        elif nitrogen_out_of_range >= 75:
            return PumpControlOutput.SHORT
        elif nitrogen_out_of_range >= 50:
            return PumpControlOutput.MEDIUM
        else:
            return PumpControlOutput.LONG

    def make_moisture_decision(self) -> PumpControlOutput:
        moisture_out_of_range = percentage_out_of_range(self.moisture, self.plant.moisture.min, self.plant.moisture.max)

        # Calculates how far out of the preferred moisture range we are.
        if moisture_out_of_range >= 100:
            return PumpControlOutput.NONE
        elif moisture_out_of_range >= 75:
            return PumpControlOutput.SHORT
        elif moisture_out_of_range >= 50:
            return PumpControlOutput.MEDIUM
        else:
            return PumpControlOutput.LONG


    def decide(self) -> DecisionOutput:
        nutrient_pump_votes: list[PumpControlOutput] = []
        water_pump_votes: list[PumpControlOutput] = []

        # Decide whether or not to enable the lights
        light_decision = self.make_light_decision()

        # Soil moisture decision
        water_pump_votes.append(self.make_moisture_decision())

        # Nitrogen decision
        nutrient_pump_votes.append(self.make_nitrogen_decision())

        water_pump_counts = Counter(water_pump_votes)
        water_pump_decisions = sorted(water_pump_votes, key=lambda x: -water_pump_counts[x])

        nutrient_pump_counts = Counter(nutrient_pump_votes)
        nutrient_pump_decisions = sorted(nutrient_pump_votes, key=lambda x: -nutrient_pump_counts[x])

        selected_water_pump_decision = water_pump_decisions[0]
        selected_nutrient_pump_decision = nutrient_pump_decisions[0]

        return DecisionOutput(selected_water_pump_decision, selected_nutrient_pump_decision, light_decision)