import time

from machine import I2C, Pin, Timer
from ssd1306 import SSD1306_I2C


class Display:
    def __init__(self, sda, scl, width, height):
        self._sda = sda
        self._scl = scl
        self.width = width
        self.height = height

        self._i2c = I2C(sda=Pin(self._sda), scl=Pin(self._scl))
        self.oled = SSD1306_I2C(width, height, self._i2c)

    def clear(self):
        self.oled.fill(0)
        self.oled.show()


class MenuScreen(Display):
    def __init__(self, sda, scl, width, height, line_height=10):
        super().__init__(sda, scl, width, height)

        self._line_height = line_height
        self.lines = width // self._line_height

        # keep the lines centerd on the screen
        self.__offset = (width - self.lines * self._line_height) // 2
        self.y = self.__offset

        self._items = [
            "add",
        ]

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._items.append("add")

    def get_current_item(self):
        return self._items[0]

    def cycle(self, direction):
        if direction == "forward":
            self._items = self._items[1:] + self._items[:1]
        else:
            self._items = self._items[-1:] + self._items[:-1]

    def render(self):
        # render the first line with the indicator
        self.oled.text("> " + self._items[0], 0, self.y)
        self.y += self._line_height

        # then the rest
        for i in range(1, min(len(self._items), self.lines - 1)):
            self.oled.text(self._items[i], 0, self.y)
            self.y += self._line_height

        self.y = self.__offset
        self.oled.show()


class TypingScreen(Display):
    def __init__(self, sda, scl, width, height):
        super().__init__(sda, scl, width, height)
