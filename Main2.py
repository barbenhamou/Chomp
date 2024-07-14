import pygame
import time

WIDTH = 750
HEIGHT = 500
BROWN = (150, 75, 0)
DIMENSIONS = 10
CELL_WIDTH = WIDTH / DIMENSIONS
CELL_HEIGHT = HEIGHT / DIMENSIONS
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

background_color = BLACK
grid = []
screen = None
running = True

class Rectangle:
    def __init__(self, UpLeft: tuple, DownRight: tuple, color: tuple, screen):
        self.UpLeft = UpLeft
        self.DownRight = DownRight
        self.color = color
        self.screen = screen

    def show(self):
        pygame.draw.rect(self.screen, self.color,
                         pygame.Rect(self.UpLeft[0] + 1, self.UpLeft[1] + 1, self.DownRight[0] - self.UpLeft[0],
                                     self.DownRight[1] - self.UpLeft[1]))

    def get_eaten(self, color):
        self.color = color


def init_screen():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chomp')
    screen.fill(background_color)
    pygame.display.flip()
    return screen


def init_grid(screen):
    global grid
    grid = [[Rectangle((i * CELL_WIDTH, j * CELL_HEIGHT),
                       (i * CELL_WIDTH + CELL_WIDTH - 1, j * CELL_HEIGHT + CELL_HEIGHT - 1), BROWN, screen) for i in
             range(DIMENSIONS)] for j in range(DIMENSIONS)]
    grid[0][0].color = ORANGE  # Mark the poisonous piece


def display_grid():
    for row in grid:
        for rect in row:
            rect.show()
    pygame.display.update()


def get_rect_index(mousePos: tuple):
    return (int(mousePos[0] / CELL_WIDTH), int(mousePos[1] / CELL_HEIGHT))


def game_over(winner):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{winner} WINS!!!', True, WHITE, RED)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)

    while True:
        screen.fill(RED)
        screen.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def eat(pos: tuple, color):
    for i in range(pos[0], DIMENSIONS):
        for j in range(pos[1], DIMENSIONS):
            grid[j][i].get_eaten(color)

def deeat(pos: tuple, color, rem):
    for i in range(pos[0], DIMENSIONS):
        for j in range(pos[1], DIMENSIONS):
            grid[j][i].color = rem[j][i]

def is_eaten(x, y):
    return grid[y][x].color == ORANGE


def evaluate_board():
    remaining_cells = sum(1 for row in grid for rect in row if rect.color != ORANGE)
    return remaining_cells


def minimax(depth, is_maximizing):
    if depth == 0 or is_eaten(0, 0):
        return evaluate_board()

    if is_maximizing:
        best_score = float('-inf')
        for x in range(DIMENSIONS):
            for y in range(DIMENSIONS):
                if not is_eaten(x, y):
                    original_color = grid[y][x].color
                    to_remain = [[grid[y][x].color for x in range(DIMENSIONS)] for y in range(DIMENSIONS)]
                    eat((y, x), ORANGE)
                    score = minimax(depth - 1, False)
                    print(score)
                    deeat((y, x), original_color, to_remain)
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for x in range(DIMENSIONS):
            for y in range(DIMENSIONS):
                if not is_eaten(x, y):
                    original_color = grid[y][x].color
                    to_remain = [[grid[y][x].color for x in range(DIMENSIONS)] for y in range(DIMENSIONS)]
                    eat((y, x), ORANGE)
                    score = minimax(depth - 1, True)
                    deeat((y, x), original_color, to_remain)
                    best_score = min(score, best_score)
        return best_score


def find_best_move():
    best_score = float('-inf')
    best_move = None
    for x in range(DIMENSIONS):
        for y in range(DIMENSIONS):
            if not is_eaten(x, y):
                original_color = grid[y][x].color
                to_remain = [[grid[y][x].color for x in range(DIMENSIONS)] for y in range(DIMENSIONS)]
                eat((y, x), ORANGE)
                score = minimax(3, False)
                deeat((y, x), original_color, to_remain)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
    return best_move


def computer_eating(eaten_rect: tuple):
    if eaten_rect == (0, 0):
        game_over("PLAYER")

    display_thinking_message()
    best_move = find_best_move()
    hide_thinking_message()

    if best_move is None or best_move == (0, 0):
        game_over("PLAYER")

    eat(best_move, ORANGE)


def display_thinking_message():
    print("thinking")


def hide_thinking_message():
    print("done thinking")


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
                if (x,y) == (0,0):
                    game_over("COMPUTER")
                if grid[y][x].color != ORANGE:  # Ensure the clicked cell is not already eaten
                    eat((x, y), ORANGE)
                    display_grid()
                    time.sleep(1)
                    computer_eating((x, y))
                    display_grid()

    pygame.quit()


if __name__ == "__main__":
    main()