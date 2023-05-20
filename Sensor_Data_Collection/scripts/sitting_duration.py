import utime as time
    
def start_sitting_duration(switch, time_step=1, DEBUG=True):
    while True:
        if self.switch.is_active:
            self.duration += 1
        time.sleep(time_step)

'''
# Protocol for uploading to L2S2
minutes = duration // 60

if minutes < 60:
    # upload minutes
else:
    hours = round(minutes / 60, 1)
    # upload hours
'''