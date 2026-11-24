from greenhouse_lib.model.models import DepletionStrategy, PlantEnvironment, GrowthStrategy, DecisionOutput


class BasicGrowthStrategy(GrowthStrategy):

    def apply_decision(self, decision: DecisionOutput, environment: PlantEnvironment) -> PlantEnvironment:
        pass
