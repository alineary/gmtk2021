from datetime import datetime, timedelta
import main
import pygame.freetype
import pygame


def render_score(screen, score):
    pygame.font.init()
    myfont = pygame.freetype.Font("resources/PixelOperator.ttf", 50)
    myfont.render_to(screen, (60, 60), " Score: " + str(score) + " ", (78, 52, 37), (227, 192, 132))


delta_timer = datetime.now()


def clamp(num: int, min_value: int, max_value: int):
    return max(min(num, max_value), min_value)


def is_in_range(num, min, max):
    return min <= num <= max


def set_delta_time():
    global delta_time
    delta_time = datetime.now()


def get_delta_time():
    if main.menu_was_enabled:
        return timedelta()
    else:
        return datetime.now() - delta_time


class Timer:
    def __init__(self, countdown_time):
        self.countdown_time = timedelta(seconds=countdown_time)
        self.done = False

    def update(self):
        self.countdown_time = self.countdown_time - get_delta_time()
        self.done = self.countdown_time <= timedelta()
        return self.done
