'''

PROCESS 1 PSEUDOCODE
'''


# ---- STAGE 1. IMPORT SCRIPTS and initialise classes------
# initalise l2s2

# ----- STAGE 2 - READ VARIABLES IN -----

# read input from joystick to buffer
# read input from accelerometer to accel buffer 
# read input from motors
# read input from gps
# read pressure plate input
# read distance sensor
# 

# ----- STAGE 3 - WARNING SYSTEMS ------
# 
# crash prevention function
# crash detection
# sudden joystick pullback stop

# ---- STAGE 4 - FILTERING AND TREMOR TRACKING ----
# update joystick pos from filter
# record tremor data 

# ---- STAGE 5 - CALCULATE MOTOR DESIRED SIGNALS FROM CONTROL THEORY ------
# find speeds from pos
# find motor signals from speeds


# ----- STAGE 6 - SEND SIGNALS TO MOTOR -----
#updateMotorSignals()

# ----- STAGE 7 - USAGE TRACKING ------
# estimate speed
# estimate distance travelled
# count sitting duration
# GPS


# ----- STAGE 8 - L2S2 (Per minute) ------


# ----



# variables for use in speed Estimator
A = 1
w = 0.1
b = 0.2
tau = 0.6
var_accel = 1
var_motor = 1

def speedEstimator(prevSpeed,leftMotorSignal,rightMotorSignal
                   , leftMotorSignal_prev, rightMotorSignal_prev, acc_y,var_accel,var_motor, time_step = 0.001):
    # estimate curr speed assuming joystick proportional to speed accounting for lag
    # improve confidence by using acceleration to adjust

    leftMotorSignal_approx = (leftMotorSignal - leftMotorSignal_prev)*(1 - math.exp(-time_step) / tau) + leftMotorSignal_prev # exp will be a constant 
    rightMotorSignal_approx = (rightMotorSignal - rightMotorSignal_prev)*(1 - math.exp(-time_step) / tau) + rightMotorSignal_prev
    speed_motor = (leftMotorSignal_approx + rightMotorSignal_approx) / 2 # assuming centre of mass equidistant between wheels


    if (abs(leftMotorSignal - leftMotorSignal_prev) + abs(rightMotorSignal - rightMotorSignal_prev)) < 0.05:
        speed = speed_motor
    else:
        speed_accel =  acc_y * time_step + prevSpeed
        speed = (speed_motor*var_accel + speed_accel*var_motor)  / (var_accel + var_motor) # Kalman filtered velocity
    return speed