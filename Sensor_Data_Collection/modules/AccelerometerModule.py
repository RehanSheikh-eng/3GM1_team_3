from machine import I2C, Pin
from lib import mpu6050
import utime as time
import collections


GRAVITY_ACCEL = 9.81
class AccelData(
    collections.namedtuple(
        "AccelData", ["AccX", "AccY", "AccZ"]
    )
):
    pass

class Accel:

    def __init__(self, i2c_id=0, sda_pin=8, scl_pin=9):

        self.i2c = I2C(i2c_id, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.sensor = mpu6050.MPU(self.i2c)
        self.running = False

    def get_corrected_values(self):

        values = self.sensor.read_sensors_scaled()
        return AccelData(values.AccX * GRAVITY_ACCEL, values.AccY * GRAVITY_ACCEL, values.AccZ * GRAVITY_ACCEL)


