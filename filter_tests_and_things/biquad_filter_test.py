''' this filter was tested but does no work well enough for our purposes
written by Ana'''

# defs and classes
class BiquadFilter:
    def __init__(self, coeff):
        """General IIR digital filter using cascaded biquad sections.  The specific
        filter type is configured using a coefficient matrix.  These matrices can be
        generated for low-pass, high-pass, and band-pass configurations.
        """
        self.coeff = coeff  # coefficient matricies
        self.sections = len(self.coeff)  # number of biquad sections in chain
        self.state = [[0, 0] for i in range(self.sections)]  # biquad state vectors

    def update(self, input):
        # Iterate over the biquads in sequence.  The accum variable transfers
        # the input into the chain, the output of each section into the input of
        # the next, and final output value.
        accum = input
        for s in range(self.sections):
            A = self.coeff[s][0]
            B = self.coeff[s][1]
            Z = self.state[s]
            x = accum - A[1] * Z[0] - A[2] * Z[1]
            accum = B[0] * x + B[1] * Z[0] + B[2] * Z[1]
            Z[1] = Z[0]
            Z[0] = x

        return accum

#filter coefficients
bandpass_coeff= [[ 0.01482675, 0.02965349,0.01482675,1.0,-0.83741793,0.25181397],
 [ 1.0,2.,1.,1.,-0.80710729, 0.60719683],
 [ 1., -2.,     1.,        1.,       -1.61666504,  0.66842549],
 [ 1.  ,       -2.,   1.,       1.,      -1.86140932,  0.89685145]]

lowpass_coeff = [[6.23869835e-05,  1.24773967e-04,  6.23869835e-05,  1.00000000e+00, -1.67466095e+00,  7.04858682e-01],
 [1.00000000e+00,  2.00000000e+00,  1.00000000e+00,  1.00000000e+00, -1.83312526e+00,  8.66180446e-01]]

#creating the filters
bandpass_filter = BiquadFilter(bandpass_coeff)
Lowpass_filter = BiquadFilter(lowpass_coeff)


filtered_value = Lowpass_filter.update(value) # desired motion
filtered_signal.append(filtered_value)

Tremor_value = bandpass_filter.update(value) # tremor
tremor_signal.append(tremor_value)
