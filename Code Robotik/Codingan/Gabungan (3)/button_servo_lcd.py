# Import libraries
import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
#servo1.stop()

duty = 2

counter = 0

lcd = CharLCD('PCF8574', 0x27)

def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

while True:

    button_state = GPIO.input(22)

    if button_state == False:
        counter += 1
        print(counter)

    if counter == 0:
        lcd.clear()
        derajat = 25
        setAngle(derajat)
        lcd.write_string(f'derajat : {derajat}')
    elif counter == 1:
        derajat = 50
        setAngle(derajat)
        lcd.write_string(f'derajat : {derajat}')
    elif counter == 2:
        derajat = 180
        setAngle(derajat)
        lcd.write_string(f'derajat : {derajat}')
        counter = 0

#Clean things up at the end
servo1.stop()
GPIO.cleanup()
