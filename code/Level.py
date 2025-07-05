
import sys
import pygame
import random
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_PINK, SPAWN_LIFESAVER_EVENT, POWERUP_DURATION, SPAWN_POWERUP_EVENT
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.Enemy import Enemy
from code.LifeSaver import LifeSaver
class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Cosmocat'))
        self.timeout = 20000 #20 segundos
        if game_mode in MENU_OPTION[1]:
            self.entity_list.append(EntityFactory.get_entity('Auroracat'))
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(SPAWN_LIFESAVER_EVENT, 10000)  # aparece a cada 10 segundos
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(SPAWN_POWERUP_EVENT, POWERUP_DURATION)  # aparece a cada 10 segundos
    

    def run(self):
        pygame.mixer_music.load(f'./assets/Songs/{self.name}.mp3')
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            # Eventos
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


            # Atualiza e desenha entidades
            for ent in self.entity_list:
                if hasattr(ent, "draw"):
                    ent.draw(self.window)
                else:
                    self.window.blit(ent.surf, ent.rect)

                ent.move()

                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

            # Desenha barra de vida dos players no canto da tela
            for ent in self.entity_list:
                if isinstance(ent, Player):
                    ent.draw_health_hud(self.window)

            pygame.display.flip()

            # Verificações
            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

                        # Verificar se algum player morreu
            for entity in self.entity_list:
                if isinstance(entity, Player) and entity.health <= 0:
                    from code.GameOver import GameOver 
                    pygame.mixer_music.stop()
                    gameover_screen = GameOver(self.window)
                    pygame.time.delay(500)  # pausa de 0.5 segundo
                    option = gameover_screen.run()

                    if option == 'TENTAR NOVAMENTE':
                        return 'RESTART'
                    elif option == 'VOLTAR AO MENU':
                        return 'MENU'


            for entity in self.entity_list[:]:
                if isinstance(entity, LifeSaver):
                    for other in self.entity_list:
                        if isinstance(other, Player) and entity.rect.colliderect(other.rect):
                            from code.Const import ENTITY_HEALTH
                            max_health = ENTITY_HEALTH[other.name]
                            other.health = min(other.health + 30, max_health)
                            self.entity_list.remove(entity)
                            break


    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)