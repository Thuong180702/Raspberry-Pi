import RPi.GPIO as GPIO
import time
import smbus

# Địa chỉ I2C của LCD
LCD_ADDRESS = 0x27

# Chân GPIO của cảm biến siêu âm
TRIG = 23
ECHO = 24

# Thiết lập chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Thiết lập giao tiếp I2C với LCD
bus = smbus.SMBus(1)


def read_distance():
    # Gửi xung trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Đọc thời gian trả về của xung echo
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Tính khoảng cách
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


def display_lcd(message):
    # Thiết lập LCD vào chế độ 4 dòng
    bus.write_byte_data(LCD_ADDRESS, 0x00, 0x38)
    time.sleep(0.05)
    # Thiết lập LCD hiển thị và con trỏ về vị trí đầu tiên
    bus.write_byte_data(LCD_ADDRESS, 0x00, 0x0C)
    time.sleep(0.05)
    # Gửi dữ liệu đến LCD
    for char in message:
        bus.write_byte_data(LCD_ADDRESS, 0x40, ord(char))
        time.sleep(0.01)


try:
    while True:
        # Đọc giá trị khoảng cách
        distance = read_distance()
        # Hiển thị giá trị lên LCD
        display_lcd("Distance: {} cm".format(distance))
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
