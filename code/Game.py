import pygame
from code.Menu import Menu
from code.Menu import WIN_WIDTH, WIN_HEIGHT
from code.Menu import MENU_OPTION
from code.Level import Level
class Game:
    def __init__(self):
        pygame.init()  # Inicializa todos os módulos do pygame
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))  # Cria a janela do jogo

    def run(self):
        pygame.mixer_music.load('./assets/Songs/menu-song.mp3')  # Carrega música do menu
        pygame.mixer_music.play(-1)  # Toca em loop infinito

        while True:
            menu = Menu(self.window)  # Cria o menu
            menu_return = menu.run() 

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1]]:
                while True:
                    level = Level(self.window, 'Level1', menu_return)  # Inicia o nível
                    level_return = level.run() 

                    if level_return == 'RESTART':  # Reinicia o mesmo nível
                        continue
                    elif level_return == 'MENU':  # Volta pro menu
                        break
                    else:
                        break  
            elif menu_return == MENU_OPTION[3]:
                pygame.quit() 
                quit()  # Encerra o programa

