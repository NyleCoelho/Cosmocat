from code.Const import ENTITY_SPEED, WIN_WIDTH, ENTITY_SHOT_DELAY, WIN_HEIGHT
from code.Entity import Entity
from code.EnemyShot import EnemyShot
import pygame
import random
import math
class Enemy(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/Boom.wav')
        self.killed_by_player = False
        self.velocity_x = -ENTITY_SPEED[self.name]  # continua indo pra esquerda
        self.wave_offset = random.uniform(0, math.pi * 2)  # cada inimigo começa com uma fase diferente
        self.t = 0  # tempo interno para o zigue-zague


    def move(self):
        self.rect.x += self.velocity_x  # continua indo pra esquerda
        
        self.t += 0.1  # avança no tempo da onda
        wave_amplitude = 50  # quanto ele "voa" pra cima e pra baixo
        wave_speed = 0.03     # velocidade da oscilação

        # Movimento vertical baseado em seno
        self.rect.y += math.sin(self.t + self.wave_offset) * wave_speed * wave_amplitude

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
