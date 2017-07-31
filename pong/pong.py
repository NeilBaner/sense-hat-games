from sense_hat import SenseHat
from time import sleep
inverted = True
sense = SenseHat()
if inverted:
    sense.set_rotation(180)

y = 4
oy = 4
score = 0
t = 0
ball_position = [3, 3]
ball_velocity = [1, 1]

def draw_ball():
    ball_position[0] += ball_velocity[0]
    ball_position[1] += ball_velocity[1]

    if ball_position[1] == 7 or ball_position[1] == 0:
        ball_velocity[1] = -ball_velocity[1]

    if ball_position[0] == 0:
        sense.show_message("You lost! ", text_colour=(255, 0, 0))
        quit()
        
    if ball_position[0] == 7:
        sense.show_message("You won! ", text_colour=(0, 255, 0))
        quit()

    if ball_position[0] == 1 and y == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[1] = 0
    if ball_position[0] == 1 and y-1 == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        if ball_position[1] != 0:
            ball_velocity[1] = -1
    if ball_position[0] == 1 and y+1 == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        if ball_position[1] != 7:
            ball_velocity[1] = 1

    if ball_position[0] == 6 and oy == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[1] = 0
    if ball_position[0] == 6 and oy-1 == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        if ball_position[1] != 0:
            ball_velocity[1] = -1
    if ball_position[0] == 6 and oy+1 == ball_position[1]:
        ball_velocity[0] = -ball_velocity[0]
        if ball_position[1] != 7:
            ball_velocity[1] = 1
        
    sense.set_pixel(ball_position[0], ball_position[1], 0, 0, 255)
    
def draw_bat():
    sense.set_pixel(0, y, 255, 255, 255)
    sense.set_pixel(0, y-1, 255, 255, 255)
    sense.set_pixel(0, y+1, 255, 255, 255)

    sense.set_pixel(7, oy, 255, 255, 0)
    sense.set_pixel(7, oy-1, 255, 255, 0)
    sense.set_pixel(7, oy+1, 255, 255, 0)

draw_bat()

def move_up(event):
    global y
    if event.action=='pressed' and y>1:
        y-=1

def move_down(event):
    global y
    if event.action=='pressed' and y<6:
        y+=1
if not inverted:
    sense.stick.direction_up = move_up
    sense.stick.direction_down = move_down
else:
    sense.stick.direction_down = move_up
    sense.stick.direction_up = move_down
    
while True:
    global t
    sense.clear(0, 0, 0)
    if ball_position[1]>oy and oy < 6 and t%3 != 0:
        oy+=1
    if ball_position[1]<oy and oy > 1 and t%3 != 0:
        oy-=1
    draw_bat()
    draw_ball()
    t += 1
    sleep(0.25)
    
