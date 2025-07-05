import pygame
from code.Menu import Menu
from code.Menu import WIN_WIDTH, WIN_HEIGHT
from code.Menu import MENU_OPTION
from code.Level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        pygame.mixer_music.load('./assets/Songs/menu-song.mp3')
        pygame.mixer_music.play(-1)

        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1]]:
                while True:
                    level = Level(self.window, 'Level1', menu_return)
                    level_return = level.run()

                    if level_return == 'RESTART':
                        continue  # reinicia o nível
                    elif level_return == 'MENU':
                        break  # volta pro menu principal
                    else:
                        break  # qualquer outro caso
            elif menu_return == MENU_OPTION[3]:
                pygame.quit()
                quit()
            else:
                pass
