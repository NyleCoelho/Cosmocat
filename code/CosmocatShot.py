from code.Const import ENTITY_SPEED
from code.Entity import Entity

class CosmocatShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False, custom_scale=(40, 20))  # tamanho pequeno

    def move(self):
        self.rect.centerx += ENTITY_SPEED[self.name]


