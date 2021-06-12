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

    random_wagon = random.choice(WAGON_TYPES)()
    wagon = gameobjects.Wagon(random_wagon, pygame.Vector2(-100, 100))
    wagon.set_target(pygame.Vector2(400, 100))
    main.wagon_group.add(wagon)
    main.draggable_sprites.append(wagon)
    # Append wagon to track
    return wagon


def update():
    global timer
    timer.update()
    if timer.done:
        spawn_new_wagon()
        timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)

