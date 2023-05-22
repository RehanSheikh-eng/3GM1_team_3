
import machine
import utime
import time
import ustruct
import sys

IS_PICO_EXPLORER = 0 # Set 0 for Pico Decker and Pico Display 2.0, 1 for Pico Explorer

HAS_PICO_EXPLORER_DISPLAY = 0
HAS_PICO_DISPLAY_2 = 1
L2S2_SPI_BUS = 1


if IS_PICO_EXPLORER:
    HAS_PICO_EXPLORER_DISPLAY = 1
    HAS_PICO_DISPLAY_2 = 0
    L2S2_SPI_BUS = 0


from pimoroni import Button
if HAS_PICO_EXPLORER_DISPLAY:
    from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER, PEN_P4
if HAS_PICO_DISPLAY_2:
    from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
    from pimoroni import RGBLED

from pimoroni_bus import SPIBus




def setDisplaySPI():
    global display
    # We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
    if HAS_PICO_EXPLORER_DISPLAY:
        display = PicoGraphics(display=DISPLAY_PICO_EXPLORER, pen_type=PEN_P4)
    if HAS_PICO_DISPLAY_2:
        display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate = 270)
    #print("Display SPI")
    #print(machine.SPI(0))


def setL2S2SPI():
    global spi1
    if L2S2_SPI_BUS == 0:
        spi1 = machine.SPI(0,
                      baudrate=100000,
                      polarity=0,
                      phase=1,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(18),
                      mosi=machine.Pin(19),
                      miso=machine.Pin(16))
        #print("L2S2 SPI")
        #print(machine.SPI(0))
    if L2S2_SPI_BUS == 1:
        spi1 = machine.SPI(1,
                      baudrate=100000,
                      polarity=0,
                      phase=1,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(10),
                      mosi=machine.Pin(11),
                      miso=machine.Pin(12))
        #print("L2S2 SPI")
        #print(machine.SPI(1))


# Stubs

def myTimeNow():
    return 1234

def CCITT_crc16_false(data: bytes, start, length): # ignoring start and length for now as it wasn't used
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

L2S2_TIMEOUT = 10


# Assign chip select (CS) pin (and start it high)
if L2S2_SPI_BUS == 0:
    spi1cs = machine.Pin(6, machine.Pin.OUT)
if L2S2_SPI_BUS == 1:
    spi1cs = machine.Pin(13, machine.Pin.OUT)

spi1cs.value(1)


setL2S2SPI()
# Needs the following twice to correctly start from cold
setDisplaySPI()
setDisplaySPI()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

if HAS_PICO_DISPLAY_2:
    led = RGBLED(6, 7, 8)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)



    
