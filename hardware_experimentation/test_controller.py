"""
library made to test controller.py
@ Ashwin Gunasekaran 22/05/23
"""
# first import the necessary libraries
print("RUNNING TESTS ON CONTROLLER ... ")
import controller 
import numpy
import matplotlib.pyplot as plt

visualisation = False # turn on to visualise position to speed function

# test positionToSpeed function
assert(controller.positionToSpeed(0,2,3,5) == 0)
assert(round(controller.positionToSpeed(1,1,1,1),4) == 0.9640)
assert(round(controller.positionToSpeed(-2,2,3,4,2,3,4),6) == -1.999818)

#test positionToSpeed function
assert(controller.positionToAngularVelocity(0,2,3,5) == 0)
assert(round(controller.positionToAngularVelocity(1,1,1,1),4) == 0.9640)
assert(round(controller.positionToAngularVelocity(-2,2,3,4,2,3,4),6) == -1.999818)

assert(round(controller.findMotorSignalsFromSetSpeeds(2,0,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[0],4) == 13.3333)
assert(round(controller.findMotorSignalsFromSetSpeeds(2,0,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[1],4) == 13.3333)
assert(round(controller.findMotorSignalsFromSetSpeeds(0,2,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[0],4) == -3.3333)
assert(round(controller.findMotorSignalsFromSetSpeeds(0,2,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[1],4) == 3.3333)
assert(round(controller.findMotorSignalsFromSetSpeeds(2,2,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[0],4) == 10)
assert(round(controller.findMotorSignalsFromSetSpeeds(2,2,l = 0.5,wheelRadius = 0.15,motorVoltageConstant = 1)[1],4) == 16.6667)

if visualisation == True:
    x = np.linspace(-20,20,100)
    y = []
    for element in x:
        y.append(controller.positionToSpeed(element))
    plt.plot(x,y)
    plt.show()

print("NO ERRORS DETECTED")