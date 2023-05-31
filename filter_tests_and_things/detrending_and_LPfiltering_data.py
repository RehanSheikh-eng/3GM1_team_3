
from functions_and_classes import ButterworthFilter,LowPassFilter
import numpy as np
import matplotlib.pyplot as plt


def readjoystickTextFile():
    data = []
    xPos_vector = []
    yPos_vector = []
    iteration = []
    j = 0
    with open('../tremor_analysis/JoystickTextFiles/tremor_simulator_100HZ.txt') as file:
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


Bfilter = ButterworthFilter(9, 3.0, 0.01)
alpha = 0.6
LPfilter = LowPassFilter(alpha)
listXPOS, listYPOS = readjoystickTextFile()
# plt.plot(listXPOS)
plt.plot(listYPOS)
plt.xlabel('samples')
plt.ylabel('position')
plt.title('Y position of the joystick')
plt.show()

data = listYPOS  # Replace with your actual data

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
plt.title('Frequency Spectrum of Unfiltered Data')
plt.show()

filtered_data = []
for i in range(len(data)-1):
    filtered_value = LPfilter.update(data[i])
    filtered_data.append(filtered_value)
    fft_data = np.fft.fft(filtered_data)
freq = np.fft.fftfreq(len(filtered_data), d=1/sampling_rate)

# Plot the frequencies
positive_freq_filtered = freq[:len(filtered_data)//2]  # Positive frequencies only (up to Nyquist frequency)
plt.plot(positive_freq_filtered, np.abs(fft_data[:len(filtered_data)//2]))
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Noise Filtered Data')
plt.show()

filtered_data1 = []
for i in range(len(filtered_data)-1):
    filtered_value = Bfilter.update(filtered_data[i])
    filtered_data1.append(filtered_value)
    fft_data = np.fft.fft(filtered_data1)
freq = np.fft.fftfreq(len(filtered_data1), d=1/sampling_rate)

# Plot the frequencies
positive_freq_filtered1 = freq[:len(filtered_data1)//2]  # Positive frequencies only (up to Nyquist frequency)
plt.plot(positive_freq_filtered1, np.abs(fft_data[:len(filtered_data1)//2]))
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Butterworth Filtered Data')
plt.show()

plt.plot(filtered_data)
plt.plot(filtered_data1)
plt.xlabel('samples')
plt.ylabel('position')
plt.title('Unfiltered and Filtered Position of the Joystick')
plt.show()

extracted_tremor_data = []
for i in range(len(filtered_data)-1):
    extracted_tremor_value = filtered_data[i] - filtered_data1[i]
    extracted_tremor_data.append(extracted_tremor_value)

plt.plot(extracted_tremor_data)
plt.xlabel('samples')
plt.ylabel('position')
plt.title('Extracted Tremor Data')
plt.show()

print(extracted_tremor_data)