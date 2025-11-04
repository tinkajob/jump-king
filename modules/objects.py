import modules.config as conf
import modules.player_controller as player
import modules.npcs as npcs
import modules.utils as utils
import modules.music as music
import modules.ui as ui
import modules.pygame_objects as py_objs

levels, level_surfaces = [], []
utils.detect_levels()
utils.make_levels(py_objs.tile_images)
level = levels[conf.current_level]

player = player.PlayerController(conf.SCREEN_WIDTH / 2 - conf.player_size / 2, 891, conf.player_size)
main_babe = npcs.BabeController(1200, 160, conf.player_size)

game_music = music.MusicController()
effect = ui.FadeManager(conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT)

play_button = ui.Button(conf.coordinates["play_button"], conf.sizes["play_button"])
quit_button = ui.Button(conf.coordinates["quit_button"], conf.sizes["quit_button"], 3)
submit_button = ui.Button(conf.coordinates["submit_button"], conf.sizes["submit_button"], 3)
logout_button = ui.Button(conf.coordinates["logout_button"], conf.sizes["logout_button"], 3)

username_input = ui.InputField(conf.coordinates["username_input"], conf.sizes["input"], False, "username")
password_input = ui.InputField(conf.coordinates["password_input"], conf.sizes["input"], True, "password")

title = ui.Text(conf.title_text, "white", "title", ((conf.SCREEN_WIDTH / 2), 200))
play_text = ui.Text("PLAY", "white", "normal", play_button.rect.center)
quit_text = ui.Text("QUIT", "white", "smaller", quit_button.rect.center)
submit_text = ui.Text("Submit", "white", "normal", submit_button.rect.center)
logout_text = ui.Text("Logout", "white", "normal", logout_button.rect.center)
FPS_text = ui.Text("000", "grey_dark", "timer", (conf.SCREEN_WIDTH - 60,15))
timer_text = ui.Text("0:00:00", "grey_dark", "timer", (50, 15))

cursor = ui.Cursor((0, 0), (4, 36))

notification = ui.Notification(((conf.SCREEN_WIDTH / 2) - 300, 800), (600, 150), "{Notification message}")

# We input all possible options to choose from when we define a dropdown menu
path, campaigns_list, files = utils.list_current_folder(conf.campaigns_folder) # We don't actually need path and files, it's just because the function returns those
campaigns_list.remove("levels")
campaign_dropdown = ui.DropdownMenu(conf.coordinates["campaigns_dropdown"], conf.sizes["campaigns_dropdown"], campaigns_list)

# Importance order for UI elements (topmost drawn last)
# login_ui_elements = [notification, campaign_dropdown, cursor, username_input, password_input, submit_button, quit_button, submit_text, quit_text]