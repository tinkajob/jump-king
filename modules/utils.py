import os, json, hashlib, pygame

from modules.config import level_paths, tile_size, stats_folder, def_stats, game_stats, SCREEN_HEIGHT, SCREEN_WIDTH, campaigns_folder, messages, bg_resize_koeficient
from modules.platform import Platform
import modules.objects as objects
#from modules.pygame_objects import endscreens, scaled_bgs, tile_images

def log_in(username:str, password:str, title:str, effect:object, username_input:str, password_input:str, username_text:str, password_text:str, stats:list):
    """Handles user login and account creation based on provided inputs."""

    load_player_stats(username, stats)
    if username != "" and username.lower() != "guest": #ce je player
        if stats.get("password", 0) == 0:
            stats["password"] = hash_password(password)
            title.text = f"Welcome, {username}!"
            title.update()
            effect.start_fade_out()
            return "main_menu"
        
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

def load_level_from_file(level_number:int):
    """Based on ***level_number*** loads level data from file to list named ***level***"""

    level = []
    with open(level_paths[level_number], 'r') as file:
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
                platforms.append(Platform(col_index * tile_size, row_index * tile_size, tile_size, tile_size, autotile(neighbors)))
    return platforms 

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

def draw_scene(scene:str, screen:pygame.Surface, scaled_bgs:list, endscreens:list, current_level:int = 0, delta_time:float = 0):
    """Handles drawing scenes"""

    if scene == "main_menu":
        screen.blit(scaled_bgs[0], dynamic_bg_pos(pygame.mouse.get_pos(), scaled_bgs[0], False, (-300, 0)))
        objects.play_button.draw(screen)
        objects.quit_button.draw(screen)
        objects.logout_button.draw(screen)
        objects.title.draw(screen)
        objects.play_text.draw(screen)
        objects.quit_text.draw(screen)
        objects.logout_text.draw(screen)
        objects.notification.draw(screen)

    elif scene == "running":
        screen.blit(scaled_bgs[current_level + 1], dynamic_bg_pos(objects.player.get_center_pos(), scaled_bgs[current_level + 1]))
        screen.blit(objects.level_surfaces[current_level], (0, 0))
        objects.player.draw(screen)
        objects.main_babe.draw(screen, current_level, delta_time)
        objects.timer_text.draw(screen)
        objects.FPS_text.draw(screen)
        objects.notification.draw(screen)
    
    elif scene == "endscreen":
        screen.blit(endscreens[0], dynamic_bg_pos(pygame.mouse.get_pos(), endscreens[0], False))
        objects.notification.draw(screen)

    elif scene == "login":
        screen.blit(scaled_bgs[0], dynamic_bg_pos(pygame.mouse.get_pos(), scaled_bgs[0], False, (-300, 0))) #(-600, 0)
        objects.submit_button.draw(screen)
        objects.quit_button.draw(screen)
        objects.username_input.draw(screen)
        objects.password_input.draw(screen)
        objects.submit_text.draw(screen)
        objects.quit_text.draw(screen)
        objects.username_text.draw(screen)
        objects.password_text.draw(screen)
        objects.cursor.draw(screen, delta_time)
        objects.notification.draw(screen)

def save_player_stats(PLAYER_NAME:str, stats:list):
    """Saves player stats to its corresponding file"""
    os.makedirs(stats_folder, exist_ok=True)
    update_player_stats(stats)

    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")
    
    with open(filepath, "w") as file:
        json.dump(stats, file, indent = 4)

def load_player_stats(PLAYER_NAME:str, stats:list):
    """Loads player stats from its corresponding file"""
    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            loaded_stats = json.load(file)
        stats.clear()
        stats.update(loaded_stats)
    else:
        for stat in stats:
            stats[stat] = 0
    
    #ce trenutno v stats.json ni neke vrednosti (smo na novo uvedli/ponesreci zbrisana), jo nastavimo na fallback vrednost
    for key, value in def_stats.items():
        if key not in stats:
            stats[key] = value

def wipe_stats(PLAYER_NAME:str, stats:list):
    """Resets all player values to 0 and saves them"""
    for stat in stats:
        stats[stat] = 0
    save_player_stats(PLAYER_NAME, stats)

