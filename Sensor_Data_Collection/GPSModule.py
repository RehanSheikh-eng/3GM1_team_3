import serial
import time
import json

class GPSModule:
    def __init__(self, port='/dev/serial0', baud_rate=9600, timeout=1):
        """
        Initializes the GPSModule object.

        Args:
            port (str): The port to which the GPS module is connected.
            baud_rate (int): The baud rate for serial communication.
            timeout (float): The timeout for serial communication.
        """
        self.ser = serial.Serial(port, baud_rate, timeout=timeout)
        self.ser.flush()
        self.decimal_format = decimal_format


    def get_data(self):
        """
        Gets the data from the GPS module.

        Returns:
            dict: A dictionary containing the timestamp, latitude, and longitude.
        """
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            data = self.parse_gpgga_string(line)
            return data

    def parse_gpgga_string(self, gpgga_string):
        """
        Parses a GPGGA string to extract the GPS data.

        Args:
            gpgga_string (str): The GPGGA string to parse.

        Returns:
            dict: A dictionary containing the timestamp, latitude, and longitude.
        """
        components = gpgga_string.split(",")
        if "$GPGGA" in components[0]:
            timestamp = components[1]
            latitude = components[2]
            longitude = components[4]
            return {
                "timestamp": timestamp,
                "latitude": latitude,
                "longitude": longitude
            }
        else:
            return None

    def dump_to_json(self, filepath):
        """
        Dumps the GPS data to a JSON file.

        Args:
            filepath (str): The path to the JSON file.
        """
        data = self.get_data()
        if data:
            with open(filepath, 'w') as f:
                json.dump(data, f)
