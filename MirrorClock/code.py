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
from adafruit_led_animation.animation.chase import Chase
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
mic = analogio.AnalogIn(board.A2)


#initialize the i2c
#SCL = A5
#SDA = A4
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(myI2C)

#r = rtc.RTC()
#rtc.datetime = time.struct_time((2023, 12, 21, 13, 42, 15, 3, -1, -1))
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

previousButtonPress = False

chase = Chase(pixels, speed=0.1, color=(255,255,255), size=1, spacing=5)

comet = RainbowComet(pixels, speed=0.05, tail_length=12, bounce=True)
sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)

#while True:
#    chase.animate()

counter = 0
column = 0
row = 0
sep_on = True
#rtc.datetime = time.struct_time((2017,1,9,15,6,0,0,9,-1))
mode = 1

def displayBorder():
    for i in range(10):
        pixels[grid[9][i]] = (20,20,200)
        pixels[grid[8][i]] = (20,20,200)
        pixels[grid[0][i]] = (20,20,200)
        pixels[grid[1][i]] = (20,20,200)
        pixels[grid[i][0]] = (20,20,200)
        pixels[grid[i][9]] = (20,20,200)
        
def displayBinaryClock():
    pixels.fill((0,0,0))
    displayBorder()
    
    # Set up the binary hours/mins
    t = rtc.datetime
    hours = t.tm_hour
    mins = t.tm_min
    seconds = t.tm_sec
    print("Time: ")
    print(hours)
    print(mins)
    print(seconds)
    
    if hours >= 8:
        pixels[grid[2][4]] = (200,20,20)
        pixels[grid[3][4]] = (200,20,20)
        hours = hours - 8
    
    if hours >= 4:
        pixels[grid[2][3]] = (200,20,20)
        pixels[grid[3][3]] = (200,20,20)
        hours = hours - 4
    
    if hours >= 2:
        pixels[grid[2][2]] = (200,20,20)
        pixels[grid[3][2]] = (200,20,20)
        hours = hours - 2
    
    if hours >= 1:
        pixels[grid[2][1]] = (200,20,20)
        pixels[grid[3][1]] = (200,20,20)
        hours = hours - 1
    
    if mins >= 32:
        pixels[grid[4][6]] = (200,20,20)
        pixels[grid[5][6]] = (200,20,20)
        mins = mins - 32

    if mins >= 16:
        pixels[grid[4][5]] = (200,20,20)
        pixels[grid[5][5]] = (200,20,20)
        mins = mins - 16

    if mins >= 8:
        pixels[grid[4][4]] = (200,20,20)
        pixels[grid[5][4]] = (200,20,20)
        mins = mins - 8
    
    if mins >= 4:
        pixels[grid[4][3]] = (200,20,20)
        pixels[grid[5][3]] = (200,20,20)
        mins = mins - 4
    
    if mins >= 2:
        pixels[grid[4][2]] = (200,20,20)
        pixels[grid[5][2]] = (200,20,20)
        mins = mins - 2
    
    if mins >= 1:
        pixels[grid[4][1]] = (200,20,20)
        pixels[grid[5][1]] = (200,20,20)
        mins = mins - 1
    
    if seconds >= 32:
        pixels[grid[6][6]] = (200,20,20)
        pixels[grid[7][6]] = (200,20,20)
        seconds = seconds - 32

    if seconds >= 16:
        pixels[grid[6][5]] = (200,20,20)
        pixels[grid[7][5]] = (200,20,20)
        seconds = seconds - 16

    if seconds >= 8:
        pixels[grid[6][4]] = (200,20,20)
        pixels[grid[7][4]] = (200,20,20)
        seconds = seconds - 8
    
    if seconds >= 4:
        pixels[grid[6][3]] = (200,20,20)
        pixels[grid[7][3]] = (200,20,20)
        seconds = seconds - 4
    
    if seconds >= 2:
        pixels[grid[6][2]] = (200,20,20)
        pixels[grid[7][2]] = (200,20,20)
        seconds = seconds - 2
    
    if seconds >= 1:
        pixels[grid[6][1]] = (200,20,20)
        pixels[grid[7][1]] = (200,20,20)
        seconds = seconds - 1
        
    pixels.show()
    time.sleep(.1);


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
    
    print("Current time: ")
    print(t.tm_hour)
    print(t.tm_min)
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
    time.sleep(.1)

while True:
    if mode == 1:
        displayBinaryClock()
        
    if mode == 2: 
        displayClock()
   
    if mode == 3:
        sparkle.animate()
    
    if mode == 4: 
        comet.animate()

    if mode == 5:
        chase.animate()

    if button.value == False:
        if previousButtonPress == False:
            previousButtonPress = True
            print("Button pressed")
            mode = mode + 1
            if mode > 5:
                mode = 1
            else:
                time.sleep(.5)
        else:
            previousButtonPress = False

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
