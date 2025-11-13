import os, json, hashlib, pygame

import modules.platform as platform
import modules.pygame_objects as py_objs
import modules.objects as objs
import modules.config as conf

# For the values that don't change values during game we use this import (a bit faster)
from modules.config import SUPPORTED_IMAGE_FORMATS, SCREEN_WIDTH, SCREEN_HEIGHT, fallback_resources_folder, stats_folder, def_stats, campaigns_folder, messages, tile_size, bg_resize_koeficient, tile_images_paths, player_images_paths, babe_images_paths, button_images_paths

# MISCELANEOUS
def log_in(username:str, password:str, title:str, effect:object, username_input:str, password_input:str, stats:list):
    """Handles user login and account creation based on provided inputs."""

    is_new_player = load_player_stats(username)
    next_scene = "main_menu"

    # If we play as quest
    if username == "" or username.lower() == "quest":
        title.text = "Welcome!"
        title.update()
        effect.start_fade_out()
        return "main_menu"

    if is_new_player:
        stats["password"] = hash_password(password)
        title.text = f"Welcome, {username}!"
        title.update()
        effect.start_fade_out()
        return "main_menu"
    
    # If the user's password is correct
    if hash_password(password) == stats["password"]:
        title.text = f"Welcome back, {username}!"
        title.update()
        effect.start_fade_out()
    
    else:
        username_input.input_text = ""
        password_input.input_text = ""
        password_input.masked_text = ""
        username_input.text.text = ""
        password_input.text.text = ""
        username_input.text.update()
        password_input.text.update()
        next_scene = "login"
        
    save_player_stats(username, stats)
    return next_scene

def hash_password(password:str):
    """Encrypts password using hash function"""
    password = str(password)
    return hashlib.sha256(password.encode()).hexdigest()

