from machine import Pin, PWM


class Motor:

    def __init__(self, RPWM_pin, LPWM_pin, PWM_freq = 2000):

        self._forward_pwm = PWM(Pin(RPWM_pin)) # , PWM_freq, 0) #freq=PWM_freq, duty_u16=0)
        
        self._reverse_pwm = PWM(Pin(LPWM_pin)) #, PWM_freq, 0) #freq=PWM_freq, duty_u16=0)

        # self._brake_relay = Pin(brake_pin, Pin.OUT)
        self.disable()

    def enable(self):
        self._enabled = True
        # self._brake_relay.on()

    def disable(self):
        self._enabled = False
        # self._brake_relay.off()
        self._forward_pwm.duty_u16(0)
        self._reverse_pwm.duty_u16(0)

    def set_speed(self, set_value):
        print(set_value)
        if not self._enabled:
            pass
        else:
            pwm_value = int(abs(set_value)*65535)    
            if set_value >= 0:
                self._forward_pwm.duty_u16(pwm_value)
                self._reverse_pwm.duty_u16(0)
            elif set_value < 0:
                self._reverse_pwm.duty_u16(pwm_value)
                self._forward_pwm.duty_u16(0)
            
                