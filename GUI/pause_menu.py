import pygame_menu
from db_utils import db_operations
from GUI.themes.wild_west import wild_west


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.pause_menu = self.init_menu_surface()

    def init_menu_surface(self):
        pause_menu = pygame_menu.Menu("Menu", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)
        highscores = db_operations.get_top_five()

        pause_menu.add.image("resources/wildwagons_large.png")
        # TODO: Move to botton-left corner
        # pause_menu.add.label('A game created by M1st3rButt3r, eleanmai, RobinStarkgraff and alineary', font_size=15, font_color=(0, 0, 0))
        pause_menu.add.button('Play', self.toggle, background_color=(101, 66, 41), font_color=(229, 204, 175))
        pause_menu.add.button('Quit', pygame_menu.events.PYGAME_QUIT, background_color=(101, 66, 41),
                              font_color=(229, 204, 175))
        pause_menu.add.label('Highscores:', font_color=(255, 255, 255))
        for i in range(len(highscores)):
            pause_menu.add.label(highscores[i][0] + ': ' + str(highscores[i][1]), font_size=20, font_color=(255, 255, 255))

        return pause_menu

    def toggle(self):
        if self.pause_menu.is_enabled():
            self.pause_menu.disable()
        else:
            self.pause_menu.enable()
