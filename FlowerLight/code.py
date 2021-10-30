import neopixel
import time
import board
import random
from digitalio import DigitalInOut, Direction, Pull
from adafruit_led_animation.animation.chase import Chase

btn = DigitalInOut(board.GP9)
btn.direction = Direction.INPUT
btn.pull = Pull.UP


breathDirection = 1
brightness = 0.1
maxBrightness = .8
minBrightness = .1
currentColor = 0
nextColor = 0
transitionPercent = 0
animationMode = 1
counter = 0
pressed = False
# color is set as an array so we can breathe from one color to the next.
color = [[255,255,255], [0,255,120], [0,50,255]]
pixelCount = 5

pixels = neopixel.NeoPixel(board.GP1, pixelCount, brightness = .3, auto_write=False)

step = 0

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


def rainbow_cycle(wait, step):
    j = step
    for i in range(5):
        rc_index = (i * 256 // 10) + j * 5
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)

def twinkle():
    pixels.fill((0,0,0))
    pixels[random.randint(0,4)] = (255,255,255)
    pixels[random.randint(0,4)] = (255,255,255)

    pixels.show()
    
chase = Chase(pixels, speed=0.1, color=(255,255,255), size=1, spacing=5)

while True:
    if btn.value == False:
        if pressed == False:

            pressed = True
            animationMode = animationMode + 1
            step = 0

            if animationMode > 5:
                animationMode = 1

            print("PRESSED!  Animation mode ", animationMode)
            time.sleep(0.2)
    else:
        pressed = False
    
    if animationMode == 1:
        pixels.brightness = brightness
        brightness = brightness + breathDirection/60
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
    elif animationMode == 2:
        step = step + 1
        if step > 255:
            step = 1
        rainbow_cycle(0.05, step)
    elif animationMode == 3:
        twinkle()
        time.sleep(0.05)
    elif animationMode == 4:
        chase.animate()
    elif animationMode == 5:
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(.05)
