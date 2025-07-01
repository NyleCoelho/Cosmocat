#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame.image
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import WIN_WIDTH, WIN_HEIGHT, C_GREEN, MENU_OPTION, C_WHITE, C_GREEN

class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./assets/Backgrounds/menu/blue-preview.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./assets/Songs/menu-song.mp3')
        pygame.mixer_music.play(-1)

        while True:
            # Limpa a tela (opcional)
            self.window.fill((0, 0, 0))
            
            # Desenha o fundo (se houver)
            self.window.blit(self.surf, self.rect)
            
            # ---- TÍTULO DO JOGO (Centralizado) ----
            title1_y = int(WIN_HEIGHT * 0.3)  # 30% da altura
            title2_y = title1_y + 80  # Subtítulo 50px abaixo
            self.menu_text(100, "COSMOCAT", C_GREEN, (WIN_WIDTH // 2, title1_y))
            self.menu_text(100, "Strike Mission", C_GREEN, (WIN_WIDTH // 2, title2_y))
            
            # ---- OPÇÕES DO MENU (Centralizadas) ----
            options_start_y = WIN_HEIGHT // 1.8  # Começa no meio exato
            for i in range(len(MENU_OPTION)):
                option_y = options_start_y + 60 * i  # Espaçamento de 40px
                color = C_GREEN if i == menu_option else C_WHITE
                self.menu_text(50, MENU_OPTION[i], color, (WIN_WIDTH // 2, option_y))
            
            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # end pygame
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:  # DOWN KEY
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                    if event.key == pygame.K_UP:  # UP KEY
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if event.key == pygame.K_RETURN:  # ENTER
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        font_path = ('./assets/fonts/title.ttf')
        text_font = pygame.font.Font(font_path, text_size)    
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
