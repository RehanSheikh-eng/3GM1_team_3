from machine import I2C, Pin
import mpu6050
import time
import ujson

class Accel:
    """
    A class used to represent an MPU6050 Accelerometer.

    Attributes
    ----------
    i2c : I2C
        an I2C object for communication
    sensor : mpu6050
        an mpu6050 accelerometer object
    running : bool
        a flag indicating whether data collection is currently running

    Methods
    -------
    """

    def __init__(self, sda_pin=8, scl_pin=9):
        """
        Constructs all the necessary attributes for the accelerometer object.

        Parameters
        ----------
        sda_pin : int, optional
            the GPIO pin number used for the I2C data line (SDA)
        scl_pin : int, optional
            the GPIO pin number used for the I2C clock line (SCL)
        """
        self.i2c = I2C(1, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.sensor = mpu6050.accel(self.i2c)
        self.running = False

    def get_corrected_values(self):
        """
        Retrieve the sensor values and correct for acceleration due to gravity

        Returns:
            dict: A dictionary containing the timestamp, corrected accelerometer, and gyroscope values.
        """
        values = self.sensor.get_values()
        values["AcZ"] -= 9.81
        values['timestamp'] = time.time()
        return values

