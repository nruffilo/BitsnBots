from adafruit_circuitplayground import cp
import time

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

cp.pixels.fill(color[currentColor])

while True:
    cp.pixels.brightness = brightness
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

    cp.pixels.fill(
        (
            color[currentColor][0]*((100-transitionPercent)/100) + color[nextColor][0]*(transitionPercent/100),
            color[currentColor][1]*((100-transitionPercent)/100) + color[nextColor][1]*(transitionPercent/100),
            color[currentColor][2]*((100-transitionPercent)/100) + color[nextColor][2]*(transitionPercent/100),
        )
        )
    cp.pixels.brightness = brightness
    time.sleep(.07)