def autotile(neighbors:list):
    """Based on list ***neighbors*** chooses correct image for each tile to display"""

    if neighbors[1] == 0 and neighbors[3] == 0 and neighbors[4] == 0 and neighbors[6] == 0: #enojna
        return 0
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7]== 1: #cela polna
        return 5
    if neighbors[0] == 0 and neighbors[1] == 0 and neighbors[3] == 0 and neighbors[4] == 1 and neighbors[6] == 1: #kot levo zgoraj
        if neighbors[7] == 1:
            return 1
        elif neighbors[7] == 0:
            return 16
    if neighbors[0] == 0 and neighbors[1] == 0 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4] == 0 and neighbors[6] == 1: #kot desno zgoraj
        if neighbors[5] == 1:
            return 3
        elif neighbors[5] == 0:
            return 17
    if neighbors[0] == 0 and neighbors[1] == 0 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7]== 1: #zgoraj, daljsa
        return 2
    if neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0 and neighbors[4] == 1 and neighbors[6] == 1  and neighbors[7] == 1: #dvojna stranska levo
        return 4
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[3] == 1 and neighbors[4] == 0 and neighbors[5] == 1 and neighbors[6] == 1: #dvojna stranska desno
        return 6
    if neighbors[1] == 1  and neighbors[3] == 0 and neighbors[4] == 1 and neighbors[5] == 0 and neighbors[6] == 0 and neighbors[7]== 0: #kot levo spodaj
        if neighbors[2] == 1:
            return 7
        elif neighbors[2] == 0:
            return 18
    if neighbors[1] == 1 and neighbors[3] == 1 and neighbors[4] == 0 and neighbors[5] == 0 and neighbors[6] == 0 and neighbors[7]== 0: #kot desno spodaj
        if neighbors[0] == 1:
            return 9
        elif neighbors[0] == 0:
            return 19
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4] == 1 and neighbors[6] == 0: #dvojna spodnja
        return 8
    if neighbors[1] == 0 and neighbors[3] == 0 and neighbors[4] == 1 and neighbors[6] == 0: #enojna stranska leva
        return 10
    if neighbors[1] == 0 and neighbors[3] == 1 and neighbors[4] == 1 and neighbors[6] == 0: #enojna horizontalna
        return 11
    if neighbors[1] == 0 and neighbors[3] == 1 and neighbors[4] == 0 and neighbors[6] == 0: #enojna stranska desna
        return 12
    if neighbors[1] == 0 and neighbors[3] == 0 and neighbors[4] == 0 and neighbors[6] == 1: #enojna vrhna
        return 13
    if neighbors[1] == 1 and neighbors[3] == 0 and neighbors[4] == 0 and neighbors[6] == 1: #enojna vertikalna
        return 14
    if neighbors[1] == 1 and neighbors[3] == 0 and neighbors[4] == 0 and neighbors[6] == 0: #enojna vrhna
        return 15
    if neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 0 and neighbors[4] == 1 and neighbors[6] == 1 and neighbors[7]== 0: #leva stranska T
        return 20
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[3] == 1 and neighbors[4] == 0 and neighbors[5] == 0 and neighbors[6]== 1: #desna stranska T
        return 21
    if neighbors[1] == 0 and neighbors[3] == 1 and neighbors[4] == 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 0: #zgornja stranska T
        return 22
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[6] == 0: #spodnja stranska T
        return 23
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce na 4
        return 24
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 1 and neighbors[6]== 1 and neighbors[7] == 1: #krizisce zgornji dve
        return 25
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce spodnji dve
        return 26
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 1 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce desni dve
        return 27
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 1: #krizisce levi dve
        return 28
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce tri - ZL
        return 29
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce tri - ZD
        return 30
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 1 and neighbors[6]== 1 and neighbors[7] == 0: #krizisce tri - SL
        return 31
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5] == 0 and neighbors[6]== 1 and neighbors[7] == 1: #krizisce tri - SD
        return 32
    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[6]== 0: #dvojna spodnja + ZD
        return 33
    if neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[6]== 0: #dvojna spodnja + ZL
        return 34
    if  neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5]== 0 and neighbors[6] == 1 and neighbors[7] == 1: #dvojna zgornja + SL
        return 35
    if  neighbors[2] == 0 and neighbors[3] == 1 and neighbors[4]== 1 and neighbors[5]== 1 and neighbors[6] == 1 and neighbors[7] == 0: #dvojna zgornja + SD
        return 36
    if  neighbors[0] == 0 and neighbors[1] == 1 and neighbors[3]== 1 and neighbors[4]== 0 and neighbors[5] == 1 and neighbors[6] == 1: #dvojna stranska + ZL
        return 37
    if  neighbors[1] == 1 and neighbors[2] == 0  and neighbors[3]== 0 and neighbors[4]== 1 and neighbors[6] == 1 and neighbors[7] == 1: #dvojna stranska + ZD
        return 38
    if  neighbors[0] == 1 and neighbors[1] == 1 and neighbors[3]== 1 and neighbors[4]== 0 and neighbors[5] == 0 and neighbors[6] == 1: #dvojna stranska + SL
        return 39
    if  neighbors[1] == 1 and neighbors[2] == 1  and neighbors[3]== 0 and neighbors[4]== 1 and neighbors[6] == 1 and neighbors[7] == 0: #dvojna stranska + SD
        return 40
    if  neighbors[0] == 0 and neighbors[1] == 1  and neighbors[2]== 1 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7] == 1: #samo ZL
        return 41
    if  neighbors[0] == 1 and neighbors[1] == 1  and neighbors[2]== 0 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7] == 1: #samo ZD
        return 42
    if  neighbors[0] == 1 and neighbors[1] == 1  and neighbors[2]== 1 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 0 and neighbors[6] == 1 and neighbors[7] == 1: #samo SL
        return 43
    if  neighbors[0] == 1 and neighbors[1] == 1  and neighbors[2]== 1 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7] == 0: #samo SD
        return 44
    if  neighbors[0] == 0 and neighbors[1] == 1  and neighbors[2]== 1 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 1 and neighbors[6] == 1 and neighbors[7] == 0: #diagonala ZL in SD
        return 45
    if  neighbors[0] == 1 and neighbors[1] == 1  and neighbors[2]== 0 and neighbors[3]== 1 and neighbors[4] == 1 and neighbors[5] == 0 and neighbors[6] == 1 and neighbors[7] == 1: #iagonala ZD in SL
        return 46
    return 0 #prepisi da bo ku binary tree?

