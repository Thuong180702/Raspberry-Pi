import RPi.GPIO as GPIO
import time


class SRF05:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        self.trigger_time = 0

        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.trigger_pin, GPIO.OUT)

    def measure(self):
        now = self.time_us()

        pause = 50000 - (now - self.trigger_time)
        if pause > 0:
            self.sleep_us(pause)

        self.trigger()

        self.trigger_time = self.time_us()

        if GPIO.wait_for_edge(self.echo_pin, GPIO.RISING, timeout=30) is None:
            return None

        start = self.time_us()

        if GPIO.wait_for_edge(self.echo_pin, GPIO.FALLING, timeout=30) is None:
            return None

        end = self.time_us()

        width = end - start

        if width > 30000:
            return None

        return int(width / 58)

    def trigger(self):
        GPIO.output(self.trigger_pin, 1)
        self.sleep_us(10)
        GPIO.output(self.trigger_pin, 0)

    def time_us(self):
        return int(time.time() * 1000000)

    def sleep_us(self, us):
        time.sleep(us / 1000000.0)
