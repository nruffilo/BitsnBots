import board
import neopixel
import time
import random

print("starting?")
outerPixelCount = 60
innerPixelCount = 12

innerPixels = neopixel.NeoPixel(board.GP2, innerPixelCount, brightness = .3, auto_write=False)
outerPixels = neopixel.NeoPixel(board.GP3, outerPixelCount, brightness = .3, auto_write=False, pixel_order=neopixel.RGBW)

print("init the neopixels")
#pixels = neopixel.NeoPixel(board.GP1, 16, brightness = 0.5)
#pixels[0] = (10, 0, 0)
#innerPixels.fill((255,0,255))
#outerPixels.fill((255,0,255,0))

def rainbow_cycle(wait, step):
    j = step
    for i in range(innerPixelCount):
        rc_index = (i * 256 // 10) + j * 5
        innerPixels[i] = wheel(rc_index & 255)
    innerPixels.show()

    for i in range(outerPixelCount):
        rc_index = (i * 256 // 10) + j * 5
        outerPixels[i] = wheel(rc_index & 255)
    outerPixels.show()

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
print("functions done, about to run main loop")

while True:
    print("settings?!")
    innerPixels.fill((0,200,0))
    innerPixels.show()
    outerPixels.fill((0,0,200,0))
    outerPixels.show()
    time.sleep(.5)
    '''
    step = step + 1
    if step > 255:
        step = 1
    rainbow_cycle(0.05, step) # Increase the number to slow down the rainbow.
    '''
