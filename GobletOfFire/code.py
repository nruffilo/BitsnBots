import audiocore
import board
import audiobusio
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import time
import random
import math

print("starting")

btn = DigitalInOut(board.GP17)
btn.pull = Pull.UP
pixelCount = 7

HID = DigitalInOut(board.GP22)
HID.direction = Direction.INPUT

pixels = neopixel.NeoPixel(board.GP21, pixelCount, brightness = .6, auto_write=False)

wave_file = open("harrypotter.wav", "rb")
wave = audiocore.WaveFile(wave_file)

#audio = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)

pixels.fill((0,0,0))

flameColor = 1
flameValue = 0
flameArray = [(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0)]

def drawFlame(fv):
    #for i in range(pixelCount):
    if (flameColor == 1):
        small = fv/8
        big = fv*3
        pixels[0] = (max((100 + big)%255,75), small, small)
        pixels[1] = (max((50 + big)%255,75), small, small)
        pixels[2] = (max((120 + big)%255,75), small, small)
        pixels[3] = (max((70 + big)%255,75), small, small)
        pixels[4] = (max((140 + big)%255,75), small, small)
        pixels[5] = (max((20 + big)%255,75), small, small)
        pixels[6] = (max((200 + big)%255,75), small, small)

        #pixels[i] = redFlameGradient[random.randint(0,7)]
    else:
        #pixels[i] = blueFlameGradient[random.randint(0,7)]
        #pixels[i] = redFlameGradient[random.randint(0,7)]
        pixels[i] = (
            min(255, (i+fv)*2),
            min(255,i+fv*2),
            min(255,i+fv*8)
            )
    pixels.show()


while True:
    print("Checking HID...")
    print(HID.value)

    #if HID.value == True and flameColor == 1:
    #    flameColor = 2
    #elif HID.value == False and flameColor == 2:
    #    flameColor = 1

    drawFlame(flameValue)
    flameValue = flameValue + 1
    if flameValue > 200:
        flameValue = 0
    #audio.play(wave)
    #while audio.playing:
    #    pass

    time.sleep(.05)
