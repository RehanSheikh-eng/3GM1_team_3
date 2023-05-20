from machine import I2C, Pin
import VL53L0X as vl

class DistanceSensor:
    '''
    Class to receive distance data (in mm) from the VL53L0X infrared sensor
    Note: accuracy of sensor is low above 500mm
    '''
    def __init__(self, id, sda, scl):
        self.i2c = I2C(id = id, sda = Pin(sda), scl = Pin(scl))
        self.sensor = vl.VL53L0X(self.i2c)
        self.sensor.start()
    
    def get_distance(self):
        return self.sensor.read()
    
    def get_smooth_distance(self, MA_order = 3): # Computes the calibrated moving average (default = 3-point moving average)
        self.average_distance = 0
        for i in range(MA_order):
            self.average_distance += self.sensor.read()
        return ((int(self.average_distance) / MA_order) - 52) # Offset needed for calibration
    

