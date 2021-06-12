import pygame
import sys
import drag_n_drop
import gameobjects


def setup():
    global screen
    global clock
    global running
    global screen
    global wagon
    global wagon_group
    global sprite_group
    global draggable_sprites

    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True
    sprite_group = pygame.sprite.Group()

    # Wagon
    wagon = gameobjects.Wagon(None, pygame.Vector2(200, 0))
    wagon.set_target(pygame.Vector2(200, 200))
    wagon_group = pygame.sprite.Group()
    wagon_group.add(wagon)

    draggable_sprites = [wagon]
    sprite_group.add(draggable_sprites)

def update():
    drag_n_drop.update()
    wagon.update()


def draw():
    screen.fill((0, 0, 0))
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
