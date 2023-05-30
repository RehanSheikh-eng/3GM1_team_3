'''

PROCESS 1 PSEUDOCODE
'''
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import time

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
xFilter = ButterworthFilter(9, 3, 0.01)
yFilter = ButterworthFilter(9, 3, 0.01)
samplingFrequency = 100 
resetTime = 0
stopDuration = None
stopSignal = 0
speedAmplitudeLog = []
angSpeedAmplitudeLog = []
stop = Pin('GP16', Pin.IN)

# tim code
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque

import time

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


# ---- STAGE 1. IMPORT SCRIPTS, INITIALISE CLASSES, INITIALISE VARIABLES (OUTSIDE MAIN LOOP) ------
# initalise l2s2
import functions

from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor
from Sensor_Data_Collection.modules.SittingSwitchModule import SittingSwitch

from picozero import Speaker

DIST_ID = 0
DIST_SDA_PIN = 4
DIST_SCL_PIN = 5
SPEAKER_PIN = 17

SWITCH_PIN = None

current_total_crashes = 0 
current_true_crashes = 0

distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )
pressure_plate = SittingSwitch(SWITCH_PIN)
speaker = Speaker(SPEAKER_PIN, initial_freq=750, duty_factor = 5000)

distance_buffer = [501,501,501]

parking = False
cur_time = 0

sitting_duration = 0
start_time_sitting = 0
prev_record_time = 0
latch = 0
stopSignal = 0
stopDuration = 0


# ----- STAGE 2 - READ VARIABLES IN -----

# read input from joystick to buffer
# read input from accelerometer to accel buffer 
# read input from motors
# read input from gps
# read pressure plate input
# read distance sensor
# estimate speed

# Read distance sensor
distance_buffer.pop(0)
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3

# ----- STAGE 3 - WARNING SYSTEMS ------
# 
# crash prevention function
# crash detection
# sudden joystick pullback stop

# ---- STAGE 4 - FILTERING AND TREMOR TRACKING ----


# ---- STAGE 5 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------


# ----- STAGE 6 - SEND SIGNALS TO MOTOR -----

# ----- STAGE 7 - USAGE TRACKING ------

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