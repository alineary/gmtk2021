import pygame_menu
import pygame
from GUI.themes.wild_west import wild_west


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.pause_menu = self.init_menu_surface()

    def init_menu_surface(self):
        pause_menu = pygame_menu.Menu("Menu", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)

        pause_menu.add.button('Play', self.close, background_color=(101, 66, 41), font_color=(229, 204, 175))
        pause_menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT, background_color=(101, 66, 41),
                              font_color=(229, 204, 175))
        pause_menu.add.image("resources/station.png")  # temporary
        pause_menu.add.label('A game created by: M1st3rButt3r, eleanmai, RobinStarkgraff and alineary', font_size=15)

        return pause_menu

    def close(self):
        self.pause_menu.disable()
