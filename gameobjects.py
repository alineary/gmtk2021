import pygame
import drag_n_drop
import utils


def drive_to_target(target, current_pos, speed):
    direction_x = target.x - current_pos.x
    direction_y = target.y - current_pos.y
    direction = pygame.Vector2(direction_x, direction_y)
    if direction.length() < speed:
        return target
    else:
        return current_pos + pygame.Vector2.normalize(direction) * speed


# TODO: Wagons are only allowed to be added when the Locomotive is at it's waiting point

class Train(pygame.sprite.Sprite):
    def __init__(self, track, image, cooldown=0):
        super().__init__()
        self.track = track
        self.image = image
        self.rect = self.image.get_rect()
        self.timer = utils.Timer(cooldown)
        self.speed = 5

    def update(self):
        self.timer.update()
        # TODO: If NOT waiting position of track is current position
        if self.track is not self.rect:
            next_pos = drive_to_target(self.track, self.rect, self.speed)
            self.rect = next_pos

    def departure(self, cooldown):
        if not self.timer.done:
            return

        # Todo: track.getWagons, implement it properly once main is merged
        for wagon in []:
            wagon.toggle_draggable(False)

        self.timer = utils.Timer(cooldown)


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.wagon_data = wagon_data
        self.target = None
        self.position = position
        self.rect.center = position
        self.speed = 5

    def update(self):
        super().update()
        if self.target is not None:
            direction = self.target.xy - self.position.xy
            if direction.length() < 1:
                self.target = None
            else:
                self.position += pygame.Vector2.normalize(direction) * self.speed
                self.rect.center = self.position

    def set_target(self, target):
        self.target = target
