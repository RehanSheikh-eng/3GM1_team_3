"""
This script creates functions that will form part of the joystick control system

@ Ashwin Gunasekaran
created on 22/05/23
"""
# first import the necessary libraries
import numpy as np
import math
import matplotlib.pyplot as plt

# next define the necessary functions


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



# other functions

# create stop mechanism

def stopIfPullBackDetected(ypos,freq):

    """
    When given in a list of previous y positions at least for 2 seconds then detect if sudden pull back 

    :param @ypos: list of previous speed positions on joystick
    :out binary signal (-1,0) 
    if sharp pull back detected then a -1 is sent
    or button pressed
    """
    deltaT = 1 / freq
    cutoff = 0.5
    # detect if curr pos is less than -0.5
    # also rate of change must be big 
    # in last second must value must be greater than 0.5
    currPosTest  = (np.average(ypos[-10:-1]) < -0.5 )
    rate = (ypos[-1] - ypos[-(freq+1)])/(deltaT * freq )
    print("rate={}".format(rate))
    rateHigh = (rate < cutoff)
    lastSecond = ypos[-(freq+50):-1]
    highestValue = max(lastSecond)
    print("highest value = {}".format(highestValue))
    lastSecondPositive = highestValue > 0.3
    print(currPosTest,rateHigh,lastSecondPositive)
    if currPosTest and rateHigh and lastSecondPositive:
        return -1
    else:
        return 0

# ------ THIS WILL BE THE MAIN LOOP ----
# extract joystick input
joystickSpeedInput = 0
joystickAngularVelocityInput = 0


# extract joystick acceleration

# function to filter input
# ana to fill 

# calc demand speed and angular velocity
speedAmpltitude = 1

# code to test stop func
idx = np.linspace(1,200,200)
yfake = np.linspace(0.8,-0.8,200)
plt.plot(idx,yfake)
plt.show()
stop = stopIfPullBackDetected(yfake,100)
print(stop)
if stop == -1:
    speedAmpltitude = 0
    
    
demandSpeed = positionToSpeed(joystickSpeedInput,posSpeedAmplitude=speedAmpltitude,negSpeedAmplitude=speedAmpltitude)
demandAngularVelocity = positionToAngularVelocity(joystickAngularVelocityInput)



# calc motor signals 

leftMotorSignal, rightMotorSignal = findMotorSignalsFromSetSpeeds(demandSpeed,demandAngularVelocity)

# pass signals to motors


print("success")


    




