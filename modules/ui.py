import pygame, math
import modules.config as conf
import modules.pygame_objects as py_objs

class EffectManager:
    def __init__(self:object, screen_width:int, screen_height:int):
        """Creates a fade manager"""
        super().__init__()
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

class UIElement:
    def __init__(self, rect:pygame.Rect = pygame.rect.Rect(0, 0, 0, 0)):
        self.interactable = True
        self.mouse_down_inside = False
        self.rect = rect
    
    def detect_click(self:object, events):
        """Returns True only if user clicked (pressed + released) inside the rect."""
        clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down_inside = self.rect.collidepoint(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.mouse_down_inside and self.rect.collidepoint(event.pos):
                    clicked = True
                self.mouse_down_inside = False
        return clicked

class Text(UIElement):
    def __init__(self:object, text: str, color: str, font: str, position: tuple[int, int], center_position:bool = True):
        """
        Create a text object.
        Args:
            text (str): The text string to render.
            color (str): The color key for text to use from the colors dictionary.
            font (str): The font key to use from the fonts dictionary.
            position (tuple[int, int]): Center position for the text.
            center_position (bool): If given coordinates should be the position of the center of text. (Otherwise it's position of topleft corner).
        """
        super().__init__()
        self.text = text
        self.color = conf.colors[color]
        self.font = font
        self.pos = position
        self.center_position = center_position
        self.surface = py_objs.fonts[self.font].render(self.text, True, self.color)
        if self.center_position:
            self.rect = self.surface.get_rect(center = self.pos)
        else:
            self.rect = self.surface.get_rect(topleft = self.pos)

    def draw(self:object, screen:pygame.Surface):
        """Draws text on the screen"""
        screen.blit(self.surface, self.rect)

    def update(self:object, max_width:int = 0, font:str = "notification"):
        """Updates text and re-renders its surface"""
        self.surface = py_objs.fonts[self.font].render(self.text, True, self.color)
        
        self.wrap(max_width, font)

        #Splits lines based on \n char and renders all lines into 1 surface
        lines = self.text.splitlines()
        rendered_lines = []
        for line in lines:
            rendered_lines.append(py_objs.fonts[self.font].render(line, True, self.color))

        text_width, text_height = 0, 0
        for line in rendered_lines:
            text_height += line.get_height()
            text_width = max(text_width, line.get_width())

        self.surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)

        y = 0
        for line in rendered_lines:
            self.surface.blit(line, (0, y))
            y += line.get_height()

        if self.center_position:
            self.rect = self.surface.get_rect(center = self.pos)
        else:
            self.rect = self.surface.get_rect(topleft = self.pos)
    
    def wrap(self:object, max_width:int = 0, font:str = "notification"):
        if max_width == 0:
            return

        words = self.text.split()
        self.text = words[0]
        current_line_width = 0
        space_width = py_objs.fonts[font].size(" ")[0]
        words
        for word in words[1:]:
            word_width = py_objs.fonts[font].size(word)[0]
            if current_line_width + word_width + space_width <= max_width:
                self.text = self.text + " " + word
                lines = self.text.split("\n")
                current_line_width = py_objs.fonts[font].size(lines[len(lines) - 1])[0]
            else:
                self.text = self.text + "\n" + word
                current_line_width = 0

class InputField(UIElement):
    def __init__(self:object, pos_tuple:tuple [int, int], dimentions:tuple [int, int], mask_input:bool, type:str):
        """Creates an input field object"""
        super().__init__(pygame.rect.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1]))
        self.mask_input = mask_input
        self.color = "grey_dark"
        self.input_text = ""
        self.masked_text = ""
        self.is_focused = False
        self.text_if_empty = type
        self.changed_this_frame = False
        self.cursor = Cursor((0, 0), (4, 36), self)
        self.text = Text("username", "white", "smaller", self.rect.center)
    
    def draw(self:object, screen:pygame.Surface, delta_time):
        """Draws input field on the screen"""
        pygame.draw.rect(screen, conf.colors[self.color], self.rect, 5, 25)
        self.text.draw(screen)
        self.cursor.draw(screen, delta_time)

    def capture_input(self:object, events:list):
        """Captures text from the input field and updates the corresponding text object"""

        if not self.interactable:
            return

        self.get_focused(events)
        if not self.is_focused:
            if self.input_text == "":
                self.text.text = self.text_if_empty
                self.text.update()
            return

        self.changed_this_frame = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    self.changed_this_frame = True
                
                elif event.key == pygame.K_RETURN:
                    self.set_focused(False)
                
                elif event.unicode.isprintable() and len(self.input_text) < 20:
                    self.input_text += event.unicode
                    self.changed_this_frame = True

        if self.mask_input:
            self.text.text = "*" * len(self.input_text)
        else:
            self.text.text = self.input_text
        self.text.update()
            
        if self.changed_this_frame:
            self.cursor.time_untill_blink = 0.5
        
        self.cursor.update()

    def get_focused(self:object, events):
        """Manages functionality of being in focus"""
        if super().detect_click(events):
            self.set_focused(True)
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if not self.rect.collidepoint(event.pos):
                        self.set_focused(False)
        
    def set_focused(self:object, focus_check:bool):
        if focus_check:
            self.color = "mint_dark"
            self.is_focused = True
            self.cursor.is_visible = True

        else:
            self.color = "grey_dark"
            self.is_focused = False
            self.cursor.is_visible = False

        self.cursor.update()

