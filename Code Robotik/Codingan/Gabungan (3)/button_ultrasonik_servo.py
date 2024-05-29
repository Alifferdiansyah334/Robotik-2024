import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

# button state
counter = 0

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)

# Define variable duty
duty = 2
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def setAngle(angle):
    min_duty = 2
    max_duty = 12
    
    duty1 = min_duty + (angle / 180.0) * (max_duty - min_duty)
    
    servo1.ChangeDutyCycle(duty1)

    time.sleep(0.05)
    servo1.ChangeDutyCycle(0)
    time.sleep(0.05)

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
 

while True:

    button_state = GPIO.input(22)

    if button_state == False:
        counter += 1
        print(counter)

    if counter %2 == 1:
        dist = int(distance())
        if(dist >= 180):
            dist = 180
            print (f"Jarak = {dist} cm" )
            setAngle(dist)
            print(type(dist))
            time.sleep(2)
        else:
            print(f'Jarak = {dist} cm ')
            setAngle(dist)
            time.sleep(2)
    else:
        print("Ultrasonik stoppedl")
        time.sleep(1)
servo1.stop()
GPIO.cleanup()