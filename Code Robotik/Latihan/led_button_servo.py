# Led Button Servo
# Setiap Di klik Counter nambah 1
# Counter 1 Derajat Servo 45
# Counter 2 Derajat Servo 90
# Counter 3 Derajat Servo 135
# Counter 4 Derajat Servo 180 
# Counter 5 Derajat Servo 0
# Kalo Derajat Servo 180 Led Nyala

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(4, GPIO.OUT)

GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50) 

servo1.start(0)

duty = 2

counter = 0

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
        print(f'counter : {counter}')
        time.sleep(1)
    
    if (counter == 1):
        setAngle(45)
    elif (counter == 2): 
        setAngle(90)
    elif (counter == 3): 
        setAngle(135)
    elif (counter == 4):
        setAngle(180)
        GPIO.output(4, GPIO.HIGH)
    elif (counter == 5):
        setAngle(0)
        counter = 0
    else:
        GPIO.output(4, GPIO.LOW) 
servo1.stop()
GPIO.cleanup()
