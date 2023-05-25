"""
Plot data in joystick

"""
import array
import numpy as np
import matplotlib.pyplot as plt
from frequency_of_tremor_test import analyze_frequency


# Sampling parameters
sampling_freq = 100  # Sampling frequency in Hz
num_samples = 323  # Number of samples to acquire


data = []
xPos_vector = []
yPos_vector = []
iteration = []
j = 0
with open('tremor_analysis/tremor_simulator_100HZ.txt', 'r') as file:
    for line in file:
        j += 1
        nums = ((line.strip().split(','))) # Convert each line to a float and append to the data list
        values = []
        for i in range(3):
            values.append(float(nums[i]))
        xPos_vector.append(values[1])
        yPos_vector.append(values[2])
        iteration.append(j)
 
plt.plot(iteration,xPos_vector,label = 'xpos')
plt.plot(iteration,yPos_vector, label = 'ypos')
plt.show()
plt.legend()

print("finish")

# Allocate buffer for signal samples
signal_buffer = array.array("h", [0] * num_samples)


    # Acquire signal samples
signal_buffer = input_data = xPos_vector

    # Convert signal buffer to a numpy array
signal_np = np.array(signal_buffer)

    # Analyze frequency and determine the dominant frequency
dominant_frequency = analyze_frequency(signal_np)
print("Dominant Frequency: {:.2f} Hz".format(dominant_frequency))
print("run")
