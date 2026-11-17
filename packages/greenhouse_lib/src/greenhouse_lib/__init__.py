from enum import Enum
from typing import NamedTuple


class PlantStressModel():
    def predict(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level) -> float:
        pass

class PumpControlOutput(Enum):
    NONE = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3

class DecisionOutput(NamedTuple):
    pump: PumpControlOutput
    light: bool

class GrowthStrategy:
    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        pass

    def decide(self) -> DecisionOutput:
        pass

class BasicGrowthStrategy(GrowthStrategy):
    pass

class DeepQGrowthStrategy(GrowthStrategy):
    pass

class DepletionStrategy:
    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        pass

class BasicDepletionStrategy(DepletionStrategy):
    pass