def update_player_stats(stats:list):
    """Updates player stats based on stats from his last game"""
    #tle do pravila za use statse kku se jih zdruzuje
    stats["total_jumps"] += game_stats["jumps"]
    if stats["min_jumps_in_game"] > game_stats["jumps"]:
        stats["min_jumps_in_game"] = game_stats["jumps"]
    if stats["max_jumps_in_game"] < game_stats["jumps"]:
        stats["max_jumps_in_game"] = game_stats["jumps"]
    
    stats["total_falls"] += game_stats["falls"]
    if stats["min_falls_in_game"] > game_stats["falls"]:
        stats["min_falls_in_game"] = game_stats["falls"]
    if stats["max_falls_in_game"] < game_stats["falls"]:
        stats["max_falls_in_game"] = game_stats["falls"]
    
    stats["head_bounces"] += game_stats["head_bounces"]
    stats["wall_bounces"] += game_stats["wall_bounces"]
    
    if stats["best_screen"] < game_stats["best_screen"]:
        stats["best_screen"] = game_stats["best_screen"]

    stats["total_distance_climbed"] += game_stats["distance_climbed"]
    stats["total_distance_descended"] += game_stats["distance_descended"]
    if stats["highest_distance_climbed_in_game"] < game_stats["distance_climbed"]:
        stats["highest_distance_climbed_in_game"] = game_stats["distance_climbed"]
    if stats["highest_distance_descended_in_game"] < game_stats["distance_descended"]:
        stats["highest_distance_descended_in_game"] = game_stats["distance_descended"]

def detect_levels(campaign:str, campaigns_folder:str, level_paths:list):
    """Goes trough all files in given folder and adds them to list of levels *(ordered alphabetically)*"""
    if campaign != "":
        filepath = f"{campaigns_folder}/{campaign}/levels"
    else:
        filepath = f"{campaigns_folder}"

    root, dirs, files = list_current_folder(filepath)
    
    if not files: #tu je za zdej, dokler ne nardim dropdown al neki za zbirat campaign!!
        print(messages["err_empty_campaign"])
        filepath = f"{campaigns_folder}"
        root, dirs, files = list_current_folder(filepath)

    for file in files:
        if file.endswith(".txt"):
            level_paths.append(f"{filepath}/{file}")
    level_paths.sort()
    return level_paths

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

