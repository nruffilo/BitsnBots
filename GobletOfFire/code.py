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

wave_file_selected = open("ContestantSelected.wav", "rb")
wave_selected = audiocore.WaveFile(wave_file_selected)

wave_file_approaches = open("ContestantApproaches.wav", "rb")
wave_approaches = audiocore.WaveFile(wave_file_approaches)

wave_file_psst = open("psst.wav", "rb")
wave_psst = audiocore.WaveFile(wave_file_psst)

wave_file_secret = open("secret.wav", "rb")
wave_secret = audiocore.WaveFile(wave_file_secret)

audio = audiobusio.I2SOut(bit_clock=board.GP10, word_select=board.GP11, data=board.GP9)

flameColorsRed = [
    (0,0,0),
    (51,0,0), (102,0,0), (153, 0,0), (204,0,0), (255,0,0),
    (255,51,0), (255,102,0), (255,153,0), (255,204,0) , (255,255,0),
    (255,255,51), (255,255,102), (255,255,153), (255,255,204), (255,255,255)
]

flameColorsBlue = [
    (0,0,0),
    (0,0,51), (0,0,102), (0,0,153), (0,0,204), (0,0,255),
    (0,51,255), (0, 102,255), (0,153,255), (0,204,255) , (0,255,255),
    (51,255,255), (102,255,255), (153,255,255), (204,255,255), (255,255,255)
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
            pixels[i] = flameColorsRed[frame]
    else:
        for i in range(pixelCount):
            frame = (((i%3)+(i*2)) + fv)%16
            pixels[i] = flameColorsBlue[frame]
    pixels.show()

delayCounter = 600

while True:
    #if HID.value == True and flameColor == 1 and delayCounter >=600:
    if HID.value == True and flameColor == 1 and delayCounter >=300:
        flameColor = 2
        delayCounter = 0
        pixels.fill((0,0,200))
        pixels.show()
        audiofiletoplay = random.randint(0,20)
        if audiofiletoplay == 0:
            audio.play(wave_psst)
            time.sleep(5)
        elif audiofiletoplay == 1:
            audio.play(wave_secret)
            time.sleep(5)
        else:
            audio.play(wave_approaches)
            time.sleep(5)

    elif HID.value == False and flameColor == 2 and delayCounter > 100:
        flameColor = 1
        delayCounter = 0

    #if the button is pressed
    if (btn.value == False):
        flameColor = 2
        delayCounter = 0
        audio.play(wave_selected)
        time.sleep(4)

    drawFlame(flameValue)
    flameValue = flameValue + 1
    if flameValue > 200:
        flameValue = 0

    time.sleep(.05)
    if (delayCounter < 700):
        delayCounter = delayCounter + 1
       
