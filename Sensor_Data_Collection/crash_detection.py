import accelerometer
import time
import math

def crash_detection(accel, t = 1):
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
        time.sleep(t)
        acc_data = accel.get_corrected_values()
        acc_mag = math.sqrt(acc_data["AcX"]**2 + acc_data["AcY"]**2 + acc_data["AcZ"]**2)

        if acc_mag > 6: # Tuned using collision testing and normal use data
            # TRIGGER CRASH DETECTION PROTOCOL
