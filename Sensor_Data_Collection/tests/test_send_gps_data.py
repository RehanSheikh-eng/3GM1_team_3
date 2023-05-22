from Sensor_Data_Collection.modules.GPSModule import GPSModule
import utime as time

GPS_UART_ID = 1
GPS_UART_BAUD_RATE = 9600
GPS_TX_PIN = 4
GPS_RX_PIN = 5


def spiToL2S2(header, payload):
    global display
    global spi1
    ### Create packet for sending
    # Join together bytearrays
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

    ##### Reads spy response ######
    
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

    ##### Show response on spi #####

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


def main():
    gps_module = GPSModule(uart_id=GPS_UART_ID,
                    baud_rate=GPS_UART_BAUD_RATE,
                    tx_pin_id=GPS_TX_PIN,
                    rx_pin_id=GPS_RX_PIN
                    )
    data_prev = None

    while True:
        data = gps_module.get_data()
        if data is not None:
            print(f"Timestamp: {data['timestamp']}")
            print(f"Latitude: {data['latitude']}")
            print(f"Longitude: {data['longitude']}")

            if data_prev is not None:
                distance = gps_module.get_relative_position(data_prev, data)
                print(f"Relative position in meters: {distance}")

            data_prev = data

        time.sleep(1)  # Sleep for a second to avoid spamming the console

if __name__ == "__main__":
    main()
