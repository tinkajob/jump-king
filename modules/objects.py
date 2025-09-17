from modules.config import level_paths, SCREEN_HEIGHT, SCREEN_WIDTH, player_size, current_level, coordinates, sizes, title_text, levels_folder
from modules.player_controller import PlayerController
from modules.npcs import BabeController
from modules.utils import create_level, load_level_from_file, create_level_surface, detect_levels
from modules.music_controller import MusicController
from modules.ui import Text, Button, InputField, FadeManager, Cursor, Notification

level_paths = detect_levels(levels_folder, level_paths)

levels, level_surfaces = [], []
for i in range(len(level_paths)):
    platforms = create_level(load_level_from_file(i))
    levels.append(platforms)
    level_surfaces.append(create_level_surface(platforms))

player = PlayerController(SCREEN_WIDTH / 2 - player_size / 2, 891, player_size)
main_babe = BabeController(1200, 160, player_size)
level = levels[current_level]

music = MusicController()
effect = FadeManager(SCREEN_WIDTH, SCREEN_HEIGHT)

play_button = Button(coordinates["play_button"], sizes["play_button"], "play")
quit_button = Button(coordinates["quit_button"], sizes["quit_button"], "quit")
submit_button = Button(coordinates["submit_button"], sizes["submit_button"], "submit")
logout_button = Button(coordinates["logout_button"], sizes["logout_button"], "logout")

username_input = InputField(coordinates["username_input"], sizes["input"], False, "username")
password_input = InputField(coordinates["password_input"], sizes["input"], True, "password")

title = Text(title_text, "white", "title", ((SCREEN_WIDTH / 2), 200))
play_text = Text("PLAY", "white", "normal", play_button.rect.center)
quit_text = Text("QUIT", "white", "smaller", quit_button.rect.center)
submit_text = Text("Submit", "white", "normal", submit_button.rect.center)
logout_text = Text("Logout", "white", "normal", logout_button.rect.center)
username_text = Text("username", "white", "smaller", username_input.rect.center)
password_text = Text("password", "white", "smaller", password_input.rect.center)
endscreen_text = Text("Press any key to continue...", "black", "bold", ((SCREEN_WIDTH / 2), 840))
FPS_text = Text("000", "grey_dark", "timer", (SCREEN_WIDTH - 60,15))
timer_text = Text("0:00:00", "grey_dark", "timer", (50, 15))

cursor = Cursor((0, 0), (4, 36))

notification = Notification(((SCREEN_WIDTH / 2) - 300, 800), (600, 150), "Yes — there are several apps that help you figure out how to recycle correctly (which bin, where to drop off, etc.). Depending on your location, some can even scan barcodes or photos of packaging to tell you where it goes. Here are a few good ones + what features they offer. If you tell me what country youre in, I can suggest ones specific to your area.")