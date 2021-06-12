import pygame
import sys
import random
import gameobjects
import wagon_spawner
import os

STATION_IMAGE = pygame.image.load(os.path.join('resources', 'station.png'))
SAND_IMAGE = pygame.image.load(os.path.join('resources', 'sand.png'))
CACTI = [pygame.image.load(os.path.join('resources', 'cactus_1.png')),
         pygame.image.load(os.path.join('resources', 'cactus_2.png')),
         pygame.image.load(os.path.join('resources', 'cactus_3.png'))]


def setup():
    global screen
    global clock
    global running
    global screen
    global wagon_group
    global sprite_group
    global draggable_sprites
    global background_group
    global cactus_group
    global station_group

    pygame.init()
    screen = pygame.display.set_mode([1280, 720])
    pygame.display.set_caption("Wild Wagons")
    clock = pygame.time.Clock()
    running = True

    wagon_group = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()

    # Station
    station_group = pygame.sprite.Group()
    station = gameobjects.Beauty(STATION_IMAGE, pygame.Vector2(1000, 150), 250)

    station_group.add(station)

    # Background
    background_group = pygame.sprite.Group()
    background = gameobjects.Background(SAND_IMAGE)
    background_group.add(background)

    # Beauties
    cactus_group = pygame.sprite.Group()
    for i in range(0, 20):
        x = random.randrange(32, 1248, 1)
        y = random.randrange(32, 688, 1)
        beauty = gameobjects.Beauty(random.choice(CACTI), pygame.Vector2(x, y), 70)
        if len(pygame.sprite.spritecollide(beauty, station_group, False)) > 0 or len(pygame.sprite.spritecollide(beauty, cactus_group, False)) > 0:
            beauty.kill()
        else:
            cactus_group.add(beauty)


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()


def draw():
    screen.fill((255, 255, 255))
    background_group.draw(screen)
    cactus_group.draw(screen)
    wagon_group.draw(screen)
    sprite_group.draw(screen)
    station_group.draw(screen)
    pygame.display.update()


def game_loop():
    global events

    setup()
    while running:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)

        update()

        draw()
        clock.tick(60)
