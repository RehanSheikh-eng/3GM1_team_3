# --- STAGE 1 - IMPORTS + INITIALISATIONS (OUTSIDE MAIN LOOP) ---

# Import libraries
from machine import Timer, Pin
from collections import deque
import math
import utime as time
from picozero import Speaker

# Import functions and classes
import functions
from motor_controller import Motor
from joystick import Joystick
from Sensor_Data_Collection.modules.GPSModule import GPSModule
from Sensor_Data_Collection.modules.AccelerometerModule import Accel
from Sensor_Data_Collection.modules.L2S2Module import L2S2Module
from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor
from Sensor_Data_Collection.modules.SittingSwitchModule import SittingSwitch

# Set pins
JOYSTICK_V_X_PIN = 28
JOYSTICK_V_Y_PIN = 26

ACCEL_SDA_PIN = 0
ACCEL_SCL_PIN = 1
ACCEL_I2C_ID = 0

DIST_ID = 0
DIST_SDA_PIN = 4
DIST_SCL_PIN = 5

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5

SPEAKER_PIN = 17

SWITCH_PIN = None

# Initialise variables
current_total_crashes = 0 
current_true_crashes = 0

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

# Initialise classes
distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )
pressure_plate = SittingSwitch(SWITCH_PIN)
accel = Accel(i2c_id=ACCEL_I2C_ID,
            sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )

gps = GPSModule(uart_id=GPS_UART_ID,
                baud_rate=GPS_UART_BAUD_RATE,
                tx_pin_id=GPS_TX_PIN,
                rx_pin_id=GPS_RX_PIN
                )

joystick = Joystick(X_pin=JOYSTICK_V_X_PIN,
                    Y_pin=JOYSTICK_V_Y_PIN
                    )
speaker = Speaker(SPEAKER_PIN, initial_freq=750, duty_factor = 5000)

l2s2 = L2S2Module()
l2s2.boot_L2S2()

# Initialise timers
fast_timer = Timer(-1) # 100Hz
slow_timer = Timer(-1) # 1Hz
L2S2_timer = Timer(-1) # Once per minute

# Initialise Data storage
sensor_data = {"accel": None, "gps": None, "distance": None, "joystick": None}
previous_data = {"accel": None, "gps": None}


# --- STAGE 2 - READ VARIABLES ---

# Read input from joystick to buffer
sensor_data["joystick"] = joystick.get_values()

# read input from accelerometer to accel buffer
# read input from motors
# read input from gps
# read pressure plate input

# Read distance sensor and compute moving average
distance_buffer.pop(0)
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3


# ---- STAGE 3 - FILTERING AND TREMOR TRACKING ----



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




# ---- STAGE 4 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------


# ----- STAGE 5 - SEND SIGNALS TO MOTOR -----


# ----- STAGE 6 - WARNING SYSTEMS ------

# estimate speed
# crash prevention function
# crash detection
# sudden joystick pullback stop

speed_buffer[1] = functions.speedEstimator(speed_buffer[0], leftMotorSignal, rightMotorSignal, leftMotorSignal_prev, rightMotorSignal_prev, sensor_data["accel"][1])
functions.startCrashPrevention(distance, speed_buffer[1], speaker)
functions.startCrashPrevention()


# ----- STAGE 7 - USAGE TRACKING ------

# estimate distance travelled
# count sitting duration
# GPS

distance_travelled += functions.getDistance(speed_buffer, sensor_data, previous_data, gps)


# ----- STAGE 8 - L2S2 (Per minute) ------


# ----


