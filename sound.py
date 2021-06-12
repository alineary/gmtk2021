import pygame
import os

pygame.init()

def horn_sound():
    horn = pygame.mixer.Sound(os.path.join('sounds', 'horn.mp3'))
    horn.set_volume(0.4)
    horn.play()

# sound.horn_sound() to play horn sound