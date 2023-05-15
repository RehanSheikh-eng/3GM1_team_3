import machine
import vl53l0x

class DistanceSensor:
    def __init__(self, scl = 5, sda = 4):
        i2c = machine.I2C(0, scl, sda)
        self.sensor = vl53l0x.VL53L0X(i2c)
        self.sensor.start()
        
    def get_distance(self):
        return self.sensor.read()


def start_crash_prevention():
    IR_distance = DistanceSensor(5,4)
    
    if IR_distance.get_distance < 10: # ADJUST THRESHOLD
        # TURN ON BRAKES
