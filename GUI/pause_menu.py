import pygame_menu
import pygame
from GUI.themes.wild_west import wild_west


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.pause_menu = self.init_menu_surface()

    def init_menu_surface(self):
        pause_menu = pygame_menu.Menu("Pause", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)

        pause_menu.add.button('Continue', self.close)
        pause_menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT)

        return pause_menu

    def close(self):
        self.pause_menu.disable()
