import random
import pygame

from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Player import Player
from code.Enemy import Enemy
from code.Entity import Entity
from code.LifeSaver import LifeSaver
from code.PowerUp import PowerUp
from code.Boss import Boss
class EntityFactory:
    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        if entity_name == 'Level1Bg':
            return [
                Background(f'Level1Bg{i}', (x, 0))
                for i in range(2)
                for x in (0, WIN_WIDTH)
            ]
        elif entity_name == 'Cosmocat':
            return Player('Cosmocat', (15, WIN_HEIGHT // 2 - 70))
        elif entity_name == 'Auroracat':
            return Player('Auroracat', (15, WIN_HEIGHT // 2 + 70))
        elif entity_name == 'Enemy1':
            return Enemy('Enemy1', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
        elif entity_name == 'Enemy2':
            return Enemy('Enemy2', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
        elif entity_name == 'lifesaver':
            return LifeSaver('LifeSaver', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
        elif entity_name == 'PowerUp':
            return PowerUp('PowerUp', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
        elif entity_name == 'Boss':
            return Boss('Boss', (WIN_WIDTH + 50, random.randint(120, WIN_HEIGHT - 120)))
        else:
            return None