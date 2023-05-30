"""
This script creates functions that will form part of the joystick control system

@ Ashwin Gunasekaran
created on 22/05/23
"""
# first import the necessary libraries
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import deque
import time as utime
import sys
from defandclasses import ButterworthFilter
try:
    import motor_controller
except ModuleNotFoundError:
    print("Machine module not found: expected when not running on micropython")

global leftMotor, rightMotor


# next define the necessary functions



#creating the filters


def positionToSpeed(x,posSpeedAmplitude = 2,posSpeedOffset = -0.2,posSpeedFreq = 0.2,\
                     negSpeedAmplitude = 2, negSpeedOffset = 0.2,negSpeedFreq = 0.2 ):
    """ this function maps the position on the joystick speed input to a desired speed using
        the non linear function v = A*tanh( wx+b )

        Parameters:
        :param x: position on joystick, Type Float, -1 < x < 1 
        :param posSpeedAmplitude: A for x > 0
        :param negSpeedAmplitude: A for x < 0
        :param posSpeedOffset: b for x > 0
        :param negSpeedOffset: b for x < 0
        :param posSpeedFreq: w for x > 0
        :param negSpeedFreq: w for x < 0


        
        :return v:  desired speed
        """ 
    signalGain = 1 # gain of input pos
    x = signalGain * x
    if x > 0:
        # work in positive speed part of graph 
        v = posSpeedAmplitude* math.tanh(((posSpeedFreq * x) + posSpeedOffset))
        return max(0,v)
    elif x < 0:
        # work in negative speed part of graph
        v = negSpeedAmplitude*math.tanh(((negSpeedFreq * x) + negSpeedOffset))
        return min(v,0)
    else:
        return 0

def positionToAngularVelocity(x,posAngVelAmplitude = 2,posAngVelOffset = -0.2,posAngVelFreq = 0.2,\
                     negAngVelAmplitude = 2, negAngVelOffset = 0.2,negAngVelFreq = 0.2 ):
    """ this function maps the position on the angular velocity joystick input to a desired angular Velocity using
        the non linear function omega = A*tanh( wx+b )

        Parameters:
        :param x: position on joystick, Type Float, -1 < x < 1 
        :param posAngVelAmplitude: A for x > 0
        :param negAngVelAmplitude: A for x < 0
        :param posAngVelOffset: b for x > 0
        :param negAngVelOffset: b for x < 0
        :param posAngVelFreq: w for x > 0
        :param negAngVelFreq: w for x < 0


        
        :return Omega: desired angular speed
        """ 
    signalGain = 1 # gain of input pos
    x = signalGain * x
    if x > 0:
        # work in positive speed part of graph 
        v = posAngVelAmplitude* math.tanh((posAngVelFreq * x +posAngVelOffset))
        return max(v,0)
    elif x < 0:
        # work in negative speed part of graph
        v = negAngVelAmplitude*math.tanh((negAngVelFreq * x +negAngVelOffset))
        return min(0,v)
    else:
        return 0


def findMotorSignalsFromSetSpeeds(v,omega,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1):
    """
    this function takes in the desired speed and and angular velocity signals and calculates the motor input signals

    Parameters
    :param v: desired speed ( forwards is positive)
    :param omega: desired angular velocity, positive when vector points upwards)
    :param l: length of axle ( left to right wheel)
    :param wheelRadius: radius of wheelchair tyre
    :param motorVoltageConstant: constant k where V = k * angular velocity of wheel

    :return motorLeft_set: desired Left motor voltage
    :return motorRight_set: desired Right motor voltage

    """
    signalGain = 1 # change this to keep the range as desired
    v, omega = v * signalGain, omega * signalGain
    leftWheelSpeed = v - omega*l/2
    rightWheelSpeed = v + omega*l/2
    leftWheelAngVel = leftWheelSpeed / wheelRadius
    rightWheelAngVel = rightWheelSpeed / wheelRadius
    leftMotorSignal = leftWheelAngVel * motorVoltageConstant
    rightMotorSignal = rightWheelAngVel * motorVoltageConstant
    return leftMotorSignal, rightMotorSignal

def stopIfPullBackDetected(ypos,freq,i):

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
    currPosTest  = (math.average(ypos[-10:-1]) < -0.5 )
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

def readJoystickValues(simulator = True,listXPOS = None,listYPOS = None,i = None):
    # write functionality to return xpos,ypos
    if simulator:
        return listXPOS[i],listYPOS[i]

    return -1,-1

def readjoystickTextFile(fileName):
    data = []
    xPos_vector = []
    yPos_vector = []
    iteration = []
    j = 0
    with open('tremor_analysis/JoystickTextFiles/{}'.format(fileName), 'r') as file:
        for line in file:
            j += 1
            nums = ((line.strip().split(','))) # Convert each line to a float and append to the data list
            values = []
            for i in range(3):
                values.append(float(nums[i]))
            xPos_vector.append(values[1])
            yPos_vector.append(values[2])
            iteration.append(j)
    return xPos_vector, yPos_vector

