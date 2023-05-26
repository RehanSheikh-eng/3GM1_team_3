import utime as time

def start_crash_prevention(distance_sensor, motor, speaker, current_total_crashes, MA_order=3, time_step=1, DEBUG=True):  
    while True:
        distance = distance_sensor.get_smooth_distance(MA_order)
        gap_width = 0.004*distance # maps distance to period between speaker pulses in seconds

        if DEBUG:
            print("Distance:", distance, "mm")

        if distance < 500: # and low velocity
            speaker.play(tune = 750, duration = 0.1)
            time.sleep(gap_width)

        if distance < 500: # and high velocity
            motor.disable()
            time.sleep(5)
            motor.enable()
            current_total_crashes += 1 # Records the number of actual crashes and near misses
            # ADD CODE TO TURN ON BRAKES
            
    
        time.sleep(time_step)

