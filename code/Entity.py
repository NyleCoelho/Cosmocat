from abc import ABC, abstractmethod
import pygame.image
from code.Const import WIN_WIDTH, WIN_HEIGHT

class Entity(ABC): 
    def __init__(self, name: str, position: tuple, scale_to_screen=True):
        self.name = name
        self.surf = pygame.image.load(f'./assets/Backgrounds/level1/{name}.png').convert_alpha()
        
        if scale_to_screen:
            self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        else:
            self.surf = pygame.transform.scale(self.surf, (95, 95))  

        self.rect = self.surf.get_rect(topleft=position)
        self.speed = 0

    @abstractmethod
    def move(self):
        pass
