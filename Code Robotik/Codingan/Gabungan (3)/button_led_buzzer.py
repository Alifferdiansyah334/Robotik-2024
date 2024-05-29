import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(3, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)

counter = 0

while True:
    button_state = GPIO.input(22)
    if button_state == False:
        print('Button Pressed...')
        time.sleep(1)
        counter += 1
        print(f' counter = {counter}')

    if counter == 0:
        GPIO.output(3, GPIO.LOW)
        GPIO.output(2, GPIO.LOW)
    elif counter == 1:
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
    elif counter == 2:
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.HIGH)
        counter = 0
    
