import pygame
pygame.init()

from modules.config import SCREEN_HEIGHT, SCREEN_WIDTH, tile_size, resources_folder, bg_resize_koeficient

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
tile_images = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_1.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_2.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_3.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_4.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_5.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_6.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_7.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_8.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_9.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_10.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_11.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_12.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_13.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_14.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_15.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_16.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_17.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_18.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_19.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_20.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_21.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_22.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_23.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_24.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_25.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_26.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_27.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_28.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_29.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_30.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_31.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_32.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_33.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_34.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_35.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_36.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_37.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_38.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_39.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_40.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_41.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_42.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_43.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_44.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_45.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_46.png"), (tile_size, tile_size)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/tiles/tile_47.png"), (tile_size, tile_size)),
]
player_images = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_standing.png"), (80, 80)),  #idle
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_running1.png"), (80, 80)),  #running
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_running2.png"), (80, 80)),  #running
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_running3.png"), (80, 80)),  #running
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_running2.png"), (80, 80)),  #running
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_charging.png"), (80, 80)),  #charging
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_jumping1.png"), (80, 80)),  #jumping
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_jumping2.png"), (80, 80)),  #jumping
    pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_falling.png"), (80, 80)), True, False), #falling
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/player_animation/player_lying.png"), (80, 80)),     #lying
]
babe_images = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/babe_animation/1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/babe_animation/2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/babe_animation/3.png"), (80, 80)),
]
sfx = {
    "click":    pygame.mixer.Sound(f"{resources_folder}/sfx/click.wav"),
    "jump":     pygame.mixer.Sound(f"{resources_folder}/sfx/jump.wav"),
    "bounce":   pygame.mixer.Sound(f"{resources_folder}/sfx/bounce.wav"),
    "landing":  pygame.mixer.Sound(f"{resources_folder}/sfx/landing.wav"),
    "fall":     pygame.mixer.Sound(f"{resources_folder}/sfx/fall.wav"),
}
sfx_channel = pygame.mixer.Channel(0)
bounce_channel = pygame.mixer.Channel(1)
buttons = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button.png"), (270, 108)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button_highlited.png"), (270, 108)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button_pressed.png"), (270, 108)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button.png"), (210, 84)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button_highlited.png"), (210, 84)),
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/other/button_pressed.png"), (210, 84)),
]
fonts = {
    "normal": pygame.font.Font(f"{resources_folder}/other/font.otf", 36),
    "smaller": pygame.font.Font(f"{resources_folder}/other/font.otf", 30),
    "title": pygame.font.Font(f"{resources_folder}/other/font.otf", 70),
    "timer": pygame.font.Font(None, 36),
    "bold" : pygame.font.Font(None, 50),
    "notification": pygame.font.Font(None, 30),
}
scaled_bgs = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/menu_bg.jpg").convert(), (1920 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # menu
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg0.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level1
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg1.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level2
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg2.png").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level3
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg3.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level4
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg4.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level5
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg5.png").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level6
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg6.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level7
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg7.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level8
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg8.png").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level9
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/bgs/bg9.jpg").convert(), (1778 * bg_resize_koeficient, 1000 * bg_resize_koeficient)), # level10
]
endscreens = [
    pygame.transform.scale(pygame.image.load(f"{resources_folder}/endscreens/1.png").convert(), (1332 * bg_resize_koeficient, 1000 * bg_resize_koeficient))
]
