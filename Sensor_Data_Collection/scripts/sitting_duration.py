import utime as time
    
def start_sitting_duration(switch, time_step=1, DEBUG=True):
    while True:
        if switch.switch.is_active:
            switch.duration += 1
        
        if DEBUG:
            print(switch.duration)
            if switch.duration == 5:
                print("DEBUB STOP")
                break
        
        time.sleep(time_step)

'''
# Protocol for uploading to L2S2 (once a day)
minutes = duration / 60
hours = round(duration / 60, 1)
push(hours)
'''
