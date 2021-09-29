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

flameColors = [
    (0,0,0),
    (51,0,0), (102,0,0), (153, 0,0), (204,0,0), (255,0,0),
    (255,51,0), (255,102,0), (255,153,0), (255,204,0) , (255,255,0),
    (255,255,51), (255,255,102), (255,255,153), (255,255,204), (255,255,255)
]

pixels.fill((0,0,0))

flameColor = 1
flameValue = 0
flameArray = [(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0),(100,0,0)]

def drawFlame(fv):
    #for i in range(pixelCount):
    if (flameColor == 1):
        for i in range(pixelCount):
            frame = (((i%3)+(i*2)) + fv)%16
            pixels[i] = flameColors[frame]
            #l[T[j+1+j%3]]=HeatColor(qsub8(inoise8((j%3)*20,j*10+a,a/3),abs8((j/3)-2)*51));

    else:
        small = fv/8
        big = fv*3
        pixels[0] = (small, small, max((100 + big)%255,75))
        pixels[1] = (small, small, max((50 + big)%255,75))
        pixels[2] = (small, small, max((120 + big)%255,75))
        pixels[3] = (small, small, max((70 + big)%255,75))
        pixels[4] = (small, small, max((140 + big)%255,75))
        pixels[5] = (small, small, max((20 + big)%255,75))
        pixels[6] = (small, small, max((200 + big)%255,75))
    pixels.show()


while True:
    print("Checking HID...")
    print(HID.value)

#    if HID.value == True and flameColor == 1:
#        flameColor = 2
#    elif HID.value == False and flameColor == 2:
#        flameColor = 1

    drawFlame(flameValue)
    flameValue = flameValue + 1
    if flameValue > 200:
        flameValue = 0
    #audio.play(wave)
    #while audio.playing:
    #    pass

    time.sleep(.05)
