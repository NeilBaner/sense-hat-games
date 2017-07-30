from sense_hat import SenseHat
from time import sleep
from random import randint

sense = SenseHat()

score = 0
inverted = True
speed = 0.50
snake_pos = [4, 3, 4, 4, 4, 5, 4, 6]
apple_pos = [randint(0, 7), randint(0, 7)]
snake_dir = 1
if inverted:
    sense.set_rotation(180)
def draw_apple():
   sense.set_pixel(apple_pos[0], apple_pos[1], 255, 0, 0)
   
def draw_snake(t):
    global snake_pos, snake_dir
    if t==1:
            snake_pos.append(snake_pos[len(snake_pos)-2])
            snake_pos.append(snake_pos[len(snake_pos)-1])
    for i in range(1, len(snake_pos)-1):
        global snake_pos
        snake_pos[len(snake_pos)-i]=snake_pos[len(snake_pos)-i-2]
    
    if snake_dir == 1:
        snake_pos[1]-=1
    elif snake_dir == 2:
        snake_pos[1]+=1
    elif snake_dir == 3:
        snake_pos[0]-=1
    elif snake_dir == 4:
        snake_pos[0]+=1
    if snake_pos[0]>7:
        snake_pos[0]=0
    if snake_pos[0]<0:
        snake_pos[0]=7
    if snake_pos[1]>7:
        snake_pos[1]=0
    if snake_pos[1]<0:
        snake_pos[1]=7

    for i in range (0, int(len(snake_pos)/2)):
        if i==0:
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 255, 255)
        elif i==1:
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 127, 255)
        elif i%2 == 0:
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 63, 127)
        else:
            sense.set_pixel(snake_pos[2*(i)], snake_pos[2*(i)+1], 0, 0, 63)
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

while True:
    sense.clear()
    
    end = False
    for i in range (1, int(len(snake_pos)/2)-1):
        if not end:
            if snake_pos[0] == snake_pos[2*i] and snake_pos[1] == snake_pos[2*i+1]:
                sense.show_message("You scored " + str(score))            
                score = 0
                speed = 0.50
                snake_pos = [4, 3, 4, 4, 4, 5, 4, 6]
                apple_pos = [randint(0, 7), randint(0, 7)]
                snake_dir = 1
                end = True
    draw_apple()
    if apple_pos[0]==snake_pos[0] and apple_pos[1] == snake_pos[1]:
        draw_snake(1)
        speed = speed * 0.9
        apple_pos[0] = randint(0, 7)
        apple_pos[1] = randint(0, 7)
        score += 1
    else:
        draw_snake(0)
    sleep(speed)
