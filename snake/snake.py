# All the necessary imports - the Sense HAT libraries, the time module 
# (for the sleep function, to add pauses and control the speed of the game)
# and the random module for the randint function (to randomise the apple
# position). 

from sense_hat import SenseHat # For a real Sense HAT plugged into your Pi
#from sense_emu import SenseHat # For the Sense HAT emulator
from time import sleep
from random import randint

sense = SenseHat()

# All the variables used in this program:

score = 0
# The player's score. Gets increased by 1 every time the player successfully
# eats an apple, and is displayed at the end.

inverted = True
# I was programming this with a Raspberry Pi Touchscreen with an incredibly
# short ribbon cable, so I had to use the Sense HAT upside down, and I inverted
# the display and controls for this purpose. Change to False if you use your
# Sense HAT in the correct orientation :)

speed = 0.50
# Not technically speed, but the initial time it takes for the snake to move 1 
# pixel. Gets multiplied by 0.9 every time an apple is eaten, making the snake faster.

snake_pos = [4, 3, 4, 4, 4, 5, 4, 6]
# Possibly the jankiest way to make a snake on the Sense HAT - store the coordinates
# of each segment in a list. I didn't even make two separate lists, or lists 
# within the list. The values are arranged [x, y, x, y...x, y], where the 
# first value is the x-position of the head, the second is the y-position of 
# the head, the third is the x-position of the second segment, the fourth is 
# the y-position of the second segment and so on. Two extra values are appended
# every time an apple is eaten to make the snake longer.

apple_pos = [randint(0, 7), randint(0, 7)]
# A list of 2 randomly generated integers between 0 and 7 (inclusive) for the 
# x and y position of the apple. Gets randomly generated every time the apple is eaten. 

snake_dir = 1
# The direction the snake is facing.
# 1 = up
# 2 = down
# 3 = left
# 4 = right

if inverted:
    sense.set_rotation(180)
    # Inverts the screen of the Sense HAT (but annoyingly enough, not the joystick)

def draw_apple():
    sense.set_pixel(apple_pos[0], apple_pos[1], 255, 0, 0)
    # Lights up a pixel to represent the apple

def draw_snake(t):
    # This function is called with an argument of either 0 or 1. 
    # 0 means just draw the snake normally. 
    # 1 means add a segment
    global snake_pos, snake_dir

    if t==1:
            snake_pos.append(snake_pos[len(snake_pos)-2])
            snake_pos.append(snake_pos[len(snake_pos)-1])
	    # Duplicates the last segment by duplicating the last 2 values on the list.

    for i in range(1, len(snake_pos)-1):
        global snake_pos
        snake_pos[len(snake_pos)-i]=snake_pos[len(snake_pos)-i-2]
	# Move each segment, except the head, to where the segment in front of it was.     
    if snake_dir == 1:
        snake_pos[1]-=1
    elif snake_dir == 2:
        snake_pos[1]+=1
    elif snake_dir == 3:
        snake_pos[0]-=1
    elif snake_dir == 4:
        snake_pos[0]+=1
    # Draw the head of the snake according to the direction of the snake

    if snake_pos[0]>7:
        snake_pos[0]=0
    if snake_pos[0]<0:
        snake_pos[0]=7
    if snake_pos[1]>7:
        snake_pos[1]=0
    if snake_pos[1]<0:
        snake_pos[1]=7
    # If the snake wants to go beyond the screen, make it reappear from the opposite edge.

    for i in range (0, int(len(snake_pos)/2)):
        if i==0:
	    # Draw the snake head as a bright blue
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 255, 255)
        elif i==1:
	    # Draw the first segment as a slightly darker blue
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 127, 255)
        elif i%2 == 0:
	    # Draw all even-numbered segments as an even darker blue
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 63, 127)
        else:
	    # Draw all odd-numbered segments as the darkest blue
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 0, 63)

# Functions to change the direction of the snake
def move_up():
    global snake_dir
    if snake_dir != 2:
        snake_dir = 1
def move_down():
    global snake_dir
    if snake_dir != 1:
        snake_dir = 2
def move_left():
    global snake_dir
    if snake_dir != 4:
        snake_dir = 3
def move_right():
    global snake_dir
    if snake_dir != 3:
        snake_dir = 4

# Mapping the joystick to the functions to change the snake direction, depending on the state
# of 'inverted'
if not inverted:
    sense.stick.direction_up = move_up
    sense.stick.direction_down = move_down
    sense.stick.direction_left = move_left
    sense.stick.direction_right = move_right
else:
    sense.stick.direction_down = move_up
    sense.stick.direction_up = move_down
    sense.stick.direction_right = move_left
    sense.stick.direction_left = move_right

# Main game loop
while True:
    sense.clear()
    
    end = False
    for i in range (1, int(len(snake_pos)/2)-1):
        # Because this loop runs as many times as the snake has segments (to check if the
	# snake is eating itself), the code inside is contained in an if, which evaluates
	# to false once it is determined that the snake has eaten itself.
        if not end:
            if snake_pos[0] == snake_pos[2*i] and snake_pos[1] == snake_pos[2*i+1]:
            # Checks if the snake's head is in the same position as this segment (in this iteration)
            sense.show_message("You scored " + str(score))
		# Shows the score         
                score = 0
                speed = 0.50
                snake_pos = [4, 3, 4, 4, 4, 5, 4, 6]
                apple_pos = [randint(0, 7), randint(0, 7)]
                snake_dir = 1
		# Resets the game variables
                end = True
    draw_apple()
    # Draws the apple
    
    if apple_pos[0]==snake_pos[0] and apple_pos[1] == snake_pos[1]:
    # Checks if the snake head is in the same place as the apple (apple is eaten)
        draw_snake(1)
	# Draws the snake while increasing its length.
        speed = speed * 0.9
	# Reduces the time between redraws, increasing game speed.
        apple_pos[0] = randint(0, 7)
        apple_pos[1] = randint(0, 7)
	# Randomises the apple position
        score += 1
	# Increases the score
    else:
        draw_snake(0)
	# Draws the snake normally.
    sleep(speed)
    # Waits till the next redraw; this time is reduced as more apples are eaten.
