# Greenhouse Library
This package contains shared logic for the operation of a digital greenhouse twin.

## Plant Modeling
This package includes a fairly basic (yet still complex) model of a plant. It is broken into two *strategies*, the `GrowthStrategy` and `DepletionStrategy`. These work together to create a model that is able to slowly deplete its environmental resources, while replenishing them through basic watering and nutrient watering.

This model also produces a `DecisionOutput`, which informs the digital twin of the action that should be taken to most help the plant. This decision is made by the `ActionStrategy`.

### Growth Strategy

The growth strategy applies decision made by an `ActionStrategy`, based on asset information in `PumpPack`s. A sample pump pack for a 1:200 nutrient injector is used for this project:

```python
nutrient_pump_parameters = PumpPack(
    # 250 mL, 6.25 ppm into soil
    long=PumpBonuses(nitrogen=ParameterPack(min=5.25, max=7.25), moisture=ParameterPack(min=50, max=70)),
    # 125 mL, 3.125 ppm into soil
    medium=PumpBonuses(nitrogen=ParameterPack(min=2.125, max=4.125), moisture=ParameterPack(min=50, max=70)),
    # 75 mL, 1.875 ppm into soil
    short=PumpBonuses(nitrogen=ParameterPack(min=0.875, max=2.875), moisture=ParameterPack(min=50, max=70))
)
```

### Depletion Strategy

The depletion strategy uses a fairly rudimentary cause and effect model for determining how the environment depletes its resources each time step. 

The rules used are:

1. Vapor Pressure Deficit
   1. A high VPD will lose water quicker. 
   2. A lower vpd will reduce the water multiple.
2. High light means more photosynthesis, so water and nitrogen deplete quicker. Low light, less depletion.
3. Moisture
   1. Waterlogged roots, so they uptake less water and nitrogen leaches out of the soil.
   2. If there is extra water, it will evaporate out
4. High nitrogen stresses the plant and makes water update slower
5. Low VPD/light deviations can push multipliers negative, so clamp them before subtracting.

### Action Strategy

The job of an action strategy is to decide what the actions should be taken on the environment. The basic action strategy uses a democratic decision process, where four metrics are considered: vapor pressure deficit, moisture, and nitrogen. Each of these metrics is scored on how far out of the preferred range for the plant the value is. 