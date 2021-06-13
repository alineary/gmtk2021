import pygame
import traindata
import main
import gameobjects
import utils
from numpy.random import choice

WAGON_TYPES = [traindata.FirstClass, traindata.SecondClass, traindata.OnboardBistro, traindata.Mail]
WAGON_PROBABILITIES = [0.2, 0.5, 0.2, 0.1]
WAGON_SPAWN_COOL_DOWN = 4
MIN_WAGON_SPAWN_COOL_DOWN = 2
WAGON_SPAWN_COOL_DOWN_DECREASE_PER_WAGON = 0.05
START_WAGON_SPAWN_COOL_DOWN = 3

timer = utils.Timer(START_WAGON_SPAWN_COOL_DOWN)


def spawn_new_wagon():
    global WAGON_SPAWN_COOL_DOWN
    if main.spawn_track.full():
        main.end_screen.enable()
        return

    random_wagon = choice(WAGON_TYPES, 1, p=WAGON_PROBABILITIES, replace=False)[0]()
    print(random_wagon)
    wagon = gameobjects.Wagon(random_wagon,
                              pygame.Vector2(-100, main.spawn_track.position.y + gameobjects.WAGON_Y_OFFSET),
                              random_wagon.sprite)

    main.wagon_group.add(wagon)
    main.sprite_group.add(wagon.ghost_sprite)
    wagon.set_target(
        pygame.Vector2(main.spawn_track.next_wagon_x(), main.spawn_track.position.y + gameobjects.WAGON_Y_OFFSET))
    main.spawn_track.add_wagon(wagon)
    wagon.track = main.spawn_track
    print(WAGON_SPAWN_COOL_DOWN)
    WAGON_SPAWN_COOL_DOWN = utils.clamp(WAGON_SPAWN_COOL_DOWN - WAGON_SPAWN_COOL_DOWN_DECREASE_PER_WAGON, MIN_WAGON_SPAWN_COOL_DOWN, 10000)
    return wagon


def update():
    global timer
    timer.update()
    if timer.done:
        spawn_new_wagon()
        timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)
