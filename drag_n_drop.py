import pygame
import main
import copy

INVISIBLE_ALPHA = 0
GHOST_IMAGE_ALPHA = 100


class DraggableSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.ghost_wagon = GhostSprite(copy.copy(image))
        self.clicked = False
        self.clickOffset = pygame.Vector2()
        self.clickOffset.xy = 0, 0

    def update(self):
        self.listen_to_events()
        self.move_sprite()

    def move_sprite(self):
        if self.clicked:
            pos = pygame.mouse.get_pos()
            new_pos_x = pos[0] - self.clickOffset.x
            new_pos_y = pos[1] - self.clickOffset.y
            self.rect.x = new_pos_x
            self.rect.y = new_pos_y

    def listen_to_events(self):
        for event in main.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos):
                    self.clicked = True
                    self.clickOffset.x = pos[0] - self.rect.x
                    self.clickOffset.y = pos[1] - self.rect.y
                    self.ghost_wagon.image.set_alpha(GHOST_IMAGE_ALPHA)
                    self.ghost_wagon.rect = copy.copy(self.rect)

            if event.type == pygame.MOUSEBUTTONUP and self.clicked:
                self.clicked = False
                self.ghost_wagon.image.set_alpha(INVISIBLE_ALPHA)
                print(self.ghost_wagon.rect.y)
                print(self.rect.y)
                self.rect.x = self.ghost_wagon.rect.x
                self.rect.y = self.ghost_wagon.rect.y


class GhostSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.image.convert_alpha()
        self.image.set_alpha(INVISIBLE_ALPHA)
        self.rect = self.image.get_rect()
