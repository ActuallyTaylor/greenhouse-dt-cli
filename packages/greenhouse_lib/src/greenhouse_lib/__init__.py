from greenhouse_lib.model.growth.basic_strategy import BasicGrowthStrategy
from greenhouse_lib.model.parameters import tomato_parameters


def main():
    growth_strategy = BasicGrowthStrategy(tomato_parameters)

    growth_strategy.temperature = 70
    growth_strategy.relative_humidity = 68

    print(growth_strategy.make_vpd_decision())