def dynamic_bg_pos(input_pos:tuple [int, int], bg_image:pygame.Surface, opposite_dir:bool = True, manual_offset:tuple [int, int] = (0, 0)):
    """Returns tuple containing positions for images to offset background"""
    
    bg_pos = [0, 0]
    image_width, image_height = bg_image.get_size()
    
    # We check in which direction image fits tighter (smaller overflow %) and use the tighter direction to calculate displacement_koeficient
    if image_width / SCREEN_WIDTH > image_height / SCREEN_HEIGHT:
        displacement_koeficient = (image_height - SCREEN_HEIGHT) / SCREEN_HEIGHT
    else:
        displacement_koeficient = (image_width - SCREEN_WIDTH) / SCREEN_WIDTH

    # Coordinates where to draw image so that is centered
    coordiante_for_center_x = ((image_width - SCREEN_WIDTH) / 2) * -1
    coordiante_for_center_y = ((image_height - SCREEN_HEIGHT) / 2) * -1

    # The actual displacements based on provided input
    displacement_x = (SCREEN_WIDTH / 2 - input_pos[0]) * displacement_koeficient
    displacement_y = (SCREEN_HEIGHT / 2 - input_pos[1]) * displacement_koeficient

    # We calculate actual image coordinates
    if opposite_dir:
        bg_pos[0] = coordiante_for_center_x + displacement_x 
        bg_pos[1] = coordiante_for_center_y + displacement_y
    else:
        bg_pos[0] = coordiante_for_center_x - displacement_x
        bg_pos[1] = coordiante_for_center_y - displacement_y

    # If given, we manually offset image (if not given it's (0, 0))
    bg_pos[0] += manual_offset[0]
    bg_pos[1] += manual_offset[1]

    return bg_pos

def set_permission_to_interact(mouse_pos:tuple[int, int], ui_elements:list):
    # List of all elements that have colliding point (are overlapping) on that point 
    colliding_elements = []
    # If item collides we add it to list of colliding points and disable it
    for object in ui_elements:
        if object.rect.collidepoint(mouse_pos):
            colliding_elements.append(object)
            object.interactable = False
        else:
            object.interactable = True

    if colliding_elements:
        colliding_elements[0].interactable = True

def draw_scene(scene:str, screen:pygame.Surface, scaled_bgs:list, ui_bgs:list, current_level:int = 0, delta_time:float = 0, events = []):
    """Handles drawing scenes"""
    if scene == "login":
        screen.blit(ui_bgs["login"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["login"], False, manual_offset = (-150, 0)))
        objs.submit_button.draw(screen)
        objs.quit_button.draw(screen)
        objs.username_input.draw(screen, delta_time)
        objs.password_input.draw(screen, delta_time)
        objs.submit_text.draw(screen)
        objs.quit_text.draw(screen) # Za ta tekst naredi da se narise ze ku poklices button funkcijo (da je kar part od buttona)
        # objs.cursor.draw(screen, delta_time)
        objs.campaign_dropdown.draw(screen, events)
        objs.notification.draw(screen)
    
    elif scene == "main_menu":
        screen.blit(ui_bgs["main_menu"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["main_menu"], False, manual_offset = (-150, 0)))
        objs.play_button.draw(screen)
        objs.quit_button.draw(screen)
        objs.logout_button.draw(screen)
        objs.title.draw(screen)
        objs.play_text.draw(screen)
        objs.quit_text.draw(screen)
        objs.logout_text.draw(screen)
        objs.notification.draw(screen)

    elif scene == "running":
        screen.blit(scaled_bgs[current_level], dynamic_bg_pos(objs.player.get_pos(center_pos = True), scaled_bgs[current_level]))
        screen.blit(objs.level_surfaces[current_level], (0, 0))
        objs.player.draw(screen)
        objs.babe.draw(screen, current_level)
        objs.timer_text.draw(screen)
        objs.FPS_text.draw(screen)
        objs.notification.draw(screen)
    
    elif scene == "endscreen":
        screen.blit(ui_bgs["endscreen"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["endscreen"], False))
        objs.notification.draw(screen)

