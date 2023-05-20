import utime as time
import math

def crash_detection(accel, time_step=1, DEBUG=True):
    """
    Monitors accelerometer data to detect crash events.
    Triggers a buzzer and records the event on the front-end application through the L2S2 pipeline.

    Args:
        accel (Accel): The accelerometer object.
        t (int): The time step between samples.

    Returns:
        float: Crash signal
    """

    while True:
        
        acc_data = accel.get_corrected_values()
        acc_mag = math.sqrt(acc_data["AcX"]**2 + acc_data["AcY"]**2 + acc_data["AcZ"]**2)

        if DEBUG:
            print(f"Acceleration Magnitude: {acc_mag}ms^-2")
            
        if acc_mag > 6: # Tuned using collision testing and normal use data
            # TRIGGER CRASH DETECTION PROTOCOL:
            # 1. TRIGGER BUZZER
            # 2. RECORD INCIDENT THROUGH L2S2 PIPELINE
            pass
        
        time.sleep(time_step)