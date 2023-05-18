import pytest
from machine import UART
from unittest.mock import Mock, MagicMock, patch
from GPSModule import GPSModule

@patch('GPSModule.UART', new_callable=MagicMock)
def test_gpsmodule_init(mock_uart):
    GPSModule(1, 9600)
    mock_uart.assert_called_once_with(1, 9600)

def test_parse_gpgga_string():
    gps_module = GPSModule()
    gpgga_string = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    expected_output = {"timestamp": "123519", "latitude": "4807.038", "longitude": "01131.000"}
    assert gps_module.parse_gpgga_string(gpgga_string) == expected_output

def test_convert_to_degrees():
    gps_module = GPSModule()
    raw_value = 4807.038
    expected_output = 48.1173
    assert abs(float(gps_module.convert_to_degrees(raw_value)) - expected_output) < 0.0001

def test_get_relative_position():
    gps_module = GPSModule()
    gpgga1 = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    gpgga2 = "$GPGGA,123520,4807.038,N,01132.000,E,1,08,0.9,545.4,M,46.9,M,,*48"
    expected_output = 55597.76  # approximately 55.6 kilometers
    assert abs(gps_module.get_relative_position(gpgga1, gpgga2) - expected_output) < 10  # accept a difference of up to 10 meters

def test_get_data():
    gps_module = GPSModule()
    gps_module.uart = Mock()
    gps_module.uart.any.return_value = True
    gps_module.uart.readline.return_value = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    expected_output = {"timestamp": "123519", "latitude": "4807.038", "longitude": "01131.000"}
    assert gps_module.get_data() == expected_output
