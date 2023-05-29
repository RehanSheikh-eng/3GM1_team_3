# --- CRASH PREVENTION ---

# INITIALISATIONS
from collections import deque
from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor
from picozero import Speaker
import utime as time

DIST_ID = 0
DIST_SDA_PIN = 4
DIST_SCL_PIN = 5
SPEAKER_PIN = 17

current_total_crashes = 0

distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )
speaker = Speaker(SPEAKER_PIN, initial_freq=750, duty_factor = 5000)

distance_buffer = [501,501,501]

parking = False
cur_time = 0

# FUNCTION

def startCrashPrevention(distance, speed, speed_threshold = 1, beep_width = 100):
    global current_total_crashes
    global speedAmplitude
    global angSpeedAmplitude
    global stopSignal

    global parking
    global cur_time
    recent_crash = False

    if distance < 500 and speed <= speed_threshold:
        gap_width = round(distance, -2)
        if not parking:
            cur_time = time.ticks_ms()
        parking = True
        tdiff = round(time.ticks_ms() - cur_time, -2)
        if tdiff % (beep_width + gap_width) < beep_width and parking:
            speaker.on()
        elif tdiff % (beep_width + gap_width) >= beep_width and parking:
            speaker.off()

        stopSignal = 0
        speedAmplitude = distance/500
        angSpeedAmplitude = distance/500
        recent_crash = False

    elif distance < 500 and speed > speed_threshold:
        stopSignal = -1
        if not recent_crash:
            current_total_crashes += 1
        parking = False
        recent_crash = True
        speaker.off()

    else:
        stopSignal = 0
        speedAmplitude = 1
        angSpeedAmplitude = 1
        parking = False
        recent_crash = False
        speaker.off()

# IN MAIN LOOP
distance_buffer.pop(0)
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3
startCrashPrevention(distance, speed)