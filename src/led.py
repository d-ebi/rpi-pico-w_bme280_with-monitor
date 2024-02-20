from machine import Pin, PWM

import time


class LED:
    VERY_HIGH = int(65535 * 1.0) 
    HIGH      = int(65535 * 0.5)
    MEDIUM    = int(65535 * 0.2)
    LOW       = int(65535 * 0.05)
    VERY_LOW  = int(65535 * 0.01)
    OFF       = 0


    def __init__(self, pin):
        self.led = PWM(Pin(pin, Pin.OUT))


    def on(self, brightness):
        self.led.duty_u16(brightness)
        self.led.freq(1000)


    def off(self):
        self.led.duty_u16(LED.OFF)


    def blink(self, pitch, brightness):
        self.led.duty_u16(brightness)
        self.led.freq(1000)
        time.sleep(pitch)
        self.led.duty_u16(0)
        time.sleep(pitch)

