import time
import board
import neopixel
import array
import busio
import adafruit_scd4x
import displayio
import digitalio
from adafruit_st7735R import ST7735R
from adafruit_display_text import label
import terminalio
from displayio import FourWire
import os
import ipaddress
import wifi
import socketpool
import random
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.color import PURPLE, AMBER, JADE
import math

BAUDRATE = 24000000

print("Boot start!")
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
print("Connected to wifi!")

displayio.release_displays()
#reset_pin = digitalio.DigitalInOut(board.GP16)

clk_pin = board.GP10
mosi_pin = board.GP11

spi = busio.SPI(clk_pin, mosi_pin, board.GP12)

displayOnOff = digitalio.DigitalInOut(board.GP17)
displayOnOff.direction = digitalio.Direction.OUTPUT

display_bus = displayio.FourWire(spi, command=board.GP6, chip_select=board.GP13, reset=board.GP16)
display = ST7735R(display_bus, width=128, height=128, rotation=180)

splash = displayio.Group()
display.root_group = splash

# Draw a label
text_group = displayio.Group(x=4, y=8)
text = "Booting up...\nI'll be started \nsoon!\n\n   :)"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

pixelCount = 64

pixels = neopixel.NeoPixel(board.GP27, pixelCount, brightness=.1, auto_write=False)

comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=8, bounce=True)
chase = Chase(pixels, speed=0.1, size=4, spacing=6, color=(255, 0, 40))


#displayOnOff.value = False
displayOnOff.value = True

def alertOver2000():
    for i in range(256):
        chase.animate()
        time.sleep(.01)

    pixels.fill((0,0,0))
    pixels.show()

def alertOver1000():
    for i in range(4):
        pixels.fill((255,0,0))
        pixels.show()

        time.sleep(.5)

        pixels.fill((0,0,255))
        pixels.show()

        time.sleep(.5)

    pixels.fill((0,0,0))
    pixels.show()

rings = [
    [27,28,35,36],
    [26,29,34,37,19,20,43,44],
    [25,30,33,38,11,12,51,52,18,21,42,45]
    ]

def drawCO2Levels(co2):

    scaledCo2 = math.floor(co2/4)
    #center -- scaled ~200?
    centerColor = (min(255,scaledCo2),min(max(co2-1000,255),0),max(255-scaledCo2,0))
    for item in rings[0]:
        pixels[item] = centerColor

    #first ring
    ringColor = (0,0,0)
    if (co2 > 500):
        ringColor = (min(255,scaledCo2/2),min(max(co2-1000,255),0),max(255-scaledCo2,0))
    for item in rings[1]:
        pixels[item] = ringColor

    ring2Color = (0,0,0)
    for item in rings[2]:
        pixels[item] = ring2Color

    pixels.show()


def getFace(co2, temp):
    eyes = ""
    nose = ""
    mouth = ""
    eyes_random = random.randint(1,5)
    nose_random = random.randint(1,3)
    mouth_random = random.randint(1,4)
    if (co2 < 1000):
        if (eyes_random == 1):
            eyes = "  O  o  "
        elif (eyes_random == 2):
            eyes = "  O  O  "
        elif (eyes_random == 3):
            eyes = "  o  O  "
        elif (eyes_random == 4):
            eyes = "  o  0  "
        elif (eyes_random == 5):
            eyes = "  o  o  "

        if (nose_random == 1):
            nose = "   ..   "
        elif (nose_random == 2):
            nose = "   __   "
        elif (nose_random == 3):
            nose = "   <>   "

        if (mouth_random == 1):
            mouth = "  \__/  "
        elif (mouth_random == 2):
            mouth = "  \___  "
        elif (mouth_random == 3):
            mouth = "  ___/  "
        elif (mouth_random == 4):
            mouth = "  ---P  "

    else:
        eyes =   "  X  X  "
        nose =   "   ..   "
        mouth =  "  ---p  "

    face = eyes + "\n" + nose + "\n" + mouth
    return face

previous_co2 = 0

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()

        co2 = scd4x.CO2

        if (co2 > 1000 and previous_co2 < 1000):
            alertOver1000()

        if (co2 > 2000 and previous_co2 < 2000):
            alertOver2000()

        if (co2 > 9000 and previous_co2 < 9000):
            print("IT'S OVER 9000!")

        drawCO2Levels(co2)

        pixels.show()
        group = displayio.Group()
        measurement_group = displayio.Group(scale=1, x=6, y=100)
        measurement = "CO2: " + str(co2) + "\nTemp C: " + str(scd4x.temperature*(9/5) + 32)
        measurement_area = label.Label(terminalio.FONT, text=measurement, color=0xFFFFFF)
        measurement_group.append(measurement_area)  # Subgroup for text scaling
        group.append(measurement_group)

        face = getFace(co2, scd4x.temperature)
        face_group = displayio.Group(x=16, y=10)
        face_label = label.Label(terminalio.FONT, text=face, color=0xFFFFFF, scale=2)
        face_group.append(face_label)
        group.append(face_group)
        #make a ascii art of eyes and mouth

        display.root_group = group
        previous_co2 = co2
    time.sleep(1)
