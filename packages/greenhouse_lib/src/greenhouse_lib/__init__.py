from greenhouse_lib.model.growth.basic_strategy import BasicGrowthStrategy
from greenhouse_lib.model.parameters import PlantParameters, ParameterPack

# MARK: Plant Definitions
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

def main():
    pass