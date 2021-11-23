import neopixel
import time
import board
import random
from digitalio import DigitalInOut, Direction, Pull
from adafruit_led_animation.animation.chase import Chase

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
pixelCount = 8

pixels = neopixel.NeoPixel(board.GP0, pixelCount, brightness = .8, auto_write=False)

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

def talk(pixel):
    pixels.fill((0,0,0))
    pixels.show()
    color = 50
    speed = random.randint(4,15)
    
    while color < 255:
        color = color + speed
        pixels[pixel] = (color,color,color)
        pixels.show()
        time.sleep(0.05)
        
    time.sleep(random.randint(25,100)/100)
    
    while color > 100:
        color = color - speed
        pixels[pixel] = (color,color,color)
        time.sleep(0.05)
    
    
def converse():
    pixels.fill((0,0,0))
    pixels.show()
    #pick a random pixel to start a conversation
    #pick another random pixel to be in the conversation
    #have them talk back and forth, call and response
    #randomly join in 1 or 2 others to chat
    #small chance they all want to sparkle yell at each other
    chatters = [random.randint(0,pixelCount-1)]
    second = random.randint(0,pixelCount-1)
    while (second == chatters[0]):
        second = random.randint(0,pixelCount-1)
    chatters.append(second)
        
    for i in range(4):
        talk(chatters[0])
        talk(chatters[1])
    
    #add another random
    newChatters = random.randint(0,3)
    
    for i in range(newChatters):
        newChatter = random.randint(0,pixelCount-1)
        while newChatter in chatters:
            newChatter = random.randint(0,pixelCount-1)
        chatters.append(newChatter)
    
    lastChatter = 1
    
    for i in range(5):
        nextChatter = chatters[random.randint(0,len(chatters)-1)]
        while nextChatter == lastChatter:
            nextChatter = chatters[random.randint(0,len(chatters)-1)]
        lastChatter = nextChatter
        talk(nextChatter)
        
    #conversation over, lets see if EVERYONE chimes in...
    everyone = random.randint(0,10)
    if everyone == 0:
        for j in range(25):
            twinkle()
            time.sleep(.05)
    
chase = Chase(pixels, speed=0.1, color=(255,255,255), size=1, spacing=5)
counter = 0


while True:
    counter = counter + 1
    if counter > 100:
        animationMode = animationMode + 1
        step = 0
        counter = 0

        if animationMode > 5:
            animationMode = 1

        print("PRESSED!  Animation mode ", animationMode)
    
    if animationMode == 1:
        converse()
        counter = 100
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
        time.sleep(0.05)
