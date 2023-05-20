import utime as time

def start_crash_prevention(distance_sensor, MA_order=3, time_step=1, DEBUG=True):
    while True:
        distance = distance_sensor.get_smooth_distance(MA_order)

        if Debug:
            print("Distance:", distance, "mm")

        if distance < 200:
            print("CRASH RISK!")
            break
            # REPLACE WITH CODE TO TURN ON BRAKES/TURN OFF MOTOR
    
        time.sleep(time_step)

