import pygame

class Platform:
    def __init__(self, x_pos, y_pos, size_x, size_y, type):
        self.rect = pygame.Rect(x_pos, y_pos, size_x, size_y)
        self.type = int(type)
