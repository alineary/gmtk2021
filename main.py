import pygame
import sys
import wagon_spawner
import drag_n_drop
import gameobjects


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
    pygame.display.set_caption("Game with a Player")
    clock = pygame.time.Clock()
    running = True
    sprite_group = pygame.sprite.Group()

    # Wagon
    wagon_group = pygame.sprite.Group()

    draggable_sprites = [wagon]
    sprite_group.add(draggable_sprites)

def update():
    for wagon in wagon_group:
        wagon.update()
    wagon_spawner.update()
    drag_n_drop.update()



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
