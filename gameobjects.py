import pygame
import drag_n_drop
import os

import utils

WAGON_LENGTH = 90
WAGON_Y_OFFSET = -52
SIZE = 50


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image, SIZE * 2)
        self.rect = self.image.get_rect()
        self.wagon_data = wagon_data
        self.target = None
        self.position = position
        self.rect.topleft = position
        self.speed = 5
        self.track = None

    def set_target(self, target):
        self.target = target

    def on_begin_drag(self, pos):
        super().on_begin_drag(pos)

    def on_end_drag(self):
        super().on_end_drag()
        new_track = self.colliding_track()
        if new_track is None:
            self.rect.x = self.ghost_sprite.rect.x
            self.rect.y = self.ghost_sprite.rect.y
        else:
            if new_track is not self.track and new_track.full() is False:
                self.track.wagons.remove(self)
                self.track = new_track
                self.track.wagons.append(self)

            self.rect.y = self.track.rect.y
            self.rect.x = self.track.next_wagon_x()

    def update(self):
        super().update()
        if self.target is not None:
            direction = self.target.xy - self.position.xy
            if direction.length() < 1:
                self.target = None
            else:
                self.position += pygame.Vector2.normalize(direction) * self.speed
                self.rect.topleft = self.position


class Background(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite
        self.create_rect()
        self.create_background()

    def create_rect(self):
        rect = pygame.Rect(0, 0, 1280, 720)
        self.rect = rect

    def create_background(self):
        image = pygame.Surface(self.rect.size)
        count = round(1280 / self.sprite.get_width())
        x = 0
        while x < count:
            y = 0
            while y < count:
                image.blit(self.sprite, (x * self.sprite.get_width(), y * self.sprite.get_height()))
                y += 1
            x += 1
        self.image = image


class Beauty(pygame.sprite.Sprite):
    def __init__(self, image, position, size):
        super().__init__()
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = position
                

class Track(pygame.sprite.Sprite):
    def __init__(self, position, length, max_wagons, with_buffer_stop):
        super().__init__()
        self.sprite = pygame.image.load(os.path.join('resources', 'tracks.png'))
        self.buffer_sprite = pygame.image.load(os.path.join('resources', 'bumper.png'))
        self.position = position
        self.length = length
        self.wagons = []
        self.max_wagons = max_wagons
        self.with_buffer_stop = with_buffer_stop

        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def add_wagon(self, wagon):
        if self.full() is False:
            self.wagons.append(wagon)
            return True
        return False

    def create_image(self):
        image = pygame.Surface((self.length * self.sprite.get_width(), self.sprite.get_height()), pygame.SRCALPHA)
        for i in range(0, self.length):
            if i is self.length - 1 and self.with_buffer_stop is True:
                image.blit(self.buffer_sprite, [i * self.sprite.get_width(), 0])
            else:
                image.blit(self.sprite, [i * self.sprite.get_width(), 0])
        self.image = pygame.transform.scale(image, (SIZE * self.length, SIZE))

    def next_wagon_x(self):
        x = self.wagon_x(len(self.wagons))
        return x

    def wagon_x(self, i):
        return self.rect.width - i * WAGON_LENGTH + self.position.x - WAGON_LENGTH

    def full(self):
        return len(self.wagons) >= self.max_wagons

    def update(self):
        for i in range(0, len(self.wagons)):
            if self.wagons[i].target is None and self.wagons[i].clicked is False:
                self.wagons[i].rect.x = self.wagon_x(i)
                self.wagons[i].rect.y = self.rect.y + WAGON_Y_OFFSET
