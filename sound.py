import pygame
import os

# pygame.init()
def play_music():
    pygame.mixer.music.load(os.path.join('resources', 'sounds', 'music.mp3'))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def horn_sound():
    horn = pygame.mixer.Sound(os.path.join('resources', 'sounds', 'hornsound2.mp3'))
    horn.set_volume(0.4)
    horn.play()
    
def putdown_sound():
    putdown = pygame.mixer.Sound(os.path.join('resources', 'sounds', 'putdown.mp3'))
    putdown.set_volume(0.4)
    putdown.play()
    
def pickup_sound():
    pickup = pygame.mixer.Sound(os.path.join('resources', 'sounds', 'pickup.mp3'))
    pickup.set_volume(0.4)
    pickup.play()



# sound.horn_sound() to play horn sound
