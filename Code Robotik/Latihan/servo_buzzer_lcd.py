# Import libraries
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

lcd = CharLCD('PCF8574', 0x27)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(22,GPIO.OUT)
servo1 = GPIO.PWM(22,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
#servo1.stop()

duty = 2
counter = 0
ForAngle = 0

# Servo Func
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
    
    if ForAngle <= 180:
        ForAngle += 30
        counter += 1
        lcd.write_string(f'count = {counter}')
        setAngle(ForAngle)
    elif ForAngle >= 180:
        ForAngle = 0
        counter += 1
        lcd.write_string(f'count = {counter}')
        setAngle(ForAngle)
    if counter % 3 == 0:
        GPIO.output(4, GPIO.HIGH)
        print('buzz')
    elif counter %3 != 0:
        GPIO.output(4, GPIO.LOW) 
        print('no buzz')
    
    time.sleep(1)
    print(f'counter = {counter}')
    print(f'Angle = {ForAngle}')      
         
#Clean things up at the end
servo1.stop()
GPIO.cleanup()