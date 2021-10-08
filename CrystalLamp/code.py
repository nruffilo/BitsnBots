import board
import neopixel
import time
from digitalio import DigitalInOut, Direction, Pull
import analogio
import random
import array
import math
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.color import MAGENTA, ORANGE, TEAL
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.color import WHITE
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import PURPLE
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import AMBER

print("loading")
pixelCount = 51

mic = analogio.AnalogIn(board.GP26)

btn = DigitalInOut(board.GP9)
btn.direction = Direction.INPUT
btn.pull = Pull.UP


#Code for audio
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

PEAK_COLOR = (100, 0, 255)
NUM_SAMPLES = 160

# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))

# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
    return math.sqrt(samples_sum / len(values))

def mean(values):
    return sum(values) / len(values)

def volume_color(volume):
    return 200, volume * (255 // pixelCount), 0

pixels = neopixel.NeoPixel(board.GP3, pixelCount, brightness=.1, auto_write=False)

def soundReactive():
    readMicSamples()
    magnitude = normalized_rms(samples)
    # You might want to print this to see the values.
    # print(magnitude)
    global c, peak

    # Compute scaled logarithmic reading in the range 0 to crownPixelCount
    c = log_scale(constrain(magnitude, input_floor, input_ceiling),
                  input_floor, input_ceiling, 0, pixelCount)

    # Light up pixels that are below the scaled and interpolated magnitude.
    pixels.fill(0)
    for i in range(pixelCount):
        if i < c:
            pixels[i] = volume_color(i)
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, pixelCount - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            pixels[int(peak)] = PEAK_COLOR

    if c >= peak:
        peak = min(c, pixelCount - 1)
    elif peak > 0:
        peak = peak - 1
    pixels.show()

def readMicSamples():
    for i in range(NUM_SAMPLES):
        samples[i] = mic.value


def rainbow_cycle(wait, step):
    j = step
    for i in range(pixelCount):
        rc_index = (i * 256 // 10) + j * 5
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    time.sleep(wait)

def bounceAnimation():
    comet.animate()

def chaseAnimation():
    chase.animate()

def pulseAnimation():
    pulse.animate()

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
chase = Chase(pixels, speed=0.1, color=WHITE, size=3, spacing=6)
comet = Comet(pixels, speed=0.02, color=PURPLE, tail_length=10, bounce=True)
pulse = Pulse(pixels, speed=0.1, color=AMBER, period=3)

samples = array.array('H', [0] * NUM_SAMPLES)
readMicSamples()

input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500
peak = 0

while True:
    '''
    soundReactive()
    time.sleep(.05)
    '''
    if btn.value == False:
        if pressed == False:
            
            pressed = True
            animationMode = animationMode + 1
            step = 0

            if animationMode > 9:
                animationMode = 1
            
            print("PRESSED!  Animation mode ", animationMode)
            time.sleep(0.2)
    else:
        pressed = False
        
    if (animationMode == 1):
        step = step + 1
        if step > 255:
            step = 1
        rainbow_cycle(0.05, step) # Increase the number to slow down the rainbow.
    
    if (animationMode == 2):
        bounceAnimation()
    
    if (animationMode == 3):
        chaseAnimation()
    
    if (animationMode == 4):
        pulseAnimation()
        
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
        
