import pygame
import sys

from GUI import pause_menu
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
    menu = PauseMenu((600, 400)).init_menu_surface()


# def update():
#     print("")


def draw():
    # screen.fill((255, 255, 255))
    if menu.is_enabled():
        print("draw screen")
        menu.mainloop(screen)
    pygame.display.update()


def game_loop():
    setup()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("pressed")
                    menu.disable()
                    # if event.type == pygame.KEYDOWN:
                    #    if event.key == pygame.K_ESCAPE:
                    #        pause_menu_and_surface.pause_menu.disable()
        # update()
        draw()
        clock.tick(60)
