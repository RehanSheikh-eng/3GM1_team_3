import utime as time
from collections import deque


def joystick_change(joystick_y_positions):
    '''
    Args: array, queue and array for three joystick positions in the range -1 to 1
    Returns: total absolute change in x or y joystick position over the past 3 seconds when sampled at 1Hz
    '''

    return abs(joystick_y_positions[0] - joystick_y_positions[1]) + abs(joystick_y_positions[1] - joystick_y_positions[2])

def start_crash_prevention(distance_sensor, motor, speaker, joystick, MA_order=3, time_step=1, DEBUG=True):

    # Initialise queue for joystick data. Assumption: wheelchair takes 3s to reach steady-state velocity when joystick is fully forward
    joystick_y_positions = deque([0,0,0])

    # Initialise counter for total crashes (number of actual crashes and near misses)
    global current_total_crashes
    current_total_crashes = 0

    # Load SpeedAmplitude (i.e. joystick gain as a global variable)
    global speedAmplitude
    global angSpeedAmplitude
    global stopSignal
    
    while True:
        distance = distance_sensor.get_smooth_distance(MA_order)

        joystick_y_positions.append(joystick.get_values()[1])
        joystick_y_positions.popleft()
        stick_change = joystick_change(joystick_y_positions)

        if DEBUG:
            print("Distance:", distance, "mm")

        if distance < 500 and (stick_change > 0.1 or joystick_y_positions[2] < 0.975):
            gap_width = 0.002*distance # maps distance to period between speaker pulses in seconds
            speaker.play(tune = 750, duration = 0.1)
            t = gap_width
            speedAmplitude = distance/500 # scale joystick gain according to distance from object
            angSpeedAmplitude = distance/500
        elif distance < 500 and stick_change < 0.1 and joystick_y_positions[2] > 0.975:
            stopSignal = -1 # turns on the brakes
            current_total_crashes += 1
            t = time_step
        else:
            t = time_step
            posSpeedAmplitude = 1
            
    
        time.sleep(t)

