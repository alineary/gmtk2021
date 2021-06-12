import pygame
import drag_n_drop


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.wagon_data = wagon_data
        self.target = None
        self.position = position
        self.rect.center = position
        self.speed = 5

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
        print(self.rect)
