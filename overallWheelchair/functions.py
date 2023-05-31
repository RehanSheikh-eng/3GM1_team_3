"""

All functions that are used in main.py are stored here

"""



# import libraries
from collections import deque
from picozero import Speaker
import utime as time
import math

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

# warning functions
def startCrashPrevention(distance, speed, speaker, speed_threshold = 1, beep_width = 100):
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

def positionToSpeed(x,posSpeedAmplitude,negSpeedAmplitude,posSpeedOffset = -0.4,posSpeedFreq = 2.3,\
                      negSpeedOffset = 0.4,negSpeedFreq = 2.3 ):
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
        v = 0.85 * posSpeedAmplitude*math.tanh((posSpeedFreq * x) + posSpeedOffset)
        return max(0,v)
    elif x < 0:
        # work in negative speed part of graph
        v = 0.85 * negSpeedAmplitude*math.tanh((negSpeedFreq * x) + negSpeedOffset)
        return min(v,0)
    else:
        return 0

def positionToAngularVelocity(x,posAngVelAmplitude,negAngVelAmplitude,posAngVelOffset = -0.4,posAngVelFreq = 2.3,\
                      negAngVelOffset = 0.4,negAngVelFreq = 2.3 ):
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
    signalGain = 0.75 # gain of input pos
    x = signalGain * x
    if x > 0:
        # work in positive speed part of graph 
        v = posAngVelAmplitude* math.tanh(posAngVelFreq * x +posAngVelOffset)
        return max(v,0)
    elif x < 0:
        # work in negative speed part of graph
        v = negAngVelAmplitude*math.tanh(negAngVelFreq * x +negAngVelOffset)
        return min(0,v)
    else:
        return 0

def findMotorSignalsFromSetSpeeds(v,omega,l = 0.2,wheelRadius = 0.05,motorVoltageConstant = 1):
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
    signalGain = 0.15 # change this to keep the range as desired
    v, omega = v *  (1/3) *signalGain, omega * signalGain * 2
    leftWheelSpeed = v + omega*l/2
    rightWheelSpeed = v - omega*l/2
    leftWheelAngVel = leftWheelSpeed / wheelRadius
    rightWheelAngVel = rightWheelSpeed / wheelRadius
    leftMotorSignal = leftWheelAngVel * motorVoltageConstant
    rightMotorSignal = rightWheelAngVel * motorVoltageConstant
    return leftMotorSignal, rightMotorSignal




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
import uos

def log_data(filename, data):
    try:
        if filename not in uos.listdir():
            # Open the file for writing if it doesn't exist
            with open(filename, "w") as file:
                # Write the header to the file
                file.write(','.join([key for key in data.keys()]) + '\n')

        # Open the file for appending
        with open(filename, "a") as file:
            # Write the data to the file
            file.write(','.join([str(value) for value in data.values()]) + '\n')

    except Exception as e:
        print("Error writing to file: ", e)

def rateLimitControl(L,R,L_prev,R_prev,lowSpeedRateMax = 0.005,highSpeedRateMax = 0.005,decelRate=0.01):
    """
    function to limit change in motor rate in response to instability issues
    :param @L - current L motor position
    :param @L - current R motor position
    :param @L_prev - last set left motor position
    :param @R_prev - last set right motor position

    """
    # first limit L

    # decide which rate to use
    if abs(L) < 0.3 or abs(R) < 0.3:
        rateMax = lowSpeedRateMax
    elif abs(L) >=0.3 and abs(R)  >= 0.3:
        rateMax = highSpeedRateMax
    else:
        rateMax = lowSpeedRateMax
        print("Unusual condition in rate decider loop")
    deltaL = L - L_prev
    if abs(L) < abs(L_prev) or abs(R) < abs(R_prev):
        rateMax = decelRate
    if abs(deltaL) <= rateMax: # set values if not rate limited
        L_sp = L_prev + deltaL
    elif deltaL < 0:
        L_sp = L_prev - rateMax
    elif deltaL > 0:
        L_sp = L_prev + rateMax
    else:
        print("Unexpected condition detected in L")

    # now limit R
    deltaR = R - R_prev
    if abs(deltaR) <= rateMax:
        R_sp = R_prev + deltaR
    elif deltaR < 0:
        R_sp = R_prev - rateMax
    elif deltaR > 0:
        R_sp = R_prev + rateMax
    else:
        print("Unexpected condition detected in R")
    return L_sp, R_sp
