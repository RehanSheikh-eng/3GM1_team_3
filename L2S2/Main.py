##Accelerometer init
from Accelerometer import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

##Scale init
from hx711 import HX711
from utime import sleep_us

class Scales(HX711):
    def __init__(self, d_out, pd_sck):
        super(Scales, self).__init__(d_out, pd_sck)
        self.offset = 0

    def reset(self):
        self.power_off()
        self.power_on()

    def tare(self):
        self.offset = self.read()

    def raw_value(self):
        return self.read() - self.offset

    def stable_value(self, reads=10, delay_us=500):
        values = []
        for _ in range(reads):
            values.append(self.raw_value())
            sleep_us(delay_us)
        return self._stabilizer(values)

    @staticmethod
    def _stabilizer(values, deviation=10):
        weights = []
        for prev in values:
            weights.append(sum([1 for current in values if abs(prev - current) / (prev / 100) <= deviation]))
        return sorted(zip(values, weights), key=lambda x: x[1]).pop()[0]

##Light sensor init
from picozero import LED
from machine import ADC,Pin
import utime
adc=ADC(Pin(26))

##LED init
green=LED(15)
red=LED(14)

## Main code
if __name__ == "__main__":
    scales1 = Scales(d_out=5, pd_sck=4)
    scales1.tare()
    scales2 = Scales(d_out=9, pd_sck=8)
    scales2.tare()

## Step counter innit
import peaks
from peakfinding import peak_identifier
from math import sqrt

##Main dataloop
while True:
    intervall=50
    ax=[0]*intervall
    ay=[0]*intervall
    az=[0]*intervall
    #gx=[0]*intervall
    #gy=[0]*intervall
    #gz=[0]*intervall
    total_load= [0]*intervall
    imbalance= [0]*intervall
    for i in range(intervall):
        ax[i]=round(imu.accel.x,2)
        ay[i]=round(imu.accel.y,2)
        az[i]=round(imu.accel.z,2)
        #gx[i]=round(imu.gyro.x)
        #gy[i]=round(imu.gyro.y)
        #gz[i]=round(imu.gyro.z)
        left = scales1.raw_value()
        right = scales2.raw_value()
        total_load[i]=left + right
        #imbalance[i]=(left-right)/(left+right)*100
        ##include LED feedback system
        #print("ax:",ax,"\t","ay:",ay,"\t","az:",az,"\t","gx:",gx,"\t","gy:",gy,"\t","gz:",gz,"\t","tem:",tem," \t","left:",left,"right:",right,"Imbalance:",imbalance,"\t","light:",eclairement,"        ",end="\r")
        
        a=0
        for i in range(1000):
            a+=adc.read_u16()
            mesure=a/1000
        eclairement=round(3.3*2*1000000/(66535*10000)*mesure)
        time.sleep(0.2)
    ## Step counts
        #include find peaks as function, find peaks of az, store in array steps
    step_time=2
    step_height=0.1##not working yet
    steps=peak_identifier(az,step_time, step_height)
    step_count=len(steps)
    ##Crash counts
    crash_height=100 ##???
    #axy=[0]*intervall
    #for i in range(intervall):
     #   axy[i]=sqrt((ax[i])^2+(ay[i])^2)
     
    #crashes=peak_identifier(axy,0, crash_height)  
     
    #crash_count=len(crashes)
    ## Find corresponding loads
    min_load=-500000
    step_loads=peak_identifier(total_load, step_time, min_load)
    
    #Temperature sensor
    tem=round(imu.temperature,2)
    #Light sensor
    
    #if left>-4000 and right >-4000:
     #   green.on()
     #   red.off()
    #else:
     #   red.on()
      #  green.off()
    
    print(steps, step_count, step_loads) 
  
 ##Send data to L2S2


