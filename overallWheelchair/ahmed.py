# --- CRASH PREVENTION ---

from collections import deque
from Sensor_Data_Collection.modules.DistanceSensorModule import DistanceSensor
from picozero import Speaker

current_total_crashes = 0

distance_sensor = DistanceSensor(id = DIST_ID, 
                                sda = DIST_SDA_PIN,
                                scl = DIST_SCL_PIN
                                )
speaker = Speaker(SPEAKER_PIN, initial_freq=750, duty_factor = 5000)

# Get 3-order moving average of  distance
distance_sensor = DistanceSensor()
distance_buffer = deque([0,0,0])
distance_buffer.popleft
distance_buffer.append(distance_sensor.get_distance())
distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3

def startCrashPrevention(distance, speed, speed_threshold = 1):
    global current_total_crashes
    global speedAmplitude
    global angSpeedAmplitude
    global stopSignal

    recent_crash = False

    if distance < 500 and speed <= speed_threshold:
        gap_width = 0.002*distance
        speaker.beep(on_time=0.1, off_time=gap_width, n=1, wait=True)

        stopSignal = 0
        speedAmplitude = distance/500
        angSpeedAmplitude = distance/500
        recent_crash = False
    elif distance < 500 and speed > speed_threshold:
        stopSignal = -1
        if not recent_crash:
            current_total_crashes += 1
        recent_crash = True
    else:
        stopSignal = 0
        speedAmplitude = 1
        angSpeedAmplitude = 1
        recent_crash = False
