import pygame
import utils
import os

import wagon_spawner
import main

SCORE_PER_WAGON = 200
TIME_PENALTY_PER_TRAIN = 5


def calculate_train_stats(train):
    score = 100  # 100 per default for the engine
    time_penalty = 0

    i = 0

    # Count how many wagons there are of each type
    #

    for wagon in train:
        wagon_before = type(get_neighbour(i, train, -1))
        wagon_after = type(get_neighbour(i, train, 1))
        approved = wagon_approved(wagon, train, wagon_before, wagon_after)
        # Grant score when train caused no delay
        if approved:
            score += SCORE_PER_WAGON
        else:
            time_penalty += 1

        i += 1

    main.score += score
    main.end_screen_parent.update_score()

    return time_penalty * TIME_PENALTY_PER_TRAIN


def wagon_approved(wagon, train, wagon_before=None, wagon_after=None):
    wagon = wagon.wagon_data

    wagons_per_class = [0, 0, 0, 0, 0, 0]
    for wagon_for_class in train:
        wagons_per_class[wagon_class_pos(type(wagon_for_class.wagon_data))] += 1

    if type(wagon) == Coal and wagon_before in wagon_spawner.WAGON_TYPES:
        return False

    if wagon.neighbour_blacklist and (wagon_before in wagon.neighbour_blacklist or wagon_after in wagon.neighbour_blacklist):
        return False

    if wagon.neighbour_req and wagon_before not in wagon.neighbour_req and wagon_after not in wagon.neighbour_req:
        return False

    for req_wagon_class in wagon.exact_train_req:
        if wagons_per_class[wagon_class_pos(req_wagon_class)] != wagon.req_amount and wagons_per_class[
            wagon_class_pos(req_wagon_class)] != 0:
            return False

    for req_wagon_class in wagon.min_train_req:
        if wagons_per_class[wagon_class_pos(req_wagon_class)] < wagon.req_amount:
            return False

    for req_wagon_class in wagon.max_train_req:
        if wagons_per_class[wagon_class_pos(req_wagon_class)] > wagon.req_amount:
            return False

    return True


def wagon_class_pos(wagon_class):
    wagon_class_pos = None

    if FirstClass is wagon_class:
        wagon_class_pos = 0
    elif SecondClass is wagon_class:
        wagon_class_pos = 1
    elif OnboardBistro is wagon_class:
        wagon_class_pos = 2
    elif Mail is wagon_class:
        wagon_class_pos = 3
    elif AnimalWagon is wagon_class:
        wagon_class_pos = 4
    elif Coal is wagon_class:
        wagon_class_pos = 5

    return wagon_class_pos


def get_neighbour(wagon_index, train, offset):
    neighbour_index = wagon_index + offset
    neighbour = None
    if utils.is_in_range(neighbour_index, 0, len(train) - 1):
        neighbour = train[neighbour_index].wagon_data

    return neighbour


class FirstClass:
    def __init__(self):
        self.exact_train_req = []
        self.min_train_req = []
        self.max_train_req = []
        self.neighbour_req = [FirstClass, OnboardBistro]
        self.neighbour_blacklist = []
        self.is_first_train = False
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'first_class.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'first_class_green.png'))


class SecondClass:
    def __init__(self):
        self.exact_train_req = [SecondClass]
        self.min_train_req = []
        self.max_train_req = []
        self.neighbour_req = []
        self.neighbour_blacklist = []
        self.is_first_train = False
        self.req_amount = 3
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'second_class.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'second_class_green.png'))


class OnboardBistro:
    def __init__(self):
        self.exact_train_req = []
        self.min_train_req = []
        self.max_train_req = [OnboardBistro]
        self.neighbour_req = []
        self.neighbour_blacklist = []
        self.is_first_train = False
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'bistro.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'bistro_green.png'))


class Mail:
    def __init__(self):
        self.exact_train_req = []
        self.min_train_req = [FirstClass, OnboardBistro, SecondClass]
        self.max_train_req = []
        self.neighbour_req = []
        self.neighbour_blacklist = []
        self.is_first_train = False
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'mail.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'mail_green.png'))

class AnimalWagon:
    def __init__(self):
        self.exact_train_req = []
        self.min_train_req = []
        self.max_train_req = []
        self.neighbour_req = []
        self.neighbour_blacklist = [FirstClass, SecondClass]
        self.is_first_train = False
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'animal_wagon.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'animal_wagon_approved.png'))

class Coal:
    def __init__(self):
        self.exact_train_req = []
        self.min_train_req = []
        self.max_train_req = []
        self.neighbour_req = []
        self.neighbour_blacklist = []
        self.is_first_train = True
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'coal.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'coal_approved.png'))