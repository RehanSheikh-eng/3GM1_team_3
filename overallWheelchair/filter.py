#change 4
from motor_controller import Motor
from joystick import Joystick
from machine import Timer, Pin
from collections import deque
import math
import utime as time
from functions import log_data
from crash_prevention import startCrashPrevention
from DistanceSensorModule import DistanceSensor
from picozero import Speaker

# define objects involved in crash detection program
distance_sensor = DistanceSensor(0,4,5)
speaker = Speaker(14, initial_freq=750, duty_factor = 7000)
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
xfilter_ = ButterworthFilter(9, 2, 0.01)
yfilter_ = ButterworthFilter(9, 2, 0.01)

run = Pin('GP26', Pin.IN)

def ahmed(tim):
    safety = 1
    y, x =  test_joystick.get_values()
    #x_filter = x
    #y_filter = y
    x_filter = -xfilter_.update(x)
    y_filter = -yfilter_.update(y)
    L = safety*1*min(max(x_filter+y_filter,-1),1)
    R = safety*1*min(max(x_filter-y_filter,-1),1)
    print('lR: ',L,R)
    #log_data('logfile.csv', {'x': x, 'y': y, 'filtered_x': x_filter, 'filtered_y': y_filter})
    L_motor.set_speed(L)
    R_motor.set_speed(R)
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

#while True:
 #   update_motors(tim, distance_sensor, speaker)
 #   time.sleep(0.01)

tim.init(mode=Timer.PERIODIC, freq=100, callback=ahmed)