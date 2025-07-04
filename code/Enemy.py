from code.Const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.EnemyShot import EnemyShot
import pygame
class Enemy(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/Boom.wav')
        self.killed_by_player = False

    def move(self):       
        self.rect.centerx -= ENTITY_SPEED[self.name]
        if self.flash_timer > 0:
            self.flash_timer -= 1

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        
    def take_damage(self, amount):
        if self.health > 0:  # Só aplica se ele ainda estiver vivo
            self.health -= amount
            self.last_dmg = 'Something'  
            self.flash_timer = 100

            if self.health <= 0:  #  momento da morte
                self.death_sound.play()
