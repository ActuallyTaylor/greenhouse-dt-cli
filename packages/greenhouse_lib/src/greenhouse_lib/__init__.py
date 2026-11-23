from greenhouse_lib.model.growth.basic_strategy import percentage_out_of_range
import matplotlib.pyplot as plt

def main() -> None:
    test_range = range(0, 100)
    max = 50
    min = 40

    values = []

    for x in test_range:
        # values.append(percentage_out_of_range(x, max, min))
        print('x', x, percentage_out_of_range(x, max, min))

    print(values)
    plt.plot(values)
    plt.ylabel('Values')
    plt.show()
