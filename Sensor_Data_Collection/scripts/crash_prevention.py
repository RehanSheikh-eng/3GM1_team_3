import utime as time

def start_crash_prevention(distance_sensor, motor, speaker, current_total_crashes, MA_order=3, time_step=1, DEBUG=True):  
    while True:
        distance = distance_sensor.get_smooth_distance(MA_order)

        if DEBUG:
            print("Distance:", distance, "mm")

        if distance < 500: # and low velocity
            gap_width = 0.002*distance # maps distance to period between speaker pulses in seconds
            speaker.play(tune = 750, duration = 0.1)
            t = gap_width
        elif distance < 500: # and high velocity
            motor.disable()
            time.sleep(5)
            motor.enable()
            current_total_crashes += 1 # Records the number of actual crashes and near misses
            t = time_step
            # ADD CODE TO TURN ON BRAKES
        else:
            t = time_step
            
    
        time.sleep(t)

