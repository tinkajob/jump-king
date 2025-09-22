import pygame

import modules.objects as objects
from modules.config import musics#, music_menus_instructions

class MusicController:
    def __init__(self:object):
        """Creates a music controller object"""
        self.current_song = ""
        self.requested_song = ""
        self.is_fading_out = False
        self.fade_duration = 1000

    def play_level(self:object, current_level:int):
        """Plays the correct song based on the input"""     

        if objects.music_level_instructions:
            self.requested_song = objects.music_level_instructions[current_level]
        else:
            self.requested_song == ""

        if self.requested_song == "":
            self.play_fadeout()

        elif self.current_song != self.requested_song:
            self.current_song = self.requested_song
            pygame.mixer.music.load(musics[self.current_song])
            pygame.mixer.music.play(-1, 0, 500)

    def play_fadeout(self:object):
        if not pygame.mixer.music.get_busy():
            self.is_fading_out = False
        if not self.is_fading_out:
            pygame.mixer.music.set_volume(1)
            
        self.is_fading_out = True
        pygame.mixer.music.fadeout(self.fade_duration)
        self.current_song = ""

    def play_menu(self:object, current_menu:str):
        """Plays the main menu music"""

        self.requested_song = objects.music_menus_instructions[current_menu]

        if not self.current_song == self.requested_song:
            pygame.mixer.music.load(musics[self.requested_song])
            pygame.mixer.music.play(-1)
            self.current_song = self.requested_song
