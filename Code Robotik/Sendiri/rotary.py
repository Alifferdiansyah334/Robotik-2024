import RPi.GPIO as GPIO
import time

CLK_PIN = 18
DT_PIN = 15 
SW_PIN = 14 

DIRECTION_CW = 0
DIRECTION_CCW = 1

counter = 0
direction = DIRECTION_CW
CLK_state = 0
prev_CLK_state = 0

button_pressed = False
prev_button_state = GPIO.HIGH

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_CLK_state = GPIO.input(CLK_PIN)

try:
    while True:

        CLK_state = GPIO.input(CLK_PIN)

        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                counter -= 1
                direction = DIRECTION_CCW
            else:

                counter += 1
                direction = DIRECTION_CW

            print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE",
                  "- count:", counter)

            time.sleep(0.5)
        prev_CLK_state = CLK_state

        button_state = GPIO.input(SW_PIN)
        if button_state != prev_button_state:
            time.sleep(0.01)
            if button_state == GPIO.LOW:
                print("The button is pressed")
                button_pressed = True
            else:
                button_pressed = False

        prev_button_state = button_state

except KeyboardInterrupt:
    GPIO.cleanup()