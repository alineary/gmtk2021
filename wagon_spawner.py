import pygame
import traindata
import random
import main
import gameobjects
import utils

WAGON_TYPES = [traindata.FirstClass, traindata.SecondClass, traindata.OnboardBistro]
WAGON_SPAWN_COOL_DOWN = 10

timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)


def spawn_new_wagon():

    image = pygame.Surface([60, 30])
    image.fill((0, 0, 255))

    random_wagon = random.choice(WAGON_TYPES)()
    wagon = gameobjects.Wagon(random_wagon, pygame.Vector2(-100, 100), image)
    wagon.set_target(pygame.Vector2(400, 100))
    main.wagon_group.add(wagon)
    main.sprite_group.add(wagon.ghost_wagon)
    return wagon


def update():
    global timer
    timer.update()
    if timer.done:
        spawn_new_wagon()
        timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)

