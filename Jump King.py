import pygame, sys, math, os

import modules.config as conf
import modules.objects as objs
import modules.pygame_objects as py_objs
import modules.utils as utils

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jump King")
pygame.display.set_icon(pygame.image.load(os.path.join(conf.fallback_resources_folder, "other", "icon.png")))
VOLUME_MASTER = conf.def_stats["volume_master"]
VOLUME_SFX = conf.def_stats["volume_sfx"]
VOLUME_MUSIC = conf.def_stats["volume_music"]
objs.game_music.set_volume(py_objs.sfx, VOLUME_MASTER, VOLUME_SFX, VOLUME_MUSIC)

while conf.WINDOW_OPEN:
    conf.current_menu = "login"
    objs.game_music.play_menu(conf.current_menu)

    py_objs.screen.blit(py_objs.ui_bgs["login"], (-600, 0))
    conf.submit_button_already_clicked = False
    conf.quit_button_already_clicked = False
    objs.notification.delete_notification()
    conf.faded_in = False

    py_objs.clock.tick()
    while conf.LOGIN:
        # If we havent already started fade-in (first frame) we start fade-in
        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time
        events = pygame.event.get()

        # If we close the window
        for event in events:
            if event.type == pygame.QUIT:
                objs.effect.start_fade_out()
                conf.next_scene = "quit"
                objs.game_music.play_fadeout()

        objs.username_input.capture_input(events, objs.username_text, objs.password_text)
        objs.password_input.capture_input(events, objs.username_text, objs.password_text)
        objs.cursor.update()
        objs.campaign_dropdown.handle_highliting(events)

        if objs.submit_button.is_clicked():
            if not conf.submit_button_already_clicked:
                py_objs.sfx["click"].play()

            # We only want transition if music is different for login and main menu
            if py_objs.music_menus_instructions["login"] != py_objs.music_menus_instructions["main_menu"]:
                objs.game_music.play_fadeout()
            conf.submit_button_already_clicked = True
            conf.PLAYER_NAME = objs.username_input.input_text
            conf.next_scene = utils.log_in(objs.username_input.input_text, objs.password_input.input_text, objs.title, objs.effect, objs.username_input, objs.password_input, objs.username_text, objs.password_text, conf.stats)
            conf.CAMPAIGN = objs.campaign_dropdown.get_selection()

        if objs.quit_button.is_clicked():
            if not conf.quit_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.effect.start_fade_out()
            objs.game_music.play_fadeout()
            conf.next_scene = "quit"
            conf.quit_button_already_clicked = True

        utils.draw_scene("login", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, 0, delta_time)
        objs.effect.update(delta_time, py_objs.screen)

        if conf.next_scene == "main_menu" and not objs.effect.get_active():
            conf.MAIN_MENU = True
            conf.LOGIN = False

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.LOGIN = False
            conf.WINDOW_OPEN = False
            conf.QUITTING_GAME = True

        pygame.display.flip()

    if not conf.loaded_player_stats:
        utils.load_player_stats(conf.PLAYER_NAME, conf.stats)
        objs.game_music.update_volume(conf.stats)

    conf.faded_in = False
    conf.play_button_already_clicked = False
    conf.quit_button_already_clicked = False
    conf.logout_button_already_clicked = False

    objs.notification.delete_notification()
    conf.current_menu = "main_menu"
    objs.game_music.play_menu(conf.current_menu)

    if not conf.QUITTING_GAME:
        py_objs.tile_images, py_objs.player_images, py_objs.babe_images, py_objs.buttons, py_objs.scaled_bgs, py_objs.ui_bgs, py_objs.sfx, py_objs.fonts = utils.load_resources()

    py_objs.clock.tick()

    while conf.MAIN_MENU:
        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time

        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        # If we close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                utils.save_player_stats(conf.PLAYER_NAME, conf.stats)
                objs.effect.start_fade_out()
                objs.game_music.play_fadeout()
                conf.next_scene = "quit"

        if objs.play_button.is_clicked():
            if not conf.play_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "running"
            conf.play_button_already_clicked = True
            conf.stats["games_started"] += 1

        if objs.quit_button.is_clicked():
            if not conf.quit_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "quit"
            conf.quit_button_already_clicked = True

        if objs.logout_button.is_clicked():
            if not conf.logout_button_already_clicked:
                py_objs.sfx["click"].play()

            # We only want transition if music is different for login and main menu
            if py_objs.music_menus_instructions["login"] != py_objs.music_menus_instructions["main_menu"]:
                objs.game_music.play_fadeout()
            conf.next_scene = "login"
            objs.effect.start_fade_out()
            conf.logout_button_already_clicked = True
            objs.username_input.input_text = ""
            objs.password_input.input_text = ""
            objs.password_input.masked_text = ""
            objs.username_text.text = ""
            objs.password_text.text = ""
            objs.username_text.update()
            objs.password_text.update()

        utils.draw_scene("main_menu", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs)
        objs.effect.update(delta_time, py_objs.screen)

        if conf.next_scene == "running" and not objs.effect.get_active():
            conf.MAIN_MENU = False
            conf.GAME_RUNNING = True

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.MAIN_MENU = False
            conf.WINDOW_OPEN = False
            conf.QUITTING_GAME = True

        if conf.next_scene == "login" and not objs.effect.get_active():
            conf.LOGIN = True
            conf.MAIN_MENU = False
            utils.save_player_stats(conf.PLAYER_NAME, conf.stats)

        pygame.display.flip()

    if conf.next_scene != "login":
        pygame.mixer.music.stop()
        objs.game_music.play_level(conf.current_level)

    conf.current_level = 0
    objs.level = objs.levels[conf.current_level]
    conf.faded_in = False
    conf.game_ended = False

    objs.player.reset_position(conf.SCREEN_WIDTH / 2 - conf.player_size / 2, 891)
    objs.player.reset_values()

    objs.notification.delete_notification()
    start_time = pygame.time.get_ticks()
    conf.can_play_music = True


    if not conf.QUITTING_GAME:
        # That's commented out just because for now we set campaign on the login screen
        #py_objs.tile_images, py_objs.player_images, py_objs.babe_images, py_objs.buttons, py_objs.scaled_bgs, py_objs.ui_bgs, py_objs.sfx, py_objs.fonts = utils.load_resources(conf.CAMPAIGN, conf.fallback_resources_folder, conf.tile_images_paths, conf.player_images_paths, conf.babe_images_paths, conf.button_images_paths, conf.button_load_sizes, conf.bg_resize_koeficient, conf.sfx_keys, conf.fonts_keys, conf.fonts_sizes, conf.fonts_names, conf.ui_bgs_sizes, py_objs.ui_bgs_images_paths, py_objs.bgs_images_paths) #tu poklicemo po tem ku zberemo campaign!!! ZELU HEAVY FUNKCIJA
        objs.main_babe.find_position(py_objs.babe_position, objs.levels[len(objs.levels) - 1], conf.tile_size, conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT) # Find babe position based on config file or automatically
    py_objs.clock.tick()

    while conf.GAME_RUNNING:
        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True
        delta_time = py_objs.clock.tick(conf.FPS_cap_game) / 1000.0
        conf.time_spent += delta_time
        time = pygame.time.get_ticks() - start_time
        keys = pygame.key.get_pressed()

        hours = int(time // 3600000)
        minutes = int(time // 60000) % 60
        seconds = int(time // 1000) % 60
        objs.timer_text.text = f"{hours}:{minutes:02}:{seconds:02}"
        objs.timer_text.update()

        if conf.time_spent > 0.5:
            objs.FPS_text.text = f"FPS: {math.floor(1 / delta_time):03}"
            objs.FPS_text.update()
            conf.time_spent = 0

        if objs.player.can_move:
            objs.level, conf.current_level = objs.player.move(delta_time, keys)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf.stats["ragequits"] += 1
                utils.save_player_stats(conf.PLAYER_NAME, conf.stats)
                objs.game_music.play_fadeout()
                objs.effect.start_fade_out()
                conf.next_scene = "quit"

        if objs.main_babe.check_for_ending(objs.player) and not conf.game_ended:
            conf.next_scene = "endscreen"
            objs.effect.start_fade_out()
            conf.stats["games_played"] += 1
            objs.player.can_move = False
            objs.player.rect.y = objs.main_babe.rect.y + 10
            objs.player.rect.x = objs.main_babe.rect.x - 80
            objs.player.current_frame = 0
            objs.player.direction = "right"
            objs.game_music.play_fadeout()
            conf.can_play_music = False

        if conf.can_play_music:
            objs.game_music.play_level(conf.current_level)

        if conf.next_scene == "endscreen" and not objs.effect.get_active():
            conf.can_play_music = False
            conf.ENDSCREEN = True
            conf.GAME_RUNNING = False
            conf.game_ended = True

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.GAME_RUNNING = False
            conf.WINDOW_OPEN = False
            conf.ENDSCREEN = False
            conf.QUITTING_GAME = True
            conf.game_ended = True

        if not conf.game_ended:
            utils.draw_scene("running", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, conf.current_level, delta_time)

        objs.effect.update(delta_time, py_objs.screen)
        pygame.display.flip()

    conf.faded_in = False

    # To ensure music keeps playing uninterrupted between login and main menu
    if conf.next_scene != "login":
        pygame.mixer.music.stop()
        conf.current_menu = "endscreen"
    objs.game_music.play_menu(conf.current_menu)

    objs.notification.delete_notification()
    objs.notification.show_notification(conf.messages["endscreen"])

    while conf.ENDSCREEN:
        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time

        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                objs.effect.start_fade_out()
                objs.game_music.play_fadeout()
                conf.next_scene = "quit"

        keys = pygame.key.get_pressed()

        objs.notification.is_clicked()

        if conf.next_scene == "endscreen" or ((conf.next_scene == "main_menu" or conf.next_scene == "quit") and objs.effect.get_active()):
            utils.draw_scene("endscreen", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs)

        if conf.waiting_for_release:
            if not any(keys):
                conf.waiting_for_release = False
        elif any(keys):
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "main_menu"

        if conf.next_scene == "main_menu" and not objs.effect.get_active():
            utils.save_player_stats(conf.PLAYER_NAME, conf.stats)
            conf.ENDSCREEN = False
            conf.MAIN_MENU = True
            conf.faded_in = False
            conf.GAME_RUNNING = False

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.WINDOW_OPEN = False
            conf.MAIN_MENU = False
            conf.ENDSCREEN = False
            conf.QUITTING_GAME = True

        objs.effect.update(delta_time, py_objs.screen)
        pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
