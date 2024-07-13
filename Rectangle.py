import pygame

ORANGE = (0, 0, 0)

class Rectangle:
    def __init__(self, UpLeft: tuple, DownRight: tuple, color: tuple, screen):
        self.UpLeft = UpLeft
        self.DownRight = DownRight
        self.color = color
        self.screen = screen


    def show(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.UpLeft[0] + 1, self.UpLeft[1] + 1, self.DownRight[0] - self.UpLeft[0], self.DownRight[1] - self.UpLeft[1]))
    
    def get_eaten(self):
        self.color = ORANGE
