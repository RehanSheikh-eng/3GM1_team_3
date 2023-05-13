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
    start():
        Starts data collection from the accelerometer.
    stop():
        Stops data collection from the accelerometer.
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

    def start(self):
        """
        Starts data collection from the accelerometer. The data is printed as a JSON string with the following keys:
        'AcX', 'AcY', 'AcZ', 'Tmp', 'GyX', 'GyY', 'GyZ', and 'timestamp'.

        Data collection continues until the stop() method is called.
        """
        self.running = True
        while self.running:
            values = self.sensor.get_values()
            values['timestamp'] = time.time()
            ujson.dumps(values, "accelerometer_data")
            time.sleep(1)

    def stop(self):
        """
        Stops data collection from the accelerometer.
        """
        self.running = False

    def get_corrected_values(self):
        """
        Retrieve the sensor values and correct for drift using a complementary filter.

        Returns:
            dict: A dictionary containing the timestamp, corrected accelerometer, and gyroscope values.
        """
        pass
    