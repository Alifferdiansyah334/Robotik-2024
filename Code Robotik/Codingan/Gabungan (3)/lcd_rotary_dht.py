# --> Semua import
import RPi.GPIO as GPIO

# --> Import untuk LCD I2C untuk LCD I2C
from RPLCD.i2c import CharLCD
import time

# --> import untuk dht
import board
import adafruit_dht

# --> inisialisasi dht
dhtDevice = adafruit_dht.DHT22(board.D22, use_pulseio=False)

# --> Alamat untuk LCD
lcd = CharLCD('PCF8574', 0x27)

# --> PIN Untuk Rotary Encoder
CLK_PIN = 18
DT_PIN = 15 
SW_PIN = 14 

# --> Deklarasi untuk variable searah dan berlawanan dengan jarum jam
DIRECTION_CW = 0 
DIRECTION_CCW = 1

# --> Variabel counter untuk menghitung nilai rotary
counter = 1
direction = DIRECTION_CW
CLK_state = 0
prev_CLK_state = 0

button_pressed = False
prev_button_state = GPIO.HIGH

# --> Untuk setup pin untuk rotary
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK_PIN, GPIO.IN)
GPIO.setup(DT_PIN, GPIO.IN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_CLK_state = GPIO.input(CLK_PIN)

try:
    while True:
        
        try:
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
    
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)

        lcd.clear()

        CLK_state = GPIO.input(CLK_PIN)

        if CLK_state != prev_CLK_state and CLK_state == GPIO.HIGH:
            if GPIO.input(DT_PIN) == GPIO.HIGH:
                if (counter > 1):
                    counter -= 1
                    direction = DIRECTION_CCW
                elif (counter == 1) or (counter == 1):
                    counter = 1
                    direction = DIRECTION_CCW
                else: 
                    counter = 1
                    direction = DIRECTION_CCW
            elif GPIO.input(CLK_PIN) == GPIO.HIGH:
                if (counter >= 2)  or (counter == 3):
                    counter = 3
                    direction = DIRECTION_CW
                else:
                    counter += 1
                    direction = DIRECTION_CW
                
            print("Rotary Encoder:: direction:", "CLOCKWISE" if direction == DIRECTION_CW else "ANTICLOCKWISE",
                  "- count:", counter)

        time.sleep(0.5)
        
        prev_CLK_state = CLK_state

        if(counter == 1) :
            lcd.write_string(f"Temp F: {temperature_f} F")
        elif(counter == 2):
            lcd.clear()
            lcd.write_string(f"Temp C: {temperature_c} C")
        else:
            lcd.clear()
            lcd.write_string(f"Humidity: {humidity}")

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