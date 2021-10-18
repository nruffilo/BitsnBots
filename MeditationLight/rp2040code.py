import neopixel
import time
import board

breathDirection = 1
brightness = 0.1
maxBrightness = .8
minBrightness = .1
currentColor = 0
nextColor = 0
transitionPercent = 0
counter = 0
# color is set as an array so we can breathe from one color to the next.
color = [[255,255,255], [0,255,120], [0,50,255]]
pixelCount = 7

pixels = neopixel.NeoPixel(board.GP2, pixelCount, brightness = .3, auto_write=False)

while True:
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
