import pygame_menu
from db_utils import db_operations
from GUI.themes.wild_west import wild_west
import main


class EndMenu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.input = None
        self.submit = None
        self.submitted = False
        self.menu = self.init_menu_surface()

    def init_menu_surface(self):
        menu = pygame_menu.Menu("", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)

        menu.add.label('Score: 22', font_size=30, font_color=(255, 255, 255))
        menu.add.label('The incoming track was too full', font_size=20, font_color=(255, 255, 255))
        self.input = menu.add.text_input("Name: ", maxchar=15, font_color=(229, 204, 175))
        self.submit = menu.add.button("Submit", self.submit_score, background_color=(101, 66, 41), font_color=(229, 204, 175))
        menu.add.button('Restart', self.restart, background_color=(101, 66, 41), font_color=(229, 204, 175))
        menu.add.button('Main Menu', self.to_main_menu, background_color=(101, 66, 41), font_color=(229, 204, 175))

        return menu

    def reset_menu(self):
        self.submitted = False
        self.submit.set_title("Submit")

    def restart(self):
        self.reset_menu()
        main.reset()
        self.menu.disable()

    def to_main_menu(self):
        self.reset_menu()
        main.reset()
        main.main_menu.enable()
        self.menu.disable()

    def submit_score(self):
        if self.submitted:
            return
        name = self.input.get_value()
        score = 22
        db_operations.add_new_score(name, score)
        self.submit.set_title("Submitted")
        self.submitted = True


class PauseMenu:
    def __init__(self, window_size):
        self.window_size = window_size
        self.pause_menu = self.init_menu_surface()

    def init_menu_surface(self):
        pause_menu = pygame_menu.Menu("", self.window_size[0], self.window_size[1], center_content=True,
                                      theme=wild_west)
        highscores = db_operations.get_top_five()

        pause_menu.add.image("resources/wildwagons_large.png")
        # TODO: Move to botton-left corner
        # pause_menu.add.label('A game created by M1st3rButt3r, eleanmai, RobinStarkgraff and alineary', font_size=15, font_color=(255, 255, 255))
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