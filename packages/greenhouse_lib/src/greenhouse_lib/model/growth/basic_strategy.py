from greenhouse_lib.model.models import DepletionStrategy, PlantEnvironment, GrowthStrategy, DecisionOutput, \
    PumpControlOutput, PlantParameters, PumpPack


class BasicGrowthStrategy(GrowthStrategy):
    water_pump_behavior: PumpPack
    nutrient_pump_behavior: PumpPack

    def __init__(self, plant: PlantParameters, water_pump_behavior: PumpPack, nutrient_pump_behavior: PumpPack):
        super().__init__(plant)
        self.water_pump_behavior = water_pump_behavior
        self.nutrient_pump_behavior = nutrient_pump_behavior


    def apply_decision(self, decision: DecisionOutput, environment: PlantEnvironment) -> PlantEnvironment:
        # Make an explicit copy of the environment, python does this automatically, but it is hidden behavior.
        environment = environment

        nutrient_pump_bonus_pack = self.nutrient_pump_behavior.pack_for(decision.nutrient_pump)

        if nutrient_pump_bonus_pack:
            environment.moisture += nutrient_pump_bonus_pack.moisture.random()
            environment.nitrogen += nutrient_pump_bonus_pack.nitrogen.random()

        water_pump_bonus_pack = self.water_pump_behavior.pack_for(decision.nutrient_pump)

        if water_pump_bonus_pack:
            environment.moisture += water_pump_bonus_pack.moisture.random()
            environment.nitrogen += water_pump_bonus_pack.nitrogen.random()

        return environment