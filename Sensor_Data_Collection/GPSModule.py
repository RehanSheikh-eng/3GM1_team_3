from machine import UART, Pin
from math import radians, sin, cos, sqrt, atan2
import utime as time

class GPSModule:

    def __init__(self, uart_id=1, baud_rate=9600, tx_pin_id=4, rx_pin_id=5):
        self.uart = UART(uart_id, baud_rate, tx=Pin(tx_pin_id), rx=Pin(rx_pin_id))
        self.uart.init(baud_rate, bits=8, parity=None, stop=1)

    def get_data(self):
        if self.uart.any():
            line = self.uart.readline()
            if line:
                data = self.parse_gpgga_string(line)
                return data
        return None

    def parse_gngga_string(self, gpgga_string):
        components = gpgga_string.decode().split(",")
        if "GNGGA" in components[0]:
            timestamp = components[1]
            latitude = self.convert_to_degrees(float(components[2]))
            longitude = self.convert_to_degrees(float(components[4]))
            return {
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude
            }
        else:
            return None

    def convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position