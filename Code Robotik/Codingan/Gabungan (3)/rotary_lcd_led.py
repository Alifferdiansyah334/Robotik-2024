# --> Semua import
import RPi.GPIO as GPIO

# --> Import untuk LCD I2C untuk LCD I2C
from RPLCD.i2c import CharLCD
import time

# --> import untuk dht
import board
import adafruit_dht

# --> Alamat untuk LCD
lcd = CharLCD('PCF8574', 0x27)

# --> PIN Untuk Rotary Encoder
CLK_PIN = 18
DT_PIN = 15 
SW_PIN = 14 

# --> Deklarasi untuk variable searah dan berlawanan dengan jarum jam
DIRECTION_CW = 0
DIRECTION_CCW = 1

# --> Variabel counter untuk menghitung nilai rotary
counter = 0
direction = DIRECTION_CW
CLK_state = 0
prev_CLK_state = 0

button_pressed = False
prev_button_state = GPIO.HIGH

# --> Untuk setup pin untuk rotary
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --> Pin LED
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

try:
    while True:

        CLK_state = GPIO.input(CLK_PIN)

        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                direction = DIRECTION_CCW
                if counter <=0:
                    counter = 0
                else:
                    counter -= 1
            else:
                direction = DIRECTION_CW
                if counter >=2:
                    counter=2
                    continue
                else:
                    counter += 1
            if counter == 1:
                lcd.clear()
                GPIO.output(24, GPIO.HIGH)
                GPIO.output(23, GPIO.LOW)
                lcd.write_string(f'Nyala : {counter}')
            elif counter ==2 :
                lcd.clear()
                GPIO.output(24, GPIO.HIGH)
                GPIO.output(23, GPIO.HIGH)
                lcd.write_string(f'Nyala : {counter}')
            else:
                lcd.clear()
                GPIO.output(24, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                lcd.write_string(f'Nyala : {counter}')
            time.sleep(0.5)

        prev_CLK_state = CLK_state

        button_state = GPIO.input(SW_PIN)
        if button_state != prev_button_state:
            time.sleep(0.01)
            if button_state == GPIO.LOW:
                print("The button is pressed")
                counter = 0
                lcd.clear()
                lcd.write_string("Reset")
                GPIO.output(24, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                time.sleep(1)
                lcd.clear()
                lcd.write_string(f"Nyala : {counter}")
                button_pressed = True
            else:
                button_pressed = False

        prev_button_state = button_state

except KeyboardInterrupt:
    GPIO.cleanup()