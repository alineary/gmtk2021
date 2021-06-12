import pygame


class Wagon(pygame.sprite.Sprite):
    def __init__(self, wagondata, position):
        super().__init__()
        self.image = pygame.Surface([60, 30])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.wagondata = wagondata
        self.target = None
        self.position = position
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
