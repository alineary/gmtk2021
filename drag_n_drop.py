import pygame
import main


class DraggableSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.clicked = False
        self.clickOffset = pygame.Vector2()
        self.clickOffset.xy = 0, 0


def update():
    for sprite in main.draggable_sprites:
        listen_to_events(sprite)
        if sprite.clicked:
            pos = pygame.mouse.get_pos()
            sprite.rect.x = pos[0] - sprite.clickOffset.x
            sprite.rect.y = pos[1] - sprite.clickOffset.y


def listen_to_events(sprite):
    for event in main.events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if sprite.rect.collidepoint(pos):
                sprite.clicked = True
                sprite.clickOffset.x = pos[0] - sprite.rect.x
                sprite.clickOffset.y = pos[1] - sprite.rect.y

        if event.type == pygame.MOUSEBUTTONUP:
            sprite.clicked = False
