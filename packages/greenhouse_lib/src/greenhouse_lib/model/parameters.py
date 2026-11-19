
class ParameterPack:
    min: float
    max: float

    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

class PlantParameters:
    vdp: ParameterPack

    def __init__(self, vdp: ParameterPack):
        self.vdp = vdp

tomato_parameters = PlantParameters(
    # Ideal range for VDP for a tomato: https://vpdcharts.com/ideal-vpd-for-tomatoes/
    vdp=ParameterPack(min=0.8, max=1.2),
)
