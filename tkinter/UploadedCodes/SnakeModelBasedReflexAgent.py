# ************************************
# Python Snake(From Bro Code)
# ************************************
from tkinter import *
import random
import time

GAME_WIDTH = 1300
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 5
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

#Switch for automated random movement
#automation_controls = "on" #on or off


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            #Spawns the snake at (0,0)
            # self.coordinates.append([0, 0])

            #Spawns the snake at the center
            self.coordinates.append([GAME_WIDTH / 2, GAME_HEIGHT / 2])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):

    snake_control(snake)

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction
    global previous_direction

    #Collect Previous Direction Info Before It Changes To A New One
    previous_direction = direction
    # print("previous direction is " + previous_direction)

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    counter = 0
    for body_part in snake.coordinates[1:]:
        counter += 1
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    

def snake_control(snake):
    collision_status = check_collisions(snake)
    if (collision_status != True):
        random_direction()


proposed_direction = 'down'

def propose_a_direction():
    global proposed_direction

    Random_No = random.randint(1, 4)
    if Random_No == 1 and direction != 'right':
        proposed_direction = 'left'
    elif Random_No == 2 and direction != 'left':
        proposed_direction = 'right' 
    elif Random_No == 3 and direction != 'down':
        proposed_direction = 'up'
    elif Random_No == 4 and direction != 'up':
        proposed_direction = 'down'
    else:
        propose_a_direction()
    return proposed_direction

def same_as_previous_direction(past_direction):
    xa = propose_a_direction()
    # print("proposed direction while comparing is " + xa + " while previous direction is " + past_direction)
    if past_direction == xa:
        # print("comparison returned true")
        return True
    else:
        # print("comparison returned false")
        return False


# Suggest a Direction ✔
# Check the Direction ✔
# Move the snake ✔
# update the previous direction ✔

previous_direction = 'down'

def random_direction():   
    # global previous_direction

    # print(same_as_previous_direction())
    while (same_as_previous_direction(previous_direction) == True):

        propose_a_direction()
        # print("distinct new direction is")
        # print(distinct_new_direction)

    # print("proposed direction is " + proposed_direction)
    change_direction(proposed_direction)
    # print("changed direction to " + proposed_direction)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# window.bind('<Left>', lambda event: change_direction('left'))
# window.bind('<Right>', lambda event: change_direction('right'))
# window.bind('<Up>', lambda event: change_direction('up'))
# window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()