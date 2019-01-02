#Include the necessary Libraries
import board    #Allows the use of Pins and Sensors
import time     #Allows delays and time related functions
import neopixel #Use of neopixel strips
#easy library for accessing the sensors of the CircuitPlaygroundExpress
from adafruit_circuitplayground.express import cpx
from analogio import AnalogIn #Allows use of analog buttons (the 4 buttons)

#initialize the buttons and set their pins
button0 = AnalogIn(board.A1)
button1 = AnalogIn(board.A3)
button2 = AnalogIn(board.A5)
button3 = AnalogIn(board.A7)

#play a sound on startup
cpx.play_file("Coin.wav")

#set our middle pixel strip (the 10 on the CircuitPlayground)
middle_pixels = cpx.pixels
middle_pixels.brightness = .2

#define the number of pixels each strip will have
num_pixels = 6

#set up the pixel strip for the 4 players.
pixels = neopixel.NeoPixel(board.A6,(4*num_pixels), brightness=0.1, auto_write=False)

#load the buttons to an array, one for each player
buttons = [button0, button1, button2, button3]

#predefine some colors
RED = (100, 0, 0)
GREEN = (0, 100, 0)
WHITE = (100, 100, 100)
BLACK = (0, 0, 0)

#some variables for use during the game to determine state
buttons_pressed =[False, False, False, False]
buttons_previous_state = [0, 0, 0, 0]

#the lives a player has
fails = [0, 0, 0, 0]

#the ball location is multi-dimensional array - the first number is the strip 0-3 is the extended lines
#4 is the center.  Things will start in the middle, then hop to a random line.  In fact, the first loop will
#just run lights in the middle while players select if they are playing or not...
ball_location = [4,0]
ball_direction = 1
active_players = [False, False, False, False]
game_state = 0

#set the variable which will determine when the "ball" should move
loop_delay = 20
active_loop = 0

#clear the LED strips
middle_pixels.fill(BLACK)
middle_pixels.show()
pixels.fill(BLACK)
pixels.show()

'''
mapping
Strip/Button 0 - 2
strip/button 1 - 4 -> on the board 1 and 2 got swapped to i swapped the mapping
Strip/Button 2 - 7
strip/button 3 - 9
'''
location_map = [2, 7, 4, 9]
last_strip = -1
pressed_correct = [False, False, False, False]

#function to fill a "strip"  Since all the pixels are technically one strip,
#we cannot use .fill() we have to set just the 6 pixels in the virtual
#strip
def fillStrip(idx, color):
    start_offset = idx*num_pixels
    end_offset = (idx*num_pixels)+num_pixels
    for i in range(start_offset, end_offset):
        pixels[i] = color
    pixels.show()

#set an individual pixel on a virtualized "strip"  This allows the game to maintain
#an array of strips (0, 1, 2, and 3) for each player and keep the code concise.
def setPixel(idx, pixel, color):
    actual_pixel = (idx*num_pixels) + pixel
    pixels[actual_pixel] = color
    pixels.show()

