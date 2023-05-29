'''

PROCESS 1 PSEUDOCODE
'''

# tim code
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

Bfilter = ButterworthFilter(9, 3, 0.01)



speedAmpltitude = 1
angSpeedAmpltitude = 1
xPosBuffer = [0] * 500
xPosBuffer = deque(xPosBuffer,maxlen=500)
yPosBuffer = [0] * 500
yPosBuffer = deque(yPosBuffer,maxlen=500)
testx = []
testy = []
stops = []
filtered_signal = [] 
startTime = round(utime.time())
Bfilter = ButterworthFilter(9, 3, 0.01)
samplingFrequency = 100 
resetTime = 0
stopDuration = None
stopSignal = 0
speedAmplitudeLog = []
angSpeedAmplitudeLog = []
stop = Pin('GP16', Pin.IN)

def update_motors(tim):
    x, y = test_joystick.get_values()
    x = Bfilter.update(x)
    y = Bfilter.update(y)
    L = 0.9*min(max(x+y,-1),1)
    R = 0.9* min(max(x-y,-1),1)
    L_motor.set_speed(L)
    R_motor.set_speed(R)
    if stop.value():
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


# ---- STAGE 1. IMPORT SCRIPTS and initialise classes------
# initalise l2s2

# ----- STAGE 2 - READ VARIABLES IN -----

# read input from joystick to buffer
# read input from accelerometer to accel buffer 
# read input from motors
# read input from gps
# read pressure plate input
# read distance sensor
# 

# ----- STAGE 3 - WARNING SYSTEMS ------
# 
# crash prevention function
# crash detection
# sudden joystick pullback stop

# ---- STAGE 4 - FILTERING AND TREMOR TRACKING ----
# update joystick pos from filter
# record tremor data 

# ---- STAGE 5 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------
# find speeds from pos
# find motor signals from speeds


# ----- STAGE 6 - SEND SIGNALS TO MOTOR -----
#updateMotorSignals()

# ----- STAGE 7 - USAGE TRACKING ------
# estimate speed
# estimate distance travelled
# count sitting duration
# GPS


# ----- STAGE 8 - L2S2 (Per minute) ------


# ----



# variables for use in speed Estimator
A = 1
w = 0.1
b = 0.2
tau = 0.6
var_accel = 1
var_motor = 1

def speedEstimator(prevSpeed,leftMotorSignal,rightMotorSignal
                   , leftMotorSignal_prev, rightMotorSignal_prev, acc_y,var_accel,var_motor, time_step = 0.001):
    # estimate curr speed assuming joystick proportional to speed accounting for lag
    # improve confidence by using acceleration to adjust

    leftMotorSignal_approx = (leftMotorSignal - leftMotorSignal_prev)*(1 - math.exp(-time_step) / tau) + leftMotorSignal_prev # exp will be a constant 
    rightMotorSignal_approx = (rightMotorSignal - rightMotorSignal_prev)*(1 - math.exp(-time_step) / tau) + rightMotorSignal_prev
    speed_motor = (leftMotorSignal_approx + rightMotorSignal_approx) / 2 # assuming centre of mass equidistant between wheels


    if (abs(leftMotorSignal - leftMotorSignal_prev) + abs(rightMotorSignal - rightMotorSignal_prev)) < 0.05:
        speed = speed_motor
    else:
        speed_accel =  acc_y * time_step + prevSpeed
        speed = (speed_motor*var_accel + speed_accel*var_motor)  / (var_accel + var_motor) # Kalman filtered velocity
    return speed