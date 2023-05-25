import array
import math
import numpy as np


# Sampling parameters
sampling_freq = 1000  # Sampling frequency in Hz
num_samples = 10000    # Number of samples to acquire
#generated sine wave parameters
frequency = 5  # Frequency of the sine wave in Hz
amplitude = 1.0  # Amplitude of the sine wave
duration = 10.0  # Duration of the signal in seconds
sampling_rate = 1000  # Number of samples per second
#analysis variables
window_size=500 # for calculating intensities- it's the sample number
tremor_window= (3,17) #bounds of data we are using for analysis in Hz
intensity_threshold=1.5

#functions
def generate_sine_wave(frequency, amplitude, duration, sampling_rate):
    t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
    signal = amplitude * np.sin(2 * np.pi * frequency * t)
    return signal
def tremor_window_fft(fft_result,fft_freq,tremor_window): #t window is lower then the upper bound in hz
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
    fft_result,fft_freq= tremor_window_fft(fft_result,fft_freq,tremor_window)

    # Find the index of the maximum magnitude in the FFT result
    max_index = np.argmax(np.abs(fft_result))

    # Extract the dominant frequency
    dominant_freq = abs(fft_freq[max_index])

    return dominant_freq

def calculate_intensity(signal):
    '''the input of this function is a small sample of the signal in the window size.
     The values have to be positive so i will square the input signal'''
    # Calculate the area under the curve using the trapezoidal rule
    signal_squared= signal*signal
    area = np.trapz(signal_squared)
    intensity = area / window_size
    return intensity

def extract_tremor_from_signal():
    ''' this function extracts the intensities that correspond to one tremor, for further analysis.
    it also has to extract the actual x and y values in oder to extract the dominant frequency.
    it should returnt the intensities as well as the actual data'''
    print('tremor identified')
    return values, intensities

def calculate_tremor_length_intensity(tremor_intensities):
    length= len(tremor_intensities)*window_size*sampling_rate #length of time of tremor
    total_intensity=0
    for i in tremor_intensities:
        total_intensity += i
    average_intensity= total_intensity/length
    return length, average_intensity

def calculate_values_and_append():
    length, average_intensity = calculate_tremor_length_intensity(tremor_intensities)
    signal_np = np.array(signal_buffer)  # Convert signal buffer to a numpy array
    dominant_frequency = analyze_frequency(signal_np)

    dominant_frequency_array.append(dominant_frequency)
    length_array.append(length)
    average_intensity_array.append(average_intensity)

# Main loop for signal acquisition and analysis
#generating sample data
data1=generate_sine_wave(frequency, amplitude, duration, sampling_rate)
data2= generate_sine_wave(frequency, amplitude*2, duration/2, sampling_rate)
input_data =  array.array("h", [0] * num_samples)
if len(data2)<num_samples:
    data2zeros = np.zeros(num_samples)
    for i in range(len(data2)):
        data2zeros[i]= data2[i]
    input_data= data1+data2zeros
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
# Allocate buffer for signal samples
signal_buffer = array.array("h", [0] * num_samples)

# Acquire signal samples
#signal_buffer = input_data
dominant_frequency_array= ()
length_array=()
average_intensity_array=()
tremor_data= ()
tremor_intensities= ()
tremor_present=False

i=0
while i <= len(input_data):
    signal_buffer.append(input_data[i])
    if len(signal_buffer) >= 50:
        intensity = calculate_intensity(signal_buffer)
        if intensity >= intensity_threshold:
            tremor_present = True
            tremor_data.append(signal_buffer)
            tremor_intensities.append(intensity)
        if tremor_present:
            if intensity <= intensity_threshold:
                tremor_present = False
                calculate_values_and_append()

        signal_buffer = ()

    i=i+1


# Print the analysis outputs
print("Dominant Frequency: {:.2f} Hz".format(dominant_frequency_array))
print("length: {:.2f} seconds".format(length_array))
print("average intensity: {:.2f} units".format(average_intensity_array))

