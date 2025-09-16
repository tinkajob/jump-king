import pygame

from modules.config import musics

class MusicController:
    def __init__(self:object):
        """Creates a music controller object"""
        self.current_song = ""
        self.is_fading_out = False
        self.fade_duration = 1000

    def play(self:object, current_level:int, endscreen:bool, fadeout:str = ""):
        """Plays the correct song based on the input"""
        if not pygame.mixer.music.get_busy():
            self.is_fading_out = False
        if not self.is_fading_out:
            pygame.mixer.music.set_volume(1)

        if (current_level < 2 and not self.is_fading_out and self.current_song != "") or fadeout == "fadeout": #fadeout je tisti leveli ku nimajo muzike (nastavis pravila tm pri current_level), in na konci
            self.is_fading_out = True
            pygame.mixer.music.fadeout(self.fade_duration) # time in ms
            self.current_song = ""

        if not self.is_fading_out:
            if current_level == 5 and self.current_song != "coronation": # za npr. prvo muziko, itak loh rocno nastavis ker ves, ker so tu pravila za tocno doloceno muziko
                pygame.mixer.music.load(musics["coronation"])
                self.current_song = "coronation"
                pygame.mixer.music.play(-1)
        
            if (current_level == 2 or current_level == 3) and self.current_song != "sewer":
                pygame.mixer.music.load(musics["sewer"])
                self.current_song = "sewer"
                pygame.mixer.music.play(-1)

            if endscreen:
                pygame.mixer.music.load(musics["sunrise"])
                self.current_song = "sunrise"
                pygame.mixer.music.play(-1)

    def main_menu(self:object):
        """Plays the main menu music"""
        pygame.mixer.music.load(musics["main_menu"])
        pygame.mixer.music.play(-1)