while True:
    #add to the active loop when things will actually happen
    active_loop += 1
    #if our loop is more than the delay, reset it to 0, otherwise our variable could get huge
    if active_loop > loop_delay:
        active_loop = 0
    #determine if the buttons have been pressed or not...
    for index, button in enumerate(buttons):
        if buttons_previous_state[index] < 1000 and button.value > 9000:
            buttons_pressed[index] = True
        else:
            buttons_pressed[index] = False
        buttons_previous_state[index] = button.value

    #if our game state is 0 - if it's waiting for players to join...
    if game_state == 0:
        #if the players have pressed either of the buttons on the Circuit Playground,
        #start the game...
        if cpx.button_a or cpx.button_b:
            game_state = 1 #set the game state to active
            active_loop = 0
            for index, active_player in enumerate(active_players):
                if active_player:
                    fillStrip(index, BLACK)
        #if we are at our loop_delay, set up the next animation.
        if active_loop == loop_delay:
            middle_pixels[ball_location[1]] = BLACK
            ball_location[1] += (1*ball_direction)
            if ball_location[1] > 9:
                ball_location[1] = 0
            middle_pixels[ball_location[1]] = WHITE
        #check to see if any buttons were pressed - if so have user join/leave
        for index, button in enumerate(buttons_pressed) :
            if button:
                active_players[index] = not active_players[index]
                if active_players[index]:
                    fillStrip(index, GREEN)
                else:
                    fillStrip(index, BLACK)

    #check to see if the game state is 1 - which is "active gameplay"
    elif game_state == 1:
        #see if a button was pressed
        for index, button in enumerate(buttons_pressed):
            if button:
                #if the button was pressed, and the ball is in the final position,
                #consider it pressed correctly.
                if index == ball_location[0] and ball_location[1] == (num_pixels-1):
                    pressed_correct[index] = True

        #see if the ball needs to move - only animate on the loop_delay
        if active_loop == loop_delay:
            #if the ball is in the middle section
            if ball_location[0] == 4:
                #check to see if someone has 4 fails, if so, remove them from the game...
                for index, numfails in enumerate(fails):
                    if numfails >= 4:
                        fillStrip(index, RED)
                        active_players[index] = False
                #check to see if only 1 active player has won, if so, set them as green.
                still_alive_count = 0
                for index, player in enumerate(active_players):
                    if player:
                        still_alive_count += 1

                #we only have 1 player, play win sound and end the game
                if still_alive_count == 1:
                    game_state = 2
                    for index, player in enumerate(active_players):
                        if player:
                            fillStrip(index, GREEN)
                            cpx.play_file("Fanfare.wav")

                #last_strip is the last strip the ball was on.  It starts with -1,
                #so only run this is the last strip is NOT -1...
                if last_strip > -1:
                    setPixel(last_strip, 0, BLACK)
                #set the middle strip last pixel to black
                middle_pixels[ball_location[1]] = BLACK
                #move the ball
                ball_location[1] += 1
                #since there are only 10 pixels (0-9) if our pixel location > 9,
                #set it back to 0.
                if ball_location[1] > 9:
                    ball_location[1] = 0
                middle_pixels[ball_location[1]] = WHITE
                #check active players, see if it's on their pixel, if so, send it down
                for index, player in enumerate(active_players):
                    if player and ball_location[1] == location_map[index]:
                        ball_location[0] = index
                        ball_location[1] = -1
            #we are not in the middle, so animate a strip
            else :
                #this happens when the ball is traveling BACK to the middle
                #after bouncing off the end.  So we want to start from the
                #mapped pixel on the middle (so it looks continuous)
                if ball_location[1] == -1:
                    middle_pixels[location_map[ball_location[0]]] = BLACK
                if ball_location[1] >= 0:
                    setPixel(ball_location[0], ball_location[1], BLACK)
                #move the ball based off the direction
                ball_location[1] += (ball_direction*1)

                setPixel(ball_location[0], ball_location[1], WHITE)
                #if we hit the end of the strip, reverse direction
                if ball_location[1] == (num_pixels-1):
                    ball_direction = -1
                #now that the ball is heading back, let's check if the player
                #successfully pressed the button
                if ball_location[1] == (num_pixels-2) and ball_direction == -1:
                    if pressed_correct[ball_location[0]]:
                        cpx.play_file("Coin.wav")
                        pressed_correct[ball_location[0]] = False
                        #if we can, reduce the loop delay and make things faster
                        if loop_delay > 1:
                            loop_delay -= 1
                    else:
                        cpx.play_file("Wild_Eep.wav")
                        fails[ball_location[0]] += 1
                #if the ball is on the first pixel and traveling back to the middle,
                # set the active location as back on the strip
                if ball_location[1] == 0 and ball_direction == -1:
                    ball_location[1] = location_map[ball_location[0]]
                    last_strip = ball_location[0]
                    ball_location[0] = 4
                    ball_direction = 1

    #delay - if you want the game to move faster, you can reduce this sleep, button
    #I recommend setting the loop_delay higher than 20.  The game should start out slow.
    time.sleep(.03)