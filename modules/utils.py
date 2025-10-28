import os, json, hashlib, pygame

import modules.platform as platform
import modules.pygame_objects as py_objs
import modules.objects as objs
import modules.config as conf

#MISCELANEOUS
def log_in(username:str, password:str, title:str, effect:object, username_input:str, password_input:str, username_text:str, password_text:str, stats:list):
    """Handles user login and account creation based on provided inputs."""

    load_player_stats(username, stats)
    if username != "" and username.lower() != "guest":
        if stats.get("password", 0) == 0:
            stats["password"] = hash_password(password)
            title.text = f"Welcome, {username}!"
            title.update()
            effect.start_fade_out()
            return "main_menu"
        
        #if the password is incorrect
        elif hash_password(password) != stats["password"]:
                username_input.input_text = ""
                password_input.input_text = ""
                password_input.masked_text = ""
                username_text.text = ""
                password_text.text = ""
                username_text.update()
                password_text.update()
        else:
            title.text = f"Welcome back, {username}!"
            title.update()
            effect.start_fade_out()
            return "main_menu"
    else:
        title.text = "Welcome!"
        title.update()
        effect.start_fade_out()
        return "main_menu"
        
    save_player_stats(username, stats)

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

def dynamic_bg_pos(input_pos:tuple [int, int], bg_image:pygame.Surface, opposite_dir:bool = True, offset:tuple [int, int] = (0, 0)):
    """Returns tuple containing positions for images to offset background"""
    
    bg_pos = [0, 0]
    if bg_image.get_width() / conf.SCREEN_WIDTH > bg_image.get_height() / conf.SCREEN_HEIGHT:
        displacement_koeficient = (bg_image.get_height() - conf.SCREEN_HEIGHT) / conf.SCREEN_HEIGHT #should automatically set correct koeficient so that the bg doesnt move too much
    else:
        displacement_koeficient = (bg_image.get_width() - conf.SCREEN_WIDTH) / conf.SCREEN_WIDTH

    if not opposite_dir:
        bg_pos[0] = (((bg_image.get_width() - conf.SCREEN_WIDTH) // 2) * -1) - (((conf.SCREEN_WIDTH / 2 - input_pos[0])) * displacement_koeficient) + (offset[0] / 2)
        bg_pos[1] = (((bg_image.get_height() - conf.SCREEN_HEIGHT) // 2) * -1) - (((conf.SCREEN_HEIGHT / 2 - input_pos[1])) * displacement_koeficient) + (offset[1] / 2)
    else:
        bg_pos[0] = (((bg_image.get_width() - conf.SCREEN_WIDTH) // 2) * -1) + (((conf.SCREEN_WIDTH / 2 - input_pos[0])) * displacement_koeficient) + (offset[0] / 2)
        bg_pos[1] = (((bg_image.get_height() - conf.SCREEN_HEIGHT) // 2) * -1) + (((conf.SCREEN_HEIGHT / 2 - input_pos[1])) * displacement_koeficient) + (offset[1] / 2)

    return (bg_pos[0], bg_pos[1])

def draw_scene(scene:str, screen:pygame.Surface, scaled_bgs:list, ui_bgs:list, current_level:int = 0, delta_time:float = 0):
    """Handles drawing scenes"""

    if scene == "main_menu":
        screen.blit(ui_bgs["main_menu"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["main_menu"], False, (-300, 0)))
        objs.play_button.draw(screen)
        objs.quit_button.draw(screen)
        objs.logout_button.draw(screen)
        objs.title.draw(screen)
        objs.play_text.draw(screen)
        objs.quit_text.draw(screen)
        objs.logout_text.draw(screen)
        objs.notification.draw(screen)

    elif scene == "running":
        screen.blit(scaled_bgs[current_level], dynamic_bg_pos(objs.player.get_center_pos(), scaled_bgs[current_level]))
        screen.blit(objs.level_surfaces[current_level], (0, 0))
        objs.player.draw(screen)
        objs.main_babe.draw(screen, current_level, delta_time)
        objs.timer_text.draw(screen)
        objs.FPS_text.draw(screen)
        objs.notification.draw(screen)
    
    elif scene == "endscreen":
        screen.blit(ui_bgs["endscreen"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["endscreen"], False))
        objs.notification.draw(screen)

    elif scene == "login":
        screen.blit(ui_bgs["login"], dynamic_bg_pos(pygame.mouse.get_pos(), ui_bgs["login"], False, (-300, 0))) #(-600, 0)
        objs.submit_button.draw(screen)
        objs.quit_button.draw(screen)
        objs.username_input.draw(screen)
        objs.password_input.draw(screen)
        objs.submit_text.draw(screen)
        objs.quit_text.draw(screen) # Za ta tekst naredi da se narise ze ku poklices button funkcijo (da je kar part od buttona)
        objs.username_text.draw(screen)
        objs.password_text.draw(screen)
        objs.cursor.draw(screen, delta_time)
        objs.campaign_dropdown.draw(screen)
        objs.notification.draw(screen)

# MANAGING PLAYER STATS
def save_player_stats(PLAYER_NAME:str, stats:list):
    """Saves player stats to its corresponding file"""
    os.makedirs(conf.stats_folder, exist_ok=True)
    update_player_stats(stats)

    if PLAYER_NAME != "":
        filepath = os.path.join(conf.stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(conf.stats_folder, "guest_stats.json")
    
    with open(filepath, "w") as file:
        json.dump(stats, file, indent = 4)

def load_player_stats(PLAYER_NAME:str, stats:list):
    """Loads player stats from its corresponding file"""
    if PLAYER_NAME != "":
        filepath = os.path.join(conf.stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(conf.stats_folder, "guest_stats.json")

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            loaded_stats = json.load(file)
        stats.clear()
        stats.update(loaded_stats)
    else:
        # If the player's stats file doesn't exist (new player)
        for stat in stats:
            stats[stat] = conf.def_stats[stat]
    
    #ce trenutno v stats.json ni neke vrednosti (smo na novo uvedli/ponesreci zbrisana), jo nastavimo na fallback vrednost
    for key, value in conf.def_stats.items():
        if key not in stats:
            stats[key] = value

def wipe_stats(PLAYER_NAME:str, stats:list, def_stats:list):
    """Resets all player values to 0 and saves them"""
    for stat in stats:
        stats[stat] = def_stats[stat]
    save_player_stats(PLAYER_NAME, stats)

def update_player_stats(stats:list):
    """Updates player stats based on stats from his last game"""
    #tle do pravila za use statse kku se jih zdruzuje
    stats["total_jumps"] += conf.game_stats["jumps"]
    if stats["min_jumps_in_game"] > conf.game_stats["jumps"]:
        stats["min_jumps_in_game"] = conf.game_stats["jumps"]
    if stats["max_jumps_in_game"] < conf.game_stats["jumps"]:
        stats["max_jumps_in_game"] = conf.game_stats["jumps"]
    
    stats["total_falls"] += conf.game_stats["falls"]
    if stats["min_falls_in_game"] > conf.game_stats["falls"]:
        stats["min_falls_in_game"] = conf.game_stats["falls"]
    if stats["max_falls_in_game"] < conf.game_stats["falls"]:
        stats["max_falls_in_game"] = conf.game_stats["falls"]
    
    stats["head_bounces"] += conf.game_stats["head_bounces"]
    stats["wall_bounces"] += conf.game_stats["wall_bounces"]
    
    if stats["best_screen"] < conf.game_stats["best_screen"]:
        stats["best_screen"] = conf.game_stats["best_screen"]

    stats["total_distance_climbed"] += conf.game_stats["distance_climbed"]
    stats["total_distance_descended"] += conf.game_stats["distance_descended"]
    if stats["highest_distance_climbed_in_game"] < conf.game_stats["distance_climbed"]:
        stats["highest_distance_climbed_in_game"] = conf.game_stats["distance_climbed"]
    if stats["highest_distance_descended_in_game"] < conf.game_stats["distance_descended"]:
        stats["highest_distance_descended_in_game"] = conf.game_stats["distance_descended"]

# LEVELS
def make_levels(tile_images:list):
    #conf.level_paths = detect_levels()

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
        filepath = os.path.join(conf.campaigns_folder, conf.CAMPAIGN, "levels")
    else:
        filepath = os.path.join(conf.campaigns_folder, "levels")

    root, dirs, files = list_current_folder(filepath)
    
    if not files: #tu je za zdej, dokler ne nardim dropdown al neki za zbirat campaign!!
        print(conf.messages["err_empty_campaign"])
        filepath = f"{conf.campaigns_folder}"
        root, dirs, files = list_current_folder(filepath)

    for file in files:
        if file.endswith(".txt"):
            conf.level_paths.append(f"{filepath}/{file}")
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
                platforms.append(platform.Platform(col_index * conf.tile_size, row_index * conf.tile_size, conf.tile_size, conf.tile_size, autotile(neighbors)))
    return platforms 

def create_level_surface(level:object, tile_images:list):
    """Creates level surface by combining all platforms/tiles into one surface"""
    level_surface = pygame.Surface((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT), pygame.SRCALPHA)

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
        test_platform_area = pygame.rect.Rect(test_tiles[0].rect.x, test_tiles[0].rect.y, len(test_tiles) * conf.tile_size, conf.tile_size) # We create an area of platform
        
        # If the spaces collide we try searching for sub-area of the platform that is longer than min_row_length and not covered
        if platform_area.colliderect(test_platform_area):
            current_subrow = []

            for tile_index in range(len(tiles)):
                tile_pos = (tiles[tile_index].rect.x, tiles[tile_index].rect.y)
                
                # For each tile of the platform, we check all three tiles above it, 
                # to see if any of those collides with current platform we are testing against
                is_space_above_colliding = test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - conf.tile_size) or test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - 2 * conf.tile_size) or test_platform_area.collidepoint(tile_pos[0], tile_pos[1] - 3 * conf.tile_size)

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
def load_config():
    if conf.CAMPAIGN:
        filepath = os.path.join(conf.campaigns_folder, conf.CAMPAIGN, "config.json")
    else:
        filepath = os.path.join(conf.campaigns_folder, "config.json")

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)

def set_config_values():
    config = load_config()
    py_objs.music_level_instructions = config.get("levels_music", [])
    py_objs.music_menus_instructions = config.get("ui_music", {"login": "", "main_menu": "", "endscreen": ""})
    py_objs.bgs_images_paths = config.get("game_backgrounds", [])
    py_objs.ui_bgs_images_paths = config.get("ui_backgrounds", {"login": "", "main_menu": "", "endscreen": ""})
    py_objs.icon_name = config.get("icon")
    py_objs.babe_position = config.get("babe_position", [])

def load_image(filepath:str, subfolder:str, resources_folder:str, fallback_resources_folder:str, size:tuple[int, int], preserve_alpha:bool = False, flip_x:bool = False, flip_y:bool = False):
    from modules.config import SUPPORTED_IMAGE_FORMATS
    
    path = os.path.join(resources_folder, subfolder, filepath)
    fallback_path = os.path.join(fallback_resources_folder, subfolder, filepath)
    found_image = False

    for format in SUPPORTED_IMAGE_FORMATS:
        if os.path.exists(f"{path}{format}"):
            image = pygame.transform.flip(pygame.image.load(f"{path}{format}"), flip_x, flip_y)
            found_image = True
    
    if not found_image:
        for format in SUPPORTED_IMAGE_FORMATS:
            if os.path.exists(f"{fallback_path}{format}"):
                image = pygame.transform.flip(pygame.image.load(f"{fallback_path}{format}"), flip_x, flip_y)
                found_image = True
    
    if not found_image:
        print("Couldn't load image")
        return

    if size[0] != 0 and size[1] != 0:
        image = pygame.transform.scale(image, size)

    if preserve_alpha:
        return image.convert_alpha()
    else:
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

    set_config_values()
    conf.current_level = 0

    # zloadamo s campaign resources
    tile_images = []
    for i in range(len(conf.tile_images_paths)):
        tile_images.append(None)
        tile_images[i] = load_image(conf.tile_images_paths[i], "tiles", resources_folder, conf.fallback_resources_folder, (conf.tile_size, conf.tile_size), True)

    player_images = []
    for i in range(len(conf.player_images_paths)):
        player_images.append(None)
        player_images[i] = load_image(conf.player_images_paths[i], "player_animation", resources_folder, conf.fallback_resources_folder, (80, 80), True)

    babe_images = []
    for i in range(len(conf.babe_images_paths)):
        babe_images.append(None)
        babe_images[i] = load_image(conf.babe_images_paths[i], "babe_animation", resources_folder, conf.fallback_resources_folder, (80, 80), True)

    buttons = []
    for i in range(len(conf.button_images_paths)):
        buttons.append(None)
        buttons[i] = load_image(conf.button_images_paths[i], "other", resources_folder, conf.fallback_resources_folder, conf.button_load_sizes[i], True)

    scaled_bgs = []
    for i in range(len(py_objs.bgs_images_paths)):
        scaled_bgs.append(None)
        scaled_bgs[i] = load_image(py_objs.bgs_images_paths[i], "bgs", resources_folder, conf.fallback_resources_folder, (1778 * conf.bg_resize_koeficient, 1000 * conf.bg_resize_koeficient))

    ui_bgs = {}
    for key, value in py_objs.ui_bgs_images_paths.items():
        ui_bgs[key] = load_image(value, "bgs", resources_folder, conf.fallback_resources_folder, conf.ui_bgs_sizes[key])

    sfx = {}
    for i in range(len(conf.sfx_keys)):
        sfx[conf.sfx_keys[i]] = load_sfx(conf.sfx_keys[i], "sfx", ".wav", resources_folder, conf.fallback_resources_folder)

    fonts = {}
    for i in range(len(conf.fonts_keys)):
        fonts[conf.fonts_keys[i]] = load_font(f"{resources_folder}/other/{conf.fonts_names[i]}.otf", f"{conf.fallback_resources_folder}/other/{conf.fonts_names[i]}.otf", conf.fonts_sizes[i])

    detect_levels()
    make_levels(tile_images)

    return tile_images, player_images, babe_images, buttons, scaled_bgs, ui_bgs, sfx, fonts
        