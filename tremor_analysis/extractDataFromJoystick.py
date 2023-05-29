"""
File created to extract joystick Xpos, Ypos from joystick, creates a text file
"""

from machine import Pin, ADC
import utime

class Joystick:
    def __init__(self, X_pin, Y_pin):
        self.X = ADC(Pin(X_pin))
        self.Y = ADC(Pin(Y_pin))
        self.X_0 = self.X.read_u16()
        self.Y_0 = self.Y.read_u16()
    
    def get_values(self):
        return (
            2 *(self.X.read_u16() - self.X_0) / (2**16 - 1),
            2 * (self.Y.read_u16() - self.X_0) / (2**16 - 1)
        )
    
    def rezero(self):
        self.X_0 = self.X.read_u16()
        self.Y_0 = self.Y.read_u16()

xPos = []
yPos = []
timeStamps = []

Joystick1 = Joystick("GP28","GP27")
i = 0
freq = 100 # Hz
duration = 8 # seconds
startTime = utime.time()
#print(startTime)
for q in range(0,freq*duration):
    #print(endTime)
    utime.sleep(1/100)
    data = Joystick1.get_values()
    xPos.append(data[0])
    yPos.append(data[1])

print("Average Frequency")
print((freq*duration)/(utime.time()-startTime))

if data is not None:
        with open('tremor_simulator_try.txt', 'a') as f:
                for l in range(0,len(xPos)):
                    x_ = xPos[l]
                    y_ = yPos[l]
                    #print(x_,y_)
                    f.write(f"{l},{x_},{y_}\n")

print('done')

