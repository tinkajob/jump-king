import pygame, math
from modules.config import colors
from modules.pygame_objects import fonts, buttons

class Text:
    def __init__(self:object, text: str, color: str, font: str, position: tuple[int, int]):
        """
        Create a text object.
        Args:
            text (str): The text string to render.
            color (str): The color key for text to use from the colors dictionary.
            font (str): The font key to use from the fonts dictionary.
            position (tuple[int, int]): Center position for the text.
        """
        self.text = text
        self.color = colors[color]
        self.font = font
        self.pos = position
        self.surface = fonts[self.font].render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center = self.pos)

    def draw(self:object, screen:pygame.Surface):
        """Draws text on the screen"""
        screen.blit(self.surface, self.rect)

    def update(self:object):
        """Updates text and re-renders its surface"""
        self.surface = fonts[self.font].render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center = self.pos)
        return self.rect

class InputField:
    def __init__(self:object, pos_tuple:tuple [int, int], dimentions:tuple [int, int], mask_input:bool, type:str):
        """Creates an input field object"""
        self.rect = pygame.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1])
        self.mask_input = mask_input
        self.color = "grey_dark"
        self.input_text = ""
        self.masked_text = ""
        self.is_focused = False
        self.type = type
        self.changed_this_frame = False
    
    def draw(self:object, screen:pygame.Surface):
        """Draws input field on the screen"""
        pygame.draw.rect(screen, colors[self.color], self.rect, 5, 25)

    def capture_input(self:object, events:list, username_text:object, password_text:object):
        """Captures text from the input field and updates the corresponding text object"""
        from modules.objects import cursor
        self.get_focused()
        if not self.is_focused:
            return

        self.changed_this_frame = False
        self.backspace_pressed = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    if self.mask_input:
                        self.masked_text = self.masked_text[:-1]
                    self.changed_this_frame = True
                
                elif event.key == pygame.K_RETURN:
                    self.is_focused = False
                
                elif event.unicode.isprintable() and len(self.input_text) < 20:
                    self.input_text += event.unicode
                    if self.mask_input:
                        self.masked_text += "*"
                    self.changed_this_frame = True

        if self.type == "username":
            username_text.text = self.input_text
            username_text.update()
            
        elif self.type == "password":
            password_text.text = self.masked_text
            password_text.update()
            
        if self.changed_this_frame:
            cursor.time_untill_blink = 0.5

    def get_focused(self:object):
        """Manages functionality of being in focus"""
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_pos):
                self.color = "mint_dark"
                self.is_focused = True

            else:
                self.color = "grey_dark"
                self.is_focused = False

class Cursor:
    def __init__(self:object, pos_tuple:tuple [int, int], size_tuple:tuple [int, int]):
        """Creates a cursor for input field"""
        self.rect = pygame.Rect(pos_tuple[0], pos_tuple[1], size_tuple[0], size_tuple[1])
        self.is_visible = False
        self.can_draw = False
        self.animation_speed = 0.5
        self.current_frame = 0
        self.time_untill_blink = 0
    
    def draw(self:object, screen:pygame.Surface, delta_time:float):
        """Draws the cursor on the screen"""
        self.time_untill_blink -= delta_time
        if self.time_untill_blink <= 0:
            self.time_untill_blink = 0
            self.current_frame += delta_time
            if self.current_frame > self.animation_speed:
                self.current_frame = 0
                if self.is_visible:
                    self.is_visible = False
                else:
                    self.is_visible = True
        else:
            self.is_visible = True

        if self.can_draw and self.is_visible:
            pygame.draw.rect(screen, colors["white"], self.rect)
    
    def update(self:object):
        """Updates cursors state and position"""
        from modules.objects import password_input, username_input, username_text, password_text
        if username_input.is_focused:
            self.rect.x = username_text.rect.right + 5
            self.rect.centery = username_text.rect.centery
            self.can_draw = True

        elif password_input.is_focused:
            self.rect.x = password_text.rect.right + 5
            self.rect.centery = password_text.rect.centery
            self.can_draw = True
        
        else:
            self.can_draw = False

class Button:
    def __init__(self:object, pos_tuple:tuple [int, int], size_tuple:tuple [int, int], type: str):
        """Creates a clickable button"""
        self.rect = pygame.Rect(pos_tuple[0], pos_tuple[1], size_tuple[0], size_tuple[1])
        self.type = type
        self.state = 0
        self.has_been_pressed = False

    def draw(self:object, screen:pygame.Surface):
        """Draws the button based on its type"""
        if self.type == "play":
            screen.blit(buttons[self.state], (self.rect.x, self.rect.y))
        elif self.type == "quit" or self.type == "submit" or self.type == "logout":
            screen.blit(buttons[self.state + 3], (self.rect.x, self.rect.y))

    def is_clicked(self:object):
        """Checks if button was pressed"""
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            self.state = 1
            if pygame.mouse.get_pressed()[0]:
                self.state = 2      
                self.has_been_pressed = True
            elif self.has_been_pressed:
                self.has_been_pressed = False
                return True
            return False
        else:
            self.state = 0

class FadeManager:
    def __init__(self:object, screen_width:int, screen_height:int):
        """Creates a fade manager"""
        self.fade_rect = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.alpha = 255
        self.is_active = False
        self.fade_in_mode = True
        self.speed = 5
    
    def start_fade_in(self:object, speed:int = 300):
        "Starts the fade in effect"
        self.is_active = True
        self.fade_in_mode = True
        self.speed = speed

    def start_fade_out(self:object, speed:int = 300):
        """Starts fade out effect"""
        self.is_active = True
        self.fade_in_mode = False
        self.speed = speed

    def update(self:object, delta_time:float, screen:pygame.Surface):
        """Updates the effect values each frame based on the framerate"""
        if not self.is_active:
            return
        
        if self.fade_in_mode:
            self.alpha -= self.speed * delta_time
            self.alpha = math.floor(self.alpha)
            if self.alpha < 0:
                self.alpha = 0
                self.is_active = False
        
        else:
            self.alpha += self.speed * delta_time
            self.alpha = math.floor(self.alpha)
            if self.alpha > 255:
                self.alpha = 255
                self.is_active = False

        self.fade_rect.fill((0, 0, 0))
        self.fade_rect.set_alpha(self.alpha)
        screen.blit(self.fade_rect, (0, 0))
    
    def get_active(self:object):
        """Returns if effect is active or not"""
        return self.is_active