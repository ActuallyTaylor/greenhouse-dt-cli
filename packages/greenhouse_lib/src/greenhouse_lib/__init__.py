from greenhouse_lib.model.growth.basic_strategy import out_of_range_penalty
import matplotlib.pyplot as plt

def main() -> None:
    test_range = range(0, 100)
    max = 35
    min = 65

    values = []

    for x in test_range:
        values.append(out_of_range_penalty(max, min, x))

    plt.plot(values)
    plt.ylabel('Values')
    plt.show()
