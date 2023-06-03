'''This code analyses the attentiation for different filters from the ones we tried to implement.
analysis only
This will not be in the pico
Written by Ana'''

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from functions_and_classes import*
from scipy.signal import butter, bode, TransferFunction

def calculate_butterworth_highpass_coeffs(cutoff_freq, sample_rate, order):
    # Calculate the normalized cutoff frequency
    normalized_cutoff = cutoff_freq / (sample_rate / 2)

    # Design the Butterworth high-pass filter
    b, a = butter(order, normalized_cutoff, btype='highpass', analog=False, output='ba')

    return b, a

# Example usage
cutoff_freq = 1.5  # Cutoff frequency in Hz
sample_rate = 100  # Sample rate in Hz
order = 9  # Filter order

b, a = calculate_butterworth_highpass_coeffs(cutoff_freq, sample_rate, order)

# The resulting filter coefficients
print("b coefficients:", b)
print("a coefficients:", a)


tf = TransferFunction(b, a)

# Compute the frequency response (magnitude and phase)
w, mag, phase = bode(tf)

# Convert angular frequency to Hz
fs = 1000  # Sample rate
f = w * fs / (2 * np.pi)

# Plot the magnitude response (in dB)
plt.figure()
plt.semilogx(f, mag)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.title('Bode Plot - Magnitude Response for F=3')
plt.grid(True)
plt.show()

# Plot the phase response
plt.figure()
plt.semilogx(f, phase)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.title('Bode Plot - Phase Response')
plt.grid(True)
plt.show()
'''Bfilter = ButterworthFilter(9,20, 0.01)
b = Bfilter.coefficients
print(b)
w, h = signal.freqz(b, fs=100)

fig, ax1 = plt.subplots()
ax1.set_title('Butterworth filter (9,20,0.01)  frequency response')

ax1.plot(w, 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Amplitude [dB]', color='b')
ax1.set_xlabel('Frequency [rad/sample]')
ax1.grid(True)
'''

