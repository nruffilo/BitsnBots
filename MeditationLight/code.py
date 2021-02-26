from adafruit_circuitplayground import cp
import time

breathDirection = 1
brightness = 0.1
maxBrightness = .8
minBrightness = .1
currentColor = 0
color = [(255,255,255), (0,255,120), (0,50,255)]

cp.pixels.fill(color[currentColor])

while True:
    cp.pixels.brightness = brightness
    brightness = brightness + breathDirection/60

    if (brightness > maxBrightness):
        breathDirection = -1

    if (brightness < minBrightness):
        breathDirection = 1
        currentColor = currentColor + 1
        if (currentColor > 2):
            currentColor = 0

    cp.pixels.fill(color[currentColor])
    cp.pixels.brightness = brightness
    time.sleep(.07)
