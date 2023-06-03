'''we wanted to compare the scipy libraries with our simplified filters
written by Ana and only used for testing'''

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Generate the input sine wave
frequency = 70  # Frequency of the sine wave in Hz
amplitude = 1.0  # Amplitude of the sine wave
duration = 1.0  # Duration of the signal in seconds
sampling_rate = 1000  # Number of samples per second

class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.filtered_value = 0.0

    def update(self, new_value):
        self.filtered_value = (self.alpha * new_value) + ((1 - self.alpha) * self.filtered_value)
        return self.filtered_value


t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
input_signal = amplitude * np.sin(2 * np.pi * frequency * t)

# Define the lowpass filter
cutoff_frequency = 50  # Cutoff frequency of the lowpass filter in Hz
order = 4  # Filter order

nyquist_frequency = 0.5 * sampling_rate
normalized_cutoff = cutoff_frequency / nyquist_frequency
b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)

# Apply the lowpass filter to the input signal
filtered_signal = signal.lfilter(b, a, input_signal)

# Plot the input and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, input_signal)
plt.title('Input Signal (Sine Wave)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(t, filtered_signal)
plt.title('Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
