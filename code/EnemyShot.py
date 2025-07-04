from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.Entity import Entity

class EnemyShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False, custom_scale=(50, 20))  # mesmo aqui

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]