def spiToL2S2(header, payload):
    global display
    global spi1
    hdr = bytearray(header.to_bytes(1,'little'))
    length = bytearray(len(payload).to_bytes(2,'little'))
    crc = CCITT_crc16_false(hdr + length + payload, 0, int(len(hdr + length + payload)))
    crcarray = bytearray(crc.to_bytes(2,'little'))
    packetToSend = hdr + length + crcarray + payload
    print(myTimeNow(),"Sending ", " ".join('{:02x}'.format(x) for x in packetToSend))
    
    display.set_pen(GREEN)
    if HAS_PICO_DISPLAY_2:
        led.set_rgb(255, 255, 255)
    
    display.text("Sending packet...", 0, 48, 240, 2)
    display.set_pen(MAGENTA)
    display.text(" ".join('{:02x}'.format(x) for x in packetToSend), 0, 64, 240, 1)
    display.update()
    
    # Have to reset the SPI bus if sharing (as with Pico Explorer)
    if IS_PICO_EXPLORER:
        setL2S2SPI()
    
    spi1cs.value(0)
    spi1.write(packetToSend)
    spi1cs.value(1)
    time.sleep_ms(10)
    spi1cs.value(0)
    replyHeader = b'\x00'
    startTime = time.ticks_ms()
    while (replyHeader == b'\x00' and time.ticks_diff(time.ticks_ms(), startTime)<(L2S2_TIMEOUT*1000)):
        spi1cs.value(0) # GSL
        replyHeader = spi1.read(1)
        time.sleep_ms(100)
        if replyHeader == b'\x00':
            spi1cs.value(1) # GSL
    
    if HAS_PICO_DISPLAY_2:
        led.set_rgb(0, 0, 255)
    replyLength = spi1.read(2)
    replyCRC = spi1.read(2)
    replyLengthVal = int.from_bytes(replyLength, 'little')
    if replyLengthVal > 0x400:
        replyLengthVal = 0x400
    replyPayload = spi1.read(replyLengthVal)
    spi1cs.value(1)
    
    # Have to re-set the SPI display if sharing the bus (as with Pico Explorer)
    if IS_PICO_EXPLORER:
        setDisplaySPI()
    
    crc = CCITT_crc16_false(replyHeader + replyLength + replyPayload, 0, int(len(replyHeader + replyLength + replyPayload)))
    print(myTimeNow(),"Reply Header ", " ".join('{:02x}'.format(x) for x in replyHeader))
    print(myTimeNow(),"Reply Length ", " ".join('{:02x}'.format(x) for x in replyLength))
    print(myTimeNow(),"Reply CRC ", " ".join('{:02x}'.format(x) for x in replyCRC))
    print(myTimeNow(),"Reply Payload ", " ".join('{:02x}'.format(x) for x in replyPayload))
    print(myTimeNow(),"Calculated CRC ", " ".join('{:02x}'.format(x) for x in crc.to_bytes(2,'little')))
    
    if crc.to_bytes(2,'little') == replyCRC :
        if HAS_PICO_DISPLAY_2:
            led.set_rgb(0, 255, 0)
        print(myTimeNow(),"Received: Header ", " ".join('{:02x}'.format(x) for x in replyHeader), "Payload ", " ".join('{:02x}'.format(x) for x in replyPayload))
        return replyHeader, replyPayload
    else:
        if HAS_PICO_DISPLAY_2:
            led.set_rgb(255, 0, 0)
        print(myTimeNow(),"L2S2 Timeout or CRC error")
        display.set_pen(RED)
        display.text("Timeout or CRC error", 0, 200, 240, 2)
        display.update()
        time.sleep(1)
        return b'\x00', b'\x00'
    

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()


# set up
clear()
display.set_font("bitmap8")


# packet1 = bytearray([0x96, 0x2a, 0x00, 0xc6, 0xbe, 0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])


lexpayload1 = bytearray([
    # 0x96, 0x63, 0x00, 0x81, 0xa0,                         # Header (generated by the send function here)
    0x62, 0x37, 0x38, 0x62, 0x38, 0x35, 0x63, 0x63,       # Field ID: b78b85cc-c937-48e6-8915-ab0308bbe147|159
    0x2d, 0x63, 0x39, 0x33, 0x37, 0x2d, 0x34, 0x38,
    0x65, 0x36, 0x2d, 0x38, 0x39, 0x31, 0x35, 0x2d,
    0x61, 0x62, 0x30, 0x33, 0x30, 0x38, 0x62, 0x62,
    0x65, 0x31, 0x34, 0x37, 0x7c, 0x31, 0x35, 0x39,
    0x00,
    0x05,                                                # Type
    0x32, 0x30, 0x32, 0x32, 0x2d, 0x30, 0x37, 0x2d,      # Content: 2022-07-06T15:15:57|U|012|A001234|1|Y|2|N|3|Y|0|P1234ABC
    0x30, 0x36, 0x54, 0x31, 0x35, 0x3a, 0x31, 0x35,
    0x3a, 0x35, 0x37, 0x7c, 0x55, 0x7c, 0x30, 0x31,
    0x32, 0x7c, 0x41, 0x30, 0x30, 0x31, 0x32, 0x33,
    0x34, 0x7c, 0x31, 0x7c, 0x59, 0x7c, 0x32, 0x7c,
    0x4e, 0x7c, 0x33, 0x7c, 0x59, 0x7c, 0x30, 0x7c,
    0x50, 0x31, 0x32, 0x33, 0x34, 0x41, 0x42, 0x43,
    0x00
    ])
