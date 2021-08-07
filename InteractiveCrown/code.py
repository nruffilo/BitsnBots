# Circuit Playground NeoPixel
# Huge thank you to https://learn.adafruit.com and Core Electronics (https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa2J5Ym03ZE5BREwwX0ZBMUVOX0x0TkdYNDlVd3xBQ3Jtc0trZjdtUWpBbFhUeG5POFZackhFRVVOc1pSTm12dkpNOFVwWFo5XzFNZ2RXcklvU21FTldKUjBHSlU4dVJNaE0wYlVIX1k5bXQ0UFRQMXFtODJob1VyOGtZaXJJaWVDMXZnY01pRVloUTMtYmlWd1ptZw&q=https%3A%2F%2Fcore-electronics.com.au%2Ftutorials%2Fsound-reactive-lights-circuitpython-circuit-playground-express-tutorial.html) for their tutorial on sound reactive.
import time
import board
import neopixel
import random
import array
import math
import audiobusio
from digitalio import DigitalInOut, Direction, Pull
import touchio

touchPad1 = touchio.TouchIn(board.A4)
touchPad2 = touchio.TouchIn(board.A5)

btn = DigitalInOut(board.BUTTON_B)
btn.direction = Direction.INPUT
btn.pull = Pull.DOWN

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
    return 200, volume * (255 // crownPixelCount), 0

#pixels = cp.pixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.4, auto_write=False)
pixels.brightness = .4
pixels.auto_write = False
crown = neopixel.NeoPixel(board.A1, 20, brightness=.4, auto_write=False)
crownPixelCount = 20
# choose which demos to play
# 1 means play, 0 means don't!
color_chase_demo = 1
flash_demo = 1
rainbow_demo = 1
rainbow_cycle_demo = 1
pressed = False

animationMode = 1
step = 0
mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)
#mic = cp.mic
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))
input_floor = normalized_rms(samples) + 10
input_ceiling = input_floor + 500
peak = 0

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


def color_chase(color, wait):
    for i in range(10):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    for i in range(crownPixelCount):
        crown[i] = color
        time.sleep(wait)
        crown.show()
    time.sleep(0.5)


def rainbow_cycle(wait, step):
    j = step
    for i in range(10):
        rc_index = (i * 256 // 10) + j * 5
        pixels[i] = wheel(rc_index & 255)
    pixels.show()
    for i in range(crownPixelCount):
        rc_index = (i * 256 // crownPixelCount) + j * 5
        crown[i] = wheel(rc_index & 255)
    crown.show()
    time.sleep(wait)

def twinkle():
    pixels.fill(OFF)
    crown.fill(OFF)
    pixels[random.randint(0,9)] = WHITE
    pixels[random.randint(0,9)] = WHITE

    crown[random.randint(0,19)] = WHITE
    crown[random.randint(0,19)] = WHITE
    crown[random.randint(0,19)] = WHITE

    pixels.show()
    crown.show()

def soundReactive():
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    # You might want to print this to see the values.
    # print(magnitude)
    global c, peak

    # Compute scaled logarithmic reading in the range 0 to crownPixelCount
    c = log_scale(constrain(magnitude, input_floor, input_ceiling),
                  input_floor, input_ceiling, 0, crownPixelCount)

    # Light up pixels that are below the scaled and interpolated magnitude.
    crown.fill(0)
    pixels.fill(0)
    ''' THIS IS THE ORIGINAL ASSUMING A STRIP, the crown is bottom/top
    for i in range(crownPixelCount):
        if i < c:
            crown[i] = volume_color(i)
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, crownPixelCount - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            crown[int(peak)] = PEAK_COLOR
    '''
    for i in range(14):
        crown[i] = volume_color(c)

    if c > 10:
        for i in range(6):
            crown[14+i] = volume_color(c-14)

    if c >= peak:
        peak = min(c, crownPixelCount - 1)
    elif peak > 0:
        peak = peak - 1
    crown.show()

    for i in range(10):
        if i < c:
            pixels[i] = volume_color(i)
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, 10 - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            pixels[int(peak)] = PEAK_COLOR

    pixels.show()
    crown.show()

def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        for i in range(crownPixelCount):
            idx = int(i + j)
            crown[i] = wheel(idx & 255)
        crown.show()

        time.sleep(wait)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)
crown.fill(OFF)
crown.show()
pixels.fill(OFF)
pixels.show()
peak = 0
while True:
    '''
    if color_chase_demo:
        color_chase(RED, 0.1)  # Increase the number to slow down the color chase
        color_chase(YELLOW, 0.1)
        color_chase(GREEN, 0.1)
        color_chase(CYAN, 0.1)
        color_chase(BLUE, 0.1)
        color_chase(PURPLE, 0.1)
        color_chase(OFF, 0.1)
    if flash_demo:
        pixels.fill(RED)
        pixels.show()
        # Increase or decrease to change the speed of the solid color change.
        time.sleep(1)
        pixels.fill(GREEN)
        pixels.show()
        time.sleep(1)
        pixels.fill(BLUE)
        pixels.show()
        time.sleep(1)
        pixels.fill(WHITE)
        pixels.show()
        time.sleep(1)
    '''

    if touchPad1.value or touchPad2.value:
        if pressed == False:
            pressed = True
            animationMode = animationMode + 1
            step = 0

            if animationMode > 4:
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

    if (animationMode == 3):
        soundReactive()
        time.sleep(0.05)

    if (animationMode == 4):
        crown.fill(0)
        pixels.fill(0)
        crown.show()
        pixels.show()
        time.sleep(.25)


    '''
    if rainbow_demo:
        rainbow(0.05)  # Increase the number to slow down the rainbow.
    '''
