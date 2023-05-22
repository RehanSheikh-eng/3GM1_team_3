'''
FOR MICROPYTHON (TO BE RUN ON PICO)
'''

import L2S2SPItest as L2S2

# Test data
GPS_longitude = "69"

# Configure wifi
payload_set_wifi = bytearray("AndroidAP0DE9|tgir1565".encode("utf-8"))
L2S2.spiToL2S2(5, payload_set_wifi)

# Configure field ID
def get_field_id(record_id, plate_template_id, control_id):
    return record_id + "|" + plate_template_id + "|" + control_id

record_id = "110" # Patient: Minnie Mouse
plate_template_id = "6e0485b5-cd17-4438-aff8-afe0578ed71f" # Plate: Group_3_Production
control_id = "4" # Textbox: GPSLongitude

field_id = get_field_id(record_id, plate_template_id, control_id)

# Configure payload
def get_payload(field_id, type, content, units = None):
    '''
    See Page 12 of "Instrument to MMDC" document for type code
    '''
    _type = bytearray(1)
    _type[0] = type
    payload =  bytearray(field_id.encode("utf-8")) + _type + bytearray(content.encode("utf-8")) + bytearray(units.encode("utf-8"))
    return payload

payload_test = get_payload(field_id, type = "5", content = GPS_longitude, units = "degrees")

# Send data
L2S2.spiToL2S2(150, payload = payload_test)