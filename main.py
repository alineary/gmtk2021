import time

import pygame
import sys
import random

import utils
import wagon_spawner
import os
import gameobjects
import sound

from GUI.menus import PauseMenu, EndMenu

STATION_IMAGE = pygame.image.load(os.path.join('resources', 'station.png'))
SAND_IMAGE = pygame.image.load(os.path.join('resources', 'sand.png'))
LOGO = pygame.image.load(os.path.join('resources', 'wildwagons.png'))
CACTI = [pygame.image.load(os.path.join('resources', 'cactus_1.png')),
         pygame.image.load(os.path.join('resources', 'cactus_2.png')),
         pygame.image.load(os.path.join('resources', 'cactus_3.png'))]
PLATFORM = [pygame.transform.flip(pygame.image.load(os.path.join('resources', 'right_platform.png')),True, False),
            pygame.image.load(os.path.join('resources', 'middle_platform.png')),
            pygame.image.load(os.path.join('resources', 'right_platform.png'))]
MAX_WAGONS_ON_TRACK = 5
ENGINE_OFFSET = 800
menu_was_enabled = False

def setup():
    global screen
    global clock
    global running
    global screen
    global score
    global main_menu
    global main_menu_parent
    global wagon_group
    global sprite_group
    global draggable_sprites
    global background_group
    global cactus_group
    global station_group
    global track_group
    global spawn_track
    global end_screen_parent
    global end_screen
    global train_group
    global platform_group

    pygame.init()
    screen = pygame.display.set_mode([1280, 720])
    pygame.display.set_caption("Wild Wagons")
    pygame.display.set_icon(LOGO)

    sound.play_music()

    clock = pygame.time.Clock()
    running = True

    score = 0

    sprite_group = pygame.sprite.Group()

    # Trains
    train_group = pygame.sprite.Group()

    # Wagon
    wagon_group = pygame.sprite.Group()
    draggable_sprites = []

    # Tracks
    track_group = pygame.sprite.Group()
    spawn_track = gameobjects.Track(pygame.Vector2(0, 250), 17, MAX_WAGONS_ON_TRACK)
    track1 = gameobjects.Track(pygame.Vector2(0, 400), 26, MAX_WAGONS_ON_TRACK, ENGINE_OFFSET)
    track2 = gameobjects.Track(pygame.Vector2(0, 550), 26, MAX_WAGONS_ON_TRACK, ENGINE_OFFSET)
    track_group.add(spawn_track)
    track_group.add(track1)
    track_group.add(track2)

    # Station
    station_group = pygame.sprite.Group()
    station = gameobjects.Beauty(STATION_IMAGE, pygame.Vector2(1030, 200), 250)
    station_group.add(station)

    # Background
    background_group = pygame.sprite.Group()
    background = gameobjects.Background(SAND_IMAGE)
    background_group.add(background)

    # Platforms
    platform_group = pygame.sprite.Group()
    platform_left = gameobjects.Beauty(PLATFORM[0], pygame.Vector2(310,440), 200)

    platform = gameobjects.Beauty(PLATFORM[1], pygame.Vector2(400, 440), 200)
    platform_group.add(platform)
    platform = gameobjects.Beauty(PLATFORM[1], pygame.Vector2(400 + 160, 440), 200)
    platform_group.add(platform)

    platform_right = gameobjects.Beauty(PLATFORM[2], pygame.Vector2(80 + 640, 440), 200)
    platform_group.add(platform_left)
    platform_group.add(platform_right)

    platform_left = gameobjects.Beauty(PLATFORM[0], pygame.Vector2(310,140), 200)
    platform_group.add(platform_left)
    o = 60
    for i in range(0, 5):
        platform = gameobjects.Beauty(PLATFORM[1], pygame.Vector2(0 + o, 140), 200)
        platform_group.add(platform)
        o += 160

    platform_right = gameobjects.Beauty(PLATFORM[2], pygame.Vector2(80 + 640, 140), 200)
    platform_group.add(platform_right)

    # Cactus
    cactus_group = pygame.sprite.Group()
    for i in range(0, 100):
        x = random.randrange(32, 1248, 1)
        y = random.randrange(32, 688, 1)
        beauty = gameobjects.Beauty(random.choice(CACTI), pygame.Vector2(x, y), 70)
        if len(pygame.sprite.spritecollide(beauty, station_group, False)) > 0 or \
                len(
                    pygame.sprite.spritecollide(beauty, cactus_group, False)) > 0 or \
                len(
                    pygame.sprite.spritecollide(beauty, track_group, False)) > 0 or \
                len(
                    pygame.sprite.spritecollide(beauty, platform_group, False)) > 0:
            beauty.kill()
        else:
            cactus_group.add(beauty)

    main_menu_parent = PauseMenu((1280, 720))
    main_menu = main_menu_parent.pause_menu
    end_screen_parent = EndMenu((1280, 720))
    end_screen = end_screen_parent.menu
    end_screen.disable()


def reset():
    global score

    for track in track_group:
        track.wagons = []
        if track.engine is not None:
            track.engine.kill()
            track.init_engine(ENGINE_OFFSET)
    for wagon in wagon_group:
        wagon.kill()
    score = 0
    wagon_spawner.timer = utils.Timer(wagon_spawner.START_WAGON_SPAWN_COOLDOWN)


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()
    for track in track_group:
        track.update()


def draw():
    screen.fill((255, 255, 255))

    background_group.draw(screen)
    platform_group.draw(screen)
    cactus_group.draw(screen)
    track_group.draw(screen)
    wagon_group.draw(screen)
    sprite_group.draw(screen)
    station_group.draw(screen)
    train_group.draw(screen)

    for track in track_group:
        if track.engine is not None:
            utils.render_timer(screen, int(track.engine.timer.countdown_time.total_seconds()), track.position + track.timer_offset)

    #score
    utils.render_score(screen, score)

    # menu
    if main_menu.is_enabled():
        main_menu.update(events)
        if main_menu.is_enabled():
            main_menu.draw(screen)

    if end_screen.is_enabled():
        end_screen.update(events)
        if end_screen.is_enabled():
            end_screen.draw(screen)

    pygame.display.update()


def game_loop():
    global events
    global menu_was_enabled

    setup()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu_parent.get_scores()
                    main_menu.toggle()
        if not main_menu.is_enabled():
            update()
            utils.set_delta_time()
        menu_was_enabled = main_menu.is_enabled() or end_screen.is_enabled()
        draw()
        clock.tick(60)
