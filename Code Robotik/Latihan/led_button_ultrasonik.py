# Button Led Ultrasonik
# Kalo button nya di klik counter nambah 1
# Setiap button di klik kelipatan 3 Ultrasonik Nyala
# Kalo Jarak Ultrasonik 7 - 15 Led Nyala

import RPi.GPIO as GPIO
import time

#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

counter = 0

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
        print(f'counter : {counter}')
        time.sleep(1)
    
    if (counter == 0):
        print('Ultrasonik Mati')
        time.sleep(0.5)
    elif(counter %3 == 0):
        dist = int(distance())
        print (f'Jarak : {dist} cm')
        if (dist >= 6 and dist <= 16):
            GPIO.output(2, GPIO.HIGH)
        else :
            GPIO.output(2, GPIO.LOW)
            time.sleep(0.5)
    elif(counter %3 != 0):
        print('Ultrasonik Mati')
        time.sleep(0.5)
        
GPIO.cleanup()
        
    
        
