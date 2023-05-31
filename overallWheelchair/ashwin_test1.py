'''

PROCESS 1 PSEUDOCODE
'''

# tim code
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin

import math
import utime

# filter code

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

Bfilter = ButterworthFilter(9, 3, 0.01)




filtered_signal = [] 
startTime = round(utime.time())
xfilter = ButterworthFilter(9, 3, 0.01)
yfilter = ButterworthFilter(9, 3, 0.01)
samplingFrequency = 100 
resetTime = 0
stopDuration = None
stopSignal = 0
speedAmplitudeLog = []
angSpeedAmplitudeLog = []
run = Pin('GP16', Pin.IN)

def update_motors(tim):
    print('update')
    x, y = test_joystick.get_values()
    x = xfilter.update(x)
    y = yfilter.update(y)
    L = 0.9*min(max(x+y,-1),1)
    R = 0.9* min(max(x-y,-1),1)
    L_motor.set_speed(L)
    R_motor.set_speed(R)
    if not run.value():
        L_motor.disable()
        R_motor.disable()
        tim.deinit()


test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP0', 'GP1', 'GP14')
R_motor = Motor('GP2', 'GP3', 'GP15')

L_motor.enable()
R_motor.enable()

tim = Timer()

tim.init(mode=Timer.PERIODIC, freq=100, callback=update_motors)


