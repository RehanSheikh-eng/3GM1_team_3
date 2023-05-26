# Import time and thread libs
import utime as time
import _thread

# Import sensor modules
from modules.GPSModule import GPSModule
from modules.AccelerometerModule import Accel
from modules.DistanceSensorModule import DistanceSensor
from modules.SittingSwitchModule import SittingSwitch
from picozero import Speaker

# Import scripts
from scripts.crash_detection import start_crash_detection
from scripts.crash_prevention import start_crash_prevention
from scripts.distance_integration import start_distance_intergration
from scripts.sitting_duration import start_sitting_duration

# Debug mode
DEBUG = True 

# Define GLOBAL CONSTANTS
TIME_STEP = 1

# Define PINS/CONSTS
ACCEL_SDA_PIN = 8
ACCEL_SCL_PIN = 9

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


# Initialise the Pico
distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )

accel = Accel(sda_pin=ACCEL_SDA_PIN,
            scl_pin=ACCEL_SCL_PIN
            )

gps = GPSModule(uart_id=GPS_UART_ID,
                baud_rate=GPS_UART_BAUD_RATE,
                tx_pin_id=GPS_TX_PIN,
                rx_pin_id=GPS_RX_PIN
                )

sitting_switch = SittingSwitch(pin=SWITCH_PIN)

speaker = Speaker(SPEAKER_PIN, duty_factor = 5000) # duty_factor controls volume


# Start threads
_thread.start_new_thread(start_crash_detection,
                        (accel,
                        TIME_STEP,
                        DEBUG
                        ))

_thread.start_new_thread(start_crash_prevention,
                        (distance_sensor,
                        DIST_MA_ORDER,
                        TIME_STEP,
                        DEBUG
                        ))

_thread.start_new_thread(start_distance_intergration,
                        (accel,
                        gps,
                        TIME_STEP,
                        DEBUG
                        ))


_thread.start_new_thread(start_sitting_duration,
                        (sitting_switch,
                        TIME_STEP,
                        DEBUG
                        ))