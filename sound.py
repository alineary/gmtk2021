import pygame
import os

pygame.init()
def play_music():
    pygame.mixer.music.load(os.path.join('resources', 'sounds', 'music.mp3'))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

def horn_sound():
    horn = pygame.mixer.Sound(os.path.join('resources', 'sounds', 'horn.mp3'))
    horn.set_volume(0.4)
    horn.play()

# sound.horn_sound() to play horn sound
