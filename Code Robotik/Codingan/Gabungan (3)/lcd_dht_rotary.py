import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD
import board
import adafruit_dht

CLK_PIN = 18
DT_PIN = 15 
SW_PIN = 14 

dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)
DIRECTION_CW = 0
DIRECTION_CCW = 1
lcd = CharLCD('PCF8574', 0x27)

counter = 1
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
        # temperature_c = dhtDevice.temperature
        # temperature_f = temperature_c * (9 / 5) + 32
        # humidity = dhtDevice.humidity

        CLK_state = GPIO.input(CLK_PIN)

        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            try:    
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
            except Exception as error:
                continue
            
            print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
                )
            )
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                direction = DIRECTION_CCW
                if counter <=1:
                    counter = 1
                else:
                    counter -= 1
            else:
                direction = DIRECTION_CW
                if counter >=3:
                    counter=3
                    continue
                else:
                    counter += 1

            print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE",
                "- count:", counter)
            

            if counter == 1:
                lcd.clear()
                lcd.write_string(f"Temp F: {temperature_f} F")
            elif counter ==2 :
                lcd.clear()
                lcd.write_string(f"Temp C: {temperature_c} C")
            else:
                lcd.clear()
                lcd.write_string(f"Humidity: {humidity}")
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