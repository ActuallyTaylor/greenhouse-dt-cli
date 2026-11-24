# Greenhouse Library
This package contains shared logic for the operation of a digital greenhouse twin.

## Plant Modeling
This package includes a fairly basic (yet still complex) model of a plant. It is broken into two *strategies*, the `GrowthStrategy` and `DepletionStrategy`. These work together to create a model that is able to slowly deplete its environmental resources, while replenishing them through basic watering and nutrient watering.

This model also produces a `DecisionOutput`, which informs the digital twin of the action that should be taken to most help the plant. This decision is made by the `ActionStrategy`.

### Growth Strategy

The growth strategy 

### Depletion Strategy

### Action Strategy