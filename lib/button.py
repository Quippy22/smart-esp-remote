import time

import uasyncio as asyncio
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
        """
        Initialize a Button instance.

        Args:
            pin_num (int): GPIO pin number where the button is connected.
            short_press (coroutine): Async callback for short press.
            long_press (coroutine): Async callback for long press.
            long_press_ms (int): Duration in ms to consider a press as "long".
            debounce_ms (int): Time in ms to ignore repeated triggers (debounce).
            timer_id (int): Timer ID for long press detection.

        The button is hardcoded with PULL-UP
        """

        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)  # Set up the GPIO pin with pull-up
        self.short_press = short_press  # Async function for short press
        self.long_press = long_press  # Async function for long press
        self.long_press_ms = long_press_ms  # Threshold for long press
        self.debounce_ms = debounce_ms  # Debounce time
        self._last_press_time = 0  # Timestamp of last press
        self._timer = Timer(timer_id)  # Timer for long press detection
        self._is_pressed = False  # Track button state

        # Attach an interrupt to handle presses and releases
        self.pin.irq(
            trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._irq_handler
        )

    def _irq_handler(self, pin):
        """
        IRQ handler called on pin change (press or release).

        Args:
            pin (Pin): The Pin object that triggered the interrupt.
        """
        now = time.ticks_ms()  # Current time in milliseconds

        if pin.value() == 0:  # Button pressed (LOW)
            # Ignore if pressed too soon after last press (debounce)
            if time.ticks_diff(now, self._last_press_time) < self.debounce_ms:
                return

            self._last_press_time = now
            self._is_pressed = True

            if self.long_press:
                # Start a one-shot timer to detect long press
                self._timer.init(
                    mode=Timer.ONE_SHOT,
                    period=self.long_press_ms,
                    callback=lambda t: asyncio.create_task(self._handle_long_press()),
                )
            else:
                # No long press, trigger short press immediately
                if self.short_press:
                    asyncio.create_task(
                        # Pass the button instance
                        self.short_press(self)
                    )
        else:
            # Button released (HIGH)
            self._timer.deinit()  # Cancel long press timer
            if self._is_pressed and self.long_press:
                # If released before long press threshold, treat as short press
                if time.ticks_diff(now, self._last_press_time) < self.long_press_ms:
                    if self.short_press:
                        asyncio.create_task(self.short_press(self))
            self._is_pressed = False

    async def _handle_long_press(self):
        """
        Called when long press timer expires.
        Triggers the long_press callback if button is still pressed.
        """
        if self._is_pressed and self.long_press:
            await self.long_press(self)  # Pass the button instance
