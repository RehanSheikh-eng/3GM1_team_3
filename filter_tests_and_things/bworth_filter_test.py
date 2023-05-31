from functions_and_classes import*
import matplotlib.pyplot as plt


# generated sine wave parameters
frequency = 2  # Frequency of the sine wave in Hz
amplitude = 1.0  # Amplitude of the sine wave
duration = 1.0  # Duration of the signal in seconds
sampling_rate = 100  # Number of samples per second
# parameters
order = 9
cutoff_f = 3
sampling_period = 0.01

Bfilter = ButterworthFilter(9, 3, 0.01)

# Simulate input data
#input_data = generate_sine_wave(frequency, amplitude, duration, sampling_rate)

sampling_rate = 100 # Replace with your desired sampling rate
duration = 2.0  # Total duration of the signal in seconds
frequency = 10.0  # Frequency of the sine wave in Hz
pause_duration = 1.0  # Duration of the pause between sine waves in seconds

# Time values
t_sine = np.arange(0, duration, 1 / sampling_rate)
t_pause = np.arange(0, pause_duration, 1 / sampling_rate)

# Create the input data
sine_wave = np.sin(2 * np.pi * frequency * t_sine)
pause = np.sin(2 * np.pi * frequency*1.1 * t_pause)


# Concatenate the sine waves with the pause
input_data = np.concatenate([sine_wave, pause, sine_wave])
t = np.arange(0, len(input_data)) / sampling_rate

# t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)


# Apply the filter to each input data point
filtered_signal= []
for value in input_data:
    filtered_value = Bfilter.update(value)
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