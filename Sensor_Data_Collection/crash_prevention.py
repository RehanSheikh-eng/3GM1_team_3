import machine
import vl53l0x

class DistanceSensor:
    def __init__(self):
        i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
        self.sensor = vl53l0x.VL53L0X(i2c)
        self.sensor.start()
        
    def get_distance(self):
        return self.sensor.read()
