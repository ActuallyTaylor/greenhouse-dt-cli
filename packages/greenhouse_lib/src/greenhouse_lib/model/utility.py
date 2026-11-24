def percentage_out_of_range(value: float | int, minimum: float | int, maximum: float | int):
    # Avoid divide by zero errors.
    if minimum == maximum:
        return 0.0

    # Swap minimum and maximum in case they are flipped.
    if minimum > maximum:
        minimum, maximum = maximum, minimum

    return ((value - minimum) / (maximum - minimum)) * 100
