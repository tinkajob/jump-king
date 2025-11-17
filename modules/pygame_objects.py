import pygame, os

import modules.config as conf

from modules.utils import load_json, load_resources, load_offsets
pygame.init()

screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
clock = pygame.time.Clock()
sfx_channel = pygame.mixer.Channel(0)
bounce_channel = pygame.mixer.Channel(1)

# Load config from .json file
config = load_json(os.path.join("campaigns", conf.CAMPAIGN, "config.json"))
level_musics = config.get("levels_music", [])
menu_musics = config.get("ui_music", {"login": "", "main_menu": "", "endscreen": ""})
bgs_images_paths = config.get("game_backgrounds", [])
ui_bgs_images_paths = config.get("ui_backgrounds", {"login": "", "main_menu": "", "endscreen": ""})
icon_name = config.get("icon")
babe_position = config.get("babe_position", [])
bg_offsets = load_offsets(config["bg_offsets"])

conf.def_stats = load_json(os.path.join("resources", "other", "def_stats.json"))

tile_images, player_images, babe_images, buttons, scaled_bgs, ui_bgs, sfx, fonts = load_resources()