#============================= OTHER =============================
SCREEN_WIDTH, SCREEN_HEIGHT = 1320, 1000
CAMPAIGN = "main"
currently_loaded_campaign = ""
GAME_RUNNING, MAIN_MENU, ENDSCREEN, LOGIN, waiting_for_release, WINDOW_OPEN = False, False, False, True, True, True
QUITTING_GAME = False
current_level, current_frame, time_spent = 0, 0, 0
start_time, hours, minutes, seconds = 0, 0, 0, 0
tile_size = 40
stats_folder, campaigns_folder, fallback_resources_folder = "stats", "campaigns", "resources"
level_paths = []
game_stats = { #kar merimo v 1 igri (per-game stats, primer: jumps)
    "jumps": 0,
    "falls": 0,
    "head_bounces": 0,
    "wall_bounces": 0,
    "best_screen": 0,
    "distance_climbed": 0,
    "distance_descended": 0,
    "fall_distance": 0,
    "finish_time": 0,
    "time_on_endscreen": 0,
    "current_jump_streak": 0,
    "best_jump_streak": 0,
}
# All-time, preferences, (per-user)
stats = {}
def_stats = {}
loaded_player_stats = False
#============================= OTHER =============================

#============================= PLAYER & ENTITIES =============================
gravity, jump_power, bounce_power = 30, -17, -17
player_size, max_speed = 80, 4
PLAYER_NAME = ""
babe_min_row_length = 5
#============================= PLAYER & ENTITIES =============================

#============================= SOUND =============================
VOLUME_MASTER = 0.5
VOLUME_SFX = 0.1
VOLUME_MUSIC = 0.1
music_level_instructions = []
music_menus_instructions = {}
can_play_music = True
play_button_already_clicked, quit_button_already_clicked, submit_button_already_clicked, logout_button_already_clicked = False, False, False, False
sfx_keys = [
    "click",
    "jump",
    "bounce",
    "landing",
    "fall",
]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav"]
#============================= SOUND =============================

#============================= USER INTERFACE =============================
faded_in = False
game_ended = False
FPS_cap_game, FPS_cap_menus = 144, 60
bg_resize_koeficient = 1.05
current_menu = "login"
next_scene = "login"
title_text = "Welcome!"
sizes = {
    "play_button": (270, 108),
    "quit_button": (210, 84),
    "submit_button": (210, 84),
    "logout_button": (210, 84),
    "input": (420, 84), 
    "campaigns_dropdown": (420, 84),
}
coordinates = {
    "play_button": ((SCREEN_WIDTH / 2) - (sizes["play_button"][0] / 2), (SCREEN_HEIGHT / 2) - (sizes["play_button"][1] / 2)),
    "quit_button": ((SCREEN_WIDTH / 2) - (sizes["quit_button"][0] / 2), (SCREEN_HEIGHT / 2) - (sizes["quit_button"][1] / 2) + 100),
    "submit_button": (((SCREEN_WIDTH / 2) - (sizes["submit_button"][0] / 2)), ((SCREEN_HEIGHT / 2) + 150)), 
    "logout_button": (((SCREEN_WIDTH / 2) - (sizes["logout_button"][0] / 2)), ((SCREEN_HEIGHT / 2) + 150)),
    "username_input": (((SCREEN_WIDTH / 2) - (sizes["input"][0] / 2)), ((SCREEN_HEIGHT / 2) - 150)), 
    "password_input": (((SCREEN_WIDTH / 2) - (sizes["input"][0] / 2)), ((SCREEN_HEIGHT / 2) - 50)),
    "campaigns_dropdown": (((SCREEN_WIDTH / 2) - sizes["campaigns_dropdown"][0] / 2), ((SCREEN_HEIGHT / 2) - 300))
}
colors = {
    "black": (0, 0, 0),                 #crna
    "grey_dark": (75, 75, 75),          #TEMNO siva
    "grey_middle": (100, 100, 100),
    "grey_bright": (200, 200, 200),     #svetlo siva
    "white": (255, 255, 255),           #bela
    "mint_dark": (95, 210, 115),        #TEMNA mint zelena
    "yellow_bright": (255, 255, 0),     #SVETLO rumena
    "blue_bright": (0, 180, 255),       #bolj svetlo modra
    "orange": (255, 130, 0),            #oranzna
    "green": (0, 255, 0),               #zelena
    "pink": (255, 0, 255),              #pinky
    "red": (255, 0, 0),                 #SVETLA rdeca
    "mint_bright": (115, 255, 140),     #SVETLA mint zelena
    "red_dark": (180, 0, 0),            #TEMNA rdeca
    "yellow_dark": (200, 200, 85),      #TEMNO RUMENA
}
messages = {
    "greeting_back": f"Welcome back, {PLAYER_NAME}",
    "greeting_new": f"Welcome, {PLAYER_NAME}",
    "greeting_guest": f"Logged in as guest. You are using shared stats.",
    "err_password": f"ERROR logging in!\nPassword you entered is incorrect!",
    "err_loading_music_config": f"Failed to load config file for music!",
    "err_empty_campaign": f"This campaign has no levels!", 
    "err_no_campaign_selected": f"Please select a campaign to continue!",
    "loaded_music_config": f"Music config loaded successfully!",
    "endscreen": f"Press any key or click to continue...",
}
tile_images_paths = [
    "tile_1",
    "tile_2",
    "tile_3",
    "tile_4",
    "tile_5",
    "tile_6",
    "tile_7",
    "tile_8",
    "tile_9",
    "tile_10",
    "tile_11",
    "tile_12",
    "tile_13",
    "tile_14",
    "tile_15",
    "tile_16",
    "tile_17",
    "tile_18",
    "tile_19",
    "tile_20",
    "tile_21",
    "tile_22",
    "tile_23",
    "tile_24",
    "tile_25",
    "tile_26",
    "tile_27",
    "tile_28",
    "tile_29",
    "tile_30",
    "tile_31",
    "tile_32",
    "tile_33",
    "tile_34",
    "tile_35",
    "tile_36",
    "tile_37",
    "tile_38",
    "tile_39",
    "tile_40",
    "tile_41",
    "tile_42",
    "tile_43",
    "tile_44",
    "tile_45",
    "tile_46",
    "tile_47",
]
player_images_paths = [
    "player_standing",
    "player_running1",
    "player_running2",
    "player_running3",
    "player_running2",
    "player_charging",
    "player_jumping1",
    "player_jumping2",
    "player_falling",
    "player_lying",
]
babe_images_paths = [
    "1",
    "2",
    "3",
]
button_images_paths = [
    "button",
    "button_highlited",
    "button_pressed",
    "button",
    "button_highlited",
    "button_pressed",
]
button_load_sizes = [
    sizes["play_button"],
    sizes["play_button"],
    sizes["play_button"],
    sizes["quit_button"],
    sizes["quit_button"],
    sizes["quit_button"],
]
bgs_images_paths = []
ui_bgs_sizes = {
    "login": (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient),
    "main_menu": (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient),
    "endscreen": (1332 * bg_resize_koeficient, 1000 * bg_resize_koeficient)
}
ui_bgs_images_paths = {}
fonts_names = [
    "font",
    "font",
    "font",
    "",
    "",
    "",
]
fonts_sizes = [36, 30, 70, 36, 50, 30]
fonts_keys = [
    "normal",
    "smaller",
    "title",
    "timer",
    "bold",
    "notification",
]
SUPPORTED_IMAGE_FORMATS = [
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tga", ".webp", ".tif", ".tiff"
]
#============================= USER INTERFACE =============================