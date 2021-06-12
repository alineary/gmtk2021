import pygame
import sys
import wagon_spawner


def setup():
    global clock
    global running
    global screen
    global wagon_group
    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True

    # Wagon
    wagon_group = pygame.sprite.Group()


def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()


def draw():
    screen.fill((0, 0, 0))
    wagon_group.draw(screen)
    pygame.display.update()


def game_loop():
    setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        update()

        draw()
        clock.tick(60)
