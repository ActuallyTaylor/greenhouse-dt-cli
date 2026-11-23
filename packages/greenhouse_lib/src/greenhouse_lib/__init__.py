from greenhouse_lib.model.growth.basic_strategy import percentage_out_of_range, BasicGrowthStrategy
from greenhouse_lib.model.models import GrowthStrategy, DecisionOutput
import matplotlib.pyplot as plt

from greenhouse_lib.model.parameters import tomato_parameters

def run_decision_and_update(strategy: GrowthStrategy, temperature: float, humidity: float, nitrogen, moisture, light,
                            ph_level) -> DecisionOutput:
    strategy.update(temperature, humidity, nitrogen, moisture, light, ph_level)
    return strategy.decide()

def main() -> None:
    growth_strategy = BasicGrowthStrategy(tomato_parameters)

    decision = run_decision_and_update(growth_strategy, 70, 70, 20, 60, 500, 6)

    print(decision)