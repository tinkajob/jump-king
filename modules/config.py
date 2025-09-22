#============================= OTHER =============================
SCREEN_WIDTH, SCREEN_HEIGHT = 1320, 1000
CAMPAIGN = "main"
running, main_menu, endscreen, login, waiting_for_release, WINDOW_OPEN = False, False, False, True, True, True
current_level, current_frame, time_spent = 0, 0, 0
start_time, hours, minutes, seconds = 0, 0, 0, 0
tile_size = 40
stats_folder, campaigns_folder, resources_folder = "stats", "campaigns", "resources"
level_paths = []
game_stats = { #kar merimo v 1 igri (per-game stats, primer: jumps)
    "jumps": 0,
    "falls": 0,
    "head_bounces": 0,
    "wall_bounces": 0,
    "current_jump_streak": 0,
    "best_jump_streak": 0,
    "best_screen": 0,
    "distance_climbed": 0,
    "distance_descended": 0,
    "fall_distance": 0,
}
stats = {}
def_stats = { #all time (per-user stats, primer: total jumps, min_jumps_in_game)
    "password": 0,                              #DONE
    "total_playtime": 0,
    "personal_best_time": 0,
    "avg_completion_time": 0,
    "total_jumps": 0,                           #DONE
    "total_falls": 0,                           #DONE
    "highest_position": 0,
    "total_fall_distance": 0,
    "games_played": 0,                          #DONE
    "best_jump_streak": 0,
    "avg_jump_streak": 0,
    "head_bounces": 0,                          #DONE
    "wall_bounces": 0,                          #DONE
    "ragequits": 0,                             #DONE
    "pause_count": 0,
    "total_airtime": 0,
    "longest_airtime": 0,
    "min_jumps_in_game": 99999999999,           #DONE
    "max_jumps_in_game": 0,                     #DONE
    "min_falls_in_game": 99999999999,           #DONE
    "max_falls_in_game": 0,                     #DONE
    "avg_airtime": 0,
    "time_on_endscreen": 0,
    "games_started": 0, 
    "finished_games": 0,
    "finish_rate": 0,
    "best_screen": 0,                           #DONE
    "total_distance_climbed": 0,                #DONE                    #dodaj se za igro z najvecjo razliko
    "total_distance_descended": 0,              #DONE                    #dodaj se za igro z najvecjo razliko
    "highest_distance_climbed_in_game": 0,
    "highest_distance_descended_in_game": 0,
    #dodaj se za avg stvari in pogruntej!!!!!
}
loaded_player_stats = False
#============================= OTHER =============================

#============================= PLAYER & ENTITIES =============================
gravity, jump_power, bounce_power = 30, -17, -17
player_size, max_speed = 80, 4
PLAYER_NAME = ""
#============================= PLAYER & ENTITIES =============================

#============================= SOUND =============================
musics = {
    "main_menu":    f"{resources_folder}/music/main_menu.mp3",
    "sewer":        f"{resources_folder}/music/sewer.mp3",
    "fallen_king":  f"{resources_folder}/music/fallen_king.mp3",
    "despair":      f"{resources_folder}/music/despair.mp3",
    "masse":        f"{resources_folder}/music/masse.mp3",
    "sky_blue":     f"{resources_folder}/music/sky_blue.mp3",
    "coronation":   f"{resources_folder}/music/coronation.mp3",
    "sunrise":      f"{resources_folder}/music/sunrise.mp3",
    "legend":       f"{resources_folder}/music/a_legend_lives_on.mp3",
    "zacasno":      f"{resources_folder}/music/bg_music.mp3",
}
music_level_instructions = []
music_menus_instructions = {}
can_play_music = True
play_button_already_clicked, quit_button_already_clicked, submit_button_already_clicked, logout_button_already_clicked = False, False, False, False
#============================= SOUND =============================

#============================= USER INTERFACE =============================
faded_in = False
game_ended = False
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
}
coordinates = {
    "play_button": ((SCREEN_WIDTH / 2) - (sizes["play_button"][0] / 2), (SCREEN_HEIGHT / 2) - (sizes["play_button"][1] / 2)),
    "quit_button": ((SCREEN_WIDTH / 2) - (sizes["quit_button"][0] / 2), (SCREEN_HEIGHT / 2) - (sizes["quit_button"][1] / 2) + 100),
    "submit_button": (((SCREEN_WIDTH / 2) - (sizes["submit_button"][0] / 2)), ((SCREEN_HEIGHT / 2) + 150)), 
    "logout_button": (((SCREEN_WIDTH / 2) - (sizes["logout_button"][0] / 2)), ((SCREEN_HEIGHT / 2) + 150)),
    "username_input": (((SCREEN_WIDTH / 2) - (sizes["input"][0] / 2)), ((SCREEN_HEIGHT / 2) - 150)), 
    "password_input": (((SCREEN_WIDTH / 2) - (sizes["input"][0] / 2)), ((SCREEN_HEIGHT / 2) - 50))
}
colors = {
    "black": (0, 0, 0),                 #crna
    "white": (255, 255, 255),           #bela
    "mint_dark": (95, 210, 115),        #TEMNA mint zelena
    "yellow_bright": (255, 255, 0),     #SVETLO rumena
    "blue_bright": (0, 180, 255),       #bolj svetlo modra
    "grey_bright": (200, 200, 200),     #svetlo siva
    "orange": (255, 130, 0),            #oranzna
    "green": (0, 255, 0),               #zelena
    "pink": (255, 0, 255),              #pinky
    "grey_dark": (75, 75, 75),          #TEMNO siva
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
    "loaded_music_config": f"Music config loaded successfully!",
    "endscreen": f"Press any key to continue...",
}
#============================= USER INTERFACE =============================