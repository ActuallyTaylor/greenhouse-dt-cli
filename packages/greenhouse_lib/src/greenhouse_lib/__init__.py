from greenhouse_lib.model.growth.basic_strategy import out_of_range_penalty
import matplotlib.pyplot as plt

def main() -> None:
    test_range = range(0, 100)
    max = 25
    min = 50

    values = []

    for x in test_range:
        values.append(out_of_range_penalty(max, min, x))

    plt.plot(values)
    plt.ylabel('Values')
    plt.show()
