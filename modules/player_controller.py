import pygame, math

import modules.config as conf
import modules.pygame_objects as py_objs
import modules.objects as objs

class PlayerController:
    def __init__(self:object, x_pos:int, y_pos:int, size:int):
        """Creates a player object"""
        self.rect = pygame.Rect(x_pos, y_pos, 60, 69)
        self.collision_top_rect = pygame.Rect(x_pos + 9, y_pos - 1, 42, 1) # okej
        self.collision_bottom_rect = pygame.Rect(x_pos + 5, y_pos + size, 50, 1) #okej
        self.collision_left_rect = pygame.Rect(x_pos - 1, y_pos + 5, 1, size - 34)
        self.collision_right_rect = pygame.Rect(x_pos + size, y_pos + 5, 1, size - 34)
        self.speed_y = self.speed_x = 0
        self.touched_floor = False
        self.jump_charge = 0
        self.jump_key_pressed = False
        self.has_fallen = False
        self.current_frame, self.running_frames = 9, 0
        self.collisions = [False, False, False, False] #up, down, right, left
        self.direction = ""
        self.has_hit_wall_midair = False
        self.is_not_allowed_to_move = ""
        self.has_collided_prev_frame, self.has_collided_this_frame = True, False # za sfx, bo se za pristat
        self.times_bounced_midair = 0 # za fall in animation
        self.fell = True
        self.jumped_from_y = 0
        self.jumped_from_level = 0
        self.head_bounce = False
        self.has_received_input = False
        self.time_since_pressed_left, self.time_since_pressed_right = 0.0, 0.0
        self.can_move = True
        self.time_charged = 0
        self.friction = 1

    def draw(self:object, screen:pygame.Surface):
        """Draws the player on the screen"""
        if self.speed_x < 0 or self.direction == "left":
            screen.blit(pygame.transform.flip(py_objs.player_images[self.current_frame], True, False), (self.rect.x - 6, self.rect.y - 11))
        else:
            screen.blit(py_objs.player_images[self.current_frame], (self.rect.x - 6, self.rect.y - 11))

    def reset_position(self:object, x_pos:int, y_pos:int):
        """Resets player position"""
        self.rect.x = x_pos
        self.rect.y = y_pos

    def animate(self:object, keys:list, delta_time:float):
        """Sets the correct frame for the player object to draw"""
        if self.speed_x == 0:
            if (not any(keys)) or ((keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d])):
                self.current_frame = 0
            if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
                self.current_frame = 5
                
        if self.speed_x != 0 and self.touched_floor:
            self.running_frames += delta_time
            if self.running_frames > 0.65:
                self.running_frames -= 0.65
            self.current_frame = math.floor(self.running_frames * 6.15)
            
        if self.speed_y < 0:
            self.current_frame = 6
            
        if self.speed_y > 0:
            self.current_frame = 7
            
        if self.has_hit_wall_midair:
            self.current_frame = 8
            if not py_objs.bounce_channel.get_busy() and self.has_collided_this_frame:
                py_objs.bounce_channel.play(py_objs.sfx["bounce"])
        
        if self.fell:
            self.current_frame = 9
            if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
                self.fell = False
                self.jumped_from_level = conf.current_level
                self.jumped_from_y = self.rect.y

    def move(self:object, delta_time:float, keys:list):
        """Handles player movement based on the input"""
        self.friction = self.check_borders()


        self.time_since_pressed_left -= delta_time
        self.time_since_pressed_right -= delta_time

        self.speed_x *= self.friction
        if self.touched_floor and not any(keys):
            self.speed_x *= 0.5
        if self.speed_x > conf.max_speed and self.touched_floor:
            self.speed_x = conf.max_speed
        elif self.speed_x < conf.max_speed * -1 and self.touched_floor:
            self.speed_x = conf.max_speed * -1

        if any(keys) and not self.has_received_input:
            self.has_received_input = True

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.time_since_pressed_left = 0.1
            if self.touched_floor and not self.jump_key_pressed and self.is_not_allowed_to_move != "left":
                self.speed_x = conf.max_speed * -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.time_since_pressed_right = 0.1
            if self.touched_floor and not self.jump_key_pressed and self.is_not_allowed_to_move != "right":
                self.speed_x = conf.max_speed

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.touched_floor:
            self.time_since_pressed_left = 0
            self.time_since_pressed_right = 0
            self.speed_x = 0
        
        if not self.touched_floor:
            if self.speed_y <= 0:
                self.speed_y += conf.gravity * delta_time
            else: 
                self.speed_y += conf.gravity * 2 * delta_time

        self.collision_top_rect.x = self.rect.x + 9
        self.collision_top_rect.y = self.rect.y - 1
        self.collision_bottom_rect.x = self.rect.x + 5
        self.collision_bottom_rect.y = self.rect.y + self.rect.size[1]
        self.collision_left_rect.x = self.rect.x - 1
        self.collision_left_rect.y = self.rect.y + 5
        self.collision_right_rect.x = self.rect.x + self.rect.size[0]
        self.collision_right_rect.y = self.rect.y + 5

        self.check_collision_with_platforms()
        
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.time_charged <= 2:
            if self.touched_floor:
                self.jump_charge -= 34 * delta_time
                self.time_charged += delta_time
                self.speed_x *= 0.5
                self.jump_key_pressed = True
                if self.jump_charge < conf.jump_power:
                    self.jump_charge = conf.jump_power
        
        else:
            if self.jump_charge > -5:
                self.jump_charge = -5
            if self.jump_key_pressed and self.touched_floor:
                self.jump_key_pressed = False
                self.rect.y -= 1
                self.speed_y = self.jump_charge
                if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.time_since_pressed_right > 0:
                    self.speed_x = conf.max_speed * 1.75
                    self.touched_floor = False
                elif keys[pygame.K_LEFT] or keys[pygame.K_a] or self.time_since_pressed_left > 0:
                    self.speed_x = conf.max_speed * -1.75
                    self.touched_floor = False
                else:
                    self.speed_x = 0
                py_objs.sfx["jump"].play()
                self.jumped_from_y = self.rect.y
                self.jumped_from_level = conf.current_level
                conf.game_stats["jumps"] += 1
            else:
                self.jump_charge = 0

        if abs(self.speed_x) < 0.1:
            if self.direction == "":
                if self.speed_x < 0:
                    self.direction = "left"
                else:
                    self.direction = "right"
            self.speed_x = 0
        else:
            self.direction = ""
        if self.speed_y > 20:
            self.speed_y = 20
        
        self.animate(keys, delta_time)
        self.rect.x += self.speed_x * delta_time * 80
        self.rect.y += self.speed_y * delta_time * 90
        keys = []
        return objs.level, conf.current_level

    def check_borders(self:object):
        """Checks if the player is colliding with window borders"""
        self.is_not_allowed_to_move = ""
        if self.rect.right > conf.SCREEN_WIDTH: # RIGHT
            self.rect.right = conf.SCREEN_WIDTH
            self.is_not_allowed_to_move = "right"
            self.has_hit_wall_midair = True
            if self.touched_floor:
                return 0
            else:
                self.times_bounced_midair += 1
                py_objs.sfx["bounce"].play()
                return -0.5
        
        if self.rect.left < 0: # LEFT
            self.rect.left = 0
            self.is_not_allowed_to_move = "left"
            self.has_hit_wall_midair = True 
            if self.touched_floor:
                self.direction = "left"
                return 0
            else:
                self.times_bounced_midair += 1
                py_objs.sfx["bounce"].play()
                return -0.5
            
        if self.rect.centery > conf.SCREEN_HEIGHT: # BOTTOM
            conf.current_level -= 1
            if not conf.current_level < 0:
                self.reset_position(self.rect.x, 0)
                objs.level = objs.levels[conf.current_level]
            else:
                conf.current_level += 1
                self.reset_position((conf.SCREEN_WIDTH / 2) - (conf.player_size / 2), conf.SCREEN_HEIGHT - 400)
                
        if self.rect.centery < 0: # TOP
            conf.current_level += 1
            if not conf.current_level >= len(conf.level_paths):
                self.reset_position(self.rect.x, conf.SCREEN_HEIGHT - self.rect.size[0])
                objs.level = objs.levels[conf.current_level]
            else:
                self.speed_y = 1
                self.rect.centery = 1
                conf.current_level -= 1
                py_objs.sfx["bounce"].play()
                conf.game_stats["head_bounces"] += 1
                self.head_bounce = True
        return 1
    
    def check_collision_with_platforms(self:object):
        """Checks if the player is colliding with the platforms"""
        self.touched_floor = False
        self.has_collided_prev_frame = self.has_collided_this_frame
        for platform in objs.level:
            if not platform.type == 5 or (self.rect.centerx - platform.rect.centerx) ** 2 + (self.rect.centery - platform.rect.centery) ** 2 < 2250: #tle ce pogruntas kire kombinacije sosednjih platform se tudi nemorejo nikoli zgodit (kasni koti - poglej v autotile za stevilko), loh dodas kukr za 5
                self.collisions[0] = False
                self.collisions[1] = False
                self.collisions[2] = False
                self.collisions[3] = False
                dist_x = abs(self.rect.centerx - platform.rect.centerx)
                dist_y = abs(self.rect.centery - platform.rect.centery)

                if self.collision_bottom_rect.colliderect(platform.rect):
                    self.collisions[0] = True
                
                if self.collision_top_rect.colliderect(platform.rect):
                    self.collisions[1] = True
                
                if self.collision_right_rect.colliderect(platform.rect):
                    self.collisions[2] = True
                
                if self.collision_left_rect.colliderect(platform.rect):
                    self.collisions[3] = True

                self.has_collided_this_frame = any(self.collisions)

                if self.collisions[0]:
                    self.touched_floor = True   # za zdej nerabimo cekirat tipov platform, kr so itak samo 1 (bom pol dodau se myb checkpointe in ostale)
                    self.speed_y = 0
                    self.rect.bottom = platform.rect.top
                    self.has_hit_wall_midair = False

                    if not self.has_collided_prev_frame: # landing detection, sfx, orientation
                        self.time_charged = 0
                        if self.speed_x > 0:
                            self.direction = "right"
                        elif self.speed_x < 0:
                            self.direction = "left"
                        if (self.rect.y - 20 > self.jumped_from_y and (self.times_bounced_midair >= 2 or self.head_bounce)) or self.jumped_from_level > conf.current_level:   # pravila za fall
                            self.fell = True
                            py_objs.sfx["fall"].play()
                            conf.game_stats["falls"] += 1
                            conf.game_stats["fall_distance"] += abs(self.jumped_from_y - self.rect.y)
                        else:
                            if self.times_bounced_midair % 2 != 0: # pogledamo ce smo se odbili liho stevilo krat, da obrnemo smer
                                if self.direction == "right":
                                    self.direction = "left"
                                elif self.direction == "left":
                                    self.direction = "right"
                            if self.has_received_input:
                                py_objs.sfx["landing"].play()
                                if self.jumped_from_y - self.rect.y > 5:
                                    conf.game_stats["distance_climbed"] += self.jumped_from_y - self.rect.y + 1
                                
                                elif conf.current_level > self.jumped_from_level: #ce skocimo v nov level
                                    conf.game_stats["distance_climbed"] += self.jumped_from_y + (1000 - self.rect.y) + 1
                                
                                elif self.jumped_from_y - self.rect.y < -5:
                                    conf.game_stats["distance_descended"] += abs(self.jumped_from_y - self.rect.y) - 1

                                conf.game_stats["wall_bounces"] += self.times_bounced_midair
                                if conf.current_level + 1 > conf.game_stats["best_screen"]:
                                    conf.game_stats["best_screen"] = conf.current_level + 1
                        self.speed_x = 0
                    self.times_bounced_midair = 0
                    self.head_bounce = False
                    return
                
                if self.collisions[0] and self.collisions[2]:
                    if dist_x <= dist_y:
                        self.touched_floor = True
                        self.speed_y = 0
                        self.rect.bottom = platform.rect.top
                    
                    else:
                        self.rect.right = platform.rect.left
                        self.speed_x *= -0.5
                    return

                if self.collisions[0] and self.collisions[3]:
                    if dist_x <= dist_y:
                        self.touched_floor = True
                        self.speed_y = 0
                        self.rect.bottom = platform.rect.top
                    
                    else:
                        self.rect.left = platform.rect.right
                        self.speed_x *= -0.5
                    return
                
                if self.collisions[1]:
                    self.speed_y = 1
                    self.rect.top = platform.rect.bottom
                    self.head_bounce = True
                    py_objs.sfx["bounce"].play()
                    conf.game_stats["head_bounces"] += 1
                    return
                
                if self.collisions[2] and not self.collisions[3]:
                    self.rect.right = platform.rect.left
                    self.speed_x *= -0.5
                    if not self.collisions[0]:
                        self.has_hit_wall_midair = True
                        self.times_bounced_midair += 1
                    return

                if self.collisions[3] and not self.collisions[2]:
                    self.rect.left = platform.rect.right
                    self.speed_x *= -0.5
                    if not self.collisions[0]:
                        self.has_hit_wall_midair = True
                        self.times_bounced_midair += 1
                    return

    def get_center_pos(self:object):
        """Returns current player position"""
        return self.rect.center

    def reset_values(self:object):
        """Resets all player values"""
        self.speed_y = self.speed_x = 0
        self.touched_floor = False
        self.jump_charge = 0
        self.jump_key_pressed = False
        self.has_fallen = False
        self.current_frame, self.running_frames = 9, 0
        self.collisions = [False, False, False, False] #up, down, right, left
        self.direction = ""
        self.has_hit_wall_midair = False
        self.is_not_allowed_to_move = ""
        self.has_collided_prev_frame, self.has_collided_this_frame = True, False # za sfx, bo se za pristat
        self.times_bounced_midair = 0 # za fall in animation
        self.fell = True
        self.jumped_from_y = 0
        self.jumped_from_level = 0
        self.head_bounce = False
        self.has_received_input = False
        self.can_move = True
        self.time_charged = 0
