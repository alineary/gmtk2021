import sys
import pygame
import os
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Visualization')

WINDOW_SIZE = (1280, 720)

SIDETRACK = 15

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((320, 180))
small_things = pygame.Surface((640, 360))
background = pygame.Surface((1280, 720))

sand_img = pygame.image.load(os.path.join('resources', 'sand.png'))
station_img = pygame.image.load(os.path.join('resources', 'station.png'))
cactus_1 = pygame.image.load(os.path.join('resources', 'cactus_1.png'))
cactus_2 = pygame.image.load(os.path.join('resources', 'cactus_2.png'))
cactus_3 = pygame.image.load(os.path.join('resources', 'cactus_3.png'))
track_img = pygame.image.load(os.path.join('resources', 'tracks.png'))
bumper_img = pygame.image.load(os.path.join('resources', 'bumper.png'))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    track_count = SIDETRACK
    i = 0
    while i < track_count:
        small_things.blit(track_img, (i * track_img.get_width(), 125))
        i += 1
    small_things.blit(bumper_img, (i * track_img.get_width(), 125))
    count = round(screen.get_width() / sand_img.get_width())
    x = 0
    while x < count:
        y = 0
        while y < count:
            small_things.blit(track_img, (x * track_img.get_width(), 190))
            small_things.blit(track_img, (x * track_img.get_width(), 255))
            background.blit(sand_img, (x * sand_img.get_width(), y * sand_img.get_height()))
            y += 1
        x += 1
    display.blit(station_img, (250, 20))
    small_things.blit(cactus_1, (20, 50))
    small_things.blit(cactus_2, (30, 90))
    small_things.blit(cactus_3, (130, 90))
    small_things.blit(cactus_2, (70, 70))
    small_things.blit(cactus_3, (50, 30))
    small_things.blit(cactus_1, (160, 80))

    pygame.Surface.set_colorkey(display, (0, 0, 0))
    pygame.Surface.set_colorkey(small_things, (0, 0, 0))
    background.blit(pygame.transform.scale(small_things, [screen.get_width(), screen.get_height()]), (0, 0))
    background.blit(pygame.transform.scale(display, [screen.get_width(), screen.get_height()]), (0, 0))
    screen.blit(pygame.transform.scale(background, [screen.get_width(), screen.get_height()]), (0, 0))
    pygame.display.update()
    clock.tick(60)
