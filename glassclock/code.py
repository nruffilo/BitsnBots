import time
import board
import neopixel
import math
import busio
import digitalio
import analogio
import adafruit_ds3231
import ulab
import ulab.fft
import ulab.vector

from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.color import WHITE

pixel_pin = board.D11
button = digitalio.DigitalInOut(board.D2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
# The number of NeoPixels
num_pixels = 100

#load the mic
#mic = audiobusio.PDMIn(board.A1, board.A2,sample_rate=16000, bit_depth=16)
#samples_bit = array.array('H', [0] * (fft_size+3))
mic = analogio.AnalogIn(board.A3)


#initialize the i2c
#SCL = A5
#SDA = A4
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(myI2C)

#r = rtc.RTC()
#rtc.datetime = time.struct_time((2021, 02, 20, 17, 50, 15, 0, -1, -1))
print("Current Time: ")
current_time = rtc.datetime
#print(current_time)

#rtc = adafruit_ds3231.DS3231(myI2C)

print("RTC Loaded")

ORDER = neopixel.GRB

grid = [
        [99,98,97,96,95,94,93,92,91,90],
        [80,81,82,83,84,85,86,87,88,89],
        [79,78,77,76,75,74,73,72,71,70],
        [60,61,62,63,64,65,66,67,68,69],
        [59,58,57,56,55,54,53,52,51,50],
        [40,41,42,43,44,45,46,47,48,49],
        [39,38,37,36,35,34,33,32,31,30],
        [20,21,22,23,24,25,26,27,28,29],
        [19,18,17,16,15,14,13,12,11,10],
        [0,1,2,3,4,5,6,7,8,9]
        ]


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
)

#chase = RainbowComet(pixels, speed=0.05, tail_length=12, bounce=True)
chase = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)

#while True:
#    chase.animate()

counter = 0
column = 0
row = 0
sep_on = True
#rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))
mode = 2

def displayClock():
    pixels.fill((0,0,0))
    global sep_on
    global grid
    if sep_on:
        pixels[grid[4][3]] = (255,255,255)
        pixels[grid[4][6]] = (255,255,255)
        sep_on = False
    else:
        pixels[grid[5][3]] = (255,255,255)
        pixels[grid[5][6]] = (255,255,255)
        sep_on = True
        
    t = rtc.datetime
    tens_hour = math.floor(t.tm_hour/10)
    ones_hour = t.tm_hour%10
    
    tens_min = math.floor(t.tm_min/10)
    ones_min = t.tm_min%10
     
    #display on the hour/mins
    for i in range(tens_hour):
        pixels[grid[0][i]] = (255,255,255)
        pixels[grid[1][i]] = (255,255,255)    
    
    for i in range(ones_hour):
        pixels[grid[2][i]] = (255,255,255)
        pixels[grid[3][i]] = (255,255,255)    
    
    for i in range(tens_min):
        pixels[grid[6][i]] = (255,255,255)
        pixels[grid[7][i]] = (255,255,255)    

    for i in range(ones_min):
        pixels[grid[8][i]] = (255,255,255)
        pixels[grid[9][i]] = (255,255,255)    
    
    pixels.show()
    time.sleep(.5)

def displayAudio():
    pixels.fill((0,0,0))
    print(mic.value)
    time.sleep(.01)
    
while True:
    if mode == 1:
        displayClock()
    
    if mode == 2:
        displayAudio()
        
    if button.value == False:
        print("Button pressed")
        mode = mode + 1
        if mode > 2:
            mode = 1
        time.sleep(3)

'''
    counter=counter+1
    pixels.fill((0,0,0))
    column = math.floor(counter/10)
    row = counter%10
    pixels[grid[column][row]] = (255,255,255)
    pixels.show()
    time.sleep(.1)
    if counter >= 99:
        counter = 0
'''
