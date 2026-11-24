from greenhouse_lib.model.models import PlantParameters, ParameterPack, PumpBonuses, PumpPack

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

# How much a single pump effects the environment, based on information in https://hort.cornell.edu/greenhouse/crops/factsheets/FertilizerCalculations.pdf
# The nutrient pump is a 1:200 injector containing 3.79 liters of 150 ppm nitrogen. Pump lengths were derived from a chemical engineer's best guess.
# We are assuming that the plants are potted in 6kg of dry weight soil (1 12 inch pot)
#
# Math:
# 3.79 liters of 150 ppm nitrogen
# 1 ppm ~= 1 mg/l
# 75 ml / 1,000 ml = 0.075 l
# 150 mg/l * 0.075 l = 11.25 mg
#
# To convert back to PPM we need the soil weight (6 kg)
# 11.25 mg / 6 kg =  1.875 mg / kg
# 1 ppm = 1 mg / kg
# 1.875 mg / kg = 1.875 ppm
nutrient_pump_parameters = PumpPack(
    # 250 mL, 6.25 ppm into soil
    long=PumpBonuses(nitrogen=ParameterPack(min=5.25, max=7.25), moisture=ParameterPack(min=50, max=70)),
    # 125 mL, 3.125 ppm into soil
    medium=PumpBonuses(nitrogen=ParameterPack(min=2.125, max=4.125), moisture=ParameterPack(min=50, max=70)),
    # 75 mL, 1.875 ppm into soil
    short=PumpBonuses(nitrogen=ParameterPack(min=0.875, max=2.875), moisture=ParameterPack(min=50, max=70))
)

# Assuming 6kg dry weight of soil (1 12 inch pot)
# 125 ml = 125 g / 6,000 g = 0.02083333333 * 100 = 2.08%
water_pump_parameters = PumpPack(
    # 250 mL, 4.16 %
    long=PumpBonuses(nitrogen=ParameterPack(min=0, max=0), moisture=ParameterPack(min=3.66, max=4.66)),
    # 125 mL, 2.08 %
    medium=PumpBonuses(nitrogen=ParameterPack(min=0, max=0), moisture=ParameterPack(min=1.58, max=2.58)),
    # 75 mL, 1.25 %
    short=PumpBonuses(nitrogen=ParameterPack(min=0, max=0), moisture=ParameterPack(min=0.75, max=1.5))
)