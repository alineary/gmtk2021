import pygame
import drag_n_drop
import os
import utils
import main
import traindata
import sound

WAGON_LENGTH = 90
WAGON_Y_OFFSET = -52
BUFFER_X_OFFSET = -52
SIZE = 50
ENGINE_WAIT_TIME = 10


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
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('resources', 'wagons', 'engine.png')),
                                            (SIZE * 2, SIZE * 2))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = track.position.x - self.rect.width
        self.rect.y = track.position.y + WAGON_Y_OFFSET
        self.timer = utils.Timer(0)
        self.speed = 6

    def update(self):
        self.listen_on_events()
        self.check_for_new_train_arrivals()
        self.move_train_if_not_waiting()

    def listen_on_events(self):
        for event in main.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos):
                    if self.timer.done and self.rect.x == self.track.engine_pos.x:
                        additional_wait_time = self.track.departure()
                        self.timer = utils.Timer(ENGINE_WAIT_TIME + additional_wait_time)

    def check_for_new_train_arrivals(self):
        if not self.timer.done:
            if self.timer.update():
                self.rect.x = self.track.position.x - self.rect.width

    def move_train_if_not_waiting(self):
        if self.timer.done:
            target = self.track.engine_pos
        else:
            target = pygame.Vector2(self.track.rect.width, self.rect.y)

        next_pos = drive_to_target_if_exists(target, self.rect, self.speed)
        if next_pos is None:
            self.track.is_available = True if self.timer.done else False
            return
        self.rect.x = next_pos.x
        self.rect.y = next_pos.y


class Wagon(drag_n_drop.DraggableSprite):
    def __init__(self, wagon_data, position, image):
        super().__init__(image, SIZE * 2)
        self.rect = self.image.get_rect()
        self.wagon_data = wagon_data
        self.target = None
        self.position = position
        self.rect.topleft = position
        self.speed = 6
        self.track = None
        self.finished = False

    # Todo: Update target when self updates in track pos
    def set_target(self, target):
        self.target = target

    def on_begin_drag(self, pos):
        super().on_begin_drag(pos)
        self.target = None

    def on_end_drag(self):
        super().on_end_drag()
        new_track = self.colliding_track()
        if new_track is None:
            self.rect.x = self.ghost_sprite.rect.x
            self.rect.y = self.ghost_sprite.rect.y
        else:
            if new_track is not self.track and not new_track.full() and new_track.is_available:
                self.track.wagons.remove(self)
                self.track.update_dependencies()
                self.track = new_track
                self.track.wagons.append(self)
                self.track.update_dependencies()

            self.rect.y = self.track.rect.y
            self.rect.x = self.track.next_wagon_x()

    def toggle_approval(self, approved):
        print(approved)
        if approved:
            self.image = pygame.transform.scale(self.wagon_data.sprite_approved, (SIZE * 2, SIZE * 2))
            return
        self.image = pygame.transform.scale(self.wagon_data.sprite, (SIZE * 2, SIZE * 2))

    def departure(self):
        self.target = pygame.Vector2(self.track.rect.width, self.rect.y)
        self.finished = True

    def update(self):
        super().update()
        future_pos = drive_to_target_if_exists(self.target, self.rect, self.speed)
        if future_pos is None:
            self.target = None
            if self.finished:
                self.track.wagons.remove(self)
                main.wagon_group.remove(self)
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
    def __init__(self, position, length, max_wagons, engine_rest_pos=None):
        super().__init__()
        self.sprite = pygame.image.load(os.path.join('resources', 'tracks.png'))
        self.buffer_sprite = pygame.image.load(os.path.join('resources', 'bumper.png'))
        self.position = position
        self.timer_offset = (10, 55)
        self.length = length
        self.wagons = []
        self.engine = None
        self.max_wagons = max_wagons
        self.with_buffer_stop = engine_rest_pos is None
        self.engine_pos = None
        # TODO: Make use of availability dragging is not possible, neither FROM nor TO this track
        self.is_available = True
        self.init_engine(engine_rest_pos)

        self.create_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def init_engine(self, engine_rest_pos):
        if engine_rest_pos is None:
            return
        self.engine_pos = pygame.Vector2(engine_rest_pos, self.position.y + WAGON_Y_OFFSET)
        self.engine = Engine(self)
        main.train_group.add(self.engine)
        return

    def departure(self):
        # Todo: The scoring comes here
        # Play horn Sound
        sound.horn_sound()
        for wagon in self.wagons:
            wagon.departure()
        self.is_available = False
        return traindata.calculate_train_stats(self.wagons)

    def add_wagon(self, wagon):
        if self.full() is False:
            self.wagons.append(wagon)
            return True
        return False

    def update_dependencies(self):
        i = 0
        for wagon in self.wagons:
            wagon_before = type(traindata.get_neighbour(i, self.wagons, -1))
            wagon_after = type(traindata.get_neighbour(i, self.wagons, 1))
            approved = traindata.wagon_approved(wagon, self.wagons, wagon_before, wagon_after)
            wagon.toggle_approval(approved)
            i += 1

    def create_image(self):
        image = pygame.Surface((self.length * self.sprite.get_width(), self.sprite.get_height()), pygame.SRCALPHA)
        for i in range(0, self.length):
            if i is self.length - 1 and self.with_buffer_stop is True:
                image.blit(self.buffer_sprite, [i * self.sprite.get_width(), 0])
            else:
                image.blit(self.sprite, [i * self.sprite.get_width(), 0])
        self.image = pygame.transform.scale(image, (SIZE * self.length, SIZE))

    def next_wagon_x(self):
        return self.wagon_x(len(self.wagons))

    # The tracks width (end of track) - the wagon lengths
    def wagon_x(self, position):
        end_pos = self.rect.width
        if self.engine is not None:
            end_pos = self.engine_pos.x
        end_pos += BUFFER_X_OFFSET if self.with_buffer_stop else 0

        return end_pos - (position + 1) * WAGON_LENGTH

    def full(self):
        return len(self.wagons) >= self.max_wagons

    def update(self):
        for i in range(0, len(self.wagons)):
            if self.wagons[i].target is None and self.wagons[i].clicked is False:
                self.wagons[i].rect.x = self.wagon_x(i)
                self.wagons[i].rect.y = self.rect.y + WAGON_Y_OFFSET

        if self.engine is not None:
            self.engine.update()
