import pygame
import sys
import random
import wagon_spawner
import os
import gameobjects

from GUI.pause_menu import PauseMenu

STATION_IMAGE = pygame.image.load(os.path.join('resources', 'station.png'))
SAND_IMAGE = pygame.image.load(os.path.join('resources', 'sand.png'))
LOGO = pygame.image.load(os.path.join('resources', 'wildwagons.png'))
CACTI = [pygame.image.load(os.path.join('resources', 'cactus_1.png')),
         pygame.image.load(os.path.join('resources', 'cactus_2.png')),
         pygame.image.load(os.path.join('resources', 'cactus_3.png'))]
MAX_WAGONS_ON_TRACK = 5
ENGINE_OFFSET = 800


def setup():
    global screen
    global clock
    global running
    global screen
    global menu
    global wagon_group
    global sprite_group
    global draggable_sprites
    global background_group
    global cactus_group
    global station_group
    global track_group
    global spawn_track

    pygame.init()
    screen = pygame.display.set_mode([1280, 720])
    pygame.display.set_caption("Wild Wagons")
    pygame.display.set_icon(LOGO)

    clock = pygame.time.Clock()
    running = True
    menu = PauseMenu((1280, 720)).pause_menu
    sprite_group = pygame.sprite.Group()

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

    # Cactus
    cactus_group = pygame.sprite.Group()
    for i in range(0, 30):
        x = random.randrange(32, 1248, 1)
        y = random.randrange(32, 688, 1)
        beauty = gameobjects.Beauty(random.choice(CACTI), pygame.Vector2(x, y), 70)
        if len(pygame.sprite.spritecollide(beauty, station_group, False)) > 0 or \
                len(
                    pygame.sprite.spritecollide(beauty, cactus_group, False)) > 0 or \
                len(
                    pygame.sprite.spritecollide(beauty, track_group, False)) > 0:
            beauty.kill()
        else:
            cactus_group.add(beauty)


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()
    for track in track_group:
        track.update()


def draw():
    screen.fill((255, 255, 255))

    background_group.draw(screen)
    cactus_group.draw(screen)
    track_group.draw(screen)
    wagon_group.draw(screen)
    sprite_group.draw(screen)
    station_group.draw(screen)

    # menu
    if menu.is_enabled():
        menu.update(events)
        if menu.is_enabled():
            menu.draw(screen)

    pygame.display.update()


def game_loop():
    global events

    setup()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.toggle()
        if not menu.is_enabled():
            update()
        draw()
        clock.tick(60)
