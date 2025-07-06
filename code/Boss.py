from code.Enemy import Enemy
from code.Const import WIN_WIDTH, WIN_HEIGHT, ENTITY_SHOT_DELAY
import pygame
import random

class Boss(Enemy):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Redimensiona o sprite do boss
        self.surf = pygame.transform.scale(self.surf, (500, 480))
        self.rect = self.surf.get_rect(topleft=self.rect.topleft)
        self.death_sound = pygame.mixer.Sound('./assets/Sound-Effects/Boom.wav')
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.vertical_direction = 1
        self.float_speed = 2
        self.stop_x = WIN_WIDTH - 600  # posição final do boss
        self.damage_sound = pygame.mixer.Sound('./assets/Sound-Effects/Hit.wav')
        self.damage_sound.set_volume(3.5)  
        self.mask = pygame.mask.from_surface(self.surf)

    def move(self):
        if self.rect.x > self.stop_x:
            self.rect.x -= 2  # entra da direita até posição final
        else:
            # Flutuação vertical
            self.rect.y += self.float_speed * self.vertical_direction
            if self.rect.top <= 100:
                self.vertical_direction = 1
            elif self.rect.bottom >= WIN_HEIGHT - 100:
                self.vertical_direction = -1

            if self.flash_timer > 0:
                self.flash_timer -= 1

    def shoot(self):
        now = pygame.time.get_ticks()
        if not hasattr(self, 'last_shot'):
            self.last_shot = now
        if now - self.last_shot >= 1000:
            self.last_shot = now
            from code.EnemyShot import EnemyShot
            return EnemyShot('BossShot', self.rect.midleft)
        return None
    
    def take_damage(self, amount):
        if self.health > 0:  # Só aplica se ele ainda estiver vivo
            self.health -= amount
            self.last_dmg = 'Something'  
            self.flash_timer = 100
            self.damage_sound.play()

            if self.health <= 0:  #  momento da morte
                self.death_sound.play()