# payload1 = bytearray([0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])
payload1 = bytearray([0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])
payload2 = bytearray([0x01, 0x00, 0x00, 0x00])
payload3 = bytearray([0x00, 0x01, 0x00, 0x00])
payload4 = bytearray([0x00, 0x00, 0x01, 0x00])

print(myTimeNow(),"Startup")
# Start CS pin high
spi1cs.value(1)
clear()

while True:
    #clear()
    display.set_pen(CYAN)
    display.text("L2S2 SPI TEST", 0, 0, 240, 4)
    display.text("'A' button - Wifi Credentials Packet", 0, 230, 240, 1)
    
    if button_a.read():                                   # if a button press is detected then...
        clear()                                           # clear to black
        display.set_pen(WHITE)                            # change the pen colour
        display.text("Button A pressed", 10, 10, 240, 4)  # display some text on the screen
        display.update()                                  # update the display
        time.sleep(1)                                     # pause for a sec
        clear()                                           # clear to black again
    elif button_b.read():
        clear()
        display.set_pen(CYAN)
        display.text("Button B pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_x.read():
        clear()
        display.set_pen(MAGENTA)
        display.text("Button X pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_y.read():
        clear()
        display.set_pen(YELLOW)
        display.text("Button Y pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    else:
        display.set_pen(YELLOW)
        display.text("Sending test payload", 0, 32, 240, 2)
        display.update()
        #spiToL2S2(150, payload1)
        #spiToL2S2(150, lexpayload1)
        spiToL2S2(99, payload2)
        spiToL2S2(99, payload3)
        spiToL2S2(99, payload4)

    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses








###############################################################################
# Old Main
# packet1 = bytearray([0x96, 0x2a, 0x00, 0xc6, 0xbe, 0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])
payload1 = bytearray([0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])
payload2 = bytearray([0x01, 0x00, 0x00, 0x00])
payload3 = bytearray([0x00, 0x01, 0x00, 0x00])
payload4 = bytearray([0x00, 0x00, 0x01, 0x00])


print(myTimeNow(),"Startup")
# Start CS pin high
spi1cs.value(1)

#replyHeader = bytearray([0x96])
#replyLength = bytearray([0x2a, 0x00])
#replyCRC = bytearray([0xc6, 0xbe])
#replyPayload = bytearray([0x45, 0x36, 0x34, 0x36, 0x38, 0x45, 0x42, 0x35, 0x2d, 0x46, 0x31, 0x30, 0x36, 0x2d, 0x34, 0x41, 0x33, 0x46, 0x2d, 0x38, 0x43, 0x36, 0x32, 0x2d, 0x36, 0x43, 0x36, 0x39, 0x35, 0x39, 0x43, 0x31, 0x35, 0x42, 0x41, 0x36, 0x7c, 0x33, 0x37, 0x00, 0x01, 0x00])
#crc = CCITT_crc16_false(replyHeader + replyLength + replyPayload, 0, int(len(replyHeader + replyLength + replyPayload)))
#print(myTimeNow(),"Reply Header ", " ".join('{:02x}'.format(x) for x in replyHeader))
#print(myTimeNow(),"Reply Length ", " ".join('{:02x}'.format(x) for x in replyLength))
#print(myTimeNow(),"Reply CRC ", " ".join('{:02x}'.format(x) for x in replyCRC))
#print(myTimeNow(),"Reply Payload ", " ".join('{:02x}'.format(x) for x in replyPayload))
#print(myTimeNow(),"Calculated CRC ", " ".join('{:02x}'.format(x) for x in crc.to_bytes(2,'little')))

while (1):
    spiToL2S2(150, payload1)
    spiToL2S2(99, payload2)
    spiToL2S2(99, payload3)
    spiToL2S2(99, payload4)
    



