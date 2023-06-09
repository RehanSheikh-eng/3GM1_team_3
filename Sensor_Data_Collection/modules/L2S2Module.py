import machine
import utime
import time
import ustruct
import sys

class L2S2Module:
    def __init__(self):
        self.spi1 = None
        self.spi1cs = None
        self.L2S2_TIMEOUT = 10
        self.table = [ 
            # Your table values
        ]

    def setL2S2SPI(self):
        self.spi1 = machine.SPI(1,
                        baudrate=100000,
                        polarity=0,
                        phase=1,
                        bits=8,
                        firstbit=machine.SPI.MSB,
                        sck=machine.Pin(10),
                        mosi=machine.Pin(11),
                        miso=machine.Pin(12))
    
    def boot_L2S2(self):
        self.spi1cs = machine.Pin(13, machine.Pin.OUT)
        self.spi1cs.value(1)
        self.setL2S2SPI()
        print(self.myTimeNow(), "Startup")

    def myTimeNow(self):
        yr, mt, d, hr, m, s, day, yrday = utime.localtime()
        yr = str(yr) if len(str(yr)) > 1 else "0" + str(yr)
        mt = str(mt) if len(str(mt)) > 1 else "0" + str(mt)
        d = str(d) if len(str(d)) > 1 else "0" + str(d)
        hr = str(hr) if len(str(hr)) > 1 else "0" + str(hr)
        m = str(m) if len(str(m)) > 1 else "0" + str(m)
        s = str(s) if len(str(s)) > 1 else "0" + str(s)
        return yr + "-" + mt + "-" + d + " " + hr + ":" + m + ":" + s

    def CCITT_crc16_false(self, data: bytes, start, length): # ignoring start and length for now as it wasn't used
        table = [ 
            0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
            0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6, 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
            0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485, 0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
            0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4, 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
            0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823, 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
            0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12, 0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
            0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41, 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
            0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70, 0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
            0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F, 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
            0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E, 0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
            0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D, 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
            0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C, 0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
            0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB, 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
            0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A, 0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
            0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9, 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
            0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8, 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
        ]
        
        crc = 0xFFFF
        for byte in data:
            crc = (crc << 8) ^ table[(crc >> 8) ^ byte]
            crc &= 0xFFFF
        return crc

    def set_wifi(self, wifi_name, wifi_password):
        payload_set_wifi = bytearray((wifi_name + "|" + wifi_password).encode("utf-8"))
        self.spiToL2S2(5, payload_set_wifi)

    def spiToL2S2(self, header, payload):

        hdr = bytearray(header.to_bytes(1,'little'))
        length = bytearray(len(payload).to_bytes(2,'little'))
        crc = self.CCITT_crc16_false(hdr + length + payload, 0, int(len(hdr + length + payload)))
        crcarray = bytearray(crc.to_bytes(2,'little'))
        packetToSend = hdr + length + crcarray + payload
        print(self.myTimeNow(),"Sending ", " ".join('{:02x}'.format(x) for x in packetToSend))

        self.spi1cs.value(0)
        self.spi1.write(packetToSend)
        self.spi1cs.value(1)
        time.sleep_ms(10)
        self.spi1cs.value(0)
        replyHeader = b'\x00'
        startTime = time.ticks_ms()
        while (replyHeader == b'\x00' and time.ticks_diff(time.ticks_ms(), startTime)<(self.L2S2_TIMEOUT*1000)):
            self.spi1cs.value(0) 
            replyHeader = self.spi1.read(1)
            time.sleep_ms(100)
            if replyHeader == b'\x00':
                self.spi1cs.value(1)
        ##### Show response on spi #####
        replyLength = self.spi1.read(2)
        replyCRC = self.spi1.read(2)
        replyLengthVal = int.from_bytes(replyLength, 'little')
        if replyLengthVal > 0x400:
            replyLengthVal = 0x400
        replyPayload = self.spi1.read(replyLengthVal)
        self.spi1cs.value(1)

        crc = self.CCITT_crc16_false(replyHeader + replyLength + replyPayload, 0, int(len(replyHeader + replyLength + replyPayload)))
        print(self.myTimeNow(),"Reply Header ", " ".join('{:02x}'.format(x) for x in replyHeader))
        print(self.myTimeNow(),"Reply Length ", " ".join('{:02x}'.format(x) for x in replyLength))
        print(self.myTimeNow(),"Reply CRC ", " ".join('{:02x}'.format(x) for x in replyCRC))
        print(self.myTimeNow(),"Reply Payload ", " ".join('{:02x}'.format(x) for x in replyPayload))
        print(self.myTimeNow(),"Calculated CRC ", " ".join('{:02x}'.format(x) for x in crc.to_bytes(2,'little')))

        if crc.to_bytes(2,'little') == replyCRC :
            print(self.myTimeNow(),"Received: Header ", " ".join('{:02x}'.format(x) for x in replyHeader), "Payload ", " ".join('{:02x}'.format(x) for x in replyPayload))
            return replyHeader, replyPayload
        else:
            print(self.myTimeNow(),"L2S2 Timeout or CRC error")
            time.sleep(1)
            return b'\x00', b'\x00'

    @staticmethod
    def get_field_id(record_id, plate_template_id, control_id):
        return record_id + "|" + plate_template_id + "|" + control_id + "\0"

    @staticmethod
    def get_payload_int(field_id, _type, content, units = None):
        _field_b = bytearray(field_id.encode("utf-8"))

        #Creation of the datatype of content as byte:
        _type_b = bytearray(1)
        _type_b[0]=_type

        #Creation of the content as bytearray (here content is an int) 
        #Need to make if options for different datatypes
        if (_type == 1):
            _content_b = bytearray([0x00])
            _content_b[0] = content
        elif (_type == 2):
            _content_b = content.to_bytes(4,'little')
        elif (_type == 3):
            _content_b = content.to_bytes(8,'little')
        elif (_type == 4):
            _content_b = content.to_bytes(8,'little') #seconds since 1st Jan 1970, held as a long (64-bit C type time_t)
        elif (_type == 5):
            _content_b = bytearray((content + '\0').encode("utf-8"))

        _units_b = bytearray(units.encode("utf-8"))

        payload =  _field_b + _type_b + _content_b + _units_b
        return payload

    def send_data(self, record_id, plate_template_id, control_id, _type, content, units = None):
        field_id = self.get_field_id(record_id, plate_template_id, control_id)
        payload_test = self.get_payload_int(field_id, _type, content, units)
        print(f"PAYLOAD: {payload_test}")
        #Payload_diode init
        payload_diode = bytearray([0x00, 0x00, 0xFF, 0x00]) #red = (0, 0, 255)

        #Diode on
        self.spiToL2S2(99, payload_diode)


        # Send data off
        header, replyPayload = self.spiToL2S2(header=150, payload=payload_test)  # assuming 98 is the correct header for this operation

        if header == b'\x00':
            print("Data sent successfully!")
        else:
            print("Data sending failed!")

        #Payload_diode off
        payload_diode = bytearray([0x00, 0x00, 0x00, 0x00]) #off = (0, 0, 0)

        #Diode off
        self.spiToL2S2(99, payload_diode)
        return 

# Usage:
#l2s2_module = L2S2Module("AndroidAP", "ahmed123")
#l2s2_module.send_data("110", "6e0485b5-cd17-4438-aff8-afe0578ed71f", "4", _type = 5, content = "69", units = "degrees")

