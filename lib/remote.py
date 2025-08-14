import time

import uasyncio as asyncio
from machine import Pin

from button import Button
from database import DeviceDB
from screens import MenuScreen


class Remote:
    def __init__(self, menu, database, button1, button2):
        self.db = database
        self.current_list = "device"

        self.menu = menu
        self.menu.items = self._parse(self.db.devices)

        self.btn1 = button1
        self.btn2 = button2

        # Set buttons to general async handlers
        self.btn1.short_press = self.button_pressed
        self.btn1.long_press = self.button_long_pressed
        self.btn2.short_press = self.button_pressed
        self.btn2.long_press = self.button_long_pressed

    async def button_pressed(self, btn):
        """simple clikcs are used for navigation through the menu or letters(in typing mode)"""
        if btn == self.btn1:
            self.menu.cycle("backward")
            self.menu.render()
        else:
            self.menu.cycle("forward")
            self.menu.render()

    async def button_long_pressed(self, btn):
        """long presses are used for interactions"""
        if btn == self.btn1:
            pass
        else:
            pass

    def _parse(self, lst):
        return [e.rsplit(".", 1)[0] for e in lst]
