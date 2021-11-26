from adafruit_motor import motor
import time
import board
import pwmio
import neopixel
import random

pwm_a = pwmio.PWMOut(board.GP0, frequency=50)
pwm_b = pwmio.PWMOut(board.GP2, frequency=50)

pixelCount = 12

pixels = neopixel.NeoPixel(board.GP1, pixelCount, brightness = .8, auto_write=False)


stirring = motor.DCMotor(pwm_a, pwm_b)
stirring.throttle = 0

print("motor set up")
stirring.throttle = 1
pixels.fill((0,0,0))

while True:
    pixels.fill((255,255,255))
    
    pixels[random.randint(0,(pixelCount-1))] = (200,50,50)
    pixels[random.randint(0,(pixelCount-1))] = (50,200,50)
    pixels[random.randint(0,(pixelCount-1))] = (50,50,200)
    
    pixels.show()
    time.sleep(.1)
