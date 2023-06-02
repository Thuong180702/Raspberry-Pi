import lcddriver
import time
import RPi.GPIO as GPIO
import SRF05

GPIO.setmode(GPIO.BCM)

display = lcddriver.lcd()

sensor = SRF05.SRF05(trigger_pin=13, echo_pin=11)


def main():
    try:
        while True:
            distance = sensor.measure()

            display.lcd_clear()
            display.lcd_display_string("Distance:{:.2f}cm".format(distance), 1)
            display.backlight(1)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()
        display.lcd_clear()


if __name__ == "__main__":
    main()
