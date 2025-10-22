import pygame
from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
from numpy import sqrt

# Initialize Pygame
init()

# Game settings
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 25
rows = 25

width = 600
height = 600
wr = width / cols
hr = height / rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("Snake Game with A* Algorithm")
clock = time.Clock()
done = False

class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = None
        self.obstacle = False
        if randint(1, 101) < 3:  # 3% chance of obstacle
            self.obstacle = True

    def show(self, color):
        draw.rect(screen, color, [self.x * hr + 2, self.y * wr + 2, hr - 4, wr - 4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# A* pathfinding algorithm
def getpath(food, snake):
    food.camefrom = None
    for s in snake:
        s.camefrom = None
    openset = [snake[-1]]
    closedset = []
    dir_array = []

    while openset:
        current = min(openset, key=lambda x: x.f)
        openset.remove(current)
        closedset.append(current)

        # If the goal has been reached
        if current == food:
            break

        for neighbor in current.neighbors:
            if neighbor in closedset or neighbor.obstacle or neighbor in snake:
                continue

            temp_g = current.g + 1
            if neighbor in openset:
                if temp_g < neighbor.g:
                    neighbor.g = temp_g
            else:
                neighbor.g = temp_g
                openset.append(neighbor)

            neighbor.h = sqrt((neighbor.x - food.x) ** 2 + (neighbor.y - food.y) ** 2)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.camefrom = current

    # No path found
    if current != food:
        return []

    # Reconstruct path
    while current.camefrom:
        if current.x == current.camefrom.x and current.y < current.camefrom.y:
            dir_array.append(2)  # Up
        elif current.x == current.camefrom.x and current.y > current.camefrom.y:
            dir_array.append(0)  # Down
        elif current.x < current.camefrom.x and current.y == current.camefrom.y:
            dir_array.append(3)  # Left
        elif current.x > current.camefrom.x and current.y == current.camefrom.y:
            dir_array.append(1)  # Right
        current = current.camefrom

    # Reset nodes
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = None
            grid[i][j].f = 0
            grid[i][j].g = 0
            grid[i][j].h = 0

    return dir_array[::-1]  # Reverse the direction array

# Initialize grid
grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows / 2)][round(cols / 2)]]
food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]
score = 0

def display_score(score):
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, [10, 10])

def game_over_screen(score):
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render('Game Over!', True, WHITE)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(game_over_text, [width // 2 - 150, height // 2 - 30])
    screen.blit(score_text, [width // 2 - 150, height // 2 + 30])
    display.flip()
    
    # Wait for the user to close the window
    waiting_for_close = True
    while waiting_for_close:
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting_for_close = False
        clock.tick(10)

while not done:
    clock.tick(12)
    screen.fill(BLACK)

    # Get next direction
    if not dir_array:
        dir_array = getpath(food, snake)
    if dir_array:
        direction = dir_array.pop(0)

    # Determine next position
    if direction == 0:  # Down
        next_pos = grid[current.x][current.y + 1]
    elif direction == 1:  # Right
        next_pos = grid[current.x + 1][current.y]
    elif direction == 2:  # Up
        next_pos = grid[current.x][current.y - 1]
    elif direction == 3:  # Left
        next_pos = grid[current.x - 1][current.y]
    else:
        next_pos = current

    # Check boundaries
    if next_pos.x < 0 or next_pos.x >= rows or next_pos.y < 0 or next_pos.y >= cols:
        done = True
        continue

    # Check for self-collision
    if next_pos in snake:
        done = True
        continue

    # Move snake
    snake.append(next_pos)
    current = next_pos

    # Check for food collection
    if current.x == food.x and current.y == food.y:
        while True:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstacle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
        score += 10
    else:
        snake.pop(0)

    # Draw snake, obstacles, and food
    for spot in snake:
        spot.show(WHITE)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstacle:
                grid[i][j].show(RED)
    food.show(GREEN)
    snake[-1].show(BLUE)
    display_score(score)
    display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

# Display final score and game over screen
game_over_screen(score)
print(f'Final Score: {score}')
pygame.quit()
