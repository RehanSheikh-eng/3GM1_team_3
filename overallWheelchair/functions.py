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


def startCrashDetection():
    pass

def joyStickPullBack():
    pass


# filtering and tremor tracking

def findFilteredJoystickPosition():
    pass

def startTremorAnalysis():
    pass


# control

def speedEstimator():
    pass

def positionToSpeed():
    pass

def positionToAngularVelocity():
    pass

def findMotorSignalsFromSpeeds():
    pass



def updateMotorSpeeds():
    pass


# usage tracking

def getDistance():
    pass

def startSittingDuration():
    pass


def getGPSdata():
    pass

# L2S2

# 