class Cursor(UIElement):
    def __init__(self:object, pos_tuple:tuple [int, int], dimentions:tuple [int, int], parent_input_field):
        """Creates a cursor for input field"""
        super().__init__(pygame.rect.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1]))
        self.is_visible = False
        self.can_draw = False
        self.animation_speed = 0.5
        self.current_frame = 0
        self.parent_input = parent_input_field
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
            pygame.draw.rect(screen, conf.colors["white"], self.rect)
    
    def update(self:object):
        """Updates cursors state and position"""
        from modules.objects import password_input, username_input
        if self.parent_input.is_focused:
            self.rect.x = self.parent_input.text.rect.right + 5
            self.rect.centery = self.parent_input.text.rect.centery
            self.can_draw = True
        
        else:
            self.can_draw = False

class Button(UIElement):
    def __init__(self:object, pos_tuple:tuple [int, int], dimentions:tuple [int, int], offset:int = 0):
        """Creates a clickable button"""
        super().__init__(pygame.rect.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1]))
        self.state = 0
        self.has_been_pressed = False
        self.offset = offset # Offset from first button image from all the images

    def draw(self:object, screen:pygame.Surface):
        """Draws the button based on its type"""
        screen.blit(py_objs.buttons[self.state + self.offset], (self.rect.x, self.rect.y))

    def is_clicked(self:object, events):
        """Checks if button was pressed"""
        if not self.interactable:
            return

        mouse_position = pygame.mouse.get_pos()
        was_clicked = super().detect_click(events)

        if self.rect.collidepoint(mouse_position):
            self.state = 1
            
            if pygame.mouse.get_pressed()[0]:
                self.state = 2      
                self.has_been_pressed = True
            
            elif self.has_been_pressed and was_clicked:
                self.has_been_pressed = False
                return True
            return False
        else:
            self.state = 0

class Notification(UIElement):
    def __init__(self:object, pos_tuple:tuple [int, int], dimentions:tuple [int, int], text:str):
        """Creates a notification object"""
        super().__init__(pygame.rect.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1]))
        self.text = Text(text, "white", "notification", self.rect.center)
        self.max_width = 700
        self.margin = 25
        self.is_visible = True
        self.color = conf.colors["grey_dark"]
        self.has_been_pressed = False

    def show_notification(self, message):
        self.is_visible = True
        self.text.text = message
        self.update()

    def clear_notification_if_clicked(self:object, events):
        if super().detect_click(events):
            self.is_visible = False

    def delete_notification(self):
        self.is_visible = False

    def draw(self, screen:pygame.Surface):
        """If allowed, draws notification on screen"""
        if not self.is_visible:
            return
        
        pygame.draw.rect(screen, self.color, self.rect, 0, 25)
        self.text.draw(screen)

    def update(self:object):
        """Updates its rect and position"""
        self.text.update(self.max_width - (2 * self.margin), "notification")
        self.rect.x = self.text.rect.x - self.margin
        self.rect.width = self.text.rect.width + (2 * self.margin)
        self.rect.height = self.text.rect.height + (2 * self.margin)
        self.rect.y = 950 - (self.text.rect.height + (2 * self.margin))
        
        if self.rect.width > self.max_width:
            self.rect.width = self.max_width

        self.text.rect.center = self.rect.center

