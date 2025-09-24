import pygame, sys, math

from modules.config import *
from modules.objects import *
from modules.pygame_objects import *
from modules.utils import log_in, draw_scene, load_player_stats, save_player_stats

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Jump King")
pygame.display.set_icon(pygame.image.load(f"{resources_folder}/other/icon.png"))

while WINDOW_OPEN:
    music.main_menu()
    screen.blit(scaled_bgs[0], (-600, 0))
    submit_button_already_clicked = False
    notification.delete_notification()
    faded_in = False

    clock.tick()
    while login:
        if not faded_in:
            effect.start_fade_in()
            faded_in = True

        delta_time = clock.tick(60) / 1000.0 #tisto je FPS cap
        time_spent += delta_time
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                effect.start_fade_out()
                next_scene = "quit"
                music.play(current_level, endscreen, "fadeout")
        
        username_input.capture_input(events, username_text, password_text)
        password_input.capture_input(events, username_text, password_text)
        cursor.update()

        if submit_button.is_clicked():
            if not submit_button_already_clicked:
                sfx["click"].play()
            submit_button_already_clicked = True
            PLAYER_NAME = username_input.input_text
            next_scene = log_in(username_input.input_text, password_input.input_text, title, effect, username_input, password_input, username_text, password_text, stats)

        if quit_button.is_clicked():
            if not quit_button_already_clicked:
                sfx["click"].play()
            effect.start_fade_out()
            music.play(current_level, endscreen, "fadeout")
            next_scene = "quit"
            quit_button_already_clicked = True

        draw_scene("login", screen, 0, delta_time)
        effect.update(delta_time, screen)

        if next_scene == "main_menu" and not effect.get_active():
            main_menu = True
            login = False

        if next_scene == "quit" and not effect.get_active():
            login = False
            WINDOW_OPEN = False

        pygame.display.flip()

    if not loaded_player_stats:
        load_player_stats(PLAYER_NAME, stats)

    faded_in = False
    play_button_already_clicked = False
    quit_button_already_clicked = False
    logout_button_already_clicked = False
    
    notification.delete_notification()

    while main_menu:
        delta_time = clock.tick(60) / 1000.0 #tisto je FPS cap
        time_spent += delta_time

        if not faded_in:
            effect.start_fade_in()
            faded_in = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                effect.start_fade_out()
                music.play("fadeout")
                next_scene = "quit"

        if play_button.is_clicked():
            if not play_button_already_clicked:
                sfx["click"].play()
            music.play(current_level, endscreen, "fadeout")
            effect.start_fade_out()
            next_scene = "running"
            play_button_already_clicked = True
            stats["games_started"] += 1
        
        if quit_button.is_clicked():
            if not quit_button_already_clicked:
                sfx["click"].play()
            music.play(current_level, endscreen, "fadeout")
            effect.start_fade_out()
            next_scene = "quit"
            quit_button_already_clicked = True

        if logout_button.is_clicked():
            if not logout_button_already_clicked:
                sfx["click"].play()
            next_scene = "login"
            effect.start_fade_out()
            music.play(current_level, endscreen, "fadeout")
            logout_button_already_clicked = True
            username_input.input_text = ""
            password_input.input_text = ""
            password_input.masked_text = ""
            username_text.text = ""
            password_text.text = ""
            username_text.update()
            password_text.update()

        draw_scene("main_menu", screen)
        effect.update(delta_time, screen)

        if next_scene == "running" and not effect.get_active():
            main_menu = False
            running = True
        if next_scene == "quit" and not effect.get_active():
            main_menu = False
            WINDOW_OPEN = False
        if next_scene == "login" and not effect.get_active():
            login = True
            main_menu = False
            save_player_stats(PLAYER_NAME, stats)

        pygame.display.flip()

    pygame.mixer.music.stop()
    music.play(current_level, endscreen)
    faded_in = False
    game_ended = False
    current_level = 0
    level = levels[current_level]
    player.reset_position(SCREEN_WIDTH / 2 - player_size / 2, 891)
    player.reset_values()
    notification.delete_notification()
    start_time = pygame.time.get_ticks()

    while running:
        if not faded_in:
            effect.start_fade_in()
            faded_in = True
        delta_time = clock.tick(144) / 1000.0 #tisto je FPS cap
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
                music.play(current_level, endscreen, "fadeout")
                effect.start_fade_out()
                next_scene = "quit"

        if main_babe.check_for_ending(player) and not game_ended:
            next_scene = "endscreen"
            music.play(current_level, endscreen, "fadeout")
            effect.start_fade_out()
            stats["games_played"] += 1
            player.can_move = False
            player.rect.y = main_babe.rect.y + 10
            player.rect.x = main_babe.rect.x - 80
            player.current_frame = 0
            player.direction = "right"

        if can_play_music:
            music.play(current_level, endscreen)
            
        if next_scene == "endscreen" and not effect.get_active():
            can_play_music = False
            endscreen = True
            running = False
            game_ended = True

        if next_scene == "quit" and not effect.get_active():
            running = False
            WINDOW_OPEN = False
            endscreen = False
            game_ended = True

        if not game_ended:
            draw_scene("running", screen, current_level, delta_time)

        effect.update(delta_time, screen)
        pygame.display.flip()

    faded_in = False
    pygame.mixer.music.stop()
    music.play(current_level, endscreen)
    notification.delete_notification()
    notification.show_notification(messages["endscreen"])

    while endscreen:
        delta_time = clock.tick(60) / 1000.0 # tisto je FPS cap
        time_spent += delta_time

        if not faded_in:
            effect.start_fade_in()
            faded_in = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                effect.start_fade_out()
                music.play(current_level, endscreen, "fadeout")
                next_scene = "quit"
        
        keys = pygame.key.get_pressed()

        notification.is_clicked()

        if next_scene == "endscreen" or ((next_scene == "main_menu" or next_scene == "quit") and effect.get_active()):
            draw_scene("endscreen", screen)

        if waiting_for_release:
            if not any(keys):
                waiting_for_release = False
        elif any(keys):
            music.play(current_level, endscreen, "fadeout")
            effect.start_fade_out()
            next_scene = "main_menu"
            
        if next_scene == "main_menu" and not effect.get_active():
            save_player_stats(PLAYER_NAME, stats)
            endscreen = False
            main_menu = True
            faded_in = False
            running = False

        if next_scene == "quit" and not effect.get_active():
            WINDOW_OPEN = False
            main_menu = False
            endscreen = False

        effect.update(delta_time, screen)
        pygame.display.flip()

    notification.delete_notification()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()