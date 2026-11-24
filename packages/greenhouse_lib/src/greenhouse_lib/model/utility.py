import numpy as np

def deviation(value: float| int) -> float:
    """
    Convert a percentage out of range into a more manageable scalar.
    :param value: How far out of range a value is.
    :return: A scalar value, something like: -0.4, or +0.5.
    """
    if value > 100:
        # Subtract 100 to start the percent out of range at a base of 100.
        return (value - 100) / 100
    elif value < 0:
        return value / 100
    else:
        return 0

def percentage_out_of_range(value: float | int, minimum: float | int, maximum: float | int):
    # Avoid divide by zero errors.
    if minimum == maximum:
        return 0.0

    # Swap minimum and maximum in case they are flipped.
    if minimum > maximum:
        minimum, maximum = maximum, minimum

    return ((value - minimum) / (maximum - minimum)) * 100

def vpd(temperature: float, relative_humidity: float) -> float:
    """
    Computes the Vapor-pressure deficit for a greenhouse
    Based on: https://en.wikipedia.org/wiki/Vapour-pressure_deficit#Computing_VPD_for_plants_in_a_greenhouse
    :param relative_humidity:
    :param temperature: Degrees Celsius of the outside temperature
    :return:
    """
    A = -1.0440397e4
    B = -11.29465
    C = -2.7022355e-2
    D = 1.289036e-5
    E = -2.4780681e-9
    F = 6.5459673

    rankine_temperature = (temperature + 273.15) * 1.8
    exponent = (A / rankine_temperature) + B + (C * rankine_temperature) + D * (rankine_temperature ** 2) + E * (rankine_temperature ** 3) + (F * np.log(rankine_temperature))
    saturation_vapor_pressure = np.e ** exponent

    vapor_pressure_deficit = saturation_vapor_pressure * (1 - (relative_humidity / 100))

    # Convert the VPD in PSI to kPa
    return vapor_pressure_deficit * 6.894757
