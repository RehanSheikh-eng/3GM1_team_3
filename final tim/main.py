## main.py -- put your code here!#change 3
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import utime as time
from functions import log_data, positionToSpeed, positionToAngularVelocity, findMotorSignalsFromSetSpeeds, rateLimitControl
from crash_prevention import startCrashPrevention
from DistanceSensorModule import DistanceSensor
from picozero import Speaker

# define objects involved in crash detection program
distance_sensor = DistanceSensor(0,4,5)
# speaker = Speaker(14, initial_freq=700, duty_factor = 7000)
speaker = Pin(14, Pin.OUT)	
current_total_crashes = 0 
current_true_crashes = 0
parking = False
cur_time = 0
distance_buffer = [501,501,501]
L_prev = 0
R_prev = 0
v_prev = 0
w_prev = 0
test2 = 1
passedUncrashStage = False
wellnessScore = 0.7
# filter code


run = Pin('GP26', Pin.IN)

recovering = False

def stop(tim):
    print("finish")
    L_motor.disable()
    R_motor.disable()
    tim.deinit()

def crash():
    global recovering
    recovering = True
    print("crashed")
    L_motor.disable()
    R_motor.disable()
    global crashTime
    crashTime = time.time()
    global resetTime
    global reinitCrashDetectionTime
    resetTime = crashTime + 2
    reinitCrashDetectionTime = resetTime + 5
    global passedUncrashStage
    passedUncrashStage = False
    global wellnessScore
    wellnessScore = 0.9 * wellnessScore
    

def uncrash():
    print("uncrashed")
    L_motor.enable()
    R_motor.enable()
    global passedUncrashStage
    passedUncrashStage = True


def recovered():
    global recovering
    recovering = False
    print("recovered")
    

def ahmed(tim):
    #global L_prev
    #global R_prev
    global wellnessScore
    global w_prev
    global v_prev
    global test2
    print("test 2", test2)
    #print('test',L_prev,R_prev)
    if not run.value():
        stop(tim)
        
    safety = 0.5
    y, x =  test_joystick.get_values()
    #print(x,y)
    x_filter = x
    y_filter = y
    #x_filter = xfilter_.update(x)
    #y_filter = yfilter_.update(y)
#     print('xy raw',x_filter,y_filter)
    w = positionToAngularVelocity(y,wellnessScore,wellnessScore)
    v = positionToSpeed(x,wellnessScore,wellnessScore)
    #print('dem speeds',v,w)
    v,w = rateLimitControl(v,w,v_prev,w_prev,lowSpeedRateMax = 0.01,highSpeedRateMax = 0.005,decelRate = 0.02)
    #print(' resp speeds',v,w)
    L_,R_ = findMotorSignalsFromSetSpeeds(v,w)
#   
#     print('motor signals',L_,R_)
#     left motor wired up opposite
#     L = min(max(L,-1),1)
#     R = min(max(R,-1),1)
    #L_ = safety*0.9*min(max((x_filter+y_filter)**3,-1),1)
    #R_ = safety*0.9*min(max((x_filter-y_filter)**3,-1),1)
    
#    L = 0.1
#    R = 0.1
    #print('DEMANDED: ',L_,R_)
    #print("prev",R_prev,L_prev)
    #L_,R_ = rateLimitControl(L_,R_,L_prev,R_prev,lowSpeedRateMax = 0.02,highSpeedRateMax = 0.005,decelRate = 0.05)
    #print("SUPPLIED",L_,R_)
    v_prev = v
    w_prev = w
    #R_prev = R_
    #L_prev = L_ 
    #log_data('logfile.csv', {'x': x, 'y': y, 'filtered_x': x_filter, 'filtered_y': y_filter})
    R_ = R_
    L_motor.set_speed(L_)
    R_motor.set_speed(R_)
    
    
    
    # calculate distance
    distance_buffer.pop(0)
    distance_buffer.append(distance_sensor.get_distance())
    distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3
    # crash detection
    global parking
    if not recovering:
        if startCrashPrevention(distance, speaker,parking):
            crash()
    elif recovering and time.time() > resetTime and passedUncrashStage == False:
        uncrash()
    elif recovering and time.time() > reinitCrashDetectionTime:
        recovered()
    # end main function




test_joystick = Joystick('GP28', 'GP27')

L_motor = Motor('GP0', 'GP1', 'GP8')
R_motor = Motor('GP2', 'GP3', 'GP9')

L_motor.enable()
R_motor.enable()


tim = Timer()

while False:
    L_motor.set_speed(0.01)
    R_motor.set_speed(0.01)
    time.sleep(2)
    L_motor.set_speed(0.8)
    R_motor.set_speed(0.8)
    time.sleep(2)    
    #update_motors(tim, distance_sensor, speaker)
    #time.sleep(0.01)

tim.init(mode=Timer.PERIODIC, freq=200, callback=ahmed)