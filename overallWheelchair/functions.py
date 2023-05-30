"""

All functions that are used in main.py are stored here

"""



# import libraries
from collections import deque
from picozero import Speaker
import utime as time

# warning functions
def startCrashPrevention(distance, speed, speed_threshold = 1, beep_width = 100):
    global current_total_crashes
    global speedAmplitude
    global angSpeedAmplitude
    global stopSignal
    global stopDuration

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
        stopDuration = 5
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


def startCrashDetection():
    pass

def joyStickPullBack(ypos,freq):
    """
    When given in a list of previous y positions at least for 2 seconds then detect if sudden pull back 

    :param @ypos: list of previous speed positions on joystick
    :out binary signal (-1,0) and stopping 
    if sharp pull back detected then a -1 is sent
    or button pressed
    """
    deltaT = 1 / freq
    cutoff = 0.5
    # detect if curr pos is less than -0.5
    # also rate of change must be big 
    # in last second must value must be greater than 0.5
    ypos = list(ypos)
    currPosTest  = (np.average(ypos[-10:-1]) < -0.5 )
    rate = (ypos[-1] - ypos[-(freq+1)])/(deltaT * freq )
    #print("rate={}".format(rate))
    rateHigh = (rate < cutoff)
    lastSecond = ypos[-(int(freq/2)):-1]
    highestValue = max(lastSecond)
    #print("highest value = {}".format(highestValue))
    lastSecondPositive = highestValue > 0.3
    #print(currPosTest,rateHigh,lastSecondPositive)
    if currPosTest and rateHigh and lastSecondPositive:
        return -1,2
    else:
        return 0,0


# filtering and tremor tracking

def findFilteredJoystickPosition():
    pass

def startTremorAnalysis():
    pass


# control

def speedEstimator(prevSpeed,leftMotorSignal,rightMotorSignal
                   , leftMotorSignal_prev, rightMotorSignal_prev, acc_y,var_accel,var_motor, time_step = 0.001):
    # estimate curr speed assuming joystick proportional to speed accounting for lag
    # improve confidence by using acceleration to adjust

    leftMotorSignal_approx = (leftMotorSignal - leftMotorSignal_prev)*(1 - math.exp(-time_step / tau)) + leftMotorSignal_prev # REPLACE EXP TERM WITH CONSTANT
    rightMotorSignal_approx = (rightMotorSignal - rightMotorSignal_prev)*(1 - math.exp(-time_step / tau)) + rightMotorSignal_prev
    speed_motor = (leftMotorSignal_approx + rightMotorSignal_approx) / 2 # assuming centre of mass equidistant between wheels


    if (abs(leftMotorSignal - leftMotorSignal_prev) + abs(rightMotorSignal - rightMotorSignal_prev)) < 0.05:
        speed = speed_motor
    else:
        speed_accel =  acc_y * time_step + prevSpeed
        speed = (speed_motor*var_accel + speed_accel*var_motor)  / (var_accel + var_motor) # Kalman filtered velocity
    return speed

def positionToSpeed():
    pass

def positionToAngularVelocity():
    pass

def findMotorSignalsFromSpeeds():
    pass



def updateMotorSpeeds():
    pass


# usage tracking

def getDistance(speed_buffer, sensor_data, previous_data, gps, var_speedEstimator = 1, var_GPS = 1, time_step = 0.01): # TUNE VARIANCES

    global distance_speedEstimator

    distance_speedEstimator += 0.5 * time_step * (speed_buffer[0] + speed_buffer[1]) # Integrate speed from speedEstimator()

    if previous_data["gps"] != sensor_data["gps"]:
        distance_GPS = gps.get_relative_position(previous_data["gps"], sensor_data["gps"])
        distance_kalman += (var_GPS * distance_speedEstimator + var_speedEstimator * distance_GPS) / (var_GPS + var_speedEstimator)

        distance_speedEstimator = 0

        return distance_kalman

    else:
        return 0

def start_sitting_duration(pressure_plate):
    global start_time_sitting
    global prev_record_time
    global sitting_duration
    global latch

    if pressure_plate.switch.is_active and latch == 0:
        start_time_sitting = time.time()
        prev_record_time = start_time_sitting
        latch = 1
    elif pressure_plate.switch.is_active and latch == 1:
        sitting_duration += time.time() - prev_record_time
        prev_record_time = time.time()
    elif pressure_plate.switch.is_inactive and latch == 1:
        latch = 0


def getGPSdata():
    pass

# L2S2

# 
