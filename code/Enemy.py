from code.Const import ENTITY_SPEED,ENTITY_SHOT_DELAY
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
        self.velocity_x = -ENTITY_SPEED[self.name]  
        self.wave_offset = random.uniform(0, math.pi * 2) 
        self.t = 0  # Contador para o movimento de onda

    def move(self):  # Move o inimigo horizontalmente para a esquerda e aplica movimento de onda
        self.rect.x += self.velocity_x  
        self.t += 0.1 
        wave_amplitude = 50 
        wave_speed = 0.03 
        self.rect.y += math.sin(self.t + self.wave_offset) * wave_speed * wave_amplitude
        if self.flash_timer > 0:
            self.flash_timer -= 1  

    def shoot(self): # Dispara um tiro após o delay chegar a zero e reinicia o contador de delay
        self.shot_delay -= 1  
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name] 
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx -60, self.rect.centery +30))  
        
    def take_damage(self, amount): # Aplica dano ao inimigo, inicia efeito visual de flash e toca som de morte se a vida acabar
        if self.health > 0:
            self.health -= amount  
            self.last_dmg = 'Something' 
            self.flash_timer = 100  
            if self.health <= 0:
                self.death_sound.play()
