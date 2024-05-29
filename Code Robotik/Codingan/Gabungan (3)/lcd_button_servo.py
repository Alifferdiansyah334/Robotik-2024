import RPi.GPIO as GPIO
import time

from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(26,GPIO.OUT)
servo1 = GPIO.PWM(26, 50)

servo1.start(0)

duty = 2
degree = 0

def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)

    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

while True:
    lcd.clear()
    button_state = GPIO.input(4)

    if button_state == False:
        if degree < 180:
            lcd.clear()
            degree += 20
            print('Button Pressed...')
            print(f'value servo {degree}')
            lcd.write_string(f'Derajat : {degree}')
            setAngle(degree)
        elif degree == 180:
            lcd.clear()
            degree = 0
            print("Button Pressed")
            print(f'value servo {degree}')
            lcd.write_string(f'Derajat : {degree}')
            setAngle(degree)
            time.sleep(1)
    else:
        lcd.write_string(f'Derajat : {degree}')
