import pygame
import traindata
import random
import main
import gameobjects
import utils

WAGON_TYPES = [traindata.FirstClass, traindata.SecondClass, traindata.OnboardBistro]
WAGON_SPAWN_COOL_DOWN = 2

timer = utils.Timer(0)


def spawn_new_wagon():
    if main.spawn_track.full():
        print("You lost da game")
        return

    image = pygame.Surface([60, 30])
    image.fill((random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)))

    random_wagon = random.choice(WAGON_TYPES)()
    wagon = gameobjects.Wagon(random_wagon, pygame.Vector2(-100, main.spawn_track.position.y), image)

    main.wagon_group.add(wagon)
    main.sprite_group.add(wagon.ghost_sprite)
    wagon.set_target(pygame.Vector2(main.spawn_track.next_wagon_x(), main.spawn_track.position.y))
    main.spawn_track.add_wagon(wagon)
    wagon.track = main.spawn_track
    return wagon


def update():
    global timer
    timer.update()
    if timer.done:
        spawn_new_wagon()
        timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)

