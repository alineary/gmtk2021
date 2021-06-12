import pygame
import sys
import gameobjects


def setup():
    global clock
    global running
    global screen
    global wagon
    global wagon_group
    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True

    # Wagon
    wagon = gameobjects.Wagon(None, pygame.Vector2(200, 0))
    wagon.set_target(pygame.Vector2(200, 200))
    wagon_group = pygame.sprite.Group()
    wagon_group.add(wagon)


def update():
    wagon.update()


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
