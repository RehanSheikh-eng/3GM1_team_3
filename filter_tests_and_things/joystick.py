import numpy as np
import math
import matplotlib.pyplot as plt
from collections import deque
from functions_and_classes import *


#generated sine wave parameters
frequency = 20  # Frequency of the sine wave in Hz
amplitude = 1.0  # Amplitude of the sine wave
duration = 1.0  # Duration of the signal in seconds
sampling_rate = 1000  # Number of samples per second
#lowpass filter parameters
cutoff_frequency= 10
low_alpha = 1 / (2 * math.pi * cutoff_frequency)
#setting up queue paramteters
queue_length = 1000  # Length of the queue
sample_queue = deque(maxlen=queue_length)


input_data = generate_sine_wave(frequency, amplitude, duration, sampling_rate)
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)



filter1 = LowPassFilter(low_alpha)
filtered_signal=[]
for value in input_data:
    filtered_value = filter1.update(value)
    filtered_signal.append(filtered_value)

# Plot the input and filtered signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, input_data)
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