class DropdownMenu(UIElement):
    def __init__(self, pos_tuple: tuple[int, int], dimentions:tuple[int, int], items:list):
        super().__init__(pygame.rect.Rect(pos_tuple[0], pos_tuple[1], dimentions[0], dimentions[1]))
        self.position = pos_tuple
        self.dimentions = dimentions
        self.items = items
        self.items_texts = []
        self.row_height = 50 # How high is each row
        self.item_width_limit = self.dimentions[0] - 20 # In pixels
        self.rect_border_width = 5
        self.highlited_item = 0
        self.rect = pygame.rect.Rect(self.position[0], self.position[1], self.dimentions[0], self.dimentions[1])
        self.selection_rect = pygame.rect.Rect(self.position[0], self.position[1] + self.dimentions[1] - self.rect_border_width, self.dimentions[0], len(items) * self.row_height + 2 * self.rect_border_width)
        self.highlited_rect = pygame.rect.Rect(self.position[0], self.position[1] + self.dimentions[1] + self.highlited_item * self.row_height, self.dimentions[0], self.row_height)
        self.is_anything_highlited = True
        self.is_focused = False
        self.color = "grey_dark"
        self.selected_item = ""
        self.selection_text = "Select a campaign"
        self.last_highlited_change_made_by = "" # For when we handle confirming selection
        self.font = "bold"
        self.items.sort()
        self.limit_item_length()
        self.create_texts()

    def draw(self:object, screen:pygame.surface.Surface, events):
        self.get_active(events)

        #If the dropdown isn't focused, we draw all corners rounded, and don't display selection rectangle
        if not self.is_focused:
            pygame.draw.rect(screen, conf.colors[self.color], self.rect, self.rect_border_width, 25)
            self.items_texts[0].draw(screen)
            return
        
        # Otherwise we draw the whole dropdown with all the elements
        pygame.draw.rect(screen, conf.colors[self.color], self.rect, self.rect_border_width, 0, 25, 25, 0, 0)
        pygame.draw.rect(screen, conf.colors["grey_dark"], self.selection_rect, 0, 0, 0, 0, 25, 25)
        
        if self.is_anything_highlited:
            if self.highlited_item != len(self.items) - 1:
                pygame.draw.rect(screen, conf.colors["grey_middle"], self.highlited_rect)
            else:
                pygame.draw.rect(screen, conf.colors["grey_middle"], self.highlited_rect, 0, 0, 0, 0, 25, 25)
        pygame.draw.rect(screen, conf.colors[self.color], self.selection_rect, self.rect_border_width, 0, 0, 0, 25, 25)
        
        for text in self.items_texts:
            text.draw(screen)

    def handle_highliting(self:object, events:list):
        if not self.is_focused:
            return
        
        mouse_moved = False
        enter_pressed = False

        # If we press arrow up or arrow down, we should move highlited_rect in the appropriate direction
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mouse_moved = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.highlited_item += 1
                    self.last_highlited_change_made_by = "keyboard"
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.highlited_item -= 1
                    self.last_highlited_change_made_by = "keyboard"
                elif event.key == pygame.K_RETURN:
                    enter_pressed = True

        # If we move mouse up or down, we should change highlited item! (if we are on top dropdown menu!)
        mouse_pos = pygame.mouse.get_pos()
        if self.selection_rect.collidepoint(mouse_pos) and mouse_moved:
            if mouse_pos[1] < self.highlited_rect.top:
                self.highlited_item -= 1
            elif mouse_pos[1] > self.highlited_rect.bottom:
                self.highlited_item += 1
            self.last_highlited_change_made_by = "mouse"

        # We make sure that index for highlited item is reasonable
        if self.highlited_item >= len(self.items):
            self.highlited_item = len(self.items) - 1
        elif self.highlited_item < 0:
            self.highlited_item = 0

        self.highlited_rect.top = self.position[1] + self.dimentions[1] + self.highlited_item * self.row_height
        self.handle_confirming_selection(pygame.mouse.get_pressed()[0], enter_pressed)

    def handle_confirming_selection(self:object, mouse_down:bool, enter_pressed:bool):
        if (self.last_highlited_change_made_by == "mouse" and mouse_down and self.highlited_rect.collidepoint(pygame.mouse.get_pos())) or (self.last_highlited_change_made_by == "keyboard" and enter_pressed):
            self.selected_item = self.items[self.highlited_item]
            self.is_focused = False
            self.items_texts[0].text = self.selected_item
            self.items_texts[0].update()

    def get_active(self:object, events):
        mouse_pos = pygame.mouse.get_pos()

        if super().detect_click(events):
            self.set_active(True)
            return
        
        if not self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            self.set_active(False)
    
    def set_active(self:object, active_check:bool):
        if active_check:
            self.color = "mint_dark"
            self.is_focused = True
        else:
            self.color = "grey_dark"
            self.is_focused = False

    def create_texts(self:object):
        """Create text objects for all the items in the dropdown."""
        self.items_texts.append(Text("Select a campaign", "white", self.font, (self.position[0] + 15, self.position[1] + 25), False))

        for i in range(len(self.items)):
            self.items_texts.append(Text(self.items[i], "white", self.font, (self.position[0] + 15, self.position[1] + self.dimentions[1] + self.rect_border_width + self.row_height * i), False))

    def get_selection(self:object):
        return self.selected_item

    def limit_item_length(self:object):
        """Edit items texts so that if they are too long, they get shortened by getting ... at the end"""
        
        # For each element in the list of items we check if the name length is too big
        for item_index in range(len(self.items)):
            current_str = ""
            for letter in self.items[item_index]:
                current_str += letter

                # If it is, then we simply remove what we have added of too much and replace it with "..."
                if py_objs.fonts[self.font].size(current_str)[0] > self.item_width_limit:
                    current_str = current_str[:-4]
                    current_str += "..."
                    self.items[item_index] = current_str
                    break

class Slider(UIElement):
    def __init__(self:object, max_value):
        super().__init__()
        self.max_value = max_value