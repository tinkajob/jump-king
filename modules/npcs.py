import pygame, math

from modules.config import level_paths
from modules.pygame_objects import babe_images

class BabeController:
    def __init__(self:object, x_pos:int, y_pos:int, size:int):
        """Creates a babe object *(finish)*"""
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.current_frame, self.jumping_frame = 0, 0
        self.is_visible = False

    def draw(self:object, screen:pygame.Surface, current_level:int, delta_time:float):
        """Draws babe if the last level is shown"""
        if current_level == len(level_paths) - 1:
            self.is_visible = True
            screen.blit(babe_images[self.animate(delta_time)], (self.rect.x, self.rect.y))
        else:
            self.is_visible = False
        
    def animate(self:object, delta_time:float):
        """Sets the correct frame to draw"""
        self.jumping_frame += delta_time
        if self.jumping_frame > 0.45: # ta stevilka
            self.jumping_frame -= 0.45
        self.current_frame = math.floor(self.jumping_frame * 6.660) % len(babe_images) #in ta stevilka zmnozene morejo bit enake (oz. piko manjse) kukr je st. frameov animacije, zdej je uredi
        return self.current_frame

    def check_for_ending(self:object, player:object):
        """Checks whether the player collides with the babe"""
        if self.rect.colliderect(player.rect) and self.is_visible:
           return True
        return False
    
    def find_position(self, config_pos:list, last_level:list):
        # mu damo noter podatke iz config.json in uporabimo tiste vrednosti, 
        # ce niso nastavljeni, ce ne obstajajo ali pa ce niso mozni (-1, -1), potem pa poiscemo najvisje lezeco ustrezno platformo 
        # Ustrezna platforma: usaj 2 tiles v vrsti, nad njimi usaj 3 visina prosta
        if config_pos:
            self.rect.x = config_pos[0]
            self.rect.y = config_pos[1]
        else:
            pass