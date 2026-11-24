import numpy as np


def out_of_range_penalty(min_value: float | int, max_value: float | int, value: float | int, weight: float | int = 1) -> float | int:
    """
    Penalizes values based on how far from the middle of the range they are. Values outside the range are penalized twice as hard.
    :param min_value: Range minimum
    :param max_value: Range maximum
    :param value: Value to calculate penalty for.
    :param weight: Weight of the penalty.
    :return: Penalty for how far value is from the center of the range.
    """

    median = (min_value + max_value) / 2

    # Drop the weight by 0.5 if we are in range.
    if min_value < value < max_value:
        weight = weight * 0.5

    return weight * (np.abs(value - median) ** 2)
