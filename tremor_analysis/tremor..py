''' How the trmeor analysis would be implemetned in the actual wheelchair control system
Ana'''
import numpy as np

# functions and classes
# filters
class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.filtered_value = 0.0

    def update(self, new_value):
        self.filtered_value = (self.alpha * new_value) + ((1 - self.alpha) * self.filtered_value)
        return self.filtered_value

class ButterworthFilter:
    def __init__(self, order, cutoff_freq, sampling_period):
        self.order = order
        self.cutoff_freq = cutoff_freq
        self.sampling_period = sampling_period
        self.coefficients = [0.0] * (order + 1)
        self.inputs = [0.0] * (order + 1)
        self.outputs = [0.0] * (order + 1)

        self.calculate_coefficients()

    def calculate_coefficients(self):
        # Calculate filter coefficients
        a = [0.0] * (self.order + 1)
        b = [0.0] * (self.order + 1)
        theta_c = 2.0 * math.pi * self.cutoff_freq
        k = math.tan(theta_c * self.sampling_period / 2.0)
        k2 = k * k

        a[0] = 1.0
        a[1] = self.order * k2 + 2.0 * k + 1.0
        for i in range(2, self.order + 1):
            a[i] = k2 * a[i - 2] + 2.0 * k * a[i - 1] + a[i - 2]

        b[0] = k2 * self.order
        b[1] = 2.0 * k2 * self.order
        for i in range(2, self.order + 1):
            b[i] = k2 * b[i - 2] + 2.0 * k * b[i - 1] + b[i - 2]

        self.coefficients = [bi / ai for bi, ai in zip(b, a)]

    def update(self, input_value):
        # Apply the filter
        self.inputs.pop(0)
        self.inputs.append(input_value)

        output = 0.0
        for i in range(self.order + 1):
            output += self.coefficients[i] * self.inputs[self.order - i]

        self.outputs.pop(0)
        self.outputs.append(output)

        return output

def extract_tremor_data(data):
    LPfiltered_data = []
    BWfiltered_data = []
    extracted_tremor_data = []
    for i in range(len(data)-1):
       LPfiltered_value = LPfilter.update(data[i])
       LPfiltered_data.append(LPfiltered_value)

       BWfiltered_value = BWfilter.update(LPfiltered_data[i])
       BWfiltered_data.append(BWfiltered_value)
       extracted_tremor_value = BWfiltered_data[i] - LPfiltered_data[i]
       extracted_tremor_data.append(extracted_tremor_value)
return extracted_tremor_data


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



# Main loop for signal acquisition and analysis

# arrays for analysis
signal_buffer = []
dominant_frequency_array = []
length_array = []
average_intensity_array = []
tremor_data = []
tremor_intensities = []
intensity_of_whole_signal = []

# Sampling parameters
sampling_freq = 100  # Sampling frequency in Hz
num_samples = 1000    # Number of samples to acquire

# tremor analysis variables
window_size = 25 # for calculating intensities- it's the sample number
tremor_window = (3, 17)  # bounds of data we are using for analysis in Hz
intensity_threshold = 0.025

# initial conditions
tremor_present = False  # initial cond for the loops to work
i = 0
tremor_count = 0
BWfilter = ButterworthFilter(9, 3.0, 0.01)
LPfilter = LowPassFilter(0.6) #lower alpha filters more noise


data = listXPOS  # Replace with your actual data
extracted_tremor_data= extract_tremor_data(data)

def tremor_analysis(input_data):
    while i <= (len(input_data)-1):
        signal_buffer.extend([input_data[i]])
        if len(signal_buffer) >= window_size:
            intensity = calculate_intensity(signal_buffer)
            intensity_of_whole_signal.extend([intensity])
            if intensity >= intensity_threshold and tremor_present == False:

            if intensity >= intensity_threshold:
                tremor_present = True
                tremor_data.extend(signal_buffer)
                tremor_intensities.extend([intensity])
            if tremor_present:
                if intensity <= intensity_threshold:
                    tremor_present = False
                    calculate_values_and_append(tremor_intensities, tremor_data)
                    tremor_data = []
                    tremor_intensities = []

            signal_buffer = []

        i = i+1

#end of running program
if tremor_present:
    tremor_present = False
    calculate_values_and_append(tremor_intensities, tremor_data)
    tremor_data = []




# SEND the analysis outputs
print("Dominant Frequency:", dominant_frequency_array)
print("Length:", length_array)
print("Average Intensity:", average_intensity_array)

