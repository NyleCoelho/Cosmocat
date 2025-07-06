from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Player import Player
from code.Enemy import Enemy
from code.Entity import Entity
from code.LifeSaver import LifeSaver
from code.PowerUp import PowerUp
from code.Boss import Boss
import random
import pygame
class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'Level1Bg':
                list_bg = []
                for i in range(2):
                    list_bg.append(Background(f'Level1Bg{i}', (0,0)))
                    list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH,0)))
                return list_bg
            case 'Cosmocat':
                return Player('Cosmocat', (15, WIN_HEIGHT / 2 - 70))
            case 'Auroracat':
                return Player('Auroracat', (15, WIN_HEIGHT / 2 + 70))
            case 'Enemy1':
                return Enemy('Enemy1', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
            case 'Enemy2':
                return Enemy('Enemy2', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
            case 'lifesaver':
                return LifeSaver('LifeSaver', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
            case 'PowerUp':
                return PowerUp('PowerUp', (WIN_WIDTH + 10, random.randint(120, WIN_HEIGHT - 120)))
            case 'Boss':
                return Boss('Boss', (WIN_WIDTH + 50, random.randint(120, WIN_HEIGHT - 120)))