# MANAGING PLAYER STATS
def save_player_stats(PLAYER_NAME:str, saving_reason:str = ""):
    """Saves player stats to its corresponding file"""
    os.makedirs(stats_folder, exist_ok=True)
    
    if saving_reason == "game_ended":
        update_player_stats()
    elif saving_reason == "ragequit":
        update_player_stats(True)

    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")
    
    with open(filepath, "w") as file:
        json.dump(conf.stats, file, indent = 4)

def load_player_stats(PLAYER_NAME:str):
    """Loads player stats from its corresponding file"""
    is_new_player = False

    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")

    loaded_stats = load_json(filepath)
    if loaded_stats:
        conf.stats.clear()
        conf.stats.update(loaded_stats)
    
    else:
        # If the player's stats file doesn't exist (new player)
        for stat in def_stats:
            conf.stats[stat] = def_stats[stat]
            is_new_player = True
    
    #ce trenutno v stats.json ni neke vrednosti (smo na novo uvedli/ponesreci zbrisana), jo nastavimo na fallback vrednost
    for key, value in def_stats.items():
        if key not in conf.stats:
            conf.stats[key] = value
    
    return is_new_player

def wipe_stats(PLAYER_NAME:str, stats:list, def_stats:list):
    """Resets all player values to value in def_stats and saves them"""
    for stat in stats:
        stats[stat] = def_stats[stat]
    save_player_stats(PLAYER_NAME, stats)

def update_player_stats(ragequitting:bool = False):
    """Updates player stats based on stats from his last game"""
    #tle do pravila za use statse kku se jih zdruzuje

    # These values will update even if we ragequit, because they must/can be updated without risk
    conf.stats["total_jumps"] += conf.game_stats["jumps"]
    conf.stats["total_falls"] += conf.game_stats["falls"]
    
    conf.stats["max_jumps_in_game"] = max(conf.game_stats["jumps"], conf.stats["max_jumps_in_game"])
    conf.stats["max_falls_in_game"] = max(conf.game_stats["falls"], conf.stats["max_falls_in_game"])
    
    conf.stats["head_bounces"] += conf.game_stats["head_bounces"]
    conf.stats["wall_bounces"] += conf.game_stats["wall_bounces"]
    
    conf.stats["best_screen"] = max(conf.game_stats["best_screen"], conf.stats["best_screen"])
    
    conf.stats["total_distance_climbed"] += conf.game_stats["distance_climbed"]
    conf.stats["total_distance_descended"] += conf.game_stats["distance_descended"]
    
    conf.stats["highest_distance_climbed_in_game"] = max(conf.game_stats["distance_climbed"], conf.stats["highest_distance_climbed_in_game"])
    conf.stats["highest_distance_descended_in_game"] = max(conf.game_stats["distance_descended"], conf.stats["highest_distance_descended_in_game"])
    
    # Values below will only save/update if we reached end of campaign
    if ragequitting:
        return

    conf.stats["min_jumps_in_game"] = min(conf.game_stats["jumps"], conf.stats["min_jumps_in_game"])
    conf.stats["min_falls_in_game"] = min(conf.game_stats["falls"], conf.stats["min_falls_in_game"])

# LEVELS
def make_levels(tile_images:list):
    objs.levels, objs.level_surfaces = [], []
    for i in range(len(conf.level_paths)):
        platforms = create_level(load_level_from_file(i))
        objs.levels.append(platforms)
        objs.level_surfaces.append(create_level_surface(platforms, tile_images))

def list_current_folder(path:str):
    """Walks the current folder and outputs all items in that folder"""
    if not os.path.exists(path):
        return "", [], []

    dirs = []
    files = []

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                dirs.append(entry.name)
            elif entry.is_file():
                files.append(entry.name)
    return path, dirs, files

def detect_levels():
    """Goes trough all files in given folder and adds them to list of levels *(ordered alphabetically)*"""
    conf.level_paths = []

    if conf.CAMPAIGN != "":
        filepath = os.path.join(campaigns_folder, conf.CAMPAIGN, "levels")
    else:
        filepath = os.path.join(campaigns_folder, "levels")

    root, dirs, files = list_current_folder(filepath)
    
    if not files:
        print(messages["err_empty_campaign"])
        filepath = os.path.join(campaigns_folder, "levels")
        root, dirs, files = list_current_folder(filepath)

    for file in files:
        if file.endswith(".txt"):
            conf.level_paths.append(os.path.join(filepath, file))
    conf.level_paths.sort()

