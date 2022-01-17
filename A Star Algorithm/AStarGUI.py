import pygame
import random
import numpy as np

pygame.init()

sx = 480
sy = 480
screen = pygame.display.set_mode((sx, sy))
done = False
x = 0
y = 0
ev = 'r'
fl = 0
clock = pygame.time.Clock()
color = (0, 0, 0) #(Snake Tail Color)
sp = {0: (x, y)}
size = 1
points = 0

# f = open("score.txt", "r")
# max_score = int(f.readline())
# max_sc = max_score
# f.close()


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    cou = 0

    while len(open_list) > 0:
        pygame.event.get()
        cou += 1
        if cou > 1000:
            return -1
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        r1 = random.randrange(255)
        g1 = random.randrange(255)
        b1 = random.randrange(255)
        color = (r1, g1, b1)
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            a1, b1 = node_position
            # Remove below comment to visualise the Path
            # pygame.draw.rect(screen, color, pygame.Rect((a1 - 1) * 20, (b1 - 1) * 20, 5, 5))
            # pygame.display.flip()

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                # H: Manhattan distance to end point
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h
                # Child is already in the open list
                for open_node in open_list:
                    # check if the new path to children is worst or equal
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    # Add the child to the open list
                    open_list.append(child)


# def newScore(sc):
#     f = open("score.txt", "w")
#     f.write(sc)
#     f.close()


pygame.font.init()
myfont = pygame.font.SysFont("monospace",16)


def drawbox(x, y, col=color):
    pygame.draw.rect(screen, col, pygame.Rect(x, y, 20, 20))
    pygame.draw.rect(screen, (84,194,205), pygame.Rect(x, y, 20, 20), 2) #(Block border in snake)


def randomSnack():
    rx1 = random.randrange((sx - 20) / 20)
    ry1 = random.randrange((sy - 20) / 20)
    rx2, ry2 = rx1 * 20, ry1 * 20
    for i in range(0, size):
        a, b = sp[i]
        if a == rx2 and b == ry2:
            return randomSnack()

    return rx1 * 20, ry1 * 20


rx, ry = randomSnack()


def genMatrix(sp):
    mat = np.zeros(shape=(2 + sx // 20, 2 + sy // 20))
    for i in range(0, 2 + sx // 20):
        mat[0, i] = 1
        mat[i, 0] = 1
        mat[1 + sx // 20, i] = 1
        mat[i, 1 + sx // 20] = 1

    for i in sp:
        a, b = sp[i]
        mat[1 + a // 20, 1 + b // 20] = 1
    a, b = sp[0]
    mat[1 + a // 20, 1 + b // 20] = 0
    start = (1 + a // 20, 1 + b // 20)
    end = (1 + rx // 20, 1 + ry // 20)
    path = astar(mat, start, end)
    print(path)
    return path

#Screen color
screen.fill((0, 0, 0))
con = 0
# pygame.mixer.music.load('sound/disfigure_blank.mp3')
# pygame.mixer.music.play(-1)

while not done:
    fl = 0
    # if max_sc < points:
    #     max_sc = points
    screen.blit(pygame.image.load('apple.png'), (rx - 2, ry - 2))
    textsurface = myfont.render("Score : " + str(points), 1, (0, 0, 0))
    # textsurface2 = myfont.render("Max Score : " + str(max_sc), False, (255, 255, 0))
    screen.blit(textsurface, (sx - 160, 30))
    # screen.blit(textsurface2, (sx - 160, 10))
    # pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(rx, ry, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                r1 = random.randrange(255)
                g1 = random.randrange(255)
                b1 = random.randrange(255)
                color = (r1, g1, b1)
            pressed = pygame.key.get_pressed()

    path = genMatrix(sp)
    if path == -1:
        rx, ry = randomSnack()
        path = genMatrix(sp)
        con += 1
        if con > 10:
            # if points > max_score:
            #     newScore(str(points))
            size = 1
            points = 0
            x, y = 0, 0
            sp = {0: (x, y)}
            # pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/lose.wav'))
        continue
    con = 0

    if path is None:
        # if points > max_score:
        #     newScore(str(points))
        size = 1
        points = 0
        x, y = 0, 0
        sp = {0: (x, y)}
        # pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/lose.wav'))
        continue
    for j in path:
        fl = 0
        screen.fill((84,194,205)) #Background color
        # if max_sc < points:
        #     max_sc = points
        screen.blit(pygame.image.load('apple.png'), (rx - 2, ry - 2))
        textsurface = myfont.render("Score : " + str(points), 1, (0, 0, 0))
        # textsurface2 = myfont.render("Max Score : " + str(max_sc), False, (255, 255, 0))
        screen.blit(textsurface, (5, 10))
        # screen.blit(textsurface2, (sx - 160, 10))
        nx, ny = sp[0]
        nx1, ny1 = j
        sp[0] = ((nx1 - 1) * 20, (ny1 - 1) * 20)
        nx1, ny1 = ((nx1 - 1) * 20, (ny1 - 1) * 20)
        sp[1] = (nx, ny)
        for i in range(size - 1, 0, -1):
            nx, ny = sp[i]
            drawbox(nx, ny, color)
            tx, ty = sp[i - 1]
            sp[i] = (tx, ty)
        drawbox(nx1, ny1, (0, 0, 0)) #snake head color
        pygame.display.flip()
        clock.tick(20)
        x, y = sp[0]
        if x == rx and y == ry:
            sp[size] = (rx + 1, ry + 1)
            rx, ry = randomSnack()
            if size < 5000:
                size += 1
            points += 1
            # pygame.mixer.Channel(1).set_volume(0.5)
            # pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/hit.wav'))
    # print(sp)
    screen.blit(pygame.image.load('apple.png'), (rx - 2, ry - 2))