from code.Const import ENTITY_SPEED
from code.Entity import Entity
import random
import math
import pygame
class LifeSaver(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False, custom_scale=(50, 50))  # define tamanho fixo
        self.velocity_x = -ENTITY_SPEED[self.name]  # movimento para a esquerda
        self.wave_offset = random.uniform(0, math.pi * 2)  # desfase da onda para variar o movimento senoidal
        self.t = 0  # tempo usado na equação senoidal
        self.mask = pygame.mask.from_surface(self.surf)  # máscara para colisão perfeita

    def move(self):
        self.rect.x += self.velocity_x  # movimento horizontal constante
        self.t += 0.1
        wave_amplitude = 50
        wave_speed = 0.03
        # movimento vertical de onda 
        self.rect.y += math.sin(self.t + self.wave_offset) * wave_speed * wave_amplitude