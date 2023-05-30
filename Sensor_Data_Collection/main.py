'''
PROCESS 1 PSEUDOCODE
'''
from machine import Pin, Timer
import math
from Sensor_Data_Collection.modules.GPSModule import GPSModule
from Sensor_Data_Collection.modules.AccelerometerModule import Accel
from Sensor_Data_Collection.modules.L2S2Module import L2S2Module
from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor
from Sensor_Data_Collection.modules.SittingSwitchModule import SittingSwitch

# Debug mode
DEBUG = True 

# Define PINS/CONSTS
ACCEL_SDA_PIN = 0
ACCEL_SCL_PIN = 1
ACCEL_I2C_ID = 0

DIST_ID = 0
DIST_SDA_PIN = 0
DIST_SCL_PIN = 1
DIST_MA_ORDER = 3

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5

SPEAKER_PIN = 15

SWITCH_PIN = None

# Intit Timers scales (ms)
time_crash_detection = 10




# Initialise the Pico
#distance_sensor = DistanceSensor(id = DIST_ID, 
#                                sda = DIST_SDA_PIN,
#                                scl = DIST_SCL_PIN
#                                )
accel = Accel(i2c_id=ACCEL_I2C_ID,
            sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )
gps = GPSModule(uart_id=GPS_UART_ID,
                baud_rate=GPS_UART_BAUD_RATE,
                tx_pin_id=GPS_TX_PIN,
                rx_pin_id=GPS_RX_PIN
                )
l2s2 = L2S2Module()
l2s2.boot_L2S2()
#sitting_switch = SittingSwitch(pin=SWITCH_PIN)
#speaker = Speaker(SPEAKER_PIN, duty_factor = 5000) # duty_factor controls volume

# Initialise Sensor timers
#joystick_timer = Timer(-1)
accelerometer_timer = Timer(-1)
#motor_timer = Timer(-1)
gps_timer = Timer(-1)
#distance_sensor_timer = Timer(-1)
L2S2_timer = Timer(-1)


# Initialise Script timers
crash_detection_timer = Timer(-1)



# Initialise Data storage
sensor_data = {"accel": None, "gps": None, "distance": None}
previous_data = {"accel": None, "gps": None}



current_true_crashes = 0

# Data collection ISRs
def accel_isr(timer):
    sensor_data["accel"] = accel.get_corrected_values()

def gps_isr(timer):
    gps_data = gps.get_data()
    print(gps_data)
    if gps_data is not None:
        sensor_data["gps"] = gps_data

def distance_isr(timer):
    sensor_data["distance"] = distance_sensor.get_smooth_distance()

# Data Processing ISR
def crash_detection_isr(timer):
    accel_data = sensor_data["accel"]
    distance = sensor_data["distance"]
    global current_true_crashes
    if accel_data is not None and distance is not None:
        acc_mag = math.sqrt(accel_data.AccX**2 + accel_data.AccY**2)
        jerk = None
        if previous_data["accel"] is not None:
            prev_acc_mag = math.sqrt(previous_data["accel"].AccX**2 + previous_data["accel"].AccY**2 )
            jerk = (acc_mag - prev_acc_mag) / (time_crash_detection/1000) # Assuming this ISR runs every 1s
        # Update previous data
        previous_data["accel"] = accel_data

        if jerk > 50 and acc_mag > 6:  # Add gyro condition if needed
            current_true_crashes += 1
            if DEBUG:
                print("Crash Detected")
                

# L2S2 Data Sending ISR
def L2S2_isr(timer):
    # Assuming that the data to be sent is stored in sensor_data
    if sensor_data["gps"] is not None:
        print("Sending Data")
        l2s2.send_data(record_id="110", 
                    plate_template_id="6e0485b5-cd17-4438-aff8-afe0578ed71f", 
                    control_id="4", 
                    _type=5, 
                    content=sensor_data["gps"]["longitude"], # or any relevant content
                    units="degrees"
                    )

# Data Timers
accelerometer_timer.init(period=10, mode=Timer.PERIODIC, callback=accel_isr)
gps_timer.init(period=1000, mode=Timer.PERIODIC, callback=gps_isr)
#distance_sensor_timer.init(period=-10, mode=Timer.PERIODIC, callback=distance_isr)
#motor_timer.init(period=60000, mode=Timer.PERIODIC, callback=)
#joystick_timer.init(period=60000, mode=Timer.PERIODIC, callback=)



# Script Timers
crash_detection_timer.init(period=time_crash_detection, mode=Timer.PERIODIC, callback=crash_detection_isr)
L2S2_timer.init(period=5000, mode=Timer.PERIODIC, callback=L2S2_isr)



































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


# ---- STAGE 5 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------


# ----- STAGE 6 - SEND SIGNALS TO MOTOR -----

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

