import numpy as np
import scipy.signal as signal

# Define filter parameters
sampling_rate = 100  # Sampling rate in Hz
pass_range = [3, 17]  # Pass frequency range in Hz
filter_order = 4  # Filter order

# Calculate the Butterworth filter coefficients
nyquist_rate = 0.5 * sampling_rate
normalized_pass_range = [f / nyquist_rate for f in pass_range]
sos = signal.butter(filter_order, normalized_pass_range, btype='band', output='sos')

# Print the second-order sections (biquad) coefficients
print("Second-order sections (biquad) coefficients for bandpass filter:")
print(sos)

# Define filter parameters
sampling_rate = 100  # Sampling rate in Hz
pass_frequency = 3  # Pass frequency in Hz
filter_order = 4  # Filter order

# Calculate the Butterworth filter coefficients
nyquist_rate = 0.5 * sampling_rate
normalized_pass_frequency = pass_frequency / nyquist_rate
sos = signal.butter(filter_order, normalized_pass_frequency, btype='lowpass', output='sos')

# Print the second-order sections (biquad) coefficients
print("Second-order sections (biquad) coefficients:")
print(sos)