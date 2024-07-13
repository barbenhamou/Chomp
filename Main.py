import pygame
from Rectangle import Rectangle
import time

WIDTH = 750
HEIGHT = 500
BROWN = (150, 75, 0)
DIMENSIONS = 10
CELL_WIDTH = WIDTH / DIMENSIONS
CELL_HEIGHT = HEIGHT / DIMENSIONS
ORANGE = (0, 0, 0)

background_color = (0, 0, 0)
grid = []
screen = None
running = True

def init_screen():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chomp')
    screen.fill(background_color)
    pygame.display.flip()
    return screen

def init_grid(screen):
    global grid
    grid = [[Rectangle((i * CELL_WIDTH, j * CELL_HEIGHT), (i * CELL_WIDTH + CELL_WIDTH - 1, j * CELL_HEIGHT + CELL_HEIGHT - 1), BROWN, screen) for i in range(DIMENSIONS)] for j in range(DIMENSIONS)]

def display_grid():
    for row in grid:
        for rect in row:
            rect.show()
    pygame.display.update()

def get_rect_index(mousePos: tuple):
    return (int(mousePos[0] / CELL_WIDTH), int(mousePos[1] / CELL_HEIGHT))

def loser(name):
    print("loser")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{name} LOST!!!', True, (0,0,0), (255,0,0))
    textRect = text.get_rect()
    textRect.center = (350, 250)
    
    while True:
        screen.fill((255,0,0))
        screen.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def eat(pos: tuple):
    for i in range(pos[0], DIMENSIONS):
        for j in range(pos[1], DIMENSIONS):
            grid[j][i].get_eaten()

def find_best_move():
    # Avoid the poisonous piece (0, 0)
    for x in range(DIMENSIONS):
        for y in range(DIMENSIONS):
            if grid[y][x].color != ORANGE and (x != 0 or y != 0):
                return (x, y)
    return (0, 0)  # Fallback, though ideally this should not happen

def computer_eating(eaten_rect: tuple):
    global running
    if eaten_rect == (0, 0):
        loser("PLAYER")

    if grid[1][1].color != ORANGE:
            best_move = (1,1)
    else:
        best_move = find_best_move()
        
    if best_move == (0, 0):
        loser("COMPUTER")
        
    eat(best_move)
        

def main():
    pygame.init()
    screen = init_screen()
    init_grid(screen)

    global running
    while running:
        display_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = get_rect_index(pygame.mouse.get_pos())
                if grid[y][x].color != ORANGE:  # Ensure the clicked cell is not already eaten
                    eat((x, y))
                    last = (x, y)
                    display_grid()
                    time.sleep(1)
                    computer_eating(last)

    pygame.quit()

if __name__ == "__main__":
    main()