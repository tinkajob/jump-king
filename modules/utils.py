import os, json, hashlib, pygame

from modules.config import (
    level_paths,
    tile_size,
    stats_folder,
    def_stats,
    game_stats,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from modules.platform import Platform
import modules.objects as objects
from modules.pygame_objects import endscreens, scaled_bgs, tile_images


def log_in(
    username,
    password,
    title,
    effect,
    username_input,
    password_input,
    username_text,
    password_text,
    stats,
):
    load_player_stats(username, stats)
    if username != "" and username.lower() != "guest":  # ce je player
        if stats.get("password", 0) == 0:
            stats["password"] = hash_password(password)
            title.text = f"Welcome, {username}!"
            title.update()
            effect.start_fade_out()
            return "main_menu"

        elif hash_password(password) != stats["password"]:
            username_input.input_text = ""
            password_input.input_text = ""
            password_input.masked_text = ""
            username_text.text = ""
            password_text.text = ""
            username_text.update()
            password_text.update()
        else:
            title.text = f"Welcome back, {username}!"
            title.update()
            effect.start_fade_out()
            return "main_menu"
    else:
        title.text = "Welcome!"
        title.update()
        effect.start_fade_out()
        return "main_menu"

    save_player_stats(username, stats)


def hash_password(password):
    password = str(password)
    return hashlib.sha256(password.encode()).hexdigest()


def load_level_from_file(level_number):
    level = []
    with open(level_paths[level_number], "r") as file:
        for line_number, line in enumerate(file, start=1):
            row = []
            for char in line.strip():
                if char.isdigit():
                    row.append(int(char))
            level.append(row)
    return level


def create_level(level_data):
    rows = len(level_data)
    cols = len(level_data[0]) if rows > 0 else 0
    platforms = []
    relative_offfsets = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    for row_index, row in enumerate(level_data):
        for col_index, col in enumerate(row):
            if col != 0:
                neighbors = []
                for relative_x, relative_y in relative_offfsets:
                    offset_row, offset_col = (
                        row_index + relative_y,
                        col_index + relative_x,
                    )  # dejanski offseti
                    if (offset_row >= 0 and offset_row < rows) and (
                        offset_col >= 0 and offset_col < cols
                    ):
                        neighbors.append(level_data[offset_row][offset_col])
                    else:
                        neighbors.append(0)
                platforms.append(
                    Platform(
                        col_index * tile_size,
                        row_index * tile_size,
                        tile_size,
                        tile_size,
                        autotile(neighbors),
                    )
                )
    return platforms


def autotile(neighbors):
    if (
        neighbors[1] == 0
        and neighbors[3] == 0
        and neighbors[4] == 0
        and neighbors[6] == 0
    ):  # enojna
        return 0
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # cela polna
        return 5
    if (
        neighbors[0] == 0
        and neighbors[1] == 0
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 1
    ):  # kot levo zgoraj
        if neighbors[7] == 1:
            return 1
        elif neighbors[7] == 0:
            return 16
    if (
        neighbors[0] == 0
        and neighbors[1] == 0
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[6] == 1
    ):  # kot desno zgoraj
        if neighbors[5] == 1:
            return 3
        elif neighbors[5] == 0:
            return 17
    if (
        neighbors[0] == 0
        and neighbors[1] == 0
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # zgoraj, daljsa
        return 2
    if (
        neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # dvojna stranska levo
        return 4
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[5] == 1
        and neighbors[6] == 1
    ):  # dvojna stranska desno
        return 6
    if (
        neighbors[1] == 1
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 0
        and neighbors[7] == 0
    ):  # kot levo spodaj
        if neighbors[2] == 1:
            return 7
        elif neighbors[2] == 0:
            return 18
    if (
        neighbors[1] == 1
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[5] == 0
        and neighbors[6] == 0
        and neighbors[7] == 0
    ):  # kot desno spodaj
        if neighbors[0] == 1:
            return 9
        elif neighbors[0] == 0:
            return 19
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # dvojna spodnja
        return 8
    if (
        neighbors[1] == 0
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # enojna stranska leva
        return 10
    if (
        neighbors[1] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # enojna horizontalna
        return 11
    if (
        neighbors[1] == 0
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[6] == 0
    ):  # enojna stranska desna
        return 12
    if (
        neighbors[1] == 0
        and neighbors[3] == 0
        and neighbors[4] == 0
        and neighbors[6] == 1
    ):  # enojna vrhna
        return 13
    if (
        neighbors[1] == 1
        and neighbors[3] == 0
        and neighbors[4] == 0
        and neighbors[6] == 1
    ):  # enojna vertikalna
        return 14
    if (
        neighbors[1] == 1
        and neighbors[3] == 0
        and neighbors[4] == 0
        and neighbors[6] == 0
    ):  # enojna vrhna
        return 15
    if (
        neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # leva stranska T
        return 20
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[5] == 0
        and neighbors[6] == 1
    ):  # desna stranska T
        return 21
    if (
        neighbors[1] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # zgornja stranska T
        return 22
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # spodnja stranska T
        return 23
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce na 4
        return 24
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # krizisce zgornji dve
        return 25
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce spodnji dve
        return 26
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce desni dve
        return 27
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # krizisce levi dve
        return 28
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce tri - ZL
        return 29
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce tri - ZD
        return 30
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # krizisce tri - SL
        return 31
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # krizisce tri - SD
        return 32
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # dvojna spodnja + ZD
        return 33
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[6] == 0
    ):  # dvojna spodnja + ZL
        return 34
    if (
        neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # dvojna zgornja + SL
        return 35
    if (
        neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # dvojna zgornja + SD
        return 36
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[5] == 1
        and neighbors[6] == 1
    ):  # dvojna stranska + ZL
        return 37
    if (
        neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # dvojna stranska + ZD
        return 38
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[3] == 1
        and neighbors[4] == 0
        and neighbors[5] == 0
        and neighbors[6] == 1
    ):  # dvojna stranska + SL
        return 39
    if (
        neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 0
        and neighbors[4] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # dvojna stranska + SD
        return 40
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # samo ZL
        return 41
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # samo ZD
        return 42
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # samo SL
        return 43
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # samo SD
        return 44
    if (
        neighbors[0] == 0
        and neighbors[1] == 1
        and neighbors[2] == 1
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 1
        and neighbors[6] == 1
        and neighbors[7] == 0
    ):  # diagonala ZL in SD
        return 45
    if (
        neighbors[0] == 1
        and neighbors[1] == 1
        and neighbors[2] == 0
        and neighbors[3] == 1
        and neighbors[4] == 1
        and neighbors[5] == 0
        and neighbors[6] == 1
        and neighbors[7] == 1
    ):  # iagonala ZD in SL
        return 46
    return 0  # prepisi da bo ku binary tree?


def draw_scene(scene, screen, current_level=0, delta_time=0):
    if scene == "main_menu":
        screen.blit(scaled_bgs[0], (-600, 0))
        objects.play_button.draw(screen)
        objects.quit_button.draw(screen)
        objects.logout_button.draw(screen)
        objects.title.draw(screen)
        objects.play_text.draw(screen)
        objects.quit_text.draw(screen)
        objects.logout_text.draw(screen)

    elif scene == "running":
        screen.blit(scaled_bgs[current_level + 1], (0, 0))
        screen.blit(objects.level_surfaces[current_level], (0, 0))
        objects.player.draw(screen)
        objects.main_babe.draw(screen, current_level, delta_time)
        objects.timer_text.draw(screen)
        objects.FPS_text.draw(screen)

    elif scene == "endscreen":
        screen.blit(endscreens[0], (-6, 0))
        objects.endscreen_text.draw(screen)

    elif scene == "login":
        screen.blit(scaled_bgs[0], (-600, 0))
        objects.submit_button.draw(screen)
        objects.quit_button.draw(screen)
        objects.username_input.draw(screen)
        objects.password_input.draw(screen)
        objects.submit_text.draw(screen)
        objects.quit_text.draw(screen)
        objects.username_text.draw(screen)
        objects.password_text.draw(screen)
        objects.cursor.draw(screen, delta_time)


def save_player_stats(PLAYER_NAME, stats):
    os.makedirs(stats_folder, exist_ok=True)
    update_player_stats(stats)

    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")

    with open(filepath, "w") as file:
        json.dump(stats, file, indent=4)


def load_player_stats(PLAYER_NAME, stats):
    if PLAYER_NAME != "":
        filepath = os.path.join(stats_folder, f"{PLAYER_NAME}_stats.json")
    else:
        filepath = os.path.join(stats_folder, "guest_stats.json")

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            loaded_stats = json.load(file)
        stats.clear()
        stats.update(loaded_stats)
    else:
        for stat in stats:
            stats[stat] = 0

    for key, value in def_stats.items():
        if key not in stats:
            stats[key] = value


def wipe_stats(stats):
    for stat in stats:
        stats[stat] = 0
    save_player_stats()


def update_player_stats(stats):
    # tle do pravila za use statse kku se jih zdruzuje
    stats["total_jumps"] += game_stats["jumps"]
    if stats["min_jumps_in_game"] > game_stats["jumps"]:
        stats["min_jumps_in_game"] = game_stats["jumps"]
    if stats["max_jumps_in_game"] < game_stats["jumps"]:
        stats["max_jumps_in_game"] = game_stats["jumps"]

    stats["total_falls"] += game_stats["falls"]
    if stats["min_falls_in_game"] > game_stats["falls"]:
        stats["min_falls_in_game"] = game_stats["falls"]
    if stats["max_falls_in_game"] < game_stats["falls"]:
        stats["max_falls_in_game"] = game_stats["falls"]

    stats["head_bounces"] += game_stats["head_bounces"]
    stats["wall_bounces"] += game_stats["wall_bounces"]

    if stats["best_screen"] < game_stats["best_screen"]:
        stats["best_screen"] = game_stats["best_screen"]

    stats["total_distance_climbed"] += game_stats["distance_climbed"]
    stats["total_distance_descended"] += game_stats["distance_descended"]
    if stats["highest_distance_climbed_in_game"] < game_stats["distance_climbed"]:
        stats["highest_distance_climbed_in_game"] = game_stats["distance_climbed"]
    if stats["highest_distance_descended_in_game"] < game_stats["distance_descended"]:
        stats["highest_distance_descended_in_game"] = game_stats["distance_descended"]


def create_level_surface(level):
    level_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for platform in level:
        level_surface.blit(
            tile_images[platform.type], (platform.rect.x, platform.rect.y)
        )

    return level_surface
