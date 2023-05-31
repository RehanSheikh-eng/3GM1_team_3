# --- CRASH PREVENTION ---

from collections import deque
from test.DistanceSensorModule import DistanceSensor
from picozero import Speaker
from picozero import Buzzer
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
# speaker = Buzzer(SPEAKER_PIN)

# Get 3-order moving average of  distance
distance_buffer = [501,501,501]

parking = False
cur_time = 0

def startCrashPrevention(distance, speed, speed_threshold = 1, beep_width = 100):
    global current_total_crashes
    global speedAmplitude
    global angSpeedAmplitude
    global stopSignal

    global parking
    global cur_time
    recent_crash = False
    speaker_counter = 0

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
        
        #elif 100 < tdiff < 100 + gap_width:
        #    speaker.off()
        # elif 100 + gap_width < tdiff < 200 + gap_width:
        #    speaker.on()
        
        # speaker.beep(on_time=0.1, off_time=gap_width, n=1, wait=True)

        stopSignal = 0
        speedAmplitude = distance/500
        angSpeedAmplitude = distance/500
        recent_crash = False
        print("Current time: ", cur_time)
        print("Gap width: ", gap_width)
        
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
    
    time.sleep(0.01)


while True:
    distance_buffer.pop(0)
    distance_buffer.append(distance_sensor.get_distance())
    distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3
    print(distance)
    print(parking)
    startCrashPrevention(distance, 0.9)