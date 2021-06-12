import pygame
import sys
import wagon_spawner


def setup():
    global screen
    global clock
    global running
    global screen
    global wagon_group
    global sprite_group
    global draggable_sprites

    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Wild Wagons")
    clock = pygame.time.Clock()
    running = True

    wagon_group = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()


def draw():
    screen.fill((255, 255, 255))
    wagon_group.draw(screen)
    sprite_group.draw(screen)
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
