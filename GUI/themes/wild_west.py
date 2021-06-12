import pygame_menu
from pygame_menu import Theme

font = pygame_menu.font.FONT_MUNRO
wild_west = Theme(widget_font=font,
                  title_font=font,
                  title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                  background_color=(78, 52, 37, 200),
                  widget_margin=(15, 20),
                  title_background_color=(157, 111, 68),
                  )
