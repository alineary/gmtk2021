import pygame
import pygame_menu


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size

    def init_menu_surface(self):
        surface = pygame.display.set_mode(self.window_size)
        pause_menu = pygame_menu.Menu("Pause", self.window_size[0], self.window_size[1], center_content=True)

        pause_menu.add.button('Continue', pygame_menu.events.CLOSE)
        pause_menu.add.button('Quit', pygame_menu.events.EXIT)

        return pause_menu, surface


def show_menu(pause_menu, surface):
    pause_menu.enable()
    if pause_menu.is_enabled():
        pause_menu.draw(surface)
        surface.fill('#A0522D')
    pygame.display.update()
