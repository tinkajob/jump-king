import pygame

class Platform:
    def __init__(self:object, x_pos:int, y_pos:int, size_x:int, size_y:int, type:int):
        """Creates a platform object"""
        self.rect = pygame.Rect(x_pos, y_pos, size_x, size_y)
        self.type = int(type)
