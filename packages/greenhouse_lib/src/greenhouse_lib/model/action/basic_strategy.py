from collections import Counter

from greenhouse_lib.model.models import ActionStrategy, DecisionOutput, PumpControlOutput, PlantEnvironment, \
    PlantParameters
from greenhouse_lib.model.utility import percentage_out_of_range, vpd


# MARK: Growth Strategy
class BasicActionStrategy(ActionStrategy):
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

    def update(self, environment: PlantEnvironment):
        self.temperature = environment.temperature
        self.relative_humidity = environment.relative_humidity
        self.nitrogen = environment.nitrogen
        self.moisture = environment.moisture
        self.light = environment.light
        self.ph_level = environment.ph_level

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

    def make_vpd_decision(self) -> PumpControlOutput:
        # Calculate how much far out of the vapor pressure deficit range we are.
        vapor_pressure_deficit = vpd(self.temperature, self.relative_humidity)
        vpd_out_of_range = percentage_out_of_range(vapor_pressure_deficit, self.plant.vpd.min, self.plant.vpd.max)

        # In the case of VPD, low VPD means there is already enough water in the soil. In the case of a high VPD, there is not enough wateri n the system.
        if vpd_out_of_range >= 75:
            return PumpControlOutput.LONG
        elif vpd_out_of_range >= 50:
            return PumpControlOutput.MEDIUM
        elif vpd_out_of_range >= 25:
            return PumpControlOutput.SHORT
        else:
            return PumpControlOutput.NONE

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
        light_decision = self.make_light_decision()

        # Vapor Pressure Deficit decision
        water_pump_votes.append(self.make_vpd_decision())

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
