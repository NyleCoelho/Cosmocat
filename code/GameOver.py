import os
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, GAMEOVER_OPTION, C_WHITE, C_RED
class GameOver:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/gameover.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.navigate_sound = pygame.mixer.Sound('./assets/Sound-Effects/menu-hover.wav')

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./assets/Songs/gameover.wav')
        pygame.mixer_music.play(1)  # Toca a música 1 vez

        while True:
            self.window.fill((0, 0, 0))
            self.window.blit(self.surf, self.rect)

            # Títulos
            title1_y = int(WIN_HEIGHT * 0.35)
            title2_y = title1_y + 80
            self.menu_text(100, "GAMER OVER", C_RED, (WIN_WIDTH // 2, title1_y))
            self.menu_text(30, "CATLAND ENTRARÁ EM RUÍNA SEM SUA PROTEÇÃO.", C_RED, (WIN_WIDTH // 2, title2_y))

            # Opções do menu
            options_start_y = WIN_HEIGHT // 1.8
            for i in range(len(GAMEOVER_OPTION)):
                option_y = options_start_y + 60 * i
                color = C_RED if i == menu_option else C_WHITE
                self.menu_text(50, GAMEOVER_OPTION[i], color, (WIN_WIDTH // 2, option_y))

            pygame.display.flip()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Navega para baixo
                        self.navigate_sound.play()
                        if menu_option < len(GAMEOVER_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_w:  # Navega para cima
                        self.navigate_sound.play()
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(GAMEOVER_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # Confirma opção
                        self.navigate_sound.play()
                        return GAMEOVER_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        font_path = './assets/fonts/title.ttf'
        text_font = pygame.font.Font(font_path, text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
