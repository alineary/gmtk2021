import pygame
import sys
import gameobjects


def setup():
    global screen
    global clock
    global running
    global screen
    global wagon
    global wagon1
    global wagon_group
    global draggable_sprites

    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Wild Wagons")
    clock = pygame.time.Clock()
    running = True

    # Wagon
    wagon_image = pygame.Surface([60, 30])
    wagon_image1 = pygame.Surface([60, 30])
    wagon_image.fill((0, 0, 255))
    wagon_image1.fill((0, 0, 255))

    wagon = gameobjects.Wagon(None, pygame.Vector2(200, 0), wagon_image)
    wagon1 = gameobjects.Wagon(None, pygame.Vector2(400, 0), wagon_image1)
    wagon.set_target(pygame.Vector2(200, 10))
    wagon1.set_target(pygame.Vector2(400, 10))
    wagon_group = pygame.sprite.Group()
    wagon_group.add(wagon)
    wagon_group.add(wagon.ghost_image)
    wagon_group.add(wagon1)
    wagon_group.add(wagon1.ghost_image)

    draggable_sprites = [wagon, wagon1]


def update():
    wagon.update()
    wagon1.update()


def draw():
    screen.fill((255, 255, 255))
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
