import pygame, math

from modules.config import level_paths
from modules.pygame_objects import babe_images

class BabeController:
    def __init__(self, x_pos, y_pos, size):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.current_frame, self.jumping_frame = 0, 0
        self.is_visible = False

    def draw(self, screen, current_level, delta_time):
        if current_level == len(level_paths) - 1:
            self.is_visible = True
            screen.blit(babe_images[self.animate(delta_time)], (self.rect.x, self.rect.y))
        else:
            self.is_visible = False
        
    def animate(self, delta_time):
        self.jumping_frame += delta_time
        if self.jumping_frame > 0.45: # ta stevilka
            self.jumping_frame -= 0.45
        self.current_frame = math.floor(self.jumping_frame * 6.660) % len(babe_images) #in ta stevilka zmnozene morejo bit enake (oz. piko manjse) kukr je st. frameov animacije, zdej je uredi
        return self.current_frame

    def check_for_ending(self, player):
        if self.rect.colliderect(player.rect) and self.is_visible:
           return True
        return False