def load_level_from_file(level_number:int):
    """Based on ***level_number*** loads level data from file to list named ***level***"""

    level = []
    with open(conf.level_paths[level_number], 'r') as file:
        for line_number, line in enumerate(file, start = 1):
            row = []
            for char in line.strip():
                if char.isdigit():
                    row.append(int(char))
            level.append(row)
    return level

def create_level(level_data:list):
    """Based on list ***level_data***, which has level data stored inside creates level *(all the platforms for that level)*"""

    rows = len(level_data)
    cols = len(level_data[0]) if rows > 0 else 0
    platforms = []
    relative_offfsets = [ 
        (-1, -1),   (0, -1),    (1, -1),
        (-1, 0),                (1, 0),
        (-1, 1),    (0, 1),     (1, 1)
    ]
    for row_index, row in enumerate(level_data):
        for col_index, col in enumerate(row):
            if col != 0:
                neighbors = []
                for relative_x, relative_y in relative_offfsets:
                    offset_row, offset_col = row_index + relative_y, col_index + relative_x # dejanski offseti
                    if (offset_row >= 0 and offset_row < rows) and (offset_col >= 0 and offset_col < cols):
                        neighbors.append(level_data[offset_row][offset_col])
                    else:
                        neighbors.append(0)
                platforms.append(platform.Platform(col_index * tile_size, row_index * tile_size, tile_size, tile_size, autotile(neighbors)))
    return platforms 

def create_level_surface(level:object, tile_images:list):
    """Creates level surface by combining all platforms/tiles into one surface"""
    level_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for platform in level:
        level_surface.blit(tile_images[platform.type], (platform.rect.x, platform.rect.y))

    return level_surface

def slice_level(last_level:list, tile_size:int, min_row_length:int):
    """Slice given level into horizontal rows of tiles and return list of rows (which are lists of tiles)"""
    level_rows = []
    last_row_start_index = 0
    row_length = 0

    # We dont need to check the last (min_row_length - 1) tiles as they can't 
    # have enough neighbours to form suitable platforms for babe to stand on
    for i in range(len(last_level) - (min_row_length - 1)): 
        if i - last_row_start_index < row_length: # If we already included that platform in previous row, we skip it this time
            continue
        
        platform = last_level[i]
        current_row = [platform]

        # Then we check all following tiles
        for j in range(i + 1, len(last_level)):
            next_platform = last_level[j]
            same_row = next_platform.rect.y == platform.rect.y and next_platform.rect.x - tile_size * (j - i) == platform.rect.x
            last_tile = j == len(last_level) - 1

            # If the tile is part of the current row, we add it to current row
            if same_row:
                current_row.append(next_platform)
            
            # If the tile is not part of the same row, or if it's the last tile, we finalize the row
            if not same_row or last_tile:
                last_row_start_index = i
                row_length = len(current_row)
                break
                
        level_rows.append(current_row)

    return level_rows

def find_valid_subrows(tiles:list, level_rows:list, platform_index:int, platform_area:pygame.rect.Rect, min_row_length:int):
    is_colliding_with_any_platform = False
    occupied_subrows = []
    
    # We check for colliding with all previous platforms
    for testing_platform_index in range(platform_index):
        test_tiles = level_rows[testing_platform_index]

        # For each previous platform we create area, that the platform occupies
        test_platform_area = pygame.rect.Rect(test_tiles[0].rect.x, test_tiles[0].rect.y, len(test_tiles) * tile_size, tile_size) # We create an area of platform
        
        # If the spaces collide we try searching for sub-area of the platform that is longer than min_row_length and not covered
        if platform_area.colliderect(test_platform_area):
            current_subrow = []

            for tile_index in range(len(tiles)):
                tile_pos = (tiles[tile_index].rect.x, tiles[tile_index].rect.y)
                
                # For each tile of the platform, we check all three tiles above it, 
                # to see if any of those collides with current platform we are testing against
                is_space_above_colliding = test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - tile_size) or test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - 2 * tile_size) or test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - 3 * tile_size)

                # If any of 3 above spaces is in the way, we add that tile to current_subrow of occupied tiles
                if is_space_above_colliding:
                    current_subrow.append(tiles[tile_index])

                # If all 3 spaces above are free, that tile is free
                # our current_subrow untill now should be added to occupied_subrows,
                # and we should start over with current_subrows
                else:
                    if len(current_subrow) > 0:
                        occupied_subrows.append(current_subrow)
                    current_subrow = []
            
            # If we reach the last tile, we also need to check what we have got until now
            if len(current_subrow) > 0:#= min_row_length:
                occupied_subrows.append(current_subrow)
    
    valid_subrows = combine_subrows(occupied_subrows, tiles, min_row_length)

    return valid_subrows

