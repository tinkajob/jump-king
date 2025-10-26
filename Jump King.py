import pygame, sys, math, os

from modules.config import *
from modules.objects import *
from modules.pygame_objects import *
from modules.utils import log_in, draw_scene, load_player_stats, save_player_stats, load_resources

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jump King")
pygame.display.set_icon(pygame.image.load(os.path.join(fallback_resources_folder, "other", "icon.png")))
VOLUME_MASTER = def_stats["volume_master"]
VOLUME_SFX = def_stats["volume_sfx"]
VOLUME_MUSIC = def_stats["volume_music"]
music.set_volume(sfx, VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC)

while WINDOW_OPEN:
    current_menu = "login"
    music.play_menu(current_menu)

    screen.blit(ui_bgs["login"], (-600, 0))
    submit_button_already_clicked = False
    notification.delete_notification()
    faded_in = False

    clock.tick()
    while LOGIN:
        # If we havent already started fade-in (first frame) we start fade-in
        if not faded_in:
            effect.start_fade_in()
            faded_in = True

        delta_time = clock.tick(FPS_cap_menus) / 1000.0
        time_spent += delta_time
        events = pygame.event.get()

        # If we close the window
        for event in events:
            if event.type == pygame.QUIT:
                effect.start_fade_out()
                next_scene = "quit"
                music.play_fadeout()

        username_input.capture_input(events, username_text, password_text)
        password_input.capture_input(events, username_text, password_text)
        cursor.update()

        if submit_button.is_clicked():
            if not submit_button_already_clicked:
                sfx["click"].play()

            # We only want transition if music is different for login and main menu
            if music_menus_instructions["login"] != music_menus_instructions["main_menu"]:
                music.play_fadeout()
            submit_button_already_clicked = True
            PLAYER_NAME = username_input.input_text
            next_scene = log_in(username_input.input_text, password_input.input_text, title, effect, username_input, password_input, username_text, password_text, stats)

        if quit_button.is_clicked():
            if not quit_button_already_clicked:
                sfx["click"].play()
            effect.start_fade_out()
            music.play_fadeout()
            next_scene = "quit"
            quit_button_already_clicked = True

        draw_scene("login", screen, scaled_bgs, ui_bgs, 0, delta_time)
        effect.update(delta_time, screen)

        if next_scene == "main_menu" and not effect.get_active():
            MAIN_MENU = True
            LOGIN = False

        if next_scene == "quit" and not effect.get_active():
            LOGIN = False
            WINDOW_OPEN = False
            QUITTING_GAME = True

        pygame.display.flip()

    if not loaded_player_stats:
        load_player_stats(PLAYER_NAME, stats)
        music.update_volume(stats)

    faded_in = False
    play_button_already_clicked = False
    quit_button_already_clicked = False
    logout_button_already_clicked = False

    notification.delete_notification()
    current_menu = "main_menu"
    music.play_menu(current_menu)

    while MAIN_MENU:
        delta_time = clock.tick(FPS_cap_menus) / 1000.0
        time_spent += delta_time

        if not faded_in:
            effect.start_fade_in()
            faded_in = True

        # If we close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_player_stats(PLAYER_NAME, stats)
                effect.start_fade_out()
                music.play_fadeout()
                next_scene = "quit"

        if play_button.is_clicked():
            if not play_button_already_clicked:
                sfx["click"].play()
            music.play_fadeout()
            effect.start_fade_out()
            next_scene = "running"
            play_button_already_clicked = True
            stats["games_started"] += 1

        if quit_button.is_clicked():
            if not quit_button_already_clicked:
                sfx["click"].play()
            music.play_fadeout()
            effect.start_fade_out()
            next_scene = "quit"
            quit_button_already_clicked = True

        if logout_button.is_clicked():
            if not logout_button_already_clicked:
                sfx["click"].play()

            # We only want transition if music is different for login and main menu
            if music_menus_instructions["login"] != music_menus_instructions["main_menu"]:
                music.play_fadeout()
            next_scene = "login"
            effect.start_fade_out()
            logout_button_already_clicked = True
            username_input.input_text = ""
            password_input.input_text = ""
            password_input.masked_text = ""
            username_text.text = ""
            password_text.text = ""
            username_text.update()
            password_text.update()

        draw_scene("main_menu", screen, scaled_bgs, ui_bgs)
        effect.update(delta_time, screen)

        if next_scene == "running" and not effect.get_active():
            MAIN_MENU = False
            GAME_RUNNING = True

        if next_scene == "quit" and not effect.get_active():
            MAIN_MENU = False
            WINDOW_OPEN = False
            QUITTING_GAME = True

        if next_scene == "login" and not effect.get_active():
            LOGIN = True
            MAIN_MENU = False
            save_player_stats(PLAYER_NAME, stats)

        pygame.display.flip()

    if next_scene != "login":
        pygame.mixer.music.stop()
        music.play_level(current_level)

    current_level = 0
    level = levels[current_level]
    faded_in = False
    game_ended = False

    player.reset_position(SCREEN_WIDTH / 2 - player_size / 2, 891)
    player.reset_values()

    notification.delete_notification()
    start_time = pygame.time.get_ticks()
    can_play_music = True


    if not QUITTING_GAME:
        load_resources(CAMPAIGN) #tu poklicemo po tem ku zberemo campaign!!! ZELU HEAVY FUNKCIJA
        main_babe.find_position(babe_position, levels[len(levels) - 1], tile_size, SCREEN_WIDTH, SCREEN_HEIGHT) # Find babe position based on config file or automatically
    clock.tick()

    while GAME_RUNNING:
        if not faded_in:
            effect.start_fade_in()
            faded_in = True
        delta_time = clock.tick(FPS_cap_game) / 1000.0
        time_spent += delta_time
        time = pygame.time.get_ticks() - start_time
        keys = pygame.key.get_pressed()

        hours = int(time // 3600000)
        minutes = int(time // 60000) % 60
        seconds = int(time // 1000) % 60
        timer_text.text = f"{hours}:{minutes:02}:{seconds:02}"
        timer_text.update()

        if time_spent > 0.5:
            FPS_text.text = f"FPS: {math.floor(1 / delta_time):03}"
            FPS_text.update()
            time_spent = 0

        if player.can_move:
            level, current_level = player.move(delta_time, keys, current_level, level, levels)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats["ragequits"] += 1
                save_player_stats(PLAYER_NAME, stats)
                music.play_fadeout()
                effect.start_fade_out()
                next_scene = "quit"

        if main_babe.check_for_ending(player) and not game_ended:
            next_scene = "endscreen"
            effect.start_fade_out()
            stats["games_played"] += 1
            player.can_move = False
            player.rect.y = main_babe.rect.y + 10
            player.rect.x = main_babe.rect.x - 80
            player.current_frame = 0
            player.direction = "right"
            music.play_fadeout()
            can_play_music = False

        if can_play_music:
            music.play_level(current_level)

        if next_scene == "endscreen" and not effect.get_active():
            can_play_music = False
            ENDSCREEN = True
            GAME_RUNNING = False
            game_ended = True

        if next_scene == "quit" and not effect.get_active():
            GAME_RUNNING = False
            WINDOW_OPEN = False
            ENDSCREEN = False
            QUITTING_GAME = True
            game_ended = True

        if not game_ended:
            draw_scene("running", screen, scaled_bgs, ui_bgs, current_level, delta_time)

        effect.update(delta_time, screen)
        pygame.display.flip()

    faded_in = False

    # To ensure music keeps playing uninterrupted between login and main menu
    if next_scene != "login":
        pygame.mixer.music.stop()
        current_menu = "endscreen"
    music.play_menu(current_menu)

    notification.delete_notification()
    notification.show_notification(messages["endscreen"])

    while ENDSCREEN:
        delta_time = clock.tick(FPS_cap_menus) / 1000.0
        time_spent += delta_time

        if not faded_in:
            effect.start_fade_in()
            faded_in = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                effect.start_fade_out()
                music.play_fadeout()
                next_scene = "quit"

        keys = pygame.key.get_pressed()

        notification.is_clicked()

        if next_scene == "endscreen" or ((next_scene == "main_menu" or next_scene == "quit") and effect.get_active()):
            draw_scene("endscreen", screen, scaled_bgs, ui_bgs)

        if waiting_for_release:
            if not any(keys):
                waiting_for_release = False
        elif any(keys):
            music.play_fadeout()
            effect.start_fade_out()
            next_scene = "main_menu"

        if next_scene == "main_menu" and not effect.get_active():
            save_player_stats(PLAYER_NAME, stats)
            ENDSCREEN = False
            MAIN_MENU = True
            faded_in = False
            GAME_RUNNING = False

        if next_scene == "quit" and not effect.get_active():
            WINDOW_OPEN = False
            MAIN_MENU = False
            ENDSCREEN = False
            QUITTING_GAME = True

        effect.update(delta_time, screen)
        pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
