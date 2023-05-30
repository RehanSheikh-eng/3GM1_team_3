import numpy as np
import matplotlib.pyplot as plt
from detrending_and_LPfiltering_data import extracted_tremor_data


data = extracted_tremor_data # Replace with your actual data
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

