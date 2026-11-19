import math

from greenhouse_lib.model.models import GrowthStrategy, DecisionOutput, PumpControlOutput


# MARK: Static Methods
def vdp(temperature: float, relative_humidity: float) -> float:
    """
    Computes the Vapor-pressure deficit for a greenhouse
    Based on: https://en.wikipedia.org/wiki/Vapour-pressure_deficit#Computing_VPD_for_plants_in_a_greenhouse
    :param relative_humidity:
    :param temperature:
    :return:
    """
    A = -1.0440397e4
    B = -11.29465
    C = -2.7022355e-2
    D = 1.289036e-5
    E = -2.4780681e-9
    F = 6.545973

    rankine_temperature = temperature + 459.67
    exponent = (A / rankine_temperature) + B + (C * rankine_temperature) + (math.pow(D * rankine_temperature, 2)) + (math.pow(E * rankine_temperature, 3)) + (F * math.log(rankine_temperature))
    saturation_vapor_pressure = math.pow(math.e, exponent)

    vapor_pressure_deficit = saturation_vapor_pressure * (1 - (relative_humidity / 100))

    return vapor_pressure_deficit

# MARK: Growth Strategy
class BasicGrowthStrategy(GrowthStrategy):
    # Current temperature, °C
    temperature: float | int = 0
    # Relative humidity, %
    relative_humidity: float | int = 0
    # Current level of nitrogen in the soil, mg/kg
    nitrogen: float | int = 0
    # Moisture % of the soil
    moisture: float | int = 0
    # Current light level in Photosynthetic Photon Flux Density (PPFD), µmol/m²/s.
    light: float | int = 0
    # Current ph level of the soil (0-14)
    ph_level: float | int = 0

    def update(self, temperature: float, humidity: float, nitrogen, moisture, light, ph_level):
        self.temperature = temperature
        self.relative_humidity = humidity
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.light = light
        self.ph_level = ph_level

    def decide(self) -> DecisionOutput:
        vapor_pressure_deficit = vdp(self.temperature, self.relative_humidity)

        return DecisionOutput(PumpControlOutput.NONE, False)

    # Nitrogen Stress, pH Stress
    # Moisture?
    # Light sensor in PPFD, for Daily Light Integral