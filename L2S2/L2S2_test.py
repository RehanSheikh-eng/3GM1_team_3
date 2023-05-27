'''
FOR MICROPYTHON (TO BE RUN ON PICO)
'''

import L2S2_lib as L2S2
import utime as time

# Boot
L2S2.boot_L2S2()

# Configure wifi
#payload_set_wifi = bytearray('AndroidAP|wtdm1984'.encode("utf-8"))
#L2S2.spiToL2S2(5, payload_set_wifi)

# Send data
L2S2.data_send(_record_id = "110", _plate_id = "6e0485b5-cd17-4438-aff8-afe0578ed71f", _control_id = "17", _type = 2, _content = 420, _units = "degrees")