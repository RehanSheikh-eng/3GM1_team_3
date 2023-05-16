from picozero import Switch
import time

class SittingSwitch:
    def __init__(self, pin):
        self.switch = Switch(pin)
        self.duration = 0
    
    def count_duration(self):
        while True:
            if self.switch.is_active:
                self.duration += 1
            time.sleep(1)

'''
# Protocol for uploading to L2S2
minutes = duration // 60

if minutes < 60:
    # upload minutes
else:
    hours = round(minutes / 60, 1)
    # upload hours
'''