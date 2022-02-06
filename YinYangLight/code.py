import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import analogio
import random
import array
import math

print("loading")
pixelCount = 14

#code for meditation light
breathDirection = 1
brightness = 0.1
maxBrightness = .5
minBrightness = .1
currentColor = 0
nextColor = 0
transitionPercent = 0
counter = 0
color = [[255,255,255], [0,200,120], [0,50,220]]

def meditation():
    global breathDirection, brightness, maxBrightness, minBrightness, currentColor, nextColor, transitionPercent, counter, color
    pixels.brightness = brightness
    brightness = brightness + breathDirection/100
    transitionPercent = transitionPercent + 100/86
    if (brightness > maxBrightness):
        breathDirection = -1
        
    if (brightness < minBrightness):
        breathDirection = 1
        transitionPercent = 0
        currentColor = currentColor + 1
        nextColor = currentColor + 1
        if (currentColor > 2):
            currentColor = 0
        if (nextColor > 2):
            nextColor = 0

    pixels.fill(
        (
            color[currentColor][0]*((100-transitionPercent)/100) + color[nextColor][0]*(transitionPercent/100),
            color[currentColor][1]*((100-transitionPercent)/100) + color[nextColor][1]*(transitionPercent/100),
            color[currentColor][2]*((100-transitionPercent)/100) + color[nextColor][2]*(transitionPercent/100),
        )
        )
    pixels.brightness = brightness
    pixels.show()
    time.sleep(.07)

btn = DigitalInOut(board.GP6)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

pixels = neopixel.NeoPixel(board.GP0, pixelCount, brightness=.3, auto_write=False)

def rainbow_cycle(wait, step):
    j = step
    for i in range(pixelCount):
        rc_index = (i * 256 // 10) + j * 5
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def runFireAnimation():
    for i in range(pixelCount):
        flamePixels[i][0] = flamePixels[i][0] + flamePixels[i][3]
        flamePixels[i][1] = flamePixels[i][1] + flamePixels[i][3]/5
        flamePixels[i][2] = flamePixels[i][2] + flamePixels[i][3]/5
        #if we are over 255 in the red, then assign a new set of random flicker values
        if (flamePixels[i][0] > 255):
            flamePixels[i][0] = random.randint(25,100)
            flamePixels[i][1] = random.randint(2,50)
            flamePixels[i][2] = random.randint(2,50)
            flamePixels[i][3] = random.randint(1,12)
        pixels[i] = (flamePixels[i][0], flamePixels[i][1], flamePixels[i][2])
    pixels.show()
    

pressed = False
animationMode = 1
step = 0
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

flamePixels = [
[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],
[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5],[100,10,10,5]
]

yinYangSequence = [0,1,2,3,12,11,10,9,8,7,4,5,0]
yinYangFrame = 0

def runYinYang(frame):
    
    if (frame < 39):
        i = frame % 13
        pixels.fill((0,0,0))
        pixels[yinYangSequence[i]] = (200,200,200)
        pixels[yinYangSequence[i-1]] = (125,125,125)
        pixels[yinYangSequence[i-2]] = (75,75,75)
        pixels[yinYangSequence[i-3]] = (25,25,25)
    elif (frame >= 39):
        if frame == 39:       
            pixels.fill((25,25,25));
        if frame == 40:
            pixels.fill((75,75,75));
        if frame == 41:
            pixels.fill((125,125,125));
        if frame == 42:
            pixels.fill((200,200,200));
        if frame == 43:
            pixels.fill((125,125,125));
        if frame == 44:
            pixels.fill((75,75,75));
        if frame == 45:
            pixels.fill((25,25,25));
        if frame == 46:
            pixels.fill((0,0,0));

    pixels.show()
    time.sleep(.1)
    
while True:
    if btn.value == False:
        if pressed == False:

            pressed = True
            animationMode = animationMode + 1
            step = 0

            if animationMode > 10:
                animationMode = 1

            print("PRESSED!  Animation mode ", animationMode)
            time.sleep(0.2)
    else:
        pressed = False

    if (animationMode == 1):
        yinYangFrame = yinYangFrame + 1
        if yinYangFrame > 46:
            yinYangFrame = 0
        runYinYang(yinYangFrame)

    if (animationMode == 2):
        step = step + 1
        if step > 255:
            step = 1
        rainbow_cycle(0.05, step) # Increase the number to slow down the rainbow.
    
    if (animationMode == 3):
        runFireAnimation()
        time.sleep(0.05)

    if (animationMode == 4):
        meditation()

    if (animationMode == 5):
        pixels.fill((60,60,60))
        pixels.show()
        time.sleep(0.1)

    if (animationMode == 6):
        pixels.fill((100,100,100))
        pixels.show()
        time.sleep(0.1)

    if (animationMode == 7):
        pixels.fill((160,160,160))
        pixels.show()
        time.sleep(0.1)

    if (animationMode == 8):
        pixels.fill((240,240,240))
        pixels.show()
        time.sleep(0.1)

    if (animationMode == 9):
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(0.1)
