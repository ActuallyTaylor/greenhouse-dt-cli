import pytest

from greenhouse_lib.model.growth.basic_strategy import BasicGrowthStrategy
from greenhouse_lib.model.models import GrowthStrategy, DecisionOutput, PumpControlOutput

from greenhouse_lib.model.parameters import tomato_parameters


def run_decision_and_update(strategy: GrowthStrategy, temperature: float, humidity: float, nitrogen, moisture, light,
                            ph_level) -> DecisionOutput:
    strategy.update(temperature, humidity, nitrogen, moisture, light, ph_level)
    return strategy.decide()


def test_growth_decision():
    growth_strategy = BasicGrowthStrategy(tomato_parameters)

    decision = run_decision_and_update(growth_strategy, 70, 70, 30, 60, 500, 6)

    assert decision.light_on == True
    assert decision.water_pump == PumpControlOutput.MEDIUM
    assert decision.nutrient_pump == PumpControlOutput.MEDIUM


def test_vpd_decision():
    growth_strategy = BasicGrowthStrategy(tomato_parameters)

    growth_strategy.temperature = 75
    growth_strategy.relative_humidity = 65

    print(growth_strategy.make_vpd_decision())