def dynamic_bg_pos(input_pos:tuple [int, int], bg_image:pygame.Surface, opposite_dir:bool = True, offset:tuple [int, int] = (0, 0)):
    """Returns tuple containing positions for images to offset background"""
    
    bg_pos = [0, 0]
    if bg_image.get_width() / SCREEN_WIDTH > bg_image.get_height() / SCREEN_HEIGHT:
        displacement_koeficient = (bg_image.get_height() - SCREEN_HEIGHT) / SCREEN_HEIGHT #should automatically set correct koeficient so that the bg doesnt move too much
    else:
        displacement_koeficient = (bg_image.get_width() - SCREEN_WIDTH) / SCREEN_WIDTH

    bg_pos[0] = (((bg_image.get_width() - SCREEN_WIDTH) // 2) * -1) + (((SCREEN_WIDTH / 2 - input_pos[0])) * displacement_koeficient) + offset[0]
    bg_pos[1] = (((bg_image.get_height() - SCREEN_HEIGHT) // 2) * -1) + (((SCREEN_HEIGHT / 2 - input_pos[1])) * displacement_koeficient) + offset[1]

    if not opposite_dir:
        bg_pos[0] = (((bg_image.get_width() - SCREEN_WIDTH) // 2) * -1) - (((SCREEN_WIDTH / 2 - input_pos[0])) * displacement_koeficient) + offset [0]
        bg_pos[1] = (((bg_image.get_height() - SCREEN_HEIGHT) // 2) * -1) - (((SCREEN_HEIGHT / 2 - input_pos[1])) * displacement_koeficient) + offset[1]

    return (bg_pos[0], bg_pos[1])

def create_level_surface(level:object, tile_images:list):
    """Creates level surface by combining all platforms/tiles into one surface"""
    level_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for platform in level:
        level_surface.blit(tile_images[platform.type], (platform.rect.x, platform.rect.y))

    return level_surface

def load_music_config(campaign:str = ""):
    """Loads music instructions based on music_config.json"""
    if campaign != "":
        filepath = f"{campaigns_folder}/{campaign}/music_config.json"
    else:
        filepath = f"{campaigns_folder}/music_config.json"

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            data = json.load(file)
            levels_config = data.get("levels", [])
            menus_config  = data.get("menus", {"login": "", "main": "", "endscreen": ""})

            objects.notification.show_notification(messages["loaded_music_config"])
    else:
        objects.notification.show_notification(messages["err_loading_music_config"])
        return [], {"login": "", "main": "", "endscreen": ""}

    return levels_config, menus_config

def load_image(path:str, fallback_path:str,scale:bool, size:tuple[int, int], preserve_alpha:bool = False, flip_x:bool = False, flip_y:bool = False):
    from modules.config import SUPPORTED_IMAGE_FORMATS
    
    found_image = False

    for format in SUPPORTED_IMAGE_FORMATS:
        if os.path.exists(f"{path}{format}"):
            image = pygame.transform.flip(pygame.image.load(f"{path}{format}"), flip_x, flip_y)
            found_image = True
    
    if not found_image:
        for format in SUPPORTED_IMAGE_FORMATS:
            if os.path.exists(f"{fallback_path}{format}"):
                image = pygame.transform.flip(pygame.image.load(f"{fallback_path}{format}"), flip_x, flip_y)
        
    if scale:
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

def load_sfx(path:str, fallback_path):
    if os.path.exists(path):
        sfx = pygame.mixer.Sound(path)
    else:
        sfx = pygame.mixer.Sound(fallback_path)
    
    return sfx

def load_resources(CAMPAIGN):
    from modules.config import fallback_resources_folder, tile_images_paths, player_images_paths, babe_images_paths, button_images_paths, button_load_sizes, bgs_images_paths, bg_resize_koeficient, endscreens_images_paths, sfx_keys, fonts_keys, fonts_sizes, fonts_names

    resources_folder = f"campaigns/{CAMPAIGN}/resources"

    # zloadamo s campaign resources
    tile_images = []
    for i in range(len(tile_images_paths)):
        tile_images.append(None)
        tile_images[i] = load_image(resources_folder + tile_images_paths[i],fallback_resources_folder + tile_images_paths[i], True, (tile_size, tile_size), True)

    player_images = []
    for i in range(len(player_images_paths)):
        player_images.append(None)
        player_images[i] = load_image(resources_folder + player_images_paths[i], fallback_resources_folder + player_images_paths[i], True, (80, 80), True)

    babe_images = []
    for i in range(len(babe_images_paths)):
        babe_images.append(None)
        babe_images[i] = load_image(resources_folder + babe_images_paths[i], fallback_resources_folder + babe_images_paths[i], True, (80, 80), True)

    buttons = []
    for i in range(len(button_images_paths)):
        buttons.append(None)
        buttons[i] = load_image(resources_folder + button_images_paths[i], fallback_resources_folder + button_images_paths[i], True, button_load_sizes[i], True)

    scaled_bgs = []
    for i in range(len(bgs_images_paths)):
        scaled_bgs.append(None)
        scaled_bgs[i] = load_image(resources_folder + bgs_images_paths[i], fallback_resources_folder + bgs_images_paths[i], True, (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient))

    endscreens = []
    for i in range(len(endscreens_images_paths)):
        endscreens.append(None)
        endscreens[i] = load_image(resources_folder + endscreens_images_paths[i], fallback_resources_folder + endscreens_images_paths[i], True, (1332 * bg_resize_koeficient, 1000 * bg_resize_koeficient))

    sfx = {}
    for i in range(len(sfx_keys)):
        sfx[sfx_keys[i]] = load_sfx(f"{resources_folder}/sfx/{sfx_keys[i]}.wav", f"{fallback_resources_folder}/sfx/{sfx_keys[i]}.wav")

    fonts = {}
    for i in range(len(fonts_keys)):
        fonts[fonts_keys[i]] = load_font(f"{resources_folder}/other/{fonts_names[i]}.otf", f"{fallback_resources_folder}/other/{fonts_names[i]}.otf", fonts_sizes[i])

    return tile_images, player_images, babe_images, buttons, scaled_bgs, endscreens, sfx, fonts
        