import pygame, sys, math, os

import modules.config as conf
import modules.objects as objs
import modules.pygame_objects as py_objs

from modules.utils import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jump King")
pygame.display.set_icon(pygame.image.load(os.path.join(conf.fallback_resources_folder, "other", "icon.png")))
conf.VOLUME_MASTER = conf.def_stats["volume_master"]
conf.VOLUME_SFX = conf.def_stats["volume_sfx"]
conf.VOLUME_MUSIC = conf.def_stats["volume_music"]
objs.game_music.set_volume(py_objs.sfx, conf.VOLUME_MASTER, conf.VOLUME_SFX, conf.VOLUME_MUSIC)

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
        # LOGIN ===========================================================================
        # If we havent already started fade-in (first frame) we start fade-in
        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time
        events = pygame.event.get()

        for event in events:
            # If we close the window
            if event.type == pygame.QUIT:
                objs.effect.start_fade_out()
                conf.next_scene = "quit"
                objs.game_music.play_fadeout()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                set_permission_to_interact(pygame.mouse.get_pos(), objs.login_ui_elements)

        objs.username_input.capture_input(events)
        objs.password_input.capture_input(events)
        objs.campaign_dropdown.handle_highliting(events)
        objs.notification.clear_notification_if_clicked(events)

        if objs.submit_button.is_clicked(events):
            if not conf.submit_button_already_clicked:
                py_objs.sfx["click"].play()
            
            conf.CAMPAIGN = objs.campaign_dropdown.get_selection()
            if conf.CAMPAIGN != "":
                conf.next_scene = log_in(objs.username_input.input_text, objs.password_input.input_text, objs.title, objs.effect, objs.username_input, objs.password_input, conf.stats)
                
                # We only want transition if music is different for login and main menu
                if py_objs.menu_musics["login"] != py_objs.menu_musics["main_menu"]:
                    objs.game_music.play_fadeout()
                conf.submit_button_already_clicked = True
                conf.PLAYER_NAME = objs.username_input.input_text
            else:
                conf.next_scene = "login"
                objs.notification.show_notification(conf.messages["err_no_campaign_selected"])

        if objs.quit_button.is_clicked(events):
            if not conf.quit_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.effect.start_fade_out()
            objs.game_music.play_fadeout()
            conf.next_scene = "quit"
            conf.quit_button_already_clicked = True

        draw_scene("login", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, 0, delta_time, events = events)
        objs.effect.update(delta_time, py_objs.screen)

        if conf.next_scene == "main_menu" and not objs.effect.get_active():
            conf.MAIN_MENU = True
            conf.LOGIN = False

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.LOGIN = False
            conf.WINDOW_OPEN = False
            conf.QUITTING_GAME = True

        pygame.display.flip()
        # LOGIN ===========================================================================

    conf.faded_in = False
    conf.play_button_already_clicked = False
    conf.quit_button_already_clicked = False
    conf.logout_button_already_clicked = False

    objs.notification.delete_notification()
    conf.current_menu = "main_menu"
    objs.game_music.play_menu(conf.current_menu)

    if not conf.QUITTING_GAME and conf.CAMPAIGN != conf.currently_loaded_campaign:
        py_objs.tile_images, py_objs.player_images, py_objs.babe_images, py_objs.buttons, py_objs.scaled_bgs, py_objs.ui_bgs, py_objs.sfx, py_objs.fonts = load_resources()
        conf.currently_loaded_campaign = conf.CAMPAIGN

    py_objs.clock.tick()

    while conf.MAIN_MENU:
        # MAIN MENU ===========================================================================
        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time
        events = pygame.event.get()

        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        # If we close the window
        for event in events:
            if event.type == pygame.QUIT:
                objs.effect.start_fade_out()
                objs.game_music.play_fadeout()
                conf.next_scene = "quit"

        if objs.play_button.is_clicked(events):
            if not conf.play_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "running"
            conf.play_button_already_clicked = True
            conf.stats["games_started"] += 1

        if objs.quit_button.is_clicked(events):
            if not conf.quit_button_already_clicked:
                py_objs.sfx["click"].play()
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "quit"
            conf.quit_button_already_clicked = True

        if objs.logout_button.is_clicked(events):
            if not conf.logout_button_already_clicked:
                py_objs.sfx["click"].play()

            # We only want transition if music is different for login and main menu
            if py_objs.menu_musics["login"] != py_objs.menu_musics["main_menu"]:
                objs.game_music.play_fadeout()
            conf.next_scene = "login"
            objs.effect.start_fade_out()
            conf.logout_button_already_clicked = True
            objs.username_input.input_text = ""
            objs.password_input.input_text = ""
            objs.username_input.text.text = ""
            objs.password_input.text.text = ""
            objs.username_input.text.update()
            objs.password_input.text.update()

        draw_scene("main_menu", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, events = events)
        objs.effect.update(delta_time, py_objs.screen)

        if conf.next_scene == "running" and not objs.effect.get_active():
            conf.MAIN_MENU = False
            conf.GAME_RUNNING = True

        if conf.next_scene == "quit" and not objs.effect.get_active():
            save_player_stats(conf.PLAYER_NAME, "quitting")
            conf.MAIN_MENU = False
            conf.WINDOW_OPEN = False
            conf.QUITTING_GAME = True

        if conf.next_scene == "login" and not objs.effect.get_active():
            conf.LOGIN = True
            conf.MAIN_MENU = False
            save_player_stats(conf.PLAYER_NAME, "logout")

        pygame.display.flip()
        # MAIN MENU ===========================================================================

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
        objs.babe.find_position(py_objs.babe_position, objs.levels[len(objs.levels) - 1], conf.tile_size, conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT) # Find babe position based on config file or automatically
    
    py_objs.clock.tick()

    while conf.GAME_RUNNING:
        # GAME LOOP ===========================================================================
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
        objs.player.manage_end_animation(delta_time = delta_time)
        objs.babe.animate(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                conf.stats["ragequits"] += 1
                save_player_stats(conf.PLAYER_NAME, "ragequit", objs.player.rect.y)
                objs.game_music.play_fadeout()
                objs.effect.start_fade_out()
                conf.next_scene = "quit"

        if not objs.babe.end_animation_status == "started" and objs.babe.check_for_ending(objs.player.get_rect()) == "start_animation":
            objs.player.manage_end_animation(objs.babe.get_pos(), first_frame = True)
        
        if objs.babe.check_for_ending(objs.player.get_rect()) == "end_game" and not conf.game_ended and conf.next_scene != "endscreen":
            conf.next_scene = "endscreen"
            objs.effect.start_fade_out()
            conf.game_stats["finish_time"] = time
            objs.player.manage_end_animation(delta_time = 0, stop = True)
            objs.game_music.play_fadeout()
            conf.can_play_music = False

        if conf.can_play_music:
            objs.game_music.play_level(conf.current_level)

        if conf.next_scene == "endscreen" and not objs.effect.get_active():
            conf.GAME_RUNNING = False
            conf.ENDSCREEN = True
            conf.game_ended = True
            conf.can_play_music = False

        if conf.next_scene == "quit" and not objs.effect.get_active():
            conf.GAME_RUNNING = False
            conf.WINDOW_OPEN = False
            conf.ENDSCREEN = False
            conf.QUITTING_GAME = True
            conf.game_ended = True

        if not conf.game_ended:
            draw_scene("running", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, conf.current_level, delta_time, events = events)

        objs.effect.update(delta_time, py_objs.screen)
        pygame.display.flip()
        # GAME LOOP ===========================================================================

    conf.faded_in = False

    # To ensure music keeps playing uninterrupted between login and main menu
    if conf.next_scene != "login":
        pygame.mixer.music.stop()
        conf.current_menu = "endscreen"
    objs.game_music.play_menu(conf.current_menu)

    objs.babe.reset()

    objs.notification.delete_notification()
    objs.notification.show_notification(conf.messages["endscreen"])

    py_objs.clock.tick()
    finish_time = pygame.time.get_ticks()

    while conf.ENDSCREEN:
        # ENDSCREEN ===========================================================================
        delta_time = py_objs.clock.tick(conf.FPS_cap_menus) / 1000.0
        conf.time_spent += delta_time
        events = pygame.event.get()

        if not conf.faded_in:
            objs.effect.start_fade_in()
            conf.faded_in = True

        for event in events:
            if event.type == pygame.QUIT:
                objs.effect.start_fade_out()
                objs.game_music.play_fadeout()
                conf.next_scene = "quit"
            
            if event.type == pygame.MOUSEBUTTONUP:
                objs.effect.start_fade_out()
                objs.game_music.play_fadeout()
                conf.next_scene = "main_menu"

        keys = pygame.key.get_pressed()

        objs.notification.clear_notification_if_clicked(events)

        if conf.next_scene == "endscreen" or ((conf.next_scene == "main_menu" or conf.next_scene == "quit") and objs.effect.get_active()):
            draw_scene("endscreen", py_objs.screen, py_objs.scaled_bgs, py_objs.ui_bgs, events = events)

        if conf.waiting_for_release:
            if not any(keys):
                conf.waiting_for_release = False
        elif any(keys):
            objs.game_music.play_fadeout()
            objs.effect.start_fade_out()
            conf.next_scene = "main_menu"

        if conf.next_scene == "main_menu" and not objs.effect.get_active():
            conf.game_stats["time_on_endscreen"] = pygame.time.get_ticks() - finish_time
            save_player_stats(conf.PLAYER_NAME, "game_ended")
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
        # ENDSCREEN ===========================================================================

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
