import microcontroller
import board
import neopixel
import time
import random
from adafruit_circuitplayground import cp
from digitalio import DigitalInOut, Direction, Pull

leftButton = DigitalInOut(board.A2)
leftLED = DigitalInOut(board.A3)
rightButton = DigitalInOut(board.A5)
rightLED = DigitalInOut(board.A4)

leftButton.direction = Direction.INPUT
leftButton.pull = Pull.UP
leftButtonPressed = False
leftButtonPrevious = False

rightButton.direction = Direction.INPUT
rightButton.pull = Pull.UP
rightButtonPressed = False
rightButtonPrevious = False

leftLED.direction = Direction.OUTPUT
leftLED.value = False

rightLED.direction = Direction.OUTPUT
rightLED.value = False

pongGameActive = 1
pongGameWinner = 0

timeItActive = True
timeItWinner = 0
gameGrid = [[],[]]
timeItDrops = 0

mode = 1
gameMode = 0
gameActive = False
modeSelecting = False

pixelCount = 71

globalBrightness = .05
leftPixels = neopixel.NeoPixel(board.A1, pixelCount, brightness=globalBrightness, auto_write=False)
rightPixels = neopixel.NeoPixel(board.A6, pixelCount, brightness=globalBrightness, auto_write=False)
cp.pixels.brightness = globalBrightness
cp.pixels.auto_write = False

ORDER = neopixel.RGB
ballPosition = 0
ballDirection = 1



