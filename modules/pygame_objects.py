import pygame
pygame.init()

from modules.config import SCREEN_HEIGHT, SCREEN_WIDTH, CAMPAIGN
from modules.utils import load_resources

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
sfx_channel = pygame.mixer.Channel(0)
bounce_channel = pygame.mixer.Channel(1)

tile_images, player_images, babe_images, buttons, scaled_bgs, endscreens, sfx, fonts = load_resources(CAMPAIGN)