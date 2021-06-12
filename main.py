import pygame
import sys
import wagon_spawner
import gameobjects

MAX_WAGONS_ON_TRACK = 5

def setup():
    global screen
    global clock
    global running
    global screen
    global wagon_group
    global sprite_group
    global draggable_sprites
    global track_group
    global spawn_track

    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True
    sprite_group = pygame.sprite.Group()

    # Wagon
    wagon_group = pygame.sprite.Group()
    draggable_sprites = []

    # Tracks
    track_group = pygame.sprite.Group()
    spawn_track = gameobjects.Track(pygame.Vector2(0, 0), 15, MAX_WAGONS_ON_TRACK)
    track1 = gameobjects.Track(pygame.Vector2(0, 200), 15, MAX_WAGONS_ON_TRACK)
    track2 = gameobjects.Track(pygame.Vector2(0, 400), 15, MAX_WAGONS_ON_TRACK)
    track_group.add(spawn_track)
    track_group.add(track1)
    track_group.add(track2)


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()
    for track in track_group:
        track.update()


def draw():
    screen.fill((0, 0, 0))
    track_group.draw(screen)
    sprite_group.draw(screen)
    wagon_group.draw(screen)
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
