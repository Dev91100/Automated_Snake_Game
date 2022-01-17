#From Youtube Channel named "Kite"

import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        # print(cur)
 
        #When snake collides with itself
        if len(self.positions) > 2 and new in self.positions[2:]:
            print("self collision")
            self.reset()
        #When snake touches a barrier 
        elif (cur[0] == (screen_width - gridsize) or (cur[0] == 0)) or (cur[1] == (screen_height - gridsize) or (cur[1] == 0)):
            print("touched barrier")
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)

        # while (self.position[0] == 0 or self.position[1] == 0 or self.position[0] == screen_width or self.position[0] == screen_height):
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(1, grid_width-2)*gridsize, random.randint(1, grid_height-2)*gridsize)
        print(self.position)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(84,194,205), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)



    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(20)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score : {0}".format(snake.score), 1, (0,0,0))
        screen.blit(text, (5,10))
        snake.turn(GOAL_BASED_AGENT(snake.get_head_position()))
        pygame.display.update()

# percept => current location of snake
# state => 
# goal => location of food
# rules => x and y coordinates must match
# action => last movement?

def GOAL_BASED_AGENT(current_location):
    goal = food.position
    action = up

    if (goal[0] != current_location[0]):
        if (goal[0] > current_location[0]):
            action = right
        elif (goal[0] < current_location[0]):
            action = left
    # else:
    #     action = random.choice([left, right])

    if (goal[1] != current_location[1]):
        if (goal[1] > current_location[1]):
            action = down
        elif (goal[1] < current_location[1]):
            action = up
    # else:
    #     action = random.choice([up, down])

    return action
    
snake = Snake()
food = Food()
main()