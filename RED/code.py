import time
from adafruit_crickit import crickit
from adafruit_circuitplayground.express import cpx
import adafruit_hcsr04
import board
import math
import random

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A3, echo_pin=board.A2)

crickit.servo_1.angle = 90
crickit.servo_2.angle = 90

visuals = []

left_wheel = crickit.dc_motor_1
right_wheel = crickit.dc_motor_2

left_wheel_direction = -1
right_wheel_direction = 1

def sayHello():
    cpx.play_tone(160,.3)
    cpx.play_tone(220,.3)
    cpx.play_tone(260,.1)
    cpx.play_tone(320,.1)
    crickit.servo_1.angle = 160
    time.sleep(1)
    crickit.servo_1.angle = 170
    time.sleep(.1)
    crickit.servo_1.angle = 150
    time.sleep(.1)
    crickit.servo_1.angle = 170
    time.sleep(1)
    crickit.servo_1.angle = 90

def spinLeft():
    print("Spinning Left");
    left_wheel.throttle = -.5 * left_wheel_direction
    right_wheel.throttle = .5 * right_wheel_direction
    time.sleep(.5)
    left_wheel.throttle = 0
    right_wheel.throttle = 0
    time.sleep(.1)

def spinRight():
    print("Spinning right");
    left_wheel.throttle = .5 * left_wheel_direction
    right_wheel.throttle = -.5 * right_wheel_direction
    time.sleep(.5)
    left_wheel.throttle = 0
    right_wheel.throttle = 0
    time.sleep(.1)

def doTheMonkey():
    for x in range(5):
        crickit.servo_1.angle = 160
        crickit.servo_2.angle = 160
        time.sleep(.5)
        crickit.servo_1.angle = 20
        crickit.servo_2.angle = 20
        time.sleep(.5)

def Dance():
    spinLeft()
    spinRight()
    spinRight()
    spinLeft()
    doTheMonkey()
    crickit.servo_1.angle = 90
    crickit.servo_2.angle = 90

def HedwigsTheme():
    # E(low) A C B A E(high) D B A C B G (low) Bflat E (low)
    cpx.play_tone(247,.2) # low B
    cpx.play_tone(329,.2) #E (low)
    cpx.play_tone(392,.1) # G (low)
    cpx.play_tone(369,.1) #F sharp (low)

    cpx.play_tone(329,.2) #E (low)
    cpx.play_tone(493,.2) # B
    cpx.play_tone(440,.4) # A
    cpx.play_tone(369,.4) #F sharp (low)

    cpx.play_tone(329,.2) #E (low)
    cpx.play_tone(392,.1) # G (low)
    cpx.play_tone(369,.1) #F sharp (low)
    cpx.play_tone(293,.2) #D (low)
    cpx.play_tone(349,.1) #F (low)
    cpx.play_tone(247,.6) #B (low)

    crickit.servo_2.angle = 20
    cpx.play_file("wingardium.wav")
    crickit.servo_2.angle = 15
    time.sleep(.1)
    crickit.servo_2.angle = 25
    time.sleep(.1)
    crickit.servo_2.angle = 15
    time.sleep(.1)
    crickit.servo_2.angle = 25
    time.sleep(.1)
    crickit.servo_2.angle = 15
    time.sleep(.1)
    crickit.servo_2.angle = 90

#sayHello()

#Dance()
cpx.play_file("hello.wav")
#HedwigsTheme()
action = random.randint(0,3)

while True:
    try:
        #print(sonar.distance)
        distance = sonar.distance
        visuals.append(math.floor(distance))
        if len(visuals) > 10:
            visuals.pop(0)

            highs = 0
            lows = 0
            for measure in visuals:
                if measure < 20:
                    lows = lows + 1
                if measure > 30:
                    highs = highs + 1

            if lows > 2 and highs > 5:
                action = random.randint(0,3)
                if action == 0:
                    sayHello()
                if action == 1:
                    Dance()
                if action == 2:
                    cpx.play_file("doit.wav")
                if action == 3:
                    HedwigsTheme()
                visuals = []
        print(visuals)

    except RuntimeError:
        print("Retrying!")
    time.sleep(0.2)

sonar.deinit()