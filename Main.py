import lcddriver
import time

display = lcddriver.lcd()


# Hàm chạy chương trình
def main():
    display.lcd_display_string("Thuong", 1)
    display.backlight(1)


# Chạy chương trình
if __name__ == "__main__":
    main()
