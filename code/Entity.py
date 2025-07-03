from abc import ABC, abstractmethod
import pygame.image
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_DAMAGE, ENTITY_HEALTH, ENTITY_SCORE

class Entity(ABC): 
    def __init__(self, name: str, position: tuple, scale_to_screen=True, custom_scale=None):
        self.name = name
        self.surf = pygame.image.load(f'./assets/Backgrounds/level1/{name}.png').convert_alpha()
        
        if scale_to_screen:
            self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        elif custom_scale:
            self.surf = pygame.transform.scale(self.surf, custom_scale)
        else:
            self.surf = pygame.transform.scale(self.surf, (150, 150))  

        self.rect = self.surf.get_rect(topleft=position)
        self.speed = 0

        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'


    @abstractmethod
    def move(self):
        pass
