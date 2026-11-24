from enum import Enum
from random import uniform
from typing import NamedTuple


class ParameterPack:
    min: float
    max: float

    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

    def random(self):
        return uniform(self.min, self.max)


class PlantParameters:
    vpd: ParameterPack
    nitrogen: ParameterPack
    moisture: ParameterPack
    ph: ParameterPack
    light: ParameterPack

    def __init__(self, vpd: ParameterPack, nitrogen: ParameterPack, moisture: ParameterPack, ph: ParameterPack,
                 light: ParameterPack):
        self.vpd = vpd
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.ph = ph
        self.light = light


class PumpBonuses:
    """
    How much a particular activation of a pump will affect the soil.
    """
    moisture: ParameterPack
    nitrogen: ParameterPack

    def __init__(self, moisture: ParameterPack, nitrogen: ParameterPack):
        self.nitrogen = nitrogen
        self.moisture = moisture


class PumpControlOutput(Enum):
    NONE = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3


class PumpPack:
    long: PumpBonuses
    medium: PumpBonuses
    short: PumpBonuses

    def __init__(self, long: PumpBonuses, medium: PumpBonuses, short: PumpBonuses):
        self.long = long
        self.medium = medium
        self.short = short

    def pack_for(self, output: PumpControlOutput) -> PumpBonuses | None:
        match output:
            case PumpControlOutput.SHORT:
                return self.short
            case PumpControlOutput.MEDIUM:
                return self.medium
            case PumpControlOutput.LONG:
                return self.long
        return None


class DecisionOutput(NamedTuple):
    water_pump: PumpControlOutput
    nutrient_pump: PumpControlOutput
    light_on: bool


class PlantEnvironment:
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

    def update(self, temperature: float | int | None, humidity: float | int | None, nitrogen: float | int | None,
               moisture: float | int | None, light: float | int | None, ph_level: float | int | None):
        if temperature is not None:
            self.temperature = temperature

        if humidity is not None:
            self.relative_humidity = humidity

        if nitrogen is not None:
            self.nitrogen = nitrogen

        if moisture is not None:
            self.moisture = moisture

        if light is not None:
            self.light = light

        if ph_level is not None:
            self.ph_level = ph_level


class ActionStrategy:
    """
    A strategy for what control actions should be made based on the plant environment.
    """

    def update(self, environment: PlantEnvironment):
        pass

    def decide(self) -> DecisionOutput:
        pass


class DepletionStrategy:
    """
    A model for how a time step depletes the resources in a plant environment.
    """
    plant: PlantParameters

    def __init__(self, plant: PlantParameters):
        self.plant = plant

    def step(self, environment: PlantEnvironment) -> PlantEnvironment:
        pass


class GrowthStrategy:
    """
    A model for how a decision (water or nutrient pump length, or light level) affects the plant environment.
    """
    plant: PlantParameters

    def __init__(self, plant: PlantParameters):
        self.plant = plant

    def apply_decision(self, decision: DecisionOutput, environment: PlantEnvironment) -> PlantEnvironment:
        pass


class PlantModelTuner:
    light_impact: float = 1
    nitrogen_impact: float = 1
    moisture_impact: float = 1
    vpd_impact: float = 1
    ph_impact: float = 1


class PlantModel:
    """
    A model of a plant that uses growth and depletion strategies
    This model uses a `ActionStrategy` and `DepletionStrategy` to slowly deplete the values in the plant.
    """

    plant: PlantParameters
    action_strategy: ActionStrategy
    growth_strategy: GrowthStrategy
    depletion_strategy: DepletionStrategy
    environment: PlantEnvironment

    tuner: PlantModelTuner

    def __init__(self, plant: PlantParameters, action_strategy: ActionStrategy, growth_strategy: GrowthStrategy,
                 depletion_strategy: DepletionStrategy, environment: PlantEnvironment = PlantEnvironment(),
                 tuner: PlantModelTuner = PlantModelTuner()):
        self.plant = plant
        self.action_strategy = action_strategy
        self.growth_strategy = growth_strategy
        self.depletion_strategy = depletion_strategy
        self.environment = environment
        self.tuner = tuner

    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        """
        Provide the plant model with new true values.
        :param temperature: The temperature in degrees Celsius
        :param humidity: The relative humidity percentage
        :param nitrogen: Current level of nitrogen in the soil, parts per million (ppm)
        :param moisture: Relative moisture % of the soil
        :param light: Current light level in Photosynthetic Photon Flux Density (PPFD), µmol/m²/s.
        :param ph_level: Current ph level of the soil (0-14)
        """
        self.environment.update(temperature, humidity, nitrogen, moisture, light, ph_level)
        self.action_strategy.update(self.environment)

    def step(self):
        """
        Step the plant model one time step forward.
        :return:
        """
        # Deplete the resources in the environment.
        self.environment = self.depletion_strategy.step(self.environment)

        # Update the growth strategy with our new nitrogen and moisture guesses.
        self.action_strategy.update(self.environment)

    def decide(self) -> DecisionOutput:
        """
        Decide what controls the plant currently needs
        :return:
        """
        # Make decisions based on the current environment.
        decisions = self.action_strategy.decide()
        # Update the environment with the decisions we just made.
        self.environment = self.growth_strategy.apply_decision(decisions, self.environment)
        return decisions

    def stress(self) -> float:
        """
        A quick and dirty calculation of how stressed out a plant is based on how far out of the normal operating conditions
        the plant is.
        :returns a basic stress indicator for the plant's current health based on the environment
        """
        # Import here since this would pollute the top level imports of this file.
        from greenhouse_lib.model.utility import deviation, percentage_out_of_range, vpd

        light_deviation = abs(
            deviation(percentage_out_of_range(self.environment.light, self.plant.light.min, self.plant.light.max)))
        nitrogen_deviation = abs(deviation(
            percentage_out_of_range(self.environment.nitrogen, self.plant.nitrogen.min, self.plant.nitrogen.max)))
        moisture_deviation = abs(deviation(
            percentage_out_of_range(self.environment.moisture, self.plant.moisture.min, self.plant.moisture.max)))
        ph_deviation = abs(
            deviation(percentage_out_of_range(self.environment.ph_level, self.plant.ph.min, self.plant.ph.max)))

        vapor_pressure_deficit = vpd(self.environment.temperature, self.environment.relative_humidity)
        vpd_deviation = abs(
            deviation(percentage_out_of_range(vapor_pressure_deficit, self.plant.vpd.min, self.plant.vpd.max)))

        return (self.tuner.light_impact * light_deviation +
                self.tuner.nitrogen_impact * nitrogen_deviation +
                self.tuner.moisture_impact * moisture_deviation +
                self.tuner.vpd_impact * vpd_deviation + ph_deviation)
