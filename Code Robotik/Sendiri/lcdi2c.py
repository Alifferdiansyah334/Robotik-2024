# PIN LCD 
# GND -> GND
# VCC -> 5V
# SDA -> GPIO 2
# SCL -> GPIO 3

from RPLCD.i2c import CharLCD
import time

# Set up the LCD using the address found with i2cdetect
lcd = CharLCD('PCF8574', 0x27)

while True:
    # Clear the display
    lcd.clear()

    # Write a string on the first line and move to the next line
    lcd.write_string('LEO ALEXANDER MENCOLOK')
    time.sleep(1)  # Wait for 2 seconds

    # Move to the second line
   # lcd.crlf()  # Carriage Return and Line Feed
    #lcd.write_string('Raspi + LCD')
    #time.sleep(1)  # Wait for 5 seconds

    # Clear the display and show goodbye message
    #lcd.clear()
    #lcd.write_string('Goodbye!')
    #time.sleep(1)

# Turn off the backlight and clear display
lcd.backlight_enabled = False
lcd.close()