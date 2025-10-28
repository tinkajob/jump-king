import pygame
pygame.init()

import modules.config as conf
import modules.utils as utils

screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
clock = pygame.time.Clock()
sfx_channel = pygame.mixer.Channel(0)
bounce_channel = pygame.mixer.Channel(1)

# Load config from .json file
config = utils.load_config()
music_level_instructions = config.get("levels_music", [])
music_menus_instructions = config.get("ui_music", {"login": "", "main_menu": "", "endscreen": ""})
bgs_images_paths = config.get("game_backgrounds", [])
ui_bgs_images_paths = config.get("ui_backgrounds", {"login": "", "main_menu": "", "endscreen": ""})
icon_name = config.get("icon")
babe_position = config.get("babe_position", [])

tile_images, player_images, babe_images, buttons, scaled_bgs, ui_bgs, sfx, fonts = utils.load_resources()