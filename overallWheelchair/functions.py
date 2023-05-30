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
