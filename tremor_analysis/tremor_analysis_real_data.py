
import numpy as np
import matplotlib.pyplot as plt





# Sampling parameters
sampling_freq = 100  # Sampling frequency in Hz
num_samples = 1000    # Number of samples to acquire

# analysis variables
window_size = 25 # for calculating intensities- it's the sample number
tremor_window = (3, 17)  # bounds of data we are using for analysis in Hz
intensity_threshold = 0.4


# functions
def generate_sine_wave(frequency1, amplitude1, duration1, sampling_rate1):
    t = np.linspace(0, duration1, int(duration1 * sampling_rate1), endpoint=False)
    signal = amplitude1 * np.sin(2 * np.pi * frequency1 * t)
    return signal


def tremor_window_fft(fft_result, fft_freq, tremor_window1):  # t window is lower than the upper bound in hz
    new_fft_result = []
    new_fft_freq = []
    for i in range(len(fft_freq)):
        if (abs(fft_freq[i]) >= tremor_window1[0]) and (abs(fft_freq[i]) <= tremor_window1[1]):
            new_fft_result.append(fft_result[i])
            new_fft_freq.append(fft_freq[i])
    return new_fft_result, new_fft_freq
# Function to perform FFT and find the dominant frequency


def analyze_frequency(signal):

    # Perform FFT on the signal
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(len(signal), (1 / sampling_freq))
    tremor_n = len(dominant_frequency_array) +1
    plt.plot(fft_freq, np.abs(fft_result))
    plt.title('frequency composition of tremor ' + str(tremor_n))
    plt.show()
    fft_result, fft_freq = tremor_window_fft(fft_result, fft_freq, tremor_window)


    # Find the index of the maximum magnitude in the FFT result
    if len(fft_result) > 0:
        max_index = np.argmax(np.abs(fft_result))
        # Extract the dominant frequency
        dominant_freq = abs(fft_freq[max_index])
    else:
        dominant_freq = 0
    return dominant_freq


def calculate_intensity(signal):
    ''' the input of this function is a small sample of the signal in the window size.
     The values have to be positive so i will square the input signal'''
    # Calculate the area under the curve using the trapezoidal rule
    signal_array = np.array(signal)
    signal_squared = signal_array*signal_array
    area = np.trapz(signal_squared)
    intensity1 = area / window_size
    return intensity1


def calculate_tremor_length_intensity(tremor_intensities1):
    length = len(tremor_intensities1)*window_size/sampling_freq # length of time of tremor
    total_intensity = 0
    for j in tremor_intensities:
        total_intensity += j
    if length != 0:
        average_intensity = total_intensity/len(tremor_intensities1)

    else:
        average_intensity = 0
    return length, average_intensity


def calculate_values_and_append(tremor_intensities1, tremor_data1):
    length, average_intensity = calculate_tremor_length_intensity(tremor_intensities1)
    dominant_frequency = analyze_frequency(tremor_data1)


    dominant_frequency_array.append(dominant_frequency)
    length_array.append(length)
    average_intensity_array.append(average_intensity)

def readjoystickTextFile(fileName):
    data = []
    xPos_vector = []
    yPos_vector = []
    iteration = []
    j = 0
    with open('./JoystickTextFiles/{}'.format(fileName), 'r') as file:
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

# Main loop for signal acquisition and analysis

listXPOS, listYPOS = readjoystickTextFile(fileName = 'tremor_simulator_100HZ.txt')
position= []
for i in range(len(listXPOS)-1):
    position.append( listXPOS[i] + listYPOS[i]*1j)
plt.plot(listXPOS)
plt.plot(listYPOS)
plt.plot(position)
plt.show()
input_data =listYPOS
t = np.arange(0, len(input_data)) * sampling_freq

# arrays for analysis
signal_buffer = []
dominant_frequency_array = []
length_array = []
average_intensity_array = []
tremor_data = []
tremor_intensities = []
intensity_of_whole_signal = []
# initial conditions
tremor_present = False  # initial cond for the loops to work
i = 0
tremor_count = 0
input_data= extracted_tremor_data

while i <= (len(input_data)-1):
    signal_buffer.extend([input_data[i]])
    if len(signal_buffer) >= window_size:
        intensity = calculate_intensity(signal_buffer)
        intensity_of_whole_signal.extend([intensity])
        if intensity >= intensity_threshold and tremor_present == False:
            print('tremor started at:', i / sampling_freq)

        if intensity >= intensity_threshold:
            tremor_present = True
            tremor_data.extend(signal_buffer)
            tremor_intensities.extend([intensity])
        if tremor_present:
            if intensity <= intensity_threshold:
                tremor_present = False
                print('tremor ended at:', i/sampling_freq)
                calculate_values_and_append(tremor_intensities, tremor_data)
                tremor_data = []
                tremor_intensities = []

        signal_buffer = []

    i = i+1
if tremor_present:
    tremor_present = False
    calculate_values_and_append(tremor_intensities, tremor_data)
    tremor_data = []


fig, axs = plt.subplots(2)
fig.suptitle('The Input Signal and Its Intensity')
axs[0].plot(t, input_data)
axs[0].set(ylabel='Amplitude', xlabel='time')
axs[1].plot(intensity_of_whole_signal, marker='o', markerfacecolor='red', markersize=6)
axs[1].set(ylabel='Intensity', xlabel='n of samples')

# Print the analysis outputs
print("Dominant Frequency:", dominant_frequency_array)
print("length:", length_array)
print("average intensity:", average_intensity_array)

plt.tight_layout()
plt.show()