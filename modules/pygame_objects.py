import pygame
pygame.init()

from modules.config import SCREEN_HEIGHT, SCREEN_WIDTH, CAMPAIGN
from modules.utils import load_resources, load_config

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
sfx_channel = pygame.mixer.Channel(0)
bounce_channel = pygame.mixer.Channel(1)

# Load config from .json file
config = load_config(CAMPAIGN)
music_level_instructions = config.get("levels_music", [])
music_menus_instructions = config.get("ui_music", {"login": "", "main_menu": "", "endscreen": ""})
bgs_images_paths = config.get("game_backgrounds", [])
ui_bgs_images_paths = config.get("ui_backgrounds", {"login": "", "main_menu": "", "endscreen": ""})
icon_name = config.get("icon")
babe_position = config.get("babe_position", [])

tile_images, player_images, babe_images, buttons, scaled_bgs, ui_bgs, sfx, fonts = load_resources(CAMPAIGN)