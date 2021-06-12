import sys
import pygame

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (600,400)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((200,133))

sand_img = pygame.image.load("resources\sand.png")
station_img = pygame.image.load("resources\station.png")

while True:

    count = round(WINDOW_SIZE[0] / sand_img.get_width())
    x = 0
    while x < count:
        y = 0
        while y < count:
            display.blit(sand_img, (x * sand_img.get_width(), y * sand_img.get_height()))
            y += 1
        x += 1
    display.blit(station_img, (50,30))
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)