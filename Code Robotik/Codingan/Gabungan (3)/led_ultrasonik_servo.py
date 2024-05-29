import RPi.GPIO as GPIO
import time

#ultrasonik
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 4
GPIO_ECHO = 17
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#servo
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)
servo1.start(0)
duty = 2


#led
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

#ultasonik
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

#servo
def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

try:
    while True:
        dist = int(distance())
        
        if dist <= 20:
            setAngle(180)
            GPIO.output(14, GPIO.HIGH)
            time.sleep(1)
        elif dist >= 20:
            setAngle(0)
            GPIO.output(14, GPIO.HIGH)
            GPIO.output(15, GPIO.HIGH)
            time.sleep(1)
        else:
            setAngle(0)
            GPIO.output(14, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
            time.sleep(1)
            
        print(f"Jarak = {dist} cm")
        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()