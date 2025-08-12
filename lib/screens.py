import time

from machine import I2C, Pin, Timer

from ssd1306 import SSD1306_I2C

i2c = I2C(sda=Pin(27), scl=Pin(26))
oled = SSD1306_I2C(128, 64, i2c)

