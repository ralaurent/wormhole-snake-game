import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
SNAKE_SIZE = 30
GRID_SIZE = 30 
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 5
PINK = (255, 124, 132)
BORDER_PINK = (255, 0, 61)
DARK_GREY = (50, 50, 50) 
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

grid = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wormhole")

clock = pygame.time.Clock()

def random_grid_position():
    return random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

inside_wormhole = False
just_exited_wormhole = False  

worm_x, worm_y = random_grid_position()
worm_dx, worm_dy = 0, 0

worm_body = [(worm_x, worm_y)]

food_x, food_y = random_grid_position()

wormhole1_x, wormhole1_y = random_grid_position()
wormhole2_x, wormhole2_y = random_grid_position()

def check_self_collision(worm_body):
    head = worm_body[0]
    return any(segment == head for segment in worm_body[1:])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                worm_dx, worm_dy = 0, -GRID_SIZE
            elif event.key == pygame.K_DOWN:
                worm_dx, worm_dy = 0, GRID_SIZE
            elif event.key == pygame.K_LEFT:
                worm_dx, worm_dy = -GRID_SIZE, 0
            elif event.key == pygame.K_RIGHT:
                worm_dx, worm_dy = GRID_SIZE, 0

    worm_x += worm_dx
    worm_y += worm_dy

    if worm_x < 0 or worm_x >= WIDTH or worm_y < 0 or worm_y >= HEIGHT:
        pygame.quit()
        exit()

    if math.dist((worm_x, worm_y), (food_x, food_y)) < SNAKE_SIZE:
        worm_body.append((worm_x, worm_y))
        food_x, food_y = random_grid_position()

    if math.dist((worm_x, worm_y), (wormhole1_x, wormhole1_y)) < SNAKE_SIZE:
        if not inside_wormhole:
            worm_x, worm_y = wormhole2_x, wormhole2_y
            inside_wormhole = True
            just_exited_wormhole = False
    elif math.dist((worm_x, worm_y), (wormhole2_x, wormhole2_y)) < SNAKE_SIZE:
        if not inside_wormhole:
            worm_x, worm_y = wormhole1_x, wormhole1_y
            inside_wormhole = True
            just_exited_wormhole = False
    else:
        inside_wormhole = False

    if not inside_wormhole and just_exited_wormhole:
        just_exited_wormhole = False

    if inside_wormhole and not just_exited_wormhole:
        wormhole1_x, wormhole1_y = random_grid_position()
        wormhole2_x, wormhole2_y = random_grid_position()
        just_exited_wormhole = True

    if check_self_collision(worm_body):
        pygame.quit()
        exit()

    worm_body.insert(0, (worm_x, worm_y))
    if len(worm_body) > 1:
        worm_body.pop()

    grid.fill(DARK_GREY) 

    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(grid, BLACK, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(grid, BLACK, (0, y), (WIDTH, y), 1)

    pygame.draw.rect(grid, GREEN, pygame.Rect(food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))

    for segment in worm_body:
        pygame.draw.rect(grid, PINK, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(grid, BORDER_PINK, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE), 1)

    pygame.draw.circle(grid, BLACK, (wormhole1_x + SNAKE_SIZE // 2, wormhole1_y + SNAKE_SIZE // 2), SNAKE_SIZE // 2)
    pygame.draw.circle(grid, BLACK, (wormhole2_x + SNAKE_SIZE // 2, wormhole2_y + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

    pygame.display.flip()

    clock.tick(FPS)
