from greenhouse_lib.model.models import DepletionStrategy, PlantEnvironment, PlantParameters
from greenhouse_lib.model.utility import percentage_out_of_range, vpd, deviation


class BasicDepletionStrategy(DepletionStrategy):
    base_moisture_loss = 0.5  # % per step
    base_nitrogen_loss = 0.2  # ppm per step

    def __init__(self, plant: PlantParameters, base_moisture_loss: float = 0.5, base_nitrogen_loss: float = 0.2):
        super().__init__(plant)
        self.base_moisture_loss = base_moisture_loss
        self.base_nitrogen_loss = base_nitrogen_loss

    def step(self, environment: PlantEnvironment):
        # Make an explicit copy of the environment, python does this automatically, but it is hidden behavior.
        environment = environment

        light_deviation = deviation(
            percentage_out_of_range(environment.light, self.plant.light.min, self.plant.light.max))
        nitrogen_deviation = deviation(
            percentage_out_of_range(environment.nitrogen, self.plant.nitrogen.min, self.plant.nitrogen.max))
        moisture_deviation = deviation(
            percentage_out_of_range(environment.moisture, self.plant.moisture.min, self.plant.moisture.max))

        vapor_pressure_deficit = vpd(environment.temperature, environment.relative_humidity)
        vpd_deviation = deviation(
            percentage_out_of_range(vapor_pressure_deficit, self.plant.vpd.min, self.plant.vpd.max))

        # Baseline water loss
        water_mult = self.base_moisture_loss
        nitrogen_mult = self.base_nitrogen_loss

        ### VPD ###
        # A high VPD will lose water quicker. So multiply by 1 + vpd to increase the multiplier. A lower vpd will reduce the water multiple.
        water_mult *= (1 + vpd_deviation)

        ### Light ###
        # High light means more photosynthesis, so water and nitrogen deplete quicker. Low light, less depletion.
        water_mult *= (1 + light_deviation)
        nitrogen_mult *= (1 + light_deviation)

        ### Moisture ###
        if moisture_deviation > 0:
            # Waterlogged roots, so they uptake less water and nitrogen leaches out of the soil.
            water_mult *= max(0.0, 1 - 0.5 * moisture_deviation)
            # If there is extra water, it will evaporate out
            water_mult += 2.0 * moisture_deviation

            nitrogen_mult *= (1 + moisture_deviation)
        elif moisture_deviation < 0:
            # Soil is dry, so moisture uptake falls quickly, and less N is lost in the soil
            water_mult *= max(0.0, 1 + 2.0 * moisture_deviation)
            nitrogen_mult *= max(0.0, 1 + moisture_deviation)

        ### Nitrogen ###
        if nitrogen_deviation > 0:
            # High nitrogen stresses the plant and makes water update slower
            water_mult *= max(0.0, 1 - 0.3 * nitrogen_deviation)

        # Low VPD/light deviations can push multipliers negative, so clamp them before subtracting.
        water_mult = max(0.0, water_mult)
        nitrogen_mult = max(0.0, nitrogen_mult)

        environment.moisture = max(0.0, environment.moisture - water_mult)
        environment.nitrogen = max(0.0, environment.nitrogen - nitrogen_mult)

        return environment
