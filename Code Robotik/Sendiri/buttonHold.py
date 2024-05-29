import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    button_state = GPIO.input(22)
    if button_state == False:
        print('Button Pressed...')
        time.sleep(1)
