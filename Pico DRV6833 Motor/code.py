from adafruit_motor import motor
import time
import board
import pwmio

pwm_a = pwmio.PWMOut(board.GP0, frequency=50)
pwm_b = pwmio.PWMOut(board.GP2, frequency=50)

stirring = motor.DCMotor(pwm_a, pwm_b)
stirring.throttle = 0

print("motor set up")

while True:
    print("running loop at .3")
    stirring.throttle = 0.3
    time.sleep(1)
    stirring.throttle = 0
    time.sleep(1)
