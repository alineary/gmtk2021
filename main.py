import pygame
import sys


def setup():
    global clock
    global running
    global screen
    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True


def update():
    print("")


def draw():
    screen.fill((0, 0, 0))
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
