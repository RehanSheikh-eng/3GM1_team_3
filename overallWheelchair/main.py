from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import time


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

speed_buffer = [0,0]
distance_speedEstimator = 0
distance_travelled = 0


# ----- STAGE 2 - READ VARIABLES IN -----

# read input from joystick to buffer
# read input from accelerometer to accel buffer
# read input from motors
# read input from gps
# read pressure plate input
# read distance sensor

# Read distance sensor
distance_buffer.pop(0)
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3

# ----- STAGE 3 - WARNING SYSTEMS ------
# 
# crash prevention function
# crash detection
# sudden joystick pullback stop

functions.startCrashPrevention()
functions.startCrashPrevention()


# ---- STAGE 4 - FILTERING AND TREMOR TRACKING ----



xfilter = functions.ButterworthFilter(9, 3, 0.01)
yfilter = functions.ButterworthFilter(9, 3, 0.01)

run = Pin('GP16', Pin.IN)

def update_motors(tim):
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




# ---- STAGE 5 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------


# ----- STAGE 6 - SEND SIGNALS TO MOTOR -----

# ----- STAGE 7 - USAGE TRACKING ------

# estimate speed
# estimate distance travelled
# count sitting duration
# GPS

speed = functions.speedEstimator(speed_buffer[0], leftMotorSignal, rightMotorSignal, leftMotorSignal_prev, rightMotorSignal_prev, sensor_data["accel"][1])
distance_travelled += getDistance(speed_buffer, sensor_data, previous_data, gps)


# ----- STAGE 8 - L2S2 (Per minute) ------


# ----


