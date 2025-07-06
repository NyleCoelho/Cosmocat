from code.Const import ENTITY_SPEED
from code.Entity import Entity
import pygame

class EnemyShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False)  # deixa o custom_scale de fora

        if name == 'BossShot':
            self.surf = pygame.image.load('./assets/BossShot.png').convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (80, 40))  # Tamanho maior para o boss
        else:
            self.surf = pygame.image.load(f'./assets/{name}.png').convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (30, 15))  # Tamanho padrão

        self.rect = self.surf.get_rect(center=position)  # atualiza o rect e a máscara depois de mudar a imagem
        self.mask = pygame.mask.from_surface(self.surf)

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

