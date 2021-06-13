import pygame
import main
import copy

INVISIBLE_ALPHA = 0
GHOST_IMAGE_ALPHA = 100


class DraggableSprite(pygame.sprite.Sprite):
    def __init__(self, image, scale):
        super().__init__()
        self.image = pygame.transform.scale(image, (scale, scale))
        self.ghost_sprite = GhostSprite(pygame.transform.scale(copy.copy(image), (scale, scale)))
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
                    self.on_begin_drag(pos)

            if event.type == pygame.MOUSEBUTTONUP and self.clicked:
                self.on_end_drag()
    
    def on_begin_drag(self, pos):
        self.clicked = True
        self.clickOffset.x = pos[0] - self.rect.x
        self.clickOffset.y = pos[1] - self.rect.y
        self.ghost_sprite.image.set_alpha(GHOST_IMAGE_ALPHA)
        self.ghost_sprite.rect = copy.copy(self.rect)

    def on_end_drag(self):
        self.clicked = False
        self.ghost_sprite.image.set_alpha(INVISIBLE_ALPHA)

    def colliding_track(self):
        for track in main.track_group:
            if pygame.sprite.collide_rect(self, track):
                return track
        return None


class GhostSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.image.convert_alpha()
        self.image.set_alpha(INVISIBLE_ALPHA)
        self.rect = self.image.get_rect()
