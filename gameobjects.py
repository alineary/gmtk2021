import pygame
import drag_n_drop
import os

import utils

WAGON_LENGTH = 60


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image)
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


class Track(pygame.sprite.Sprite):
    def __init__(self, position, length, max_wagons):
        super().__init__()
        self.sprite = pygame.image.load(os.path.join('resources', 'tracks.png'))
        self.position = position
        self.length = length
        self.wagons = []
        self.max_wagons = max_wagons

        self.create_rect()
        self.create_image()

    def add_wagon(self, wagon):
        if self.full() is False:
            self.wagons.append(wagon)
            return True
        return False

    def create_rect(self):
        rect = pygame.rect.Rect(self.position.x, self.position.y, self.length * self.sprite.get_width(), self.sprite.get_height())
        self.rect = rect

    def create_image(self):
        image = pygame.Surface(self.rect.size)

        for i in range(0, self.length):
            image.blit(self.sprite, [i * self.sprite.get_width(), 0])
        self.image = image

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
                self.wagons[i].rect.y = self.rect.y
