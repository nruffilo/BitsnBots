import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import random

btn = DigitalInOut(board.GP20)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
pixelCount = 16

pixels = neopixel.NeoPixel(board.GP26, pixelCount, brightness = .1, auto_write=False)
print("init the neopixels")
#pixels = neopixel.NeoPixel(board.GP1, 16, brightness = 0.5)
#pixels[0] = (10, 0, 0)
pixels.fill((255,0,255))

MAX_PINK_RED =247
MAX_PINK_GREEN = 74
MAX_PINK_BLUE = 230

def rainbow_cycle(wait, step):
    j = step
    for i in range(pixelCount):
        rc_index = (i * 256 // 10) + j * 5
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)

def circle_chase(wait,step):
    pixels.fill(OFF)
    #steps 0-100 run LEFT, then 101-200 run RIGHT.
    if (step <=100):
        myPercent = max(0,100-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[3] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[2] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        
        myPercent = max(0,120-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[4] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[1] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,140-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[5] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[0] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,160-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[6] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[15] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
      
        myPercent = max(0,180-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[7] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[14] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,200-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[8] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[13] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,220-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[9] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[12] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,240-(step*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[10] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[11] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
    else:
        useStep = step-100
        myPercent = max(0,100-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[10] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[11] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        
        myPercent = max(0,120-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[9] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[12] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,140-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[8] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[13] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,160-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[7] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[14] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
      
        myPercent = max(0,180-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[6] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[15] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,200-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[5] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[0] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,220-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[4] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[1] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)

        myPercent = max(0,240-(useStep*2))/100
        if (myPercent > 1):
            myPercent = 0
        pixels[3] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)
        pixels[2] = (myPercent*MAX_PINK_RED, myPercent*MAX_PINK_GREEN, myPercent*MAX_PINK_BLUE)


    pixels.show()
    time.sleep(wait)

def twinkle():
    pixels.fill(OFF)
    pixels[random.randint(0,pixelCount-1)] = WHITE
    pixels[random.randint(0,pixelCount-1)] = WHITE
    pixels.show()

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

while True:
    if btn.value == False:
        if pressed == False:
            pressed = True
            animationMode = animationMode + 1
            step = 0

            if animationMode > 7:
                animationMode = 1
    else:
        pressed = False
        
    if (animationMode == 1):
        step = step + 1
        if step > 255:
            step = 1
        rainbow_cycle(0.05, step) # Increase the number to slow down the rainbow.
        
    if (animationMode == 2):
        twinkle()
        time.sleep(0.10)
        
    if (animationMode == 3): #chase back-and-forth
        step = step +1
        if step > 200:
            step = 1
        circle_chase(0.05, step)
        
    if (animationMode == 4): #solid low white 20%
        pixels.fill((40,40,40))
        pixels.show()
        time.sleep(0.10)
        
    if (animationMode == 5): #solid low white 40%
        pixels.fill((80,80,80))
        pixels.show()
        time.sleep(0.10)

    if (animationMode == 6): #solid low white 60%
        pixels.fill((120,120,120))
        pixels.show()
        time.sleep(0.10)

    if (animationMode == 7): #solid low white 80%
        pixels.fill((200,200,200))
        pixels.show()
        time.sleep(0.10)
