
from defandclasses import *

#testing
if __name__ == '__main__':
    # Create a low-pass filter with alpha = 0.2
    filter = LowPassFilter(0.2)

    # Simulate input data
    input_data = [0.5, 0.8, 0.3, 0.9, 0.6]

    # Apply the filter to each input data point
    for value in input_data:
        filtered_value = filter.update(value)
        print("Input: {:.2f} Filtered: {:.2f}".format(value, filtered_value))

    # Create a high-pass filter with alpha = 0.2
    filter = HighPassFilter(0.2)

    # Simulate input data
    input_data = [1.2, 0.8, 1.5, 1.0, 0.5]

    # Apply the filter to each input data point
    for value in input_data:
        filtered_value = filter.update(value)
        print("Input: {:.2f} Filtered: {:.2f}".format(value, filtered_value))

    import math

    # Create a Butterworth filter with order = 9, cutoff frequency = 1.5 Hz, and sampling period = 0.1 s
    filter = ButterworthFilter(9, 1.5, 0.1)

    # Simulate input data
    input_data = [0.5, 0.8, 0.3, 0.9, 0.6]

    # Apply the filter to each input data point
    for value in input_data:
        filtered_value = filter.update(value)
        print("Input: {:.2f} Filtered: {:.2f}".format(value, filtered_value))

while True:
    ax_new = sensor.accel.x
    filtered_ax = low_pass_filter(filtered_ax, ax_new)