import pygame

import drag_n_drop


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagondata, position):
        super().__init__()
        self.image = pygame.Surface([60, 30])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.wagondata = wagondata
        self.target = None
        self.position = position
        self.rect.center = position
        self.speed = 1

    def set_target(self, target):
        self.target = target

    def update(self):
        if self.target is not None:
            direction = self.target.xy - self.position.xy
            if direction.length() < 1:
                self.target = None
            else:
                self.position += pygame.Vector2.normalize(direction) * self.speed
                self.rect.center = self.position


class Track(pygame.sprite.Sprite):
    def __init__(self, position, length, direction):
        super().__init__()
        self.sprite = pygame.image.load('./resources/tracks.png')
        self.position = position
        self.length = length
        self.wagons = []
        self.direction = direction

        self.create_rect()
        self.create_image()

    def add_wagon(self, wagon):
        self.wagons.append(wagon)

    def create_rect(self):
        rect = pygame.rect.Rect(self.position.x, self.position.y, self.length * self.sprite.get_width(), self.sprite.get_height())
        self.rect = rect

    def create_image(self):
        image = pygame.Surface(self.rect.size)

        for i in range(0, self.length):
            image.blit(self.sprite, [i * self.sprite.get_width(), 0])
        self.image = image
