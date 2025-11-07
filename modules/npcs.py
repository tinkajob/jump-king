import pygame, math

import modules.config as conf
from modules.config import tile_size, babe_min_row_length
import modules.pygame_objects as py_objs

from modules.utils import slice_level, find_valid_subrows

class BabeController:
    def __init__(self:object, x_pos:int, y_pos:int, size:int):
        """Creates a babe object *(finish)*"""
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.player_collision_rect = pygame.rect.Rect(x_pos - (babe_min_row_length * tile_size - size), y_pos, size + (babe_min_row_length * tile_size - size), size)
        self.current_frame, self.jumping_frame = 0, 0
        self.is_visible = False
        self.end_animation_status = ""
        self.current_frame = 0
        self.first_time_end_animation_called = True

    def draw(self:object, screen:pygame.Surface, current_level:int):
        """Draws babe if the last level is shown"""
        if current_level == len(conf.level_paths) - 1:
            self.is_visible = True
            screen.blit(py_objs.babe_images[self.current_frame], (self.rect.x, self.rect.y))
        else:
            self.is_visible = False
        
    def animate(self:object, delta_time:float = 0):
        """Sets the correct frame to draw"""

        # How we animate end animation
        if self.end_animation_status == "started":
            self.current_frame = 0
            return
        
        # At the end we do one aditional jump
        if self.end_animation_status == "end":
            if self.first_time_end_animation_called:
                self.jumping_frame = 0
                self.first_time_end_animation_called = False

            self.jumping_frame += delta_time
            self.current_frame = math.floor(self.jumping_frame * 6.660)

            if self.current_frame == 0:
                self.rect.y -= 50 * delta_time

            if self.current_frame == 2:
                self.rect.y += 50 * delta_time

            if self.current_frame >= len(py_objs.babe_images):
                self.current_frame = 0
            return

        self.jumping_frame += delta_time
        if self.jumping_frame > 0.45: # ta stevilka
            self.jumping_frame -= 0.45
        self.current_frame = math.floor(self.jumping_frame * 6.660) % len(py_objs.babe_images) #in ta stevilka zmnozene morejo bit enake (oz. piko manjse) kukr je st. frameov animacije, zdej je uredi

    def reset(self:object):
        self.end_animation_status = ""
        self.current_frame, self.jumping_frame = 0, 0
        self.is_visible = False
        self.first_time_end_animation_called = True

    def check_for_ending(self:object, player_rect:pygame.rect.Rect):
        """Checks whether the player collides with the babe"""
        if not self.is_visible:
            return ""

        if self.rect.colliderect(player_rect):
           self.end_animation_status = "end"
           return "end_game"

        if self.player_collision_rect.colliderect(player_rect):
            self.end_animation_status = "started"
            return "start_animation"
        
        return ""
    
    def get_pos(self:object):
        return self.rect.topleft

    def get_correct_platform_position(self:object, platform):
        # We position babe on the right side of the platform
        x_pos = platform[0].rect.x + (len(platform) * tile_size) - self.rect.width

        # We just set it to the y value of platform, then offset by babe size
        y_pos = platform[0].rect.y - self.rect.height
        
        return x_pos, y_pos

    def auto_position_on_last_level(self:object, last_level:list, tile_size:int, min_row_length:int):
        # First we slice level into horizontal platforms
        level_rows = slice_level(last_level, tile_size, min_row_length)
        suitable_platforms = []

        # When we have all the rows we check each platforms if it's suitable for babe to stand on
        for platform_index in range(len(level_rows)):
            tiles = level_rows[platform_index]

            # First we eliminate all platforms, shorter than min_row_length
            if len(tiles) < min_row_length:
                continue
            
            # Then we check for 3 spaces above, and eliminate platforms that are too high
            platform_area = pygame.rect.Rect(tiles[0].rect.x, tiles[0].rect.y - (3 * tile_size), len(tiles) * tile_size, 4 * tile_size) # We create an area of platform + 3 tiles above
            if platform_area.y < 0: 
                continue
            
            # If the platform collides with any other previous platform, we add any suitable subrows manually, and we skip that platform
            valid_subrows = find_valid_subrows(tiles, level_rows, platform_index, platform_area, min_row_length)
            
            # If the platform doesn't collide with any other, the whole platform is returned, otherwise we return list of all subrows, siutable for babe
            if tiles != valid_subrows:
                for valid_subrow in valid_subrows:
                    suitable_platforms.append(valid_subrow)
                continue

            suitable_platforms.append(tiles)
        
        return suitable_platforms

    def find_position(self, config_pos:list, last_level:list, tile_size:int, SCREEN_WIDTH, SCREEN_HEIGHT):
        # If there is position specified in config.json, we use that,
        # otherwise we auto-position babe (highest suitable platoform)
        
        # Suitable platform: long at least (babe_min_rowh_lenght) tiles, above at least 3 tiles free
        
        # If position is specified in config.json, we use those values
        if config_pos:
            self.rect.x = config_pos[0]
            self.rect.y = config_pos[1]
            return

        # Otherwise we auto_position babe (if there are any suitable platforms):
        suitable_platforms = self.auto_position_on_last_level(last_level, tile_size, babe_min_row_length)
        if suitable_platforms:
            self.rect.x, self.rect.y = self.get_correct_platform_position(suitable_platforms[0])
            return

        # If there are no suitable platforms for babe we just draw it in the middle of the screen
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2