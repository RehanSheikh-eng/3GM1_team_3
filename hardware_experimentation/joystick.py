from machine import Pin, ADC

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
        