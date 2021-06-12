import pygame
import sys

from GUI.pause_menu import PauseMenu


def setup():
    global clock
    global running
    global screen
    global menu
    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True
    menu = PauseMenu((600, 400)).pause_menu


# def update():
#     print("")


def draw():
    screen.fill((255, 255, 255))

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
                    menu.disable()
        # update()
        draw()
        clock.tick(60)
