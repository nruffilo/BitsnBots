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
flameValue = 20
flameDirection = 1

def drawFlame(fv):
    for i in range(pixelCount):
        if (flameColor == 1):
            #pixels[i] = redFlameGradient[random.randint(0,7)]
            pixels[i] = (
                min(255, (i+fv)*10),
                min(255,i+fv*2),
                min(255,i+fv*2)
                )
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

    if HID.value == True and flameColor == 1:
        flameColor = 2
    elif HID.value == False and flameColor == 2:
        flameColor = 1

    drawFlame(flameValue)
    flameValue = flameValue + flameDirection
    if flameValue > 80 or flameValue < 20:
        flameDirection = -flameDirection
    #audio.play(wave)
    #while audio.playing:
    #    pass

    time.sleep(.05)
