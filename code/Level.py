import sys
import pygame
import random
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import C_WHITE, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, SPAWN_LIFESAVER_EVENT, POWERUP_DURATION, SPAWN_POWERUP_EVENT, WIN_WIDTH
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.Enemy import Enemy
from code.LifeSaver import LifeSaver
from code.Win import Win

class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))  # plano de fundo
        self.entity_list.append(EntityFactory.get_entity('Cosmocat'))  # jogador principal
        self.timeout = 170000  # tempo limite da fase
        self.start_time = pygame.time.get_ticks()
        self.timer_font = pygame.font.Font('./assets/fonts/title.ttf', 32)

        if game_mode in MENU_OPTION[1]:  # modo cooperativo
            self.entity_list.append(EntityFactory.get_entity('Auroracat'))

        # define timers para eventos recorrentes
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(SPAWN_LIFESAVER_EVENT, 10000)
        pygame.time.set_timer(SPAWN_POWERUP_EVENT, POWERUP_DURATION)

        self.boss_spawned = False

    def run(self):
        pygame.mixer_music.load(f'./assets/Songs/{self.name}.mp3')
        pygame.mixer_music.play(-1)  # toca em loop

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time

            # se o tempo acabar e o boss estiver vivo, Game Over
            if elapsed_time >= self.timeout:
                boss_alive = any(ent.name == 'Boss' for ent in self.entity_list)
                if boss_alive:
                    return 'GAMEOVER'

            # trata eventos do pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))
                if event.type == SPAWN_LIFESAVER_EVENT:
                    self.entity_list.append(EntityFactory.get_entity('lifesaver'))
                if event.type == SPAWN_POWERUP_EVENT:
                    self.entity_list.append(EntityFactory.get_entity('PowerUp'))

            # movimenta e desenha entidades
            for ent in self.entity_list:
                if hasattr(ent, "draw"):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

                ent.move()

                # dispara tiros se for player ou inimigo
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # desenha barra de vida dos jogadores
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    ent.draw_health_hud(self.window)

            # exibe cronômetro
            remaining_time = max(0, (self.timeout - elapsed_time) // 1000)
            self.level_text(f"Tempo restante: {remaining_time}s", C_WHITE, (WIN_WIDTH // 2, 40))
            pygame.display.flip()

            # verifica colisões e mortes
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

            # vitória se o boss for derrotado
            if self.boss_spawned:
                boss_still_alive = any(ent.name == 'Boss' for ent in self.entity_list)
                if not boss_still_alive:
                    pygame.mixer_music.stop()
                    win_screen = Win(self.window)
                    pygame.time.delay(500)
                    option = win_screen.run()
                    if option == 'JOGAR NOVAMENTE':
                        return 'RESTART'
                    elif option == 'VOLTAR AO MENU':
                        return 'MENU'

            # verifica se algum jogador morreu
            for entity in self.entity_list:
                if isinstance(entity, Player) and entity.health <= 0:
                    from code.GameOver import GameOver
                    pygame.mixer_music.stop()
                    gameover_screen = GameOver(self.window)
                    pygame.time.delay(500)
                    option = gameover_screen.run()
                    if option == 'TENTAR NOVAMENTE':
                        return 'RESTART'
                    elif option == 'VOLTAR AO MENU':
                        return 'MENU'

            # recuperação de vida ao colidir com lifesaver
            for entity in self.entity_list[:]:
                if isinstance(entity, LifeSaver):
                    for other in self.entity_list:
                        if isinstance(other, Player) and entity.rect.colliderect(other.rect):
                            from code.Const import ENTITY_HEALTH
                            max_health = ENTITY_HEALTH[other.name]
                            other.health = min(other.health + 30, max_health)
                            self.entity_list.remove(entity)
                            break

            # invoca o boss quando restam 60 segundos
            if remaining_time == 60 and not self.boss_spawned:
                self.entity_list.append(EntityFactory.get_entity('Boss'))
                self.boss_spawned = True

    def level_text(self, text: str, text_color: tuple, text_center_pos: tuple):
        # exibe texto no topo (ex: cronômetro)
        text_surf = self.timer_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
