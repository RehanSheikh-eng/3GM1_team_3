from machine import UART, Pin
from math import radians, sin, cos, sqrt, atan2
import utime as time

class GPSModule:

    def __init__(self, uart_id=1, baud_rate=9600, tx_pin_id=4, rx_pin_id=5):
        self.uart = UART(uart_id, baud_rate, tx=Pin(tx_pin_id), rx=Pin(rx_pin_id))
        self.uart.init(baud_rate, bits=8, parity=None, stop=1)

    def get_data(self):
        data = b''
        while self.uart.any():
            data += self.uart.readline()
        if data:
            try:
                sentences = data.decode().split('\r\n')  # split data into separate sentences
                for sentence in sentences:
                    if sentence:
                        #print(sentence)
                        parsed_data = self.parse_gpgga_string(sentence)
                        if parsed_data is not None:
                            return parsed_data
                        
            except UnicodeError:
                print("Error: Unicode Error")
                
        return None


    def parse_gpgga_string(self, gpgga_string):
        try:
            components = gpgga_string.split(",")
            #print(components)
        except UnicodeError:
            print("Error: Unable to decode string.")
            return None
        except AttributeError:
            print("Error: The input is not a string.")
            return None

        if "GPRMC" in components[0]:
            try:
                timestamp = components[1]
                latitude = components[2] if "GPGGA" in components[0] else components[3]
                longitude = components[4] if "GPGGA" in components[0] else components[5]

                if latitude and longitude:  # Ensure the fields are not empty
                    latitude = self.convert_to_degrees(float(latitude))
                    longitude = self.convert_to_degrees(float(longitude))
                else:
                    print("Error: Latitude or Longitude data missing.")
                    return None
            except (IndexError, ValueError):
                print("Error: Invalid NMEA sentence.")
                return None

            return {
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude
            }

        return None

    def convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

    def get_relative_position(self, data1, data2):
        R = 6371e3  # Earth's radius in meters
        try:
            lat1 = radians(float(data1["latitude"]))
            lon1 = radians(float(data1["longitude"]))
            lat2 = radians(float(data2["latitude"]))
            lon2 = radians(float(data2["longitude"]))
        except TypeError:
            return 0
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c  # Output distance in meters


