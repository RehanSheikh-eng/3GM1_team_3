from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import time

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



# speedAmpltitude = 1
# angSpeedAmpltitude = 1
# xPosBuffer = [0] * 500
# xPosBuffer = deque(xPosBuffer,maxlen=500)
# yPosBuffer = [0] * 500
# yPosBuffer = deque(yPosBuffer,maxlen=500)
# testx = []
# testy = []
# stops = []
# filtered_signal = [] 
# startTime = round(utime.time())
xfilter = ButterworthFilter(12, 2, 0.01)
yfilter = ButterworthFilter(12, 2, 0.01)
run = Pin('GP26', Pin.IN)

def update_motors(tim):
    safety = 0.8
    x, y = test_joystick.get_values()
    x = xfilter.update(x)
    y = yfilter.update(y)
    L = safety*0.9*min(max(x+y,-1),1)
    R = safety*0.9*min(max(x-y,-1),1)
    L_motor.set_speed(L)
    R_motor.set_speed(R)
    if not run.value():
        L_motor.disable()
        R_motor.disable()
        tim.deinit()


test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP0', 'GP1', 'GP8')
R_motor = Motor('GP2', 'GP3', 'GP9')

L_motor.enable()
R_motor.enable()

tim = Timer()

tim.init(mode=Timer.PERIODIC, freq=100, callback=update_motors)