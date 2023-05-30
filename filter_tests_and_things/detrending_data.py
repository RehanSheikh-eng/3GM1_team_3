
from defandclasses import ButterworthFilter
import numpy as np
import matplotlib.pyplot as plt


def readjoystickTextFile():
    data = []
    xPos_vector = []
    yPos_vector = []
    iteration = []
    j = 0
    with open('tremor_analysis/JoystickTextFiles/tremor_simulator_100HZ.txt') as file:
        for line in file:
            j += 1
            nums = ((line.strip().split(','))) # Convert each line to a float and append to the data list
            values = []
            for i in range(3):
                values.append(float(nums[i]))
            xPos_vector.append(values[1])
            yPos_vector.append(values[2])
            iteration.append(j)
    return xPos_vector, yPos_vector


Bfilter = ButterworthFilter(9, 3, 0.01)
listXPOS, listYPOS = readjoystickTextFile()
plt.plot(listXPOS)
plt.plot(listYPOS)
plt.show()

data = listXPOS  # Replace with your actual data

# Compute the power spectrum using Fourier transform
fft_data = np.fft.fft(data)

# Frequency values
sampling_rate = 100  # Replace with your actual sampling rate
freq = np.fft.fftfreq(len(data), d=1/sampling_rate)

# Plot the frequencies
positive_freq = freq[:len(data)//2]  # Positive frequencies only (up to Nyquist frequency)
plt.plot(positive_freq, np.abs(fft_data[:len(data)//2]))
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Data')
plt.show()