def combine_subrows(occupied_subrows: list, platform:list, min_row_length:int):
    """Out of all occupied_subrows we project occupied tiles on initial platform, and then form valid subrows from this projection"""
    valid_subrows = []
    invalid_tiles = []
    current_valid_subrow = []

    #If there are no subrows of occupied platform tiles (platform is all good), we just return it
    if not occupied_subrows:
        return platform

    # For each subrow of occupied_subrows (which there are)
    for subrow in occupied_subrows:
        # We check each tile against all platform_tiles
        for subrow_tile in subrow:
            for platform_tile in platform:
                # If our occupied_subrow and platform tile have the same x coordinate, that means that this platform tile is invalid (occupied)
                # If this platform tile is invalid, we add it to the list of ivalid tiles, but only if it hasn't occurred yet
                if subrow_tile.rect.x == platform_tile.rect.x and invalid_tiles.count(platform_tile) == 0:
                    invalid_tiles.append(platform_tile)

    # For each platform tile we check if it appears in invalid_tiles
    for platform_tile_index in range(len(platform)):
        platform_tile = platform[platform_tile_index]
        is_platform_tile_valid = True
        for invalid_platform in invalid_tiles:
            # If current_platform_tile appears in invalid_tiles, we add our current_valid_subrow to valid_subrows (if it's long enough), and start finding new current_valid_subrow
            if platform_tile.rect.x == invalid_platform.rect.x:
                is_platform_tile_valid = False
                break
        
        if is_platform_tile_valid:
            current_valid_subrow.append(platform_tile)
        else:
            if len(current_valid_subrow) >= min_row_length:
                valid_subrows.append(current_valid_subrow)
            current_valid_subrow = []
        
        # If we encounter the last tile, we also need to check whether we have suitable subrows!
        if platform_tile_index == len(platform) - 1:
            if len(current_valid_subrow) >= min_row_length:
                valid_subrows.append(current_valid_subrow)
            current_valid_subrow = []

    return valid_subrows

# LOADING GAME FILES
def load_json(filepath:str):
    """Tries loading JSON file, if it fails returns False."""
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return False

def set_config_values(filepath:str):
    config = load_json(filepath)
    py_objs.level_musics = config.get("levels_music", [])
    py_objs.menu_musics = config.get("ui_music", {"login": "", "main_menu": "", "endscreen": ""})
    py_objs.bgs_images_paths = config.get("game_backgrounds", [])
    py_objs.ui_bgs_images_paths = config.get("ui_backgrounds", {"login": "", "main_menu": "", "endscreen": ""})
    py_objs.icon_name = config.get("icon")
    py_objs.babe_position = config.get("babe_position", [])

def find_background_load_size(image:pygame.surface.Surface, bg_resize_koeficient:float = 1):
    """Find image size in order to fit the whole screen"""
    image_size = image.get_size()

    # Ratios between width and height
    scale = max(SCREEN_WIDTH / image_size[0], SCREEN_HEIGHT / image_size[1])
    size = (image_size[0] * scale * bg_resize_koeficient, image_size[1] * scale * bg_resize_koeficient)

    return size

