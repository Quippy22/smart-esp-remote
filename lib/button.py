import time

from machine import Pin, Timer


class Button:
    def __init__(
        self,
        pin_num,
        short_press=None,
        long_press=None,
        long_press_ms=500,
        debounce_ms=50,
        timer_id=0,
    ):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.short_press = short_press
        self.long_press = long_press
        self.long_press_ms = long_press_ms
        self.debounce_ms = debounce_ms
        self._last_press_time = 0
        self._timer = Timer(timer_id)
        self._is_pressed = False

        self.pin.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._irq_handler
        )

    def _irq_handler(self, pin):
        now = time.ticks_ms()

        # Button pressed (LOW)
        if pin.value() == 0:
            if time.ticks_diff(now, self._last_press_time) < self.debounce_ms:
                return  # Ignore bounce
            self._last_press_time = now
            self._is_pressed = True
            if self.long_press:
                self._timer.init(
                    mode=Timer.ONE_SHOT,
                    period=self.long_press_ms,
                    callback=lambda t: self._handle_long_press(),
                )
            else:
                if self.short_press:
                    self.short_press()

        # Button released (HIGH)
        else:
            self._timer.deinit()
            if self._is_pressed and self.long_press:
                # If released before long press timer expired → short press
                if time.ticks_diff(now, self._last_press_time) < self.long_press_ms:
                    if self.short_press:
                        self.short_press()
            self._is_pressed = False

    def _handle_long_press(self):
        if self._is_pressed and self.long_press:
            self.long_press()
