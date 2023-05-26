import utime as time
from collections import deque

def joystick_change(joystick_y_positions):
    '''
    Args: array, queue and array for three joystick positions in the range -1 to 1
    Returns: total absolute change in x or y joystick position over the past 3 seconds when sampled at 1Hz
    '''

    return abs(joystick_y_positions[0] - joystick_y_positions[1]) + abs(joystick_y_positions[1] - joystick_y_positions[2])

def start_crash_prevention(distance_sensor, motor, speaker, joystick, current_total_crashes, MA_order=3, time_step=1, DEBUG=True):

    # Initialise queue for joystick data. Assumption: wheelchair takes 3s to reach steady-state velocity when joystick is fully forward
    joystick_y_positions = deque([0,0,0])
    
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
        elif distance < 500 and stick_change < 0.1 and joystick_y_positions[2] > 0.975 :
            motor.disable()
            time.sleep(5)
            motor.enable()
            current_total_crashes += 1 # Records the number of actual crashes and near misses
            t = time_step
            # ADD CODE TO TURN ON BRAKES
        else:
            t = time_step
            
    
        time.sleep(t)