def load_image(filepath:str, subfolder:str, resources_folder:str, fallback_resources_folder:str, size:tuple[int, int] = [], preserve_alpha:bool = False, auto_scale:bool = False, flip_x:bool = False, flip_y:bool = False):
    path = os.path.join(resources_folder, subfolder, filepath)
    fallback_path = os.path.join(fallback_resources_folder, subfolder, filepath)
    found_image = False

    for format in SUPPORTED_IMAGE_FORMATS:
        current_path = path + format
        if os.path.exists(current_path):
            image = pygame.transform.flip(pygame.image.load(current_path), flip_x, flip_y)
            found_image = True

    if not found_image:
        for format in SUPPORTED_IMAGE_FORMATS:
            current_path = fallback_path + format
            if os.path.exists(current_path):
                image = pygame.transform.flip(pygame.image.load(current_path), flip_x, flip_y)
                found_image = True

    if not found_image:
        print("Couldn't load image")
        return
    
    # If we are given a list of sizes we use this, otherwise if we want to auto scale we call find_background_load_size(). If non of the above we leave default size
    if not size and auto_scale:
        size = find_background_load_size(image, bg_resize_koeficient)

    if size:
        image = pygame.transform.scale(image, size)

    if preserve_alpha:
        return image.convert_alpha()
    return image.convert()

def load_font(path:str, fallback_path:str, size:int):
    if os.path.exists(path):
        font = pygame.font.Font(path, size)
    
    elif os.path.exists(fallback_path):
        font = pygame.font.Font(fallback_path, size)

    else:
        font = pygame.font.Font(None, size)
    
    return font

def load_sfx(filepath:str, subfolder:str, format:str, resources_folder:str, fallback_resources_folder:str):
    path = os.path.join(resources_folder, subfolder, filepath + format)
    fallback_path = os.path.join(fallback_resources_folder, subfolder, filepath + format)

    if os.path.exists(path):
        sfx = pygame.mixer.Sound(path)
    elif os.path.exists(fallback_path):
        sfx = pygame.mixer.Sound(fallback_path)
    else:
        print("Couldn't load sound effects")

    return sfx

def load_resources():
    resources_folder = os.path.join("campaigns", conf.CAMPAIGN, "resources")

    set_config_values(filepath = os.path.join("campaigns", conf.CAMPAIGN, "config.json"))
    conf.current_level = 0

    tile_images = []
    for i in range(len(tile_images_paths)):
        tile_images.append(None)
        tile_images[i] = load_image(tile_images_paths[i], "tiles", resources_folder, fallback_resources_folder, (tile_size, tile_size), True)

    player_images = []
    for i in range(len(player_images_paths)):
        player_images.append(None)
        player_images[i] = load_image(player_images_paths[i], "player_animation", resources_folder, fallback_resources_folder, (80, 80), True)

    babe_images = []
    for i in range(len(babe_images_paths)):
        babe_images.append(None)
        babe_images[i] = load_image(babe_images_paths[i], "babe_animation", resources_folder, fallback_resources_folder, (80, 80), True)

    buttons = []
    for i in range(len(button_images_paths)):
        buttons.append(None)
        buttons[i] = load_image(button_images_paths[i], "other", resources_folder, fallback_resources_folder, conf.button_load_sizes[i], True)

    scaled_bgs = []
    # We load all of the bgs images paths, if there are too few bgs specified, we duplicate the last one
    for i in range(len(conf.level_paths)):
        scaled_bgs.append(None)
        scaled_bgs[i] = load_image(py_objs.bgs_images_paths[min(i, len(py_objs.bgs_images_paths) - 1)], "bgs", resources_folder, fallback_resources_folder, (), False, True)

    ui_bgs = {}
    for key, value in py_objs.ui_bgs_images_paths.items():
        ui_bgs[key] = load_image(value, "bgs", resources_folder, fallback_resources_folder, (), False, True)

    sfx = {}
    for i in range(len(conf.sfx_keys)):
        sfx[conf.sfx_keys[i]] = load_sfx(conf.sfx_keys[i], "sfx", ".wav", resources_folder, fallback_resources_folder)

    fonts = {}
    for i in range(len(conf.fonts_keys)):
        fonts[conf.fonts_keys[i]] = load_font(os.path.join(resources_folder, "other", conf.fonts_names[i] + ".otf"), os.path.join(fallback_resources_folder, "other", conf.fonts_names[i] + ".otf"), conf.fonts_sizes[i])

    detect_levels()
    make_levels(tile_images)

    return tile_images, player_images, babe_images, buttons, scaled_bgs, ui_bgs, sfx, fonts
