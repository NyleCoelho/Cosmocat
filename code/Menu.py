import os
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_GREEN, MENU_OPTION, C_WHITE, C_GREEN
class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/menu-background.png').convert_alpha()  # fundo do menu
        self.rect = self.surf.get_rect(left=0, top=0)
        self.navigate_sound = pygame.mixer.Sound('./assets/Sound-Effects/menu-hover.wav')  # som da navegação

    def run(self):
        menu_option = 0  # índice da opção selecionada
        pygame.mixer_music.load('./assets/Songs/menu-song.mp3')  # música do menu
        pygame.mixer_music.play(-1)

        while True:
            self.window.fill((0, 0, 0))  # limpa a tela
            self.window.blit(self.surf, self.rect)  # desenha o fundo

            # desenha o título
            title1_y = int(WIN_HEIGHT * 0.3)
            title2_y = title1_y + 80
            self.menu_text(100, "COSMOCAT", C_GREEN, (WIN_WIDTH // 2, title1_y))
            self.menu_text(100, "Strike Mission", C_GREEN, (WIN_WIDTH // 2, title2_y))

            # desenha as opções do menu
            options_start_y = WIN_HEIGHT // 1.8
            for i in range(len(MENU_OPTION)):
                option_y = options_start_y + 60 * i
                color = C_GREEN if i == menu_option else C_WHITE  # destaca a opção selecionada
                self.menu_text(50, MENU_OPTION[i], color, (WIN_WIDTH // 2, option_y))

            pygame.display.flip()  # atualiza a tela

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # navega para baixo
                        self.navigate_sound.play()
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0  # volta para o topo
                    if event.key == pygame.K_w:  # navega para cima
                        self.navigate_sound.play()
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1  # vai para o final
                    if event.key == pygame.K_RETURN:  # seleciona a opção
                        self.navigate_sound.play()
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        font_path = './assets/fonts/title.ttf'
        text_font = pygame.font.Font(font_path, text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)  # renderiza texto na tela