import pygame
import drag_n_drop
import os
import utils
import main

WAGON_LENGTH = 60
ENGINE_WAIT_TIME = 5


def drive_to_target_if_exists(target, current_pos, speed):
    if target is None:
        return None

    if target.x == current_pos.x and target.y == current_pos.y:
        return None

    direction_x = target.x - current_pos.x
    direction_y = target.y - current_pos.y
    direction = pygame.Vector2(direction_x, direction_y)
    if direction.length() < speed:
        return target
    else:
        current_pos.x += pygame.Vector2.normalize(direction).x * speed
        current_pos.y += pygame.Vector2.normalize(direction).y * speed
        return current_pos


class Engine(pygame.sprite.Sprite):
    def __init__(self, track):
        super().__init__()
        self.track = track
        self.image = pygame.image.load(os.path.join('resources', 'cactus_1.png'))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = track.position.x
        self.rect.y = track.position.y
        self.timer = utils.Timer(0)
        self.speed = 5

    def update(self):
        self.listen_on_events()
        self.check_for_new_train_arrivals()
        self.move_train_if_not_waiting()

    def move_train_if_not_waiting(self):
        # TODO: Target is not necessarily engine_pos
        next_pos = drive_to_target_if_exists(self.track.engine_pos, self.rect, self.speed)
        if next_pos is None:
            return
        self.rect.x = next_pos.x
        self.rect.y = next_pos.y

    def check_for_new_train_arrivals(self):
        if not self.timer.done:
            if self.timer.update():
                self.track.is_available = True
                self.image.set_alpha(255)
                # TODO: Make a proper start position for this
                self.rect.x = 0

    def listen_on_events(self):
        for event in main.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos):
                    self.departure()

    def departure(self):
        if not self.timer.done:
            return

        for wagon in self.track.wagons:
            wagon.toggle_draggable(False)
        self.track.is_available = False
        # TODO: Instead of invisible, let it drive off (+ wagons)
        self.image.set_alpha(drag_n_drop.INVISIBLE_ALPHA)
        self.timer = utils.Timer(ENGINE_WAIT_TIME)


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
        future_pos = drive_to_target_if_exists(self.target, self.rect, self.speed)
        if future_pos is None:
            self.target = None
            return

        self.rect.x = future_pos.x
        self.rect.y = future_pos.y


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
    def __init__(self, position, length, max_wagons, engine_pos=None):
        super().__init__()
        self.sprite = pygame.image.load(os.path.join('resources', 'tracks.png'))
        self.position = position
        self.length = length
        self.wagons = []
        self.engine = None
        self.max_wagons = max_wagons
        self.engine_pos = None
        # TODO: Make use of availability
        self.is_available = True
        self.init_engine(engine_pos)

        self.create_rect()
        self.create_image()

    def init_engine(self, engine_pos):
        if engine_pos is None:
            return None
        self.engine_pos = pygame.Vector2(engine_pos, self.position.y)
        self.engine = Engine(self)
        main.wagon_group.add(self.engine)
        return

    def add_wagon(self, wagon):
        if self.full() is False:
            self.wagons.append(wagon)
            return True
        return False

    def create_rect(self):
        rect = pygame.rect.Rect(self.position.x, self.position.y, self.length * self.sprite.get_width(),
                                self.sprite.get_height())
        self.rect = rect

    def create_image(self):
        image = pygame.Surface(self.rect.size)

        for i in range(0, self.length):
            image.blit(self.sprite, [i * self.sprite.get_width(), 0])
        self.image = image

    def next_wagon_x(self):
        return self.wagon_x(len(self.wagons))

    # The tracks width (end of track) - the wagon lengths
    def wagon_x(self, position):
        end_pos = self.rect.width
        if self.engine is not None:
            position += 1
            end_pos = self.engine_pos.x

        return end_pos - (position + 1) * WAGON_LENGTH

    def full(self):
        return len(self.wagons) >= self.max_wagons

    def update(self):
        for i in range(0, len(self.wagons)):
            if self.wagons[i].target is None and self.wagons[i].clicked is False:
                self.wagons[i].rect.x = self.wagon_x(i)
                self.wagons[i].rect.y = self.rect.y

        if self.engine is not None:
            self.engine.update()
