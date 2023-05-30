import array
import math
import numpy as np


# Sampling parameters
sampling_freq = 1000  # Sampling frequency in Hz
num_samples = 10000    # Number of samples to acquire
# generated sine wave parameters
frequency = 5  # Frequency of the sine wave in Hz
amplitude = 1.0  # Amplitude of the sine wave
duration = 10.0  # Duration of the signal in seconds
sampling_rate = 1000  # Number of samples per second

def generate_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return signal
def tremor_window_fft(fft_result,fft_freq,tremor_window): #t window is lower then upper bound
    new_fft_result=[]
    new_fft_freq=[]
    for i in range(len(fft_freq)):
        if abs(fft_freq[i])>= tremor_window[0] and abs(fft_freq[i]) <= tremor_window[1]:
            new_fft_result.append(fft_result[i])
            new_fft_freq.append(fft_freq[i])
    return new_fft_result,new_fft_freq
# Function to perform FFT and find the dominant frequency
def analyze_frequency(signal):
    # Perform FFT on the signal
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(len(signal), 1 / sampling_freq)
    fft_result,fft_freq= tremor_window_fft(fft_result,fft_freq,(3,17))

    # Find the index of the maximum magnitude in the FFT result
    max_index = np.argmax(np.abs(fft_result))

    # Extract the dominant frequency
    dominant_freq = abs(fft_freq[max_index])

    return dominant_freq

# Main loop for signal acquisition and analysis
def main():
    # Allocate buffer for signal samples
    signal_buffer = array.array("h", [0] * num_samples)


    # Acquire signal samples
    signal_buffer = input_data

    # Convert signal buffer to a numpy array
    signal_np = np.array(signal_buffer)

    # Analyze frequency and determine the dominant frequency
    dominant_frequency = analyze_frequency(signal_np)

    # Print the dominant frequency
    print("Dominant Frequency: {:.2f} Hz".format(dominant_frequency))

    # Delay before acquiring the next set of samples

# Run the main function


input_data = (generate_sine_wave(frequency, amplitude, duration, sampling_rate) + generate_sine_wave(frequency/2, amplitude*2, duration, sampling_rate))
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
main()