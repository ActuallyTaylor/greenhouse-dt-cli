from enum import Enum
from typing import NamedTuple


class PlantStressModel:
    def predict(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level) -> float:
        pass

class PumpControlOutput(Enum):
    NONE = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3

class DecisionOutput(NamedTuple):
    pump: PumpControlOutput
    light_on: bool

    def __init__(self, pump_control: PumpControlOutput, light_on: bool):
        self.pump = pump_control
        self.light_on = light_on

class GrowthStrategy:
    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        pass

    def decide(self) -> DecisionOutput:
        pass

class DepletionStrategy:
    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        pass
