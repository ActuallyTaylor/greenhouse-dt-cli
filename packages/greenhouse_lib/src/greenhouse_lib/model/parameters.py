from PIL.ImageChops import lighter


class ParameterPack:
    min: float
    max: float

    def __init__(self, min: float, max: float):
        self.min = min
        self.max = max

class PlantParameters:
    vpd: ParameterPack
    nitrogen: ParameterPack
    moisture: ParameterPack
    ph: ParameterPack
    light: ParameterPack

    def __init__(self, vpd: ParameterPack, nitrogen: ParameterPack, moisture: ParameterPack, ph: ParameterPack, light: ParameterPack):
        self.vpd = vpd
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.ph = ph
        self.light = light

tomato_parameters = PlantParameters(
    # Ideal range for VDP for a tomato: https://vpdcharts.com/ideal-vpd-for-tomatoes/
    vpd=ParameterPack(min=0.8, max=1.2),
    # Ideal range for nitrogen ppm: https://extension.colostate.edu/resource/vegetable-gardening-nitrogen-recommendations/
    nitrogen=ParameterPack(min=15,max=40),
    # Ideal range for tomato soil: https://lawngardenpro.com/how-wet-should-tomato-plant-soil-be/
    moisture=ParameterPack(min=50, max=70),
    # Ideal ph range for tomato soil: https://extension.rutgers.edu/fs678
    ph=ParameterPack(min=6, max=6.5),
    # Idea light range for tomatoes: https://www.thriveagritech.com/blog-posts/tomato-lighting-requirements-greenhouse-dli-ppfd-guide
    light=ParameterPack(min=400,max=600)
)