def calcJoystickSpeedFromHealthScore(healthScore):
    maxHealthScore = 100 # CHANGE
    minHealthScore = 0
    averageHealthScore = 50
    if healthScore > averageHealthScore:
        return 1
    elif healthScore < minHealthScore:
        return healthScore / averageHealthScore
    else:
        return 1

# other functions
# INITIALISE KEY VARS

stopDuration = 0
speedAmpltitude = 1
angSpeedAmpltitude = 1
xPosBuffer = [0] * 500
xPosBuffer = deque(xPosBuffer,maxlen=500)
yPosBuffer = [0] * 500
yPosBuffer = deque(yPosBuffer,maxlen=500)
testx = []
testy = []
stops = []
filtered_signal = [] 
startTime = round(utime.time())
Bfilter = ButterworthFilter(9, 3, 0.01)
samplingFrequency = 100 
resetTime = 0
stopDuration = None
stopSignal = 0
speedAmplitudeLog = []
angSpeedAmplitudeLog = []
# ------ THIS WILL BE THE MAIN LOOP ----
listXPOS, listYPOS = readjoystickTextFile(fileName = 'sudden_Stop_100hz_try2.txt')

for i in range(0,len(listYPOS)):


    # ------- EXTRACTION PHASE ------
    # extract joystick input
    # when simulator is turned on a text file can be inputted
    utime.sleep(1/samplingFrequency)
    # --- SIMULATOR VERSION ----- CHANGE THIS LINE FOR REAL OPERATION
    joystickAngularVelocityInput,joystickSpeedInput = readJoystickValues(simulator=True,listXPOS= listXPOS,
    listYPOS= listYPOS,i = i)
    # --- NO CHANGES REQUIRED BELOW


    xPosBuffer.append(joystickAngularVelocityInput)
    testx.append(joystickAngularVelocityInput)
    yPosBuffer.append(joystickSpeedInput)
    testy.append(joystickSpeedInput)


    # extract joystick acceleration

    # extract health score
    healthScore = 50

    # calc current time
    currTime = round(utime.time()) - startTime
    if i % 100 == 0:
        print(currTime)
    # ------- FILTER PHASE -------
    # function to filter input
    filtered_value = Bfilter.update(joystickSpeedInput)
    filtered_signal.append(filtered_value)
    # ana to fill 

    # ------- SYSTEM SAFETY MANEOUVERS -------
    # code to test stop func
    if i % 100 == 0:
        print("stop signal: {}, currTime: {}, resetTime:{}".format(stopSignal,currTime,resetTime))
    if stopSignal == -1 and currTime > resetTime: # reset the stop signal if enough time passes
        stopSignal = 0
        speedAmpltitude = 1
        angSpeedAmpltitude = 1

    if False:
        idx = np.linspace(1,200,200)
        yfake = np.linspace(0.8,-0.8,200)
        plt.plot(idx,yfake)
        plt.show()
    if stopSignal != -1: # under normal operating conditions check if a stop is necessary
        stopSignal,stopDuration = stopIfPullBackDetected(yPosBuffer,100,i)

        if stopSignal == -1:
            resetTime = round(utime.time()) - startTime + stopDuration
    stops.append(stopSignal)
    if stopSignal == -1: # stop if signal detected
        print(stopSignal)
        speedAmpltitude = 0
        angSpeedAmpltitude = 0
    else:
        speedAmpltitude *= calcJoystickSpeedFromHealthScore(healthScore=healthScore) * speedAmpltitude    
        angSpeedAmpltitude *= calcJoystickSpeedFromHealthScore(healthScore=healthScore) * angSpeedAmpltitude    

    
    # ------ CALCULATE DEMANDED SPEEDS ------

    # calc demand speed and angular velocity
    demandSpeed = positionToSpeed(joystickSpeedInput,posSpeedAmplitude=speedAmpltitude,negSpeedAmplitude=speedAmpltitude)
    demandAngularVelocity = positionToAngularVelocity(joystickAngularVelocityInput,posAngVelAmplitude=angSpeedAmpltitude,negAngVelAmplitude=angSpeedAmpltitude)
    angSpeedAmplitudeLog.append(demandAngularVelocity)# monitor these
    speedAmplitudeLog.append(demandSpeed)# monitor these

    # ------ CALCULATE OUTPUT SIGNALS
    # calc motor signals 

    leftMotorSignal, rightMotorSignal = findMotorSignalsFromSetSpeeds(demandSpeed,demandAngularVelocity)


    # PASS MOTOR SIGNAL TO MOTORS


    # update key variables 


print("actual frequency:",800/(utime.time() - startTime)) # actual is around 83 hz for 8 seconds of 100 hz samples
plt.plot(filtered_signal,label = 'filt signal y')
plt.plot(testy,label = 'raw y')
plt.plot(speedAmplitudeLog,label = 'est speed')
print(np.shape(stops))
print(np.shape(testx))
plt.plot(stops)
plt.show()
print("program executed")


        




