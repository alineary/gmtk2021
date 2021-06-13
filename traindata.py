import pygame
import utils
import os

import main

SCORE_PER_WAGON = 100
TIME_PENALTY_PER_TRAIN = 5


def calculate_train_stats(train):
    score = 100  # 100 per default for the engine
    time_penalty = 0

    i = 0

    # Count how many wagons there are of each type
    #
    wagons_per_class = [0, 0, 0, 0]
    for wagon in train:
        wagons_per_class[wagon_class_pos(type(wagon.wagon_data))] += 1

    for wagon in train:
        wagon = wagon.wagon_data
        wagon_before = type(get_neighbour(i, train, -1))
        wagon_after = type(get_neighbour(i, train, 1))
        time_penalty_before = time_penalty

        if wagon.neighbour_req and wagon_before not in wagon.neighbour_req and wagon_after not in wagon.neighbour_req:
            time_penalty += 1

        for req_wagon_class in wagon.min_train_req:
            if wagons_per_class[wagon_class_pos(req_wagon_class)] < wagon.req_amount:
                time_penalty += 1
                break

        for req_wagon_class in wagon.max_train_req:
            if wagons_per_class[wagon_class_pos(req_wagon_class)] > wagon.req_amount:
                time_penalty += 1

        # Grant score when train caused no delay
        if time_penalty_before == time_penalty:
            score += SCORE_PER_WAGON

        i += 1

    main.score += score
    main.end_screen_parent.update_score()

    return time_penalty * TIME_PENALTY_PER_TRAIN


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

    return wagon_class_pos


def get_neighbour(wagon_index, train, offset):
    neighbour_index = wagon_index + offset
    neighbour = None
    if utils.is_in_range(neighbour_index, 0, len(train) - 1):
        wagon = train[neighbour_index]
        neighbour = train[neighbour_index].wagon_data

    return neighbour


class FirstClass:
    def __init__(self):
        self.min_train_req = []
        self.max_train_req = []
        self.neighbour_req = [FirstClass, OnboardBistro]
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'first_class.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'first_class_green.png'))


class SecondClass:
    def __init__(self):
        self.min_train_req = [SecondClass]
        self.max_train_req = []
        self.neighbour_req = []
        self.req_amount = 3
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'second_class.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'second_class_green.png'))


class OnboardBistro:
    def __init__(self):
        self.min_train_req = []
        self.max_train_req = [OnboardBistro]
        self.neighbour_req = []
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'bistro.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'bistro_green.png'))


class Mail:
    def __init__(self):
        self.min_train_req = [FirstClass, OnboardBistro, SecondClass]
        self.max_train_req = []
        self.neighbour_req = []
        self.req_amount = 1
        self.sprite = pygame.image.load(os.path.join('resources/wagons', 'mail.png'))
        self.sprite_approved = pygame.image.load(os.path.join('resources/approved', 'mail_green.png'))