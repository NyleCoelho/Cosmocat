from code.Const import ENTITY_SPEED
from code.Entity import Entity
import random
import math
import pygame

class LifeSaver(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False, custom_scale=(50, 50))
        self.velocity_x = -ENTITY_SPEED[self.name]  # continua indo pra esquerda
        self.wave_offset = random.uniform(0, math.pi * 2)  
        self.t = 0  # tempo interno para o zigue-zague
        self.mask = pygame.mask.from_surface(self.surf)


    def move(self):
        self.rect.x += self.velocity_x  # continua indo pra esquerda
        
        self.t += 0.1  # avança no tempo da onda
        wave_amplitude = 50  # "voa" pra cima e pra baixo
        wave_speed = 0.03     # velocidade da oscilação

        # Movimento vertical baseado em seno
        self.rect.y += math.sin(self.t + self.wave_offset) * wave_speed * wave_amplitude

        if self.flash_timer > 0:
            self.flash_timer -= 1