import pygame
import traindata
import random
import main
import gameobjects
import utils

WAGON_TYPES = [traindata.FirstClass, traindata.SecondClass, traindata.OnboardBistro, traindata.Mail]
WAGON_SPAWN_COOL_DOWN = 2
START_WAGON_SPAWN_COOLDOWN = 0

timer = utils.Timer(START_WAGON_SPAWN_COOLDOWN)


def spawn_new_wagon():
    if main.spawn_track.full():
        main.end_screen.enable()
        return

    random_wagon = random.choice(WAGON_TYPES)()
    wagon = gameobjects.Wagon(random_wagon,
                              pygame.Vector2(-100, main.spawn_track.position.y + gameobjects.WAGON_Y_OFFSET),
                              random_wagon.sprite)

    main.wagon_group.add(wagon)
    main.sprite_group.add(wagon.ghost_sprite)
    wagon.set_target(
        pygame.Vector2(main.spawn_track.next_wagon_x(), main.spawn_track.position.y + gameobjects.WAGON_Y_OFFSET))
    main.spawn_track.add_wagon(wagon)
    wagon.track = main.spawn_track
    return wagon


def update():
    global timer
    timer.update()
    if timer.done:
        spawn_new_wagon()
        timer = utils.Timer(WAGON_SPAWN_COOL_DOWN)
