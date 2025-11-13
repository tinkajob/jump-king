import pygame, os

import modules.pygame_objects as py_objs
import modules.config as conf
from modules.config import SUPPORTED_AUDIO_FORMATS

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
        import modules.config as conf
        conf.VOLUME_MASTER = stats["volume_master"]
        conf.VOLUME_SFX = stats["volume_sfx"]
        conf.VOLUME_MUSIC = stats["volume_music"]
        self.set_volume(py_objs.sfx, conf.VOLUME_MASTER, conf.VOLUME_SFX, conf.VOLUME_MUSIC)

    def play_level(self:object, current_level:int):
        """Plays the correct song based on the input"""     
        self.requested_song == ""
        self.requested_song = py_objs.level_musics[current_level]

        if self.requested_song == "":
            self.current_song = ""
            self.play_fadeout()
            return

        self.load_music()

    def play_fadeout(self:object):
        """Plays the fadeout effect"""
        if not pygame.mixer.music.get_busy():
            self.is_fading_out = False
        if not self.is_fading_out:
            self.set_volume(py_objs.sfx, conf.VOLUME_MASTER, conf.VOLUME_SFX, conf.VOLUME_MUSIC)
            
        self.is_fading_out = True
        pygame.mixer.music.fadeout(self.fade_duration)
        self.current_song = ""

    def play_menu(self:object, current_menu:str):
        """Plays the main menu music"""

        # Here we get the name of the song we want to play
        self.requested_song = py_objs.menu_musics[current_menu]
        self.load_music()
   
    def load_music(self:object):
        # If we already play the same music as requested, we skip all the other code entirely
        if self.current_song == self.requested_song:
            return
        
        found_music = False
        music_filepath = ""

        # We first check if the music file is in the campaign resources folder
        for format in SUPPORTED_AUDIO_FORMATS:
            if os.path.exists(os.path.join("campaigns", conf.CAMPAIGN, "resources", "music", self.requested_song) + format):
                music_filepath = os.path.join("campaigns", conf.CAMPAIGN, "resources", "music", self.requested_song) + format
                found_music = True
                break
        
        # If not, we check for backup resources
        if not found_music:
            for format in SUPPORTED_AUDIO_FORMATS:
                if os.path.exists(os.path.join("resources", "music", self.requested_song) + format):
                    music_filepath = os.path.join("resources", "music", self.requested_song) + format
                    break

        # If we haven't found it, we don't play anything
        if music_filepath == "":
            self.current_song = ""
            self.play_fadeout()
            return

        # If we found a music file we load it
        pygame.mixer.music.load(music_filepath)
        pygame.mixer.music.play(-1, fade_ms = 500)
        self.current_song = self.requested_song