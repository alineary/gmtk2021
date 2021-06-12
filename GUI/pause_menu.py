import pygame_menu
import pygame

from GUI.themes.wild_west import wild_west


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size

    def init_menu_surface(self):
        pause_menu = pygame_menu.Menu("Pause", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)

        pause_menu.add.label("Press ESC to continue")
        pause_menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT)
        pause_menu.add.label("[Insert Title] - a game by: \n M1st3rButt3r, eleanmai, RobinStarkgraff \n and alineary")

        return pause_menu
