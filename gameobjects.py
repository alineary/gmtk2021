import pygame

import drag_n_drop


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.wagon_data = wagon_data
        self.target = None
        self.position = position
        self.speed = 1

    def set_target(self, target):
        self.target = target

    def update(self):
        super().update()
        if self.target is not None:
            direction = self.target.xy - self.position.xy
            if direction.length() < 1:
                self.target = None
            else:
                self.position += pygame.Vector2.normalize(direction) * self.speed
                self.rect.center = self.position
