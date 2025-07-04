from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.CosmocatShot import CosmocatShot
import pygame

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position, scale_to_screen=False)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.shot_sound = pygame.mixer.Sound('./assets/Sound-Effects/Shoot.wav')
        self.shot_sound.set_volume(0.5)
        self.original_surf = self.surf.copy()

    def move(self):
        angle = 0  # padrão (reto)
        pressed_key = pygame.key.get_pressed()
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]  
            angle = -5
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name] 
            angle = 5      
        pass

        self.surf = pygame.transform.rotate(self.original_surf, angle)

        # Recalcula o rect para manter a posição após rotação
        self.rect = self.surf.get_rect(center=self.rect.center)

        if self.flash_timer > 0:
            self.flash_timer -= 1

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                self.shot_sound.play()
                return CosmocatShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

