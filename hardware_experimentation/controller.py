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
        v = negSpeedAmplitude*math.tanh(((negSpeedFreq * x) +negSpeedOffset))
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



