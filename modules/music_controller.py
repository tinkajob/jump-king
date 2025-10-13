import pygame

#import modules.objects as objects
from modules.pygame_objects import sfx, music_level_instructions, music_menus_instructions
from modules.config import musics, VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC

class MusicController:
    def __init__(self:object):
        """Creates a music controller object"""
        self.current_song = ""
        self.requested_song = ""
        self.is_fading_out = False
        self.fade_duration = 1000

    def set_volume(self:object, sfx:list, master_volume:float = 0.5, sfx_volume:float = 0.1, music_volume:float = 0.1, ):
        """Sets the volume for each sound category"""
        pygame.mixer.music.set_volume(master_volume * music_volume)
        for sound in sfx.values():
            sound.set_volume(master_volume * sfx_volume)

    def update_volume(self:object, stats:list):
        """Sets volume variables to values from the player's stats"""
        global VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC, sfx
        VOLUME_MASTER = stats["volume_master"]
        VOLUME_SFX = stats["volume_sfx"]
        VOLUME_MUSIC = stats["volume_music"]
        self.set_volume(sfx, VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC)

    def play_level(self:object, current_level:int):
        """Plays the correct song based on the input"""     

        if music_level_instructions:
            self.requested_song = music_level_instructions[current_level]
        else:
            self.requested_song == ""

        if self.requested_song == "":
            self.play_fadeout()

        elif self.current_song != self.requested_song:
            self.current_song = self.requested_song
            pygame.mixer.music.load(musics[self.current_song])
            pygame.mixer.music.play(-1, 0, 500)

    def play_fadeout(self:object):
        """Plays the fadeout effect"""
        if not pygame.mixer.music.get_busy():
            self.is_fading_out = False
        if not self.is_fading_out:
            self.set_volume(sfx, VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC)
            
        self.is_fading_out = True
        pygame.mixer.music.fadeout(self.fade_duration)
        self.current_song = ""

    def play_menu(self:object, current_menu:str):
        """Plays the main menu music"""

        self.requested_song = music_menus_instructions[current_menu]

        if self.current_song != self.requested_song:
            pygame.mixer.music.load(musics[self.requested_song])
            pygame.mixer.music.play(-1)
            self.current_song = self.requested_song
