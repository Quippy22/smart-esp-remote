import time

from machine import I2C, Pin, Timer

from ssd1306 import SSD1306_I2C



class Display:
    def __init__(self, sda, scl, width, height):
        self.sda = sda
        self.scl = scl
        self.width = width
        self.height = height

        self.i2c = I2C(sda=Pin(self.sda), scl=Pin(self.scl))
        self.oled = SSD1306_I2C(width, height, self.i2c)
            
    def clear(self):
        self.oled.fill(0)
        self.oled.show()

class MenuScreen(Display):
    def __init__(self, sda, scl, width, height):
        super().__init__(sda, scl, width, height)
        pass

class TypingScreen(Display):
    def __init__(self, sda, scl, width, height):
        super().__init__(sda, scl, width, height)
        pass
