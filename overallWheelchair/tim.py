# main.py -- put your code here!#change 3
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import utime as time
from functions import log_data, positionToSpeed, positionToAngularVelocity, findMotorSignalsFromSetSpeeds
from crash_prevention import startCrashPrevention
from DistanceSensorModule import DistanceSensor
from picozero import Speaker

# define objects involved in crash detection program
distance_sensor = DistanceSensor(0,4,5)
speaker = Speaker(14, initial_freq=750, duty_factor = 0)
current_total_crashes = 0 
current_true_crashes = 0
parking = False
cur_time = 0
distance_buffer = [501,501,501]

# filter code

class ButterworthFilter:
    def __init__(self, order, cutoff_freq, sampling_period):
        self.order = order
        self.cutoff_freq = cutoff_freq
        self.sampling_period = sampling_period
        self.coefficients = [0.0] * (order + 1)
        self.inputs = [0.0] * (order + 1)
        self.outputs = [0.0] * (order + 1)

        self.calculate_coefficients()

    def calculate_coefficients(self):
        # Calculate filter coefficients
        a = [0.0] * (self.order + 1)
        b = [0.0] * (self.order + 1)
        theta_c = 2.0 * math.pi * self.cutoff_freq
        k = math.tan(theta_c * self.sampling_period / 2.0)
        k2 = k * k

        a[0] = 1.0
        a[1] = self.order * k2 + 2.0 * k + 1.0
        for i in range(2, self.order + 1):
            a[i] = k2 * a[i - 2] + 2.0 * k * a[i - 1] + a[i - 2]

        b[0] = k2 * self.order
        b[1] = 2.0 * k2 * self.order
        for i in range(2, self.order + 1):
            b[i] = k2 * b[i - 2] + 2.0 * k * b[i - 1] + b[i - 2]

        self.coefficients = [bi / ai for bi, ai in zip(b, a)]

    def update(self, input_value):
        # Apply the filter
        self.inputs.pop(0)
        self.inputs.append(input_value)

        output = 0.0
        for i in range(self.order + 1):
            output += self.coefficients[i] * self.inputs[self.order - i]

        self.outputs.pop(0)
        self.outputs.append(output)

        return output



# speedAmpltitude = 1
# angSpeedAmpltitude = 1
# xPosBuffer = [0] * 500
# xPosBuffer = deque(xPosBuffer,maxlen=500)
# yPosBuffer = [0] * 500
# yPosBuffer = deque(yPosBuffer,maxlen=500)
# testx = []
# testy = []
# stops = []
# filtered_signal = [] 
# startTime = round(utime.time())
xfilter_ = ButterworthFilter(9, 2.5, 0.01)
yfilter_ = ButterworthFilter(9, 2.5, 0.01)

run = Pin('GP26', Pin.IN)

def ahmed(tim):
    safety = 1
    x, y =  test_joystick.get_values()
    print(x,y)
    #x_filter = x
    #y_filter = y
    x_filter = xfilter_.update(x)
    y_filter = yfilter_.update(y)
    print('xy raw',x_filter,y_filter)
    w = positionToAngularVelocity(y)
    v = positionToSpeed(x)
    print('speeds',v,w)
    L_,R_ = findMotorSignalsFromSetSpeeds(v,w)
    print('motor signals',L_,R_)
    #left motor wired up opposite
    #L = min(max(L,-1),1)
    #R = min(max(R,-1),1)
    #L = safety*1*min(max(x_filter+y_filter,-1),1)
    #R = safety*1*min(max(x_filter-y_filter,-1),1)
    #R = 0.3
    #L = 0.3
    #L = -L
    #print('lR: ',L,R)
    #log_data('logfile.csv', {'x': x, 'y': y, 'filtered_x': x_filter, 'filtered_y': y_filter})
    L_motor.set_speed(L_)
    R_motor.set_speed(R_)
    if not run.value():
        print("finish")
        L_motor.disable()
        R_motor.disable()
        

        tim.deinit()
    
    # calculate distance
    distance_buffer.pop(0)
    distance_buffer.append(distance_sensor.get_distance())
    distance = (distance_buffer[0] + distance_buffer[1] + distance_buffer[2])/3
    # crash detection
    startCrashPrevention(distance, speaker)

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

tim.init(mode=Timer.PERIODIC, freq=100, callback=ahmed)
 