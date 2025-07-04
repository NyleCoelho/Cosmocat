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
            self.surf = pygame.transform.scale(self.surf, (120, 100))  

        self.rect = self.surf.get_rect(topleft=position)
        self.speed = 0

        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'
        self.flash_timer = 0 
        self.damage_sound = pygame.mixer.Sound('./assets/Sound-Effects/Hit.wav')
        self.damage_sound.set_volume(1.5)  # Ajusta volume se quiser


    @abstractmethod
    def move(self):
        pass

    def take_damage(self, amount):
        self.health -= amount
        self.last_dmg = 'Something'
        self.flash_timer = 100  
        self.damage_sound.play()

    def draw(self, screen):
        if self.flash_timer > 0:
            flash = self.surf.copy()

            # Criar uma cópia da alpha (máscara de transparência)
            alpha_mask = pygame.mask.from_surface(flash)
            mask_surface = alpha_mask.to_surface(setcolor=(151, 0, 40, 100), unsetcolor=(0, 0, 0, 0))
            mask_surface = mask_surface.convert_alpha()

            # Aplica o vermelho SOMENTE nas áreas visíveis
            flash.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, self.rect.topleft)
        else:
            screen.blit(self.surf, self.rect.topleft)