def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def stars():
    global pixelCount
    leftPixels.fill((0, 0, 0))
    rightPixels.fill((0, 0, 0))
    star = random.randint(-pixelCount+1, pixelCount-1)

    if star > 0:
        leftPixels[star] = (255, 255, 255)
    else:
        rightPixels[-star] = (255, 255, 255)

    leftPixels.show()
    rightPixels.show()


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(pixelCount):
            pixel_index = (i * 256 // pixelCount) + j
            leftPixels[i] = wheel(pixel_index & 255)
            rightPixels[i] = wheel(pixel_index & 255)
        rightPixels.show()
        leftPixels.show()
        time.sleep(wait)


def pingPong():
    global pongGameActive, pongGameWinner
    if not pongGameActive:
        if pongGameWinner == 1:
            leftPixels.fill((200, 0, 0))
            rightPixels.fill((0, 200, 0))
        else:
            leftPixels.fill((0, 200, 0))
            rightPixels.fill((200, 0, 0))
        leftPixels.show()
        rightPixels.show()
        time.sleep(0.3)
    else:
        leftPixels.fill((0, 0, 0))
        rightPixels.fill((0, 0, 0))
        global ballPosition, ballDirection, blueLives, redLives, pongSpeed
        global leftButtonPressed, rightButtonPressed, leftButtonPrevious, rightButtonPrevious

        leftButtonCurrent = leftButton.value
        rightButtonCurrent = rightButton.value

        leftOffset = 0
        rightOffset = 0
        if not leftButtonCurrent and leftButtonPrevious:
            leftButtonPressed = True
            leftOffset = 155
        else:
            leftButtonPressed = False

        if not rightButtonCurrent and rightButtonPrevious:
            rightButtonPressed = True
            rightOffset = 155
        else:
            rightButtonPressed = False

        leftButtonPrevious = leftButtonCurrent
        rightButtonPrevious = rightButtonCurrent

        leftPixels[70] = (100 + leftOffset, 0, 0)
        leftPixels[69] = (100 + leftOffset, 0, 0)
        leftPixels[68] = (100 + leftOffset, 0, 0)
        leftPixels[67] = (100 + leftOffset, 0, 0)
        rightPixels[70] = (0, 0, 100 + rightOffset)
        rightPixels[69] = (0, 0, 100 + rightOffset)
        rightPixels[68] = (0, 0, 100 + rightOffset)
        rightPixels[67] = (0, 0, 100 + rightOffset)

        ballPosition = ballPosition + ballDirection

        # check to see if a button was pressed at the wrong time.
        if rightButtonPressed and ballPosition < 67:
            blueLives = blueLives - 1
            ballDirection = -ballDirection
            ballPosition = 0
            rightPixels.fill((200, 0, 200))
            rightPixels.show()
            time.sleep(2)

        if leftButtonPressed and ballPosition > -67:
            redLives = redLives - 1
            ballDirection = -ballDirection
            ballPosition = 0
            leftPixels.fill((200, 0, 200))
            leftPixels.show()
            time.sleep(2)

        # check to see if things were actually CORRECT
        if rightButtonPressed and ballPosition >= 67:
            ballPosition = 66
            ballDirection = -ballDirection
            pongSpeed = pongSpeed - 0.01
            if pongSpeed < 0.01:
                pongSpeed = 0.01

        if leftButtonPressed and ballPosition <= -67:
            ballPosition = -66
            ballDirection = -ballDirection
            pongSpeed = pongSpeed - 0.01
            if pongSpeed < 0.01:
                pongSpeed = 0.01

        # check to see if there is a winner...
        if (redLives < 0):
            pongGameActive = False
            pongGameWinner = 1

        if (blueLives < 0):
            pongGameActive = False
            pongGameWinner = 2

        if ballPosition > 70:
            blueLives = blueLives - 1
            ballDirection = -ballDirection
            ballPosition = 0
            rightPixels.fill((200, 0, 200))
            rightPixels.show()
            time.sleep(2)
        if ballPosition < -70:
            redLives = redLives - 1
            ballDirection = -ballDirection
            ballPosition = 0
            leftPixels.fill((200, 0, 200))
            leftPixels.show()
            time.sleep(2)

        if ballPosition > 0:
            rightPixels[ballPosition] = (255, 255, 255)

        if ballPosition < 0:
            leftPixels[-ballPosition] = (255, 255, 255)

        rightPixels.show()
        leftPixels.show()
        time.sleep(pongSpeed)

#time it is a simple game where pixels fall from both sides and each side has to press it before it hits the bottom
def timeIt():
    global timeItActive, timeItWinner
    if not timeItActive:
        if timeItWinner == 1:
            leftPixels.fill((200, 0, 0))
            rightPixels.fill((0, 200, 0))
        else:
            leftPixels.fill((0, 200, 0))
            rightPixels.fill((200, 0, 0))
        leftPixels.show()
        rightPixels.show()
        time.sleep(0.3)
    else:
        leftPixels.fill((0, 0, 0))
        rightPixels.fill((0, 0, 0))
        global gameGrid, timeItDrops, blueLives, redLives
        global leftButtonPressed, rightButtonPressed, leftButtonPrevious, rightButtonPrevious

        leftButtonCurrent = leftButton.value
        rightButtonCurrent = rightButton.value

        leftOffset = 0
        rightOffset = 0
        if not leftButtonCurrent and leftButtonPrevious:
            leftButtonPressed = True
            leftOffset = 155
        else:
            leftButtonPressed = False

        if not rightButtonCurrent and rightButtonPrevious:
            rightButtonPressed = True
            rightOffset = 155
        else:
            rightButtonPressed = False

        leftButtonPrevious = leftButtonCurrent
        rightButtonPrevious = rightButtonCurrent

        leftPixels[70] = (100 + leftOffset, 0, 0)
        leftPixels[69] = (100 + leftOffset, 0, 0)
        leftPixels[68] = (100 + leftOffset, 0, 0)
        leftPixels[67] = (100 + leftOffset, 0, 0)
        rightPixels[70] = (0, 0, 100 + rightOffset)
        rightPixels[69] = (0, 0, 100 + rightOffset)
        rightPixels[68] = (0, 0, 100 + rightOffset)
        rightPixels[67] = (0, 0, 100 + rightOffset)

        addBall = random.randint(0,100-timeItDrops)
        if addBall == 0:
            gameGrid[0].append(0)
            gameGrid[1].append(0)

        #move all the balls down
        for i in gameGrid[0]:
            gameGrid[0][i] = gameGrid[0][i] + 1
            gameGrid[1][i] = gameGrid[1][i] + 1
            
            # check to to see if it's beyond the bottom
            if gameGrid[0][i] >= pixelCount:
                gameGrid[0][i] = 0
                blueLives = blueLives - 1
                rightPixels.fill((200,0,0))
            
            if gameGrid[1][i] >= pixelCount:
                gameGrid[1][i] = 0
                redLives = redLives - 1
                leftPixels.fill((200, 0, 0))
                           
            leftPixels[gameGrid[0][i]] = (255, 255, 255)
            rightPixels[gameGrid[0][i]] = (255, 255, 255)
        
        #check to see if button was pressed and there was a pixel in there, if so, push it to top, otherwise lose a life
        if leftButtonPressed:
            foundBall = False
            for i in gameGrid[1]:
                if gameGrid[1][i] >= 67:
                    foundBall = True
                    gameGrid[1][i] = 0
            
            if not foundBall:
                redLives = redLives - 1
                leftPixels.fill((200, 0, 0))
                
        if rightButtonPressed:
            foundBall = False
            for i in gameGrid[0]:
                if gameGrid[0][i] >= 67:
                    foundBall = True
                    gameGrid[0][i] = 0
            
            if not foundBall:
                blueLives = blueLives - 1
                rightPixels.fill((200, 0, 0))
        
        leftPixels.show()
        rightPixels.show()

        time.sleep(.05)


modeButtonPressed = False
pongSpeed = 0.08
redLives = 3
blueLives = 3


while True:
    # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step#
    # print(leftButton.value)
    # print(rightButton.value)
    # print("...")
    leftLED.value = not leftButton.value
    rightLED.value = not rightButton.value

    if cp.button_a and not modeButtonPressed:
        print("changing modes")
        modeButtonPressed = True
        mode = mode + 1
        pongSpeed = 0.1
        redLives = 3
        blueLives = 3
        pongGameActive = 1
        pongGameWinner = 0
        gameMode = 0
        gameActive = False
        if mode >= 4:
            mode = 1

    if modeButtonPressed and not cp.button_a:
        modeButtonPressed = False

    if mode == 1:
        stars()
        time.sleep(.1)

#    if mode == 2:
#        rainbow_cycle()
#        time.sleep(.1)

    # game select
    if mode == 2:
        if not gameActive:
            cp.pixels.fill((0, 0, 0))
            if gameMode == 0:
                cp.pixels[3] = (0, 0, 200)
                cp.pixels[4] = (0, 0, 200)
            elif gameMode == 1:
                cp.pixels[1] = (0, 200, 200)
                cp.pixels[0] = (0, 200, 200)
            elif gameMode == 2:
                cp.pixels[9] = (200, 0, 200)
                cp.pixels[8] = (200, 0, 200)
            elif gameMode == 3:
                cp.pixels[5] = (200, 200, 0)
                cp.pixels[6] = (200, 200, 0)
                
            cp.pixels.show()

            if (not leftButton.value or not rightButton.value) and not modeSelecting:
                gameMode = gameMode + 1
                if gameMode > 3:
                    gameMode = 0
                timeItActive = True
                timeItWinner = 0
                pongGameActive = True
                pongGameWinner = 0
                gameGrid = [[],[]]
                redLives = 3
                blueLives = 3
                timeItDrops = 0
                modeSelecting = True
            elif leftButton.value and rightButton.value and modeSelecting:
                modeSelecting = False

            if cp.button_b:
                gameActive = True

            time.sleep(0.1)
        else:
            if gameMode == 0:
                pingPong()
            if gameMode == 1:
                timeIt()
            if gameMode == 2:
                defender()
            if gameMode == 3:
                beats()



    if mode == 3:
        pingPong()
