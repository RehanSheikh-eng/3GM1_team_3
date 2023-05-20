from picozero import Switch

class SittingSwitch:
    def __init__(self, pin):
        self.switch = Switch(pin)
        self.duration = 0